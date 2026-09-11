"""RV02-RD003 online training runner; exposed development worlds only.

This module realizes the already-preregistered E0/E1/ES training contract without
opening any held-out or formal capability.  E1 and ES are coupled to the same
retained E1 hidden-spike eligibility stream; ES changes only the assigned hidden
source identity through the deterministic preregistered permutation.  Task
outcomes never enter the learner.
"""

from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from sparkbrain.research.rv01.physical_learner_bridge import (
    build_physical_field,
    runtime_pulse,
)
from sparkbrain.research.rv02_boundary_recruitment import (
    apply_boundary_gain,
    run_probe,
    score_probe,
)
from sparkbrain.research.rv02_hidden_eligibility import (
    HiddenEligibilityTrace,
    OnlineHiddenEligibilityPlasticity,
    deterministic_hidden_permutation,
)
from sparkbrain.research.rv02_recruitment import PORTS, connection_hash
from sparkbrain.research.rv02_scale import (
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
)
from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

RD003_GAIN = 4.0
RD003_HORIZON_MS = 40.0
RD003_MODES = ("disabled", "causal", "shuffled")


def planned_rd003_cells(
    config: ScaleStudyConfig | None = None,
) -> tuple[tuple[str, int], ...]:
    config = config or ScaleStudyConfig()
    return tuple(
        (world["family"], scale)
        for world in development_worlds(config)
        for scale in config.scales
    )


def _new_gained_field(
    config: ScaleStudyConfig,
    world: dict[str, Any],
    scale: int,
) -> TemporalExcitableField:
    audit = audit_scale(config, world, scale)
    field = build_physical_field(
        unit_count=audit["unit_count"],
        directed_edges=audit["edges"],
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    field.receptor_ids = PORTS
    field.config = replace(
        field.config,
        max_events_per_run=4096,
        max_spikes_per_run=512,
    )
    gained, _ = apply_boundary_gain(field, RD003_GAIN)
    return gained


def _hidden_rows(spikes: tuple[SpikeEvent, ...]) -> tuple[dict[str, Any], ...]:
    return tuple(asdict(row) for row in spikes if row.unit_id not in PORTS)


def _budget_rows(rows: list[HiddenEligibilityTrace]) -> tuple[tuple[float, float, int], ...]:
    """Outcome-blind eligibility amount used by the E1/ES matching gate."""

    return tuple(
        (round(row.time_ms, 12), round(row.magnitude, 12), row.observed_unit_id)
        for row in rows
    )


def _schedule_external(
    field: TemporalExcitableField,
    *,
    event_id: str,
    time_ms: float,
    unit_id: int,
) -> None:
    field.schedule_arrival(
        SynapticArrival(
            time_ms=time_ms,
            target_id=unit_id,
            current=1.0,
            source_id=None,
            pulse_id=event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )


def _training_schedule(world: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    ordinal = 0
    for route_index, (route, exposures) in enumerate(
        zip(world["routes"], world["exposures"], strict=True)
    ):
        for episode in range(exposures):
            for position, unit_id in enumerate(route):
                rows.append(
                    {
                        "ordinal": ordinal,
                        "route_index": route_index,
                        "episode": episode,
                        "position": position,
                        "unit_id": unit_id,
                        "time_ms": float(route_index * 10000 + episode * 100 + position * 5),
                        "event_id": f"rd003-ext-{ordinal:06d}",
                    }
                )
                ordinal += 1
    return tuple(rows)


def _probe_arm(
    field: TemporalExcitableField,
    world: dict[str, Any],
    unit_count: int,
) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for route_index, route in enumerate(world["routes"]):
        pair: dict[str, Any] = {"route_index": route_index}
        for name, cut in (("natural", False), ("boundary_zero", True)):
            probe = run_probe(
                field,
                route[0],
                horizon_ms=RD003_HORIZON_MS,
                cut_hidden_boundary=cut,
            )
            if probe.get("status") != "incomplete_native_guard":
                probe["behavior"] = score_probe(probe["spikes"], route, unit_count)
                probe["status"] = "complete"
            pair[name] = probe
        pair["complete"] = all(
            pair[name]["status"] == "complete" for name in ("natural", "boundary_zero")
        )
        rows.append(pair)
    return tuple(rows)


def run_rd003_cell(
    config: ScaleStudyConfig,
    world: dict[str, Any],
    scale: int,
) -> dict[str, Any]:
    """Run one fixed exposed RD003 development cell.

    This function is intentionally not called by ordinary unit tests.  Once a
    source revision is frozen for RD003 development execution, a separate runner
    may invoke the full 18-cell matrix exactly as preregistered.
    """

    if config != ScaleStudyConfig():
        raise ValueError("RD003 configuration is fixed to ScaleStudyConfig defaults")
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
        raise RuntimeError("RD003 arm connection state differs before training")

    training_rows: list[dict[str, Any]] = []
    actual_hidden: dict[str, list[dict[str, Any]]] = {mode: [] for mode in RD003_MODES}
    e1_budget: list[HiddenEligibilityTrace] = []
    es_budget: list[HiddenEligibilityTrace] = []
    schedule = _training_schedule(world)

    for row in schedule:
        time_ms = float(row["time_ms"])
        spikes_by_mode: dict[str, tuple[SpikeEvent, ...]] = {}
        for mode in RD003_MODES:
            spikes = fields[mode].run_until(time_ms)
            spikes_by_mode[mode] = spikes
            actual_hidden[mode].extend(_hidden_rows(spikes))

        # The shuffled arm consumes the same E1 hidden-event budget; only source
        # assignment is permuted.  Its own hidden spikes are retained separately
        # for scientific interpretation but cannot alter the control budget.
        causal_eligibility = learners["causal"].record_hidden_spikes(
            spike for spike in spikes_by_mode["causal"] if spike.unit_id not in PORTS
        )
        shuffled_eligibility = learners["shuffled"].record_hidden_spikes(
            spike for spike in spikes_by_mode["causal"] if spike.unit_id not in PORTS
        )
        e1_budget.extend(causal_eligibility)
        es_budget.extend(shuffled_eligibility)

        updates_by_mode: dict[str, list[dict[str, Any]]] = {}
        pulse = runtime_pulse(
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            unit_id=int(row["unit_id"]),
            magnitude=1.0,
        )
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
                "e1_new_eligibility": [item.state_dict() for item in causal_eligibility],
                "es_new_eligibility": [item.state_dict() for item in shuffled_eligibility],
                "updates": updates_by_mode,
            }
        )

    if schedule:
        final_time = (
            float(schedule[-1]["time_ms"])
            + learners["causal"].config.maximum_lag_ms
        )
        final_spikes: dict[str, tuple[SpikeEvent, ...]] = {}
        for mode in RD003_MODES:
            spikes = fields[mode].run_until(final_time)
            final_spikes[mode] = spikes
            actual_hidden[mode].extend(_hidden_rows(spikes))
        causal_tail = learners["causal"].record_hidden_spikes(
            spike for spike in final_spikes["causal"] if spike.unit_id not in PORTS
        )
        shuffled_tail = learners["shuffled"].record_hidden_spikes(
            spike for spike in final_spikes["causal"] if spike.unit_id not in PORTS
        )
        e1_budget.extend(causal_tail)
        es_budget.extend(shuffled_tail)

    if _budget_rows(e1_budget) != _budget_rows(es_budget):
        raise RuntimeError("RD003 E1/ES eligibility event budget mismatch")
    if learners["disabled"].hidden_trace_records:
        raise RuntimeError("RD003 E0 unexpectedly retained hidden eligibility")

    trained_hashes = {mode: connection_hash(field) for mode, field in fields.items()}
    probes = {
        mode: _probe_arm(fields[mode], world, audit["unit_count"])
        for mode in RD003_MODES
    }
    complete = all(
        pair["complete"]
        for mode in RD003_MODES
        for pair in probes[mode]
    )
    return {
        "protocol": "rv02-rd003-online-hidden-eligibility-v1",
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "world_id": world["world_id"],
        "family": world["family"],
        "scale": scale,
        "audit": audit,
        "gain": RD003_GAIN,
        "training_schedule_hash": digest(schedule),
        "training_schedule": schedule,
        "initial_connection_hashes": initial_hashes,
        "trained_connection_hashes": trained_hashes,
        "shuffled_mapping": {str(k): v for k, v in sorted(mapping.items())},
        "e1_eligibility_budget": [row.state_dict() for row in e1_budget],
        "es_eligibility_budget": [row.state_dict() for row in es_budget],
        "eligibility_budget_hash": digest(_budget_rows(e1_budget)),
        "actual_runtime_hidden_spikes": actual_hidden,
        "training_rows": training_rows,
        "learner_states": {mode: learners[mode].state_dict() for mode in RD003_MODES},
        "probes": probes,
        "complete": complete,
        "scientific_status": "not_scored_development_diagnosis",
    }


__all__ = [
    "RD003_GAIN",
    "RD003_HORIZON_MS",
    "RD003_MODES",
    "planned_rd003_cells",
    "run_rd003_cell",
]
