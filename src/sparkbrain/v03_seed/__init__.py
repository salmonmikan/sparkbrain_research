"""Executable v0.3 design seeds.

These components are intentionally isolated from the accepted v0.2.1 runtime.
They are reference implementations for Codex integration, ablation, and review;
they are not evidence that v0.3 performance or biological fidelity is established.
"""

from .belief import BeliefFieldConfig, PersistentBeliefField
from .coalition import CoalitionGate, CoalitionGateConfig
from .concepts import ConceptFormationConfig, OnlineConceptFormer
from .contracts import (
    BeliefActivation,
    CoalitionState,
    ConceptCandidate,
    EvidenceContribution,
    EvidenceSummary,
    IgnitionDecision,
    OrganAssessment,
    OrganEvidence,
    PerceptualSpark,
    SensorySample,
)
from .evidence import EvidenceLedger, EvidenceLedgerConfig
from .input_diagnosis import (
    AUTONOMOUS_INPUT_TRACKS,
    DEFAULT_INPUT_TRACK,
    ORACLE_INPUT_TRACK,
    FeatureRecord,
    FrozenPairEvaluator,
    InputFrontend,
    InputRecord,
    LocalCompositionalFrontend,
    PairPrediction,
    StrictSymbolicOracleFrontend,
    WholeHashFrontend,
    create_frontend,
)
from .loop import PerceptualInterpreter, V03ReferenceLoop, V03StepResult
from .organs import OrganGateConfig, assess_organ_candidate
from .sensory_field import (
    AdaptiveSensoryField,
    SensoryChannelTrace,
    SensoryFieldConfig,
    SensoryObservation,
    SensoryWorkCounters,
)
from .sensory_worlds import (
    DistractorNoiseWorld,
    GoalTargetWorld,
    HabituationWorld,
    SensoryWorldStep,
    StimulusSpecificityWorld,
    UnexpectedChangeWorld,
)
from .text_frontend import (
    compositional_text_features,
    normalize_text,
    sparse_cosine_similarity,
    symbolic_metadata_features,
    whole_string_hash_features,
)

__all__ = [
    "AdaptiveSensoryField",
    "BeliefActivation",
    "BeliefFieldConfig",
    "CoalitionGate",
    "CoalitionGateConfig",
    "CoalitionState",
    "ConceptCandidate",
    "ConceptFormationConfig",
    "EvidenceContribution",
    "EvidenceLedger",
    "EvidenceLedgerConfig",
    "EvidenceSummary",
    "DistractorNoiseWorld",
    "AUTONOMOUS_INPUT_TRACKS",
    "DEFAULT_INPUT_TRACK",
    "ORACLE_INPUT_TRACK",
    "FeatureRecord",
    "FrozenPairEvaluator",
    "InputFrontend",
    "InputRecord",
    "LocalCompositionalFrontend",
    "PairPrediction",
    "StrictSymbolicOracleFrontend",
    "WholeHashFrontend",
    "create_frontend",
    "IgnitionDecision",
    "GoalTargetWorld",
    "HabituationWorld",
    "OnlineConceptFormer",
    "OrganAssessment",
    "OrganEvidence",
    "OrganGateConfig",
    "PerceptualInterpreter",
    "PerceptualSpark",
    "PersistentBeliefField",
    "SensoryFieldConfig",
    "SensoryChannelTrace",
    "SensoryObservation",
    "SensorySample",
    "SensoryWorkCounters",
    "SensoryWorldStep",
    "StimulusSpecificityWorld",
    "UnexpectedChangeWorld",
    "V03ReferenceLoop",
    "V03StepResult",
    "assess_organ_candidate",
    "compositional_text_features",
    "normalize_text",
    "sparse_cosine_similarity",
    "symbolic_metadata_features",
    "whole_string_hash_features",
]
