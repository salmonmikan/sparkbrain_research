from __future__ import annotations

from sparkbrain.v03_integration import V03TraceSession, replay_checkpoint, replay_trace


def _session() -> V03TraceSession:
    session = V03TraceSession(config={"seed": 1801}, state={"evidence": {"e1": {"source": "vision"}}})
    session.record(
        "coalition_evaluated",
        {"cited_evidence_ids": ["e1"], "score_components": {"support": 1.0}},
        {"beliefs": {"object:a": {"winner": "cat", "residual_losers": ["toy"]}}},
    )
    return session


def test_checkpoint_replay_preserves_state_hash_and_trace() -> None:
    checkpoint = _session().checkpoint("checkpoint:one")
    restored = replay_trace(checkpoint)
    assert replay_checkpoint(checkpoint) == checkpoint.state_hash
    assert restored.inspect() == checkpoint.state
    assert restored.events == checkpoint.trace


def test_inspection_is_non_mutating_and_attribution_cannot_be_invented() -> None:
    session = _session()
    before = session.state_hash()
    assert session.inspect()["evidence"]["e1"]["source"] == "vision"
    assert session.state_hash() == before
    try:
        session.record("workspace_broadcast", {"cited_evidence_ids": ["missing"]}, {})
    except ValueError as error:
        assert "absent" in str(error)
    else:
        raise AssertionError("unknown evidence citation was accepted")


def test_fork_is_explicit_and_parent_checkpoint_is_unchanged() -> None:
    parent = _session()
    checkpoint = parent.checkpoint("checkpoint:one")
    child = parent.fork(checkpoint, branch_id="fork:goal", intervention={"kind": "alter_goal", "goal": "inspect"})
    assert child.parent_checkpoint_id == checkpoint.checkpoint_id
    assert child.events[0].kind == "intervention"
    assert parent.state_hash() == checkpoint.state_hash
