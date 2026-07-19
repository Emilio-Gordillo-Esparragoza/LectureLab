# One- and two-way ANOVA

## What

**Analysis of variance (ANOVA)** partitions the total sum of squares of a response $Y$ into pieces attributable to controlled factors and residual error. For a one-way design with factor $A$,

$$
\mathrm{SS}_{\mathrm{Total}} = \mathrm{SS}_{\mathrm{Between}} + \mathrm{SS}_{\mathrm{Within}},
\quad
F = \frac{\mathrm{MSB}}{\mathrm{MSW}} = \frac{\mathrm{SSB}/\mathrm{df}_{B}}{\mathrm{SSW}/\mathrm{df}_{W}}.
$$

Under the classical null (equal group means, i.i.d. Gaussian errors, equal variances), $F$ follows an $F(\mathrm{df}_{B},\mathrm{df}_{W})$ distribution (Fisher, 1925; Scheffé, 1959).

For two-way factorial designs the model is

$$
Y \sim C(A) * C(B)
$$

with main effects of $A$, $B$, and the interaction $A\times B$.

## Why it is used here

In the **`active_matter`** lab, each trajectory is labeled by initial controls $\alpha$ (dipole) and $\zeta$ (alignment). ANOVA answers: *how much of the variation in nematic order $S$ (or KE, enstrophy, …) is explained by those circumstances?* The teaching sandbox in the Streamlit app lets users feel SSB vs SSW before trusting real-data $F$ and $p$.

Gray–Scott and acoustic labs **do not** use ANOVA: their grids are exploratory phase / response surfaces, not balanced inference targets.

## Assumptions (checked in-app / notebooks)

- Independent trajectories within cells  
- Approximately equal variances (Levene)  
- Approximately normal residuals (Shapiro)  
- For two-way: interpret interaction before main effects when $A\times B$ is large  

## Code

- `src/stats.py` — `one_way_anova`, teaching sandbox helpers, two-way via `statsmodels`  
- UI: `tab_teaching`, `tab_realdata` in `app/streamlit_app.py`

## Sources

Fisher (1925); Scheffé (1959). See [bibliography.md](../bibliography.md).
