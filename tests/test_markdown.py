"""Tests for markdown conversion functions."""

import pytest

from build import basic_markdown_to_html


class TestBasicMarkdownToHtml:
    """Tests for the fallback markdown converter."""

    def test_convert_h1(self) -> None:
        """Convert h1 headers."""
        text = "# Header One"
        result = basic_markdown_to_html(text)
        assert "<h1>Header One</h1>" in result

    def test_convert_h2(self) -> None:
        """Convert h2 headers."""
        text = "## Header Two"
        result = basic_markdown_to_html(text)
        assert "<h2>Header Two</h2>" in result

    def test_convert_h3(self) -> None:
        """Convert h3 headers."""
        text = "### Header Three"
        result = basic_markdown_to_html(text)
        assert "<h3>Header Three</h3>" in result

    def test_convert_bold(self) -> None:
        """Convert bold text."""
        text = "This is **bold** text."
        result = basic_markdown_to_html(text)
        assert "<strong>bold</strong>" in result

    def test_convert_italic(self) -> None:
        """Convert italic text."""
        text = "This is *italic* text."
        result = basic_markdown_to_html(text)
        assert "<em>italic</em>" in result

    def test_convert_inline_code(self) -> None:
        """Convert inline code."""
        text = "Use `code` here."
        result = basic_markdown_to_html(text)
        assert "<code>code</code>" in result

    def test_convert_link(self) -> None:
        """Convert links."""
        text = "Visit [Example](https://example.com) site."
        result = basic_markdown_to_html(text)
        assert '<a href="https://example.com">Example</a>' in result

    def test_convert_unordered_list(self) -> None:
        """Convert unordered lists."""
        text = """- Item one
- Item two
- Item three"""
        result = basic_markdown_to_html(text)
        assert "<ul>" in result
        assert "<li>Item one</li>" in result
        assert "<li>Item two</li>" in result
        assert "<li>Item three</li>" in result
        assert "</ul>" in result

    def test_convert_ordered_list(self) -> None:
        """Convert ordered lists."""
        text = """1. First item
2. Second item
3. Third item"""
        result = basic_markdown_to_html(text)
        assert "<ol>" in result
        assert "<li>First item</li>" in result
        assert "<li>Second item</li>" in result
        assert "<li>Third item</li>" in result
        assert "</ol>" in result

    def test_convert_code_block(self) -> None:
        """Convert fenced code blocks."""
        text = """```python
def hello():
    print("world")
```"""
        result = basic_markdown_to_html(text)
        assert "<pre><code>" in result
        assert "def hello():" in result
        assert "</code></pre>" in result

    def test_convert_table(self) -> None:
        """Convert markdown tables."""
        text = """| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |"""
        result = basic_markdown_to_html(text)
        assert "<table>" in result
        assert "<thead>" in result
        assert "<th>Header 1</th>" in result
        assert "<th>Header 2</th>" in result
        assert "<tbody>" in result
        assert "<td>Cell 1</td>" in result
        assert "</table>" in result

    def test_wrap_paragraphs(self) -> None:
        """Plain text is wrapped in paragraph tags."""
        text = "This is a paragraph."
        result = basic_markdown_to_html(text)
        assert "<p>This is a paragraph.</p>" in result

    def test_multiple_paragraphs(self) -> None:
        """Multiple paragraphs separated by blank lines."""
        text = """First paragraph.

Second paragraph."""
        result = basic_markdown_to_html(text)
        assert "<p>First paragraph.</p>" in result
        assert "<p>Second paragraph.</p>" in result

    def test_headers_not_wrapped_in_p(self) -> None:
        """Headers should not be wrapped in paragraph tags."""
        text = "## A Header"
        result = basic_markdown_to_html(text)
        assert "<p><h2>" not in result
        assert "<h2>A Header</h2>" in result

    def test_code_blocks_preserved(self) -> None:
        """Code blocks preserve their content exactly."""
        text = """```
# This is not a header
**This is not bold**
```"""
        result = basic_markdown_to_html(text)
        # Content inside code block should not be converted
        assert "<h1>" not in result
        assert "<strong>" not in result
        assert "# This is not a header" in result

    def test_nested_formatting(self) -> None:
        """Handle nested formatting (bold within text)."""
        text = "Some **bold** and *italic* text."
        result = basic_markdown_to_html(text)
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_link_with_title(self) -> None:
        """Links work without title attribute."""
        text = "[Click here](https://example.com)"
        result = basic_markdown_to_html(text)
        assert '<a href="https://example.com">Click here</a>' in result
