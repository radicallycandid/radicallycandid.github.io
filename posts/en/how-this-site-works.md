---
title: "How This Site Works"
date: 2026-03-03
draft: true
excerpt: A custom static site generator in 1,150 lines of Python. One dependency, four templates, and a build pipeline that turns Markdown into a bilingual website.
---

## A Static Site Generator

This site runs on a custom static site generator: a single Python script called `build.py`, about 1,150 lines long. It has one runtime dependency (`markdown`) and three commands: `python build.py` to build the site, `python build.py serve` to start a local dev server, and `python build.py clean` to wipe the output directory.

The concept is the same as Hugo, Jekyll, or Eleventy: take text files, parse their metadata, convert them to HTML, wrap them in templates, and write the result as static files. The difference is scope. Hugo is a Go binary with a plugin system, theme ecosystem, taxonomies, and hundreds of configuration options. Jekyll needs Ruby and a gem dependency chain. This is a single script with exactly the features one site needs, nothing more.{mn}The template engines differ too. Hugo uses Go templates, Jekyll uses Liquid, Eleventy uses Nunjucks. This site uses a homegrown engine that supports two constructs: variable substitution and conditional/loop blocks.{/mn}

## Repository Structure

The diagram below shows how source files map through `build.py` to the final output. Hover over any node to trace its connections.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/repo-architecture.html?embed&amp;lang=en" title="Repository architecture visualization"></iframe>
</div>

Content is authored in `posts/` and `pages/`, split by language into `en/` and `pt/` subdirectories. Templates define the HTML structure. Static assets (CSS, JavaScript, fonts, interactive embeds) pass through untouched. The `output/` directory is ephemeral and gitignored.

## The Build Pipeline

For each language, `build.py` runs a sequence of transformations on every Markdown file: parse frontmatter, convert Markdown to HTML (Tufte extensions included), extract headings for the table of contents, then render the result through two template passes (content template first, base template second). After all posts and pages are built, it generates the homepage, the Atom feed, copies static assets, and writes the root page.

The diagram below shows these processing stages in detail. Click any step to see a concrete before-and-after transformation.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/build-pipeline.html?embed&amp;lang=en" title="Build pipeline visualization"></iframe>
</div>

## Content and Frontmatter

Every post starts as a Markdown file with YAML-like frontmatter at the top:

```
---
title: "How This Site Works"
date: 2026-03-03
excerpt: A custom static site generator...
---

The actual content here.
```

The build script parses this by splitting on `---` fences, extracting key-value pairs, then handing the body to Python's `markdown` library with fenced code, tables, table of contents, and a small Tufte extension enabled.{mn}The script used to carry its own fallback converter for when the library wasn't installed. It was never needed in practice, so it's gone, and `markdown` is now a hard dependency.{/mn} The result is standard HTML with the three Tufte constructs already converted.

## Tufte Extensions

Tufte CSS translates Edward Tufte's principles of information design to the web: high information density, minimal visual clutter, and sidenotes instead of footnotes. This site extends it with three custom Markdown syntaxes:

**Sidenotes** (`{sn}...{/sn}`) become numbered notes in the margin. They reference a specific claim or sentence.

**Margin notes** (`{mn}...{/mn}`) are unnumbered. They add context without implying a specific anchor point.{mn}Like this one. No number, no interruption. Just additional context if you want it.{/mn}

**New thoughts** (`{nt}...{/nt}`) render as small-caps text, Tufte's convention for beginning a new section within a chapter.

Under the hood, they're a Python-Markdown extension: an inline pattern that runs during the conversion, after code spans and fenced blocks have been set aside, so a `{sn}` inside code stays literal. A sidenote becomes a `<label>`, an `<input>` checkbox (for mobile toggle), and a `<span>`. The checkbox trick means sidenotes work on mobile without any JavaScript: tap the number to show or hide the note.

## The Template Engine

Rather than pulling in Jinja2 or Mako, the generator uses a homegrown template engine. It supports two things:

**Variables**: `{{title}}` gets replaced with the value from a context dictionary.

**Blocks**: `{{#key}}...{{/key}}` acts as both a conditional (render this section if `key` is truthy) and a loop (if `key` is a list, render the inner content once per item).

That's the entire API. Four templates define the site: `base.html` (30 lines, the site shell with header, nav, and meta tags), `post.html` (19 lines), `page.html` (15 lines), and `index.html` (20 lines). Rendering is two-pass: the content template runs first (e.g., `post.html` fills in the title, date, and body), then the result is wrapped into `base.html`.{mn}The trade-off is real: no HTML escaping, no nesting of same-tag blocks. Both are fine here because all content is author-controlled and no template actually nests blocks. Rendering is a single pass, so a `{{` inside a post body is never treated as a placeholder, and a placeholder missing from the context stops the build instead of rendering blank.{/mn}

## Bilingual Architecture

Every piece of content exists in both English and Portuguese. The file structure mirrors this:

```
posts/en/how-this-site-works.md
posts/pt/how-this-site-works.md
```

The build script finds content pairs by matching filenames across language directories. If a post exists in both `en/` and `pt/`, the generator adds a language toggle (the flag icon in the header) that links directly to the other version.

The root `index.html` is the Portuguese homepage itself. A small script in its `<head>` checks `localStorage` for a previous language choice, then `navigator.language`, and sends the visitor to `/en/` only if either one says English. No server-side logic needed.{mn}Portuguese readers get the homepage with no extra hop, and so do visitors without JavaScript and link previews. Returning English readers are redirected before the page paints.{/mn}

## The Frontend

### Speed

The site loads two CSS files (the Tufte base, which also declares the fonts, and custom overrides) and up to three small JavaScript files (theme toggle, language preference, and the table of contents on posts that have one). No external requests. No CDN. No analytics.{mn}ET Book and Source Code Pro are self-hosted in `static/css/`. The four ET Book faces add up to about 150KB as WOFF2, and browsers only download the ones a page actually uses.{/mn}

Pages are static HTML served from GitHub Pages. There is nothing to be slow about.

### Dark Mode

The theme system uses CSS custom properties on `:root` for light mode and `[data-theme="dark"]` for dark. A script in the `<head>` checks `localStorage` before the browser paints, so there's never a flash of the wrong theme.{mn}The toggle button is injected via JavaScript after DOM load. If JS is disabled, you get the system preference and that's it. Graceful degradation.{/mn}

### Table of Contents

Posts with three or more headings get a table of contents. On wide screens (1440px+), it appears as a fixed sidebar on the left. On smaller screens, it's hidden. The build script extracts `h2` and `h3` tags, generates IDs, and produces the navigation HTML. A small script uses `IntersectionObserver` to highlight the current section as you scroll.

### Interactive Embeds

The D3.js visualizations (like the diagrams above) are self-contained HTML files in `static/embeds/`, one file per visualization for both languages, with D3 served from the site itself. Each one works both standalone and embedded via iframe. `?lang=en` or `?lang=pt` in the URL picks the language. With `?embed`, they hide their own chrome (theme toggle, instructions) and follow the parent page's theme through the browser's `storage` event: the toggle writes to `localStorage`, and same-origin iframes hear about it.

## Drafts

Setting `draft: true` in a post's frontmatter means the post gets built and is accessible by direct URL, but it doesn't appear on the index page or in the Atom feed. Useful for sharing specific posts before broad publication.
