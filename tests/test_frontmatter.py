"""Tests for frontmatter parsing and validation."""

from pathlib import Path

import pytest

from build import (
    FrontmatterError,
    parse_frontmatter,
    validate_frontmatter,
)


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_parse_basic_frontmatter(self) -> None:
        """Parse frontmatter with title and date."""
        content = """---
title: My Post
date: 2026-01-10
---

Body content here."""

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["title"] == "My Post"
        assert frontmatter["date"] == "2026-01-10"
        assert body == "Body content here."

    def test_parse_frontmatter_with_subtitle_and_excerpt(self) -> None:
        """Parse frontmatter with all common fields."""
        content = """---
title: My Post
subtitle: A subtitle
date: 2026-01-10
excerpt: Brief description.
---

Body."""

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["title"] == "My Post"
        assert frontmatter["subtitle"] == "A subtitle"
        assert frontmatter["date"] == "2026-01-10"
        assert frontmatter["excerpt"] == "Brief description."

    def test_parse_frontmatter_strips_quotes(self) -> None:
        """Values with quotes should have quotes stripped."""
        content = """---
title: "Quoted Title"
subtitle: 'Single Quoted'
---

Body."""

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["title"] == "Quoted Title"
        assert frontmatter["subtitle"] == "Single Quoted"

    def test_parse_content_without_frontmatter(self) -> None:
        """Content without frontmatter returns empty dict and full content."""
        content = "Just some content without frontmatter."

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter == {}
        assert body == content

    def test_parse_frontmatter_with_colons_in_value(self) -> None:
        """Values can contain colons."""
        content = """---
title: Time is 10:30:00
---

Body."""

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["title"] == "Time is 10:30:00"

    def test_parse_frontmatter_missing_closing_delimiter(self) -> None:
        """Missing closing --- raises FrontmatterError."""
        content = """---
title: My Post

Body without closing delimiter."""

        with pytest.raises(FrontmatterError, match="missing closing '---'"):
            parse_frontmatter(content)

    def test_parse_frontmatter_invalid_line(self) -> None:
        """Line without colon raises FrontmatterError."""
        content = """---
title: My Post
invalid line without colon
---

Body."""

        with pytest.raises(FrontmatterError, match="expected 'key: value'"):
            parse_frontmatter(content)

    def test_parse_frontmatter_with_filepath_in_error(self) -> None:
        """Error messages include filepath when provided."""
        content = """---
title: My Post
invalid line
---

Body."""

        filepath = Path("posts/my-post.md")
        with pytest.raises(FrontmatterError, match="posts/my-post.md"):
            parse_frontmatter(content, filepath)

    def test_parse_frontmatter_empty_lines_ignored(self) -> None:
        """Empty lines in frontmatter are ignored."""
        content = """---
title: My Post

date: 2026-01-10

---

Body."""

        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["title"] == "My Post"
        assert frontmatter["date"] == "2026-01-10"


class TestValidateFrontmatter:
    """Tests for validate_frontmatter function."""

    def test_valid_frontmatter_no_warnings(self) -> None:
        """Complete frontmatter produces no warnings."""
        frontmatter = {
            "title": "My Post",
            "date": "2026-01-10",
            "excerpt": "A description.",
        }

        warnings = validate_frontmatter(frontmatter)

        assert warnings == []

    def test_missing_title_warning(self) -> None:
        """Missing title produces warning."""
        frontmatter = {"date": "2026-01-10", "excerpt": "A description."}

        warnings = validate_frontmatter(frontmatter)

        assert any("missing 'title'" in w for w in warnings)

    def test_missing_date_warning(self) -> None:
        """Missing date produces warning."""
        frontmatter = {"title": "My Post", "excerpt": "A description."}

        warnings = validate_frontmatter(frontmatter)

        assert any("missing 'date'" in w for w in warnings)

    def test_missing_excerpt_warning(self) -> None:
        """Missing excerpt produces warning."""
        frontmatter = {"title": "My Post", "date": "2026-01-10"}

        warnings = validate_frontmatter(frontmatter)

        assert any("missing 'excerpt'" in w for w in warnings)

    def test_invalid_date_format_warning(self) -> None:
        """Invalid date format produces warning."""
        frontmatter = {
            "title": "My Post",
            "date": "January 10, 2025",  # Wrong format
            "excerpt": "A description.",
        }

        warnings = validate_frontmatter(frontmatter)

        assert any("invalid date format" in w for w in warnings)

    def test_filepath_included_in_warnings(self) -> None:
        """Warnings include filepath when provided."""
        frontmatter = {"date": "2026-01-10"}
        filepath = Path("posts/my-post.md")

        warnings = validate_frontmatter(frontmatter, filepath)

        assert any("my-post.md" in w for w in warnings)

    def test_empty_frontmatter_all_warnings(self) -> None:
        """Empty frontmatter produces all warnings."""
        frontmatter: dict[str, str] = {}

        warnings = validate_frontmatter(frontmatter)

        assert len(warnings) == 3  # title, date, excerpt
