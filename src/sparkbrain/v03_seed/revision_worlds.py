from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any

from .contracts import EvidenceRecord
from .evidence import EvidenceLedger

C15_SCHEMA_VERSION = "0.3"
C15_E0_GLOBAL = "E0_global"
C15_E1_ORACLE_ENTITY = "E1_oracle_entity"
BELIEF_ORDER = ("alpha", "beta", "gamma")
WORLD_ORDER = ("maintain", "update", "recover", "insufficient")
VARIANT_ORDER = (
    "base",
    "irrelevant_distractor",
    "same_id_duplicate",
    "correlated_copy",
)

_SPLIT_CONFIG = {
    "train": (153_000, 16),
    "dev": (253_000, 8),
    "test": (453_000, 8),
}
EXPECTED_SPLIT_MANIFEST_SHA256 = {
    "dev": "e4f7cc4ab4c2fa5c81a6d17c927424a3575431f0a6578ab87146c130ab87d6f7",
    "test": "66d580f4e63a55f4a26441709caf8b443bfe701fdac548ff22867a60b7a31cf6",
    "train": "bfd3e031edcc9d0c23a55bac1f5797420f1f85d7fca0a0e689ca4ff414fc3266",
}
EXPECTED_FULL_FIXTURE_SHA256 = {
    "dev": "8cec9458524b467c54927ba46a3055754e59aa531de21d8a8037bec993c04589",
    "test": "cd27e177476f5c0adba37bf7c4e5284996f6155dd4d61ed1547be2bf1a7051c6",
    "train": "4bb90acded764199b912b712becc16252c791086dbddc9f80259dd99de5ea455",
}

_STAGE_SPECS = {
    "establish_A": ((0, "A", "support", 1.0), (1, "A", "support", 0.9)),
    "establish_B_contradict_A": (
        (0, "B", "support", 1.0),
        (1, "B", "support", 0.9),
        (2, "A", "contradict", 0.85),
        (3, "A", "contradict", 0.8),
    ),
    "maintain_A": ((0, "A", "support", 1.0), (1, "A", "support", 0.9)),
    "recover_A_contradict_B": (
        (0, "A", "support", 1.0),
        (1, "A", "support", 0.9),
        (2, "B", "contradict", 0.85),
        (3, "B", "contradict", 0.8),
    ),
    "insufficient_A": ((0, "A", "support", 0.35),),
}
_WORLD_SEQUENCES = {
    "maintain": (("establish_A",), "maintain_A", "A", True, "A", "maintain"),
    "update": (
        ("establish_A",),
        "establish_B_contradict_A",
        "A",
        True,
        "B",
        "update",
    ),
    "recover": (
        ("establish_A", "establish_B_contradict_A"),
        "recover_A_contradict_B",
        "B",
        True,
        "A",
        "recover",
    ),
    "insufficient": (
        ("establish_A",),
        "insufficient_A",
        "A",
        False,
        "A",
        "insufficient_information",
    ),
}


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def _digest16(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_split(split: str) -> tuple[int, int]:
    if split not in _SPLIT_CONFIG:
        raise ValueError("split must be train, dev, or test")
    return _SPLIT_CONFIG[split]


@dataclass(frozen=True, slots=True)
class SplitManifestRow:
    episode_id: str
    episode_seed: int
    family_id: str
    world: str

    def to_dict(self) -> dict[str, object]:
        return {
            "episode_id": self.episode_id,
            "episode_seed": self.episode_seed,
            "family_id": self.family_id,
            "world": self.world,
        }


@dataclass(frozen=True, slots=True)
class FixtureEvidence:
    correlation_group: str
    entity_key: str
    evidence_id: str
    hypothesis_id: str
    polarity: str
    source_id: str
    strength: float
    time: float

    def validate(self) -> None:
        for value in (
            self.correlation_group,
            self.entity_key,
            self.evidence_id,
            self.hypothesis_id,
            self.source_id,
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("fixture evidence IDs must be non-empty strings")
        if self.polarity not in {"support", "contradict"}:
            raise ValueError("fixture evidence polarity must be support or contradict")
        if (
            isinstance(self.strength, bool)
            or not isinstance(self.strength, (int, float))
            or not math.isfinite(self.strength)
            or self.strength < 0
        ):
            raise ValueError("fixture evidence strength must be finite and non-negative")
        if (
            isinstance(self.time, bool)
            or not isinstance(self.time, (int, float))
            or not math.isfinite(self.time)
            or self.time < 0
        ):
            raise ValueError("fixture evidence time must be finite and non-negative")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "correlation_group": self.correlation_group,
            "entity_key": self.entity_key,
            "evidence_id": self.evidence_id,
            "hypothesis_id": self.hypothesis_id,
            "polarity": self.polarity,
            "source_id": self.source_id,
            "strength": self.strength,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, value: object) -> FixtureEvidence:
        expected = {
            "correlation_group",
            "entity_key",
            "evidence_id",
            "hypothesis_id",
            "polarity",
            "source_id",
            "strength",
            "time",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("fixture evidence has unexpected fields")
        row = cls(**value)
        row.validate()
        return row


@dataclass(frozen=True, slots=True)
class FixtureVariant:
    assessment_deliveries: tuple[FixtureEvidence, ...]
    attribution_targets: tuple[str, ...]
    variant_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "assessment_deliveries": [row.to_dict() for row in self.assessment_deliveries],
            "attribution_targets": list(self.attribution_targets),
            "variant_id": self.variant_id,
        }


@dataclass(frozen=True, slots=True)
class RevisionFixtureEpisode:
    context_stages: tuple[tuple[FixtureEvidence, ...], ...]
    entity_key: str
    episode_id: str
    episode_seed: int
    family_id: str
    previous_truth: str
    sufficient_information: bool
    target_truth: str
    transition_target: str
    variants: tuple[FixtureVariant, ...]
    world: str

    def to_dict(self) -> dict[str, object]:
        return {
            "context_stages": [
                [evidence.to_dict() for evidence in stage] for stage in self.context_stages
            ],
            "entity_key": self.entity_key,
            "episode_id": self.episode_id,
            "episode_seed": self.episode_seed,
            "family_id": self.family_id,
            "previous_truth": self.previous_truth,
            "sufficient_information": self.sufficient_information,
            "target_truth": self.target_truth,
            "transition_target": self.transition_target,
            "variants": [variant.to_dict() for variant in self.variants],
            "world": self.world,
        }


def build_split_manifest(split: str) -> tuple[SplitManifestRow, ...]:
    base, fixtures_per_world = _require_split(split)
    rows: list[SplitManifestRow] = []
    for world_index, world in enumerate(WORLD_ORDER):
        for index in range(fixtures_per_world):
            episode_seed = base + 100 * world_index + index
            family_id = f"fam-{_digest16(f'c15v4-family|{split}|{world}|{index}')}"
            episode_id = (
                "ep-"
                + _digest16(
                    f"c15v4-episode|{split}|{world}|{index}|{episode_seed}"
                )
            )
            rows.append(SplitManifestRow(episode_id, episode_seed, family_id, world))
    return tuple(rows)


def canonical_split_manifest_json(split: str) -> bytes:
    return canonical_json_bytes(
        {
            "rows": [row.to_dict() for row in build_split_manifest(split)],
            "schema_version": C15_SCHEMA_VERSION,
            "split": split,
        }
    )


def split_manifest_sha256(split: str) -> str:
    return _sha256(canonical_split_manifest_json(split))


def _belief_assignment(episode_seed: int) -> dict[str, str]:
    return {
        "A": BELIEF_ORDER[episode_seed % 3],
        "B": BELIEF_ORDER[(episode_seed + 1) % 3],
        "C": BELIEF_ORDER[(episode_seed + 2) % 3],
    }


def _make_evidence(
    *,
    family_id: str,
    entity_key: str,
    hypothesis_id: str,
    polarity: str,
    strength: float,
    stage: int,
    slot: int,
) -> FixtureEvidence:
    source_id = f"src-{_digest16(f'c15v4-source|{family_id}|{stage}|{slot}')}"
    group_id = f"grp-{_digest16(f'c15v4-group|{family_id}|{stage}|{slot}')}"
    body: dict[str, object] = {
        "correlation_group": group_id,
        "entity_key": entity_key,
        "hypothesis_id": hypothesis_id,
        "polarity": polarity,
        "source_id": source_id,
        "strength": strength,
        "time": float(stage * 10 + slot),
    }
    evidence_id = f"ev-{_digest16('c15v4-evidence|' + canonical_json_bytes(body).decode())}"
    return FixtureEvidence(evidence_id=evidence_id, **body)  # type: ignore[arg-type]


def _make_stage(
    name: str,
    *,
    stage: int,
    family_id: str,
    entity_key: str,
    beliefs: dict[str, str],
) -> tuple[FixtureEvidence, ...]:
    return tuple(
        _make_evidence(
            family_id=family_id,
            entity_key=entity_key,
            hypothesis_id=beliefs[symbol],
            polarity=polarity,
            strength=strength,
            stage=stage,
            slot=slot,
        )
        for slot, symbol, polarity, strength in _STAGE_SPECS[name]
    )


def _build_episode(row: SplitManifestRow) -> RevisionFixtureEpisode:
    beliefs = _belief_assignment(row.episode_seed)
    entity_key = f"ent-{_digest16('c15v4-entity|' + row.family_id)}"
    context_names, assessment_name, previous, sufficient, target, transition = (
        _WORLD_SEQUENCES[row.world]
    )
    context = tuple(
        _make_stage(
            name,
            stage=stage,
            family_id=row.family_id,
            entity_key=entity_key,
            beliefs=beliefs,
        )
        for stage, name in enumerate(context_names)
    )
    assessment = _make_stage(
        assessment_name,
        stage=2,
        family_id=row.family_id,
        entity_key=entity_key,
        beliefs=beliefs,
    )
    attribution_targets = tuple(
        evidence.evidence_id
        for evidence in assessment
        if evidence.hypothesis_id == beliefs[target] and evidence.polarity == "support"
    )
    variants: list[FixtureVariant] = []
    for variant_id in VARIANT_ORDER:
        deliveries = list(assessment)
        if variant_id == "irrelevant_distractor":
            deliveries.append(
                _make_evidence(
                    family_id=row.family_id,
                    entity_key=entity_key,
                    hypothesis_id=beliefs["C"],
                    polarity="support",
                    strength=0.25,
                    stage=2,
                    slot=4,
                )
            )
        elif variant_id == "same_id_duplicate":
            deliveries.append(assessment[0])
        elif variant_id == "correlated_copy":
            original = assessment[0]
            deliveries.append(
                FixtureEvidence(
                    correlation_group=original.correlation_group,
                    entity_key=original.entity_key,
                    evidence_id=(
                        "ev-"
                        + _digest16("c15v4-correlated|" + original.evidence_id)
                    ),
                    hypothesis_id=original.hypothesis_id,
                    polarity=original.polarity,
                    source_id=original.source_id,
                    strength=original.strength,
                    time=original.time,
                )
            )
        variants.append(FixtureVariant(tuple(deliveries), attribution_targets, variant_id))
    return RevisionFixtureEpisode(
        context_stages=context,
        entity_key=entity_key,
        episode_id=row.episode_id,
        episode_seed=row.episode_seed,
        family_id=row.family_id,
        previous_truth=beliefs[previous],
        sufficient_information=sufficient,
        target_truth=beliefs[target],
        transition_target=transition,
        variants=tuple(variants),
        world=row.world,
    )


def build_full_fixture(split: str) -> tuple[RevisionFixtureEpisode, ...]:
    _require_split(split)
    return tuple(_build_episode(row) for row in build_split_manifest(split))


def canonical_full_fixture_json(split: str) -> bytes:
    return canonical_json_bytes(
        {
            "episodes": [episode.to_dict() for episode in build_full_fixture(split)],
            "schema_version": C15_SCHEMA_VERSION,
            "split": split,
        }
    )


def full_fixture_sha256(split: str) -> str:
    return _sha256(canonical_full_fixture_json(split))


def adapt_fixture_evidence_id(evidence_id: str, *, entity_condition: str) -> str:
    if not isinstance(evidence_id, str) or not evidence_id.strip():
        raise ValueError("evidence_id must be a non-empty string")
    if entity_condition == C15_E1_ORACLE_ENTITY:
        return evidence_id
    if entity_condition == C15_E0_GLOBAL:
        return f"ev-{_digest16('c15v4-e0|' + evidence_id)}"
    raise ValueError("entity_condition must be E0_global or E1_oracle_entity")


def adapt_fixture_entity_key(entity_key: str, *, entity_condition: str) -> str:
    if not isinstance(entity_key, str) or not entity_key.strip():
        raise ValueError("entity_key must be a non-empty string")
    if entity_condition == C15_E1_ORACLE_ENTITY:
        return entity_key
    if entity_condition == C15_E0_GLOBAL:
        return "__global__"
    raise ValueError("entity_condition must be E0_global or E1_oracle_entity")


def map_attribution_target_ids(
    evidence_ids: tuple[str, ...], *, entity_condition: str
) -> tuple[str, ...]:
    if not isinstance(evidence_ids, tuple):
        raise ValueError("attribution target IDs must be a tuple")
    return tuple(
        adapt_fixture_evidence_id(evidence_id, entity_condition=entity_condition)
        for evidence_id in evidence_ids
    )


def fixture_lineage_ids(
    evidence_id: str, *, entity_condition: str
) -> tuple[str, str]:
    adapted_evidence_id = adapt_fixture_evidence_id(
        evidence_id, entity_condition=entity_condition
    )
    return (
        f"sa-{_digest16('c15v4-sample|' + adapted_evidence_id)}",
        f"sp-{_digest16('c15v4-spark|' + adapted_evidence_id)}",
    )


def fixture_evidence_to_record(
    evidence: FixtureEvidence, *, entity_condition: str
) -> EvidenceRecord:
    """Apply the frozen C15 lineage adapter without changing fixture identity."""

    evidence.validate()
    adapted_evidence_id = adapt_fixture_evidence_id(
        evidence.evidence_id, entity_condition=entity_condition
    )
    adapted_entity_key = adapt_fixture_entity_key(
        evidence.entity_key, entity_condition=entity_condition
    )
    _, spark_id = fixture_lineage_ids(
        evidence.evidence_id, entity_condition=entity_condition
    )
    record = EvidenceRecord(
        correlation_group=evidence.correlation_group,
        entity_key=adapted_entity_key,
        evidence_id=adapted_evidence_id,
        hypothesis_id=evidence.hypothesis_id,
        metadata={},
        parent_evidence_ids=(),
        parent_spark_ids=(spark_id,),
        polarity=evidence.polarity,
        schema_version=C15_SCHEMA_VERSION,
        source_id=evidence.source_id,
        strength=evidence.strength,
        time=evidence.time,
    )
    record.validate()
    return record


def add_fixture_evidence(
    ledger: EvidenceLedger,
    evidence: FixtureEvidence,
    *,
    entity_condition: str,
    seen_evidence_ids: set[str],
) -> EvidenceRecord:
    """Register lineage once, then preserve exact same-ID redelivery as a ledger no-op."""

    record = fixture_evidence_to_record(
        evidence, entity_condition=entity_condition
    )
    if record.evidence_id not in seen_evidence_ids:
        sample_id, spark_id = fixture_lineage_ids(
            evidence.evidence_id, entity_condition=entity_condition
        )
        ledger.register_sample(sample_id)
        ledger.register_spark(spark_id, (sample_id,))
        seen_evidence_ids.add(record.evidence_id)
    ledger.add(record)
    return record


def assert_frozen_fixture_hashes() -> None:
    for split in _SPLIT_CONFIG:
        if split_manifest_sha256(split) != EXPECTED_SPLIT_MANIFEST_SHA256[split]:
            raise ValueError(f"C15 {split} split manifest hash mismatch")
        if full_fixture_sha256(split) != EXPECTED_FULL_FIXTURE_SHA256[split]:
            raise ValueError(f"C15 {split} full fixture hash mismatch")


def fixture_document(split: str) -> dict[str, Any]:
    """Return the exact evaluator document, never a production observation."""

    return json.loads(canonical_full_fixture_json(split))
