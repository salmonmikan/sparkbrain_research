"""SparkBrain v0.6 Assembly-free and taxonomy-free endogenous Dynamics.

The package initializer installs Protocol-Amendment-002 runtime guards before
exposing the Primary modules. V06-00 through V06-09 establish provenance,
anti-self-confirmation, observer isolation, G0/G1/G2 Dynamics, normal-rule
reinjection, external correction, state-dependence probes, and an
intervention-ready autonomous endogenous-chain runtime.
"""

from .taxonomy import (
    ALLOWED_STRUCTURAL_EXAMPLES,
    FORBIDDEN_FUNCTIONAL_CLASS_NAMES,
    FORBIDDEN_FUNCTIONAL_FIELDS,
    audit_runtime_source_tree,
    install_runtime_taxonomy_guard,
    validate_taxonomy_free_mapping,
    verify_taxonomy_variant_runtime_equality,
)

install_runtime_taxonomy_guard()

from .endogenous_chain import (  # noqa: E402
    AutonomousEndogenousChainRuntime,
    EndogenousChainConfig,
    EndogenousChainIntervention,
    EndogenousChainSpark,
    EndogenousInterventionRecord,
    EndogenousProposalRecord,
)
from .forward import (  # noqa: E402
    AssemblyFreeForwardRuntime,
    EndogenousSparkRecord,
    ExternalStepRecord,
    ForwardCompletionEvaluation,
    ForwardRuntimeConfig,
    ProposalScheduleRecord,
    evaluate_forward_completion,
    train_external_sequences,
)
from .foundation import (  # noqa: E402
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
from .g0 import (  # noqa: E402
    G0Comparison,
    QueueControlResult,
    classify_g0_support,
    compare_queue_controls,
    field_with_queue_mode,
    run_queue_condition,
)
from .local_expectation import (  # noqa: E402
    LocalExpectationConfig,
    LocalTemporalExpectation,
    LocalTransitionStats,
)
from .local_transition import (  # noqa: E402
    LocalPathAdaptation,
    LocalTransitionResolution,
    PendingLocalTransition,
    PreparedLocalTransition,
    SparseLocalTransitionAdaptation,
    SparseTransitionConfig,
)
from .reality import (  # noqa: E402
    EndogenousLineageIndex,
    QueueCancellation,
    RealityCorrectionConfig,
    RealityCorrectionEngine,
    RealityCorrectionResult,
)
from .reinjection import (  # noqa: E402
    FieldReinjectionGate,
    ReinjectionConfig,
    ReinjectionDecision,
)

__version__ = "0.6.0.dev0"

__all__ = [
    "ALLOWED_STRUCTURAL_EXAMPLES",
    "AssemblyFreeForwardRuntime",
    "AssemblyFreeRuntimeState",
    "AutonomousEndogenousChainRuntime",
    "EndogenousChainConfig",
    "EndogenousChainIntervention",
    "EndogenousChainRecord",
    "EndogenousChainSpark",
    "EndogenousInterventionRecord",
    "EndogenousLineageIndex",
    "EndogenousProposalRecord",
    "EndogenousPulseProposal",
    "EndogenousSparkRecord",
    "EventOrigin",
    "ExternalStepRecord",
    "FORBIDDEN_FUNCTIONAL_CLASS_NAMES",
    "FORBIDDEN_FUNCTIONAL_FIELDS",
    "FieldReinjectionGate",
    "ForwardCompletionEvaluation",
    "ForwardRuntimeConfig",
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
    "ProposalScheduleRecord",
    "ProvenanceLedger",
    "QueueCancellation",
    "QueueControlResult",
    "RealityCorrectionConfig",
    "RealityCorrectionEngine",
    "RealityCorrectionResult",
    "RealityMatchRecord",
    "ReinjectionConfig",
    "ReinjectionDecision",
    "RuntimeObserver",
    "RuntimePulse",
    "SparseLocalTransitionAdaptation",
    "SparseTransitionConfig",
    "audit_runtime_source_tree",
    "build_checkpoint",
    "classify_g0_support",
    "compare_queue_controls",
    "evaluate_forward_completion",
    "field_with_queue_mode",
    "install_runtime_taxonomy_guard",
    "load_checkpoint",
    "run_observer",
    "run_queue_condition",
    "save_checkpoint",
    "train_external_sequences",
    "validate_checkpoint",
    "validate_runtime_mapping",
    "validate_taxonomy_free_mapping",
    "verify_non_interference",
    "verify_taxonomy_variant_runtime_equality",
]
