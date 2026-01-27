"""Pytest fixtures for manim-quantum tests."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_manim_config():
    """Configure Manim for testing with temporary directories."""
    from manim import config, tempconfig

    # Create a temporary directory for media files
    temp_dir = tempfile.mkdtemp()
    media_dir = Path(temp_dir) / "media"
    media_dir.mkdir(exist_ok=True)

    # Create necessary subdirectories
    (media_dir / "Tex").mkdir(exist_ok=True)
    (media_dir / "texts").mkdir(exist_ok=True)
    (media_dir / "images").mkdir(exist_ok=True)
    (media_dir / "videos").mkdir(exist_ok=True)

    # Configure Manim to use the temporary directory
    with tempconfig({
        "media_dir": str(media_dir),
        "log_dir": str(Path(temp_dir) / "logs"),
        "quality": "low_quality",
        "preview": False,
        "disable_caching": True,
        "write_to_movie": False,
    }):
        # Set the media directory globally
        config.media_dir = str(media_dir)
        yield

    # Cleanup is handled by tempfile automatically


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
