# Final scientific synthesis

## Research question
Does the observed clustering of PSLV failures provide statistical evidence of a change in launch reliability relative to a constant-reliability baseline?

## Historical reliability
Across 64 PSLV launches, 60 were successful and 4 were unsuccessful, giving an observed success proportion of 0.9375. Under the primary constant-reliability model, the posterior is Beta(61,5), with mean 0.9242 and 95% credible interval [0.8499, 0.9746].

## Recent failures
The consecutive C61/C62 failures are unusual relative to a simple constant-reliability explanation. This motivates temporal analysis, but unusual clustering alone does not establish a permanent reliability change.

## Time-varying models
Change-point and recent-window analyses are compatible with a reduction in recent reliability. The recent-period signal persists across nearby windows, but the change-point location is not unique, calendar-time evidence is weaker than launch-index evidence, and only four failures are available.

## Prediction
Rolling-origin validation does not show a clear predictive advantage for the more complex models. The constant model has slightly better average scores, while the bootstrap interval for the M1-versus-M0 log-score difference includes zero.

## Scientific boundary
The statistical analysis describes temporal patterns in launch outcomes. It does not establish an engineering mechanism or causal effect. Future comparable launches can update the posterior: a success gives Beta(62,5), while a failure gives Beta(61,6).

Analysis date: 2026-10-01. Dataset: PSLV_verified_dataset_v1.0.csv.