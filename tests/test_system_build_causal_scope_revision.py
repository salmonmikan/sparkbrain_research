from __future__ import annotations

import inspect
from copy import deepcopy
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
    for index, (observation, candidate) in enumerate(events, start=1):
        result = pilot.step(
            observation,
            CandidateEvidence(candidate, f"evidence-{index:03d}"),
        )
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

    result = pilot.step(observation, CandidateEvidence("alpha", "rejected-evidence"))

    assert result.abstained
    assert result.reason == reason
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


def test_identical_observation_conflict_is_full_no_write() -> None:
    pilot = CausalScopeRevisionPilot()
    assert pilot.step((0.0,), CandidateEvidence("alpha", "evidence-001")).committed
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    result = pilot.step((0.0,), CandidateEvidence("beta", "evidence-002"))

    assert result.abstained
    assert result.reason == "identical_observation_conflict"
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


@pytest.mark.parametrize(
    "evidence",
    [
        CandidateEvidence("absent", "invalid-candidate"),
        CandidateEvidence("alpha", "invalid-strength", 2.0),
        CandidateEvidence("alpha", "nan-strength", float("nan")),
        CandidateEvidence("alpha", "contains space"),
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
    assert pilot.inspect()["evidence_bindings"] == {}
    assert pilot.inspect()["sequence"] == 0


def test_duplicate_evidence_id_is_explicit_idempotent_no_write() -> None:
    pilot = CausalScopeRevisionPilot()
    evidence = CandidateEvidence("alpha", "receipt-001", 0.75)
    first = pilot.step((0.0,), evidence)
    assert first.committed
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    duplicate = pilot.step((0.0,), evidence)

    assert not duplicate.committed
    assert not duplicate.abstained
    assert duplicate.reason == "duplicate_evidence_id"
    assert duplicate.token == first.token
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


@pytest.mark.parametrize(
    ("observation", "evidence"),
    [
        ((0.1,), CandidateEvidence("alpha", "receipt-001", 0.75)),
        ((0.0,), CandidateEvidence("beta", "receipt-001", 0.75)),
        ((0.0,), CandidateEvidence("alpha", "receipt-001", 0.50)),
    ],
)
def test_conflicting_evidence_id_reuse_is_full_no_write(
    observation: tuple[float, ...],
    evidence: CandidateEvidence,
) -> None:
    pilot = CausalScopeRevisionPilot()
    assert pilot.step((0.0,), CandidateEvidence("alpha", "receipt-001", 0.75)).committed
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    conflict = pilot.step(observation, evidence)

    assert not conflict.committed
    assert conflict.abstained
    assert conflict.reason == "evidence_identity_conflict"
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


def test_distinct_evidence_ids_may_commit_same_consistent_observation() -> None:
    pilot = CausalScopeRevisionPilot()
    assert pilot.step((0.0,), CandidateEvidence("alpha", "receipt-001")).committed
    assert pilot.step((0.0,), CandidateEvidence("alpha", "receipt-002")).committed
    state = pilot.inspect()
    assert state["sequence"] == 2
    assert len(state["evidence_bindings"]) == 2
    assert state["routes"]["scope-00000001"]["supports"]["alpha"] == 2.0


def test_shared_prefix_state_and_actions_ignore_unseen_suffix() -> None:
    left = CausalScopeRevisionPilot()
    right = CausalScopeRevisionPilot()
    prefix = FIXED_STREAMS["interleaved"][:3]
    left_actions = []
    right_actions = []
    for observation, candidate in prefix:
        evidence_id = f"prefix-{len(left_actions) + 1:03d}"
        left_actions.append(left.step(observation, CandidateEvidence(candidate, evidence_id)))
        right_actions.append(right.step(observation, CandidateEvidence(candidate, evidence_id)))

    assert left_actions == right_actions
    assert left.inspect() == right.inspect()
    assert left.state_hash() == right.state_hash()

    left.step((0.40,), CandidateEvidence("beta", "suffix-left"))
    right.step((0.02,), CandidateEvidence("alpha", "suffix-right"))
    assert left.inspect() != right.inspect()


def test_checkpoint_replay_reproduces_exact_next_decision_and_integrated_state() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:3])
    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "checkpoint"
        ScopeRevisionCheckpointManager.save(pilot, root)
        restored = ScopeRevisionCheckpointManager.load(root)

        assert restored.inspect() == pilot.inspect()
        assert restored.state_hash() == pilot.state_hash()
        left = pilot.step((0.40,), CandidateEvidence("beta", "evidence-004"))
        right = restored.step((0.40,), CandidateEvidence("beta", "evidence-004"))
        assert left == right
        assert restored.inspect() == pilot.inspect()


def test_checkpoint_is_no_clobber() -> None:
    pilot = CausalScopeRevisionPilot()
    with TemporaryDirectory() as tmp:
        ScopeRevisionCheckpointManager.save(pilot, tmp)
        with pytest.raises(FileExistsError):
            ScopeRevisionCheckpointManager.save(pilot, tmp)


def test_checkpoint_requires_route_state_for_every_router_component() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:2])
    payload = deepcopy(pilot._checkpoint_payload())
    payload["routes"].pop("scope-00000002")
    with pytest.raises(ValueError, match="exactly match"):
        CausalScopeRevisionPilot._from_checkpoint_payload(payload)


def test_checkpoint_requires_global_sequence_permutation_without_gap_or_duplicate() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:3])
    payload = deepcopy(pilot._checkpoint_payload())
    payload["routes"]["scope-00000002"]["evidence"][0]["sequence"] = 1
    payload["evidence_bindings"]["evidence-002"]["sequence"] = 1
    with pytest.raises(ValueError, match="unique permutation"):
        CausalScopeRevisionPilot._from_checkpoint_payload(payload)


def test_checkpoint_requires_exact_evidence_identity_ledger() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:2])
    payload = deepcopy(pilot._checkpoint_payload())
    payload["evidence_bindings"]["evidence-002"]["candidate"] = "alpha"
    with pytest.raises(ValueError, match="do not match committed evidence ledger"):
        CausalScopeRevisionPilot._from_checkpoint_payload(payload)


def test_checkpoint_schema_one_is_rejected_after_identity_contract_change() -> None:
    pilot = _run(FIXED_STREAMS["interleaved"][:1])
    payload = deepcopy(pilot._checkpoint_payload())
    payload["schema_version"] = 1
    with pytest.raises(ValueError, match="unsupported"):
        CausalScopeRevisionPilot._from_checkpoint_payload(payload)


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
