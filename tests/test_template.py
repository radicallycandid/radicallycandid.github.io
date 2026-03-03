"""Tests for template rendering."""

from pathlib import Path

import pytest

from build import render_template


class TestRenderTemplate:
    """Tests for the template rendering function."""

    def test_simple_variable_substitution(self, mock_templates_dir: Path) -> None:
        """Replace simple {{variable}} placeholders."""
        (mock_templates_dir / "test.html").write_text("<h1>{{title}}</h1>")
        result = render_template("test.html", {"title": "Hello World"})
        assert result == "<h1>Hello World</h1>"

    def test_multiple_variables(self, mock_templates_dir: Path) -> None:
        """Replace multiple variables."""
        (mock_templates_dir / "test.html").write_text("<h1>{{title}}</h1><p>{{content}}</p>")
        result = render_template("test.html", {
            "title": "Title",
            "content": "Body text"
        })
        assert result == "<h1>Title</h1><p>Body text</p>"

    def test_missing_variable_left_unchanged(self, mock_templates_dir: Path) -> None:
        """Missing variables are left as-is in the output."""
        (mock_templates_dir / "test.html").write_text("<h1>{{title}}</h1><p>{{missing}}</p>")
        result = render_template("test.html", {"title": "Title"})
        assert result == "<h1>Title</h1><p>{{missing}}</p>"

    def test_conditional_truthy(self, mock_templates_dir: Path) -> None:
        """Conditional blocks render when value is truthy."""
        (mock_templates_dir / "test.html").write_text("{{#show}}Visible{{/show}}")
        result = render_template("test.html", {"show": True})
        assert result == "Visible"

    def test_conditional_falsy(self, mock_templates_dir: Path) -> None:
        """Conditional blocks are removed when value is falsy."""
        (mock_templates_dir / "test.html").write_text("Before{{#show}}Hidden{{/show}}After")
        result = render_template("test.html", {"show": False})
        assert result == "BeforeAfter"

    def test_loop_over_list(self, mock_templates_dir: Path) -> None:
        """Loop over a list of items."""
        (mock_templates_dir / "test.html").write_text(
            "<ul>{{#items}}<li>{{name}}</li>{{/items}}</ul>"
        )
        result = render_template("test.html", {
            "items": [
                {"name": "One"},
                {"name": "Two"},
                {"name": "Three"},
            ]
        })
        assert result == "<ul><li>One</li><li>Two</li><li>Three</li></ul>"

    def test_empty_list(self, mock_templates_dir: Path) -> None:
        """Empty list produces no output."""
        (mock_templates_dir / "test.html").write_text(
            "<ul>{{#items}}<li>{{name}}</li>{{/items}}</ul>"
        )
        result = render_template("test.html", {"items": []})
        assert result == "<ul></ul>"

    def test_nested_conditionals(self, mock_templates_dir: Path) -> None:
        """Nested conditionals work correctly."""
        (mock_templates_dir / "test.html").write_text(
            "{{#outer}}Outer{{#inner}}Inner{{/inner}}{{/outer}}"
        )
        result = render_template("test.html", {"outer": True, "inner": True})
        assert result == "OuterInner"

        result = render_template("test.html", {"outer": True, "inner": False})
        assert result == "Outer"

        result = render_template("test.html", {"outer": False, "inner": True})
        assert result == ""
