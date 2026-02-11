"""
Example scenes demonstrating manim-quantum capabilities.

Run these examples with:
    manim -pql examples/basic_examples.py BellStateCircuit
    manim -pql examples/basic_examples.py StateVectorDemo
    manim -pql examples/basic_examples.py BlochSphereDemo
    ... and so on for other scenes.
"""
import numpy as np
from manim import (
    DEGREES,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    MathTex,
    Scene,
    Text,
    ThreeDScene,
    Write,
)

from manim_quantum import (
    BlochSphere,
    BlochSphereStateTransition,
    CircuitEvaluationAnimation,
    QuantumCircuit,
    StateVector,
)
from manim_quantum.styles import StylePresets


class BellStateCircuit(Scene):
    """
    Demonstrates a simple Bell state preparation circuit.

    Shows:
    - Basic circuit creation
    - Adding gates (H, CNOT, Measure)
    - Glow animation for circuit evaluation using animations module
    """

    def construct(self):
        # Title
        title = Text("Bell State Preparation", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Create circuit
        circuit = QuantumCircuit(num_qubits=2)
        circuit.add_gate("H", [0])
        circuit.add_gate("CNOT", [0, 1])
        circuit.add_gate("Measure", [0])
        circuit.add_gate("Measure", [1])
        circuit.build()

        # Position and show circuit (no default offset)
        self.play(Write(circuit), run_time=2)
        self.wait(0.5)

        # Use the animations module for circuit evaluation
        anim = CircuitEvaluationAnimation(circuit)
        self.play(anim.create_shot_animation(run_time=1.5))
        self.wait()


class StateVectorDemo(Scene):
    """
    Demonstrates state vector visualization.

    Shows:
    - Creating state vectors for basis states
    - Equal superposition (|+⟩)
    - Bell state
    - Probability bar visualization
    """

    def construct(self):
        # Title
        title = Text("Quantum State Vectors", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Basis state |0⟩
        sv_0 = StateVector.from_basis_state(0, num_qubits=1)
        sv_0.shift(LEFT * 4 + UP * 1.5)

        label_0 = MathTex(r"|0\rangle", r"\text{ state}", font_size=30)
        label_0.next_to(sv_0, DOWN)

        self.play(FadeIn(sv_0), Write(label_0))
        self.wait(0.5)

        # Superposition |+⟩
        sv_plus = StateVector.superposition(num_qubits=1)
        sv_plus.shift(UP * 1.5)

        label_plus = MathTex(r"|+\rangle", r"\text{ state}", font_size=30)
        label_plus.next_to(sv_plus, DOWN)

        self.play(FadeIn(sv_plus), Write(label_plus))
        self.wait(0.5)

        # Bell state
        sv_bell = StateVector.bell_state("phi+")
        sv_bell.shift(RIGHT * 4 + UP * 1.5)

        label_bell = MathTex(r"\text{Bell } |\Phi^+\rangle", font_size=30)
        label_bell.next_to(sv_bell, DOWN)

        self.play(FadeIn(sv_bell), Write(label_bell))
        self.wait()

        # Fade out the amplitude displays and show probability bars version
        self.play(
            FadeOut(sv_0), FadeOut(sv_plus), FadeOut(sv_bell),
            FadeOut(label_0), FadeOut(label_plus), FadeOut(label_bell)
        )

        sv_prob = StateVector.bell_state("phi+", show_probabilities=True)
        sv_prob.shift(DOWN * 0.5)

        prob_label = MathTex(r"\text{Probability bars for } |\Phi^+\rangle", font_size=30)
        prob_label.next_to(sv_prob, UP, buff=0.5)

        self.play(FadeIn(sv_prob), Write(prob_label))
        self.wait()


class BlochSphereDemo(ThreeDScene):
    """
    Demonstrates Bloch sphere visualization.

    Shows:
    - Basic Bloch sphere creation
    - Different quantum states
    - State transitions along the surface
    - Labels that always face the camera

    Note: Requires ThreeDScene for proper 3D rendering.
    """

    def construct(self):
        # Set up camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create Bloch sphere at |0⟩ with thicker arrow
        bloch = BlochSphere.basis_state("0", radius=2, arrow_thickness=0.04)

        # Make labels always face the camera
        bloch.add_labels_to_scene(self)

        self.play(FadeIn(bloch), run_time=2)
        self.wait()

        # Transition to |+⟩ state (after H gate)
        # Arrow smoothly moves along the surface
        self.play(
            BlochSphereStateTransition(bloch, np.pi / 2, 0),
            run_time=1.5,
        )
        self.wait(2)

        # Transition to |1⟩ state
        self.play(
            BlochSphereStateTransition(bloch, np.pi, 0),
            run_time=1.5,
        )
        self.wait(2)


class StyleShowcase(Scene):
    """
    Demonstrates different visual styles.

    Shows the same circuit rendered with different style presets.
    """

    def construct(self):
        title = Text("Style Presets", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        styles = [
            ("Default", StylePresets.default()),
            ("IBM", StylePresets.ibm()),
            ("Google", StylePresets.google()),
        ]

        circuits = []
        for i, (name, style) in enumerate(styles):
            circuit = QuantumCircuit(num_qubits=2, style=style)
            circuit.add_gate("H", [0])
            circuit.add_gate("CNOT", [0, 1])
            circuit.build()

            label = Text(name, font_size=20)

            circuit.scale(0.6)
            circuit.shift(DOWN * (i - 1) * 2)

            label.next_to(circuit, LEFT, buff=0.5)

            circuits.append((circuit, label))

        for circuit, label in circuits:
            self.play(Write(circuit), Write(label), run_time=1)

        self.wait(2)


# Entry point for running all examples
if __name__ == "__main__":
    print("Run examples with:")
    print("  manim -pql examples/basic_examples.py BellStateCircuit")
    print("  manim -pql examples/basic_examples.py StateVectorDemo")
    print("  manim -pql examples/basic_examples.py BlochSphereDemo")
    print("  ... and so on for other scenes.")
