"""C19-R1 IO bridge.

Official pairs and the target-blind visible envelope are inherited exactly from
C19-v4. Evaluator targets are materialized only after the caller has an
immutable R1 raw preservation boundary.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from typing import Any

from sparkbrain.external_validation.belief_r import BeliefRPair
from sparkbrain.v03_external_validation.c19_r1_revision_authority import RawBundleR1
from sparkbrain.v03_external_validation.c19_r1_scoring import validate_evaluator_targets
from sparkbrain.v03_external_validation.official_io_v4 import (
    FINAL_SOURCE_INDEX,
    FINAL_STEP_INDEX,
    assert_visible_envelope_target_blind,
    load_verified_official_pairs,
    target_blind_visible_examples,
)
from sparkbrain.v03_external_validation.official_protocol_v4 import EXPECTED_PAIRS


def _record_id(pair: BeliefRPair, *, step_index: int) -> str:
    row = pair.time_t if step_index == 0 else pair.time_t1
    return f"{pair.pair_id}:{row.step}"


def evaluator_targets_after_preservation(
    pairs: Sequence[BeliefRPair],
    raw: RawBundleR1,
) -> tuple[dict[str, Any], ...]:
    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError("R1 evaluator target bridge requires exactly 1744 pairs")
    targets = []
    for pair_index, pair in enumerate(pairs):
        record_id = _record_id(pair, step_index=FINAL_STEP_INDEX)
        targets.append(
            {
                "pair_index": pair_index,
                "record_id_hash": hashlib.sha256(record_id.encode("utf-8")).hexdigest(),
                "source_index": FINAL_SOURCE_INDEX,
                "step_index": FINAL_STEP_INDEX,
                "target_choice_id": pair.time_t1.ground_truth,
                "update_required": pair.update_required,
            }
        )
    return validate_evaluator_targets(raw, targets)


__all__ = [
    "assert_visible_envelope_target_blind",
    "evaluator_targets_after_preservation",
    "load_verified_official_pairs",
    "target_blind_visible_examples",
]
