"""Visual styling for quantum circuit components."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manim import BLUE, GRAY, RED, TEAL, WHITE, YELLOW


@dataclass
class QuantumStyle:
    """
    Configuration for visual styling of quantum circuit components.

    This class defines colors, sizes, and other visual properties used
    throughout manim-quantum visualizations.

    Attributes:
        wire_color: Color of quantum wires.
        wire_stroke_width: Stroke width for wires.
        gate_fill_color: Background color for gate boxes.
        gate_fill_opacity: Opacity of gate fill.
        gate_stroke_color: Border color for gates.
        gate_stroke_width: Border width for gates.
        gate_text_color: Color of gate labels.
        gate_width: Width of single-qubit gate boxes.
        gate_height: Height of gate boxes.
        gate_spacing: Horizontal spacing between gates.
        gate_font_scale: Scale factor for gate labels.
        control_dot_radius: Radius of control dots (for CNOT, etc.).
        control_dot_color: Color of control dots.
        target_radius: Radius of target circles (for CNOT).
        measurement_fill_color: Background color for measurement gates.
        wire_label_color: Color of wire labels.
        wire_label_scale: Scale factor for wire labels.
        wire_label_buff: Buffer between label and wire.
        highlight_color: Color for highlighted elements.
        pulse_color: Color for pulse animations.
        glow_color: Color for glow animations.
        sphere_color: Color of Bloch sphere surface.
        sphere_opacity: Opacity of Bloch sphere surface.
        axis_color: Color of Bloch sphere axes.
        ket_color: Color of ket notation labels.
        state_vector_color: Color of state vector arrows.
        state_dot_color: Color of state dots.
        amplitude_color: Color of amplitude text.
        probability_bar_color: Fill color for probability bars.
        probability_bar_stroke: Stroke color for probability bars.
        probability_text_color: Color of probability values.

    Example:
        >>> style = QuantumStyle(gate_fill_color="#1a1a2e", wire_color="#4ecdc4")
        >>> circuit = QuantumCircuit(num_qubits=2, style=style)
    """

    # Wire styling
    wire_color: Any = WHITE
    wire_stroke_width: float = 2.0

    # Gate box styling
    gate_fill_color: Any = "#1a1a2e"
    gate_fill_opacity: float = 1.0
    gate_stroke_color: Any = WHITE
    gate_stroke_width: float = 2.0
    gate_text_color: Any = WHITE

    # Gate dimensions
    gate_width: float = 0.6
    gate_height: float = 0.6
    gate_spacing: float = 1.2
    gate_font_scale: float = 0.7

    # Control/target styling
    control_dot_radius: float = 0.08
    control_dot_color: Any = WHITE
    target_radius: float = 0.25

    # Measurement styling
    measurement_fill_color: Any = "#2d2d44"

    # Wire label styling
    wire_label_color: Any = WHITE
    wire_label_scale: float = 0.6
    wire_label_buff: float = 0.3

    # Animation colors
    highlight_color: Any = YELLOW
    pulse_color: Any = BLUE
    glow_color: Any = BLUE

    # Bloch sphere styling
    sphere_color: Any = BLUE
    sphere_opacity: float = 0.3
    axis_color: Any = GRAY
    state_vector_color: Any = RED
    state_dot_color: Any = RED

    # State vector styling
    ket_color: Any = WHITE
    amplitude_color: Any = WHITE
    probability_bar_color: Any = TEAL
    probability_bar_stroke: Any = WHITE
    probability_text_color: Any = WHITE


class StylePresets:
    """
    Predefined style presets for common visual themes.

    Example:
        >>> circuit = QuantumCircuit(num_qubits=2, style=StylePresets.ibm())
    """

    @staticmethod
    def default() -> QuantumStyle:
        """Default style with dark theme."""
        return QuantumStyle()

    @staticmethod
    def ibm() -> QuantumStyle:
        """IBM Quantum-inspired style."""
        return QuantumStyle(
            wire_color="#FFFFFF",
            gate_fill_color="#6929C4",
            gate_stroke_color="#BE95FF",
            gate_text_color="#FFFFFF",
            control_dot_color="#BE95FF",
            measurement_fill_color="#1192E8",
            pulse_color="#08BDBA",
            glow_color="#08BDBA",
            sphere_color="#6929C4",
            state_vector_color="#FA4D56",
        )

    @staticmethod
    def google() -> QuantumStyle:
        """Google Quantum AI-inspired style."""
        return QuantumStyle(
            wire_color="#DADCE0",
            gate_fill_color="#4285F4",
            gate_stroke_color="#8AB4F8",
            gate_text_color="#FFFFFF",
            control_dot_color="#FFFFFF",
            measurement_fill_color="#34A853",
            pulse_color="#FBBC04",
            glow_color="#FBBC04",
            sphere_color="#4285F4",
            state_vector_color="#EA4335",
        )

    @staticmethod
    def dark() -> QuantumStyle:
        """Dark theme with high contrast."""
        return QuantumStyle(
            wire_color="#E0E0E0",
            gate_fill_color="#1E1E2E",
            gate_stroke_color="#89B4FA",
            gate_text_color="#CDD6F4",
            control_dot_color="#89B4FA",
            measurement_fill_color="#313244",
            highlight_color="#F9E2AF",
            pulse_color="#89DCEB",
            glow_color="#89DCEB",
            sphere_color="#89B4FA",
            sphere_opacity=0.2,
            state_vector_color="#F38BA8",
            probability_bar_color="#A6E3A1",
        )

    @staticmethod
    def light() -> QuantumStyle:
        """Light theme for presentations."""
        return QuantumStyle(
            wire_color="#1E1E2E",
            gate_fill_color="#FFFFFF",
            gate_fill_opacity=0.9,
            gate_stroke_color="#1E1E2E",
            gate_text_color="#1E1E2E",
            control_dot_color="#1E1E2E",
            measurement_fill_color="#F5F5F5",
            highlight_color="#F59E0B",
            pulse_color="#3B82F6",
            glow_color="#3B82F6",
            sphere_color="#3B82F6",
            sphere_opacity=0.15,
            axis_color="#6B7280",
            state_vector_color="#EF4444",
            state_dot_color="#EF4444",
            ket_color="#1E1E2E",
            amplitude_color="#1E1E2E",
            probability_bar_color="#10B981",
            probability_bar_stroke="#1E1E2E",
            probability_text_color="#1E1E2E",
        )

    @staticmethod
    def pastel() -> QuantumStyle:
        """Soft pastel color scheme."""
        return QuantumStyle(
            wire_color="#6C7A89",
            gate_fill_color="#FFE5EC",
            gate_stroke_color="#FFB3C6",
            gate_text_color="#4A5568",
            control_dot_color="#FFB3C6",
            measurement_fill_color="#E0F2FE",
            highlight_color="#FDE68A",
            pulse_color="#A5D8FF",
            glow_color="#A5D8FF",
            sphere_color="#C4B5FD",
            sphere_opacity=0.25,
            state_vector_color="#FCA5A5",
            probability_bar_color="#86EFAC",
        )


__all__ = [
    "QuantumStyle",
    "StylePresets",
]
