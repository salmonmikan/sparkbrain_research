"""Read-only v0.3 trace, checkpoint, replay and intervention contracts.

This namespace deliberately does not alter v0.2 readers, runtime APIs, or the
existing Brain Lab.  It consumes explicit v0.3 state supplied by a caller.
"""

from .contracts import (
    TRACE_SCHEMA_VERSION,
    V03Checkpoint,
    V03TraceEvent,
    V03TraceSession,
    canonical_json,
)
from .replay import replay_checkpoint, replay_trace

__all__ = [
    "TRACE_SCHEMA_VERSION",
    "V03Checkpoint",
    "V03TraceEvent",
    "V03TraceSession",
    "canonical_json",
    "replay_checkpoint",
    "replay_trace",
]
