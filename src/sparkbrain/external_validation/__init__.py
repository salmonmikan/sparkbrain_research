"""Model-independent external validation foundations."""

from .belief_r import (
    BeliefRPair,
    BeliefRSpec,
    BeliefRVerification,
    acquire_or_verify,
    load_belief_r_episodes,
    load_belief_r_spec,
    verify_belief_r_cache,
)
from .gate import ExternalModelGateError, require_model_evaluation_gate
from .schema import PredictionStep, RevisionTarget

__all__ = [
    "BeliefRPair",
    "BeliefRSpec",
    "BeliefRVerification",
    "ExternalModelGateError",
    "PredictionStep",
    "RevisionTarget",
    "acquire_or_verify",
    "load_belief_r_episodes",
    "load_belief_r_spec",
    "require_model_evaluation_gate",
    "verify_belief_r_cache",
]
