"""Prospective exposed-development R01-17 real-delay causal timing probe.

The real five-cell acquisition is intentionally callable only by the frozen
execution wrapper. CI tests should exercise construction and pure scoring
helpers with synthetic rows and must not call :func:`acquire_raw_suite`.
"""

from __future__ import annotations

import copy
import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

from sparkbrain.research.rv01.physical_learner_bridge import (
    CurrentPhysicalLearnerBridge,
    build_physical_field,
    connection_snapshots,
    connection_state_hash,
    runtime_pulse,
)
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin

R01_17_PROTOCOL_ID = "rv01-r01-17-real-delay-causal-timing-v1"
R01_17_WORLD_SALT = "rv01-r01-17-real-delay-world-grid-v1"
R01_17_DEVELOPMENT_SEEDS = (141800, 141801, 141802, 141803, 141804)
R01_17_UNIT_COUNT = 4
R01_17_ROUTE = (0, 1, 2, 3)
R01_17_EXPOSURES = 6
R01_17_INITIAL_WEIGHT = 0.05
R01_17_MIN_DELAY_DISPLACEMENT_MS = 0.5
R01_17_MIN_CAUSAL_SHIFT_MS = 0.5
R01_17_TIMING_TOLERANCE_MS = 0.05
R01_17_FORMAL_AUTHORITY = False
R01_17_HELD_OUT_AUTHORITY = False


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class R0117WorldSpec:
    seed: int
    training_lag_ms: float
    initial_delay_ms: float
    threshold: float
    cue_magnitude: float

    def validate(self) -> None:
        if self.seed not in R01_17_DEVELOPMENT_SEEDS:
            raise ValueError("R01-17 seed is outside the fixed development namespace")
        if not 3.8 <= self.training_lag_ms <= 4.2:
            raise ValueError("R01-17 training lag left the preregistered range")
        separation = self.initial_delay_ms - self.training_lag_ms
        if not 1.5 <= separation <= 2.25:
            raise ValueError("R01-17 initial-delay separation left the preregistered range")
        if not 0.45 <= self.threshold <= 0.53:
            raise ValueError("R01-17 threshold left the preregistered range")
        if self.cue_magnitude != round(self.threshold + 0.65, 6):
            raise ValueError("R01-17 cue magnitude diverged from its fixed rule")

    @property
    def world_id(self) -> str:
        self.validate()
        return f"r01-17:development:real-delay-chain:{self.seed}"

    @property
    def identity_sha256(self) -> str:
        self.validate()
        return _digest(self.state_dict(include_identity=False))

    def state_dict(self, *, include_identity: bool = True) -> dict[str, Any]:
        result: dict[str, Any] = {
            "cue_magnitude": self.cue_magnitude,
            "exposures": R01_17_EXPOSURES,
            "formal_authority": R01_17_FORMAL_AUTHORITY,
            "held_out_authority": R01_17_HELD_OUT_AUTHORITY,
            "initial_delay_ms": self.initial_delay_ms,
            "initial_weight": R01_17_INITIAL_WEIGHT,
            "minimum_causal_shift_ms": R01_17_MIN_CAUSAL_SHIFT_MS,
            "minimum_delay_displacement_ms": R01_17_MIN_DELAY_DISPLACEMENT_MS,
            "phase": "development",
            "protocol_id": R01_17_PROTOCOL_ID,
            "route": list(R01_17_ROUTE),
            "seed": self.seed,
            "threshold": self.threshold,
            "timing_tolerance_ms": R01_17_TIMING_TOLERANCE_MS,
            "training_lag_ms": self.training_lag_ms,
            "unit_count": R01_17_UNIT_COUNT,
            "world_salt": R01_17_WORLD_SALT,
        }
        if include_identity:
            result["identity_sha256"] = self.identity_sha256
            result["world_id"] = self.world_id
        return result


def build_world_spec(seed: int) -> R0117WorldSpec:
    if seed not in R01_17_DEVELOPMENT_SEEDS:
        raise ValueError("R01-17 seed is outside the fixed development namespace")
    rng = random.Random(seed ^ 0x170117)
    training_lag = round(3.8 + rng.random() * 0.4, 6)
    offset = round(1.5 + rng.random() * 0.75, 6)
    threshold = round(0.45 + rng.random() * 0.08, 6)
    spec = R0117WorldSpec(
        seed=seed,
        training_lag_ms=training_lag,
        initial_delay_ms=round(training_lag + offset, 6),
        threshold=threshold,
        cue_magnitude=round(threshold + 0.65, 6),
    )
    spec.validate()
    return spec


def prospective_world_specs() -> tuple[R0117WorldSpec, ...]:
    rows = tuple(build_world_spec(seed) for seed in R01_17_DEVELOPMENT_SEEDS)
    if len(rows) != 5 or len({row.world_id for row in rows}) != 5:
        raise RuntimeError("R01-17 prospective world grid is not exactly five unique cells")
    if len({row.identity_sha256 for row in rows}) != 5:
        raise RuntimeError("R01-17 prospective identity hashes are not unique")
    return rows


def prospective_world_grid_hash() -> str:
    return _digest([row.state_dict() for row in prospective_world_specs()])


def _connections(field: TemporalExcitableField) -> list[dict[str, Any]]:
    return [row.state_dict() for row in connection_snapshots(field)]


def _training_pulses(spec: R0117WorldSpec, episode: int) -> tuple[Any, ...]:
    start = float(episode * 1000)
    return tuple(
        runtime_pulse(
            event_id=f"r01-17:{spec.seed}:train:{episode}:{index}",
            time_ms=start + index * spec.training_lag_ms,
            unit_id=unit_id,
            magnitude=spec.cue_magnitude,
            origin=EventOrigin.EXTERNAL,
        )
        for index, unit_id in enumerate(R01_17_ROUTE)
    )


def _rewrite_checkpoint_delays(
    checkpoint: dict[str, Any],
    delay_by_edge: dict[tuple[int, int], float],
) -> dict[str, Any]:
    value = copy.deepcopy(checkpoint)
    rows = value.get("connections")
    if not isinstance(rows, list):
        raise TypeError("R01-17 checkpoint must contain a list connection inventory")
    seen: set[tuple[int, int]] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("R01-17 checkpoint connection row must be a mapping")
        key = (int(row["source_id"]), int(row["target_id"]))
        if key not in delay_by_edge:
            raise RuntimeError("R01-17 delay reset would change topology")
        row["delay_ms"] = float(delay_by_edge[key])
        seen.add(key)
    if seen != set(delay_by_edge):
        raise RuntimeError("R01-17 delay reset omitted a registered edge")
    return value


def _probe_checkpoint(
    checkpoint: dict[str, Any],
    spec: R0117WorldSpec,
    *,
    arm: str,
) -> dict[str, Any]:
    field = TemporalExcitableField.from_state_dict(copy.deepcopy(checkpoint))
    before_hash = connection_state_hash(field)
    inventory = _connections(field)
    cue_time = 100.0
    field.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time,
            target_id=R01_17_ROUTE[0],
            current=spec.cue_magnitude,
            source_id=None,
            pulse_id=f"r01-17:{spec.seed}:{arm}:fixed-cue",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    horizon = cue_time + max(spec.initial_delay_ms, spec.training_lag_ms) * 8.0
    current = cue_time
    spikes: list[Any] = []
    while current < horizon:
        target = min(horizon, current + 0.25)
        spikes.extend(field.run_until(target))
        current = target
        if not field.state_dict().get("queue") and current > cue_time:
            break
    later = tuple(row for row in spikes if float(row.time_ms) > cue_time)
    after_hash = connection_state_hash(field)
    if after_hash != before_hash:
        raise RuntimeError("R01-17 probe mutated frozen connection state")
    return {
        "arm": arm,
        "connection_hash_after": after_hash,
        "connection_hash_before": before_hash,
        "connections": inventory,
        "generated_times_ms": [float(row.time_ms) for row in later],
        "generated_units": [int(row.unit_id) for row in later],
    }


def _acquire_world(spec: R0117WorldSpec) -> dict[str, Any]:
    spec.validate()
    edges = tuple(zip(R01_17_ROUTE, R01_17_ROUTE[1:], strict=False))
    field = build_physical_field(
        unit_count=R01_17_UNIT_COUNT,
        directed_edges=edges,
        threshold=spec.threshold,
        initial_weight=R01_17_INITIAL_WEIGHT,
        initial_delay_ms=spec.initial_delay_ms,
    )
    pre = _connections(field)
    api_hashes: set[str] = set()
    training_exposures: list[dict[str, Any]] = []
    for episode in range(R01_17_EXPOSURES):
        pulses = _training_pulses(spec, episode)
        bridge = CurrentPhysicalLearnerBridge(field)
        api_hashes.add(bridge.api.api_hash)
        connection_hash_before = connection_state_hash(field)
        observations = bridge.observe_sequence(pulses)
        connection_hash_after = connection_state_hash(field)
        training_exposures.append(
            {
                "connection_hash_after": connection_hash_after,
                "connection_hash_before": connection_hash_before,
                "connections_after": _connections(field),
                "episode": episode,
                "observations": [row.state_dict() for row in observations],
                "pulses": [pulse.as_dict() for pulse in pulses],
            }
        )
    if len(api_hashes) != 1:
        raise RuntimeError("R01-17 learner API changed inside one prospective cell")
    post = _connections(field)
    checkpoint = field.state_dict()
    pre_delay = {
        (int(row["source_id"]), int(row["target_id"])): float(row["delay_ms"]) for row in pre
    }
    fd_checkpoint = _rewrite_checkpoint_delays(checkpoint, pre_delay)
    return {
        "arms": {
            "F0": _probe_checkpoint(checkpoint, spec, arm="F0"),
            "FD": _probe_checkpoint(fd_checkpoint, spec, arm="FD"),
            "SHAM": _probe_checkpoint(checkpoint, spec, arm="SHAM"),
        },
        "learner_api_hash": next(iter(api_hashes)),
        "post_training_connections": post,
        "pre_training_connections": pre,
        "spec": spec.state_dict(),
        "training_exposures": training_exposures,
    }


def acquire_raw_suite(*, source_git_sha: str, python_runtime: str) -> dict[str, Any]:
    """Acquire the real fixed five-cell raw suite; do not call from CI/tests."""

    if len(source_git_sha) != 40 or any(c not in "0123456789abcdef" for c in source_git_sha):
        raise ValueError("R01-17 source_git_sha must be a lowercase full Git SHA")
    worlds = [_acquire_world(spec) for spec in prospective_world_specs()]
    return {
        "formal_authority": False,
        "held_out_authority": False,
        "phase": "development",
        "protocol_id": R01_17_PROTOCOL_ID,
        "python_runtime": python_runtime,
        "raw_suite_sha256": _digest(worlds),
        "source_git_sha": source_git_sha,
        "world_grid_sha256": prospective_world_grid_hash(),
        "worlds": worlds,
    }


def _edge_map(rows: list[dict[str, Any]]) -> dict[tuple[int, int], dict[str, Any]]:
    result: dict[tuple[int, int], dict[str, Any]] = {}
    for row in rows:
        key = (int(row["source_id"]), int(row["target_id"]))
        if key in result:
            raise ValueError("duplicate R01-17 connection edge")
        result[key] = row
    return result


def _first_arrivals(arm: dict[str, Any]) -> dict[int, float]:
    result: dict[int, float] = {}
    for unit, time_ms in zip(arm["generated_units"], arm["generated_times_ms"], strict=True):
        result.setdefault(int(unit), float(time_ms))
    return result


def score_raw_suite(raw: dict[str, Any]) -> dict[str, Any]:
    """Apply only the preregistered R01-17 decision rule to preserved raw rows."""

    if raw.get("protocol_id") != R01_17_PROTOCOL_ID:
        raise ValueError("R01-17 scorer received a different protocol")
    worlds = raw.get("worlds")
    if not isinstance(worlds, list) or len(worlds) != len(R01_17_DEVELOPMENT_SEEDS):
        raise ValueError("R01-17 scorer requires the complete fixed five-cell raw suite")
    if raw.get("world_grid_sha256") != prospective_world_grid_hash():
        raise ValueError("R01-17 raw suite world-grid hash drifted")
    if raw.get("raw_suite_sha256") != _digest(worlds):
        raise ValueError("R01-17 raw suite content hash mismatch")
    observed_seeds = [int(row["spec"]["seed"]) for row in worlds]
    if observed_seeds != list(R01_17_DEVELOPMENT_SEEDS):
        raise ValueError("R01-17 raw suite seed order/identity drifted")

    scored_worlds: list[dict[str, Any]] = []
    for row in worlds:
        seed = int(row["spec"]["seed"])
        if row["spec"] != build_world_spec(seed).state_dict():
            raise ValueError("R01-17 raw suite spec diverged from the frozen construction")
        pre = _edge_map(row["pre_training_connections"])
        post = _edge_map(row["post_training_connections"])
        if set(pre) != set(post):
            raise RuntimeError("R01-17 pre/post topology drifted")
        expected_edges = set(zip(R01_17_ROUTE, R01_17_ROUTE[1:], strict=False))
        if set(pre) != expected_edges:
            raise RuntimeError("R01-17 raw suite does not contain the fixed chain")

        delay_displacements = {
            f"{source}->{target}": abs(
                float(post[(source, target)]["delay_ms"]) - float(pre[(source, target)]["delay_ms"])
            )
            for source, target in sorted(expected_edges)
        }
        delay_eligible = all(
            value >= R01_17_MIN_DELAY_DISPLACEMENT_MS for value in delay_displacements.values()
        )

        arms = row["arms"]
        f0 = arms["F0"]
        fd = arms["FD"]
        sham = arms["SHAM"]
        f0_edges = _edge_map(f0["connections"])
        fd_edges = _edge_map(fd["connections"])
        sham_edges = _edge_map(sham["connections"])
        arm_binding_valid = (
            set(f0_edges) == expected_edges
            and set(fd_edges) == expected_edges
            and set(sham_edges) == expected_edges
            and all(
                float(f0_edges[key]["weight"])
                == float(fd_edges[key]["weight"])
                == float(sham_edges[key]["weight"])
                == float(post[key]["weight"])
                for key in expected_edges
            )
            and all(
                float(f0_edges[key]["delay_ms"]) == float(post[key]["delay_ms"])
                and float(sham_edges[key]["delay_ms"]) == float(post[key]["delay_ms"])
                and float(fd_edges[key]["delay_ms"]) == float(pre[key]["delay_ms"])
                for key in expected_edges
            )
        )
        expected_units = list(R01_17_ROUTE[1:])
        route_preserved = (
            list(f0["generated_units"]) == expected_units
            and list(fd["generated_units"]) == expected_units
        )
        sham_exact = (
            sham["connection_hash_before"] == f0["connection_hash_before"]
            and sham["generated_units"] == f0["generated_units"]
            and sham["generated_times_ms"] == f0["generated_times_ms"]
        )
        f0_arrivals = _first_arrivals(f0)
        fd_arrivals = _first_arrivals(fd)
        complete_arrivals = all(
            unit in f0_arrivals and unit in fd_arrivals for unit in R01_17_ROUTE[1:]
        )
        arrival_shifts = {
            str(unit): fd_arrivals[unit] - f0_arrivals[unit]
            for unit in R01_17_ROUTE[1:]
            if unit in f0_arrivals and unit in fd_arrivals
        }
        causal_timing = complete_arrivals and all(
            value >= R01_17_MIN_CAUSAL_SHIFT_MS and value > R01_17_TIMING_TOLERANCE_MS
            for value in arrival_shifts.values()
        )

        if not delay_eligible:
            disposition = "REAL_DELAY_INELIGIBLE"
        elif arm_binding_valid and route_preserved and sham_exact and causal_timing:
            disposition = "REAL_DELAY_SUPPORT_CELL"
        else:
            disposition = "REAL_DELAY_NEGATIVE_CELL"

        scored_worlds.append(
            {
                "arm_binding_valid": arm_binding_valid,
                "arrival_shifts_ms": arrival_shifts,
                "delay_displacements_ms": delay_displacements,
                "delay_eligible": delay_eligible,
                "disposition": disposition,
                "route_preserved": route_preserved,
                "seed": seed,
                "sham_exact": sham_exact,
                "world_id": row["spec"]["world_id"],
            }
        )

    dispositions = [row["disposition"] for row in scored_worlds]
    if any(value == "REAL_DELAY_INELIGIBLE" for value in dispositions):
        classification = "INSUFFICIENT_REAL_DELAY_CONSTRUCTION"
    elif all(value == "REAL_DELAY_SUPPORT_CELL" for value in dispositions):
        classification = "SUPPORTED_REAL_DELAY_CAUSAL_TIMING"
    elif all(value == "REAL_DELAY_NEGATIVE_CELL" for value in dispositions):
        classification = "UNSUPPORTED_REAL_DELAY_CAUSAL_TIMING"
    else:
        classification = "MIXED_REAL_DELAY_CAUSAL_TIMING"
    return {
        "classification": classification,
        "formal_authority": False,
        "held_out_authority": False,
        "minimum_causal_shift_ms": R01_17_MIN_CAUSAL_SHIFT_MS,
        "minimum_delay_displacement_ms": R01_17_MIN_DELAY_DISPLACEMENT_MS,
        "phase": "development",
        "protocol_id": R01_17_PROTOCOL_ID,
        "raw_suite_sha256": raw["raw_suite_sha256"],
        "score_sha256": _digest(scored_worlds),
        "scored_worlds": scored_worlds,
        "timing_tolerance_ms": R01_17_TIMING_TOLERANCE_MS,
    }


__all__ = [
    "R01_17_DEVELOPMENT_SEEDS",
    "R01_17_MIN_CAUSAL_SHIFT_MS",
    "R01_17_MIN_DELAY_DISPLACEMENT_MS",
    "R01_17_PROTOCOL_ID",
    "R01_17_TIMING_TOLERANCE_MS",
    "R0117WorldSpec",
    "acquire_raw_suite",
    "build_world_spec",
    "prospective_world_grid_hash",
    "prospective_world_specs",
    "score_raw_suite",
]
