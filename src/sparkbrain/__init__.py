"""SparkBrain inspectable event-driven cognition research prototype."""

__version__ = "0.2.1"

from .engine import SparkBrain
from .model import BrainConfig, EventKind, Spark, SparkKind
from .protocols import BrainBackend
from .replay import TraceReplay, load_trace
from .serialization import dump_state, load_state, state_hash
from .validation import SCHEMA_VERSION

__all__ = [
    "__version__",
    "BrainBackend",
    "BrainConfig",
    "EventKind",
    "SCHEMA_VERSION",
    "Spark",
    "SparkBrain",
    "SparkKind",
    "TraceReplay",
    "dump_state",
    "load_state",
    "load_trace",
    "state_hash",
]
