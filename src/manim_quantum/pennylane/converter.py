"""PennyLane QNode to QuantumCircuit converter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from manim_quantum.circuits.circuit import QuantumCircuit
    from manim_quantum.styles import QuantumStyle


@runtime_checkable
class QNodeProtocol(Protocol):
    """Protocol for PennyLane QNode objects."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the QNode."""
        ...

    def construct(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
        """Construct the tape from the QNode."""
        ...


# Gate name mapping from PennyLane to manim-quantum
PENNYLANE_GATE_MAP = {
    "Hadamard": "H",
    "PauliX": "X",
    "PauliY": "Y",
    "PauliZ": "Z",
    "CNOT": "CNOT",
    "CZ": "CZ",
    "CY": "CY",
    "SWAP": "SWAP",
    "RX": "RX",
    "RY": "RY",
    "RZ": "RZ",
    "S": "S",
    "T": "T",
    "Toffoli": "Toffoli",
    "Identity": "I",
}


# Circuit configuration keys that should NOT be passed to the QNode
CIRCUIT_CONFIG_KEYS = {
    "style", "wire_labels", "x_start", "x_end", "wire_spacing",
    "compress", "center"
}


def circuit_from_qnode(
        qnode: QNodeProtocol,
        *args: Any,
        style: "QuantumStyle | None" = None,
        wire_labels: list[str] | None = None,
        x_start: float = -5.5,
        x_end: float = 5.5,
        wire_spacing: float = 1.0,
        compress: bool = True,
        center: bool = True,
        **kwargs: Any,
) -> "QuantumCircuit":
    """
    Convert a PennyLane QNode to a manim-quantum QuantumCircuit.

    This function executes the QNode with the given arguments to extract
    the circuit structure, then creates a visual representation.

    Args:
        qnode: A PennyLane QNode function.
        *args: Positional arguments to pass to the QNode.
        style: Visual style configuration.
        wire_labels: Optional custom labels for each wire.
        x_start: Left boundary of the circuit.
        x_end: Right boundary of the circuit.
        wire_spacing: Vertical spacing between wires.
        compress: If True, gates are arranged in compact form.
        center: If True, gates are centered horizontally.
        **kwargs: Keyword arguments to pass to the QNode.

    Returns:
        A QuantumCircuit visualization of the QNode.

    Example:
        >>> import pennylane as qml
        >>> dev = qml.device("default.qubit", wires=2)
        >>> @qml.qnode(dev)
        ... def my_circuit(theta):
        ...     qml.RY(theta, wires=0)
        ...     qml.CNOT(wires=[0, 1])
        ...     return qml.expval(qml.PauliZ(0))
        >>> circuit = circuit_from_qnode(my_circuit, 0.5)  # type: ignore[arg-type]
    """
    try:
        import pennylane as qml
    except ImportError:
        raise ImportError(
            "PennyLane is required for this feature. "
            "Install it with: pip install pennylane"
        )

    from manim_quantum.circuits.circuit import QuantumCircuit

    # Use construct() to get the tape (works with PennyLane 0.44.0+)
    # Only pass kwargs that are meant for the QNode (not circuit config)
    tape = qnode.construct(args, kwargs)

    # Determine number of qubits
    num_wires = len(tape.wires)

    # Create the circuit with configuration options
    circuit = QuantumCircuit(
        num_qubits=num_wires,
        style=style,
        wire_labels=wire_labels,
        x_start=x_start,
        x_end=x_end,
        wire_spacing=wire_spacing,
        compress=compress,
        center=center,
    )

    # Add gates from the tape
    for op in tape.operations:
        gate_name = PENNYLANE_GATE_MAP.get(op.name, op.name)
        wires = list(op.wires)

        # Extract parameters if any
        params: list[float | str] | None = None
        if op.parameters:
            params = [float(p) for p in op.parameters]

        circuit.add_gate(gate_name, wires, params)

    # Add measurements
    for measurement in tape.measurements:
        if hasattr(measurement, 'wires') and measurement.wires:
            for wire in measurement.wires:
                circuit.add_gate("Measure", [wire])

    return circuit.build()


def operations_from_qnode(
        qnode: QNodeProtocol,
        *args: Any,
        **kwargs: Any,
) -> list[tuple[str, list[int], list[float | str] | None]]:
    """
    Extract operations from a PennyLane QNode.

    Args:
        qnode: A PennyLane QNode function.
        *args: Positional arguments to pass to the QNode.
        **kwargs: Keyword arguments to pass to the QNode.

    Returns:
        List of (gate_name, wires, params) tuples.
    """
    try:
        import pennylane as qml
    except ImportError:
        raise ImportError(
            "PennyLane is required for this feature. "
            "Install it with: pip install pennylane"
        )

    # Use construct() to get the tape (works with PennyLane 0.44.0+)
    tape = qnode.construct(args, kwargs)

    operations: list[tuple[str, list[int], list[float | str] | None]] = []
    for op in tape.operations:
        gate_name = PENNYLANE_GATE_MAP.get(op.name, op.name)
        wires = list(op.wires)
        params: list[float | str] | None = [float(p) for p in op.parameters] if op.parameters else None
        operations.append((gate_name, wires, params))

    return operations
