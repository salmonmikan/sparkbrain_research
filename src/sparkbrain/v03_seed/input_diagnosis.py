from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from .text_frontend import (
    compositional_text_features,
    sparse_cosine_similarity,
    whole_string_hash_features,
)

AUTONOMOUS_INPUT_TRACKS = ("I0_whole_hash", "I1_local_compositional")
ORACLE_INPUT_TRACK = "I2_symbolic_oracle"
DEFAULT_INPUT_TRACK = "I1_local_compositional"

_FORBIDDEN_ORACLE_FIELDS = {
    "answer",
    "evaluator",
    "gold",
    "label",
    "split",
    "target",
    "test_only",
    "truth",
}


@dataclass(frozen=True, slots=True)
class InputRecord:
    record_id: str
    text: str
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class FeatureRecord:
    record_id: str
    condition_id: str
    oracle: bool
    features: tuple[tuple[str, float], ...]
    input_bytes: int

    def as_mapping(self) -> dict[str, float]:
        return dict(self.features)

    @property
    def feature_hash(self) -> str:
        payload = json.dumps(self.features, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class PairPrediction:
    pair_id: str
    condition_id: str
    oracle: bool
    expected_relation: str
    predicted_relation: str
    similarity: float
    correct: bool
    left_feature_hash: str
    right_feature_hash: str
    left_feature_count: int
    right_feature_count: int
    shared_feature_count: int
    input_bytes: int


class InputFrontend(Protocol):
    condition_id: str
    oracle: bool

    def encode(self, record: InputRecord) -> FeatureRecord: ...


def _feature_record(
    record: InputRecord,
    *,
    condition_id: str,
    oracle: bool,
    features: Mapping[str, float],
) -> FeatureRecord:
    return FeatureRecord(
        record.record_id,
        condition_id,
        oracle,
        tuple(sorted((str(key), float(value)) for key, value in features.items())),
        len(record.text.encode("utf-8")),
    )


class WholeHashFrontend:
    condition_id = "I0_whole_hash"
    oracle = False

    def __init__(self, *, buckets: int = 128) -> None:
        self.buckets = buckets

    def encode(self, record: InputRecord) -> FeatureRecord:
        return _feature_record(
            record,
            condition_id=self.condition_id,
            oracle=self.oracle,
            features=whole_string_hash_features(record.text, buckets=self.buckets),
        )


class LocalCompositionalFrontend:
    condition_id = "I1_local_compositional"
    oracle = False

    def encode(self, record: InputRecord) -> FeatureRecord:
        return _feature_record(
            record,
            condition_id=self.condition_id,
            oracle=self.oracle,
            features=compositional_text_features(record.text),
        )


def _normalized_key(value: object) -> str:
    return str(value).strip().lower().replace("-", "_")


def _reject_forbidden_fields(value: object, *, path: str = "metadata") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = _normalized_key(key)
            if normalized in _FORBIDDEN_ORACLE_FIELDS:
                raise ValueError(f"forbidden Oracle field at {path}.{key}")
            _reject_forbidden_fields(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_forbidden_fields(child, path=f"{path}[{index}]")


class StrictSymbolicOracleFrontend:
    condition_id = ORACLE_INPUT_TRACK
    oracle = True

    def encode(self, record: InputRecord) -> FeatureRecord:
        if record.metadata is None:
            raise ValueError("structured symbolic_event metadata is required for Oracle mode")
        _reject_forbidden_fields(record.metadata)
        if set(record.metadata) != {"symbolic_event"}:
            raise ValueError("Oracle metadata must contain only symbolic_event")
        event = record.metadata["symbolic_event"]
        if not isinstance(event, Mapping) or set(event) != {"kind", "literal"}:
            raise ValueError("symbolic_event must contain exactly kind and literal")
        if event["kind"] != "literal":
            raise ValueError("C11 Oracle accepts literal events only")
        literal = event["literal"]
        if not isinstance(literal, Mapping):
            raise ValueError("symbolic_event.literal must be a mapping")
        if set(literal) != {"entity", "positive", "predicate"}:
            raise ValueError("literal must contain exactly entity, positive, and predicate")
        predicate = literal["predicate"]
        entity = literal["entity"]
        positive = literal["positive"]
        if not isinstance(predicate, str) or not predicate:
            raise ValueError("literal.predicate must be a non-empty string")
        if not isinstance(entity, str) or not entity:
            raise ValueError("literal.entity must be a non-empty string")
        if not isinstance(positive, bool):
            raise ValueError("literal.positive must be a boolean")
        canonical = json.dumps(
            {"entity": entity, "positive": positive, "predicate": predicate},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        signature = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        features = {
            "sym:kind:literal": 1.0,
            f"sym:predicate:{predicate}": 1.0,
            f"sym:entity:{entity}": 1.0,
            f"sym:positive:{positive}": 1.0,
            f"sym:event-signature:{signature}": 4.0,
        }
        return _feature_record(
            record,
            condition_id=self.condition_id,
            oracle=self.oracle,
            features=features,
        )


def create_frontend(
    condition_id: str = DEFAULT_INPUT_TRACK, *, allow_oracle: bool = False
) -> InputFrontend:
    if condition_id == "I0_whole_hash":
        return WholeHashFrontend()
    if condition_id == "I1_local_compositional":
        return LocalCompositionalFrontend()
    if condition_id == ORACLE_INPUT_TRACK:
        if not allow_oracle:
            raise ValueError("I2_symbolic_oracle is diagnostic-only and disabled by default")
        return StrictSymbolicOracleFrontend()
    raise ValueError(f"unknown input track: {condition_id}")


class FrozenPairEvaluator:
    def __init__(self, *, similarity_threshold: float) -> None:
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be between zero and one")
        self.similarity_threshold = similarity_threshold

    def evaluate(
        self,
        *,
        pair_id: str,
        expected_relation: str,
        left: FeatureRecord,
        right: FeatureRecord,
    ) -> PairPrediction:
        if left.condition_id != right.condition_id or left.oracle != right.oracle:
            raise ValueError("pair features must come from the same input condition")
        if expected_relation not in {"different", "similar"}:
            raise ValueError("expected_relation must be different or similar")
        left_features = left.as_mapping()
        right_features = right.as_mapping()
        similarity = sparse_cosine_similarity(left_features, right_features)
        predicted = "similar" if similarity >= self.similarity_threshold else "different"
        return PairPrediction(
            pair_id,
            left.condition_id,
            left.oracle,
            expected_relation,
            predicted,
            similarity,
            predicted == expected_relation,
            left.feature_hash,
            right.feature_hash,
            len(left.features),
            len(right.features),
            len(set(left_features) & set(right_features)),
            left.input_bytes + right.input_bytes,
        )
