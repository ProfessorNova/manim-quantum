"""Ket label helper for quantum state notation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from manim import MathTex, VGroup

if TYPE_CHECKING:
    from manim_quantum.styles import QuantumStyle


class KetLabel(VGroup):
    """
    A ket notation label (|ψ⟩).

    Args:
        content: Content inside the ket (e.g., "0", "1", "ψ", "00").
        style: Visual style configuration.

    Example:
        >>> ket = KetLabel("0")  # Creates |0⟩
        >>> ket = KetLabel("\\psi")  # Creates |ψ⟩
    """

    def __init__(
            self,
            content: str,
            style: "QuantumStyle | None" = None,
    ) -> None:
        super().__init__()

        self.content = content

        # Import here to avoid circular imports
        from manim_quantum.styles import QuantumStyle
        self.style = style or QuantumStyle()

        self._build()

    def _build(self) -> None:
        """Build the ket label."""
        # Kets always use LaTeX for proper mathematical notation
        tex = MathTex(
            f"|{self.content}\\rangle",
            color=self.style.ket_color,
        )
        self.add(tex)

    @classmethod
    def basis(cls, state: int | str, num_qubits: int = 1, **kwargs) -> "KetLabel":
        """
        Create a ket label for a basis state.

        Args:
            state: Basis state as integer or binary string.
            num_qubits: Number of qubits for formatting.
            **kwargs: Additional arguments.

        Returns:
            KetLabel for the basis state.
        """
        if isinstance(state, int):
            state = format(state, f'0{num_qubits}b')
        return cls(state, **kwargs)

    @classmethod
    def zero(cls, **kwargs) -> "KetLabel":
        """Create |0⟩ ket."""
        return cls("0", **kwargs)

    @classmethod
    def one(cls, **kwargs) -> "KetLabel":
        """Create |1⟩ ket."""
        return cls("1", **kwargs)

    @classmethod
    def plus(cls, **kwargs) -> "KetLabel":
        """Create |+⟩ ket."""
        return cls("+", **kwargs)

    @classmethod
    def minus(cls, **kwargs) -> "KetLabel":
        """Create |-⟩ ket."""
        return cls("-", **kwargs)

    @classmethod
    def psi(cls, **kwargs) -> "KetLabel":
        """Create |ψ⟩ ket."""
        return cls(r"\psi", **kwargs)

    @classmethod
    def phi(cls, **kwargs) -> "KetLabel":
        """Create |φ⟩ ket."""
        return cls(r"\phi", **kwargs)
