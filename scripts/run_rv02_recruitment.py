"""Run or verify the fixed, bounded RD001 development diagnosis locally."""
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
from sparkbrain.research.rv02_recruitment import run_recruitment_cell  # noqa: E402
from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig, audit_scale, development_worlds, digest,
)

CONTRACT = "docs/research/RV02_RD001_RECRUITMENT_CONTRACT.md"
RUNNER = "scripts/run_rv02_recruitment.py"


def source_inventory(root: Path) -> dict[str, str]:
    paths = [*sorted((root / "src").rglob("*.py")), root / RUNNER, root / CONTRACT]
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def planned_cells() -> list[tuple[str, int]]:
    config = ScaleStudyConfig()
    return [(world["family"], scale) for world in development_worlds(config)
            for scale in config.scales]


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
    for row in rows:
        if row["status"] != "complete":
            continue
        result = row["result"]
        world = next(w for w in development_worlds(ScaleStudyConfig())
                     if w["family"] == row["family"])
        if digest(result["audit"]) != digest(audit_scale(ScaleStudyConfig(), world, row["scale"])):
            raise ValueError("world/resource audit mismatch")
        if len(result["route_probes"]) != len(world["routes"]):
            raise ValueError("route cardinality mismatch")
        if len(result["training_rows"]) != result["audit"]["external_observation_count"]:
            raise ValueError("training cardinality mismatch")
        hidden_trace_count = sum(
            unit not in world["ports"] for training in result["training_rows"]
            for unit in training["external_trace_units"])
        if (hidden_trace_count != result["hidden_external_trace_count"]
                or hidden_trace_count != 0 or result["changed_hidden_edges"]):
            raise ValueError("hidden learning boundary violated")
        flattened = [result["positive_control"]]
        for index, route in enumerate(result["route_probes"]):
            if route["route_index"] != index:
                raise ValueError("probe route order mismatch")
            flattened.extend(route[k] for k in ("natural", "extended", "boundary_zero"))
            natural, extended, cut = (route[k] for k in
                                      ("natural", "extended", "boundary_zero"))
            for key, horizon, ablated in (("natural", 40., False), ("extended", 160., False),
                                          ("boundary_zero", 40., True)):
                probe = route[key]
                if (probe["horizon_ms"] != horizon or probe["cut_hidden_boundary"] is not ablated
                        or probe["cue_unit"] != world["routes"][index][0]):
                    raise ValueError("probe condition contract mismatch")
            prefix = [spike for spike in extended["spikes"] if spike["time_ms"] <= 140.]
            if prefix != natural["spikes"] or route["extended_40ms_prefix_matches"] is not True:
                raise ValueError("extended prefix mismatch")
            if route["boundary_visible_trace_equal"] != (
                    cut["visible_trace"] == natural["visible_trace"]):
                raise ValueError("boundary trace comparison mismatch")
            if route["boundary_visible_final_state_equal"] != (
                    cut["visible_final_state_hash"] == natural["visible_final_state_hash"]):
                raise ValueError("boundary state comparison mismatch")
        for probe in flattened:
            if (probe["observed_state_hash"] != probe["reference_state_hash"]
                    or probe["observer_equivalence"] is not True):
                raise ValueError("observer equivalence mismatch")
            if probe["probe_connection_hash_before"] != probe["probe_connection_hash_after"]:
                raise ValueError("probe learning detected")
            if digest(probe["visible_final_state"]) != probe["visible_final_state_hash"]:
                raise ValueError("visible state hash mismatch")
        positive = result["positive_control"]
        min_hidden = min(set(range(result["audit"]["unit_count"]))-set(world["ports"]))
        positive_pass = any(s["unit_id"] == min_hidden and s["time_ms"] == 100.
                            for s in positive["spikes"])
        if (result["positive_control_passed"] is not True or not positive_pass
                or positive["cue_unit"] != min_hidden or positive["horizon_ms"] != 40.
                or positive["cut_hidden_boundary"] is not False):
            raise ValueError("positive control failed")
        probes += len(flattened)
    if summary["complete_probes"] != probes:
        raise ValueError("probe count mismatch")
    return {"integrity_verified": True, "complete_cells": complete,
            "complete_probes": probes, "raw_sha256": summary["raw_sha256"]}


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
        result = run_recruitment_cell(config, world, int(args.worker[1]))
        result["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    if args.output is None:
        raise SystemExit("--output requires a fresh local directory")
    if subprocess.check_output(["git", "status", "--porcelain", "--", "src", "scripts", "tests"],
                               cwd=ROOT, text=True):
        raise SystemExit("commit source/tests before execution")
    git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {"protocol": "rv02-rd001-development", "source_git_sha": git_sha,
                "source_hashes": source_inventory(ROOT), "config": ScaleStudyConfig().state_dict(),
                "planned_cells": planned_cells(), "formal_execution_allowed": False,
                "cell_timeout_seconds": 60, "total_timeout_seconds": 600,
                "memory_limit_bytes": 1024**3, "python": sys.version, "platform": sys.platform}
    with (args.output / "manifest.json").open("x") as stream:
        json.dump(manifest, stream, sort_keys=True, indent=2)
        stream.write("\n")
    started, statuses, probe_count = time.monotonic(), [], 0
    staging = args.output / "raw_cells.jsonl.tmp"
    with staging.open("x") as stream:
        for family, scale in planned_cells():
            identity = {"family": family, "scale": scale}
            remaining = 600-(time.monotonic()-started)
            if remaining <= 0:
                row = {**identity, "status": "not_started_total_deadline"}
            else:
                begin = time.monotonic()
                try:
                    worker = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                             "--worker", family, str(scale)], capture_output=True,
                                            text=True, timeout=min(60, remaining), check=False)
                    if worker.returncode:
                        row = {**identity, "status": "incomplete_worker_failure",
                               "exit_code": worker.returncode, "stderr": worker.stderr[-8000:]}
                    else:
                        result = json.loads(worker.stdout)
                        row = {**identity, "status": "complete", "result": result}
                        probe_count += 3*len(result["route_probes"])+1
                except subprocess.TimeoutExpired:
                    row = {**identity, "status": "incomplete_timeout"}
                row["wall_seconds"] = time.monotonic()-begin
            statuses.append({k: v for k, v in row.items() if k != "result"})
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False)+"\n")
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
    summary = {"statuses": statuses,
               "complete_cells": sum(r["status"] == "complete" for r in statuses),
               "complete_probes": probe_count, "formal_execution_allowed": False,
               "raw_sha256": hashlib.sha256(raw).hexdigest(),
               "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
               "scientific_status": "not_evaluated_development_diagnosis"}
    with (args.output / "summary.json").open("x") as stream:
        json.dump(summary, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(verify_bundle(args.output), sort_keys=True))
    return 0 if summary["complete_cells"] == 18 else 1


if __name__ == "__main__":
    raise SystemExit(main())
