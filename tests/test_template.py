"""Tests for template rendering."""

import tempfile
from pathlib import Path

import pytest

from build import render_template, TEMPLATES_DIR


class TestRenderTemplate:
    """Tests for the template rendering function."""

    def test_simple_variable_substitution(self, tmp_path: Path) -> None:
        """Replace simple {{variable}} placeholders."""
        template_content = "<h1>{{title}}</h1>"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        # Temporarily override TEMPLATES_DIR
        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"title": "Hello World"})
            assert result == "<h1>Hello World</h1>"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_multiple_variables(self, tmp_path: Path) -> None:
        """Replace multiple variables."""
        template_content = "<h1>{{title}}</h1><p>{{content}}</p>"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {
                "title": "Title",
                "content": "Body text"
            })
            assert result == "<h1>Title</h1><p>Body text</p>"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_missing_variable_left_unchanged(self, tmp_path: Path) -> None:
        """Missing variables are left as-is in the output."""
        template_content = "<h1>{{title}}</h1><p>{{missing}}</p>"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"title": "Title"})
            # Variables not in context are left unchanged
            assert result == "<h1>Title</h1><p>{{missing}}</p>"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_conditional_truthy(self, tmp_path: Path) -> None:
        """Conditional blocks render when value is truthy."""
        template_content = "{{#show}}Visible{{/show}}"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"show": True})
            assert result == "Visible"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_conditional_falsy(self, tmp_path: Path) -> None:
        """Conditional blocks are removed when value is falsy."""
        template_content = "Before{{#show}}Hidden{{/show}}After"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"show": False})
            assert result == "BeforeAfter"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_loop_over_list(self, tmp_path: Path) -> None:
        """Loop over a list of items."""
        template_content = "<ul>{{#items}}<li>{{name}}</li>{{/items}}</ul>"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {
                "items": [
                    {"name": "One"},
                    {"name": "Two"},
                    {"name": "Three"},
                ]
            })
            assert result == "<ul><li>One</li><li>Two</li><li>Three</li></ul>"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_empty_list(self, tmp_path: Path) -> None:
        """Empty list produces no output."""
        template_content = "<ul>{{#items}}<li>{{name}}</li>{{/items}}</ul>"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"items": []})
            assert result == "<ul></ul>"
        finally:
            build.TEMPLATES_DIR = original_dir

    def test_nested_conditionals(self, tmp_path: Path) -> None:
        """Nested conditionals work correctly."""
        template_content = "{{#outer}}Outer{{#inner}}Inner{{/inner}}{{/outer}}"
        template_file = tmp_path / "test.html"
        template_file.write_text(template_content)

        import build
        original_dir = build.TEMPLATES_DIR
        build.TEMPLATES_DIR = tmp_path

        try:
            result = render_template("test.html", {"outer": True, "inner": True})
            assert result == "OuterInner"

            result = render_template("test.html", {"outer": True, "inner": False})
            assert result == "Outer"

            result = render_template("test.html", {"outer": False, "inner": True})
            assert result == ""
        finally:
            build.TEMPLATES_DIR = original_dir
