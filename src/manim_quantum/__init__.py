"""Manim-Quantum: A Manim library for quantum computing visualizations.

This library provides tools for creating beautiful animations of quantum
circuits, state vectors, Bloch spheres, and other quantum computing concepts.
"""

from __future__ import annotations

# Animations
from manim_quantum.animations import (
    GateAnimation,
    CircuitEvaluationAnimation,
    BlochSphereStateTransition,
    BlochSphereRotation,
)
# Bloch sphere
from manim_quantum.bloch import BlochSphere
# Circuit components
from manim_quantum.circuits import QuantumCircuit, QuantumGate, QuantumWire
# PennyLane integration
from manim_quantum.pennylane import circuit_from_qnode
# State representations
from manim_quantum.states import StateVector, KetLabel
# Styles
from manim_quantum.styles import QuantumStyle, StylePresets

__version__ = "0.1.0"

__all__ = [
    # Circuits
    "QuantumCircuit",
    "QuantumGate",
    "QuantumWire",
    # Bloch
    "BlochSphere",
    # States
    "StateVector",
    "KetLabel",
    # Animations
    "GateAnimation",
    "CircuitEvaluationAnimation",
    "BlochSphereStateTransition",
    "BlochSphereRotation",
    # Styles
    "QuantumStyle",
    "StylePresets",
    # PennyLane
    "circuit_from_qnode",
]
