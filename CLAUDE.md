# CLAUDE.md

## Project

vmargato.com, a personal blog built on a custom static site generator. No framework. No CMS. One Python script (`build.py`, ~1150 lines) that converts Markdown to HTML.

Live at **vmargato.com**, deployed via GitHub Pages.

## Commands

```bash
make install-dev         # uv sync --extra dev (pinned by uv.lock)
uv run python build.py                  # Build the site (output/ directory)
uv run python build.py build --strict   # Build, failing on frontmatter warnings (what CI runs)
uv run python build.py serve            # Build + local server on :8000
uv run python build.py clean            # Remove output/
make test                               # Run pytest
make lint                               # Run ruff check + format check
make typecheck                          # Run mypy --strict
```

Dependencies live only in `pyproject.toml`; `uv.lock` pins them. Run tools through `uv run`. A failed build exits with status 1.

After any content or template change, run `uv run python build.py` and check `output/` before committing. The `output/` directory is gitignored. Deployment is GitHub Actions (`.github/workflows/`): a test job runs on every push and pull request (`uv sync --locked`, ruff check, ruff format --check, mypy on `build.py` and `tests`, pytest), and on pushes to `main` a deploy job then runs `build.py build --strict` and uploads `output/` to GitHub Pages.

## Repository structure

```
posts/{en,pt}/*.md          Blog posts (bilingual, paired by filename slug)
pages/{en,pt}/*.md          Standalone pages (about)
templates/*.html            Mustache-like templates (base, post, page, index)
static/css/                 tufte.css (foundation, @font-face) + custom.css (theme, layout) + embed-fonts.css
static/js/                  theme.js, lang.js, toc.js
static/embeds/              Interactive D3.js visualizations (standalone HTML)
static/vendor/              Vendored D3 (d3-7.9.0.min.js)
static/css/et-book/         ET Book typeface files (woff2 + woff)
static/css/source-code-pro/ Source Code Pro 400 (woff2)
static/css/inter/           Inter, used by the embeds
tests/                      pytest suite for build.py
build.py                    The entire build system
```

## Content conventions

- Every post and page lives in both `en/` and `pt/`. Filenames must match across languages for the bilingual toggle to work.
- Frontmatter is YAML-like between `---` fences. Required fields: `title`, `date` (YYYY-MM-DD), `excerpt`. Optional: `draft: true` (accessible by direct URL but hidden from index and feed).
- Tufte extensions in markdown: `{mn}margin note{/mn}`, `{sn}sidenote{/sn}`, `{nt}new thought{/nt}`.
- Raw HTML in markdown passes through untouched. Interactive embeds use `<div class="graph-embed">` with an iframe pointing to `static/embeds/`.
- Each embed is one file for both languages: `?lang=pt|en` (default `en`) picks strings from its `STRINGS` dictionary, and `?embed` hides standalone chrome (theme toggle, instructions). Iframes use `?embed&amp;lang=en` or `?embed&amp;lang=pt`. Theme sync is a `storage` listener on `theme-preference`: the parent's theme.js writes localStorage, which fires the event in same-origin iframes.

## Writing style

- Direct, honest tone. No marketing language, no corporate jargon, no clichés.
- No em dashes. Use commas, periods, or parentheses instead.
- Follow each language's own capitalization conventions (EN and PT rules differ).
- EN and PT versions should be structurally equivalent (same paragraphs, same progression of ideas) but each must read as if natively written by an American or a Brazilian. Idiomaticity over literal accuracy.
- Margin notes over footnotes. The information is there if you want it, without forcing the reader to decide whether to interrupt their flow.

## Visual and design principles

- Tufte CSS: information density, minimize the superfluous, let the content speak.
- Grayscale palette with CSS variables for light/dark mode. No accent colors.
- Speed is non-negotiable. No unnecessary JavaScript. No external requests: fonts and D3 are self-hosted.
- ET Book typeface for body text, Source Code Pro for code.
- Interactive embeds (D3.js) should educate, not decorate. Each one should teach the reader something concrete.

## Technical patterns

- CSS theme: custom properties on `:root` (light) and `[data-theme="dark"]` (dark). `theme.js` handles toggle + localStorage persistence + system preference fallback.
- Sticky header uses `::before` pseudo-element with `-100vw` left/right offsets for full-viewport background without breaking the Tufte layout width.
- Table of contents appears as a fixed sidebar on screens >= 1440px. Uses IntersectionObserver for scroll tracking.
- Embeds are self-contained HTML files in `static/embeds/`. Each has its own CSS variables, D3.js vendored at `static/vendor/d3-7.9.0.min.js`, fonts self-hosted via `static/css/embed-fonts.css`, and embed/standalone dual mode.
- Template engine is simple string replacement: `{{variable}}`, `{{#key}}...{{/key}}` for conditionals/loops. One regex pass, so inserted values are never rescanned. An unknown `{{key}}` raises `BuildError`. Loop items see the outer context, item keys first.
- Tufte syntax is a Python-Markdown extension (`TufteExtension`: an inline pattern plus a treeprocessor that adds the label and checkbox), so `{sn}`, `{mn}` and `{nt}` stay literal inside code.

## Testing and quality

- `pytest` for build.py (frontmatter parsing, markdown conversion, Tufte extensions, template rendering, i18n).
- `ruff` for linting, `mypy` for type checking (strict mode).
- Python >= 3.10, single runtime dependency (`markdown>=3.4`).

## Known limitations

Things to be aware of when modifying the codebase. All have been reviewed and intentionally accepted as-is for a single-site personal blog.

### Regex and template engine

- **No nesting.** The Tufte inline pattern (`TUFTE_RE`, `{sn}...{/sn}`) and the template block regex (`{{#key}}...{{/key}}`) both use non-greedy `.*?`. Nesting the same tag type will match incorrectly. No content or template uses nesting, so this is fine.
- **Template values are trusted.** No HTML escaping. All context values (titles, excerpts, body) pass through raw, though a `{{...}}` inside a value is never re-rendered. Safe because all content is author-controlled.
- **Loop items must be dicts.** A non-dict item renders with the outer context only, so its own placeholders raise `BuildError` as unknown variables.

### URL construction

Filesystem paths use `Path` objects and are centralized at the top of `build.py`. URL-relative paths (`root="../../"`, `root="../"`, `root=""`, `url_prefix="posts/"`) are hardcoded in 4 call sites (`build_post`, `build_page`, `build_index`, `build_root_index`). Works correctly, but adding a new content type would mean adding another hardcoded root.

### Test coverage

102 tests pass. Well-covered: frontmatter parsing, markdown conversion, Tufte extensions, template rendering, i18n, heading extraction, all build functions, the full pipeline, and `main()` exit codes (including `--strict`). Still untested: `clean()`, and `serve()` beyond its exit on a failed build (simple wrappers with minimal logic).

### Frontend

- No `og:image` meta tag. Social shares show title/description but no preview image.
- SVG graphs in embeds have no ARIA labels or keyboard navigation.
