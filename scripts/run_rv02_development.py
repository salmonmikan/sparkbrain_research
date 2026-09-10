"""Bounded, local-only RV02 development feasibility runner; no formal mode."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.research.rv02_scale import (  # noqa: E402
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
    run_development_cell,
)


def verify_bundle(output: Path, source_root: Path = ROOT) -> dict:
    """Verify persisted evidence independently; integrity is not capability success."""
    try:
        manifest = json.loads((output / "manifest.json").read_text())
        summary = json.loads((output / "summary.json").read_text())
        raw = (output / "raw_cells.jsonl").read_bytes()
        rows = [json.loads(line) for line in raw.splitlines()]
        config = ScaleStudyConfig.from_state_dict(manifest["config"])
        if digest(manifest["config"]) != manifest["config_hash"]:
            raise ValueError("config hash mismatch")
        if hashlib.sha256(raw).hexdigest() != summary["raw_sha256"]:
            raise ValueError("raw hash mismatch")
        planned = [tuple(item) for item in manifest["planned_cells"]]
        if len(planned) != len(set(planned)) or len(rows) != len(planned):
            raise ValueError("planned/raw cardinality or uniqueness mismatch")
        worlds = development_worlds(config)
        expected_all = [
            (w["family"], scale, architecture)
            for w in worlds
            for scale in config.scales
            for architecture in ("field", "reservoir")
        ]
        if planned not in (expected_all, expected_all[:6]):
            raise ValueError("planned matrix must be complete development or smoke matrix")
        observed = [(r["family"], r["scale"], r["architecture"]) for r in rows]
        if observed != planned:
            raise ValueError("raw identity/order mismatch")
        statuses = [{key: value for key, value in row.items() if key != "result"} for row in rows]
        if summary["statuses"] != statuses:
            raise ValueError("summary statuses mismatch")
        if summary["planned_cell_count"] != len(planned):
            raise ValueError("summary planned count mismatch")
        if summary["complete_cell_count"] != sum(r["status"] == "complete" for r in rows):
            raise ValueError("summary complete count mismatch")
        for item in (manifest, summary):
            if (
                item["formal_execution_allowed"] is not False
                or item["comparative_capability_claim_allowed"] is not False
            ):
                raise ValueError("scientific boundary changed")
        for row in rows:
            if row["status"] == "complete":
                result = row["result"]
                world = next(w for w in worlds if w["family"] == row["family"])
                if digest(result["audit"]) != digest(audit_scale(config, world, row["scale"])):
                    raise ValueError("cell world/topology/resource audit mismatch")
                if result["architecture"] != row["architecture"] or result["complete"] is not True:
                    raise ValueError("completed cell result mismatch")
                if len(result["probes"]) != len(world["routes"]):
                    raise ValueError("probe cardinality mismatch")
        if not manifest["source_hashes"]:
            raise ValueError("empty source manifest")
        expected_sources = {
            str(p.relative_to(source_root)) for p in (source_root / "src").rglob("*.py")
        }
        expected_sources.add("scripts/run_rv02_development.py")
        if set(manifest["source_hashes"]) != expected_sources:
            raise ValueError("source manifest inventory mismatch")
        for relative, expected_hash in manifest["source_hashes"].items():
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("invalid source path")
            actual = hashlib.sha256((source_root / path).read_bytes()).hexdigest()
            if actual != expected_hash:
                raise ValueError(f"source hash mismatch: {relative}")
        return {
            "integrity_verified": True,
            "complete_cell_count": summary["complete_cell_count"],
            "planned_cell_count": len(planned),
            "raw_sha256": summary["raw_sha256"],
        }
    except (OSError, KeyError, TypeError, StopIteration) as error:
        raise ValueError("incomplete or malformed development bundle") from error


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--output", type=Path)
    result.add_argument("--verify", type=Path, help="verify a saved bundle without model execution")
    result.add_argument(
        "--smoke", action="store_true", help="one family, all three scales, both architectures"
    )
    result.add_argument("--cell-timeout", type=float, default=60.0)
    result.add_argument("--total-timeout", type=float, default=600.0)
    result.add_argument(
        "--worker", nargs=3, metavar=("FAMILY", "SCALE", "ARCHITECTURE"), help=argparse.SUPPRESS
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if args.verify is not None:
        print(json.dumps(verify_bundle(args.verify), sort_keys=True))
        return 0
    config = ScaleStudyConfig()
    config.validate()
    worlds = development_worlds(config)
    if args.worker:
        # Set the hard address-space bound before importing Field/reservoir modules.
        import resource

        ceiling = 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))
        family, scale, architecture = args.worker
        world = next(w for w in worlds if w["family"] == family)
        value = run_development_cell(config, world, int(scale), architecture)
        value["engineering_peak_rss_native"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        value["engineering_peak_rss_units"] = "bytes" if sys.platform == "darwin" else "KiB"
        print(json.dumps(value, sort_keys=True, allow_nan=False))
        return 0
    if args.output is None:
        raise SystemExit("--output requires an explicit fresh local directory")
    if not 0 < args.cell_timeout <= 60 or not 0 < args.total_timeout <= 600:
        raise SystemExit("timeouts must be positive, at most 60s/cell and 600s total")
    source_git_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    dirty_source = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "src", "scripts", "tests"], cwd=ROOT, text=True
    )
    if dirty_source:
        raise SystemExit("commit development source/tests before execution")
    # mkdir is an atomic no-clobber claim; partial results remain if interrupted.
    args.output.mkdir(parents=True, exist_ok=False)
    if args.smoke:
        worlds = worlds[:1]
    planned = [
        (w["family"], scale, architecture)
        for w in worlds
        for scale in config.scales
        for architecture in ("field", "reservoir")
    ]
    source_hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ROOT / "src").rglob("*.py"))
    }
    source_hashes[str(Path(__file__).relative_to(ROOT))] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    manifest = {
        "protocol": "rv02-development-feasibility-v1",
        "config": config.state_dict(),
        "source_git_sha": source_git_sha,
        "config_hash": digest(config.state_dict()),
        "planned_cells": planned,
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "source_hashes": source_hashes,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cell_timeout_seconds": args.cell_timeout,
        "total_timeout_seconds": args.total_timeout,
        "memory_limit_bytes": 1024**3,
    }
    with (args.output / "manifest.json").open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    started, statuses = time.monotonic(), []
    raw_staging = args.output / "raw_cells.jsonl.tmp"
    with raw_staging.open("x", encoding="utf-8") as stream:
        for family, scale, architecture in planned:
            remaining = args.total_timeout - (time.monotonic() - started)
            identity = {"family": family, "scale": scale, "architecture": architecture}
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
                            architecture,
                        ],
                        capture_output=True,
                        text=True,
                        timeout=min(args.cell_timeout, remaining),
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
                        status = "complete" if result["complete"] else "incomplete_event_budget"
                        row = {**identity, "status": status, "result": result}
                except subprocess.TimeoutExpired:
                    row = {**identity, "status": "incomplete_timeout"}
                row["engineering_wall_seconds"] = time.monotonic() - begin
            statuses.append({key: value for key, value in row.items() if key != "result"})
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    raw_bytes = raw_staging.read_bytes()
    raw_rows = [json.loads(line) for line in raw_bytes.splitlines()]
    if len(raw_rows) != len(planned):
        raise RuntimeError("persisted raw cell count mismatch")
    # Publish only closed, complete bytes. link fails if another writer owns the path.
    os.link(raw_staging, args.output / "raw_cells.jsonl")
    summary = {
        "statuses": statuses,
        "complete_cell_count": sum(s["status"] == "complete" for s in statuses),
        "planned_cell_count": len(planned),
        "scientific_status": "not_evaluated_development_feasibility",
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "raw_sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }
    with (args.output / "summary.json").open("x", encoding="utf-8") as stream:
        json.dump(summary, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    verify_bundle(args.output)
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "statuses"}, sort_keys=True
        )
    )
    return 0 if summary["complete_cell_count"] == len(planned) else 1


if __name__ == "__main__":
    raise SystemExit(main())
