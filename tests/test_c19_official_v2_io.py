from __future__ import annotations

from sparkbrain.external_validation.belief_r import BeliefRPair, BeliefRRow
from sparkbrain.v03_external_validation.official_io_v2 import (
    assert_visible_envelope_target_blind,
    target_blind_visible_examples,
)
from sparkbrain.v03_external_validation.official_protocol_v2 import EXPECTED_PAIRS


def _row(index: int, step: str, truth: str) -> BeliefRRow:
    return BeliefRRow(
        question=f"visible question {index} {step}",
        ground_truth=truth,
        step=step,
        modus="modus",
        relation_type="relation",
        agreement_level="",
        atomic_idx=str(index),
        dataset_id=f"dataset-{index}-{step}",
        choices=("choice-a", "choice-b", "choice-c"),
    )


def _pairs() -> tuple[BeliefRPair, ...]:
    return tuple(
        BeliefRPair(
            pair_id=f"belief_r:{index}:synthetic",
            time_t=_row(index, "time_t", "a"),
            time_t1=_row(index, "time_t1", "b" if index < 1074 else "a"),
        )
        for index in range(EXPECTED_PAIRS)
    )


def test_bound_visible_bridge_is_target_blind_and_step_ordered() -> None:
    examples = target_blind_visible_examples(_pairs())
    assert len(examples) == EXPECTED_PAIRS * 2
    assert_visible_envelope_target_blind(examples)
    expected_fields = {
        "record_id",
        "source_index",
        "pair_index",
        "step_index",
        "question",
        "choices",
    }
    assert all(set(example) == expected_fields for example in examples)
    assert all("ground_truth" not in example for example in examples)
    assert all("update_required" not in example for example in examples)
    assert examples[0]["source_index"] == 0
    assert examples[0]["step_index"] == 0
    assert examples[1]["source_index"] == 1
    assert examples[1]["step_index"] == 1
    assert examples[-1]["pair_index"] == EXPECTED_PAIRS - 1
