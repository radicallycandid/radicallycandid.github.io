"""Tests for Tufte-specific conversions."""

import pytest

from build import convert_newthought, convert_sidenotes


class TestConvertSidenotes:
    """Tests for sidenote and marginnote conversion."""

    def test_convert_single_sidenote(self) -> None:
        """Convert a single sidenote."""
        html = "Some text{sn}This is a sidenote.{/sn} continues here."
        result = convert_sidenotes(html)

        assert 'class="margin-toggle sidenote-number"' in result
        assert 'class="sidenote"' in result
        assert "This is a sidenote." in result
        assert "{sn}" not in result
        assert "{/sn}" not in result

    def test_convert_single_marginnote(self) -> None:
        """Convert a single margin note."""
        html = "Some text{mn}This is a margin note.{/mn} continues here."
        result = convert_sidenotes(html)

        assert 'class="margin-toggle"' in result
        assert 'class="marginnote"' in result
        assert "This is a margin note." in result
        assert "{mn}" not in result
        assert "{/mn}" not in result

    def test_sidenotes_are_numbered_sequentially(self) -> None:
        """Multiple sidenotes get sequential IDs."""
        html = "First{sn}Note 1{/sn} and second{sn}Note 2{/sn}."
        result = convert_sidenotes(html)

        assert 'id="sn-1"' in result
        assert 'id="sn-2"' in result

    def test_marginnotes_are_numbered_sequentially(self) -> None:
        """Multiple marginnotes get sequential IDs."""
        html = "First{mn}Note 1{/mn} and second{mn}Note 2{/mn}."
        result = convert_sidenotes(html)

        assert 'id="mn-1"' in result
        assert 'id="mn-2"' in result

    def test_mixed_sidenotes_and_marginnotes(self) -> None:
        """Sidenotes and marginnotes share the counter."""
        html = "A{sn}Sidenote{/sn} and{mn}Marginnote{/mn}."
        result = convert_sidenotes(html)

        # They share the counter, so IDs increment together
        assert 'id="sn-1"' in result
        assert 'id="mn-2"' in result

    def test_sidenote_with_html_content(self) -> None:
        """Sidenotes can contain HTML."""
        html = "Text{sn}Note with <strong>bold</strong> text.{/sn}."
        result = convert_sidenotes(html)

        assert "<strong>bold</strong>" in result
        assert 'class="sidenote"' in result

    def test_multiline_sidenote(self) -> None:
        """Sidenotes can span multiple lines."""
        html = """Text{sn}This is a
multiline sidenote.{/sn} continues."""
        result = convert_sidenotes(html)

        assert "This is a\nmultiline sidenote." in result

    def test_no_sidenotes_unchanged(self) -> None:
        """Text without sidenotes passes through unchanged."""
        html = "Just regular text."
        result = convert_sidenotes(html)

        assert result == html

    def test_marginnote_has_plus_symbol(self) -> None:
        """Marginnotes display the ⊕ symbol."""
        html = "Text{mn}A margin note.{/mn}."
        result = convert_sidenotes(html)

        assert "&#8853;" in result  # ⊕ symbol


class TestConvertNewthought:
    """Tests for newthought conversion."""

    def test_convert_newthought(self) -> None:
        """Convert newthought syntax to span."""
        html = "{nt}The beginning{/nt} of a new section."
        result = convert_newthought(html)

        assert '<span class="newthought">The beginning</span>' in result
        assert "{nt}" not in result
        assert "{/nt}" not in result

    def test_multiple_newthoughts(self) -> None:
        """Multiple newthoughts are converted."""
        html = "{nt}First{/nt} paragraph. {nt}Second{/nt} paragraph."
        result = convert_newthought(html)

        assert result.count('<span class="newthought">') == 2

    def test_no_newthought_unchanged(self) -> None:
        """Text without newthought passes through unchanged."""
        html = "Regular text without newthought."
        result = convert_newthought(html)

        assert result == html

    def test_newthought_with_formatting(self) -> None:
        """Newthought can contain other formatting."""
        html = "{nt}Text with <em>emphasis</em>{/nt} here."
        result = convert_newthought(html)

        assert '<span class="newthought">Text with <em>emphasis</em></span>' in result
