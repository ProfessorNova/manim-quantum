"""Core functionality tests for manim-quantum."""

from __future__ import annotations

import numpy as np


class TestQuantumCircuit:
    """Tests for QuantumCircuit class."""

    def test_circuit_creation(self):
        """Test basic circuit creation."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        assert circuit.num_qubits == 2
        assert len(circuit._wires) == 2

    def test_circuit_with_custom_params(self):
        """Test circuit with custom parameters."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(
            num_qubits=3,
            x_start=-4,
            x_end=4,
            wire_spacing=1.5,
        )
        assert circuit.num_qubits == 3
        assert circuit.x_start == -4
        assert circuit.x_end == 4
        assert circuit.wire_spacing == 1.5

    def test_add_single_qubit_gate(self):
        """Test adding a single-qubit gate."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        gate = circuit.add_gate("H", [0])

        assert gate.name == "H"
        assert gate.target_wires == [0]
        assert len(circuit._gates) == 1

    def test_add_two_qubit_gate(self):
        """Test adding a two-qubit gate."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        gate = circuit.add_gate("CNOT", [0, 1])

        assert gate.name == "CNOT"
        assert gate.target_wires == [0, 1]

    def test_add_parameterized_gate(self):
        """Test adding a parameterized gate."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=1)
        gate = circuit.add_gate("RZ", [0], params=[np.pi / 4])

        assert gate.name == "RZ"
        assert gate.params == [np.pi / 4]

    def test_add_multiple_gates(self):
        """Test adding multiple gates at once."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        gates = circuit.add_gates([
            ("H", [0]),
            ("CNOT", [0, 1]),
        ])

        assert len(gates) == 2
        assert len(circuit._gates) == 2

    def test_circuit_build(self):
        """Test circuit build method."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        result = circuit.build()

        # Should return self for chaining
        assert result is circuit

    def test_circuit_from_operations(self):
        """Test creating circuit from operations list."""
        from manim_quantum import QuantumCircuit

        operations = [
            ("H", [0], None),
            ("CNOT", [0, 1], None),
            ("RZ", [1], [np.pi / 2]),
        ]
        circuit = QuantumCircuit.from_operations(operations, num_qubits=2)

        assert circuit.num_qubits == 2
        assert len(circuit._gates) == 3


class TestQuantumGate:
    """Tests for QuantumGate class."""

    def test_gate_creation(self):
        """Test basic gate creation."""
        from manim_quantum import QuantumGate

        gate = QuantumGate("H", [0])
        assert gate.name == "H"
        assert gate.target_wires == [0]

    def test_gate_with_params(self):
        """Test gate with parameters."""
        from manim_quantum import QuantumGate

        gate = QuantumGate("RX", [0], params=[np.pi / 2])
        assert gate.params == [np.pi / 2]


class TestQuantumWire:
    """Tests for QuantumWire class."""

    def test_wire_creation(self):
        """Test basic wire creation."""
        from manim_quantum import QuantumWire

        wire = QuantumWire(index=0, x_start=-5, x_end=5, y=0)
        assert wire.index == 0
        assert wire.x_start == -5
        assert wire.x_end == 5
        assert wire.y == 0

    def test_wire_with_label(self):
        """Test wire with label."""
        from manim_quantum import QuantumWire

        wire = QuantumWire(index=0, x_start=-5, x_end=5, y=0, label="|0\\rangle")
        assert wire.label_text == "|0\\rangle"

    def test_wire_masking(self):
        """Test wire region masking."""
        from manim_quantum import QuantumWire

        wire = QuantumWire(index=0, x_start=-5, x_end=5, y=0)
        wire.mask_region(0, 0.3)

        assert len(wire._masked_regions) == 1
        assert wire._masked_regions[0] == (0, 0.3)


class TestStateVector:
    """Tests for StateVector class."""

    def test_state_vector_creation(self, sample_amplitudes):
        """Test state vector creation."""
        from manim_quantum import StateVector

        sv = StateVector(sample_amplitudes)
        assert np.allclose(sv.amplitudes, sample_amplitudes)
        assert sv.num_qubits == 2

    def test_basis_state_creation(self):
        """Test basis state creation."""
        from manim_quantum import StateVector

        sv = StateVector.from_basis_state(0, num_qubits=1)
        assert sv.num_qubits == 1
        assert np.allclose(sv.amplitudes, [1, 0])

    def test_superposition_creation(self):
        """Test superposition state creation."""
        from manim_quantum import StateVector

        sv = StateVector.superposition(num_qubits=1)
        expected = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
        assert np.allclose(sv.amplitudes, expected)

    def test_bell_state_creation(self):
        """Test Bell state creation."""
        from manim_quantum import StateVector

        sv = StateVector.bell_state("phi+")
        expected = np.array([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
        assert np.allclose(sv.amplitudes, expected)

    def test_ghz_state_creation(self):
        """Test GHZ state creation."""
        from manim_quantum import StateVector

        sv = StateVector.ghz_state(num_qubits=3)
        assert sv.num_qubits == 3
        assert np.isclose(abs(sv.amplitudes[0]) ** 2, 0.5)
        assert np.isclose(abs(sv.amplitudes[-1]) ** 2, 0.5)


class TestKetLabel:
    """Tests for KetLabel class."""

    def test_ket_creation(self):
        """Test ket label creation."""
        from manim_quantum import KetLabel

        ket = KetLabel("0")
        assert ket.content == "0"

    def test_ket_basis(self):
        """Test ket basis creation."""
        from manim_quantum import KetLabel

        ket = KetLabel.basis(0, num_qubits=2)
        assert ket.content == "00"


class TestBlochSphere:
    """Tests for BlochSphere class."""

    def test_bloch_sphere_creation(self):
        """Test Bloch sphere creation."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere()
        assert sphere.radius == 2.0
        assert sphere._theta == 0.0
        assert sphere._phi == 0.0

    def test_bloch_sphere_with_initial_state(self):
        """Test Bloch sphere with initial state."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere(initial_state=(np.pi / 2, 0))
        assert np.isclose(sphere._theta, np.pi / 2)
        assert np.isclose(sphere._phi, 0)

    def test_basis_state_creation(self):
        """Test basis state Bloch sphere."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere.basis_state("0")
        assert sphere._theta == 0

        sphere = BlochSphere.basis_state("1")
        assert np.isclose(sphere._theta, np.pi)

    def test_plus_state(self):
        """Test |+⟩ state Bloch sphere."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere.plus_state()
        assert np.isclose(sphere._theta, np.pi / 2)
        assert np.isclose(sphere._phi, 0)

    def test_set_state(self):
        """Test setting Bloch sphere state."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere()
        sphere.set_state(np.pi / 4, np.pi / 3)

        assert np.isclose(sphere._theta, np.pi / 4)
        assert np.isclose(sphere._phi, np.pi / 3)

    def test_get_state_amplitudes(self):
        """Test getting state amplitudes."""
        from manim_quantum import BlochSphere

        # |0⟩ state
        sphere = BlochSphere.basis_state("0")
        alpha, beta = sphere.get_state_amplitudes()
        assert np.isclose(abs(alpha), 1.0)
        assert np.isclose(abs(beta), 0.0)


class TestQuantumStyle:
    """Tests for QuantumStyle class."""

    def test_default_style(self):
        """Test default style creation."""
        from manim_quantum.styles import QuantumStyle

        style = QuantumStyle()
        assert style.gate_width == 0.6
        assert style.wire_stroke_width == 2.0

    def test_custom_style(self):
        """Test custom style creation."""
        from manim_quantum.styles import QuantumStyle

        style = QuantumStyle(gate_width=0.8, wire_color="#FF0000")
        assert style.gate_width == 0.8
        assert style.wire_color == "#FF0000"


class TestStylePresets:
    """Tests for StylePresets class."""

    def test_ibm_preset(self):
        """Test IBM style preset."""
        from manim_quantum.styles import StylePresets

        style = StylePresets.ibm()
        assert style.gate_fill_color == "#6929C4"

    def test_google_preset(self):
        """Test Google style preset."""
        from manim_quantum.styles import StylePresets

        style = StylePresets.google()
        assert style.gate_fill_color == "#4285F4"

    def test_dark_preset(self):
        """Test dark style preset."""
        from manim_quantum.styles import StylePresets

        style = StylePresets.dark()
        assert style.gate_fill_color == "#1E1E2E"

    def test_light_preset(self):
        """Test light style preset."""
        from manim_quantum.styles import StylePresets

        style = StylePresets.light()
        assert style.gate_fill_color == "#FFFFFF"


class TestCircuitEvaluationAnimation:
    """Tests for CircuitEvaluationAnimation class."""

    def test_animation_creation(self):
        """Test basic animation factory creation."""
        from manim_quantum import CircuitEvaluationAnimation, QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        circuit.build()

        anim_factory = CircuitEvaluationAnimation(circuit)
        assert anim_factory.circuit is circuit

    def test_glow_animation(self):
        """Test glow animation creation."""
        from manim_quantum import CircuitEvaluationAnimation, QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        circuit.build()

        anim_factory = CircuitEvaluationAnimation(circuit)
        anim = anim_factory.create_glow_animation()
        assert anim is not None

    def test_shot_animation(self):
        """Test shot animation creation."""
        from manim_quantum import CircuitEvaluationAnimation, QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        circuit.build()

        anim_factory = CircuitEvaluationAnimation(circuit)
        anim = anim_factory.create_shot_animation()
        assert anim is not None

    def test_animation_with_specific_wires(self):
        """Test animations can be limited to specific wires."""
        from manim_quantum import CircuitEvaluationAnimation, QuantumCircuit

        circuit = QuantumCircuit(num_qubits=3)
        circuit.add_gate("H", [0])
        circuit.add_gate("H", [1])
        circuit.add_gate("H", [2])
        circuit.build()

        anim_factory = CircuitEvaluationAnimation(circuit)
        # Test that specifying wires doesn't raise an error
        anim = anim_factory.create_glow_animation(wires=[0, 1])
        assert anim is not None

        anim = anim_factory.create_shot_animation(wires=[0])
        assert anim is not None
