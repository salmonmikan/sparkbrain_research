"""Run or verify the fixed, bounded RD002 development diagnosis locally."""

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
from sparkbrain.research.rv02_boundary_recruitment import (  # noqa: E402
    GAINS,
    run_boundary_cell,
    score_probe,
)
from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
)

CONTRACT = "docs/research/RV02_RD002_BOUNDARY_GAIN_CONTRACT.md"
RUNNER = "scripts/run_rv02_boundary_recruitment.py"


def source_inventory(root: Path) -> dict[str, str]:
    paths = [
        *sorted((root / "src").rglob("*.py")),
        *sorted((root / "scripts").glob("*rv02*.py")),
        root / CONTRACT,
        *sorted((root / "tests").glob("test_rv02*.py")),
    ]
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def planned_cells() -> list[tuple[str, int]]:
    config = ScaleStudyConfig()
    return [
        (world["family"], scale) for world in development_worlds(config) for scale in config.scales
    ]


def verify_bundle(output: Path, source_root: Path = ROOT) -> dict:
    manifest = json.loads((output / "manifest.json").read_text())
    summary = json.loads((output / "summary.json").read_text())
    compressed = (output / "raw_cells.jsonl.gz").read_bytes()
    raw = gzip.decompress(compressed)
    if hashlib.sha256(compressed).hexdigest() != summary["compressed_sha256"]:
        raise ValueError("compressed hash mismatch")
    if hashlib.sha256(raw).hexdigest() != summary["raw_sha256"]:
        raise ValueError("raw hash mismatch")
    if manifest["source_hashes"] != source_inventory(source_root):
        raise ValueError("source manifest mismatch")
    if manifest["config"] != ScaleStudyConfig().state_dict():
        raise ValueError("config mismatch")
    if [tuple(x) for x in manifest["planned_cells"]] != planned_cells():
        raise ValueError("planned matrix mismatch")
    rows = [json.loads(line) for line in raw.splitlines()]
    if [(r["family"], r["scale"]) for r in rows] != planned_cells():
        raise ValueError("raw matrix mismatch")
    statuses = [{k: v for k, v in row.items() if k != "result"} for row in rows]
    if statuses != summary["statuses"]:
        raise ValueError("statuses mismatch")
    complete = sum(row["status"] == "complete" for row in rows)
    if summary["complete_cells"] != complete:
        raise ValueError("complete count mismatch")
    for item in (manifest, summary):
        if item["formal_execution_allowed"] is not False:
            raise ValueError("formal boundary mismatch")
    probes = 0
    attempted = 0
    for row in rows:
        if "result" not in row:
            if row["missing_probe_identities"] != expected_probes(row["family"]):
                raise ValueError("missing failure identities")
            continue
        result = row["result"]
        world = next(
            w for w in development_worlds(ScaleStudyConfig()) if w["family"] == row["family"]
        )
        if digest(result["audit"]) != digest(audit_scale(ScaleStudyConfig(), world, row["scale"])):
            raise ValueError("world/resource audit mismatch")
        pairs = result["route_probes"]
        if [(p["gain"], p["route_index"]) for p in pairs] != [
            (g, i) for g in GAINS for i in range(len(world["routes"]))
        ]:
            raise ValueError("probe identity mismatch")
        if len(result["training_rows"]) != result["audit"]["external_observation_count"]:
            raise ValueError("training cardinality mismatch")
        if result["changed_hidden_edges"] or result["hidden_external_trace_count"]:
            raise ValueError("hidden training changed")
        for pair in pairs:
            for key, cut in (("natural", False), ("boundary_zero", True)):
                attempted += 1
                probe = pair[key]
                if probe["status"] != "complete":
                    if (
                        probe["status"] != "incomplete_native_guard"
                        or probe["metrics_available"] is not False
                    ):
                        raise ValueError("invalid failure record")
                    continue
                probes += 1
                if probe["horizon_ms"] != 40.0 or probe["cut_hidden_boundary"] is not cut:
                    raise ValueError("condition mismatch")
                if probe["cue_unit"] != world["routes"][pair["route_index"]][0]:
                    raise ValueError("cue mismatch")
                if (
                    not probe["observer_equivalence"]
                    or probe["observed_state_hash"] != probe["reference_state_hash"]
                ):
                    raise ValueError("observer mismatch")
                if probe["probe_connection_hash_before"] != probe["probe_connection_hash_after"]:
                    raise ValueError("probe learning")
                if probe["actual_arrivals"] >= 4096 or probe["actual_spikes"] >= 512:
                    raise ValueError("native bound reached")
                if digest(probe["behavior"]) != digest(
                    score_probe(
                        probe["spikes"],
                        world["routes"][pair["route_index"]],
                        result["audit"]["unit_count"],
                    )
                ):
                    raise ValueError("score mismatch")
                if digest(probe["visible_final_state"]) != probe["visible_final_state_hash"]:
                    raise ValueError("visible state mismatch")
        is_complete = all(
            p[k]["status"] == "complete" for p in pairs for k in ("natural", "boundary_zero")
        )
        if (
            result["complete"] is not is_complete
            or (row["status"] == "complete") is not is_complete
        ):
            raise ValueError("completion mismatch")
    if summary["complete_probes"] != probes or summary["attempted_probes"] != attempted:
        raise ValueError("probe count mismatch")
    return {
        "integrity_verified": True,
        "complete_cells": complete,
        "complete_probes": probes,
        "attempted_probes": attempted,
        "raw_sha256": summary["raw_sha256"],
    }


def expected_probes(family: str) -> list[dict]:
    world = next(w for w in development_worlds(ScaleStudyConfig()) if w["family"] == family)
    return [
        {"gain": g, "route_index": i, "condition": c}
        for g in GAINS
        for i in range(len(world["routes"]))
        for c in ("natural", "boundary_zero")
    ]


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

        resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
        config = ScaleStudyConfig()
        world = next(w for w in development_worlds(config) if w["family"] == args.worker[0])
        result = run_boundary_cell(config, world, int(args.worker[1]))
        result["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    if args.output is None:
        raise SystemExit("--output requires a fresh local directory")
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--", "src", "scripts", "tests", CONTRACT],
        cwd=ROOT,
        text=True,
    ):
        raise SystemExit("commit source/tests before execution")
    git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "protocol": "rv02-rd002-development",
        "source_git_sha": git_sha,
        "source_hashes": source_inventory(ROOT),
        "config": ScaleStudyConfig().state_dict(),
        "planned_cells": planned_cells(),
        "formal_execution_allowed": False,
        "cell_timeout_seconds": 60,
        "total_timeout_seconds": 600,
        "memory_limit_bytes": 1024**3,
        "python": sys.version,
        "platform": sys.platform,
    }
    with (args.output / "manifest.json").open("x") as stream:
        json.dump(manifest, stream, sort_keys=True, indent=2)
        stream.write("\n")
    started, statuses, probe_count, attempted_count = time.monotonic(), [], 0, 0
    staging = args.output / "raw_cells.jsonl.tmp"
    with staging.open("x") as stream:
        for family, scale in planned_cells():
            identity = {"family": family, "scale": scale}
            remaining = 600 - (time.monotonic() - started)
            if remaining <= 0:
                row = {**identity, "status": "not_started_total_deadline"}
            else:
                begin = time.monotonic()
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
                        timeout=min(60, remaining),
                        check=False,
                    )
                    if worker.returncode:
                        row = {
                            **identity,
                            "status": "incomplete_worker_failure",
                            "exit_code": worker.returncode,
                            "stderr": worker.stderr[-8000:],
                        }
                    else:
                        result = json.loads(worker.stdout)
                        row = {
                            **identity,
                            "status": "complete"
                            if result["complete"]
                            else "incomplete_native_guard",
                            "result": result,
                        }
                        attempted_count += 2 * len(result["route_probes"])
                        probe_count += sum(
                            p[k]["status"] == "complete"
                            for p in result["route_probes"]
                            for k in ("natural", "boundary_zero")
                        )
                except subprocess.TimeoutExpired:
                    row = {**identity, "status": "incomplete_timeout"}
                row["wall_seconds"] = time.monotonic() - begin
            if "result" not in row:
                row["missing_probe_identities"] = expected_probes(family)
                row["metrics_available"] = False
            statuses.append({k: v for k, v in row.items() if k != "result"})
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    raw = staging.read_bytes()
    compressed = gzip.compress(raw, mtime=0)
    gzip_staging = args.output / "raw_cells.jsonl.gz.tmp"
    with gzip_staging.open("xb") as stream:
        stream.write(compressed)
        stream.flush()
        os.fsync(stream.fileno())
    os.link(gzip_staging, args.output / "raw_cells.jsonl.gz")
    summary = {
        "statuses": statuses,
        "complete_cells": sum(r["status"] == "complete" for r in statuses),
        "complete_probes": probe_count,
        "attempted_probes": attempted_count,
        "formal_execution_allowed": False,
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "scientific_status": "not_evaluated_development_diagnosis",
    }
    with (args.output / "summary.json").open("x") as stream:
        json.dump(summary, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(verify_bundle(args.output), sort_keys=True))
    return 0 if summary["complete_cells"] == 18 else 1


if __name__ == "__main__":
    raise SystemExit(main())
