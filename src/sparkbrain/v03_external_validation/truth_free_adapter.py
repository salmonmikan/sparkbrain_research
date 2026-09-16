"""Prospective, target-blind C19-v2 Belief-R surface adapter.

This module is readiness-only. It has no dataset loader and accepts only the
backend-visible surface envelope explicitly preregistered for C19-v2.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass

from sparkbrain.v03_seed.input_diagnosis import (
    FeatureRecord,
    InputRecord,
    LocalCompositionalFrontend,
    WholeHashFrontend,
)

ADAPTER_CONTRACT_ID = "c19-belief-r-truth-free-symbolic-adapter-v1"
PROTOCOL_ID = "c19-external-v2"
PLANNED_OFFICIAL_IDENTITY = "c19-external-v2-official-v1"
CONDITION_ID = "I2_truth_free_symbolic_surface"
QUERY_MARKER = "What necessarily had to follow"

_SENTENCE_BOUNDARY = re.compile(r"[.!?]+")
_WHITESPACE = re.compile(r"\s+")
_CHOICE_NAMES = ("a", "b", "c")


@dataclass(frozen=True, slots=True)
class TruthFreeBeliefRInput:
    """The complete C19-v2 adapter input boundary.

    No benchmark semantic metadata or evaluator Target is accepted by this API.
    """

    record_id: str
    source_index: int
    step_index: int
    question: str
    choices: tuple[str, str, str]

    def validate(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        for name in ("source_index", "step_index"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer")
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("question must be a non-empty string")
        if self.question.count(QUERY_MARKER) != 1:
            raise ValueError("question must contain the registered query marker exactly once")
        if not isinstance(self.choices, tuple) or len(self.choices) != 3:
            raise ValueError("choices must be an ordered three-string tuple")
        if any(
            not isinstance(choice, str) or not choice.strip() for choice in self.choices
        ):
            raise ValueError("choices must contain three non-empty strings")


def normalize_surface(value: str) -> str:
    """Normalize visible surface text without inferring semantics."""

    return _WHITESPACE.sub(" ", unicodedata.normalize("NFKC", value).casefold()).strip()


def canonical_visible_envelope(value: TruthFreeBeliefRInput) -> str:
    """Return the exact data-matched envelope supplied to every autonomous condition."""

    value.validate()
    choices = {
        name: choice for name, choice in zip(_CHOICE_NAMES, value.choices, strict=True)
    }
    payload = {
        "choices": choices,
        "question": value.question,
        "source_index": value.source_index,
        "step_index": value.step_index,
    }
    return json.dumps(
        payload,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def surface_events(value: TruthFreeBeliefRInput) -> tuple[tuple[str, int, str], ...]:
    """Parse only surface roles/order from the allowed visible envelope."""

    value.validate()
    premise_prefix, marker, _query_tail = value.question.partition(QUERY_MARKER)
    if not marker:
        raise ValueError("registered query marker is missing")
    normalized_prefix = normalize_surface(premise_prefix)
    premises = tuple(
        normalized
        for segment in _SENTENCE_BOUNDARY.split(normalized_prefix)
        if (normalized := normalize_surface(segment))
    )
    if not premises:
        raise ValueError("question must contain at least one premise before the query marker")

    events: list[tuple[str, int, str]] = [
        ("source_index", 0, str(value.source_index)),
        ("step_index", 0, str(value.step_index)),
        ("query_marker", 0, normalize_surface(QUERY_MARKER)),
    ]
    events.extend(("premise", index, premise) for index, premise in enumerate(premises))
    events.extend(
        ("choice", index, normalize_surface(choice))
        for index, choice in enumerate(value.choices)
    )
    return tuple(events)


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class BeliefRTruthFreeSymbolicAdapter:
    """Map the visible C19-v2 envelope to role-qualified surface features."""

    condition_id = CONDITION_ID
    oracle = False
    contract_id = ADAPTER_CONTRACT_ID

    def encode(self, value: TruthFreeBeliefRInput) -> FeatureRecord:
        envelope = canonical_visible_envelope(value)
        events = surface_events(value)
        features: dict[str, float] = {
            f"c19tf:contract:{ADAPTER_CONTRACT_ID}": 1.0,
            f"c19tf:event-count:{len(events)}": 1.0,
        }
        for role, ordinal, surface in events:
            digest = _fingerprint(surface)
            features[f"c19tf:{role}:{ordinal}:{digest}"] = 1.0
        return FeatureRecord(
            record_id=value.record_id,
            condition_id=self.condition_id,
            oracle=self.oracle,
            features=tuple(sorted(features.items())),
            input_bytes=len(envelope.encode("utf-8")),
        )


def whole_hash_visible_input(value: TruthFreeBeliefRInput) -> FeatureRecord:
    """I0 control on the same visible C19-v2 envelope."""

    envelope = canonical_visible_envelope(value)
    return WholeHashFrontend().encode(InputRecord(value.record_id, envelope))


def compositional_visible_input(value: TruthFreeBeliefRInput) -> FeatureRecord:
    """I1 control on the same visible C19-v2 envelope."""

    envelope = canonical_visible_envelope(value)
    return LocalCompositionalFrontend().encode(InputRecord(value.record_id, envelope))


def static_representation_audit(value: TruthFreeBeliefRInput) -> dict[str, object]:
    """Return source-level admission facts without reading official data."""

    adapter = BeliefRTruthFreeSymbolicAdapter().encode(value)
    i0 = whole_hash_visible_input(value)
    i1 = compositional_visible_input(value)
    return {
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "condition_id": CONDITION_ID,
        "oracle": adapter.oracle,
        "same_visible_input_bytes": adapter.input_bytes == i0.input_bytes == i1.input_bytes,
        "exact_feature_equivalent_to_i0": adapter.features == i0.features,
        "exact_feature_equivalent_to_i1": adapter.features == i1.features,
        "source_index": value.source_index,
        "step_index": value.step_index,
    }
