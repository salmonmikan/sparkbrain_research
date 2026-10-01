#!/usr/bin/env python3
"""One pre-reviewed, non-evidentiary paired-coverage diagnostic; never an ownership test.

--check-source is model-free. Execution requires an independently published/reviewed
source freeze with schema v05-paired-coverage-runner-freeze-1, protocol_sha256,
runner_sha256 and package_sources_sha256 (every src/sparkbrain/**/*.py file).
The caller supplies its exact SHA-256. Ordinary imports are used, including the
legacy definitions imported by sparkbrain.__init__; the extra freeze binds them.

No retry/resume mode exists. Native value views are incomplete ownership snapshots,
not complete rollback/commit or resumable fixtures. Python audit hooks deny audited
socket/process-launch operations; this is NOT OS-level network isolation. SIGKILL,
OOM or another hard termination may leave partial files and no final manifest.
The reviewed command must include an external 120-second SIGKILL timeout backstop;
Python signal handling alone cannot preempt uninterruptible native calls.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import resource
import signal
import sys
import time
import traceback
from pathlib import Path
from typing import Any

PROTOCOL_PATH = "artifacts/research/v05_paired_coverage_20261001/protocol.json"
PROTOCOL_SHA256 = "09edae7add4210121b699583b935c8ba5b0dd2b382fa8d9d848d6ac0ce6bff25"
ARM_ORDER = ["single", "paired_4ms", "spaced_40ms"]
CONFIG_PATHS = {
    "brain": "config", "base": "base.config", "field": "base.field.config",
    "burst": "base.burst_detector.config", "cascade": "base.cascade_tracker.config",
    "ignition": "base.ignition_gate.config", "base_plasticity": "base.plasticity.config",
    "receptor": "receptors.config", "assembly": "assemblies.config",
    "plasticity": "plasticity.config", "homeostasis": "homeostasis.config",
    "action": "action_policy.config",
}
LIMITS = {
    "address_space_bytes": 512 * 1024**2, "artifact_bytes": 32 * 1024**2,
    "cpu_seconds": 60, "wall_seconds": 120, "fresh_brains": 3,
    "process_episode_attempts": 9, "raw_pulses": 15, "raw_pulses_per_call": 2,
    "native_loads": 0, "outcome_calls": 0, "whole_brain_copies": 0,
}
RESERVE = {"cpu_seconds": 5, "wall_seconds": 10, "artifact_bytes": 4 * 1024**2,
           "address_space_bytes": 2 * 1024**2}


class BindingError(RuntimeError):
    """Source, configuration, or frozen-input binding failed."""


class InvariantError(RuntimeError):
    """An actual runtime invariant failed; this is not a target miss."""


class BudgetError(RuntimeError):
    """Execution budget exhausted; retain partial evidence without retry."""


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str, error: type[Exception] = BindingError) -> None:
    if not condition:
        raise error(message)


def read_protocol(root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    """Validate frozen bytes and all 27 source files without any model import."""
    path = root / PROTOCOL_PATH
    require(digest_file(path) == PROTOCOL_SHA256, "protocol SHA-256 mismatch")
    protocol = json.loads(path.read_text(encoding="utf-8"))
    hashes = protocol["source_files_sha256"]
    require(len(hashes) == 27, "expected exactly 27 protocol source hashes")
    actual = {name: digest_file(root / name) for name in sorted(hashes)}
    require(actual == hashes, "protocol runtime-source hashes mismatch")
    require(protocol["arm_order"] == ARM_ORDER, "arm order mismatch")
    require([arm["arm"] for arm in protocol["arms"]] == ARM_ORDER, "arm table mismatch")
    require(canonical(protocol["limits"]) == canonical(LIMITS), "resource limits mismatch")
    require(set(protocol["configuration"]) == set(CONFIG_PATHS), "12 configs required")
    require([arm["target"] for arm in protocol["arms"]] == [False, True, False],
            "exactly the paired arm must be the target")
    episodes = [episode for arm in protocol["arms"] for episode in arm["episodes"]]
    require(all(len(arm["episodes"]) == 3 for arm in protocol["arms"]), "episode count")
    require(len({episode["episode_id"] for episode in episodes}) == 9, "episode IDs")
    require(sum(len(episode["pulses"]) for episode in episodes) == 15, "pulse total")
    return protocol, actual


def verify_freeze(root: Path, path: Path, expected: str) -> dict[str, Any]:
    """The separate implementation freeze binds ordinary Python import closure."""
    require(digest_file(path) == expected, "implementation-freeze SHA-256 mismatch")
    freeze = json.loads(path.read_text(encoding="utf-8"))
    require(freeze["schema"] == "v05-paired-coverage-runner-freeze-1", "freeze schema")
    require(freeze["protocol_sha256"] == PROTOCOL_SHA256, "freeze protocol binding")
    require(freeze["runner_sha256"] == digest_file(Path(__file__)), "freeze runner binding")
    paths = sorted((root / "src/sparkbrain").rglob("*.py"))
    actual = {path.relative_to(root).as_posix(): digest_file(path) for path in paths}
    require(actual == freeze["package_sources_sha256"], "complete package freeze mismatch")
    return freeze


class EvidenceWriter:
    """Exclusive files; total output quota includes partial files and finalization."""

    def __init__(self, directory: Path) -> None:
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
        self.directory = directory
        self.bytes_written = 0
        self.files: dict[str, bool] = {}
        self.finalizing = False

    def write(self, name: str, value: Any) -> None:
        require(Path(name).name == name, "evidence filenames must be flat")
        ceiling = LIMITS["artifact_bytes"]
        if not self.finalizing:
            ceiling -= RESERVE["artifact_bytes"]
        with (self.directory / name).open("xb", buffering=0) as stream:
            self.files[name] = False
            encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                                       ensure_ascii=False, allow_nan=False)
            for chunk in encoder.iterencode(value):
                data = chunk.encode("utf-8")
                if self.bytes_written + len(data) + 1 > ceiling:
                    raise BudgetError("cumulative artifact budget reached")
                before = stream.tell()
                try:
                    view = memoryview(data)
                    while view:
                        written = stream.write(view)
                        if not written:
                            raise OSError("evidence write made no progress")
                        view = view[written:]
                finally:
                    self.bytes_written += stream.tell() - before
            stream.write(b"\n")
            self.bytes_written += 1
            stream.flush()
            os.fsync(stream.fileno())
            self.files[name] = True

    def manifest(self) -> dict[str, Any]:
        return {
            name: {"sha256": digest_file(self.directory / name),
                   "bytes": (self.directory / name).stat().st_size, "complete_json": complete}
            for name, complete in sorted(self.files.items()) if name != "manifest.json"
        }


class Budget:
    """Linux process limits; finalization is inside, never beyond, the limits."""

    def __init__(self) -> None:
        self.wall_start = time.monotonic()
        self.finalizing = False
        self.memory_reserve: bytearray | None = None

    def install(self) -> None:
        require(sys.platform == "linux", "resource accounting is supported on Linux only")
        resource.setrlimit(resource.RLIMIT_AS,
                           (LIMITS["address_space_bytes"], LIMITS["address_space_bytes"]))
        resource.setrlimit(resource.RLIMIT_CPU,
                           (LIMITS["cpu_seconds"] - RESERVE["cpu_seconds"],
                            LIMITS["cpu_seconds"]))
        signal.signal(signal.SIGXCPU, self._interrupt)
        signal.signal(signal.SIGALRM, self._interrupt)
        signal.setitimer(signal.ITIMER_REAL,
                         LIMITS["wall_seconds"] - RESERVE["wall_seconds"]
                         - (time.monotonic() - self.wall_start))
        self.memory_reserve = bytearray(RESERVE["address_space_bytes"])

    def _interrupt(self, signum: int, _frame: Any) -> None:
        if self.finalizing:
            os._exit(124)  # Hard-stop path intentionally makes no completeness claim.
        self.finish()
        raise BudgetError(f"resource signal {signum}; finalization reserve entered")

    def finish(self) -> None:
        if self.finalizing:
            return
        self.finalizing = True
        self.memory_reserve = None
        resource.setrlimit(resource.RLIMIT_CPU,
                           (LIMITS["cpu_seconds"], LIMITS["cpu_seconds"]))
        remaining = LIMITS["wall_seconds"] - (time.monotonic() - self.wall_start)
        if remaining <= 0:
            os._exit(124)
        signal.setitimer(signal.ITIMER_REAL, remaining)

    def check(self) -> None:
        sample = self.sample()
        if (sample["wall_seconds"] >= LIMITS["wall_seconds"] - RESERVE["wall_seconds"]
                or sample["cpu_seconds"] >= LIMITS["cpu_seconds"] - RESERVE["cpu_seconds"]):
            raise BudgetError("execution reserve boundary reached")

    def sample(self) -> dict[str, Any]:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return {"wall_seconds": time.monotonic() - self.wall_start,
                "cpu_seconds": usage.ru_utime + usage.ru_stime,
                "peak_rss_bytes": usage.ru_maxrss * 1024,
                "address_space_limit_bytes": resource.getrlimit(resource.RLIMIT_AS)[0]}


def deny_network_and_subprocess(event: str, _args: tuple[Any, ...]) -> None:
    """Python audit coverage only; not a sandbox for malicious native extensions."""
    if event.startswith("socket.") or event in {
        "subprocess.Popen", "os.system", "os.posix_spawn", "os.posix_spawnp",
        "os.fork", "os.forkpty", "os.exec", "pty.spawn", "ctypes.dlopen",
    }:
        raise PermissionError(f"Python audit denied {event}")


def actual_configuration(brain: Any) -> dict[str, Any]:
    configs = {}
    for name, path in CONFIG_PATHS.items():
        value = brain
        for part in path.split("."):
            value = getattr(value, part)
        require(dataclasses.is_dataclass(value), f"{name} config is not a dataclass")
        configs[name] = dataclasses.asdict(value)
    return configs


def field_values(brain: Any) -> dict[str, Any]:
    field = brain.base.field
    return {
        "units": [dataclasses.asdict(field.units[key]) for key in sorted(field.units)],
        "connections": [dataclasses.asdict(field.connections[key])
                        for key in sorted(field.connections)],
        "receptor_ids": list(field.receptor_ids),
        "actual_input_routes": list(field.last_input_routes),
        "current_time_ms": field.current_time_ms,
        "last_run_arrivals": field.last_run_arrivals,
        "last_run_spikes": field.last_run_spikes,
    }


def identity_witnesses(brain: Any, retained: list[Any]) -> dict[str, Any]:
    def matches(obj: Any, attribute: str) -> list[dict[str, int]]:
        return [{"result_index": ri, "item_index": ii}
                for ri, result in enumerate(retained)
                for ii, item in enumerate(getattr(result, attribute)) if item is obj]

    pending = brain.pending_activation
    return {
        "basis": "actual Python is comparisons against strongly retained result objects",
        "retained_result_count": len(retained),
        "brain_results_are_retained": len(brain.results) == len(retained)
        and all(a is b for a, b in zip(brain.results, retained, strict=True)),
        "candidate_prototypes": {
            key: {"prototype_object_id": id(candidate.prototype),
                  "pattern_matches": matches(candidate.prototype, "patterns")}
            for key, candidate in sorted(brain.assemblies.candidates.items())
        },
        "pending_object_id": id(pending) if pending is not None else None,
        "pending_activation_matches": matches(pending, "assembly_activations")
        if pending is not None else [],
    }


def field_changes(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    def changed(section: str, keys: tuple[str, ...]) -> list[dict[str, Any]]:
        old = {tuple(row[key] for key in keys): row for row in before[section]}
        new = {tuple(row[key] for key in keys): row for row in after[section]}
        return [{"key": key, "before": old.get(key), "after": new.get(key)}
                for key in sorted(old.keys() | new.keys()) if old.get(key) != new.get(key)]

    return {"changed_units_including_thresholds": changed("units", ("unit_id",)),
            "changed_connections": changed("connections", ("source_id", "target_id"))}


def preserve_observation(writer: EvidenceWriter, prefix: str, brain: Any,
                         retained: list[Any], before: dict[str, Any] | None) -> dict[str, Any]:
    """Separate exclusive files retain earlier components if later inspection fails."""
    writer.write(prefix + "_native.json", {
        "warning": "Incomplete native value view; not complete ownership or resumable snapshot",
        "value": brain.state_dict(),
    })
    field = field_values(brain)
    writer.write(prefix + "_field.json", field)
    if before is not None:
        writer.write(prefix + "_changes.json", field_changes(before, field))
    writer.write(prefix + "_retained_runtime_results.json", {
        "scope": "Raw retained runtime results; may be partial if an attempted call raised",
        "v05_results": [dataclasses.asdict(result) for result in brain.results],
        "v04_results": [dataclasses.asdict(result) for result in brain.base.results],
    })
    candidates = {}
    for key, candidate in sorted(brain.assemblies.candidates.items()):
        complete = dataclasses.asdict(candidate)
        complete["episode_ids"] = sorted(complete["episode_ids"])
        native = candidate.as_dict()
        require(all(name in native and canonical(value) == canonical(native[name])
                    for name, value in complete.items()),
                "candidate serializer omitted/changed declared fields", InvariantError)
        candidates[key] = native
    pending = brain.pending_activation
    witness = identity_witnesses(brain, retained)
    observation = {
        "candidates": candidates,
        "pending_activation": None if pending is None else dataclasses.asdict(pending),
        "pending_action": None if brain.pending_action is None
        else dataclasses.asdict(brain.pending_action),
        "suppressed_assemblies": sorted(brain.assemblies.suppressed),
        "suppressed_units": sorted(brain.suppressed_unit_ids),
        "identity_witnesses": witness,
        "retained_result_episode_ids": [result.metadata["episode_id"] for result in retained],
    }
    writer.write(prefix + "_observations.json", observation)
    return {"field": field, "observation": observation}


def first_episode_gate(observation: dict[str, Any], result: dict[str, Any],
                       mature_episodes: int) -> dict[str, Any]:
    mature_candidates = [key for key, candidate in observation["candidates"].items()
                         if candidate["episode_count"] >= mature_episodes]
    mature_activations = [i for i, row in enumerate(result["assembly_activations"])
                          if row["mature"]]
    passed = not mature_candidates and not mature_activations \
        and observation["pending_activation"] is None
    return {"passed": passed, "mature_candidates": mature_candidates,
            "mature_activation_indices": mature_activations,
            "pending_activation": observation["pending_activation"]}


def target_gate(observation: dict[str, Any], target_ids: list[str]) -> dict[str, Any]:
    pending = observation["pending_activation"]
    key = pending["assembly_id"] if pending is not None else None
    candidate = observation["candidates"].get(key)
    witness = observation["identity_witnesses"]
    prototype_links = witness["candidate_prototypes"].get(key, {}).get("pattern_matches", [])
    checks = {
        "exactly_third_target_episode": observation["retained_result_episode_ids"] == target_ids,
        "actual_pending_present": pending is not None,
        "actual_pending_mature_unsuppressed": pending is not None
        and pending["mature"] is True and pending["suppressed"] is False,
        "resolves_to_candidate": candidate is not None,
        "candidate_exact_three_target_ids": candidate is not None
        and sorted(candidate["episode_ids"]) == sorted(target_ids)
        and candidate["episode_count"] == 3,
        "candidate_prototype_identity": bool(prototype_links),
        "pending_activation_identity": bool(witness["pending_activation_matches"]),
        "result_retention_identity": witness["brain_results_are_retained"],
    }
    return {"covered": all(checks.values()), "checks": checks,
            "pending": pending, "candidate": candidate,
            "prototype_indices": prototype_links,
            "pending_indices": witness["pending_activation_matches"]}


def verify_observation(observation: dict[str, Any], seen_ids: list[str]) -> None:
    require(observation["identity_witnesses"]["brain_results_are_retained"],
            "runtime did not retain the exact returned results", InvariantError)
    require(observation["retained_result_episode_ids"] == seen_ids,
            "retained episode IDs differ", InvariantError)
    require(not observation["suppressed_units"] and not observation["suppressed_assemblies"],
            "unexpected suppression", InvariantError)
    for key, candidate in observation["candidates"].items():
        require(candidate["assembly_id"] == key, "candidate mapping mismatch", InvariantError)
        require(candidate["episode_count"] == len(candidate["episode_ids"])
                and set(candidate["episode_ids"]) <= set(seen_ids),
                "candidate episode independence mismatch", InvariantError)


def exception_record(error: BaseException) -> dict[str, Any]:
    return {"type": type(error).__name__, "message": str(error),
            "traceback": traceback.format_exc()}


def run(root: Path, output: Path, freeze_path: Path, freeze_sha256: str) -> int:
    """Execution entrypoint. Do not call until the exact freeze passes independent review."""
    budget = Budget()
    writer = EvidenceWriter(output)
    counts = {"constructor_attempts": 0, "fresh_brains": 0, "process_episode_attempts": 0,
              "completed_calls": 0, "raw_pulses": 0, "native_loads": 0,
              "whole_brain_copies": 0, "outcome_calls": 0}
    terminal: dict[str, Any] = {"status": "incomplete", "counts": counts}
    brains: list[Any] = []  # Retain every arm, including negative controls.
    retained_by_arm: dict[str, list[Any]] = {}
    coverage = None
    controls = []
    current_prefix = "preflight"
    brain = None
    before = None
    try:
        budget.install()
        sys.addaudithook(deny_network_and_subprocess)
        sys.dont_write_bytecode = True
        # A fresh empty cache prefix forces ordinary imports to compile the frozen .py
        # bytes, rather than accepting an old timestamp-valid .pyc. No cache is written.
        cache = output / "empty_bytecode_cache"
        cache.mkdir(mode=0o700, exist_ok=False)
        sys.pycache_prefix = str(cache)
        require(not any(name == "sparkbrain" or name.startswith("sparkbrain.")
                        for name in sys.modules), "SparkBrain must not be pre-imported")
        protocol, hashes = read_protocol(root)
        freeze = verify_freeze(root, freeze_path, freeze_sha256)
        writer.write("preflight.json", {
            "protocol": protocol, "protocol_sha256": PROTOCOL_SHA256,
            "verified_protocol_source_hashes": hashes, "source_freeze": freeze,
            "source_freeze_sha256": freeze_sha256,
            "python": sys.version, "platform": sys.platform, "uname": list(os.uname()),
            "pid": os.getpid(), "argv": sys.argv,
            "source_root": str(root), "runner_sha256": digest_file(Path(__file__)),
            "limits": LIMITS, "finalization_reserve_inside_limits": RESERVE,
            "network_enforcement": "Python audit denies socket.*, subprocess/process launch and "
            "ctypes.dlopen; not OS network isolation; not a native-extension security sandbox",
            "counts": counts, "resources": budget.sample(),
        })
        budget.check()
        sys.path.insert(0, str(root / "src"))
        # Ordinary imports, after both complete source bindings have been preserved.
        from sparkbrain.v04.contracts import SignalPulse
        from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig
        from sparkbrain.v05.contracts import V05StepResult

        imported = {}
        for name, module in sorted(sys.modules.items()):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                path = Path(module.__file__).resolve()
                relative = path.relative_to(root).as_posix()
                require(relative in freeze["package_sources_sha256"], "unfrozen module imported")
                require(digest_file(path) == freeze["package_sources_sha256"][relative],
                        "imported module source changed")
                imported[name] = relative
        writer.write("imported_sources.json", imported)
        for arm_index, arm in enumerate(protocol["arms"]):
            budget.check()
            current_prefix = f"{arm_index}_{arm['arm']}_initial"
            brain = None
            before = None
            writer.write(current_prefix + "_attempt.json", {
                "counts_before_attempt": counts, "arm": arm["arm"],
                "next_constructor_attempt": counts["constructor_attempts"] + 1,
            })
            counts["constructor_attempts"] += 1
            brain = IntegratedV05Brain(V05BrainConfig(**protocol["configuration"]["brain"]))
            brains.append(brain)
            counts["fresh_brains"] += 1
            retained: list[Any] = []
            retained_by_arm[arm["arm"]] = retained
            configs = actual_configuration(brain)
            writer.write(current_prefix + "_configuration.json", configs)
            require(canonical(configs) == canonical(protocol["configuration"]),
                    "actual constructor configuration differs from all-12 frozen projection")
            writer.write(current_prefix + "_topology.json",
                         dataclasses.asdict(brain.base._topology))
            saved = preserve_observation(writer, current_prefix, brain, retained, None)
            before = saved["field"]
            require(not brain.results and not brain.base.results and not brain.assemblies.candidates
                    and brain.pending_activation is None and brain.current_time_ms == 0.0,
                    "constructor state is not fresh", InvariantError)
            require(len({id(item) for item in brains}) == len(brains),
                    "arm constructors returned the same graph", InvariantError)
            seen_ids: list[str] = []
            for episode_index, episode in enumerate(arm["episodes"]):
                budget.check()
                current_prefix = f"{arm_index}_{arm['arm']}_{episode_index + 1}"
                pulses = tuple(SignalPulse(**row) for row in episode["pulses"])
                require(canonical([pulse.as_dict() for pulse in pulses])
                        == canonical(episode["pulses"]), "actual pulse constructor mismatch")
                writer.write(current_prefix + "_attempt.json", {
                    "episode": episode, "flags": protocol["process_episode_flags"],
                    "counts_before_attempt": counts, "resources": budget.sample(),
                    "next_process_attempt": counts["process_episode_attempts"] + 1,
                    "raw_pulses_in_attempt": len(pulses),
                })
                counts["process_episode_attempts"] += 1
                counts["raw_pulses"] += len(pulses)
                # Exactly one call contains the whole pair. No extra/warm-up/outcome calls.
                result = brain.process_episode(pulses, episode_id=episode["episode_id"],
                                               **protocol["process_episode_flags"])
                retained.append(result)
                counts["completed_calls"] += 1
                raw_result = dataclasses.asdict(result)
                writer.write(current_prefix + "_result.json", raw_result)
                require(type(result) is V05StepResult, "unexpected result type", InvariantError)
                require(canonical(raw_result) == canonical(result.as_dict()),
                        "native result serializer omitted/changed data", InvariantError)
                saved = preserve_observation(writer, current_prefix, brain, retained, before)
                before = saved["field"]
                seen_ids.append(episode["episode_id"])
                observation = saved["observation"]
                verify_observation(observation, seen_ids)
                require(canonical(raw_result["raw_pulses"]) == canonical(episode["pulses"]),
                        "returned inputs differ from frozen episode", InvariantError)
                if episode_index == 0:
                    gate = first_episode_gate(
                        observation, raw_result,
                        protocol["configuration"]["assembly"]["mature_episodes"],
                    )
                    writer.write(current_prefix + "_first_gate.json", gate)
                    require(gate["passed"], "first-episode immaturity failed", InvariantError)
                if arm["target"] and episode_index == 2:
                    coverage = target_gate(observation, seen_ids)
                    writer.write(current_prefix + "_target_gate.json", coverage)
                if not arm["target"]:
                    controls.append({"arm": arm["arm"], "episode_id": episode["episode_id"],
                                     "patterns": len(raw_result["patterns"]),
                                     "candidates": len(observation["candidates"]),
                                     "activations": len(raw_result["assembly_activations"])})
        require(counts == {"constructor_attempts": 3, "fresh_brains": 3,
                           "process_episode_attempts": 9, "completed_calls": 9,
                           "raw_pulses": 15, "native_loads": 0,
                           "whole_brain_copies": 0, "outcome_calls": 0},
                "finite plan counts differ", InvariantError)
        budget.check()
        require(coverage is not None, "target gate missing", InvariantError)
        controls_expected = all(
            row["patterns"] == row["candidates"] == row["activations"] == 0
            for row in controls
        )
        terminal.update({"status": "target_coverage_present" if coverage["covered"]
                         else "coverage_blocked", "target_gate": coverage,
                         "control_characterization": controls,
                         "controls_match_expected_zero_activity": controls_expected,
                         "timing_contrast_interpretation":
                         "expected_descriptive_contrast_present"
                         if coverage["covered"] and controls_expected else "unsupported",
                         "scientific_credit": 0,
                         "classification": protocol["classification"]})
    except BaseException as error:
        budget.finish()
        writer.finalizing = True
        terminal.update({"status": "stopped", "failure": exception_record(error),
                         "failure_stage": current_prefix, "target_gate_if_observed": coverage,
                         "control_characterization_so_far": controls})
        # Best effort only: never retry a model call or overwrite an existing raw component.
        try:
            writer.write("terminal_error.json", terminal["failure"])
            if brain is not None:
                retained = retained_by_arm.get(ARM_ORDER[len(brains) - 1], [])
                preserve_observation(writer, "failure_partial", brain, retained, before)
        except BaseException as inspection_error:
            terminal["partial_preservation_error"] = exception_record(inspection_error)
    finally:
        budget.finish()
        writer.finalizing = True
        terminal["resources_before_final_files"] = budget.sample()
        terminal["artifact_bytes_before_final_files"] = writer.bytes_written
        terminal["no_retry"] = True
        terminal["native_views_are_complete_ownership_snapshots"] = False
        try:
            writer.write("terminal.json", terminal)
            writer.write("manifest.json", {"files": writer.manifest(),
                                           "manifest_excludes_itself": True,
                                           "resources_before_manifest": budget.sample()})
        except BaseException as final_error:
            print(f"Finalization incomplete: {type(final_error).__name__}: {final_error}",
                  file=sys.stderr)
            return 2
    return 0 if terminal["status"] in {"target_coverage_present", "coverage_blocked"} else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-source", action="store_true", help="Never import SparkBrain")
    parser.add_argument("--run-reviewed", action="store_true", help="Execute once after review")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-freeze", type=Path)
    parser.add_argument("--source-freeze-sha256")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check_source == args.run_reviewed:
        parser.error("choose exactly one of --check-source or --run-reviewed")
    if bool(args.source_freeze) != bool(args.source_freeze_sha256):
        parser.error("source freeze path and SHA-256 must be supplied together")
    if args.check_source:
        _, hashes = read_protocol(root)
        if args.source_freeze:
            verify_freeze(root, args.source_freeze, args.source_freeze_sha256)
        require(not any(name == "sparkbrain" or name.startswith("sparkbrain.")
                        for name in sys.modules), "source check imported SparkBrain")
        print(canonical({"status": "source_check_passed", "source_files": len(hashes),
                         "protocol_sha256": PROTOCOL_SHA256,
                         "complete_package_freeze_checked": bool(args.source_freeze),
                         "model_imported": False}))
        return 0
    if not args.output or not args.source_freeze:
        parser.error("reviewed execution requires --output and the exact source freeze")
    return run(root, args.output.resolve(), args.source_freeze.resolve(), args.source_freeze_sha256)


if __name__ == "__main__":
    raise SystemExit(main())
