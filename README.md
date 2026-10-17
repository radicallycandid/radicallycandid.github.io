# radicallycandid.github.io

Source for [vmargato.com](https://vmargato.com), a bilingual (English and Portuguese) personal blog. One Python script, `build.py`, turns the Markdown in `posts/` and `pages/` into static HTML in `output/`. GitHub Actions tests every push and deploys `main` to GitHub Pages.

```bash
uv sync --extra dev                     # install dependencies (pinned by uv.lock)
uv run python build.py serve            # build and serve on localhost:8000
uv run python build.py build --strict   # build, failing on frontmatter warnings
uv run pytest                           # tests
uv run ruff check . && uv run mypy build.py tests
```

See [CLAUDE.md](CLAUDE.md) for content conventions, the writing style, and known limitations.
