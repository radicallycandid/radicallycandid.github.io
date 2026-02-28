#!/usr/bin/env python3
"""
Static site generator for vmargato.com.

Converts markdown files to HTML using Tufte CSS styling with support for
sidenotes, margin notes, and newthought spans.

Usage:
    python build.py          # Build the site
    python build.py serve    # Build and start local server
    python build.py clean    # Remove output directory
"""

from __future__ import annotations

import argparse
import http.server
import re
import shutil
import socketserver
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

# Use markdown library if available, otherwise fallback to basic conversion
try:
    import markdown

    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Warning: 'markdown' library not found. Install with: pip install markdown")
    print("Using basic markdown conversion (limited features).")


# =============================================================================
# Exceptions
# =============================================================================


class BuildError(Exception):
    """Base exception for build errors with user-friendly messages."""

    pass


class FrontmatterError(BuildError):
    """Error in post frontmatter."""

    pass


class TemplateError(BuildError):
    """Error in template rendering."""

    pass


# =============================================================================
# Configuration
# =============================================================================

ROOT_DIR = Path(__file__).parent
POSTS_DIR = ROOT_DIR / "posts"
PAGES_DIR = ROOT_DIR / "pages"
TEMPLATES_DIR = ROOT_DIR / "templates"
OUTPUT_DIR = ROOT_DIR / "output"
STATIC_DIR = ROOT_DIR / "static"

# Site metadata
SITE_TITLE = "Vitor Margato"
SITE_URL = "https://vmargato.com"

# Internationalization
LANGUAGES = ["en", "pt"]
DEFAULT_LANG = "en"

I18N = {
    "en": {
        "published_label": "Published",
        "updated_label": "Updated",
        "site_description": f"Personal site of {SITE_TITLE}",
    },
    "pt": {
        "published_label": "Publicado",
        "updated_label": "Atualizado",
        "site_description": f"Site pessoal de {SITE_TITLE}",
    },
}

PT_MONTHS = {
    "January": "janeiro",
    "February": "fevereiro",
    "March": "março",
    "April": "abril",
    "May": "maio",
    "June": "junho",
    "July": "julho",
    "August": "agosto",
    "September": "setembro",
    "October": "outubro",
    "November": "novembro",
    "December": "dezembro",
}

# Inline SVG flags for language selector (simplified circular flags)
LANG_FLAGS = {
    "en": (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        '<clipPath id="fc"><circle cx="50" cy="50" r="50"/></clipPath>'
        '<g clip-path="url(#fc)">'
        '<rect width="100" height="100" fill="#bf0a30"/>'
        '<rect y="8" width="100" height="7.7" fill="#fff"/>'
        '<rect y="23" width="100" height="7.7" fill="#fff"/>'
        '<rect y="38" width="100" height="7.7" fill="#fff"/>'
        '<rect y="54" width="100" height="7.7" fill="#fff"/>'
        '<rect y="69" width="100" height="7.7" fill="#fff"/>'
        '<rect y="84" width="100" height="7.7" fill="#fff"/>'
        '<rect width="42" height="54" fill="#002868"/>'
        '</g></svg>'
    ),
    "pt": (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        '<clipPath id="fc"><circle cx="50" cy="50" r="50"/></clipPath>'
        '<g clip-path="url(#fc)">'
        '<rect width="100" height="100" fill="#009c3b"/>'
        '<polygon points="5,50 50,10 95,50 50,90" fill="#ffdf00"/>'
        '<circle cx="50" cy="50" r="20" fill="#002776"/>'
        '<circle cx="50" cy="50" r="17" fill="none" stroke="#fff" stroke-width="1.5"/>'
        '</g></svg>'
    ),
}

# Minimum number of headings required to show table of contents
MIN_HEADINGS_FOR_TOC = 3

# Default port for local development server
DEFAULT_SERVER_PORT = 8000

# Date format for display
DATE_FORMAT_INPUT = "%Y-%m-%d"
DATE_FORMAT_OUTPUT = "%B %d, %Y"  # e.g., "January 10, 2026"


# =============================================================================
# Frontmatter Parsing
# =============================================================================


def parse_frontmatter(content: str, filepath: Path | None = None) -> tuple[dict[str, str], str]:
    """
    Parse YAML-like frontmatter from markdown content.

    Frontmatter is delimited by --- at the start of the file:

        ---
        title: My Post
        date: 2026-01-10
        ---

        Content here...

    Args:
        content: Raw markdown file content.
        filepath: Optional path for error messages.

    Returns:
        Tuple of (frontmatter dict, body content).

    Raises:
        FrontmatterError: If frontmatter is malformed.
    """
    frontmatter: dict[str, str] = {}
    body = content
    location = f" in {filepath}" if filepath else ""

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise FrontmatterError(
                f"Malformed frontmatter{location}: missing closing '---'"
            )

        fm_text = parts[1].strip()
        body = parts[2].strip()

        for line_num, line in enumerate(fm_text.split("\n"), start=2):
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                raise FrontmatterError(
                    f"Invalid frontmatter{location} at line {line_num}: "
                    f"expected 'key: value', got '{line}'"
                )
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, body


def validate_frontmatter(
    frontmatter: dict[str, str], filepath: Path | None = None
) -> list[str]:
    """
    Validate frontmatter and return list of warnings.

    Args:
        frontmatter: Parsed frontmatter dictionary.
        filepath: Optional path for warning messages.

    Returns:
        List of warning messages (empty if all is well).
    """
    warnings: list[str] = []
    location = filepath.name if filepath else "post"

    # Check for recommended fields
    if "title" not in frontmatter:
        warnings.append(f"{location}: missing 'title' in frontmatter (using filename)")

    if "date" not in frontmatter:
        warnings.append(f"{location}: missing 'date' in frontmatter (using file mtime)")

    if "excerpt" not in frontmatter:
        warnings.append(f"{location}: missing 'excerpt' (index page will show no description)")

    # Validate date format if present
    if "date" in frontmatter:
        try:
            datetime.strptime(frontmatter["date"], DATE_FORMAT_INPUT)
        except ValueError:
            warnings.append(
                f"{location}: invalid date format '{frontmatter['date']}' "
                f"(expected YYYY-MM-DD)"
            )

    return warnings


# =============================================================================
# Tufte-Specific Conversions
# =============================================================================


def convert_sidenotes(html: str) -> str:
    """
    Convert custom sidenote/marginnote syntax to Tufte HTML.

    Syntax:
        {sn}This is a sidenote{/sn}  -> numbered sidenote
        {mn}This is a margin note{/mn} -> unnumbered margin note

    Args:
        html: HTML content with sidenote syntax.

    Returns:
        HTML with Tufte sidenote markup.
    """
    sidenote_counter = [0]  # Use list to allow modification in nested function

    def replace_sidenote(match: re.Match[str]) -> str:
        sidenote_counter[0] += 1
        note_id = f"sn-{sidenote_counter[0]}"
        content = match.group(1)
        return (
            f'<label for="{note_id}" class="margin-toggle sidenote-number"></label>'
            f'<input type="checkbox" id="{note_id}" class="margin-toggle"/>'
            f'<span class="sidenote">{content}</span>'
        )

    def replace_marginnote(match: re.Match[str]) -> str:
        sidenote_counter[0] += 1
        note_id = f"mn-{sidenote_counter[0]}"
        content = match.group(1)
        return (
            f'<label for="{note_id}" class="margin-toggle">&#8853;</label>'
            f'<input type="checkbox" id="{note_id}" class="margin-toggle"/>'
            f'<span class="marginnote">{content}</span>'
        )

    html = re.sub(r"\{sn\}(.*?)\{/sn\}", replace_sidenote, html, flags=re.DOTALL)
    html = re.sub(r"\{mn\}(.*?)\{/mn\}", replace_marginnote, html, flags=re.DOTALL)

    return html


def convert_newthought(html: str) -> str:
    """
    Convert {nt}Text{/nt} to Tufte newthought spans.

    Newthought is used to begin a new section with small-caps styling.

    Args:
        html: HTML content with newthought syntax.

    Returns:
        HTML with newthought spans.
    """
    return re.sub(
        r"\{nt\}(.*?)\{/nt\}", r'<span class="newthought">\1</span>', html
    )


# =============================================================================
# Basic Markdown Conversion (Fallback)
# =============================================================================


def basic_markdown_to_html(text: str) -> str:
    """
    Basic markdown conversion without external libraries.

    Supports: headers, bold, italic, inline code, links, lists, tables,
    code blocks, and paragraphs.

    Args:
        text: Markdown text to convert.

    Returns:
        HTML string.
    """
    # Extract and protect code blocks first (they may contain blank lines)
    code_blocks: list[str] = []

    def save_code_block(match: re.Match[str]) -> str:
        code_blocks.append(match.group(2))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

    text = re.sub(r"```(\w*)\n(.*?)```", save_code_block, text, flags=re.DOTALL)

    # Headers (process h3 before h2 before h1 to avoid conflicts)
    text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)

    # Process lists and tables
    text = _convert_lists(text)
    text = _convert_tables(text)

    # Paragraphs - split on blank lines
    text = _wrap_paragraphs(text)

    # Restore code blocks
    for i, code in enumerate(code_blocks):
        text = text.replace(f"__CODE_BLOCK_{i}__", f"<pre><code>{code}</code></pre>")

    return text


def _convert_lists(text: str) -> str:
    """Convert markdown lists (- item and 1. item) to HTML ul/ol."""
    lines = text.split("\n")
    result: list[str] = []
    in_list = False
    list_type: str | None = None
    list_items: list[str] = []

    ol_pattern = re.compile(r"^(\d+)\.\s+(.+)$")

    for line in lines:
        stripped = line.strip()
        ol_match = ol_pattern.match(stripped)

        if stripped.startswith("- "):
            if in_list and list_type != "ul":
                result.append(_render_list(list_type, list_items))
                list_items = []
            in_list = True
            list_type = "ul"
            list_items.append(stripped[2:])
        elif ol_match:
            if in_list and list_type != "ol":
                result.append(_render_list(list_type, list_items))
                list_items = []
            in_list = True
            list_type = "ol"
            list_items.append(ol_match.group(2))
        else:
            if in_list:
                result.append(_render_list(list_type, list_items))
                list_items = []
                in_list = False
                list_type = None
            result.append(line)

    if in_list:
        result.append(_render_list(list_type, list_items))

    return "\n".join(result)


def _render_list(list_type: str | None, items: list[str]) -> str:
    """Render a list as HTML."""
    if not list_type or not items:
        return ""
    li_items = "\n".join(f"<li>{item}</li>" for item in items)
    return f"<{list_type}>\n{li_items}\n</{list_type}>"


def _convert_tables(content: str) -> str:
    """Convert markdown tables to HTML tables."""
    lines = content.split("\n")
    result: list[str] = []
    in_table = False
    table_rows: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
            table_rows.append(stripped)
        else:
            if in_table:
                result.append(_render_table(table_rows))
                table_rows = []
                in_table = False
            result.append(line)

    if in_table:
        result.append(_render_table(table_rows))

    return "\n".join(result)


def _render_table(rows: list[str]) -> str:
    """Render table rows as HTML."""
    if len(rows) < 2:
        return "\n".join(rows)

    html = ["<table>"]

    # First row is header
    header_cells = [cell.strip() for cell in rows[0].split("|")[1:-1]]
    html.append("<thead><tr>")
    for cell in header_cells:
        html.append(f"<th>{cell}</th>")
    html.append("</tr></thead>")

    # Skip separator row, remaining rows are body
    html.append("<tbody>")
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.split("|")[1:-1]]
        html.append("<tr>")
        for cell in cells:
            html.append(f"<td>{cell}</td>")
        html.append("</tr>")
    html.append("</tbody>")

    html.append("</table>")
    return "\n".join(html)


def _wrap_paragraphs(text: str) -> str:
    """Wrap non-block content in paragraph tags."""
    paragraphs = text.split("\n\n")
    processed: list[str] = []

    block_prefixes = ("<h", "<pre", "<ul", "<ol", "<table", "__CODE_BLOCK_")

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if any(p.startswith(prefix) for prefix in block_prefixes):
            processed.append(p)
        else:
            processed.append(f"<p>{p}</p>")

    return "\n\n".join(processed)


# =============================================================================
# Table of Contents
# =============================================================================


def extract_headings(html: str) -> list[dict[str, str | int]]:
    """
    Extract h2 and h3 headings from HTML for table of contents.

    Args:
        html: HTML content to scan.

    Returns:
        List of heading dicts with 'level', 'id', and 'text' keys.
    """
    headings: list[dict[str, str | int]] = []
    pattern = r'<h([23])(?:\s+id="([^"]*)")?[^>]*>(.*?)</h\1>'

    for match in re.finditer(pattern, html, re.DOTALL):
        level = int(match.group(1))
        existing_id = match.group(2)
        text = match.group(3)

        # Strip HTML tags from heading text
        clean_text = re.sub(r"<[^>]+>", "", text).strip()

        # Generate ID if needed
        if existing_id:
            heading_id = existing_id
        else:
            heading_id = re.sub(r"[^\w\s-]", "", clean_text.lower())
            heading_id = re.sub(r"[\s]+", "-", heading_id)

        headings.append({"level": level, "id": heading_id, "text": clean_text})

    return headings


def add_heading_ids(html: str, headings: list[dict[str, str | int]]) -> str:
    """
    Add IDs to h2 and h3 tags that don't have them.

    Args:
        html: HTML content.
        headings: List of heading metadata from extract_headings().

    Returns:
        HTML with IDs added to headings.
    """
    heading_index = 0

    def add_id(match: re.Match[str]) -> str:
        nonlocal heading_index
        if heading_index >= len(headings):
            return match.group(0)

        tag = match.group(1)
        existing_id = match.group(2)
        attrs = match.group(3) or ""
        content = match.group(4)

        heading = headings[heading_index]
        heading_index += 1

        if existing_id:
            return match.group(0)
        return f'<h{tag} id="{heading["id"]}"{attrs}>{content}</h{tag}>'

    pattern = r'<h([23])(?:\s+id="([^"]*)")?(\s[^>]*)?>(.+?)</h\1>'
    return re.sub(pattern, add_id, html, flags=re.DOTALL)


def generate_toc_html(headings: list[dict[str, str | int]]) -> str:
    """
    Generate HTML for the table of contents.

    Args:
        headings: List of heading metadata from extract_headings().

    Returns:
        HTML string for the ToC navigation.
    """
    if not headings:
        return ""

    lines = ['<nav class="toc" aria-label="Table of contents">', '<ul class="toc-list">']

    for heading in headings:
        level_class = "toc-h2" if heading["level"] == 2 else "toc-h3"
        lines.append(
            f'<li class="{level_class}">'
            f'<a href="#{heading["id"]}">{heading["text"]}</a>'
            f"</li>"
        )

    lines.append("</ul>")
    lines.append("</nav>")

    return "\n".join(lines)


# =============================================================================
# Markdown to HTML Conversion
# =============================================================================


def markdown_to_html(text: str) -> tuple[str, list[dict[str, str | int]]]:
    """
    Convert markdown to HTML with Tufte extensions.

    Args:
        text: Markdown content.

    Returns:
        Tuple of (HTML string, list of headings).
    """
    if HAS_MARKDOWN:
        md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
        html = md.convert(text)
    else:
        html = basic_markdown_to_html(text)

    # Apply Tufte-specific conversions
    html = convert_sidenotes(html)
    html = convert_newthought(html)

    # Extract headings for ToC
    headings = extract_headings(html)

    # Add IDs to headings that don't have them
    html = add_heading_ids(html, headings)

    return html, headings


# =============================================================================
# Template Rendering
# =============================================================================


def render_template(template_name: str, context: dict[str, object]) -> str:
    """
    Simple template rendering with mustache-like syntax.

    Supports:
        {{variable}} - Variable substitution
        {{#key}}...{{/key}} - Conditionals and loops

    Args:
        template_name: Name of template file in templates directory.
        context: Dictionary of template variables.

    Returns:
        Rendered HTML string.
    """
    template_path = TEMPLATES_DIR / template_name
    template = template_path.read_text()

    def render_content(content: str, ctx: dict[str, object]) -> str:
        def replace_block(match: re.Match[str]) -> str:
            key = match.group(1)
            inner = match.group(2)
            value = ctx.get(key)

            if isinstance(value, list):
                result = []
                for item in value:
                    rendered = inner
                    if isinstance(item, dict):
                        rendered = render_content(rendered, item)
                    result.append(rendered)
                return "".join(result)
            elif value:
                return render_content(inner, ctx)
            return ""

        content = re.sub(
            r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}", replace_block, content, flags=re.DOTALL
        )

        # Simple variable replacement
        for key, value in ctx.items():
            if not isinstance(value, list):
                content = content.replace("{{" + key + "}}", str(value) if value else "")

        return content

    return render_content(template, context)


# =============================================================================
# Date Formatting
# =============================================================================


def format_date(date_str: str, lang: str = "en") -> str:
    """
    Format a date string to human-readable format.

    Args:
        date_str: Date in YYYY-MM-DD format.
        lang: Language code ("en" or "pt").

    Returns:
        Formatted date string (e.g., "January 10, 2026" or "10 de janeiro de 2026").
    """
    try:
        dt = datetime.strptime(date_str, DATE_FORMAT_INPUT)
        if lang == "pt":
            month_en = dt.strftime("%B")
            month_pt = PT_MONTHS.get(month_en, month_en)
            return f"{dt.day} de {month_pt} de {dt.year}"
        return dt.strftime(DATE_FORMAT_OUTPUT)
    except ValueError:
        return date_str


def get_other_lang(lang: str) -> str:
    """Return the alternate language code."""
    return "en" if lang == "pt" else "pt"


def find_content_pairs(content_dir: Path) -> dict[str, dict[str, Path]]:
    """
    Find content files across languages and pair them by slug.

    Args:
        content_dir: Base content directory (e.g., POSTS_DIR or PAGES_DIR).

    Returns:
        Dict mapping slug to {lang: Path}, e.g. {"hello-world": {"en": Path, "pt": Path}}.
    """
    pairs: dict[str, dict[str, Path]] = {}
    for lang in LANGUAGES:
        lang_dir = content_dir / lang
        if lang_dir.exists():
            for md in sorted(lang_dir.glob("*.md")):
                slug = md.stem
                if slug not in pairs:
                    pairs[slug] = {}
                pairs[slug][lang] = md
    return pairs


# =============================================================================
# Build Functions
# =============================================================================


def build_post(
    md_path: Path,
    lang: str,
    has_alternate: bool = False,
    warnings: list[str] | None = None,
) -> dict[str, object]:
    """
    Build a single post and return its metadata.

    Args:
        md_path: Path to markdown source file.
        lang: Language code ("en" or "pt").
        has_alternate: Whether an alternate language version exists.
        warnings: Optional list to collect validation warnings.

    Returns:
        Dictionary of post metadata for index page.

    Raises:
        BuildError: If the post cannot be built.
    """
    try:
        content = md_path.read_text()
    except OSError as e:
        raise BuildError(f"Cannot read {md_path}: {e}") from e

    frontmatter, body = parse_frontmatter(content, md_path)

    # Validate and collect warnings
    if warnings is not None:
        warnings.extend(validate_frontmatter(frontmatter, md_path))

    # Extract metadata
    title = frontmatter.get("title", md_path.stem.replace("-", " ").title())
    subtitle = frontmatter.get("subtitle", "")
    excerpt = frontmatter.get("excerpt", "")

    # Get dates
    published_date = frontmatter.get("date", "")
    file_mtime = datetime.fromtimestamp(md_path.stat().st_mtime)
    updated_date = file_mtime.strftime(DATE_FORMAT_INPUT)

    if not published_date:
        published_date = updated_date

    was_updated = updated_date != published_date

    # Convert body to HTML
    body_html, headings = markdown_to_html(body)

    # Generate table of contents
    toc_html = generate_toc_html(headings)
    has_toc = len(headings) >= MIN_HEADINGS_FOR_TOC

    # i18n
    strings = I18N[lang]
    other = get_other_lang(lang)
    output_name = md_path.stem + ".html"

    # Render templates
    post_content = render_template(
        "post.html",
        {
            "title": title,
            "subtitle": subtitle,
            "published_date": format_date(published_date, lang),
            "updated_date": format_date(updated_date, lang) if was_updated else "",
            "was_updated": was_updated,
            "body": body_html,
            "toc": toc_html,
            "has_toc": has_toc,
            "root": "../../",
            "published_label": strings["published_label"],
            "updated_label": strings["updated_label"],
        },
    )

    full_html = render_template(
        "base.html",
        {
            "title": title,
            "content": post_content,
            "description": excerpt,
            "og_type": "article",
            "root": "../../",
            "lang": lang,
            "other_lang": other,
            "has_alternate": has_alternate,
            "other_lang_url": f"../../{other}/posts/{output_name}",
            "lang_flag": LANG_FLAGS[other],
            "home_url": f"../../{lang}/index.html",
        },
    )

    # Write output
    output_path = OUTPUT_DIR / lang / "posts" / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html)

    print(f"  Built: {output_path.relative_to(ROOT_DIR)}")

    return {
        "title": title,
        "published_date": published_date,
        "published_date_formatted": format_date(published_date, lang),
        "updated_date": updated_date,
        "updated_date_formatted": format_date(updated_date, lang),
        "was_updated": was_updated,
        "excerpt": excerpt,
        "url": f"posts/{output_name}",
        "path": md_path,
    }


def build_index(posts: list[dict[str, object]], lang: str) -> None:
    """
    Build the index page for a given language.

    Args:
        posts: List of post metadata dictionaries.
        lang: Language code ("en" or "pt").
    """
    strings = I18N[lang]
    other = get_other_lang(lang)

    posts = sorted(posts, key=lambda p: str(p["updated_date"]), reverse=True)

    # Add translated updated label to each post item for the template loop
    for post in posts:
        post["updated_label"] = strings["updated_label"]

    # Load about page content for the homepage
    about_path = PAGES_DIR / lang / "about.md"
    about_html = ""
    if about_path.exists():
        about_raw = about_path.read_text()
        _, about_body = parse_frontmatter(about_raw, about_path)
        about_html, _ = markdown_to_html(about_body)

    index_content = render_template("index.html", {"posts": posts, "about_html": about_html})
    full_html = render_template(
        "base.html",
        {
            "title": "Home",
            "content": index_content,
            "description": strings["site_description"],
            "og_type": "website",
            "root": "../",
            "lang": lang,
            "other_lang": other,
            "has_alternate": True,
            "other_lang_url": f"../{other}/index.html",
            "lang_flag": LANG_FLAGS[other],
            "home_url": f"../{lang}/index.html",
        },
    )

    output_path = OUTPUT_DIR / lang / "index.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html)
    print(f"  Built: {output_path.relative_to(ROOT_DIR)}")


def build_page(
    md_path: Path,
    lang: str,
    has_alternate: bool = False,
) -> None:
    """
    Build a single standalone page (e.g. About).

    Pages are simpler than posts: no date required, no listing.
    Output goes to output/{lang}/slug.html.

    Args:
        md_path: Path to markdown source file.
        lang: Language code ("en" or "pt").
        has_alternate: Whether an alternate language version exists.
    """
    try:
        content = md_path.read_text()
    except OSError as e:
        raise BuildError(f"Cannot read {md_path}: {e}") from e

    frontmatter, body = parse_frontmatter(content, md_path)

    title = frontmatter.get("title", md_path.stem.replace("-", " ").title())
    subtitle = frontmatter.get("subtitle", "")
    description = frontmatter.get("description", frontmatter.get("excerpt", ""))

    body_html, headings = markdown_to_html(body)
    toc_html = generate_toc_html(headings)
    has_toc = len(headings) >= MIN_HEADINGS_FOR_TOC

    strings = I18N[lang]
    other = get_other_lang(lang)
    output_name = md_path.stem + ".html"

    page_content = render_template(
        "page.html",
        {
            "title": title,
            "subtitle": subtitle,
            "body": body_html,
            "toc": toc_html,
            "has_toc": has_toc,
            "root": "../",
        },
    )

    full_html = render_template(
        "base.html",
        {
            "title": title,
            "content": page_content,
            "description": description,
            "og_type": "website",
            "root": "../",
            "lang": lang,
            "other_lang": other,
            "has_alternate": has_alternate,
            "other_lang_url": f"../{other}/{output_name}",
            "lang_flag": LANG_FLAGS[other],
            "home_url": f"../{lang}/index.html",
        },
    )

    output_path = OUTPUT_DIR / lang / (md_path.stem + ".html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html)
    print(f"  Built: {output_path.relative_to(ROOT_DIR)}")


def build_feed(posts: list[dict[str, object]], lang: str) -> None:
    """
    Generate an Atom feed from published posts.

    Args:
        posts: List of post metadata dictionaries.
        lang: Language code ("en" or "pt").
    """
    posts = sorted(posts, key=lambda p: str(p["published_date"]), reverse=True)

    entries: list[str] = []
    for post in posts[:20]:
        entries.append(
            f"  <entry>\n"
            f"    <title>{xml_escape(str(post['title']))}</title>\n"
            f"    <link href=\"{SITE_URL}/{lang}/{post['url']}\"/>\n"
            f"    <id>{SITE_URL}/{lang}/{post['url']}</id>\n"
            f"    <updated>{post['published_date']}T00:00:00Z</updated>\n"
            f"    <summary>{xml_escape(str(post.get('excerpt', '')))}</summary>\n"
            f"  </entry>"
        )

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    feed = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{lang}">\n'
        f"  <title>{SITE_TITLE}</title>\n"
        f'  <link href="{SITE_URL}/{lang}/feed.xml" rel="self"/>\n'
        f'  <link href="{SITE_URL}/{lang}/"/>\n'
        f"  <updated>{now}</updated>\n"
        f"  <id>{SITE_URL}/{lang}/</id>\n"
        f"  <author>\n"
        f"    <name>{SITE_TITLE}</name>\n"
        f"  </author>\n"
        + "\n".join(entries) + "\n"
        "</feed>\n"
    )

    output_path = OUTPUT_DIR / lang / "feed.xml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(feed)
    print(f"  Built: {output_path.relative_to(ROOT_DIR)}")


def copy_static() -> None:
    """Copy static assets to output directory."""
    output_static = OUTPUT_DIR / "static"
    if output_static.exists():
        shutil.rmtree(output_static)
    shutil.copytree(STATIC_DIR, output_static)
    print("  Copied: static/")


def build_root_redirect() -> None:
    """
    Build the root index.html that redirects to the default language.

    Checks localStorage for explicit preference, then navigator.language,
    then falls back to DEFAULT_LANG.
    """
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="alternate" hreflang="en" href="{SITE_URL}/en/index.html">
    <link rel="alternate" hreflang="pt" href="{SITE_URL}/pt/index.html">
    <link rel="alternate" hreflang="x-default" href="{SITE_URL}/{DEFAULT_LANG}/index.html">
    <script>
        (function() {{
            var pref = localStorage.getItem('lang-preference');
            if (pref && (pref === 'en' || pref === 'pt')) {{
                window.location.replace('/' + pref + '/index.html');
                return;
            }}
            var lang = (navigator.language || '').toLowerCase();
            if (lang.startsWith('pt')) {{
                window.location.replace('/pt/index.html');
            }} else {{
                window.location.replace('/{DEFAULT_LANG}/index.html');
            }}
        }})();
    </script>
    <meta http-equiv="refresh" content="0;url=/{DEFAULT_LANG}/index.html">
</head>
<body></body>
</html>"""
    output_path = OUTPUT_DIR / "index.html"
    output_path.write_text(html)
    print(f"  Built: {output_path.relative_to(ROOT_DIR)} (redirect)")


def clean() -> None:
    """Remove the output directory."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"Cleaned: {OUTPUT_DIR}")
    else:
        print("Nothing to clean.")


def build() -> bool:
    """
    Build the entire site in all configured languages.

    Returns:
        True if build succeeded, False if there were errors.
    """
    print("Building site...")
    print()

    warnings: list[str] = []
    errors: list[str] = []

    # Validate required directories
    if not TEMPLATES_DIR.exists():
        print(f"Error: Templates directory not found: {TEMPLATES_DIR}")
        return False

    if not STATIC_DIR.exists():
        print(f"Error: Static directory not found: {STATIC_DIR}")
        return False

    # Clean and create output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    # Copy static files (shared across languages)
    copy_static()

    # Find content pairs across languages
    post_pairs = find_content_pairs(POSTS_DIR)
    page_pairs = find_content_pairs(PAGES_DIR)

    total_posts = 0
    total_pages = 0

    for lang in LANGUAGES:
        print(f"  [{lang.upper()}]")

        # Build posts for this language
        posts: list[dict[str, object]] = []
        for slug, lang_paths in sorted(post_pairs.items()):
            if lang not in lang_paths:
                continue
            has_alternate = get_other_lang(lang) in lang_paths
            try:
                post_meta = build_post(lang_paths[lang], lang, has_alternate, warnings)
                posts.append(post_meta)
            except BuildError as e:
                errors.append(str(e))
                print(f"    Error: {e}")

        # Build index
        build_index(posts, lang)
        total_posts += len(posts)

        # Build standalone pages (about is inlined on the homepage)
        for slug, lang_paths in sorted(page_pairs.items()):
            if slug == "about":
                continue
            if lang not in lang_paths:
                continue
            has_alternate = get_other_lang(lang) in lang_paths
            try:
                build_page(lang_paths[lang], lang, has_alternate)
                total_pages += 1
            except BuildError as e:
                errors.append(str(e))
                print(f"    Error: {e}")

        # Build Atom feed
        if posts:
            build_feed(posts, lang)

    # Build root redirect
    build_root_redirect()

    # Copy CNAME for GitHub Pages custom domain
    cname_path = ROOT_DIR / "CNAME"
    if cname_path.exists():
        shutil.copy2(cname_path, OUTPUT_DIR / "CNAME")
        print("  Copied: CNAME")

    # Print warnings
    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    # Print summary
    print()
    if errors:
        print(f"Build completed with {len(errors)} error(s).")
        return False

    print(
        f"Done! Built {total_posts} post(s) and {total_pages} page(s) "
        f"across {len(LANGUAGES)} language(s)."
    )
    print(f"Open {OUTPUT_DIR / 'index.html'} in your browser.")
    return True


def serve(port: int = DEFAULT_SERVER_PORT) -> None:
    """
    Build the site and start a local development server.

    Args:
        port: Port number for the server.
    """
    if not build():
        print("Server not started due to build errors.")
        return

    print()
    print(f"Starting server at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    print()

    import os

    os.chdir(OUTPUT_DIR)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


# =============================================================================
# CLI Entry Point
# =============================================================================


def main() -> None:
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Static site generator for vmargato.com.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python build.py          Build the site
    python build.py serve    Build and start local server
    python build.py clean    Remove output directory
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command (default)
    subparsers.add_parser("build", help="Build the site (default)")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Build and start local server")
    serve_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_SERVER_PORT,
        help=f"Port for the server (default: {DEFAULT_SERVER_PORT})",
    )

    # Clean command
    subparsers.add_parser("clean", help="Remove output directory")

    args = parser.parse_args()

    if args.command == "serve":
        serve(args.port)
    elif args.command == "clean":
        clean()
    else:
        # Default to build
        build()


if __name__ == "__main__":
    main()
