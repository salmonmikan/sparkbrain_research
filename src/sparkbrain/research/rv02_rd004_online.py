"""RV02-RD004 one-shot exposed-development cell implementation.

RD003 attempt-001 is consumed and is never rerun here. RD004 inherits its fixed
training mechanism but uses the preregistered relative probe clock: complete the
6.5 ms training tail, wash out for exactly 100 ms without input or learning,
freeze one shared state per arm, then run natural/cut 40 ms probes from that
state with the cue anchored to the snapshot clock.
"""

from __future__ import annotations

from typing import Any

from sparkbrain.research.rv01.physical_learner_bridge import runtime_pulse
from sparkbrain.research.rv02_hidden_eligibility import (
    HiddenEligibilityTrace,
    OnlineHiddenEligibilityPlasticity,
    deterministic_hidden_permutation,
)
from sparkbrain.research.rv02_rd003_online import (
    RD003_GAIN,
    RD003_MODES,
    _budget_rows,
    _hidden_rows,
    _new_gained_field,
    _schedule_external,
    _training_schedule,
    planned_rd003_cells,
)
from sparkbrain.research.rv02_rd004_probe_clock import (
    RD004_ELIGIBILITY_TAIL_MS,
    RD004_HORIZON_MS,
    RD004_WASHOUT_MS,
    run_rd004_probe,
    score_rd004_probe,
)
from sparkbrain.research.rv02_recruitment import PORTS, connection_hash
from sparkbrain.research.rv02_scale import ScaleStudyConfig, audit_scale, digest
from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField

RD004_PROTOCOL = "rv02-rd004-relative-probe-clock-v1"
_NATIVE_GUARD_MESSAGES = ("max_events_per_run exceeded", "max_spikes_per_run exceeded")


def planned_rd004_cells(
    config: ScaleStudyConfig | None = None,
) -> tuple[tuple[str, int], ...]:
    return planned_rd003_cells(config)


def _is_native_guard(exc: RuntimeError) -> bool:
    return str(exc) in _NATIVE_GUARD_MESSAGES


def _probe_arm_from_snapshot(
    snapshot: dict[str, Any],
    world: dict[str, Any],
    unit_count: int,
) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for route_index, route in enumerate(world["routes"]):
        pair: dict[str, Any] = {"route_index": route_index}
        for name, cut in (("natural", False), ("boundary_zero", True)):
            probe = run_rd004_probe(
                snapshot["snapshot_state"],
                int(route[0]),
                cut_hidden_boundary=cut,
                horizon_ms=RD004_HORIZON_MS,
            )
            if probe["status"] == "complete":
                probe["behavior"] = score_rd004_probe(
                    probe["spikes"],
                    route,
                    unit_count,
                    cue_time_ms=float(probe["cue_time_ms"]),
                )
            pair[name] = probe
        pair["complete"] = all(
            pair[name]["status"] == "complete" for name in ("natural", "boundary_zero")
        )
        if pair["natural"].get("shared_snapshot_hash") != pair["boundary_zero"].get(
            "shared_snapshot_hash"
        ):
            raise RuntimeError("RD004 natural/cut probes did not share one exact snapshot")
        if pair["natural"].get("cue_time_ms") != pair["boundary_zero"].get("cue_time_ms"):
            raise RuntimeError("RD004 natural/cut cue clocks diverged")
        rows.append(pair)
    return tuple(rows)


def _classify_probe_status(probes: dict[str, tuple[dict[str, Any], ...]]) -> str:
    statuses = {
        pair[name]["status"]
        for mode in RD003_MODES
        for pair in probes[mode]
        for name in ("natural", "boundary_zero")
    }
    if "incomplete_native_guard_probe" in statuses:
        return "incomplete_native_guard_probe"
    if statuses != {"complete"}:
        return "incomplete_integrity_failure"
    return "complete"


def _failure_result(
    *,
    world: dict[str, Any],
    scale: int,
    audit: dict[str, Any],
    schedule: tuple[dict[str, Any], ...],
    initial_hashes: dict[str, str],
    training_rows: list[dict[str, Any]],
    actual_hidden: dict[str, list[dict[str, Any]]],
    learners: dict[str, OnlineHiddenEligibilityPlasticity],
    e1_budget: list[HiddenEligibilityTrace],
    es_budget: list[HiddenEligibilityTrace],
    status: str,
    error: str,
) -> dict[str, Any]:
    return {
        "protocol": RD004_PROTOCOL,
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "world_id": world["world_id"],
        "family": world["family"],
        "scale": scale,
        "audit": audit,
        "gain": RD003_GAIN,
        "eligibility_tail_ms": RD004_ELIGIBILITY_TAIL_MS,
        "washout_ms": RD004_WASHOUT_MS,
        "probe_horizon_ms": RD004_HORIZON_MS,
        "training_schedule_hash": digest(schedule),
        "training_schedule": schedule,
        "initial_connection_hashes": initial_hashes,
        "partial_connection_hashes": {
            mode: connection_hash(learner.field) for mode, learner in learners.items()
        },
        "e1_eligibility_budget": [row.state_dict() for row in e1_budget],
        "es_eligibility_budget": [row.state_dict() for row in es_budget],
        "actual_runtime_hidden_spikes": actual_hidden,
        "training_rows": training_rows,
        "learner_states": {mode: learners[mode].state_dict() for mode in RD003_MODES},
        "status": status,
        "error": error,
        "complete": False,
        "scientific_status": "not_scored_development_diagnosis",
    }


def run_rd004_cell(
    config: ScaleStudyConfig,
    world: dict[str, Any],
    scale: int,
) -> dict[str, Any]:
    """Run one RD004 exposed-development cell under the frozen preregistration."""

    if config != ScaleStudyConfig():
        raise ValueError("RD004 configuration is fixed to ScaleStudyConfig defaults")
    audit = audit_scale(config, world, scale)
    base = _new_gained_field(config, world, scale)
    initial_state = base.state_dict()
    fields = {
        mode: TemporalExcitableField.from_state_dict(initial_state)
        for mode in RD003_MODES
    }
    hidden_units = tuple(sorted(set(fields["causal"].units) - set(PORTS)))
    mapping = deterministic_hidden_permutation(
        hidden_units,
        namespace=f"{world['world_id']}|scale={scale}",
    )
    learners = {
        "disabled": OnlineHiddenEligibilityPlasticity(
            fields["disabled"], visible_units=PORTS, mode="disabled"
        ),
        "causal": OnlineHiddenEligibilityPlasticity(
            fields["causal"], visible_units=PORTS, mode="causal"
        ),
        "shuffled": OnlineHiddenEligibilityPlasticity(
            fields["shuffled"],
            visible_units=PORTS,
            mode="shuffled",
            shuffled_mapping=mapping,
        ),
    }
    initial_hashes = {mode: connection_hash(field) for mode, field in fields.items()}
    if len(set(initial_hashes.values())) != 1:
        raise RuntimeError("RD004 arm connection state differs before training")

    training_rows: list[dict[str, Any]] = []
    actual_hidden: dict[str, list[dict[str, Any]]] = {mode: [] for mode in RD003_MODES}
    e1_budget: list[HiddenEligibilityTrace] = []
    es_budget: list[HiddenEligibilityTrace] = []
    schedule = _training_schedule(world)

    try:
        for row in schedule:
            time_ms = float(row["time_ms"])
            spikes_by_mode: dict[str, tuple[SpikeEvent, ...]] = {}
            for mode in RD003_MODES:
                spikes = tuple(fields[mode].run_until(time_ms))
                spikes_by_mode[mode] = spikes
                actual_hidden[mode].extend(_hidden_rows(spikes))

            causal_eligibility = learners["causal"].record_hidden_spikes(
                spike for spike in spikes_by_mode["causal"] if spike.unit_id not in PORTS
            )
            shuffled_eligibility = learners["shuffled"].record_hidden_spikes(
                spike for spike in spikes_by_mode["causal"] if spike.unit_id not in PORTS
            )
            e1_budget.extend(causal_eligibility)
            es_budget.extend(shuffled_eligibility)

            pulse = runtime_pulse(
                event_id=str(row["event_id"]),
                time_ms=time_ms,
                unit_id=int(row["unit_id"]),
                magnitude=1.0,
            )
            updates_by_mode: dict[str, list[dict[str, Any]]] = {}
            for mode in RD003_MODES:
                updates = learners[mode].observe_external(pulse)
                updates_by_mode[mode] = [update.state_dict() for update in updates]
                _schedule_external(
                    fields[mode],
                    event_id=str(row["event_id"]),
                    time_ms=time_ms,
                    unit_id=int(row["unit_id"]),
                )
            training_rows.append(
                {
                    **row,
                    "e1_new_eligibility": [
                        item.state_dict() for item in causal_eligibility
                    ],
                    "es_new_eligibility": [
                        item.state_dict() for item in shuffled_eligibility
                    ],
                    "updates": updates_by_mode,
                }
            )
    except RuntimeError as exc:
        if not _is_native_guard(exc):
            raise
        return _failure_result(
            world=world,
            scale=scale,
            audit=audit,
            schedule=schedule,
            initial_hashes=initial_hashes,
            training_rows=training_rows,
            actual_hidden=actual_hidden,
            learners=learners,
            e1_budget=e1_budget,
            es_budget=es_budget,
            status="incomplete_native_guard_training",
            error=str(exc),
        )

    tail_hidden: dict[str, list[dict[str, Any]]] = {mode: [] for mode in RD003_MODES}
    source_clocks = {mode: float(fields[mode].current_time_ms) for mode in RD003_MODES}
    tail_ends = {
        mode: source_clocks[mode] + RD004_ELIGIBILITY_TAIL_MS for mode in RD003_MODES
    }
    tail_spikes: dict[str, tuple[SpikeEvent, ...]] = {}
    try:
        for mode in RD003_MODES:
            spikes = tuple(fields[mode].run_until(tail_ends[mode]))
            tail_spikes[mode] = spikes
            rows = list(_hidden_rows(spikes))
            tail_hidden[mode].extend(rows)
            actual_hidden[mode].extend(rows)
    except RuntimeError as exc:
        if not _is_native_guard(exc):
            raise
        return _failure_result(
            world=world,
            scale=scale,
            audit=audit,
            schedule=schedule,
            initial_hashes=initial_hashes,
            training_rows=training_rows,
            actual_hidden=actual_hidden,
            learners=learners,
            e1_budget=e1_budget,
            es_budget=es_budget,
            status="incomplete_native_guard_training",
            error=str(exc),
        )

    causal_tail = learners["causal"].record_hidden_spikes(
        spike for spike in tail_spikes["causal"] if spike.unit_id not in PORTS
    )
    shuffled_tail = learners["shuffled"].record_hidden_spikes(
        spike for spike in tail_spikes["causal"] if spike.unit_id not in PORTS
    )
    e1_budget.extend(causal_tail)
    es_budget.extend(shuffled_tail)
    if _budget_rows(e1_budget) != _budget_rows(es_budget):
        raise RuntimeError("RD004 E1/ES eligibility event budget mismatch")
    if learners["disabled"].hidden_trace_records:
        raise RuntimeError("RD004 E0 unexpectedly retained hidden eligibility")

    washout_hidden: dict[str, list[dict[str, Any]]] = {mode: [] for mode in RD003_MODES}
    washout_ends = {mode: tail_ends[mode] + RD004_WASHOUT_MS for mode in RD003_MODES}
    try:
        for mode in RD003_MODES:
            spikes = tuple(fields[mode].run_until(washout_ends[mode]))
            rows = list(_hidden_rows(spikes))
            washout_hidden[mode].extend(rows)
            actual_hidden[mode].extend(rows)
    except RuntimeError as exc:
        if not _is_native_guard(exc):
            raise
        return _failure_result(
            world=world,
            scale=scale,
            audit=audit,
            schedule=schedule,
            initial_hashes=initial_hashes,
            training_rows=training_rows,
            actual_hidden=actual_hidden,
            learners=learners,
            e1_budget=e1_budget,
            es_budget=es_budget,
            status="incomplete_native_guard_washout",
            error=str(exc),
        )

    snapshots = {
        mode: {
            "source_clock_ms": source_clocks[mode],
            "tail_end_ms": tail_ends[mode],
            "washout_end_ms": washout_ends[mode],
            "cue_time_ms": float(fields[mode].current_time_ms),
            "snapshot_state": fields[mode].state_dict(),
            "snapshot_state_hash": fields[mode].state_hash(),
            "connection_hash": connection_hash(fields[mode]),
        }
        for mode in RD003_MODES
    }
    trained_hashes = {mode: connection_hash(fields[mode]) for mode in RD003_MODES}

    try:
        probes = {
            mode: _probe_arm_from_snapshot(
                snapshots[mode], world, int(audit["unit_count"])
            )
            for mode in RD003_MODES
        }
    except (RuntimeError, ValueError) as exc:
        return {
            **_failure_result(
                world=world,
                scale=scale,
                audit=audit,
                schedule=schedule,
                initial_hashes=initial_hashes,
                training_rows=training_rows,
                actual_hidden=actual_hidden,
                learners=learners,
                e1_budget=e1_budget,
                es_budget=es_budget,
                status="incomplete_integrity_failure",
                error=str(exc),
            ),
            "probe_snapshots": {
                mode: {
                    key: value for key, value in snapshot.items() if key != "snapshot_state"
                }
                for mode, snapshot in snapshots.items()
            },
        }

    status = _classify_probe_status(probes)
    complete = status == "complete"
    return {
        "protocol": RD004_PROTOCOL,
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "world_id": world["world_id"],
        "family": world["family"],
        "scale": scale,
        "audit": audit,
        "gain": RD003_GAIN,
        "eligibility_tail_ms": RD004_ELIGIBILITY_TAIL_MS,
        "washout_ms": RD004_WASHOUT_MS,
        "probe_horizon_ms": RD004_HORIZON_MS,
        "training_schedule_hash": digest(schedule),
        "training_schedule": schedule,
        "initial_connection_hashes": initial_hashes,
        "trained_connection_hashes": trained_hashes,
        "shuffled_mapping": {str(k): v for k, v in sorted(mapping.items())},
        "e1_eligibility_budget": [row.state_dict() for row in e1_budget],
        "es_eligibility_budget": [row.state_dict() for row in es_budget],
        "eligibility_budget_hash": digest(_budget_rows(e1_budget)),
        "actual_runtime_hidden_spikes": actual_hidden,
        "tail_hidden_spikes": tail_hidden,
        "washout_hidden_spikes": washout_hidden,
        "training_rows": training_rows,
        "learner_states": {mode: learners[mode].state_dict() for mode in RD003_MODES},
        "probe_snapshots": {
            mode: {key: value for key, value in snapshot.items() if key != "snapshot_state"}
            for mode, snapshot in snapshots.items()
        },
        "probes": probes,
        "status": status,
        "complete": complete,
        "scientific_status": "not_scored_development_diagnosis",
    }


__all__ = [
    "RD004_PROTOCOL",
    "planned_rd004_cells",
    "run_rd004_cell",
]
