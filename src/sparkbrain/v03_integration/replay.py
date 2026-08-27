from __future__ import annotations

from .contracts import V03Checkpoint, V03TraceSession, _hash


def replay_trace(
    checkpoint: V03Checkpoint, *, parent_checkpoint: V03Checkpoint | None = None
) -> V03TraceSession:
    checkpoint.as_dict()
    if checkpoint.parent_checkpoint_id is not None:
        if parent_checkpoint is None:
            pass
        else:
            replay_trace(parent_checkpoint)
            parent_hash = parent_checkpoint.canonical_hash()
            fork_point = (
                parent_checkpoint.trace[-1].event_hash
                if parent_checkpoint.trace
                else parent_checkpoint.initial_state_hash
            )
            if (
                checkpoint.parent_checkpoint_id != parent_checkpoint.checkpoint_id
                or checkpoint.parent_checkpoint_hash != parent_hash
                or checkpoint.parent_state_hash != parent_checkpoint.state_hash
                or checkpoint.fork_point_event_hash != fork_point
            ):
                raise ValueError("fork parent binding is broken")
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
    if checkpoint.trace:
        if before != checkpoint.state_hash or _hash(checkpoint.state) != checkpoint.state_hash:
            raise ValueError("trace terminal hash mismatch")
    elif (
        checkpoint.state != checkpoint.initial_state
        or checkpoint.state_hash != checkpoint.initial_state_hash
    ):
        raise ValueError("empty trace terminal hash mismatch")
    if checkpoint.parent_checkpoint_id is not None:
        first = checkpoint.trace[0] if checkpoint.trace else None
        if (
            first is None
            or first.kind != "intervention"
            or first.payload.get("parent_checkpoint_hash")
            != checkpoint.parent_checkpoint_hash
            or first.payload.get("parent_state_hash") != checkpoint.parent_state_hash
            or _hash(first.payload.get("intervention")) != checkpoint.intervention_hash
        ):
            raise ValueError("fork intervention binding is broken")
    result = V03TraceSession(
        checkpoint.config,
        checkpoint.branch_id,
        dict(checkpoint.initial_state),
        checkpoint.parent_checkpoint_id,
        checkpoint.parent_checkpoint_hash,
        checkpoint.parent_state_hash,
        checkpoint.fork_point_event_hash,
        checkpoint.intervention_hash,
    )
    result.initial_state = dict(checkpoint.initial_state)
    result.initial_hash = checkpoint.initial_state_hash
    result.config_hash = checkpoint.config_hash
    result.state = dict(checkpoint.state)
    result._events = list(checkpoint.trace)
    return result


def replay_checkpoint(checkpoint: V03Checkpoint) -> str:
    return replay_trace(checkpoint).state_hash()
