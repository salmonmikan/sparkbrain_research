from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from .contracts import SENSORY_CONTRACT_VERSION, EntityBinding, PerceptualSpark

E0_GLOBAL = "I2_symbolic_oracle__G0_probability__E0_global"
E1_ORACLE_ENTITY = "I2_symbolic_oracle__G0_probability__E1_oracle_entity"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def derive_binding_id(
    *,
    parent_spark_id: str,
    entity_hint: str | None,
    entity_slot: str | None,
    assignment_status: str,
) -> str:
    payload = _canonical_json(
        [
            SENSORY_CONTRACT_VERSION,
            parent_spark_id,
            entity_hint,
            entity_slot,
            assignment_status,
        ]
    )
    return f"bind-{hashlib.sha256(payload.encode()).hexdigest()}"


def bind_entity(
    spark: PerceptualSpark,
    *,
    condition_id: str,
    entity_hint: str | None,
) -> EntityBinding:
    spark.validate()
    if condition_id == E0_GLOBAL:
        entity_key = "__global__"
        status = "assigned"
        confidence = 1.0
    elif condition_id == E1_ORACLE_ENTITY:
        if not spark.entity_slot:
            raise ValueError("E1 oracle entity requires a nonempty perceptual entity_slot")
        entity_key = spark.entity_slot
        status = "assigned"
        confidence = 1.0
    else:
        raise ValueError("C13 permits only condition-separated E0 and E1 binding")
    binding = EntityBinding(
        binding_id=derive_binding_id(
            parent_spark_id=spark.spark_id,
            entity_hint=entity_hint,
            entity_slot=spark.entity_slot,
            assignment_status=status,
        ),
        entity_hint=entity_hint,
        entity_slot=spark.entity_slot,
        entity_key=entity_key,
        assignment_status=status,
        confidence=confidence,
        time=spark.time,
        parent_spark_id=spark.spark_id,
    )
    binding.validate()
    return binding


class LearnedSlotBinder(Protocol):
    """Exchangeable C13 interface only; E2 implementation/execution is forbidden."""

    def assign(self, spark: PerceptualSpark) -> EntityBinding: ...


@dataclass(frozen=True, slots=True)
class SlotMetricRow:
    sequence: int
    predicted_slot: str | None
    oracle_entity: str
    assignment_status: str

    def validate(self) -> None:
        if self.sequence < 0 or not self.oracle_entity:
            raise ValueError("slot metric sequence and oracle entity are required")
        if self.assignment_status not in {"assigned", "unassigned", "uncertain"}:
            raise ValueError("invalid slot assignment status")
        if self.assignment_status == "assigned" and not self.predicted_slot:
            raise ValueError("assigned slot row requires predicted_slot")
        if self.assignment_status != "assigned" and self.predicted_slot is not None:
            raise ValueError("non-assigned slot row cannot set predicted_slot")


def permutation_invariant_slot_metrics(rows: Iterable[SlotMetricRow]) -> dict[str, object]:
    ordered = sorted(rows, key=lambda row: row.sequence)
    if len({row.sequence for row in ordered}) != len(ordered):
        raise ValueError("slot metric sequences must be unique")
    for row in ordered:
        row.validate()
    total = len(ordered)
    assigned = [row for row in ordered if row.assignment_status == "assigned"]
    predicted = sorted({row.predicted_slot for row in assigned if row.predicted_slot is not None})
    entities = sorted({row.oracle_entity for row in assigned})
    size = max(len(predicted), len(entities))
    padded_predicted = predicted + [
        f"~dummy-predicted-{index}" for index in range(size - len(predicted))
    ]
    padded_entities = entities + [f"~dummy-entity-{index}" for index in range(size - len(entities))]
    contingency = {
        (slot, entity): sum(
            1
            for row in assigned
            if row.predicted_slot == slot and row.oracle_entity == entity
        )
        for slot in padded_predicted
        for entity in padded_entities
    }
    candidates: list[tuple[int, tuple[tuple[str, str], ...]]] = []
    for permutation in itertools.permutations(padded_entities):
        mapping = tuple(zip(padded_predicted, permutation, strict=True))
        weight = sum(contingency[pair] for pair in mapping)
        candidates.append((weight, mapping))
    maximum = max((item[0] for item in candidates), default=0)
    best_mapping = (
        min(mapping for weight, mapping in candidates if weight == maximum)
        if candidates
        else ()
    )
    best_weight = maximum
    mapping_dict = dict(best_mapping)

    switch_numerator = 0
    switch_denominator = 0
    previous_by_entity: dict[str, str] = {}
    for row in assigned:
        mapped = mapping_dict[row.predicted_slot]
        previous = previous_by_entity.get(row.oracle_entity)
        if previous is not None:
            switch_denominator += 1
            switch_numerator += int(previous != mapped)
        previous_by_entity[row.oracle_entity] = mapped
    assigned_count = len(assigned)
    unassigned_count = sum(row.assignment_status == "unassigned" for row in ordered)
    uncertain_count = sum(row.assignment_status == "uncertain" for row in ordered)
    return {
        "assigned_coverage": assigned_count / total if total else 0.0,
        "assigned_count": assigned_count,
        "eligible_count": total,
        "matched_accuracy": best_weight / assigned_count if assigned_count else 0.0,
        "matched_count": best_weight,
        "matching": [list(pair) for pair in best_mapping],
        "slot_switch_count": switch_numerator,
        "slot_switch_denominator": switch_denominator,
        "slot_switch_rate": switch_numerator / switch_denominator if switch_denominator else 0.0,
        "unassigned_count": unassigned_count,
        "unassigned_rate": unassigned_count / total if total else 0.0,
        "uncertain_count": uncertain_count,
        "uncertain_rate": uncertain_count / total if total else 0.0,
    }
