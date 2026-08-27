"""Target-blind synthetic C19 proxy and conservative fault attribution."""

from __future__ import annotations

import random
from typing import Any

from .contracts import FaultAttribution, digest, validate_attribution_row, validate_prediction_row


def fresh_proxy_splits(*, seed: int, episodes_per_split: int = 4) -> dict[str, list[str]]:
    """Create disjoint opaque IDs; no official dataset text or labels are used."""

    if episodes_per_split < 1:
        raise ValueError("episodes_per_split must be positive")
    generator = random.Random(seed)
    identifiers = [f"proxy-{generator.getrandbits(64):016x}" for _ in range(episodes_per_split * 3)]
    if len(set(identifiers)) != len(identifiers):
        raise RuntimeError("proxy identifier collision")
    return {
        "train": identifiers[:episodes_per_split],
        "dev": identifiers[episodes_per_split : 2 * episodes_per_split],
        "synthetic_proxy": identifiers[2 * episodes_per_split :],
    }


def attribute_fault(
    *,
    entity_count: int,
    local_correct: bool,
    oracle_correct: bool,
    gate_changed_decision: bool,
    state_changed_decision: bool,
    objective_changed_decision: bool,
) -> FaultAttribution:
    """Return a cause only for a uniquely isolating intervention.

    Belief-R's one answer entity cannot distinguish entity binding from other
    components, therefore that axis always remains inconclusive there.
    """

    if entity_count == 1:
        return FaultAttribution("inconclusive", None, "single_entity_no_binding_counterfactual")
    candidates = []
    if not local_correct and oracle_correct:
        candidates.append("input")
    if gate_changed_decision:
        candidates.append("gate")
    if state_changed_decision:
        candidates.append("state")
    if objective_changed_decision:
        candidates.append("objective")
    if len(candidates) != 1:
        return FaultAttribution("inconclusive", None, "non_identifying_or_multiple_counterfactuals")
    return FaultAttribution("attributed", candidates[0], "unique_registered_counterfactual")


def synthetic_proxy_row(
    *, seed: int, episode_id: str, input_track: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """A deterministic schema exercise, explicitly not an official evaluation."""

    prediction = "retain" if input_track != "I0_whole_hash" else "revise"
    truth = "retain"
    fault = attribute_fault(
        entity_count=2,
        local_correct=prediction == truth,
        oracle_correct=True,
        gate_changed_decision=False,
        state_changed_decision=False,
        objective_changed_decision=False,
    )
    episode_hash = digest({"seed": seed, "episode_id": episode_id})
    row = {
        "condition_id": f"{input_track}/G0_probability_margin/E1_oracle_entity",
        "entity_count": 2,
        "evaluator_only": input_track == "I2_symbolic_oracle",
        "episode_id_hash": episode_hash,
        "fault_attribution": fault.to_dict(),
        "input_track": input_track,
        "oracle_diagnostic": input_track == "I2_symbolic_oracle",
        "prediction": prediction,
        "probabilities": {
            "retain": 0.75 if prediction == "retain" else 0.25,
            "revise": 0.25 if prediction == "retain" else 0.75,
        },
        "seed": seed,
        "split": "synthetic_proxy",
        "step_index": 0,
        "track": "oracle" if input_track == "I2_symbolic_oracle" else "autonomous",
        "trace_checkpoint_hash": None,
        "truth": truth,
        "work_counters": {"active_sparks": 0, "edge_evaluations": 0, "state_updates": 0},
    }
    attribution = {
        "available": fault.status == "attributed",
        "condition_id": row["condition_id"],
        "dominant_component": fault.dominant_component,
        "entity_count": 2,
        "episode_id_hash": episode_hash,
        "reason": fault.reason,
        "seed": seed,
        "status": fault.status,
    }
    validate_prediction_row(row)
    validate_attribution_row(attribution)
    return row, attribution
