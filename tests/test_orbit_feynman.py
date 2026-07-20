"""Unit tests for Kepler / Feynman hodograph geometry."""

from __future__ import annotations

import numpy as np
import pytest

from src.orbit_feynman import (
    construction_at_theta,
    equal_angle_triangles,
    equal_area_triangles,
    hodograph_circle,
    radius_polar,
    sample_orbit,
    specific_angular_momentum,
    velocities,
)


def test_periapsis_radius() -> None:
    a, e = 1.0, 0.5
    r_peri = radius_polar(0.0, a, e)
    assert r_peri == pytest.approx(a * (1 - e))


def test_focus_sum_is_2a() -> None:
    a, e = 1.25, 0.4
    for theta in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        snap = construction_at_theta(theta, a=a, e=e, mu=1.0)
        assert snap.focus_sum == pytest.approx(2 * a, rel=1e-5, abs=1e-5)


def test_angular_momentum_constant() -> None:
    a, e, mu = 1.0, 0.35, 1.0
    h_ref = specific_angular_momentum(a, e, mu)
    theta = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    rx = radius_polar(theta, a, e) * np.cos(theta)
    ry = radius_polar(theta, a, e) * np.sin(theta)
    vx, vy = velocities(theta, a, e, mu)
    h = rx * vy - ry * vx
    assert h == pytest.approx(h_ref, rel=1e-9, abs=1e-9)


def test_hodograph_points_lie_on_circle() -> None:
    a, e, mu = 1.0, 0.5, 1.0
    circ = hodograph_circle(a, e, mu)
    theta = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    vx, vy = velocities(theta, a, e, mu)
    dist = np.hypot(vx - circ.center_vx, vy - circ.center_vy)
    assert dist == pytest.approx(circ.radius, rel=1e-9, abs=1e-9)


def test_equal_area_triangles_share_sector_area() -> None:
    tris = equal_area_triangles(a=1.0, e=0.45, mu=1.0, n_sectors=8)
    areas = np.array([t.sector_area for t in tris])
    assert areas.std() / areas.mean() < 1e-6


def test_equal_angle_dv_nearly_constant() -> None:
    tris = equal_angle_triangles(a=1.0, e=0.45, mu=1.0, n_sectors=8)
    dvs = np.array([t.dv_mag for t in tris])
    # Inverse-square + equal Δθ ⇒ nearly flat |Δv|
    assert dvs.std() / dvs.mean() < 0.05


def test_sample_orbit_shapes() -> None:
    data = sample_orbit(a=1.0, e=0.3, mu=1.0, n=120)
    assert len(data["theta"]) == 120
    assert data["x"].shape == (120,)
    assert data["vx"].shape == (120,)
