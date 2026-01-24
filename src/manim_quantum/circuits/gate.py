"""Quantum gate visualization components."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import (
    Circle,
    Dot,
    Line,
    MathTex,
    Rectangle,
    VGroup,
)

if TYPE_CHECKING:
    from manim_quantum.styles import QuantumStyle

# Gate type categories
SINGLE_QUBIT_GATES = {"H", "X", "Y", "Z", "S", "T", "RX", "RY", "RZ", "U", "I"}
TWO_QUBIT_GATES = {"CNOT", "CX", "CZ", "CY", "SWAP", "ISWAP", "CRX", "CRY", "CRZ"}
MEASUREMENT_GATES = {"Measure", "M"}


class QuantumGate(VGroup):
    """
    Visual representation of a quantum gate.

    Supports various gate types including single-qubit gates, controlled gates,
    and measurement operations.

    Args:
        name: Gate type identifier (e.g., "H", "CNOT", "RZ").
        target_wires: Wire indices the gate acts on.
        params: Optional parameters for parameterized gates.
        style: Visual style configuration.

    Example:
        >>> gate = QuantumGate("H", [0])
        >>> gate.render(wire_positions={0: 0}, x=0)
    """

    def __init__(
            self,
            name: str,
            target_wires: list[int],
            params: list[float] | None = None,
            style: "QuantumStyle | None" = None,
    ) -> None:
        super().__init__()

        self.name = name.upper() if name not in {"Measure"} else name
        self.target_wires = target_wires
        self.params = params or []

        # Import here to avoid circular imports
        from manim_quantum.styles import QuantumStyle
        self.style = style or QuantumStyle()

        self._visual: VGroup | None = None
        self._mask_width = 0.6

    def render(self, wire_positions: dict[int, float], x: float) -> VGroup:
        """
        Render the gate at the specified position.

        Args:
            wire_positions: Mapping of wire index to y-coordinate.
            x: x-coordinate for the gate.

        Returns:
            VGroup containing the gate visualization.
        """
        if self.name in SINGLE_QUBIT_GATES:
            self._visual = self._render_single_qubit(wire_positions, x)
        elif self.name in {"CNOT", "CX"}:
            self._visual = self._render_cnot(wire_positions, x)
        elif self.name in {"CZ", "CY"}:
            self._visual = self._render_controlled_gate(wire_positions, x)
        elif self.name == "SWAP":
            self._visual = self._render_swap(wire_positions, x)
        elif self.name in MEASUREMENT_GATES:
            self._visual = self._render_measurement(wire_positions, x)
        else:
            # Default: render as a generic gate box
            self._visual = self._render_generic(wire_positions, x)

        self.add(self._visual)
        return self._visual

    def _render_single_qubit(
            self, wire_positions: dict[int, float], x: float
    ) -> VGroup:
        """Render a single-qubit gate as a box with label."""
        wire_idx = self.target_wires[0]
        y = wire_positions.get(wire_idx, 0)

        group = VGroup()

        # Gate box
        box = Rectangle(
            width=self.style.gate_width,
            height=self.style.gate_height,
            fill_color=self.style.gate_fill_color,
            fill_opacity=self.style.gate_fill_opacity,
            stroke_color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        box.move_to([x, y, 0])
        group.add(box)

        # Gate label
        label_text = self._get_gate_label()
        label = MathTex(label_text, color=self.style.gate_text_color)
        label.scale(self.style.gate_font_scale)
        label.move_to([x, y, 0])
        group.add(label)

        self._mask_width = self.style.gate_width

        return group

    def _render_cnot(self, wire_positions: dict[int, float], x: float) -> VGroup:
        """Render a CNOT (controlled-X) gate."""
        control_wire = self.target_wires[0]
        target_wire = self.target_wires[1]

        control_y = wire_positions.get(control_wire, 0)
        target_y = wire_positions.get(target_wire, 0)

        group = VGroup()

        # Vertical line connecting control and target
        conn_line = Line(
            start=[x, control_y, 0],
            end=[x, target_y, 0],
            color=self.style.gate_stroke_color,
            stroke_width=self.style.wire_stroke_width,
        )
        group.add(conn_line)

        # Control dot
        control_dot = Dot(
            point=[x, control_y, 0],
            radius=self.style.control_dot_radius,
            color=self.style.control_dot_color,
        )
        group.add(control_dot)

        # Target (⊕ symbol)
        target_circle = Circle(
            radius=self.style.target_radius,
            color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        target_circle.move_to([x, target_y, 0])
        group.add(target_circle)

        # Cross lines inside target circle
        cross_h = Line(
            start=[x - self.style.target_radius, target_y, 0],
            end=[x + self.style.target_radius, target_y, 0],
            color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        cross_v = Line(
            start=[x, target_y - self.style.target_radius, 0],
            end=[x, target_y + self.style.target_radius, 0],
            color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        group.add(cross_h, cross_v)

        self._mask_width = self.style.target_radius * 2

        return group

    def _render_controlled_gate(
            self, wire_positions: dict[int, float], x: float
    ) -> VGroup:
        """Render a controlled gate (CZ, CY, etc.)."""
        control_wire = self.target_wires[0]
        target_wire = self.target_wires[1]

        control_y = wire_positions.get(control_wire, 0)
        target_y = wire_positions.get(target_wire, 0)

        group = VGroup()

        # Vertical line
        conn_line = Line(
            start=[x, control_y, 0],
            end=[x, target_y, 0],
            color=self.style.gate_stroke_color,
            stroke_width=self.style.wire_stroke_width,
        )
        group.add(conn_line)

        # Control dot
        control_dot = Dot(
            point=[x, control_y, 0],
            radius=self.style.control_dot_radius,
            color=self.style.control_dot_color,
        )
        group.add(control_dot)

        # Target gate box
        gate_label = self.name[1:]  # Remove "C" prefix
        box = Rectangle(
            width=self.style.gate_width * 0.8,
            height=self.style.gate_height * 0.8,
            fill_color=self.style.gate_fill_color,
            fill_opacity=self.style.gate_fill_opacity,
            stroke_color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        box.move_to([x, target_y, 0])
        group.add(box)

        label = MathTex(gate_label, color=self.style.gate_text_color)
        label.scale(self.style.gate_font_scale * 0.8)
        label.move_to([x, target_y, 0])
        group.add(label)

        self._mask_width = self.style.gate_width

        return group

    def _render_swap(self, wire_positions: dict[int, float], x: float) -> VGroup:
        """Render a SWAP gate."""
        wire1 = self.target_wires[0]
        wire2 = self.target_wires[1]

        y1 = wire_positions.get(wire1, 0)
        y2 = wire_positions.get(wire2, 0)

        group = VGroup()

        # Vertical line
        conn_line = Line(
            start=[x, y1, 0],
            end=[x, y2, 0],
            color=self.style.gate_stroke_color,
            stroke_width=self.style.wire_stroke_width,
        )
        group.add(conn_line)

        # X symbols at each wire
        for y in [y1, y2]:
            size = 0.15
            cross1 = Line(
                start=[x - size, y - size, 0],
                end=[x + size, y + size, 0],
                color=self.style.gate_stroke_color,
                stroke_width=self.style.gate_stroke_width,
            )
            cross2 = Line(
                start=[x - size, y + size, 0],
                end=[x + size, y - size, 0],
                color=self.style.gate_stroke_color,
                stroke_width=self.style.gate_stroke_width,
            )
            group.add(cross1, cross2)

        self._mask_width = 0.4

        return group

    def _render_measurement(
            self, wire_positions: dict[int, float], x: float
    ) -> VGroup:
        """Render a measurement gate."""
        group = VGroup()

        for wire_idx in self.target_wires:
            y = wire_positions.get(wire_idx, 0)

            # Measurement box
            box = Rectangle(
                width=self.style.gate_width,
                height=self.style.gate_height,
                fill_color=self.style.measurement_fill_color,
                fill_opacity=self.style.gate_fill_opacity,
                stroke_color=self.style.gate_stroke_color,
                stroke_width=self.style.gate_stroke_width,
            )
            box.move_to([x, y, 0])
            group.add(box)

            # Meter arc
            arc_radius = self.style.gate_height * 0.25
            arc_center = [x, y - arc_radius * 0.3, 0]

            # Simple arc representation using lines
            arc_points = []
            for angle in np.linspace(np.pi, 0, 10):
                px = arc_center[0] + arc_radius * np.cos(angle)
                py = arc_center[1] + arc_radius * np.sin(angle)
                arc_points.append([px, py, 0])

            for i in range(len(arc_points) - 1):
                seg = Line(
                    start=arc_points[i],
                    end=arc_points[i + 1],
                    color=self.style.gate_text_color,
                    stroke_width=1.5,
                )
                group.add(seg)

            # Meter needle
            needle = Line(
                start=arc_center,
                end=[x + arc_radius * 0.7, y + arc_radius * 0.5, 0],
                color=self.style.gate_text_color,
                stroke_width=1.5,
            )
            group.add(needle)

        self._mask_width = self.style.gate_width

        return group

    def _render_generic(
            self, wire_positions: dict[int, float], x: float
    ) -> VGroup:
        """Render a generic gate as a labeled box."""
        group = VGroup()

        # Find y range for multi-qubit gates
        y_values = [wire_positions.get(w, 0) for w in self.target_wires]
        y_min, y_max = min(y_values), max(y_values)
        y_center = (y_min + y_max) / 2
        height = max(self.style.gate_height, y_max - y_min + self.style.gate_height)

        box = Rectangle(
            width=self.style.gate_width,
            height=height,
            fill_color=self.style.gate_fill_color,
            fill_opacity=self.style.gate_fill_opacity,
            stroke_color=self.style.gate_stroke_color,
            stroke_width=self.style.gate_stroke_width,
        )
        box.move_to([x, y_center, 0])
        group.add(box)

        label = MathTex(self.name, color=self.style.gate_text_color)
        label.scale(self.style.gate_font_scale)
        label.move_to([x, y_center, 0])
        group.add(label)

        self._mask_width = self.style.gate_width

        return group

    def _get_gate_label(self) -> str:
        """Get the display label for the gate."""
        # Handle rotation gates with parameters
        if self.name in {"RX", "RY", "RZ"} and self.params:
            angle = self.params[0]
            # Format angle nicely
            if abs(angle - np.pi) < 0.01:
                angle_str = r"\pi"
            elif abs(angle - np.pi / 2) < 0.01:
                angle_str = r"\frac{\pi}{2}"
            elif abs(angle - np.pi / 4) < 0.01:
                angle_str = r"\frac{\pi}{4}"
            else:
                angle_str = f"{angle:.2f}"
            return f"{self.name}({angle_str})"

        return self.name

    def get_mask_width(self) -> float:
        """Get the width to mask on wires under this gate."""
        return self._mask_width
