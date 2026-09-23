from __future__ import annotations

import argparse
import copy
import hashlib
import math
import os
from pathlib import Path
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival, canonical_json
from sparkbrain.v05.route_architecture import apply_edge_intervention
from sparkbrain.v05.route_preformal import bind_preformal_r1
from sparkbrain.v05.route_preformal_r2 import (
    CANDIDATE_ID,
    DEVELOPMENT_REVISION,
    RESPONSE_FIELDS,
    bind_preformal_r2_contract_closure,
)

R93_ANALYST_AUTHORITY = "EVA-20260923T140800+0900-R93-4D7C2A91"
R93_ANALYST_COMMIT = "92a85ab4f7795e97e5c0e750c8edfcc77a74c0bd"
CLOSED_R2_SOURCE_HEAD = "43d0f25541a3c447d4c7156303647ae94f3119f4"
QUEUE_ENTRY_ID = "D34-Q002"
MEASUREMENT_WINDOW_MS = 64.0
RESULT_SCHEMA = "cand34-route-preformal-r2-one-bounded-response-v1"
RESULT_STATUS = "PREFORMAL_DEVELOPMENT_RESULT_EXPOSED"
EVIDENTIARY_STATUS = "PREFORMAL_DEVELOPMENT_ONLY_ZERO_CONFIRMATORY_CREDIT"


def _sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _sample_potential(field: object, unit_id: int, time_ms: float) -> float:
    unit = field.units[unit_id]
    if time_ms < unit.last_update_ms:
        raise RuntimeError("cannot sample membrane potential before last unit update")
    elapsed = time_ms - unit.last_update_ms
    return float(unit.potential) * math.exp(-elapsed / field.config.membrane_tau_ms)


def _spike_rows(spikes: list[object], unit_ids: set[int]) -> list[dict[str, object]]:
    return [
        {
            "time_ms": float(spike.time_ms),
            "unit_id": int(spike.unit_id),
            "potential_before_reset": float(spike.potential_before_reset),
            "dynamic_threshold": float(spike.dynamic_threshold),
        }
        for spike in spikes
        if int(spike.unit_id) in unit_ids
    ]


def _secondary_assembly_response(
    *,
    closure: object,
    field: object,
    spikes: list[object],
    window_end_ms: float,
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for binding in closure.unit_export_map:
        unit_ids = set(int(value) for value in binding.unit_ids)
        rows.append(
            {
                "assembly_id": binding.assembly_id,
                "prototype_sha256": binding.prototype_sha256,
                "unit_ids": list(binding.unit_ids),
                "spikes": _spike_rows(spikes, unit_ids),
                "membrane_potential_at_window_end": {
                    str(unit_id): _sample_potential(field, unit_id, window_end_ms)
                    for unit_id in binding.unit_ids
                },
            }
        )
    return {
        "measurement_window_ms": MEASUREMENT_WINDOW_MS,
        "assemblies": rows,
    }


def _intervention_kind(arm: str) -> str:
    if arm == "target_sham":
        return "sham"
    if arm.endswith("transmission_null"):
        return "transmission_null"
    if arm.endswith("delay_plus_1ms"):
        return "delay_plus_1ms"
    raise RuntimeError(f"unbound R2 arm: {arm}")


def _execute_condition(
    *,
    source_brain: object,
    closure: object,
    condition: object,
) -> dict[str, object]:
    clone = copy.deepcopy(source_brain)
    field = clone.base.field
    if clone.state_hash() != closure.checkpoint_sha256:
        raise RuntimeError("condition clone does not match frozen checkpoint")
    if field.state_dict()["queue"]:
        raise RuntimeError("frozen development checkpoint is not quiescent")

    edge = condition.intervention_edge
    original = field.connection(edge.source_id, edge.target_id)
    if (
        float(original.weight) != float(edge.weight)
        or float(original.delay_ms) != float(edge.delay_ms)
        or bool(original.plastic) != bool(edge.plastic)
    ):
        raise RuntimeError("intervention edge drifted from frozen queue binding")

    kind = _intervention_kind(condition.arm)
    applied = apply_edge_intervention(field, edge, kind)
    anchor_ms = float(field.current_time_ms)
    nominal_ms = anchor_ms + float(edge.delay_ms)
    plus_one_ms = nominal_ms + 1.0
    window_end_ms = anchor_ms + MEASUREMENT_WINDOW_MS
    if plus_one_ms > window_end_ms:
        raise RuntimeError("R2 observation boundary exceeds frozen 64ms window")

    source = field.units[condition.cue_source_id]
    expected_current = float(field.dynamic_threshold(source))
    if not math.isclose(
        expected_current,
        float(condition.cue_current),
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise RuntimeError("source-only cue current drifted from frozen R2 binding")
    if anchor_ms < float(source.refractory_until_ms):
        raise RuntimeError("frozen source is refractory at R2 cue anchor")
    if condition.cue_source_id == condition.observed_destination_unit_id:
        raise RuntimeError("R2 source-only cue would directly cue observed destination")

    pulse_id = f"{QUEUE_ENTRY_ID}:{condition.step_id}:source-only"
    field.schedule_arrival(
        SynapticArrival(
            time_ms=anchor_ms,
            target_id=condition.cue_source_id,
            current=float(condition.cue_current),
            source_id=None,
            pulse_id=pulse_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )

    all_spikes: list[object] = []
    cue_spikes = list(field.run_until(anchor_ms))
    all_spikes.extend(cue_spikes)
    source_spiked = any(
        int(spike.unit_id) == condition.cue_source_id
        and math.isclose(float(spike.time_ms), anchor_ms, rel_tol=0.0, abs_tol=1e-12)
        for spike in cue_spikes
    )
    if not source_spiked:
        raise RuntimeError("prospectively guaranteed source-only cue failed to spike source")

    nominal_spikes = list(field.run_until(nominal_ms))
    all_spikes.extend(nominal_spikes)
    destination = field.units[condition.observed_destination_unit_id]
    potential_nominal = _sample_potential(
        field,
        condition.observed_destination_unit_id,
        nominal_ms,
    )
    last_spike_nominal = destination.last_spike_ms

    plus_one_spikes = list(field.run_until(plus_one_ms))
    all_spikes.extend(plus_one_spikes)
    destination = field.units[condition.observed_destination_unit_id]
    potential_plus_one = _sample_potential(
        field,
        condition.observed_destination_unit_id,
        plus_one_ms,
    )
    last_spike_plus_one = destination.last_spike_ms

    tail_spikes = list(field.run_until(window_end_ms))
    all_spikes.extend(tail_spikes)
    destination_spike_times = [
        float(spike.time_ms)
        for spike in all_spikes
        if int(spike.unit_id) == condition.observed_destination_unit_id
    ]
    destination_spike_state = {
        "last_spike_ms_at_nominal_arrival": (
            None if last_spike_nominal is None else float(last_spike_nominal)
        ),
        "last_spike_ms_at_nominal_plus_1ms": (
            None if last_spike_plus_one is None else float(last_spike_plus_one)
        ),
        "spiked_at_nominal_arrival": any(
            math.isclose(value, nominal_ms, rel_tol=0.0, abs_tol=1e-12)
            for value in destination_spike_times
        ),
        "spiked_at_nominal_plus_1ms": any(
            math.isclose(value, plus_one_ms, rel_tol=0.0, abs_tol=1e-12)
            for value in destination_spike_times
        ),
        "spike_times_ms_within_64ms": destination_spike_times,
    }

    response = {
        "cued_source_spike_guaranteed_by_contract": source_spiked,
        "edge_destination_membrane_potential_at_nominal_arrival": potential_nominal,
        "edge_destination_membrane_potential_at_nominal_plus_1ms": potential_plus_one,
        "edge_destination_spike_state": destination_spike_state,
        "assembly_level_frozen_response_secondary": _secondary_assembly_response(
            closure=closure,
            field=field,
            spikes=all_spikes,
            window_end_ms=window_end_ms,
        ),
    }
    if tuple(response) != RESPONSE_FIELDS:
        raise RuntimeError("R2 response field order or membership drifted")

    return {
        "step_id": condition.step_id,
        "arm": condition.arm,
        "edge_index": int(condition.edge_index),
        "intervention_edge_before": edge.as_dict(),
        "intervention_edge_after": applied.as_dict(),
        "cue_source_id": int(condition.cue_source_id),
        "cue_current": float(condition.cue_current),
        "observed_destination_unit_id": int(condition.observed_destination_unit_id),
        "anchor_ms": anchor_ms,
        "nominal_arrival_ms": nominal_ms,
        "nominal_plus_1ms": plus_one_ms,
        "window_end_ms": window_end_ms,
        "response": response,
        "response_sha256": _sha256(response),
    }


def execute_once() -> dict[str, object]:
    source_brain, _, _, _, _ = bind_preformal_r1()
    closure, queue = bind_preformal_r2_contract_closure()

    if closure.candidate_id != CANDIDATE_ID:
        raise RuntimeError("candidate identity drift")
    if closure.development_revision != DEVELOPMENT_REVISION:
        raise RuntimeError("development revision drift")
    if queue.queue_entry_id != QUEUE_ENTRY_ID:
        raise RuntimeError("unexpected PRE_FORMAL queue entry")
    if queue.status != "AWAITING_FRESH_ANALYST_READY_REVIEW":
        raise RuntimeError("frozen D34-Q002 queue status drift")
    if queue.response_bearing_execution_performed or queue.formal_action_performed:
        raise RuntimeError("D34-Q002 is not an untouched one-way development queue")
    if source_brain.state_hash() != closure.checkpoint_sha256:
        raise RuntimeError("source checkpoint hash drift")
    if source_brain.results or source_brain.trace:
        raise RuntimeError("source checkpoint already contains response exposure")
    if closure.response_bearing_execution_allowed:
        raise RuntimeError("closed R2 contract was mutated in place to permit execution")
    if closure.formal_action_allowed:
        raise RuntimeError("closed R2 contract unexpectedly permits FORMAL action")

    condition_rows = [
        _execute_condition(
            source_brain=source_brain,
            closure=closure,
            condition=condition,
        )
        for condition in closure.queue_conditions
    ]
    payload: dict[str, object] = {
        "schema": RESULT_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "queue_entry_id": QUEUE_ENTRY_ID,
        "development_revision": DEVELOPMENT_REVISION,
        "analyst_authority": R93_ANALYST_AUTHORITY,
        "analyst_commit": R93_ANALYST_COMMIT,
        "closed_r2_source_head": CLOSED_R2_SOURCE_HEAD,
        "execution_source_head": os.environ.get("GITHUB_SHA", "LOCAL_UNBOUND"),
        "contract_closure_sha256": closure.sha256,
        "checkpoint_sha256": closure.checkpoint_sha256,
        "opportunity_plan_sha256": closure.opportunity_plan_sha256,
        "queue_sha256": queue.sha256,
        "queue_policy": closure.queue_policy,
        "claim_scope": closure.claim_scope,
        "primary_reduction": closure.primary_reduction,
        "secondary_export": closure.secondary_export,
        "response_fields": list(closure.response_fields),
        "condition_count": len(condition_rows),
        "conditions": condition_rows,
        "result_status": RESULT_STATUS,
        "evidentiary_status": EVIDENTIARY_STATUS,
        "independent_confirmatory_credit": 0,
        "formal_action_performed": False,
        "official_scoring_performed": False,
        "repeat_response_execution_permitted_by_this_record": False,
    }
    return {**payload, "sha256": _sha256(payload)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = execute_once()
    with output.open("x", encoding="utf-8") as handle:
        handle.write(canonical_json(result) + "\n")
    print(f"preserved raw PRE_FORMAL result sha256={result['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
