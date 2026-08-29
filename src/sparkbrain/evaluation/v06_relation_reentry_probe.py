from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.consistency import (
    AnonymousConsistencyConfig,
    UntypedBoundaryConsistency,
)
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)
from sparkbrain.v06.world_boundary import AnonymousBoundaryWorld, AnonymousWorldLink

from .v06_boundary_probe import _build_primary, _run_episode, pulse


@dataclass(frozen=True, slots=True)
class RelationReentryProbeResult:
    condition_id: str
    learned_links: tuple[tuple[str, str, float, int, int], ...]
    boundary_event_id: str
    relation_record_targets: tuple[str, ...]
    relation_record_reliabilities: tuple[float, ...]
    effective_currents: tuple[float, ...]
    accepted_count: int
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    external_observation_count_before_probe: int
    external_observation_count_after_probe: int
    committed_positive_updates_before_probe: int
    committed_positive_updates_after_probe: int
    runtime_state_hash: str
    runtime_state: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationReentryAssessment:
    acquisition_changes_field: bool
    reversal_changes_field: bool
    return_restores_field: bool
    stable_control_stays_stable: bool
    no_reentry_has_no_effect: bool
    consistency_reset_has_no_effect: bool
    unrelated_relation_has_no_effect: bool
    all_links_use_same_projection: bool
    no_external_count_from_reentry: bool
    no_positive_self_confirmation: bool
    taxonomy_free: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalRelationReentrySuite:
    acquisition: RelationReentryProbeResult
    reversal: RelationReentryProbeResult
    return_to_old: RelationReentryProbeResult
    stable: RelationReentryProbeResult
    no_reentry: RelationReentryProbeResult
    consistency_reset: RelationReentryProbeResult
    unrelated_relation: RelationReentryProbeResult
    assessment: RelationReentryAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "acquisition": self.acquisition.state_dict(),
            "assessment": self.assessment.state_dict(),
            "consistency_reset": self.consistency_reset.state_dict(),
            "no_reentry": self.no_reentry.state_dict(),
            "return_to_old": self.return_to_old.state_dict(),
            "reversal": self.reversal.state_dict(),
            "stable": self.stable.state_dict(),
            "unrelated_relation": self.unrelated_relation.state_dict(),
        }


def _world(port_id: str, target: str) -> AnonymousBoundaryWorld:
    return AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id=port_id,
                target=target,
                lag_ms=10.0,
                magnitude=1.0,
            ),
        )
    )


def _train_phases(
    *,
    phases: tuple[tuple[str, int], ...],
    cue_unit_id: int = 0,
    port_id: str = "port:7",
) -> tuple[Any, Any, UntypedBoundaryConsistency, float]:
    runtime, emitter, _, consistency = _build_primary()
    episode_index = 0
    for target, episodes in phases:
        world = _world(port_id, target)
        for _ in range(episodes):
            start_ms = 100.0 + episode_index * 70.0
            _run_episode(
                runtime,
                emitter,
                world,
                consistency,
                cue_unit_id=cue_unit_id,
                start_ms=start_ms,
                episode_id=f"train:{port_id}:{target}:{episode_index}",
            )
            episode_index += 1
    return runtime, emitter, consistency, 100.0 + episode_index * 70.0


def _learned_links(
    consistency: UntypedBoundaryConsistency,
) -> tuple[tuple[str, str, float, int, int], ...]:
    rows = []
    for value in consistency.state_dict()["links"].values():
        rows.append(
            (
                str(value["port_id"]),
                str(value["target"]),
                float(value["reliability"]),
                int(value["consistent_count"]),
                int(value["inconsistent_count"]),
            )
        )
    return tuple(sorted(rows))


def _run_probe(
    *,
    condition_id: str,
    phases: tuple[tuple[str, int], ...],
    reentry_enabled: bool = True,
    reset_consistency: bool = False,
    cue_unit_id: int = 0,
    learned_port_id: str = "port:7",
) -> RelationReentryProbeResult:
    runtime, emitter, consistency, probe_start_ms = _train_phases(
        phases=phases,
        cue_unit_id=cue_unit_id,
        port_id=learned_port_id,
    )
    learned_before_reset = _learned_links(consistency)
    active_consistency = consistency
    if reset_consistency:
        active_consistency = UntypedBoundaryConsistency(
            runtime.ledger,
            AnonymousConsistencyConfig(
                maximum_pair_lag_ms=20.0,
                pending_ttl_ms=30.0,
            ),
        )

    before_chain = len(runtime.generated_sparks)
    runtime.present_external(pulse(f"probe:{condition_id}", probe_start_ms, 0))
    runtime.advance_silence(probe_start_ms + 15.0)
    chain_sparks = tuple(runtime.generated_sparks[before_chain:])
    boundary_events = tuple(
        event
        for event in emitter.emit(
            chain_sparks,
            source_state_hash=runtime.state_hash(),
        )
        if event.port_id == "port:7"
    )
    if len(boundary_events) != 1:
        raise RuntimeError("relation re-entry probe requires exactly one port:7 event")
    boundary = boundary_events[0]

    external_before = runtime.ledger.external_observation_count
    updates_before = runtime.ledger.committed_positive_updates
    generated_before = len(runtime.generated_sparks)
    reentry = AnonymousRelationReentry(
        active_consistency,
        runtime.ledger,
        runtime.reinjection,
        RelationReentryConfig(
            delay_ms=1.0,
            magnitude_gain=0.9,
            maximum_magnitude=2.0,
            minimum_consistent_count=1,
            minimum_reliability=0.0,
            proposal_ttl_ms=10.0,
            maximum_links_per_boundary=8,
        ),
    )
    records = reentry.schedule(boundary, runtime.field) if reentry_enabled else ()
    runtime.advance_silence(probe_start_ms + 17.0)
    generated = tuple(runtime.generated_sparks[generated_before:])
    runtime_state = {
        "active_consistency": active_consistency.state_dict(),
        "chain": runtime.state_dict(),
        "reentry": reentry.state_dict(),
    }
    return RelationReentryProbeResult(
        condition_id=condition_id,
        learned_links=learned_before_reset,
        boundary_event_id=boundary.event_id,
        relation_record_targets=tuple(row.target for row in records),
        relation_record_reliabilities=tuple(row.reliability for row in records),
        effective_currents=tuple(
            row.reinjection.effective_current for row in records
        ),
        accepted_count=sum(row.reinjection.accepted for row in records),
        generated_units=tuple(row.unit_id for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        external_observation_count_before_probe=external_before,
        external_observation_count_after_probe=(
            runtime.ledger.external_observation_count
        ),
        committed_positive_updates_before_probe=updates_before,
        committed_positive_updates_after_probe=(
            runtime.ledger.committed_positive_updates
        ),
        runtime_state_hash=runtime.state_hash(),
        runtime_state=runtime_state,
    )


def _currents_match(
    observed: tuple[float, ...],
    expected: tuple[float, ...],
) -> bool:
    return len(observed) == len(expected) and all(
        math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)
        for left, right in zip(observed, expected, strict=True)
    )


def run_canonical_relation_reentry_suite() -> CanonicalRelationReentrySuite:
    acquisition = _run_probe(
        condition_id="acquisition",
        phases=(("unit:8", 3),),
    )
    reversal = _run_probe(
        condition_id="reversal",
        phases=(("unit:8", 3), ("unit:9", 3)),
    )
    returned = _run_probe(
        condition_id="return-to-old",
        phases=(("unit:8", 3), ("unit:9", 3), ("unit:8", 3)),
    )
    stable = _run_probe(
        condition_id="stable",
        phases=(("unit:8", 9),),
    )
    no_reentry = _run_probe(
        condition_id="no-reentry",
        phases=(("unit:8", 3),),
        reentry_enabled=False,
    )
    reset = _run_probe(
        condition_id="consistency-reset",
        phases=(("unit:8", 3),),
        reset_consistency=True,
    )
    unrelated = _run_probe(
        condition_id="unrelated-relation",
        phases=(("unit:9", 3),),
        cue_unit_id=4,
        learned_port_id="port:9",
    )

    all_rows = (
        acquisition,
        reversal,
        returned,
        stable,
        no_reentry,
        reset,
        unrelated,
    )
    no_external = all(
        row.external_observation_count_before_probe
        == row.external_observation_count_after_probe
        for row in all_rows
    )
    no_positive = all(
        row.committed_positive_updates_before_probe
        == row.committed_positive_updates_after_probe
        for row in all_rows
    )
    lowered = str({row.condition_id: row.runtime_state for row in all_rows}).lower()
    forbidden = (
        "assembly_id",
        "relation_type",
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "correct_action",
        "reward_value",
        "utility_target",
        "functional_role",
        "meaning_state",
    )
    same_projection = (
        reversal.relation_record_targets == ("unit:8", "unit:9")
        and reversal.accepted_count == 2
        and _currents_match(reversal.effective_currents, (0.45, 0.72))
    )
    assessment = RelationReentryAssessment(
        acquisition_changes_field=acquisition.generated_units == (8,),
        reversal_changes_field=reversal.generated_units == (9,),
        return_restores_field=returned.generated_units == (8,),
        stable_control_stays_stable=stable.generated_units == (8,),
        no_reentry_has_no_effect=no_reentry.generated_units == (),
        consistency_reset_has_no_effect=reset.generated_units == (),
        unrelated_relation_has_no_effect=unrelated.generated_units == (),
        all_links_use_same_projection=same_projection,
        no_external_count_from_reentry=no_external,
        no_positive_self_confirmation=no_positive,
        taxonomy_free=not any(term in lowered for term in forbidden),
        engineering_candidate=False,
    )
    assessment = RelationReentryAssessment(
        **{
            **assessment.state_dict(),
            "engineering_candidate": all(
                (
                    assessment.acquisition_changes_field,
                    assessment.reversal_changes_field,
                    assessment.return_restores_field,
                    assessment.stable_control_stays_stable,
                    assessment.no_reentry_has_no_effect,
                    assessment.consistency_reset_has_no_effect,
                    assessment.unrelated_relation_has_no_effect,
                    assessment.all_links_use_same_projection,
                    assessment.no_external_count_from_reentry,
                    assessment.no_positive_self_confirmation,
                    assessment.taxonomy_free,
                )
            ),
        }
    )
    return CanonicalRelationReentrySuite(
        acquisition=acquisition,
        reversal=reversal,
        return_to_old=returned,
        stable=stable,
        no_reentry=no_reentry,
        consistency_reset=reset,
        unrelated_relation=unrelated,
        assessment=assessment,
    )
