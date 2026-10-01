"""The 22 prospectively frozen fake-only cases; never import SparkBrain."""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "assembly_m1_contract_sentinel", ROOT / "scripts/assembly_m1_contract_sentinel.py"
)
assert SPEC is not None and SPEC.loader is not None
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)
A, B, ZERO = (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)
FIXTURES_CREATED = 0


def make(caps=None):
    global FIXTURES_CREATED
    FIXTURES_CREATED += 1
    assert FIXTURES_CREATED <= 64
    return M.SentinelCoordinator(caps or M.Caps())


def window(event_id="occ-001", index=0, **changes):
    offset = 200 * index
    result = M.Window(
        event_id, offset, offset + 40, offset + 72, ((offset + 40, "Q", 1.0),)
    )
    return replace(result, **changes)


def observed(context=A, event_id="occ-001"):
    coordinator = make()
    action = coordinator.observe(window(event_id), supplied_context=context)
    return coordinator, action


def finish(coordinator, event_id="occ-001", receipt_id="receipt-001", outcome=1.0):
    return coordinator.deliver(M.Receipt(receipt_id, event_id, outcome), delivered_ms=80)


def action_values(action):
    return action.prediction, action.decision, action.reason


def numeric_projection(coordinator):
    state = coordinator.inspect()
    return {
        "caps": state["caps"],
        "backend": state["_backend"],
        "consumer_counts": (state["_consumer"]["observe_calls"],
                            state["_consumer"]["feedback_calls"]),
        "credited": [
            ({key: value for key, value in observation.items() if key != "event_id"}, outcome)
            for observation, outcome in state["_consumer"]["credited"]
        ],
        "receipt_count": len(state["_receipts"]),
        "event_count": len(state["_events"]),
        "channels": state["_channels"],
        "last_receipt_ms": state["_last_receipt_ms"],
        "pending": state["_pending"],
    }


def test_c01_accept_a():
    coordinator, action = observed(A)
    assert action_values(action) == (1.0, "act_alpha", "predictive_scope_agreement")
    pending = coordinator.inspect()["_pending"]["observation"]
    assert dict(pending["sensory"]) == {"signal": 0.0, "temporal_0": 1.0, "temporal_1": 0.0}
    assert pending["route"] == (0.0, 1.0, 0.0)
    assert pending["time_seconds"] == 0.072


def test_c02_accept_b():
    _, action = observed(B)
    assert action_values(action) == (-1.0, "act_beta", "predictive_scope_agreement")


def test_c03_sham():
    first, first_action = observed(A)
    sham, sham_action = observed(tuple(A))
    assert first_action == sham_action
    assert first.inspect() == sham.inspect()


def test_c04_both_consumer_swap():
    first, first_action = observed(A)
    swapped, swapped_action = observed(B)
    assert first_action.decision == "act_alpha"
    assert swapped_action.decision == "act_beta"
    left, right = first.inspect(), swapped.inspect()
    assert left["_backend"] == right["_backend"]  # same pulses, clock and backend work
    assert left["_events"] == right["_events"]  # original observation/ID unchanged


def test_c05_prediction_only_swap():
    normal = M.adapt(window(), A)
    changed = replace(normal, sensory=M.adapt(window(), B).sensory)
    assert M.fake_decide(changed).reason == "predictive_scope_disagreement"
    assert M.fake_decide(changed).decision == "abstain"


def test_c06_route_only_swap():
    normal = M.adapt(window(), A)
    changed = replace(normal, route=M.adapt(window(), B).route)
    assert M.fake_decide(changed).reason == "predictive_scope_disagreement"
    assert M.fake_decide(changed).decision == "abstain"


def test_c07_zero_context():
    _, action = observed(ZERO)
    assert action.decision == "abstain"
    assert action.prediction is None


def test_c08_reduced_capacity_accept():
    coordinator = make(M.Caps(3, 3))
    assert coordinator.observe(window(), supplied_context=A).decision == "act_alpha"


def test_c09_capacity_precheck():
    coordinator = make(M.Caps(64, 4))
    before = coordinator.inspect()
    with pytest.raises(ValueError):
        coordinator.observe(window(route=(0.0, 0.0, 0.0)), supplied_context=A)
    assert coordinator.inspect() == before
    assert coordinator.inspect()["_backend"]["advance_calls"] == 0


def test_c10_insufficient_capacity():
    coordinator = make(M.Caps(2, 8))
    before = coordinator.inspect()
    with pytest.raises(ValueError):
        coordinator.observe(window(), supplied_context=A)
    assert coordinator.inspect() == before


def test_c11_identity_rename():
    left, left_action = observed(A, "occ-001")
    right, right_action = observed(A, "unrelated-token-z")
    finish(left)
    finish(right, event_id="unrelated-token-z", receipt_id="different-receipt-y")
    assert action_values(left_action) == action_values(right_action)
    assert numeric_projection(left) == numeric_projection(right)
    assert left.inspect()["_events"] != right.inspect()["_events"]


def test_c12_pending_credit():
    coordinator, _ = observed(B)
    pending = coordinator.inspect()["_pending"]["observation"]
    revision = finish(coordinator, outcome=-1.0)
    state = coordinator.inspect()
    assert state["_consumer"]["credited"] == [(pending, -1.0)]
    assert state["_backend"]["advance_calls"] == 1
    assert state["_consumer"]["feedback_calls"] == 1
    assert revision.sequence == 1 and state["_pending"] is None


def test_c13_duplicate_receipt():
    coordinator, _ = observed()
    revision = finish(coordinator)
    before = coordinator.inspect()
    replay = coordinator.deliver(M.Receipt("receipt-001", "occ-001", 1.0), delivered_ms=999)
    assert replay == revision
    assert coordinator.inspect() == before


def test_c14_conflicting_receipt():
    coordinator, _ = observed()
    finish(coordinator)
    before = coordinator.inspect()
    with pytest.raises(ValueError, match="identity conflict"):
        coordinator.deliver(M.Receipt("receipt-001", "occ-001", -1.0), delivered_ms=90)
    assert coordinator.inspect() == before


def test_c15_wrong_event_receipt():
    coordinator, _ = observed()
    before = coordinator.inspect()
    with pytest.raises(ValueError, match="pending occurrence"):
        coordinator.deliver(M.Receipt("receipt-001", "wrong-event", 1.0), delivered_ms=80)
    assert coordinator.inspect() == before


def test_c16_clock_boundaries():
    coordinator = make()
    before = coordinator.inspect()
    with pytest.raises(ValueError):
        coordinator.observe(window(pulses=((41, "Q", 1.0),)), supplied_context=A)
    assert coordinator.inspect() == before
    coordinator.observe(window(), supplied_context=A)
    before = coordinator.inspect()
    with pytest.raises(ValueError, match="follow decision"):
        coordinator.deliver(M.Receipt("receipt-001", "occ-001", 1.0), delivered_ms=72)
    assert coordinator.inspect() == before


def test_c17_complete_fake_rollback():
    for fault in ("after_backend", "after_observe"):
        coordinator = make()
        before = coordinator.inspect()
        with pytest.raises(RuntimeError, match="injected"):
            coordinator.observe(window(), supplied_context=A, fault_at=fault)
        assert coordinator.inspect() == before
    for fault in ("after_feedback", "after_commit"):
        coordinator, _ = observed()
        before = coordinator.inspect()
        with pytest.raises(RuntimeError, match="injected"):
            coordinator.deliver(
                M.Receipt("receipt-001", "occ-001", 1.0), delivered_ms=80, fault_at=fault
            )
        assert coordinator.inspect() == before


def test_c18_observer_noninterference():
    normal, normal_action = observed()
    rendered, rendered_action = observed()
    before = rendered.inspect()
    assert '"transient_buffer"' in rendered.render()  # actual export path was called
    assert rendered.inspect() == before
    assert rendered_action == normal_action and rendered.inspect() == normal.inspect()
    finish(normal)
    finish(rendered)
    rendered.render()
    assert normal.inspect() == rendered.inspect()


def test_c19_invalid_context():
    for context in ((float("nan"), 0.0), (1.0,)):
        coordinator = make()
        before = coordinator.inspect()
        with pytest.raises(ValueError):
            coordinator.observe(window(), supplied_context=context)
        assert coordinator.inspect() == before


def test_c20_reserved_channel():
    coordinator = make()
    before = coordinator.inspect()
    with pytest.raises(ValueError, match="reserved"):
        coordinator.observe(window(sensory=(("temporal_0", 0.0),)), supplied_context=A)
    assert coordinator.inspect() == before


def test_c21_channel_schema():
    coordinator, _ = observed()
    finish(coordinator)
    before = coordinator.inspect()
    changed = window("occ-002", 1, sensory=(("other_signal", 0.0),))
    with pytest.raises(ValueError, match="schema changed"):
        coordinator.observe(changed, supplied_context=A)
    assert coordinator.inspect() == before


def test_c22_single_pending():
    coordinator, _ = observed()
    before = coordinator.inspect()
    with pytest.raises(RuntimeError, match="unresolved"):
        coordinator.observe(window("occ-002", 1), supplied_context=B)
    assert coordinator.inspect() == before
    assert asdict(coordinator._pending.window) == asdict(window())
