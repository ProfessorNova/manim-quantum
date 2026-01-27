"""PennyLane QNode to QuantumCircuit converter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from manim_quantum.circuits.circuit import QuantumCircuit
    from manim_quantum.styles import QuantumStyle


@runtime_checkable
class QNodeProtocol(Protocol):
    """Protocol for PennyLane QNode objects."""

    tape: Any

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the QNode."""
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


def circuit_from_qnode(
        qnode: QNodeProtocol,
        *args: Any,
        style: "QuantumStyle | None" = None,
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

    # Execute the QNode to populate the tape
    _ = qnode(*args, **kwargs)

    # Get the tape (circuit representation)
    tape = qnode.tape

    # Determine number of qubits
    num_wires = len(tape.wires)

    # Create the circuit
    circuit = QuantumCircuit(num_qubits=num_wires, style=style)

    # Add gates from the tape
    for op in tape.operations:
        gate_name = PENNYLANE_GATE_MAP.get(op.name, op.name)
        wires = list(op.wires)

        # Extract parameters if any
        params = None
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
) -> list[tuple[str, list[int], list[float] | None]]:
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

    # Execute the QNode to populate the tape
    _ = qnode(*args, **kwargs)
    tape = qnode.tape

    operations = []
    for op in tape.operations:
        gate_name = PENNYLANE_GATE_MAP.get(op.name, op.name)
        wires = list(op.wires)
        params = [float(p) for p in op.parameters] if op.parameters else None
        operations.append((gate_name, wires, params))

    return operations
