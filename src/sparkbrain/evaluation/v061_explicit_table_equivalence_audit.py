from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class StateLocality(StrEnum):
    CENTRAL_TABLE = "central-table"
    LOCAL_TRANSITION = "local-transition"
    FIELD_DISTRIBUTED = "field-distributed"
    TRANSIENT_LINEAGE = "transient-lineage"
    TRANSIENT_QUEUE = "transient-queue"


class UpdateGate(StrEnum):
    EXTERNAL_CAUSAL = "external-causal"
    EXTERNAL_CORRELATIONAL = "external-correlational"
    INTERNAL_ONLY = "internal-only"
    STATIC = "static"


@dataclass(frozen=True, slots=True)
class MechanismDescriptor:
    mechanism_id: str
    state_locality: StateLocality
    persistent: bool
    expires_or_decays: bool
    key_dimensions: tuple[str, ...]
    value_dimensions: tuple[str, ...]
    update_gate: UpdateGate
    direct_query_returns_target: bool
    uses_assembly_key: bool = False
    uses_typed_functional_head: bool = False
    reads_evaluator_target: bool = False
    reads_scalar_reward: bool = False
    generated_activity_can_positive_update: bool = False

    def validate(self) -> None:
        if not self.mechanism_id:
            raise ValueError("mechanism_id must be non-empty")
        if len(set(self.key_dimensions)) != len(self.key_dimensions):
            raise ValueError("key dimensions must be unique")
        if len(set(self.value_dimensions)) != len(self.value_dimensions):
            raise ValueError("value dimensions must be unique")
        if not self.key_dimensions and self.state_locality is StateLocality.CENTRAL_TABLE:
            raise ValueError("central table requires a key")
        if (
            self.generated_activity_can_positive_update
            and self.update_gate is not UpdateGate.INTERNAL_ONLY
        ):
            raise ValueError(
                "generated positive update must be represented as internal-only gating"
            )

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "state_locality": self.state_locality.value,
            "update_gate": self.update_gate.value,
        }


@dataclass(frozen=True, slots=True)
class TableEquivalenceAssessment:
    mechanism_id: str
    forbidden_privileged_structure: bool
    self_confirmation_risk: bool
    explicit_target_lookup_equivalent: bool
    explicit_transition_memory: bool
    transient_causal_eligibility_candidate: bool
    distributed_field_candidate: bool
    requires_further_behavioral_equivalence_test: bool
    accepted_as_emergent_field_organization: bool
    classification: str
    reasons: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


_TARGET_KEYS = frozenset(
    {
        "target",
        "target_id",
        "next_target",
        "external_target",
        "correct_action",
        "answer",
    }
)
_LINEAGE_KEYS = frozenset(
    {
        "lineage_id",
        "proposal_id",
        "path_id",
        "transition_id",
        "source_id",
        "context_id",
        "assembly_id",
    }
)
_TYPED_VALUES = frozenset(
    {
        "prediction",
        "action",
        "reward",
        "memory",
        "role",
        "meaning",
        "correctness",
    }
)


def audit_table_equivalence(
    descriptor: MechanismDescriptor,
) -> TableEquivalenceAssessment:
    """Classify a proposed mechanism without judging benchmark performance.

    Passing this audit never proves emergence. It only excludes some obvious
    forms of evaluator privilege, self-confirmation, and explicit lookup.
    """

    descriptor.validate()
    keys = set(descriptor.key_dimensions)
    values = set(descriptor.value_dimensions)
    reasons: list[str] = []

    privileged = any(
        (
            descriptor.uses_assembly_key,
            descriptor.uses_typed_functional_head,
            descriptor.reads_evaluator_target,
            descriptor.reads_scalar_reward,
            bool(values.intersection(_TYPED_VALUES)),
            "correct_action" in keys,
            "answer" in keys,
        )
    )
    if privileged:
        reasons.append("contains privileged or typed functional structure")

    self_confirmation = (
        descriptor.generated_activity_can_positive_update
        or descriptor.update_gate is UpdateGate.INTERNAL_ONLY
    )
    if self_confirmation:
        reasons.append("internally generated activity can create positive evidence")

    target_addressed = bool(keys.intersection(_TARGET_KEYS)) or bool(
        values.intersection(_TARGET_KEYS)
    )
    lineage_addressed = bool(keys.intersection(_LINEAGE_KEYS))
    explicit_lookup = (
        descriptor.persistent
        and descriptor.direct_query_returns_target
        and target_addressed
        and (descriptor.state_locality is StateLocality.CENTRAL_TABLE or lineage_addressed)
    )
    if explicit_lookup:
        reasons.append("persistent keyed state directly returns a target")

    explicit_transition_memory = (
        descriptor.persistent
        and descriptor.state_locality
        in {StateLocality.CENTRAL_TABLE, StateLocality.LOCAL_TRANSITION}
        and lineage_addressed
    )
    if explicit_transition_memory:
        reasons.append("persistent lineage-keyed transition memory")

    transient_eligibility = (
        not descriptor.persistent
        and descriptor.expires_or_decays
        and descriptor.state_locality is StateLocality.TRANSIENT_LINEAGE
        and lineage_addressed
        and descriptor.update_gate is UpdateGate.EXTERNAL_CAUSAL
        and not descriptor.direct_query_returns_target
        and not privileged
        and not self_confirmation
    )
    if transient_eligibility:
        reasons.append("bounded externally gated causal-lineage eligibility candidate")

    field_candidate = (
        descriptor.state_locality is StateLocality.FIELD_DISTRIBUTED
        and descriptor.expires_or_decays
        and descriptor.update_gate is UpdateGate.EXTERNAL_CAUSAL
        and not descriptor.direct_query_returns_target
        and not privileged
        and not self_confirmation
    )
    if field_candidate:
        reasons.append("distributed Field-state candidate without direct target lookup")

    further_test = (
        transient_eligibility
        or field_candidate
        or (
            explicit_transition_memory
            and not explicit_lookup
            and not privileged
            and not self_confirmation
        )
    )
    # Static description can reject obvious designs, but cannot establish that
    # a surviving candidate is emergent rather than behaviorally equivalent to
    # a compact explicit predictor.
    accepted_as_emergent = False

    if privileged:
        classification = "forbidden-privileged-structure"
    elif self_confirmation:
        classification = "invalid-self-confirming-mechanism"
    elif explicit_lookup:
        classification = "explicit-target-lookup"
    elif transient_eligibility:
        classification = "transient-causal-eligibility-candidate"
    elif field_candidate:
        classification = "distributed-field-candidate"
    elif explicit_transition_memory:
        classification = "explicit-transition-memory"
    else:
        classification = "unclassified-requires-audit"
        reasons.append("static structure is insufficient for classification")

    return TableEquivalenceAssessment(
        mechanism_id=descriptor.mechanism_id,
        forbidden_privileged_structure=privileged,
        self_confirmation_risk=self_confirmation,
        explicit_target_lookup_equivalent=explicit_lookup,
        explicit_transition_memory=explicit_transition_memory,
        transient_causal_eligibility_candidate=transient_eligibility,
        distributed_field_candidate=field_candidate,
        requires_further_behavioral_equivalence_test=further_test,
        accepted_as_emergent_field_organization=accepted_as_emergent,
        classification=classification,
        reasons=tuple(reasons),
    )


def canonical_mechanism_descriptors() -> tuple[MechanismDescriptor, ...]:
    return (
        MechanismDescriptor(
            mechanism_id="explicit-lineage-target-lookup",
            state_locality=StateLocality.CENTRAL_TABLE,
            persistent=True,
            expires_or_decays=False,
            key_dimensions=("lineage_id", "context_id"),
            value_dimensions=("next_target",),
            update_gate=UpdateGate.EXTERNAL_CORRELATIONAL,
            direct_query_returns_target=True,
        ),
        MechanismDescriptor(
            mechanism_id="assembly-conditioned-target",
            state_locality=StateLocality.CENTRAL_TABLE,
            persistent=True,
            expires_or_decays=False,
            key_dimensions=("assembly_id",),
            value_dimensions=("target_id",),
            update_gate=UpdateGate.EXTERNAL_CORRELATIONAL,
            direct_query_returns_target=True,
            uses_assembly_key=True,
        ),
        MechanismDescriptor(
            mechanism_id="typed-reward-head",
            state_locality=StateLocality.CENTRAL_TABLE,
            persistent=True,
            expires_or_decays=False,
            key_dimensions=("context_id",),
            value_dimensions=("action", "reward"),
            update_gate=UpdateGate.EXTERNAL_CORRELATIONAL,
            direct_query_returns_target=True,
            uses_typed_functional_head=True,
            reads_scalar_reward=True,
        ),
        MechanismDescriptor(
            mechanism_id="self-confirming-lineage-score",
            state_locality=StateLocality.LOCAL_TRANSITION,
            persistent=True,
            expires_or_decays=True,
            key_dimensions=("transition_id",),
            value_dimensions=("scalar_credit",),
            update_gate=UpdateGate.INTERNAL_ONLY,
            direct_query_returns_target=False,
            generated_activity_can_positive_update=True,
        ),
        MechanismDescriptor(
            mechanism_id="bounded-causal-eligibility",
            state_locality=StateLocality.TRANSIENT_LINEAGE,
            persistent=False,
            expires_or_decays=True,
            key_dimensions=("proposal_id", "transition_id"),
            value_dimensions=("eligibility",),
            update_gate=UpdateGate.EXTERNAL_CAUSAL,
            direct_query_returns_target=False,
        ),
        MechanismDescriptor(
            mechanism_id="distributed-consequence-trace",
            state_locality=StateLocality.FIELD_DISTRIBUTED,
            persistent=False,
            expires_or_decays=True,
            key_dimensions=("source_id",),
            value_dimensions=("trace_amplitude",),
            update_gate=UpdateGate.EXTERNAL_CAUSAL,
            direct_query_returns_target=False,
        ),
        MechanismDescriptor(
            mechanism_id="persistent-local-credit",
            state_locality=StateLocality.LOCAL_TRANSITION,
            persistent=True,
            expires_or_decays=True,
            key_dimensions=("transition_id",),
            value_dimensions=("scalar_credit",),
            update_gate=UpdateGate.EXTERNAL_CAUSAL,
            direct_query_returns_target=False,
        ),
    )
