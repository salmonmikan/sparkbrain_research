from __future__ import annotations

from .contracts import V03Checkpoint, V03TraceSession, _hash


def replay_trace(checkpoint: V03Checkpoint) -> V03TraceSession:
    checkpoint.as_dict()
    parent = before = checkpoint.initial_state_hash
    for index, event in enumerate(checkpoint.trace):
        if (
            event.sequence != index
            or event.branch_id != checkpoint.branch_id
            or event.parent_event_hash != parent
            or event.state_hash_before != before
        ):
            raise ValueError("trace lineage is broken")
        event.as_dict()
        parent, before = event.event_hash, event.state_hash_after
    if checkpoint.trace and before != checkpoint.state_hash:
        raise ValueError("trace terminal hash mismatch")
    if _hash(checkpoint.state) != checkpoint.state_hash:
        raise ValueError("checkpoint state hash mismatch")
    result = V03TraceSession(
        checkpoint.config,
        checkpoint.branch_id,
        dict(checkpoint.initial_state),
        checkpoint.parent_checkpoint_id,
    )
    result.initial_state = dict(checkpoint.initial_state)
    result.initial_hash = checkpoint.initial_state_hash
    result.config_hash = checkpoint.config_hash
    result.state = dict(checkpoint.state)
    result._events = list(checkpoint.trace)
    return result


def replay_checkpoint(checkpoint: V03Checkpoint) -> str:
    return replay_trace(checkpoint).state_hash()
