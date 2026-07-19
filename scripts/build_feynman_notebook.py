"""Build notebooks/feynman_lost_lecture.ipynb (elementary + formal proofs)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "feynman_lost_lecture.ipynb"


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


cells = [
    md(
        """# Feynman’s Lost Lecture — The Motion of Planets Around the Sun

> I am going to give what I will call an elementary demonstration. But elementary does not mean easy to understand. Elementary means that very little is required to know ahead of time in order to understand it, except to have an infinite amount of intelligence. There may be a large number of steps that hard to follow, but to each does not require already knowing the calculus or Fourier transforms. Yeah, that’s all, infinite intelligence. I think you’re up to that, don’t you?
>
> — **Richard Feynman**, 1964

**Goal.** From Newton’s inverse-square law and Kepler’s second law (equal areas), prove that a bound orbit is an **ellipse** with the Sun at a focus.

This notebook has two parts:

- **Part A — Elementary demonstration** (hodograph geometry, eccentric point, 90° construction)
- **Part B — Formal demonstration** (vector hodograph, Runge–Lenz, optional Binet)

Docs: `docs/celestial/feynman_elementary.md`, `docs/celestial/feynman_formal.md`, `docs/bibliography.md`.  
Video: https://youtu.be/xdIjYBtnvZU  
Lab module: `src/orbit_feynman.py`
"""
    ),
    md("## Setup"),
    code(
        """\
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path.cwd()
if not (ROOT / "src").exists():
    ROOT = Path.cwd().parent
sys.path.insert(0, str(ROOT))

from src.orbit_feynman import (
    construction_at_theta,
    fit_circle_2d,
    hodograph_circle,
    orbit_diagnostics,
    sample_orbit,
    second_focus,
)

# Canonical demo orbit
A, E, MU = 1.0, 0.5, 1.0
data = sample_orbit(a=A, e=E, mu=MU, n=400)
circ = hodograph_circle(a=A, e=E, mu=MU)
print("h theory:", orbit_diagnostics(A, E, MU)["h_theory"])
print("hodograph center, radius:", circ)
"""
    ),
    md(
        """## Part A — Elementary demonstration

### A.1 Equal areas and a central force

Kepler’s second law (equal areas in equal times) is equivalent to a force always directed toward the Sun. Then $\\Delta\\mathbf{v}$ is radial. Combined with $|\\mathbf{a}|\\propto 1/r^{2}$, equal orbital angles produce **equal** $|\\Delta\\mathbf{v}|$ — so the velocity tips form a circle (Goodstein & Goodstein; Maxwell).
"""
    ),
    code(
        """\
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# Position space
ax = axes[0]
ax.plot(np.append(data["x"], data["x"][0]), np.append(data["y"], data["y"][0]),
        color="#5F6B45", lw=2, label="orbit")
ax.scatter([0], [0], c="#9A7340", s=80, marker="*", zorder=5, label="Sun $F_1$")
f2x, f2y = second_focus(A, E)
ax.scatter([f2x], [f2y], c="#5C574E", s=50, marker="x", label="$F_2$")
th = np.deg2rad(50)
snap = construction_at_theta(th, a=A, e=E, mu=MU)
ax.scatter([snap.rx], [snap.ry], c="#1A1814", s=40, label="planet")
ax.plot([0, snap.rx], [0, snap.ry], ls=":", color="#5C574E", lw=1)
ax.set_aspect("equal")
ax.set_title("Position space")
ax.legend(loc="upper right", fontsize=8)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Velocity space
ax = axes[1]
ax.plot(np.append(data["vx"], data["vx"][0]), np.append(data["vy"], data["vy"][0]),
        color="#5F6B45", lw=2, label="hodograph")
phi = np.linspace(0, 2 * np.pi, 200)
ax.plot(
    circ.center_vx + circ.radius * np.cos(phi),
    circ.center_vy + circ.radius * np.sin(phi),
    ls="--", color="#9A7340", label="velocity circle",
)
ax.scatter([0], [0], c="#1A1814", s=40, label="O")
ax.scatter([circ.center_vx], [circ.center_vy], c="#9A7340", s=50, marker="D", label="eccentric C")
ax.plot([0, snap.px], [0, snap.py], color="#5C574E", lw=1.5)
ax.scatter([snap.px], [snap.py], c="#1A1814", s=30)
ax.set_aspect("equal")
ax.set_title("Velocity space (hodograph)")
ax.legend(loc="upper right", fontsize=8)
ax.set_xlabel(r"$v_x$")
ax.set_ylabel(r"$v_y$")

fig.suptitle("Elementary picture: orbit ↔ circular hodograph", y=1.02)
plt.tight_layout()
plt.show()

print(f"|PF1|+|PF2| = {snap.focus_sum:.6f}  (2a = {2*A:.6f})")
"""
    ),
    md(
        """### A.2 Eccentric point and 90° construction

The velocity origin $O$ is offset from the circle center $C$. Rotating $Op$ by $90^{\\circ}$ and using the perpendicular-bisector construction recovers points on the ellipse (Feynman / Maxwell / Hall–Higson). Below: several frames of the construction overlay.
"""
    ),
    code(
        """\
thetas = np.linspace(0, 2 * np.pi, 8, endpoint=False)
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(np.append(data["x"], data["x"][0]), np.append(data["y"], data["y"][0]),
        color="#5F6B45", lw=2)
ax.scatter([0], [0], c="#9A7340", s=80, marker="*")
ax.scatter([f2x], [f2y], c="#5C574E", s=50, marker="x")

for th in thetas:
    s = construction_at_theta(float(th), a=A, e=E, mu=MU)
    ax.scatter([s.rx], [s.ry], c="#1A1814", s=25)
    ax.scatter([s.construct_x], [s.construct_y], c="#8A9470", s=20, marker="D", alpha=0.8)

ax.set_aspect("equal")
ax.set_title("Construction points track the elliptical orbit")
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.show()
"""
    ),
    md(
        """### A.3 Elementary conclusion

The set of constructed points satisfies $|PF_1|+|PF_2|=2a$. By definition that locus is an **ellipse** with foci $F_1$ (Sun) and $F_2$. Therefore the planet’s orbit is an ellipse.
"""
    ),
    md(
        """## Part B — Formal demonstration

### B.1 Circular hodograph from $d\\mathbf{v}/d\\theta$

$$
\\frac{d\\mathbf{v}}{d\\theta} = -\\frac{\\mu}{h}\\hat{\\mathbf{r}}.
$$

Only for $a\\propto 1/r^{2}$ does the $r^{2}$ in $dt/d\\theta$ cancel to leave a constant-magnitude turn — a circle in velocity space.
"""
    ),
    code(
        """\
cx, cy, rad, rms = fit_circle_2d(data["vx"], data["vy"])
print(f"Fitted circle: center=({cx:.6f}, {cy:.6f}), R={rad:.6f}, RMS={rms:.3e}")
print(f"Theory:        center=(0, {circ.center_vy:.6f}), R={circ.radius:.6f}")
print(f"ang_mom CV = {np.std(data['h']) / np.mean(data['h']):.3e}")
print(f"focus-sum error mean = {np.mean(np.abs(data['focus_sum'] - 2*A)):.3e}")
"""
    ),
    md(
        """### B.2 Runge–Lenz vector ⇒ focused conic

$$
\\mathbf{A} = \\mathbf{v}\\times\\mathbf{h} - \\mu\\,\\hat{\\mathbf{r}},
\\qquad \\dot{\\mathbf{A}}=\\mathbf{0}
\\quad\\Rightarrow\\quad
r = \\frac{h^{2}/\\mu}{1+e\\cos\\theta}.
$$

Bound orbits ($e<1$) are ellipses. Hyperbolas ($e>1$) are the Rutherford case Feynman connected to the same geometry.
"""
    ),
    code(
        """\
# Numeric Runge–Lenz check: A should be ~constant along the orbit
x, y, vx, vy = data["x"], data["y"], data["vx"], data["vy"]
r = np.hypot(x, y)
hx = x * vy - y * vx  # h_z
# A = v × h - mu r_hat  (planar: h = h z-hat)
# v × h = (vx, vy, 0) × (0,0,h) = (vy*h, -vx*h, 0)
Ax = vy * hx - MU * (x / r)
Ay = -vx * hx - MU * (y / r)
A_mag = np.hypot(Ax, Ay)
print(f"|A| mean={A_mag.mean():.6f}, std={A_mag.std():.3e}")
print(f"e from |A|/mu = {A_mag.mean()/MU:.6f}  (input e={E})")
print(f"A direction ~ ({Ax.mean():.4f}, {Ay.mean():.4f})  (periapsis on +x ⇒ A along +x)")
"""
    ),
    md(
        """### B.3 Optional Binet sketch

With $u=1/r$,
$$
\\frac{d^{2}u}{d\\theta^{2}}+u=\\frac{\\mu}{h^{2}},
$$
solved by $u=(\\mu/h^{2})(1+e\\cos\\theta)$ — the same focused conic.
"""
    ),
    code(
        """\
diag = orbit_diagnostics(A, E, MU)
for k, v in diag.items():
    print(f"{k:24s} {v}")
"""
    ),
    md(
        """## Pointers

| Resource | Path |
|----------|------|
| Elementary write-up | `docs/celestial/feynman_elementary.md` |
| Formal write-up | `docs/celestial/feynman_formal.md` |
| Bibliography | `docs/bibliography.md` |
| Streamlit lab | sidebar → `planetary_motion` |
| Implementation | `src/orbit_feynman.py` |

**Sources.** Goodstein & Goodstein, *Feynman’s Lost Lecture*; Maxwell, *Matter and Motion*; Newton, *Principia*; Hall & Higson notes; Cariñena–Rañada–Santander (2016).
"""
    ),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    },
    "cells": cells,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"Wrote {OUT}")
