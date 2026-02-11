"""
Example scenes demonstrating PennyLane integration with manim-quantum.

These examples show how to visualize PennyLane quantum circuits using manim-quantum.
The circuit_from_qnode function automatically converts PennyLane QNodes into
visualizable quantum circuits.

Run these examples with:
    manim -pql examples/pennylane_examples.py UsingPennylane
    manim -pql examples/pennylane_examples.py UsingPennylaneWithParameter
"""
from manim import PI, DOWN, UP, Scene, ValueTracker, Write
import pennylane as qml

from manim_quantum import (
    CircuitEvaluationAnimation,
    StateVector,
    circuit_from_qnode,
)


class UsingPennylane(Scene):
    """
    Basic example of using PennyLane with manim-quantum.

    This scene demonstrates:
    - Creating a quantum circuit using PennyLane's QNode
    - Converting the QNode to a manim-quantum circuit
    - Animating the circuit with glow effects
    """
    def construct(self):
        dev = qml.device("default.qubit", wires=2)

        @qml.qnode(dev)
        def my_circuit(theta):
            qml.RY(theta, wires=0)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliZ(0))

        circuit = circuit_from_qnode(my_circuit, 0.5, x_start=-3, x_end=3)
        self.play(Write(circuit), run_time=2)
        self.wait(0.5)

        anim = CircuitEvaluationAnimation(circuit)
        self.play(anim.create_glow_animation(run_time=1.5))
        self.wait()


class UsingPennylaneWithParameter(Scene):
    """
    Advanced example showing animated parameters with PennyLane circuits.

    This scene demonstrates:
    - Using ValueTracker to create animated parameters
    - Real-time updates of circuit visualization as parameters change
    - Synchronized state vector display showing quantum state evolution
    - Smooth animation of parameter values from 0.5 to π to 0
    """
    def construct(self):
        dev = qml.device("default.qubit", wires=2)

        @qml.qnode(dev)
        def my_circuit(theta):
            qml.RY(theta, wires=0)
            qml.CNOT(wires=[0, 1])
            return qml.state()

        theta = ValueTracker(0.5)
        circuit = circuit_from_qnode(my_circuit, theta.get_value()).move_to(UP)

        sv = StateVector(my_circuit(theta.get_value()), show_probabilities=True)
        sv.move_to(DOWN)

        circuit.add_updater(lambda m: m.become(circuit_from_qnode(my_circuit, theta.get_value()).move_to(UP)))
        sv.add_updater(lambda m: m.become(StateVector(my_circuit(theta.get_value()), show_probabilities=True).move_to(DOWN)))

        self.play(Write(circuit), Write(sv))
        self.wait(0.5)

        self.play(theta.animate.set_value(PI), run_time=3)
        self.wait()

        self.play(theta.animate.set_value(0), run_time=3)
        self.wait()
