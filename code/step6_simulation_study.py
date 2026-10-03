"""Simple operating-characteristics study for the PSLV surveillance framework.

The simulation uses the same Beta-Bernoulli constant model and the same
uniform-prior change-point calculation used in the paper.  It asks a narrow
question: how often does the change-point layer report a practically large
decline when the data-generating process is constant, abruptly changing, or
smoothly changing?

The script writes one summary table for the manuscript and one row-level
table for reproducibility.  It intentionally does not simulate engineering
causes or claim that simulated scenarios reproduce PSLV.
"""

from pathlib import Path
import math

import numpy as np
import pandas as pd
from scipy.special import betaln


SEED = 20261002
REPLICATES = 2000
N_LAUNCHES = 64
K_VALUES = np.arange(10, 55)
DRAW_COUNT = 1000


def change_point_posterior(y):
    """Return posterior weights for the same M1 model used in the paper."""
    log_weights = []
    for k in K_VALUES:
        left = y[:k]
        right = y[k:]
        left_success = int(left.sum())
        right_success = int(right.sum())
        left_failure = len(left) - left_success
        right_failure = len(right) - right_success
        log_left = betaln(1 + left_success, 1 + left_failure) - betaln(1, 1)
        log_right = betaln(1 + right_success, 1 + right_failure) - betaln(1, 1)
        log_weights.append(log_left + log_right)
    log_weights = np.asarray(log_weights)
    weights = np.exp(log_weights - log_weights.max())
    return weights / weights.sum()


def posterior_decline_probability(y, threshold, rng):
    """Estimate P(delta > threshold) after averaging over k and p1, p2."""
    weights = change_point_posterior(y)
    probabilities = []
    for k in K_VALUES:
        left = y[:k]
        right = y[k:]
        left_success = int(left.sum())
        right_success = int(right.sum())
        p_before = rng.beta(1 + left_success, 1 + len(left) - left_success, DRAW_COUNT)
        p_after = rng.beta(1 + right_success, 1 + len(right) - right_success, DRAW_COUNT)
        probabilities.append(np.mean((p_before - p_after) > threshold))
    return float(np.dot(weights, probabilities)), int(K_VALUES[np.argmax(weights)])


def smooth_probabilities(start, end):
    """Create a smooth launch-index reliability path from start to end."""
    t = np.linspace(-6, 6, N_LAUNCHES)
    transition = 1 / (1 + np.exp(-t))
    return start + (end - start) * transition


def make_scenarios():
    """Return named probability paths for transparent simulation scenarios."""
    return {
        "constant": np.full(N_LAUNCHES, 0.94),
        "abrupt_decline": np.r_[np.full(32, 0.97), np.full(32, 0.80)],
        "mild_abrupt_decline": np.r_[np.full(32, 0.96), np.full(32, 0.91)],
        "smooth_decline": smooth_probabilities(0.97, 0.85),
        "random_clustering": np.full(N_LAUNCHES, 0.94),
        "configuration_heterogeneity": np.tile([0.98, 0.94, 0.90, 0.96], 16),
    }


def main():
    rng = np.random.default_rng(SEED)
    scenario_paths = make_scenarios()
    rows = []

    for scenario, probabilities in scenario_paths.items():
        for replicate in range(REPLICATES):
            y = rng.binomial(1, probabilities)
            decline_0, mode_k = posterior_decline_probability(y, 0.0, rng)
            decline_5, _ = posterior_decline_probability(y, 0.05, rng)
            successes = int(y.sum())
            failures = N_LAUNCHES - successes
            p_hat = (1 + successes) / (2 + N_LAUNCHES)
            lower = rng.beta(1 + successes, 1 + failures, 2000)
            lower_bound = float(np.quantile(lower, 0.025))
            upper_bound = float(np.quantile(lower, 0.975))
            rows.append(
                {
                    "scenario": scenario,
                    "replicate": replicate + 1,
                    "successes": successes,
                    "failures": failures,
                    "posterior_decline_probability": decline_0,
                    "posterior_practical_decline_probability": decline_5,
                    "change_point_mode": mode_k,
                    "meaningful_decline_flag": int(decline_5 > 0.95),
                    "constant_posterior_mean": p_hat,
                    "constant_95_lower": lower_bound,
                    "constant_95_upper": upper_bound,
                }
            )

    detail = pd.DataFrame(rows)
    summary = (
        detail.groupby("scenario", as_index=False)
        .agg(
            replicates=("replicate", "count"),
            mean_posterior_decline_probability=("posterior_decline_probability", "mean"),
            meaningful_decline_rate=("meaningful_decline_flag", "mean"),
            mean_change_point_mode=("change_point_mode", "mean"),
            mean_posterior_success=("constant_posterior_mean", "mean"),
        )
    )
    flag_counts = detail.groupby("scenario")["meaningful_decline_flag"].agg(["sum", "count"]).reset_index()
    z = 1.96
    flag_counts["flag_rate_lower_95"] = 0.0
    flag_counts["flag_rate_upper_95"] = 0.0
    for row_index, row in flag_counts.iterrows():
        successes = float(row["sum"])
        trials = float(row["count"])
        denominator = 1 + z**2 / trials
        center = (successes / trials + z**2 / (2 * trials)) / denominator
        half_width = z * np.sqrt((successes / trials * (1 - successes / trials) / trials) + z**2 / (4 * trials**2)) / denominator
        flag_counts.loc[row_index, "flag_rate_lower_95"] = max(0.0, center - half_width)
        flag_counts.loc[row_index, "flag_rate_upper_95"] = min(1.0, center + half_width)
    summary = summary.merge(
        flag_counts.rename(columns={"sum": "flag_count", "count": "replicates"})[
            ["scenario", "flag_count", "flag_rate_lower_95", "flag_rate_upper_95"]
        ],
        on="scenario",
    )

    root = Path(r"D:\PSLV_Reliability")
    final_dir = root / "results" / "final"
    paper_tables = root / "paper" / "tables"
    final_dir.mkdir(parents=True, exist_ok=True)
    paper_tables.mkdir(parents=True, exist_ok=True)
    detail.to_csv(final_dir / "simulation_operating_characteristics_detail.csv", index=False)
    summary.to_csv(final_dir / "simulation_operating_characteristics.csv", index=False)
    summary.to_csv(paper_tables / "simulation_operating_characteristics.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
