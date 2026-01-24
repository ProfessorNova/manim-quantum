"""Main quantum circuit visualization class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import numpy as np
from manim import (
    VGroup,
)

from manim_quantum.circuits.gate import QuantumGate
from manim_quantum.circuits.wire import QuantumWire
from manim_quantum.styles import QuantumStyle

if TYPE_CHECKING:
    pass


class QuantumCircuit(VGroup):
    """
    A complete quantum circuit visualization.

    This is the main class for creating quantum circuit diagrams. It manages
    wires, gates, and provides methods for animations.

    Args:
        num_qubits: Number of qubits (wires) in the circuit.
        wire_labels: Optional custom labels for each wire.
        x_start: Left boundary of the circuit.
        x_end: Right boundary of the circuit.
        wire_spacing: Vertical spacing between wires.
        style: Visual style configuration.

    Example:
        >>> circuit = QuantumCircuit(num_qubits=2)
        >>> circuit.add_gate("H", [0])
        >>> circuit.add_gate("CNOT", [0, 1])
        >>> circuit.add_gate("Measure", [0, 1])
    """

    def __init__(
            self,
            num_qubits: int = 2,
            wire_labels: list[str] | None = None,
            x_start: float = -5.5,
            x_end: float = 5.5,
            wire_spacing: float = 1.0,
            style: QuantumStyle | None = None,
    ) -> None:
        super().__init__()

        self.num_qubits = num_qubits
        self.x_start = x_start
        self.x_end = x_end
        self.wire_spacing = wire_spacing
        self.style = style or QuantumStyle()

        self._gates: list[QuantumGate] = []
        self._wires: dict[int, QuantumWire] = {}
        self._gate_x_positions: list[float] = []
        self._next_gate_x = x_start + 1.5

        self._build_wires(wire_labels)

    def _build_wires(self, labels: list[str] | None) -> None:
        """Create the quantum wires."""
        for i in range(self.num_qubits):
            y = -i * self.wire_spacing
            label = labels[i] if labels and i < len(labels) else None
            wire = QuantumWire(
                index=i, x_start=self.x_start, x_end=self.x_end,
                y=y, label=label, style=self.style,
            )
            self._wires[i] = wire
            self.add(wire)

    def _get_wire_positions(self) -> dict[int, float]:
        """Get mapping from wire index to y-coordinate."""
        return {idx: wire.y for idx, wire in self._wires.items()}

    def add_gate(
            self,
            name: str,
            target_wires: list[int],
            params: list[float] | None = None,
            x: float | None = None,
    ) -> QuantumGate:
        """
        Add a gate to the circuit.

        Args:
            name: Gate type (e.g., "H", "X", "CNOT", "RZ").
            target_wires: Wire indices the gate acts on.
            params: Optional parameters (e.g., rotation angles).
            x: Optional x-position; auto-calculated if not provided.

        Returns:
            The created QuantumGate object.
        """
        gate = QuantumGate(
            name=name,
            target_wires=target_wires,
            params=params,
            style=self.style,
        )

        if x is None:
            x = self._next_gate_x
            self._next_gate_x += self.style.gate_spacing

        self._gate_x_positions.append(x)
        self._gates.append(gate)

        wire_positions = self._get_wire_positions()
        gate_visual = gate.render(wire_positions, x)
        self.add(gate_visual)

        half_width = gate.get_mask_width() / 2
        for wire_idx in target_wires:
            if wire_idx in self._wires:
                self._wires[wire_idx].mask_region(x, half_width)

        return gate

    def add_gates(
            self, gates: Sequence[tuple[str, list[int]] | tuple[str, list[int], list[float]]]
    ) -> list[QuantumGate]:
        """
        Add multiple gates at once.

        Args:
            gates: List of gate specifications as (name, wires) or (name, wires, params).

        Returns:
            List of created QuantumGate objects.
        """
        created = []
        for gate_spec in gates:
            if len(gate_spec) == 2:
                name, wires = gate_spec
                params = None
            else:
                name, wires, params = gate_spec
            created.append(self.add_gate(name, wires, params))
        return created

    def build(self) -> QuantumCircuit:
        """
        Finalize the circuit after all gates are added.

        This rebuilds wire segments to properly show breaks at gate positions.

        Returns:
            Self for method chaining.
        """
        for wire in self._wires.values():
            wire.rebuild_segments()
        return self

    def get_wire(self, index: int) -> QuantumWire | None:
        """Get a wire by index."""
        return self._wires.get(index)

    def get_wire_endpoint(self, wire_index: int, side: str = "right") -> np.ndarray:
        """
        Get the endpoint of a wire.

        Args:
            wire_index: Wire index.
            side: "left" or "right".

        Returns:
            3D coordinate array.
        """
        wire = self._wires.get(wire_index)
        if wire is None:
            return np.array([0, 0, 0])
        x = self.x_start if side == "left" else self.x_end
        return np.array([x, wire.y, 0])

    def highlight_wires(self, wires: list[int], color=None) -> None:
        """Highlight specified wires."""
        for wire_idx in wires:
            wire = self._wires.get(wire_idx)
            if wire:
                wire.highlight(color)

    def reset_wire_highlights(self, wires: list[int] | None = None) -> None:
        """Reset wire colors to default."""
        wires = wires if wires is not None else list(self._wires.keys())
        for wire_idx in wires:
            wire = self._wires.get(wire_idx)
            if wire:
                wire.reset_highlight()

    @classmethod
    def from_operations(
            cls,
            operations: list[tuple[str, list[int], list[float] | None]],
            num_qubits: int | None = None,
            **kwargs,
    ) -> QuantumCircuit:
        """
        Create a circuit from a list of operations.

        Args:
            operations: List of (gate_name, wires, params) tuples.
            num_qubits: Number of qubits (auto-detected if None).
            **kwargs: Additional arguments for QuantumCircuit.

        Returns:
            Configured QuantumCircuit instance.
        """
        if num_qubits is None:
            all_wires = [w for _, wires, _ in operations for w in wires]
            num_qubits = max(all_wires) + 1 if all_wires else 1

        circuit = cls(num_qubits=num_qubits, **kwargs)
        for name, wires, params in operations:
            circuit.add_gate(name, wires, params if params else None)

        return circuit.build()
