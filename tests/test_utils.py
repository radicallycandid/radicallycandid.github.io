"""Tests for utility functions."""

import pytest

from build import format_date, extract_headings, add_heading_ids, generate_toc_html


class TestFormatDate:
    """Tests for date formatting."""

    def test_format_valid_date(self) -> None:
        """Format a valid YYYY-MM-DD date."""
        result = format_date("2026-01-10")
        assert result == "January 10, 2026"

    def test_format_different_months(self) -> None:
        """Format dates with different months."""
        assert format_date("2026-06-15") == "June 15, 2026"
        assert format_date("2026-12-25") == "December 25, 2026"

    def test_format_invalid_date_returns_original(self) -> None:
        """Invalid date format returns the original string."""
        result = format_date("not-a-date")
        assert result == "not-a-date"

    def test_format_wrong_format_returns_original(self) -> None:
        """Wrong date format returns the original string."""
        result = format_date("01/10/2025")
        assert result == "01/10/2025"

    def test_format_empty_string(self) -> None:
        """Empty string returns empty string."""
        result = format_date("")
        assert result == ""


class TestExtractHeadings:
    """Tests for heading extraction."""

    def test_extract_h2_headings(self) -> None:
        """Extract h2 headings from HTML."""
        html = "<h2>First Section</h2><p>Text</p><h2>Second Section</h2>"
        headings = extract_headings(html)

        assert len(headings) == 2
        assert headings[0]["text"] == "First Section"
        assert headings[0]["level"] == 2
        assert headings[1]["text"] == "Second Section"

    def test_extract_h3_headings(self) -> None:
        """Extract h3 headings from HTML."""
        html = "<h3>Subsection</h3>"
        headings = extract_headings(html)

        assert len(headings) == 1
        assert headings[0]["text"] == "Subsection"
        assert headings[0]["level"] == 3

    def test_extract_mixed_headings(self) -> None:
        """Extract both h2 and h3 headings."""
        html = "<h2>Section</h2><h3>Subsection</h3><h2>Another</h2>"
        headings = extract_headings(html)

        assert len(headings) == 3
        assert headings[0]["level"] == 2
        assert headings[1]["level"] == 3
        assert headings[2]["level"] == 2

    def test_generate_id_from_text(self) -> None:
        """IDs are generated from heading text."""
        html = "<h2>My Section Title</h2>"
        headings = extract_headings(html)

        assert headings[0]["id"] == "my-section-title"

    def test_preserve_existing_id(self) -> None:
        """Existing IDs are preserved."""
        html = '<h2 id="custom-id">My Section</h2>'
        headings = extract_headings(html)

        assert headings[0]["id"] == "custom-id"

    def test_strip_html_from_heading_text(self) -> None:
        """HTML tags are stripped from heading text."""
        html = "<h2>Section with <strong>bold</strong> text</h2>"
        headings = extract_headings(html)

        assert headings[0]["text"] == "Section with bold text"

    def test_no_headings(self) -> None:
        """No headings returns empty list."""
        html = "<p>Just a paragraph.</p>"
        headings = extract_headings(html)

        assert headings == []

    def test_h1_not_extracted(self) -> None:
        """h1 headings are not extracted (only h2 and h3)."""
        html = "<h1>Title</h1><h2>Section</h2>"
        headings = extract_headings(html)

        assert len(headings) == 1
        assert headings[0]["text"] == "Section"


class TestAddHeadingIds:
    """Tests for adding IDs to headings."""

    def test_add_id_to_heading_without_id(self) -> None:
        """Add ID to heading that doesn't have one."""
        html = "<h2>My Section</h2>"
        headings = [{"level": 2, "id": "my-section", "text": "My Section"}]

        result = add_heading_ids(html, headings)

        assert '<h2 id="my-section">' in result

    def test_preserve_existing_id(self) -> None:
        """Don't modify headings that already have IDs."""
        html = '<h2 id="existing">My Section</h2>'
        headings = [{"level": 2, "id": "existing", "text": "My Section"}]

        result = add_heading_ids(html, headings)

        assert '<h2 id="existing">' in result
        assert result.count('id="') == 1  # Only one ID


class TestGenerateTocHtml:
    """Tests for ToC HTML generation."""

    def test_generate_toc_with_headings(self) -> None:
        """Generate ToC HTML from headings."""
        headings = [
            {"level": 2, "id": "section-one", "text": "Section One"},
            {"level": 3, "id": "subsection", "text": "Subsection"},
            {"level": 2, "id": "section-two", "text": "Section Two"},
        ]

        result = generate_toc_html(headings)

        assert '<nav class="toc"' in result
        assert '<ul class="toc-list">' in result
        assert 'href="#section-one"' in result
        assert 'href="#subsection"' in result
        assert 'href="#section-two"' in result
        assert 'class="toc-h2"' in result
        assert 'class="toc-h3"' in result

    def test_empty_headings_returns_empty(self) -> None:
        """Empty headings list returns empty string."""
        result = generate_toc_html([])
        assert result == ""

    def test_toc_has_aria_label(self) -> None:
        """ToC has accessibility label."""
        headings = [{"level": 2, "id": "test", "text": "Test"}]
        result = generate_toc_html(headings)

        assert 'aria-label="Table of contents"' in result
