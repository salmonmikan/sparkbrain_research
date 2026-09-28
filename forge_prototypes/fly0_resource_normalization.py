"""Resource-exposure diagnostic for the noncanonical FLY-0 loop.

The diagnostic separates metrics that share an exact controller-interface
definition from implementation-local activity counters.  It deliberately
refuses to turn unlike activity instrumentation into a matched-resource claim.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Literal

from forge_prototypes.fly0_hierarchical_loop import (
    HierarchicalSensorimotorLoop,
    WorldState,
    build_fly0_loop,
    build_reactive_loop,
    run_to_target,
)

ActivityBasis = Literal["topology_trace_events", "reactive_activation_events"]
LoopBuilder = Callable[[WorldState], HierarchicalSensorimotorLoop]


@dataclass(frozen=True)
class ExposureRow:
    controller: str
    activity_basis: ActivityBasis
    accepted_steps: int
    committed_world_transitions: int
    controller_calls: int
    active_proposals: int
    fired_events: int
    peak_fired_events_per_controller_call: int
    event_budget_per_controller_call: int
    replay_exact: bool

    def __post_init__(self) -> None:
        integer_fields = (
            self.accepted_steps,
            self.committed_world_transitions,
            self.controller_calls,
            self.active_proposals,
            self.fired_events,
            self.peak_fired_events_per_controller_call,
            self.event_budget_per_controller_call,
        )
        if any(value < 0 for value in integer_fields):
            raise ValueError("exposure counters must be non-negative")
        if self.committed_world_transitions < 1:
            raise ValueError("at least one committed transition is required")
        if self.event_budget_per_controller_call < 1:
            raise ValueError("event budget must be positive")
        if self.peak_fired_events_per_controller_call > self.event_budget_per_controller_call:
            raise ValueError("observed activity exceeds the declared event budget")

    def common_surface_per_transition(self) -> dict[str, float]:
        denominator = self.committed_world_transitions
        return {
            "controller_calls": self.controller_calls / denominator,
            "active_proposals": self.active_proposals / denominator,
        }

    def activity_per_transition(self) -> dict[str, float]:
        """Return descriptive activity only; the basis must stay attached."""

        denominator = self.committed_world_transitions
        return {
            "fired_events": self.fired_events / denominator,
            "peak_budget_fraction": (
                self.peak_fired_events_per_controller_call
                / self.event_budget_per_controller_call
            ),
        }


@dataclass(frozen=True)
class ResourceNormalizationReport:
    status: str
    initial_world: WorldState
    rows: tuple[ExposureRow, ...]
    common_interface_exposure_matched: bool
    activity_instrumentation_commensurate: bool
    activity_resource_exposure_matched: bool
    reason_codes: tuple[str, ...]
    claim_boundary: str

    def summary(self) -> dict[str, object]:
        return {
            "status": self.status,
            "initial_world": asdict(self.initial_world),
            "rows": {
                row.controller: {
                    **asdict(row),
                    "common_surface_per_transition": row.common_surface_per_transition(),
                    "activity_per_transition": row.activity_per_transition(),
                }
                for row in self.rows
            },
            "comparability": {
                "common_interface_exposure_matched": (
                    self.common_interface_exposure_matched
                ),
                "activity_instrumentation_commensurate": (
                    self.activity_instrumentation_commensurate
                ),
                "activity_resource_exposure_matched": (
                    self.activity_resource_exposure_matched
                ),
                "reason_codes": list(self.reason_codes),
            },
            "claim_boundary": self.claim_boundary,
        }


def _capture_exposure(
    name: str,
    builder: LoopBuilder,
    basis: ActivityBasis,
    initial_world: WorldState,
) -> ExposureRow:
    loop = builder(initial_world)
    checkpoint = loop.checkpoint()
    first = run_to_target(loop)
    first_tokens = tuple(result.after.token() for result in first)
    loop.restore(checkpoint)
    second = run_to_target(loop)
    accepted = tuple(result for result in first if result.accepted)
    proposals = tuple(proposal for result in accepted for proposal in result.proposals)
    active = tuple(proposal for proposal in proposals if proposal.active)
    per_call = tuple(proposal.feedback.fired_events for proposal in proposals)
    return ExposureRow(
        controller=name,
        activity_basis=basis,
        accepted_steps=len(accepted),
        committed_world_transitions=len(accepted),
        controller_calls=len(proposals),
        active_proposals=len(active),
        fired_events=sum(per_call),
        peak_fired_events_per_controller_call=max(per_call, default=0),
        event_budget_per_controller_call=loop.event_budget,
        replay_exact=first_tokens
        == tuple(result.after.token() for result in second),
    )


def build_resource_normalization_report() -> ResourceNormalizationReport:
    initial_world = WorldState(position=2, target=-1)
    rows = (
        _capture_exposure(
            "fly0_structured",
            build_fly0_loop,
            "topology_trace_events",
            initial_world,
        ),
        _capture_exposure(
            "reactive_reference",
            build_reactive_loop,
            "reactive_activation_events",
            initial_world,
        ),
    )
    common_signatures = {
        (
            row.accepted_steps,
            row.committed_world_transitions,
            row.controller_calls,
            row.active_proposals,
            row.event_budget_per_controller_call,
            row.common_surface_per_transition()["controller_calls"],
            row.common_surface_per_transition()["active_proposals"],
        )
        for row in rows
    }
    bases = {row.activity_basis for row in rows}
    activity_signatures = {
        (
            row.fired_events,
            row.peak_fired_events_per_controller_call,
            row.activity_per_transition()["fired_events"],
        )
        for row in rows
    }
    common_matched = len(common_signatures) == 1
    commensurate = len(bases) == 1
    activity_matched = commensurate and len(activity_signatures) == 1
    reasons: list[str] = []
    if not commensurate:
        reasons.append("DISTINCT_ACTIVITY_INSTRUMENTATION")
    if len(activity_signatures) != 1:
        reasons.append("RAW_ACTIVITY_EXPOSURE_MISMATCH")
    if not common_matched:
        reasons.append("COMMON_INTERFACE_EXPOSURE_MISMATCH")
    return ResourceNormalizationReport(
        status="NON_EVIDENTIARY_NONCANONICAL_FORGE",
        initial_world=initial_world,
        rows=rows,
        common_interface_exposure_matched=common_matched,
        activity_instrumentation_commensurate=commensurate,
        activity_resource_exposure_matched=activity_matched,
        reason_codes=tuple(reasons),
        claim_boundary=(
            "Interface-normalized counts are engineering diagnostics only; internal "
            "activity counts do not support performance, energy, topology-superiority, "
            "biological-fidelity, or scientific claims."
        ),
    )


def require_matched_activity_exposure(report: ResourceNormalizationReport) -> None:
    """Fail closed before any caller labels unlike activity exposure as matched."""

    if not report.activity_resource_exposure_matched:
        reasons = ",".join(report.reason_codes) or "UNSPECIFIED_ACTIVITY_MISMATCH"
        raise RuntimeError(f"activity resource exposure is not matched: {reasons}")


if __name__ == "__main__":
    print(
        json.dumps(
            build_resource_normalization_report().summary(),
            indent=2,
            sort_keys=True,
        )
    )
