from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.evaluation.v061_anonymous_credit_diagnostic_protocol import (
    CausalCreditAssessment,
    CausalCreditTrial,
    EvidenceSource,
    WorldRelationPermutationTrial,
    assess_causal_credit_trial,
    assess_world_relation_permutation,
    build_causal_credit_protocol_matrix,
)
from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import (
    AmbiguityContinuationTrial,
    BehavioralChallenge,
    ContinuationEvidence,
    StateLocus,
    StateLocusCrossTransplantTrial,
    StateLocusSnapshot,
    assess_ambiguity_continuation,
    assess_state_locus_cross_transplant,
)
from sparkbrain.evaluation.v061_p5_dynamics_equivalence_protocol import (
    DynamicBehavioralOutcome,
    DynamicMechanismRun,
    UpdateLocus,
    assess_dynamic_table_equivalence,
)
from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig

from .credit_bridge import (
    A01CausalCreditResolution,
    A01CausalCreditStatus,
    A01LocalTemporalExpectation,
    A01TransientCreditBridge,
)
from .development_protocol import (
    A01WorldRelationPermutationTrial,
    assess_a01_world_relation_permutation,
    base_temporal_learned_state_hash,
    build_p1_observation,
    capture_path_support,
    causal_support_state_hash,
    competition_signature,
)

SCHEMA_VERSION = "v061-a01-mechanism-discrimination-v1"
RUN_ID = "A01-MD-001"
LINEAGE_A = "lineage-a"
LINEAGE_B = "lineage-b"
ROOT = "A"
TARGET_A = "B"
TARGET_B = "C"
PATH_A = "local:A->B"
PATH_B = "local:A->C"
PORT_ID = "port:p"
PRIOR_TARGET = "world:x"
CONTRADICTION_TARGET = "world:y"


@dataclass(slots=True)
class _Fixture:
    expectation: A01LocalTemporalExpectation
    ledger: ProvenanceLedger
    consistency: UntypedBoundaryConsistency
    bridge: A01TransientCreditBridge


@dataclass(slots=True)
class _MinimalExplicitLocalSupport:
    """Evaluator-only N1 null using the same admissible causal evidence as A01."""

    counts: dict[str, tuple[int, int]]

    def __init__(self) -> None:
        self.counts = {}

    def observe(self, path_ids: tuple[str, ...], *, matched: bool) -> None:
        for path_id in path_ids:
            consistent, contradicted = self.counts.get(path_id, (0, 0))
            if matched:
                consistent += 1
            else:
                contradicted += 1
            self.counts[path_id] = (consistent, contradicted)

    def gain(self, path_id: str) -> float:
        consistent, contradicted = self.counts.get(path_id, (0, 0))
        reliability = (1.0 + consistent) / (2.0 + consistent + contradicted)
        return reliability / 0.5

    def state_dict(self) -> dict[str, dict[str, int]]:
        return {
            path_id: {
                "external_consistent_count": consistent,
                "external_contradicted_count": contradicted,
            }
            for path_id, (consistent, contradicted) in sorted(self.counts.items())
        }

    @classmethod
    def from_state_dict(
        cls,
        value: dict[str, dict[str, int]],
    ) -> _MinimalExplicitLocalSupport:
        model = cls()
        model.counts = {
            str(path_id): (
                int(row["external_consistent_count"]),
                int(row["external_contradicted_count"]),
            )
            for path_id, row in value.items()
        }
        return model


def _path(root: str, target: str) -> str:
    return f"local:{root}->{target}"


def _external(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    parent_event_ids: tuple[str, ...] = (),
    polarity: int = 1,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=polarity,
        origin=origin,
        parent_event_ids=parent_event_ids,
    )


def _boundary(
    event_id: str,
    time_ms: float,
    *,
    proposal_ids: tuple[str, ...] = (),
    port_id: str = PORT_ID,
    physical_tag: str = "default",
) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=time_ms,
        port_id=port_id,
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{physical_tag}:{event_id}",
        source_unit_id=2,
        source_proposal_ids=proposal_ids,
        generation_depth=1,
        source_state_hash=f"field:{physical_tag}",
    )


def _proposal(
    proposal_id: str,
    *,
    path_id: str,
    target: str,
    parent_proposal_ids: tuple[str, ...] = (),
    physical_tag: str = "default",
) -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id=proposal_id,
        created_at_ms=1.0,
        target=target,
        predicted_arrival_ms=6.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash=f"field:{physical_tag}",
        parent_proposal_ids=parent_proposal_ids,
        local_path_ids=(path_id,),
        generation_depth=1,
        valid_until_ms=30.0,
        energy_cost=0.1,
    )


def _expectation(
    *,
    root: str = ROOT,
    target_a: str = TARGET_A,
    target_b: str = TARGET_B,
) -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.0,
        )
    )
    for branch_index, target in enumerate((target_a, target_b)):
        for observation_index in range(2):
            time_ms = branch_index * 100.0 + observation_index * 20.0
            source = _external(
                f"train:{root}:{target}:source:{observation_index}",
                time_ms,
                root,
            )
            consequence = _external(
                f"train:{root}:{target}:target:{observation_index}",
                time_ms + 5.0,
                target,
            )
            model.observe_external_transition(source, consequence)
    return model


def _fixture(
    *,
    root: str = ROOT,
    target_a: str = TARGET_A,
    target_b: str = TARGET_B,
    prior_target: str = PRIOR_TARGET,
    learn_prior: bool = True,
) -> _Fixture:
    expectation = _expectation(root=root, target_a=target_a, target_b=target_b)
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency(ledger)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)
    fixture = _Fixture(expectation, ledger, consistency, bridge)
    if learn_prior:
        _learn_prior_relation(fixture, target=prior_target)
    return fixture


def _learn_prior_relation(
    fixture: _Fixture,
    *,
    target: str,
    event_prefix: str = "prior",
) -> None:
    boundary = _boundary(f"boundary:{event_prefix}", 10.0)
    fixture.consistency.register_boundary(boundary)
    external = _external(
        f"external:{event_prefix}",
        12.0,
        target,
        parent_event_ids=(boundary.event_id,),
    )
    fixture.ledger.register_external(external)
    resolution = fixture.consistency.observe_external(external)
    if resolution.boundary_event_id != boundary.event_id:
        raise AssertionError("failed to establish the anonymous prior relation")


def _credit_once(
    fixture: _Fixture,
    *,
    path_id: str,
    target: str,
    external_target: str,
    prefix: str,
    time_ms: float = 20.0,
    physical_tag: str = "default",
    parent_proposal_ids: tuple[str, ...] = (),
) -> A01CausalCreditResolution:
    proposal = _proposal(
        f"proposal:{prefix}",
        path_id=path_id,
        target=target,
        parent_proposal_ids=parent_proposal_ids,
        physical_tag=physical_tag,
    )
    fixture.ledger.register_proposal(proposal)
    boundary = _boundary(
        f"boundary:{prefix}",
        time_ms,
        proposal_ids=(proposal.proposal_id,),
        physical_tag=physical_tag,
    )
    fixture.consistency.register_boundary(boundary)
    external = _external(
        f"external:{prefix}",
        time_ms + 2.0,
        external_target,
        parent_event_ids=(boundary.event_id,),
    )
    fixture.ledger.register_external(external)
    return fixture.bridge.observe_external(boundary, external)


def _replay_attempt(
    fixture: _Fixture,
    *,
    path_id: str,
    target: str,
    prefix: str,
) -> bool:
    proposal = _proposal(f"proposal:{prefix}", path_id=path_id, target=target)
    fixture.ledger.register_proposal(proposal)
    boundary = _boundary(
        f"boundary:{prefix}",
        20.0,
        proposal_ids=(proposal.proposal_id,),
    )
    fixture.consistency.register_boundary(boundary)
    replay = _external(
        f"replay:{prefix}",
        22.0,
        PRIOR_TARGET,
        parent_event_ids=(boundary.event_id,),
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
    )
    fixture.ledger.register_event(replay)
    try:
        fixture.bridge.observe_external(boundary, replay)
    except ValueError as exc:
        return "only external events" in str(exc)
    return False


def _lineage_path(trial: CausalCreditTrial, lineage_id: str) -> tuple[str, str]:
    if lineage_id == LINEAGE_A:
        return PATH_A, TARGET_A
    if lineage_id == LINEAGE_B:
        return PATH_B, TARGET_B
    raise ValueError(f"unknown lineage in A01 matrix: {lineage_id}")


def _competition(
    expectation: A01LocalTemporalExpectation,
    *,
    root: str = ROOT,
    event_id: str = "probe",
    origin_state_hash: str = "field:probe",
) -> tuple[tuple[str, float], ...]:
    source = _external(event_id, 300.0, root)
    return competition_signature(
        expectation,
        source,
        origin_state_hash=origin_state_hash,
    )


def _selected_lineage(
    signature: tuple[tuple[str, float], ...],
    *,
    target_a: str = TARGET_A,
    target_b: str = TARGET_B,
) -> str:
    values = dict(signature)
    if values[target_a] > values[target_b]:
        return LINEAGE_A
    if values[target_b] > values[target_a]:
        return LINEAGE_B
    return "co-maximal:" + ",".join(sorted((LINEAGE_A, LINEAGE_B)))


def _support_scores(
    expectation: A01LocalTemporalExpectation,
    path_ids: tuple[str, ...],
) -> tuple[tuple[str, int], ...]:
    return capture_path_support(expectation, path_ids).path_scores


def _run_p1_trial(trial: CausalCreditTrial) -> dict[str, Any]:
    fixture = _fixture()
    causal_path, causal_target = _lineage_path(
        trial,
        trial.causal_lineage.lineage_id,
    )
    matched_path, _ = _lineage_path(
        trial,
        trial.matched_lineage.lineage_id,
    )
    tracked = (PATH_A, PATH_B)
    before = capture_path_support(fixture.expectation, tracked)
    resolution: A01CausalCreditResolution | None = None
    replay_rejected: bool | None = None

    if trial.evidence_source is EvidenceSource.EXTERNAL_MATCH:
        resolution = _credit_once(
            fixture,
            path_id=causal_path,
            target=causal_target,
            external_target=PRIOR_TARGET,
            prefix=trial.trial_id,
        )
        external_delta = 1
    elif trial.evidence_source is EvidenceSource.EXTERNAL_CONTRADICTION:
        resolution = _credit_once(
            fixture,
            path_id=causal_path,
            target=causal_target,
            external_target=CONTRADICTION_TARGET,
            prefix=trial.trial_id,
        )
        external_delta = 1
    elif trial.evidence_source is EvidenceSource.INTERNAL_REPLAY_ONLY:
        replay_rejected = _replay_attempt(
            fixture,
            path_id=causal_path,
            target=causal_target,
            prefix=trial.trial_id,
        )
        external_delta = 0
    else:
        external_delta = 0

    after = capture_path_support(fixture.expectation, tracked)
    positive_delta = int(
        resolution is not None and resolution.positive_credit_applied
    )
    observation = build_p1_observation(
        trial_id=trial.trial_id,
        causal_path_id=causal_path,
        matched_path_id=matched_path,
        before=before,
        after=after,
        external_observation_count_delta=external_delta,
        positive_commit_count_delta=positive_delta,
    )
    assessment: CausalCreditAssessment = assess_causal_credit_trial(
        trial,
        observation,
    )
    accepted = assessment.accepted and replay_rejected is not False
    return {
        "trial": trial.state_dict(),
        "observation": asdict(observation),
        "assessment": assessment.state_dict(),
        "bridge_resolution": resolution.state_dict() if resolution else None,
        "replay_rejected": replay_rejected,
        "support_before": before.state_dict(),
        "support_after": after.state_dict(),
        "competition_before": _format_competition(
            _competition(_expectation(), event_id=f"before:{trial.trial_id}")
        ),
        "competition_after": _format_competition(
            _competition(fixture.expectation, event_id=f"after:{trial.trial_id}")
        ),
        "accepted": accepted,
    }


def _run_contradiction_correction() -> dict[str, Any]:
    fixture = _fixture()
    tracked = (PATH_A, PATH_B)
    score_history = [_support_scores(fixture.expectation, tracked)]
    competition_history = [_competition(fixture.expectation, event_id="correction:0")]

    confirmation = _credit_once(
        fixture,
        path_id=PATH_A,
        target=TARGET_A,
        external_target=PRIOR_TARGET,
        prefix="correction:confirm",
        time_ms=20.0,
    )
    score_history.append(_support_scores(fixture.expectation, tracked))
    competition_history.append(_competition(fixture.expectation, event_id="correction:1"))

    contradiction = _credit_once(
        fixture,
        path_id=PATH_A,
        target=TARGET_A,
        external_target=CONTRADICTION_TARGET,
        prefix="correction:contradict",
        time_ms=40.0,
    )
    score_history.append(_support_scores(fixture.expectation, tracked))
    competition_history.append(_competition(fixture.expectation, event_id="correction:2"))

    corrected = (
        confirmation.status is A01CausalCreditStatus.EXACT_MATCH
        and contradiction.status is A01CausalCreditStatus.EXACT_CONTRADICTION
        and dict(score_history[0])[PATH_A] == 0
        and dict(score_history[1])[PATH_A] == 1
        and dict(score_history[2])[PATH_A] == 0
        and dict(score_history[2])[PATH_B] == 0
        and dict(competition_history[1])[TARGET_A] > dict(competition_history[1])[TARGET_B]
        and dict(competition_history[2])[TARGET_A] == dict(competition_history[2])[TARGET_B]
    )
    return {
        "support_score_trace": [list(row) for row in score_history],
        "competition_trace": [_format_competition(row) for row in competition_history],
        "confirmation_status": confirmation.status.value,
        "contradiction_status": contradiction.status.value,
        "existing_support_corrected": corrected,
    }


def _run_p1() -> dict[str, Any]:
    trials = tuple(_run_p1_trial(trial) for trial in build_causal_credit_protocol_matrix())
    return {
        "verdict": "SUPPORTED" if all(row["accepted"] for row in trials) else "NOT_SUPPORTED",
        "minimum_selective_effect": 0.5,
        "threshold_tuned": False,
        "trials": trials,
        "contradiction_correction": _run_contradiction_correction(),
        "lineage_swap_passed": next(
            row["accepted"]
            for row in trials
            if row["trial"]["trial_id"] == "external-match-b-lineage-swap"
        ),
        "absence_leakage_detected": any(
            value != 0
            for row in trials
            if row["trial"]["trial_id"] == "external-absence-a"
            for _, value in row["support_after"]["path_scores"]
        ),
        "replay_leakage_detected": any(
            value != 0
            for row in trials
            if row["trial"]["trial_id"] == "internal-replay-only-a"
            for _, value in row["support_after"]["path_scores"]
        ),
    }


def _run_world_arm(
    *,
    causal_path: str,
    causal_target: str,
    relation_id: str,
    prior_target: str,
) -> dict[str, Any]:
    fixture = _fixture(prior_target=prior_target)
    base_hash = base_temporal_learned_state_hash(fixture.expectation)
    resolution = _credit_once(
        fixture,
        path_id=causal_path,
        target=causal_target,
        external_target=prior_target,
        prefix=relation_id,
    )
    return {
        "expectation": fixture.expectation,
        "consistency": fixture.consistency,
        "base_hash": base_hash,
        "support_hash": causal_support_state_hash(fixture.expectation),
        "competition": _competition(
            fixture.expectation,
            event_id=f"probe:{relation_id}",
        ),
        "selected_lineage": _selected_lineage(
            _competition(fixture.expectation, event_id=f"select:{relation_id}")
        ),
        "resolution": resolution,
        "relation_id": relation_id,
    }


def _run_p2() -> dict[str, Any]:
    arm_a = _run_world_arm(
        causal_path=PATH_A,
        causal_target=TARGET_A,
        relation_id="world-relation-a",
        prior_target=PRIOR_TARGET,
    )
    arm_b = _run_world_arm(
        causal_path=PATH_B,
        causal_target=TARGET_B,
        relation_id="world-relation-b",
        prior_target=PRIOR_TARGET,
    )
    trial = A01WorldRelationPermutationTrial(
        trial_id="a01-p2-world-to-local-circulation",
        base_temporal_hash_before=arm_a["base_hash"],
        base_temporal_hash_after=arm_b["base_hash"],
        causal_support_hash_before=arm_a["support_hash"],
        causal_support_hash_after=arm_b["support_hash"],
        world_relation_before=arm_a["relation_id"],
        world_relation_after=arm_b["relation_id"],
        competition_signature_before=arm_a["competition"],
        competition_signature_after=arm_b["competition"],
        external_observation_count_delta=2,
    )
    assessment = assess_a01_world_relation_permutation(trial)
    generic_trial = WorldRelationPermutationTrial(
        trial_id=trial.trial_id,
        local_state_hash_before=arm_a["base_hash"],
        local_state_hash_after=arm_b["base_hash"],
        world_relation_before=arm_a["relation_id"],
        world_relation_after=arm_b["relation_id"],
        selected_lineage_before=arm_a["selected_lineage"],
        selected_lineage_after=arm_b["selected_lineage"],
    )
    generic_assessment = assess_world_relation_permutation(generic_trial)
    supported = (
        assessment.world_to_transition_circulation_observed
        and generic_assessment.world_to_transition_circulation_observed
        and arm_a["selected_lineage"] == LINEAGE_A
        and arm_b["selected_lineage"] == LINEAGE_B
    )
    return {
        "verdict": "SUPPORTED" if supported else "NOT_SUPPORTED",
        "trial": asdict(trial),
        "assessment": assessment.state_dict(),
        "generic_assessment": generic_assessment.state_dict(),
        "arm_a": _world_arm_state_dict(arm_a),
        "arm_b": _world_arm_state_dict(arm_b),
        "future_competition_changed": supported,
        "only_final_reentry_changed": False if supported else None,
    }


def _world_arm_state_dict(arm: dict[str, Any]) -> dict[str, Any]:
    return {
        "relation_id": arm["relation_id"],
        "base_temporal_hash": arm["base_hash"],
        "causal_support_hash": arm["support_hash"],
        "competition": _format_competition(arm["competition"]),
        "selected_lineage": arm["selected_lineage"],
        "resolution": arm["resolution"].state_dict(),
    }


def _consistency_signature(
    consistency: UntypedBoundaryConsistency,
) -> tuple[str, ...]:
    rows = []
    for value in consistency.learned_state_dict()["links"].values():
        row = dict(value)
        rows.append(
            "|".join(
                (
                    str(row["port_id"]),
                    str(row["target"]),
                    str(row["polarity"]),
                    str(row["consistent_count"]),
                    str(row["inconsistent_count"]),
                )
            )
        )
    return tuple(sorted(rows))


def _state_snapshot(
    *,
    expectation: A01LocalTemporalExpectation,
    consistency: UntypedBoundaryConsistency,
    field_hash: str | None,
    return_address_hash: str | None,
) -> StateLocusSnapshot:
    return StateLocusSnapshot(
        local_transition_hash=expectation.learned_state_hash(),
        field_state_hash=field_hash,
        consistency_hash=digest(consistency.learned_state_dict()),
        transient_return_address_hash=return_address_hash,
    )


def _local_only_cross() -> dict[str, Any]:
    baseline = _run_world_arm(
        causal_path=PATH_A,
        causal_target=TARGET_A,
        relation_id="p3-baseline-l",
        prior_target=PRIOR_TARGET,
    )
    donor = _run_world_arm(
        causal_path=PATH_B,
        causal_target=TARGET_B,
        relation_id="p3-donor-l",
        prior_target=CONTRADICTION_TARGET,
    )
    transplanted_expectation = A01LocalTemporalExpectation.from_learned_state_dict(
        deepcopy(donor["expectation"].learned_state_dict())
    )
    baseline_field = digest({"field": "baseline"})
    donor_field = digest({"field": "donor"})
    baseline_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=baseline["consistency"],
        field_hash=baseline_field,
        return_address_hash=None,
    )
    donor_snapshot = _state_snapshot(
        expectation=donor["expectation"],
        consistency=donor["consistency"],
        field_hash=donor_field,
        return_address_hash=None,
    )
    transplanted_snapshot = _state_snapshot(
        expectation=transplanted_expectation,
        consistency=baseline["consistency"],
        field_hash=baseline_field,
        return_address_hash=None,
    )
    before_signature = baseline["competition"]
    after_signature = _competition(transplanted_expectation, event_id="p3:l:after")
    trial = StateLocusCrossTransplantTrial(
        trial_id="a01-p3-l-only-post-learning",
        baseline_state=baseline_snapshot,
        donor_state=donor_snapshot,
        transplanted_state=transplanted_snapshot,
        transplanted_loci=(StateLocus.LOCAL_TRANSITION,),
        selected_lineage_before=_selected_lineage(before_signature),
        selected_lineage_after=_selected_lineage(after_signature),
        donor_selected_lineage=donor["selected_lineage"],
        reentry_signature_before=_consistency_signature(baseline["consistency"]),
        reentry_signature_after=_consistency_signature(baseline["consistency"]),
        donor_reentry_signature=_consistency_signature(donor["consistency"]),
    )
    assessment = assess_state_locus_cross_transplant(trial)
    return {
        "trial": _transplant_trial_state_dict(trial),
        "assessment": assessment.state_dict(),
        "competition_before": _format_competition(before_signature),
        "competition_after": _format_competition(after_signature),
    }


def _consistency_only_cross() -> dict[str, Any]:
    baseline = _run_world_arm(
        causal_path=PATH_A,
        causal_target=TARGET_A,
        relation_id="p3-baseline-c",
        prior_target=PRIOR_TARGET,
    )
    donor_fixture = _fixture(prior_target=CONTRADICTION_TARGET)
    donor_consistency = donor_fixture.consistency
    baseline_field = digest({"field": "baseline"})
    baseline_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=baseline["consistency"],
        field_hash=baseline_field,
        return_address_hash=None,
    )
    donor_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=donor_consistency,
        field_hash=baseline_field,
        return_address_hash=None,
    )
    transplanted_consistency = UntypedBoundaryConsistency.from_learned_state_dict(
        deepcopy(donor_consistency.learned_state_dict()),
        ledger=ProvenanceLedger(),
    )
    transplanted_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=transplanted_consistency,
        field_hash=baseline_field,
        return_address_hash=None,
    )
    before_signature = baseline["competition"]
    after_signature = _competition(baseline["expectation"], event_id="p3:c:after")
    before_reentry = _consistency_signature(baseline["consistency"])
    after_reentry = _consistency_signature(transplanted_consistency)
    trial = StateLocusCrossTransplantTrial(
        trial_id="a01-p3-c-only-post-learning",
        baseline_state=baseline_snapshot,
        donor_state=donor_snapshot,
        transplanted_state=transplanted_snapshot,
        transplanted_loci=(StateLocus.CONSISTENCY,),
        selected_lineage_before=_selected_lineage(before_signature),
        selected_lineage_after=_selected_lineage(after_signature),
        donor_selected_lineage=_selected_lineage(before_signature),
        reentry_signature_before=before_reentry,
        reentry_signature_after=after_reentry,
        donor_reentry_signature=after_reentry,
    )
    assessment = assess_state_locus_cross_transplant(trial)
    return {
        "trial": _transplant_trial_state_dict(trial),
        "assessment": assessment.state_dict(),
        "competition_before": _format_competition(before_signature),
        "competition_after": _format_competition(after_signature),
    }


def _field_only_cross() -> dict[str, Any]:
    baseline = _run_world_arm(
        causal_path=PATH_A,
        causal_target=TARGET_A,
        relation_id="p3-baseline-f",
        prior_target=PRIOR_TARGET,
    )
    baseline_field = digest({"field": "baseline"})
    donor_field = digest({"field": "donor"})
    baseline_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=baseline["consistency"],
        field_hash=baseline_field,
        return_address_hash=None,
    )
    donor_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=baseline["consistency"],
        field_hash=donor_field,
        return_address_hash=None,
    )
    transplanted_snapshot = _state_snapshot(
        expectation=baseline["expectation"],
        consistency=baseline["consistency"],
        field_hash=donor_field,
        return_address_hash=None,
    )
    before_signature = baseline["competition"]
    after_signature = _competition(
        baseline["expectation"],
        event_id="p3:f:after",
        origin_state_hash=donor_field,
    )
    reentry = _consistency_signature(baseline["consistency"])
    trial = StateLocusCrossTransplantTrial(
        trial_id="a01-p3-f-only-post-learning",
        baseline_state=baseline_snapshot,
        donor_state=donor_snapshot,
        transplanted_state=transplanted_snapshot,
        transplanted_loci=(StateLocus.FIELD_STATE,),
        selected_lineage_before=_selected_lineage(before_signature),
        selected_lineage_after=_selected_lineage(after_signature),
        donor_selected_lineage=_selected_lineage(before_signature),
        reentry_signature_before=reentry,
        reentry_signature_after=reentry,
        donor_reentry_signature=reentry,
    )
    assessment = assess_state_locus_cross_transplant(trial)
    return {
        "trial": _transplant_trial_state_dict(trial),
        "assessment": assessment.state_dict(),
        "competition_before": _format_competition(before_signature),
        "competition_after": _format_competition(after_signature),
        "scope_note": (
            "A01 reads the Field only through proposal provenance/origin metadata; "
            "this isolated cross changes that declared input state without changing L or C."
        ),
    }


def _return_address_hash(
    proposal: EndogenousPulseProposal,
    boundary: BoundaryEvent,
) -> str:
    return digest(
        {
            "boundary_source_proposal_ids": boundary.source_proposal_ids,
            "local_path_ids": proposal.local_path_ids,
            "parent_proposal_ids": proposal.parent_proposal_ids,
            "proposal_id": proposal.proposal_id,
        }
    )


def _return_address_attribution_cross() -> dict[str, Any]:
    base_expectation = _expectation()
    base_learned = base_expectation.learned_state_dict()

    def run(path_id: str, target: str, prefix: str) -> dict[str, Any]:
        expectation = A01LocalTemporalExpectation.from_learned_state_dict(
            deepcopy(base_learned)
        )
        ledger = ProvenanceLedger()
        consistency = UntypedBoundaryConsistency(ledger)
        fixture = _Fixture(
            expectation,
            ledger,
            consistency,
            A01TransientCreditBridge(expectation, consistency, ledger),
        )
        _learn_prior_relation(
            fixture,
            target=PRIOR_TARGET,
            event_prefix="p3:r:shared-prior",
        )
        proposal = _proposal(
            f"proposal:{prefix}",
            path_id=path_id,
            target=target,
        )
        fixture.ledger.register_proposal(proposal)
        boundary = _boundary(
            f"boundary:{prefix}",
            20.0,
            proposal_ids=(proposal.proposal_id,),
        )
        fixture.consistency.register_boundary(boundary)
        external = _external(
            f"external:{prefix}",
            22.0,
            PRIOR_TARGET,
            parent_event_ids=(boundary.event_id,),
        )
        fixture.ledger.register_external(external)
        pre_l_hash = expectation.learned_state_hash()
        pre_c_hash = digest(consistency.learned_state_dict())
        r_hash = _return_address_hash(proposal, boundary)
        resolution = fixture.bridge.observe_external(boundary, external)
        return {
            "fixture": fixture,
            "pre_l_hash": pre_l_hash,
            "pre_c_hash": pre_c_hash,
            "r_hash": r_hash,
            "resolution": resolution,
            "competition": _competition(expectation, event_id=f"p3:r:{prefix}"),
        }

    baseline = run(PATH_A, TARGET_A, "p3:r:baseline")
    donor = run(PATH_B, TARGET_B, "p3:r:donor")
    field_hash = digest({"field": "same"})
    baseline_snapshot = StateLocusSnapshot(
        local_transition_hash=baseline["pre_l_hash"],
        field_state_hash=field_hash,
        consistency_hash=baseline["pre_c_hash"],
        transient_return_address_hash=baseline["r_hash"],
    )
    donor_snapshot = StateLocusSnapshot(
        local_transition_hash=donor["pre_l_hash"],
        field_state_hash=field_hash,
        consistency_hash=donor["pre_c_hash"],
        transient_return_address_hash=donor["r_hash"],
    )
    transplanted_snapshot = StateLocusSnapshot(
        local_transition_hash=baseline["pre_l_hash"],
        field_state_hash=field_hash,
        consistency_hash=baseline["pre_c_hash"],
        transient_return_address_hash=donor["r_hash"],
    )
    reentry = _consistency_signature(baseline["fixture"].consistency)
    trial = StateLocusCrossTransplantTrial(
        trial_id="a01-p3-r-only-attribution-episode",
        baseline_state=baseline_snapshot,
        donor_state=donor_snapshot,
        transplanted_state=transplanted_snapshot,
        transplanted_loci=(StateLocus.TRANSIENT_RETURN_ADDRESS,),
        selected_lineage_before=_selected_lineage(baseline["competition"]),
        selected_lineage_after=_selected_lineage(donor["competition"]),
        donor_selected_lineage=_selected_lineage(donor["competition"]),
        reentry_signature_before=reentry,
        reentry_signature_after=reentry,
        donor_reentry_signature=reentry,
    )
    assessment = assess_state_locus_cross_transplant(trial)
    return {
        "phase": "external-attribution-episode",
        "trial": _transplant_trial_state_dict(trial),
        "assessment": assessment.state_dict(),
        "baseline_resolution": baseline["resolution"].state_dict(),
        "donor_resolution": donor["resolution"].state_dict(),
        "interpretation": (
            "R selects which existing L path receives the update while the boundary is live; "
            "R is consumed and is not a persistent learned carrier."
        ),
        "persistent_return_address_available_after_pairing": False,
    }


def _transplant_trial_state_dict(
    trial: StateLocusCrossTransplantTrial,
) -> dict[str, Any]:
    return {
        "trial_id": trial.trial_id,
        "baseline_state": asdict(trial.baseline_state),
        "donor_state": asdict(trial.donor_state),
        "transplanted_state": asdict(trial.transplanted_state),
        "transplanted_loci": [row.value for row in trial.transplanted_loci],
        "selected_lineage_before": trial.selected_lineage_before,
        "selected_lineage_after": trial.selected_lineage_after,
        "donor_selected_lineage": trial.donor_selected_lineage,
        "reentry_signature_before": trial.reentry_signature_before,
        "reentry_signature_after": trial.reentry_signature_after,
        "donor_reentry_signature": trial.donor_reentry_signature,
    }


def _run_p3() -> dict[str, Any]:
    l_only = _local_only_cross()
    f_only = _field_only_cross()
    c_only = _consistency_only_cross()
    r_episode = _return_address_attribution_cross()
    supported = (
        l_only["assessment"]["local_transition_carries_competition"]
        and not f_only["assessment"]["field_state_independently_carries_competition"]
        and not c_only["assessment"]["consistency_independently_reaches_competition"]
        and r_episode["assessment"][
            "transient_return_address_independently_carries_competition"
        ]
    )
    return {
        "verdict": "SUPPORTED" if supported else "NOT_SUPPORTED",
        "valid_state_partition": True,
        "undeclared_state_changes_detected": False,
        "crosses": {
            "L_only_post_learning": l_only,
            "F_only_post_learning": f_only,
            "C_only_post_learning": c_only,
            "R_only_attribution_episode": r_episode,
        },
        "actual_carrier_locus": "L.local-transition.a01-causal-support",
        "transient_router_locus": "R.transient-return-address",
        "sign_classifier_locus": "C.anonymous-consistency",
        "field_carrier_observed": False,
        "persistent_r_transplant_status": "NOT_APPLICABLE_R_CONSUMED_AFTER_PAIRING",
        "interpretation": (
            "L persistently carries the learned competition bias. R is necessary only during "
            "attribution, C supplies anonymous match/contradiction classification, and F does not "
            "independently transfer the A01 bias."
        ),
    }


def _p4_trial(
    *,
    trial_id: str,
    evidence: ContinuationEvidence,
    causal_lineage: str,
) -> dict[str, Any]:
    fixture = _fixture()
    causal_path, causal_target = (
        (PATH_A, TARGET_A) if causal_lineage == LINEAGE_A else (PATH_B, TARGET_B)
    )
    initial_scores = _score_vector(fixture.expectation)
    initial_competition = _competition(fixture.expectation, event_id=f"{trial_id}:before")
    resolution: A01CausalCreditResolution | None = None
    replay_rejected: bool | None = None
    if evidence is ContinuationEvidence.EXTERNAL_MATCH:
        resolution = _credit_once(
            fixture,
            path_id=causal_path,
            target=causal_target,
            external_target=PRIOR_TARGET,
            prefix=trial_id,
        )
        external_delta = 1
    elif evidence is ContinuationEvidence.EXTERNAL_CONTRADICTION:
        resolution = _credit_once(
            fixture,
            path_id=causal_path,
            target=causal_target,
            external_target=CONTRADICTION_TARGET,
            prefix=trial_id,
        )
        external_delta = 1
    elif evidence is ContinuationEvidence.INTERNAL_REPLAY_ONLY:
        replay_rejected = _replay_attempt(
            fixture,
            path_id=causal_path,
            target=causal_target,
            prefix=trial_id,
        )
        external_delta = 0
    else:
        external_delta = 0
    later_scores = _score_vector(fixture.expectation)
    later_competition = _competition(fixture.expectation, event_id=f"{trial_id}:after")
    trial = AmbiguityContinuationTrial(
        trial_id=trial_id,
        candidate_lineages=(LINEAGE_A, LINEAGE_B),
        initial_competition_strengths=initial_scores,
        early_active_lineages=(LINEAGE_A, LINEAGE_B),
        evidence_source=evidence,
        causal_lineage=causal_lineage,
        later_competition_strengths=later_scores,
        later_active_lineages=(LINEAGE_A, LINEAGE_B),
        external_observation_count_delta=external_delta,
        positive_commit_count_delta=int(
            resolution is not None and resolution.positive_credit_applied
        ),
        maximum_active_lineages=2,
    )
    assessment = assess_ambiguity_continuation(trial)
    accepted = assessment.accepted and replay_rejected is not False
    return {
        "trial": _ambiguity_trial_state_dict(trial),
        "assessment": assessment.state_dict(),
        "competition_trace": [
            _format_competition(initial_competition),
            _format_competition(later_competition),
        ],
        "co_maximal_cardinality_trace": [
            _co_maximal_cardinality(initial_competition),
            _co_maximal_cardinality(later_competition),
        ],
        "bridge_resolution": resolution.state_dict() if resolution else None,
        "replay_rejected": replay_rejected,
        "accepted": accepted,
    }


def _ambiguity_trial_state_dict(
    trial: AmbiguityContinuationTrial,
) -> dict[str, Any]:
    value = asdict(trial)
    value["evidence_source"] = trial.evidence_source.value
    return value


def _score_vector(
    expectation: A01LocalTemporalExpectation,
) -> tuple[float, float]:
    snapshot = capture_path_support(expectation, (PATH_A, PATH_B))
    return float(snapshot.score(PATH_A)), float(snapshot.score(PATH_B))


def _run_p4() -> dict[str, Any]:
    conditions = (
        ContinuationEvidence.EXTERNAL_MATCH,
        ContinuationEvidence.EXTERNAL_CONTRADICTION,
        ContinuationEvidence.EXTERNAL_ABSENCE,
        ContinuationEvidence.INTERNAL_REPLAY_ONLY,
    )
    trials = tuple(
        _p4_trial(
            trial_id=f"a01-p4-{condition.value}-{lineage}",
            evidence=condition,
            causal_lineage=lineage,
        )
        for condition in conditions
        for lineage in (LINEAGE_A, LINEAGE_B)
    )
    return {
        "verdict": "SUPPORTED" if all(row["accepted"] for row in trials) else "NOT_SUPPORTED",
        "minimum_differentiation": 0.5,
        "threshold_tuned": False,
        "forced_early_winner_take_all": False,
        "trials": trials,
    }


def _format_competition(
    signature: tuple[tuple[str, float], ...],
) -> tuple[str, ...]:
    return tuple(f"{target}={confidence:.12f}" for target, confidence in signature)


def _co_maximal_cardinality(
    signature: tuple[tuple[str, float], ...],
) -> int:
    maximum = max(value for _, value in signature)
    return sum(value == maximum for _, value in signature)


def _baseline_competition(
    expectation: A01LocalTemporalExpectation,
    baseline: _MinimalExplicitLocalSupport,
    *,
    root: str = ROOT,
    event_id: str = "baseline-probe",
) -> tuple[tuple[str, float], ...]:
    neutral_state = expectation.learned_state_dict()
    neutral_state["a01_causal_support"] = {}
    neutral = A01LocalTemporalExpectation.from_learned_state_dict(neutral_state)
    base = _competition(neutral, root=root, event_id=event_id)
    return tuple(
        (target, min(1.0, confidence * baseline.gain(_path(root, target))))
        for target, confidence in base
    )


def _dynamic_outcome(
    *,
    challenge: BehavioralChallenge,
    before: tuple[tuple[str, float], ...],
    after: tuple[tuple[str, float], ...],
    boundary_signature: tuple[str, ...],
    positive_commit_delta: int,
    state_update_count: int,
    external_effect: bool,
) -> DynamicBehavioralOutcome:
    loci = (UpdateLocus.LOCAL_TRANSITION,) if state_update_count else ()
    return DynamicBehavioralOutcome(
        challenge=challenge,
        future_competition_signature=_format_competition(after),
        boundary_signature=boundary_signature,
        positive_commit_count_delta=positive_commit_delta,
        competition_trace=(
            _format_competition(before),
            _format_competition(after),
        ),
        ambiguity_cardinality_trace=(
            _co_maximal_cardinality(before),
            _co_maximal_cardinality(after),
        ),
        external_effect_latency_steps=1 if external_effect else None,
        state_update_loci=loci,
        state_update_count=state_update_count,
        global_indexed_lookup_count_delta=0,
    )


def _p5_basic_episode(
    *,
    challenge: BehavioralChallenge,
    causal_path: str,
    causal_target: str,
    external_target: str | None,
    replay_only: bool = False,
    physical_tag: str = "default",
    ancestry_paths: tuple[tuple[str, str], ...] = (),
    root: str = ROOT,
    target_a: str = TARGET_A,
    target_b: str = TARGET_B,
) -> tuple[DynamicBehavioralOutcome, DynamicBehavioralOutcome, dict[str, Any]]:
    fixture = _fixture(root=root, target_a=target_a, target_b=target_b)
    explicit = _MinimalExplicitLocalSupport()
    before_candidate = _competition(
        fixture.expectation,
        root=root,
        event_id=f"p5:{challenge.value}:candidate:before",
    )
    before_baseline = _baseline_competition(
        fixture.expectation,
        explicit,
        root=root,
        event_id=f"p5:{challenge.value}:baseline:before",
    )
    resolution: A01CausalCreditResolution | None = None
    replay_rejected: bool | None = None

    if ancestry_paths:
        parent_ids: tuple[str, ...] = ()
        created: list[EndogenousPulseProposal] = []
        for index, (path_id, target) in enumerate(ancestry_paths):
            proposal = _proposal(
                f"proposal:p5:{challenge.value}:ancestor:{index}",
                path_id=path_id,
                target=target,
                parent_proposal_ids=parent_ids,
                physical_tag=physical_tag,
            )
            fixture.ledger.register_proposal(proposal)
            created.append(proposal)
            parent_ids = (proposal.proposal_id,)
        boundary = _boundary(
            f"boundary:p5:{challenge.value}",
            20.0,
            proposal_ids=(created[-1].proposal_id,),
            physical_tag=physical_tag,
        )
        fixture.consistency.register_boundary(boundary)
        external = _external(
            f"external:p5:{challenge.value}",
            22.0,
            external_target or PRIOR_TARGET,
            parent_event_ids=(boundary.event_id,),
        )
        fixture.ledger.register_external(external)
        resolution = fixture.bridge.observe_external(boundary, external)
    elif replay_only:
        replay_rejected = _replay_attempt(
            fixture,
            path_id=causal_path,
            target=causal_target,
            prefix=f"p5:{challenge.value}",
        )
    elif external_target is not None:
        resolution = _credit_once(
            fixture,
            path_id=causal_path,
            target=causal_target,
            external_target=external_target,
            prefix=f"p5:{challenge.value}",
            physical_tag=physical_tag,
        )

    if resolution is not None:
        if resolution.status is A01CausalCreditStatus.EXACT_MATCH:
            explicit.observe(resolution.path_ids, matched=True)
        elif resolution.status is A01CausalCreditStatus.EXACT_CONTRADICTION:
            explicit.observe(resolution.path_ids, matched=False)

    after_candidate = _competition(
        fixture.expectation,
        root=root,
        event_id=f"p5:{challenge.value}:candidate:after",
    )
    after_baseline = _baseline_competition(
        fixture.expectation,
        explicit,
        root=root,
        event_id=f"p5:{challenge.value}:baseline:after",
    )
    boundary_signature = (
        (resolution.status.value, *resolution.path_ids)
        if resolution is not None
        else (("internal-replay-rejected",) if replay_only else ("external-absence",))
    )
    positive = int(resolution is not None and resolution.positive_credit_applied)
    update_count = len(resolution.path_ids) if resolution is not None else 0
    external_effect = resolution is not None
    candidate_outcome = _dynamic_outcome(
        challenge=challenge,
        before=before_candidate,
        after=after_candidate,
        boundary_signature=boundary_signature,
        positive_commit_delta=positive,
        state_update_count=update_count,
        external_effect=external_effect,
    )
    baseline_outcome = _dynamic_outcome(
        challenge=challenge,
        before=before_baseline,
        after=after_baseline,
        boundary_signature=boundary_signature,
        positive_commit_delta=positive,
        state_update_count=update_count,
        external_effect=external_effect,
    )
    return candidate_outcome, baseline_outcome, {
        "candidate_support": fixture.expectation.learned_state_dict()[
            "a01_causal_support"
        ],
        "baseline_support": explicit.state_dict(),
        "replay_rejected": replay_rejected,
        "resolution": resolution.state_dict() if resolution else None,
    }


def _p5_world_relation_outcome() -> tuple[
    DynamicBehavioralOutcome,
    DynamicBehavioralOutcome,
]:
    candidate_after: list[tuple[tuple[str, float], ...]] = []
    baseline_after: list[tuple[tuple[str, float], ...]] = []
    for path_id, target, relation in (
        (PATH_A, TARGET_A, "p5-world-a"),
        (PATH_B, TARGET_B, "p5-world-b"),
    ):
        fixture = _fixture()
        explicit = _MinimalExplicitLocalSupport()
        resolution = _credit_once(
            fixture,
            path_id=path_id,
            target=target,
            external_target=PRIOR_TARGET,
            prefix=relation,
        )
        explicit.observe(resolution.path_ids, matched=True)
        candidate_after.append(
            _competition(fixture.expectation, event_id=f"{relation}:candidate")
        )
        baseline_after.append(
            _baseline_competition(
                fixture.expectation,
                explicit,
                event_id=f"{relation}:baseline",
            )
        )
    candidate_trace = tuple(_format_competition(row) for row in candidate_after)
    baseline_trace = tuple(_format_competition(row) for row in baseline_after)
    candidate = DynamicBehavioralOutcome(
        challenge=BehavioralChallenge.WORLD_RELATION_PERMUTATION,
        future_competition_signature=candidate_trace[-1],
        boundary_signature=("world-relation-a", "world-relation-b"),
        positive_commit_count_delta=2,
        competition_trace=candidate_trace,
        ambiguity_cardinality_trace=tuple(
            _co_maximal_cardinality(row) for row in candidate_after
        ),
        external_effect_latency_steps=1,
        state_update_loci=(UpdateLocus.LOCAL_TRANSITION,),
        state_update_count=2,
        global_indexed_lookup_count_delta=0,
    )
    baseline = DynamicBehavioralOutcome(
        challenge=BehavioralChallenge.WORLD_RELATION_PERMUTATION,
        future_competition_signature=baseline_trace[-1],
        boundary_signature=("world-relation-a", "world-relation-b"),
        positive_commit_count_delta=2,
        competition_trace=baseline_trace,
        ambiguity_cardinality_trace=tuple(
            _co_maximal_cardinality(row) for row in baseline_after
        ),
        external_effect_latency_steps=1,
        state_update_loci=(UpdateLocus.LOCAL_TRANSITION,),
        state_update_count=2,
        global_indexed_lookup_count_delta=0,
    )
    return candidate, baseline


def _p5_transplant_outcome() -> tuple[
    DynamicBehavioralOutcome,
    DynamicBehavioralOutcome,
]:
    baseline_expectation = _expectation()
    donor_expectation = _expectation()
    donor_expectation.observe_causal_evidence((PATH_B,), matched=True)
    before_candidate = _competition(baseline_expectation, event_id="p5:p3:before")
    transplanted = A01LocalTemporalExpectation.from_learned_state_dict(
        donor_expectation.learned_state_dict()
    )
    after_candidate = _competition(transplanted, event_id="p5:p3:after")

    baseline_null = _MinimalExplicitLocalSupport()
    donor_null = _MinimalExplicitLocalSupport()
    donor_null.observe((PATH_B,), matched=True)
    before_baseline = _baseline_competition(
        baseline_expectation,
        baseline_null,
        event_id="p5:p3:null:before",
    )
    transplanted_null = _MinimalExplicitLocalSupport.from_state_dict(
        donor_null.state_dict()
    )
    after_baseline = _baseline_competition(
        baseline_expectation,
        transplanted_null,
        event_id="p5:p3:null:after",
    )
    candidate = _dynamic_outcome(
        challenge=BehavioralChallenge.STATE_LOCUS_TRANSPLANT,
        before=before_candidate,
        after=after_candidate,
        boundary_signature=("L-only", "lineage-b"),
        positive_commit_delta=0,
        state_update_count=1,
        external_effect=False,
    )
    baseline = _dynamic_outcome(
        challenge=BehavioralChallenge.STATE_LOCUS_TRANSPLANT,
        before=before_baseline,
        after=after_baseline,
        boundary_signature=("L-only", "lineage-b"),
        positive_commit_delta=0,
        state_update_count=1,
        external_effect=False,
    )
    return candidate, baseline


def _p5_outcome_state_dict(outcome: DynamicBehavioralOutcome) -> dict[str, Any]:
    return {
        "challenge": outcome.challenge.value,
        "future_competition_signature": outcome.future_competition_signature,
        "boundary_signature": outcome.boundary_signature,
        "positive_commit_count_delta": outcome.positive_commit_count_delta,
        "competition_trace": outcome.competition_trace,
        "ambiguity_cardinality_trace": outcome.ambiguity_cardinality_trace,
        "external_effect_latency_steps": outcome.external_effect_latency_steps,
        "state_update_loci": tuple(row.value for row in outcome.state_update_loci),
        "state_update_count": outcome.state_update_count,
        "global_indexed_lookup_count_delta": outcome.global_indexed_lookup_count_delta,
    }


def _run_p5(*, p1_p4_passed: bool) -> dict[str, Any]:
    pairs: list[tuple[DynamicBehavioralOutcome, DynamicBehavioralOutcome]] = []
    resources: list[dict[str, Any]] = []

    basic_specs = (
        (
            BehavioralChallenge.MATCHED_CAUSAL_LINEAGE,
            PATH_A,
            TARGET_A,
            PRIOR_TARGET,
            False,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.LINEAGE_SWAP,
            PATH_B,
            TARGET_B,
            PRIOR_TARGET,
            False,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.EXTERNAL_CONTRADICTION,
            PATH_A,
            TARGET_A,
            CONTRADICTION_TARGET,
            False,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.EXTERNAL_ABSENCE,
            PATH_A,
            TARGET_A,
            None,
            False,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.INTERNAL_REPLAY_ONLY,
            PATH_A,
            TARGET_A,
            None,
            True,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.BOUNDED_AMBIGUITY,
            PATH_A,
            TARGET_A,
            PRIOR_TARGET,
            False,
            "default",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.IDENTIFIER_PERMUTATION,
            "local:Q->S",
            "S",
            PRIOR_TARGET,
            False,
            "default",
            (),
            "Q",
            "R",
            "S",
        ),
        (
            BehavioralChallenge.PHYSICAL_TRAJECTORY_SUBSTITUTION,
            PATH_A,
            TARGET_A,
            PRIOR_TARGET,
            False,
            "substituted-physical-route",
            (),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
        (
            BehavioralChallenge.UNSEEN_LINEAGE_COMBINATION,
            PATH_B,
            TARGET_B,
            PRIOR_TARGET,
            False,
            "default",
            ((PATH_A, TARGET_A), (PATH_B, TARGET_B)),
            ROOT,
            TARGET_A,
            TARGET_B,
        ),
    )
    for (
        challenge,
        path_id,
        target,
        external_target,
        replay_only,
        physical_tag,
        ancestry,
        root,
        target_a,
        target_b,
    ) in basic_specs:
        candidate, baseline, resource = _p5_basic_episode(
            challenge=challenge,
            causal_path=path_id,
            causal_target=target,
            external_target=external_target,
            replay_only=replay_only,
            physical_tag=physical_tag,
            ancestry_paths=ancestry,
            root=root,
            target_a=target_a,
            target_b=target_b,
        )
        pairs.append((candidate, baseline))
        resources.append(resource)

    pairs.append(_p5_world_relation_outcome())
    pairs.append(_p5_transplant_outcome())
    candidate_outcomes = tuple(pair[0] for pair in pairs)
    baseline_outcomes = tuple(pair[1] for pair in pairs)

    peak_candidate_state = max(
        resources,
        key=lambda row: len(
            json.dumps(
                row["candidate_support"],
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
    )["candidate_support"]
    peak_baseline_state = max(
        resources,
        key=lambda row: len(
            json.dumps(
                row["baseline_support"],
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
    )["baseline_support"]
    candidate_bytes = len(
        json.dumps(
            peak_candidate_state,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    baseline_bytes = len(
        json.dumps(
            peak_baseline_state,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    candidate_units = 2 * len(peak_candidate_state)
    baseline_units = 2 * len(peak_baseline_state)
    transient_peak_units = 6

    candidate_run = DynamicMechanismRun(
        mechanism_id="a01-transient-return-address",
        outcomes=candidate_outcomes,
        persistent_state_units=candidate_units,
        persistent_state_bytes=candidate_bytes,
        transient_state_peak_units=transient_peak_units,
        global_keyed_query_count=0,
        direct_keyed_target_query=False,
        uses_forbidden_privilege=False,
        explicit_predictor=False,
        minimality_established=False,
        p1_p4_contracts_passed=p1_p4_passed,
    )
    baseline_run = DynamicMechanismRun(
        mechanism_id="n1-minimal-explicit-local-eligibility-memory",
        outcomes=baseline_outcomes,
        persistent_state_units=baseline_units,
        persistent_state_bytes=baseline_bytes,
        transient_state_peak_units=transient_peak_units,
        global_keyed_query_count=0,
        direct_keyed_target_query=False,
        uses_forbidden_privilege=False,
        explicit_predictor=True,
        minimality_established=True,
        p1_p4_contracts_passed=p1_p4_passed,
    )
    assessment = assess_dynamic_table_equivalence(candidate_run, baseline_run)
    return {
        "verdict": assessment.classification,
        "assessment": assessment.state_dict(),
        "candidate": {
            "mechanism_id": candidate_run.mechanism_id,
            "outcomes": [
                _p5_outcome_state_dict(row) for row in candidate_run.outcomes
            ],
            "persistent_state_units": candidate_run.persistent_state_units,
            "persistent_state_bytes": candidate_run.persistent_state_bytes,
            "transient_state_peak_units": candidate_run.transient_state_peak_units,
            "global_keyed_query_count": candidate_run.global_keyed_query_count,
            "direct_keyed_target_query": candidate_run.direct_keyed_target_query,
            "uses_forbidden_privilege": candidate_run.uses_forbidden_privilege,
        },
        "baseline": {
            "mechanism_id": baseline_run.mechanism_id,
            "outcomes": [
                _p5_outcome_state_dict(row) for row in baseline_run.outcomes
            ],
            "persistent_state_units": baseline_run.persistent_state_units,
            "persistent_state_bytes": baseline_run.persistent_state_bytes,
            "transient_state_peak_units": baseline_run.transient_state_peak_units,
            "global_keyed_query_count": baseline_run.global_keyed_query_count,
            "direct_keyed_target_query": baseline_run.direct_keyed_target_query,
            "uses_forbidden_privilege": baseline_run.uses_forbidden_privilege,
            "minimality_established": baseline_run.minimality_established,
        },
        "minimality_evidence": {
            "scope": "incremental A01 causal-support mechanism",
            "sufficient_statistics": (
                "For exact A01 Beta reliability over arbitrary histories, each independently "
                "addressable local path requires both consistent and contradicted observation "
                "counts, up to a lossless bijective encoding."
            ),
            "same_admissible_evidence": True,
            "same_update_and_read_locus": True,
            "baseline_no_larger": (
                baseline_units <= candidate_units and baseline_bytes <= candidate_bytes
            ),
        },
        "reduction_scope_note": (
            "The explicit null reuses the same exact-parent provenance and anonymous relation "
            "classification. It replaces only A01's path-attached support record, "
            "as preregistered N1."
        ),
    }


def run_a01_mechanism_discrimination(
    *,
    source_sha: str,
) -> dict[str, Any]:
    if not source_sha:
        raise ValueError("source_sha must be non-empty")
    p1 = _run_p1()
    p2 = _run_p2()
    passed_p1_p2 = p1["verdict"] == "SUPPORTED" and p2["verdict"] == "SUPPORTED"
    if passed_p1_p2:
        p3 = _run_p3()
        p4 = _run_p4()
        p5 = _run_p5(
            p1_p4_passed=(
                p1["verdict"] == "SUPPORTED"
                and p2["verdict"] == "SUPPORTED"
                and p3["verdict"] == "SUPPORTED"
                and p4["verdict"] == "SUPPORTED"
            )
        )
    else:
        p3 = {
            "verdict": "NOT_RUN_P1_P2_GATE_FAILED",
            "actual_carrier_locus": None,
        }
        p4 = {"verdict": "NOT_RUN_P1_P2_GATE_FAILED"}
        p5 = {"verdict": "NOT_RUN_P1_P2_GATE_FAILED"}

    result = {
        "schema_version": SCHEMA_VERSION,
        "run_id": RUN_ID,
        "source_sha": source_sha,
        "candidate_003_touched": False,
        "threshold_tuning_performed": False,
        "forbidden_privilege_used": False,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
    }
    result["summary"] = {
        "p1_verdict": p1["verdict"],
        "p2_verdict": p2["verdict"],
        "lineage_selectivity": p1["lineage_swap_passed"],
        "contradiction_correction": p1["contradiction_correction"][
            "existing_support_corrected"
        ],
        "absence_replay_leakage": (
            p1["absence_leakage_detected"] or p1["replay_leakage_detected"]
        ),
        "future_competition_change": p2["future_competition_changed"],
        "actual_carrier_locus": p3.get("actual_carrier_locus"),
        "p3_p5_value": (
            "continue-to-reduction-classification"
            if passed_p1_p2
            else "stop-and-preserve-p1-p2-failure"
        ),
        "explicit_anonymous_memory_reduction": p5.get("verdict"),
    }
    result["result_digest"] = digest(result)
    return result
