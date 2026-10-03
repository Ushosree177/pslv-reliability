# FINAL_RESULTS_v1.2

This lock preserves the empirical Step 1--5 results and updates the validation additions.

## Simulation

- Seed: `20261002`
- Replicates: 2,000 per labelled stream
- Launches per dataset: 64
- Practical-decline flag: `P(Delta > 0.05) > 0.95`
- Monte Carlo intervals: Wilson 95% intervals

The constant reference and repeat-constant streams use the same Bernoulli mechanism `p=0.94` with independent random streams; they are not different scientific mechanisms.

| Stream | Mean P(Delta > 0) | Flag rate | Wilson 95% interval |
|---|---:|---:|---:|
| Constant reference | 0.505 | 0.0050 | [0.0027, 0.0092] |
| Repeat constant stream | 0.495 | 0.0025 | [0.0011, 0.0058] |
| Configuration heterogeneity | 0.504 | 0.0040 | [0.0020, 0.0079] |
| Mild abrupt decline | 0.678 | 0.0185 | [0.0135, 0.0254] |
| Smooth decline | 0.813 | 0.1030 | [0.0904, 0.1171] |
| Strong abrupt decline | 0.900 | 0.2875 | [0.2681, 0.3077] |

## Sequential validation

The 44 paired one-step-ahead predictions use 10,000 bootstrap replicates.

| Metric | Estimate M1 minus M0 | Bootstrap 95% interval |
|---|---:|---:|
| Log score | 0.002105 | [-0.012980, 0.025144] |
| Brier score | -0.000273 | [-0.003411, 0.001707] |

Both intervals include zero.

## Prior sensitivity

Across the five examined priors, posterior means range from 0.9118 to 0.9324, 95% credible intervals overlap substantially, and the posterior predictive probability of two consecutive failures ranges from 0.00541 to 0.00895.
