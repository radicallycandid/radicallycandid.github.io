# Plan: Tackle All Technical Debt

## Context

The CLAUDE.md documents all known technical debt. This plan addresses every item, starting from the most critical, grouping related changes, and deferring what isn't worth fixing for a single-site personal blog. Each phase leaves the codebase in a working state.

---

## Phase 1: CI Quality Gates

**Why:** A broken commit currently deploys to production unchecked. This is the highest-impact, lowest-effort fix.

**File:** `.github/workflows/deploy.yml`

Replace the "Install dependencies" step (line 29-30) and insert a quality checks step before "Build site" (line 32-33):

```yaml
      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Quality checks
        run: |
          ruff check build.py
          mypy build.py
          pytest
```

This replaces `pip install -r requirements.txt` with `pip install -e ".[dev]"` (which installs both runtime and dev deps from pyproject.toml).

**Verify:** `pip install -e ".[dev]" && ruff check build.py && mypy build.py && pytest` locally.

---

## Phase 2: Test Infrastructure

**Why:** Template tests repeat a try/finally patching block 8 times. A conftest.py fixture eliminates this and sets up reusable fixtures for Phase 4.

### 2a. Create `tests/conftest.py`

```python
"""Shared test fixtures."""
from pathlib import Path
import pytest
import build

@pytest.fixture
def mock_templates_dir(tmp_path: Path):
    original = build.TEMPLATES_DIR
    build.TEMPLATES_DIR = tmp_path
    yield tmp_path
    build.TEMPLATES_DIR = original

@pytest.fixture
def mock_output_dir(tmp_path: Path):
    output = tmp_path / "output"
    output.mkdir()
    original = build.OUTPUT_DIR
    build.OUTPUT_DIR = output
    yield output
    build.OUTPUT_DIR = original

@pytest.fixture
def sample_post_md() -> str:
    return """---
title: Test Post
date: 2026-01-15
excerpt: A test post.
---

## Introduction

This is a test post.

## Section Two

More content.

## Section Three

Even more.
"""
```

### 2b. Simplify `tests/test_template.py`

Every test method changes from:

```python
def test_simple_variable_substitution(self, tmp_path: Path) -> None:
    template_file = tmp_path / "test.html"
    template_file.write_text("<h1>{{title}}</h1>")
    import build
    original_dir = build.TEMPLATES_DIR
    build.TEMPLATES_DIR = tmp_path
    try:
        result = render_template("test.html", {"title": "Hello World"})
        assert result == "<h1>Hello World</h1>"
    finally:
        build.TEMPLATES_DIR = original_dir
```

to:

```python
def test_simple_variable_substitution(self, mock_templates_dir: Path) -> None:
    (mock_templates_dir / "test.html").write_text("<h1>{{title}}</h1>")
    result = render_template("test.html", {"title": "Hello World"})
    assert result == "<h1>Hello World</h1>"
```

Apply to all 8 test methods. Remove `import tempfile` (unused). Remove `from build import TEMPLATES_DIR` (no longer needed).

**Verify:** `pytest tests/test_template.py -v` — all 8 tests pass.

---

## Phase 3: Refactor build_post/build_page Duplication

**Why:** These two functions share ~80% identical code. Extracting shared logic makes future changes safer and eliminates divergence risk.

**File:** `build.py`

### 3a. Extract `_render_content()` helper

Add before `build_post()` (before line 729). This function takes already-parsed frontmatter and body, does the shared work (markdown conversion, TOC, template rendering, file write):

```python
def _render_content(
    md_path: Path,
    lang: str,
    has_alternate: bool,
    frontmatter: dict[str, str],
    body: str,
    root: str,
    output_dir: Path,
    content_template: str,
    og_type: str,
    extra_template_vars: dict[str, object] | None = None,
) -> None:
```

Inside it:
- Extract title/subtitle from frontmatter
- Call `markdown_to_html(body)` and `generate_toc_html()`
- Get `other = get_other_lang(lang)`, compute `output_name`
- Build content template context (merging `extra_template_vars`)
- Render inner template, then base.html
- Compute `other_lang_url` based on `og_type` ("article" → `{root}{other}/posts/{name}`, else `{root}{other}/{name}`)
- Write output file, print build message

### 3b. Slim down `build_post()` (lines 729-830)

Keep only post-specific logic:
- Read file + parse frontmatter (lines 750-755)
- Validate + collect warnings (lines 757-759)
- Date handling with mtime fallback (lines 767-770)
- Call `_render_content(root="../../", output_dir=OUTPUT_DIR/lang/"posts", content_template="post.html", og_type="article", extra_template_vars={"published_date": format_date(...)})`
- Return metadata dict (lines 822-830)

### 3c. Slim down `build_page()` (lines 878-945)

Keep only:
- Read file + parse frontmatter (lines 894-899)
- Call `_render_content(root="../", output_dir=OUTPUT_DIR/lang, content_template="page.html", og_type="website")`

**Verify:**
1. Before: `python build.py build && cp -r output/ /tmp/output_before/`
2. After: `python build.py build && diff -r output/ /tmp/output_before/` — should be identical
3. `pytest -v` — all tests pass
4. `ruff check build.py && mypy build.py` — clean

---

## Phase 4: Integration Tests

**Why:** The entire build pipeline (build_post, build_page) has zero test coverage.

**File:** New `tests/test_build.py`

Tests using `mock_templates_dir` and `mock_output_dir` fixtures from conftest.py:

- `TestBuildPost::test_creates_html_file` — minimal post.html + base.html templates, verify output file exists and contains title
- `TestBuildPost::test_draft_flag` — frontmatter with `draft: true`, verify metadata returns `draft=True`
- `TestBuildPost::test_collects_warnings` — post missing excerpt, verify warnings list populated
- `TestBuildPost::test_date_fallback_to_mtime` — post with no date field, verify published_date is set
- `TestBuildPage::test_creates_html_file` — verify output at `{output}/en/about.html`
- `TestBuildPage::test_page_uses_website_og_type` — verify "website" appears in output

**Verify:** `pytest tests/test_build.py -v` — all new tests pass. `pytest -v` — full suite passes.

---

## Phase 5: CSS Focus Styles

**Why:** Keyboard navigation is broken — no visible focus indicator on interactive elements.

**File:** `static/css/custom.css`

Add after the existing hover rules (~line 155):

```css
.theme-toggle:focus-visible,
.lang-toggle:focus-visible {
    outline: 2px solid var(--text-color);
    outline-offset: 2px;
}

.toc-list a:focus-visible,
.nav-links a:focus-visible,
.site-title:focus-visible,
.post-title a:focus-visible {
    outline: 2px solid var(--text-color);
    outline-offset: 2px;
}
```

`:focus-visible` shows outline only for keyboard nav, not mouse clicks.

**Verify:** Open site, Tab through elements, confirm visible outline appears.

---

## Phase 6: JS Accessibility (aria-current)

**Why:** Screen readers can't tell which ToC section is active.

**File:** `static/js/toc.js`, in `setActiveLink()` (lines 57-69)

Add `aria-current` attribute management:

```javascript
if (href === '#' + id) {
    link.classList.add('active');
    link.setAttribute('aria-current', 'true');
} else {
    link.classList.remove('active');
    link.removeAttribute('aria-current');
}
```

**Verify:** Inspect active `.toc-list a` element in DevTools, confirm `aria-current="true"` present.

---

## Phase 7: HTML Semantics & SEO

**Why:** Published dates aren't machine-readable, no canonical URLs, no Twitter cards.

### 7a. `<time datetime>` on dates

**File:** `templates/post.html` line 10 — change:
```html
<span class="post-date">{{published_date}}</span>
```
to:
```html
<time class="post-date" datetime="{{published_date_iso}}">{{published_date}}</time>
```

**File:** `templates/index.html` line 13 — change:
```html
<span class="post-date">{{published_date_formatted}}</span>
```
to:
```html
<time class="post-date" datetime="{{published_date}}">{{published_date_formatted}}</time>
```

**File:** `build.py` — in `_render_content()` (or `build_post()`), pass `published_date_iso` (the YYYY-MM-DD string) in `extra_template_vars`. The index template already has `published_date` (ISO string) from the metadata dict.

### 7b. Canonical URL + Twitter card

**File:** `templates/base.html` — add after line 10:
```html
    {{#canonical_url}}<link rel="canonical" href="{{canonical_url}}">{{/canonical_url}}
    {{#canonical_url}}<meta property="og:url" content="{{canonical_url}}">{{/canonical_url}}
    <meta name="twitter:card" content="summary">
```

**File:** `build.py` — pass `canonical_url` in every `render_template("base.html", ...)` call:
- `build_post` / `_render_content` for articles: `f"{SITE_URL}/{lang}/posts/{output_name}"`
- `build_page` / `_render_content` for pages: `f"{SITE_URL}/{lang}/{output_name}"`
- `build_index`: `f"{SITE_URL}/{lang}/"`

**Verify:** `python build.py build`, inspect a generated post HTML for `<time datetime>`, `<link rel="canonical">`, `<meta name="twitter:card">`.

---

## Phase 8: Regex Hardening

**Why:** Edge cases in the fallback markdown parser and heading ID generation.

**File:** `build.py`

1. **Code block language** (line 326): `r"```(\w*)\n"` → `r"```([^\n]*)\n"` — accepts `c++`, `objective-c`, etc.

2. **Bold/italic ordering** (lines 334-335): Add `***` processing before `**`:
   ```python
   text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
   text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
   text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
   ```

3. **Heading ID collision** (in `extract_headings()`, after line 511): Add deduplication:
   ```python
   base_id = heading_id
   counter = 1
   while any(h["id"] == heading_id for h in headings):
       heading_id = f"{base_id}-{counter}"
       counter += 1
   ```

**Tests to add:**

`tests/test_markdown.py`:
- `test_code_block_with_special_language` — ` ```c++\nint main() {}\n``` ` produces `<pre><code>`
- `test_bold_italic_combined` — `***bold italic***` → `<strong><em>bold italic</em></strong>`

`tests/test_utils.py`:
- `test_duplicate_heading_ids_get_suffixed` — two `<h2>Examples</h2>` get IDs `examples` and `examples-1`

**Verify:** `pytest -v` — all tests pass including new ones.

---

## Deferred Items

These are documented as debt in CLAUDE.md but not worth fixing:

| Item | Why defer |
|---|---|
| Hardcoded configuration | Works fine for a single site. Config file adds complexity for zero benefit. |
| Template engine limitations (escaping, nesting) | No real content triggers these. The templates are simple and controlled. |
| Dead CSS in tufte.css | Third-party stylesheet, intended for broader use. Removing saves ~200 bytes. |
| Tablet breakpoint | The 75% content width scales naturally. Looks fine on tablets. |
| ToC width "inconsistency" | 280px is hidden default, 260px is visible at 1440px+. Intentional. |
| D3.js version pinning | v7 has been stable for years. Major version pin is appropriate. |
| Google Fonts @import | Only used for code blocks below the fold. Performance impact negligible. |
| Embed accessibility (ARIA on SVG, keyboard drag) | High effort, low real-world impact for educational visualizations. |
| Sidenote counter list[0] vs nonlocal | Cosmetic. Function works correctly. |
| print() vs structured logging | print() is correct for a 0.1s build script. |
| os.chdir() in serve() | Standard pattern for SimpleHTTPRequestHandler. Dev-only. |
| format_date() tested in 2 files | Harmless. Tests cover different aspects. |
| Mixed Path/string ops | URLs are strings, files are Paths. This is correct. |
| "Feed" hardcoded in base.html | Invisible `<link>` tag title. "Feed" works in both EN and PT. |
| og:image | Requires an actual image to exist. Out of scope. |
| Sidenote nesting regex | Nested sidenotes are typographically nonsensical. No real use case. |
| Template same-name block nesting | No template uses this pattern. Would require a recursive parser. |
| IntersectionObserver polyfill | 97%+ browser support. Same as :focus-visible. |

---

## Execution Order

```
Phase 1 (CI)              — independent, do first
Phase 2 (conftest)        — independent, do second
Phase 5 (CSS focus)       — independent  ┐
Phase 6 (JS aria-current) — independent  ├── batch these together
Phase 7 (HTML semantics)  — independent  ┘
Phase 8 (regex hardening) — independent
Phase 3 (refactor)        — after Phase 2 (uses fixtures for confidence)
Phase 4 (integration tests) — after Phase 3 (tests refactored code)
```

## Final Verification

After all phases: `ruff check build.py && mypy build.py && pytest -v && python build.py build` — everything green, output looks correct.
