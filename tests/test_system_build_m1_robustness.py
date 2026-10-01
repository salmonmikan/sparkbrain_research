from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from sparkbrain.system_build import (
    IntegratedM1CheckpointManager,
    IntegratedM1Session,
    M1Cycle,
    M1Observation,
    M1OutcomeReceipt,
)

CHECKPOINT_CUTPOINTS = (1, 8, 31, 63)
FAULT_POSITIONS = (1, 31, 63)
SESSION_FAULT_POINTS = (
    "before_action",
    "after_action",
    "after_outcome",
)
COMPONENT_FAULT_POINTS = (
    "before_predictive_revision",
    "after_predictive_revision",
    "before_scope_revision",
    "after_scope_revision",
)
MAX_ACCEPTANCE_COMMITS = 512
EXPECTED_ACCEPTANCE_COMMITS = 267


@dataclass
class CommitBudget:
    committed: int = 0

    def cycle(self, session: IntegratedM1Session) -> M1Cycle:
        result = session.cycle()
        self.committed += 1
        assert self.committed <= MAX_ACCEPTANCE_COMMITS
        return result


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _assert_committed_invariants(session: IntegratedM1Session, expected: int) -> None:
    state = session.inspect()
    pilot = state["pilot"]
    trace = pilot["trace"]
    event_bindings = pilot["event_bindings"]
    receipt_bindings = pilot["receipt_bindings"]
    scoped = pilot["scope_revision"]

    assert state["world"]["index"] == expected
    assert len(state["world"]["actions"]) == expected
    assert pilot["sequence"] == expected
    assert pilot["pending_observation"] is None
    assert pilot["pending_action"] is None
    assert len(event_bindings) == expected
    assert len(receipt_bindings) == expected
    assert len(trace) == expected
    assert scoped["sequence"] == expected
    assert len(scoped["evidence_bindings"]) == expected

    expected_sequences = list(range(1, expected + 1))
    assert [row["sequence"] for row in trace] == expected_sequences
    assert sorted(row["sequence"] for row in scoped["evidence_bindings"].values()) == (
        expected_sequences
    )
    for sequence, row in enumerate(trace, start=1):
        event_id = f"event-{sequence:04d}"
        receipt_id = f"receipt-{event_id}"
        assert row["observation"]["event_id"] == event_id
        assert row["action"]["event_id"] == event_id
        assert row["receipt"]["event_id"] == event_id
        assert row["receipt"]["receipt_id"] == receipt_id
        assert row["revision"]["event_id"] == event_id
        assert row["revision"]["receipt_id"] == receipt_id
        assert row["revision"]["sequence"] == sequence

        assert event_bindings[event_id] == _digest(row["observation"])

        receipt_binding = receipt_bindings[receipt_id]
        assert receipt_binding["event_id"] == event_id
        assert receipt_binding["outcome"] == row["receipt"]["outcome"]
        assert receipt_binding["revision"] == row["revision"]

        outcome = float(row["receipt"]["outcome"])
        scope_binding = scoped["evidence_bindings"][receipt_id]
        assert scope_binding == {
            "candidate": "alpha" if outcome >= 0 else "beta",
            "observation_digest": _digest(
                {"features": row["observation"]["routing_features"]}
            ),
            "route_token": row["revision"]["scope_revision"]["token"],
            "sequence": sequence,
            "strength": min(1.0, abs(outcome)),
        }


def _assert_exact_next_cycle(
    left: IntegratedM1Session,
    right: IntegratedM1Session,
    budget: CommitBudget,
) -> None:
    left_cycle = budget.cycle(left)
    right_cycle = budget.cycle(right)
    assert left_cycle.as_dict() == right_cycle.as_dict()
    assert left.inspect() == right.inspect()
    assert left.state_hash() == right.state_hash()


def test_fixed_post_integration_robustness_acceptance_surface() -> None:
    budget = CommitBudget()
    nominal = IntegratedM1Session()

    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        checkpoints: dict[int, Path] = {}
        nominal_cycles: list[dict[str, object]] = []
        nominal_hashes: list[str] = []

        for sequence in range(1, 65):
            nominal_cycles.append(budget.cycle(nominal).as_dict())
            _assert_committed_invariants(nominal, sequence)
            nominal_hashes.append(nominal.state_hash())
            if sequence in CHECKPOINT_CUTPOINTS:
                checkpoint = root / f"cycle-{sequence:02d}"
                IntegratedM1CheckpointManager.save(nominal, checkpoint)
                checkpoints[sequence] = checkpoint

        # One restored continuation per fixed cutpoint reuses the nominal timeline as
        # its control, avoiding redundant executions while preserving exact suffix checks.
        for cutpoint in CHECKPOINT_CUTPOINTS:
            restored = IntegratedM1CheckpointManager.load(checkpoints[cutpoint])
            _assert_committed_invariants(restored, cutpoint)
            assert restored.state_hash() == nominal_hashes[cutpoint - 1]
            for sequence in range(cutpoint + 1, 65):
                replayed = budget.cycle(restored)
                assert replayed.as_dict() == nominal_cycles[sequence - 1]
                _assert_committed_invariants(restored, sequence)
                assert restored.state_hash() == nominal_hashes[sequence - 1]

        # Session-owned faults exercise the outer session transaction directly.
        for cutpoint in FAULT_POSITIONS:
            for fault in SESSION_FAULT_POINTS:
                recovered = IntegratedM1CheckpointManager.load(checkpoints[cutpoint])
                control = IntegratedM1CheckpointManager.load(checkpoints[cutpoint])
                before = recovered.inspect()
                before_hash = recovered.state_hash()
                with pytest.raises(RuntimeError, match="injected"):
                    recovered.cycle(_fault_at=fault)
                assert recovered.inspect() == before
                assert recovered.state_hash() == before_hash
                _assert_exact_next_cycle(recovered, control, budget)

            # Component-owned faults bypass the session safety net so this test proves
            # IntegratedM1Pilot.apply_outcome() restores its own component/pending state.
            for fault in COMPONENT_FAULT_POINTS:
                recovered = IntegratedM1CheckpointManager.load(checkpoints[cutpoint])
                control = IntegratedM1CheckpointManager.load(checkpoints[cutpoint])
                observation = recovered.world.next_observation()
                action = recovered.pilot.observe(observation)
                receipt = recovered.world.resolve(action)
                pilot_before = recovered.pilot.inspect()
                pilot_hash_before = recovered.pilot.state_hash()
                world_after_resolve = recovered.world.state_dict()

                with pytest.raises(RuntimeError, match="injected"):
                    recovered.pilot.apply_outcome(receipt, _fault_at=fault)

                assert recovered.pilot.inspect() == pilot_before
                assert recovered.pilot.state_hash() == pilot_hash_before
                assert recovered.world.state_dict() == world_after_resolve

                revision = recovered.pilot.apply_outcome(receipt)
                budget.committed += 1
                assert budget.committed <= MAX_ACCEPTANCE_COMMITS
                completed = M1Cycle(observation, action, receipt, revision)
                clean = budget.cycle(control)
                assert completed.as_dict() == clean.as_dict()
                assert recovered.inspect() == control.inspect()
                assert recovered.state_hash() == control.state_hash()

        # Duplicate receipt redelivery is idempotent and deterministic continuation
        # remains identical to a clean checkpoint continuation.
        duplicate = IntegratedM1CheckpointManager.load(checkpoints[1])
        duplicate_control = IntegratedM1CheckpointManager.load(checkpoints[1])
        first = nominal_cycles[0]
        receipt = M1OutcomeReceipt.from_dict(first["receipt"])
        before = duplicate.inspect()
        prior_revision = duplicate.pilot.apply_outcome(receipt)
        assert json.loads(json.dumps(prior_revision.as_dict())) == json.loads(
            json.dumps(first["revision"])
        )
        assert duplicate.inspect() == before
        _assert_exact_next_cycle(duplicate, duplicate_control, budget)

        # Conflicting receipt-ID reuse is a complete no-write failure.
        conflict = IntegratedM1CheckpointManager.load(checkpoints[1])
        conflict_control = IntegratedM1CheckpointManager.load(checkpoints[1])
        before = conflict.inspect()
        with pytest.raises(ValueError, match="receipt identity conflict"):
            conflict.pilot.apply_outcome(
                M1OutcomeReceipt(receipt.receipt_id, receipt.event_id, receipt.outcome + 0.1)
            )
        assert conflict.inspect() == before
        _assert_exact_next_cycle(conflict, conflict_control, budget)

        # Reusing a committed event ID is rejected before any component can mutate.
        event_conflict = IntegratedM1CheckpointManager.load(checkpoints[1])
        event_control = IntegratedM1CheckpointManager.load(checkpoints[1])
        before = event_conflict.inspect()
        with pytest.raises(ValueError, match="event_id has already been used"):
            event_conflict.pilot.observe(
                M1Observation("event-0001", 1.0, {"signal": 0.45}, (0.45,))
            )
        assert event_conflict.inspect() == before
        _assert_exact_next_cycle(event_conflict, event_control, budget)

        # Pending overlap and a mismatched outcome both preserve the exact pending
        # state. Completing the original event then matches a clean session cycle.
        pending = IntegratedM1CheckpointManager.load(checkpoints[1])
        pending_control = IntegratedM1CheckpointManager.load(checkpoints[1])
        observation = pending.world.next_observation()
        action = pending.pilot.observe(observation)
        pending_state = pending.pilot.inspect()
        pending_hash = pending.pilot.state_hash()
        with pytest.raises(RuntimeError, match="pending event"):
            pending.pilot.observe(observation)
        assert pending.pilot.inspect() == pending_state
        assert pending.pilot.state_hash() == pending_hash
        with pytest.raises(ValueError, match="does not match the pending observation"):
            pending.pilot.apply_outcome(M1OutcomeReceipt("wrong-receipt", "wrong-event", 0.0))
        assert pending.pilot.inspect() == pending_state
        assert pending.pilot.state_hash() == pending_hash

        valid_receipt = pending.world.resolve(action)
        revision = pending.pilot.apply_outcome(valid_receipt)
        budget.committed += 1
        assert budget.committed <= MAX_ACCEPTANCE_COMMITS
        completed = M1Cycle(observation, action, valid_receipt, revision)
        clean = budget.cycle(pending_control)
        assert completed.as_dict() == clean.as_dict()
        assert pending.inspect() == pending_control.inspect()
        assert pending.state_hash() == pending_control.state_hash()

    assert budget.committed == EXPECTED_ACCEPTANCE_COMMITS
    assert budget.committed <= MAX_ACCEPTANCE_COMMITS
