# Bayesian Reliability Surveillance of PSLV Launches

## Overview

This project develops an auditable **Bayesian reliability-surveillance
framework** for a sparse sequence of PSLV launch outcomes.

The motivating observation is that the final two launches in the
analyzed record, **PSLV-C61 and PSLV-C62**, were unsuccessful. Two
consecutive failures can be unusual under a high-reliability system
without necessarily proving that the underlying reliability has
permanently deteriorated.

The project therefore separates three questions:

1.  **Surveillance:** Is the observed failure clustering unusual under a
    constant-reliability reference model?
2.  **Diagnosis:** Is a temporal change in reliability plausible, and
    how uncertain are its timing and magnitude?
3.  **Prediction:** Does introducing temporal structure actually improve
    prediction of future launches?

The analysis is deliberately framed as a statistical reliability study.
It does **not** claim to establish an engineering root cause or prove a
causal mechanism.

------------------------------------------------------------------------

## Research Question

> **Does the observed clustering of PSLV failures provide statistical
> evidence of a change in launch reliability relative to a
> constant-reliability baseline?**

A secondary question is:

> **Does a more complex time-varying reliability model improve
> prospective predictive performance over a constant-reliability
> model?**

These questions are intentionally separated because an unusual sequence,
evidence of temporal heterogeneity, and improved forecasting are not
equivalent claims.

------------------------------------------------------------------------

# Architecture

``` mermaid
flowchart TD

    A[Official PSLV Mission Records] --> B[Source Audit]
    B --> C[Frozen Version 1.0 Dataset]

    C --> D[Data Quality Checks]
    D --> E[Exploratory Data Analysis]

    E --> F1[Failure Chronology]
    E --> F2[Failure Gaps]
    E --> F3[Cumulative Success]
    E --> F4[Rolling Success]
    E --> F5[Failure Timeline]
    E --> F6[Rolling Uncertainty]

    C --> G[Bayesian Constant Baseline M0]
    G --> G1[Beta-Bernoulli Model]
    G1 --> G2[Posterior Beta(61,5)]
    G1 --> G3[Prior Sensitivity]
    G1 --> G4[Posterior Predictive Checks]
    G1 --> G5[Sequential Bayesian Updating]

    C --> H[Surveillance Layer]
    H --> H1[Runs Probability]
    H --> H2[Failure-Gap Analysis]
    H --> H3[Posterior Predictive Probability]

    C --> I[Diagnosis Layer]
    I --> I1[Interior Bayesian Change Point M1]
    I --> I2[Recent-Window Sensitivity M2]
    I --> I3[Smooth Logistic Trend M3]
    I --> I4[Configuration-Adjusted Sensitivity]
    I --> I5[Degradation Probabilities]

    C --> J[Operating-Characteristics Simulation]
    J --> J1[Constant]
    J --> J2[Configuration Heterogeneity]
    J --> J3[Mild Abrupt Decline]
    J --> J4[Smooth Decline]
    J --> J5[Strong Abrupt Decline]

    G --> K[Predictive Validation]
    I --> K

    K --> K1[Rolling-Origin Validation]
    K --> K2[One-Step-Ahead Prequential Validation]
    K1 --> K3[Log Score]
    K1 --> K4[Brier Score]
    K2 --> K3
    K2 --> K4
    K3 --> K5[Bootstrap Uncertainty]
    K4 --> K5
    K5 --> L[Calibration]

    H --> M[Integrated Evidence]
    I --> M
    J --> M
    K --> M
    G --> M

    M --> N[Statistical Interpretation]
    N --> O[Engineering/Causal Boundary]
    O --> P[Final Conclusion]
```

------------------------------------------------------------------------

# 1. Data

## Dataset

The frozen Version 1.0 dataset contains:

-   **64 chronological PSLV launches**
-   **60 successful primary missions**
-   **4 unsuccessful primary missions**
-   Observed success proportion: **0.9375 (93.75%)**

The four unsuccessful missions are:

-   PSLV-D1
-   PSLV-C39
-   PSLV-C61
-   PSLV-C62

The final two failures, C61 and C62, are consecutive.

Each launch record retains information such as:

-   launch date
-   mission identifier
-   source-facing outcome
-   outcome verification source
-   source disagreement indicator
-   launch configuration
-   failure-stage information
-   cause-status information
-   previous-failure indicator

### Data audit

The final audit records:

-   64 launches
-   0 duplicate missions
-   0 missing dates
-   0 missing outcomes
-   0 unverified outcomes
-   1 reviewed source conflict
-   2 missing/unknown configuration values
-   5 missing payload fields

The data-freeze rule is:

> Any future correction creates a new dataset version rather than
> silently changing the analysis input.

Failure-stage descriptions are treated as descriptive metadata, not as
proven root causes.

------------------------------------------------------------------------

# 2. Statistical Unit

The statistical unit is **one launch**.

For launch (i):

\[ Y_i =
```{=tex}
\begin{cases}
1, & \text{successful primary mission}\\
0, & \text{unsuccessful primary mission}
\end{cases}
```
\]

The simplest probability model is therefore Bernoulli:

\[ Y_i `\mid `{=tex}p `\sim `{=tex}`\text{Bernoulli}`{=tex}(p). \]

Here (p) represents the underlying probability of a successful launch.

------------------------------------------------------------------------

# 3. Overall Analytical Strategy

The project is organized into three layers.

## Layer 1 --- Surveillance

Question:

> Is the observed failure ordering unusual under a stable reference
> process?

Methods:

-   conditional runs probability
-   failure-gap summaries
-   posterior predictive probability of consecutive failures
-   prior predictive checks
-   posterior predictive checks

## Layer 2 --- Diagnosis

Question:

> Could the underlying reliability have changed over time?

Methods:

-   Bayesian unknown change-point model
-   recent-window sensitivity analysis
-   smooth temporal trend model
-   launch-index versus calendar-time sensitivity
-   configuration-adjusted sensitivity analysis
-   posterior probabilities of practical degradation

## Layer 3 --- Prediction

Question:

> Does the additional temporal structure improve forecasts of unseen
> launches?

Methods:

-   rolling-origin validation
-   one-step-ahead prequential validation
-   log score
-   Brier score
-   calibration
-   paired bootstrap uncertainty

The three layers must not be conflated.

------------------------------------------------------------------------

# 4. Baseline Model: Beta-Bernoulli Reliability

The constant-reliability model is:

\[ Y_i `\mid `{=tex}p `\sim `{=tex}`\text{Bernoulli}`{=tex}(p) \]

with:

\[ p `\sim `{=tex}`\text{Beta}`{=tex}(1,1). \]

The prior is uniform over the interval (\[0,1\]).

The observed data contain:

\[ S=60 \]

successes and:

\[ F=4 \]

failures.

Because the Beta prior is conjugate to the Bernoulli likelihood:

\[ p`\mid `{=tex}D `\sim `{=tex}`\text{Beta}`{=tex}(1+60,1+4) \]

so:

\[ `\boxed{p\mid D \sim \text{Beta}(61,5)}`{=tex} \]

The posterior mean is:

\[ E\[p`\mid `{=tex}D\] = `\frac{61}{61+5}`{=tex} = 0.9242. \]

The central 95% credible interval is:

\[ \[0.8499,0.9746\]. \]

This model is the reference against which temporal models are compared.

------------------------------------------------------------------------

# 5. Prior Sensitivity

Because Bayesian results can depend on the prior when data are sparse,
multiple priors were examined:

-   Beta(0.5, 0.5)
-   Beta(1, 1)
-   Beta(2, 2)
-   Beta(5, 1)
-   Beta(9, 1)

The posterior means range from:

\[ 0.9118 `\quad `{=tex}`\text{to}`{=tex} `\quad 0.9324`{=tex}. \]

The resulting credible intervals overlap substantially.

The posterior predictive probability of two consecutive failures ranges
from approximately:

\[ 0.00541 `\quad `{=tex}`\text{to}`{=tex} `\quad 0.00895`{=tex}. \]

This supports stability of the qualitative interpretation under the
examined priors.

------------------------------------------------------------------------

# 6. Surveillance: Is the Failure Cluster Unusual?

The failures occur at launch indices:

\[ 1,;41,;63,;64. \]

The final two failures therefore form a consecutive pair.

## 6.1 Runs Probability

The exact lower-tail runs probability under the conditional reference
is:

\[ 0.0090. \]

This indicates that the observed ordering is unusual under that
reference.

However:

> An unusual ordering is not by itself evidence that a persistent
> engineering degradation exists.

## 6.2 Posterior Predictive Probability

Under the constant model:

\[ p`\mid `{=tex}D`\sim`{=tex}`\text{Beta}`{=tex}(61,5). \]

The probability that the next two launches are both failures is:

\[ E\[(1-p)\^2`\mid `{=tex}D\] = `\frac{5\cdot6}{66\cdot67}`{=tex} =
0.0068. \]

Thus:

\[
`\boxed{P(\text{two consecutive future failures}\mid M_0,D)=0.0068}`{=tex}
\]

This provides a Bayesian measure of how unusual such a pair is under the
constant-reliability model.

------------------------------------------------------------------------

# 7. Diagnosis: Bayesian Change-Point Model

The primary temporal model allows one unknown change point (k).

\[ p_i =
```{=tex}
\begin{cases}
p_1, & i\leq k\\
p_2, & i>k
\end{cases}
```
\]

where:

-   (p_1) = reliability before the change
-   (p_2) = reliability after the change
-   \(k\) = unknown change-point location

Independent:

\[ p_1,p_2`\sim`{=tex}`\text{Beta}`{=tex}(1,1) \]

priors are used.

The interior model evaluates:

\[ k`\in`{=tex}{10,`\ldots`{=tex},54}. \]

At least 10 launches are required in each segment.

This restriction prevents one- or two-launch segments from dominating
the model comparison.

It also means that the interior model is **not designed to place an
abrupt change at launches 63--64**.

------------------------------------------------------------------------

# 8. Degradation Parameter

The practical reliability difference is defined as:

\[ `\Delta`{=tex}=p\_{`\text{before}`{=tex}}-p\_{`\text{after}`{=tex}}.
\]

Three posterior quantities are emphasized:

\[ P(`\Delta`{=tex}\>0) \]

\[ P(`\Delta`{=tex}\>0.05) \]

\[ P(`\Delta`{=tex}\>0.10). \]

Interpretation:

-   (P(`\Delta`{=tex}\>0)): probability of any decline
-   (P(`\Delta`{=tex}\>0.05)): probability of a decline exceeding 5
    percentage points
-   (P(`\Delta`{=tex}\>0.10)): probability of a decline exceeding 10
    percentage points

Observed values:

\[ P(`\Delta`{=tex}\>0)=0.7824 \]

\[ P(`\Delta`{=tex}\>0.05)=0.5795 \]

\[ P(`\Delta`{=tex}\>0.10)=0.3746. \]

These indicate that a decline is plausible, but strong evidence for a
large decline is not established.

------------------------------------------------------------------------

# 9. Change-Point Uncertainty

For the interior change-point model:

-   posterior mode: (k=54)
-   posterior mean: (37.42)
-   central 95% interval: (\[11,54\])

The mode occurs at the upper boundary of the permitted grid.

Therefore:

> The mode at (k=54) must not be interpreted as an identified physical
> or statistical transition exactly at launch 54.

The broad posterior interval indicates substantial uncertainty about the
transition location.

------------------------------------------------------------------------

# 10. Endpoint-Sensitive Recent-Window Analysis

Because C61 and C62 are at the endpoint, an additional analysis compares
the historical period with the final:

-   2 launches
-   3 launches
-   4 launches
-   5 launches
-   6 launches

For the last two launches:

\[ P(p\_{`\text{old}`{=tex}}\>p\_{`\text{recent}`{=tex}})=0.9998. \]

For the last six launches:

\[ P(p\_{`\text{old}`{=tex}}\>p\_{`\text{recent}`{=tex}})=0.9931. \]

These results are useful for surveillance but are explicitly treated as
exploratory because the recent windows were examined after the failure
sequence was observed and the number of failures is small.

------------------------------------------------------------------------

# 11. Smooth Temporal Trend

The change-point model assumes a relatively abrupt transition.

A separate model allows reliability to change smoothly over time using
Bayesian logistic regression:

\[ `\text{logit}`{=tex}(p_t)=`\alpha`{=tex}+`\beta `{=tex}t. \]

A negative (`\beta`{=tex}) corresponds to a declining success
probability.

Two time representations are considered:

1.  launch-index time
2.  calendar time

The posterior probability of a negative trend is:

-   launch-index time: **0.7747**
-   calendar time: **0.5492**

The difference illustrates sensitivity to how time is represented.

------------------------------------------------------------------------

# 12. Configuration-Adjusted Sensitivity

Configuration indicators are incorporated into penalized logistic
models, with and without temporal terms.

These analyses are descriptive sensitivity checks rather than primary
inferential models because only four failures are observed and several
configuration groups are sparse.

The purpose is to investigate whether an apparent temporal pattern could
be related to configuration heterogeneity.

------------------------------------------------------------------------

# 13. Bayes Factors

Model comparisons include:

\[ BF\_{M1/M0}=0.300 \]

for the interior change-point model,

\[ BF\_{M2/M0}=115.56 \]

for the two-launch member of the exploratory recent-window family, and

\[ BF\_{M3/M0}=1.320 \]

for the smooth trend model.

The large two-launch Bayes factor must not be interpreted as proof of a
uniquely identified change point because that endpoint comparison is
specifically motivated by the observed C61/C62 pair.

------------------------------------------------------------------------

# 14. Operating-Characteristics Simulation

A simulation study evaluates how the surveillance/diagnosis procedure
behaves under sparse data.

The simulation uses:

-   (n=64) launches
-   the same Beta-Bernoulli baseline
-   the same interior change-point grid
-   2,000 datasets per scenario
-   random seed: `20261002`

## Simulated scenarios

### A. Constant reference

\[ p=0.94 \]

### B. Independent constant replicate

Same constant mechanism with an independent random stream.

### C. Strong abrupt decline

\[ 0.97`\rightarrow0.80`{=tex} \]

after launch 32.

### D. Mild abrupt decline

\[ 0.96`\rightarrow0.91`{=tex} \]

### E. Smooth decline

\[ 0.97`\rightarrow0.85`{=tex} \]

### F. Configuration heterogeneity

Configuration-specific probabilities:

\[ 0.98,;0.94,;0.90,;0.96 \]

without a temporal trend.

------------------------------------------------------------------------

# 15. Simulation Decision Flag

A secondary practical-decline flag is recorded when:

\[ P(`\Delta`{=tex}\>0.05)\>0.95. \]

This is a reporting threshold, not an operational reliability or safety
limit.

## Flag rates

  Scenario                        Practical-decline flag rate
  ----------------------------- -----------------------------
  Constant reference                                    0.50%
  Repeat constant                                       0.25%
  Configuration heterogeneity                           0.40%
  Mild abrupt decline                                   1.85%
  Smooth decline                                       10.30%
  Strong abrupt decline                                28.75%

The simulation demonstrates two important properties:

1.  False alarms are low under stable or non-temporal scenarios.
2.  Detection power is limited when only 64 launches are available.

Even a strong simulated abrupt decline is flagged in only 28.75% of
simulated datasets.

Therefore, failure to detect a strong change in a sparse record cannot
automatically be interpreted as evidence that no change exists.

------------------------------------------------------------------------

# 16. Predictive Validation

Temporal diagnosis and prediction are deliberately separated.

A model can indicate temporal heterogeneity without producing better
future forecasts.

Two predictive-validation designs are used.

------------------------------------------------------------------------

## 16.1 Rolling-Origin Validation

Training cutoffs:

``` text
20, 25, 30, 35, 40, 45, 50
```

At each cutoff, the following ten launches are held out.

Example:

``` text
Train: 1–20
Test:  21–30
```

Then:

``` text
Train: 1–25
Test:  26–35
```

and so forth.

The last scored block is launches 51--60, so C61 and C62 are not
directly included in this historical validation design.

------------------------------------------------------------------------

# 17. Predictive Metrics

## Log Score

For predicted success probability (q_i):

\[ LS= `\frac{1}{m}`{=tex} `\sum`{=tex}\_{i=1}\^{m} \[
y_i`\log`{=tex}(q_i) + (1-y_i)`\log`{=tex}(1-q_i)\]. \]

Higher is better.

Log score strongly penalizes confidently incorrect predictions.

## Brier Score

\[ BS= `\frac{1}{m}`{=tex} `\sum`{=tex}\_{i=1}^{m}(q_i-y_i)^2. \]

Lower is better.

------------------------------------------------------------------------

# 18. Historical Predictive Results

  Model               Mean Log Score   Mean Brier Score
  ----------------- ---------------- ------------------
  M0 Constant                -0.1503            0.02999
  M1 Change Point            -0.1577            0.03097
  M3 Smooth Trend            -0.1507            0.03000

The constant model is slightly better on average in the historical
rolling-origin design.

The bootstrap 95% interval for the M1--M0 log-score difference is:

\[ \[-0.0195,0.0035\]. \]

Because the interval includes zero, a robust predictive advantage is not
established.

------------------------------------------------------------------------

# 19. One-Step-Ahead Prequential Validation

A complementary design makes 44 sequential one-step-ahead predictions.

For each training size:

\[ 20,21,`\ldots`{=tex},63, \]

the next launch is predicted using only previous outcomes.

Workflow:

``` text
Train on launches 1–20
        ↓
Predict launch 21
        ↓
Observe launch 21
        ↓
Train on launches 1–21
        ↓
Predict launch 22
        ↓
Repeat
        ↓
Predict through launch 64
```

This design includes the final launches after their preceding histories.

------------------------------------------------------------------------

# 20. Sequential Predictive Results

  Model               Mean Log Score   Mean Brier Score
  ----------------- ---------------- ------------------
  M0 Constant                -0.2613            0.06491
  M1 Change Point            -0.2592            0.06463

The change-point model is numerically slightly better in this sequential
design.

However:

### Log-score difference

\[ M1-M0=0.002105 \]

95% interval:

\[ \[-0.012980,0.025144\]. \]

### Brier difference

\[ -0.000273 \]

95% interval:

\[ \[-0.003411,0.001707\]. \]

Both intervals include zero.

Therefore, the sequential design also does not establish a robust
predictive advantage.

------------------------------------------------------------------------

# 21. Bootstrap Uncertainty

The paired validation scores are resampled 10,000 times to assess
uncertainty in model-score differences.

Because the validation windows overlap and the number of failures is
small, the bootstrap is treated as a descriptive uncertainty assessment
rather than a large-sample inferential guarantee.

------------------------------------------------------------------------

# 22. Calibration

Calibration compares:

\[ `\text{mean predicted probability}`{=tex} \]

against:

\[ `\text{observed success frequency}`{=tex}. \]

A perfectly calibrated model lies near the 45-degree line.

Calibration is used as an exploratory predictive diagnostic alongside
log and Brier scores.

------------------------------------------------------------------------

# 23. Posterior Predictive Checking

Posterior predictive checks ask:

> If the fitted model were the data-generating mechanism, what datasets
> or future outcomes would it generate?

The reproducibility archive includes checks involving:

-   number of future failures
-   longest failure runs
-   change-point model predictive runs
-   recent-failure sensitivity
-   historical posterior updating

These checks help assess whether the observed sequence is compatible
with the fitted probability model.

------------------------------------------------------------------------

# 24. Sequential Bayesian Updating

Under the constant model:

\[ p`\mid `{=tex}D`\sim `{=tex}Beta(61,5). \]

If a future launch succeeds:

\[ Beta(61,5)`\rightarrow `{=tex}Beta(62,5). \]

If a future launch fails:

\[ Beta(61,5)`\rightarrow `{=tex}Beta(61,6). \]

This provides a direct mechanism for continued reliability surveillance
as new launch outcomes become available.

------------------------------------------------------------------------

# 25. Engineering and Causal Boundary

The statistical analysis can quantify:

-   how unusual the failure ordering is
-   uncertainty about possible temporal change
-   possible degradation magnitude
-   predictive performance of competing statistical models

It cannot, from this dataset alone:

-   identify a failed component
-   prove a common physical mechanism
-   prove that a stage-level anomaly caused a long-term reliability
    change
-   replace engineering failure investigation

Therefore:

> **Statistical association with time is not treated as causal
> engineering attribution.**

------------------------------------------------------------------------

# 26. Final Findings

The frozen PSLV record contains:

-   64 launches
-   60 successes
-   4 failures

The final two failures are unusual under the constant-reliability
reference.

A temporal decline is plausible, but:

-   the change-point location is diffuse
-   the magnitude of degradation is uncertain
-   endpoint evidence is exploratory
-   smooth-trend evidence depends on the definition of time
-   configuration information is sparse
-   predictive improvement is not robustly demonstrated

The historical rolling-origin validation slightly favors the constant
model.

The endpoint-inclusive sequential validation gives the change-point
model a small numerical advantage, but the uncertainty interval includes
zero.

Therefore the defensible statistical conclusion is:

> **The recent failure cluster warrants continued surveillance, but the
> available evidence does not establish a persistent reliability
> degradation or a robust predictive advantage for time-varying
> models.**

------------------------------------------------------------------------

# 27. Reproducibility Architecture

The project should maintain the following logical repository structure:

``` text
pslv-bayesian-reliability/
│
├── README.md
│
├── data/
│   ├── raw/
│   ├── audited/
│   └── frozen/
│
├── data_audit/
│   ├── source_audit/
│   ├── data_dictionary/
│   └── freeze_statement/
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_bayesian_baseline.ipynb
│   ├── 04_change_point.ipynb
│   ├── 05_temporal_sensitivity.ipynb
│   ├── 06_simulation.ipynb
│   └── 07_predictive_validation.ipynb
│
├── src/
│   ├── data/
│   ├── baseline/
│   ├── surveillance/
│   ├── changepoint/
│   ├── trends/
│   ├── simulation/
│   ├── prediction/
│   └── diagnostics/
│
├── simulations/
│   ├── scenarios/
│   ├── outputs/
│   └── figures/
│
├── validation/
│   ├── rolling_origin/
│   ├── sequential/
│   ├── bootstrap/
│   └── calibration/
│
├── figures/
│   ├── main/
│   └── supplementary/
│
├── results/
│   ├── tables/
│   ├── model_outputs/
│   └── validation_reports/
│
├── manuscript/
│   └── manuscript.tex
│
└── analysis_manifest/
    └── versioned_manifest
```

This is a **recommended organization for reproducibility**; the
manuscript itself states that the reproducibility package contains the
data-construction script, analysis notebooks, simulation and
sequential-validation scripts, random seeds, priors, validation windows,
and analysis outputs in a versioned analysis manifest.

------------------------------------------------------------------------

# 28. Reproducibility Principles

The project follows these principles:

### 1. Freeze the data before inference

No silent changes to the analysis dataset.

### 2. Record all assumptions

Examples:

-   priors
-   candidate change-point grid
-   minimum segment size
-   simulation scenarios
-   validation windows
-   random seeds

### 3. Separate exploratory and confirmatory evidence

The recent-window analysis is explicitly treated as exploratory.

### 4. Separate model fit from prediction

A model that describes historical temporal variation is not
automatically a better forecasting model.

### 5. Quantify uncertainty

Use:

-   posterior distributions
-   credible intervals
-   bootstrap intervals
-   Monte Carlo intervals

### 6. Preserve the causal boundary

Statistical temporal association is not treated as proof of engineering
causality.

------------------------------------------------------------------------

# 29. Key Mathematical Objects

  Symbol             Meaning
  ------------------ -------------------------------------------
  (Y_i)              Outcome of launch (i)
  \(p\)              Constant success probability
  (p_1)              Pre-change success probability
  (p_2)              Post-change success probability
  \(k\)              Unknown change-point location
  (`\Delta`{=tex})   (p\_{before}-p\_{after})
  (q_i)              Predicted success probability
  (LS)               Log score
  (BS)               Brier score
  (M_0)              Constant-reliability model
  (M_1)              Interior Bayesian change-point model
  (M_2)              Endpoint/recent-window sensitivity family
  (M_3)              Smooth temporal trend model

------------------------------------------------------------------------

# 30. Key Results at a Glance

``` text
Launches                         64
Successes                        60
Failures                         4
Observed success rate            93.75%

M0 posterior                     Beta(61,5)
M0 posterior mean                0.9242
M0 95% credible interval         [0.8499, 0.9746]

Runs probability                 0.0090
M0 P(two consecutive failures)   0.0068
M1 P(two consecutive failures)   0.0312

M1 P(Δ > 0)                      0.7824
M1 P(Δ > 0.05)                   0.5795
M1 P(Δ > 0.10)                   0.3746

Recent 2: P(old > recent)       0.9998
Recent 6: P(old > recent)       0.9931

Historical M0 log score          -0.1503
Historical M1 log score          -0.1577
Historical M3 log score          -0.1507

Sequential M0 log score          -0.2613
Sequential M1 log score          -0.2592

Sequential M1-M0 log difference  0.002105
95% interval                     [-0.012980, 0.025144]
```

------------------------------------------------------------------------

# 31. Limitations

The principal limitations are:

1.  Only four failures are observed.
2.  Launches may not be perfectly independent or exchangeable.
3.  Configuration groups are sparse.
4.  The final two-launch window contains only two observations.
5.  Launch-index time and calendar time answer different temporal
    questions.
6.  The interior change-point model deliberately excludes tiny terminal
    segments.
7.  The recent-window model is endpoint-sensitive and exploratory.
8.  Historical validation uses overlapping test windows.
9.  The historical rolling-origin validation stops before C61/C62.
10. The endpoint-inclusive sequential validation contains only 44
    predictions.
11. Statistical association does not establish engineering causality.

------------------------------------------------------------------------

# 32. References

The methodology is grounded in the references used in the manuscript,
including:

-   Gelman et al. --- *Bayesian Data Analysis*
-   Reliability estimation under scarce data
-   Bayesian reliability updating
-   Bayesian change-point analysis
-   Proper scoring rules
-   Forecast evaluation
-   Bootstrap methodology
-   Official Indian Space Research Organisation PSLV mission records

The primary public data sources used in the manuscript are the official
ISRO PSLV launch history and the official PSLV-C62 mission catalogue.

------------------------------------------------------------------------

## Project Status

**Framework:** Complete

**Dataset:** Frozen Version 1.0

**Main analysis:** Complete

**Operating-characteristics simulation:** Complete

**Historical rolling-origin validation:** Complete

**Sequential one-step-ahead validation:** Complete

**Supplementary diagnostics:** Complete

**Manuscript interpretation:** Complete

**Core conclusion:** Recent clustering is unusual and a decline is
plausible, but persistent degradation and robust predictive improvement
are not established by the current sparse record.
