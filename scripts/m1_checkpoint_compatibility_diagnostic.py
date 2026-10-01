#!/usr/bin/env python3
"""Run the frozen zero-transition M1 file-loader compatibility diagnostic."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import importlib.util
import inspect
import json
import os
import selectors
import shutil
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

try:
    import resource
except ImportError:
    resource = None

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/m1_checkpoint_compatibility_v1.json"
PROTOCOL_SHA256 = "0889e1984865a93c4663f9ca5bd6e29d2ccdd97cf523ceb62f80ce768ac84c14"
INPUTS = ROOT / "protocols/m1_checkpoint_compatibility_inputs_v1.json"
INPUTS_SHA256 = "974850e46c8e8e472b03ff341e821087481f9efe47f3138646f7147501d77100"
_BUDGET: tuple[Path, int, float] | None = None
ERRORS = {
    "C03": "unsupported M1 checkpoint identity",
    "C05": "unsupported pilot checkpoint schema or build id",
    "C06": "unsupported direct checkpoint schema",
    "C07": "unsupported BUILD-SB-002 checkpoint identity",
    "C08": "unsupported M1 compositor state identity",
    "C09": "pilot config has unexpected fields",
    "C10": "router config does not match checkpoint config",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class BudgetExceeded(RuntimeError):
    pass


class ObservationFailure(RuntimeError):
    pass


def retained_bytes(root: Path) -> int:
    return sum(p.stat().st_size for p in root.rglob("*") if p.is_file())


def guard(extra_bytes: int = 0) -> None:
    if _BUDGET is None:
        return
    root, maximum, deadline = _BUDGET
    if time.monotonic() >= deadline:
        raise BudgetExceeded("overall deadline reached; no further runtime work")
    if retained_bytes(root) + extra_bytes > maximum:
        raise BudgetExceeded("retained-output admission/checkpoint threshold exceeded")


def write_json(path: Path, value: Any, *, emergency: bool = False) -> None:
    raw = canonical(value) + b"\n"
    if emergency:
        if len(raw) > 256 * 1024:
            raise ValueError("emergency metadata exceeds 256KiB allowance")
    else:
        guard(len(raw))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if not emergency:
        guard()


def append_jsonl(path: Path, value: Any) -> None:
    raw = canonical(value) + b"\n"
    guard(len(raw))
    with path.open("ab") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    guard()


def replace_owned_json(path: Path, value: Any) -> None:
    raw = canonical(value) + b"\n"
    guard(max(0, len(raw) - path.stat().st_size))
    path.write_bytes(raw)
    guard()


def copy_input(source: Path, destination: Path) -> None:
    guard(retained_bytes(source))
    shutil.copytree(source, destination)
    guard()


def inventory(root: Path) -> dict[str, str]:
    if not root.is_dir():
        raise FileNotFoundError(root)
    paths = sorted(root.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("diagnostic inputs must not contain symbolic links")
    return {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in paths if p.is_file()}


def enforce_output(root: Path, maximum: int) -> None:
    size = retained_bytes(root)
    if size > maximum:
        raise BudgetExceeded(f"retained-output cap exceeded: {size} > {maximum}")


def load_protocol() -> dict[str, Any]:
    raw = PROTOCOL.read_bytes()
    if sha(raw) != PROTOCOL_SHA256:
        raise ValueError("frozen protocol digest mismatch")
    return json.loads(raw)


def load_inputs() -> dict[str, Any]:
    raw = INPUTS.read_bytes()
    if sha(raw) != INPUTS_SHA256:
        raise ValueError("frozen input manifest digest mismatch")
    value = json.loads(raw)
    if value["protocol_sha256"] != PROTOCOL_SHA256:
        raise ValueError("input/protocol binding mismatch")
    return value


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def preflight(source_commit: str, protocol: dict[str, Any]) -> dict[str, Any]:
    if len(source_commit) != 40 or git("rev-parse", "HEAD") != source_commit:
        raise ValueError("execution source commit must equal exact checked-out HEAD")
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("diagnostic requires a clean committed source tree")
    if git("diff", "--name-only", protocol["source_commit"], "HEAD", "--",
           "src/sparkbrain", "schemas"):
        raise ValueError("runtime/schema tree differs from frozen baseline")
    for path, expected in protocol["source_files_sha256"].items():
        if sha((ROOT / path).read_bytes()) != expected:
            raise ValueError(f"frozen runtime source mismatch: {path}")
    versions = {}
    for name in ("jsonschema", "numpy", "torch"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return {"source_commit": source_commit, "source_tree": git("rev-parse", "HEAD^{tree}"),
            "runtime_baseline_commit": protocol["source_commit"],
            "runner_sha256": sha(Path(__file__).read_bytes()),
            "protocol_sha256": sha(PROTOCOL.read_bytes()),
            "inputs_sha256": sha(INPUTS.read_bytes()),
            "runtime_source_files_sha256": {
                p: sha((ROOT / p).read_bytes())
                for p in git("ls-files", "src/sparkbrain").splitlines()},
            "schema_assets_sha256": {
                p: sha((ROOT / p).read_bytes()) for p in git("ls-files", "schemas").splitlines()},
            "python": sys.version, "executable": sys.executable,
            "dependency_versions": versions, "scientific_credit": 0,
            "command": sys.argv}


def apply_limits(protocol: dict[str, Any]) -> None:
    if resource is None:
        raise RuntimeError("bounded execution requires POSIX resource limits")
    budget = protocol["budget"]
    resource.setrlimit(resource.RLIMIT_AS, (budget["max_address_space_bytes"],) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (budget["max_cpu_seconds_per_process"],) * 2)


def runtime_imports() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "src"))
    from sparkbrain.system_build import (
        CausalScopeRevisionPilot,
        CausalScopeRouter,
        DeterministicM1World,
        IntegratedM1CheckpointManager,
        IntegratedM1Pilot,
        IntegratedM1Session,
        PilotCheckpointManager,
        PilotConfig,
        PredictiveRevisionPilot,
        ScopeRevisionCheckpointManager,
        ScopeRevisionConfig,
    )
    from sparkbrain.v032 import DirectCheckpointManager
    return {cls.__name__: cls for cls in (
        CausalScopeRevisionPilot, CausalScopeRouter, DeterministicM1World,
        IntegratedM1CheckpointManager, IntegratedM1Pilot, IntegratedM1Session,
        PilotCheckpointManager, PilotConfig, PredictiveRevisionPilot,
        ScopeRevisionCheckpointManager, ScopeRevisionConfig, DirectCheckpointManager,
    )}


def targets(runtime: dict[str, Any]) -> list[tuple[str, type[Any], str]]:
    pairs = [
        ("integrated_load", "IntegratedM1CheckpointManager", "load"),
        ("predictive_load", "PilotCheckpointManager", "load"),
        ("direct_load", "DirectCheckpointManager", "load"),
        ("direct_reconstruct", "DirectCheckpointManager", "_load_bytes"),
        ("scope_load", "ScopeRevisionCheckpointManager", "load"),
        ("predictive_restore", "PredictiveRevisionPilot", "_from_checkpoint_payload"),
        ("scope_restore", "CausalScopeRevisionPilot", "_from_checkpoint_payload"),
        ("compositor_restore", "IntegratedM1Pilot", "_restore_own_payload"),
        ("world_restore", "DeterministicM1World", "from_state_dict"),
        ("session_construct", "IntegratedM1Session", "__init__"),
        ("compositor_construct", "IntegratedM1Pilot", "__init__"),
        ("predictive_construct", "PredictiveRevisionPilot", "__init__"),
        ("scope_construct", "CausalScopeRevisionPilot", "__init__"),
        ("router_restore", "CausalScopeRouter", "from_state_dict"),
        ("router_construct", "CausalScopeRouter", "__init__"),
    ]
    return [(label, runtime[owner], method) for label, owner, method in pairs]


@contextlib.contextmanager
def milestones(selected: list[tuple[str, type[Any], str]], events: list[dict[str, Any]],
               phase: list[str], sink: Any = None,
               measurement_errors: list[dict[str, Any]] | None = None):
    originals = []
    depth = 0
    errors = measurement_errors if measurement_errors is not None else []

    def record(value: dict[str, Any]) -> bool:
        events.append(value)
        if errors:
            return False
        try:
            if sink is not None:
                sink(value)
        except Exception as exc:
            errors.append({"at_event": value, "error_type": type(exc).__name__, "error": str(exc)})
            return False
        return True

    def wrap(label: str, function: Any):
        def delegated(*args: Any, **kwargs: Any) -> Any:
            nonlocal depth
            # Intent is not a confirmed invocation. Stop before admitting a new
            # top-level call, but never replace an in-flight method's own outcome.
            if depth == 0 and errors:
                raise ObservationFailure("measurement failed before next admitted call")
            recorded = record({"phase": phase[0], "name": label, "event": "call_intent"})
            if depth == 0 and not recorded:
                raise ObservationFailure("measurement failed before delegate invocation")
            depth += 1
            try:
                try:
                    result = function(*args, **kwargs)
                except BaseException as exc:
                    record({"phase": phase[0], "name": label, "event": "error",
                            "error_type": type(exc).__name__, "error": str(exc)})
                    raise
                record({"phase": phase[0], "name": label, "event": "return"})
                return result
            finally:
                depth -= 1
        return delegated

    try:
        for label, owner, method in selected:
            raw = inspect.getattr_static(owner, method)
            originals.append((owner, method, raw))
            if isinstance(raw, (staticmethod, classmethod)):
                replacement = type(raw)(wrap(label, raw.__func__))
            else:
                replacement = wrap(label, raw)
            setattr(owner, method, replacement)
        yield
    finally:
        for owner, method, raw in reversed(originals):
            setattr(owner, method, raw)


def event_count(events: list[dict[str, Any]], name: str, phase: str | None = None) -> int:
    """Count completed delegate calls; interrupted intents remain explicitly unknown."""
    return sum(row["name"] == name and row["event"] in {"return", "error"}
               and (phase is None or row["phase"] == phase) for row in events)


def mutate_input(root: Path, case: dict[str, Any]) -> dict[str, Any]:
    before = inventory(root)
    path = case["mutation_path"]
    if path == "none":
        return {"before": before, "after": before, "modified_files": []}
    relative, suffix = path.split(".json/", 1)
    relative += ".json"
    target = root / relative
    data = json.loads(target.read_bytes())
    owner = data
    keys = suffix.split("/")
    for key in keys[:-1]:
        owner = owner[key]
    if case["mutation_value"] == "DELETE":
        del owner[keys[-1]]
    else:
        owner[keys[-1]] = case["mutation_value"]
    if case["case_id"] == "C06":
        data["payload_hash"] = sha(canonical({k: v for k, v in data.items()
                                              if k != "payload_hash"}))
    if case["case_id"] in {"C07", "C10"}:
        data["payload_sha256"] = sha(canonical(data["payload"]))
    replace_owned_json(target, data)
    if relative != "manifest.json":
        manifest_path = root / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["files"][relative] = sha(target.read_bytes())
        replace_owned_json(manifest_path, manifest)
    after = inventory(root)
    return {"before": before, "after": after,
            "modified_files": [name for name in before if before[name] != after[name]],
            "mutation_path": path, "mutation_value": case["mutation_value"]}


def disposition(case_id: str, primary: dict[str, Any], saveback: dict[str, Any]) -> str:
    if not primary["returned"] and primary.get("error_type") not in {"ValueError", "TypeError"}:
        return "incomplete_load_infrastructure"
    if case_id == "C04":
        if primary["returned"]:
            return "observed_alias_acceptance"
        if primary.get("error_type") == "ValueError" and primary.get("error") == ERRORS["C03"]:
            return "observed_alias_rejection"
        return "unexpected_load_exception"
    if case_id in ERRORS:
        if primary["returned"]:
            return "unexpected_acceptance"
        if primary["error_type"] == "ValueError" and primary["error"] == ERRORS[case_id]:
            return "expected_semantic_rejection"
        return "unexpected_load_exception"
    if not primary["returned"]:
        return "unexpected_control_rejection"
    if saveback.get("status") != "completed":
        return "accepted_control_saveback_incomplete"
    return "accepted_control_equal" if saveback["equal"] else "accepted_control_byte_difference"


def mark_measurement(result: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    if errors:
        result["status"] = "incomplete_instrumentation"
        result["measurement_errors"] = errors


def worker(args: argparse.Namespace, protocol: dict[str, Any]) -> None:
    global _BUDGET
    args.output.mkdir(parents=True, exist_ok=False)
    args.output_created = True
    apply_limits(protocol)
    _BUDGET = (args.root, protocol["budget"]["max_retained_bytes"], args.deadline)
    guard()
    frozen_inputs = load_inputs()
    actual_source = preflight(args.source_commit, protocol)
    parent_source = json.loads((args.root / "STARTED.json").read_bytes())
    for key in ("source_commit", "source_tree", "runner_sha256", "protocol_sha256", "inputs_sha256",
                "runtime_source_files_sha256", "schema_assets_sha256", "python", "executable"):
        if actual_source[key] != parent_source[key]:
            raise ValueError(f"worker source binding changed: {key}")
    if args.mode == "case":
        mutation = json.loads((args.root / "mutations" / f"{args.case_id}.json").read_bytes())
        expected_before = (json.loads((args.root / "setup/result.json").read_bytes())["fixture"]
                           if args.case_id == "C02" else frozen_inputs["retained_fixture"]["files"])
        if mutation["before"] != expected_before or inventory(args.reference) != mutation["after"]:
            raise ValueError("worker input differs from frozen parent mutation inventory")
        if inventory(args.root / "base-fixture") != frozen_inputs["retained_fixture"]["files"]:
            raise ValueError("retained base input differs from frozen inventory")
    write_json(args.output / "STARTED.json", {
        "source_commit": args.source_commit, "protocol_sha256": sha(PROTOCOL.read_bytes()),
        "runner_sha256": sha(Path(__file__).read_bytes()), "mode": args.mode,
        "case_id": args.case_id, "python": sys.version, "pid": os.getpid(),
        "limits_active_before_runtime_import": True,
    })
    runtime = runtime_imports()
    events: list[dict[str, Any]] = []
    measurement_errors: list[dict[str, Any]] = []
    phase = ["setup" if args.mode == "setup" else "primary-load"]
    manager = runtime["IntegratedM1CheckpointManager"]
    try:
        with milestones(targets(runtime), events, phase,
                        lambda row: append_jsonl(args.output / "milestones.jsonl", row),
                        measurement_errors):
            if args.mode == "setup":
                predictive = runtime["PredictiveRevisionPilot"](
                    runtime["PilotConfig"](context_gate=0.25))
                scoped = runtime["CausalScopeRevisionPilot"](
                    runtime["ScopeRevisionConfig"](minimum_confidence=0.65))
                session = runtime["IntegratedM1Session"](pilot=runtime["IntegratedM1Pilot"](
                    predictive=predictive, scoped=scoped))
                config = {
                    "predictive": session.pilot.predictive.config.as_dict(),
                    "scope": session.pilot.scoped.config.as_dict(),
                }
                if canonical(config) != canonical(frozen_inputs["nondefault_public_configs"]):
                    raise ValueError("zero-cycle setup config differs from input freeze")
                guard()
                manager.save(session, args.output / "nondefault")
                guard()
                result = {"status": "completed", "dynamics_transitions": 0,
                          "fixture": inventory(args.output / "nondefault"), "config": config}
            else:
                before = inventory(args.reference)
                primary: dict[str, Any] = {"returned": False}
                write_json(args.output / "primary-attempt.json", {
                    "case_id": args.case_id, "status": "about_to_invoke_integrated_load"})
                try:
                    session = manager.load(args.reference)
                except Exception as exc:
                    primary.update(error_type=type(exc).__name__, error=str(exc))
                else:
                    primary["returned"] = True
                # Persist acceptance/rejection before inspection or save-back can fail.
                write_json(args.output / "primary-result.json", primary,
                           emergency=bool(measurement_errors))
                if measurement_errors:
                    write_json(args.output / "measurement-errors.json", measurement_errors,
                               emergency=True)
                    raise ObservationFailure("primary outcome retained; measurement incomplete")
                guard()
                after_load = inventory(args.reference)
                saveback: dict[str, Any] = {"status": "not_applicable"}
                if primary["returned"]:
                    primary["inspect"] = session.inspect()
                    primary["state_hash"] = session.state_hash()
                    primary["config"] = {
                        "predictive": session.pilot.predictive.config.as_dict(),
                        "scope": session.pilot.scoped.config.as_dict(),
                    }
                    expected_config = {
                        "predictive": json.loads((args.reference /
                                                  "predictive/pilot-state.json").read_bytes())[
                                                      "config"],
                        "scope": json.loads((args.reference /
                                             "scope/sb002-state.json").read_bytes())[
                                                 "payload"]["config"],
                    }
                    primary["saved_config_preserved"] = (
                        canonical(primary["config"]) == canonical(expected_config))
                    if args.case_id == "C02":
                        primary["nondefault_config_matches_plan"] = (
                            canonical(primary["config"]) ==
                            canonical(frozen_inputs["nondefault_public_configs"]))
                    phase[0] = "save-back"
                    try:
                        guard()
                        manager.save(session, args.output / "saveback")
                        guard()
                    except Exception as exc:
                        saveback = {"status": "incomplete", "error_type": type(exc).__name__,
                                    "error": str(exc)}
                    else:
                        saved = inventory(args.output / "saveback")
                        changed = sorted(name for name in set(before) | set(saved)
                                         if before.get(name) != saved.get(name))
                        saveback = {"status": "completed", "files": saved,
                                    "equal": saved == before,
                                    "changed_files": changed}
                after_all = inventory(args.reference)
                result = {"case_id": args.case_id, "status": "completed",
                          "primary_load": primary, "save_back": saveback,
                          "input_before": before, "input_after_load": after_load,
                          "input_after_saveback": after_all,
                          "input_unchanged": before == after_load == after_all,
                          "disposition": disposition(args.case_id, primary, saveback),
                          "dynamics_transitions": 0}
                if result["disposition"] == "incomplete_load_infrastructure":
                    result["status"] = "incomplete_infrastructure"
                elif saveback["status"] == "incomplete":
                    result["status"] = "incomplete_saveback"
        mark_measurement(result, measurement_errors)
        result["direct_reconstructions"] = event_count(events, "direct_reconstruct")
        result["primary_integrated_loads"] = event_count(events, "integrated_load", "primary-load")
        if result["direct_reconstructions"] > (1 if args.mode == "setup" else 2):
            raise RuntimeError("direct reconstruction accounting exceeded allocation")
        if result["primary_integrated_loads"] != (0 if args.mode == "setup" else 1):
            raise RuntimeError("primary load accounting mismatch")
        write_json(args.output / "result.json", result, emergency=bool(measurement_errors))
    finally:
        if measurement_errors and not (args.output / "measurement-errors.json").exists():
            write_json(args.output / "measurement-errors.json", measurement_errors, emergency=True)
        write_json(args.output / "milestones.json", events, emergency=True)
        enforce_output(args.root, protocol["budget"]["max_retained_bytes"])


def retained_fixture(output: Path) -> dict[str, Any]:
    guard()
    source = ROOT / "scripts/verify_m1_cold_resume_artifacts.py"
    spec = importlib.util.spec_from_file_location("m1_retained_data_verifier", source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files, archive = module.read_bundle(module.DEFAULT / "corrected.parts", "corrected")
    prefix = "observed/checkpoints/step-007/"
    chosen = {name.removeprefix(prefix): raw for name, raw in files.items()
              if name.startswith(prefix)}
    if len(chosen) != 6:
        raise ValueError("retained fixture requires exactly six files")
    frozen = load_inputs()["retained_fixture"]
    if archive != frozen["archive_sha256"] or {
            name: sha(raw) for name, raw in chosen.items()} != frozen["files"]:
        raise ValueError("retained fixture differs from frozen six-file input manifest")
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in chosen.items():
        guard(len(raw))
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        guard()
    return {"archive_sha256": archive, "prefix": prefix, "files": inventory(output)}


def capped_subprocess(command: list[str], root: Path, name: str,
                      timeout: float) -> dict[str, Any]:
    """Bound pipe retention; abort the owned process group on any observed excess."""
    begin = time.monotonic()
    status, truncated = "returned", False
    env = {**os.environ, "PYTHONHASHSEED": "1", "OMP_NUM_THREADS": "1",
           "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    guard()
    with (root / f"{name}.stdout").open("xb") as stdout, \
            (root / f"{name}.stderr").open("xb") as stderr, \
            subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True) as process:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, stdout)
            selector.register(process.stderr, selectors.EVENT_READ, stderr)
            try:
                while selector.get_map():
                    guard()
                    remaining = timeout - (time.monotonic() - begin)
                    if remaining <= 0:
                        raise TimeoutError("worker wall deadline reached")
                    for key, _ in selector.select(min(remaining, 0.1)):
                        raw = os.read(key.fileobj.fileno(), 65536)
                        if not raw:
                            selector.unregister(key.fileobj)
                            continue
                        guard(len(raw))
                        key.data.write(raw)
                        key.data.flush()
                        guard()
                process.wait(timeout=max(0.001, timeout - (time.monotonic() - begin)))
            except BaseException as exc:
                if isinstance(exc, BudgetExceeded):
                    status = "budget_exceeded"
                elif isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)):
                    status = "timed_out"
                else:
                    status = "capture_error"
                truncated = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
    return {"name": name, "status": status, "returncode": process.returncode,
            "stdout_stderr_may_be_truncated": truncated,
            "elapsed_seconds": time.monotonic() - begin, "command": command}


def read_events(path: Path) -> tuple[list[dict[str, Any]], bool]:
    if not path.exists():
        return [], False
    events = []
    for line in path.read_bytes().splitlines(keepends=True):
        try:
            if not line.endswith(b"\n"):
                return events, True
            events.append(json.loads(line))
        except (ValueError, UnicodeError):
            return events, True
    return events, False


def collect_case(root: Path, case_id: str, launch: dict[str, Any]) -> dict[str, Any]:
    folder = root / "cases" / case_id
    result_path = folder / "result.json"
    row = json.loads(result_path.read_bytes()) if result_path.exists() else {
        "case_id": case_id, "status": "incomplete_worker"}
    primary_path = folder / "primary-result.json"
    if primary_path.exists():
        row["primary_load"] = {**row.get("primary_load", {}),
                               **json.loads(primary_path.read_bytes())}
    events, truncated = read_events(folder / "milestones.jsonl")
    final_events = folder / "milestones.json"
    if final_events.exists():
        events = json.loads(final_events.read_bytes())
    primary_events = [e for e in events if e["name"] == "integrated_load"
                      and e["phase"] == "primary-load"]
    if "primary_load" not in row and any(e["event"] == "return" for e in primary_events):
        row["primary_load"] = {"returned": True, "recovered_from_return_journal": True}
    row["primary_calls_completed_observed"] = event_count(events, "integrated_load", "primary-load")
    row["direct_reconstructions_completed_observed"] = event_count(events, "direct_reconstruct")
    row["primary_invocation_intents_observed"] = sum(
        e["event"] == "call_intent" for e in primary_events)
    row["primary_attempt_intent_recorded"] = (folder / "primary-attempt.json").exists()
    failed = launch["returncode"] != 0 or launch["status"] != "returned"
    row["observations_may_be_incomplete"] = truncated or failed
    if failed:
        row["status"] = "incomplete_worker"
    if row.get("primary_load", {}).get("returned") and "save_back" not in row:
        row["save_back"] = {"status": "not_completed",
                            "phase_started": any(e["phase"] == "save-back" for e in events)}
    row["worker_status"] = launch
    row["raw_result"] = str(result_path.relative_to(root)) if result_path.exists() else None
    # Keep the full inspected state in the raw case result, not repeated in the summary.
    if "primary_load" in row:
        row["primary_load"] = {k: v for k, v in row["primary_load"].items() if k != "inspect"}
    return row


def run(args: argparse.Namespace, protocol: dict[str, Any]) -> None:
    global _BUDGET
    if args.output.exists():
        raise FileExistsError("diagnostic output is no-clobber")
    started = time.monotonic()
    provenance = preflight(args.source_commit, protocol)
    frozen_inputs = load_inputs()
    args.output.mkdir(parents=True, exist_ok=False)
    args.output_created = True
    root = args.output.resolve()
    budget = protocol["budget"]
    previous_budget = _BUDGET
    deadline = started + budget["max_total_seconds"]
    _BUDGET = (root, budget["max_retained_bytes"], deadline)
    cases = {row["case_id"]: {"case_id": row["case_id"], "status": "not_started"}
             for row in protocol["cases"]}
    worker_rows: list[dict[str, Any]] = []
    fixture = None
    transport_before = None
    failure = None
    setup_success = False
    transport = ROOT / "artifacts/m1_cold_resume_diagnostic_20261001/corrected.parts"

    def journal(row: dict[str, Any]) -> None:
        append_jsonl(root / "case-progress.jsonl", row)

    def launch(name: str, mode: str, output: Path, reference: Path | None = None,
               case_id: str | None = None) -> dict[str, Any]:
        guard()
        remaining = deadline - time.monotonic()
        command = [sys.executable, str(Path(__file__).resolve()), "--mode", mode,
                   "--output", str(output), "--root", str(root),
                   "--source-commit", args.source_commit, "--deadline", str(deadline)]
        if reference is not None:
            command += ["--reference", str(reference)]
        if case_id is not None:
            command += ["--case-id", case_id]
        row = capped_subprocess(command, root, name, min(remaining, budget["max_worker_seconds"]))
        worker_rows.append(row)
        write_json(root / "worker-status" / f"{name}.json", row, emergency=True)
        error_path = output / "ERROR.json"
        measurement_path = output / "measurement-errors.json"
        error = json.loads(error_path.read_bytes()) if error_path.exists() else {}
        measurements = (json.loads(measurement_path.read_bytes())
                        if measurement_path.exists() else [])
        if (row["status"] == "budget_exceeded" or error.get("error_type") == "BudgetExceeded"
                or any(e["error_type"] == "BudgetExceeded" for e in measurements)):
            raise BudgetExceeded(f"worker {name} observed a budget stop; no later worker admitted")
        return row

    try:
        # Retain all ten planned rows before archive/setup/preparation can fail.
        write_json(root / "planned-matrix.json", list(cases.values()))
        write_json(root / "STARTED.json", provenance)
        guard(PROTOCOL.stat().st_size + INPUTS.stat().st_size)
        for source, name in ((PROTOCOL, "protocol.json"), (INPUTS, "inputs.json")):
            with (root / name).open("xb") as stream:
                stream.write(source.read_bytes())
            guard()
        fixture = retained_fixture(root / "base-fixture")
        if fixture != frozen_inputs["retained_fixture"]:
            raise ValueError("retained fixture differs from input freeze")
        write_json(root / "input-provenance.json", fixture)
        transport_before = inventory(transport)
        write_json(root / "source-transport-before.json", transport_before)
        setup = launch("setup", "setup", root / "setup")
        setup_result_path = root / "setup/result.json"
        setup_success = (setup["returncode"] == 0 and setup["status"] == "returned"
                         and setup_result_path.exists()
                         and json.loads(setup_result_path.read_bytes())["status"] == "completed")
        guard()
        for case in protocol["cases"]:
            guard()
            case_id = case["case_id"]
            reference = root / "case-inputs" / case_id
            if case_id == "C02" and not setup_success:
                cases[case_id] = {"case_id": case_id, "status": "blocked_setup_failure"}
                journal(cases[case_id])
                continue
            cases[case_id]["status"] = "preparing_input"
            journal(cases[case_id])
            source = root / "setup/nondefault" if case_id == "C02" else root / "base-fixture"
            copy_input(source, reference)
            mutation = mutate_input(reference, case)
            write_json(root / "mutations" / f"{case_id}.json", mutation)
            cases[case_id]["status"] = "worker_launch_pending"
            journal(cases[case_id])
            status = launch(case_id, "case", root / "cases" / case_id, reference, case_id)
            cases[case_id] = collect_case(root, case_id, status)
            journal({"case_id": case_id, "status": cases[case_id]["status"],
                     "primary_load": cases[case_id].get("primary_load")})
            guard()
    except BaseException as exc:
        failure = {"error_type": type(exc).__name__, "error": str(exc),
                   "traceback": traceback.format_exc()}
        write_json(root / "ERROR.json", failure, emergency=True)
        raise
    finally:
        try:
            # Reconcile any interrupted current case from its independently flushed journal.
            by_name = {row["name"]: row for row in worker_rows}
            for case_id, row in list(cases.items()):
                if case_id in by_name:
                    cases[case_id] = collect_case(root, case_id, by_name[case_id])
                elif row["status"] in {"not_started", "preparing_input", "worker_launch_pending"}:
                    row["status"] = "blocked_controller_failure" if failure else "not_started"
            setup_events, setup_truncated = read_events(root / "setup/milestones.jsonl")
            if (root / "setup/milestones.json").exists():
                setup_events = json.loads((root / "setup/milestones.json").read_bytes())
            direct = event_count(setup_events, "direct_reconstruct") + sum(
                row.get("direct_reconstructions_completed_observed", 0) for row in cases.values())
            entries = sum(row.get("primary_calls_completed_observed", 0) for row in cases.values())
            base_unchanged = (inventory(root / "base-fixture") == fixture["files"]
                              if fixture is not None else None)
            source_unchanged = (inventory(transport) == transport_before
                                if transport_before is not None else None)
            size = retained_bytes(root)
            setup_failed = "setup" in by_name and not setup_success
            unknown = setup_truncated or setup_failed or any(
                row.get("observations_may_be_incomplete", False) for row in cases.values())
            summary = {
                "status": "complete" if failure is None and setup_success and all(
                    row["status"] == "completed" for row in cases.values()) else "incomplete",
                "cases": list(cases.values()), "workers": worker_rows,
                "setup_complete": setup_success,
                "primary_integrated_loads_completed_observed": entries,
                "direct_reconstructions_completed_observed": direct,
                "counts_are_lower_bounds": unknown,
                "retained_fixture_unchanged": base_unchanged,
                "source_transport_unchanged": source_unchanged,
                "retained_bytes_before_final_metadata": size,
                "output_threshold_exceeded": size > budget["max_retained_bytes"],
                "elapsed_seconds": time.monotonic() - started,
                "deadline_exceeded": time.monotonic() > deadline,
                "dynamics_transitions": 0, "scientific_credit": 0,
                "controller_failure": failure,
                "resource_boundary": "32MiB admission/checkpoint threshold, not a hard filesystem "
                                     "quota; bounded failure metadata is retained after a stop",
            }
            if base_unchanged is False or source_unchanged is False or direct > 21 or entries > 10:
                summary["status"] = "integrity_failure"
            write_json(root / "summary.json", summary, emergency=True)
            write_json(root / "inventory.json", inventory(root), emergency=True)
            print(json.dumps({"status": summary["status"], "cases": len(cases),
                              "primary_calls_completed_observed": entries,
                              "direct_reconstructions_completed_observed": direct,
                              "counts_are_lower_bounds": unknown, "dynamics_transitions": 0}))
        finally:
            _BUDGET = previous_budget


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("run", "setup", "case"), default="run")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--case-id")
    parser.add_argument("--deadline", type=float)
    args = parser.parse_args()
    args.output_created = False
    protocol = load_protocol()
    try:
        if args.mode == "run":
            run(args, protocol)
        else:
            worker(args, protocol)
    except BaseException as exc:
        if args.output_created and not (args.output / "ERROR.json").exists():
            write_json(args.output / "ERROR.json", {
                "error_type": type(exc).__name__, "error": str(exc),
                "traceback": traceback.format_exc()}, emergency=True)
        raise


if __name__ == "__main__":
    main()
