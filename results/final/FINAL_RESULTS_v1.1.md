# FINAL_RESULTS_v1.1

This update preserves all locked Step 1--5 results from `FINAL_RESULTS_v1.0.md` and adds two reproducible validation analyses.

## Added analyses

- Operating-characteristics simulation: 500 replicates per scenario, seed 20261002, 64 observations per dataset.
- One-step-ahead prequential validation: training sizes 20 through 63, 44 scored predictions.

## Simulation results

The practical-decline flag is `P(Delta > 0.05) > 0.95`.

| Scenario | Mean P(Delta > 0) | Practical flag rate | Mean change-point mode | Mean posterior success |
|---|---:|---:|---:|---:|
| Constant, p=0.94 | 0.490 | 0.008 | 29.54 | 0.929 |
| Random clustering, p=0.94 | 0.518 | 0.000 | 30.71 | 0.927 |
| Configuration heterogeneity | 0.485 | 0.000 | 30.08 | 0.931 |
| Mild abrupt decline | 0.677 | 0.020 | 35.33 | 0.922 |
| Smooth decline | 0.805 | 0.104 | 37.18 | 0.898 |
| Strong abrupt decline | 0.906 | 0.294 | 37.82 | 0.873 |

## Sequential validation results

| Model | Predictions | Mean log score | Mean Brier score |
|---|---:|---:|---:|
| M0 constant | 44 | -0.261275 | 0.064906 |
| M1 change point | 44 | -0.259170 | 0.064632 |

The sequential improvement for M1 is small and is not treated as decisive evidence of predictive superiority. It complements, rather than replaces, the locked seven-window validation.

## Interpretation

The expanded evidence supports a conservative conclusion: the framework has low practical-decline flag rates under stable, clustered, and configuration-heterogeneous scenarios, but limited power under sparse abrupt or smooth changes. In the PSLV data, the failure cluster is unusual, degradation is plausible but poorly identified, and no robust predictive advantage for a time-varying model is established.
