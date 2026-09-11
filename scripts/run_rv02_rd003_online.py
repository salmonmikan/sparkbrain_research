"""Run or verify the frozen RV02-RD003 exposed development matrix."""

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

from sparkbrain.research.rv02_boundary_recruitment import score_probe  # noqa: E402
from sparkbrain.research.rv02_rd003_online import (  # noqa: E402
    planned_rd003_cells,
    run_rd003_cell,
)
from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig,
    development_worlds,
    digest,
)

CONTRACT = "docs/research/RV02_RD003_ONLINE_HIDDEN_ELIGIBILITY_PREREG.md"
RUNNER = "scripts/run_rv02_rd003_online.py"


def source_inventory(root: Path) -> dict[str, str]:
    paths = [
        *sorted((root / "src" / "sparkbrain" / "research").glob("rv02*.py")),
        root / "src/sparkbrain/research/rv01/physical_plasticity.py",
        root / "src/sparkbrain/research/rv01/physical_learner_bridge.py",
        root / CONTRACT,
        root / RUNNER,
        *sorted((root / "tests").glob("test_rv02*.py")),
    ]
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def world_for_family(family: str) -> dict:
    config = ScaleStudyConfig()
    matches = [world for world in development_worlds(config) if world["family"] == family]
    if len(matches) != 1:
        raise ValueError(f"unexpected development family: {family}")
    return matches[0]


def eligibility_budget(result: dict, key: str) -> tuple[tuple[float, float, int], ...]:
    return tuple(
        (
            round(float(row["time_ms"]), 12),
            round(float(row["magnitude"]), 12),
            int(row["observed_unit_id"]),
        )
        for row in result[key]
    )


def verify_result(result: dict) -> None:
    if result["protocol"] != "rv02-rd003-online-hidden-eligibility-v1":
        raise ValueError("protocol mismatch")
    if result["formal_execution_allowed"] is not False:
        raise ValueError("formal boundary opened")
    if result["comparative_capability_claim_allowed"] is not False:
        raise ValueError("comparative claim boundary opened")
    if result["gain"] != 4.0:
        raise ValueError("RD003 gain drifted")
    if result["scientific_status"] != "not_scored_development_diagnosis":
        raise ValueError("RD003 result was scored before independent interpretation")
    if digest(tuple(result["training_schedule"])) != result["training_schedule_hash"]:
        raise ValueError("training schedule hash mismatch")
    e1 = eligibility_budget(result, "e1_eligibility_budget")
    es = eligibility_budget(result, "es_eligibility_budget")
    if e1 != es or digest(e1) != result["eligibility_budget_hash"]:
        raise ValueError("E1/ES eligibility budget mismatch")
    if result["learner_states"]["disabled"]["hidden_trace_records"]:
        raise ValueError("E0 retained hidden eligibility")

    world = world_for_family(result["family"])
    unit_count = int(result["audit"]["unit_count"])
    for mode in ("disabled", "causal", "shuffled"):
        for pair in result["probes"][mode]:
            route = world["routes"][int(pair["route_index"])]
            for name in ("natural", "boundary_zero"):
                probe = pair[name]
                if probe["status"] != "complete":
                    continue
                if probe["probe_connection_hash_before"] != probe["probe_connection_hash_after"]:
                    raise ValueError("probe changed connection state")
                expected = score_probe(probe["spikes"], route, unit_count)
                if digest(expected) != digest(probe["behavior"]):
                    raise ValueError("probe score reconstruction mismatch")


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
        raise ValueError("source inventory mismatch")
    if manifest["config"] != ScaleStudyConfig().state_dict():
        raise ValueError("configuration mismatch")
    if [tuple(row) for row in manifest["planned_cells"]] != list(planned_rd003_cells()):
        raise ValueError("planned matrix mismatch")
    if manifest["formal_execution_allowed"] is not False:
        raise ValueError("manifest formal boundary opened")

    rows = [json.loads(line) for line in raw.splitlines()]
    if [(row["family"], row["scale"]) for row in rows] != list(planned_rd003_cells()):
        raise ValueError("raw matrix identity mismatch")
    complete = 0
    for row in rows:
        if row["status"] == "complete":
            verify_result(row["result"])
            complete += 1
        elif row.get("result") is not None:
            verify_result(row["result"])
    if summary["complete_cells"] != complete:
        raise ValueError("complete cell count mismatch")
    return {
        "integrity_verified": True,
        "complete_cells": complete,
        "raw_sha256": summary["raw_sha256"],
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
        result = run_rd003_cell(ScaleStudyConfig(), world_for_family(family), int(scale_text))
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
        raise SystemExit("commit RD003 source/tests before development execution")

    git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "protocol": "rv02-rd003-online-hidden-eligibility-v1",
        "source_git_sha": git_sha,
        "source_hashes": source_inventory(ROOT),
        "config": ScaleStudyConfig().state_dict(),
        "planned_cells": planned_rd003_cells(),
        "formal_execution_allowed": False,
        "cell_timeout_seconds": 180,
        "total_timeout_seconds": 2400,
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
        for family, scale in planned_rd003_cells():
            remaining = 2400 - (time.monotonic() - started)
            identity = {"family": family, "scale": scale}
            if remaining <= 0:
                row = {**identity, "status": "not_started_total_deadline", "result": None}
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
                        timeout=min(180, remaining),
                        check=False,
                    )
                    if worker.returncode:
                        row = {
                            **identity,
                            "status": "incomplete_worker_failure",
                            "result": None,
                            "exit_code": worker.returncode,
                            "stderr": worker.stderr[-12000:],
                        }
                    else:
                        result = json.loads(worker.stdout)
                        status = (
                            "complete"
                            if result["complete"]
                            else "incomplete_probe_guard"
                        )
                        row = {
                            **identity,
                            "status": status,
                            "result": result,
                        }
                except subprocess.TimeoutExpired:
                    row = {**identity, "status": "incomplete_timeout", "result": None}
                row["wall_seconds"] = time.monotonic() - begin
            statuses.append({key: value for key, value in row.items() if key != "result"})
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    raw = staging.read_bytes()
    compressed = gzip.compress(raw, mtime=0)
    (args.output / "raw_cells.jsonl.gz").write_bytes(compressed)
    summary = {
        "statuses": statuses,
        "complete_cells": sum(row["status"] == "complete" for row in statuses),
        "formal_execution_allowed": False,
        "scientific_status": "not_scored_development_diagnosis",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n"
    )
    print(json.dumps(verify_bundle(args.output), sort_keys=True))
    return 0 if summary["complete_cells"] == len(planned_rd003_cells()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
