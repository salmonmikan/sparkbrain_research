"""Isolated SparkBrain v0.6 confirmatory comparators.

Modules in this package may consume frozen experiment specifications and emit
confirmatory records. They must not be imported by the Primary v0.6 runtime.
"""

from .g3_recurrent import (
    G3QualificationGrid,
    GenericRecurrentPredictor,
    evaluate_world,
    run_condition,
    run_qualification_grid,
)

__all__ = [
    "G3QualificationGrid",
    "GenericRecurrentPredictor",
    "evaluate_world",
    "run_condition",
    "run_qualification_grid",
]
