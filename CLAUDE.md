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

### Critical: CI has no quality gates

The deploy workflow (`.github/workflows/deploy.yml`) runs `python build.py build` and deploys directly. No tests, no linting, no type checking. All the tooling exists (`make test`, `make lint`, `make typecheck`) but none runs in CI. A broken commit deploys to production unchecked.

### High: `build.py` core architecture

- **God functions.** `build()` (~106 lines) orchestrates everything: directory setup, static copying, content pairing, post/page/index/feed building, CNAME, warnings. `build_post()` (~103 lines) does file I/O, frontmatter parsing, date logic, markdown conversion, TOC generation, two template renders, and file writing. Both should be decomposed.
- **Post/page duplication.** `build_post()` and `build_page()` share ~80% identical code (read file, parse frontmatter, convert markdown, extract headings, generate TOC, render template, write). No shared abstraction.
- **Language pair lookup duplicated.** The same loop pattern for finding EN/PT pairs appears twice (once for posts, once for pages).
- **Path construction scattered.** `"../../"`, `"../"`, `"posts/"` hardcoded in multiple places across build functions. No path helper.

### High: test coverage gaps

85 tests pass, but they cover ~40-50% of functions. Completely untested: `build()`, `build_post()`, `build_index()`, `build_page()`, `build_feed()` (the entire build pipeline), `copy_static()`, `build_root_redirect()`, `serve()`, `main()`, `markdown_to_html()` integration (full pipeline including Tufte extensions), and internal helpers (`_convert_lists()`, `_convert_tables()`, `_wrap_paragraphs()`). The functions that are tested (frontmatter parsing, basic markdown, template rendering, i18n) are well-covered. No `conftest.py` exists. Template tests repeat a manual try/finally patching pattern 8 times instead of using a fixture.

### High: fragile regex patterns in `build.py`

- Sidenote/marginnote regex doesn't handle nesting (`{sn}outer {sn}inner{/sn}{/sn}` breaks).
- Code block language tag uses `\w*` which rejects `objective-c`, `c++`, etc.
- Template block regex can't handle nested blocks with the same key name.
- Bold/italic: `***bold italic***` produces `<strong>` only, not nested emphasis.
- Table parsing assumes row 2 is always the separator with no validation.
- Heading extraction has no collision detection for duplicate IDs.

### Medium: template engine limitations

- No escaping: values containing `{{` create invalid syntax.
- Loop items must be dicts (strings/primitives fail silently).
- Variable substitution runs after block processing, so injected block syntax would be evaluated.
- Missing template files throw raw `FileNotFoundError` with no context.
- No HTML escaping (intentional for body content, but means all context values are trusted).

### Medium: frontend gaps

**CSS:**
- No focus styles on `.theme-toggle`, `.lang-toggle`, or `.toc-list a` (keyboard navigation broken for these elements).
- Dead CSS in tufte.css: `.danger`, `.numeral`, `.epigraph`, `.sans`, `.table-wrapper` are unused.
- No tablet breakpoint (jumps from mobile at 760px to desktop at 1440px).
- Magic numbers: ToC width is 280px in one place, 260px in another; `scrollY + 100` in JS vs `HEADER_OFFSET = 80`.

**JS:**
- `IntersectionObserver` (toc.js) has no fallback for older browsers.
- ToC `setActiveLink()` sets a CSS class but no `aria-current` attribute for screen readers.

**Templates:**
- Hardcoded "Feed" string in base.html is English-only (not localized for PT).
- Missing `<time datetime>` on published dates (not machine-readable).
- No `og:image`, `og:url`, `twitter:card` meta tags (social shares show no preview).
- No `<link rel="canonical">` (could help with bilingual duplicate content).

### Medium: hardcoded configuration

All settings live as Python constants in `build.py` with no config file or env var override: `SITE_TITLE`, `SITE_URL`, `MIN_HEADINGS_FOR_TOC`, `DEFAULT_SERVER_PORT`, `DATE_FORMAT_INPUT`, `DATE_FORMAT_OUTPUT`, `PT_MONTHS`, `LANG_FLAGS`, template names, output path structure. Not a problem today (single site), but makes the SSG impossible to reuse without editing source.

### Low: external dependencies not pinned

- D3.js loaded as `d3.v7.min.js` (no patch version) in all 4 embed files. Behavior could change silently.
- Google Fonts loaded via `@import` in custom.css. Rendering could shift.

### Low: embed accessibility

- SVG graphs have no ARIA labels on nodes.
- No keyboard navigation for draggable graph elements.
- Instructions hidden in embed mode with no alternative for screen readers.

### Low: minor code smells

- Sidenote counter uses `list [0]` closure pattern instead of `nonlocal` (inconsistent with other counters).
- Scattered `print()` statements instead of structured logging.
- `os.chdir(OUTPUT_DIR)` in `serve()` mutates process-level state.
- `format_date()` tested in two separate test files with overlapping assertions.
- Mixed `Path` and string operations for path handling.
