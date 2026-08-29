"""SparkBrain v0.6 assembly-free endogenous-dynamics foundation.

V06-00 through V06-05 establish provenance, anti-self-confirmation,
Assembly-free runtime state, observer isolation, checkpoints, the G0
queue-drain diagnostic, G1 local timing expectations, and G2 sparse local
transition adaptation. Field reinjection is not yet implemented.
"""

from .foundation import (
    AssemblyFreeRuntimeState,
    EndogenousChainRecord,
    EndogenousPulseProposal,
    EventOrigin,
    ImmutableRuntimeTrace,
    LearningEligibility,
    ProvenanceLedger,
    RealityMatchRecord,
    RuntimeObserver,
    RuntimePulse,
    build_checkpoint,
    load_checkpoint,
    run_observer,
    save_checkpoint,
    validate_checkpoint,
    validate_runtime_mapping,
    verify_non_interference,
)
from .g0 import (
    G0Comparison,
    QueueControlResult,
    classify_g0_support,
    compare_queue_controls,
    field_with_queue_mode,
    run_queue_condition,
)
from .local_expectation import (
    LocalExpectationConfig,
    LocalTemporalExpectation,
    LocalTransitionStats,
)
from .local_transition import (
    LocalPathAdaptation,
    LocalTransitionResolution,
    PendingLocalTransition,
    PreparedLocalTransition,
    SparseLocalTransitionAdaptation,
    SparseTransitionConfig,
)

__version__ = "0.6.0.dev0"

__all__ = [
    "AssemblyFreeRuntimeState",
    "EndogenousChainRecord",
    "EndogenousPulseProposal",
    "EventOrigin",
    "G0Comparison",
    "ImmutableRuntimeTrace",
    "LearningEligibility",
    "LocalExpectationConfig",
    "LocalPathAdaptation",
    "LocalTemporalExpectation",
    "LocalTransitionResolution",
    "LocalTransitionStats",
    "PendingLocalTransition",
    "PreparedLocalTransition",
    "ProvenanceLedger",
    "QueueControlResult",
    "RealityMatchRecord",
    "RuntimeObserver",
    "RuntimePulse",
    "SparseLocalTransitionAdaptation",
    "SparseTransitionConfig",
    "build_checkpoint",
    "classify_g0_support",
    "compare_queue_controls",
    "field_with_queue_mode",
    "load_checkpoint",
    "run_observer",
    "run_queue_condition",
    "save_checkpoint",
    "validate_checkpoint",
    "validate_runtime_mapping",
    "verify_non_interference",
]
