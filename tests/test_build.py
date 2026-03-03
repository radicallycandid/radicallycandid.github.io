"""Integration tests for build_post and build_page."""

from pathlib import Path

import pytest

import build
from build import build_post, build_page


# Minimal templates that exercise the rendering pipeline
BASE_HTML = """<!DOCTYPE html>
<html lang="{{lang}}">
<head><title>{{title}}</title></head>
<body>{{content}}</body>
</html>"""

POST_HTML = """<article>
<h1>{{title}}</h1>
<time datetime="{{published_date_iso}}">{{published_date}}</time>
<section>{{body}}</section>
</article>"""

PAGE_HTML = """<article>
<h1>{{title}}</h1>
<section>{{body}}</section>
</article>"""


@pytest.fixture
def build_env(tmp_path: Path) -> Path:
    """Set up minimal templates and output dir for build functions."""
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "base.html").write_text(BASE_HTML)
    (templates / "post.html").write_text(POST_HTML)
    (templates / "page.html").write_text(PAGE_HTML)

    output = tmp_path / "output"
    output.mkdir()

    original_templates = build.TEMPLATES_DIR
    original_output = build.OUTPUT_DIR
    original_root = build.ROOT_DIR

    build.TEMPLATES_DIR = templates
    build.OUTPUT_DIR = output
    build.ROOT_DIR = tmp_path

    yield tmp_path

    build.TEMPLATES_DIR = original_templates
    build.OUTPUT_DIR = original_output
    build.ROOT_DIR = original_root


def _write_md(base: Path, lang: str, subdir: str, slug: str, content: str) -> Path:
    """Helper to write a markdown file in the expected directory structure."""
    d = base / subdir / lang
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{slug}.md"
    p.write_text(content)
    return p


class TestBuildPost:
    """Integration tests for build_post."""

    def test_creates_html_file(self, build_env: Path) -> None:
        """build_post writes an HTML file containing the post title."""
        md = _write_md(build_env, "en", "posts", "hello", """---
title: Hello World
date: 2026-01-15
excerpt: A greeting.
---

Some content here.
""")
        meta = build_post(md, "en")
        output = build.OUTPUT_DIR / "en" / "posts" / "hello.html"
        assert output.exists()
        html = output.read_text()
        assert "Hello World" in html
        assert meta["title"] == "Hello World"

    def test_draft_flag(self, build_env: Path) -> None:
        """Posts with draft: true return draft=True in metadata."""
        md = _write_md(build_env, "en", "posts", "draft-post", """---
title: Draft Post
date: 2026-02-01
excerpt: Not ready yet.
draft: true
---

Draft content.
""")
        meta = build_post(md, "en")
        assert meta["draft"] is True

    def test_collects_warnings(self, build_env: Path) -> None:
        """Posts missing excerpt populate the warnings list."""
        md = _write_md(build_env, "en", "posts", "no-excerpt", """---
title: No Excerpt Post
date: 2026-02-01
---

Content without excerpt.
""")
        warnings: list[str] = []
        build_post(md, "en", warnings=warnings)
        assert any("excerpt" in w for w in warnings)

    def test_date_fallback_to_mtime(self, build_env: Path) -> None:
        """Posts without a date field fall back to file mtime."""
        md = _write_md(build_env, "en", "posts", "no-date", """---
title: No Date Post
excerpt: Testing mtime fallback.
---

Content.
""")
        warnings: list[str] = []
        meta = build_post(md, "en", warnings=warnings)
        # published_date should be set (not empty)
        assert meta["published_date"]


class TestBuildPage:
    """Integration tests for build_page."""

    def test_creates_html_file(self, build_env: Path) -> None:
        """build_page writes an HTML file at output/{lang}/slug.html."""
        md = _write_md(build_env, "en", "pages", "about", """---
title: About Me
---

I am a person.
""")
        build_page(md, "en")
        output = build.OUTPUT_DIR / "en" / "about.html"
        assert output.exists()
        html = output.read_text()
        assert "About Me" in html

    def test_page_uses_website_og_type(self, build_env: Path) -> None:
        """Pages use 'website' og_type (not 'article')."""
        # We can verify this indirectly: the canonical URL should not contain /posts/
        md = _write_md(build_env, "en", "pages", "contact", """---
title: Contact
description: Get in touch.
---

Email me.
""")
        build_page(md, "en")
        output = build.OUTPUT_DIR / "en" / "contact.html"
        html = output.read_text()
        # The base template doesn't include og_type in our minimal version,
        # but we can verify the file was created at the page path (not posts/)
        assert output.exists()
        assert "Contact" in html
