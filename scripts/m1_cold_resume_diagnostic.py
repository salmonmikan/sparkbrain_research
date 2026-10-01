#!/usr/bin/env python3
"""Bounded, non-evidentiary M1 cold-process checkpoint diagnostic.

The frozen protocol is deliberately separate from production runtime and from
PR164's same-process long-run robustness acceptance tests.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/m1_cold_resume_diagnostic_v2.json"


def canonical(value: Any) -> bytes:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return (text + "\n").encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(value))
        stream.flush()
        os.fsync(stream.fileno())


def inventory(path: Path) -> dict[str, str]:
    if not path.is_dir():
        raise FileNotFoundError(f"checkpoint directory missing: {path}")
    return {str(p.relative_to(path)): digest(p.read_bytes())
            for p in sorted(path.rglob("*")) if p.is_file()}


def compare_directories(left: Path, right: Path) -> dict[str, Any]:
    """Compare actual bytes, with digests only as concise retained provenance."""
    a, b = inventory(left), inventory(right)
    paths = sorted(set(a) | set(b))
    changed = [p for p in paths if p not in a or p not in b
               or (left / p).read_bytes() != (right / p).read_bytes()]
    return {"equal": not changed, "changed_files": changed,
            "left_files": a, "right_files": b}


def enforce_disk(root: Path, limit: int) -> None:
    size = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
    if size > limit:
        raise RuntimeError(f"retained-output cap exceeded: {size} > {limit}")


def load_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def row_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row[key] for key in ("step", "cycle", "inspect_hash")}


def compare_rows(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> dict[str, Any]:
    if len(left) != len(right):
        return {"equal": False, "reason": "row_count", "left": len(left), "right": len(right)}
    for index, (a, b) in enumerate(zip(left, right, strict=True)):
        if canonical(row_signature(a)) != canonical(row_signature(b)):
            return {"equal": False, "reason": "row_mismatch", "index": index,
                    "left": a, "right": b}
    return {"equal": True, "rows": len(left)}


def exact_or_fail(left: Path, right: Path, failure: Path) -> dict[str, Any]:
    comparison = compare_directories(left, right)
    if not comparison["equal"]:
        write_json(failure / "comparison.json", comparison)
        shutil.copytree(left, failure / "left")
        shutil.copytree(right, failure / "right")
        raise AssertionError(f"serialized state mismatch: {comparison['changed_files']}")
    return comparison


def record_row(stream: Any, row: dict[str, Any]) -> None:
    stream.write(canonical(row))
    stream.flush()
    os.fsync(stream.fileno())


def failure_category(status: dict[str, Any], error_path: Path) -> str | None:
    if status["returncode"] == 0 and not status["timed_out"]:
        return None
    if status["timed_out"]:
        return "worker_timeout"
    if error_path.is_file():
        error = json.loads(error_path.read_bytes())
        message = error.get("error", "")
        if message.startswith("serialized state mismatch"):
            return "serialized_byte_mismatch"
        if message.startswith("future transition mismatch"):
            return "future_transition_mismatch"
        if message.startswith("save changed inspect"):
            return "save_observer_effect"
    return "incomplete_resource_worker_or_runner"


def dependency_versions() -> dict[str, str | None]:
    versions = {}
    for name in ("jsonschema", "numpy", "torch"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def runtime_imports() -> tuple[Any, Any]:
    # Source/config freeze and STARTED precede this import in the worker.
    sys.path.insert(0, str(ROOT / "src"))
    from sparkbrain.system_build import IntegratedM1CheckpointManager, IntegratedM1Session
    return IntegratedM1CheckpointManager, IntegratedM1Session


def worker(args: argparse.Namespace, protocol: dict[str, Any]) -> None:
    out = args.output
    out.mkdir(parents=True, exist_ok=False)
    args.output_created = True
    write_json(out / "STARTED.json", {
        "mode": args.mode, "cut": args.cut, "hashseed": os.environ.get("PYTHONHASHSEED"),
        "protocol_sha256": digest(PROTOCOL.read_bytes()),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "pid": os.getpid(), "parent_pid": os.getppid(),
        "reference_timeline": "observed" if args.mode in {"restore", "secondary"} else None,
    })
    budget = protocol["budget"]
    resource.setrlimit(resource.RLIMIT_AS, (budget["max_address_space_bytes_per_worker"],) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (budget["max_cpu_seconds_per_worker"],) * 2)
    manager, session_class = runtime_imports()
    if args.mode == "restore" or args.mode == "secondary":
        session = manager.load(args.reference / "checkpoints" / f"step-{args.cut:03d}")
    else:
        session = session_class()
    write_json(out / "config.json", {
        "predictive": session.pilot.predictive.config.as_dict(),
        "reference_brain": asdict(session.pilot.predictive.reference_brain.config),
        "scope": session.pilot.scoped.config.as_dict(),
    })
    if session.pilot.predictive.reference_brain.config.random_seed != protocol["model_seed"]:
        raise RuntimeError("runtime seed differs from frozen protocol")

    def snapshot(step: int) -> tuple[Path, dict[str, str]]:
        target = out / "checkpoints" / f"step-{step:03d}"
        before = session.state_hash()
        manager.save(session, target)
        if session.state_hash() != before:
            raise AssertionError("save changed inspect/state hash")
        enforce_disk(out.parent, budget["max_output_bytes"])
        return target, inventory(target)

    if args.mode == "secondary":
        quiet, _ = snapshot(args.cut)
        before = session.state_hash()
        try:
            clone = copy.deepcopy(session)
            deepcopy_result = {"supported": True,
                               "inspect_equal": clone.inspect() == session.inspect()}
        except Exception as exc:
            deepcopy_result = {"supported": False, "error_type": type(exc).__name__,
                               "error": str(exc)}
        if session.state_hash() != before:
            raise AssertionError("deepcopy attempt changed original state")
        after_copy = out / "after-deepcopy"
        manager.save(session, after_copy)
        exact_or_fail(quiet, after_copy, out / "deepcopy-original-mismatch")
        observation = session.world.next_observation()
        action = session.pilot.observe(observation)
        pending = out / "pending"
        manager.save(session, pending)
        restored = manager.load(pending)
        roundtrip = out / "pending-roundtrip"
        manager.save(restored, roundtrip)
        pending_comparison = exact_or_fail(pending, roundtrip, out / "pending-roundtrip-mismatch")
        try:
            unexpected_cycle = restored.cycle().as_dict()
            cycle_result = {"rejected": False, "committed_cycles": 1,
                            "unexpected_cycle": unexpected_cycle}
        except Exception as exc:
            cycle_result = {"rejected": True, "committed_cycles": 0,
                            "error_type": type(exc).__name__, "error": str(exc)}
        after = out / "pending-after-cycle"
        manager.save(restored, after)
        no_write = compare_directories(roundtrip, after)
        write_json(out / "secondary.json", {
            "deepcopy": deepcopy_result,
            "pending_observation": observation.as_dict(), "pending_action": action.as_dict(),
            "pending_roundtrip": pending_comparison, "automatic_cycle": cycle_result,
            "automatic_cycle_no_write": no_write,
            "claim_boundary": "API boundary only, separate from quiet checkpoint continuation",
        })
        enforce_disk(out.parent, budget["max_output_bytes"])
        return

    start = args.cut if args.mode == "restore" else 0
    reference_rows = load_rows(args.reference / "cycles.jsonl") if args.mode == "restore" else []
    if args.mode != "baseline":
        initial, _ = snapshot(start)
        if args.mode == "restore":
            exact_or_fail(args.reference / "checkpoints" / f"step-{start:03d}", initial,
                          out / "initial-mismatch")
    with (out / "cycles.jsonl").open("xb") as stream:
        for step in range(start + 1, protocol["horizon"] + 1):
            cycle = session.cycle().as_dict()
            row = {"step": step, "cycle": cycle, "inspect_hash": session.state_hash()}
            # Preserve transition outputs before comparisons or the next transition.
            record_row(stream, row)
            if args.mode == "restore":
                expected = reference_rows[step - 1]
                if canonical(row_signature(row)) != canonical(row_signature(expected)):
                    write_json(out / "transition-mismatch.json", {"left": expected, "right": row})
                    manager.save(session, out / "transition-mismatch-checkpoint")
                    raise AssertionError(f"future transition mismatch at step {step}")
            if args.mode != "baseline" or step == protocol["horizon"]:
                saved, files = snapshot(step)
                write_json(out / "file-records" / f"step-{step:03d}.json", files)
                if args.mode == "restore":
                    exact_or_fail(args.reference / "checkpoints" / f"step-{step:03d}", saved,
                                  out / f"serialized-mismatch-{step:03d}")
                    # All bytes were compared. Keep cut/final payloads and hashes for
                    # intermediate matches; preserve complete payloads on any failure.
                    if step != protocol["horizon"]:
                        shutil.rmtree(saved)
    write_json(out / "COMPLETED.json", {"cycles": protocol["horizon"] - start,
                                       "status": "completed"})


def run(args: argparse.Namespace, protocol: dict[str, Any]) -> int:
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    args.output_created = True
    started = time.monotonic()
    source_files = {str(p.relative_to(ROOT)): digest(p.read_bytes())
                    for p in sorted((ROOT / "src" / "sparkbrain").rglob("*.py"))}
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    changes = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    if changes:
        raise RuntimeError("runner requires clean tracked/untracked source workspace")
    subprocess.run(["git", "diff", "--exit-code", protocol["runtime_source_commit"],
                    "--", "src", "schemas"],
                   cwd=ROOT, check=True, capture_output=True)
    write_json(out / "STARTED.json", {
        "protocol": protocol, "protocol_sha256": digest(PROTOCOL.read_bytes()),
        "source_commit": head, "runtime_source_files_sha256": source_files,
        "schema_assets_sha256": inventory(ROOT / "schemas"),
        "dependency_versions": dependency_versions(),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "scientific_credit": 0,
    })
    shutil.copyfile(PROTOCOL, out / "protocol.json")
    workers: list[dict[str, Any]] = []

    def launch(name: str, mode: str, seed: int, cut: int = 0) -> bool:
        remaining = protocol["budget"]["total_timeout_seconds"] - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError("overall frozen wall deadline reached")
        command = [sys.executable, str(Path(__file__).resolve()), "--mode", mode,
                   "--output", str(out / name), "--cut", str(cut)]
        if mode in {"restore", "secondary"}:
            command += ["--reference", str(out / "observed")]
        environment = {**os.environ, "PYTHONHASHSEED": str(seed),
                       "PYTHONPATH": str(ROOT / "src"), "OMP_NUM_THREADS": "1",
                       "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
        begin = time.monotonic()
        with (out / f"{name}.stdout").open("xb") as stdout, \
                (out / f"{name}.stderr").open("xb") as stderr:
            try:
                result = subprocess.run(command, cwd=ROOT, env=environment, stdout=stdout,
                                        stderr=stderr, timeout=min(
                                            protocol["budget"]["worker_timeout_seconds"],
                                            remaining),
                                        check=False)
                status = {"returncode": result.returncode, "timed_out": False}
            except subprocess.TimeoutExpired:
                status = {"returncode": None, "timed_out": True}
        row = {"name": name, "mode": mode, "cut": cut, "hashseed": seed,
               "elapsed_seconds": time.monotonic() - begin, **status,
               "failure_category": failure_category(status, out / name / "ERROR.json")}
        workers.append(row)
        write_json(out / "worker-status" / f"{name}.json", row)
        enforce_disk(out, protocol["budget"]["max_output_bytes"])
        return status["returncode"] == 0 and not status["timed_out"]

    complete = launch("baseline", "baseline", protocol["baseline_hashseed"])
    if complete:
        complete = launch("observed", "observed", protocol["observed_hashseed"])
    comparisons: dict[str, Any] = {}
    if complete:
        comparisons["observer_rows"] = compare_rows(load_rows(out / "baseline/cycles.jsonl"),
                                                    load_rows(out / "observed/cycles.jsonl"))
        final = f"checkpoints/step-{protocol['horizon']:03d}"
        comparisons["observer_final_bytes"] = compare_directories(out / "baseline" / final,
                                                                   out / "observed" / final)
        write_json(out / "observer-comparisons.json", comparisons)
        complete = all(item["equal"] for item in comparisons.values())
    if complete:
        for seed in protocol["restore_hashseeds"]:
            for cut in protocol["cutpoints"]:
                ok = launch(f"restore-{seed}-{cut}", "restore", seed, cut)
                complete = ok and complete
        secondary_ok = launch("secondary", "secondary", protocol["baseline_hashseed"], 7)
    else:
        secondary_ok = False
    actual = sum(len(load_rows(p)) for p in out.glob("*/cycles.jsonl"))
    secondary_path = out / "secondary/secondary.json"
    secondary_commits = (json.loads(secondary_path.read_bytes())["automatic_cycle"]
                         ["committed_cycles"] if secondary_path.exists() else None)
    failures = [{"worker": row["name"], "category": row["failure_category"]}
                for row in workers if row["mode"] != "secondary" and row["failure_category"]]
    for name, comparison in comparisons.items():
        if not comparison["equal"]:
            failures.append({"worker": "observer_control", "category": name + "_mismatch"})
    summary = {"primary_status": "pass" if complete else "not_pass",
               "primary_failures": failures,
               "expected_committed_cycles": protocol["expected_committed_cycles"],
               "recorded_committed_cycles": actual, "secondary_completed": secondary_ok,
               "secondary_actual_committed_cycles": secondary_commits,
               "worker_count": len(workers), "scientific_credit": 0,
               "claim_boundary": protocol["claim_ceiling"]}
    if complete and actual != protocol["expected_committed_cycles"]:
        summary["primary_status"] = "failed_count_integrity"
    write_json(out / "summary.json", summary)
    write_json(out / "inventory.json", inventory(out))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["primary_status"] == "pass" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("run", "baseline", "observed", "restore", "secondary"),
                        default="run")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--cut", type=int, default=0)
    args = parser.parse_args()
    args.output_created = False
    protocol = json.loads(PROTOCOL.read_bytes())
    if args.mode == "run":
        try:
            return run(args, protocol)
        except Exception as exc:
            if args.output_created and not (args.output / "RUN_ERROR.json").exists():
                write_json(args.output / "RUN_ERROR.json", {
                    "status": "incomplete_infrastructure_or_runner",
                    "type": type(exc).__name__, "error": str(exc),
                    "traceback": traceback.format_exc(),
                })
            raise
    try:
        worker(args, protocol)
        return 0
    except Exception as exc:
        if args.output_created and not (args.output / "ERROR.json").exists():
            write_json(args.output / "ERROR.json", {"type": type(exc).__name__, "error": str(exc),
                                                   "traceback": traceback.format_exc()})
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
