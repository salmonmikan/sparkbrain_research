from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.world_boundary import AnonymousBoundaryWorld, AnonymousWorldLink

from .v06_boundary_probe import _build_primary, _run_episode


@dataclass(frozen=True, slots=True)
class RevisionSnapshot:
    phase_id: str
    episode_count: int
    boundary_count: int
    external_observation_count: int
    committed_positive_updates: int
    link_count: int
    old_consistent_count: int
    old_inconsistent_count: int
    old_reliability: float | None
    new_consistent_count: int
    new_inconsistent_count: int
    new_reliability: float | None
    primary_state_hash: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RevisionConditionResult:
    acquisition: RevisionSnapshot
    reversal: RevisionSnapshot
    return_to_old: RevisionSnapshot
    reversal_crossing_episode: int | None
    reacquisition_crossing_episode: int | None
    runtime_state: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return {
            "acquisition": self.acquisition.state_dict(),
            "reacquisition_crossing_episode": self.reacquisition_crossing_episode,
            "return_to_old": self.return_to_old.state_dict(),
            "reversal": self.reversal.state_dict(),
            "reversal_crossing_episode": self.reversal_crossing_episode,
            "runtime_state": self.runtime_state,
        }


@dataclass(frozen=True, slots=True)
class StableControlResult:
    snapshot: RevisionSnapshot
    runtime_state: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return {
            "runtime_state": self.runtime_state,
            "snapshot": self.snapshot.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class RevisionAssessment:
    acquired_old_relation: bool
    reversed_to_new_relation: bool
    reacquired_old_relation: bool
    reversal_crossing_episode: int | None
    reacquisition_crossing_episode: int | None
    old_relation_retained: bool
    stable_control_single_link: bool
    stable_control_no_inconsistency: bool
    no_positive_self_confirmation: bool
    runtime_taxonomy_free: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalRevisionSuite:
    revision: RevisionConditionResult
    stable_control: StableControlResult
    assessment: RevisionAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "revision": self.revision.state_dict(),
            "stable_control": self.stable_control.state_dict(),
        }


def _world(target: str) -> AnonymousBoundaryWorld:
    return AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id="port:7",
                target=target,
                lag_ms=10.0,
                magnitude=1.0,
            ),
        )
    )


def _snapshot(
    *,
    phase_id: str,
    episode_count: int,
    runtime: Any,
    emitter: Any,
    consistency: UntypedBoundaryConsistency,
) -> RevisionSnapshot:
    old = consistency.link_state(port_id="port:7", target="unit:8")
    new = consistency.link_state(port_id="port:7", target="unit:9")
    consistency_state = consistency.state_dict()
    return RevisionSnapshot(
        phase_id=phase_id,
        episode_count=episode_count,
        boundary_count=sum(
            event.port_id == "port:7" for event in emitter.events
        ),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
        link_count=len(consistency_state["links"]),
        old_consistent_count=old.consistent_count if old is not None else 0,
        old_inconsistent_count=old.inconsistent_count if old is not None else 0,
        old_reliability=consistency.reliability(
            port_id="port:7",
            target="unit:8",
        ),
        new_consistent_count=new.consistent_count if new is not None else 0,
        new_inconsistent_count=new.inconsistent_count if new is not None else 0,
        new_reliability=consistency.reliability(
            port_id="port:7",
            target="unit:9",
        ),
        primary_state_hash=runtime.state_hash(),
    )


def _run_phase(
    *,
    phase_id: str,
    target: str,
    episodes: int,
    start_episode_index: int,
    runtime: Any,
    emitter: Any,
    consistency: UntypedBoundaryConsistency,
) -> tuple[RevisionSnapshot, tuple[RevisionSnapshot, ...]]:
    world = _world(target)
    snapshots: list[RevisionSnapshot] = []
    for local_index in range(episodes):
        global_index = start_episode_index + local_index
        start_ms = 100.0 + global_index * 70.0
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            cue_unit_id=0,
            start_ms=start_ms,
            episode_id=f"{phase_id}:{local_index}",
        )
        snapshots.append(
            _snapshot(
                phase_id=phase_id,
                episode_count=local_index + 1,
                runtime=runtime,
                emitter=emitter,
                consistency=consistency,
            )
        )
    return snapshots[-1], tuple(snapshots)


def _first_new_exceeds_old(
    snapshots: tuple[RevisionSnapshot, ...],
) -> int | None:
    for index, row in enumerate(snapshots, start=1):
        if (
            row.old_reliability is not None
            and row.new_reliability is not None
            and row.new_reliability > row.old_reliability
        ):
            return index
    return None


def _first_old_exceeds_new(
    snapshots: tuple[RevisionSnapshot, ...],
) -> int | None:
    for index, row in enumerate(snapshots, start=1):
        if (
            row.old_reliability is not None
            and row.new_reliability is not None
            and row.old_reliability > row.new_reliability
        ):
            return index
    return None


def run_revision_condition(episodes_per_phase: int = 3) -> RevisionConditionResult:
    if episodes_per_phase < 1:
        raise ValueError("episodes_per_phase must be positive")
    runtime, emitter, _, consistency = _build_primary()
    acquisition, _ = _run_phase(
        phase_id="acquisition",
        target="unit:8",
        episodes=episodes_per_phase,
        start_episode_index=0,
        runtime=runtime,
        emitter=emitter,
        consistency=consistency,
    )
    reversal, reversal_rows = _run_phase(
        phase_id="reversal",
        target="unit:9",
        episodes=episodes_per_phase,
        start_episode_index=episodes_per_phase,
        runtime=runtime,
        emitter=emitter,
        consistency=consistency,
    )
    returned, return_rows = _run_phase(
        phase_id="return-to-old",
        target="unit:8",
        episodes=episodes_per_phase,
        start_episode_index=episodes_per_phase * 2,
        runtime=runtime,
        emitter=emitter,
        consistency=consistency,
    )
    runtime.advance_silence(100.0 + episodes_per_phase * 3 * 70.0)
    consistency.expire(runtime.field.current_time_ms + 50.0)
    runtime_state = {
        "boundary": emitter.state_dict(),
        "chain": runtime.state_dict(),
        "consistency": consistency.state_dict(),
    }
    return RevisionConditionResult(
        acquisition=acquisition,
        reversal=reversal,
        return_to_old=returned,
        reversal_crossing_episode=_first_new_exceeds_old(reversal_rows),
        reacquisition_crossing_episode=_first_old_exceeds_new(return_rows),
        runtime_state=runtime_state,
    )


def run_stable_control(episodes: int = 9) -> StableControlResult:
    if episodes < 1:
        raise ValueError("episodes must be positive")
    runtime, emitter, _, consistency = _build_primary()
    snapshot, _ = _run_phase(
        phase_id="stable",
        target="unit:8",
        episodes=episodes,
        start_episode_index=0,
        runtime=runtime,
        emitter=emitter,
        consistency=consistency,
    )
    runtime.advance_silence(100.0 + episodes * 70.0)
    consistency.expire(runtime.field.current_time_ms + 50.0)
    return StableControlResult(
        snapshot=snapshot,
        runtime_state={
            "boundary": emitter.state_dict(),
            "chain": runtime.state_dict(),
            "consistency": consistency.state_dict(),
        },
    )


def run_canonical_revision_suite() -> CanonicalRevisionSuite:
    revision = run_revision_condition()
    stable = run_stable_control()
    acquisition = revision.acquisition
    reversal = revision.reversal
    returned = revision.return_to_old
    stable_snapshot = stable.snapshot
    lowered = str(
        {
            "revision": revision.runtime_state,
            "stable": stable.runtime_state,
        }
    ).lower()
    forbidden = (
        "assembly_id",
        "relation_type",
        "correct_action",
        "scalar_reward",
        "outcome_label",
        "functional_role",
        "meaning_state",
    )
    assessment = RevisionAssessment(
        acquired_old_relation=(
            acquisition.old_consistent_count == 3
            and acquisition.old_inconsistent_count == 0
            and acquisition.old_reliability is not None
            and acquisition.old_reliability > 0.5
            and acquisition.new_reliability is None
        ),
        reversed_to_new_relation=(
            reversal.old_inconsistent_count == 3
            and reversal.new_consistent_count == 3
            and reversal.old_reliability is not None
            and reversal.new_reliability is not None
            and reversal.new_reliability > reversal.old_reliability
        ),
        reacquired_old_relation=(
            returned.old_consistent_count == 6
            and returned.new_inconsistent_count == 3
            and returned.old_reliability is not None
            and returned.new_reliability is not None
            and returned.old_reliability > returned.new_reliability
        ),
        reversal_crossing_episode=revision.reversal_crossing_episode,
        reacquisition_crossing_episode=revision.reacquisition_crossing_episode,
        old_relation_retained=(
            reversal.old_consistent_count == acquisition.old_consistent_count
            and returned.old_consistent_count > reversal.old_consistent_count
        ),
        stable_control_single_link=stable_snapshot.link_count == 1,
        stable_control_no_inconsistency=(
            stable_snapshot.old_consistent_count == 9
            and stable_snapshot.old_inconsistent_count == 0
            and stable_snapshot.new_reliability is None
        ),
        no_positive_self_confirmation=(
            acquisition.committed_positive_updates == 0
            and reversal.committed_positive_updates == 0
            and returned.committed_positive_updates == 0
            and stable_snapshot.committed_positive_updates == 0
        ),
        runtime_taxonomy_free=not any(term in lowered for term in forbidden),
        engineering_candidate=False,
    )
    assessment = RevisionAssessment(
        **{
            **assessment.state_dict(),
            "engineering_candidate": all(
                (
                    assessment.acquired_old_relation,
                    assessment.reversed_to_new_relation,
                    assessment.reacquired_old_relation,
                    assessment.old_relation_retained,
                    assessment.stable_control_single_link,
                    assessment.stable_control_no_inconsistency,
                    assessment.no_positive_self_confirmation,
                    assessment.runtime_taxonomy_free,
                    assessment.reversal_crossing_episode == 2,
                    assessment.reacquisition_crossing_episode == 2,
                )
            ),
        }
    )
    return CanonicalRevisionSuite(
        revision=revision,
        stable_control=stable,
        assessment=assessment,
    )
