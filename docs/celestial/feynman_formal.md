# Formal demonstration (hodograph + Runge–Lenz)

**Companion code:** `src/orbit_feynman.py` · **UI:** `planetary_motion` → *Formal demonstration* · **Notebook:** `notebooks/feynman_lost_lecture.ipynb` (Part B)

This page is the **calculus / vector** companion to the [elementary geometric proof](feynman_elementary.md). Both prove the same theorem; this route makes conservation laws explicit.

## 1. Newton’s law and angular momentum

$$
\mathbf{F} = -\frac{\mu m}{r^{2}}\hat{\mathbf{r}},\quad \mu=GM.
$$

Torque $\mathbf{r}\times\mathbf{F}=\mathbf{0}$ ⇒ specific angular momentum $\mathbf{h}=\mathbf{r}\times\mathbf{v}$ is constant. Equivalently, areal velocity $\tfrac12 h$ is constant (Kepler II).

**Why:** without conserved $h$, equal-angle slices would not correspond to the equal $|\Delta v|$ argument, and the Binet / Runge–Lenz reductions below would not close.

## 2. Hodograph from $d\mathbf{v}/d\theta$

$$
\frac{d\mathbf{v}}{d\theta}
= \mathbf{a}\,\frac{dt}{d\theta}
= \Bigl(-\frac{\mu}{r^{2}}\hat{\mathbf{r}}\Bigr)\frac{r^{2}}{h}
= -\frac{\mu}{h}\hat{\mathbf{r}}.
$$

Integrating shows that $\mathbf{v}(\theta)$ traces a **circle** of radius $\mu/h$ whose center is displaced from the velocity origin by a vector of length $e\mu/h$ (eccentricity). This is the analytic content of Feynman’s / Maxwell’s circular hodograph.

**Why inverse-square is special:** only $a\propto 1/r^{2}$ cancels the $r^{2}$ in $dt/d\theta$ to give a $\theta$-derivative of constant magnitude along $-\hat{\mathbf{r}}$.

## 3. Laplace–Runge–Lenz vector

Define

$$
\mathbf{A} = \mathbf{v}\times\mathbf{h} - \mu\,\hat{\mathbf{r}}.
$$

For the inverse-square force, $\dot{\mathbf{A}}=\mathbf{0}$. Dot with $\mathbf{r}$:

$$
\mathbf{A}\cdot\mathbf{r} = h^{2} - \mu r
\quad\Rightarrow\quad
r = \frac{h^{2}/\mu}{1+e\cos\theta},\quad e=\frac{|\mathbf{A}|}{\mu}.
$$

This is the polar equation of a **conic** with focus at the force center. The bound case $E<0$ ($e<1$) is an ellipse (Kepler I). The same conserved vector organizes hyperbolic Rutherford scattering ($e>1$), which Feynman linked to the same geometry.

**Why this tool:** Runge–Lenz is the modern, coordinate-clean proof that $1/r^{2}$ ⇒ conic focus orbits; it packages the eccentric displacement of the hodograph into a single conserved vector (Goldstein; Laplace–Runge–Lenz tradition).

## 4. Binet equation (optional ODE route)

With $u=1/r$ and conserved $h$,

$$
\frac{d^{2}u}{d\theta^{2}} + u = \frac{\mu}{h^{2}}.
$$

General solution: $u=(\mu/h^{2})\bigl(1+e\cos(\theta-\theta_0)\bigr)$ — again a focused conic.

**Why include it:** connects the geometric story to the standard undergraduate ODE treatment without replacing the elementary lecture.

## 5. Numeric diagnostics (this repo)

For each synthetic $(e,h)$ cell, `orbit_diagnostics` checks:

| Diagnostic | Claim |
|------------|--------|
| `hodograph_circle_rms` | Velocity tips fit a circle |
| `ang_mom_cv` | $h$ constant along the orbit |
| `focus_sum_error` | $\bigl||PF_1|+|PF_2|-2a\bigr|\approx 0$ |

## Relation to the elementary proof

| Elementary | Formal |
|------------|--------|
| Equal $\|\Delta v\|$ in equal angles | $d\mathbf{v}/d\theta=-\mu\hat{\mathbf{r}}/h$ |
| Eccentric point $C$ vs origin $O$ | Displacement $\|\mathbf{A}\|/\mu=e$ |
| Gardener’s definition $\|PF_1\|+\|PF_2\|=2a$ | Polar conic with $e<1$ |

## Sources

Newton (*Principia*); Maxwell (*Matter and Motion*); Goodstein & Goodstein (1996); Cariñena–Rañada–Santander (2016); standard Runge–Lenz treatments. See [bibliography.md](../bibliography.md).
