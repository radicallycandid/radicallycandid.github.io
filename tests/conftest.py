"""Shared test fixtures."""

from pathlib import Path

import pytest

import build


@pytest.fixture
def mock_templates_dir(tmp_path: Path) -> Path:
    original = build.TEMPLATES_DIR
    build.TEMPLATES_DIR = tmp_path
    yield tmp_path
    build.TEMPLATES_DIR = original
