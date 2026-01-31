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

    def test_circuit_compression_disabled(self):
        """Test circuit without compression (default behavior)."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=3, compress=False)
        circuit.add_gate("H", [0])
        circuit.add_gate("H", [1])
        circuit.add_gate("H", [2])

        # Without compression, gates should be placed sequentially
        positions = circuit._gate_x_positions
        assert len(positions) == 3
        # Each gate should be at a different x position
        assert positions[0] != positions[1]
        assert positions[1] != positions[2]

    def test_circuit_compression_enabled(self):
        """Test circuit with compression enabled."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=3, compress=True)
        circuit.add_gate("H", [0])
        circuit.add_gate("H", [1])
        circuit.add_gate("H", [2])

        # With compression, all three H gates on different wires should be at same x position
        positions = circuit._gate_x_positions
        assert len(positions) == 3
        assert positions[0] == positions[1] == positions[2]

    def test_circuit_compression_parallel_gates(self):
        """Test that non-overlapping gates are parallelized."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=4, compress=True)
        circuit.add_gate("H", [0])
        circuit.add_gate("X", [1])
        circuit.add_gate("Y", [2])
        circuit.add_gate("Z", [3])

        # All gates operate on different wires, so should be at same x position
        positions = circuit._gate_x_positions
        assert all(p == positions[0] for p in positions)

    def test_circuit_compression_sequential_on_same_wire(self):
        """Test that gates on the same wire remain sequential."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2, compress=True)
        circuit.add_gate("H", [0])
        circuit.add_gate("X", [0])
        circuit.add_gate("Y", [0])

        # Gates on same wire must be sequential
        positions = circuit._gate_x_positions
        assert positions[0] < positions[1] < positions[2]

    def test_circuit_compression_cnot_blocks_wires(self):
        """Test that multi-qubit gates properly block all involved wires."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=3, compress=True)
        circuit.add_gate("CNOT", [0, 1])  # Blocks wires 0 and 1
        circuit.add_gate("H", [0])  # Must wait for CNOT
        circuit.add_gate("H", [1])  # Must wait for CNOT
        circuit.add_gate("H", [2])  # Can be parallel with CNOT

        positions = circuit._gate_x_positions
        # CNOT and H on wire 2 should be at same position (layer 0)
        assert positions[0] == positions[3]
        # H gates on wires 0 and 1 should be in next layer
        assert positions[1] == positions[2]
        assert positions[1] > positions[0]

    def test_circuit_compression_mixed_scenario(self):
        """Test complex scenario with mixed gate dependencies."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=4, compress=True)
        # Layer 0: All parallel
        circuit.add_gate("H", [0])
        circuit.add_gate("H", [1])
        circuit.add_gate("H", [2])
        circuit.add_gate("H", [3])

        # Layer 1: CNOT blocks 0,1; X blocks 2
        circuit.add_gate("CNOT", [0, 1])
        circuit.add_gate("X", [2])

        # Layer 2: Y on wire 3 (can be in layer 1); Z on wire 0 (must be layer 2)
        circuit.add_gate("Y", [3])
        circuit.add_gate("Z", [0])

        positions = circuit._gate_x_positions

        # First 4 H gates should all be in layer 0
        assert positions[0] == positions[1] == positions[2] == positions[3]

        # CNOT and X should be in layer 1
        assert positions[4] == positions[5]
        assert positions[4] > positions[0]

        # Y on wire 3 should be in layer 1 (parallel with CNOT and X)
        assert positions[6] == positions[4]

        # Z on wire 0 must wait for CNOT, so layer 2
        assert positions[7] > positions[4]

    def test_circuit_compression_depth_reduction(self):
        """Test that compression actually reduces circuit depth."""
        from manim_quantum import QuantumCircuit

        # Without compression
        circuit_uncompressed = QuantumCircuit(num_qubits=3, compress=False)
        for i in range(3):
            circuit_uncompressed.add_gate("H", [i])

        # With compression
        circuit_compressed = QuantumCircuit(num_qubits=3, compress=True)
        for i in range(3):
            circuit_compressed.add_gate("H", [i])

        # Count unique x positions (layers)
        uncompressed_depth = len(set(circuit_uncompressed._gate_x_positions))
        compressed_depth = len(set(circuit_compressed._gate_x_positions))

        # Compressed should have fewer layers
        assert compressed_depth < uncompressed_depth
        assert compressed_depth == 1  # All gates can be parallel
        assert uncompressed_depth == 3  # All gates are sequential

    def test_circuit_compression_preserves_functionality(self):
        """Test that compression doesn't change gate order on same wire."""
        from manim_quantum import QuantumCircuit

        circuit = QuantumCircuit(num_qubits=2, compress=True)
        circuit.add_gate("H", [0])
        circuit.add_gate("X", [1])
        circuit.add_gate("Y", [0])
        circuit.add_gate("Z", [1])

        # Check gates on wire 0: H then Y
        wire_0_gates = [g for g in circuit._gates if 0 in g.target_wires]
        assert len(wire_0_gates) == 2
        assert wire_0_gates[0].name == "H"
        assert wire_0_gates[1].name == "Y"

        # Check gates on wire 1: X then Z
        wire_1_gates = [g for g in circuit._gates if 1 in g.target_wires]
        assert len(wire_1_gates) == 2
        assert wire_1_gates[0].name == "X"
        assert wire_1_gates[1].name == "Z"


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
        assert sphere.get_theta() == 0.0
        assert sphere.get_phi() == 0.0

    def test_bloch_sphere_with_initial_state(self):
        """Test Bloch sphere with initial state."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere(initial_state=(np.pi / 2, 0))
        assert np.isclose(sphere.get_theta(), np.pi / 2)
        assert np.isclose(sphere.get_phi(), 0)

    def test_basis_state_creation(self):
        """Test basis state Bloch sphere."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere.basis_state("0")
        assert sphere.get_theta() == 0

        sphere = BlochSphere.basis_state("1")
        assert np.isclose(sphere.get_theta(), np.pi)

    def test_plus_state(self):
        """Test |+⟩ state Bloch sphere."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere.plus_state()
        assert np.isclose(sphere.get_theta(), np.pi / 2)
        assert np.isclose(sphere.get_phi(), 0)

    def test_set_state(self):
        """Test setting Bloch sphere state."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere()
        sphere.set_state(np.pi / 4, np.pi / 3)

        assert np.isclose(sphere.get_theta(), np.pi / 4)
        assert np.isclose(sphere.get_phi(), np.pi / 3)

    def test_get_state_amplitudes(self):
        """Test getting state amplitudes."""
        from manim_quantum import BlochSphere

        # |0⟩ state
        sphere = BlochSphere.basis_state("0")
        alpha, beta = sphere.get_state_amplitudes()
        assert np.isclose(abs(alpha), 1.0)
        assert np.isclose(abs(beta), 0.0)

    def test_set_state_updates_arrow_in_place(self):
        """Test that set_state updates arrow without recreating it."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere()
        original_arrow = sphere.state_arrow

        # Update state
        sphere.set_state(np.pi / 2, np.pi / 4)

        # Arrow should be the same object, just updated
        assert sphere.state_arrow is original_arrow
        assert np.isclose(sphere.get_theta(), np.pi / 2)
        assert np.isclose(sphere.get_phi(), np.pi / 4)

    def test_get_theta(self):
        """Test get_theta method."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere(initial_state=(np.pi / 3, np.pi / 4))
        assert np.isclose(sphere.get_theta(), np.pi / 3)

    def test_get_phi(self):
        """Test get_phi method."""
        from manim_quantum import BlochSphere

        sphere = BlochSphere(initial_state=(np.pi / 3, np.pi / 4))
        assert np.isclose(sphere.get_phi(), np.pi / 4)


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


class TestBlochSphereAnimations:
    """Tests for Bloch sphere animation classes."""

    def test_state_transition_creation(self):
        """Test BlochSphereStateTransition creation."""
        from manim_quantum import BlochSphere, BlochSphereStateTransition

        sphere = BlochSphere.basis_state("0")
        anim = BlochSphereStateTransition(sphere, np.pi / 2, 0)

        assert anim.bloch_sphere is sphere
        assert np.isclose(anim.initial_theta, 0)
        assert np.isclose(anim.initial_phi, 0)
        assert np.isclose(anim.target_theta, np.pi / 2)
        assert np.isclose(anim.target_phi, 0)

    def test_state_transition_interpolation(self):
        """Test BlochSphereStateTransition interpolation."""
        from manim_quantum import BlochSphere, BlochSphereStateTransition

        sphere = BlochSphere.basis_state("0")
        anim = BlochSphereStateTransition(sphere, np.pi, 0)

        # Test interpolation at alpha=0.5 (halfway)
        anim.interpolate_mobject(0.5)
        assert np.isclose(sphere.get_theta(), np.pi / 2)
        assert np.isclose(sphere.get_phi(), 0)

        # Test interpolation at alpha=1.0 (end)
        anim.interpolate_mobject(1.0)
        assert np.isclose(sphere.get_theta(), np.pi)
        assert np.isclose(sphere.get_phi(), 0)

    def test_rotation_animation_creation(self):
        """Test BlochSphereRotation creation."""
        from manim_quantum import BlochSphere, BlochSphereRotation

        sphere = BlochSphere.basis_state("0")
        anim = BlochSphereRotation(sphere, "y", np.pi / 2)

        assert anim.bloch_sphere is sphere
        assert anim.axis == "y"
        assert np.isclose(anim.angle, np.pi / 2)

    def test_rotation_around_y_axis(self):
        """Test rotation around Y axis."""
        from manim_quantum import BlochSphere, BlochSphereRotation

        # Start at |0⟩ (north pole)
        sphere = BlochSphere.basis_state("0")
        anim = BlochSphereRotation(sphere, "y", np.pi / 2)

        # After π/2 rotation around Y, should be at equator
        anim.interpolate_mobject(1.0)
        assert np.isclose(sphere.get_theta(), np.pi / 2, atol=1e-6)

    def test_rotation_around_x_axis(self):
        """Test rotation around X axis."""
        from manim_quantum import BlochSphere, BlochSphereRotation

        sphere = BlochSphere.basis_state("0")
        anim = BlochSphereRotation(sphere, "x", np.pi / 2)

        # Rotation should update the state
        anim.interpolate_mobject(1.0)
        # State should have changed from initial
        assert not (np.isclose(sphere.get_theta(), 0) and np.isclose(sphere.get_phi(), 0))

    def test_rotation_around_z_axis(self):
        """Test rotation around Z axis."""
        from manim_quantum import BlochSphere, BlochSphereRotation

        # Start at |+⟩ (on equator at phi=0)
        sphere = BlochSphere.plus_state()
        anim = BlochSphereRotation(sphere, "z", np.pi / 2)

        # After π/2 rotation around Z, phi should change by π/2
        initial_phi = sphere.get_phi()
        anim.interpolate_mobject(1.0)
        # Theta should stay the same (still on equator)
        assert np.isclose(sphere.get_theta(), np.pi / 2, atol=1e-6)
        # Phi should have rotated
        assert np.isclose(sphere.get_phi(), initial_phi + np.pi / 2, atol=1e-6)

    def test_rotation_invalid_axis(self):
        """Test that invalid axis raises error."""
        from manim_quantum import BlochSphere, BlochSphereRotation
        import pytest

        sphere = BlochSphere.basis_state("0")

        with pytest.raises(ValueError, match="Invalid axis"):
            BlochSphereRotation(sphere, "w", np.pi / 2)
