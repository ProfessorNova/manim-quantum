"""Pytest fixtures for manim-quantum tests."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_manim_config():
    """Configure Manim for testing with temporary directories."""
    from manim import config

    # Create a temporary directory for media files
    temp_dir = tempfile.mkdtemp()
    media_dir = Path(temp_dir) / "media"
    media_dir.mkdir(exist_ok=True)

    # Create necessary subdirectories
    (media_dir / "Tex").mkdir(exist_ok=True)
    (media_dir / "texts").mkdir(exist_ok=True)
    (media_dir / "images").mkdir(exist_ok=True)
    (media_dir / "videos").mkdir(exist_ok=True)

    # Store original config values
    original_media_dir = config.media_dir
    original_quality = config.quality
    original_preview = config.preview

    # Configure Manim to use the temporary directory
    config.media_dir = str(media_dir)
    config.quality = "low_quality"
    config.preview = False
    config.disable_caching = True
    config.write_to_movie = False

    yield

    # Restore original config
    config.media_dir = original_media_dir
    config.quality = original_quality
    config.preview = original_preview


@pytest.fixture(autouse=True)
def ensure_media_dirs():
    """Ensure media directories exist for each test."""
    from manim import config

    media_dir = Path(config.media_dir)

    # Ensure all necessary subdirectories exist
    for subdir in ["Tex", "texts", "images", "videos"]:
        (media_dir / subdir).mkdir(parents=True, exist_ok=True)

    yield


@pytest.fixture
def sample_amplitudes():
    """Sample amplitudes for a 2-qubit state vector."""
    return np.array([0.5, 0.5, 0.5, 0.5])
