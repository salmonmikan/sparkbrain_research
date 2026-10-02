#!/usr/bin/env python3
"""Source-only PR182 history-conditioned export diagnostic; scientific credit zero.

No model is imported by module loading or --check-source. --run-reviewed is opt-in
and requires a separately hashed implementation freeze and an actual Linux parent:
PYTHONHASHSEED=<frozen integer> timeout -s KILL 180s python -B THIS_SCRIPT
--run-reviewed --output FRESH_DIR --source-freeze FREEZE --source-freeze-sha256 SHA.

GraphAudit, primitive_tree, identity_witnesses and resource/preservation patterns
are source-adapted from scripts/v05_acquired_ownership_probe.py (PR180, SHA-256
 d24730db318749deba4428ea7d26d283181bc3a91353d268eb2528f23db2bc7d),
itself attributed to PR176/177. No historical runner is imported or executed.
Typed/reference graph bytes are the oracle; hashes only address retained evidence.
No M1, outcome update, checkpoint load, commit, retry or scientific promotion.
"""

from __future__ import annotations

import argparse
import ast
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
from itertools import combinations
from pathlib import Path
from typing import Any

PROTOCOL_PATH = "artifacts/research/v05_history_export_20261002/protocol.json"
PROTOCOL_SHA256 = "48b2925fac2fb56200e59a9fb88df60c18868d5553e4390fe6c47864b6ac9c82"
DOCUMENT_PATH = "docs/research/v05_history_export_protocol_20261002.md"
DOCUMENT_SHA256 = "d0e3e9e30d5c11bc95aada3d69e7ca9f761b7031a28a8303fffca8abd1ef30e6"
INPUTS_PATH = "artifacts/research/v05_history_export_20261002/inputs.jsonl"
INPUTS_SHA256 = "69a25de3c3aef84743d45494a1193df0eac695b4d0c8a0beb8f07fad5129ee39"
SCHEMA_PATH = "artifacts/research/v05_owned_state_20261001/source_map.json"
SCHEMA_SHA256 = "af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69"
SOURCE_PIN = "9b1179aa18060436e4a05f2ff21f4cffc098f79d"
IMPLEMENTATION_PATHS = {
    "scripts/v05_history_export_probe.py",
    "tests/test_v05_history_export_runner.py",
}
BRANCHES = ["A", "B", "A_repeat", "B_repeat"]
SEEDS = [910071, 910072]
CHANNELS = ["A", "C", "F", "H", "I", "J", "K", "L", "M", "Q"]
CANONICAL_FIELDS = ("ordered_units", "relative_bins", "unit_ids", "spike_count", "source_kind")
PROJECTION_VERSION = "native-strongest-canonical-mature-1"
LIMITS = {
    "address_space_bytes": 512 * 1024**2,
    "artifact_bytes": 96 * 1024**2,
    "cpu_seconds": 120,
    "wall_seconds": 180,
}
RESERVE = {
    "cpu_seconds": 3,
    "wall_seconds": 10,
    "artifact_bytes": 4 * 1024**2,
    "address_space_bytes": 2 * 1024**2,
}
MAX_COUNTS = {
    "roots": 2,
    "acquisition_process_attempts": 128,
    "query_process_attempts": 8,
    "total_process_attempts": 136,
    "submitted_pulses": 816,
    "whole_brain_copies": 8,
    "external_object_mutations": 64,
    "commits": 0,
    "m1_calls": 0,
    "native_loads": 0,
    "outcome_updates": 0,
}
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


class BindingError(RuntimeError):
    """Frozen source, input, configuration or launch mismatch."""


class InvariantError(RuntimeError):
    """Unsupported graph or ownership mismatch; stop without retries."""


class BudgetError(RuntimeError):
    """An attempt or resource ceiling has been reached."""


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

    def write_bytes(self, name: str, data: bytes) -> None:
        """Preserve already frozen raw input/freeze bytes exactly, inside the same cap."""
        require(Path(name).name == name, "evidence filenames must be flat")
        ceiling = LIMITS["artifact_bytes"] - (0 if self.finalizing else RESERVE["artifact_bytes"])
        with (self.directory / name).open("xb", buffering=0) as stream:
            self.files[name] = False
            view = memoryview(data)
            while view:
                if self.bytes_written + len(view) > ceiling:
                    raise BudgetError("cumulative artifact budget reached")
                written = stream.write(view)
                if not written:
                    raise OSError("evidence write made no progress")
                self.bytes_written += written
                view = view[written:]
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
        # Linux start ticks include interpreter startup; no new per-phase wall allowance.
        start_ticks = int(Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()[19])
        elapsed = time.clock_gettime(time.CLOCK_BOOTTIME) - start_ticks / os.sysconf("SC_CLK_TCK")
        self.wall_start = time.monotonic() - elapsed
        self.installed = False
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
        self.installed = True
        signal.signal(signal.SIGXCPU, self._interrupt)
        signal.signal(signal.SIGALRM, self._interrupt)
        remaining = LIMITS["wall_seconds"] - RESERVE["wall_seconds"] - self.sample()["wall_seconds"]
        require(remaining > 0, "preflight exhausted wall reserve", BudgetError)
        signal.setitimer(signal.ITIMER_REAL, remaining)
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
        if not self.installed:
            return
        resource.setrlimit(resource.RLIMIT_CPU, (LIMITS["cpu_seconds"], LIMITS["cpu_seconds"]))
        remaining = LIMITS["wall_seconds"] - (time.monotonic() - self.wall_start)
        if remaining <= 0:
            os._exit(124)
        signal.setitimer(signal.ITIMER_REAL, remaining)

    def check(self) -> None:
        sample = self.sample()
        reserve = {"cpu_seconds": 0, "wall_seconds": 0} if self.finalizing else RESERVE
        if (
            sample["wall_seconds"] >= LIMITS["wall_seconds"] - reserve["wall_seconds"]
            or sample["cpu_seconds"] >= LIMITS["cpu_seconds"] - reserve["cpu_seconds"]
        ):
            raise BudgetError("execution reserve boundary reached")

    def sample(self) -> dict[str, Any]:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return {
            "wall_seconds": time.monotonic() - self.wall_start,
            "wall_origin_monotonic": self.wall_start,
            "wall_origin": "Linux process start ticks; precision 1/SC_CLK_TCK",
            "cpu_origin": "RUSAGE_SELF process lifetime",
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


def exception_record(error: BaseException) -> dict[str, Any]:
    return {
        "type": type(error).__name__,
        "message": str(error),
        "traceback": "".join(traceback.format_exception(error)),
    }


def read_protocol(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    for name, expected in (
        (PROTOCOL_PATH, PROTOCOL_SHA256),
        (DOCUMENT_PATH, DOCUMENT_SHA256),
        (INPUTS_PATH, INPUTS_SHA256),
        (SCHEMA_PATH, SCHEMA_SHA256),
    ):
        require(digest_file(root / name) == expected, f"frozen bytes changed: {name}")
    spec = json.loads((root / PROTOCOL_PATH).read_text())
    require(spec["source_pin"] == SOURCE_PIN, "source pin mismatch")
    require(spec["max_counts"] == MAX_COUNTS, "attempt count contract mismatch")
    require(all(spec["limits"][k] == v for k, v in LIMITS.items()), "resource cap mismatch")
    require(package_hashes(root) == spec["package_sources_sha256"], "package source mismatch")
    require(len(spec["package_sources_sha256"]) == 157, "complete source inventory required")
    for name, expected in spec["reuse_sources_sha256"].items():
        require(digest_file(root / name) == expected, f"reuse source changed: {name}")
    schema = json.loads((root / SCHEMA_PATH).read_text())
    require(len(schema["files"]) == 16, "graph source inventory mismatch")
    require(sum(len(v["classes"]) for v in schema["files"].values()) == 50, "graph class count")
    for name, row in schema["files"].items():
        require(row["sha256"] == spec["package_sources_sha256"][name], "graph source binding")
        require(all(not c["custom_copy_hooks"] for c in row["classes"].values()), "copy hooks")
    inputs = [json.loads(line) for line in (root / INPUTS_PATH).read_text().splitlines()]
    validate_inputs(inputs)
    source_configuration_preflight(root, spec)
    return spec, schema, inputs


CONFIG_TYPES = {
    "brain": ("v05/brain.py", "V05BrainConfig"),
    "base": ("v04/brain.py", "V04BrainConfig"),
    "field": ("v04/field.py", "ExcitableFieldConfig"),
    "burst": ("v04/dynamics.py", "BurstDetectorConfig"),
    "cascade": ("v04/dynamics.py", "CascadeTrackerConfig"),
    "ignition": ("v04/dynamics.py", "IgnitionGateConfig"),
    "base_plasticity": ("v04/plasticity.py", "TimingPlasticityConfig"),
    "receptor": ("v05/receptors.py", "ReceptorConfig"),
    "assembly": ("v05/assemblies.py", "AssemblyConfig"),
    "plasticity": ("v05/plasticity.py", "V05PlasticityConfig"),
    "homeostasis": ("v05/homeostasis.py", "HomeostasisConfig"),
    "action": ("v05/action.py", "ActionPolicyConfig"),
}


def source_configuration_preflight(root: Path, spec: dict[str, Any]) -> None:
    """Inspect declarations only. No import, config instance, topology or producer."""
    require(set(spec["configuration"]) == set(CONFIG_TYPES) == set(CONFIG_PATHS), "12 configs")
    for key, (path, name) in CONFIG_TYPES.items():
        tree = ast.parse((root / "src/sparkbrain" / path).read_text())
        cls = next(
            node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name
        )
        fields = {node.target.id for node in cls.body if isinstance(node, ast.AnnAssign)}
        require(fields == set(spec["configuration"][key]), f"config field drift: {key}")
    require(spec["configuration"]["assembly"]["max_candidates"] == 32, "native cap must be 32")
    require(spec["configuration"]["assembly"]["mature_episodes"] == 3, "native maturity drift")


def config_arguments(key: str, settings: dict[str, Any]) -> dict[str, Any]:
    """Restore the sole tuple-valued native config from its JSON wire representation."""
    arguments = copy.deepcopy(settings)
    if key == "action":
        require(type(arguments["actions"]) is list, "action wire format must be a list")
        arguments["actions"] = tuple(arguments["actions"])
    return arguments


def validate_inputs(records: list[dict[str, Any]]) -> None:
    require(len(records) == 136, "literal input count")
    serial = 0
    for seed_index, seed in enumerate(SEEDS):
        rows = records[68 * seed_index : 68 * (seed_index + 1)]
        for i, row in enumerate(rows):
            acquisition = i < 64
            keys = {"seed", "phase", "observation", "index" if acquisition else "branch"}
            require(set(row) == keys and row["seed"] == seed, "audit record shape/seed")
            require(row["phase"] == ("acquisition" if acquisition else "query"), "phase order")
            if acquisition:
                require(row["index"] == i, "complete original acquisition order")
            else:
                require(row["branch"] == BRANCHES[i - 64], "fixed query order")
            observation = row["observation"]
            require(set(observation) == {"occurrence_id", "start_ms", "pulses"}, "model keys")
            identifier = serial if acquisition else serial - (i > 64)
            if i == 64:
                identifier = serial
            expected_id = f"history-export-20261002-{identifier:06d}"
            require(observation["occurrence_id"] == expected_id, "opaque monotonic receipt")
            if acquisition or i == 64:
                serial += 1
            start = float(i * 200) if acquisition else 12800.0
            require(observation["start_ms"] == start, "fixed independent query time")
            pulses = observation["pulses"]
            require(len(pulses) == 6, "six raw pulses required")
            for pulse in pulses:
                require(
                    set(pulse)
                    == {
                        "time_ms",
                        "channel",
                        "magnitude",
                        "polarity",
                        "location",
                        "novelty",
                        "prediction_error",
                        "source_id",
                        "metadata",
                    },
                    "raw pulse fields",
                )
                require(pulse["source_id"] == "probe-input" and pulse["metadata"] == {}, "source")
                require(pulse["location"] is None and pulse["polarity"] == 1, "pulse validity")
                require(pulse["novelty"] == pulse["prediction_error"] == 0.0, "supplied modulation")
            current = [p for p in pulses if p["channel"] == "Q"]
            require(
                len(current) == 1 and current[0]["time_ms"] == start + 40, "identical current Q"
            )
            require(current[0]["magnitude"] == 1.18, "Q magnitude")
            raw_raster(observation)
        a, b, ar, br = [row["observation"] for row in rows[64:]]
        require(a == ar and b == br, "exact repeated raw inputs")
        require(a["occurrence_id"] == b["occurrence_id"], "same query receipt")
        swapped = copy.deepcopy(a)
        for pulse in swapped["pulses"]:
            pulse["channel"] = {"A": "C", "C": "A"}.get(pulse["channel"], pulse["channel"])
        require(swapped == b, "only A/C order may differ")


def raw_raster(observation: dict[str, Any]) -> list[float]:
    """PR169 outcome-blind normalized 10 x 41 floor/ceil raster, source copied in form."""
    vector = [0.0] * 410
    for pulse in observation["pulses"]:
        relative = pulse["time_ms"] - observation["start_ms"]
        magnitude = pulse["magnitude"]
        require(math.isfinite(relative) and 0 <= relative <= 40, "raw cutoff violation")
        require(math.isfinite(magnitude) and magnitude >= 0, "invalid raw magnitude")
        require(pulse["channel"] in CHANNELS, "unknown raw channel")
        low = math.floor(relative)
        fraction = relative - low
        offset = CHANNELS.index(pulse["channel"]) * 41
        vector[offset + low] += magnitude * (1 - fraction)
        if fraction:
            vector[offset + low + 1] += magnitude * fraction
    total = sum(vector)
    require(math.isfinite(total) and total > 0, "invalid total raw magnitude")
    require(all(math.isfinite(value) for value in vector), "nonfinite raw raster arithmetic")
    return [value / total for value in vector]


def verify_freeze(root: Path, path: Path, expected: str, spec: dict[str, Any]) -> dict[str, Any]:
    require(digest_file(path) == expected, "implementation-freeze SHA mismatch")
    frozen = json.loads(path.read_text())
    bindings = {
        "schema": "v05-history-export-runner-freeze-1",
        "protocol_sha256": PROTOCOL_SHA256,
        "document_sha256": DOCUMENT_SHA256,
        "inputs_sha256": INPUTS_SHA256,
        "graph_schema_sha256": SCHEMA_SHA256,
        "source_pin": SOURCE_PIN,
        "configuration_sha256": hashlib.sha256(
            canonical(spec["configuration"]).encode()
        ).hexdigest(),
        "pythonhashseed": "0",
        "external_timeout_argv": ["timeout", "-s", "KILL", "180s"],
    }
    for key, value in bindings.items():
        require(frozen.get(key) == value, f"freeze binding mismatch: {key}")
    require(set(frozen["implementation_sources_sha256"]) == IMPLEMENTATION_PATHS, "two-file freeze")
    for name, sha in frozen["implementation_sources_sha256"].items():
        require(digest_file(root / name) == sha, f"implementation drift: {name}")
    require(
        Path(__file__).resolve() == root / "scripts/v05_history_export_probe.py", "runner origin"
    )
    require(frozen["package_sources_sha256"] == spec["package_sources_sha256"], "package freeze")
    require(package_hashes(root) == frozen["package_sources_sha256"], "runtime source drift")
    require(frozen["reuse_sources_sha256"] == spec["reuse_sources_sha256"], "reuse freeze")
    for name, sha in frozen["reuse_sources_sha256"].items():
        require(digest_file(root / name) == sha, f"reuse drift: {name}")
    require(Path(frozen["output_directory"]).is_absolute(), "absolute exclusive output required")
    return frozen


def verify_timeout_parent() -> dict[str, Any]:
    parent = os.getppid()
    words = [
        word.decode() for word in Path(f"/proc/{parent}/cmdline").read_bytes().split(b"\0") if word
    ]
    own = [word.decode() for word in Path("/proc/self/cmdline").read_bytes().split(b"\0") if word]
    require(len(words) >= 6 and Path(words[0]).name == "timeout", "actual timeout parent required")
    require(words[1:4] == ["-s", "KILL", "180s"], "exact timeout -s KILL 180s required")
    require(words[4:] == own, "timeout child argv mismatch")
    require(
        os.environ.get("PYTHONHASHSEED") == "0" and sys.flags.hash_randomization == 0,
        "actual hash seed state mismatch",
    )
    return {
        "parent_pid": parent,
        "parent_argv": words,
        "process_argv": own,
        "pythonhashseed": "0",
        "hash_randomization_flag": sys.flags.hash_randomization,
    }


def loaded_source_origins(root: Path, spec: dict[str, Any]) -> dict[str, str]:
    imported = {}
    for name, module in sorted(sys.modules.copy().items()):
        if name != "sparkbrain" and not name.startswith("sparkbrain."):
            continue
        require(not name.startswith("sparkbrain.system_build"), "M1 module import forbidden")
        require(module is not None and module.__spec__ is not None, "missing module origin")
        path = Path(module.__file__).resolve()
        origin = Path(module.__spec__.origin).resolve()
        expected = root / "src" / Path(*name.split("."))
        expected = (
            expected / "__init__.py" if hasattr(module, "__path__") else expected.with_suffix(".py")
        )
        require(path == origin == expected, f"loaded source origin mismatch: {name}")
        relative = path.relative_to(root).as_posix()
        require(
            digest_file(path) == spec["package_sources_sha256"].get(relative), "loaded source SHA"
        )
        for value in vars(module).values():
            if getattr(value, "__module__", None) == name and hasattr(value, "__code__"):
                require(Path(value.__code__.co_filename).resolve() == path, "loaded code origin")
        imported[name] = relative
    require(bool(imported), "no loaded producer sources")
    return imported


def canonical_content(prototype: Any) -> tuple[Any, ...]:
    return tuple(getattr(prototype, field) for field in CANONICAL_FIELDS)


def freeze_dictionary(bank: Any) -> dict[str, Any]:
    """Bind every mature prototype once, preserving collisions and native-ID audit rows."""
    rows = [
        (canonical_content(candidate.prototype), identifier)
        for identifier, candidate in bank.candidates.items()
        if len(candidate.episode_ids) >= bank.config.mature_episodes
    ]
    rows.sort(key=lambda row: row[0])
    contents = [content for content, _ in rows]
    collisions = []
    for content in dict.fromkeys(contents):
        identifiers = [identifier for candidate, identifier in rows if candidate == content]
        if len(identifiers) > 1:
            collisions.append(identifiers)
    return json.loads(
        canonical(
            {
                "binding": {
                    "projection_version": PROJECTION_VERSION,
                    "source_pin": SOURCE_PIN,
                    "N": len(contents),
                    "canonical_prototypes": contents,
                    "dictionary_sha256": hashlib.sha256(canonical(contents).encode()).hexdigest(),
                },
                "coordinates": [
                    {"assembly_id": identifier, "canonical": content}
                    for content, identifier in rows
                ],
                "collisions": collisions,
            }
        )
    )


ACTIVATION_FIELDS = (
    "assembly_id",
    "pattern_id",
    "time_ms",
    "similarity",
    "occurrences",
    "episode_count",
    "mature",
    "unit_ids",
    "suppressed",
)


def export_native(
    brain: Any,
    result: Any,
    observation: dict[str, Any],
    dictionary: dict[str, Any],
    similarity: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Audit native matching, then detach its actual pending activation without reweighting.

    The injected similarity callable is the pinned native pure function in reviewed
    execution. Tests supply plain fake objects/functions and never import that model.
    """
    bank = brain.assemblies
    binding = json.loads(canonical(dictionary["binding"]))
    audit: dict[str, Any] = {"patterns": [], "strongest_ties": [], "withheld_reasons": []}
    issues: set[str] = set()
    n = binding.get("N")
    if type(n) is not int or not 0 <= n <= 32:
        issues.add("binding_error")
        n = 0
    if binding["N"] == 0:
        issues.add("no_mature_dictionary")
    if dictionary["collisions"]:
        issues.add("canonical_collision")
    if freeze_dictionary(bank) != dictionary:
        issues.add("binding_error")
    expected_activations = []
    for pattern_index, pattern in enumerate(result.patterns):
        if pattern.spike_count < brain.config.min_pattern_spikes:
            audit["patterns"].append({"index": pattern_index, "accepted_internal_pattern": False})
            continue
        scores = []
        candidates = list(bank.candidates.items())
        for identifier, candidate in candidates:
            score = similarity(candidate.prototype, pattern)
            valid = type(score) in (int, float) and math.isfinite(score) and 0 <= score <= 1
            if not valid:
                issues.add("value_error")
            scores.append(
                {
                    "assembly_id": identifier,
                    "canonical": canonical_content(candidate.prototype),
                    "episode_ids": sorted(candidate.episode_ids),
                    "episode_count": len(candidate.episode_ids),
                    "mature": len(candidate.episode_ids) >= bank.config.mature_episodes,
                    "suppressed": identifier in bank.suppressed,
                    "score": score
                    if valid
                    else {"invalid_type": type(score).__name__, "repr": repr(score)},
                }
            )
        record: dict[str, Any] = {
            "index": pattern_index,
            "pattern_id": pattern.pattern_id,
            "canonical": canonical_content(pattern),
            "accepted_internal_pattern": True,
            "scores": scores,
            "best_ties": [],
            "native_id_tiebreak_winner": None,
        }
        audit["patterns"].append(record)
        if any(type(row["score"]) is dict for row in scores) or not scores:
            continue
        best_score = max(row["score"] for row in scores)
        ties = [row["assembly_id"] for row in scores if row["score"] == best_score]
        record["best_ties"] = sorted(ties)
        record["best_score"] = best_score
        identifier = min(ties)
        record["native_id_tiebreak_winner"] = identifier
        if len(ties) > 1:
            issues.add("native_match_tie")
        if best_score < bank.config.similarity_threshold:
            continue
        candidate = bank.candidates[identifier]
        expected_activations.append(
            {
                "assembly_id": identifier,
                "pattern_id": pattern.pattern_id,
                "time_ms": pattern.end_ms,
                "similarity": best_score,
                "occurrences": candidate.occurrences,
                "episode_count": len(candidate.episode_ids),
                "mature": len(candidate.episode_ids) >= bank.config.mature_episodes,
                "unit_ids": candidate.prototype.unit_ids,
                "suppressed": identifier in bank.suppressed,
            }
        )
    actual = [
        {key: getattr(row, key) for key in ACTIVATION_FIELDS} for row in result.assembly_activations
    ]
    # Primitive comparisons preserve tuples here; only the outward export is JSON-detached.
    if actual != expected_activations:
        issues.add("binding_error")
    usable = [row for row in result.assembly_activations if row.mature and not row.suppressed]
    strongest = max(
        usable, key=lambda row: (row.similarity, row.episode_count, row.assembly_id), default=None
    )
    if strongest is not None:
        key = (strongest.similarity, strongest.episode_count)
        audit["strongest_ties"] = [
            {"activation_index": i, "assembly_id": row.assembly_id, "pattern_id": row.pattern_id}
            for i, row in enumerate(result.assembly_activations)
            if row.mature and not row.suppressed and (row.similarity, row.episode_count) == key
        ]
        if len(audit["strongest_ties"]) > 1:
            issues.add("native_strongest_tie")
    pending = brain.pending_activation
    audit["pending_is_native_strongest"] = pending is strongest
    audit["pending_returned_identity_indices"] = [
        i for i, row in enumerate(result.assembly_activations) if row is pending
    ]
    if pending is not strongest:
        issues.add("binding_error")
    features = [0.0] * n
    audit["winner_canonical"] = None
    if pending is not None:
        value = pending.similarity
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
            issues.add("value_error")
        positions = [
            i
            for i, row in enumerate(dictionary["coordinates"])
            if row["assembly_id"] == pending.assembly_id
        ]
        candidate = bank.candidates.get(pending.assembly_id)
        if (
            len(positions) != 1
            or candidate is None
            or not pending.mature
            or pending.suppressed
            or len(candidate.episode_ids) < bank.config.mature_episodes
        ):
            issues.add("binding_error")
        else:
            audit["winner_canonical"] = canonical_content(candidate.prototype)
            position = positions[0]
            prototypes = binding.get("canonical_prototypes", [])
            if (
                type(prototypes) is not list
                or position >= len(prototypes)
                or position >= n
                or json.loads(canonical(audit["winner_canonical"])) != prototypes[position]
            ):
                issues.add("binding_error")
            else:
                features[position] = value
    priority = [
        "value_error",
        "binding_error",
        "no_mature_dictionary",
        "canonical_collision",
        "native_match_tie",
        "native_strongest_tie",
    ]
    audit["withheld_reasons"] = [reason for reason in priority if reason in issues]
    status = (
        audit["withheld_reasons"][0]
        if issues
        else ("accepted_match" if pending is not None else "accepted_no_match")
    )
    exported = {
        "schema": "v05-history-export-1",
        "occurrence_id": observation["occurrence_id"],
        "decision_ms": result.end_ms,
        "accepted": not issues,
        "status": status,
        "features": [] if issues else features,
        "binding": binding,
    }
    primitive_tree(exported)
    return exported, audit


def learned_state(brain: Any) -> dict[str, Any]:
    """Frozen native learning subset; all other state still receives the full graph oracle."""
    return {
        "assemblies": brain.assemblies,
        "plasticity": brain.plasticity,
        "homeostasis": brain.homeostasis,
        "predictor": brain.predictor,
        "action_policy": brain.action_policy,
        "weights_delays": [
            (key, edge.weight, edge.delay_ms) for key, edge in brain.base.field.connections.items()
        ],
        "thresholds": [(key, unit.base_threshold) for key, unit in brain.base.field.units.items()],
        "configuration": actual_configuration(brain),
    }


class PrivateOwner:
    """Single acquired pointer; this diagnostic has no commit operation."""

    __slots__ = ("_brain",)

    def __init__(self, brain: Any) -> None:
        self._brain = brain


class Probe:
    """The sole bounded plan: two original prefixes, then four isolated queries each."""

    def __init__(
        self,
        spec: dict[str, Any],
        audit: GraphAudit,
        writer: EvidenceWriter,
        budget: Budget,
        pulse_type: type,
        result_type: type,
        similarity: Any,
    ) -> None:
        self.spec, self.audit, self.writer, self.budget = spec, audit, writer, budget
        self.pulse_type, self.result_type, self.similarity = pulse_type, result_type, similarity
        self.counts = dict.fromkeys(MAX_COUNTS, 0)
        self.graph_files: dict[str, str] = {}
        self.brains: dict[str, Any] = {}
        self.owner: PrivateOwner | None = None
        self.stage = "preconstruction"
        self.seed_results: list[dict[str, Any]] = []

    def bump(self, changes: dict[str, int]) -> None:
        for key, amount in changes.items():
            require(
                amount >= 0 and self.counts[key] + amount <= MAX_COUNTS[key],
                f"attempt ceiling: {key}",
                BudgetError,
            )
        for key, amount in changes.items():
            self.counts[key] += amount

    def capture(self, label: str, value: Any, name: str = "brain") -> dict[str, Any]:
        self.budget.check()
        try:
            inventory, mutable = self.audit.inspect(value, name)
        except BaseException as error:
            self.writer.write(label + "-partial-graph.json", self.audit.partial)
            self.writer.write(label + "-graph-error.json", exception_record(error))
            raise
        data = canonical(inventory).encode()
        sha = hashlib.sha256(data).hexdigest()
        if sha not in self.graph_files:
            filename = "graph-" + sha + ".json"
            self.writer.write(filename, inventory)
            self.graph_files[sha] = filename
        self.writer.write(
            label + "-graph.json",
            {
                "inventory_file": self.graph_files[sha],
                "canonical_inventory_sha256": sha,
                "oracle": "complete typed/reference bytes; hash only addresses retained inventory",
                "node_count": len(inventory["nodes"]),
                "mutable_identity_count": len(mutable),
            },
        )
        return {"bytes": data, "sha256": sha, "mutable": mutable, "paths": dict(self.audit.paths)}

    def progress(self, label: str) -> None:
        print(
            canonical({"stage": label, "counts": self.counts, "resources": self.budget.sample()}),
            flush=True,
        )

    def same_graph(self, label: str, current: dict[str, Any], before: dict[str, Any]) -> None:
        same = current["bytes"] == before["bytes"]
        self.writer.write(
            label + "-equality.json",
            {
                "before": before["sha256"],
                "after": current["sha256"],
                "exact_typed_bytes_equal": same,
            },
        )
        require(same, f"full graph differs: {label}", InvariantError)

    def root_exact(self, label: str, before: dict[str, Any]) -> None:
        pointer_ok = self.owner is not None and self.owner._brain is self.brains["root"]
        self.writer.write(
            label + "-owner.json", {"owner_is_acquired_root": pointer_ok, "commits": 0}
        )
        require(pointer_ok, "acquired owner pointer changed", InvariantError)
        self.same_graph(label, self.capture(label, self.brains["root"]), before)

    def pairwise(self, label: str, snapshots: dict[str, dict[str, Any]]) -> None:
        rows = []
        for left, right in combinations(snapshots, 2):
            a, b = snapshots[left], snapshots[right]
            common = a["mutable"] & b["mutable"]
            rows.append(
                {
                    "left": left,
                    "right": right,
                    "shared_mutable_paths": [
                        {"left": a["paths"][identity], "right": b["paths"][identity]}
                        for identity in sorted(common, key=lambda item: a["paths"][item])
                    ],
                }
            )
        self.writer.write(label + "-isolation.json", rows)
        require(
            len(rows) == 10 and all(not row["shared_mutable_paths"] for row in rows),
            "root/copy mutable graph intersection",
            InvariantError,
        )

    def step(self, brain: Any, row: dict[str, Any], label: str) -> tuple[Any, tuple[Any, ...]]:
        self.stage = label
        self.budget.check()
        observation = row["observation"]
        callers = tuple(self.pulse_type(**copy.deepcopy(p)) for p in observation["pulses"])
        require(
            all(type(p) is self.pulse_type and type(p.metadata) is dict for p in callers),
            "actual caller pulse type",
            InvariantError,
        )
        require(
            [dataclasses.asdict(p) for p in callers] == observation["pulses"], "caller input drift"
        )
        caller_state = self.capture(label + "-caller", callers, "caller")
        owned = copy.deepcopy(callers, {})
        owned_state = self.capture(label + "-ingress", owned, "caller")
        self.same_graph(label + "-input-copy", owned_state, caller_state)
        common = caller_state["mutable"] & owned_state["mutable"]
        self.writer.write(
            label + "-ingress-isolation.json",
            {"shared_mutable_paths": [caller_state["paths"][key] for key in sorted(common)]},
        )
        require(not common, "caller ingress alias", InvariantError)
        phase = row["phase"]
        self.writer.write(
            label + "-raw410.json",
            {
                "observation": observation,
                "channels": CHANNELS,
                "bins": 41,
                "values": raw_raster(observation),
                "outcome_blind": True,
            },
        )
        self.bump(
            {
                "total_process_attempts": 1,
                phase + "_process_attempts": 1,
                "submitted_pulses": len(owned),
            }
        )
        self.writer.write(
            label + "-attempt.json",
            {
                "record": row,
                "flags": self.spec["call_flags"][phase],
                "counts_including_attempt": self.counts,
                "resources": self.budget.sample(),
            },
        )
        try:
            result = brain.process_episode(
                owned,
                episode_id=observation["occurrence_id"],
                **copy.deepcopy(self.spec["call_flags"][phase]),
            )
        except BaseException as error:
            self.writer.write(label + "-raw-error.json", exception_record(error))
            self.capture(label + "-after-processing-error", brain)
            raise
        # The complete typed raw result is written before gates or scientific interpretation.
        self.capture(label + "-raw-return", result, "result")
        require(type(result) is self.result_type, "native result class mismatch", InvariantError)
        require(
            brain.results[-1] is result and brain.base.results[-1] is result.v04_result,
            "native result retention identity",
            InvariantError,
        )
        require(
            len(result.raw_pulses) == len(owned)
            and all(
                a is b
                for a, b in zip(
                    result.raw_pulses,
                    sorted(owned, key=lambda p: (p.time_ms, p.channel)),
                    strict=True,
                )
            ),
            "native raw input identity",
            InvariantError,
        )
        require(result.end_ms == observation["start_ms"] + 72, "decision clock mismatch")
        self.same_graph(
            label + "-caller-unmodified",
            self.capture(label + "-caller-after", callers, "caller"),
            caller_state,
        )
        return result, callers

    def mutate_external(
        self,
        label: str,
        callers: tuple[Any, ...],
        exported: dict[str, Any],
        candidate: Any,
        after: dict[str, Any],
        root_state: dict[str, Any],
    ) -> None:
        targets = [(f"caller[{i}].metadata", pulse.metadata) for i, pulse in enumerate(callers)]
        targets += [
            ("export.features", exported["features"]),
            ("export.binding", exported["binding"]),
        ]
        require(
            len(targets) == 8 and len({id(obj) for _, obj in targets}) == 8,
            "eight distinct actual external targets required",
            InvariantError,
        )
        for index, (path, target) in enumerate(targets):
            self.budget.check()
            before = json.loads(canonical(target))
            self.bump({"external_object_mutations": 1})
            self.writer.write(
                f"{label}-mutation-{index}-attempt.json",
                {
                    "actual_target_path": path,
                    "before": before,
                    "counts_including_attempt": self.counts,
                },
            )
            if path == "export.features":
                target.append(-1.0)
            else:
                target["external_mutation_probe"] = True
            self.writer.write(
                f"{label}-mutation-{index}-returned.json",
                {
                    "actual_target_path": path,
                    "after": target,
                },
            )
        self.same_graph(
            label + "-candidate-after-eight-mutations",
            self.capture(label + "-candidate-after-eight-mutations", candidate),
            after,
        )
        self.root_exact(label + "-root-after-eight-mutations", root_state)
        self.capture(label + "-mutated-callers", callers, "caller")
        self.writer.write(label + "-mutated-diagnostic-export.json", exported)
        # Deliberately no further process call on this candidate, including blocked exports.

    def execute(
        self, factory: Any, prepared: dict[str, Any], records: list[dict[str, Any]]
    ) -> None:
        for seed_index, seed in enumerate(SEEDS):
            label = f"seed-{seed}"
            self.stage = label + "-constructor"
            self.budget.check()
            self.brains = {}
            self.owner = None
            self.bump({"roots": 1})
            self.writer.write(
                label + "-constructor-attempt.json",
                {
                    "counts_including_attempt": self.counts,
                    "configuration": self.spec["configuration"],
                    "resources": self.budget.sample(),
                },
            )
            try:
                root = factory(
                    copy.deepcopy(prepared["brain"]),
                    receptor_config=copy.deepcopy(prepared["receptor"]),
                    assembly_config=copy.deepcopy(prepared["assembly"]),
                    homeostasis_config=copy.deepcopy(prepared["homeostasis"]),
                    plasticity_config=copy.deepcopy(prepared["plasticity"]),
                    action_config=copy.deepcopy(prepared["action"]),
                )
            except BaseException as error:
                self.writer.write(label + "-constructor-error.json", exception_record(error))
                raise
            self.brains["root"] = root
            self.owner = PrivateOwner(root)
            self.capture(label + "-initial", root)
            require(type(root.action_policy.config.actions) is tuple, "actual native action tuple")
            configuration = actual_configuration(root)
            self.writer.write(label + "-actual-configuration.json", configuration)
            require(
                canonical(configuration) == canonical(self.spec["configuration"]),
                "actual complete configuration mismatch",
            )
            rows = records[seed_index * 68 : (seed_index + 1) * 68]
            for index, row in enumerate(rows[:64]):
                self.step(root, row, f"{label}-acquire-{index:02d}")
                if (index + 1) % 16 == 0:
                    self.progress(f"{label}: acquisition {index + 1}/64")
            root_state = self.capture(label + "-acquired", root)
            learned = self.capture(label + "-frozen-learning", learned_state(root), "learning")
            self.writer.write(label + "-acquired-alias-witnesses.json", identity_witnesses(root))
            dictionary = freeze_dictionary(root.assemblies)
            dictionary_bytes = canonical(dictionary)
            self.writer.write(label + "-dictionary.json", dictionary)
            self.capture(label + "-candidate-inventory", root.assemblies, "assemblies")
            require(
                dictionary["binding"]["N"] <= 32 and len(root.assemblies.candidates) <= 32,
                "native bank cap exceeded",
                InvariantError,
            )
            snapshots = {"root": root_state}
            # Four independent fresh memos, all before the first query regardless of N.
            for branch in BRANCHES:
                self.stage = label + "-copy-" + branch
                self.budget.check()
                self.bump({"whole_brain_copies": 1})
                self.writer.write(
                    self.stage + "-attempt.json",
                    {
                        "counts_including_attempt": self.counts,
                        "fresh_memo": True,
                        "resources": self.budget.sample(),
                    },
                )
                try:
                    candidate = copy.deepcopy(root, {})
                except BaseException as error:
                    self.writer.write(self.stage + "-error.json", exception_record(error))
                    raise
                self.brains[branch] = candidate
                snapshots[branch] = self.capture(self.stage, candidate)
                self.same_graph(self.stage, snapshots[branch], root_state)
            self.root_exact(label + "-root-after-copies", root_state)
            self.pairwise(label + "-all-copies-before-queries", snapshots)
            self.progress(label + ": four independent copies ready")
            outputs: dict[str, dict[str, Any]] = {}
            query_graphs: dict[str, dict[str, Any]] = {}
            for row in rows[64:]:
                branch = row["branch"]
                query_label = label + "-query-" + branch
                candidate = self.brains[branch]
                result, callers = self.step(candidate, row, query_label)
                after = self.capture(query_label + "-candidate", candidate)
                query_graphs[branch] = after
                snapshots[branch] = after
                self.writer.write(
                    query_label + "-alias-witnesses.json", identity_witnesses(candidate)
                )
                self.root_exact(query_label + "-root-after-query", root_state)
                self.same_graph(
                    query_label + "-learning-frozen",
                    self.capture(query_label + "-learning", learned_state(candidate), "learning"),
                    learned,
                )
                self.pairwise(query_label + "-live-graphs", snapshots)
                exported, matching = export_native(
                    candidate, result, row["observation"], dictionary, self.similarity
                )
                self.writer.write(query_label + "-export.json", exported)
                self.writer.write(query_label + "-matching.json", matching)
                # Keep exact preserved export bytes before mutating the actual detached object.
                outputs[branch] = json.loads(canonical(exported))
                caller_snapshot = self.capture(query_label + "-external-input", callers, "caller")
                external_ids = set(primitive_tree(exported))
                dictionary_ids = set(primitive_tree(dictionary))
                common = external_ids & (
                    after["mutable"] | caller_snapshot["mutable"] | dictionary_ids
                )
                self.writer.write(
                    query_label + "-export-isolation.json",
                    {
                        "shared_mutable_count": len(common),
                        "candidate_inventory": after["sha256"],
                        "caller_inventory": caller_snapshot["sha256"],
                        "frozen_dictionary_included": True,
                    },
                )
                require(not common, "primitive export aliases candidate/caller", InvariantError)
                self.mutate_external(query_label, callers, exported, candidate, after, root_state)
                dictionary_unchanged = canonical(dictionary) == dictionary_bytes
                self.writer.write(
                    query_label + "-frozen-dictionary-guard.json",
                    {
                        "exact_canonical_bytes_unchanged": dictionary_unchanged,
                        "before_sha256": hashlib.sha256(dictionary_bytes.encode()).hexdigest(),
                        "after_sha256": hashlib.sha256(canonical(dictionary).encode()).hexdigest(),
                    },
                )
                require(dictionary_unchanged, "frozen dictionary mutated", InvariantError)
                self.progress(query_label + ": raw/export and ownership checks preserved")
            result_summary = summarize_seed(seed, dictionary, outputs, query_graphs, rows[64:])
            self.writer.write(label + "-summary.json", result_summary)
            self.seed_results.append(result_summary)
            self.root_exact(label + "-final-root", root_state)
            self.progress(label + ": complete")
        require(self.counts == MAX_COUNTS, "incomplete fixed attempt plan", InvariantError)


def summarize_seed(
    seed: int,
    dictionary: dict[str, Any],
    outputs: dict[str, dict[str, Any]],
    graphs: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    repeats = {
        branch: {
            "full_native_graph_equal": graphs[branch]["bytes"]
            == graphs[branch + "_repeat"]["bytes"],
            "complete_export_equal": canonical(outputs[branch])
            == canonical(outputs[branch + "_repeat"]),
        }
        for branch in ("A", "B")
    }
    repeat_ok = all(all(row.values()) for row in repeats.values())
    accepted = all(output["accepted"] for output in outputs.values())
    distance = math.dist(outputs["A"]["features"], outputs["B"]["features"]) if accepted else None
    status = (
        "repeat_failure"
        if not repeat_ok
        else "representation_withheld"
        if not accepted
        else (
            "producer_contrast_observed"
            if outputs["A"]["features"] != outputs["B"]["features"]
            else "producer_alias"
        )
    )
    rasters = {row["branch"]: raw_raster(row["observation"]) for row in records}
    n = dictionary["binding"]["N"]
    return {
        "seed": seed,
        "status": status,
        "dimension": n,
        "single_candidate": n == 1,
        "vectors": {key: value["features"] for key, value in outputs.items()},
        "export_statuses": {key: value["status"] for key, value in outputs.items()},
        "repeats": repeats,
        "euclidean_distance": distance,
        "ownership_guards": "passed",
        "future_m1_capacity": "future_m1_capacity_blocked" if n > 7 else "default_capacity_only",
        "source_only_scope_birth_reference": 0.25,
        "distance_exceeds_source_reference": distance > 0.25 if distance is not None else None,
        "raw410_l1": sum(abs(a - b) for a, b in zip(rasters["A"], rasters["B"], strict=True)),
        "raw410_exact_repeats": {
            branch: rasters[branch] == rasters[branch + "_repeat"] for branch in ("A", "B")
        },
        "actual_m1_execution": "not_performed",
        "learned_consumer_benefit": "not_tested",
        "joint_atomicity": "not_tested",
        "scientific_credit": 0,
        "claim_ceiling": "Representation prerequisite for fixed inherited histories only",
    }


def run(root: Path, output: Path, freeze_path: Path, freeze_sha256: str) -> int:
    """Opt-in only; source/config/origin guards precede the first producer constructor."""
    budget = Budget()
    writer = EvidenceWriter(output)
    probe: Probe | None = None
    terminal: dict[str, Any] = {
        "status": "incomplete",
        "classification": "EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY",
        "scientific_credit": 0,
        "no_retry": True,
        "actual_m1_execution": "not_performed",
        "learned_consumer_benefit": "not_tested",
        "joint_atomicity": "not_tested",
        "hard_termination_limitation": "SIGKILL/OOM can prevent finalization; retain partial files",
        "native_hashes_are_ownership_oracles": False,
    }
    try:
        budget.install()
        require("--run-reviewed" in sys.argv, "reviewed execution must be explicitly selected")
        require(
            not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules),
            "producer must not already be imported",
        )
        timeout_parent = verify_timeout_parent()
        spec, schema, records = read_protocol(root)
        frozen = verify_freeze(root, freeze_path, freeze_sha256, spec)
        require(Path(frozen["output_directory"]) == output, "freeze output directory mismatch")
        writer.write_bytes("literal-inputs.jsonl", (root / INPUTS_PATH).read_bytes())
        writer.write_bytes("source-freeze.json", freeze_path.read_bytes())
        writer.write(
            "preflight.json",
            {
                "protocol_sha256": PROTOCOL_SHA256,
                "document_sha256": DOCUMENT_SHA256,
                "inputs_sha256": INPUTS_SHA256,
                "implementation_freeze_sha256": freeze_sha256,
                "package_sources_sha256": spec["package_sources_sha256"],
                "source_pin": SOURCE_PIN,
                "python": sys.version,
                "platform": sys.platform,
                "uname": list(os.uname()),
                "argv": sys.argv,
                "pid": os.getpid(),
                "external_timeout": timeout_parent,
                "limits": LIMITS,
                "finalization_reserves_inside_limits": RESERVE,
                "max_counts": MAX_COUNTS,
                "resources": budget.sample(),
                "network_enforcement": "Python audit hook only, not OS isolation",
            },
        )
        sys.addaudithook(deny_network_and_subprocess)
        sys.dont_write_bytecode = True
        cache = output / "empty_bytecode_cache"
        cache.mkdir(mode=0o700, exist_ok=False)
        sys.pycache_prefix = str(cache)
        sys.path.insert(0, str(root / "src"))
        budget.check()
        # Only these opt-in paths load native code; model-free modes never enter run().
        from sparkbrain.v04.contracts import SignalPulse
        from sparkbrain.v05.assemblies import pattern_similarity
        from sparkbrain.v05.brain import IntegratedV05Brain
        from sparkbrain.v05.contracts import V05StepResult

        audit = GraphAudit.from_schema(schema)
        writer.write("loaded-source-origins.json", loaded_source_origins(root, spec))
        require(not any(cache.rglob("*")), "unexpected bytecode cache")
        # Config dataclasses are checked before topology/producer creation. The six internal
        # base configurations are additionally checked on each constructed producer before input.
        prepared = {}
        for key, (path, name) in CONFIG_TYPES.items():
            module = importlib.import_module(
                "sparkbrain." + path.removesuffix(".py").replace("/", ".")
            )
            prepared[key] = getattr(module, name)(
                **config_arguments(key, spec["configuration"][key])
            )
        require(type(prepared["action"].actions) is tuple, "native action tuple required")
        preflight_configs = {key: dataclasses.asdict(value) for key, value in prepared.items()}
        writer.write("configuration-preflight.json", preflight_configs)
        require(
            canonical(preflight_configs) == canonical(spec["configuration"]), "config preflight"
        )
        writer.write(
            "loaded-source-origins-before-construction.json", loaded_source_origins(root, spec)
        )
        probe = Probe(spec, audit, writer, budget, SignalPulse, V05StepResult, pattern_similarity)
        probe.execute(IntegratedV05Brain, prepared, records)
        writer.write("loaded-source-origins-after-plan.json", loaded_source_origins(root, spec))
        terminal["status"] = "fixed_plan_complete"
    except BaseException as error:
        budget.finish()
        writer.finalizing = True
        terminal.update(
            {
                "status": "resource_stopped" if isinstance(error, BudgetError) else "stopped",
                "failure": exception_record(error),
                "failure_stage": probe.stage if probe else "preflight",
            }
        )
        try:
            writer.write("terminal-error.json", terminal["failure"])
            if probe is not None:
                for label, brain in probe.brains.items():
                    probe.capture("terminal-partial-" + label, brain)
        except BaseException as preservation_error:
            terminal["partial_preservation_error"] = exception_record(preservation_error)
    finally:
        budget.finish()
        writer.finalizing = True
        terminal["counts"] = probe.counts if probe else dict.fromkeys(MAX_COUNTS, 0)
        terminal["seed_results"] = probe.seed_results if probe else []
        terminal["resources"] = budget.sample()
        terminal["artifact_bytes_before_terminal"] = writer.bytes_written
        terminal["incomplete_files"] = [
            name for name, complete in writer.files.items() if not complete
        ]
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
            print(
                canonical({"status": terminal["status"], "counts": terminal["counts"]}), flush=True
            )
        except BaseException as error:
            print(f"Finalization incomplete: {type(error).__name__}: {error}", file=sys.stderr)
            return 2
    return 0 if terminal["status"] == "fixed_plan_complete" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check-source", action="store_true", help="Read sources; never import the model"
    )
    mode.add_argument(
        "--run-reviewed", action="store_true", help="Execute the separately reviewed freeze"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-freeze", type=Path)
    parser.add_argument("--source-freeze-sha256")
    args = parser.parse_args()
    if bool(args.source_freeze) != bool(args.source_freeze_sha256):
        parser.error("source-freeze path and SHA-256 are required together")
    root = Path(__file__).resolve().parents[1]
    if args.check_source:
        before = {
            name: value
            for name, value in sys.modules.copy().items()
            if name == "sparkbrain" or name.startswith("sparkbrain.")
        }
        spec, schema, records = read_protocol(root)
        if args.source_freeze:
            verify_freeze(root, args.source_freeze, args.source_freeze_sha256, spec)
        after = {
            name: value
            for name, value in sys.modules.copy().items()
            if name == "sparkbrain" or name.startswith("sparkbrain.")
        }
        require(before == after, "source check imported producer modules")
        print(
            canonical(
                {
                    "status": "source_check_passed",
                    "model_imported": False,
                    "package_source_files": len(spec["package_sources_sha256"]),
                    "schema_classes": sum(len(r["classes"]) for r in schema["files"].values()),
                    "input_records": len(records),
                    "protocol_sha256": PROTOCOL_SHA256,
                    "implementation_freeze_checked": bool(args.source_freeze),
                }
            )
        )
        return 0
    if not args.source_freeze or not args.output:
        parser.error("reviewed execution requires --output and exact separately reviewed freeze")
    return run(root, args.output.resolve(), args.source_freeze.resolve(), args.source_freeze_sha256)


if __name__ == "__main__":
    raise SystemExit(main())
