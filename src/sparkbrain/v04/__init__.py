"""SparkBrain v0.4 pre-semantic temporal signal dynamics.

v0.4 is intentionally isolated from the semantic v0.3 reference runtime.  It
models transduction, local excitation, delayed propagation, adaptation, bursts,
cascades, temporal assemblies, ignition, and reward-modulated plasticity.
"""

__version__ = "0.4.0.dev0"

from .brain import IntegratedV04Brain, V04BrainConfig
from .contracts import (
    BurstEvent,
    CascadeEvent,
    IgnitionEvent,
    SignalPulse,
    SpikeEvent,
    V04StepResult,
)
from .dynamics import (
    AssemblyMemory,
    BurstDetector,
    CascadeTracker,
    IgnitionGate,
)
from .evaluation import run_reference_experiments
from .field import ExcitableFieldConfig, TemporalExcitableField
from .plasticity import TimingPlasticityConfig, TimingPlasticityRule
from .topology import Connection, FieldTopology, UnitState, explicit_topology, grid_topology
from .transduction import (
    FrameDeltaTransducer,
    ScalarDeltaTransducer,
    TemporalExpectationTracker,
    TextPulseTransducer,
    pulse_train,
)
from .visualizer import build_trace_html, write_trace_html

__all__ = [
    "__version__",
    "AssemblyMemory",
    "BurstDetector",
    "BurstEvent",
    "CascadeEvent",
    "CascadeTracker",
    "Connection",
    "ExcitableFieldConfig",
    "FieldTopology",
    "FrameDeltaTransducer",
    "IgnitionEvent",
    "IgnitionGate",
    "IntegratedV04Brain",
    "ScalarDeltaTransducer",
    "SignalPulse",
    "SpikeEvent",
    "TemporalExcitableField",
    "TemporalExpectationTracker",
    "TextPulseTransducer",
    "TimingPlasticityConfig",
    "TimingPlasticityRule",
    "UnitState",
    "V04BrainConfig",
    "V04StepResult",
    "build_trace_html",
    "explicit_topology",
    "grid_topology",
    "pulse_train",
    "run_reference_experiments",
    "write_trace_html",
]
