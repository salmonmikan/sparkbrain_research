from __future__ import annotations

import inspect
from dataclasses import fields
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from sparkbrain.system_build import (
    DeterministicM1World,
    IntegratedM1CheckpointManager,
    IntegratedM1Pilot,
    IntegratedM1Session,
    M1Observation,
    M1OutcomeReceipt,
)
from sparkbrain.system_build.acceptance import m1_acceptance_manifest


def test_public_runtime_inputs_exclude_privileged_fields_and_claims_are_bounded() -> None:
    forbidden = {
        "answer",
        "entity",
        "episode",
        "evaluator",
        "future",
        "gold",
        "held_out",
        "heldout",
        "label",
        "oracle",
        "regime",
        "scope",
        "target",
        "truth",
    }
    names = {field.name for field in fields(M1Observation)}
    names.update(field.name for field in fields(M1OutcomeReceipt))
    names.update(inspect.signature(IntegratedM1Pilot.observe).parameters)
    names.update(inspect.signature(IntegratedM1Pilot.apply_outcome).parameters)
    assert not names & forbidden

    state = IntegratedM1Pilot().inspect()
    assert state["evidentiary_status"] == "NON_EVIDENTIARY_BUILD"
    assert state["scientific_credit"] == 0
    assert "does not establish comparative support" in state["claim_boundary"]


def test_bounded_world_closes_loop_across_two_scopes_and_plural_hypotheses() -> None:
    session = IntegratedM1Session()
    cycles = [session.cycle() for _ in range(8)]

    assert all(cycle.revision.committed for cycle in cycles)
    assert cycles[0].action.decision == "abstain"
    assert {cycle.action.decision for cycle in cycles} >= {
        "abstain",
        "act_alpha",
        "act_beta",
    }
    state = session.pilot.inspect()
    assert state["sequence"] == 8
    assert len(state["scope_revision"]["router"]["components"]) == 2
    assert len(state["predictive"]["hypotheses"]) >= 2
    assert len(state["trace"]) == 8


def test_world_action_affects_later_outcome_without_hidden_runtime_field() -> None:
    left = DeterministicM1World()
    right = DeterministicM1World()
    pilot = IntegratedM1Pilot()
    observation = left.next_observation()
    action = pilot.observe(observation)
    abstain_outcome = left.resolve(action).outcome
    acted = action.__class__(
        action.event_id,
        "act_alpha",
        "test_fixed_action",
        action.prediction,
        action.selected_state_id,
        action.route_token,
        action.route_candidate,
    )
    acted_outcome = right.resolve(acted).outcome
    assert acted_outcome != abstain_outcome


def test_duplicate_receipt_is_idempotent_and_conflict_is_no_write() -> None:
    pilot = IntegratedM1Pilot()
    world = DeterministicM1World()
    action = pilot.observe(world.next_observation())
    receipt = world.resolve(action)
    first = pilot.apply_outcome(receipt)
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    duplicate = pilot.apply_outcome(receipt)
    assert duplicate == first
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash

    conflict = M1OutcomeReceipt(receipt.receipt_id, receipt.event_id, receipt.outcome + 0.1)
    with pytest.raises(ValueError, match="receipt identity conflict"):
        pilot.apply_outcome(conflict)
    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


@pytest.mark.parametrize(
    "fault",
    [
        "before_predictive_revision",
        "after_predictive_revision",
        "before_scope_revision",
        "after_scope_revision",
    ],
)
def test_component_revision_faults_restore_exact_pending_state(fault: str) -> None:
    pilot = IntegratedM1Pilot()
    world = DeterministicM1World()
    action = pilot.observe(world.next_observation())
    receipt = world.resolve(action)
    before = pilot.inspect()
    before_hash = pilot.state_hash()

    with pytest.raises(RuntimeError, match="injected"):
        pilot.apply_outcome(receipt, _fault_at=fault)

    assert pilot.inspect() == before
    assert pilot.state_hash() == before_hash


@pytest.mark.parametrize(
    "fault",
    [
        "before_action",
        "after_action",
        "after_outcome",
        "before_predictive_revision",
        "after_predictive_revision",
        "before_scope_revision",
        "after_scope_revision",
    ],
)
def test_session_faults_restore_world_and_both_components(fault: str) -> None:
    session = IntegratedM1Session()
    before = session.inspect()
    before_hash = session.state_hash()

    with pytest.raises(RuntimeError, match="injected"):
        session.cycle(_fault_at=fault)

    assert session.inspect() == before
    assert session.state_hash() == before_hash


def test_midrun_checkpoint_reproduces_exact_remaining_trace_and_hash() -> None:
    session = IntegratedM1Session()
    for _ in range(4):
        session.cycle()

    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "checkpoint"
        IntegratedM1CheckpointManager.save(session, root)
        restored = IntegratedM1CheckpointManager.load(root)
        assert restored.inspect() == session.inspect()
        assert restored.state_hash() == session.state_hash()

        left = [session.cycle().as_dict() for _ in range(4)]
        right = [restored.cycle().as_dict() for _ in range(4)]
        assert right == left
        assert restored.inspect() == session.inspect()
        assert restored.state_hash() == session.state_hash()


def test_checkpoint_is_strict_digest_bound_and_no_clobber() -> None:
    session = IntegratedM1Session()
    session.cycle()
    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "checkpoint"
        IntegratedM1CheckpointManager.save(session, root)
        with pytest.raises(FileExistsError):
            IntegratedM1CheckpointManager.save(session, root)

        world_path = root / IntegratedM1CheckpointManager.WORLD
        world_path.write_text('{"actions":[],"index":0}\n', encoding="utf-8")
        with pytest.raises(ValueError, match="digest mismatch"):
            IntegratedM1CheckpointManager.load(root)


def test_pending_event_and_event_identity_are_strict() -> None:
    pilot = IntegratedM1Pilot()
    observation = DeterministicM1World().next_observation()
    pilot.observe(observation)
    with pytest.raises(RuntimeError, match="pending event"):
        pilot.observe(observation)


def test_resource_ceiling_and_m1_manifest_are_explicit() -> None:
    world = DeterministicM1World.from_state_dict(
        {"actions": ["abstain"] * 64, "index": 64}
    )
    with pytest.raises(RuntimeError, match="64-cycle"):
        world.next_observation()
    assert "cross_component_atomic_revision_and_fault_rollback" in m1_acceptance_manifest()
    assert "non_evidentiary_zero_credit_claim_boundary" in m1_acceptance_manifest()
