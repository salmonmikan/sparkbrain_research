from __future__ import annotations

from .contracts import V03Checkpoint, V03TraceSession, _hash


def replay_trace(checkpoint: V03Checkpoint) -> V03TraceSession:
    """Verify the recorded hash chain and restore the stored checkpoint only.

    State is not inferred from UI fields.  The terminal checkpoint is the sole
    restore authority, while event hashes provide tamper detection.
    """
    previous = None
    for index, event in enumerate(checkpoint.trace):
        if event.sequence != index or event.branch_id != checkpoint.branch_id:
            raise ValueError("trace ordering or branch lineage is invalid")
        if previous is not None and event.state_hash_before != previous:
            raise ValueError("trace state-hash chain is broken")
        previous = event.state_hash_after
    if checkpoint.trace and previous != checkpoint.state_hash:
        raise ValueError("trace terminal hash does not match checkpoint")
    if _hash(checkpoint.state) != checkpoint.state_hash:
        raise ValueError("checkpoint state hash mismatch")
    session = V03TraceSession(
        config=checkpoint.config,
        branch_id=checkpoint.branch_id,
        state=dict(checkpoint.state),
        parent_checkpoint_id=checkpoint.parent_checkpoint_id,
    )
    session._events = list(checkpoint.trace)
    return session


def replay_checkpoint(checkpoint: V03Checkpoint) -> str:
    return replay_trace(checkpoint).state_hash()
