"""Bound Belief-R input/evaluator bridge for the C19 official-v2 run.

Model-side examples contain only the visible question/choices envelope. Evaluator
truth is materialized separately and only after the caller has preserved raw.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.belief_r import (
    BeliefRPair,
    BeliefRSpec,
    iter_belief_r_pairs,
    load_belief_r_spec,
    verify_belief_r_cache,
)
from sparkbrain.v03_external_validation.official_execution_v2 import RawBundleV2
from sparkbrain.v03_external_validation.official_protocol_v2 import EXPECTED_PAIRS
from sparkbrain.v03_external_validation.official_scoring_v2 import (
    validate_evaluator_targets,
)

FINAL_SOURCE_INDEX = 1
FINAL_STEP_INDEX = 1


def _record_id(pair: BeliefRPair, *, step_index: int) -> str:
    row = pair.time_t if step_index == 0 else pair.time_t1
    return f"{pair.pair_id}:{row.step}"


def load_verified_official_pairs(
    cache_path: Path, spec_path: Path
) -> tuple[BeliefRSpec, tuple[BeliefRPair, ...]]:
    """Verify the pinned cache and return its exact deterministic pair ordering."""

    spec = load_belief_r_spec(spec_path)
    verification = verify_belief_r_cache(cache_path, spec)
    if verification.pair_count != EXPECTED_PAIRS:
        raise ValueError("verified Belief-R pair count differs from C19-v2 contract")
    pairs = tuple(iter_belief_r_pairs(cache_path, spec))
    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError("materialized Belief-R pair count differs from C19-v2 contract")
    return spec, pairs


def target_blind_visible_examples(
    pairs: Sequence[BeliefRPair],
) -> tuple[dict[str, object], ...]:
    """Project parsed official pairs into the exact model-visible envelope."""

    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError("C19-v2 visible envelope requires exactly 1744 pairs")
    examples: list[dict[str, object]] = []
    for pair_index, pair in enumerate(pairs):
        for step_index, row in enumerate((pair.time_t, pair.time_t1)):
            examples.append(
                {
                    "record_id": _record_id(pair, step_index=step_index),
                    "source_index": step_index,
                    "pair_index": pair_index,
                    "step_index": step_index,
                    "question": row.question,
                    "choices": tuple(row.choices),
                }
            )
    return tuple(examples)


def evaluator_targets_after_preservation(
    pairs: Sequence[BeliefRPair],
    raw: RawBundleV2,
) -> tuple[dict[str, Any], ...]:
    """Create evaluator-only targets and prove their unique/total raw join."""

    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError("C19-v2 evaluator target bridge requires exactly 1744 pairs")
    targets: list[dict[str, Any]] = []
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
    validated = validate_evaluator_targets(raw, targets)
    return tuple(dict(target) for target in validated)


def assert_visible_envelope_target_blind(
    examples: Iterable[Mapping[str, object]],
) -> None:
    """Fail closed if evaluator-owned fields enter a model-side example."""

    allowed = {
        "record_id",
        "source_index",
        "pair_index",
        "step_index",
        "question",
        "choices",
    }
    forbidden = {"ground_truth", "target_choice_id", "update_required", "truth", "label"}
    for example in examples:
        if set(example) != allowed:
            raise ValueError("model-visible example fields differ from frozen C19-v2 envelope")
        if forbidden.intersection(example):
            raise ValueError("evaluator-owned target field leaked into model-visible envelope")
