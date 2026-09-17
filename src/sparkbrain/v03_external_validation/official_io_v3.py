"""C19 official-v3 IO bridge with unchanged v2 parser/envelope semantics."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.belief_r import BeliefRPair, BeliefRSpec
from sparkbrain.v03_external_validation import official_io_v2 as v2
from sparkbrain.v03_external_validation.official_execution_v3 import RawBundleV3, to_v2_raw

FINAL_SOURCE_INDEX = v2.FINAL_SOURCE_INDEX
FINAL_STEP_INDEX = v2.FINAL_STEP_INDEX
assert_visible_envelope_target_blind = v2.assert_visible_envelope_target_blind
load_verified_official_pairs = v2.load_verified_official_pairs
target_blind_visible_examples = v2.target_blind_visible_examples


def evaluator_targets_after_preservation(
    pairs: Sequence[BeliefRPair],
    raw: RawBundleV3,
) -> tuple[dict[str, Any], ...]:
    return v2.evaluator_targets_after_preservation(pairs, to_v2_raw(raw))


__all__ = [
    "BeliefRPair",
    "BeliefRSpec",
    "FINAL_SOURCE_INDEX",
    "FINAL_STEP_INDEX",
    "Path",
    "assert_visible_envelope_target_blind",
    "evaluator_targets_after_preservation",
    "load_verified_official_pairs",
    "target_blind_visible_examples",
]
