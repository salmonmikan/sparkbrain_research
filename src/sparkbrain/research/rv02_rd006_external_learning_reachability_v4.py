"""RD006 v4 PORT-to-hidden learner-boundary synthetic preflight.

This OPEN_DEVELOPMENT revision changes exactly one learner boundary: an
ordinary external PORT trace may causally update an already-existing
PORT-to-hidden edge when an actual hidden spike is observed in the fixed
0.5--6.5 ms window.  It is implementation verification only.  Result-bearing
RD006 matrices, capability scoring, and held-out access fail closed here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict
from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3
from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology

PROTOCOL_ID = (
    "rv02-rd006-external-learning-reachability-a-"
    "v4-port-to-hidden-trace-boundary-preflight"
)
OBJECT_ID = v1.OBJECT_ID
ANALYST_GENERATION_ID = (
    "EVA-20260927T185823+0900-R153-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT"
)
PARENT_AUDIT_HEAD = "b22b58bccdf9538c6f1c741592db4f415d404262"
DEVELOPMENT_PHASE = "OPEN_DEVELOPMENT"
EVIDENTIARY_STATUS = "DEVELOPMENT_IMPLEMENTATION_ZERO_CONFIRMATORY_CREDIT"
CHANGED_INVARIANT = (
    "ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY: "
    "PORT_TO_PORT_ONLY -> PORT_TO_PORT_PLUS_PORT_TO_HIDDEN"
)

PORTS = v1.PORTS
RD006Config = v1.RD006Config
DirectFieldPlasticityConfig = v1.DirectFieldPlasticityConfig
PhysicalConnectionUpdate = v1.PhysicalConnectionUpdate
RuntimePulse = v1.RuntimePulse
EventOrigin = v1.EventOrigin


class PreflightExecutionForbidden(RuntimeError):
    """Raised when result-bearing or protected surfaces are requested."""


def _forbid(entrypoint: str) -> None:
    raise PreflightExecutionForbidden(
        f"{entrypoint} is forbidden by the RD006 v4 synthetic-preflight contract"
    )


def run_matrix(*args: object, **kwargs: object) -> None:
    _forbid("run_matrix")


def run_family_pair(*args: object, **kwargs: object) -> None:
    _forbid("run_family_pair")


def run_execution_cell(*args: object, **kwargs: object) -> None:
    _forbid("run_execution_cell")


def score_capability(*args: object, **kwargs: object) -> None:
    _forbid("score_capability")


def load_held_out(*args: object, **kwargs: object) -> None:
    _forbid("load_held_out")


def _edge_class(source_id: int, target_id: int) -> str:
    source_role = "PORT" if source_id in PORTS else "HIDDEN"
    target_role = "PORT" if target_id in PORTS else "HIDDEN"
    return f"{source_role}_TO_{target_role}"


def _spike_event_id(spike: SpikeEvent) -> str:
    return f"hidden-spike:{v1.digest(spike.as_dict())[:24]}"


class PortToHiddenExternalPlasticity(v1.ExternalOnlyPhysicalPlasticity):
    """Ordinary learner with the single R153 PORT-to-hidden boundary extension.

    PORT-to-PORT processing delegates unchanged to the v1 ordinary learner.
    Hidden spikes are target events only: they never create hidden traces.
    The hidden target magnitude is the binary event value 1.0, matching the
    fixed external pulse magnitude without adding outcome-dependent modulation.
    """

    STATE_SCHEMA_VERSION = 1

    def __init__(
        self,
        field: TemporalExcitableField,
        config: DirectFieldPlasticityConfig | None = None,
    ) -> None:
        resolved = config or DirectFieldPlasticityConfig()
        if resolved != DirectFieldPlasticityConfig():
            raise ValueError("RD006 v4 ordinary learner parameters are fixed")
        super().__init__(field, resolved)
        self.port_to_hidden_update_count = 0
        self.observed_hidden_spike_count = 0
        self.ignored_port_spike_count = 0

    def observe_external(
        self, pulse: RuntimePulse
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        if pulse.origin is EventOrigin.EXTERNAL:
            if not pulse.target.startswith("unit:"):
                raise ValueError("ordinary Field plasticity requires a unit target")
            unit_id = int(pulse.target.removeprefix("unit:"))
            if unit_id not in PORTS:
                raise ValueError("RD006 v4 external traces require a PORT target")
        return super().observe_external(pulse)

    def observe_hidden_spikes(
        self, spikes: tuple[SpikeEvent, ...]
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        """Observe actual Field spikes without accepting outcome context.

        Input order is preserved and must be nondecreasing.  Each hidden spike
        is processed before a same-clock external pulse is observed.  PORT
        spikes are ignored and never become learner traces.
        """

        updates: list[PhysicalConnectionUpdate] = []
        previous_time = self.current_time_ms
        for spike in spikes:
            if spike.unit_id not in self.field.units:
                raise KeyError(f"unknown spike unit: {spike.unit_id}")
            if spike.time_ms < previous_time:
                raise ValueError("spike observations cannot move backwards")
            previous_time = spike.time_ms
            self._expire_traces(spike.time_ms)
            self.current_time_ms = spike.time_ms
            if spike.unit_id in PORTS:
                self.ignored_port_spike_count += 1
                continue
            updates.extend(self._observe_hidden_spike(spike))
            self.observed_hidden_spike_count += 1
        return tuple(updates)

    def observe_clock(
        self,
        spikes: tuple[SpikeEvent, ...],
        external_pulse: RuntimePulse,
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        """Apply hidden-spike updates before the same-clock external trace."""

        hidden_updates = self.observe_hidden_spikes(spikes)
        external_updates = self.observe_external(external_pulse)
        return hidden_updates + external_updates

    def _observe_hidden_spike(
        self, spike: SpikeEvent
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        updates: list[PhysicalConnectionUpdate] = []
        for edge in sorted(
            self.field.incoming[spike.unit_id],
            key=lambda row: (row.source_id, row.target_id),
        ):
            if edge.source_id not in PORTS:
                continue
            trace = self._unit_traces.get(edge.source_id)
            if trace is None or not edge.plastic or edge.weight < 0.0:
                continue
            lag_ms = spike.time_ms - trace.time_ms
            if not self._eligible_lag(lag_ms):
                continue
            modulation = self._modulation(trace.magnitude, 1.0)
            delta = (
                self.config.potentiation_rate
                * modulation
                * math.exp(-lag_ms / self.config.potentiation_tau_ms)
            )
            updates.append(
                self._update_edge(
                    edge,
                    mode="causal_port_to_hidden_potentiation",
                    lag_ms=lag_ms,
                    source_event_id=trace.event_id,
                    target_event_id=_spike_event_id(spike),
                    weight_delta=delta,
                    desired_delay_ms=lag_ms,
                )
            )
            if len(updates) >= self.config.maximum_updates_per_event:
                raise RuntimeError("maximum_updates_per_event exceeded")
        self.port_to_hidden_update_count += len(updates)
        self.update_count += len(updates)
        return tuple(updates)

    def learner_state_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.STATE_SCHEMA_VERSION,
            "protocol_id": PROTOCOL_ID,
            "config": asdict(self.config),
            "current_time_ms": self.current_time_ms,
            "external_observation_count": self.external_observation_count,
            "ignored_endogenous_count": self.ignored_endogenous_count,
            "update_count": self.update_count,
            "port_to_hidden_update_count": self.port_to_hidden_update_count,
            "observed_hidden_spike_count": self.observed_hidden_spike_count,
            "ignored_port_spike_count": self.ignored_port_spike_count,
            "port_traces": [
                asdict(self._unit_traces[unit_id])
                for unit_id in sorted(self._unit_traces)
            ],
        }

    @classmethod
    def from_learner_state_dict(
        cls,
        field: TemporalExcitableField,
        value: dict[str, Any],
    ) -> PortToHiddenExternalPlasticity:
        if value.get("schema_version") != cls.STATE_SCHEMA_VERSION:
            raise ValueError("unsupported RD006 v4 learner state schema")
        if value.get("protocol_id") != PROTOCOL_ID:
            raise ValueError("learner state protocol mismatch")
        config = DirectFieldPlasticityConfig(**value["config"])
        learner = cls(field, config)
        traces: dict[int, v1.UnitExternalTrace] = {}
        for row in value["port_traces"]:
            trace = v1.UnitExternalTrace(**row)
            if trace.unit_id not in PORTS:
                raise ValueError("serialized learner trace must belong to a PORT")
            traces[trace.unit_id] = trace
        learner._unit_traces = traces
        learner.current_time_ms = float(value["current_time_ms"])
        learner.external_observation_count = int(value["external_observation_count"])
        learner.ignored_endogenous_count = int(value["ignored_endogenous_count"])
        learner.update_count = int(value["update_count"])
        learner.port_to_hidden_update_count = int(
            value["port_to_hidden_update_count"]
        )
        learner.observed_hidden_spike_count = int(
            value["observed_hidden_spike_count"]
        )
        learner.ignored_port_spike_count = int(value["ignored_port_spike_count"])
        if learner.current_time_ms != field.current_time_ms:
            raise ValueError("field and learner clocks must match at restore")
        learner._expire_traces(learner.current_time_ms)
        return learner

    def checkpoint(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "field": self.field.state_dict(),
            "learner": self.learner_state_dict(),
        }

    @classmethod
    def from_checkpoint(
        cls, value: dict[str, Any]
    ) -> tuple[TemporalExcitableField, PortToHiddenExternalPlasticity]:
        if value.get("schema_version") != 1:
            raise ValueError("unsupported RD006 v4 checkpoint schema")
        field = TemporalExcitableField.from_state_dict(value["field"])
        return field, cls.from_learner_state_dict(field, value["learner"])


def serialize_checkpoint(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def replay_checkpoint(
    payload: bytes,
) -> tuple[TemporalExcitableField, PortToHiddenExternalPlasticity]:
    value = json.loads(payload.decode("utf-8"))
    if serialize_checkpoint(value) != payload:
        raise ValueError("checkpoint serialization is not canonical")
    return PortToHiddenExternalPlasticity.from_checkpoint(value)


def _microfixture_field() -> TemporalExcitableField:
    units = tuple(
        UnitState(
            unit_id=unit_id,
            x=float(unit_id),
            y=0.0,
            base_threshold=0.5,
        )
        for unit_id in range(38)
    )
    connections = (
        Connection(0, 1, weight=0.05, delay_ms=5.0),
        Connection(0, 36, weight=0.75, delay_ms=5.5),
        Connection(36, 1, weight=0.05, delay_ms=5.0),
        Connection(36, 37, weight=0.05, delay_ms=5.0),
        Connection(2, 36, weight=-0.25, delay_ms=5.0),
        Connection(3, 36, weight=0.05, delay_ms=5.0, plastic=False),
    )
    return TemporalExcitableField(
        explicit_topology(units, connections, receptor_ids=PORTS),
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=1.0,
        ),
    )


def _pulse(unit_id: int, *, event_id: str, time_ms: float) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
    )


def _synthetic_hidden_spike(unit_id: int, time_ms: float) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=("synthetic-contract",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def _positive_microfixture() -> dict[str, Any]:
    field = _microfixture_field()
    learner = PortToHiddenExternalPlasticity(field)
    pulse = _pulse(0, event_id="port-pulse-000", time_ms=0.0)
    learner.observe_external(pulse)
    v1.schedule_external(
        field,
        event_id=pulse.event_id,
        time_ms=pulse.time_ms,
        unit_id=0,
        magnitude=pulse.magnitude,
    )
    port_spikes = field.run_until(0.0)
    checkpoint_payload = serialize_checkpoint(learner.checkpoint())

    hidden_spikes = tuple(
        spike for spike in field.run_until(5.5) if spike.unit_id not in PORTS
    )
    updates = learner.observe_hidden_spikes(hidden_spikes)

    replay_field, replay_learner = replay_checkpoint(checkpoint_payload)
    replay_hidden_spikes = tuple(
        spike
        for spike in replay_field.run_until(5.5)
        if spike.unit_id not in PORTS
    )
    replay_updates = replay_learner.observe_hidden_spikes(replay_hidden_spikes)

    update_rows = tuple(update.state_dict() for update in updates)
    replay_rows = tuple(update.state_dict() for update in replay_updates)
    if len(port_spikes) != 1 or len(hidden_spikes) != 1 or len(updates) != 1:
        raise RuntimeError("positive PORT-to-hidden microfixture did not close")
    if updates[0].source_id != 0 or updates[0].target_id != 36:
        raise RuntimeError("positive microfixture updated the wrong edge")
    final_field_state_equal = v1.canonical_json(
        field.state_dict()
    ) == v1.canonical_json(replay_field.state_dict())
    if update_rows != replay_rows or not final_field_state_equal:
        raise RuntimeError("checkpoint replay diverged")
    return {
        "external_port_pulse": asdict(pulse),
        "actual_port_spikes": [spike.as_dict() for spike in port_spikes],
        "actual_hidden_spikes": [spike.as_dict() for spike in hidden_spikes],
        "updates": list(update_rows),
        "updated_edge_class": _edge_class(
            updates[0].source_id, updates[0].target_id
        ),
        "checkpoint_roundtrip_deterministic": True,
        "replay_updates_equal": update_rows == replay_rows,
        "final_field_state_equal": final_field_state_equal,
    }


def _port_to_port_parity() -> dict[str, Any]:
    parent_field = _microfixture_field()
    v4_field = TemporalExcitableField.from_state_dict(parent_field.state_dict())
    parent = v1.ExternalOnlyPhysicalPlasticity(parent_field)
    learner = PortToHiddenExternalPlasticity(v4_field)
    pulses = (
        _pulse(0, event_id="p2p-000", time_ms=0.0),
        _pulse(1, event_id="p2p-001", time_ms=5.5),
    )
    parent_updates: tuple[PhysicalConnectionUpdate, ...] = ()
    v4_updates: tuple[PhysicalConnectionUpdate, ...] = ()
    for pulse in pulses:
        parent_updates += parent.observe_external(pulse)
        v4_updates += learner.observe_external(pulse)
    parent_rows = tuple(update.state_dict() for update in parent_updates)
    v4_rows = tuple(update.state_dict() for update in v4_updates)
    if parent_rows != v4_rows or parent_field.state_dict() != v4_field.state_dict():
        raise RuntimeError("existing PORT-to-PORT behavior changed")
    return {
        "status": "PASS",
        "updates": list(v4_rows),
        "parent_updates_equal": True,
        "final_field_state_equal": True,
    }


def _negative_microfixtures() -> dict[str, Any]:
    cases: dict[str, Any] = {}
    for name, source_id, spike_time in (
        ("absent_edge", 4, 5.5),
        ("negative_edge", 2, 5.5),
        ("nonplastic_edge", 3, 5.5),
        ("out_of_window", 0, 7.0),
    ):
        field = _microfixture_field()
        learner = PortToHiddenExternalPlasticity(field)
        initial_keys = tuple(sorted(field.connections))
        initial_rows = v1.connection_rows(field)
        learner.observe_external(_pulse(source_id, event_id=name, time_ms=0.0))
        updates = learner.observe_hidden_spikes(
            (_synthetic_hidden_spike(36, spike_time),)
        )
        if updates or tuple(sorted(field.connections)) != initial_keys:
            raise RuntimeError(f"negative microfixture failed: {name}")
        if v1.connection_rows(field) != initial_rows:
            raise RuntimeError(f"negative edge mutated: {name}")
        cases[name] = {
            "status": "PASS",
            "update_count": 0,
            "connection_set_unchanged": True,
            "connection_values_unchanged": True,
        }

    field = _microfixture_field()
    learner = PortToHiddenExternalPlasticity(field)
    initial_rows = v1.connection_rows(field)
    learner.observe_hidden_spikes((_synthetic_hidden_spike(1, 5.5),))
    if v1.connection_rows(field) != initial_rows:
        raise RuntimeError("PORT spike mutated a connection")
    cases["port_spike_not_hidden_target"] = {
        "status": "PASS",
        "update_count": 0,
        "ignored_port_spike_count": learner.ignored_port_spike_count,
    }

    field = _microfixture_field()
    learner = PortToHiddenExternalPlasticity(field)
    forbidden_before = {
        key: asdict(field.connections[key]) for key in ((36, 1), (36, 37))
    }
    learner.observe_external(_pulse(0, event_id="class-guard", time_ms=0.0))
    updates = learner.observe_hidden_spikes((_synthetic_hidden_spike(36, 5.5),))
    forbidden_after = {
        key: asdict(field.connections[key]) for key in ((36, 1), (36, 37))
    }
    if forbidden_before != forbidden_after:
        raise RuntimeError("hidden-source edge class was updated")
    if {_edge_class(update.source_id, update.target_id) for update in updates} != {
        "PORT_TO_HIDDEN"
    }:
        raise RuntimeError("unexpected edge class updated")
    cases["hidden_to_port"] = {
        "status": "PASS",
        "update_count": 0,
        "connection_values_unchanged": True,
    }
    cases["hidden_to_hidden"] = {
        "status": "PASS",
        "update_count": 0,
        "connection_values_unchanged": True,
    }

    field = _microfixture_field()
    learner = PortToHiddenExternalPlasticity(field)
    try:
        learner.observe_external(_pulse(36, event_id="hidden-external", time_ms=0.0))
    except ValueError:
        cases["hidden_external_trace_rejected"] = {"status": "PASS"}
    else:
        raise RuntimeError("hidden external target created a learner trace")
    return cases


def fixed_future_evaluation_surface() -> dict[str, Any]:
    config = RD006Config()
    return {
        "topology": "V3_FIXED",
        "seed": config.seed,
        "families": len(v1.FAMILIES),
        "unit_count": config.unit_count,
        "edge_count": config.unit_count * config.degree,
        "degree": config.degree,
        "event_spacing_ms": 5.5,
        "minimum_return_lag_ms": config.minimum_return_lag_ms,
        "maximum_return_lag_ms": config.maximum_return_lag_ms,
        "threshold": config.threshold,
        "initial_weight": config.initial_weight,
        "initial_delay_ms": config.initial_delay_ms,
        "boundary_gain": config.boundary_gain,
        "input_magnitude": config.input_magnitude,
        "max_events_per_run": config.max_events_per_run,
        "max_spikes_per_run": config.max_spikes_per_run,
    }


def build_synthetic_preflight() -> dict[str, Any]:
    v3_static = v3.build_static_preflight()
    report = {
        "schema_version": 1,
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "analyst_generation_id": ANALYST_GENERATION_ID,
        "parent_audit_head": PARENT_AUDIT_HEAD,
        "development_phase": DEVELOPMENT_PHASE,
        "claim_ceiling": "SYSTEM",
        "evidentiary_status": EVIDENTIARY_STATUS,
        "scientific_credit": 0,
        "changed_invariant": CHANGED_INVARIANT,
        "changed_invariant_count": 1,
        "trace_contract": {
            "source": "ACTUAL_EXTERNAL_PULSE_ON_PORT_ONLY",
            "target": "ACTUAL_HIDDEN_SPIKE",
            "trace_lifetime_ms": [0.5, 6.5],
            "same_clock_precedence": [
                "FIELD_RUN_UNTIL_CLOCK",
                "OBSERVE_ACTUAL_HIDDEN_SPIKES",
                "OBSERVE_CURRENT_EXTERNAL_PORT_PULSE",
                "ENQUEUE_CURRENT_EXTERNAL_PORT_PULSE",
            ],
            "hidden_spike_creates_trace": False,
            "hidden_target_event_magnitude": 1.0,
            "serialization": "FIELD_AND_LEARNER_CHECKPOINT_SCHEMA_1",
        },
        "allowed_update_edge_classes": ["PORT_TO_PORT", "PORT_TO_HIDDEN"],
        "forbidden_update_edge_classes": [
            "HIDDEN_TO_PORT",
            "HIDDEN_TO_HIDDEN",
            "ABSENT_EDGE",
            "NEGATIVE_EDGE",
            "NONPLASTIC_EDGE",
            "NEW_EDGE_CREATION",
        ],
        "ordinary_learner_parameters": asdict(DirectFieldPlasticityConfig()),
        "fixed_future_evaluation_surface": fixed_future_evaluation_surface(),
        "v3_static_preflight_report_sha256": v3_static["report_sha256"],
        "positive_microfixture": _positive_microfixture(),
        "negative_microfixtures": _negative_microfixtures(),
        "port_to_port_behavior": _port_to_port_parity(),
        "outcome_conditioning_inputs_accepted": False,
        "hidden_return_learning_enabled": False,
        "synthetic_microfixture_dynamics_executed": True,
        "six_family_result_bearing_matrix_executed": False,
        "capability_scoring": False,
        "held_out_access": False,
        "new_scientific_result": False,
        "preflight_status": "PASS",
        "next_action": "STOP_FOR_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    report["report_sha256"] = v1.digest(report)
    return report


def serialize_synthetic_preflight(report: dict[str, Any]) -> bytes:
    return (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def replay_synthetic_preflight(payload: bytes) -> dict[str, Any]:
    report = json.loads(payload.decode("utf-8"))
    claimed = report.pop("report_sha256", None)
    computed = v1.digest(report)
    if claimed != computed:
        raise ValueError("synthetic preflight report digest mismatch")
    report["report_sha256"] = claimed
    if serialize_synthetic_preflight(report) != payload:
        raise ValueError("synthetic preflight serialization is not canonical")
    return report


__all__ = [
    "ANALYST_GENERATION_ID",
    "CHANGED_INVARIANT",
    "DEVELOPMENT_PHASE",
    "EVIDENTIARY_STATUS",
    "OBJECT_ID",
    "PARENT_AUDIT_HEAD",
    "PROTOCOL_ID",
    "PortToHiddenExternalPlasticity",
    "PreflightExecutionForbidden",
    "build_synthetic_preflight",
    "fixed_future_evaluation_surface",
    "load_held_out",
    "replay_checkpoint",
    "replay_synthetic_preflight",
    "run_execution_cell",
    "run_family_pair",
    "run_matrix",
    "score_capability",
    "serialize_checkpoint",
    "serialize_synthetic_preflight",
]
