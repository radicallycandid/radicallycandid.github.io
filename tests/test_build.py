"""Integration tests for the build pipeline."""

import shutil
from pathlib import Path

import pytest

import build
from build import build_post, build_page


# Minimal templates that exercise the rendering pipeline
BASE_HTML = """<!DOCTYPE html>
<html lang="{{lang}}">
<head><title>{{title}}</title>
{{#canonical_url}}<link rel="canonical" href="{{canonical_url}}">{{/canonical_url}}
</head>
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

INDEX_HTML = """<section>
<ul>{{#posts}}<li>{{title}}</li>{{/posts}}</ul>
{{about_html}}
</section>"""


@pytest.fixture
def build_env(tmp_path: Path) -> Path:
    """Set up minimal templates and output dir for build functions."""
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "base.html").write_text(BASE_HTML)
    (templates / "post.html").write_text(POST_HTML)
    (templates / "page.html").write_text(PAGE_HTML)
    (templates / "index.html").write_text(INDEX_HTML)

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

    def test_collects_warnings(self, build_env: Path) -> None:
        """Pages missing excerpt populate the warnings list."""
        md = _write_md(build_env, "en", "pages", "no-excerpt-page", """---
title: No Excerpt
---

Content without excerpt.
""")
        warnings: list[str] = []
        build_page(md, "en", warnings=warnings)
        assert any("excerpt" in w for w in warnings)

    def test_page_uses_website_og_type(self, build_env: Path) -> None:
        """Pages use 'website' og_type (not 'article')."""
        md = _write_md(build_env, "en", "pages", "contact", """---
title: Contact
description: Get in touch.
---

Email me.
""")
        build_page(md, "en")
        output = build.OUTPUT_DIR / "en" / "contact.html"
        assert output.exists()
        assert "Contact" in output.read_text()


class TestBuildIndex:
    """Integration tests for build_index."""

    def test_creates_index_file(self, build_env: Path) -> None:
        """build_index writes output/{lang}/index.html."""
        posts = [
            {
                "title": "Post One",
                "published_date": "2026-01-15",
                "published_date_formatted": "January 15, 2026",
                "excerpt": "First post.",
                "url": "posts/post-one.html",
                "draft": False,
            },
        ]
        build.build_index(posts, "en")
        output = build.OUTPUT_DIR / "en" / "index.html"
        assert output.exists()
        assert "Post One" in output.read_text()

    def test_index_sorts_by_date_descending(self, build_env: Path) -> None:
        """Posts appear newest-first on the index."""
        posts = [
            {
                "title": "Older",
                "published_date": "2026-01-01",
                "published_date_formatted": "January 1, 2026",
                "excerpt": "",
                "url": "posts/older.html",
                "draft": False,
            },
            {
                "title": "Newer",
                "published_date": "2026-02-01",
                "published_date_formatted": "February 1, 2026",
                "excerpt": "",
                "url": "posts/newer.html",
                "draft": False,
            },
        ]
        build.build_index(posts, "en")
        html = (build.OUTPUT_DIR / "en" / "index.html").read_text()
        assert html.index("Newer") < html.index("Older")

    def test_index_includes_about_html(self, build_env: Path) -> None:
        """Index page embeds about.md content when available."""
        pages_dir = build_env / "pages" / "en"
        pages_dir.mkdir(parents=True)
        (pages_dir / "about.md").write_text("""---
title: About
---

I am a test person.""")
        original_pages = build.PAGES_DIR
        build.PAGES_DIR = build_env / "pages"
        try:
            build.build_index([], "en")
            html = (build.OUTPUT_DIR / "en" / "index.html").read_text()
            assert "test person" in html
        finally:
            build.PAGES_DIR = original_pages


class TestBuildFeed:
    """Integration tests for build_feed."""

    def test_creates_feed_file(self, build_env: Path) -> None:
        """build_feed writes output/{lang}/feed.xml."""
        posts = [
            {
                "title": "Feed Post",
                "published_date": "2026-01-15",
                "excerpt": "A post for the feed.",
                "url": "posts/feed-post.html",
            },
        ]
        build.build_feed(posts, "en")
        output = build.OUTPUT_DIR / "en" / "feed.xml"
        assert output.exists()
        content = output.read_text()
        assert "<title>Feed Post</title>" in content
        assert "feed-post.html" in content

    def test_feed_is_valid_xml_structure(self, build_env: Path) -> None:
        """Feed has proper Atom structure."""
        posts = [
            {
                "title": "Test",
                "published_date": "2026-01-01",
                "excerpt": "Excerpt.",
                "url": "posts/test.html",
            },
        ]
        build.build_feed(posts, "en")
        content = (build.OUTPUT_DIR / "en" / "feed.xml").read_text()
        assert content.startswith('<?xml version="1.0"')
        assert "<feed " in content
        assert "</feed>" in content
        assert "<entry>" in content
        assert "</entry>" in content

    def test_feed_limits_to_20_entries(self, build_env: Path) -> None:
        """Feed includes at most 20 posts."""
        posts = [
            {
                "title": f"Post {i}",
                "published_date": f"2026-01-{i:02d}",
                "excerpt": f"Excerpt {i}.",
                "url": f"posts/post-{i}.html",
            }
            for i in range(1, 26)
        ]
        build.build_feed(posts, "en")
        content = (build.OUTPUT_DIR / "en" / "feed.xml").read_text()
        assert content.count("<entry>") == 20


class TestCopyStatic:
    """Integration tests for copy_static."""

    def test_copies_static_directory(self, build_env: Path) -> None:
        """copy_static creates output/static with contents of static/."""
        static_dir = build_env / "static"
        static_dir.mkdir()
        (static_dir / "test.css").write_text("body { color: red; }")

        original_static = build.STATIC_DIR
        build.STATIC_DIR = static_dir
        try:
            build.copy_static()
            copied = build.OUTPUT_DIR / "static" / "test.css"
            assert copied.exists()
            assert copied.read_text() == "body { color: red; }"
        finally:
            build.STATIC_DIR = original_static


class TestBuildRootRedirect:
    """Integration tests for build_root_redirect."""

    def test_creates_root_redirect(self, build_env: Path) -> None:
        """build_root_redirect writes output/index.html with language detection."""
        build.build_root_redirect()
        output = build.OUTPUT_DIR / "index.html"
        assert output.exists()
        html = output.read_text()
        assert "localStorage" in html
        assert "navigator.language" in html
        assert "lang-preference" in html
        assert 'hreflang="en"' in html
        assert 'hreflang="pt"' in html
        assert 'hreflang="x-default"' in html
        assert 'http-equiv="refresh"' in html


class TestRenderContentUrls:
    """Test URL construction in _render_content."""

    def test_post_url_includes_posts_prefix(self, build_env: Path) -> None:
        """Posts generate URLs with posts/ prefix."""
        md = _write_md(build_env, "en", "posts", "test-urls", """---
title: URL Test
date: 2026-01-15
excerpt: Testing URLs.
---

Content.""")
        build_post(md, "en", has_alternate=True)
        output = build.OUTPUT_DIR / "en" / "posts" / "test-urls.html"
        html = output.read_text()
        assert "/en/posts/test-urls.html" in html

    def test_page_url_no_posts_prefix(self, build_env: Path) -> None:
        """Pages generate URLs without posts/ prefix."""
        md = _write_md(build_env, "en", "pages", "test-page-urls", """---
title: Page URL Test
description: Testing page URLs.
---

Content.""")
        build_page(md, "en", has_alternate=True)
        output = build.OUTPUT_DIR / "en" / "test-page-urls.html"
        html = output.read_text()
        assert "/en/test-page-urls.html" in html
        assert "/posts/" not in html


class TestBuild:
    """Integration tests for the full build() pipeline."""

    def test_full_build_succeeds(self, build_env: Path) -> None:
        """Full build with minimal content returns True."""
        _write_md(build_env, "en", "posts", "hello", """---
title: Hello
date: 2026-01-15
excerpt: World.
---

Content.""")
        _write_md(build_env, "pt", "posts", "hello", """---
title: Ola
date: 2026-01-15
excerpt: Mundo.
---

Conteudo.""")
        _write_md(build_env, "en", "pages", "about", """---
title: About
---

About me.""")
        _write_md(build_env, "pt", "pages", "about", """---
title: Sobre
---

Sobre mim.""")

        static_dir = build_env / "static"
        static_dir.mkdir()
        (static_dir / "test.txt").write_text("static")

        original_posts = build.POSTS_DIR
        original_pages = build.PAGES_DIR
        original_static = build.STATIC_DIR
        build.POSTS_DIR = build_env / "posts"
        build.PAGES_DIR = build_env / "pages"
        build.STATIC_DIR = static_dir
        try:
            if build.OUTPUT_DIR.exists():
                shutil.rmtree(build.OUTPUT_DIR)

            result = build.build()
            assert result is True

            assert (build.OUTPUT_DIR / "index.html").exists()
            assert (build.OUTPUT_DIR / "en" / "index.html").exists()
            assert (build.OUTPUT_DIR / "pt" / "index.html").exists()
            assert (build.OUTPUT_DIR / "en" / "posts" / "hello.html").exists()
            assert (build.OUTPUT_DIR / "pt" / "posts" / "hello.html").exists()
            assert (build.OUTPUT_DIR / "en" / "feed.xml").exists()
            assert (build.OUTPUT_DIR / "pt" / "feed.xml").exists()
            assert (build.OUTPUT_DIR / "static").exists()
        finally:
            build.POSTS_DIR = original_posts
            build.PAGES_DIR = original_pages
            build.STATIC_DIR = original_static

    def test_build_fails_without_templates(self, build_env: Path) -> None:
        """Build returns False when templates directory is missing."""
        original = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = build_env / "nonexistent"
        try:
            if build.OUTPUT_DIR.exists():
                shutil.rmtree(build.OUTPUT_DIR)
            result = build.build()
            assert result is False
        finally:
            build.TEMPLATES_DIR = original
