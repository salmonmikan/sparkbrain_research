from __future__ import annotations

import math
from dataclasses import dataclass

from .v061_p3_p5_diagnostic_protocol import StateLocus
from .v061_premechanism_admission import MechanismFamily, PreMechanismProposal

PROPOSAL_ID = "a01-family-b-distributed-field-trace-gen1-v1"
PROTOCOL_BUNDLE_SOURCE_SHA = "7af99d6c3bbbf946f90fc01d9bc7cc7661de2006"
MECHANISM_RULE_SPEC_PATH = "docs/V061_A01_FAMILY_B_DISTRIBUTED_FIELD_TRACE_GEN1.md"
NULL_LADDER_SPEC_PATH = "docs/V061_A01_NULL_LADDER.md"
BELIEF_STATE_NULL_ID = "v061-a01-bgen1-explicit-latent-cause-belief-null-v1"
DEFAULT_WIDTH = 4
DEFAULT_DECAY = 0.5


@dataclass(frozen=True, slots=True)
class DistributedFieldTraceState:
    """Anonymous local Field carrier for Family-B construction tests.

    The carrier deliberately contains no lineage ID, semantic/task label,
    transition key, evaluator key, or caller-selected address.
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
        _validate_vector(self.eligibility, expected_width=len(self.eligibility))
        _validate_vector(self.credit, expected_width=len(self.credit))

    def deposit_local_activity(
        self,
        activity: tuple[float, ...],
    ) -> DistributedFieldTraceState:
        """Decay prior eligibility and add anonymous local Field activity."""

        self.validate()
        _validate_vector(activity, expected_width=len(self.eligibility))
        if any(value < 0.0 for value in activity):
            raise ValueError("local activity must be non-negative")
        eligibility = tuple(
            self.decay * previous + current
            for previous, current in zip(self.eligibility, activity, strict=True)
        )
        return DistributedFieldTraceState(
            eligibility=eligibility,
            credit=self.credit,
            decay=self.decay,
        )

    def apply_external_world_return(
        self,
        boundary_activity: tuple[float, ...],
        *,
        sign: int,
    ) -> DistributedFieldTraceState:
        """Apply signed anonymous boundary consequence component-wise."""

        self.validate()
        if sign not in {-1, 1}:
            raise ValueError("external world-return sign must be -1 or +1")
        _validate_vector(boundary_activity, expected_width=len(self.eligibility))
        if any(value < 0.0 for value in boundary_activity):
            raise ValueError("boundary activity must be non-negative")
        credit = tuple(
            previous + sign * eligible * boundary
            for previous, eligible, boundary in zip(
                self.credit,
                self.eligibility,
                boundary_activity,
                strict=True,
            )
        )
        return DistributedFieldTraceState(
            eligibility=self.eligibility,
            credit=credit,
            decay=self.decay,
        )

    def internal_replay(self) -> DistributedFieldTraceState:
        """Internal replay alone cannot create or alter consequence credit."""

        self.validate()
        return self

    def competition_score(self, activity: tuple[float, ...]) -> float:
        """Return the local Field contribution to later competition."""

        self.validate()
        _validate_vector(activity, expected_width=len(self.credit))
        if any(value < 0.0 for value in activity):
            raise ValueError("competition activity must be non-negative")
        return sum(
            credit * local
            for credit, local in zip(self.credit, activity, strict=True)
        )

    def export_field_carrier(
        self,
    ) -> tuple[tuple[float, ...], tuple[float, ...], float]:
        """Export exactly the F-only carrier used by the prospective P3 test."""

        self.validate()
        return self.eligibility, self.credit, self.decay

    @classmethod
    def from_field_carrier(
        cls,
        carrier: tuple[tuple[float, ...], tuple[float, ...], float],
    ) -> DistributedFieldTraceState:
        eligibility, credit, decay = carrier
        state = cls(eligibility=eligibility, credit=credit, decay=decay)
        state.validate()
        return state


def _validate_decay(decay: float) -> None:
    if not math.isfinite(decay) or not 0.0 <= decay < 1.0:
        raise ValueError("decay must be finite and in [0, 1)")


def _validate_vector(values: tuple[float, ...], *, expected_width: int) -> None:
    if len(values) != expected_width:
        raise ValueError("vector width mismatch")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("vector values must be finite")


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
