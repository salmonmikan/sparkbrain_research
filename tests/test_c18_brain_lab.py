from __future__ import annotations

import inspect
from dataclasses import replace

import pytest

from sparkbrain.v03_integration import (
    V03Checkpoint,
    V03TraceSession,
    replay_checkpoint,
    replay_trace,
)


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
    parent = item.checkpoint("one")
    child_checkpoint = child.checkpoint("child")
    assert child_checkpoint.parent_checkpoint_hash == parent.canonical_hash()
    assert child.events[0].parent_event_hash == child_checkpoint.initial_state_hash
    replay_trace(child_checkpoint, parent_checkpoint=parent)


def test_public_trace_session_signatures_are_stable() -> None:
    assert tuple(inspect.signature(V03TraceSession.inspect).parameters) == ("self",)
    assert tuple(inspect.signature(V03TraceSession.record).parameters) == (
        "self",
        "kind",
        "payload",
        "delta",
    )
    assert tuple(inspect.signature(V03TraceSession.checkpoint).parameters) == (
        "self",
        "checkpoint_id",
    )
    assert tuple(inspect.signature(V03TraceSession.fork).parameters) == (
        "self",
        "checkpoint",
        "branch_id",
        "intervention",
    )


def test_extra_state_rejected() -> None:
    value = make().checkpoint("one").as_dict()
    value["state"]["extra"] = True
    with pytest.raises(ValueError):
        V03Checkpoint.from_dict(value)


def test_schema_rejects_missing_payload_and_nested_type() -> None:
    value = make().checkpoint("one").as_dict()
    value["trace"][0]["payload"].pop("cited_evidence_ids")
    with pytest.raises(ValueError):
        V03Checkpoint.from_dict(value)


def test_fork_rejects_parent_and_child_binding_tampering() -> None:
    parent = make().checkpoint("parent")
    child = make().fork(parent, branch_id="child", intervention={"kind": "remove"})
    child_checkpoint = child.checkpoint("child")
    for edit in (
        lambda value: value["trace"][0]["payload"].update({"parent_state_hash": "0" * 64}),
        lambda value: value.update({"parent_checkpoint_hash": "0" * 64}),
        lambda value: value["trace"][0].update({"parent_event_hash": "0" * 64}),
        lambda value: value["trace"][0]["payload"].pop("parent_checkpoint_hash"),
    ):
        value = child_checkpoint.as_dict()
        edit(value)
        with pytest.raises(ValueError):
            V03Checkpoint.from_dict(value)

    other = make().checkpoint("other")
    with pytest.raises(ValueError, match="fork parent binding"):
        replay_trace(child_checkpoint, parent_checkpoint=other)
    with pytest.raises(ValueError):
        replay_trace(replace(child_checkpoint, parent_checkpoint_hash=None))


def test_fork_rejects_tampered_parent_state_event_payload_and_hash() -> None:
    parent = make().checkpoint("parent")
    for edit in (
        lambda value: value["state"]["beliefs"].update({"tampered": True}),
        lambda value: value["trace"][0].update({"event_hash": "0" * 64}),
        lambda value: value["trace"][0]["payload"].update({"reason": "tampered"}),
        lambda value: value.update({"state_hash": "0" * 64}),
    ):
        value = parent.as_dict()
        edit(value)
        with pytest.raises(ValueError):
            V03Checkpoint.from_dict(value)
    direct_tampered = (
        replace(parent, state={**parent.state, "beliefs": {"tampered": True}}),
        replace(parent, state_hash="0" * 64),
        replace(parent, trace=(replace(parent.trace[0], event_hash="0" * 64),)),
        replace(parent, trace=(replace(parent.trace[0], payload={"cited_evidence_ids": []}),)),
    )
    item = make()
    for checkpoint in direct_tampered:
        with pytest.raises(ValueError):
            item.fork(checkpoint, branch_id="tampered", intervention={"kind": "remove"})
    value = make().checkpoint("one").as_dict()
    value["state"]["suppressed_modules"] = "not-an-array"
    with pytest.raises(ValueError):
        V03Checkpoint.from_dict(value)
