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
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.research.rv02_rd003_online import _training_schedule  # noqa: E402
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
from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
)

CONTRACT = "docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md"
RUNNER = "scripts/run_rv02_rd004.py"
ALLOWED_STATUSES = {
    "complete",
    "incomplete_native_guard_training",
    "incomplete_native_guard_washout",
    "incomplete_native_guard_probe",
    "incomplete_integrity_failure",
    "incomplete_execution_failure",
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
    expected_modes = {"disabled", "causal", "shuffled"}
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


def verify_result(result: dict) -> None:
    if result["protocol"] != RD004_PROTOCOL:
        raise ValueError("RD004 protocol mismatch")
    if result["status"] not in ALLOWED_STATUSES:
        raise ValueError("unknown RD004 cell status")
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

    e1 = eligibility_budget(result.get("e1_eligibility_budget", []))
    es = eligibility_budget(result.get("es_eligibility_budget", []))
    if e1 != es:
        raise ValueError("RD004 E1/ES eligibility budget mismatch")
    if "eligibility_budget_hash" in result and digest(e1) != result["eligibility_budget_hash"]:
        raise ValueError("RD004 eligibility budget hash mismatch")
    disabled = result.get("learner_states", {}).get("disabled")
    if disabled is not None and disabled.get("hidden_trace_records"):
        raise ValueError("RD004 E0 retained hidden eligibility")

    snapshots = result.get("probe_snapshots")
    if result["status"] in {
        "complete",
        "incomplete_native_guard_probe",
        "incomplete_integrity_failure",
    } and snapshots is not None:
        if set(snapshots) != {"disabled", "causal", "shuffled"}:
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

    _validate_probe_inventory(result, world)
    probes = result.get("probes")
    if probes is None:
        return

    unit_count = int(result["audit"]["unit_count"])
    for mode in ("disabled", "causal", "shuffled"):
        for pair in probes[mode]:
            route = world["routes"][int(pair["route_index"])]
            natural = pair["natural"]
            cut = pair["boundary_zero"]
            if natural.get("shared_snapshot_hash") != cut.get("shared_snapshot_hash"):
                raise ValueError("RD004 natural/cut snapshot mismatch")
            if natural.get("cue_time_ms") != cut.get("cue_time_ms"):
                raise ValueError("RD004 natural/cut cue-time mismatch")
            for probe in (natural, cut):
                if probe.get("horizon_ms") != RD004_HORIZON_MS:
                    raise ValueError("RD004 probe horizon mismatch")
                if probe.get("probe_connection_hash_before") != probe.get(
                    "probe_connection_hash_after"
                ):
                    raise ValueError("RD004 probe changed connection state")
                if probe["status"] != "complete":
                    if probe["status"] != "incomplete_native_guard_probe":
                        raise ValueError("unexpected RD004 probe status")
                    continue
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
        for mode in ("disabled", "causal", "shuffled")
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
    if manifest["source_git_sha"] != git_head(source_root):
        raise ValueError("RD004 artifact source SHA does not match checked-out source")
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

    git_sha = git_head(ROOT)
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "protocol": RD004_PROTOCOL,
        "source_git_sha": git_sha,
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
