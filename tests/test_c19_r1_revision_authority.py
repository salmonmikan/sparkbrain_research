from __future__ import annotations

import random
from collections import Counter

from sparkbrain.v03_external_validation.c19_r1_protocol import (
    EXPECTED_PAIRS,
    INPUT_TRACK,
    MECHANISM_ID,
    OFFICIAL_SEEDS,
    ROW_KIND,
)
from sparkbrain.v03_external_validation.c19_r1_revision_authority import (
    certainty_tuple,
    revision_authority_executor,
    select_revision_authority,
)
from sparkbrain.v03_external_validation.c19_r1_scoring import (
    atomic_idx_cluster_resample_indices,
)
from sparkbrain.v03_external_validation.c19_r1_source_map import (
    atomic_idx_clusters,
    atomic_idx_source_map_sha256,
    validate_atomic_idx_source_map,
)


def _synthetic_source_map() -> tuple[dict[str, object], ...]:
    return validate_atomic_idx_source_map(
        tuple(
            {"pair_index": pair_index, "atomic_idx": f"atomic-{pair_index // 2}"}
            for pair_index in range(EXPECTED_PAIRS)
        )
    )


def test_revision_wins_exact_certainty_tie() -> None:
    probabilities = {"a": 0.6, "b": 0.3, "c": 0.1}
    selected, chosen, certainty0, certainty1 = select_revision_authority(
        probabilities, probabilities
    )
    assert selected == 1
    assert chosen == probabilities
    assert certainty0 == certainty1


def test_certainty_is_margin_then_top_probability() -> None:
    assert certainty_tuple({"a": 0.5, "b": 0.3, "c": 0.2}) == (0.2, 0.5)


def test_executor_is_target_blind_and_stateless_for_visible_pair() -> None:
    row = {
        "row_id": "unit-r1",
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
    )
    first = revision_authority_executor(row, examples)
    second = revision_authority_executor(row, examples)
    assert first == second
    assert len(first) == 1
    emitted = first[0]
    assert set(emitted) == {"record_id", "source_index", "pair_index", "prediction", "metadata"}
    assert emitted["record_id"] == "unit:1"
    assert emitted["source_index"] == 1
    assert emitted["pair_index"] == 0
    metadata = emitted["metadata"]
    assert metadata["input_track"] == INPUT_TRACK
    assert metadata["selected_visible_step"] in (0, 1)
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


def test_cluster_resample_carries_whole_atomic_clusters_at_same_multiplicity() -> None:
    source_map = _synthetic_source_map()
    sampled = atomic_idx_cluster_resample_indices(source_map, random.Random(19901))
    counts = Counter(sampled)
    for _, pair_indices in atomic_idx_clusters(source_map):
        multiplicities = {counts[pair_index] for pair_index in pair_indices}
        assert len(multiplicities) == 1
