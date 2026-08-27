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
from .readiness import (
    C19ReadinessValidationError,
    build_frozen_protocol,
    validate_bundle,
    write_blocked_readiness_bundle,
)

__all__ = [
    "C18TraceCheckpointAdapter",
    "EXACT_NINE_ARTIFACTS",
    "FaultAttribution",
    "C19ReadinessValidationError",
    "build_frozen_protocol",
    "validate_bundle",
    "validate_disabled_preregistration",
    "write_blocked_readiness_bundle",
]
