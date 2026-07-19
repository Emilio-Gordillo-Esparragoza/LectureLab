# Effect sizes: $\eta^{2}$, $\omega^{2}$, partial $\eta^{2}$

## What

A significant $p$-value does not say **how large** a factor’s imprint is. Effect sizes rescale sums of squares:

$$
\eta^{2} = \frac{\mathrm{SS}_{\mathrm{effect}}}{\mathrm{SS}_{\mathrm{Total}}},
\qquad
\omega^{2} = \frac{\mathrm{SS}_{\mathrm{effect}} - \mathrm{df}_{\mathrm{effect}}\,\mathrm{MS}_{\mathrm{error}}}{\mathrm{SS}_{\mathrm{Total}} + \mathrm{MS}_{\mathrm{error}}}.
$$

In multifactor ANOVA, **partial** $\eta^{2}$ uses

$$
\eta^{2}_{p} = \frac{\mathrm{SS}_{\mathrm{effect}}}{\mathrm{SS}_{\mathrm{effect}} + \mathrm{SS}_{\mathrm{error}}}
$$

so each term is judged relative to residual error rather than the whole total (Olejljnik & Algina, 2003).

## Why it is used here

In `active_matter`, $\zeta$ can show enormous $F$ with $\eta^{2}\approx 0.9$ while $\alpha$ is weak alone but participates in a sizable $\alpha\times\zeta$ interaction. Reporting $\eta^{2}$ / partial $\eta^{2}$ / $\omega^{2}$ prevents mistaking “$p$ tiny” for “every factor matters equally” (Cohen, 1988).

The teaching sandbox surfaces $\eta^{2}$ and $\omega^{2}$ next to $F$ and $p$ so learners see significance and magnitude together.

## Assumptions / caveats

- $\eta^{2}$ is positively biased in small samples; $\omega^{2}$ partially corrects that.  
- Partial $\eta^{2}$ values for different terms are **not** additive to 1.  
- Effect-size cutoffs (e.g. 0.01 / 0.06 / 0.14) are conventional heuristics, not laws of physics.

## Code

- `src/stats.py` — `eta_squared`, `omega_squared`, verdict helpers  
- Real-data two-way table in `tab_realdata`

## Sources

Cohen (1988); Olejljnik & Algina (2003). See [bibliography.md](../bibliography.md).
