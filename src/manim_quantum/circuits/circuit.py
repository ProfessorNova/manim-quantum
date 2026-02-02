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
        compress: If True, gates are automatically arranged in the most compact
            form by parallelizing gates on non-overlapping wires (minimizes depth).
        center: If True, gates are centered horizontally within the circuit bounds
            after all gates are added (during build()).

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
            compress: bool = True,
            center: bool = False,
    ) -> None:
        super().__init__()

        self.num_qubits = num_qubits
        self.x_start = x_start
        self.x_end = x_end
        self.wire_spacing = wire_spacing
        self.style = style or QuantumStyle()
        self.compress = compress
        self.center = center

        self._gates: list[QuantumGate] = []
        self._wires: dict[int, QuantumWire] = {}
        self._gate_x_positions: list[float] = []
        self._gate_visuals: list[VGroup] = []
        self._next_gate_x = x_start + 1.5
        self._wire_next_free_layer: dict[int, int] = {i: 0 for i in range(num_qubits)}
        self._needs_rebuild = False

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

    def _ensure_built(self) -> None:
        """Ensure the circuit is built before it's used."""
        if self._needs_rebuild:
            self.build()
            self._needs_rebuild = False

    def _get_wire_positions(self) -> dict[int, float]:
        """Get mapping from wire index to y-coordinate."""
        return {idx: wire.y for idx, wire in self._wires.items()}

    def add_gate(
            self,
            name: str,
            target_wires: list[int],
            params: list[float | str] | None = None,
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
            if self.compress:
                # Compression: find the minimum layer where all target wires are free
                min_layer = max(self._wire_next_free_layer.get(w, 0) for w in target_wires)
                x = self.x_start + 1.5 + min_layer * self.style.gate_spacing

                # Update wire availability - all target wires are now occupied up to next layer
                for wire_idx in target_wires:
                    self._wire_next_free_layer[wire_idx] = min_layer + 1
            else:
                x = self._next_gate_x
                self._next_gate_x += self.style.gate_spacing

        self._gate_x_positions.append(x)
        self._gates.append(gate)

        wire_positions = self._get_wire_positions()
        gate_visual = gate.render(wire_positions, x)
        self._gate_visuals.append(gate_visual)
        self.add(gate_visual)

        half_width = gate.get_mask_width() / 2
        for wire_idx in target_wires:
            if wire_idx in self._wires:
                self._wires[wire_idx].mask_region(x, half_width)

        self._needs_rebuild = True
        return gate

    def add_gates(
            self, gates: Sequence[tuple[str, list[int]] | tuple[str, list[int], list[float | str]]]
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
        If center=True, gates will be centered horizontally within the circuit bounds.

        Note: This is called automatically when the circuit is rendered, so manual
        calls are optional but can be used for explicit control.

        Returns:
            Self for method chaining.
        """
        if self.center and self._gate_x_positions:
            self._center_gates()

        for wire in self._wires.values():
            wire.rebuild_segments()

        self._needs_rebuild = False
        return self

    def _center_gates(self) -> None:
        """Center all gates horizontally within the circuit bounds."""
        if not self._gate_x_positions:
            return

        # Calculate the bounding box of all gates
        min_gate_x = min(self._gate_x_positions)
        max_gate_x = max(self._gate_x_positions)

        # Calculate current gates center and target center
        gates_center = (min_gate_x + max_gate_x) / 2
        circuit_center = (self.x_start + self.x_end) / 2

        # Calculate offset to center gates
        offset = circuit_center - gates_center

        if abs(offset) < 0.001:  # Already centered
            return

        # Shift all gate positions and visuals
        for i, gate_visual in enumerate(self._gate_visuals):
            self._gate_x_positions[i] += offset
            gate_visual.shift(np.array([offset, 0, 0]))

        # Update wire mask regions
        for wire in self._wires.values():
            wire.shift_masks(offset)

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

    # Override methods to ensure circuit is built before use
    def get_center(self):
        """Get the center of the circuit, ensuring it's built first."""
        self._ensure_built()
        return super().get_center()

    def get_top(self):
        """Get the top of the circuit, ensuring it's built first."""
        self._ensure_built()
        return super().get_top()

    def get_bottom(self):
        """Get the bottom of the circuit, ensuring it's built first."""
        self._ensure_built()
        return super().get_bottom()

    def get_left(self):
        """Get the left of the circuit, ensuring it's built first."""
        self._ensure_built()
        return super().get_left()

    def get_right(self):
        """Get the right of the circuit, ensuring it's built first."""
        self._ensure_built()
        return super().get_right()

    def get_family(self, *args, **kwargs):
        """Get the mobject family, ensuring the circuit is built first."""
        self._ensure_built()
        return super().get_family(*args, **kwargs)

    def family_members_with_points(self):
        """Get family members with points, ensuring the circuit is built first."""
        self._ensure_built()
        return super().family_members_with_points()

    def get_all_points(self) -> np.ndarray:
        """Get all points, ensuring the circuit is built first."""
        self._ensure_built()
        result = super().get_all_points()
        return np.asarray(result)

    def get_critical_point(self, direction):
        """Get a critical point, ensuring the circuit is built first."""
        self._ensure_built()
        return super().get_critical_point(direction)

    def generate_target(self, use_deepcopy: bool = True):
        """Generate a target for animations, ensuring the circuit is built first."""
        self._ensure_built()
        return super().generate_target(use_deepcopy=use_deepcopy)

    @classmethod
    def from_operations(
            cls,
            operations: list[tuple[str, list[int], list[float | str] | None]],
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

        return circuit
