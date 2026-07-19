# Gray–Scott reaction–diffusion

## What

Gray–Scott kinetics (Gray & Scott, 1984) for species $A,B$:

$$
\partial_t A = D_A\nabla^{2}A - AB^{2} + f(1-A),
\quad
\partial_t B = D_B\nabla^{2}B + AB^{2} - (f+k)B.
$$

The Well ensemble samples **feed** $f$ and **kill** $k$ across named regimes (Gliders, Bubbles, Maze, Worms, Spirals, Spots). Extracted metrics include pattern contrast ($\mathrm{std}\,A+\mathrm{std}\,B$), mean concentrations, and related scalars.

## Why phase diagrams instead of ANOVA

Regimes are **qualitative attractors** in $(f,k)$ space (Turing-like morphogenesis lineage; Turing, 1952). The scientific display is a **phase diagram** and metric-vs-parameter curves, not a claim that $f$ and $k$ are balanced experimental factors for $F$-tests. Using ANOVA here would mis-state the question.

## Why the physics checks

- Species means in $[0,1]$ — bounded concentrations.  
- Contrast–feed association — sanity that pattern strength covaries with $f$ on the synthetic/real grid.

## Code

- `src/dataset_catalog.py` — `GRAY_SCOTT`  
- `app/streamlit_app.py` — `tab_phase_diagram`, `tab_pattern_metrics`  
- `notebooks/gray_scott_analysis.ipynb`

## Sources

Gray & Scott (1984); Turing (1952); The Well `gray_scott_reaction_diffusion` card. See [bibliography.md](../bibliography.md).
