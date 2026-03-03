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


@pytest.fixture
def mock_output_dir(tmp_path: Path) -> Path:
    output = tmp_path / "output"
    output.mkdir()
    original = build.OUTPUT_DIR
    build.OUTPUT_DIR = output
    yield output
    build.OUTPUT_DIR = original


@pytest.fixture
def sample_post_md() -> str:
    return """---
title: Test Post
date: 2026-01-15
excerpt: A test post.
---

## Introduction

This is a test post.

## Section Two

More content.

## Section Three

Even more.
"""
