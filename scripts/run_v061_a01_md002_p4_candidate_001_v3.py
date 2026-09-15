#!/usr/bin/env python3
"""Serialization-safe entrypoint for the prospectively repaired P4 candidate.

The P4 retained-trace protocol intentionally keeps active-lineage records as
JSON lists while the bound merged-ancestry measurement is represented as
protocol tuples in memory. Raw evidence is JSON, so this entrypoint normalizes
only that measurement payload back to the protocol representation before the
frozen scorer re-validates ``P4RetainedTraceInput``. No candidate mechanism,
threshold, condition, or verdict rule is changed here.
"""

from __future__ import annotations

from typing import Any

import run_v061_a01_md002_p4_candidate_001_v2 as core

from sparkbrain.v061_a01.md002_p4_trace_binding import P4RetainedTraceInput
from sparkbrain.v061_a01.md002_protocol import canonical_sha256


def _trace_from_json(values: list[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for value in values:
        row = dict(value)
        if row.get("type") == "md002-merged-ancestry-measurement":
            measurement = dict(row.get("measurement", {}))
            for key in (
                "boundary_source_proposal_ids",
                "active_lineages_before",
                "active_lineages_after",
            ):
                current = measurement.get(key)
                if isinstance(current, list):
                    measurement[key] = tuple(str(item) for item in current)
            row["measurement"] = measurement
        rows.append(row)
    return tuple(rows)


def _validate_trace_binding(row: dict[str, Any]) -> str | None:
    trace_value = row.get("retained_runtime_trace")
    events_value = row.get("retained_boundary_events")
    digest_value = row.get("retained_runtime_trace_sha256")
    observation_value = row.get("merged_ancestry_observation")
    if not isinstance(trace_value, list) or not isinstance(events_value, list):
        return "missing-retained-runtime-trace"
    if not isinstance(digest_value, str):
        return "missing-retained-runtime-trace-digest"
    if not isinstance(observation_value, dict):
        return "missing-merged-ancestry-observation"
    try:
        events = tuple(
            core._boundary_from_state(dict(value)) for value in events_value
        )
        trace = _trace_from_json(trace_value)
        retained = P4RetainedTraceInput(
            boundary_events=events,
            runtime_trace=trace,
            runtime_trace_sha256=digest_value,
        )
        expected = core._observation_state(retained.observation())
    except (KeyError, TypeError, ValueError) as error:
        return f"retained-trace-invalid:{type(error).__name__}"
    if canonical_sha256(observation_value) != canonical_sha256(expected):
        return "retained-trace-observation-binding"
    return None


core._validate_trace_binding = _validate_trace_binding


if __name__ == "__main__":
    core.main()
