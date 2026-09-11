"""RD003 online hidden-eligibility adapter; development only.

This module implements the smallest prospective mechanism required by the
RD003 preregistration. Hidden runtime spikes may create short-lived local
eligibility, but only a later externally originated observation may commit a
physical connection update. The module contains no task score, route label,
reward, correctness flag, or success-directed input.
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.research.rv01.physical_plasticity import (
    ExternalOnlyPhysicalPlasticity,
    PhysicalConnectionUpdate,
)
from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse

EligibilityMode = Literal["disabled", "causal", "shuffled"]


@dataclass(frozen=True, slots=True)
class HiddenEligibilityTrace:
    observed_unit_id: int
    assigned_source_id: int
    time_ms: float
    magnitude: float
    event_id: str
    source_pulse_ids: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["source_pulse_ids"] = list(self.source_pulse_ids)
        return row


def deterministic_hidden_permutation(
    hidden_units: Iterable[int], *, namespace: str
) -> dict[int, int]:
    """Return a deterministic non-identity cycle over hidden unit ids.

    The mapping is fixed from a caller-supplied namespace and unit inventory;
    it never depends on task outcomes. A singleton hidden inventory cannot
    support the lineage-shuffled control and therefore fails closed.
    """

    units = tuple(sorted(set(int(unit_id) for unit_id in hidden_units)))
    if len(units) < 2:
        raise ValueError("shuffled eligibility requires at least two hidden units")
    if not namespace:
        raise ValueError("permutation namespace must be non-empty")
    material = f"rv02-rd003-es-v1|{namespace}|{','.join(map(str, units))}"
    raw = hashlib.sha256(material.encode("utf-8")).digest()
    offset = 1 + int.from_bytes(raw[:8], "big") % (len(units) - 1)
    return {
        unit_id: units[(index + offset) % len(units)]
        for index, unit_id in enumerate(units)
    }


class OnlineHiddenEligibilityPlasticity(ExternalOnlyPhysicalPlasticity):
    """External-only physical learner plus transient hidden-return eligibility.

    Recording hidden spikes never mutates physical connection state. A later
    external observation may potentiate an existing hidden->visible connection
    when the retained hidden trace falls inside the inherited direct-Field lag
    window. In ``shuffled`` mode the same trace budget is reassigned through a
    deterministic hidden-unit permutation before any outcome is observed.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        *,
        visible_units: Iterable[int],
        mode: EligibilityMode,
        shuffled_mapping: dict[int, int] | None = None,
    ) -> None:
        super().__init__(field)
        if mode not in ("disabled", "causal", "shuffled"):
            raise ValueError("invalid RD003 eligibility mode")
        self.visible_units = frozenset(int(unit_id) for unit_id in visible_units)
        if not self.visible_units or not self.visible_units.issubset(field.units):
            raise ValueError("visible unit inventory must be a non-empty Field subset")
        self.hidden_units = frozenset(set(field.units) - set(self.visible_units))
        if not self.hidden_units:
            raise ValueError("RD003 requires at least one hidden unit")
        self.mode: EligibilityMode = mode
        self.shuffled_mapping = self._validate_mapping(shuffled_mapping)
        self._hidden_traces: dict[int, HiddenEligibilityTrace] = {}
        self.hidden_trace_records: list[HiddenEligibilityTrace] = []
        self.hidden_trace_expiry_records: list[dict[str, Any]] = []
        self.hidden_return_updates: list[PhysicalConnectionUpdate] = []

    def _validate_mapping(
        self, mapping: dict[int, int] | None
    ) -> dict[int, int] | None:
        if self.mode != "shuffled":
            if mapping is not None:
                raise ValueError("only shuffled mode accepts a hidden permutation")
            return None
        if mapping is None:
            raise ValueError("shuffled mode requires a hidden permutation")
        normalized = {int(source): int(target) for source, target in mapping.items()}
        if set(normalized) != set(self.hidden_units):
            raise ValueError("shuffled mapping keys must equal hidden unit inventory")
        if set(normalized.values()) != set(self.hidden_units):
            raise ValueError("shuffled mapping must be a bijection over hidden units")
        if any(source == target for source, target in normalized.items()):
            raise ValueError("shuffled mapping must not preserve a hidden identity")
        return normalized

    def record_hidden_spikes(
        self, spikes: Iterable[SpikeEvent]
    ) -> tuple[HiddenEligibilityTrace, ...]:
        """Record runtime hidden spikes without changing any physical edge."""

        rows: list[HiddenEligibilityTrace] = []
        if self.mode == "disabled":
            return ()
        for spike in spikes:
            if spike.unit_id not in self.hidden_units:
                continue
            assigned = spike.unit_id
            if self.mode == "shuffled":
                assert self.shuffled_mapping is not None
                assigned = self.shuffled_mapping[spike.unit_id]
            magnitude = max(0.0, float(spike.potential_before_reset))
            event_material = (
                f"{spike.unit_id}|{assigned}|{spike.time_ms:.12g}|"
                + "|".join(spike.source_pulse_ids)
            )
            event_id = "rv02-rd003-hidden-" + hashlib.sha256(
                event_material.encode("utf-8")
            ).hexdigest()[:20]
            trace = HiddenEligibilityTrace(
                observed_unit_id=spike.unit_id,
                assigned_source_id=assigned,
                time_ms=float(spike.time_ms),
                magnitude=magnitude,
                event_id=event_id,
                source_pulse_ids=tuple(spike.source_pulse_ids),
            )
            self._hidden_traces[assigned] = trace
            self.hidden_trace_records.append(trace)
            rows.append(trace)
        return tuple(rows)

    def observe_external(
        self, pulse: RuntimePulse
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        if pulse.origin is not EventOrigin.EXTERNAL:
            return super().observe_external(pulse)
        self._expire_hidden_traces(pulse.time_ms)
        hidden_updates = self._commit_hidden_returns(pulse)
        ordinary_updates = super().observe_external(pulse)
        self.hidden_return_updates.extend(hidden_updates)
        return hidden_updates + ordinary_updates

    def _expire_hidden_traces(self, now_ms: float) -> None:
        expired = tuple(
            source_id
            for source_id, trace in self._hidden_traces.items()
            if now_ms - trace.time_ms > self.config.maximum_lag_ms
        )
        for source_id in expired:
            trace = self._hidden_traces.pop(source_id)
            self.hidden_trace_expiry_records.append(
                {
                    "assigned_source_id": source_id,
                    "event_id": trace.event_id,
                    "expired_at_ms": float(now_ms),
                    "trace_time_ms": trace.time_ms,
                }
            )

    def _commit_hidden_returns(
        self, pulse: RuntimePulse
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        if self.mode == "disabled":
            return ()
        target_id = self._unit_id(pulse.target)
        if target_id not in self.visible_units:
            raise ValueError("RD003 external gate must target a visible unit")
        updates: list[PhysicalConnectionUpdate] = []
        for edge in sorted(
            self.field.incoming[target_id],
            key=lambda row: (row.source_id, row.target_id),
        ):
            if edge.source_id not in self.hidden_units:
                continue
            trace = self._hidden_traces.get(edge.source_id)
            if trace is None or not edge.plastic or edge.weight < 0.0:
                continue
            lag = pulse.time_ms - trace.time_ms
            if not self._eligible_lag(lag):
                continue
            modulation = self._modulation(trace.magnitude, pulse.magnitude)
            factor = math.exp(-lag / self.config.potentiation_tau_ms)
            weight_delta = self.config.potentiation_rate * modulation * factor
            updates.append(
                self._update_edge(
                    edge.source_id,
                    edge.target_id,
                    mode="hidden_return_potentiation",
                    lag_ms=lag,
                    source_event_id=trace.event_id,
                    target_event_id=pulse.event_id,
                    weight_delta=weight_delta,
                    desired_delay_ms=lag,
                )
            )
            if len(updates) >= self.config.maximum_updates_per_event:
                raise RuntimeError("maximum_updates_per_event exceeded")
        return tuple(updates)

    def state_dict(self) -> dict[str, Any]:
        row = super().state_dict()
        row.update(
            {
                "eligibility_mode": self.mode,
                "visible_units": sorted(self.visible_units),
                "hidden_units": sorted(self.hidden_units),
                "shuffled_mapping": (
                    None
                    if self.shuffled_mapping is None
                    else {
                        str(source): target
                        for source, target in sorted(self.shuffled_mapping.items())
                    }
                ),
                "hidden_traces": {
                    str(source_id): trace.state_dict()
                    for source_id, trace in sorted(self._hidden_traces.items())
                },
                "hidden_trace_records": [
                    trace.state_dict() for trace in self.hidden_trace_records
                ],
                "hidden_trace_expiry_records": list(self.hidden_trace_expiry_records),
                "hidden_return_updates": [
                    update.state_dict() for update in self.hidden_return_updates
                ],
            }
        )
        return row


__all__ = [
    "EligibilityMode",
    "HiddenEligibilityTrace",
    "OnlineHiddenEligibilityPlasticity",
    "deterministic_hidden_permutation",
]
