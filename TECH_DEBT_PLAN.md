# Plan: Tackle All Technical Debt

## Context

The CLAUDE.md documents all known technical debt. This plan addressed every item, starting from the most critical, grouping related changes, and deferring what isn't worth fixing for a single-site personal blog. Each phase left the codebase in a working state.

All 14 phases are now complete. 106 tests pass, ruff clean, build produces correct output.

---

## Completed Phases

### Phase 1: CI Quality Gates — DONE

deploy.yml now runs ruff, mypy, and pytest before building. A broken commit no longer deploys unchecked.

### Phase 2: Test Infrastructure — DONE

`tests/conftest.py` created with `mock_templates_dir` fixture. All 8 template tests simplified to use the fixture (no more try/finally patching).

### Phase 3: Refactor build_post/build_page Duplication — DONE

Extracted `_render_content()` (shared rendering) and `find_content_pairs()` (language pair lookup). `build_post()` reduced from ~103 to 67 lines. `build_page()` reduced to 34 lines. Post/page duplication eliminated.

### Phase 4: Integration Tests — DONE

`tests/test_build.py` added with initial tests covering `build_post()` and `build_page()`.

### Phase 5: CSS Focus Styles — DONE

`:focus-visible` outlines added for `.theme-toggle`, `.lang-toggle`, `.toc-list a`, `.nav-links a`, `.site-title`, `.post-title a`.

### Phase 6: JS Accessibility (aria-current) — DONE

`setActiveLink()` in toc.js now sets/removes `aria-current="true"` alongside the active CSS class.

### Phase 7: HTML Semantics & SEO — DONE

`<time datetime>` on published dates. `<link rel="canonical">` and `<meta property="og:url">` conditional on `canonical_url`. `<meta name="twitter:card" content="summary">`. `og:title`, `og:description`, `og:type` all present.

### Phase 8: Regex Hardening — DONE

Code block language tag uses `[^\n]*` (accepts `c++`, `objective-c`). Bold/italic processes `***` before `**` before `*`. Heading ID extraction deduplicates with `-N` suffix. Tests for all three.

### Phase 9: Decompose `build()` — DONE

Extracted 4 helpers: `_validate_build_dirs()`, `_prepare_output_dir()`, `_build_language()`, `_copy_cname()`. `build()` is now a ~35-line orchestrator.

### Phase 10: Fix `_render_content()` coupling — DONE

Added `url_prefix` parameter replacing `og_type`-based URL routing. Added `RenderResult` dataclass so `_render_content()` returns computed values. `build_post()` no longer re-derives title/excerpt/output_name.

### Phase 11: Validate frontmatter for pages — DONE

`build_page()` now accepts `warnings` parameter and calls `validate_frontmatter()`. `_build_language()` passes warnings through. Test added for page warning collection.

### Phase 12: Clean up dead code and fixtures — DONE

Removed `TemplateError` exception class (dead code). Removed unused `mock_output_dir` and `sample_post_md` fixtures from conftest.py.

### Phase 13: Expand test coverage — DONE

Added 12 new tests: `TestBuildIndex` (3), `TestBuildFeed` (3), `TestCopyStatic` (1), `TestBuildRootRedirect` (1), `TestRenderContentUrls` (2), `TestBuild` (2). Total: 106 tests.

### Phase 14: Consolidate `format_date()` tests — DONE

Renamed `TestFormatDateI18n` to `TestFormatDate` in test_i18n.py. Added 4 unique tests from test_utils.py (January EN, different months, wrong format, empty string). Removed `TestFormatDate` from test_utils.py.

---

## Deferred Items

These are documented as debt in CLAUDE.md but not worth fixing for a single-site personal blog:

| Item | Why defer |
|---|---|
| Hardcoded configuration | Works fine for a single site. Config file adds complexity for zero benefit. |
| Template engine limitations (escaping, nesting) | No real content triggers these. The templates are simple and controlled. |
| Dead CSS in tufte.css | Third-party stylesheet, intended for broader use. Removing saves ~200 bytes. |
| Dead ToC default width 280px | Never renders (sidebar hidden until 1440px where width is 260px). Harmless. |
| Tablet breakpoint | The 75% content width scales naturally. Looks fine on tablets. |
| Magic number scrollY+100 vs HEADER_OFFSET=80 | Different purposes (initial position detection vs scroll target offset). Works correctly. |
| D3.js version pinning | v7 has been stable for years. Major version pin is appropriate. |
| Google Fonts @import | Only used for code blocks below the fold. Performance impact negligible. |
| Embed accessibility (ARIA on SVG, keyboard drag) | High effort, low real-world impact for educational visualizations. |
| Sidenote counter list[0] vs nonlocal | Cosmetic. Function works correctly. |
| print() vs structured logging | print() is correct for a 0.1s build script. |
| os.chdir() in serve() | Standard pattern for SimpleHTTPRequestHandler. Dev-only. |
| "Feed" hardcoded in base.html | Invisible `<link>` tag title. "Feed" works in both EN and PT. |
| og:image | Requires an actual image to exist. Out of scope until a default image is designed. |
| Sidenote nesting regex | Nested sidenotes are typographically nonsensical. No real use case. |
| Template same-name block nesting | No template uses this pattern. Would require a recursive parser. |
| IntersectionObserver guard | 97%+ browser support since 2019. Not worth a polyfill. |
| Table separator validation (fallback parser) | Only affects the fallback parser when the `markdown` library is unavailable. No real-world impact. |
| build_index() re-reads about.md | Called twice (once per language). Two file reads is negligible. |
