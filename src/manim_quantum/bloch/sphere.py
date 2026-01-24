"""Bloch sphere visualization for single-qubit states."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import (
    ORIGIN,
    PI,
    Arrow3D,
    Dot3D,
    Line3D,
    MathTex,
    Surface,
    ThreeDScene,
    VGroup,
)

from manim_quantum.styles import QuantumStyle

if TYPE_CHECKING:
    from manim import Scene


class BlochSphere(VGroup):
    """
    3D Bloch sphere visualization for single-qubit states.

    The Bloch sphere represents a qubit state as a point on the unit sphere,
    where the poles correspond to |0⟩ and |1⟩, and superposition states
    lie on the surface.

    Args:
        radius: Sphere radius.
        show_axes: Whether to show the X, Y, Z axes.
        show_labels: Whether to show axis labels.
        show_state_vector: Whether to show the state arrow.
        initial_state: Initial state as (theta, phi) in radians.
        style: Visual style configuration.

    Note:
        This component requires a ThreeDScene to render properly.
        Use self.set_camera_orientation() in your scene to get a good view.
        Call bloch.add_labels_to_scene(self) to make labels face the camera.

    Example:
        >>> class MyScene(ThreeDScene):
        ...     def construct(self):
        ...         bloch = BlochSphere()
        ...         bloch.add_labels_to_scene(self)
        ...         self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
        ...         self.add(bloch)
    """

    def __init__(
            self,
            radius: float = 2.0,
            show_axes: bool = True,
            show_labels: bool = True,
            show_state_vector: bool = True,
            initial_state: tuple[float, float] | None = None,
            style: QuantumStyle | None = None,
    ) -> None:
        super().__init__()

        self.radius = radius
        self.show_axes = show_axes
        self.show_labels = show_labels
        self.show_state_vector = show_state_vector
        self.style = style or QuantumStyle()

        # Current state in spherical coordinates (theta, phi)
        # theta: angle from +z axis (0 = |0⟩, pi = |1⟩)
        # phi: angle in xy-plane from +x axis
        self._theta = 0.0
        self._phi = 0.0

        # Store labels separately for camera-facing behavior
        self._label_mobjects: list[MathTex] = []

        self._build()

        if initial_state is not None:
            self.set_state(*initial_state)

    def _build(self) -> None:
        """Build the Bloch sphere visualization."""
        # Sphere surface
        self.sphere = self._create_sphere()
        self.add(self.sphere)

        # Axes
        if self.show_axes:
            self.axes = self._create_axes()
            self.add(self.axes)

        # Labels
        if self.show_labels:
            self.labels = self._create_labels()
            self.add(self.labels)

        # State vector
        if self.show_state_vector:
            self.state_arrow = self._create_state_arrow()
            self.state_dot = self._create_state_dot()
            self.add(self.state_arrow, self.state_dot)

    def _create_sphere(self) -> Surface:
        """Create the sphere surface."""
        sphere = Surface(
            lambda u, v: np.array([
                self.radius * np.sin(v) * np.cos(u),
                self.radius * np.sin(v) * np.sin(u),
                self.radius * np.cos(v),
            ]),
            u_range=[0, 2 * PI],
            v_range=[0, PI],
            resolution=(32, 16),
        )
        sphere.set_fill(self.style.sphere_color, opacity=self.style.sphere_opacity)
        sphere.set_stroke(self.style.sphere_color, width=0.5, opacity=0.3)
        return sphere

    def _create_axes(self) -> VGroup:
        """Create the coordinate axes."""
        axes = VGroup()
        r = self.radius * 1.3

        # X axis (red)
        x_axis = Line3D(
            start=[-r, 0, 0],
            end=[r, 0, 0],
            color=self.style.axis_color,
        )
        axes.add(x_axis)

        # Y axis (green)
        y_axis = Line3D(
            start=[0, -r, 0],
            end=[0, r, 0],
            color=self.style.axis_color,
        )
        axes.add(y_axis)

        # Z axis (blue)
        z_axis = Line3D(
            start=[0, 0, -r],
            end=[0, 0, r],
            color=self.style.axis_color,
        )
        axes.add(z_axis)

        return axes

    def _create_labels(self) -> VGroup:
        """Create axis labels."""
        labels = VGroup()
        r = self.radius * 1.5

        # Basis state labels
        label_0 = MathTex("|0\\rangle", color=self.style.ket_color)
        label_0.move_to([0, 0, r])
        labels.add(label_0)
        self._label_mobjects.append(label_0)

        label_1 = MathTex("|1\\rangle", color=self.style.ket_color)
        label_1.move_to([0, 0, -r])
        labels.add(label_1)
        self._label_mobjects.append(label_1)

        # Axis labels
        x_label = MathTex("X", color=self.style.axis_color)
        x_label.move_to([r, 0, 0])
        labels.add(x_label)
        self._label_mobjects.append(x_label)

        y_label = MathTex("Y", color=self.style.axis_color)
        y_label.move_to([0, r, 0])
        labels.add(y_label)
        self._label_mobjects.append(y_label)

        return labels

    def add_labels_to_scene(self, scene: "Scene") -> None:
        """
        Register labels with a ThreeDScene to make them always face the camera.

        This method should be called after creating the BlochSphere to ensure
        that axis labels (|0⟩, |1⟩, X, Y) always face the camera regardless
        of camera rotation.

        Args:
            scene: The ThreeDScene instance to register labels with.

        Example:
            >>> class MyScene(ThreeDScene):
            ...     def construct(self):
            ...         bloch = BlochSphere()
            ...         bloch.add_labels_to_scene(self)
            ...         self.add(bloch)
        """
        if hasattr(scene, 'add_fixed_orientation_mobjects'):
            scene.add_fixed_orientation_mobjects(*self._label_mobjects)

    def _create_state_arrow(self) -> Arrow3D:
        """Create the state vector arrow."""
        point = self._get_cartesian()
        arrow = Arrow3D(
            start=ORIGIN,
            end=point,
            color=self.style.state_vector_color,
        )
        return arrow

    def _create_state_dot(self) -> Dot3D:
        """Create the state point on the sphere surface."""
        point = self._get_cartesian()
        dot = Dot3D(
            point=point,
            radius=0.08,
            color=self.style.state_dot_color,
        )
        return dot

    def _get_cartesian(self) -> np.ndarray:
        """Get cartesian coordinates of current state."""
        x = self.radius * np.sin(self._theta) * np.cos(self._phi)
        y = self.radius * np.sin(self._theta) * np.sin(self._phi)
        z = self.radius * np.cos(self._theta)
        return np.array([x, y, z])

    def set_state(self, theta: float, phi: float) -> None:
        """
        Set the qubit state using Bloch sphere angles.

        Args:
            theta: Polar angle from +z (0 to π).
            phi: Azimuthal angle in xy-plane (0 to 2π).
        """
        self._theta = float(theta)
        self._phi = float(phi)

        if self.show_state_vector:
            point = self._get_cartesian()

            # Update arrow
            self.remove(self.state_arrow)
            self.state_arrow = Arrow3D(
                start=ORIGIN,
                end=point,
                color=self.style.state_vector_color,
            )
            self.add(self.state_arrow)

            # Update dot
            self.state_dot.move_to(point)

    def set_state_from_amplitudes(self, alpha: complex, beta: complex) -> None:
        """
        Set the state from qubit amplitudes |ψ⟩ = α|0⟩ + β|1⟩.

        Args:
            alpha: Amplitude for |0⟩.
            beta: Amplitude for |1⟩.
        """
        # Normalize
        norm = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
        if norm < 1e-10:
            self.set_state(0, 0)
            return

        alpha = alpha / norm
        beta = beta / norm

        # Convert to Bloch angles
        # |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
        theta = 2 * np.arccos(min(1.0, abs(alpha)))

        if abs(beta) < 1e-10:
            phi = 0.0
        else:
            # Extract relative phase
            if abs(alpha) < 1e-10:
                phi = np.angle(beta)
            else:
                phi = np.angle(beta) - np.angle(alpha)

        self.set_state(theta, phi)

    def get_state_amplitudes(self) -> tuple[complex, complex]:
        """
        Get the qubit amplitudes for the current state.

        Returns:
            Tuple (alpha, beta) where |ψ⟩ = α|0⟩ + β|1⟩.
        """
        alpha = np.cos(self._theta / 2)
        beta = np.exp(1j * self._phi) * np.sin(self._theta / 2)
        return complex(alpha), complex(beta)

    @classmethod
    def basis_state(
            cls,
            state: str | int,
            **kwargs,
    ) -> BlochSphere:
        """
        Create a Bloch sphere showing a basis state.

        Args:
            state: "0" or "1" (or 0, 1).
            **kwargs: Additional arguments for BlochSphere.

        Returns:
            BlochSphere at the specified basis state.
        """
        state = str(state)
        theta = 0 if state == "0" else PI
        return cls(initial_state=(theta, 0), **kwargs)

    @classmethod
    def plus_state(cls, **kwargs) -> BlochSphere:
        """Create a Bloch sphere showing |+⟩ state (on +X axis)."""
        return cls(initial_state=(PI / 2, 0), **kwargs)

    @classmethod
    def minus_state(cls, **kwargs) -> BlochSphere:
        """Create a Bloch sphere showing |-⟩ state (on -X axis)."""
        return cls(initial_state=(PI / 2, PI), **kwargs)

    @classmethod
    def plus_i_state(cls, **kwargs) -> BlochSphere:
        """Create a Bloch sphere showing |+i⟩ state (on +Y axis)."""
        return cls(initial_state=(PI / 2, PI / 2), **kwargs)

    @classmethod
    def minus_i_state(cls, **kwargs) -> BlochSphere:
        """Create a Bloch sphere showing |-i⟩ state (on -Y axis)."""
        return cls(initial_state=(PI / 2, 3 * PI / 2), **kwargs)
