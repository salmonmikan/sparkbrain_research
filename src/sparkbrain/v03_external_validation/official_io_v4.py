"""C19 official-v4 IO bridge with unchanged v3 parser/envelope semantics."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.belief_r import BeliefRPair, BeliefRSpec
from sparkbrain.v03_external_validation import official_io_v3 as v3
from sparkbrain.v03_external_validation.official_execution_v4 import RawBundleV4, to_v3_raw

FINAL_SOURCE_INDEX = v3.FINAL_SOURCE_INDEX
FINAL_STEP_INDEX = v3.FINAL_STEP_INDEX
assert_visible_envelope_target_blind = v3.assert_visible_envelope_target_blind
load_verified_official_pairs = v3.load_verified_official_pairs
target_blind_visible_examples = v3.target_blind_visible_examples


def evaluator_targets_after_preservation(
    pairs: Sequence[BeliefRPair],
    raw: RawBundleV4,
) -> tuple[dict[str, Any], ...]:
    return v3.evaluator_targets_after_preservation(pairs, to_v3_raw(raw))


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
