# Step 3 Bayesian constant-reliability report

Under Beta(1,1), the analytical posterior is Beta(61,5). Posterior mean: 0.9242.
95% credible interval: [0.8499, 0.9746].
Exact posterior predictive probability of next-launch success: 0.9242.
Exact posterior predictive probability of two specified future failures: 0.00678.
This is a posterior predictive probability, not a conventional p-value.

The overall failure count and longest failure run are compared with posterior predictive simulations.
The final-two-failures event is relatively uncommon under the fitted constant model.
This motivates Step 4 but does not prove a change in reliability.

## Limitations

- All launches share one underlying success probability p.
- Outcomes are conditionally independent given p.
- Vehicle configuration differences are not included in the primary model.
- Mission classification is treated as fixed.
- Engineering covariates and failure mechanisms are not modeled.
- The model cannot establish causal reasons for failures.
- Future predictions assume the same reliability mechanism continues.

Random seeds checked: 20261001, 20261002, 20261003.
Simulation count per check: 50000.