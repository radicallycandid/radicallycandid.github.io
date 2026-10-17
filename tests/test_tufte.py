"""Tests for Tufte-specific conversions."""

from build import markdown_to_html


def convert(text: str) -> str:
    """Run text through the full markdown pipeline and return the HTML."""
    html, _ = markdown_to_html(text)
    return html


class TestConvertSidenotes:
    """Tests for sidenote and marginnote conversion."""

    def test_convert_single_sidenote(self) -> None:
        """Convert a single sidenote."""
        result = convert("Some text{sn}This is a sidenote.{/sn} continues here.")

        assert result == (
            '<p>Some text<label for="sn-1" class="margin-toggle sidenote-number"></label>'
            '<input type="checkbox" id="sn-1" class="margin-toggle"/>'
            '<span class="sidenote">This is a sidenote.</span> continues here.</p>'
        )

    def test_convert_single_marginnote(self) -> None:
        """Convert a single margin note."""
        result = convert("Some text{mn}This is a margin note.{/mn} continues here.")

        assert result == (
            '<p>Some text<label for="mn-1" class="margin-toggle">&#8853;</label>'
            '<input type="checkbox" id="mn-1" class="margin-toggle"/>'
            '<span class="marginnote">This is a margin note.</span> continues here.</p>'
        )

    def test_sidenotes_are_numbered_sequentially(self) -> None:
        """Multiple sidenotes get sequential IDs."""
        result = convert("First{sn}Note 1{/sn} and second{sn}Note 2{/sn}.")

        assert 'id="sn-1"' in result
        assert 'id="sn-2"' in result

    def test_marginnotes_are_numbered_sequentially(self) -> None:
        """Multiple marginnotes get sequential IDs."""
        result = convert("First{mn}Note 1{/mn} and second{mn}Note 2{/mn}.")

        assert 'id="mn-1"' in result
        assert 'id="mn-2"' in result

    def test_mixed_sidenotes_and_marginnotes(self) -> None:
        """Sidenotes and marginnotes share the counter, in document order."""
        result = convert("A{mn}Marginnote{/mn} and{sn}Sidenote{/sn}.")

        assert 'id="mn-1"' in result
        assert 'id="sn-2"' in result

    def test_numbering_spans_paragraphs(self) -> None:
        """IDs stay unique across paragraphs and nested elements."""
        result = convert("*A{sn}one{/sn}*\n\nB{mn}two{/mn}\n\n- C{sn}three{/sn}")

        assert result.index('id="sn-1"') < result.index('id="mn-2"')
        assert result.index('id="mn-2"') < result.index('id="sn-3"')

    def test_sidenote_with_markdown_content(self) -> None:
        """Inline markdown inside a note still renders."""
        result = convert("Text{sn}Note with **bold**, `code` and [a link](https://x.y).{/sn}.")

        assert (
            '<span class="sidenote">Note with <strong>bold</strong>, <code>code</code> '
            'and <a href="https://x.y">a link</a>.</span>'
        ) in result

    def test_multiline_sidenote(self) -> None:
        """Sidenotes can span multiple lines inside a paragraph."""
        result = convert("Text{sn}This is a\nmultiline sidenote.{/sn} continues.")

        assert '<span class="sidenote">This is a\nmultiline sidenote.</span>' in result

    def test_no_sidenotes_unchanged(self) -> None:
        """Text without sidenotes passes through unchanged."""
        assert convert("Just regular text.") == "<p>Just regular text.</p>"

    def test_marginnote_has_plus_symbol(self) -> None:
        """Marginnotes display the ⊕ symbol."""
        result = convert("Text{mn}A margin note.{/mn}.")

        assert "&#8853;" in result  # ⊕ symbol


class TestTufteSyntaxInCode:
    """Tufte syntax inside code stays literal."""

    def test_inline_code_stays_literal(self) -> None:
        """A note inside a code span is not converted."""
        result = convert("Write `{sn}x{/sn}`, `{mn}y{/mn}` or `{nt}z{/nt}`.")

        assert "<code>{sn}x{/sn}</code>" in result
        assert "<code>{mn}y{/mn}</code>" in result
        assert "<code>{nt}z{/nt}</code>" in result
        assert "margin-toggle" not in result
        assert "newthought" not in result

    def test_fenced_block_stays_literal(self) -> None:
        """A note inside a fenced code block is not converted."""
        result = convert("```\n{sn}x{/sn} and {nt}y{/nt}\n```")

        assert "{sn}x{/sn} and {nt}y{/nt}" in result
        assert "margin-toggle" not in result
        assert "newthought" not in result

    def test_real_note_next_to_code_still_converts(self) -> None:
        """A real note after a code span converts and skips the code's IDs."""
        result = convert("Use `{sn}x{/sn}`.{sn}Real note.{/sn}")

        assert "<code>{sn}x{/sn}</code>" in result
        assert '<span class="sidenote">Real note.</span>' in result
        assert 'id="sn-1"' in result


class TestConvertNewthought:
    """Tests for newthought conversion."""

    def test_convert_newthought(self) -> None:
        """Convert newthought syntax to span."""
        result = convert("{nt}The beginning{/nt} of a new section.")

        assert result == '<p><span class="newthought">The beginning</span> of a new section.</p>'

    def test_multiple_newthoughts(self) -> None:
        """Multiple newthoughts are converted."""
        result = convert("{nt}First{/nt} paragraph. {nt}Second{/nt} paragraph.")

        assert result.count('<span class="newthought">') == 2

    def test_no_newthought_unchanged(self) -> None:
        """Text without newthought passes through unchanged."""
        assert convert("Regular text without newthought.") == (
            "<p>Regular text without newthought.</p>"
        )

    def test_newthought_with_formatting(self) -> None:
        """Newthought can contain other formatting."""
        result = convert("{nt}Text with *emphasis*{/nt} here.")

        assert '<span class="newthought">Text with <em>emphasis</em></span>' in result
