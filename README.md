# manim-quantum

[![PyPI version](https://badge.fury.io/py/manim-quantum.svg)](https://badge.fury.io/py/manim-quantum)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/professornova/manim-quantum/actions/workflows/tests.yml/badge.svg)](https://github.com/professornova/manim-quantum/actions)

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
from manim_quantum import QuantumCircuit


class BellCircuit(Scene):
    def construct(self):
        # Create a 2-qubit circuit
        circuit = QuantumCircuit(num_qubits=2)

        # Add gates
        circuit.add_gate("H", [0])  # Hadamard on qubit 0
        circuit.add_gate("CNOT", [0, 1])  # CNOT with control=0, target=1
        circuit.add_gate("Measure", [0, 1])  # Measure both qubits

        # Build and display
        circuit.build()
        self.play(Create(circuit))

        # Animate circuit evaluation
        self.play(circuit.create_glow_animation())
```

Render with:

```bash
manim -pql your_file.py BellCircuit
```

### Visualizing State Vectors

```python
from manim import *
from manim_quantum import StateVector


class StateDemo(Scene):
    def construct(self):
        # Create a Bell state
        bell = StateVector.bell_state("phi+")

        # Or from explicit amplitudes
        import numpy as np
        custom = StateVector([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])

        # Show probability bars instead of amplitudes
        with_bars = StateVector.bell_state("phi+", show_probabilities=True)

        self.play(FadeIn(bell))
```

### Bloch Sphere Visualization

```python
from manim import *
from manim_quantum import BlochSphere


class BlochDemo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create Bloch sphere at |0⟩ state
        bloch = BlochSphere.basis_state("0")
        self.play(Create(bloch))

        # Animate to |+⟩ state (after Hadamard)
        import numpy as np
        self.play(bloch.animate.set_state(np.pi / 2, 0))
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

| Gate     | Syntax                     | Description           |
|----------|----------------------------|-----------------------|
| Hadamard | `add_gate("H", [0])`       | Single-qubit Hadamard |
| Pauli-X  | `add_gate("X", [0])`       | Bit flip              |
| Pauli-Y  | `add_gate("Y", [0])`       | Y rotation            |
| Pauli-Z  | `add_gate("Z", [0])`       | Phase flip            |
| CNOT     | `add_gate("CNOT", [0, 1])` | Controlled-NOT        |
| CZ       | `add_gate("CZ", [0, 1])`   | Controlled-Z          |
| SWAP     | `add_gate("SWAP", [0, 1])` | Swap qubits           |
| RX/RY/RZ | `add_gate("RZ", [0], [θ])` | Rotation gates        |
| Measure  | `add_gate("Measure", [0])` | Measurement           |

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

## Documentation

Full documentation is available at [manim-quantum.readthedocs.io](https://manim-quantum.readthedocs.io).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/professornova/manim-quantum.git
cd manim-quantum

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Roadmap

- [ ] More gate types (Toffoli, custom unitaries)
- [ ] Quantum error visualization
- [ ] Circuit optimization animations
- [ ] Density matrix visualization
- [ ] Multi-qubit Bloch sphere alternatives
- [ ] Interactive components

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use manim-quantum in academic work, please cite:

```bibtex
@software{manim_quantum,
  title = {manim-quantum: Quantum Computing Visualizations for Manim},
  author = {manim-quantum contributors},
  year = {2025},
  url = {https://github.com/professornova/manim-quantum}
}
```

## Acknowledgments

- [Manim Community](https://www.manim.community/) for the amazing animation library
- [PennyLane](https://pennylane.ai/) for quantum computing framework integration
- The quantum computing education community

---

Made with ❤️ for quantum education
