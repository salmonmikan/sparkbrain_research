"""SparkBrain v0.3.2 additive corrective APIs.

The v0.3.1 runtime remains available under :mod:`sparkbrain.v03`.  This package
contains corrected measurement semantics, direct checkpoints, sensory
suppression diagnostics, a pure residual-ablation helper, and a truth-free
multi-evidence input research scaffold.
"""

from .checkpoint import DirectCheckpointManager
from .contracts import SensoryChannelDecision, V032StepResult
from .input_semantics import (
    CompositionalInterpretation,
    RelationAwareLocalInterpreter,
    SemanticEvidence,
)
from .metrics import (
    AttributionMetrics,
    RevisionMetrics,
    action_mismatch_rate,
    attribution_metrics,
    revision_metrics,
)
from .residual import ResidualStateDiff, disable_loser_residual_only
from .runtime import IntegratedV032Brain

__all__ = [
    'AttributionMetrics',
    'CompositionalInterpretation',
    'DirectCheckpointManager',
    'IntegratedV032Brain',
    'RelationAwareLocalInterpreter',
    'ResidualStateDiff',
    'RevisionMetrics',
    'SemanticEvidence',
    'SensoryChannelDecision',
    'V032StepResult',
    'action_mismatch_rate',
    'attribution_metrics',
    'disable_loser_residual_only',
    'revision_metrics',
]
