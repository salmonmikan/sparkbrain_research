"""SparkBrain v0.5 pre-semantic functional temporal-assembly research."""

__version__ = "0.5.0.dev0"

from .action import ActionPolicyConfig, AssemblyActionPolicy
from .assemblies import (
    AssemblyCandidate,
    AssemblyConfig,
    TemporalAssemblyMemory,
    pattern_from_spikes,
    pattern_similarity,
    patterns_from_step,
)
from .brain import IntegratedV05Brain, V05BrainConfig
from .checkpoint import load_checkpoint, save_checkpoint
from .contracts import (
    ActionDecision,
    ActivityPattern,
    AssemblyActivation,
    PredictionDecision,
    ReceptorTrace,
    StabilitySnapshot,
    V05StepResult,
)
from .evaluation import render_v05_report, run_v05_reference_experiments
from .homeostasis import HomeostasisConfig, HomeostaticController
from .plasticity import V05PlasticityConfig, V05PlasticityController
from .prediction import AssemblyPredictor
from .receptors import MultiTimescaleReceptorBank, ReceptorConfig
from .topology import layered_reservoir_topology
from .visualizer import build_v05_html, write_v05_html
from .worlds import (
    MOTIF_X,
    MOTIF_Y,
    MotifDefinition,
    MotifEpisode,
    MotifWorldConfig,
    held_out_episodes,
    make_episode,
    training_episodes,
)

__all__ = [
    "__version__",
    "ActionDecision",
    "ActionPolicyConfig",
    "ActivityPattern",
    "AssemblyActionPolicy",
    "AssemblyActivation",
    "AssemblyCandidate",
    "AssemblyConfig",
    "AssemblyPredictor",
    "HomeostasisConfig",
    "HomeostaticController",
    "IntegratedV05Brain",
    "MOTIF_X",
    "MOTIF_Y",
    "MotifDefinition",
    "MotifEpisode",
    "MotifWorldConfig",
    "MultiTimescaleReceptorBank",
    "PredictionDecision",
    "ReceptorConfig",
    "ReceptorTrace",
    "StabilitySnapshot",
    "TemporalAssemblyMemory",
    "V05BrainConfig",
    "V05PlasticityConfig",
    "V05PlasticityController",
    "V05StepResult",
    "build_v05_html",
    "held_out_episodes",
    "layered_reservoir_topology",
    "load_checkpoint",
    "make_episode",
    "pattern_from_spikes",
    "pattern_similarity",
    "patterns_from_step",
    "render_v05_report",
    "run_v05_reference_experiments",
    "save_checkpoint",
    "training_episodes",
    "write_v05_html",
]
