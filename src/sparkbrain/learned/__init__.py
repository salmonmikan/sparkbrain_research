"""Optional PyTorch learned-routing backend.

Importing :mod:`sparkbrain` does not import PyTorch.  Consumers opt in by
importing this package and installing the ``learned`` extra.
"""

from .backend import LearnedBrainBackend
from .config import LearnedConfig
from .contracts import EvaluationSummary, LearnedExample, PredictionRecord, WorkCounters

__all__ = [
    "EvaluationSummary",
    "LearnedBrainBackend",
    "LearnedConfig",
    "LearnedExample",
    "PredictionRecord",
    "WorkCounters",
]
