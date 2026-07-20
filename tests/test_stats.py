"""Unit tests for shared statistical helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stats import (
    detect_anomalies,
    eta_squared,
    one_way_anova,
    omega_squared,
    simulate_anova_groups,
    verdict_from_p_and_eta,
)


def test_eta_squared_bounds() -> None:
    assert eta_squared(0.0, 10.0) == 0.0
    assert eta_squared(5.0, 10.0) == pytest.approx(0.5)
    assert eta_squared(1.0, 0.0) == 0.0


def test_omega_squared_non_negative() -> None:
    assert omega_squared(10.0, 2.0, 1.0, 20.0) >= 0.0
    assert omega_squared(0.0, 1.0, 1.0, 0.0) == 0.0


def test_verdict_strong_evidence() -> None:
    text, level = verdict_from_p_and_eta(0.001, 0.20)
    assert level == "strong_evidence"
    assert "Strong" in text


def test_verdict_no_difference() -> None:
    text, level = verdict_from_p_and_eta(0.4, 0.01)
    assert level == "no_visible_difference"
    assert "Without visible" in text


def test_simulate_anova_reproducible() -> None:
    a = simulate_anova_groups(3, 20, mean_diff=2.0, within_sd=0.5, seed=7)
    b = simulate_anova_groups(3, 20, mean_diff=2.0, within_sd=0.5, seed=7)
    assert a.f == pytest.approx(b.f)
    assert a.p == pytest.approx(b.p)
    assert a.ss_between + a.ss_within == pytest.approx(a.ss_total)
    assert a.p < 0.05


def test_one_way_anova_detects_separation() -> None:
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "y": np.concatenate(
                [rng.normal(0, 0.4, 30), rng.normal(2, 0.4, 30), rng.normal(4, 0.4, 30)]
            ),
            "g": ["A"] * 30 + ["B"] * 30 + ["C"] * 30,
        }
    )
    out = one_way_anova(df, "y", "g")
    assert out["p"] < 1e-6
    assert out["eta_sq"] > 0.5
    assert not out["tukey"].empty


def test_detect_anomalies_flags_outlier() -> None:
    df = pd.DataFrame(
        {
            "cell": ["a"] * 10,
            "y": [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.02, 0.98, 1.01, 50.0],
        }
    )
    flagged = detect_anomalies(df, "y", ["cell"], method="mad", threshold=3.5)
    assert flagged["is_anomaly"].iloc[-1]
    assert flagged["is_anomaly"].sum() >= 1
