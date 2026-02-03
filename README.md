# manim-quantum

[![PyPI version](https://badge.fury.io/py/manim-quantum.svg)](https://badge.fury.io/py/manim-quantum)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/professornova/manim-quantum/actions/workflows/ci.yml/badge.svg)](https://github.com/professornova/manim-quantum/actions)

A [Manim](https://www.manim.community/) plugin for creating beautiful quantum computing visualizations and animations.

<p>
  <img src="https://raw.githubusercontent.com/professornova/manim-quantum/main/docs/assets/demo.gif" width="600" alt="Demo animation">
</p>

## Features

- 🔧 **Quantum Circuits**: Create and animate quantum circuits with common gates
- 📊 **State Vectors**: Visualize quantum states with amplitudes or probability bars
- 🌐 **Bloch Sphere**: 3D Bloch sphere representations for single-qubit states
- 🔗 **PennyLane Integration**: Convert PennyLane QNodes to visual circuits
- 🎨 **Customizable Styles**: Multiple style presets (IBM, Google, dark, light)
- ✨ **Animations**: Built-in animations for circuit evaluation and state transitions

## Installation

```bash
pip install manim-quantum
```

With PennyLane integration:

```bash
pip install manim-quantum[pennylane]
```

For development:

```bash
pip install manim-quantum[dev]
```

## Quick Start

### Creating a Bell State Circuit

```python
from manim import *
from manim_quantum import QuantumCircuit, CircuitEvaluationAnimation


class BellCircuit(Scene):
    def construct(self):
        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        circuit.add_gate("CNOT", [0, 1])
        circuit.add_gate("Measure", [0])
        circuit.add_gate("Measure", [1])

        self.play(Create(circuit), run_time=2)
        self.wait(0.5)

        anim = CircuitEvaluationAnimation(circuit)
        self.play(anim.create_glow_animation(run_time=1.5))
        self.wait()
```

Render with:

```bash
manim -pql your_file.py BellCircuit
```

### PennyLane Integration

```python
import pennylane as qml
from manim_quantum.pennylane import circuit_from_qnode

# Define a PennyLane circuit
dev = qml.device("default.qubit", wires=2)


@qml.qnode(dev)
def my_circuit(theta):
    qml.RY(theta, wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))


# Convert to visual circuit
circuit = circuit_from_qnode(my_circuit, 0.5)
```

## Supported Gates

| Gate        | Syntax                         | Description                   |
|-------------|--------------------------------|-------------------------------|
| Hadamard    | `add_gate("H", [0])`           | Single-qubit Hadamard         |
| Identity    | `add_gate("I", [0])`           | Identity                      |
| Pauli-X     | `add_gate("X", [0])`           | Bit flip                      |
| Pauli-Y     | `add_gate("Y", [0])`           | Y rotation                    |
| Pauli-Z     | `add_gate("Z", [0])`           | Phase flip                    |
| Phase (S)   | `add_gate("S", [0])`           | Phase gate                    |
| Phase (Sdg) | `add_gate("Sdg", [0])`         | Phase gate (dagger)           |
| T           | `add_gate("T", [0])`           | T gate                        |
| Tdg         | `add_gate("Tdg", [0])`         | T gate (dagger)               |
| RX/RY/RZ    | `add_gate("RZ", [0], [theta])` | Rotation gates                |
| U           | `add_gate("U", [0], [t,p,l])`  | Generic single-qubit rotation |
| CNOT/CX     | `add_gate("CNOT", [0, 1])`     | Controlled-NOT                |
| CY          | `add_gate("CY", [0, 1])`       | Controlled-Y                  |
| CZ          | `add_gate("CZ", [0, 1])`       | Controlled-Z                  |
| SWAP        | `add_gate("SWAP", [0, 1])`     | Swap qubits                   |
| iSWAP       | `add_gate("ISWAP", [0, 1])`    | iSWAP gate                    |
| CRX/CRY/CRZ | `add_gate("CRZ", [0, 1], [t])` | Controlled rotations          |
| Measure/M   | `add_gate("Measure", [0])`     | Measurement                   |

## Styling

Use predefined style presets:

```python
from manim_quantum import QuantumCircuit
from manim_quantum.styles import StylePresets

# IBM Quantum-inspired style
circuit = QuantumCircuit(num_qubits=2, style=StylePresets.ibm())

# Google Quantum AI-inspired style  
circuit = QuantumCircuit(num_qubits=2, style=StylePresets.google())

# Dark theme
circuit = QuantumCircuit(num_qubits=2, style=StylePresets.dark())
```

Or create custom styles:

```python
from manim_quantum.styles import QuantumStyle

my_style = QuantumStyle(
    gate_stroke_color="#FF6B6B",
    wire_color="#4ECDC4",
    gate_fill_color="#1A1A2E",
)
```

## Examples

See the [examples/](examples/) directory for more complete examples:

- `basic_examples.py` - Circuit, state vector, and Bloch sphere demos
- More examples coming soon!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/professornova/manim-quantum.git
cd manim-quantum

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Manim Community](https://www.manim.community/)
- [PennyLane](https://pennylane.ai/)
