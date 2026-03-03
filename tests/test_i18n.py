"""Tests for internationalization functions."""

import pytest
from pathlib import Path

from build import format_date, get_other_lang, find_content_pairs


class TestFormatDate:
    """Tests for date formatting across languages."""

    def test_format_date_english_default(self) -> None:
        """Default language is English."""
        assert format_date("2026-02-21") == "February 21, 2026"

    def test_format_date_english_explicit(self) -> None:
        """Explicit English formatting."""
        assert format_date("2026-02-21", "en") == "February 21, 2026"

    def test_format_date_english_january(self) -> None:
        """January formatting in English."""
        assert format_date("2026-01-10") == "January 10, 2026"

    def test_format_date_different_months_english(self) -> None:
        """Format dates with various months in English."""
        assert format_date("2026-06-15") == "June 15, 2026"
        assert format_date("2026-12-25") == "December 25, 2026"

    def test_format_date_portuguese(self) -> None:
        """Portuguese date format: day de month de year."""
        assert format_date("2026-02-21", "pt") == "21 de fevereiro de 2026"

    def test_format_date_portuguese_january(self) -> None:
        """Portuguese January."""
        assert format_date("2026-01-10", "pt") == "10 de janeiro de 2026"

    def test_format_date_portuguese_december(self) -> None:
        """Portuguese December."""
        assert format_date("2026-12-25", "pt") == "25 de dezembro de 2026"

    def test_format_date_portuguese_march(self) -> None:
        """Portuguese March (with cedilla)."""
        result = format_date("2026-03-15", "pt")
        assert "março" in result

    def test_format_date_invalid_returns_original(self) -> None:
        """Invalid date returns original regardless of language."""
        assert format_date("not-a-date", "pt") == "not-a-date"
        assert format_date("not-a-date", "en") == "not-a-date"

    def test_format_date_wrong_format_returns_original(self) -> None:
        """Non-ISO date format returns the original string."""
        assert format_date("01/10/2025") == "01/10/2025"

    def test_format_date_empty_string(self) -> None:
        """Empty string returns empty string."""
        assert format_date("") == ""


class TestGetOtherLang:
    """Tests for language alternation."""

    def test_en_to_pt(self) -> None:
        assert get_other_lang("en") == "pt"

    def test_pt_to_en(self) -> None:
        assert get_other_lang("pt") == "en"


class TestFindContentPairs:
    """Tests for content pairing across languages."""

    def test_find_pairs_both_languages(self, tmp_path: Path) -> None:
        """Content exists in both languages."""
        en_dir = tmp_path / "en"
        pt_dir = tmp_path / "pt"
        en_dir.mkdir()
        pt_dir.mkdir()
        (en_dir / "hello.md").write_text("hello")
        (pt_dir / "hello.md").write_text("ola")

        pairs = find_content_pairs(tmp_path)

        assert "hello" in pairs
        assert "en" in pairs["hello"]
        assert "pt" in pairs["hello"]

    def test_find_pairs_single_language(self, tmp_path: Path) -> None:
        """Content exists in only one language."""
        en_dir = tmp_path / "en"
        en_dir.mkdir()
        (en_dir / "only-english.md").write_text("hello")

        pairs = find_content_pairs(tmp_path)

        assert "only-english" in pairs
        assert "en" in pairs["only-english"]
        assert "pt" not in pairs["only-english"]

    def test_find_pairs_empty(self, tmp_path: Path) -> None:
        """No content in any language."""
        pairs = find_content_pairs(tmp_path)
        assert pairs == {}

    def test_find_pairs_multiple_slugs(self, tmp_path: Path) -> None:
        """Multiple content files across languages."""
        en_dir = tmp_path / "en"
        pt_dir = tmp_path / "pt"
        en_dir.mkdir()
        pt_dir.mkdir()
        (en_dir / "post-a.md").write_text("a")
        (en_dir / "post-b.md").write_text("b")
        (pt_dir / "post-a.md").write_text("a-pt")

        pairs = find_content_pairs(tmp_path)

        assert len(pairs) == 2
        assert "en" in pairs["post-a"] and "pt" in pairs["post-a"]
        assert "en" in pairs["post-b"] and "pt" not in pairs["post-b"]
