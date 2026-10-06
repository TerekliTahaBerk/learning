# Learning book site

The Markdown documents in `spanish/`, `ai-engineering/`, and `yds/` are the only content source. The static generator preserves their directory structure, rewrites local Markdown links to HTML, copies linked PDFs, and creates a search index.

Build locally with Pandoc 2.17+:

```bash
python3 site/build.py
python3 -m http.server 8765 --directory site-dist
```

Open `http://localhost:8765/`. The GitHub Pages workflow builds the same output on each content change and publishes the `site-dist` artifact. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions** once for this repository.

The deployed site has three independent book entrances: `/spanish/README.html`, `/ai-engineering/README.html`, and `/yds/README.html`. It uses relative asset and document URLs, so the same output works at a project Pages path or a custom domain.
