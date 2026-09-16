"""Prospective source-only implementation binding for C19-v2.

This module never locates or opens Belief-R.  Callers inject the already-admitted
visible envelope only after a future execution admission.  The binding is
training-free: every projection coefficient is derived deterministically from
the frozen row seed, so official fit/tune/select is impossible by construction.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from sparkbrain.v03_external_validation.truth_free_adapter import (
    BeliefRTruthFreeSymbolicAdapter,
    TruthFreeBeliefRInput,
    compositional_visible_input,
    whole_hash_visible_input,
)
from sparkbrain.v03_seed.coalition import C14_BOUNDED_MODE, CoalitionGate
from sparkbrain.v03_seed.contracts import EvidenceContribution
from sparkbrain.v03_seed.evidence import EvidenceLedger
from sparkbrain.v03_seed.input_diagnosis import FeatureRecord

BINDING_ID = "c19-external-v2-source-only-structural-binding-v1"
FROZEN_PROTOCOL_HEAD = "90c936a7abca7eba0dac1f977753503551e73368"
PLANNED_IDENTITY = "c19-external-v2-official-v1"
CHOICES = ("a", "b", "c")
INPUT_TRACKS = (
    "I0_whole_hash",
    "I1_local_compositional",
    "I2_truth_free_symbolic_surface",
)
BASELINES = (
    "direct_stateless",
    "explicit_state_probabilistic",
    "modular_rim_like",
    "recurrent",
    "transformer",
)
_ALLOWED_EXAMPLE_KEYS = {
    "record_id",
    "source_index",
    "pair_index",
    "step_index",
    "question",
    "choices",
}


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _unit(seed: int, salt: str, value: str) -> float:
    digest = hashlib.sha256(f"{seed}:{salt}:{value}".encode()).digest()
    integer = int.from_bytes(digest[:8], "big")
    return integer / float((1 << 64) - 1)


def _softmax(values: Mapping[str, float]) -> dict[str, float]:
    maximum = max(values.values())
    exponentials = {key: math.exp(value - maximum) for key, value in values.items()}
    total = sum(exponentials.values())
    return {key: value / total for key, value in exponentials.items()}


def _normalize(values: Mapping[str, float]) -> dict[str, float]:
    total = sum(max(float(value), 0.0) for value in values.values())
    if total <= 0:
        return {choice: 1.0 / len(CHOICES) for choice in CHOICES}
    return {choice: max(float(values[choice]), 0.0) / total for choice in CHOICES}


def _validate_example(example: Mapping[str, object]) -> TruthFreeBeliefRInput:
    if set(example) != _ALLOWED_EXAMPLE_KEYS:
        raise ValueError("C19 bound executor accepts only the frozen target-blind visible envelope")
    choices = example["choices"]
    if not isinstance(choices, (list, tuple)) or len(choices) != 3:
        raise ValueError("visible choices must contain exactly three strings")
    pair_index = example["pair_index"]
    if isinstance(pair_index, bool) or not isinstance(pair_index, int) or pair_index < 0:
        raise ValueError("pair_index must be a non-negative integer")
    value = TruthFreeBeliefRInput(
        record_id=str(example["record_id"]),
        source_index=int(example["source_index"]),
        step_index=int(example["step_index"]),
        question=str(example["question"]),
        choices=tuple(str(choice) for choice in choices),
    )
    value.validate()
    return value


def encode_visible(value: TruthFreeBeliefRInput, input_track: str) -> FeatureRecord:
    if input_track == "I0_whole_hash":
        return whole_hash_visible_input(value)
    if input_track == "I1_local_compositional":
        return compositional_visible_input(value)
    if input_track == "I2_truth_free_symbolic_surface":
        return BeliefRTruthFreeSymbolicAdapter().encode(value)
    raise ValueError(f"unsupported frozen C19 input track: {input_track!r}")


def representation_bytes(record: FeatureRecord) -> bytes:
    payload = {
        "condition_id": record.condition_id,
        "features": record.features,
        "input_bytes": record.input_bytes,
        "oracle": record.oracle,
        "record_id": record.record_id,
    }
    return _canonical(payload).encode("utf-8")


def _project(record: FeatureRecord, *, seed: int, salt: str) -> tuple[dict[str, float], int]:
    logits = {choice: 0.0 for choice in CHOICES}
    operations = 0
    for feature, raw_value in record.features:
        value = float(raw_value)
        for choice in CHOICES:
            weight = 2.0 * _unit(seed, salt, f"{choice}:{feature}") - 1.0
            logits[choice] += value * weight
            operations += 1
    scale = math.sqrt(max(len(record.features), 1))
    return _softmax({choice: value / scale for choice, value in logits.items()}), operations


def _top(probabilities: Mapping[str, float]) -> str:
    return min(CHOICES, key=lambda choice: (-float(probabilities[choice]), choice))


def _g0_step(
    probabilities: Mapping[str, float], previous: str | None
) -> tuple[str | None, str]:
    ranked = sorted(
        ((float(probabilities[choice]), choice) for choice in CHOICES),
        key=lambda item: (-item[0], item[1]),
    )
    score, choice = ranked[0]
    margin = score - ranked[1][0]
    if score >= 0.50 and margin >= 0.08:
        return choice, "ignited"
    return previous, "retained_or_undecided"


def _g1_pair(
    steps: Sequence[tuple[TruthFreeBeliefRInput, dict[str, float]]],
) -> tuple[str | None, str, int]:
    ledger = EvidenceLedger()
    gate = CoalitionGate()
    current: str | None = None
    operations = 0
    reason = "no_candidates"
    for value, probabilities in steps:
        group = f"visible-source:{value.source_index}"
        for choice in CHOICES:
            ledger.add(
                EvidenceContribution(
                    evidence_id=f"c19:{value.record_id}:{value.step_index}:{choice}",
                    source_id=group,
                    belief_key=choice,
                    time=float(value.step_index),
                    support=float(probabilities[choice]),
                    correlation_group=group,
                )
            )
            operations += 1
        activations = {(None, choice): float(probabilities[choice]) for choice in CHOICES}
        decision = gate.evaluate(
            activations,
            ledger,
            now=float(value.step_index),
            mode=C14_BOUNDED_MODE,
        )
        # A second no-new-evidence settle is prospectively fixed so C14's stability
        # requirement measures a stable coalition rather than another evidence vote.
        decision = gate.evaluate(
            activations,
            ledger,
            now=float(value.step_index),
            mode=C14_BOUNDED_MODE,
        )
        operations += 2 * len(CHOICES)
        reason = decision.reason
        if decision.ignited:
            current = decision.belief_key
    return current, reason, operations


def _pairs(
    examples: Sequence[Mapping[str, object]],
) -> tuple[tuple[int, tuple[tuple[Mapping[str, object], TruthFreeBeliefRInput], ...]], ...]:
    grouped: dict[int, list[tuple[Mapping[str, object], TruthFreeBeliefRInput]]] = defaultdict(list)
    for example in examples:
        visible = _validate_example(example)
        grouped[int(example["pair_index"])].append((example, visible))
    result = []
    for pair_index, values in sorted(grouped.items()):
        ordered = tuple(sorted(values, key=lambda item: item[1].step_index))
        if len(ordered) != 2 or tuple(item[1].step_index for item in ordered) != (0, 1):
            raise ValueError("C19 binding requires exactly step 0 and step 1 for every pair")
        result.append((pair_index, ordered))
    return tuple(result)


def condition_executor(
    row: Mapping[str, object],
    examples: Sequence[Mapping[str, object]],
) -> list[dict[str, Any]]:
    if row.get("row_kind") != "c19_condition":
        raise ValueError("condition executor received a non-condition row")
    input_track = str(row["input_track"])
    gate = str(row["gate"])
    seed = int(row["seed"])
    output: list[dict[str, Any]] = []
    for pair_index, pair in _pairs(examples):
        encoded_steps: list[tuple[TruthFreeBeliefRInput, FeatureRecord, dict[str, float]]] = []
        work = 0
        for _raw, visible in pair:
            representation = encode_visible(visible, input_track)
            probabilities, operations = _project(representation, seed=seed, salt="c19-readout-v1")
            work += operations
            encoded_steps.append((visible, representation, probabilities))
        prediction: str | None = None
        gate_reason = ""
        if gate == "G0_probability_margin":
            for _visible, _representation, probabilities in encoded_steps:
                prediction, gate_reason = _g0_step(probabilities, prediction)
        elif gate == "G1_coalition":
            prediction, gate_reason, gate_work = _g1_pair(
                tuple((visible, probabilities) for visible, _record, probabilities in encoded_steps)
            )
            work += gate_work
        else:
            raise ValueError(f"unsupported frozen gate: {gate!r}")
        final_raw, final_visible = pair[-1]
        rep_hashes = [hashlib.sha256(representation_bytes(item[1])).hexdigest() for item in encoded_steps]
        output.append(
            {
                "record_id": final_visible.record_id,
                "source_index": final_visible.source_index,
                "pair_index": pair_index,
                "prediction": prediction,
                "metadata": {
                    "binding_id": BINDING_ID,
                    "input_track": input_track,
                    "gate": gate,
                    "seed": seed,
                    "representation_sha256": rep_hashes,
                    "final_probabilities": encoded_steps[-1][2],
                    "gate_reason": gate_reason,
                    "work_counters": {"projection_and_gate_operations": work},
                    "final_step_index": int(final_raw["step_index"]),
                },
            }
        )
    return output


def _baseline_probabilities(
    kind: str,
    records: Sequence[FeatureRecord],
    *,
    seed: int,
) -> tuple[dict[str, float], int]:
    projections: list[dict[str, float]] = []
    work = 0
    if kind == "modular_rim_like":
        final_modules = []
        for module in range(4):
            probabilities, operations = _project(
                records[-1], seed=seed, salt=f"rim-module-{module}"
            )
            work += operations
            final_modules.append(probabilities)
        selected = sorted(final_modules, key=lambda row: max(row.values()), reverse=True)[:2]
        averaged = {
            choice: sum(row[choice] for row in selected) / len(selected) for choice in CHOICES
        }
        return _normalize(averaged), work

    for record in records:
        probabilities, operations = _project(record, seed=seed, salt="baseline-readout-v1")
        projections.append(probabilities)
        work += operations

    if kind == "direct_stateless":
        return projections[-1], work
    if kind == "explicit_state_probabilistic":
        log_state = {choice: 0.0 for choice in CHOICES}
        for row in projections:
            for choice in CHOICES:
                log_state[choice] += math.log(max(row[choice], 1e-12))
                work += 1
        return _softmax(log_state), work
    if kind == "recurrent":
        state = dict(projections[0])
        for row in projections[1:]:
            state = {choice: 0.5 * state[choice] + 0.5 * row[choice] for choice in CHOICES}
            work += len(CHOICES)
        return _normalize(state), work
    if kind == "transformer":
        final_hash = records[-1].feature_hash
        weighted = {choice: 0.0 for choice in CHOICES}
        weights = []
        for record in records:
            weight = math.exp(_unit(seed, "causal-attention-v1", f"{record.feature_hash}:{final_hash}"))
            weights.append(weight)
        total = sum(weights)
        for weight, row in zip(weights, projections, strict=True):
            for choice in CHOICES:
                weighted[choice] += weight / total * row[choice]
                work += 1
        return _normalize(weighted), work
    raise ValueError(f"unsupported frozen baseline: {kind!r}")


def baseline_executor(
    kind: str,
    row: Mapping[str, object],
    examples: Sequence[Mapping[str, object]],
) -> list[dict[str, Any]]:
    if kind not in BASELINES or row.get("baseline_kind") != kind:
        raise ValueError("baseline executor/frozen row mismatch")
    seed = int(row["seed"])
    output = []
    for pair_index, pair in _pairs(examples):
        visible = [item[1] for item in pair]
        records = [encode_visible(item, "I2_truth_free_symbolic_surface") for item in visible]
        probabilities, work = _baseline_probabilities(kind, records, seed=seed)
        final = visible[-1]
        output.append(
            {
                "record_id": final.record_id,
                "source_index": final.source_index,
                "pair_index": pair_index,
                "prediction": _top(probabilities),
                "metadata": {
                    "binding_id": BINDING_ID,
                    "baseline_kind": kind,
                    "seed": seed,
                    "representation_access": "exact_I2_truth_free_symbolic_surface",
                    "representation_sha256": [
                        hashlib.sha256(representation_bytes(record)).hexdigest()
                        for record in records
                    ],
                    "final_probabilities": probabilities,
                    "work_counters": {"deterministic_operations": work},
                    "fit_tune_select": False,
                },
            }
        )
    return output


def baseline_registry() -> dict[str, Any]:
    return {
        kind: (lambda row, examples, frozen_kind=kind: baseline_executor(frozen_kind, row, examples))
        for kind in BASELINES
    }


def binding_manifest() -> dict[str, Any]:
    return {
        "schema_version": "1",
        "binding_id": BINDING_ID,
        "frozen_protocol_head": FROZEN_PROTOCOL_HEAD,
        "planned_official_identity": PLANNED_IDENTITY,
        "training_policy": "zero_update_deterministic_seeded_projection",
        "official_fit_tune_select": False,
        "condition_readout": "sha256_seeded_signed_projection_v1",
        "gates": {
            "G0_probability_margin": {"score_threshold": 0.50, "margin_threshold": 0.08},
            "G1_coalition": {
                "implementation": "sparkbrain.v03_seed.coalition:C14_BOUNDED_MODE",
                "settle_rounds_per_visible_step": 2,
            },
        },
        "baseline_representation_access": {
            kind: "exact_I2_truth_free_symbolic_surface" for kind in BASELINES
        },
        "representation_confounds": {
            "I2_G0_G1_byte_identity_required": True,
            "direct_stateless_exact_I2": True,
            "explicit_state_probabilistic_exact_I2": True,
            "persistent_state_novelty_claim_allowed": False,
            "architecture_superiority_claim_allowed_without_resource_match": False,
            "isolation_axis_tested": False,
        },
        "baseline_semantics": {
            "direct_stateless": "final-step fixed projection only",
            "explicit_state_probabilistic": "product-of-step probability state",
            "modular_rim_like": "four seeded modules, top-two confidence aggregation",
            "recurrent": "fixed 0.5 recurrent probability state",
            "transformer": "two-step causal attention over fixed projection states",
        },
        "resource_policy": {
            "data_match": "exact same injected official pairs and exact I2 bytes for all baselines",
            "optimization_match": "zero updates for C19 readout and every baseline",
            "parameter_role": "training-free generated coefficients; report as fixed, not learned",
            "compute_match": "measure deterministic operation counters; unmatched rows are descriptive",
            "winner_claim_requires_all_frozen_matching_dimensions": True,
        },
    }
