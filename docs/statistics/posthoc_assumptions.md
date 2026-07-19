# Post-hoc tests and assumption screens

## What

After a significant omnibus ANOVA, **which** levels differ?

| Tool | Role |
|------|------|
| **Tukey HSD** | All pairwise mean contrasts controlling family-wise error under equal variance (Tukey, 1949) |
| **Welch $t$ + Holm** | Unequal-variance pairwise tests with sequential FWER control (Welch, 1947; Holm, 1979) |
| **Levene** | Test homogeneity of variances before trusting classical ANOVA / Tukey (Levene, 1960) |
| **Shapiro–Wilk** | Normality of residuals (Shapiro & Wilk, 1965) |

## Why it is used here

The `active_matter` real-data panel is not only “is there a $\zeta$ effect?” but “which alignment levels separate?” Tukey (or Welch+Holm when variances misbehave) answers that without exploding false positives across the $\zeta$ grid.

Levene / Shapiro are **gates**: they document when the textbook $F$ story is strained (e.g. coarse spatial downsampling inflating residuals). They do not auto-rewrite the physics; they qualify the statistical claim.

## Assumptions

- Tukey: equal variances, balanced or nearly balanced cells, Gaussian errors  
- Welch: relaxes equal variance; still needs approximate normality for small $n$  
- Holm: controls FWER under arbitrary dependence of $p$-values in the sequential sense  

## Code

- `src/stats.py` — pairwise / assumption helpers consumed by notebooks and `tab_realdata`  
- Notebooks: `notebooks/analysis.ipynb`

## Sources

Tukey (1949); Welch (1947); Holm (1979); Levene (1960); Shapiro & Wilk (1965). See [bibliography.md](../bibliography.md).
