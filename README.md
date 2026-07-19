# The Well · active_matter Statistical Lab

Statistical analysis and an interactive ANOVA dashboard for physics simulations from **[The Well](https://github.com/PolymathicAI/the_well)** (`active_matter` dataset).

**Live demo:** [https://physcientific.onrender.com/](https://physcientific.onrender.com/)  
*(Render free tier may cold-start for ~30–60s after idle.)*

Repository: [Emilio-Gordillo-Esparragoza/phyScientific](https://github.com/Emilio-Gordillo-Esparragoza/phyScientific)

## What this project does

1. **Extracts** scalar physics features from each trajectory (nematic order, kinetic energy, enstrophy, divergence residual, spectral slope, …) plus control factors `alpha` (dipole) and `zeta` (alignment).
2. **Quantifies** how much initial circumstances matter with **one- / two-way ANOVA**, effect sizes (η², ω²), Tukey HSD, and pairwise t-tests.
3. **Validates** approximate physics laws (concentration ≈ 1, ∇·u ≈ 0, isotropic→nematic transition vs `zeta`).
4. **Flags anomalies** within each `(alpha, zeta)` cell.
5. Ships an **interactive Streamlit app** with a teaching ANOVA sandbox (sliders for mean difference / within-group dispersion → live F, p, SSE, η² + evidence verdict).

## Findings

Results below are from the committed real feature table [`data/features.parquet`](data/features.parquet): **134** trajectories, **45/45** α×ζ factorial cells, `synthetic = 0`. Features were computed while streaming The Well train split from Hugging Face with `--time-stride 8 --space-stride 16` (analysis-ready table, not full-resolution fields).

### Experimental design

- **System:** continuum theory of rod-like active particles in a Stokes fluid (`active_matter`).
- **Factors (initial / control circumstances):** dipole strength `alpha ∈ {-1, -2, -3, -4, -5}` and alignment `zeta ∈ {1, 3, …, 17}` (`beta` fixed at 0.8 in the source ensemble).
- **Responses used for inference:** primarily nematic order `nematic_order_S` (orientation-tensor magnitude), plus kinetic energy, enstrophy, concentration statistics, discrete divergence RMS, spectral slope, and time-to-steady.

### How much do initial circumstances matter?

Two-way ANOVA `nematic_order_S ~ C(alpha) * C(zeta)`:

| Term | F | p | partial η² |
|------|--:|--:|----------:|
| `zeta` (alignment) | ≈ 325 | ≈ 2×10⁻⁶² | **≈ 0.97** |
| `alpha` (dipole) | ≈ 1.5 | ≈ 0.22 | ≈ 0.06 |
| `alpha × zeta` | ≈ 3.6 | ≈ 1×10⁻⁶ | ≈ 0.56 |

One-way ANOVA on `zeta` alone: F ≈ 195, η² ≈ **0.93** — strong evidence for differences across alignment levels.

**Takeaway:** In this ensemble, **alignment (`zeta`) is the primary knob** for the isotropic→nematic-like rise in order. **Dipole strength (`alpha`) does not clearly shift mean order on its own**; it matters mainly by **modulating how strongly `zeta` acts** (significant interaction). Changing “initial circumstances” is therefore not uniform across parameters: `zeta` carries almost all of the between-group structure for `S`.

Reproduce interactively in the app tab **Real-data ANOVA** (two-way) or in [`notebooks/analysis.ipynb`](notebooks/analysis.ipynb).

### Physics-law checks

| Check | Result | Interpretation |
|-------|--------|----------------|
| Concentration conservation | mean concentration = **1.0000** (target 1) | PASS — consistent with periodic BCs and `c≡1` initialization |
| Phase transition signature | Spearman(`S`, `zeta`) ρ ≈ **0.86**, p ≈ 4×10⁻⁴⁰ | PASS — order rises with alignment |
| Near-incompressibility | discrete `div_u_rms` elevated on the coarse analysis grid | Documented **downsampling caveat** — not treated as a failure of the Stokes sims; finer `--space-stride` reduces this residual |

### Anomalies

A within-cell MAD screen on `nematic_order_S` flags on the order of **~12 / 134** trajectories as atypical relative to their `(alpha, zeta)` neighbors. These are **quality / outlier notes** (unusual random initializations or extract noise), not automatic claims that the underlying physics is broken. See the **Physics & anomalies** tab.

### Methods note

All headline numbers refer to the stride-reduced feature table used for statistics and the live demo. Full-resolution HDF5 fields remain on Hugging Face; re-run extraction with smaller strides for higher-fidelity residuals if needed.

## Project layout

```
phyScientific/
├── app/streamlit_app.py      # Dashboard (3 tabs)
├── data/features.parquet     # Real analysis-ready feature table
├── notebooks/analysis.ipynb  # Narrative statistical analysis
├── src/
│   ├── extract_features.py   # HF stream / synthetic feature builder
│   └── stats.py              # Shared ANOVA / t-test / anomaly helpers
├── requirements.txt          # Full local stack (extraction + app)
├── requirements-app.txt      # Slim runtime deps (Render / demo)
├── render.yaml               # Render Blueprint
└── README.md
```

## Environment (important)

Default system Python may be **3.14**. Extraction needs **3.11 or 3.12**. A `.venv` on Python 3.12 is expected:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

For **running only the dashboard** (no extraction):

```powershell
pip install -r requirements-app.txt
streamlit run app/streamlit_app.py
```

## Data

### Preferred: real features from Hugging Face

`data/features.parquet` should contain **real** The Well `active_matter` trajectories whenever possible. The train split is a complete **5 α × 9 ζ** factorial (**45** HDF5 files). Most cells have **3** trajectories; a few files in the HF release contain 1–2 or 4 trajectories, so a full extract is typically ~130–140 rows rather than a rigid 135.

Each remote file is ~740 MB. Streaming with space/time strides is the efficient path (no full local mirror required):

```powershell
# Full factorial (recommended). Checkpoints after every file; safe to re-run with --resume.
python -u -m src.extract_features --splits train --time-stride 8 --space-stride 16 --max-traj-per-file 3 --workers 4 --out data/features.parquet

# Resume after a network interruption
python -u -m src.extract_features --splits train --time-stride 8 --space-stride 16 --max-traj-per-file 3 --workers 4 --out data/features.parquet --resume
```

**Efficiency plan used by this project**

1. Stream all **45** train cells via `fsspec` + `h5py` (avoids the Windows `WellDataset` path bug).
2. Aggressive but documented strides: `--time-stride 8 --space-stride 16`, capped at 3 traj/file.
3. Concurrent streams with `--workers 4`.
4. Checkpoint every file into `data/features.parquet`.

### Fallback only: synthetic demo table

```powershell
python -m src.extract_features --synthetic --out data/features.parquet
```

## Run the analysis notebook

```powershell
.\.venv\Scripts\Activate.ps1
jupyter notebook notebooks/analysis.ipynb
```

## Run the Streamlit dashboard

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app/streamlit_app.py
```

### Tabs

| Tab | Content |
|-----|---------|
| **ANOVA sandbox** | Sliders for #groups, n, mean difference, within-group SD → live F, p, SSE, η², and an evidence verdict. |
| **Real-data ANOVA** | One-way / two-way ANOVA and pairwise t-tests on `features.parquet`. |
| **Physics & anomalies** | Conservation / incompressibility / phase-transition checks + anomaly table. |

## Deploy on Render

The public demo is a **Render** Web Service (Streamlit needs a long-running process; Vercel/Supabase alone are not suitable without a rewrite).

### One-click from Blueprint

1. Push this repo to GitHub (already: `Emilio-Gordillo-Esparragoza/phyScientific`).
2. Open [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect the `phyScientific` repository.
4. Render reads [`render.yaml`](render.yaml): builds with `requirements-app.txt`, starts Streamlit on `$PORT`.
5. After the first deploy, the service URL is typically `https://physcientific.onrender.com` (confirm in the Render UI).

### Manual Web Service

- **Runtime:** Python 3.12  
- **Build command:** `pip install -r requirements-app.txt`  
- **Start command:** `streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --browser.gatherUsageStats false`  
- **Health check path:** `/`

`data/features.parquet` is committed so the live app does **not** download The Well at runtime. Free tier instances sleep when idle; the first request after sleep can take about a minute.

## Feature dictionary

| Column | Meaning |
|--------|---------|
| `alpha`, `zeta`, `L` | Control / initial-circumstance parameters |
| `mean_concentration`, `std_concentration` | Conservation / mixing |
| `nematic_order_S`, `nematic_order_S_final` | Orientation order parameter (phase transition) |
| `kinetic_energy`, `enstrophy` | Flow intensity |
| `div_u_rms` | Incompressibility residual |
| `spectral_slope` | KE spectrum log–log slope |
| `time_to_steady` | Fraction of time to order-parameter plateau |
| `synthetic` | `False` for real Well data; `True` for demo generator |

## Citation

If you use The Well / `active_matter` data, please cite the Well paper and the active-matter source paper (see [dataset card](https://huggingface.co/datasets/polymathic-ai/active_matter)).
