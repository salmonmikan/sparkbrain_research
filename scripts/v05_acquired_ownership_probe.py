#!/usr/bin/env python3
"""PR180 acquired-state ownership diagnostic, NONCANONICAL / NON_EVIDENTIARY.

This module and --check-source are model-free. Only --run-reviewed enters model
paths, after binding every package source, protocol, schema, runner and test.
No prior runner is imported. GraphAudit is adapted by source copy from PR176's
scripts/v05_owned_state_probe.py: exact types/fields, ordered containers, reference
tracking and mutable-identity isolation. Resource/writer/configuration patterns
are source copies from scripts/v05_paired_coverage_probe.py (PR177), with explicit
separate freeze binding below. Neither prior scientific result is rerun or upgraded.

Required external command: timeout -s KILL 120s python -B THIS_SCRIPT
--run-reviewed --output FRESH_DIR --source-freeze FREEZE --source-freeze-sha256 SHA.
An actual Linux timeout parent is required. Python audit socket/process denial is
NOT OS network isolation. SIGKILL/OOM can prevent finalization. No retry/resume.
"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import hashlib
import importlib
import json
import math
import os
import resource
import signal
import sys
import time
import traceback
from collections import deque
from pathlib import Path
from typing import Any

PROTOCOL_PATH = "artifacts/research/v05_acquired_ownership_20261001/protocol.json"
PROTOCOL_SHA256 = "723859ed058957a4bf832ef09a8b42407e5fde3b0a5d8186de1edcd5f39c0a3f"
SCHEMA_PATH = "artifacts/research/v05_owned_state_20261001/source_map.json"
SCHEMA_SHA256 = "af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69"
SOURCE_PIN = "9549a2bf6bc76cb7b5714742f3ed54decd618263"
IMPLEMENTATION_PATHS = {
    "scripts/v05_acquired_ownership_probe.py",
    "tests/test_v05_acquired_ownership_runner.py",
}
REUSE_PATHS = {"scripts/v05_owned_state_probe.py", "scripts/v05_paired_coverage_probe.py"}
BRANCHES = ["export_abort", "event_cap_abort", "direct_reference", "commit"]
CONFIG_PATHS = {
    "brain": "config",
    "base": "base.config",
    "field": "base.field.config",
    "burst": "base.burst_detector.config",
    "cascade": "base.cascade_tracker.config",
    "ignition": "base.ignition_gate.config",
    "base_plasticity": "base.plasticity.config",
    "receptor": "receptors.config",
    "assembly": "assemblies.config",
    "plasticity": "plasticity.config",
    "homeostasis": "homeostasis.config",
    "action": "action_policy.config",
}
LIMITS = {
    "address_space_bytes": 536870912,
    "artifact_bytes": 33554432,
    "cpu_seconds": 60,
    "wall_seconds": 120,
    "fresh_roots": 1,
    "whole_brain_copy_attempts": 4,
    "process_attempts": 7,
    "submitted_raw_pulses": 14,
    "native_loads": 0,
    "outcome_calls": 0,
}
COUNTS = {
    "aborted_transactions": 2,
    "expected_processing_exceptions": 1,
    "fresh_roots": 1,
    "owner_commits": 1,
    "process_attempts": 7,
    "process_returns": 6,
    "submitted_raw_pulses": 14,
    "whole_brain_copy_attempts": 4,
}
RESERVE = {
    "cpu_seconds": 5,
    "wall_seconds": 10,
    "artifact_bytes": 4 * 1024**2,
    "address_space_bytes": 2 * 1024**2,
}


class BindingError(RuntimeError):
    """Source, configuration or bounded-input contract mismatch."""


class InvariantError(RuntimeError):
    """Graph, identity, isolation or transaction invariant mismatch."""


class CoverageBlocked(RuntimeError):
    """Required mature state is absent; stop with no additional acquisition."""


class BudgetError(RuntimeError):
    """Stop within the fixed caps, preserving partial evidence."""


class InjectedExportValidationError(RuntimeError):
    """Deliberate postprocessing/export-boundary fault, not a runtime defect."""


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str, error: type[Exception] = BindingError) -> None:
    if not condition:
        raise error(message)


def package_hashes(root: Path) -> dict[str, str]:
    paths = sorted((root / "src/sparkbrain").rglob("*.py"))
    return {path.relative_to(root).as_posix(): digest_file(path) for path in paths}


def read_protocol(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    require(digest_file(root / PROTOCOL_PATH) == PROTOCOL_SHA256, "protocol SHA mismatch")
    protocol = json.loads((root / PROTOCOL_PATH).read_text(encoding="utf-8"))
    require(protocol["source_pin"] == SOURCE_PIN, "source pin mismatch")
    require(len(protocol["package_sources_sha256"]) == 157, "157 source bindings required")
    require(
        package_hashes(root) == protocol["package_sources_sha256"],
        "complete package source mismatch",
    )
    require(protocol["limits"] == LIMITS, "limit mismatch")
    require(protocol["complete_run_counts"] == COUNTS, "count mismatch")
    require([b["name"] for b in protocol["branches"]] == BRANCHES, "branch order mismatch")
    require(set(protocol["configuration"]) == set(CONFIG_PATHS), "twelve configs required")
    require(digest_file(root / SCHEMA_PATH) == SCHEMA_SHA256, "graph schema SHA mismatch")
    schema = json.loads((root / SCHEMA_PATH).read_text(encoding="utf-8"))
    require(len(schema["files"]) == 16, "sixteen graph-schema files required")
    require(
        sum(len(row["classes"]) for row in schema["files"].values()) == 50,
        "fifty graph-schema classes required",
    )
    for name, row in schema["files"].items():
        require(
            row["sha256"] == protocol["package_sources_sha256"][name],
            "schema/runtime source mismatch",
        )
        require(
            all(not cls["custom_copy_hooks"] for cls in row["classes"].values()),
            "schema contains unsupported copy hooks",
        )
    return protocol, schema


def verify_freeze(root: Path, path: Path, expected: str) -> dict[str, Any]:
    require(digest_file(path) == expected, "implementation-freeze SHA mismatch")
    frozen = json.loads(path.read_text(encoding="utf-8"))
    require(frozen["schema"] == "v05-acquired-ownership-runner-freeze-1", "freeze schema")
    require(frozen["protocol_sha256"] == PROTOCOL_SHA256, "freeze protocol binding")
    require(frozen["graph_schema_sha256"] == SCHEMA_SHA256, "freeze schema binding")
    require(
        set(frozen["implementation_sources_sha256"]) == IMPLEMENTATION_PATHS,
        "freeze must bind exactly the dedicated runner and model-free tests",
    )
    for name, sha in frozen["implementation_sources_sha256"].items():
        require(digest_file(root / name) == sha, f"implementation drift: {name}")
    require(
        digest_file(Path(__file__))
        == frozen["implementation_sources_sha256"]["scripts/v05_acquired_ownership_probe.py"],
        "executed runner differs from freeze",
    )
    require(set(frozen["reuse_sources_sha256"]) == REUSE_PATHS, "reuse provenance inventory")
    for name, sha in frozen["reuse_sources_sha256"].items():
        require(digest_file(root / name) == sha, f"reuse source drift: {name}")
    require(
        package_hashes(root) == frozen["package_sources_sha256"], "freeze complete package mismatch"
    )
    require(
        frozen["external_timeout_argv"] == ["timeout", "-s", "KILL", "120s"],
        "freeze timeout contract mismatch",
    )
    return frozen


def verify_timeout_parent() -> dict[str, Any]:
    parent = os.getppid()
    argv = Path(f"/proc/{parent}/cmdline").read_bytes().split(b"\0")
    words = [word.decode() for word in argv if word]
    require(
        len(words) >= 6
        and Path(words[0]).name == "timeout"
        and words[1:4] == ["-s", "KILL", "120s"],
        "execution requires actual timeout -s KILL 120s parent",
    )
    return {
        "parent_pid": parent,
        "parent_argv": words,
        "limitation": "Hard kill may leave partial artifacts and no final manifest",
    }


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
        with (self.directory / name).open("xb", buffering=65536) as stream:
            self.files[name] = False
            encoder = json.JSONEncoder(
                sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
            )
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
            name: {
                "sha256": digest_file(self.directory / name),
                "bytes": (self.directory / name).stat().st_size,
                "complete_json": complete,
            }
            for name, complete in sorted(self.files.items())
            if name != "manifest.json"
        }


class Budget:
    """Linux process limits; finalization is inside, never beyond, the limits."""

    def __init__(self) -> None:
        self.wall_start = time.monotonic()
        self.finalizing = False
        self.memory_reserve: bytearray | None = None

    def install(self) -> None:
        require(sys.platform == "linux", "resource accounting is supported on Linux only")
        resource.setrlimit(
            resource.RLIMIT_AS, (LIMITS["address_space_bytes"], LIMITS["address_space_bytes"])
        )
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (LIMITS["cpu_seconds"] - RESERVE["cpu_seconds"], LIMITS["cpu_seconds"]),
        )
        signal.signal(signal.SIGXCPU, self._interrupt)
        signal.signal(signal.SIGALRM, self._interrupt)
        signal.setitimer(
            signal.ITIMER_REAL,
            LIMITS["wall_seconds"] - RESERVE["wall_seconds"] - (time.monotonic() - self.wall_start),
        )
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
        resource.setrlimit(resource.RLIMIT_CPU, (LIMITS["cpu_seconds"], LIMITS["cpu_seconds"]))
        remaining = LIMITS["wall_seconds"] - (time.monotonic() - self.wall_start)
        if remaining <= 0:
            os._exit(124)
        signal.setitimer(signal.ITIMER_REAL, remaining)

    def check(self) -> None:
        sample = self.sample()
        if (
            sample["wall_seconds"] >= LIMITS["wall_seconds"] - RESERVE["wall_seconds"]
            or sample["cpu_seconds"] >= LIMITS["cpu_seconds"] - RESERVE["cpu_seconds"]
        ):
            raise BudgetError("execution reserve boundary reached")

    def sample(self) -> dict[str, Any]:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return {
            "wall_seconds": time.monotonic() - self.wall_start,
            "cpu_seconds": usage.ru_utime + usage.ru_stime,
            "peak_rss_bytes": usage.ru_maxrss * 1024,
            "address_space_limit_bytes": resource.getrlimit(resource.RLIMIT_AS)[0],
        }


def deny_network_and_subprocess(event: str, _args: tuple[Any, ...]) -> None:
    """Python audit coverage only; not a sandbox for malicious native extensions."""
    if event.startswith("socket.") or event in {
        "subprocess.Popen",
        "os.system",
        "os.posix_spawn",
        "os.posix_spawnp",
        "os.fork",
        "os.forkpty",
        "os.exec",
        "pty.spawn",
        "ctypes.dlopen",
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


class GraphAudit:
    """PR176 GraphAudit adapted to an explicit node table for partial preservation.

    The typed/reference oracle retains order for dictionaries, sequences and deques,
    set membership (canonicalized only in the inventory), and every declared field.
    Node IDs are traversal labels, never Python object IDs or native state hashes.
    """

    def __init__(self, allowed: dict[type, set[str]]) -> None:
        self.allowed = allowed
        self.partial: dict[str, Any] = {}
        self.paths: dict[int, str] = {}
        self.mutable: set[int] = set()

    @classmethod
    def from_schema(cls, schema: dict[str, Any]) -> GraphAudit:
        # Called only inside reviewed execution, after complete source/freeze binding.
        allowed = {}
        for path, record in schema["files"].items():
            module = importlib.import_module(
                path.removeprefix("src/").removesuffix(".py").replace("/", ".")
            )
            for name, row in record["classes"].items():
                actual = getattr(module, name)
                require(actual.__module__ == module.__name__, "schema class origin mismatch")
                for hook in ("__copy__", "__deepcopy__", "__reduce__", "__reduce_ex__"):
                    require(
                        getattr(actual, hook, None) is getattr(object, hook, None),
                        f"unsupported custom copy hook: {actual.__name__}.{hook}",
                    )
                allowed[actual] = set(row["declared_fields"])
        return cls(allowed)

    def inspect(self, root: object, label: str = "brain") -> tuple[dict[str, Any], set[int]]:
        seen: dict[int, int] = {}
        self.paths, self.mutable = {}, set()
        nodes: list[dict[str, Any]] = []
        self.partial = {
            "format": "typed-reference-graph-1",
            "nodes": nodes,
            "root": None,
            "complete": False,
        }

        def visit(value: object, path: str) -> Any:
            kind = type(value)
            if value is None or kind in (bool, int, str):
                return [kind.__name__, value]
            if kind is float:
                require(math.isfinite(value), f"nonfinite graph value at {path}", InvariantError)
                return ["float", value]
            require(
                kind in (dict, list, tuple, set, deque) or kind in self.allowed,
                f"unsupported graph type at {path}: {kind.__module__}.{kind.__name__}",
                InvariantError,
            )
            identity = id(value)
            if identity in seen:
                return {"ref": seen[identity]}
            index = len(nodes)
            seen[identity], self.paths[identity] = index, path
            if kind is not tuple:
                self.mutable.add(identity)
            row: dict[str, Any] = {"node": index, "path": path}
            nodes.append(row)  # Attach before descent; partial traversals remain available.
            if kind is dict:
                row.update(type="dict", items=[])
                for i, (key, item) in enumerate(value.items()):
                    pair: list[Any] = []
                    row["items"].append(pair)
                    pair.append(visit(key, f"{path}.key[{i}]"))
                    pair.append(visit(item, f"{path}.value[{i}]"))
            elif kind in (list, tuple, deque):
                row.update(type=kind.__name__, items=[])
                if kind is deque:
                    row["maxlen"] = value.maxlen
                for i, item in enumerate(value):
                    row["items"].append(visit(item, f"{path}[{i}]"))
            elif kind is set:
                row.update(type="set", items=[])
                require(
                    all(
                        type(item) in (str, int)
                        or (
                            type(item) is tuple
                            and len(item) == 2
                            and all(type(v) is int for v in item)
                        )
                        for item in value
                    ),
                    f"unsupported set elements at {path}",
                    InvariantError,
                )
                for i, item in enumerate(
                    sorted(value, key=lambda v: (type(v).__name__, canonical(v)))
                ):
                    row["items"].append(visit(item, f"{path}.set[{i}]"))
            else:
                row.update(type=f"{kind.__module__}.{kind.__name__}", fields={})
                names = (
                    set(vars(value))
                    if hasattr(value, "__dict__")
                    else {field.name for field in dataclasses.fields(value)}
                )
                row["observed_fields"] = sorted(names)
                require(
                    names == self.allowed[kind], f"unknown/missing fields at {path}", InvariantError
                )
                for name in sorted(names):
                    row["fields"][name] = visit(getattr(value, name), f"{path}.{name}")
            return {"ref": index}

        self.partial["root"] = visit(root, label)
        self.partial["complete"] = True
        return self.partial, set(self.mutable)


def primitive_tree(value: Any) -> dict[int, str]:
    """Reject handles, subclasses, cycles and aliases in the outward JSON tree."""
    mutable: dict[int, str] = {}

    def visit(item: Any, path: str) -> None:
        kind = type(item)
        if item is None or kind in (bool, int, str):
            return
        if kind is float:
            require(math.isfinite(item), "nonfinite export", InvariantError)
            return
        require(kind in (dict, list), f"nonprimitive export at {path}", InvariantError)
        require(id(item) not in mutable, f"aliased/cyclic export at {path}", InvariantError)
        mutable[id(item)] = path
        if kind is dict:
            require(all(type(key) is str for key in item), "nonstring export key", InvariantError)
            for key, child in item.items():
                visit(child, f"{path}.{key}")
        else:
            for i, child in enumerate(item):
                visit(child, f"{path}[{i}]")

    visit(value, "export")
    return mutable


def pulse_guard(pulses: Any, pulse_type: type, episode: dict[str, Any]) -> None:
    require(type(pulses) is tuple and len(pulses) == 2, "exact two-pulse tuple required")
    for pulse, expected in zip(pulses, episode["pulses"], strict=True):
        require(type(pulse) is pulse_type, "exact SignalPulse class required")
        require(
            type(pulse.metadata) is dict and not pulse.metadata, "empty actual metadata required"
        )
        require(
            {field.name for field in dataclasses.fields(pulse)} == set(expected),
            "pulse field inventory differs",
        )
        for name, value in expected.items():
            actual = getattr(pulse, name)
            require(
                type(actual) is type(value) and actual == value,
                f"frozen pulse field mismatch: {name}",
            )


def identity_witnesses(brain: Any) -> dict[str, Any]:
    """Readable source-backed object paths; equality never substitutes for `is`."""
    results, base_results = brain.results, brain.base.results
    field, topology = brain.base.field, brain.base._topology

    def matches(value: Any, attribute: str) -> list[str]:
        return [
            f"brain.results[{ri}].{attribute}[{i}]"
            for ri, result in enumerate(results)
            for i, item in enumerate(getattr(result, attribute))
            if item is value
        ]

    edges = []
    for key, edge in field.connections.items():
        edges.append(
            {
                "connection_key": list(key),
                "outgoing_paths": [
                    f"brain.base.field.outgoing[{edge.source_id}][{i}]"
                    for i, row in enumerate(field.outgoing[edge.source_id])
                    if row is edge
                ],
                "incoming_paths": [
                    f"brain.base.field.incoming[{edge.target_id}][{i}]"
                    for i, row in enumerate(field.incoming[edge.target_id])
                    if row is edge
                ],
            }
        )
    buffers = [
        (f"brain.base.burst_detector._window[{i}]", item)
        for i, item in enumerate(brain.base.burst_detector._window)
    ]
    buffers += [
        (f"brain.base.cascade_tracker._pending[{i}]", item)
        for i, item in enumerate(brain.base.cascade_tracker._pending)
    ]
    return {
        "basis": "Live `is` checks, supported by full typed/reference inventories",
        "sources": {
            "runtime": "src/sparkbrain/v05/brain.py:154-244",
            "field": "src/sparkbrain/v04/field.py:85-110",
            "detectors": "src/sparkbrain/v04/dynamics.py",
            "memory": "src/sparkbrain/v05/assemblies.py",
        },
        "candidate_prototypes": {
            key: {
                "source": f"brain.assemblies.candidates[{key!r}].prototype",
                "retained_paths": matches(candidate.prototype, "patterns"),
            }
            for key, candidate in brain.assemblies.candidates.items()
        },
        "pending_activation_paths": matches(brain.pending_activation, "assembly_activations")
        if brain.pending_activation is not None
        else [],
        "pending_action_paths": [
            f"brain.results[{i}].action"
            for i, result in enumerate(results)
            if brain.pending_action is result.action
        ],
        "v04_result_links": [
            {
                "source": f"brain.results[{i}].v04_result",
                "retained_paths": [
                    f"brain.base.results[{j}]"
                    for j, row in enumerate(base_results)
                    if result.v04_result is row
                ],
            }
            for i, result in enumerate(results)
        ],
        "emitted_input_links": [
            {
                "source": f"brain.results[{i}].emitted_pulses[{j}]",
                "retained_paths": [
                    f"brain.base.results[{bi}].input_pulses[{pi}]"
                    for bi, base in enumerate(base_results)
                    for pi, pulse in enumerate(base.input_pulses)
                    if pulse is emitted
                ],
            }
            for i, result in enumerate(results)
            for j, emitted in enumerate(result.emitted_pulses)
        ],
        "buffered_spike_links": [
            {
                "source": path,
                "retained_paths": [
                    f"brain.base.results[{ri}].spikes[{si}]"
                    for ri, result in enumerate(base_results)
                    for si, spike in enumerate(result.spikes)
                    if spike is buffered
                ],
            }
            for path, buffered in buffers
        ],
        "connection_links": edges,
        "cascade_memory_link": {
            "source": "brain.base.cascade_tracker.memory",
            "target": "brain.base.assembly_memory",
            "same_object": brain.base.cascade_tracker.memory is brain.base.assembly_memory,
        },
        "topology_unit_separation": [
            {
                "initial_path": f"brain.base._topology.units[{i}]",
                "live_path": f"brain.base.field.units[{row.unit_id}]",
                "separate": row is not field.units[row.unit_id],
            }
            for i, row in enumerate(topology.units)
        ],
        "topology_connection_separation": [
            {
                "initial_path": f"brain.base._topology.connections[{i}]",
                "live_key": [row.source_id, row.target_id],
                "separate": row is not field.connections[(row.source_id, row.target_id)],
            }
            for i, row in enumerate(topology.connections)
        ],
    }


def mature_gate(brain: Any, expected_ids: list[str]) -> dict[str, Any]:
    pending = brain.pending_activation
    candidate = None if pending is None else brain.assemblies.candidates.get(pending.assembly_id)
    witnesses = identity_witnesses(brain)
    checks = {
        "exact_retained_episodes": [r.metadata["episode_id"] for r in brain.results]
        == expected_ids,
        "actual_mature_unsuppressed_pending": pending is not None
        and pending.mature is True
        and pending.suppressed is False,
        "exact_candidate_episode_set": candidate is not None
        and candidate.episode_ids == set(expected_ids)
        and candidate.episode_count == len(expected_ids),
        "pending_in_newest_result": bool(brain.results)
        and pending is not None
        and any(pending is row for row in brain.results[-1].assembly_activations),
        "prototype_in_retained_result": candidate is not None
        and bool(witnesses["candidate_prototypes"][pending.assembly_id]["retained_paths"]),
        "no_suppression": not brain.assemblies.suppressed and not brain.suppressed_unit_ids,
    }
    return {
        "covered": all(checks.values()),
        "checks": checks,
        "expected_episode_ids": expected_ids,
        "pending_activation_paths": witnesses["pending_activation_paths"],
        "candidate_prototype": None
        if candidate is None
        else witnesses["candidate_prototypes"][pending.assembly_id],
    }


def clocks_and_fault_state(brain: Any) -> dict[str, Any]:
    field = brain.base.field
    return {
        "field_end_ms": field.current_time_ms,
        "receptor_Q": None
        if "Q" not in brain.receptors.channels
        else dataclasses.asdict(brain.receptors.channels["Q"]),
        "unit_clocks": [
            {
                "unit_id": unit.unit_id,
                "last_update_ms": unit.last_update_ms,
                "last_spike_ms": unit.last_spike_ms,
                "refractory_until_ms": unit.refractory_until_ms,
            }
            for unit in field.units.values()
        ],
        "candidate_clocks": [
            {
                "assembly_id": candidate.assembly_id,
                "first_seen_ms": candidate.first_seen_ms,
                "last_seen_ms": candidate.last_seen_ms,
            }
            for candidate in brain.assemblies.candidates.values()
        ],
        "queue_heap_layout": [
            {"time_ms": time_ms, "counter": counter, "arrival": dataclasses.asdict(arrival)}
            for time_ms, counter, arrival in field._queue
        ],
        "queue_counter": field._counter,
        "total_arrivals": field.total_arrivals,
        "last_run_arrivals": field.last_run_arrivals,
        "total_spikes": field.total_spikes,
        "last_run_spikes": field.last_run_spikes,
    }


def exception_record(error: BaseException) -> dict[str, Any]:
    return {
        "type": type(error).__name__,
        "message": str(error),
        "traceback": "".join(traceback.format_exception(error)),
    }


class PrivateOwner:
    """Prototype private pointer, with no public live-state getter."""

    __slots__ = ("_brain",)

    def __init__(self, brain: Any) -> None:
        self._brain = brain

    def transact(self, prepare: Any) -> Any:
        # All fallible work is in prepare. These final two lines are the commit boundary.
        candidate, detached_output = prepare()
        self._brain = candidate
        return detached_output


class Probe:
    """One fixed acquisition, four retained clones, no retries or reconstruction."""

    def __init__(
        self,
        spec: dict[str, Any],
        audit: GraphAudit,
        writer: EvidenceWriter,
        budget: Budget,
        pulse_type: type,
        result_type: type,
    ) -> None:
        self.spec, self.audit, self.writer, self.budget = spec, audit, writer, budget
        self.pulse_type, self.result_type = pulse_type, result_type
        self.counts = dict.fromkeys(COUNTS, 0)
        self.counts.update(native_loads=0, outcome_calls=0)
        self.graph_files: dict[str, str] = {}
        self.brains: dict[str, Any] = {}
        self.callers: dict[str, Any] = {}
        self.owned_inputs: dict[str, Any] = {}
        self.returned_results: list[Any] = []
        self.outputs: dict[str, Any] = {}
        self.stage = "before_constructor"
        self.owner: PrivateOwner | None = None
        self.returned = False
        self.constructor_attempts = 0

    def bump(self, name: str, amount: int = 1) -> None:
        require(self.counts[name] + amount <= COUNTS[name], f"count ceiling: {name}", BudgetError)
        self.counts[name] += amount

    def capture(self, label: str, value: Any, root_name: str = "brain") -> dict[str, Any]:
        try:
            inventory, mutable = self.audit.inspect(value, root_name)
        except BaseException as error:
            self.writer.write(label + "-partial-graph.json", self.audit.partial)
            self.writer.write(label + "-graph-error.json", exception_record(error))
            raise
        data = canonical(inventory).encode("utf-8")
        sha = hashlib.sha256(data).hexdigest()
        if sha not in self.graph_files:
            filename = "graph-" + sha + ".json"
            self.writer.write(filename, inventory)
            self.graph_files[sha] = filename
        self.writer.write(
            label + "-graph.json",
            {
                "inventory_file": self.graph_files[sha],
                "inventory_sha256": sha,
                "oracle": "exact complete typed/reference bytes; hashes only address stored bytes",
                "node_count": len(inventory["nodes"]),
                "mutable_identity_count": len(mutable),
            },
        )
        return {"bytes": data, "sha256": sha, "mutable": mutable, "paths": dict(self.audit.paths)}

    def observe(self, label: str, brain: Any) -> dict[str, Any]:
        state = self.capture(label, brain)
        witness = identity_witnesses(brain)
        self.writer.write(
            label + "-observations.json",
            {
                "clocks_and_processing": clocks_and_fault_state(brain),
                "identity": witness,
                "candidate_episode_sets": {
                    key: sorted(c.episode_ids) for key, c in brain.assemblies.candidates.items()
                },
            },
        )
        require(
            all(
                row["outgoing_paths"] and row["incoming_paths"]
                for row in witness["connection_links"]
            ),
            "live edge alias failure",
            InvariantError,
        )
        require(
            witness["cascade_memory_link"]["same_object"], "memory alias failure", InvariantError
        )
        require(
            all(
                row["separate"]
                for row in witness["topology_unit_separation"]
                + witness["topology_connection_separation"]
            ),
            "initial topology/live state alias",
            InvariantError,
        )
        require(
            all(
                row["retained_paths"] == [f"brain.base.results[{i}]"]
                for i, row in enumerate(witness["v04_result_links"])
            ),
            "v05/base result identity mismatch",
            InvariantError,
        )
        require(
            all(row["retained_paths"] for row in witness["emitted_input_links"]),
            "emitted/base input identity mismatch",
            InvariantError,
        )
        return state

    def original_exact(self, label: str, before: dict[str, Any]) -> None:
        require(
            self.owner is not None and self.owner._brain is self.brains["root"],
            "owner changed before commit",
            InvariantError,
        )
        current = self.capture(label + "-original", self.brains["root"])
        self.writer.write(
            label + "-original-equality.json",
            {
                "exact_typed_bytes_equal": current["bytes"] == before["bytes"],
                "owner_is_original_root": True,
                "before_inventory": before["sha256"],
                "current_inventory": current["sha256"],
            },
        )
        require(current["bytes"] == before["bytes"], "original graph changed", InvariantError)

    def step(self, brain: Any, episode: dict[str, Any], label: str) -> tuple[Any, dict[str, Any]]:
        self.stage = label
        self.budget.check()
        callers = tuple(self.pulse_type(**row) for row in episode["pulses"])
        self.callers[label] = (
            callers  # Retain the actual SignalPulse objects, not constructor dicts.
        )
        pulse_guard(callers, self.pulse_type, episode)
        caller_graph = self.capture(label + "-caller", callers, "caller")
        owned = copy.deepcopy(callers, {})
        self.owned_inputs[label] = owned
        pulse_guard(owned, self.pulse_type, episode)
        owned_graph = self.capture(label + "-detached-input", owned, "caller")
        self.writer.write(
            label + "-input-detachment.json",
            {
                "complete_typed_bytes_equal": caller_graph["bytes"] == owned_graph["bytes"],
                "shared_mutable_paths": [
                    caller_graph["paths"][key]
                    for key in caller_graph["mutable"] & owned_graph["mutable"]
                ],
            },
        )
        require(
            caller_graph["bytes"] == owned_graph["bytes"]
            and not caller_graph["mutable"] & owned_graph["mutable"],
            "input detachment failed",
            InvariantError,
        )
        self.writer.write(
            label + "-attempt.json",
            {
                "episode": episode,
                "flags": self.spec["process_episode_flags"],
                "counts_before": self.counts,
                "resources": self.budget.sample(),
            },
        )
        self.bump("process_attempts")
        self.bump("submitted_raw_pulses", 2)
        try:
            result = brain.process_episode(
                owned,
                episode_id=episode["episode_id"],
                **copy.deepcopy(self.spec["process_episode_flags"]),
            )
        except BaseException as error:
            # Preserve the real call exception before inspection, gates or summaries.
            self.writer.write(label + "-processing-error.json", exception_record(error))
            self.observe(label + "-after-processing-error", brain)
            raise
        self.bump("process_returns")
        self.returned_results.append(result)
        # Complete typed raw return precedes export, validation and coverage gates.
        self.capture(label + "-raw-return", result, "result")
        state = self.observe(label + "-after-return", brain)
        require(type(result) is self.result_type, "unexpected result type", InvariantError)
        require(
            brain.results[-1] is result and brain.base.results[-1] is result.v04_result,
            "actual result was not retained",
            InvariantError,
        )
        require(
            canonical([p.as_dict() for p in result.raw_pulses]) == canonical(episode["pulses"]),
            "raw result inputs differ",
            InvariantError,
        )
        require(
            all(any(item is pulse for item in result.raw_pulses) for pulse in owned),
            "retained input does not bind detached caller",
            InvariantError,
        )
        live_graph, live_ids = self.audit.inspect(brain)
        del live_graph
        caller_ids = self.audit.inspect(callers, "caller")[1]
        require(not live_ids & caller_ids, "caller mutable input leaked into graph", InvariantError)
        return result, state

    def detached(self, label: str, result: Any, brain: Any) -> Any:
        raw = dataclasses.asdict(result)
        self.writer.write(label + "-raw-values.json", raw)
        native = result.as_dict()
        require(
            canonical(raw) == canonical(native), "output serializer lost fields", InvariantError
        )
        output = json.loads(canonical(native))
        self.outputs[label] = output
        export_ids = primitive_tree(output)
        live_ids = self.audit.inspect(brain)[
            1
        ]  # Recompute live IDs, never compare stale snapshots.
        shared = set(export_ids) & live_ids
        self.writer.write(label + "-export.json", output)
        self.writer.write(
            label + "-export-isolation.json",
            {
                "mutable_export_paths": list(export_ids.values()),
                "shared_mutable_export_paths": [export_ids[key] for key in shared],
                "source": "src/sparkbrain/v05/contracts.py:114-129; JSON detached tree",
            },
        )
        require(not shared, "mutable output leaked owned graph", InvariantError)
        return output

    def coverage(self, label: str, brain: Any, ids: list[str]) -> None:
        gate = mature_gate(brain, ids)
        self.writer.write(label + "-maturity-gate.json", gate)
        require(gate["covered"], label + ": actual mature pending coverage absent", CoverageBlocked)

    def successful_clocks(self, label: str, brain: Any, index: int) -> None:
        expected = 44.0 + 200.0 * index
        observed = clocks_and_fault_state(brain)
        self.writer.write(
            label + "-clock-gate.json",
            {
                "expected_field_end_ms": expected,
                "expected_receptor_Q_last_ms": expected - 32.0,
                "actual_field_end_ms": observed["field_end_ms"],
                "actual_receptor_Q": observed["receptor_Q"],
            },
        )
        require(
            observed["field_end_ms"] == expected
            and observed["receptor_Q"] is not None
            and observed["receptor_Q"]["last_time_ms"] == expected - 32.0,
            "successful field/receptor clock mismatch",
            InvariantError,
        )

    def pairwise_copies(self, before: dict[str, Any]) -> None:
        # No branch is processed until all four whole-brain copies exist and pass.
        for label in BRANCHES:
            self.stage = "copy-" + label
            self.budget.check()
            self.writer.write(self.stage + "-attempt.json", {"counts_before": self.counts})
            self.bump("whole_brain_copy_attempts")
            self.brains[label] = copy.deepcopy(self.brains["root"], {})
            state = self.observe(self.stage, self.brains[label])
            self.writer.write(
                self.stage + "-equality.json",
                {
                    "before_inventory": before["sha256"],
                    "copy_inventory": state["sha256"],
                    "complete_typed_bytes_equal": state["bytes"] == before["bytes"],
                },
            )
            require(state["bytes"] == before["bytes"], "whole-copy graph mismatch", InvariantError)
            self.original_exact(self.stage, before)
        # All graphs and their complete content remain live at this same-time comparison.
        live = {
            name: self.capture("pairwise-" + name, brain) for name, brain in self.brains.items()
        }
        rows = []
        names = list(live)
        for i, left in enumerate(names):
            for right in names[i + 1 :]:
                shared = live[left]["mutable"] & live[right]["mutable"]
                rows.append(
                    {
                        "left": left,
                        "right": right,
                        "shared_mutable_paths": [
                            {
                                "left_path": live[left]["paths"][key],
                                "right_path": live[right]["paths"][key],
                            }
                            for key in shared
                        ],
                    }
                )
        self.writer.write("pairwise-mutable-isolation.json", rows)
        require(
            len(rows) == 10 and not any(row["shared_mutable_paths"] for row in rows),
            "root/copy mutable identity overlap",
            InvariantError,
        )

    def success_branch(self, label: str, ids: list[str]) -> tuple[dict[str, Any], Any]:
        brain = self.brains[label]
        result, state = self.step(brain, self.spec["suffix"], label)
        self.successful_clocks(label, brain, 3)
        self.coverage(label, brain, ids)
        output = self.detached(label, result, brain)
        # Export/inspection must themselves be observational.
        after_export = self.capture(label + "-after-export", brain)
        require(after_export["bytes"] == state["bytes"], "export changed producer", InvariantError)
        return state, output

    def execute(self, brain_type: type, config_type: type) -> None:
        self.budget.check()
        self.writer.write(
            "constructor-attempt.json", {"attempt": 1, "resources": self.budget.sample()}
        )
        self.constructor_attempts += 1
        root = brain_type(config_type(**self.spec["configuration"]["brain"]))
        self.bump("fresh_roots")
        self.brains["root"] = root
        self.owner = PrivateOwner(root)
        self.observe("fresh-root", root)
        configs = actual_configuration(root)
        self.writer.write("actual-twelve-constructor-configs.json", configs)
        require(
            canonical(configs) == canonical(self.spec["configuration"]),
            "actual twelve constructor configurations differ",
        )
        require(
            not root.results
            and not root.base.results
            and not root.assemblies.candidates
            and root.pending_activation is None
            and root.current_time_ms == 0.0,
            "root is not fresh",
            InvariantError,
        )
        ids: list[str] = []
        for index, episode in enumerate(self.spec["prefix"]):
            label = f"prefix-{index + 1}"
            result, _ = self.step(root, episode, label)
            ids.append(episode["episode_id"])
            self.successful_clocks(label, root, index)
            if index == 0:
                first = {
                    "pending_null": root.pending_activation is None,
                    "no_mature_candidates": all(
                        c.episode_count < 3 for c in root.assemblies.candidates.values()
                    ),
                    "no_mature_activations": all(not a.mature for a in result.assembly_activations),
                }
                self.writer.write("prefix-1-immaturity-gate.json", first)
                require(
                    all(first.values()), "first prefix maturity control failed", CoverageBlocked
                )
        self.coverage("acquired-prefix", root, ids)
        before = self.observe("acquired-beforestate", root)
        self.pairwise_copies(before)
        ids.append(self.spec["suffix"]["episode_id"])

        def prepare_export_abort() -> tuple[Any, Any]:
            state, _ = self.success_branch("export_abort", ids)
            require(
                state["bytes"] != before["bytes"],
                "export candidate did not advance",
                InvariantError,
            )
            self.original_exact("export-before-injection", before)
            self.writer.write(
                "export-injection-boundary.json",
                {
                    "fault": "InjectedExportValidationError",
                    "placement": "after processing, raw/graph/output preservation and validation",
                    "complete_advanced_graph": state["sha256"],
                    "commit_count": self.counts["owner_commits"],
                },
            )
            raise InjectedExportValidationError("acquired-ownership-export-boundary-20261001")

        try:
            self.owner.transact(prepare_export_abort)
        except InjectedExportValidationError as error:
            self.writer.write("export_abort-injected-error.json", exception_record(error))
            self.bump("aborted_transactions")
        self.original_exact("export-abandoned", before)

        self.stage = "event_cap_abort-config"
        candidate = self.brains["event_cap_abort"]
        exact = self.observe("event-cap-exact-copy", candidate)
        require(
            exact["bytes"] == before["bytes"],
            "fault branch not exact acquired copy",
            InvariantError,
        )
        old_config = candidate.base.field.config  # Keep the replaced object alive too.
        candidate.base.field.config = dataclasses.replace(old_config, max_events_per_run=1)
        after_config = self.observe("event-cap-after-config", candidate)
        old_values, new_values = (
            dataclasses.asdict(old_config),
            dataclasses.asdict(candidate.base.field.config),
        )
        expected_values = dict(old_values, max_events_per_run=1)
        self.writer.write(
            "event-cap-config-change.json", {"before": old_values, "after": new_values}
        )
        require(
            new_values == expected_values, "unexpected fault configuration change", InvariantError
        )
        fault_before = clocks_and_fault_state(candidate)

        def prepare_event_cap_abort() -> tuple[Any, Any]:
            self.step(candidate, self.spec["suffix"], "event_cap_abort")
            # An unexpected real process return cannot reach the owner assignment.
            raise InvariantError("genuine event-cap processing exception was absent")

        try:
            self.owner.transact(prepare_event_cap_abort)
        except RuntimeError as error:
            require(
                type(error) is RuntimeError and str(error) == "max_events_per_run exceeded",
                "unexpected processing error in event-cap branch",
                InvariantError,
            )
            self.bump("expected_processing_exceptions")
            self.bump("aborted_transactions")
        else:
            raise InvariantError("genuine event-cap processing exception was absent")
        failed = self.observe("event-cap-final-failed-state", candidate)
        fault_after = clocks_and_fault_state(candidate)
        fault_checks = {
            "changed_beyond_config": failed["bytes"] != after_config["bytes"],
            "Q_two_observations": fault_after["receptor_Q"]["observations"]
            == fault_before["receptor_Q"]["observations"] + 2,
            "Q_last_time_612": fault_after["receptor_Q"]["last_time_ms"] == 612.0,
            "two_actual_arrival_pops": fault_after["last_run_arrivals"] == 2
            and fault_after["total_arrivals"] == fault_before["total_arrivals"] + 2,
            "arrival_scheduling_advanced": fault_after["queue_counter"]
            > fault_before["queue_counter"],
            "queue_changed": fault_after["queue_heap_layout"] != fault_before["queue_heap_layout"],
        }
        self.writer.write(
            "event-cap-genuine-fault-gate.json",
            {
                "checks": fault_checks,
                "before_processing": fault_before,
                "after_error": fault_after,
                "exact_clone_inventory": exact["sha256"],
                "after_config_inventory": after_config["sha256"],
                "failed_inventory": failed["sha256"],
                "source": "v04/field.py:270-293; v05/receptors.py:61-78,126-137",
                "no_spike_or_field_clock_advance_requirement": True,
            },
        )
        require(
            all(fault_checks.values()), "genuine processing mutation witness absent", InvariantError
        )
        self.original_exact("event-cap-abandoned", before)

        direct_state, direct_output = self.success_branch("direct_reference", ids)
        self.original_exact("direct-reference-finished", before)

        def prepare_commit() -> tuple[Any, Any]:
            commit_state, detached_output = self.success_branch("commit", ids)
            self.original_exact("commit-before-publication", before)
            checks = {
                "complete_typed_graph_bytes_equal": commit_state["bytes"] == direct_state["bytes"],
                "complete_detached_output_equal": canonical(detached_output)
                == canonical(direct_output),
                "candidate_advanced": commit_state["bytes"] != before["bytes"],
            }
            self.writer.write(
                "precommit-direct-equality.json",
                {
                    "checks": checks,
                    "commit_graph": commit_state["sha256"],
                    "direct_graph": direct_state["sha256"],
                    "owner_commits_before": self.counts["owner_commits"],
                },
            )
            require(all(checks.values()), "commit/direct mismatch", InvariantError)
            self.budget.check()
            # No filesystem write, export, validation, counter or inspection after this return
            # inside the owner transaction; only pointer assignment and detached-tree return.
            return self.brains["commit"], detached_output

        exported = self.owner.transact(prepare_commit)
        self.returned = True
        self.bump("owner_commits")  # Accounting is post-return, outside every abort handler.
        self.stage = "postcommit-external-mutation"
        self.mutate_after_return(exported, direct_state, before)
        expected_counts = {**COUNTS, "native_loads": 0, "outcome_calls": 0}
        require(self.counts == expected_counts, "full-run counts mismatch", InvariantError)
        self.stage = "complete"

    def mutate_after_return(
        self, output: Any, committed_before: dict[str, Any], old_before: dict[str, Any]
    ) -> None:
        require(
            self.returned and self.owner._brain is self.brains["commit"],
            "post-return owner identity mismatch",
            InvariantError,
        )
        callers = self.callers["commit"]
        targets = [(f"caller[{i}].metadata", pulse.metadata) for i, pulse in enumerate(callers)]
        targets.append(("export.metadata", output["metadata"]))
        for section in ("raw_pulses", "emitted_pulses"):
            targets.extend(
                (f"export.{section}[{i}].metadata", pulse["metadata"])
                for i, pulse in enumerate(output[section])
            )
        targets.extend(
            (f"export.v04_result.input_pulses[{i}].metadata", pulse["metadata"])
            for i, pulse in enumerate(output["v04_result"]["input_pulses"])
        )
        self.writer.write(
            "postreturn-control-before.json",
            {
                "caller_pulses": [p.as_dict() for p in callers],
                "export": output,
                "targets": [{"path": path, "value": value} for path, value in targets],
            },
        )
        require(
            len(callers) == 2
            and len(output["raw_pulses"]) == 2
            and output["emitted_pulses"]
            and output["v04_result"]["input_pulses"],
            "missing external mutation target",
            InvariantError,
        )
        committed_live = self.audit.inspect(self.owner._brain)[1]
        exported_live = primitive_tree(output)
        caller_live = self.audit.inspect(callers, "caller")[1]
        require(
            not committed_live & (set(exported_live) | caller_live),
            "external objects overlap committed graph before mutation",
            InvariantError,
        )
        changes = []
        for path, metadata in targets:
            require(type(metadata) is dict, "external metadata is not exact dict", InvariantError)
            old = canonical(metadata)
            metadata.update(copy.deepcopy(self.spec["external_mutation_controls"]["mutation"]))
            new = canonical(metadata)
            changes.append(
                {"path": path, "before_bytes": old, "after_bytes": new, "changed": old != new}
            )
        self.writer.write("postreturn-control-changes.json", changes)
        self.writer.write(
            "postreturn-control-after.json",
            {
                "caller_pulses": [p.as_dict() for p in callers],
                "export": output,
            },
        )
        self.capture("postreturn-mutated-callers", callers, "caller")
        self.capture("postreturn-mutated-export", output, "export")
        current = self.observe("postreturn-committed", self.owner._brain)
        original = self.observe("postreturn-old-root", self.brains["root"])
        checks = {
            "every_target_changed": all(row["changed"] for row in changes),
            "committed_graph_exact": current["bytes"] == committed_before["bytes"],
            "old_root_graph_exact": original["bytes"] == old_before["bytes"],
            "owner_is_commit_candidate": self.owner._brain is self.brains["commit"],
        }
        self.writer.write("postreturn-isolation-gate.json", checks)
        require(all(checks.values()), "postcommit mutation isolation failure", InvariantError)


def run(root: Path, output: Path, freeze_path: Path, freeze_sha256: str) -> int:
    """Only CLI reviewed mode calls this model-bearing entrypoint, exactly once."""
    budget = Budget()
    writer = EvidenceWriter(output)  # Exclusive directory: existing evidence is never overwritten.
    probe: Probe | None = None
    terminal: dict[str, Any] = {
        "status": "incomplete",
        "classification": "EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY",
        "scientific_credit": 0,
        "no_retry": True,
        "native_output_hashes_are_ownership_oracles": False,
        "claim_ceiling": "Restricted acquired-assembly ownership under two specified faults only",
        "hard_termination_limitation": "SIGKILL/OOM may prevent finalization; retain partial files",
    }
    try:
        budget.install()
        sys.addaudithook(deny_network_and_subprocess)
        sys.dont_write_bytecode = True
        cache = output / "empty_bytecode_cache"
        cache.mkdir(mode=0o700, exist_ok=False)
        sys.pycache_prefix = str(cache)
        require(
            not any(name == "sparkbrain" or name.startswith("sparkbrain.") for name in sys.modules),
            "SparkBrain must not already be imported",
        )
        timeout_parent = verify_timeout_parent()
        protocol, schema = read_protocol(root)
        frozen = verify_freeze(root, freeze_path, freeze_sha256)
        require(
            Path(frozen["output_directory"]).is_absolute()
            and Path(frozen["output_directory"]) == output,
            "frozen output path mismatch",
        )
        writer.write(
            "preflight.json",
            {
                "protocol": protocol,
                "protocol_sha256": PROTOCOL_SHA256,
                "graph_schema_sha256": SCHEMA_SHA256,
                "source_freeze": frozen,
                "source_freeze_path": str(freeze_path),
                "source_freeze_sha256": freeze_sha256,
                "source_root": str(root),
                "runner_sha256": digest_file(Path(__file__)),
                "python": sys.version,
                "platform": sys.platform,
                "uname": list(os.uname()),
                "argv": sys.argv,
                "pid": os.getpid(),
                "external_timeout": timeout_parent,
                "limits": LIMITS,
                "finalization_reserves_inside_limits": RESERVE,
                "network_enforcement": (
                    "Python audit denies socket.*, process launch and ctypes.dlopen; "
                    "NOT OS network isolation or a native-extension security sandbox"
                ),
                "bytecode": "fresh empty cache prefix and dont_write_bytecode=True",
                "resources": budget.sample(),
            },
        )
        budget.check()
        sys.path.insert(0, str(root / "src"))
        # Ordinary model imports are intentionally located ONLY after every frozen-source check.
        from sparkbrain.v04.contracts import SignalPulse
        from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig
        from sparkbrain.v05.contracts import V05StepResult

        audit = GraphAudit.from_schema(schema)
        imported = {}
        for name, module in sorted(sys.modules.items()):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                path = Path(module.__file__).resolve()
                relative = path.relative_to(root).as_posix()
                require(relative in protocol["package_sources_sha256"], "unfrozen module imported")
                require(
                    digest_file(path) == protocol["package_sources_sha256"][relative],
                    "imported module source drift",
                )
                imported[name] = relative
        writer.write("imported-sources.json", imported)
        require(not any(cache.rglob("*")), "bytecode cache is not empty")
        probe = Probe(protocol, audit, writer, budget, SignalPulse, V05StepResult)
        probe.execute(IntegratedV05Brain, V05BrainConfig)
        terminal["status"] = "restricted_acquired_ownership_observed"
    except BaseException as error:
        budget.finish()
        writer.finalizing = True
        committed = (
            probe is not None
            and probe.owner is not None
            and "commit" in probe.brains
            and probe.owner._brain is probe.brains["commit"]
        )
        terminal.update(
            {
                "status": "postcommit_failure"
                if committed
                else "coverage_blocked"
                if isinstance(error, CoverageBlocked)
                else "stopped",
                "failure": exception_record(error),
                "failure_stage": probe.stage if probe else "preflight",
                "owner_pointer_committed": committed,
            }
        )
        try:
            writer.write("terminal-error.json", terminal["failure"])
            # No dynamics retry. Preserve each currently retained graph if reserve permits.
            if probe is not None:
                for label, brain in probe.brains.items():
                    probe.capture("terminal-partial-" + label, brain)
        except BaseException as preservation_error:
            terminal["partial_preservation_error"] = exception_record(preservation_error)
    finally:
        budget.finish()
        writer.finalizing = True
        terminal["counts"] = (
            probe.counts
            if probe
            else {**dict.fromkeys(COUNTS, 0), "native_loads": 0, "outcome_calls": 0}
        )
        terminal["constructor_attempts"] = probe.constructor_attempts if probe else 0
        if probe is not None and probe.owner is not None:
            # A signal after pointer assignment but before return/accounting is a commit,
            # never an abort. Observe the real pointer without putting work in that boundary.
            actually_committed = (
                "commit" in probe.brains and probe.owner._brain is probe.brains["commit"]
            )
            terminal["counts"]["owner_commits"] = int(actually_committed)
            terminal["successful_owner_return_observed"] = probe.returned
        terminal["resources_before_final_files"] = budget.sample()
        terminal["artifact_bytes_before_final_files"] = writer.bytes_written
        try:
            writer.write("terminal.json", terminal)
            writer.write(
                "manifest.json",
                {
                    "files": writer.manifest(),
                    "manifest_excludes_itself": True,
                    "resources_before_manifest": budget.sample(),
                },
            )
        except BaseException as error:
            print(f"Finalization incomplete: {type(error).__name__}: {error}", file=sys.stderr)
            return 2
    return 0 if terminal["status"] == "restricted_acquired_ownership_observed" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check-source", action="store_true", help="Never import SparkBrain")
    modes.add_argument(
        "--run-reviewed", action="store_true", help="Execute once after freeze/review"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-freeze", type=Path)
    parser.add_argument("--source-freeze-sha256")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if bool(args.source_freeze) != bool(args.source_freeze_sha256):
        parser.error("source freeze path and exact SHA-256 must be supplied together")
    if args.check_source:
        spec, schema = read_protocol(root)
        if args.source_freeze:
            verify_freeze(root, args.source_freeze, args.source_freeze_sha256)
        require(
            not any(name == "sparkbrain" or name.startswith("sparkbrain.") for name in sys.modules),
            "source check imported SparkBrain",
        )
        print(
            canonical(
                {
                    "status": "source_check_passed",
                    "model_imported": False,
                    "package_source_files": len(spec["package_sources_sha256"]),
                    "schema_classes": sum(len(row["classes"]) for row in schema["files"].values()),
                    "protocol_sha256": PROTOCOL_SHA256,
                    "implementation_freeze_checked": bool(args.source_freeze),
                }
            )
        )
        return 0
    if not args.output or not args.source_freeze:
        parser.error("reviewed execution requires --output and exact separately reviewed freeze")
    return run(root, args.output.resolve(), args.source_freeze.resolve(), args.source_freeze_sha256)


if __name__ == "__main__":
    raise SystemExit(main())
