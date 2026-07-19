# Active matter — feature mathematics

## What

The Well `active_matter` ensemble is a continuum model of rod-like active particles in a Stokes fluid. From each trajectory we extract scalars:

| Feature | Meaning |
|---------|---------|
| Nematic order $S$ | Magnitude of the orientation tensor $\mathbf{D}$ (Frobenius / eigenvalue summary) |
| Kinetic energy | $\tfrac12\langle\|\mathbf{u}\|^{2}\rangle$ |
| Enstrophy | $\tfrac12\langle\omega^{2}\rangle$ from vorticity |
| `div_u_rms` | Discrete divergence residual (near-incompressibility proxy) |
| Spectral slope | Log–log slope of $E(k)$ as a rough cascade / structure proxy |
| Concentration stats | Mean / std of the concentration field |
| `time_to_steady` | Time to a plateau criterion |

Factors: dipole $\alpha$, alignment $\zeta$.

## Why each check exists

- **Concentration conservation** — periodic BCs and $c\equiv 1$ initialization imply mean concentration $\approx 1$; flags extraction bugs.  
- **Spearman$(S,\zeta)$** — physics expects an isotropic→nematic-like rise with alignment (de Gennes & Prost).  
- **`div_u_rms`** — Stokes solvers are nearly incompressible; elevated residuals usually signal **analysis downsampling**, not a broken simulation (documented caveat).  
- **Anomaly MAD screens** — unusual RNG seeds / extract noise inside an $(\alpha,\zeta)$ cell, not automatic claims that continuum theory failed.

## Why ANOVA (not only plots)

$\alpha$ and $\zeta$ are experimentally controlled circumstances. Factorial ANOVA quantifies how much of $S$ they explain and whether they interact — the scientific question of the lab.

## Code

- `src/extract_features.py` — feature builders  
- `src/dataset_catalog.py` — `ACTIVE_MATTER.physics_checks`  
- `src/stats.py` — `physics_validation`

## Sources

The Well dataset card; de Gennes & Prost (1993); Landau & Lifshitz (*Fluid Mechanics*). See [bibliography.md](../bibliography.md).
