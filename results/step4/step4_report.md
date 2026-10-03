# Step 4 Bayesian change-point report

The constant model M0 is compared with an analytically integrated one-change-point model M1, a pre-specified recent k=62 model M2, and a simple Bayesian logistic trend M3.

M1 posterior mode of k: 54; posterior mean: 37.42; 95% interval: [11, 54].
P(p_before > p_after): 0.7824.
P(degradation > 0.05): 0.5795.
P(degradation > 0.10): 0.3746.
Recent k=62 P(p_old > p_recent): 0.9998; this analysis is exploratory because the window is motivated by C61/C62.
M1 posterior mass on k >= 50: 0.2696; this boundary concentration does not identify a unique change point.
Change-point prior sensitivity is saved in change_point_prior_sensitivity.csv.
Model comparison Bayes factors are in model_comparison.csv; M1 uses a uniform prior over k=10,...,54.

Interpretation: a change-point posterior is evidence about possible temporal variation, not proof that C61 or C62 caused a permanent reliability change.

Limitations:
- Only four failures are observed.
- The recent regime contains only two launches.
- Configuration and engineering covariates are not modeled.
- The smooth trend uses a numerical grid and is a secondary sensitivity model.
- Out-of-sample scores use small ten-launch test blocks.

## Supplemental sensitivity analyses
The sequential update, calendar-time comparison, configuration-adjusted fits, recent-window grid, aggregate forecasting scores, bootstrap score intervals, and calibration diagnostic are secondary analyses.
Launch-index trend P(slope < 0): 0.7747.
Calendar-time trend P(slope < 0): 0.5492.
Configuration-adjusted fits are penalized logistic sensitivities and are not used as the primary inferential model.
Recent-window results cover the last 2 through 6 launches; the two-launch result must not be treated as confirmatory.
Forecasting score intervals bootstrap the seven historical windows, so they describe window uncertainty rather than pretending to have seven independent large samples.
