"""Integrity-safe raw acquisition and delayed scoring for A01 MD-002 P2.

The scientific candidate must cross STARTED before :func:`acquire_p2_shared_probe`
is called. Acquisition emits observations only; it deliberately cannot emit a
verdict. A preserved raw payload can later be reconstructed and scored under the
already-fixed P2 criteria.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .md002_development_plan import build_p2_development_plan
from .md002_fixtures import P2WorldOnlyFixture
from .md002_p2_schedule import P2ClonedSubepisodeSchedule
from .md002_p2_shared_probe import (
    P2ProbeProposal,
    P2SharedProbeObservation,
    P2SharedProbeRun,
    _execute_observation,
    _score,
)

P2_SHARED_PROBE_CRITERIA = (
    "withheld arms remain co-maximal at the shared root",
    "returned evidence changes only the causally addressed local target confidence",
    "exact-match raises and selects the requested target",
    "exact-contradiction lowers and deselects the requested target",
    "world permutation swaps match/contradiction status for each fixed proposal identity",
    "predicted arrival times remain unchanged by causal-support credit",
)


@dataclass(frozen=True, slots=True)
class P2SharedProbeRaw:
    """Raw post-attribution observations with no scientific verdict."""

    observations: tuple[P2SharedProbeObservation, ...]
    criteria: tuple[str, ...] = P2_SHARED_PROBE_CRITERIA

    def state_dict(self) -> dict[str, Any]:
        return {
            "schema": "v061-a01-md002-p2-shared-probe-raw-v1",
            "observations": [row.state_dict() for row in self.observations],
            "criteria": list(self.criteria),
            "development_only": True,
            "held_out_executed": False,
            "formal_execution_opened": False,
            "scored": False,
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> P2SharedProbeRaw:
        if value.get("schema") != "v061-a01-md002-p2-shared-probe-raw-v1":
            raise ValueError("unexpected P2 raw schema")
        if value.get("development_only") is not True:
            raise ValueError("P2 raw payload must remain development-only")
        if value.get("held_out_executed") is not False:
            raise ValueError("P2 raw payload cannot contain held-out execution")
        if value.get("formal_execution_opened") is not False:
            raise ValueError("P2 raw payload cannot open formal execution")
        if value.get("scored") is not False:
            raise ValueError("P2 raw payload must be unscored")
        criteria = tuple(str(row) for row in value.get("criteria", ()))
        if criteria != P2_SHARED_PROBE_CRITERIA:
            raise ValueError("P2 raw scoring criteria drifted")
        observations_value = value.get("observations")
        if not isinstance(observations_value, list):
            raise TypeError("P2 raw observations must be a list")
        observations = tuple(_observation_from_state_dict(row) for row in observations_value)
        if len(observations) != 8:
            raise ValueError("P2 raw payload requires exactly eight observations")
        return cls(observations=observations, criteria=criteria)


def _proposal_from_state_dict(value: dict[str, Any]) -> P2ProbeProposal:
    local_path_ids = value.get("local_path_ids")
    if not isinstance(local_path_ids, (list, tuple)):
        raise TypeError("P2 raw proposal local_path_ids must be a sequence")
    return P2ProbeProposal(
        target=str(value["target"]),
        confidence=float(value["confidence"]),
        predicted_arrival_ms=float(value["predicted_arrival_ms"]),
        local_path_ids=tuple(str(row) for row in local_path_ids),
    )


def _observation_from_state_dict(value: Any) -> P2SharedProbeObservation:
    if not isinstance(value, dict):
        raise TypeError("P2 raw observation must be an object")
    probe_rows = value.get("probe_rows")
    selected_targets = value.get("selected_targets")
    if not isinstance(probe_rows, list):
        raise TypeError("P2 raw probe_rows must be a list")
    if not isinstance(selected_targets, (list, tuple)):
        raise TypeError("P2 raw selected_targets must be a sequence")
    resolution_status = value.get("resolution_status")
    if resolution_status is not None and not isinstance(resolution_status, str):
        raise TypeError("P2 raw resolution_status must be string or null")
    observation = P2SharedProbeObservation(
        condition_id=str(value["condition_id"]),
        world_arm=str(value["world_arm"]),
        returned_external_evidence=bool(value["returned_external_evidence"]),
        proposal_id=str(value["proposal_id"]),
        requested_target=str(value["requested_target"]),
        response_target=str(value["response_target"]),
        resolution_status=resolution_status,
        probe_rows=tuple(_proposal_from_state_dict(row) for row in probe_rows),
        selected_targets=tuple(str(row) for row in selected_targets),
    )
    observation.state_dict()
    return observation


def acquire_p2_shared_probe(
    fixture: P2WorldOnlyFixture,
    schedule: P2ClonedSubepisodeSchedule,
) -> P2SharedProbeRaw:
    """Acquire the fixed development observations without computing a verdict."""

    fixture.validate()
    schedule.validate()
    conditions = build_p2_development_plan(fixture, schedule)
    observations = tuple(
        _execute_observation(condition, subepisode)
        for condition in conditions
        for subepisode in schedule.subepisodes
    )
    raw = P2SharedProbeRaw(observations=observations)
    raw.state_dict()
    return raw


def score_preserved_p2_shared_probe(raw: P2SharedProbeRaw) -> P2SharedProbeRun:
    """Score an already-preserved raw payload under the frozen criteria."""

    raw.state_dict()
    result = P2SharedProbeRun(
        observations=raw.observations,
        verdict=_score(raw.observations),
        criteria=raw.criteria,
    )
    result.state_dict()
    return result


__all__ = [
    "P2_SHARED_PROBE_CRITERIA",
    "P2SharedProbeRaw",
    "acquire_p2_shared_probe",
    "score_preserved_p2_shared_probe",
]
