# FINAL_RESULTS_v1.0

Analysis date: 2026-10-01
Dataset: PSLV_verified_dataset_v1.0.csv
Observations: 64
Successes: 60
Failures: 4
Primary prior: Beta(1,1)
Random seed used for Step 5 simulations: 20261001
Validation windows: cutoffs 20, 25, 30, 35, 40, 45, 50; ten-launch test blocks

## Locked model definitions
- M0: constant reliability, p ~ Beta(1,1).
- M1: one change point, k in 10,...,54, with independent segment priors Beta(1,1).
- M2: exploratory recent windows containing 2, 3, 4, 5, or 6 launches.
- M3: Bayesian logistic trend with Normal(0,2.5) intercept and Normal(0,1) slope grid prior.
- Configuration sensitivity: penalized logistic fits, descriptive only.

## Locked computational details
- Step 4 posterior simulations use seed 20261001 and 50,000 draws.
- Recent-window simulations use seeds 20261003 through 20261007 and 30,000 draws per window.
- Forecast comparison uses paired seven-window resampling and 10,000 bootstrap replicates with seed 20261001.
- Calibration uses every held-out prediction from seven ten-launch test blocks, binned at 0.90, 0.925, 0.95, and 0.975.

## Locked interpretation
The final two failures are unusual under a constant model. A decline is plausible, but its magnitude and timing are uncertain. Time-varying models do not show a clear predictive advantage. No causal engineering claim is made.

## Main files
- summary_statistical_results.csv
- evidence_ladder.csv
- final_two_failure_model_comparison.csv
- model_decision_matrix.csv
- robustness_matrix.csv
- assumption_audit.csv
- master_figure.png
- step5_reliability_uncertainty.png
- step5_predictive_comparison.png
- step5_scientific_synthesis.md
- manuscript_v1.0.md

## Software
Python 3.11.0 on Windows-10-10.0.26200-SP0
