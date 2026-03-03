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

## Known technical debt

### Medium: `build.py` architecture

- **Path construction scattered.** `"../../"`, `"../"`, `"posts/"` hardcoded across `build_post()`, `build_page()`, `build_index()`, and `_render_content()`. No path helper or URL builder.
- **`build_index()` re-reads about.md** every time it is called (once per language) instead of receiving or caching it. Two file reads is negligible.

### Medium: fragile regex patterns in `build.py`

- Sidenote/marginnote regex (`.*?` non-greedy) doesn't handle nesting (`{sn}outer {sn}inner{/sn}{/sn}` matches the first `{sn}` to the first `{/sn}`, leaving a trailing `{/sn}` as literal text). No real use case for nested sidenotes.
- Template block regex has the same nesting limitation for blocks with the same key name. No template uses this pattern.
- Table parsing (fallback parser) assumes row 2 is always the separator with no validation. Only affects the fallback when the `markdown` library is unavailable.

### Medium: template engine limitations

- No escaping: values containing `{{` create invalid syntax.
- Loop items must be dicts (strings/primitives produce raw template text with unresolved placeholders).
- Missing template files throw raw `FileNotFoundError` with no context.
- No HTML escaping (intentional for body content, but means all context values including titles and excerpts are trusted).

### Medium: frontend gaps

**CSS:**
- Dead CSS in tufte.css: `.danger`, `.numeral`, `.epigraph`, `.sans`, `.table-wrapper` are unused. ToC default width `280px` in custom.css is also dead (sidebar is `display: none` by default, only shown at 1440px+ where width is `260px`).
- No tablet breakpoint (jumps from mobile at 760px to desktop at 1440px).
- Magic number: `scrollY + 100` in toc.js `setInitialActive()` vs named constant `HEADER_OFFSET = 80` used elsewhere in the same file.

**JS:**
- `IntersectionObserver` (toc.js) has no feature-detection guard. Low practical impact (supported since Safari 12.1/2019).

**Templates:**
- Hardcoded "Feed" string in base.html `<link>` title is English-only (not localized for PT).
- No `og:image` meta tag (social shares have title/description but no preview image). Other social tags (`og:title`, `og:description`, `og:type`, `og:url`, `twitter:card`) are present.

### Medium: hardcoded configuration

All settings live as Python constants in `build.py` with no config file or env var override: `SITE_TITLE`, `SITE_URL`, `MIN_HEADINGS_FOR_TOC`, `DEFAULT_SERVER_PORT`, `DATE_FORMAT_INPUT`, `DATE_FORMAT_OUTPUT`, `PT_MONTHS`, `LANG_FLAGS`, template names, output path structure. Not a problem today (single site), but makes the SSG impossible to reuse without editing source.

### Medium: test coverage gaps

106 tests pass. Well-covered: frontmatter parsing, basic markdown, Tufte extensions, template rendering, i18n, heading extraction, `build_post()`, `build_page()`, `build_index()`, `build_feed()`, `copy_static()`, `build_root_redirect()`, `_render_content()` URL construction, and full `build()` pipeline. Still untested: `clean()`, `serve()`, `main()`. Internal helpers (`_convert_lists()`, `_convert_tables()`, `_wrap_paragraphs()`) have indirect coverage only through `basic_markdown_to_html` tests.

### Low: external dependencies not pinned

- D3.js loaded as `d3.v7.min.js` (no patch version) in all 4 embed files. Behavior could change silently.
- Google Fonts loaded via `@import` in custom.css (render-blocking, no preconnect) and via `<link>` in all 4 embed files.

### Low: embed accessibility

- SVG graphs have no ARIA labels (`role`, `aria-label`, `<title>`/`<desc>`) on the `<svg>` element or child nodes, in any of the 4 embeds.
- No keyboard navigation for draggable/clickable graph elements (no `tabindex`, no keydown handlers).
- Instructions hidden in embed mode (`display: none`) with no visually-hidden alternative for screen readers.

### Low: minor code smells

- Sidenote counter uses `list [0]` closure pattern instead of `nonlocal` (inconsistent with `add_heading_ids` which uses `nonlocal`).
- Scattered `print()` statements (25+) instead of structured logging.
- `os.chdir(OUTPUT_DIR)` in `serve()` mutates process-level state.
