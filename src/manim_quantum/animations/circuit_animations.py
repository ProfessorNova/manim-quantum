"""Custom animations for quantum circuit visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import (
    BLUE,
    WHITE,
    Animation,
    AnimationGroup,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MoveAlongPath,
    ShowPassingFlash,
    Succession,
    VGroup,
    linear,
)

if TYPE_CHECKING:
    from manim_quantum.circuits.circuit import QuantumCircuit
    from manim_quantum.circuits.gate import QuantumGate


class GateAnimation(Animation):
    """
    Animation for highlighting a quantum gate.

    This animation creates a visual effect to draw attention to a gate,
    useful for explaining circuit operation step by step.

    Args:
        gate: The QuantumGate to animate.
        color: Highlight color.
        run_time: Animation duration.
    """

    def __init__(
            self,
            gate: "QuantumGate",
            color=None,
            run_time: float = 0.5,
            **kwargs,
    ) -> None:
        self.gate = gate
        self.color = color or BLUE
        super().__init__(gate, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """Interpolate the animation."""
        # Simple scale pulse effect
        scale = 1.0 + 0.2 * np.sin(alpha * np.pi)
        self.mobject.scale(scale / self.mobject.get_height() * self.gate.get_height())


class CircuitEvaluationAnimation:
    """
    Factory for creating circuit evaluation animations.

    This class provides methods to create animations that show
    the flow of quantum information through a circuit.

    Args:
        circuit: The QuantumCircuit to animate.
    """

    def __init__(self, circuit: "QuantumCircuit") -> None:
        self.circuit = circuit

    def create_shot_animation(
            self,
            wires: list[int] | None = None,
            color=None,
            run_time: float = 2.0,
            lag_ratio: float = 0.0,
    ) -> Animation:
        """
        Create an animation showing glowing particles flowing through wires.

        Args:
            wires: Wire indices to animate (all if None).
            color: Particle color.
            run_time: Total animation duration.
            lag_ratio: Stagger ratio between wires.

        Returns:
            Animation showing particle flow.
        """
        color = color or self.circuit.style.glow_color or BLUE
        wires = wires if wires is not None else list(self.circuit._wires.keys())

        anims = []
        for wire_idx in wires:
            wire = self.circuit._wires.get(wire_idx)
            if wire is None:
                continue

            y = wire.y
            start = np.array([self.circuit.x_start, y, 0])
            end = np.array([self.circuit.x_end, y, 0])

            outer = Circle(radius=0.2)
            outer.set_fill(color, opacity=0.3)
            outer.set_stroke(width=0)

            inner = Dot(radius=0.1, color=color)
            inner.set_stroke(WHITE, width=1, opacity=0.8)

            packet = VGroup(outer, inner)
            packet.move_to(start)

            fade_time = 0.15 * run_time
            move_time = 0.70 * run_time

            seq = Succession(
                FadeIn(packet, run_time=fade_time),
                MoveAlongPath(
                    packet, Line(start, end), run_time=move_time, rate_func=linear
                ),
                FadeOut(packet, run_time=fade_time),
            )
            anims.append(seq)

        if not anims:
            return AnimationGroup()
        return LaggedStart(*anims, lag_ratio=lag_ratio)

    def create_glow_animation(
            self,
            wires: list[int] | None = None,
            color=None,
            run_time: float = 1.2,
            lag_ratio: float = 0.0,
    ) -> Animation:
        """
        Create an animation that makes wires glow.

        Args:
            wires: Wire indices to animate (all if None).
            color: Glow color.
            run_time: Animation duration.
            lag_ratio: Stagger ratio between wires.

        Returns:
            Animation object.
        """
        color = color or self.circuit.style.glow_color or BLUE
        wires = wires if wires is not None else list(self.circuit._wires.keys())

        anims = []
        for wire_idx in wires:
            wire = self.circuit._wires.get(wire_idx)
            if wire is None:
                continue

            y = wire.y
            start = np.array([self.circuit.x_start, y, 0])
            end = np.array([self.circuit.x_end, y, 0])

            glow_line = Line(start, end)
            glow_line.set_stroke(color, width=8, opacity=0.7)

            anims.append(ShowPassingFlash(glow_line, run_time=run_time, time_width=0.3))

        if not anims:
            return AnimationGroup()
        return LaggedStart(*anims, lag_ratio=lag_ratio)
