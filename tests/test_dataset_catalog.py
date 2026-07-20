"""Unit tests for the multi-lab dataset registry."""

from __future__ import annotations

import pytest

from src.dataset_catalog import DATASET_IDS, DATASETS, get_dataset


def test_expected_labs_registered() -> None:
    assert set(DATASET_IDS) == {
        "active_matter",
        "gray_scott",
        "acoustic_scattering",
        "planetary_motion",
    }
    assert set(DATASETS) == set(DATASET_IDS)


@pytest.mark.parametrize("dataset_id", DATASET_IDS)
def test_dataset_spec_fields(dataset_id: str) -> None:
    spec = get_dataset(dataset_id)
    assert spec.id == dataset_id
    assert spec.title
    assert spec.analysis_mode in {"anova", "phase", "interaction", "orbit"}
    assert len(spec.panel_labels) == 3
    assert spec.factor_a and spec.factor_b


def test_unknown_dataset_raises() -> None:
    with pytest.raises(KeyError, match="Unknown dataset_id"):
        get_dataset("not_a_real_lab")
