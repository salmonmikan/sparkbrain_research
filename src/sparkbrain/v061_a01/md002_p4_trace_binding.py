"""Execution-disabled retained-trace binding for A01 MD-002 P4.

P4 requires genuinely merged BoundaryEvent ancestry and later runtime-active
lineages. This module derives those identities only from retained runtime trace
records and actual BoundaryEvent objects; callers cannot provide expected
before/after lineage constants separately or cherry-pick only a favorable
subset of retained P4 boundary events.

No evidence is applied, no capability is scored, and the MD-002 execution gate
is not opened here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent

from .md002_protocol import MergedAncestryObservation, canonical_sha256


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    rows: list[str] = []
    for value in values:
        if not value:
            raise ValueError("P4 proposal identifiers must be non-empty")
        if value not in seen:
            seen.add(value)
            rows.append(value)
    return tuple(rows)


def _lineage_record(
    runtime_trace: tuple[dict[str, Any], ...],
    *,
    phase: str,
) -> tuple[str, ...]:
    matches = [
        row
        for row in runtime_trace
        if row.get("type") == "md002-p4-active-lineages" and row.get("phase") == phase
    ]
    if len(matches) != 1:
        raise ValueError(f"P4 trace requires exactly one {phase} active-lineage record")
    proposal_ids = matches[0].get("proposal_ids")
    if not isinstance(proposal_ids, list):
        raise ValueError("P4 active-lineage records require a proposal_ids list")
    if any(not isinstance(value, str) for value in proposal_ids):
        raise TypeError("P4 active-lineage proposal IDs must be strings")
    values = tuple(proposal_ids)
    if len(values) != len(set(values)):
        raise ValueError("P4 active-lineage proposal IDs must be unique")
    return _ordered_unique(values)


@dataclass(frozen=True, slots=True)
class P4RetainedTraceInput:
    """Retained P4 runtime material before scientific interpretation."""

    boundary_events: tuple[BoundaryEvent, ...]
    runtime_trace: tuple[dict[str, Any], ...]
    runtime_trace_sha256: str

    def validate(self) -> None:
        if not self.boundary_events:
            raise ValueError("P4 requires retained BoundaryEvent evidence")
        if not self.runtime_trace:
            raise ValueError("P4 requires a retained runtime trace")
        if self.runtime_trace_sha256 != canonical_sha256(self.runtime_trace):
            raise ValueError("P4 retained runtime trace digest mismatch")

        event_ids = tuple(event.event_id for event in self.boundary_events)
        if len(event_ids) != len(set(event_ids)):
            raise ValueError("P4 retained BoundaryEvents must be unique")

        retained_boundary_rows = tuple(
            row for row in self.runtime_trace if row.get("type") == "md002-p4-boundary-event"
        )
        if len(retained_boundary_rows) != len(self.boundary_events):
            raise ValueError(
                "P4 supplied BoundaryEvents must cover the complete retained boundary-event trace"
            )
        expected_boundary_rows = tuple(
            {"type": "md002-p4-boundary-event", "event": event.state_dict()}
            for event in self.boundary_events
        )
        if len({canonical_sha256(row) for row in retained_boundary_rows}) != len(
            retained_boundary_rows
        ):
            raise ValueError("P4 retained boundary-event trace contains duplicate rows")
        if {canonical_sha256(row) for row in retained_boundary_rows} != {
            canonical_sha256(row) for row in expected_boundary_rows
        }:
            raise ValueError(
                "P4 supplied BoundaryEvents do not exactly match the complete retained trace"
            )

        merged_events = tuple(
            event
            for event in self.boundary_events
            if len(set(event.source_proposal_ids)) >= 2
        )
        if not merged_events:
            raise ValueError("P4 requires a genuinely merged BoundaryEvent ancestry")
        for event in merged_events:
            if len(event.source_proposal_ids) != len(set(event.source_proposal_ids)):
                raise ValueError("P4 merged BoundaryEvent ancestry contains duplicate IDs")
            _ordered_unique(event.source_proposal_ids)

        before = _lineage_record(self.runtime_trace, phase="before")
        after = _lineage_record(self.runtime_trace, phase="after")
        boundary = self.merged_source_proposal_ids
        payload = {
            "boundary_source_proposal_ids": boundary,
            "active_lineages_before": before,
            "active_lineages_after": after,
        }
        measurement_record = {
            "type": "md002-merged-ancestry-measurement",
            "measurement": payload,
        }
        matches = [row for row in self.runtime_trace if row == measurement_record]
        if len(matches) != 1:
            raise ValueError(
                "P4 derived lineage measurement is not bound exactly once to the retained trace"
            )

    @property
    def merged_source_proposal_ids(self) -> tuple[str, ...]:
        values: list[str] = []
        for event in self.boundary_events:
            unique = _ordered_unique(event.source_proposal_ids)
            if len(unique) >= 2:
                values.extend(unique)
        return _ordered_unique(tuple(values))

    def observation(self) -> MergedAncestryObservation:
        self.validate()
        boundary = self.merged_source_proposal_ids
        before = _lineage_record(self.runtime_trace, phase="before")
        after = _lineage_record(self.runtime_trace, phase="after")
        payload = {
            "boundary_source_proposal_ids": boundary,
            "active_lineages_before": before,
            "active_lineages_after": after,
        }
        observation = MergedAncestryObservation(
            boundary_source_proposal_ids=boundary,
            active_lineages_before=before,
            active_lineages_after=after,
            runtime_trace=self.runtime_trace,
            runtime_trace_sha256=self.runtime_trace_sha256,
            measurement_record_sha256=canonical_sha256(payload),
        )
        observation.validate()
        return observation


__all__ = ["P4RetainedTraceInput"]
