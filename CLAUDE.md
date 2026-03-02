# CLAUDE.md

## Project

vmargato.com — a personal blog built on a custom static site generator. No framework. No CMS. One Python script (`build.py`, ~1200 lines) that converts Markdown to HTML.

Live at **vmargato.com**, deployed via GitHub Pages.

## Commands

```bash
python build.py          # Build the site (output/ directory)
python build.py serve    # Build + local server on :8000
python build.py clean    # Remove output/
make test                # Run pytest
make lint                # Run ruff
```

After any content or template change, run `python build.py` and check `output/` before committing. The `output/` directory is gitignored — GitHub Pages serves from the main branch directly (build.py generates into output/, but deployment uses the repo root via a separate process or Pages config).

## Repository structure

```
posts/{en,pt}/*.md          Blog posts (bilingual, paired by filename slug)
pages/{en,pt}/*.md          Standalone pages (about)
templates/*.html            Mustache-like templates (base, post, page, index)
static/css/                 tufte.css (foundation) + custom.css (theme, layout)
static/js/                  theme.js, lang.js, toc.js
static/embeds/              Interactive D3.js visualizations (standalone HTML)
static/css/et-book/         ET Book typeface files
tests/                      pytest suite for build.py
build.py                    The entire build system
```

## Content conventions

- Every post and page lives in both `en/` and `pt/`. Filenames must match across languages for the bilingual toggle to work.
- Frontmatter is YAML-like between `---` fences. Required fields: `title`, `date` (YYYY-MM-DD), `excerpt`. Optional: `draft: true` (accessible by direct URL but hidden from index and feed).
- Tufte extensions in markdown: `{mn}margin note{/mn}`, `{sn}sidenote{/sn}`, `{nt}new thought{/nt}`.
- Raw HTML in markdown passes through untouched. Interactive embeds use `<div class="graph-embed">` with an iframe pointing to `static/embeds/`.
- Embed iframes use `?embed` query param to hide standalone chrome (theme toggle, instructions). Theme sync from parent page via `postMessage`.

## Writing style

- Direct, honest tone. No marketing language, no corporate jargon, no clichés.
- No em dashes. Use commas, periods, or parentheses instead.
- Follow each language's own capitalization conventions (EN and PT rules differ).
- EN and PT versions should be structurally equivalent (same paragraphs, same progression of ideas) but each must read as if natively written by an American or a Brazilian. Idiomaticity over literal accuracy.
- Margin notes over footnotes. The information is there if you want it, without forcing the reader to decide whether to interrupt their flow.

## Visual and design principles

- Tufte CSS: information density, minimize the superfluous, let the content speak.
- Grayscale palette with CSS variables for light/dark mode. No accent colors.
- Speed is non-negotiable. No unnecessary JavaScript. No external requests blocking rendering.
- ET Book typeface for body text, Source Code Pro for code.
- Interactive embeds (D3.js) should educate, not decorate. Each one should teach the reader something concrete.

## Technical patterns

- CSS theme: custom properties on `:root` (light) and `[data-theme="dark"]` (dark). `theme.js` handles toggle + localStorage persistence + system preference fallback.
- Sticky header uses `::before` pseudo-element with `-100vw` left/right offsets for full-viewport background without breaking the Tufte layout width.
- Table of contents appears as a fixed sidebar on screens >= 1440px. Uses IntersectionObserver for scroll tracking.
- Embeds are self-contained HTML files in `static/embeds/`. Each has its own CSS variables, D3.js from CDN, and embed/standalone dual mode.
- Template engine is simple string replacement: `{{variable}}`, `{{#key}}...{{/key}}` for conditionals/loops.

## Testing and quality

- `pytest` for build.py (frontmatter parsing, markdown conversion, Tufte extensions, template rendering, i18n).
- `ruff` for linting, `mypy` for type checking (strict mode).
- Python >= 3.10, single runtime dependency (`markdown>=3.4`).
