"""One-step-ahead validation for the constant and change-point models."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import betaln, logsumexp


DATA = Path(r"D:\PSLV_Reliability\data\PSLV_verified_dataset_v1.0.csv")
OUT = Path(r"D:\PSLV_Reliability\paper\tables\sequential_one_step_scores.csv")
K_MIN = 10
SEED = 20261002
BOOTSTRAPS = 10000


def change_point_predictive_probability(y, next_index):
    """Predict success for next_index after observing y under M1."""
    n = len(y)
    candidates = range(K_MIN, n - K_MIN + 1)
    log_marginal = []
    predictive = []
    for k in candidates:
        left = y[:k]
        right = y[k:]
        left_s = int(left.sum())
        right_s = int(right.sum())
        left_f = len(left) - left_s
        right_f = len(right) - right_s
        log_marginal.append(
            betaln(1 + left_s, 1 + left_f)
            + betaln(1 + right_s, 1 + right_f)
            - 2 * betaln(1, 1)
        )
        if next_index <= k:
            predictive.append((1 + left_s) / (2 + len(left)))
        else:
            predictive.append((1 + right_s) / (2 + len(right)))
    weights = np.exp(np.asarray(log_marginal) - logsumexp(log_marginal))
    return float(np.dot(weights, predictive))


def main():
    y = pd.read_csv(DATA)["success"].to_numpy(dtype=int)
    rows = []
    for training_size in range(20, len(y)):
        observed = y[:training_size]
        actual = int(y[training_size])
        successes = int(observed.sum())
        failures = training_size - successes
        p_m0 = (1 + successes) / (2 + training_size)
        p_m1 = change_point_predictive_probability(observed, training_size + 1)
        rows.append(
            {
                "training_size": training_size,
                "next_launch_index": training_size + 1,
                "actual_success": actual,
                "m0_probability_success": p_m0,
                "m1_probability_success": p_m1,
                "m0_log_score": actual * np.log(p_m0) + (1 - actual) * np.log1p(-p_m0),
                "m1_log_score": actual * np.log(p_m1) + (1 - actual) * np.log1p(-p_m1),
                "m0_brier_score": (p_m0 - actual) ** 2,
                "m1_brier_score": (p_m1 - actual) ** 2,
            }
        )

    detail = pd.DataFrame(rows)
    bootstrap_rng = np.random.default_rng(SEED)
    indices = bootstrap_rng.integers(0, len(detail), size=(BOOTSTRAPS, len(detail)))
    log_differences = (detail.m1_log_score.to_numpy() - detail.m0_log_score.to_numpy())[indices].mean(axis=1)
    brier_differences = (detail.m1_brier_score.to_numpy() - detail.m0_brier_score.to_numpy())[indices].mean(axis=1)
    summary = pd.DataFrame(
        {
            "model": ["M0_constant", "M1_change_point"],
            "observations_scored": [len(detail), len(detail)],
            "mean_log_score": [detail.m0_log_score.mean(), detail.m1_log_score.mean()],
            "mean_brier_score": [detail.m0_brier_score.mean(), detail.m1_brier_score.mean()],
            "total_log_score": [detail.m0_log_score.sum(), detail.m1_log_score.sum()],
        }
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    detail.to_csv(OUT, index=False)
    summary.to_csv(OUT.with_name("sequential_one_step_summary.csv"), index=False)
    comparison = pd.DataFrame(
        {
            "metric": ["log_score_difference_M1_minus_M0", "brier_difference_M1_minus_M0"],
            "estimate": [
                detail.m1_log_score.mean() - detail.m0_log_score.mean(),
                detail.m1_brier_score.mean() - detail.m0_brier_score.mean(),
            ],
            "bootstrap_lower_95": [np.quantile(log_differences, 0.025), np.quantile(brier_differences, 0.025)],
            "bootstrap_upper_95": [np.quantile(log_differences, 0.975), np.quantile(brier_differences, 0.975)],
            "bootstrap_replicates": [BOOTSTRAPS, BOOTSTRAPS],
        }
    )
    comparison.to_csv(OUT.with_name("sequential_one_step_comparison.csv"), index=False)
    print(summary.to_string(index=False))
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()
