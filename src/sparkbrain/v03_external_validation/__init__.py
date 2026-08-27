"""C19 preregistered external-validation contracts.

This namespace is deliberately evaluation-disabled until C18 exposes its
accepted public trace/checkpoint contract.  It contains no dataset loader and
cannot execute an official Belief-R evaluation.
"""

from .contracts import (
    EXACT_NINE_ARTIFACTS,
    C18TraceCheckpointAdapter,
    FaultAttribution,
    validate_disabled_preregistration,
)

__all__ = [
    "C18TraceCheckpointAdapter",
    "EXACT_NINE_ARTIFACTS",
    "FaultAttribution",
    "validate_disabled_preregistration",
]
