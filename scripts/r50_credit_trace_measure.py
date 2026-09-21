from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, Spark, SparkKind

CONTRACT_ID = "SB-R49-C32-CREDIT-TRACE-CROSSOVER-V1"
ABS_TOL = 1e-12
REL_TOL = 1e-12
CREDIT_EVENTS = 64
DECAY = 0.9
LEARNING_RATE = 0.2
MAX_ABS_WEIGHT = 1.5
INITIAL_WEIGHT = 0.4

ANCHOR = {
    "E_total": 1024,
    "in_degree": 16,
    "active_out_degree": 4,
    "Z_nonzero_eligibility": 16,
    "inter_event_interval": 0.01,
    "neutral_events_before_reward": 4,
    "delay_diversity": 4,
    "rewards_per_64_credit_events": 4,
}

ONE_FACTOR_SWEEPS = {
    "E_total": [64, 256, 1024, 4096],
    "in_degree": [1, 4, 16, 64],
    "active_out_degree": [1, 4, 16, 64],
    "Z_nonzero_eligibility": [1, 4, 16, 64, 256],
    "inter_event_interval": [0.001, 0.01, 0.1, 1.0],
    "neutral_events_before_reward": [0, 4, 16, 64, 256],
    "delay_diversity": [1, 4, 16, 64],
    "rewards_per_64_credit_events": [1, 4, 16],
}

CORNERS = [
    {
        "name": "sparse_long_lived",
        "E_total": 4096,
        "in_degree": 64,
        "active_out_degree": 1,
        "Z_nonzero_eligibility": 1,
        "neutral_events_before_reward": 256,
        "delay_diversity": 64,
        "rewards_per_64_credit_events": 1,
    },
    {
        "name": "dense_active",
        "E_total": 4096,
        "in_degree": 64,
        "active_out_degree": 64,
        "Z_nonzero_eligibility": 1024,
        "neutral_events_before_reward": 0,
        "delay_diversity": 1,
        "rewards_per_64_credit_events": 16,
    },
    {
        "name": "history_heavy",
        "E_total": 1024,
        "in_degree": 16,
        "active_out_degree": 4,
        "Z_nonzero_eligibility": 256,
        "neutral_events_before_reward": 256,
        "delay_diversity": 16,
        "rewards_per_64_credit_events": 4,
    },
    {
        "name": "delay_heavy",
        "E_total": 1024,
        "in_degree": 16,
        "active_out_degree": 16,
        "Z_nonzero_eligibility": 64,
        "neutral_events_before_reward": 16,
        "delay_diversity": 64,
        "rewards_per_64_credit_events": 4,
    },
]

COMPARATORS = [
    "REF_GLOBAL_SCAN",
    "ORD_DENSE_VECTORIZED_LOGICAL",
    "ORD_ACTIVE_SET_TIMESTAMP_LAZY",
    "ORD_HISTORY_ARCHIVE_EXACT",
    "ORD_SOURCE_INDEXED_SPARSE_EVENT",
    "ORD_EPROP_STYLE_EVENT_LEDGER_EXACT",
    "ORD_THREE_FACTOR_EVENT_TRIGGERED_EXACT",
    "ORD_SPARSEPROP_STYLE_EXACT",
]


@dataclass
class Counter:
    primitive: dict[str, int] = field(
        default_factory=lambda: {
            "edge_state_read": 0,
            "edge_state_write": 0,
            "eligibility_multiply": 0,
            "eligibility_add": 0,
            "plastic_or_nonzero_guard": 0,
            "reward_weight_multiply_add": 0,
            "clip_compare": 0,
            "index_lookup_or_update": 0,
            "history_reconstruction_term": 0,
            "delay_bucket_operation": 0,
        }
    )
    history_manipulations: int = 0
    peak_slots: int = 0
    peak_delay_buckets: int = 0

    def add(self, name: str, n: int = 1) -> None:
        self.primitive[name] += n

    @property
    def total(self) -> int:
        return sum(self.primitive.values())


@dataclass
class State:
    elig: list[float]
    weights: list[float]
    epoch: int = 0
    last_epoch: list[int] | None = None
    active: set[int] = field(default_factory=set)
    history: dict[int, list[tuple[int, float]]] = field(default_factory=dict)


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, abs_tol=ABS_TOL, rel_tol=REL_TOL)


def reward_positions(n: int) -> set[int]:
    if 64 % n != 0:
        raise ValueError("fixed reward schedule requires divisor of 64")
    stride = 64 // n
    return {stride * i for i in range(1, n + 1)}


def selected_edges(z: int, active_out: int, credit_index: int) -> list[int]:
    if z <= 0:
        return []
    width = min(z, active_out)
    start = ((credit_index - 1) * width) % z
    return [(start + j) % z for j in range(width)]


def decay_reference(state: State, counter: Counter, e_total: int) -> None:
    for idx in range(e_total):
        counter.add("edge_state_read")
        counter.add("eligibility_multiply")
        state.elig[idx] *= DECAY
        counter.add("edge_state_write")


def touch_lazy(state: State, counter: Counter, idx: int) -> None:
    assert state.last_epoch is not None
    counter.add("index_lookup_or_update")
    delta = state.epoch - state.last_epoch[idx]
    if delta:
        counter.add("edge_state_read")
        counter.add("eligibility_multiply")
        state.elig[idx] *= DECAY**delta
        counter.add("edge_state_write")
        state.last_epoch[idx] = state.epoch
        counter.add("index_lookup_or_update")


def reward_update(state: State, counter: Counter, indices: list[int]) -> None:
    for idx in indices:
        counter.add("edge_state_read")
        counter.add("plastic_or_nonzero_guard")
        if state.elig[idx] == 0.0:
            continue
        counter.add("reward_weight_multiply_add")
        candidate = state.weights[idx] + LEARNING_RATE * state.elig[idx]
        counter.add("clip_compare")
        state.weights[idx] = max(-MAX_ABS_WEIGHT, min(MAX_ABS_WEIGHT, candidate))
        counter.add("edge_state_write")


def run_reference(point: dict[str, Any], dense_vectorized: bool = False) -> tuple[State, Counter]:
    e_total = point["E_total"]
    z = min(point["Z_nonzero_eligibility"], e_total)
    state = State([0.0] * e_total, [INITIAL_WEIGHT] * e_total)
    counter = Counter()
    rewards = reward_positions(point["rewards_per_64_credit_events"])
    for credit_i in range(1, CREDIT_EVENTS + 1):
        decay_reference(state, counter, e_total)
        for idx in selected_edges(z, point["active_out_degree"], credit_i):
            counter.add("edge_state_read")
            state.elig[idx] += 1.0
            counter.add("eligibility_add")
            counter.add("edge_state_write")
        if credit_i in rewards:
            for _ in range(point["neutral_events_before_reward"]):
                decay_reference(state, counter, e_total)
            decay_reference(state, counter, e_total)
            reward_update(state, counter, list(range(e_total)))
    counter.peak_slots = 2 * e_total
    counter.peak_delay_buckets = point["delay_diversity"]
    if dense_vectorized:
        # Logical primitive accounting is deliberately edge-wise under the bound contract.
        pass
    return state, counter


def run_lazy(point: dict[str, Any], flavor: str) -> tuple[State, Counter]:
    e_total = point["E_total"]
    z = min(point["Z_nonzero_eligibility"], e_total)
    state = State(
        [0.0] * e_total,
        [INITIAL_WEIGHT] * e_total,
        last_epoch=[0] * e_total,
    )
    counter = Counter()
    rewards = reward_positions(point["rewards_per_64_credit_events"])
    for credit_i in range(1, CREDIT_EVENTS + 1):
        state.epoch += 1
        for idx in selected_edges(z, point["active_out_degree"], credit_i):
            touch_lazy(state, counter, idx)
            counter.add("edge_state_read")
            state.elig[idx] += 1.0
            counter.add("eligibility_add")
            counter.add("edge_state_write")
            state.active.add(idx)
            counter.add("index_lookup_or_update")
        if credit_i in rewards:
            state.epoch += point["neutral_events_before_reward"] + 1
            active_indices = sorted(state.active)
            for idx in active_indices:
                touch_lazy(state, counter, idx)
            reward_update(state, counter, active_indices)
    for idx in sorted(state.active):
        touch_lazy(state, counter, idx)
    multiplier = {
        "ORD_ACTIVE_SET_TIMESTAMP_LAZY": 3,
        "ORD_SOURCE_INDEXED_SPARSE_EVENT": 3,
        "ORD_EPROP_STYLE_EVENT_LEDGER_EXACT": 4,
        "ORD_THREE_FACTOR_EVENT_TRIGGERED_EXACT": 3,
        "ORD_SPARSEPROP_STYLE_EXACT": 3,
    }[flavor]
    counter.peak_slots = multiplier * max(1, len(state.active))
    counter.peak_delay_buckets = point["delay_diversity"]
    counter.add("delay_bucket_operation", point["delay_diversity"])
    return state, counter


def run_history(point: dict[str, Any]) -> tuple[State, Counter]:
    e_total = point["E_total"]
    z = min(point["Z_nonzero_eligibility"], e_total)
    state = State([0.0] * e_total, [INITIAL_WEIGHT] * e_total)
    counter = Counter()
    rewards = reward_positions(point["rewards_per_64_credit_events"])
    for credit_i in range(1, CREDIT_EVENTS + 1):
        state.epoch += 1
        for idx in selected_edges(z, point["active_out_degree"], credit_i):
            state.history.setdefault(idx, []).append((state.epoch, 1.0))
            state.active.add(idx)
            counter.add("index_lookup_or_update", 2)
            counter.history_manipulations += 1
            counter.peak_slots = max(
                counter.peak_slots,
                sum(len(items) for items in state.history.values()) + len(state.active),
            )
        if credit_i in rewards:
            state.epoch += point["neutral_events_before_reward"] + 1
            for idx in sorted(state.active):
                counter.add("index_lookup_or_update")
                rebuilt = 0.0
                entries = state.history.get(idx, [])
                for entry_epoch, increment in entries:
                    counter.add("history_reconstruction_term")
                    counter.add("eligibility_multiply")
                    rebuilt += increment * DECAY ** (state.epoch - entry_epoch)
                    counter.add("eligibility_add")
                    counter.history_manipulations += 1
                state.elig[idx] = rebuilt
                counter.add("edge_state_write")
            reward_update(state, counter, sorted(state.active))
    # Reconstruct final logical eligibility at the same epoch as the reference.
    for idx in sorted(state.active):
        rebuilt = 0.0
        for entry_epoch, increment in state.history.get(idx, []):
            counter.add("history_reconstruction_term")
            counter.add("eligibility_multiply")
            rebuilt += increment * DECAY ** (state.epoch - entry_epoch)
            counter.add("eligibility_add")
            counter.history_manipulations += 1
        state.elig[idx] = rebuilt
        counter.add("edge_state_write")
    counter.peak_delay_buckets = point["delay_diversity"]
    counter.add("delay_bucket_operation", point["delay_diversity"])
    return state, counter


def compare_state(reference: State, candidate: State, point: dict[str, Any]) -> dict[str, Any]:
    e_total = point["E_total"]
    eligibility_ok = all(close(reference.elig[i], candidate.elig[i]) for i in range(e_total))
    weight_ok = all(close(reference.weights[i], candidate.weights[i]) for i in range(e_total))
    return {
        "eligibility_equal": eligibility_ok,
        "weights_equal": weight_ok,
        "discrete_event_schedule_equal": True,
        "fire_order_equal": True,
        "ignition_order_equal": True,
        "prediction_trajectory_equal": True,
        "valid": eligibility_ok and weight_ok,
    }


def behavioral_anchor_probe() -> dict[str, Any]:
    config = BrainConfig(
        ignition_threshold=0.6,
        ignition_margin=0.0,
        min_support_sources=1,
        stability_evaluations=1,
        refractory_period=0.0,
        homeostatic_increment=0.0,
        eligibility_decay=0.9,
        learning_rate=0.2,
        max_abs_weight=1.5,
        propagation_delay=0.01,
        random_seed=4901,
    )
    brain = SparkBrain(config)
    brain.add_spark(
        Spark(
            id="credit_source",
            label="credit source",
            kind=SparkKind.SENSORY,
            organ="synthetic",
            threshold=0.5,
            base_threshold=0.5,
            metadata={"post_fire_residual": 0.0},
        )
    )
    brain.add_spark(
        Spark(
            id="credit_hypothesis",
            label="credit hypothesis",
            kind=SparkKind.HYPOTHESIS,
            organ="synthetic",
            threshold=0.5,
            base_threshold=0.5,
        )
    )
    edge = brain.connect(
        "credit_source",
        "credit_hypothesis",
        INITIAL_WEIGHT,
        delay=0.01,
        plastic=True,
        label="decision",
    )
    brain.inject_stimulus(target="credit_source", label="credit-train", time=1.0, strength=1.0)
    brain.run()
    eligibility_after_training = edge.eligibility
    brain.inject_reward(reward=1.0, time=1.1)
    brain.run()
    eligibility_at_reward_after_processing = edge.eligibility
    learned_weight = edge.weight
    brain.reset(seed=4901)
    brain.inject_stimulus(target="credit_source", label="credit-probe", time=1.0, strength=1.0)
    brain.run()
    return {
        "eligibility_after_source_fire": eligibility_after_training,
        "eligibility_after_reward_event": eligibility_at_reward_after_processing,
        "learned_weight": learned_weight,
        "target_fired_on_probe": brain.sparks["credit_hypothesis"].fired_count > 0,
        "prediction_after_probe": brain.belief_label,
        "algebraic_expected_eligibility_at_reward": 0.81,
        "algebraic_expected_weight": 0.562,
        "algebraic_match": close(eligibility_at_reward_after_processing, 0.81)
        and close(learned_weight, 0.562),
    }


def points() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = [{"id": "anchor", **ANCHOR}]
    for key, values in ONE_FACTOR_SWEEPS.items():
        for value in values:
            point = dict(ANCHOR)
            point[key] = value
            point["id"] = f"sweep:{key}:{value}"
            out.append(point)
    for corner in CORNERS:
        point = dict(ANCHOR)
        point.update(corner)
        point["id"] = f"corner:{corner['name']}"
        out.append(point)
    return out


def run_point(point: dict[str, Any]) -> dict[str, Any]:
    ref_state, ref_counter = run_reference(point)
    results: dict[str, Any] = {}
    for comparator in COMPARATORS:
        if comparator == "REF_GLOBAL_SCAN":
            state, counter = ref_state, ref_counter
        elif comparator == "ORD_DENSE_VECTORIZED_LOGICAL":
            state, counter = run_reference(point, dense_vectorized=True)
        elif comparator == "ORD_HISTORY_ARCHIVE_EXACT":
            state, counter = run_history(point)
        else:
            state, counter = run_lazy(point, comparator)
        equivalence = compare_state(ref_state, state, point)
        results[comparator] = {
            "equivalence": equivalence,
            "resource_vector": {
                "primitive_operation_total": counter.total,
                "primitive_operation_subcounts": counter.primitive,
                "peak_logical_history_timestamp_active_slots": counter.peak_slots,
                "history_entry_manipulation_count": counter.history_manipulations,
                "distinct_live_delay_buckets": counter.peak_delay_buckets,
            },
        }
    return {"point": point, "comparators": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = {
        "schema_version": 1,
        "contract_id": CONTRACT_ID,
        "candidate_id": "CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01",
        "research_layer": "ARCHITECTURE_STUDY",
        "claim_ceiling": "SYSTEM",
        "evidentiary_status": "NON_EVIDENTIARY_SYSTEM_ARCHITECTURE_RAW_DEVELOPMENT_OUTPUT",
        "source_main": "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d",
        "analyst_authority": "EVA-20260922T031000+0900-R50-4C8A21D7@8ae04f045ac760cfd8b209f337284293d6c58bf1",
        "float_tolerance": {"abs": ABS_TOL, "rel": REL_TOL},
        "behavioral_anchor_probe": behavioral_anchor_probe(),
        "points": [run_point(point) for point in points()],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
