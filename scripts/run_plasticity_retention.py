#!/usr/bin/env python3
"""Bounded retention runner. Freeze/tests are model-free; run needs separate exact approval."""

from __future__ import annotations

# Capture wall time before heavyweight stdlib imports; they consume the run budget.
# ruff: noqa: E402
import time

BOOT_WALL = time.monotonic()

import argparse
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import resource
import selectors
import signal
import subprocess
import sys
import tarfile
from dataclasses import asdict, replace
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "artifacts/research/plasticity_retention_preparation_20261001"
PROTOCOL = ROOT / "protocols/plasticity_retention_bounded_v1.json"
FREEZE = ROOT / "artifacts/research/plasticity_retention_execution_20261001/freeze-v4-r3"
PUBLISHED_PREFIX = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
ARCHIVE_SHA = "2dfbe4f3afb8b046c1b465dcb52461daa027f72939dd85cf7dfad15670947082"
PREP_PINS = {
    "inputs.json": "6e9ae9652cf4593e4401e9ce149d1ff178007065c732c2950e904efb523b3773",
    "jobs.json": "e67c82326a43856aa4628c45d21ebd5cd8d9edf7b09c76c232982052544db1d6",
    "prefix_sources.json": "d9bc263106921a4c862e540795fb56c02565b8d8f370a88b570814448ee33dc9",
    "preparation_manifest.json": "bf084391b2a7e43cde63c2c8f95c0389e32bc09cce3333b15f930c5888d257a9",
}
PROTOCOL_SHA = "79a37f24eda0a5b82bb6f6e3428f48442a593f10dcb729dc3d67b30014ec0fb3"
VENDOR_SHA = "28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae"
ATTEMPT_ID = "plasticity-retention-v4-20261002"
PRIOR_FAILURE = ROOT / "artifacts/research/plasticity_retention_preflight_failure_20261002"
PRIOR_RESULT_SHA = "70a54d6f1c6b23809853e14901561bbda4aede73a885422e55a7ab6964caf223"
_MODEL_ADMISSION = False


def load_source(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("missing source loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


S = load_source("retention_support", ROOT / "scripts/plasticity_retention_support.py")
C = load_source("retention_contract", ROOT / "scripts/plasticity_retention_contract.py")
require = S.require


def prepared_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def check_preparation() -> tuple[dict, dict, dict, dict]:
    require(S.sha(PROTOCOL) == PROTOCOL_SHA, "independent protocol pin changed")
    for name, value in PREP_PINS.items():
        require(S.sha(PREPARATION / name) == value, "independent preparation pin changed: " + name)
    require(S.sha(S.VENDOR) == VENDOR_SHA, "published wrapper source changed")
    require(S.sha(PRIOR_FAILURE / "result.json") == PRIOR_RESULT_SHA, "prior failure bytes changed")
    prior = S.read(PRIOR_FAILURE / "result.json")
    require(
        prior["status"] == "failed"
        and prior["reserved_pairs"] == 0
        and prior["jobs_completed"] == 0
        and prior["job_costs"] == [],
        "prior allocation boundary",
    )
    p = S.read(PROTOCOL)
    inputs, jobs, prefixes = (
        S.read(PREPARATION / name) for name in ("inputs.json", "jobs.json", "prefix_sources.json")
    )
    require(jobs["execution_authorized"] is False, "preparation authority boundary")
    require(len(jobs["jobs"]) == 26 and sum(j["pairs"] for j in jobs["jobs"]) == 768, "job ceiling")
    return p, inputs, jobs, prefixes


def sources() -> list[Path]:
    selected = [
        Path(__file__).resolve(),
        ROOT / "scripts/plasticity_retention_support.py",
        ROOT / "scripts/plasticity_retention_contract.py",
        ROOT / "scripts/verify_plasticity_retention_run.py",
        ROOT / "scripts/verify_retention_preflight_failure.py",
        ROOT / "scripts/prepare_plasticity_retention_inputs.py",
        S.VENDOR,
        PROTOCOL,
        PRIOR_FAILURE / "result.json",
        PRIOR_FAILURE / "invocation.json",
        PRIOR_FAILURE / "independent_audit.json",
        ROOT / "docs/research/plasticity_retention_design_20261001.md",
        ROOT / "docs/research/plasticity_retention_protocol_20261001.md",
        ROOT / "tests/test_plasticity_retention_runner.py",
        ROOT / "tests/test_plasticity_retention_contract.py",
        ROOT / "tests/test_plasticity_retention_verifier.py",
        ROOT / "tests/test_retention_preflight_failure.py",
        ROOT / "AGENTS.md",
        ROOT / "pyproject.toml",
        *[PREPARATION / name for name in PREP_PINS],
    ]
    for folder in (ROOT / "src", ROOT / "schemas"):
        selected.extend(
            p
            for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
        )
    return sorted(set(selected))


def freeze(destination: Path) -> dict[str, Any]:
    """Only source/dependency/file reads and new JSON writes, never predecessor import."""
    S.validate_execution_environment()
    check_preparation()
    require(
        not S.PLANNED_OUTPUT.exists() and not S.PLANNED_OUTPUT.is_symlink(),
        "planned run output already exists; cannot freeze a new execution",
    )
    require(not destination.exists() and not destination.is_symlink(), "freeze no clobber")
    destination = destination.resolve()
    require(
        destination != S.PLANNED_OUTPUT and not destination.is_relative_to(S.PLANNED_OUTPUT),
        "freeze/run overlap",
    )
    files = {"dependencies.json": prepared_bytes(S.dependency_inventory())}
    manifest = {
        "schema": "retention-execution-freeze-1",
        "attempt_id": ATTEMPT_ID,
        "previous_attempt": {
            "source_commit": "2977aefc06d80291bb65c36b4b3bac0499084d0f",
            "manifest_sha256": "cc4dffcea78d8d82d3f5a6fc42d5474e97387b0dbcbab0377c9895233cb41834",
            "result_sha256": PRIOR_RESULT_SHA,
            "classification": "FAILED_BEFORE_WORKER_AND_MODEL_ADMISSION",
            "audited_model_pairs": 0,
        },
        "combined_model_allocation_ceiling": 768,
        "status": "UNEXECUTED",
        "scientific_credit": 0,
        "preparation_commit": "4c57cbfae78c4c3299e2936fe82c3750afd5cd83",
        "sources": {str(p.relative_to(ROOT)): S.sha(p) for p in sources()},
        "generated": {n: hashlib.sha256(v).hexdigest() for n, v in files.items()},
        "execution_source_root": str(ROOT),
        "planned_output": str(S.PLANNED_OUTPUT),
        "ceiling_pairs": 768,
        "preparation_model_calls": 0,
        "planned_output_absent_at_freeze": True,
        "authority": (
            "Requires separate reviewed source publication and explicit exact execution approval"
        ),
    }
    files["manifest.json"] = prepared_bytes(manifest)
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in files.items():
        with (destination / name).open("xb") as stream:
            stream.write(raw)
    return {"manifest_sha256": S.sha(destination / "manifest.json"), "model_calls": 0}


def verify_freeze(directory: Path) -> dict:
    S.validate_execution_environment()
    check_preparation()
    manifest = S.read(directory / "manifest.json")
    require(
        manifest["schema"] == "retention-execution-freeze-1"
        and manifest["attempt_id"] == ATTEMPT_ID
        and manifest["previous_attempt"]["result_sha256"] == PRIOR_RESULT_SHA
        and manifest["previous_attempt"]["audited_model_pairs"] == 0
        and manifest["combined_model_allocation_ceiling"] == 768
        and manifest["status"] == "UNEXECUTED"
        and manifest["ceiling_pairs"] == 768,
        "execution freeze identity",
    )
    expected = {str(p.relative_to(ROOT)): S.sha(p) for p in sources()}
    require(manifest["sources"] == expected, "actual source inventory/hash mismatch")
    require(
        {p.name for p in directory.iterdir()} == {"manifest.json", *manifest["generated"]},
        "freeze file inventory",
    )
    for name, value in manifest["generated"].items():
        require(S.sha(directory / name) == value, "dependency file digest")
    require(
        S.read(directory / "dependencies.json") == S.dependency_inventory(),
        "interpreter/stdlib actual bytes changed",
    )
    require(
        manifest["planned_output"] == str(S.PLANNED_OUTPUT)
        and manifest["execution_source_root"] == str(ROOT),
        "freeze output/source identity",
    )
    return manifest


def git(*args: str) -> bytes:
    # Git work is also charged before admission. Its OS CPU ceiling is below
    # the reservation to cover process/termination granularity conservatively.
    with S.reserve_child_cpu(2):
        remaining = signal.getitimer(signal.ITIMER_REAL)[0]
        require(remaining > 0, "Git requires active bounded driver")
        proc = None
        previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGPROF, signal.SIGALRM})
        try:
            try:
                proc = subprocess.Popen(
                    ["git", *args],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=lambda: (
                        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask),
                        S.process_limits(1),
                    ),
                )
            finally:
                signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            output, error = proc.communicate(timeout=remaining)
            require(
                proc.returncode == 0, "Git gate failure: " + error.decode(errors="replace")[:2048]
            )
            return output
        finally:
            cleanup_mask = signal.pthread_sigmask(
                signal.SIG_BLOCK, {signal.SIGPROF, signal.SIGALRM}
            )
            try:
                if proc is not None:
                    if proc.poll() is None:
                        proc.kill()
                    proc.communicate()
            finally:
                signal.pthread_sigmask(signal.SIG_SETMASK, cleanup_mask)


def gate(directory: Path, review: Path, publication: Path, approval: Path) -> dict:
    directory = directory.resolve()
    verify_freeze(directory)
    head = git("rev-parse", "HEAD").decode().strip()
    pin = S.sha(directory / "manifest.json")
    records, record_files = {}, {}
    for kind, path in (("review", review), ("publication", publication), ("approval", approval)):
        raw = path.read_bytes()
        records[kind] = json.loads(raw)
        record_files[kind] = {
            "path": "authority-records/" + kind + ".json",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }
    require(records["review"].get("source_review_approved") is True, "source review missing")
    require(records["publication"].get("verified_published") is True, "publication unverified")
    require(records["approval"].get("approved_for_execution") is True, "execution not approved")
    for kind, record in records.items():
        require(
            record.get("source_commit") == head and record.get("manifest_sha256") == pin,
            kind + " exact source/freeze mismatch",
        )
        require(
            record.get("output_root") == str(S.PLANNED_OUTPUT)
            and type(record.get("ceiling_pairs")) is int
            and record.get("ceiling_pairs") == 768,
            kind + " scope mismatch",
        )
        require(
            all(
                type(record.get(key)) is str and bool(record[key].strip())
                for key in ("record_url", "recorded_by")
            ),
            kind + " provenance missing",
        )
    for path in [*sources(), *directory.iterdir()]:
        name = str(path.relative_to(ROOT))
        require(git("show", f"{head}:{name}") == path.read_bytes(), "not committed: " + name)
    return {
        "source_commit": head,
        "manifest_sha256": pin,
        "records": records,
        "record_files": record_files,
        "authority_limit": "records are externally supplied; freeze never mints approval",
    }


def loaded_bindings(manifest: dict, dependency: dict) -> dict[str, str]:
    """Bind actually loaded module origins, not only a Git tree, before model admission."""
    stdlib = Path(dependency["stdlib_path"]).resolve()
    bindings = {}
    for name, module in list(sys.modules.items()):
        if not isinstance(module, ModuleType):
            continue
        filename = getattr(module, "__file__", None)
        origin = getattr(getattr(module, "__spec__", None), "origin", None)
        if filename is None:
            require(origin in (None, "built-in", "frozen"), "unbound module origin: " + name)
            bindings[name] = "interpreter:" + str(origin)
            continue
        path = Path(filename).resolve()
        if path.is_relative_to(ROOT):
            relative = str(path.relative_to(ROOT))
            require(
                relative in manifest["sources"] and S.sha(path) == manifest["sources"][relative],
                "loaded repository module mismatch: " + name,
            )
        elif path.is_relative_to(stdlib):
            relative = str(path.relative_to(stdlib))
            require(
                relative in dependency["stdlib_files"]
                and S.sha(path) == dependency["stdlib_files"][relative],
                "loaded stdlib module mismatch: " + name,
            )
        else:
            raise RuntimeError("loaded module outside frozen origins: " + name)
        bindings[name] = str(path) + ":" + S.sha(path)
    return bindings


def predecessor() -> Any:
    require(_MODEL_ADMISSION, "runtime import is not admitted")
    require(not any(name.startswith("sparkbrain") for name in sys.modules), "runtime preloaded")
    require(S.sha(S.VENDOR) == VENDOR_SHA, "predecessor changed")
    return load_source("retention_published_predecessor", S.VENDOR)


def extract_prefixes(output: Path, writer: Any, prefixes: dict) -> None:
    manifest = S.read(PUBLISHED_PREFIX / "transport_manifest.json")
    chunks = []
    for item in manifest["parts"]:
        raw = (PUBLISHED_PREFIX / item["path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == item["encoded_sha256"], "public part digest")
        chunks.append(base64.b64decode(b"".join(raw.split()), validate=True))
    data = b"".join(chunks)
    require(hashlib.sha256(data).hexdigest() == ARCHIVE_SHA, "public archive independent pin")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for name, record in prefixes["prefixes"].items():
            for member in record["checkpoint_members"]:
                entry = archive.getmember(member)
                require(entry.isfile(), "checkpoint member is not regular")
                stream = archive.extractfile(entry)
                require(stream is not None, "checkpoint member absent")
                raw = stream.read()
                require(
                    hashlib.sha256(raw).hexdigest() == record["files_sha256"][member],
                    "checkpoint member independent digest",
                )
                writer.raw(output / "prefixes" / name / Path(member).name, raw)


def verify_prefix(job: dict, prefixes: dict) -> Path:
    record = prefixes["prefixes"][job["prefix"]]
    require(
        hashlib.sha256(prepared_bytes(record)).hexdigest() == job["prefix_source_sha256"],
        "job prefix binding",
    )
    directory = S.PLANNED_OUTPUT / "prefixes" / job["prefix"]
    require(
        {p.name for p in directory.iterdir()}
        == {Path(p).name for p in record["checkpoint_members"]},
        "checkpoint inventory",
    )
    for member in record["checkpoint_members"]:
        require(
            S.sha(directory / Path(member).name) == record["files_sha256"][member],
            "retained copy changed",
        )
    return directory


def call_limits(job: dict) -> dict[str, int]:
    n = job["pairs"]
    v05 = job["family"] == "v05"
    return {
        "wrapper_load": 1,
        "wrapper_init": 1,
        "v05_init": 2 if v05 else 0,
        "native_load": int(v05),
        "predict": n,
        "outcome": n,
        "v05_episode": n if v05 else 0,
        "apply": n if v05 else 0,
        "v05_outcome": n if v05 else 0,
    }


def normalized(value: Any) -> Any:
    return json.loads(C.canonical(value))


def delay_map(brain: Any) -> dict[str, float]:
    return {f"{a}:{b}": edge.delay_ms for (a, b), edge in brain.base.field.connections.items()}


def configure(brain: Any, arm: dict) -> dict:
    before = normalized(brain.state_dict())
    brain.config = replace(
        brain.config,
        enable_weight_learning=arm["enable_weight_learning"],
        enable_delay_learning=False,
    )
    brain.plasticity.config = replace(brain.plasticity.config, **arm, enable_delay_learning=False)
    after = normalized(brain.state_dict())
    expected = json.loads(C.canonical(before))
    expected["config"]["enable_weight_learning"] = arm["enable_weight_learning"]
    expected["config"]["enable_delay_learning"] = False
    expected["plasticity"]["config"].update(arm)
    expected["plasticity"]["config"]["enable_delay_learning"] = False
    require(after == expected, "intervention changed state beyond specified configuration")
    require(
        brain.config.enable_homeostasis
        and not brain.config.enable_action
        and not brain.config.enable_reward_modulation,
        "common v05 configuration mismatch",
    )
    return {
        "before_sha256": C.digest(before),
        "after_sha256": C.digest(after),
        "brain_config": asdict(brain.config),
        "plasticity_config": asdict(brain.plasticity.config),
    }


def validate_job(job: dict, jobs: dict, inputs: dict, prefixes: dict) -> tuple[dict, list, Path]:
    planned = [j for j in jobs["jobs"] if j["job_id"] == job["plan"]["job_id"]]
    require(len(planned) == 1 and job["plan"] == planned[0], "job differs from published plan")
    plan = planned[0]
    require(
        job["cpu_limit"] == plan["cpu_seconds"] and job["wall_limit"] == plan["wall_seconds"],
        "job resource mismatch",
    )
    rows = inputs["streams"][plan["stream"]]
    require(
        len(rows) == plan["pairs"]
        and hashlib.sha256(prepared_bytes(rows)).hexdigest() == plan["input_sha256"],
        "job input binding",
    )
    return plan, rows, verify_prefix(plan, prefixes)


def worker_body(job: dict, directory: Path, writer: Any, ledger: Any, primary: dict) -> dict:
    global _MODEL_ADMISSION
    manifest = verify_freeze(Path(job["freeze"]))
    require(
        S.sha(Path(job["freeze"]) / "manifest.json") == job["binding"]["manifest_sha256"],
        "worker freeze differs from driver admission",
    )
    for kind, filename in job["record_paths"].items():
        require(S.sha(Path(filename)) == job["record_sha256"][kind], "approval record changed")
        require(S.read(Path(filename)) == job["binding"]["records"][kind], "record identity")
    p, inputs, jobs, prefixes = check_preparation()
    plan, rows, prefix = validate_job(job, jobs, inputs, prefixes)
    _MODEL_ADMISSION = True
    sys.path.insert(0, str(ROOT / "src"))
    vendor = predecessor()
    dependency = S.read(Path(job["freeze"]) / "dependencies.json")
    writer.json(
        directory / "loaded-before-construction.json", loaded_bindings(manifest, dependency)
    )
    model_class, brain_class = vendor.Model, vendor.IntegratedV05Brain
    original_init, brain_init = model_class.__init__, brain_class.__init__
    original_native_load = brain_class.load_checkpoint
    episode, outcome = brain_class.process_episode, brain_class.learn_outcome

    def counted_init(self: Any, *args: Any, **kwargs: Any) -> None:
        return ledger.call("wrapper_init", original_init, self, *args, **kwargs)

    def counted_brain_init(self: Any, *args: Any, **kwargs: Any) -> None:
        return ledger.call("v05_init", brain_init, self, *args, **kwargs)

    def counted_load(cls: Any, *args: Any, **kwargs: Any) -> Any:
        require(cls is brain_class, "unexpected loader class")
        return ledger.call("native_load", original_native_load, *args, **kwargs)

    def counted_episode(self: Any, *args: Any, **kwargs: Any) -> Any:
        return ledger.call("v05_episode", episode, self, *args, **kwargs)

    def counted_outcome(self: Any, *args: Any, **kwargs: Any) -> Any:
        return ledger.call("v05_outcome", outcome, self, *args, **kwargs)

    with contextlib.ExitStack() as stack:
        for cls, name, replacement in (
            (model_class, "__init__", counted_init),
            (brain_class, "__init__", counted_brain_init),
            (brain_class, "load_checkpoint", classmethod(counted_load)),
            (brain_class, "process_episode", counted_episode),
            (brain_class, "learn_outcome", counted_outcome),
        ):
            stack.enter_context(patch.object(cls, name, replacement))
        model = ledger.call("wrapper_load", model_class.load, prefix)
        ledger.require_observed()
        require(
            normalized(model.state()) == S.read(prefix / "wrapper.json"), "wrapper restore mismatch"
        )
        require(model.pending is None and len(model.receipts) == 64, "prefix receipt boundary")
        initial_delays = None
        active = {"index": -1, "audit": None, "calls": 0}
        if model.brain:
            require(
                normalized(model.brain.state_dict()) == S.read(prefix / "brain.json")["payload"],
                "native persisted-state restore mismatch",
            )
            writer.json(
                directory / "configuration.json", configure(model.brain, p["arms"][plan["arm"]])
            )
            initial_delays = delay_map(model.brain)
            controller_class = type(model.brain.plasticity)
            apply = controller_class.apply

            def observed_apply(controller: Any, field: Any, spikes: Any) -> Any:
                require(controller is model.brain.plasticity, "unexpected controller")
                active["calls"] += 1
                require(active["calls"] == 1, "extra apply per occurrence")
                audit = None
                # Observer failure is latched, while the admitted model call finishes.
                try:
                    audit = C.audit_apply_before(field, spikes, controller)
                except (TimeoutError, MemoryError):
                    raise
                except Exception as exc:
                    ledger.observation_failed = True
                    primary["observer_error"] = type(exc).__name__ + ": " + str(exc)[:2048]
                returned = ledger.call("apply", apply, controller, field, spikes)
                if audit is not None:
                    try:
                        active["audit"] = C.audit_apply_after(audit, field, controller, returned)
                        writer.json(
                            directory / "apply.jsonl",
                            {"index": active["index"], **active["audit"]},
                            append=True,
                        )
                    except (TimeoutError, MemoryError):
                        raise
                    except Exception as exc:
                        ledger.observation_failed = True
                        primary["observer_error"] = type(exc).__name__ + ": " + str(exc)[:2048]
                return returned

            stack.enter_context(patch.object(controller_class, "apply", observed_apply))
        complete = []
        for index, supplied in enumerate(rows):
            observation = {key: supplied[key] for key in p["input_contract"]["model_keys"]}
            require(set(observation) == {"occurrence_id", "start_ms", "pulses"}, "input keys")
            require(
                model.pending is None and observation["occurrence_id"] not in model.receipts,
                "observation is not a fresh receipt",
            )
            active.update(index=index, audit=None, calls=0)
            primary.clear()
            primary.update(
                index=index,
                occurrence_id=observation["occurrence_id"],
                prediction_returned=False,
                outcome_returned=False,
            )
            result = ledger.call("predict", model.predict, observation)
            primary.update(
                prediction_returned=True,
                prediction={key: result[key] for key in ("p1", "native", "occurrence_id")},
            )
            ledger.require_observed()
            require(result["input_sha256"] == S.digest(observation), "actual model input binding")
            require(result["query_time_ms"] == supplied["start_ms"] + 72, "prediction timing")
            if model.brain:
                require(active["calls"] == 1 and active["audit"] is not None, "missing apply")
                require(delay_map(model.brain) == initial_delays, "restored delay map changed")
            record = {
                **result,
                "index": index,
                "outcome": supplied["outcome"],
                "receipt_time_ms": supplied["receipt_time_ms"],
                "actual_weight_abs_change": (active["audit"] or {}).get(
                    "actual_weight_abs_change", 0
                ),
            }
            if model.brain:
                record["readout_counts_before_receipt"] = normalized(model.brain.predictor.counts)
                record["candidate_prototypes"] = {
                    key: candidate.prototype.as_dict()
                    for key, candidate in model.brain.assemblies.candidates.items()
                }
            C.metrics([record])
            writer.json(directory / "predictions.jsonl", record, append=True)
            returned = ledger.call(
                "outcome", model.outcome, supplied["occurrence_id"], supplied["outcome"]
            )
            primary["outcome_returned"] = True
            primary["outcome_value"] = returned
            ledger.require_observed()
            require(
                returned is True and model.pending is None and len(model.receipts) == 65 + index,
                "receipt completion mismatch",
            )
            writer.json(
                directory / "receipts.jsonl",
                {
                    "index": index,
                    "occurrence_id": supplied["occurrence_id"],
                    "outcome": supplied["outcome"],
                    "wrapper_sha256": C.digest(model.state()),
                    "brain_sha256": C.digest(model.brain.state_dict()) if model.brain else None,
                    "readout_counts_after_receipt": normalized(model.brain.predictor.counts)
                    if model.brain
                    else None,
                },
                append=True,
            )
            complete.append(record)
        require(
            dict(ledger.returns) == {k: v for k, v in ledger.limits.items() if v},
            "completed method totals differ from allocation",
        )
        require(not ledger.errors, "model errors in completed job")
        writer.json(directory / "loaded-after-methods.json", loaded_bindings(manifest, dependency))
        writer.json(
            directory / "final-state.json",
            {"wrapper": model.state(), "brain": model.brain.state_dict() if model.brain else None},
        )
        require(verify_prefix(plan, prefixes) == prefix, "input copy altered")
        return {
            "completed_pairs": len(complete),
            "metrics": C.metrics(complete),
            "configuration": p["arms"].get(plan["arm"]),
            "scientific_credit": 0,
        }


def worker(job_path: Path, supervisor_fd: int | None) -> int:
    started_wall, started_cpu = BOOT_WALL, S.cpu_clock()
    job = S.read(job_path)
    directory = job_path.parent
    supervisor = S.accept_supervision(supervisor_fd, job, directory)
    S.process_limits(job["cpu_limit"])
    sys.addaudithook(S.deny_network)
    writer = C.OutputWriter(S.PLANNED_OUTPUT, terminal_limit=128 * 1024, live=supervisor.check_live)
    ledger = C.CallLedger(
        lambda row: writer.json(directory / "calls.jsonl", row, append=True),
        call_limits(job["plan"]),
    )
    primary: dict[str, Any] = {}
    result = {"schema": "retention-worker-1", "job_sha256": S.digest(job), "status": "failed"}
    try:
        remaining_cpu = job["cpu_limit"] - S.cpu_clock() - 0.15
        remaining_wall = supervisor.wall_stop - time.monotonic() - 0.15
        with S.deadline(remaining_cpu, remaining_wall):
            result.update(worker_body(job, directory, writer, ledger, primary))
            ledger.require_observed()
        result["status"] = "complete"
    except BaseException as exc:
        result.update(error_type=type(exc).__name__, error=str(exc)[:4096])
    finally:
        result.update(
            calls=ledger.summary(),
            last_primary=primary,
            worker_cpu_seconds=S.cpu_clock(),
            worker_body_cpu_seconds=S.cpu_clock() - started_cpu,
            worker_wall_seconds=time.monotonic() - started_wall,
            worker_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            total_output_bytes_before_terminal=writer.total(),
            measurement_failed=writer.measurement_failed,
        )
        # No extra emergency directory: this terminal file consumes the reserved total.
        writer.json(directory / "result.json", result, terminal=True)
    return 0 if result["status"] == "complete" else 1


def launch_worker(job: dict, output: Path, writer: Any, costs: list[dict]) -> dict:
    begun_cpu, begun_wall = time.process_time(), time.monotonic()
    work = output / "jobs" / job["plan"]["job_id"]
    work.mkdir(parents=True, exist_ok=False)
    writer.json(work / "job.json", job)
    read_fd, write_fd = os.pipe2(os.O_CLOEXEC)
    envelope = {
        "schema": "retention-supervision-1",
        "parent_pid": os.getpid(),
        "parent_start_ticks": S.process_start_ticks(os.getpid()),
        "writer_fd": write_fd,
        "job_sha256": S.digest(job),
        "directory": str(work.resolve()),
        "output_root": str(output),
        "cpu_limit": job["cpu_limit"],
        "wall_limit": job["wall_limit"],
        "issued_monotonic": begun_wall,
        "wall_stop_monotonic": begun_wall + job["wall_limit"] - 0.1,
    }
    raw = C.canonical(envelope)
    require(len(raw) <= 4096 and os.write(write_fd, raw) == len(raw), "supervisor write")
    proc = None
    usage = None
    failure = None
    captures = {"stdout": bytearray(), "stderr": bytearray()}
    consumed = {"stdout": 0, "stderr": 0}
    timed_out = False
    # Arm cleanup before creation and defer timer delivery until proc is assigned.
    # The child restores the previous signal mask before exec.
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGPROF, signal.SIGALRM})
    try:
        try:
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-S",
                    "-P",
                    "-B",
                    str(Path(__file__).resolve()),
                    "worker",
                    "--job",
                    str(work / "job.json"),
                    "--supervisor-fd",
                    str(read_fd),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                pass_fds=(read_fd,),
                env=dict(os.environ),
                preexec_fn=lambda: (
                    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask),
                    S.process_limits(job["cpu_limit"]),
                ),
            )
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        with selectors.DefaultSelector() as selector:
            for name, stream in (("stdout", proc.stdout), ("stderr", proc.stderr)):
                require(stream is not None, "missing worker capture")
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            while proc.returncode is None or selector.get_map():
                if time.monotonic() >= envelope["wall_stop_monotonic"]:
                    timed_out = True
                    raise TimeoutError("worker wall allowance")
                for key, _ in selector.select(0.01):
                    data = os.read(key.fd, 4096)
                    if not data:
                        selector.unregister(key.fileobj)
                        continue
                    name = key.data
                    consumed[name] += len(data)
                    room = 65536 - len(captures[name])
                    captures[name].extend(data[:room])
                    require(consumed[name] <= 65536, name + " exceeded capture allowance")
                if proc.returncode is None:
                    pid, status, use = os.wait4(proc.pid, os.WNOHANG)
                    if pid:
                        proc.returncode, usage = os.waitstatus_to_exitcode(status), use
    except BaseException as exc:
        failure = exc
    finally:
        cleanup_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGPROF, signal.SIGALRM})
        try:
            if proc is not None and proc.returncode is None:
                try:
                    os.kill(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                _, status, usage = os.wait4(proc.pid, 0)
                proc.returncode = os.waitstatus_to_exitcode(status)
            os.close(read_fd)
            os.close(write_fd)
            if proc is not None:
                for stream in (proc.stdout, proc.stderr):
                    if stream is not None:
                        stream.close()
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, cleanup_mask)
    if proc is None:
        require(failure is not None, "worker creation returned no process")
        raise failure
    require(usage is not None, "worker resource accounting missing")
    for name, data in captures.items():
        try:
            writer.raw(work / (name + ".bin"), bytes(data))
        except BaseException as exc:
            failure = failure or exc
    cost = {
        "job_id": job["plan"]["job_id"],
        "exit_code": proc.returncode,
        "worker_cpu_seconds": usage.ru_utime + usage.ru_stime,
        "driver_cpu_seconds": time.process_time() - begun_cpu,
        "wall_seconds_before_cost": time.monotonic() - begun_wall,
        "worker_peak_rss_kib": usage.ru_maxrss,
        "driver_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "timed_out": timed_out,
        "capture_consumed_bytes": consumed,
        "capture_retained_bytes": {k: len(v) for k, v in captures.items()},
        "known_discarded_bytes": {k: consumed[k] - len(v) for k, v in captures.items()},
        "unread_pipe_bytes": "unknown after failure" if failure else 0,
        "terminal_cost_reserve_seconds": 0.1,
        "failure": None if failure is None else type(failure).__name__ + ": " + str(failure)[:2048],
    }
    costs.append(cost)
    with S.deadline(0.1, 0.1):
        writer.json(output / "job-costs.jsonl", cost, append=True, terminal=True)
    if failure:
        raise failure
    require(
        cost["worker_cpu_seconds"] <= job["cpu_limit"]
        and cost["wall_seconds_before_cost"] + 0.1 <= job["wall_limit"],
        "worker resource excess",
    )
    require(proc.returncode == 0, "worker failed: " + job["plan"]["job_id"])
    result = S.read(work / "result.json")
    require(
        result.get("status") == "complete" and result.get("job_sha256") == S.digest(job),
        "worker terminal incomplete or unbound",
    )
    require(result["completed_pairs"] == job["plan"]["pairs"], "worker incomplete pairs")
    require(
        result["calls"]["intents"]
        == result["calls"]["returns"]
        == {k: v for k, v in call_limits(job["plan"]).items() if v}
        and not result["calls"]["errors"]
        and not result["calls"]["observation_failed"],
        "worker method counts incomplete",
    )
    return result


def read_jsonl(path: Path) -> list[dict]:
    with path.open() as stream:
        return [json.loads(line) for line in stream]


def first_observables(row: dict) -> dict:
    raw = row["raw_result"]
    # Whole state_hash intentionally differs after the configured weight update.
    return {
        "p1": row["p1"],
        "native": row["native"],
        "assembly_id": row["assembly_id"],
        "mature": row["mature"],
        "emitted_pulses": raw["emitted_pulses"],
        "spikes": raw["v04_result"]["spikes"],
        "patterns": raw["patterns"],
        "activations": raw["assembly_activations"],
        "prediction": raw["prediction"],
    }


def validate_rows(job: dict, output: Path, inputs: dict) -> list[dict]:
    directory = output / "jobs" / job["job_id"]
    rows = read_jsonl(directory / "predictions.jsonl")
    receipts = read_jsonl(directory / "receipts.jsonl")
    expected = inputs["streams"][job["stream"]]
    require(len(rows) == len(receipts) == len(expected) == job["pairs"], "raw row completeness")
    for i, (row, receipt, supplied) in enumerate(zip(rows, receipts, expected, strict=True)):
        obs = {k: supplied[k] for k in ("occurrence_id", "start_ms", "pulses")}
        require(
            row["index"] == receipt["index"] == i
            and row["occurrence_id"] == receipt["occurrence_id"] == supplied["occurrence_id"]
            and row["outcome"] == receipt["outcome"] == supplied["outcome"]
            and row["input_sha256"] == S.digest(obs)
            and row["receipt_time_ms"] == supplied["receipt_time_ms"],
            "raw row input/receipt binding",
        )
    C.metrics(rows)
    if job["family"] == "v05":
        audits = read_jsonl(directory / "apply.jsonl")
        require(len(audits) == len(rows), "apply row completeness")
        require(
            all(
                a["index"] == i
                and a["delays_unchanged"] is True
                and a["extra_apply_calls"] == 0
                and a["actual_weight_abs_change"] == rows[i]["actual_weight_abs_change"]
                for i, a in enumerate(audits)
            ),
            "apply row binding",
        )
    return rows


def driver(args: argparse.Namespace) -> int:
    started_wall = BOOT_WALL
    output = args.output.resolve()
    S.validate_execution_environment()
    S.validate_output_roots(output, initialize=True)
    require(
        not output.exists() and not args.output.is_symlink(), "run output already exists; no retry"
    )
    S.process_limits(360)
    sys.addaudithook(S.deny_network)
    output.mkdir(parents=True, exist_ok=False)
    writer = C.OutputWriter(output, terminal_limit=512 * 1024)
    results, costs = {}, []
    terminal: dict[str, Any] = {
        "schema": "retention-run-1",
        "attempt_id": ATTEMPT_ID,
        "prior_attempt_audited_model_pairs": 0,
        "status": "failed",
        "scientific_credit": 0,
        "reserved_pairs": 0,
    }
    try:
        with S.deadline(358 - S.cpu_clock(), 475 - (time.monotonic() - started_wall)):
            binding = gate(args.freeze, args.review, args.publication, args.approval)
            p, inputs, jobs, prefixes = check_preparation()
            for kind, item in binding["record_files"].items():
                raw = getattr(args, kind).read_bytes()
                require(
                    hashlib.sha256(raw).hexdigest() == item["sha256"]
                    and len(raw) == item["bytes"]
                    and json.loads(raw) == binding["records"][kind],
                    "authority record changed before retention",
                )
                writer.raw(output / item["path"], raw)
            writer.json(output / "execution-gate.json", binding)
            writer.json(output / "job-plan.json", jobs)
            writer.json(
                output / "environment.json",
                {
                    "python": sys.version,
                    "python_executable_sha256": S.sha(Path(sys.executable).resolve()),
                    "python_socket_audit_denial": True,
                    "OS_network_isolation_enforced": False,
                    "network_scope": "Python socket audit hook; not an OS sandbox",
                    "address_space_bytes": 512 * 1024**2,
                    "budget_scope": (
                        "all driver/child CPU; imports, hashing, observation, scoring included"
                    ),
                },
            )
            extract_prefixes(output, writer, prefixes)
            record_paths = {
                kind: str(output / item["path"]) for kind, item in binding["record_files"].items()
            }
            record_sha = {kind: item["sha256"] for kind, item in binding["record_files"].items()}
            for plan in jobs["jobs"]:
                require(
                    S.cpu_clock() < 358 and time.monotonic() - started_wall < 475,
                    "aggregate resource headroom exhausted",
                )
                job = {
                    "plan": plan,
                    "cpu_limit": plan["cpu_seconds"],
                    "wall_limit": plan["wall_seconds"],
                    "freeze": str(args.freeze.resolve()),
                    "binding": binding,
                    "record_paths": record_paths,
                    "record_sha256": record_sha,
                }
                terminal["reserved_pairs"] += plan["pairs"]
                require(terminal["reserved_pairs"] <= 768, "global reservation ceiling")
                writer.json(
                    output / "reservations.jsonl",
                    {
                        "job_id": plan["job_id"],
                        "pairs": plan["pairs"],
                        "cumulative_pairs": terminal["reserved_pairs"],
                    },
                    append=True,
                )
                with S.reserve_child_cpu(plan["cpu_seconds"]):
                    results[plan["job_id"]] = launch_worker(job, output, writer, costs)
            scored = {}
            for fixture in p["fixtures"]:
                groups: dict[str, dict] = {}
                firsts: dict[str, list] = {}
                for plan in jobs["jobs"]:
                    if not plan["stream"].startswith(str(fixture["suffix_seed"]) + "-"):
                        continue
                    rows = validate_rows(plan, output, inputs)
                    groups.setdefault(plan["condition"], {})[plan["arm"]] = rows
                    if plan["family"] == "v05":
                        firsts.setdefault(plan["condition"], []).append(first_observables(rows[0]))
                require(
                    all(all(row == group[0] for row in group) for group in firsts.values()),
                    "first-suffix observable mismatch",
                )
                scored[str(fixture["suffix_seed"])] = C.evaluate_fixture(groups, p)
            writer.json(output / "scores.json", scored)
            writer.json(
                output / "file-manifest.json",
                {
                    str(path.relative_to(output)): S.sha(path)
                    for path in sorted(output.rglob("*"))
                    if path.is_file()
                },
            )
            terminal.update(
                status="complete",
                jobs_completed=len(results),
                pairs_completed=768,
                bounded_gate=all(r["bounded_gate"] for r in scored.values()),
            )
    except BaseException as exc:
        terminal.update(
            error_type=type(exc).__name__,
            error=str(exc)[:4096],
            jobs_completed=len(results),
            pairs_completed_lower_bound=sum(r["completed_pairs"] for r in results.values()),
            incomplete_job_methods="Inspect intent/return journals; no zero assumption",
        )
    finally:
        terminal.update(
            aggregate_cpu_seconds=S.cpu_clock(),
            wall_seconds=time.monotonic() - started_wall,
            driver_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            job_costs=costs,
            ordinary_plus_reserved_bytes_before_terminal=writer.total(),
            measurement_failed=writer.measurement_failed,
            terminal_closure_reserve={"cpu_seconds": 2, "wall_seconds": 5},
            quota_kind="projected write admission; not instantaneous filesystem quota",
        )
        if terminal["aggregate_cpu_seconds"] + 2 > 360 or terminal["wall_seconds"] + 5 > 480:
            terminal.update(
                status="failed",
                error_type="ResourceClosureBudget",
                error="terminal closure reserve exceeds aggregate ceiling",
            )
        closure_cpu = min(2, 360 - S.cpu_clock())
        closure_wall = min(5, 480 - (time.monotonic() - started_wall))
        if closure_cpu <= 0 or closure_wall <= 0:
            terminal["status"] = "failed"  # No unbudgeted write; absence means incomplete.
        else:
            with S.deadline(closure_cpu, closure_wall):
                writer.json(output / "result.json", terminal, terminal=True)
    return 0 if terminal["status"] == "complete" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("freeze", "check-freeze"):
        p = subs.add_parser(command)
        p.add_argument("--directory", type=Path, default=FREEZE)
    p = subs.add_parser("worker")
    p.add_argument("--job", type=Path, required=True)
    p.add_argument("--supervisor-fd", type=int)
    p = subs.add_parser("run")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--freeze", type=Path, default=FREEZE)
    for name in ("review", "publication", "approval"):
        p.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.command == "freeze":
        print(json.dumps(freeze(args.directory), sort_keys=True))
        return 0
    if args.command == "check-freeze":
        print(
            json.dumps(
                {
                    "manifest_sha256": S.sha(args.directory / "manifest.json"),
                    "model_calls": 0,
                    "files": len(verify_freeze(args.directory)["sources"]),
                }
            )
        )
        return 0
    if args.command == "worker":
        return worker(args.job, args.supervisor_fd)
    return driver(args)


if __name__ == "__main__":
    raise SystemExit(main())
