"""Public v0.3.1 integrated runtime facade.

The facade composes the reviewed v0.3 components without changing the frozen
v0.3 experiment or persistence contracts.
"""

from sparkbrain.v03_seed import SensorySample

from .evaluation import (
    ENGINEERING_METRICS,
    ENGINEERING_VARIANTS,
    ENGINEERING_WORLDS,
    evaluate_engineering_runtime,
    validate_engineering_evaluation,
)
from .runtime import IntegratedV03Brain, V03BrainConfig, V03StepResult

__all__ = [
    "IntegratedV03Brain",
    "ENGINEERING_METRICS",
    "ENGINEERING_VARIANTS",
    "ENGINEERING_WORLDS",
    "SensorySample",
    "V03BrainConfig",
    "V03StepResult",
    "evaluate_engineering_runtime",
    "validate_engineering_evaluation",
]
