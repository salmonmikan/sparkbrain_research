from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation


@dataclass(frozen=True, slots=True)
class LocalProposalState:
    target: str
    path_id: str
    raw_confidence: float
    adapted_confidence: float
    raw_arrival_ms: float
    adapted_arrival_ms: float
    confirmed_count: int
    contradicted_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class G2PhaseSnapshot:
    phase_id: str
    g2_rows: tuple[LocalProposalState, ...]
    g1_only_rows: tuple[LocalProposalState, ...]
    external_observation_count: int
    committed_positive_updates: int
    g2_confirmed_count: int
    g2_contradicted_count: int

    def by_target(self, target: str, *, g2_enabled: bool) -> LocalProposalState:
        rows = self.g2_rows if g2_enabled else self.g1_only_rows
        matches = tuple(row for row in rows if row.target == target)
        if len(matches) != 1:
            raise KeyError(target)
        return matches[0]

    def state_dict(self) -> dict[str, Any]:
        return {
            "committed_positive_updates": self.committed_positive_updates,
            "external_observation_count": self.external_observation_count,
            "g1_only_rows": [row.state_dict() for row in self.g1_only_rows],
            "g2_confirmed_count": self.g2_confirmed_count,
            "g2_contradicted_count": self.g2_contradicted_count,
            "g2_rows": [row.state_dict() for row in self.g2_rows],
            "phase_id": self.phase_id,
        }


@dataclass(frozen=True, slots=True)
class G2DependencyAssessment:
    raw_g1_generation_survives_without_g2: bool
    stabilization_requires_g2: bool
    timing_correction_requires_g2: bool
    reversal_requires_g2: bool
    reacquisition_requires_g2: bool
    long_run_selectivity_requires_g2: bool
    g1_only_route_remains_static: bool
    prepare_only_cannot_self_confirm: bool
    positive_commits_are_external_only: bool
    g2_burden_identified: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class G2DependencySuite:
    initial: G2PhaseSnapshot
    stabilized_old: G2PhaseSnapshot
    reversed_new: G2PhaseSnapshot
    reacquired_old: G2PhaseSnapshot
    prepare_only_commits_before_external: int
    assessment: G2DependencyAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "initial": self.initial.state_dict(),
            "prepare_only_commits_before_external": (
                self.prepare_only_commits_before_external
            ),
            "reacquired_old": self.reacquired_old.state_dict(),
            "reversed_new": self.reversed_new.state_dict(),
            "stabilized_old": self.stabilized_old.state_dict(),
            "suite_hash": self.suite_hash,
        }


def _pulse(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    magnitude: float = 1.0,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=magnitude,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _trained_g1() -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            maximum_candidates=4,
            proposal_ttl_ms=25.0,
        )
    )
    for episode, offset in enumerate((0.0, 30.0, 60.0)):
        source = _pulse(f"g2-train:{episode}:source", offset, "unit:0")
        old = _pulse(f"g2-train:{episode}:old", offset + 5.0, "unit:1")
        new = _pulse(f"g2-train:{episode}:new", offset + 5.0, "unit:2")
        model.observe_external_transition(source, old)
        model.observe_external_transition(source, new)
    return model


def _learned_g1_hash(model: LocalTemporalExpectation) -> str:
    state = model.state_dict()
    return digest(
        {
            "config": state["config"],
            "external_transition_count": state["external_transition_count"],
            "transitions": state["transitions"],
        }
    )


def _raw_proposals(
    model: LocalTemporalExpectation,
    *,
    phase_id: str,
    source_time_ms: float,
) -> tuple[Any, ...]:
    source = _pulse(
        f"g2-probe:{phase_id}",
        source_time_ms,
        "unit:0",
    )
    before = model.proposal_count
    rows = model.proposals_for(source, origin_state_hash="0" * 64)
    model.proposal_count = before
    return rows


def _snapshot(
    phase_id: str,
    model: LocalTemporalExpectation,
    transition: SparseLocalTransitionAdaptation,
    ledger: ProvenanceLedger,
    *,
    source_time_ms: float,
) -> G2PhaseSnapshot:
    rows = _raw_proposals(
        model,
        phase_id=phase_id,
        source_time_ms=source_time_ms,
    )
    path_states = transition.state_dict()["paths"]
    g2_rows: list[LocalProposalState] = []
    g1_rows: list[LocalProposalState] = []
    for proposal in rows:
        path_id = proposal.local_path_ids[0]
        state = path_states.get(path_id, {})
        scale = transition.path_confidence_scale(path_id)
        timing = float(state.get("mean_timing_correction_ms", 0.0))
        adapted_confidence = min(1.0, max(0.0, proposal.confidence * scale))
        g2_rows.append(
            LocalProposalState(
                target=proposal.target,
                path_id=path_id,
                raw_confidence=proposal.confidence,
                adapted_confidence=adapted_confidence,
                raw_arrival_ms=proposal.predicted_arrival_ms,
                adapted_arrival_ms=max(
                    proposal.created_at_ms,
                    proposal.predicted_arrival_ms + timing,
                ),
                confirmed_count=int(state.get("confirmed_count", 0)),
                contradicted_count=int(state.get("contradicted_count", 0)),
            )
        )
        g1_rows.append(
            LocalProposalState(
                target=proposal.target,
                path_id=path_id,
                raw_confidence=proposal.confidence,
                adapted_confidence=proposal.confidence,
                raw_arrival_ms=proposal.predicted_arrival_ms,
                adapted_arrival_ms=proposal.predicted_arrival_ms,
                confirmed_count=0,
                contradicted_count=0,
            )
        )
    return G2PhaseSnapshot(
        phase_id=phase_id,
        g2_rows=tuple(g2_rows),
        g1_only_rows=tuple(g1_rows),
        external_observation_count=ledger.external_observation_count,
        committed_positive_updates=ledger.committed_positive_updates,
        g2_confirmed_count=transition.confirmed_count,
        g2_contradicted_count=transition.contradicted_count,
    )


def _resolve_episode(
    model: LocalTemporalExpectation,
    transition: SparseLocalTransitionAdaptation,
    ledger: ProvenanceLedger,
    *,
    episode_id: str,
    source_time_ms: float,
    external_target: str,
    external_lag_ms: float,
) -> None:
    source = _pulse(
        f"g2-source:{episode_id}",
        source_time_ms,
        "unit:0",
    )
    ledger.register_external(source)
    prepared = transition.prepare(
        source,
        origin_state_hash=digest(
            {
                "episode_id": episode_id,
                "g1": _learned_g1_hash(model),
            }
        ),
    )
    external = _pulse(
        f"g2-external:{episode_id}",
        source_time_ms + external_lag_ms,
        external_target,
    )
    for row in prepared:
        transition.resolve_external(row.proposal.proposal_id, external)


def _phase(
    model: LocalTemporalExpectation,
    transition: SparseLocalTransitionAdaptation,
    ledger: ProvenanceLedger,
    *,
    phase_id: str,
    target: str,
    repetitions: int,
    episode_offset: int,
) -> None:
    for index in range(repetitions):
        episode = episode_offset + index
        _resolve_episode(
            model,
            transition,
            ledger,
            episode_id=f"{phase_id}:{index}",
            source_time_ms=100.0 + episode * 50.0,
            external_target=target,
            external_lag_ms=7.0,
        )


def _rows_equal(
    left: tuple[LocalProposalState, ...],
    right: tuple[LocalProposalState, ...],
) -> bool:
    return left == right


def run_g2_dependency_suite() -> G2DependencySuite:
    """Keep G1 fixed and isolate the work performed by G2 adaptation."""

    model = _trained_g1()
    learned_hash_before = _learned_g1_hash(model)
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(model, ledger)

    prepare_source = _pulse("g2-prepare-only", 90.0, "unit:0")
    ledger.register_external(prepare_source)
    transition.prepare(
        prepare_source,
        origin_state_hash=digest({"condition": "prepare-only"}),
    )
    prepare_only_commits = ledger.committed_positive_updates
    transition.expire_pending(200.0)

    initial = _snapshot(
        "initial",
        model,
        transition,
        ledger,
        source_time_ms=1000.0,
    )
    _phase(
        model,
        transition,
        ledger,
        phase_id="stabilize-old",
        target="unit:1",
        repetitions=3,
        episode_offset=0,
    )
    stabilized = _snapshot(
        "stabilized-old",
        model,
        transition,
        ledger,
        source_time_ms=1100.0,
    )
    _phase(
        model,
        transition,
        ledger,
        phase_id="reverse-new",
        target="unit:2",
        repetitions=6,
        episode_offset=3,
    )
    reversed_new = _snapshot(
        "reversed-new",
        model,
        transition,
        ledger,
        source_time_ms=1200.0,
    )
    _phase(
        model,
        transition,
        ledger,
        phase_id="reacquire-old",
        target="unit:1",
        repetitions=6,
        episode_offset=9,
    )
    reacquired = _snapshot(
        "reacquired-old",
        model,
        transition,
        ledger,
        source_time_ms=1300.0,
    )
    if _learned_g1_hash(model) != learned_hash_before:
        raise RuntimeError("G2 dependency assay mutated learned G1 transition state")

    initial_old = initial.by_target("unit:1", g2_enabled=True)
    initial_new = initial.by_target("unit:2", g2_enabled=True)
    stable_old = stabilized.by_target("unit:1", g2_enabled=True)
    stable_new = stabilized.by_target("unit:2", g2_enabled=True)
    reversed_old = reversed_new.by_target("unit:1", g2_enabled=True)
    reversed_target = reversed_new.by_target("unit:2", g2_enabled=True)
    returned_old = reacquired.by_target("unit:1", g2_enabled=True)
    returned_new = reacquired.by_target("unit:2", g2_enabled=True)

    g1_static = all(
        _rows_equal(initial.g1_only_rows, row.g1_only_rows)
        for row in (stabilized, reversed_new, reacquired)
    )
    values = {
        "raw_g1_generation_survives_without_g2": (
            {row.target for row in initial.g1_only_rows} == {"unit:1", "unit:2"}
            and all(row.raw_confidence == 0.5 for row in initial.g1_only_rows)
        ),
        "stabilization_requires_g2": (
            stable_old.adapted_confidence > stable_new.adapted_confidence
            and initial_old.adapted_confidence == initial_new.adapted_confidence
        ),
        "timing_correction_requires_g2": (
            stable_old.adapted_arrival_ms > stable_old.raw_arrival_ms
            and stable_old.raw_arrival_ms
            == stabilized.by_target("unit:1", g2_enabled=False).adapted_arrival_ms
        ),
        "reversal_requires_g2": (
            reversed_target.adapted_confidence > reversed_old.adapted_confidence
        ),
        "reacquisition_requires_g2": (
            returned_old.adapted_confidence > returned_new.adapted_confidence
        ),
        "long_run_selectivity_requires_g2": (
            abs(returned_old.adapted_confidence - returned_new.adapted_confidence)
            >= 0.2
            and all(
                row.adapted_confidence == 0.5 for row in reacquired.g1_only_rows
            )
        ),
        "g1_only_route_remains_static": g1_static,
        "prepare_only_cannot_self_confirm": prepare_only_commits == 0,
        "positive_commits_are_external_only": (
            ledger.committed_positive_updates
            == transition.confirmed_count
            == 15
        ),
    }
    assessment = G2DependencyAssessment(
        **values,
        g2_burden_identified=all(values.values()),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "initial": initial.state_dict(),
        "prepare_only_commits_before_external": prepare_only_commits,
        "reacquired_old": reacquired.state_dict(),
        "reversed_new": reversed_new.state_dict(),
        "stabilized_old": stabilized.state_dict(),
    }
    return G2DependencySuite(
        initial=initial,
        stabilized_old=stabilized,
        reversed_new=reversed_new,
        reacquired_old=reacquired,
        prepare_only_commits_before_external=prepare_only_commits,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )
