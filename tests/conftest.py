"""Pytest fixtures for manim-quantum tests."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def sample_amplitudes():
    """Sample amplitudes for a 2-qubit state vector."""
    return np.array([0.5, 0.5, 0.5, 0.5])
