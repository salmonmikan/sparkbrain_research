"""Independent fail-closed verifier for RD005 construction artifacts.

This module is deliberately separate from construction. It reconstructs the
prospective hidden-return gate from retained artifact rows and refuses future
capability eligibility unless every D1_READY cell contains the complete,
mutually consistent gate evidence fixed by the preregistration.

It runs no learner or probe and grants no formal/held-out authority.
"""

from __future__ import annotations

import math

from .rv02_rd005_construction_artifact import (
    RD005ConstructionArtifact,
    RD005ConstructionCell,
)
from .rv02_rd005_gate_construction import (
    ConnectionSnapshot,
    RD005GateConstruction,
)


def _connection_snapshots(cell: RD005ConstructionCell) -> tuple[ConnectionSnapshot, ...]:
    rows: list[ConnectionSnapshot] = []
    for row in cell.connection_rows:
        required = {"source_id", "target_id", "plastic", "weight"}
        if not required.issubset(row):
            raise ValueError("RD005 retained connection row is incomplete")
        if type(row["source_id"]) is not int or type(row["target_id"]) is not int:
            raise TypeError("RD005 retained connection IDs must be integers")
        if type(row["plastic"]) is not bool:
            raise TypeError("RD005 retained connection plastic flag must be boolean")
        weight = row["weight"]
        if isinstance(weight, bool) or not isinstance(weight, int | float):
            raise TypeError("RD005 retained connection weight must be numeric")
        if not math.isfinite(float(weight)):
            raise ValueError("RD005 retained connection weight must be finite")
        rows.append(
            ConnectionSnapshot(
                source_id=row["source_id"],
                target_id=row["target_id"],
                plastic=row["plastic"],
                initial_weight=float(weight),
            )
        )
    if not rows:
        raise ValueError("RD005 D1_READY cell requires retained connection rows")
    return tuple(rows)


def _certificate_states(rows: tuple[object, ...]) -> tuple[dict[str, object], ...]:
    states: list[dict[str, object]] = []
    for row in rows:
        state_dict = getattr(row, "state_dict", None)
        if not callable(state_dict):
            raise TypeError("RD005 certificate does not expose state_dict")
        states.append(state_dict())
    return tuple(states)


def verify_rd005_construction_cell(cell: RD005ConstructionCell) -> None:
    """Verify one retained cell as future-capability input, without executing it."""

    cell.validate()
    if cell.status == "CONSTRUCTION_INTEGRITY_FAILURE":
        return

    if cell.status == "D1_UNREACHABLE":
        if cell.error is not None:
            raise ValueError("RD005 unreachable cell must not carry an integrity error")
        if cell.selected_clock_ms is not None:
            raise ValueError("RD005 unreachable cell cannot select a gate clock")
        if any(
            (
                cell.eligibility_events,
                cell.return_events,
                cell.es_assignment,
                cell.e1_certificates,
                cell.es_certificates,
            )
        ):
            raise ValueError("RD005 unreachable cell cannot retain ready-only gate evidence")
        return

    if cell.status != "D1_READY":
        raise ValueError("RD005 construction cell has an unknown status")
    if cell.error is not None:
        raise ValueError("RD005 D1_READY cell cannot carry an integrity error")
    if cell.selected_clock_ms is None or not math.isfinite(float(cell.selected_clock_ms)):
        raise ValueError("RD005 D1_READY cell requires a finite selected clock")
    inspected_times = tuple(float(row.time_ms) for row in cell.inspected_clocks)
    if float(cell.selected_clock_ms) not in inspected_times:
        raise ValueError("RD005 selected clock is not retained in inspected construction clocks")
    if not cell.eligibility_events or not cell.return_events:
        raise ValueError("RD005 D1_READY cell requires a non-empty shared gate budget")
    if not cell.es_assignment:
        raise ValueError("RD005 D1_READY cell requires an ES source assignment")
    if not cell.e1_certificates or not cell.es_certificates:
        raise ValueError("RD005 D1_READY cell requires retained E1/ES certificates")

    gate = RD005GateConstruction(
        eligibility_events=cell.eligibility_events,
        return_events=cell.return_events,
        connections=_connection_snapshots(cell),
        shuffled_assignment=dict(cell.es_assignment),
    )
    gate.assert_development_matrix_reachable()

    expected_e1 = _certificate_states(gate.certificates("E1"))
    expected_es = _certificate_states(gate.certificates("ES"))
    actual_e1 = _certificate_states(cell.e1_certificates)
    actual_es = _certificate_states(cell.es_certificates)
    if actual_e1 != expected_e1:
        raise ValueError("RD005 retained E1 certificates do not reconstruct from artifact inputs")
    if actual_es != expected_es:
        raise ValueError("RD005 retained ES certificates do not reconstruct from artifact inputs")


def verify_rd005_artifact_for_future_capability(
    artifact: RD005ConstructionArtifact,
) -> tuple[str, ...]:
    """Return the exact capability-cell inventory only after independent verification."""

    artifact.validate()
    for cell in artifact.cells:
        verify_rd005_construction_cell(cell)
    if any(cell.status == "CONSTRUCTION_INTEGRITY_FAILURE" for cell in artifact.cells):
        return ()
    ready = tuple(cell.cell_id for cell in artifact.cells if cell.status == "D1_READY")
    if not ready:
        return ()
    return ready


__all__ = [
    "verify_rd005_artifact_for_future_capability",
    "verify_rd005_construction_cell",
]
