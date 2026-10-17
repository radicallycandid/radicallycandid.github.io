"""Tests for template rendering."""

from pathlib import Path

import pytest

from build import BuildError, render_template


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
        result = render_template("test.html", {"title": "Title", "content": "Body text"})
        assert result == "<h1>Title</h1><p>Body text</p>"

    def test_missing_variable_raises(self, mock_templates_dir: Path) -> None:
        """A variable absent from the context raises, naming the template."""
        (mock_templates_dir / "test.html").write_text("<h1>{{title}}</h1><p>{{missing}}</p>")
        with pytest.raises(BuildError, match=r"test\.html.*missing"):
            render_template("test.html", {"title": "Title"})

    def test_falsy_values_render_empty(self, mock_templates_dir: Path) -> None:
        """Keys present with None, empty string or False render as empty."""
        (mock_templates_dir / "test.html").write_text("[{{a}}][{{b}}][{{c}}]")
        result = render_template("test.html", {"a": None, "b": "", "c": False})
        assert result == "[][][]"

    def test_inserted_value_not_rescanned(self, mock_templates_dir: Path) -> None:
        """A placeholder inside an inserted value stays literal."""
        (mock_templates_dir / "test.html").write_text(
            '<main>{{content}}</main><html lang="{{lang}}">'
        )
        result = render_template("test.html", {"content": "<code>{{lang}}</code>", "lang": "pt"})
        assert result == '<main><code>{{lang}}</code></main><html lang="pt">'

    def test_inserted_block_not_rendered(self, mock_templates_dir: Path) -> None:
        """A block tag inside an inserted value stays literal."""
        (mock_templates_dir / "test.html").write_text("{{#show}}<p>{{body}}</p>{{/show}}")
        result = render_template(
            "test.html",
            {
                "show": True,
                "body": "{{#show}}x{{/show}} {{show}}",
            },
        )
        assert result == "<p>{{#show}}x{{/show}} {{show}}</p>"

    def test_loop_item_value_not_rescanned(self, mock_templates_dir: Path) -> None:
        """Values inserted inside a loop are not rescanned by the outer context."""
        (mock_templates_dir / "test.html").write_text("{{#items}}<li>{{name}}</li>{{/items}}")
        result = render_template(
            "test.html",
            {
                "items": [{"name": "{{secret}}"}],
                "secret": "leaked",
            },
        )
        assert result == "<li>{{secret}}</li>"

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
        result = render_template(
            "test.html",
            {
                "items": [
                    {"name": "One"},
                    {"name": "Two"},
                    {"name": "Three"},
                ]
            },
        )
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
