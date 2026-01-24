"""State vector visualization for quantum states."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    MathTex,
    Rectangle,
    VGroup,
)

from manim_quantum.states.ket import KetLabel

if TYPE_CHECKING:
    from manim_quantum.styles import QuantumStyle


class StateVector(VGroup):
    """
    Visual representation of a quantum state vector.

    Displays quantum states as either amplitude labels or probability bars.

    Args:
        amplitudes: Complex amplitudes for each basis state.
        show_probabilities: If True, show probability bars instead of amplitudes.
        num_qubits: Number of qubits (auto-detected if None).
        style: Visual style configuration.

    Example:
        >>> import numpy as np
        >>> sv = StateVector([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        >>> bell = StateVector.bell_state("phi+")
    """

    def __init__(
            self,
            amplitudes: list[complex] | np.ndarray,
            show_probabilities: bool = False,
            num_qubits: int | None = None,
            style: "QuantumStyle | None" = None,
    ) -> None:
        super().__init__()

        self.amplitudes = np.array(amplitudes, dtype=complex)
        self.show_probabilities = show_probabilities

        # Import here to avoid circular imports
        from manim_quantum.styles import QuantumStyle
        self.style = style or QuantumStyle()

        # Determine number of qubits
        if num_qubits is None:
            num_qubits = int(np.log2(len(self.amplitudes)))
        self.num_qubits = num_qubits

        self._build()

    def _build(self) -> None:
        """Build the state vector visualization."""
        n_states = len(self.amplitudes)

        if self.show_probabilities:
            self._build_probability_bars()
        else:
            self._build_amplitude_display()

    def _build_amplitude_display(self) -> None:
        """Build amplitude-based display (ket notation)."""
        terms = []

        for i, amp in enumerate(self.amplitudes):
            if abs(amp) < 1e-10:
                continue

            # Format amplitude
            amp_str = self._format_amplitude(amp)

            # Create basis state label
            basis = format(i, f'0{self.num_qubits}b')
            ket = KetLabel(basis, style=self.style)

            if amp_str:
                term = VGroup(
                    MathTex(amp_str, color=self.style.amplitude_color),
                    ket,
                )
                term.arrange(RIGHT, buff=0.05)
            else:
                term = ket

            terms.append(term)

        if not terms:
            # Zero state
            terms.append(MathTex("0", color=self.style.amplitude_color))

        # Arrange terms with + signs
        full_expr = VGroup()
        for i, term in enumerate(terms):
            if i > 0:
                plus = MathTex("+", color=self.style.amplitude_color)
                plus.scale(0.8)
                full_expr.add(plus)
            full_expr.add(term)
        full_expr.arrange(RIGHT, buff=0.15)

        self.add(full_expr)

    def _build_probability_bars(self) -> None:
        """Build probability bar visualization."""
        probabilities = np.abs(self.amplitudes) ** 2
        max_prob = max(probabilities) if max(probabilities) > 0 else 1

        bar_group = VGroup()
        max_bar_width = 2.0
        bar_height = 0.3

        for i, prob in enumerate(probabilities):
            # Basis state label
            basis = format(i, f'0{self.num_qubits}b')
            ket = KetLabel(basis, style=self.style)
            ket.scale(0.7)

            # Probability bar
            bar_width = (prob / max_prob) * max_bar_width if max_prob > 0 else 0
            bar = Rectangle(
                width=max(bar_width, 0.02),
                height=bar_height,
                fill_color=self.style.probability_bar_color,
                fill_opacity=0.8,
                stroke_color=self.style.probability_bar_stroke,
                stroke_width=1,
            )

            # Probability value
            prob_label = MathTex(f"{prob:.3f}", color=self.style.probability_text_color)
            prob_label.scale(0.5)

            # Arrange row: probability value on left, bar in middle, ket on right
            row = VGroup(prob_label, bar, ket)
            row.arrange(RIGHT, buff=0.2)

            bar_group.add(row)

        bar_group.arrange(DOWN, buff=0.2, aligned_edge=RIGHT)
        self.add(bar_group)

    def _format_amplitude(self, amp: complex) -> str:
        """Format a complex amplitude for display."""
        real = amp.real
        imag = amp.imag

        # Check for special values
        if abs(imag) < 1e-10:
            # Real amplitude
            if abs(real - 1) < 1e-10:
                return ""
            elif abs(real + 1) < 1e-10:
                return "-"
            elif abs(real - 1 / np.sqrt(2)) < 1e-10:
                return r"\frac{1}{\sqrt{2}}"
            elif abs(real + 1 / np.sqrt(2)) < 1e-10:
                return r"-\frac{1}{\sqrt{2}}"
            elif abs(real - 0.5) < 1e-10:
                return r"\frac{1}{2}"
            elif abs(real + 0.5) < 1e-10:
                return r"-\frac{1}{2}"
            else:
                return f"{real:.3f}"
        elif abs(real) < 1e-10:
            # Pure imaginary
            if abs(imag - 1) < 1e-10:
                return "i"
            elif abs(imag + 1) < 1e-10:
                return "-i"
            else:
                return f"{imag:.3f}i"
        else:
            # Complex
            return f"({real:.2f}{'+' if imag >= 0 else ''}{imag:.2f}i)"

    @classmethod
    def from_basis_state(
            cls,
            state: int | str,
            num_qubits: int = 1,
            **kwargs,
    ) -> StateVector:
        """
        Create a state vector for a computational basis state.

        Args:
            state: Basis state as integer or binary string (e.g., 0, "00", "101").
            num_qubits: Number of qubits.
            **kwargs: Additional arguments for StateVector.

        Returns:
            StateVector representing the basis state.
        """
        if isinstance(state, str):
            state = int(state, 2)
            num_qubits = max(num_qubits, len(bin(state)) - 2) if state > 0 else num_qubits

        n_states = 2 ** num_qubits
        amplitudes = np.zeros(n_states, dtype=complex)
        amplitudes[state] = 1.0

        return cls(amplitudes, num_qubits=num_qubits, **kwargs)

    @classmethod
    def superposition(cls, num_qubits: int = 1, **kwargs) -> StateVector:
        """
        Create an equal superposition state (|+⟩^⊗n).

        Args:
            num_qubits: Number of qubits.
            **kwargs: Additional arguments for StateVector.

        Returns:
            StateVector in equal superposition.
        """
        n_states = 2 ** num_qubits
        amplitudes = np.ones(n_states, dtype=complex) / np.sqrt(n_states)
        return cls(amplitudes, num_qubits=num_qubits, **kwargs)

    @classmethod
    def bell_state(
            cls,
            name: str = "phi+",
            **kwargs,
    ) -> StateVector:
        """
        Create a Bell state.

        Args:
            name: Bell state name ("phi+", "phi-", "psi+", "psi-").
            **kwargs: Additional arguments for StateVector.

        Returns:
            StateVector representing the Bell state.
        """
        sqrt2 = 1 / np.sqrt(2)

        bell_states = {
            "phi+": [sqrt2, 0, 0, sqrt2],  # (|00⟩ + |11⟩)/√2
            "phi-": [sqrt2, 0, 0, -sqrt2],  # (|00⟩ - |11⟩)/√2
            "psi+": [0, sqrt2, sqrt2, 0],  # (|01⟩ + |10⟩)/√2
            "psi-": [0, sqrt2, -sqrt2, 0],  # (|01⟩ - |10⟩)/√2
        }

        amplitudes = bell_states.get(name.lower(), bell_states["phi+"])
        return cls(amplitudes, num_qubits=2, **kwargs)

    @classmethod
    def ghz_state(cls, num_qubits: int = 3, **kwargs) -> StateVector:
        """
        Create a GHZ state.

        Args:
            num_qubits: Number of qubits (>= 2).
            **kwargs: Additional arguments for StateVector.

        Returns:
            StateVector representing the GHZ state.
        """
        n_states = 2 ** num_qubits
        amplitudes = np.zeros(n_states, dtype=complex)
        amplitudes[0] = 1 / np.sqrt(2)  # |00...0⟩
        amplitudes[-1] = 1 / np.sqrt(2)  # |11...1⟩
        return cls(amplitudes, num_qubits=num_qubits, **kwargs)
