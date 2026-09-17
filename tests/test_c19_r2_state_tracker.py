from __future__ import annotations

import random
from collections import Counter

from sparkbrain.v03_external_validation.c19_r2_protocol import (
    EXPECTED_PAIRS,
    INPUT_TRACK,
    MECHANISM_ID,
    OFFICIAL_SEEDS,
    ROW_KIND,
    load_and_validate_contract,
)
from sparkbrain.v03_external_validation.c19_r2_scoring import (
    atomic_idx_cluster_resample_indices,
    linear_quantile_10k,
)
from sparkbrain.v03_external_validation.c19_r2_source_map import (
    atomic_idx_clusters,
    atomic_idx_source_map_sha256,
    validate_atomic_idx_source_map,
)
from sparkbrain.v03_external_validation.c19_r2_state_tracker import (
    observe,
    readout,
    state_tracker_executor,
    transition,
)


def _synthetic_source_map() -> tuple[dict[str, object], ...]:
    return validate_atomic_idx_source_map(
        tuple(
            {"pair_index": pair_index, "atomic_idx": f"atomic-{pair_index // 2}"}
            for pair_index in range(EXPECTED_PAIRS)
        )
    )


def test_preformal_contract_has_no_identity_or_execution_authority() -> None:
    result = load_and_validate_contract()
    assert result["formal_identity"] is None
    assert result["official_execution_allowed"] is False
    assert result["status"] == "preformal_contract_checks_pass"


def test_frozen_observation_and_transition_golden_table() -> None:
    assert observe({"a": 0.5, "b": 0.3, "c": 0.2}) == ("a", True)
    assert observe({"a": 0.4, "b": 0.35, "c": 0.25}) == ("a", False)
    assert transition("RESET", {"a": 0.5, "b": 0.3, "c": 0.2}) == "A_STRONG"
    assert transition("A_STRONG", {"a": 0.4, "b": 0.35, "c": 0.25}) == "A_STRONG"
    assert transition("A_STRONG", {"a": 0.3, "b": 0.4, "c": 0.3}) == "A_WEAK"
    assert transition("A_WEAK", {"a": 0.3, "b": 0.4, "c": 0.3}) == "B_WEAK"
    assert transition("A_WEAK", {"a": 0.2, "b": 0.6, "c": 0.2}) == "B_STRONG"
    assert readout("B_WEAK") == "b"


def test_executor_is_deterministic_target_blind_and_pair_reset() -> None:
    row = {
        "row_id": "unit-r2",
        "row_kind": ROW_KIND,
        "mechanism_id": MECHANISM_ID,
        "input_track": INPUT_TRACK,
        "seed": OFFICIAL_SEEDS[0],
    }
    examples = (
        {
            "record_id": "unit:0",
            "source_index": 0,
            "pair_index": 0,
            "step_index": 0,
            "question": "Visible premise alpha. What necessarily had to follow?",
            "choices": ("A", "B", "C"),
        },
        {
            "record_id": "unit:1",
            "source_index": 1,
            "pair_index": 0,
            "step_index": 1,
            "question": "Visible revised premise beta. What necessarily had to follow?",
            "choices": ("A", "B", "C"),
        },
        {
            "record_id": "unit:2",
            "source_index": 0,
            "pair_index": 1,
            "step_index": 0,
            "question": "Visible premise gamma. What necessarily had to follow?",
            "choices": ("A", "B", "C"),
        },
        {
            "record_id": "unit:3",
            "source_index": 1,
            "pair_index": 1,
            "step_index": 1,
            "question": "Visible revised premise delta. What necessarily had to follow?",
            "choices": ("A", "B", "C"),
        },
    )
    first = state_tracker_executor(row, examples)
    second = state_tracker_executor(row, examples)
    assert first == second
    assert len(first) == 2
    for emitted in first:
        assert set(emitted) == {
            "record_id",
            "source_index",
            "pair_index",
            "prediction",
            "metadata",
        }
        metadata = emitted["metadata"]
        assert metadata["state_trace"][0] == "RESET"
        assert len(metadata["state_trace"]) == 3
        assert metadata["work_counters"]["encodings"] == 2
        assert metadata["work_counters"]["projection_passes"] == 2
        forbidden = {"ground_truth", "target", "label", "update_required", "correct"}
        assert forbidden.isdisjoint(emitted)
        assert forbidden.isdisjoint(metadata)


def test_atomic_idx_source_map_is_total_deterministic_and_target_free() -> None:
    source_map = _synthetic_source_map()
    assert len(source_map) == EXPECTED_PAIRS
    assert all(set(entry) == {"pair_index", "atomic_idx"} for entry in source_map)
    assert atomic_idx_source_map_sha256(source_map) == atomic_idx_source_map_sha256(
        tuple(dict(entry) for entry in source_map)
    )
    clusters = atomic_idx_clusters(source_map)
    assert sum(len(indices) for _, indices in clusters) == EXPECTED_PAIRS
    assert len(clusters) == EXPECTED_PAIRS // 2


def test_cluster_resample_carries_whole_clusters_at_same_multiplicity() -> None:
    source_map = _synthetic_source_map()
    sampled = atomic_idx_cluster_resample_indices(source_map, random.Random(19901))
    counts = Counter(sampled)
    for _, pair_indices in atomic_idx_clusters(source_map):
        multiplicities = {counts[pair_index] for pair_index in pair_indices}
        assert len(multiplicities) == 1


def test_type7_quantile_semantics_are_frozen() -> None:
    values = tuple(float(index) for index in range(10_000))
    assert linear_quantile_10k(values, 0.025) == 249.975
    assert linear_quantile_10k(values, 0.975) == 9749.025
