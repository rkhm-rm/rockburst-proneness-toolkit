# Rockburst Proneness Toolkit

A Python toolkit for calculating and validating rockburst-proneness criteria, developed as part of a Research Assistant project at Nazarbayev University under Prof. Amoussou Coffi Adoko (School of Mining and Geosciences, Department of Mining Engineering).

The toolkit automates the four rockburst-proneness indices used in:

> Wibisono, D.Y., Arora, K. and Gutierrez, M. (2022). *Laboratory Characterization of a Synthetic Sandstone for Tunnel Rockburst Study.* ARMA 22-2032.

## What it does

- Calculates the four established rockburst-proneness criteria from stress-strain test data:
  - **B1** – Strength Brittleness Index (compressive strength / tensile strength)
  - **R** – Burst Energy Coefficient (pre-peak / post-peak stress-strain curve area)
  - **BIM** – Brittleness Index Modified (pre-peak energy / peak elastic strain energy)
  - **F** – Strain Energy Storage Index (retained elastic energy / dissipated energy)
- Computes specimen statistics (mean, standard deviation) from raw multi-specimen data
- Numerically integrates stress-strain curves (trapezoidal rule) to compute energy areas directly from raw data points, rather than requiring pre-calculated values
- Fits a Mohr-Coulomb failure envelope from triaxial test data (linear regression of σ1 vs σ3) to back-calculate cohesion and internal friction angle

## Validation

All methods were validated by reproducing the published results in Wibisono et al. (2022):

| Criterion / Method | Computed | Published | Match |
|---|---|---|---|
| B1 | 6.82 | 5.1 – 9.6 | Strong rockburst |
| R | 1.30 | 1.3 | Bursting rock |
| BIM | 1.18 | 1.18 | Moderate-to-high liability* |
| F | 2.31 | 2.32 | Weak-medium shock |
| Friction angle | 21.4° | 21.4° | Exact match |
| Cohesion | 1.06 MPa | 1.06 MPa | Exact match |

\* The BIM and F classification charts in the source paper use continuous graded bars rather than sharp thresholds, so the numeric value should be treated as more reliable than the qualitative label near boundary values.

## Files

- `rockburst_criteria.py` — the four criteria calculators, classification functions, specimen statistics, curve integration, and Mohr-Coulomb fitting, including illustrative stress-strain and Mohr-Coulomb plots

## Status

This toolkit is validated against published data and is ready to process real laboratory specimen data once physical testing begins for the associated research project ("From Microstructure to Bursting: A Novel Reliability-based Framework for Rockburst Proneness Criteria to Enhance Mining Safety and Rockburst Hazards Management").

## Requirements

- Python 3.13+
- NumPy
- Matplotlib
