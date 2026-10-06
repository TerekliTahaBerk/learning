# Learning book site — Vercel

The Markdown documents in `spanish/`, `ai-engineering/`, and `yds/` are the content sources. The generator preserves their directory structure, rewrites local Markdown links to HTML, copies downloadable files, and creates the search index.

## Build and publish

Build locally with Python 3 and Pandoc 2.17+:

```bash
python3 site/build.py --out site-dist
```

**The current Vercel deployment serves the committed `site-dist/` output through `api/index.py`.** Include regenerated output in the same commit as content changes. Pushing `main` triggers the existing Vercel Git integration for the `learning` project. Changing Markdown alone does not refresh the served pages.

The GitHub Pages publishing workflow was removed; this private reader is deployed through Vercel.

## Reader entrances

- `/spanish/README.html`
- `/ai-engineering/README.html`
- `/yds/README.html`

YDS appears on the library home page, book switcher, sidebar and search. All 81 current YDS Markdown pages are generated, including the 47-day plan and the 332-unit vocabulary centre. Anki `.txt`, master JSON and the vocabulary maintenance script are copied alongside their links.

The existing server-side login protects book pages, search data and downloads. Deployment secrets are configured in Vercel; do not put them in the generated output. Relative URLs keep the same output usable under the current domain.

## Public static preview on your own computer

For layout checks only:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory site-dist
```

Open `http://127.0.0.1:8765/`. This local static preview does not implement the production login. To verify login behaviour, use the existing `api/index.py` server with disposable local test credentials.
