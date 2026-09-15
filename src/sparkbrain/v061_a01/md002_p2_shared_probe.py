"""Development-only shared-root probe for A01 MD-002 P2.

This module executes the already-fixed four-condition P2 attribution schedule and,
without changing that schedule, observes the actual future proposal competition
from the preregistered shared root. It is development-only: no held-out/formal
execution is opened and no threshold is tuned from observed outputs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v06.foundation import (
    EventOrigin,
    RuntimePulse,
    validate_runtime_mapping,
)

from .credit_bridge import A01CausalCreditStatus, A01TransientCreditBridge
from .md002_development_plan import (
    P2DevelopmentConditionInput,
    build_p2_development_plan,
)
from .md002_fixtures import P2WorldOnlyFixture
from .md002_p2_schedule import (
    P2AttributionSubepisode,
    P2ClonedSubepisodeSchedule,
)
from .md002_restore_adapter import RestoredA01P2Arm, restore_a01_p2_arm
from .md002_world_fixture import P2AnonymousWorldRelation


@dataclass(frozen=True, slots=True)
class P2ProbeProposal:
    target: str
    confidence: float
    predicted_arrival_ms: float
    local_path_ids: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class P2SharedProbeObservation:
    condition_id: str
    world_arm: str
    returned_external_evidence: bool
    proposal_id: str
    requested_target: str
    response_target: str
    resolution_status: str | None
    probe_rows: tuple[P2ProbeProposal, ...]
    selected_targets: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["probe_rows"] = [row.state_dict() for row in self.probe_rows]
        validate_runtime_mapping(
            value,
            path="v061_a01.md002.p2_shared_probe_observation",
        )
        return value


@dataclass(frozen=True, slots=True)
class P2SharedProbeRun:
    observations: tuple[P2SharedProbeObservation, ...]
    verdict: str
    criteria: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        value = {
            "schema": "v061-a01-md002-p2-shared-probe-v1",
            "observations": [row.state_dict() for row in self.observations],
            "verdict": self.verdict,
            "criteria": list(self.criteria),
            "development_only": True,
            "held_out_executed": False,
            "formal_execution_opened": False,
            "threshold_tuned": False,
        }
        validate_runtime_mapping(
            value,
            path="v061_a01.md002.p2_shared_probe_run",
        )
        return value


def _probe_rows(
    restored: RestoredA01P2Arm,
    schedule: P2ClonedSubepisodeSchedule,
) -> tuple[P2ProbeProposal, ...]:
    cue = RuntimePulse(
        event_id=schedule.shared_probe.cue_event_id,
        time_ms=float(schedule.shared_probe.cue_time_ms),
        target=schedule.shared_probe.root_target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )
    proposals = restored.expectation.proposals_for(
        cue,
        origin_state_hash=schedule.shared_probe.origin_state_hash,
    )
    rows = tuple(
        sorted(
            (
                P2ProbeProposal(
                    target=row.target,
                    confidence=float(row.confidence),
                    predicted_arrival_ms=float(row.predicted_arrival_ms),
                    local_path_ids=tuple(row.local_path_ids),
                )
                for row in proposals
            ),
            key=lambda row: (row.target, row.local_path_ids),
        )
    )
    if len(rows) < 2:
        raise RuntimeError(
            "P2 shared-root probe requires at least two competing proposals"
        )
    return rows


def _selected_targets(rows: tuple[P2ProbeProposal, ...]) -> tuple[str, ...]:
    best = max(row.confidence for row in rows)
    return tuple(sorted(row.target for row in rows if row.confidence == best))


def _execute_observation(
    condition: P2DevelopmentConditionInput,
    subepisode: P2AttributionSubepisode,
) -> P2SharedProbeObservation:
    restored = restore_a01_p2_arm(condition.arm_input)
    if restored.boundary is None:
        raise ValueError(
            "P2 shared-root probe requires a live return-address boundary"
        )
    proposal = restored.ledger.proposals.get(subepisode.proposal_id)
    if proposal is None:
        raise ValueError("scheduled P2 proposal is absent from restored ancestry")

    relation = P2AnonymousWorldRelation.from_state_dict(restored.world_relation)
    response_target = relation.mapping[subepisode.proposal_id]
    boundary = replace(
        restored.boundary,
        event_id=subepisode.boundary_event_id,
        time_ms=float(subepisode.boundary_time_ms),
        source_proposal_ids=(subepisode.proposal_id,),
        generation_depth=proposal.generation_depth,
    )
    restored.consistency.register_boundary(boundary)
    response = RuntimePulse(
        event_id=subepisode.response_event_id,
        time_ms=float(subepisode.response_time_ms),
        target=response_target,
        magnitude=float(boundary.magnitude),
        polarity=int(boundary.polarity),
        origin=EventOrigin.EXTERNAL,
        parent_event_ids=(boundary.event_id,),
    )

    status: str | None = None
    if condition.returned_external_evidence:
        restored.ledger.register_external(response)
        resolution = A01TransientCreditBridge(
            restored.expectation,
            restored.consistency,
            restored.ledger,
        ).observe_external(boundary, response)
        status = resolution.status.value

    rows = _probe_rows(restored, condition.schedule)
    return P2SharedProbeObservation(
        condition_id=condition.condition_id,
        world_arm=condition.world_arm,
        returned_external_evidence=condition.returned_external_evidence,
        proposal_id=subepisode.proposal_id,
        requested_target=proposal.target,
        response_target=response_target,
        resolution_status=status,
        probe_rows=rows,
        selected_targets=_selected_targets(rows),
    )


def _row_map(
    observation: P2SharedProbeObservation,
) -> dict[str, P2ProbeProposal]:
    return {row.target: row for row in observation.probe_rows}


def _score(observations: tuple[P2SharedProbeObservation, ...]) -> str:
    by_key = {
        (row.world_arm, row.returned_external_evidence, row.proposal_id): row
        for row in observations
    }
    proposal_ids = tuple(dict.fromkeys(row.proposal_id for row in observations))
    supported = True
    for proposal_id in proposal_ids:
        statuses: set[str] = set()
        for world_arm in ("control", "intervention"):
            returned = by_key[(world_arm, True, proposal_id)]
            withheld = by_key[(world_arm, False, proposal_id)]
            returned_rows = _row_map(returned)
            withheld_rows = _row_map(withheld)
            if set(returned_rows) != set(withheld_rows):
                supported = False
                continue
            if len(withheld.selected_targets) < 2:
                supported = False
            for target in returned_rows:
                if (
                    returned_rows[target].predicted_arrival_ms
                    != withheld_rows[target].predicted_arrival_ms
                ):
                    supported = False
                if (
                    target != returned.requested_target
                    and returned_rows[target].confidence
                    != withheld_rows[target].confidence
                ):
                    supported = False
            requested_delta = (
                returned_rows[returned.requested_target].confidence
                - withheld_rows[returned.requested_target].confidence
            )
            if (
                returned.resolution_status
                == A01CausalCreditStatus.EXACT_MATCH.value
            ):
                statuses.add("match")
                if (
                    requested_delta <= 0.0
                    or returned.selected_targets != (returned.requested_target,)
                ):
                    supported = False
            elif (
                returned.resolution_status
                == A01CausalCreditStatus.EXACT_CONTRADICTION.value
            ):
                statuses.add("contradiction")
                if (
                    requested_delta >= 0.0
                    or returned.requested_target in returned.selected_targets
                ):
                    supported = False
            else:
                supported = False
        if statuses != {"match", "contradiction"}:
            supported = False
    return "SUPPORTED_SELECTIVE_CIRCULATION" if supported else "NOT_SUPPORTED"


def execute_p2_shared_probe(
    fixture: P2WorldOnlyFixture,
    schedule: P2ClonedSubepisodeSchedule,
) -> P2SharedProbeRun:
    """Execute the fixed development matrix plus the preregistered shared-root probe."""

    fixture.validate()
    schedule.validate()
    conditions = build_p2_development_plan(fixture, schedule)
    observations = tuple(
        _execute_observation(condition, subepisode)
        for condition in conditions
        for subepisode in schedule.subepisodes
    )
    result = P2SharedProbeRun(
        observations=observations,
        verdict=_score(observations),
        criteria=(
            "withheld arms remain co-maximal at the shared root",
            "returned evidence changes only the causally addressed local target confidence",
            "exact-match raises and selects the requested target",
            "exact-contradiction lowers and deselects the requested target",
            "world permutation swaps match/contradiction status for each fixed proposal identity",
            "predicted arrival times remain unchanged by causal-support credit",
        ),
    )
    result.state_dict()
    return result


__all__ = [
    "P2ProbeProposal",
    "P2SharedProbeObservation",
    "P2SharedProbeRun",
    "execute_p2_shared_probe",
]
