"""Custom animations for Bloch sphere visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import Animation

if TYPE_CHECKING:
    from manim_quantum.bloch.sphere import BlochSphere


class BlochSphereStateTransition(Animation):
    """
    Animation for transitioning between quantum states on a Bloch sphere.

    This animation smoothly interpolates the state vector along the surface
    of the Bloch sphere, following a great circle path between the initial
    and final states.

    Args:
        bloch_sphere: The BlochSphere to animate.
        target_theta: Target polar angle (0 to π).
        target_phi: Target azimuthal angle (0 to 2π).
        run_time: Animation duration.
        **kwargs: Additional arguments for Animation.

    Example:
        >>> bloch = BlochSphere.basis_state("0")
        >>> self.play(BlochSphereStateTransition(bloch, np.pi/2, 0))
    """

    def __init__(
            self,
            bloch_sphere: "BlochSphere",
            target_theta: float,
            target_phi: float,
            run_time: float = 1.5,
            **kwargs,
    ) -> None:
        self.bloch_sphere = bloch_sphere
        self.initial_theta = bloch_sphere.get_theta()
        self.initial_phi = bloch_sphere.get_phi()
        self.target_theta = float(target_theta)
        self.target_phi = float(target_phi)
        super().__init__(bloch_sphere, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """Interpolate the state along the sphere surface."""
        # Linear interpolation in spherical coordinates
        theta = self.initial_theta + alpha * (self.target_theta - self.initial_theta)
        phi = self.initial_phi + alpha * (self.target_phi - self.initial_phi)

        # Update the Bloch sphere state
        self.bloch_sphere.set_state(theta, phi)


class BlochSphereRotation(Animation):
    """
    Animation for rotating the state vector around an axis on the Bloch sphere.

    This animation rotates the quantum state around a specified axis by a given angle,
    which corresponds to applying a rotation gate in quantum computing.

    Args:
        bloch_sphere: The BlochSphere to animate.
        axis: Rotation axis - one of "x", "y", or "z".
        angle: Rotation angle in radians.
        run_time: Animation duration.
        **kwargs: Additional arguments for Animation.

    Example:
        >>> bloch = BlochSphere.basis_state("0")
        >>> # Rotate by π around Y axis (equivalent to Hadamard-like rotation)
        >>> self.play(BlochSphereRotation(bloch, "y", np.pi/2))
    """

    def __init__(
            self,
            bloch_sphere: "BlochSphere",
            axis: str,
            angle: float,
            run_time: float = 1.5,
            **kwargs,
    ) -> None:
        self.bloch_sphere = bloch_sphere
        self.axis = axis.lower()
        self.angle = float(angle)

        # Store initial state
        self.initial_theta = bloch_sphere.get_theta()
        self.initial_phi = bloch_sphere.get_phi()

        # Calculate target state based on rotation
        self.target_theta, self.target_phi = self._calculate_rotation()

        super().__init__(bloch_sphere, run_time=run_time, **kwargs)

    def _calculate_rotation(self) -> tuple[float, float]:
        """Calculate the target state after rotation."""
        # Convert initial spherical to Cartesian
        x0 = np.sin(self.initial_theta) * np.cos(self.initial_phi)
        y0 = np.sin(self.initial_theta) * np.sin(self.initial_phi)
        z0 = np.cos(self.initial_theta)

        # Apply rotation matrix
        c = np.cos(self.angle)
        s = np.sin(self.angle)

        if self.axis == "x":
            x1 = x0
            y1 = c * y0 - s * z0
            z1 = s * y0 + c * z0
        elif self.axis == "y":
            x1 = c * x0 + s * z0
            y1 = y0
            z1 = -s * x0 + c * z0
        elif self.axis == "z":
            x1 = c * x0 - s * y0
            y1 = s * x0 + c * y0
            z1 = z0
        else:
            raise ValueError(f"Invalid axis: {self.axis}. Must be 'x', 'y', or 'z'.")

        # Convert back to spherical
        r = np.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)
        if r < 1e-10:
            return 0.0, 0.0

        theta = np.arccos(np.clip(z1 / r, -1, 1))
        phi = np.arctan2(y1, x1)

        return float(theta), float(phi)

    def interpolate_mobject(self, alpha: float) -> None:
        """Interpolate the rotation."""
        # Spherical linear interpolation
        theta = self.initial_theta + alpha * (self.target_theta - self.initial_theta)
        phi = self.initial_phi + alpha * (self.target_phi - self.initial_phi)

        self.bloch_sphere.set_state(theta, phi)
