from __future__ import annotations

import inspect
from dataclasses import fields
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from sparkbrain.system_build import (
    CandidateEvidence,
    CausalScopeRevisionPilot,
    ScopeRevisionCheckpointManager,
    ScopeRevisionConfig,
)
from sparkbrain.system_build.acceptance import sb002_acceptance_manifest

FIXED_STREAMS = {
    "interleaved": (
        ((0.0,), "alpha"),
        ((0.45,), "beta"),
        ((0.05,), "alpha"),
        ((0.40,), "beta"),
    ),
    "blocked": (
        ((0.0,), "alpha"),
        ((0.05,), "alpha"),
        ((0.45,), "beta"),
        ((0.40,), "beta"),
    ),
    "reverse_interleaved": (
        ((0.45,), "beta"),
        ((0.0,), "alpha"),
        ((0.40,), "beta"),
        ((0.05,), "alpha"),
    ),
}


def _run(events: tuple[tuple[tuple[float, ...], str], ...]) -> CausalScopeRevisionPilot:
    pilot = CausalScopeRevisionPilot()
    for observation, candidate in events:
        result = pilot.step(observation, CandidateEvidence(candidate))
        assert result.committed
    return pilot


@pytest.mark.parametrize("stream_id", tuple(FIXED_STREAMS))
def test_fixed_arrival_orders_recover_two_route_local_revisions(stream_id: str) -> None:
    pilot = _run(FIXED_STREAMS[stream_id])

    alpha = pilot.query((0.025,))
    beta = pilot.query((0.425,))

    assert len(pilot.inspect()["router"]["components"]) == 2
    assert alpha.revision is not None
    assert alpha.revision.selected_candidate == "alpha"
    assert beta.revision is not None
    assert beta.revision.selected_candidate == "beta"
    assert pilot.inspect()["sequence"] == 4


def test_cross_order_acceptance_compares_partition_and_local_outcomes_not_tokens() -> None:
    outcomes = []
    for events in FIXED_STREAMS.values():
        pilot = _run(events)
        outcomes.append(
            tuple(
                pilot.query(observation).revision.selected_candidate  # type: ignore[union-attr]
                for observation in ((0.025,), (0.425,))
            )
        )

    assert outcomes == [("alpha", "beta")] * 3
    forward = _run(FIXED_STREAMS["interleaved"])
    reverse = _run(FIXED_STREAMS["reverse_interleaved"])
    assert forward.query((0.025,)).routing.token != reverse.query((0.025,)).routing.token


@pytest.mark.parametrize(
    ("observation", "reason"),
    [
        ((0.225,), "ambiguous_nearest_components"),
        ((1.0,), "component_capacity_exhausted_out_of_support"),
    ],
)
def test_ambiguous_and_out_of_support_steps_are_full_no_write(
    observation: tuple[float, ...],
    reason: str,
) -> None:
    pilot = _run(FIXED_STREAMS["interleaved"])
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    result = pilot.step(observation, CandidateEvidence("alpha"))

    assert result.abstained
    assert result.reason == reason
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


def test_identical_observation_conflict_is_full_no_write() -> None:
    pilot = CausalScopeRevisionPilot()
    assert pilot.step((0.0,), CandidateEvidence("alpha")).committed
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    result = pilot.step((0.0,), CandidateEvidence("beta"))

    assert result.abstained
    assert result.reason == "identical_observation_conflict"
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


@pytest.mark.parametrize(
    "evidence",
    [
        CandidateEvidence("absent"),
        CandidateEvidence("alpha", 2.0),
        CandidateEvidence("alpha", float("nan")),
    ],
)
def test_invalid_downstream_revision_rolls_back_all_transaction_state(
    evidence: CandidateEvidence,
) -> None:
    pilot = CausalScopeRevisionPilot()
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    result = pilot.step((0.0,), evidence)

    assert result.abstained
    assert result.reason == "invalid_downstream_revision"
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash
    assert pilot.inspect()["router"]["components"] == []
    assert pilot.inspect()["routes"] == {}
    assert pilot.inspect()["observation_bindings"] == {}
    assert pilot.inspect()["sequence"] == 0


def test_shared_prefix_state_and_actions_ignore_unseen_suffix() -> None:
    left = CausalScopeRevisionPilot()
    right = CausalScopeRevisionPilot()
    prefix = FIXED_STREAMS["interleaved"][:3]
    left_actions = []
    right_actions = []
    for observation, candidate in prefix:
        left_actions.append(left.step(observation, CandidateEvidence(candidate)))
        right_actions.append(right.step(observation, CandidateEvidence(candidate)))

    assert left_actions == right_actions
    assert left.inspect() == right.inspect()
    assert left.state_hash() == right.state_hash()

    left.step((0.40,), CandidateEvidence("beta"))
    right.step((0.02,), CandidateEvidence("alpha"))
    assert left.inspect() != right.inspect()


def test_checkpoint_replay_reproduces_exact_next_decision_and_integrated_state() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:3])
    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "checkpoint"
        ScopeRevisionCheckpointManager.save(pilot, root)
        restored = ScopeRevisionCheckpointManager.load(root)

        assert restored.inspect() == pilot.inspect()
        assert restored.state_hash() == pilot.state_hash()
        left = pilot.step((0.40,), CandidateEvidence("beta"))
        right = restored.step((0.40,), CandidateEvidence("beta"))
        assert left == right
        assert restored.inspect() == pilot.inspect()


def test_checkpoint_is_no_clobber() -> None:
    pilot = CausalScopeRevisionPilot()
    with TemporaryDirectory() as tmp:
        ScopeRevisionCheckpointManager.save(pilot, tmp)
        with pytest.raises(FileExistsError):
            ScopeRevisionCheckpointManager.save(pilot, tmp)


def test_runtime_interfaces_and_fixtures_have_no_oracle_fields() -> None:
    forbidden = {
        "label",
        "truth",
        "scope",
        "regime",
        "episode",
        "future",
        "suffix",
        "evaluator",
        "heldout",
        "held_out",
        "target",
    }
    names = set(inspect.signature(CausalScopeRevisionPilot.step).parameters)
    names.update(field.name for field in fields(CandidateEvidence))
    assert not names & forbidden
    assert all(not (set(row) & forbidden) for row in FIXED_STREAMS.values())


def test_query_is_pure_for_selected_midpoint_and_out_of_support() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"])
    before = pilot.inspect()
    for observation in ((0.025,), (0.225,), (1.0,)):
        pilot.query(observation)
    assert pilot.inspect() == before


def test_resource_ceiling_and_acceptance_manifest_are_fixed() -> None:
    with pytest.raises(ValueError, match="exactly two"):
        ScopeRevisionConfig(max_components=3).validate()
    with pytest.raises(ValueError, match="maximum_dimensions"):
        ScopeRevisionConfig(maximum_dimensions=9).validate()
    assert "invalid_downstream_revision_rolls_back_full_observation_transaction" in (
        sb002_acceptance_manifest()
    )


def test_build_status_and_provenance_are_explicitly_non_evidentiary() -> None:
    state = CausalScopeRevisionPilot().inspect()
    assert state["build_id"] == "BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT"
    assert state["evidentiary_status"] == "NON_EVIDENTIARY_BUILD"
    assert state["scientific_credit"] == 0
    assert state["component_provenance"]["causal_online_router"]["prototype_head"] == (
        "f980c13d984460f158a95e8181239db8d19c8468"
    )
