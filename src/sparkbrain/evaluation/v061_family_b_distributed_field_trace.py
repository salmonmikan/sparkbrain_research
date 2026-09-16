from __future__ import annotations

import math
from dataclasses import dataclass, field

from .v061_p3_p5_diagnostic_protocol import StateLocus
from .v061_premechanism_admission import MechanismFamily, PreMechanismProposal

PROPOSAL_ID = "a01-family-b-distributed-field-trace-gen1-v1"
PRE_P4_FAMILY_SOURCE_SHA = "525ecd9e205b2657a4ed207ae2b6cef0bae4bffc"
PROTOCOL_BUNDLE_SOURCE_SHA = "7af99d6c3bbbf946f90fc01d9bc7cc7661de2006"
MECHANISM_RULE_SPEC_PATH = "docs/V061_A01_FAMILY_B_DISTRIBUTED_FIELD_TRACE_GEN1.md"
NULL_LADDER_SPEC_PATH = "docs/V061_A01_NULL_LADDER.md"
BELIEF_STATE_NULL_ID = "v061-a01-bgen1-explicit-latent-cause-belief-null-v1"
DEFAULT_WIDTH = 4
DEFAULT_DECAY = 0.5


@dataclass(slots=True)
class ExternalEvidenceLedger:
    """Acquisition-side duplicate guard, deliberately outside the F-only carrier."""

    _consumed_ids: set[str] = field(default_factory=set, repr=False)

    @property
    def consumed_ids(self) -> frozenset[str]:
        return frozenset(self._consumed_ids)

    def export_consumed_ids(self) -> tuple[str, ...]:
        """Return deterministic checkpoint state for the acquisition boundary."""

        return tuple(sorted(self._consumed_ids))

    @classmethod
    def from_consumed_ids(
        cls,
        consumed_ids: tuple[str, ...] | list[str],
    ) -> ExternalEvidenceLedger:
        """Restore acquisition deduplication state across checkpoint/restart."""

        if not isinstance(consumed_ids, (tuple, list)):
            raise TypeError("consumed evidence IDs must be a tuple or list")
        if any(
            not isinstance(evidence_id, str) or not evidence_id.strip()
            for evidence_id in consumed_ids
        ):
            raise ValueError("consumed evidence IDs must be non-empty strings")
        if len(set(consumed_ids)) != len(consumed_ids):
            raise ValueError("consumed evidence IDs must be unique")
        return cls(_consumed_ids=set(consumed_ids))

    def consume_once(self, evidence_id: str) -> None:
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            raise ValueError("external evidence ID must be a non-empty string")
        if evidence_id in self._consumed_ids:
            raise ValueError("external evidence ID already consumed")
        self._consumed_ids.add(evidence_id)


@dataclass(frozen=True, slots=True)
class DistributedFieldTraceState:
    """Anonymous local Field carrier for Family-B construction tests.

    The carrier deliberately contains no lineage ID, semantic/task label,
    transition key, evaluator key, caller-selected address, or evidence ID.
    """

    eligibility: tuple[float, ...]
    credit: tuple[float, ...]
    decay: float = DEFAULT_DECAY

    @classmethod
    def zeros(
        cls,
        width: int = DEFAULT_WIDTH,
        *,
        decay: float = DEFAULT_DECAY,
    ) -> DistributedFieldTraceState:
        if width <= 0:
            raise ValueError("width must be positive")
        _validate_decay(decay)
        zeros = (0.0,) * width
        return cls(eligibility=zeros, credit=zeros, decay=decay)

    def validate(self) -> None:
        if not self.eligibility:
            raise ValueError("field carrier must be non-empty")
        if len(self.eligibility) != len(self.credit):
            raise ValueError("eligibility and credit widths must match")
        _validate_decay(self.decay)
        _validate_eligibility(self.eligibility, decay=self.decay)
        _validate_credit(self.credit, decay=self.decay)

    def deposit_local_activity(
        self,
        activity: tuple[float, ...],
    ) -> DistributedFieldTraceState:
        """Advance one local step: decay old traces, then add local activity."""

        self.validate()
        _validate_unit_interval_vector(
            activity,
            expected_width=len(self.eligibility),
            label="local activity",
        )
        eligibility = tuple(
            self.decay * previous + current
            for previous, current in zip(self.eligibility, activity, strict=True)
        )
        credit = tuple(self.decay * previous for previous in self.credit)
        _validate_eligibility(eligibility, decay=self.decay)
        _validate_credit(credit, decay=self.decay)
        return DistributedFieldTraceState(
            eligibility=eligibility,
            credit=credit,
            decay=self.decay,
        )

    def apply_external_world_return(
        self,
        boundary_activity: tuple[float, ...],
        *,
        sign: int,
        evidence_id: str,
        evidence_ledger: ExternalEvidenceLedger,
    ) -> DistributedFieldTraceState:
        """Apply one deduplicated signed anonymous boundary consequence."""

        self.validate()
        if type(sign) is not int or sign not in {-1, 1}:
            raise ValueError("external world-return sign must be -1 or +1")
        if not isinstance(evidence_ledger, ExternalEvidenceLedger):
            raise TypeError("external world return requires an ExternalEvidenceLedger")
        _validate_unit_interval_vector(
            boundary_activity,
            expected_width=len(self.eligibility),
            label="boundary activity",
        )
        credit = tuple(
            self.decay * previous
            + (1.0 - self.decay) * sign * eligible * boundary
            for previous, eligible, boundary in zip(
                self.credit,
                self.eligibility,
                boundary_activity,
                strict=True,
            )
        )
        _validate_credit(credit, decay=self.decay)
        evidence_ledger.consume_once(evidence_id)
        return DistributedFieldTraceState(
            eligibility=self.eligibility,
            credit=credit,
            decay=self.decay,
        )

    def internal_replay(self) -> DistributedFieldTraceState:
        """Internal replay alone cannot create or strengthen consequence credit."""

        self.validate()
        return self

    def competition_score(self, activity: tuple[float, ...]) -> float:
        """Return the local Field contribution to later competition."""

        self.validate()
        _validate_unit_interval_vector(
            activity,
            expected_width=len(self.credit),
            label="competition activity",
        )
        score = sum(
            credit * local
            for credit, local in zip(self.credit, activity, strict=True)
        )
        if not math.isfinite(score):
            raise ValueError("competition score must be finite")
        return score

    def export_field_carrier(
        self,
    ) -> tuple[tuple[float, ...], tuple[float, ...], float]:
        """Export exactly the F-only carrier used by the prospective P3 test."""

        self.validate()
        return self.eligibility, self.credit, self.decay

    @classmethod
    def from_field_carrier(
        cls,
        carrier: (
            tuple[tuple[float, ...], tuple[float, ...], float]
            | list[object]
        ),
    ) -> DistributedFieldTraceState:
        """Restore a persisted F-only carrier while preserving immutability."""

        if not isinstance(carrier, (tuple, list)) or len(carrier) != 3:
            raise ValueError("field carrier must contain eligibility, credit, and decay")
        eligibility_raw, credit_raw, decay = carrier
        if not isinstance(eligibility_raw, (tuple, list)) or not isinstance(
            credit_raw, (tuple, list)
        ):
            raise TypeError("field carrier vectors must be tuple or list sequences")
        eligibility = tuple(eligibility_raw)
        credit = tuple(credit_raw)
        state = cls(eligibility=eligibility, credit=credit, decay=decay)
        state.validate()
        return state


def _validate_decay(decay: float) -> None:
    if isinstance(decay, bool) or not isinstance(decay, (int, float)):
        raise TypeError("decay must be a real number")
    if not math.isfinite(decay) or not 0.0 <= decay < 1.0:
        raise ValueError("decay must be finite and in [0, 1)")


def _resource_bound(decay: float) -> float:
    _validate_decay(decay)
    return 1.0 / (1.0 - decay)


def _validate_vector(values: tuple[float, ...], *, expected_width: int) -> None:
    if len(values) != expected_width:
        raise ValueError("vector width mismatch")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise TypeError("vector values must be real numbers")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("vector values must be finite")


def _validate_unit_interval_vector(
    values: tuple[float, ...],
    *,
    expected_width: int,
    label: str,
) -> None:
    _validate_vector(values, expected_width=expected_width)
    if any(value < 0.0 or value > 1.0 for value in values):
        raise ValueError(f"{label} values must be in [0, 1]")


def _validate_eligibility(values: tuple[float, ...], *, decay: float) -> None:
    _validate_vector(values, expected_width=len(values))
    bound = _resource_bound(decay)
    if any(value < 0.0 or value > bound + 1e-12 for value in values):
        raise ValueError("eligibility values exceed the fixed resource bound")


def _validate_credit(values: tuple[float, ...], *, decay: float) -> None:
    _validate_vector(values, expected_width=len(values))
    bound = _resource_bound(decay)
    if any(abs(value) > bound + 1e-12 for value in values):
        raise ValueError("credit values exceed the fixed resource bound")


FAMILY_B_GEN1_PROPOSAL = PreMechanismProposal(
    proposal_id=PROPOSAL_ID,
    mechanism_family=MechanismFamily.DISTRIBUTED_FIELD_TRACE,
    lineage_swap_test_declared=True,
    external_confirmation_only_positive=True,
    contradiction_correction_declared=True,
    future_local_competition_effect_declared=True,
    bounded_ambiguity_declared=True,
    uses_forbidden_privilege=False,
    expected_p3_carrier_loci=(StateLocus.FIELD_STATE,),
    explicit_null_declared=True,
    recurrent_null_declared=True,
    negative_stop_observation_declared=True,
    lineage_swap_protocol_id="v061-a01-bgen1-lineage-swap-v1",
    contradiction_protocol_id="v061-a01-bgen1-contradiction-v1",
    future_competition_protocol_id="v061-a01-bgen1-future-local-competition-v1",
    bounded_ambiguity_protocol_id="v061-a01-bgen1-bounded-plurality-v1",
    p3_protocol_id="v061-a01-bgen1-field-only-functional-transfer-v1",
    explicit_null_id="v061-a01-bgen1-explicit-eligibility-return-address-null-v1",
    recurrent_null_id="v061-a01-bgen1-resource-matched-recurrent-causal-trace-null-v1",
    negative_stop_observation_id=(
        "v061-a01-bgen1-stop-f-only-failure-or-null-reduction-v1"
    ),
    protocol_bundle_source_sha=PROTOCOL_BUNDLE_SOURCE_SHA,
    mechanism_rule_spec_path=MECHANISM_RULE_SPEC_PATH,
    null_ladder_spec_path=NULL_LADDER_SPEC_PATH,
).bind()
