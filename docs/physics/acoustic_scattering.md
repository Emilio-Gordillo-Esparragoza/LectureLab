# Acoustic scattering (maze)

## What

The Well `acoustic_scattering_maze` ensemble propagates pressure waves through maze-like density fields. Circumstance factors:

- `maze_width` — geometry / wall layout scale  
- `n_sources` — number of acoustic sources  

Responses include pressure energy, mean absolute pressure, wall fraction, and a **spectral slope** proxy for frequency content of the scattered field.

## Why interaction / response surfaces

Geometry and source count are expected to **jointly** shape energy. The lab emphasizes multiparameter response surfaces and interaction-style plots rather than factorial ANOVA, matching an exploratory simulation ensemble (Pierce, *Acoustics*, for energy/spectral motivation).

## Why the physics checks

- Finite pressure energy — no NaN/Inf extraction failures.  
- Wall fraction in $(0,1)$ — maze masks are nontrivial.  
- Energy vs `n_sources` (Spearman) — more sources should tend to raise energy on the grid.

## Code

- `src/dataset_catalog.py` — `ACOUSTIC`  
- `app/streamlit_app.py` — `tab_geometry_sources`, `tab_response_interactions`  
- `notebooks/acoustic_scattering_analysis.ipynb`

## Sources

The Well dataset card; Pierce, *Acoustics*. See [bibliography.md](../bibliography.md).
