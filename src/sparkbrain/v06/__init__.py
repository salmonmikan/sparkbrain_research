"""SparkBrain v0.6 assembly-free endogenous-dynamics foundation.

V06-00 through V06-02 establish the preregistered provenance, anti-self-
confirmation, Assembly-free runtime-state, observer-isolation, and checkpoint
contracts. G0/G1/G2 endogenous dynamics are not claimed by this slice.
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

__version__ = "0.6.0.dev0"

__all__ = [
    "AssemblyFreeRuntimeState",
    "EndogenousChainRecord",
    "EndogenousPulseProposal",
    "EventOrigin",
    "ImmutableRuntimeTrace",
    "LearningEligibility",
    "ProvenanceLedger",
    "RealityMatchRecord",
    "RuntimeObserver",
    "RuntimePulse",
    "build_checkpoint",
    "load_checkpoint",
    "run_observer",
    "save_checkpoint",
    "validate_checkpoint",
    "validate_runtime_mapping",
    "verify_non_interference",
]
