from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .v061_family_b_distributed_field_trace import (
    DistributedFieldTraceState,
    ExternalEvidenceLedger,
)


def _json_string(payload: dict[str, Any], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _json_positive_int(payload: dict[str, Any], key: str) -> int:
    value = payload[key]
    if type(value) is not int or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _json_number(payload: dict[str, Any], key: str) -> float:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a finite number")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{key} must be a finite number")
    return converted


def _json_vector(payload: dict[str, Any], key: str) -> tuple[float, ...]:
    raw = payload[key]
    if not isinstance(raw, list):
        raise ValueError(f"{key} must be a JSON array")
    values: list[float] = []
    for value in raw:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{key} values must be finite numbers")
        converted = float(value)
        if not math.isfinite(converted):
            raise ValueError(f"{key} values must be finite numbers")
        values.append(converted)
    return tuple(values)


def _fixed_json_sign(payload: dict[str, Any], key: str, expected: int) -> int:
    value = payload[key]
    if type(value) is not int or value != expected:
        raise ValueError("readiness fixture signs must be fixed at +1 and -1")
    return value


@dataclass(frozen=True, slots=True)
class FamilyBGen1ReadinessFixture:
    fixture_id: str
    width: int
    decay: float
    left_activity: tuple[float, ...]
    right_activity: tuple[float, ...]
    plural_activity: tuple[float, ...]
    left_boundary_return: tuple[float, ...]
    right_boundary_return: tuple[float, ...]
    confirmation_sign: int
    contradiction_sign: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FamilyBGen1ReadinessFixture:
        return cls(
            fixture_id=_json_string(payload, "fixture_id"),
            width=_json_positive_int(payload, "width"),
            decay=_json_number(payload, "decay"),
            left_activity=_json_vector(payload, "left_activity"),
            right_activity=_json_vector(payload, "right_activity"),
            plural_activity=_json_vector(payload, "plural_activity"),
            left_boundary_return=_json_vector(payload, "left_boundary_return"),
            right_boundary_return=_json_vector(payload, "right_boundary_return"),
            confirmation_sign=_fixed_json_sign(payload, "confirmation_sign", 1),
            contradiction_sign=_fixed_json_sign(payload, "contradiction_sign", -1),
        )

    def validate(self) -> None:
        if not self.fixture_id:
            raise ValueError("fixture_id must be non-empty")
        if type(self.width) is not int or self.width <= 0:
            raise ValueError("width must be a positive integer")
        if not math.isfinite(self.decay) or not 0.0 <= self.decay < 1.0:
            raise ValueError("decay must be finite and in [0, 1)")
        vectors = (
            self.left_activity,
            self.right_activity,
            self.plural_activity,
            self.left_boundary_return,
            self.right_boundary_return,
        )
        if any(len(vector) != self.width for vector in vectors):
            raise ValueError("all readiness vectors must match fixture width")
        if any(
            not math.isfinite(value) or value < 0.0 or value > 1.0
            for vector in vectors
            for value in vector
        ):
            raise ValueError("readiness vector values must be finite and in [0, 1]")
        if self.confirmation_sign != 1 or self.contradiction_sign != -1:
            raise ValueError("readiness fixture signs must be fixed at +1 and -1")


@dataclass(frozen=True, slots=True)
class FamilyBGen1ConstructionResult:
    fixture_id: str
    external_return_required: bool
    duplicate_evidence_rejected: bool
    dedup_state_round_trips: bool
    lineage_swap_follows_footprint: bool
    contradiction_corrects_credit: bool
    f_only_transfer_preserves_effect: bool
    bounded_plurality_differentiates_by_overlap: bool
    credit_expires_and_remains_bounded: bool

    @property
    def all_construction_checks_pass(self) -> bool:
        return all(
            (
                self.external_return_required,
                self.duplicate_evidence_rejected,
                self.dedup_state_round_trips,
                self.lineage_swap_follows_footprint,
                self.contradiction_corrects_credit,
                self.f_only_transfer_preserves_effect,
                self.bounded_plurality_differentiates_by_overlap,
                self.credit_expires_and_remains_bounded,
            )
        )


def load_readiness_fixture(path: Path) -> FamilyBGen1ReadinessFixture:
    payload = json.loads(path.read_text(encoding="utf-8"))
    fixture = FamilyBGen1ReadinessFixture.from_dict(payload)
    fixture.validate()
    return fixture


def run_construction_readiness(
    fixture: FamilyBGen1ReadinessFixture,
) -> FamilyBGen1ConstructionResult:
    """Run deterministic pre-execution construction checks only.

    This function does not acquire experiment output and must not be interpreted
    as scientific evidence or execution admission.
    """

    fixture.validate()
    empty = DistributedFieldTraceState.zeros(
        fixture.width,
        decay=fixture.decay,
    )
    ledger = ExternalEvidenceLedger()

    left = empty.deposit_local_activity(fixture.left_activity)
    left_replay = left.internal_replay()
    left_confirmed = left.apply_external_world_return(
        fixture.left_boundary_return,
        sign=fixture.confirmation_sign,
        evidence_id="readiness:left:confirm",
        evidence_ledger=ledger,
    )
    external_required = left_replay.credit != left_confirmed.credit

    checkpoint = ledger.export_consumed_ids()
    restored_ledger = ExternalEvidenceLedger.from_consumed_ids(checkpoint)
    try:
        left_confirmed.apply_external_world_return(
            fixture.left_boundary_return,
            sign=fixture.confirmation_sign,
            evidence_id="readiness:left:confirm",
            evidence_ledger=restored_ledger,
        )
    except ValueError as error:
        duplicate_rejected = str(error) == "external evidence ID already consumed"
    else:
        duplicate_rejected = False
    dedup_round_trip = (
        restored_ledger.export_consumed_ids() == checkpoint
        and checkpoint == ("readiness:left:confirm",)
    )

    right = empty.deposit_local_activity(fixture.right_activity)
    right_confirmed = right.apply_external_world_return(
        fixture.right_boundary_return,
        sign=fixture.confirmation_sign,
        evidence_id="readiness:right:confirm",
        evidence_ledger=ledger,
    )
    lineage_swap = (
        left_confirmed.competition_score(fixture.left_activity) > 0.0
        and left_confirmed.competition_score(fixture.right_activity) == 0.0
        and right_confirmed.competition_score(fixture.right_activity) > 0.0
        and right_confirmed.competition_score(fixture.left_activity) == 0.0
    )

    left_corrected = left_confirmed.apply_external_world_return(
        fixture.left_boundary_return,
        sign=fixture.contradiction_sign,
        evidence_id="readiness:left:contradict",
        evidence_ledger=ledger,
    )
    contradiction = (
        left_corrected.competition_score(fixture.left_activity) < 0.0
        < left_confirmed.competition_score(fixture.left_activity)
    )

    transplanted = DistributedFieldTraceState.from_field_carrier(
        left_confirmed.export_field_carrier()
    )
    f_only_transfer = transplanted.competition_score(
        fixture.left_activity
    ) == left_confirmed.competition_score(fixture.left_activity)

    plural = empty.deposit_local_activity(fixture.plural_activity)
    plural_left = plural.apply_external_world_return(
        fixture.left_boundary_return,
        sign=fixture.confirmation_sign,
        evidence_id="readiness:plural:left",
        evidence_ledger=ledger,
    )
    plural_right = plural.apply_external_world_return(
        fixture.right_boundary_return,
        sign=fixture.confirmation_sign,
        evidence_id="readiness:plural:right",
        evidence_ledger=ledger,
    )
    bounded_plurality = (
        plural_left.competition_score(fixture.left_activity) > 0.0
        and plural_left.competition_score(fixture.right_activity) == 0.0
        and plural_right.competition_score(fixture.right_activity) > 0.0
        and plural_right.competition_score(fixture.left_activity) == 0.0
    )

    decayed = left_confirmed.deposit_local_activity((0.0,) * fixture.width)
    bound = 1.0 / (1.0 - fixture.decay)
    credit_bounded = (
        abs(decayed.credit[0]) < abs(left_confirmed.credit[0])
        and all(abs(value) <= bound for value in decayed.credit)
    )

    return FamilyBGen1ConstructionResult(
        fixture_id=fixture.fixture_id,
        external_return_required=external_required,
        duplicate_evidence_rejected=duplicate_rejected,
        dedup_state_round_trips=dedup_round_trip,
        lineage_swap_follows_footprint=lineage_swap,
        contradiction_corrects_credit=contradiction,
        f_only_transfer_preserves_effect=f_only_transfer,
        bounded_plurality_differentiates_by_overlap=bounded_plurality,
        credit_expires_and_remains_bounded=credit_bounded,
    )
