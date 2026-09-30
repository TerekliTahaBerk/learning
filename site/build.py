#!/usr/bin/env python3
"""Build the two reading collections into a static GitHub Pages site.

The Markdown files in spanish/ and ai-engineering/ remain the source of truth.
Requires Pandoc 2.17+ on PATH. No network access is needed during the build.
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BOOKS = {
    "spanish": {"name": "İspanyolca", "subtitle": "A1–B2 · Türkçe destekli kurs", "lang": "tr"},
    "ai-engineering": {"name": "AI Engineering", "subtitle": "Notlar ve uygulamalar", "lang": "en"},
}


def title_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^#\s+(.+)$", text)
    return re.sub(r"[`*_]", "", match.group(1)).strip() if match else path.stem.replace("-", " ").title()


def short_title(path: Path) -> str:
    title = title_of(path)
    return re.sub(r"^\d{1,2}\s*[·.:-]\s*", "", title)


def url_for(path: Path) -> str:
    return path.relative_to(ROOT).with_suffix(".html").as_posix()


def relative_url(current: str, target: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(current) or ".")


def link(current: str, target: str, label: str, css: str = "", current_page: bool = False) -> str:
    active = ' aria-current="page"' if current_page else ""
    return f'<a class="{css}" href="{html.escape(relative_url(current, target), quote=True)}"{active}>{html.escape(label)}</a>'


def markdown_to_html(path: Path) -> str:
    result = subprocess.run(
        ["pandoc", "--from=gfm+raw_html", "--to=html5", "--wrap=none", "--no-highlight"],
        input=path.read_text(encoding="utf-8"), text=True, capture_output=True, check=True,
    )
    body = result.stdout
    # Pandoc preserves Markdown links; generated pages use the same directory tree.
    body = re.sub(r'(?P<pre>href="[^"#?]+)\.md(?P<post>(?:#[^"]*)?")',
                  lambda m: m.group("pre") + ".html" + m.group("post"), body)
    return body


def book_pages(book: str) -> list[Path]:
    root = ROOT / book
    pages = list(root.rglob("*.md"))
    if book == "spanish":
        def key(path: Path):
            parts = path.relative_to(root).parts
            if parts == ("README.md",): return (0, "", 0, "")
            if parts[0] == "levels":
                level = parts[1]
                if len(parts) == 3 and parts[2] == "README.md": return (1, level, 0, "")
                group = parts[2]
                if re.match(r"^\d\d-", group): return (1, level, 1, group, parts[3:])
                if group == "review": return (1, level, 2, parts[3:])
                if group == "assessment": return (1, level, 3, parts[3:])
                return (1, level, 4, parts)
            if parts[0] == "reference": return (2, "", 0, parts)
            return (3, "", 0, parts)
        return sorted(pages, key=key)
    def key(path: Path):
        rel = path.relative_to(root).parts
        return (0 if rel == ("README.md",) else 1, rel)
    return sorted(pages, key=key)


def side_nav(book: str, current: str) -> str:
    home = f"{book}/README.html"
    out = ['<nav class="book-nav" aria-label="Kitap içindekiler">',
           link(current, home, "Kitaba genel bakış", "nav-home", current == home)]
    if book == "spanish":
        for level in ("a1", "a2", "b1", "b2"):
            folder = ROOT / book / "levels" / level
            level_page = f"{book}/levels/{level}/README.html"
            open_level = f"/{level}/" in f"/{current}/"
            out.append(f'<details class="nav-group" {"open" if open_level else ""}><summary>{level.upper()} <span>{len(list(folder.glob("[0-9][0-9]-*")))} modül</span></summary>')
            out.append(link(current, level_page, "Düzey haritası", "nav-sub", current == level_page))
            for module in sorted(folder.glob("[0-9][0-9]-*")):
                if not module.is_dir(): continue
                first = module / "01-konu.md"
                target = url_for(first)
                module_open = module.name in current
                out.append(f'<details class="nav-module" {"open" if module_open else ""}><summary>{html.escape(module.name[:2])}. {html.escape(short_title(first))}</summary>')
                for lesson in sorted(module.glob("[0-9][0-9]-*.md")):
                    dest = url_for(lesson)
                    label = {"01":"Konu", "02":"Dilbilgisi", "03":"Kelime", "04":"Okuma ve dinleme", "05":"Konuşma ve yazma", "06":"Alıştırmalar", "07":"Yanıtlar ve tekrar"}.get(lesson.name[:2], lesson.stem)
                    out.append(link(current, dest, label, "nav-lesson", current == dest))
                out.append("</details>")
            out.append(link(current, f"{book}/levels/{level}/review/README.html", "Birikimli tekrar", "nav-sub", current == f"{book}/levels/{level}/review/README.html"))
            out.append(link(current, f"{book}/levels/{level}/assessment/README.html", "Değerlendirme", "nav-sub", current == f"{book}/levels/{level}/assessment/README.html"))
            out.append("</details>")
        out.append('<div class="nav-divider">Başvuru</div>')
        for path in sorted((ROOT / book / "reference").glob("*.md")):
            target = url_for(path)
            out.append(link(current, target, short_title(path), "nav-sub", current == target))
        for name in ("STUDY-SYSTEM", "ROADMAP", "PROGRESS", "SOURCES"):
            path = ROOT / book / f"{name}.md"
            out.append(link(current, url_for(path), short_title(path), "nav-sub", current == url_for(path)))
    else:
        root = ROOT / book
        education = root / "education"
        out.append('<div class="nav-divider">Eğitim</div>')
        out.append(link(current, url_for(education / "README.md"), "Eğitim haritası", "nav-sub", current == url_for(education / "README.md")))
        for course in sorted(p for p in education.iterdir() if p.is_dir()):
            overview = course / "README.md"
            out.append(f'<details class="nav-group" {"open" if course.name in current else ""}><summary>{html.escape(short_title(overview))}</summary>')
            out.append(link(current, url_for(overview), "Genel bakış", "nav-sub", current == url_for(overview)))
            for note in sorted((course / "notes").glob("*.md")):
                out.append(link(current, url_for(note), short_title(note), "nav-lesson", current == url_for(note)))
            out.append("</details>")
    out.append("</nav>")
    return "\n".join(out)


def page_shell(current: str, book: str | None, title: str, body: str, previous: str | None,
               next_page: str | None, label_map: dict[str, str]) -> str:
    root_prefix = posixpath.relpath(".", posixpath.dirname(current) or ".")
    css = relative_url(current, "assets/style.css")
    refined_css = relative_url(current, "assets/refined.css")
    js = relative_url(current, "assets/app.js")
    search_data = relative_url(current, "assets/search.json")
    is_home = book is None
    nav = side_nav(book, current) if book else ""
    controls = f'''<a class="brand" href="{html.escape(relative_url(current, "index.html"))}">Learning<span class="brand-dot">.</span></a>
      <button class="mobile-menu icon-button" type="button" data-action="menu" aria-label="İçindekileri aç" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
      <div class="header-spacer"></div><button class="search-button" type="button" data-action="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.3"/><path d="m16 16 4.2 4.2"/></svg><span>Kitap içinde ara</span><kbd>⌘ K</kbd></button>
      <div class="book-switch"><a href="{html.escape(relative_url(current, "spanish/README.html"))}" class="{'selected' if book=='spanish' else ''}">İspanyolca</a><a href="{html.escape(relative_url(current, "ai-engineering/README.html"))}" class="{'selected' if book=='ai-engineering' else ''}">AI Engineering</a></div>
      <button class="icon-button theme-button" type="button" data-action="theme" aria-label="Görünümü değiştir"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14A8.5 8.5 0 0 1 10 3.5 8.5 8.5 0 1 0 20.5 14Z"/></svg></button>'''
    sidebar = f'''<aside class="sidebar" id="sidebar"><div class="sidebar-top"><span class="section-label">KİTAPLAR</span><a class="book-link {'current' if book=='spanish' else ''}" href="{html.escape(relative_url(current, 'spanish/README.html'))}"><span class="book-mark spanish-mark">ES</span><span><strong>İspanyolca</strong><small>A1–B2 · Türkçe destekli kurs</small></span></a><a class="book-link {'current' if book=='ai-engineering' else ''}" href="{html.escape(relative_url(current, 'ai-engineering/README.html'))}"><span class="book-mark ai-mark">AI</span><span><strong>AI Engineering</strong><small>Notlar ve uygulamalar</small></span></a></div><div class="sidebar-scroll"><span class="section-label">İÇİNDEKİLER</span>{nav if nav else '<p class="sidebar-hint">Okumak için bir kitap seç.</p>'}</div></aside>'''
    prev_next = ""
    if previous or next_page:
        prev_next = '<nav class="chapter-nav" aria-label="Sayfalar arası gezinme">'
        prev_next += link(current, previous, "← Önceki sayfa", "chapter-prev") if previous else '<span></span>'
        prev_next += link(current, next_page, "Sonraki sayfa →", "chapter-next") if next_page else '<span></span>'
        prev_next += '</nav>'
    rail = '' if is_home else '''<aside class="reading-rail"><div class="rail-block"><span class="rail-title">Okuma ilerlemesi</span><div class="progress-track"><span id="read-progress"></span></div><span class="progress-label" id="progress-label">%0</span><button class="mark-read" type="button" data-action="mark-read">Okudum olarak işaretle</button></div><div class="rail-block"><span class="rail-title">Bu sayfada</span><nav class="on-this-page" id="on-this-page"></nav></div></aside>'''
    body_class = "library-home" if is_home else "reader-page"
    lang = "tr" if book != "ai-engineering" else "en"
    breadcrumb = '' if is_home else f'<div class="breadcrumbs">{link(current, f"{book}/README.html", BOOKS[book]["name"])}<span>›</span><span>{html.escape(title)}</span></div>'
    icon = relative_url(current, "assets/favicon.svg")
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{html.escape(title)} · Learning</title><meta name="description" content="{html.escape(BOOKS[book]['subtitle'] if book else 'Dijital öğrenme kitaplığı')}"><link rel="icon" type="image/svg+xml" href="{html.escape(icon)}"><link rel="stylesheet" href="{html.escape(css)}"><link rel="stylesheet" href="{html.escape(refined_css)}"><script defer src="{html.escape(js)}"></script></head><body class="{body_class}" data-search="{html.escape(search_data)}" data-page="{html.escape(current)}" data-root="{html.escape(root_prefix)}"><div class="site-layout"><header class="topbar">{controls}</header>{sidebar}<main class="main-content" id="main"><div class="reading-wrap">{breadcrumb}<article class="prose" id="article">{body}</article>{prev_next}</div></main>{rail}</div><dialog class="search-dialog" id="search-dialog"><div class="search-inner"><div class="search-head"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.3"/><path d="m16 16 4.2 4.2"/></svg><input id="search-input" type="search" placeholder="Başlık veya içerikte ara…" aria-label="Kitaplarda ara" autocomplete="off"><button type="button" data-action="close-search" aria-label="Aramayı kapat">ESC</button></div><div class="search-results" id="search-results"><p>İspanyolca ve AI Engineering sayfalarında ara.</p></div></div></dialog><div class="mobile-shade" data-action="close-menu"></div></body></html>'''


def library_home() -> str:
    return '''<div class="home-intro"><p class="home-overline">KİŞİSEL KİTAPLIK <span>·</span> İKİ ÇALIŞMA ALANI</p><h1>Öğrenme alanım<span class="title-period">.</span></h1><p class="home-lead">Dersler, notlar ve tekrarlar bir arada. Kaldığın yerden okumaya devam et.</p></div><div class="shelf-heading"><span>KİTAPLAR</span><span>02 koleksiyon</span></div><div class="book-shelf"><a class="shelf-book shelf-spanish" href="spanish/README.html"><span class="shelf-number">01 <i></i> DİL ÖĞRENİMİ</span><span class="shelf-title">İspanyolca</span><span class="shelf-desc">Türkçe konuşanlar için A1’den B2’ye yapılandırılmış kurs.</span><span class="shelf-meta">A1–B2 <span>·</span> 34 modül <span>·</span> alıştırmalar</span><span class="shelf-arrow">Kitabı aç <b aria-hidden="true">→</b></span></a><a class="shelf-book shelf-ai" href="ai-engineering/README.html"><span class="shelf-number">02 <i></i> TEKNOLOJİ</span><span class="shelf-title">AI Engineering</span><span class="shelf-desc">API kullanımı ve prompt tasarımı üzerine notlar ve kaynaklar.</span><span class="shelf-meta">Kurs notları <span>·</span> örnekler <span>·</span> PDF</span><span class="shelf-arrow">Kitabı aç <b aria-hidden="true">→</b></span></a></div><p class="home-footnote">İçerik kaynakları <a href="https://github.com/TerekliTahaBerk/learning">GitHub deposunda</a> sürümlenir.</p>'''


def build(out: Path) -> None:
    if shutil.which("pandoc") is None:
        raise SystemExit("Pandoc is required. Install pandoc 2.17+ before building.")
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(SITE / "assets", out / "assets")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    pages = {book: book_pages(book) for book in BOOKS}
    all_pages = [p for seq in pages.values() for p in seq]
    labels = {url_for(p): short_title(p) for p in all_pages}
    search = []
    for book, seq in pages.items():
        for index, path in enumerate(seq):
            current = url_for(path)
            body = markdown_to_html(path)
            previous = url_for(seq[index-1]) if index else None
            next_page = url_for(seq[index+1]) if index+1 < len(seq) else None
            rendered = page_shell(current, book, title_of(path), body, previous, next_page, labels)
            target = out / current
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
            plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))
            search.append({"title": title_of(path), "book": BOOKS[book]["name"], "path": current, "text": html.unescape(plain)[:1500]})
    for pdf in ROOT.glob("ai-engineering/**/*.pdf"):
        dest = out / pdf.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf, dest)
    (out / "assets" / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (out / "index.html").write_text(page_shell("index.html", None, "Dijital kitaplık", library_home(), None, None, labels), encoding="utf-8")
    (out / "404.html").write_text(page_shell("404.html", None, "Sayfa bulunamadı", '<div class="home-intro"><h1>Bu sayfa bulunamadı.</h1><p class="home-lead">Kitaplığa dönüp okumaya devam edebilirsin.</p><p><a href="index.html">Kitaplığa dön →</a></p></div>', None, None, labels), encoding="utf-8")
    print(f"Built {len(all_pages)} reading pages and {sum(1 for _ in ROOT.glob('ai-engineering/**/*.pdf'))} PDFs in {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "site-dist")
    build(parser.parse_args().out.resolve())
