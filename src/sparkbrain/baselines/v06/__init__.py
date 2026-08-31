"""Isolated SparkBrain v0.6 confirmatory comparators.

Modules in this package may consume frozen experiment specifications and emit
confirmatory records. They must not be imported by the Primary v0.6 runtime.
"""

from .g3_recurrent import G3QualificationGrid, GenericRecurrentPredictor
from .g3_recurrent import evaluate_world as evaluate_g3_world
from .g3_recurrent import run_condition as run_g3_condition
from .g3_recurrent import run_qualification_grid as run_g3_qualification_grid
from .g4_assembly import (
    AssemblyComparatorConfig,
    ExplicitAssemblyComparator,
    ExplicitAssemblyPrototype,
    G4QualificationGrid,
)
from .g4_assembly import evaluate_world as evaluate_g4_world
from .g4_assembly import run_condition as run_g4_condition
from .g4_assembly import run_qualification_grid as run_g4_qualification_grid
from .g5_typed import (
    G5QualificationGrid,
    TypedFunctionalHeadComparator,
    TypedHeadConfig,
)
from .g5_typed import evaluate_world as evaluate_g5_world
from .g5_typed import run_condition as run_g5_condition
from .g5_typed import run_qualification_grid as run_g5_qualification_grid

__all__ = [
    "AssemblyComparatorConfig",
    "ExplicitAssemblyComparator",
    "ExplicitAssemblyPrototype",
    "G3QualificationGrid",
    "G4QualificationGrid",
    "G5QualificationGrid",
    "GenericRecurrentPredictor",
    "TypedFunctionalHeadComparator",
    "TypedHeadConfig",
    "evaluate_g3_world",
    "evaluate_g4_world",
    "evaluate_g5_world",
    "run_g3_condition",
    "run_g3_qualification_grid",
    "run_g4_condition",
    "run_g4_qualification_grid",
    "run_g5_condition",
    "run_g5_qualification_grid",
]
