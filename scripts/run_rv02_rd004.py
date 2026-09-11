"""Run or verify the frozen RV02-RD004 exposed development matrix.

This runner is intentionally development-only. It must be executed only from an
exact immutable RD004 source ref after CI/review; it never authorizes held-out or
formal capability and it preserves incomplete cells instead of converting them
to behavioral negatives.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.research.rv02_hidden_eligibility import (  # noqa: E402
    deterministic_hidden_permutation,
)
from sparkbrain.research.rv02_rd003_online import (  # noqa: E402
    RD003_MODES,
    _training_schedule,
)
from sparkbrain.research.rv02_rd004_online import (  # noqa: E402
    RD004_PROTOCOL,
    planned_rd004_cells,
    run_rd004_cell,
)
from sparkbrain.research.rv02_rd004_probe_clock import (  # noqa: E402
    RD004_ELIGIBILITY_TAIL_MS,
    RD004_HORIZON_MS,
    RD004_WASHOUT_MS,
    score_rd004_probe,
)
from sparkbrain.research.rv02_recruitment import PORTS  # noqa: E402
from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
)

CONTRACT = "docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md"
RUNNER = "scripts/run_rv02_rd004.py"
RD004_FREEZE_REF = "freeze/rv02-rd004-development-source"
ALLOWED_STATUSES = {
    "complete",
    "incomplete_native_guard_training",
    "incomplete_native_guard_washout",
    "incomplete_native_guard_probe",
    "incomplete_integrity_failure",
    "incomplete_execution_failure",
}
_NATIVE_GUARD_MESSAGES = {"max_events_per_run exceeded", "max_spikes_per_run exceeded"}
_SCHEDULE_FIELDS = (
    "ordinal",
    "route_index",
    "episode",
    "position",
    "unit_id",
    "time_ms",
    "event_id",
)
_UPDATE_MODES = {
    "causal_potentiation",
    "anti_causal_depression",
    "hidden_return_potentiation",
}


def source_inventory(root: Path) -> dict[str, str]:
    """Bind the runner to all transitive SparkBrain runtime sources it may execute."""

    paths = [
        *sorted((root / "src/sparkbrain/v04").glob("*.py")),
        *sorted((root / "src/sparkbrain/v06").glob("*.py")),
        *sorted((root / "src/sparkbrain/research/rv01").glob("*.py")),
        *sorted((root / "src/sparkbrain/research").glob("rv02*.py")),
        root / CONTRACT,
        root / RUNNER,
        *sorted((root / "tests").glob("test_rv02*.py")),
    ]
    unique = sorted({path.resolve() for path in paths})
    missing = [path for path in unique if not path.is_file()]
    if missing:
        raise ValueError(f"RD004 source inventory has missing paths: {missing}")
    return {
        str(path.relative_to(root.resolve())): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in unique
    }


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("RD004 verification requires an exact Git source checkout") from exc


def registered_freeze_sha(root: Path) -> str:
    """Resolve the immutable RD004 development freeze without moving/fetching refs."""

    candidates = (
        f"refs/heads/{RD004_FREEZE_REF}",
        f"refs/remotes/origin/{RD004_FREEZE_REF}",
    )
    for ref in candidates:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--verify", ref],
                cwd=root,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            continue
    raise ValueError(
        f"RD004 execution source is not registered at immutable ref {RD004_FREEZE_REF}"
    )


def require_registered_execution_source(root: Path) -> str:
    head = git_head(root)
    frozen = registered_freeze_sha(root)
    if head != frozen:
        raise ValueError(
            "RD004 execution/verification checkout does not equal the registered freeze ref"
        )
    return head


def world_for_family(family: str) -> dict:
    config = ScaleStudyConfig()
    matches = [world for world in development_worlds(config) if world["family"] == family]
    if len(matches) != 1:
        raise ValueError(f"unexpected development family: {family}")
    return matches[0]


def eligibility_budget(rows: list[dict]) -> tuple[tuple[float, float, int], ...]:
    return tuple(
        (
            round(float(row["time_ms"]), 12),
            round(float(row["magnitude"]), 12),
            int(row["observed_unit_id"]),
        )
        for row in rows
    )


def _expected_probe_indices(world: dict) -> tuple[int, ...]:
    return tuple(range(len(world["routes"])))


def _validate_probe_inventory(result: dict, world: dict) -> None:
    probes = result.get("probes")
    if probes is None:
        if result["status"] in {"complete", "incomplete_native_guard_probe"}:
            raise ValueError("RD004 probe-bearing status lacks retained probes")
        return
    expected_modes = set(RD003_MODES)
    if set(probes) != expected_modes:
        raise ValueError("RD004 probe mode inventory mismatch")
    expected_indices = _expected_probe_indices(world)
    for mode in sorted(expected_modes):
        rows = probes[mode]
        if len(rows) != len(expected_indices):
            raise ValueError(f"RD004 {mode} probe route count mismatch")
        indices = tuple(int(pair.get("route_index", -1)) for pair in rows)
        if indices != expected_indices:
            raise ValueError(f"RD004 {mode} probe route-index inventory mismatch")
        for pair in rows:
            if not isinstance(pair.get("natural"), dict) or not isinstance(
                pair.get("boundary_zero"), dict
            ):
                raise ValueError("RD004 probe pair is missing a required arm")


def _validate_hidden_budget_and_states(result: dict, world: dict, scale: int) -> None:
    states = result.get("learner_states")
    if not isinstance(states, dict) or set(states) != set(RD003_MODES):
        raise ValueError("RD004 learner-state mode inventory mismatch")

    hidden_units = tuple(
        sorted(int(unit_id) for unit_id in states["causal"].get("hidden_units", []))
    )
    expected_hidden = tuple(
        unit_id
        for unit_id in range(int(result["audit"]["unit_count"]))
        if unit_id not in PORTS
    )
    if hidden_units != expected_hidden:
        raise ValueError("RD004 hidden-unit inventory mismatch")
    visible = tuple(int(unit_id) for unit_id in states["causal"].get("visible_units", []))
    if visible != PORTS:
        raise ValueError("RD004 visible-unit inventory mismatch")

    if states["disabled"].get("eligibility_mode") != "disabled":
        raise ValueError("RD004 E0 learner mode mismatch")
    if states["causal"].get("eligibility_mode") != "causal":
        raise ValueError("RD004 E1 learner mode mismatch")
    if states["shuffled"].get("eligibility_mode") != "shuffled":
        raise ValueError("RD004 ES learner mode mismatch")
    if states["disabled"].get("hidden_trace_records"):
        raise ValueError("RD004 E0 retained hidden eligibility")

    expected_mapping = deterministic_hidden_permutation(
        hidden_units,
        namespace=f"{world['world_id']}|scale={scale}",
    )
    raw_mapping = states["shuffled"].get("shuffled_mapping")
    if not isinstance(raw_mapping, dict):
        raise ValueError("RD004 shuffled learner lost its registered permutation")
    mapping = {int(source): int(target) for source, target in raw_mapping.items()}
    if mapping != expected_mapping:
        raise ValueError("RD004 shuffled hidden-source permutation mismatch")

    e1_rows = result.get("e1_eligibility_budget")
    es_rows = result.get("es_eligibility_budget")
    if not isinstance(e1_rows, list) or not isinstance(es_rows, list):
        raise ValueError("RD004 eligibility budgets must be retained as lists")
    if states["causal"].get("hidden_trace_records") != e1_rows:
        raise ValueError("RD004 E1 learner trace ledger does not match retained budget")
    if states["shuffled"].get("hidden_trace_records") != es_rows:
        raise ValueError("RD004 ES learner trace ledger does not match retained budget")
    if len(e1_rows) != len(es_rows):
        raise ValueError("RD004 E1/ES eligibility row count mismatch")

    causal_hidden = result.get("actual_runtime_hidden_spikes", {}).get("causal")
    if not isinstance(causal_hidden, list):
        raise ValueError("RD004 causal runtime hidden-spike ledger is missing")

    hidden_events: set[tuple[int, float, float, tuple[str, ...]]] = set()
    for spike in causal_hidden:
        if not isinstance(spike, dict):
            raise ValueError("RD004 retained hidden spike is not an object")
        unit_id = int(spike["unit_id"])
        if unit_id in PORTS:
            raise ValueError("RD004 hidden-spike ledger contains a visible unit")
        hidden_events.add(
            (
                unit_id,
                round(float(spike["time_ms"]), 12),
                round(max(0.0, float(spike["potential_before_reset"])), 12),
                tuple(str(item) for item in spike.get("source_pulse_ids", [])),
            )
        )

    for e1, es in zip(e1_rows, es_rows, strict=True):
        observed = int(e1["observed_unit_id"])
        if observed != int(es["observed_unit_id"]):
            raise ValueError("RD004 E1/ES observed hidden identity budget mismatch")
        if round(float(e1["time_ms"]), 12) != round(float(es["time_ms"]), 12):
            raise ValueError("RD004 E1/ES eligibility timing mismatch")
        if round(float(e1["magnitude"]), 12) != round(float(es["magnitude"]), 12):
            raise ValueError("RD004 E1/ES eligibility magnitude mismatch")
        if tuple(e1.get("source_pulse_ids", [])) != tuple(es.get("source_pulse_ids", [])):
            raise ValueError("RD004 E1/ES eligibility causal-source budget mismatch")
        if int(e1["assigned_source_id"]) != observed:
            raise ValueError("RD004 E1 eligibility source is not the observed hidden unit")
        if int(es["assigned_source_id"]) != mapping[observed]:
            raise ValueError("RD004 ES eligibility source does not follow frozen permutation")
        event_key = (
            observed,
            round(float(e1["time_ms"]), 12),
            round(float(e1["magnitude"]), 12),
            tuple(str(item) for item in e1.get("source_pulse_ids", [])),
        )
        if event_key not in hidden_events:
            raise ValueError("RD004 eligibility trace is not backed by retained runtime hidden activity")

    if eligibility_budget(e1_rows) != eligibility_budget(es_rows):
        raise ValueError("RD004 E1/ES eligibility budget mismatch")
    if "eligibility_budget_hash" in result:
        if digest(eligibility_budget(e1_rows)) != result["eligibility_budget_hash"]:
            raise ValueError("RD004 eligibility budget hash mismatch")


def _validate_training_evidence(result: dict, expected_schedule: tuple[dict, ...]) -> None:
    rows = result.get("training_rows")
    if not isinstance(rows, list):
        raise ValueError("RD004 retained training rows are missing")
    if len(rows) > len(expected_schedule):
        raise ValueError("RD004 retained training rows exceed the registered schedule")
    if result["status"] != "incomplete_native_guard_training" and len(rows) != len(
        expected_schedule
    ):
        raise ValueError("RD004 retained training rows do not cover the full registered schedule")

    e1_flat: list[dict] = []
    es_flat: list[dict] = []
    hidden_updates: dict[str, list[dict]] = {"causal": [], "shuffled": []}
    last_edge_state: dict[tuple[str, int, int], tuple[float, float]] = {}
    hidden_trace_by_event = {
        str(row["event_id"]): row
        for mode in ("causal", "shuffled")
        for row in result["learner_states"][mode].get("hidden_trace_records", [])
    }

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError("RD004 retained training row is not an object")
        expected = expected_schedule[index]
        for field in _SCHEDULE_FIELDS:
            if row.get(field) != expected[field]:
                raise ValueError(f"RD004 retained training schedule drifted at {field}")
        e1_new = row.get("e1_new_eligibility")
        es_new = row.get("es_new_eligibility")
        if not isinstance(e1_new, list) or not isinstance(es_new, list):
            raise ValueError("RD004 training row lost eligibility creation records")
        if eligibility_budget(e1_new) != eligibility_budget(es_new):
            raise ValueError("RD004 per-step E1/ES eligibility budget mismatch")
        e1_flat.extend(e1_new)
        es_flat.extend(es_new)

        updates = row.get("updates")
        if not isinstance(updates, dict) or set(updates) != set(RD003_MODES):
            raise ValueError("RD004 training update mode inventory mismatch")
        current_event_id = str(row["event_id"])
        for mode in RD003_MODES:
            if not isinstance(updates[mode], list):
                raise ValueError("RD004 training update ledger must contain lists")
            for update in updates[mode]:
                if not isinstance(update, dict) or update.get("mode") not in _UPDATE_MODES:
                    raise ValueError("RD004 training update ledger contains an unknown update")
                source = int(update["source_id"])
                target = int(update["target_id"])
                update_mode = str(update["mode"])
                lag = float(update["lag_ms"])
                if not math.isfinite(lag) or not 0.5 <= lag <= 6.5:
                    raise ValueError("RD004 training update lag is outside the inherited window")
                if update_mode == "hidden_return_potentiation":
                    if mode == "disabled":
                        raise ValueError("RD004 E0 contains a hidden-return update")
                    if source in PORTS or target not in PORTS:
                        raise ValueError("RD004 hidden-return update has the wrong connection locus")
                    if update.get("target_event_id") != current_event_id:
                        raise ValueError("RD004 hidden-return update lacks the current external gate")
                    trace = hidden_trace_by_event.get(str(update.get("source_event_id")))
                    if trace is None or int(trace["assigned_source_id"]) != source:
                        raise ValueError("RD004 hidden-return update is not bound to eligibility")
                    if abs((float(row["time_ms"]) - float(trace["time_ms"])) - lag) > 1e-9:
                        raise ValueError("RD004 hidden-return update lag does not match retained trace")
                    hidden_updates[mode].append(update)
                else:
                    if source not in PORTS or target not in PORTS:
                        raise ValueError("RD004 ordinary external update escaped visible-visible locus")
                    if update_mode == "causal_potentiation":
                        if update.get("target_event_id") != current_event_id:
                            raise ValueError("RD004 causal update lacks the current external gate")
                    elif update.get("source_event_id") != current_event_id:
                        raise ValueError("RD004 anti-causal update lacks the current external gate")

                before = (float(update["weight_before"]), float(update["delay_before_ms"]))
                after = (float(update["weight_after"]), float(update["delay_after_ms"]))
                if not all(math.isfinite(value) for value in (*before, *after)):
                    raise ValueError("RD004 connection transition contains a non-finite value")
                edge_key = (mode, source, target)
                previous = last_edge_state.get(edge_key)
                if previous is not None and any(
                    abs(left - right) > 1e-12 for left, right in zip(previous, before, strict=True)
                ):
                    raise ValueError("RD004 connection-transition chain is discontinuous")
                last_edge_state[edge_key] = after

    e1_budget = result["e1_eligibility_budget"]
    es_budget = result["es_eligibility_budget"]
    if e1_flat != e1_budget[: len(e1_flat)] or es_flat != es_budget[: len(es_flat)]:
        raise ValueError("RD004 training eligibility rows are not a prefix of retained budget")
    if result["status"] == "incomplete_native_guard_training":
        if e1_flat != e1_budget or es_flat != es_budget:
            raise ValueError("RD004 training-guard result contains unbound tail eligibility")

    for mode in ("causal", "shuffled"):
        if result["learner_states"][mode].get("hidden_return_updates") != hidden_updates[mode]:
            raise ValueError("RD004 learner hidden-return ledger disagrees with training rows")

    initial_hashes = result.get("initial_connection_hashes")
    if not isinstance(initial_hashes, dict) or set(initial_hashes) != set(RD003_MODES):
        raise ValueError("RD004 initial connection-hash inventory mismatch")
    if len(set(initial_hashes.values())) != 1:
        raise ValueError("RD004 arms did not start from one matched connection state")
    current_hashes = result.get("trained_connection_hashes")
    if current_hashes is None:
        current_hashes = result.get("partial_connection_hashes")
    if not isinstance(current_hashes, dict) or set(current_hashes) != set(RD003_MODES):
        raise ValueError("RD004 current connection-hash inventory mismatch")


def _validate_status_evidence(result: dict) -> None:
    status = result["status"]
    complete = result.get("complete")
    if type(complete) is not bool:
        raise ValueError("RD004 complete flag must be boolean")
    if status == "complete" and not complete:
        raise ValueError("RD004 complete status has a false complete flag")
    if status != "complete" and complete:
        raise ValueError("RD004 incomplete status has a true complete flag")

    error = result.get("error")
    if status in {"incomplete_native_guard_training", "incomplete_native_guard_washout"}:
        if error not in _NATIVE_GUARD_MESSAGES:
            raise ValueError("RD004 native-guard status lacks the registered guard evidence")
        if result.get("probes") is not None:
            raise ValueError("RD004 pre-probe native guard unexpectedly retained probes")
    elif status == "incomplete_native_guard_probe":
        probes = result.get("probes")
        if not isinstance(probes, dict):
            raise ValueError("RD004 probe-guard status lacks retained probes")
        guard_rows = [
            probe
            for mode in RD003_MODES
            for pair in probes[mode]
            for probe in (pair["natural"], pair["boundary_zero"])
            if probe.get("status") == "incomplete_native_guard_probe"
        ]
        if not guard_rows:
            raise ValueError("RD004 probe-guard status contains no native-guard probe")
        if any(
            probe.get("error") not in _NATIVE_GUARD_MESSAGES
            or probe.get("metrics_available") is not False
            for probe in guard_rows
        ):
            raise ValueError("RD004 native-guard probe lost fail-closed evidence")
    elif status == "incomplete_integrity_failure":
        if type(error) is not str or not error:
            raise ValueError("RD004 integrity failure lacks retained error evidence")
    elif status == "complete" and error is not None:
        raise ValueError("RD004 complete result unexpectedly contains an error")


def verify_result(result: dict) -> None:
    if result["protocol"] != RD004_PROTOCOL:
        raise ValueError("RD004 protocol mismatch")
    if result["status"] not in ALLOWED_STATUSES - {"incomplete_execution_failure"}:
        raise ValueError("unknown RD004 retained-result status")
    if result["formal_execution_allowed"] is not False:
        raise ValueError("RD004 formal boundary opened")
    if result["comparative_capability_claim_allowed"] is not False:
        raise ValueError("RD004 comparative claim boundary opened")
    if result["gain"] != 4.0:
        raise ValueError("RD004 gain drifted")
    if result["eligibility_tail_ms"] != RD004_ELIGIBILITY_TAIL_MS:
        raise ValueError("RD004 eligibility tail drifted")
    if result["washout_ms"] != RD004_WASHOUT_MS:
        raise ValueError("RD004 washout drifted")
    if result["probe_horizon_ms"] != RD004_HORIZON_MS:
        raise ValueError("RD004 probe horizon drifted")
    if result["scientific_status"] != "not_scored_development_diagnosis":
        raise ValueError("RD004 result was scored before independent interpretation")

    family = str(result["family"])
    scale = int(result["scale"])
    world = world_for_family(family)
    if result.get("world_id") != world["world_id"]:
        raise ValueError("RD004 result world identity mismatch")
    expected_schedule = tuple(_training_schedule(world))
    if tuple(result["training_schedule"]) != expected_schedule:
        raise ValueError("RD004 result training schedule differs from registered world")
    if digest(expected_schedule) != result["training_schedule_hash"]:
        raise ValueError("RD004 training schedule hash mismatch")
    expected_audit = audit_scale(ScaleStudyConfig(), world, scale)
    if digest(result["audit"]) != digest(expected_audit):
        raise ValueError("RD004 result audit does not match registered cell")

    _validate_hidden_budget_and_states(result, world, scale)
    _validate_training_evidence(result, expected_schedule)
    _validate_status_evidence(result)

    snapshots = result.get("probe_snapshots")
    if result["status"] in {
        "complete",
        "incomplete_native_guard_probe",
        "incomplete_integrity_failure",
    }:
        if not isinstance(snapshots, dict) or set(snapshots) != set(RD003_MODES):
            raise ValueError("RD004 snapshot mode inventory mismatch")
        for mode, snapshot in snapshots.items():
            source = float(snapshot["source_clock_ms"])
            tail = float(snapshot["tail_end_ms"])
            washout = float(snapshot["washout_end_ms"])
            cue = float(snapshot["cue_time_ms"])
            if abs((tail - source) - RD004_ELIGIBILITY_TAIL_MS) > 1e-9:
                raise ValueError(f"RD004 {mode} tail interval mismatch")
            if abs((washout - tail) - RD004_WASHOUT_MS) > 1e-9:
                raise ValueError(f"RD004 {mode} washout interval mismatch")
            if abs(cue - washout) > 1e-9:
                raise ValueError(f"RD004 {mode} cue not anchored to snapshot clock")
            if not isinstance(snapshot.get("snapshot_state_hash"), str):
                raise ValueError(f"RD004 {mode} snapshot state hash is missing")
            if not isinstance(snapshot.get("connection_hash"), str):
                raise ValueError(f"RD004 {mode} snapshot connection hash is missing")
    elif snapshots is not None:
        raise ValueError("RD004 pre-snapshot failure unexpectedly retained probe snapshots")

    _validate_probe_inventory(result, world)
    probes = result.get("probes")
    if probes is None:
        return

    unit_count = int(result["audit"]["unit_count"])
    for mode in RD003_MODES:
        snapshot = snapshots[mode]
        for pair in probes[mode]:
            route = world["routes"][int(pair["route_index"])]
            natural = pair["natural"]
            cut = pair["boundary_zero"]
            expected_pair_complete = all(
                probe.get("status") == "complete" for probe in (natural, cut)
            )
            if pair.get("complete") is not expected_pair_complete:
                raise ValueError("RD004 probe-pair complete flag mismatch")
            for name, probe, expected_cut in (
                ("natural", natural, False),
                ("boundary_zero", cut, True),
            ):
                if probe.get("shared_snapshot_hash") != snapshot["snapshot_state_hash"]:
                    raise ValueError(f"RD004 {mode}/{name} probe is not bound to mode snapshot")
                if probe.get("shared_connection_hash") != snapshot["connection_hash"]:
                    raise ValueError(
                        f"RD004 {mode}/{name} probe connection identity is not snapshot-bound"
                    )
                if float(probe.get("cue_time_ms")) != float(snapshot["cue_time_ms"]):
                    raise ValueError(f"RD004 {mode}/{name} probe cue is not snapshot-bound")
                if probe.get("cut_hidden_boundary") is not expected_cut:
                    raise ValueError("RD004 natural/cut intervention identity mismatch")
                if probe.get("cue_unit") != int(route[0]):
                    raise ValueError("RD004 probe cue unit does not match registered route")
                if probe.get("horizon_ms") != RD004_HORIZON_MS:
                    raise ValueError("RD004 probe horizon mismatch")
                if probe.get("probe_connection_hash_before") != probe.get(
                    "probe_connection_hash_after"
                ):
                    raise ValueError("RD004 probe changed connection state")
                if probe["status"] != "complete":
                    if probe["status"] != "incomplete_native_guard_probe":
                        raise ValueError("unexpected RD004 probe status")
                    if probe.get("metrics_available") is not False:
                        raise ValueError("RD004 incomplete probe exposes behavioral metrics")
                    continue
                if probe.get("metrics_available") is not True:
                    raise ValueError("RD004 complete probe lacks metrics availability")
                if probe.get("observer_equivalence") is not True:
                    raise ValueError("RD004 complete probe failed observer equivalence")
                expected = score_rd004_probe(
                    probe["spikes"],
                    route,
                    unit_count,
                    cue_time_ms=float(probe["cue_time_ms"]),
                )
                if digest(expected) != digest(probe["behavior"]):
                    raise ValueError("RD004 probe score reconstruction mismatch")

    is_complete = all(
        pair[name]["status"] == "complete"
        for mode in RD003_MODES
        for pair in probes[mode]
        for name in ("natural", "boundary_zero")
    )
    if result["complete"] is not is_complete:
        raise ValueError("RD004 complete flag mismatch")
    if (result["status"] == "complete") is not is_complete:
        raise ValueError("RD004 complete status mismatch")


def verify_bundle(output: Path, source_root: Path = ROOT) -> dict:
    manifest = json.loads((output / "manifest.json").read_text())
    summary = json.loads((output / "summary.json").read_text())
    compressed = (output / "raw_cells.jsonl.gz").read_bytes()
    raw = gzip.decompress(compressed)
    if hashlib.sha256(compressed).hexdigest() != summary["compressed_sha256"]:
        raise ValueError("RD004 compressed hash mismatch")
    if hashlib.sha256(raw).hexdigest() != summary["raw_sha256"]:
        raise ValueError("RD004 raw hash mismatch")
    source_sha = require_registered_execution_source(source_root)
    if manifest["source_git_sha"] != source_sha:
        raise ValueError("RD004 artifact source SHA does not match registered frozen source")
    if manifest["source_freeze_ref"] != RD004_FREEZE_REF:
        raise ValueError("RD004 manifest freeze-ref identity mismatch")
    if manifest["source_hashes"] != source_inventory(source_root):
        raise ValueError("RD004 source inventory mismatch")
    if manifest["config"] != ScaleStudyConfig().state_dict():
        raise ValueError("RD004 configuration mismatch")
    if [tuple(row) for row in manifest["planned_cells"]] != list(planned_rd004_cells()):
        raise ValueError("RD004 planned matrix mismatch")
    if manifest["protocol"] != RD004_PROTOCOL:
        raise ValueError("RD004 manifest protocol mismatch")
    if manifest["formal_execution_allowed"] is not False:
        raise ValueError("RD004 manifest formal boundary opened")
    if summary["formal_execution_allowed"] is not False:
        raise ValueError("RD004 summary formal boundary opened")
    if summary["scientific_status"] != "not_scored_development_diagnosis":
        raise ValueError("RD004 summary scientific boundary changed")

    rows = [json.loads(line) for line in raw.splitlines()]
    planned = list(planned_rd004_cells())
    if [(row["family"], row["scale"]) for row in rows] != planned:
        raise ValueError("RD004 raw matrix identity/order mismatch")
    if len(rows) != len(planned):
        raise ValueError("RD004 raw matrix cardinality mismatch")

    counts = {status: 0 for status in ALLOWED_STATUSES}
    for row, (family, scale) in zip(rows, planned, strict=True):
        if row["status"] not in ALLOWED_STATUSES:
            raise ValueError("RD004 row status invalid")
        result = row.get("result")
        if result is not None:
            if result.get("family") != family or int(result.get("scale", -1)) != scale:
                raise ValueError("RD004 retained result is bound to the wrong matrix cell")
            expected_world = world_for_family(family)
            if result.get("world_id") != expected_world["world_id"]:
                raise ValueError("RD004 retained result world ID does not match wrapper cell")
            verify_result(result)
            if result["status"] != row["status"]:
                raise ValueError("RD004 wrapper/result status mismatch")
        elif row["status"] != "incomplete_execution_failure":
            raise ValueError("RD004 non-execution failure lost retained result")
        else:
            error_fields = (row.get("error"), row.get("stderr"), row.get("exit_code"))
            if not any(value not in (None, "") for value in error_fields):
                raise ValueError("RD004 execution failure lacks retained failure evidence")
        counts[row["status"]] += 1

    if summary["status_counts"] != counts:
        raise ValueError("RD004 summary status counts mismatch")
    if summary["attempted_cells"] != len(planned):
        raise ValueError("RD004 attempted-cell count mismatch")
    return {
        "integrity_verified": True,
        "attempted_cells": len(planned),
        "status_counts": counts,
        "raw_sha256": summary["raw_sha256"],
        "source_git_sha": manifest["source_git_sha"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--worker", nargs=2, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.verify:
        print(json.dumps(verify_bundle(args.verify), sort_keys=True))
        return 0
    if args.worker:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (1536 * 1024**2, 1536 * 1024**2))
        family, scale_text = args.worker
        result = run_rd004_cell(ScaleStudyConfig(), world_for_family(family), int(scale_text))
        result["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    if args.output is None:
        raise SystemExit("--output requires a fresh directory")
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--", "src", "scripts", "tests", CONTRACT],
        cwd=ROOT,
        text=True,
    ):
        raise SystemExit("commit RD004 source/tests before development execution")

    try:
        git_sha = require_registered_execution_source(ROOT)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    # The one-way development matrix must not create even a manifest/output path
    # until its checkout is exactly the reviewed immutable freeze source.
    if args.output.exists():
        raise SystemExit("--output requires a fresh directory")
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "protocol": RD004_PROTOCOL,
        "source_git_sha": git_sha,
        "source_freeze_ref": RD004_FREEZE_REF,
        "source_hashes": source_inventory(ROOT),
        "config": ScaleStudyConfig().state_dict(),
        "planned_cells": planned_rd004_cells(),
        "formal_execution_allowed": False,
        "cell_timeout_seconds": 240,
        "total_timeout_seconds": 3600,
        "memory_limit_bytes": 1536 * 1024**2,
        "python": sys.version,
        "platform": sys.platform,
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n"
    )

    started = time.monotonic()
    statuses: list[dict] = []
    staging = args.output / "raw_cells.jsonl.tmp"
    with staging.open("x") as stream:
        for family, scale in planned_rd004_cells():
            remaining = 3600 - (time.monotonic() - started)
            identity = {"family": family, "scale": scale}
            begin = time.monotonic()
            if remaining <= 0:
                row = {
                    **identity,
                    "status": "incomplete_execution_failure",
                    "result": None,
                    "error": "total execution deadline reached before cell start",
                }
            else:
                try:
                    worker = subprocess.run(
                        [
                            sys.executable,
                            str(Path(__file__).resolve()),
                            "--worker",
                            family,
                            str(scale),
                        ],
                        capture_output=True,
                        text=True,
                        timeout=min(240, remaining),
                        check=False,
                    )
                    if worker.returncode:
                        row = {
                            **identity,
                            "status": "incomplete_execution_failure",
                            "result": None,
                            "exit_code": worker.returncode,
                            "stderr": worker.stderr[-12000:],
                        }
                    else:
                        result = json.loads(worker.stdout)
                        row = {
                            **identity,
                            "status": result["status"],
                            "result": result,
                        }
                except subprocess.TimeoutExpired as exc:
                    row = {
                        **identity,
                        "status": "incomplete_execution_failure",
                        "result": None,
                        "error": "cell timeout",
                        "stdout": (
                            (exc.stdout or "")[-12000:]
                            if isinstance(exc.stdout, str)
                            else ""
                        ),
                        "stderr": (
                            (exc.stderr or "")[-12000:]
                            if isinstance(exc.stderr, str)
                            else ""
                        ),
                    }
            row["wall_seconds"] = time.monotonic() - begin
            statuses.append({key: value for key, value in row.items() if key != "result"})
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    raw = staging.read_bytes()
    compressed = gzip.compress(raw, mtime=0)
    (args.output / "raw_cells.jsonl.gz").write_bytes(compressed)
    status_counts = {status: 0 for status in ALLOWED_STATUSES}
    for row in statuses:
        status_counts[row["status"]] += 1
    summary = {
        "attempted_cells": len(statuses),
        "status_counts": status_counts,
        "formal_execution_allowed": False,
        "scientific_status": "not_scored_development_diagnosis",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n"
    )
    print(json.dumps(verify_bundle(args.output), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
