from __future__ import annotations

import pytest

from sparkbrain.v03_integration import V03Checkpoint, V03TraceSession, replay_checkpoint


def make() -> V03TraceSession:
    item = V03TraceSession({"seed": 1802}, state={"evidence": {"e1": {"active": True}}})
    item.record(
        "coalition_evaluated", {"cited_evidence_ids": ["e1"]}, {"beliefs": {"a": {"winner": "cat"}}}
    )
    return item


def test_hashes_bind_payload_root_and_lineage() -> None:
    checkpoint = make().checkpoint("one")
    assert replay_checkpoint(checkpoint) == checkpoint.state_hash
    for edit in (
        lambda v: v["trace"][0]["payload"].update({"x": 1}),
        lambda v: v.update({"initial_state_hash": "0" * 64}),
    ):
        value = checkpoint.as_dict()
        edit(value)
        with pytest.raises(ValueError):
            V03Checkpoint.from_dict(value)


def test_citations_pre_event_and_fork_replay() -> None:
    item = make()
    with pytest.raises(ValueError):
        item.record("evidence_added", {"evidence_id": "e2", "cited_evidence_ids": ["e2"]}, {})
    child = item.fork(item.checkpoint("one"), branch_id="b", intervention={"kind": "remove"})
    assert child.parent_checkpoint_id == "one"


def test_extra_state_rejected() -> None:
    value = make().checkpoint("one").as_dict()
    value["state"]["extra"] = True
    with pytest.raises(ValueError):
        V03Checkpoint.from_dict(value)
