"""Quantum wire visualization with masking support."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import (
    LEFT,
    Line,
    MathTex,
    VGroup,
)

if TYPE_CHECKING:
    from manim_quantum.styles import QuantumStyle


class QuantumWire(VGroup):
    """
    A quantum wire (qubit line) with support for gate masking.

    The wire can have masked regions where gates are placed, creating
    visual breaks in the wire line.

    Args:
        index: Wire index (0-based).
        x_start: Left x-coordinate.
        x_end: Right x-coordinate.
        y: y-coordinate of the wire.
        label: Optional label for the wire (e.g., "|0⟩").
        style: Visual style configuration.

    Example:
        >>> wire = QuantumWire(index=0, x_start=-5, x_end=5, y=0)
        >>> wire.mask_region(0, 0.3)  # Mask from -0.3 to 0.3
        >>> wire.rebuild_segments()
    """

    def __init__(
            self,
            index: int,
            x_start: float,
            x_end: float,
            y: float,
            label: str | None = None,
            style: "QuantumStyle | None" = None,
    ) -> None:
        super().__init__()

        self.index = index
        self.x_start = x_start
        self.x_end = x_end
        self.y = y
        self.label_text = label

        # Import here to avoid circular imports
        from manim_quantum.styles import QuantumStyle
        self.style = style or QuantumStyle()

        # Masked regions: list of (center_x, half_width)
        self._masked_regions: list[tuple[float, float]] = []

        # Wire segments
        self._segments: list[Line] = []
        self._label: MathTex | None = None

        self._build_initial()

    def _build_initial(self) -> None:
        """Build the initial wire (single line)."""
        line = Line(
            start=[self.x_start, self.y, 0],
            end=[self.x_end, self.y, 0],
            color=self.style.wire_color,
            stroke_width=self.style.wire_stroke_width,
        )
        self._segments.append(line)
        self.add(line)

        # Add label if provided
        if self.label_text:
            self._label = MathTex(
                self.label_text,
                color=self.style.wire_label_color,
            )
            self._label.scale(self.style.wire_label_scale)
            self._label.next_to(
                [self.x_start, self.y, 0],
                LEFT,
                buff=self.style.wire_label_buff,
            )
            self.add(self._label)

    def mask_region(self, center_x: float, half_width: float) -> None:
        """
        Mark a region to be masked (where a gate will be drawn).

        Args:
            center_x: Center x-coordinate of the mask.
            half_width: Half-width of the mask region.
        """
        self._masked_regions.append((center_x, half_width))

    def rebuild_segments(self) -> None:
        """
        Rebuild wire segments based on masked regions.

        This should be called after all gates have been added to properly
        show wire breaks at gate positions.
        """
        # Remove old segments
        for seg in self._segments:
            self.remove(seg)
        self._segments.clear()

        if not self._masked_regions:
            # No masks, single line
            line = Line(
                start=[self.x_start, self.y, 0],
                end=[self.x_end, self.y, 0],
                color=self.style.wire_color,
                stroke_width=self.style.wire_stroke_width,
            )
            self._segments.append(line)
            self.add(line)
            return

        # Sort masked regions by x position
        sorted_masks = sorted(self._masked_regions, key=lambda m: m[0])

        # Build segments between masks
        current_x = self.x_start
        for center_x, half_width in sorted_masks:
            mask_start = center_x - half_width
            mask_end = center_x + half_width

            # Segment before this mask
            if current_x < mask_start:
                line = Line(
                    start=[current_x, self.y, 0],
                    end=[mask_start, self.y, 0],
                    color=self.style.wire_color,
                    stroke_width=self.style.wire_stroke_width,
                )
                self._segments.append(line)
                self.add(line)

            current_x = mask_end

        # Final segment after last mask
        if current_x < self.x_end:
            line = Line(
                start=[current_x, self.y, 0],
                end=[self.x_end, self.y, 0],
                color=self.style.wire_color,
                stroke_width=self.style.wire_stroke_width,
            )
            self._segments.append(line)
            self.add(line)

    def highlight(self, color=None) -> None:
        """Highlight the wire with a different color."""
        color = color or self.style.highlight_color
        for seg in self._segments:
            seg.set_color(color)

    def reset_highlight(self) -> None:
        """Reset wire color to default."""
        for seg in self._segments:
            seg.set_color(self.style.wire_color)

    def get_point_at_x(self, x: float) -> np.ndarray:
        """Get the 3D point on this wire at a given x-coordinate."""
        return np.array([x, self.y, 0])
