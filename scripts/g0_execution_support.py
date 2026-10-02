"""Source-only preparation and dormant support for the prospective G0 identity.

Importing this module never imports SparkBrain, installs limits/hooks, writes evidence,
creates a model, or authorizes execution. File hashes are a trusted-source-tree contract,
not in-memory code attestation or protection against concurrent malicious mutation.
"""
from __future__ import annotations

import ast
import dis
import hashlib
import json
import math
import os
import platform
import stat
import sys
import sysconfig
import threading
import time
import types
import weakref
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from scripts.verify_g0_joint_source_contract import (
    CONTRACT,
    CONTRACT_SHA256,
    confined_path,
    path_metadata,
    source_root,
    verify,
)

IDENTITY = "assembly-m1-g0-v1-20261002"
ARTIFACT_ROOT = "artifacts/research/assembly_m1_g0_v1_20261002"
FILESYSTEM_DURABILITY_BOUNDARY = (
    "Acknowledged evidence requires file and directory fsync on this mounted filesystem. "
    "Older directory ancestors are trusted durably provisioned storage. "
    "A crash before reservation-directory fsync completes leaves consumption uncertain; "
    "an absent marker is not permission to retry. Storage deletion, ephemeral-storage loss, "
    "and a filesystem that does not honor successful fsync are outside this guarantee."
)
LIMITS = {"cpu_seconds": 600, "wall_seconds": 900,
          "address_space_bytes": 1 << 30, "output_bytes": 256 << 20}
RESERVES = {"cpu_seconds": 30, "wall_seconds": 45,
            "address_space_bytes": 32 << 20, "output_bytes": 16 << 20}
HASH_CHUNK_BYTES = 1 << 20
PROFILE_CHECK_INTERVAL = 4096
CODE_KEY_CACHE_LIMIT = 8192
CALL_CAPS = {
    "clone_joint": 14, "v05_init": 1, "v03_init": 1, "m1_init": 1,
    "v05_process_episode": 70, "m1_observe": 5, "m1_apply_outcome": 6,
    "predictive_feedback": 4, "scope_step": 3, "producer_learn_outcome": 0,
    "pilot_checkpoint_save": 9, "direct_checkpoint_save": 9,
    "direct_checkpoint_load_bytes": 10, "facade_init": 25,
    "rawbrain_shell": 24, "v05_shell": 14, "model_rng": 25,
    "topology_rng": 1, "model_lock": 25, "registry_guard": 1,
    "pilot_checkpoint_load": 1, "direct_checkpoint_load": 1,
    "predictive_init": 2, "scope_init": 2, "scope_router_init": 3,
}
CALL_TARGETS = {
    "clone_joint": ("scripts/g0_joint_ownership.py", "clone_joint"),
    "v05_init": ("src/sparkbrain/v05/brain.py", "IntegratedV05Brain.__init__"),
    "v03_init": ("src/sparkbrain/v03/runtime.py", "IntegratedV03Brain.__init__"),
    "m1_init": ("src/sparkbrain/system_build/integrated_m1.py", "IntegratedM1Pilot.__init__"),
    "predictive_init": ("src/sparkbrain/system_build/predictive_revision.py",
                        "PredictiveRevisionPilot.__init__"),
    "scope_init": ("src/sparkbrain/system_build/causal_scope_revision.py",
                   "CausalScopeRevisionPilot.__init__"),
    "scope_router_init": ("src/sparkbrain/system_build/causal_scope_revision.py",
                          "CausalScopeRouter.__init__"),
    "v05_process_episode": ("src/sparkbrain/v05/brain.py", "IntegratedV05Brain.process_episode"),
    "m1_observe": ("src/sparkbrain/system_build/integrated_m1.py", "IntegratedM1Pilot.observe"),
    "m1_apply_outcome": ("src/sparkbrain/system_build/integrated_m1.py",
                         "IntegratedM1Pilot.apply_outcome"),
    "predictive_feedback": ("src/sparkbrain/system_build/predictive_revision.py",
                            "PredictiveRevisionPilot.feedback"),
    "scope_step": ("src/sparkbrain/system_build/causal_scope_revision.py",
                   "CausalScopeRevisionPilot.step"),
    "producer_learn_outcome": ("src/sparkbrain/v05/brain.py", "IntegratedV05Brain.learn_outcome"),
    "pilot_checkpoint_save": ("src/sparkbrain/system_build/predictive_revision.py",
                              "PilotCheckpointManager.save"),
    "direct_checkpoint_save": ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager.save"),
    "direct_checkpoint_load": ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager.load"),
    "pilot_checkpoint_load": ("src/sparkbrain/system_build/predictive_revision.py",
                              "PilotCheckpointManager.load"),
    "direct_checkpoint_load_bytes": ("src/sparkbrain/v032/checkpoint.py",
                                      "DirectCheckpointManager._load_bytes"),
    "facade_init": ("src/sparkbrain/v032/runtime.py", "IntegratedV032Brain.__init__"),
}


def protocol_call_caps(counts: Mapping[str, int] | None = None) -> dict[str, int]:
    """Explicit reconciliation of lower-level births and the published protocol totals."""
    values = CALL_CAPS if counts is None else counts
    result = {name: values[name] for name in (
        "clone_joint", "direct_checkpoint_load", "direct_checkpoint_save", "facade_init",
        "m1_apply_outcome", "m1_init", "m1_observe", "pilot_checkpoint_load",
        "pilot_checkpoint_save", "predictive_feedback", "producer_learn_outcome",
        "scope_step", "v03_init", "v05_init", "predictive_init", "scope_init", "scope_router_init")}
    result.update({"producer_process_episode": values["v05_process_episode"],
                   "direct_load_bytes": values["direct_checkpoint_load_bytes"],
                   "model_rng_init": values["model_rng"],
                   "topology_rng_init": values["topology_rng"],
                   "v03_allocations": values["rawbrain_shell"] + values["v03_init"],
                   "v05_allocations": values["v05_shell"] + values["v05_init"]})
    return result


BIRTH_TYPES = {
    "v03_init": "sparkbrain.v03.runtime.IntegratedV03Brain",
    "rawbrain_shell": "sparkbrain.v03.runtime.IntegratedV03Brain",
    "v05_init": "sparkbrain.v05.brain.IntegratedV05Brain",
    "v05_shell": "sparkbrain.v05.brain.IntegratedV05Brain",
    "facade_init": "sparkbrain.v032.runtime.IntegratedV032Brain",
    "m1_init": "sparkbrain.system_build.integrated_m1.IntegratedM1Pilot",
    "predictive_init": "sparkbrain.system_build.predictive_revision.PredictiveRevisionPilot",
    "scope_init": "sparkbrain.system_build.causal_scope_revision.CausalScopeRevisionPilot",
    "scope_router_init": "sparkbrain.system_build.causal_scope_revision.CausalScopeRouter",
    "model_rng": "random.Random", "topology_rng": "random.Random",
    "model_lock": "_thread.RLock", "registry_guard": "_thread.lock",
}


def expected_lifecycle_returns() -> dict[str, int]:
    return {**CALL_CAPS, "m1_apply_outcome": 4}


def expected_lifecycle_birth_counts() -> dict[str, int]:
    return {name: CALL_CAPS[name] for name in BIRTH_TYPES}


def lifecycle_birth_routes(name: str) -> tuple[tuple[str, str], ...]:
    if name in CALL_TARGETS:
        return (CALL_TARGETS[name],)
    if name == "rawbrain_shell":
        return (("scripts/g0_joint_ownership.py", "_construct"),
                ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes"))
    if name == "v05_shell":
        return (("scripts/g0_joint_ownership.py", "_construct"),)
    if name in {"model_rng", "topology_rng"}:
        return (("", "Random.__init__"),)
    if name == "model_lock":
        return (("", "RLock"),)
    if name == "registry_guard":
        return (("src/sparkbrain/v032/runtime.py", "<module>"),)
    raise AdmissionError("unknown resource birth route")


def validate_completed_lifecycle(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Pure primitive validation; attempted calls alone can never establish completion."""
    value = primitive(snapshot)
    required = {"counts", "caps", "returned", "failure", "pending_calls", "pending_shells",
                "births", "events", "live_resource_ids", "threads_seen", "ancillary_rngs",
                "counts_before_body", "protocol_counts"}
    if type(value) is not dict or not required <= value.keys():
        raise AdmissionError("lifecycle completion evidence is missing required fields")
    returns = expected_lifecycle_returns()
    expected_births = expected_lifecycle_birth_counts()
    if (value["failure"] is not None or value["counts_before_body"] is not True
            or canonical(value["counts"]) != canonical(CALL_CAPS)
            or canonical(value["caps"]) != canonical(CALL_CAPS)
            or canonical(value["protocol_counts"]) != canonical(protocol_call_caps())
            or canonical(value["returned"]) != canonical(returns)):
        raise AdmissionError("lifecycle attempts/returns/failure differ from the frozen completion")
    if value["pending_calls"] != [] or value["pending_shells"] != []:
        raise AdmissionError("lifecycle completion has pending calls or shell allocations")
    threads = value["threads_seen"]
    if (type(threads) is not list or not threads
            or any(type(item) is not int or item <= 0 for item in threads)
            or len(set(threads)) != len(threads)):
        raise AdmissionError("lifecycle thread identifiers are invalid")
    births, events = value["births"], value["events"]
    if type(births) is not list or type(events) is not list:
        raise AdmissionError("lifecycle birth/event ledgers must be complete lists")
    actual_births = dict.fromkeys(expected_births, 0)
    birth_by_id = {}
    guard_id = None
    birth_fields = {"birth_id", "name", "runtime_id", "type", "source_route", "thread"}
    for index, birth in enumerate(births, 1):
        if type(birth) is not dict or set(birth) != birth_fields:
            raise AdmissionError("resource birth ledger schema differs")
        name = birth["name"]
        route = birth["source_route"]
        if (type(birth["birth_id"]) is not int or birth["birth_id"] != index
                or type(name) is not str or name not in expected_births
                or type(birth["runtime_id"]) is not int
                or birth["runtime_id"] <= 0 or type(birth["thread"]) is not int
                or birth["thread"] not in threads
                or birth["type"] != BIRTH_TYPES[name]
                or type(route) is not list or tuple(route) not in lifecycle_birth_routes(name)):
            raise AdmissionError("resource birth identity/type/source route is inconsistent")
        actual_births[name] += 1
        birth_by_id[index] = birth
        if name == "registry_guard":
            guard_id = birth["runtime_id"]
    if actual_births != expected_births:
        raise AdmissionError("resource birth counts differ from the frozen completion")
    if (canonical(value["live_resource_ids"]) != canonical([guard_id])
            or sum(birth["runtime_id"] == guard_id for birth in births) != 1):
        raise AdmissionError("model resources remain live or registry guard lifetime differs")
    attempts = dict.fromkeys(CALL_CAPS, 0)
    normal = dict.fromkeys(CALL_CAPS, 0)
    exceptional = dict.fromkeys(CALL_CAPS, 0)
    observed_birth_ids = []
    ancillary = 0
    for index, event in enumerate(events, 1):
        if (type(event) is not dict or type(event.get("sequence")) is not int
                or event["sequence"] != index or type(event.get("thread")) is not int
                or event.get("thread") not in threads):
            raise AdmissionError("passive event ledger sequence/thread differs")
        kind, name = event.get("kind"), event.get("name")
        if kind == "ancillary_rng":
            if name != "stdlib_rng":
                raise AdmissionError("unrecognized ancillary resource event")
            ancillary += 1
            continue
        if type(name) is not str or name not in CALL_CAPS:
            raise AdmissionError("passive event names an unplanned model call")
        if kind == "call_attempt":
            attempts[name] += 1
            if type(event.get("attempt")) is not int or event["attempt"] != attempts[name]:
                raise AdmissionError("passive attempt sequence differs")
        elif kind == "call_return":
            normal[name] += 1
            if normal[name] + exceptional[name] > attempts[name]:
                raise AdmissionError("passive return precedes its attempted call")
        elif kind == "call_exception":
            exceptional[name] += 1
            if normal[name] + exceptional[name] > attempts[name]:
                raise AdmissionError("passive exception precedes its attempted call")
        elif kind == "resource_birth":
            birth = {key: item for key, item in event.items() if key not in {"sequence", "kind"}}
            birth_id = birth.get("birth_id")
            if canonical(birth) != canonical(birth_by_id.get(birth_id)):
                raise AdmissionError("passive resource event differs from the actual birth ledger")
            observed_birth_ids.append(birth_id)
        else:
            raise AdmissionError("unrecognized passive lifecycle event")
    expected_exceptions = {name: CALL_CAPS[name] - returns[name] for name in CALL_CAPS}
    if (attempts != CALL_CAPS or normal != returns or exceptional != expected_exceptions
            or observed_birth_ids != list(range(1, len(births) + 1))
            or type(value["ancillary_rngs"]) is not int or value["ancillary_rngs"] != ancillary):
        raise AdmissionError("passive events do not reconcile with attempts/returns/births")
    return {"validated": True, "attempted_counts": dict(CALL_CAPS),
            "normal_returns": returns, "exceptional_exits": expected_exceptions,
            "birth_counts": actual_births, "births": len(births),
            "live_registry_guard_id": guard_id, "model_resources_live": 0}


class AdmissionError(ValueError):
    """Preparation or independently authorized execution admission failed."""


class BudgetExceeded(BaseException):
    """Terminal stop; deliberately bypass native ``except Exception`` rollback."""


def primitive(value: Any) -> Any:
    """Copy exact primitive values only; never retain model/frame/exception references."""
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if type(value) in (list, tuple):
        return [primitive(item) for item in value]
    if type(value) is dict and all(type(key) is str for key in value):
        return {key: primitive(item) for key, item in value.items()}
    raise AdmissionError("evidence must contain exact finite JSON primitives")


def canonical(value: Any) -> bytes:
    return (json.dumps(primitive(value), sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise AdmissionError("duplicate JSON key")
        result[key] = value
    return result


def read_json(path: Path) -> Any:
    path = Path(path)
    checked = confined_path(source_root(path.parent), path.name, "JSON input")
    return primitive(json.loads(checked.read_bytes(), object_pairs_hook=_pairs))


def file_digest(path: Path, *, checkpoint: Callable[[], Any] | None = None) -> str:
    """Bound hash work between reserve samples; never log from a checkpoint."""
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            if checkpoint is not None:
                checkpoint()
            chunk = stream.read(HASH_CHUNK_BYTES)
            if not chunk:
                break
            value.update(chunk)
    return value.hexdigest()


def source_inventory(root: Path, paths: list[str], *,
                     checkpoint: Callable[[], Any] | None = None) -> dict[str, str]:
    root = source_root(root)
    if len(set(paths)) != len(paths):
        raise AdmissionError("duplicate source inventory path")
    result = {}
    for name in sorted(paths):
        if checkpoint is not None:
            checkpoint()
        result[name] = file_digest(confined_path(root, name, "frozen source"),
                                   checkpoint=checkpoint)
    return result


def _walk_importable(directory: Path, *,
                     checkpoint: Callable[[], Any] | None = None) -> dict[str, str]:
    """Hash importable code and package metadata; never arbitrary user documents."""
    root = source_root(directory)
    pending = [root]
    result = {}
    while pending:
        if checkpoint is not None:
            checkpoint()
        current = pending.pop()
        for path in sorted(current.iterdir()):
            if checkpoint is not None:
                checkpoint()
            info = path_metadata(path, "environment dependency")
            if stat.S_ISDIR(info.st_mode):
                if current == root and path.name in {"site-packages", "dist-packages"}:
                    continue  # Active installed packages are separate explicit roots.
                # Private home trees are never scanned: only supplied interpreter roots.
                pending.append(path)
            elif (path.suffix in {".py", ".pyc", ".pyo", ".so", ".pyd", ".dll",
                                      ".pth", ".egg-link", ".zip"}
                  or (path.parent.name.endswith((".dist-info", ".egg-info"))
                      and path.name in {"METADATA", "PKG-INFO", "RECORD", "WHEEL",
                                        "entry_points.txt", "top_level.txt"})):
                result[path.relative_to(root).as_posix()] = file_digest(
                    path, checkpoint=checkpoint)
    return result


def mapped_code_snapshot(*, checkpoint: Callable[[], Any] | None = None) -> dict[str, str]:
    """Hash only actual executable file mappings, never anonymous memory or broad trees."""
    if sys.platform != "linux":
        raise AdmissionError("native library admission requires Linux /proc")
    result = {}
    for line in Path("/proc/self/maps").read_text().splitlines():
        if checkpoint is not None:
            checkpoint()
        fields = line.split(maxsplit=5)
        if len(fields) != 6 or "x" not in fields[1] or not fields[5].startswith("/"):
            continue
        name = fields[5]
        if name.endswith(" (deleted)"):
            raise AdmissionError("deleted executable mapping is outside the frozen environment")
        path = Path(name)
        checked = confined_path(source_root(path.parent), path.name, "mapped executable library")
        with checked.open("rb") as stream:
            header = stream.read(4)
        if header != b"\x7fELF":
            raise AdmissionError("non-ELF executable mapping is outside the frozen environment")
        result[name] = file_digest(checked, checkpoint=checkpoint)
    return result


def verify_mapped_libraries(environment: dict[str, Any], *,
                            checkpoint: Callable[[], Any] | None = None) -> dict[str, str]:
    declared = {**environment["native_code_sha256"], **environment["system_libraries_sha256"],
                environment["executable"]: environment["executable_sha256"]}
    current = (mapped_code_snapshot() if checkpoint is None
               else mapped_code_snapshot(checkpoint=checkpoint))
    if any(declared.get(name) != sha for name, sha in current.items()):
        raise AdmissionError("new or changed executable mapping is outside the frozen environment")
    # Previously mapped system libraries remain pinned even when a process unloads them.
    for name, sha in environment["system_libraries_sha256"].items():
        path = Path(name)
        checked = confined_path(source_root(path.parent), path.name, "frozen system library")
        if file_digest(checked, checkpoint=checkpoint) != sha:
            raise AdmissionError("frozen system library changed")
    return current


def require_passive_lock_api() -> None:
    """Fail before execution on an allocator shape without reviewed passive events."""
    if (type(threading.Lock) is not types.BuiltinFunctionType
            or threading.Lock.__module__ != "_thread"
            or threading.Lock.__name__ != "allocate_lock"):
        raise AdmissionError("unsupported passive lock allocator API; exact builtin required")


def environment_snapshot(root: Path | None = None, *,
                         checkpoint: Callable[[], Any] | None = None) -> dict[str, Any]:
    """Source-only interpreter/dependency snapshot. No package imports or secrets."""
    if platform.python_implementation() != "CPython" or sys.version_info < (3, 11):
        raise AdmissionError("only reviewed CPython 3.11+ is supported")
    require_passive_lock_api()
    root = source_root(Path.cwd() if root is None else root)
    executable = Path(sys.executable).resolve(strict=True)
    path_metadata(executable, "interpreter binary")
    roots = sorted({str(Path(sysconfig.get_path(key)).resolve(strict=True))
                    for key in ("stdlib", "purelib", "platlib")})
    external_archives = {}
    for entry in sys.path:
        if checkpoint is not None:
            checkpoint()
        path = Path(entry or Path.cwd()).absolute()
        if path.is_relative_to(root):
            continue  # Selected source is inventoried by the exact source freeze.
        if not path.exists():
            external_archives[str(path)] = None
            continue
        info = path_metadata(path, "import search path")
        if stat.S_ISDIR(info.st_mode):
            if not any(path.is_relative_to(Path(item)) for item in roots):
                roots.append(str(source_root(path)))
        else:
            checked = confined_path(source_root(path.parent), path.name, "import archive")
            external_archives[str(path)] = file_digest(checked, checkpoint=checkpoint)
    roots = sorted(set(roots))
    inventories = {item: _walk_importable(Path(item), checkpoint=checkpoint) for item in roots}
    native_code = {str(Path(directory) / name): sha
                   for directory, files in inventories.items() for name, sha in files.items()
                   if Path(name).suffix in {".so", ".pyd", ".dll"}}
    mapped = mapped_code_snapshot(checkpoint=checkpoint)
    system_libraries = {name: sha for name, sha in mapped.items()
                        if name not in native_code and name != str(executable)}
    return {
        "schema": "g0-python-environment-v1", "implementation": platform.python_implementation(),
        "version": sys.version, "executable": str(executable),
        "executable_sha256": file_digest(executable, checkpoint=checkpoint),
        "native_code_sha256": native_code, "system_libraries_sha256": system_libraries,
        "prefix": sys.prefix, "base_prefix": sys.base_prefix,
        "platform": sys.platform, "machine": platform.machine(),
        "cache_tag": sys.implementation.cache_tag,
        "dependency_inventory_sha256": digest(canonical(inventories)),
        "dependency_roots": roots,
        "dependency_files": sum(len(items) for items in inventories.values()),
        "external_import_archives": external_archives,
        "venv_configuration_sha256": digest(
            confined_path(source_root(Path(sys.prefix)), "pyvenv.cfg", "venv configuration")
            .read_bytes()) if sys.prefix != sys.base_prefix else None,
        "dont_write_bytecode_required": True, "user_site_disabled_required": True,
    }


def _fixed_envelope(freeze: dict[str, Any]) -> None:
    for key, expected in (("identity", IDENTITY), ("limits", LIMITS), ("reserves", RESERVES),
                          ("call_caps", CALL_CAPS), ("runtime_python_files", 157),
                          ("runtime_schema_files", 15), ("contract_sha256", CONTRACT_SHA256)):
        if canonical(freeze.get(key)) != canonical(expected):
            raise AdmissionError(f"frozen {key} differs from the prospective contract")
    timeout_digest = freeze.get("timeout_executable_sha256")
    if (type(timeout_digest) is not str or len(timeout_digest) != 64
            or any(character not in "0123456789abcdef" for character in timeout_digest)):
        raise AdmissionError("missing exact GNU timeout executable pin")
    if freeze.get("schema") != "g0-execution-freeze-v1":
        raise AdmissionError("unsupported execution freeze schema")
    if freeze.get("runtime_execution_authorized") is not False:
        raise AdmissionError("a freeze must never grant its own execution authority")


def verify_preparation(root: Path, freeze_relative: str,
                       *, check_environment: bool = True,
                       checkpoint: Callable[[], Any] | None = None) -> dict[str, Any]:
    """Check exact source/literals/contracts/environment without loading runtime code."""
    root = source_root(root)
    freeze_path = confined_path(root, freeze_relative, "freeze")
    raw = freeze_path.read_bytes()
    freeze = read_json(freeze_path)
    _fixed_envelope(freeze)
    # Keep the pinned historical verifier unchanged. This coarser audit stage is
    # bracketed by checks; subordinate reads/traversal are not newly checkpointed.
    if checkpoint is not None:
        checkpoint()
    verified = verify(root)
    if checkpoint is not None:
        checkpoint()
    inventory = freeze.get("source_files_sha256")
    if type(inventory) is not dict or freeze_relative in inventory:
        raise AdmissionError("invalid or self-referential source inventory")
    required = {CONTRACT, "scripts/g0_execution_support.py", "scripts/g0_joint_ownership.py",
                "scripts/verify_g0_joint_source_contract.py",
                "scripts/run_g0_joint_eligibility.py", "scripts/v05_history_export_probe.py",
                "tests/test_g0_execution_support.py",
                "tests/test_g0_joint_eligibility_runner.py", "tests/test_g0_joint_ownership.py",
                "tests/test_g0_joint_source_contract.py", "tests/test_g0_execution_protocol.py",
                "docs/research/assembly_m1_g0_execution_preparation_20261002.md"}
    required.update(("scripts/launch_g0_joint_eligibility.py", "tests/test_g0_joint_launcher.py"))
    contract = read_json(confined_path(root, CONTRACT, "contract"))
    required.update(contract["runtime_sources_sha256"])
    required.update(contract["runtime_schema_sha256"])
    required.update(contract["reuse_sources_sha256"])
    for key in ("protocol", "inputs"):
        binding = freeze.get(key)
        if type(binding) is not dict or set(binding) != {"path", "sha256"}:
            raise AdmissionError(f"invalid frozen {key} binding")
        if binding["path"] != f"{ARTIFACT_ROOT}/{key}.json":
            raise AdmissionError(f"frozen {key} must bind the canonical prospective path")
        required.add(binding["path"])
        if inventory.get(binding["path"]) != binding["sha256"]:
            raise AdmissionError(f"frozen {key} is absent from the source inventory")
        value = read_json(confined_path(root, binding["path"], key))
        if key == "protocol":
            if (value.get("identity") != IDENTITY
                    or canonical(value.get("call_caps")) != canonical(protocol_call_caps())
                    or value.get("limits") != LIMITS or value.get("reserves") != RESERVES):
                raise AdmissionError("protocol identity/counters/resource envelope differs")
            literal = value.get("inputs", {})
            if ({"path": literal.get("path"), "sha256": literal.get("sha256")}
                    != freeze.get("inputs")):
                raise AdmissionError("protocol literal binding differs from freeze inputs")
            provenance = value.get("input_provenance", {})
            if provenance.get("source"):
                required.add(provenance["source"])
                if inventory.get(provenance["source"]) != provenance.get("sha256"):
                    raise AdmissionError("historical input provenance inventory differs")
            for path_key, hash_key in (("unique_rows_path", "unique_rows_sha256"),):
                referenced = value.get("inputs", {})
                if referenced.get(path_key):
                    required.add(referenced[path_key])
                    if inventory.get(referenced[path_key]) != referenced.get(hash_key):
                        raise AdmissionError("literal row inventory differs")
    if not required <= inventory.keys():
        raise AdmissionError("incomplete runtime/support/literal inventory")
    if source_inventory(root, list(inventory), checkpoint=checkpoint) != inventory:
        raise AdmissionError("frozen source inventory differs")
    # -B prevents writes, not reads. Reject source bytecode so fresh runtime imports
    # cannot silently consume stale compiled code outside the declared source freeze.
    for directory in ("src/sparkbrain", "scripts"):
        pending = [confined_path(root, directory, "source code directory", directory=True)]
        while pending:
            current = pending.pop()
            for child in current.iterdir():
                if checkpoint is not None:
                    checkpoint()
                info = path_metadata(child, "source bytecode inventory")
                if stat.S_ISDIR(info.st_mode):
                    pending.append(child)
                elif child.suffix in {".pyc", ".pyo"}:
                    raise AdmissionError("preexisting source bytecode is unsupported")
    if check_environment and freeze.get("environment") != environment_snapshot(
            root, checkpoint=checkpoint):
        raise AdmissionError("frozen interpreter/dependency environment differs")
    return {"classification": "SOURCE_ONLY_NON_EVIDENTIARY", "identity": IDENTITY,
            "runtime_execution_authorized": False, "scientific_credit": 0,
            "freeze_sha256": digest(raw), "source_inventory_sha256": digest(canonical(inventory)),
            "source_contract": verified, "freeze": freeze}


_PERMITS: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


class ExecutionPermit:
    """Opaque, process-local admission; public construction never creates authority."""

    def __init__(self) -> None:
        raise AdmissionError("execution permits require separately verified external authority")

    @property
    def root(self) -> Path:
        return _PERMITS[self]["root"]

    @property
    def freeze(self) -> dict[str, Any]:
        return primitive(_PERMITS[self]["verified"]["freeze"])

    @property
    def output_directory(self) -> Path:
        return _PERMITS[self]["output_directory"]

    @property
    def approval_path(self) -> Path:
        record = _PERMITS[self]
        return confined_path(record["root"], record["approval_relative"], "approval")

    @property
    def freeze_path(self) -> Path:
        record = _PERMITS[self]
        return confined_path(record["root"], record["freeze_relative"], "freeze")

    def ensure_authorized(self, root: Path | None = None) -> None:
        require_execution_permit(self, root)


def authorize_execution(root: Path, freeze_relative: str, approval_relative: str,
                        expected_approval_sha256: str,
                        authority_callback: Callable[[dict[str, Any]], bool] | None,
                        ) -> ExecutionPermit:
    """Dormant gate. The caller supplies independently verified publication/authority.

    No bundled approval exists. A local JSON ``approved`` flag, CI pass, source-only
    review, or synthetic fixture is never sufficient. The caller's authority verifier
    belongs to the trusted launch boundary, not to model code or the approval file.
    """
    if authority_callback is None or not callable(authority_callback):
        raise AdmissionError("independent external approval verifier is required")
    if any(name == "sparkbrain" or name.startswith("sparkbrain.") for name in sys.modules):
        raise AdmissionError("fresh frozen runtime imports are required")
    root = source_root(root)
    verified = verify_preparation(root, freeze_relative, checkpoint=ResourceBudget().check)
    approval_path = confined_path(root, approval_relative, "external approval")
    approval_raw = approval_path.read_bytes()
    if not expected_approval_sha256 or digest(approval_raw) != expected_approval_sha256:
        raise AdmissionError("independently supplied approval digest differs")
    approval = read_json(approval_path)
    expected = {"schema": "g0-published-execution-approval-v1", "identity": IDENTITY,
                "freeze_sha256": verified["freeze_sha256"],
                "source_inventory_sha256": verified["source_inventory_sha256"],
                "limits": LIMITS, "reserves": RESERVES, "call_caps": CALL_CAPS,
                "actual_execution_authorized": True}
    if any(canonical(approval.get(key)) != canonical(value) for key, value in expected.items()):
        raise AdmissionError("approval does not bind exact freeze/source/identity/budgets")
    if approval.get("synthetic") is not False:
        raise AdmissionError("synthetic or unspecified authority cannot execute models")
    for key in ("publication", "review", "user_approval"):
        record = approval.get(key)
        if type(record) is not dict or not record.get("reference"):
            raise AdmissionError(f"missing independent {key} evidence")
    if approval["publication"].get("exact_source_sha256") != verified["source_inventory_sha256"]:
        raise AdmissionError("published source differs from the frozen inventory")
    if (approval["review"].get("freeze_sha256") != verified["freeze_sha256"]
            or approval["review"].get("unresolved_findings") != 0):
        raise AdmissionError("review is not clean for the exact freeze")
    output = approval.get("output_directory")
    nonce = approval.get("execution_nonce")
    if (type(output) is not str or not Path(output).is_absolute()
            or type(nonce) is not str or not nonce
            or approval.get("identity_previously_consumed") is not False):
        raise AdmissionError("approval must bind a fresh nonce, unused identity and exact output")
    output_path = source_root(Path(output).parent) / Path(output).name
    if output_path.exists() or output_path.is_symlink():
        raise AdmissionError("approved output was already started or aliases another path")
    ledger_binding = approval.get("identity_ledger")
    if (type(ledger_binding) is not dict
            or set(ledger_binding) != {"path", "sha256", "reference"}
            or not ledger_binding["reference"] or not Path(ledger_binding["path"]).is_absolute()):
        raise AdmissionError("independently verified authoritative identity ledger is required")
    ledger_path = Path(ledger_binding["path"])
    ledger_path = confined_path(source_root(ledger_path.parent), ledger_path.name,
                                "identity ledger")
    if digest(ledger_path.read_bytes()) != ledger_binding["sha256"]:
        raise AdmissionError("authoritative identity ledger digest differs")
    identity_record = read_json(ledger_path).get("identities", {}).get(IDENTITY, {})
    if identity_record.get("state") != "UNCONSUMED":
        raise AdmissionError("identity is absent or already consumed in authoritative ledger")
    reservation_directory = identity_record.get("reservation_directory")
    if type(reservation_directory) is not str or not Path(reservation_directory).is_absolute():
        raise AdmissionError("authoritative identity ledger has no absolute reservation directory")
    reservation_directory = source_root(Path(reservation_directory))
    reservation = reservation_directory / (IDENTITY + ".STARTED.json")
    if reservation.exists() or reservation.is_symlink():
        raise AdmissionError("identity has a durable prior reservation")
    if authority_callback(primitive(approval)) is not True:
        raise AdmissionError("external execution authority was not independently verified")
    permit = object.__new__(ExecutionPermit)
    _PERMITS[permit] = {"root": root, "freeze_relative": freeze_relative,
                        "approval_relative": approval_relative,
                        "approval_sha256": expected_approval_sha256, "verified": verified,
                        "output_directory": output_path, "execution_nonce": nonce,
                        "consumed": False, "identity_reservation": reservation,
                        "identity_ledger_path": ledger_path,
                        "identity_ledger_sha256": ledger_binding["sha256"]}
    return permit


def require_execution_permit(permit: ExecutionPermit, root: Path | None = None, *,
                             checkpoint: Callable[[], Any] | None = None) -> None:
    if type(permit) is not ExecutionPermit or permit not in _PERMITS:
        raise AdmissionError("unissued execution permit")
    record = _PERMITS[permit]
    if root is not None and source_root(root) != record["root"]:
        raise AdmissionError("permit belongs to a different source root")
    current = verify_preparation(record["root"], record["freeze_relative"],
                                 checkpoint=checkpoint)
    if current != record["verified"]:
        raise AdmissionError("execution freeze changed after admission")
    approval = confined_path(record["root"], record["approval_relative"], "approval")
    if digest(approval.read_bytes()) != record["approval_sha256"]:
        raise AdmissionError("approval changed after admission")


_RUNTIME_ADMISSIONS: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


class _RuntimeAdmission:
    """One loader's internal validation receipt, never independent run authority."""

    def __init__(self) -> None:
        raise AdmissionError("runtime admission requires a consumed execution permit")


@contextmanager
def runtime_admission(permit: ExecutionPermit,
                       budget: ResourceBudget) -> Iterator[_RuntimeAdmission]:
    """Validate the whole environment before profiling; invalidate on every exit.

    The source tree/dependency environment remains a trusted dedicated-process
    boundary, not an in-memory code attestation or concurrent-mutation sandbox.
    Neither this receipt nor a successful synthetic test can refresh an old freeze.
    """
    if type(permit) is not ExecutionPermit or permit not in _PERMITS:
        raise AdmissionError("unissued execution permit")
    record = _PERMITS[permit]
    if record.get("consumed") is not True or record.get("budget") is not budget:
        raise AdmissionError("runtime admission requires the consumed permit's budget")
    if record.get("runtime_admission_started"):
        raise AdmissionError("runtime admission is one-shot, including failed preparation")
    record["runtime_admission_started"] = True
    if (sys.getprofile() is not None or threading.getprofile() is not None
            or sys.gettrace() is not None or threading.gettrace() is not None):
        raise AdmissionError("runtime validation must precede profiling hooks")
    if budget.finalizing:
        raise AdmissionError("finalization cannot admit runtime work")
    budget.check()
    require_execution_permit(permit, checkpoint=budget.check)
    token = object.__new__(_RuntimeAdmission)
    _RUNTIME_ADMISSIONS[token] = {
        "permit": permit, "root": record["root"], "budget": budget,
        "thread": threading.get_ident(), "phase": "prepared",
        "freeze_sha256": record["verified"]["freeze_sha256"],
        "approval_sha256": record["approval_sha256"],
        "source_files_sha256": primitive(record["verified"]["freeze"]["source_files_sha256"]),
    }
    try:
        yield token
    finally:
        _RUNTIME_ADMISSIONS.pop(token, None)


def advance_runtime_admission(permit: ExecutionPermit, token: _RuntimeAdmission,
                              budget: ResourceBudget, phase: str) -> None:
    """Ordered import/import-complete/bind gates; no dependency census under profiling."""
    transitions = {"importing": "prepared", "loaded": "importing", "bound": "loaded"}
    admitted = _RUNTIME_ADMISSIONS.get(token) if type(token) is _RuntimeAdmission else None
    record = _PERMITS.get(permit) if type(permit) is ExecutionPermit else None
    if (admitted is None or record is None or admitted["permit"] is not permit
            or admitted["budget"] is not budget or record.get("budget") is not budget
            or record.get("consumed") is not True or admitted["root"] != record["root"]
            or admitted["thread"] != threading.get_ident()
            or transitions.get(phase) != admitted["phase"]):
        raise AdmissionError("invalid, expired or replayed runtime admission")
    # Consume the transition before fallible checks: a failed import gate is final.
    admitted["phase"] = "failed"
    if budget.finalizing:
        raise AdmissionError("finalization cannot admit runtime work")
    budget.check()
    if (record["verified"]["freeze_sha256"] != admitted["freeze_sha256"]
            or record["approval_sha256"] != admitted["approval_sha256"]):
        raise AdmissionError("runtime admission binding changed")
    if phase in {"importing", "loaded"}:
        root = admitted["root"]
        for relative, expected, label in (
                (record["freeze_relative"], admitted["freeze_sha256"], "freeze"),
                (record["approval_relative"], admitted["approval_sha256"], "approval")):
            path = confined_path(root, relative, label)
            if file_digest(path, checkpoint=budget.check) != expected:
                raise AdmissionError(f"{label} changed across runtime import boundary")
        inventory = admitted["source_files_sha256"]
        if source_inventory(root, list(inventory), checkpoint=budget.check) != inventory:
            raise AdmissionError("source changed across runtime import boundary")
    budget.check()
    admitted["phase"] = phase


def fsync_directory(path: Path) -> None:
    """Synchronize one guarded directory; always release its descriptor, never retry."""
    directory = source_root(path)
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_directory_provisioning(path: Path) -> None:
    """Persist this directory's name and contents before creating one-shot evidence.

    The immediate parent contains this directory's name; synchronize both. Older
    ancestors are a trusted durable-provisioning boundary, not newly created here.
    No fsync can promise persistence after cloud/ephemeral storage is deleted.
    """
    directory = source_root(path)
    fsync_directory(directory.parent)
    fsync_directory(directory)


def exclusive_durable_write(path: Path, data: bytes,
                            *, on_created: Callable[[], None] | None = None) -> None:
    """Create once, persist its name before bytes, then acknowledge only full durability.

    The caller first admits the parent directory provisioning. Every post-create failure
    retains the marker/file. The raw descriptor remains ours until fdopen succeeds;
    afterward the handle owns it, including all write/flush/fsync/close failures.
    """
    parent = source_root(path.parent)
    if type(data) is not bytes or Path(path.name).name != path.name:
        raise AdmissionError("durable evidence requires a confined leaf and exact bytes")
    descriptor = os.open(parent / path.name,
                         os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        if on_created is not None:
            on_created()
        # Even an empty consumed marker must be in the durable directory namespace
        # before buffer setup/writes can fail or models can execute.
        fsync_directory(parent)
        handle = os.fdopen(descriptor, "wb")
        descriptor = None  # Ownership transferred only after successful fdopen.
        try:
            if handle.write(data) != len(data):
                raise OSError("short durable evidence write")
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            handle.close()
        # Persist namespace metadata again after the file's complete data/inode sync.
        fsync_directory(parent)
    finally:
        if descriptor is not None:
            os.close(descriptor)


def consume_execution_permit(permit: ExecutionPermit, output_directory: Path,
                             *, budget: ResourceBudget) -> Path:
    """Consume once before the exclusive STARTED directory; never reset after failure."""
    require_execution_permit(permit, checkpoint=budget.check)
    preflight_runtime_limits()
    record = _PERMITS[permit]
    candidate = Path(output_directory)
    candidate = source_root(candidate.parent) / candidate.name
    if candidate != record["output_directory"]:
        raise AdmissionError("execution output differs from independently approved destination")
    if record["consumed"]:
        raise AdmissionError("execution permit is already consumed")
    if candidate.exists() or candidate.is_symlink():
        raise AdmissionError("execution output has already been consumed")
    ledger_path = record["identity_ledger_path"]
    checked = confined_path(source_root(ledger_path.parent), ledger_path.name, "identity ledger")
    if digest(checked.read_bytes()) != record["identity_ledger_sha256"]:
        raise AdmissionError("identity ledger changed after admission")
    reservation = record["identity_reservation"]
    fsync_directory_provisioning(reservation.parent)
    raw = canonical({"identity": IDENTITY, "execution_nonce": record["execution_nonce"],
                     "approval_sha256": record["approval_sha256"],
                     "freeze_sha256": record["verified"]["freeze_sha256"],
                     "output_directory": str(candidate), "state": "STARTED",
                     "filesystem_durability_boundary": FILESYSTEM_DURABILITY_BOUNDARY})
    budget.reserve_output(len(raw))
    def consumed() -> None:
        # O_EXCL has succeeded. Every later failure leaves this identity consumed.
        record["consumed"] = True
        record["budget"] = budget

    exclusive_durable_write(reservation, raw, on_created=consumed)
    return candidate


def verify_timeout_parent(expected_executable_sha256: str,
                          wall_seconds: int = 900) -> dict[str, Any]:
    """Inspect the actual Linux parent, not a user-supplied 'timeout enabled' flag."""
    if sys.platform != "linux":
        raise AdmissionError("external GNU timeout verification requires Linux /proc")
    parent = Path("/proc") / str(os.getppid())
    executable = (parent / "exe").resolve(strict=True)
    argv = (parent / "cmdline").read_bytes().split(b"\0")
    argv = [item.decode("utf-8", errors="strict") for item in argv if item]
    if (executable.name != "timeout" or not expected_executable_sha256
            or digest(executable.read_bytes()) != expected_executable_sha256):
        raise AdmissionError("actual parent is not the pinned GNU timeout binary")
    # Dedicated launch contract: hard kill at 900 seconds, not 900 plus kill grace.
    if len(argv) < 4 or argv[1:3] != ["--signal=KILL", f"{wall_seconds}s"]:
        raise AdmissionError("actual timeout parent lacks the exact hard wall ceiling")
    stat_fields = (parent / "stat").read_text().rsplit(")", 1)[1].split()
    started = int(stat_fields[19]) / os.sysconf("SC_CLK_TCK")
    return {"parent_pid": os.getppid(), "started_monotonic_seconds": started,
            "executable": str(executable), "argv": argv,
            "sha256": expected_executable_sha256,
            "limitation": "SIGKILL/OOM can prevent terminal manifest creation"}


def preflight_runtime_limits() -> dict[str, Any]:
    """Read inherited limits before identity consumption; never shrink the frozen envelope.

    Both soft and hard limits must already cover the frozen envelope before any
    one-shot identity or evidence write. This read-only check never raises limits.
    Cgroups/OOM remain a separate documented platform limitation.
    """
    import resource

    requirements = (("cpu_seconds", resource.RLIMIT_CPU, LIMITS["cpu_seconds"]),
                    ("address_space_bytes", resource.RLIMIT_AS, LIMITS["address_space_bytes"]),
                    ("output_bytes", resource.RLIMIT_FSIZE, LIMITS["output_bytes"]),
                    ("core_bytes", resource.RLIMIT_CORE, 0))
    observed = []
    for key, identifier, required in requirements:
        try:
            inherited = resource.getrlimit(identifier)
        except (OSError, TypeError, ValueError):
            raise AdmissionError(f"inherited resource limits are unavailable: {key}") from None
        if type(inherited) is not tuple or len(inherited) != 2:
            raise AdmissionError(f"unsupported inherited resource limit metadata: {key}")
        soft, hard = inherited
        if (type(soft) is not int or type(hard) is not int
                or any(value < 0 and value != resource.RLIM_INFINITY for value in inherited)):
            raise AdmissionError(f"unsupported inherited resource limit metadata: {key}")
        if hard != resource.RLIM_INFINITY and hard < required:
            raise AdmissionError(f"inherited hard limit cannot support frozen envelope: {key}")
        if soft != resource.RLIM_INFINITY and soft < required:
            raise AdmissionError(f"inherited soft limit cannot support frozen envelope: {key}")
        if hard != resource.RLIM_INFINITY and (soft == resource.RLIM_INFINITY or soft > hard):
            raise AdmissionError(f"inconsistent inherited resource limit metadata: {key}")
        observed.append({"resource": key, "resource_id": identifier,
                         "inherited_soft": soft, "inherited_hard": hard,
                         "required_soft": required, "required_hard": required})
    return {"schema": "g0-inherited-limit-preflight-v1", "resources": observed,
            "read_only": True, "frozen_envelope_preserved": True}


def install_runtime_limits(permit: ExecutionPermit, *,
                           budget: ResourceBudget | None = None) -> dict[str, Any]:
    """Only after separately authorized gate: verify timeout, enforce limits/offline IO."""
    require_execution_permit(permit, checkpoint=None if budget is None else budget.check)
    import resource

    admitted_limits = preflight_runtime_limits()
    timeout_sha = permit.freeze.get("timeout_executable_sha256", "")
    launch = verify_timeout_parent(timeout_sha, LIMITS["wall_seconds"])
    if not sys.dont_write_bytecode or not sys.flags.no_user_site:
        raise AdmissionError("execution requires -B and -s for fresh pinned imports")
    for row in admitted_limits["resources"]:
        resource.setrlimit(row["resource_id"], (row["required_soft"], row["required_hard"]))
    launch["inherited_limits"] = admitted_limits

    def offline(event: str, args: tuple) -> None:
        if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.exec",
                                                    "os.posix_spawn", "pty.spawn"}:
            raise BudgetExceeded("offline dedicated runner forbids network and child processes")

    sys.addaudithook(offline)
    return launch


class ResourceBudget:
    """One fixed envelope, with terminal reserves included, never added to the caps."""

    def __init__(self, limits: Mapping[str, int] | None = None,
                 reserves: Mapping[str, int] | None = None, *,
                 sampler: Callable[[], Mapping[str, float]] | None = None) -> None:
        self.limits = dict(LIMITS if limits is None else limits)
        self.reserves = dict(RESERVES if reserves is None else reserves)
        if set(self.limits) != set(LIMITS) or set(self.reserves) != set(RESERVES):
            raise AdmissionError("unsupported budget keys")
        for key, cap in self.limits.items():
            reserve = self.reserves[key]
            if (type(cap) is not int or type(reserve) is not int
                    or cap <= 0 or not 0 <= reserve < cap or cap > LIMITS[key]):
                raise AdmissionError("invalid or expanded resource envelope")
        self._wall_start = time.monotonic()
        if sampler is None:
            if sys.platform != "linux":
                raise AdmissionError("actual budget accounting requires Linux /proc")
            # Include interpreter startup, source/environment admission and imports.
            fields = Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()
            self._wall_start = int(fields[19]) / os.sysconf("SC_CLK_TCK")
        self._sampler = sampler
        self.output_bytes = 0
        self.finalizing = False
        self.failure: str | None = None

    def bind_timeout_parent(self, launch: dict[str, Any]) -> None:
        """Align the reserve clock with the independently inspected actual timeout parent."""
        started = launch.get("started_monotonic_seconds")
        if type(started) not in (int, float) or not math.isfinite(started):
            raise AdmissionError("verified timeout launch timestamp is missing")
        if started < 0 or started > time.monotonic():
            raise AdmissionError("invalid timeout launch timestamp")
        self._wall_start = min(self._wall_start, started)
        self.check()

    def sample(self) -> dict[str, Any]:
        if self._sampler is not None:
            result = dict(self._sampler())
        else:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            pages = int(Path("/proc/self/statm").read_text().split()[0])
            memory = pages * os.sysconf("SC_PAGE_SIZE")
            result = {"cpu_seconds": usage.ru_utime + usage.ru_stime,
                      "wall_seconds": time.monotonic() - self._wall_start,
                      "address_space_bytes": memory}
        result["output_bytes"] = self.output_bytes
        return primitive(result)

    def poison(self, reason: str) -> None:
        self.failure = str(reason)
        raise BudgetExceeded(self.failure)

    def check(self) -> dict[str, Any]:
        if self.failure and not self.finalizing:
            raise BudgetExceeded(self.failure)
        sample = self.sample()
        for key, maximum in self.limits.items():
            cap = maximum if self.finalizing else maximum - self.reserves[key]
            if sample[key] >= cap:
                self.poison(f"resource cap reached before next dynamics: {key}")
        return sample

    def reserve_output(self, size: int) -> None:
        if type(size) is not int or size < 0:
            raise AdmissionError("invalid output byte charge")
        self.check()
        cap = self.limits["output_bytes"]
        if not self.finalizing:
            cap -= self.reserves["output_bytes"]
        if self.output_bytes + size > cap:
            self.poison("output cap reached before write")
        # Conservatively charge the whole attempted write even when IO fails halfway.
        self.output_bytes += size

    def finish(self) -> dict[str, Any]:
        self.finalizing = True
        return self.check()


class ExclusiveEvidenceWriter:
    """No reuse, no overwrite, raw evidence first, partial terminal verdict last."""

    def __init__(self, output_dir: Path, identity: str, budget: ResourceBudget) -> None:
        if identity != IDENTITY:
            raise AdmissionError("only the fresh prospective G0 identity is supported")
        output_dir = Path(output_dir)
        parent = source_root(output_dir.parent)
        if output_dir.name in {"", ".", ".."}:
            raise AdmissionError("invalid output directory")
        self.path = parent / output_dir.name
        budget.check()
        fsync_directory_provisioning(parent)
        self.path.mkdir(mode=0o700, exist_ok=False)
        fsync_directory(parent)  # The new output-directory name must be durable.
        fsync_directory(self.path)
        self.budget = budget
        self.records: list[dict[str, Any]] = []
        self.write_attempts: list[dict[str, Any]] = []
        self.closed = False
        self._lock = threading.RLock()
        self._write("STARTED.json", canonical({"identity": identity, "state": "STARTED",
                    "real_g0_completed": False, "scientific_credit": 0,
                    "filesystem_durability_boundary": FILESYSTEM_DURABILITY_BOUNDARY}), "start")

    def _write(self, name: str, data: bytes, kind: str) -> dict[str, Any]:
        if (type(name) is not str or Path(name).name != name or name in {"", ".", ".."}
                or type(data) is not bytes):
            raise AdmissionError("evidence must use a confined leaf name and exact bytes")
        with self._lock:
            if self.closed:
                raise AdmissionError("terminal evidence is already closed")
            self.budget.reserve_output(len(data))
            path = self.path / name
            attempt = {"name": name, "kind": kind, "planned_bytes": len(data),
                       "complete": False}
            self.write_attempts.append(attempt)
            exclusive_durable_write(path, data)
            record = {"name": name, "kind": kind, "bytes": len(data), "sha256": digest(data)}
            # Include durable IO/hash work before acknowledging this record. During
            # terminal finalization this checks the same fixed hard envelope.
            self.budget.check()
            self.records.append(record)
            attempt["complete"] = True
            return primitive(record)

    def raw_json(self, name: str, value: Any) -> dict[str, Any]:
        return self._write(name, canonical(value), "raw_json")

    def raw_bytes(self, name: str, data: bytes) -> dict[str, Any]:
        return self._write(name, data, "raw_bytes")

    def verdict(self, name: str, value: Any, *, raw_names: list[str]) -> dict[str, Any]:
        available = {item["name"] for item in self.records if item["kind"].startswith("raw_")}
        if not raw_names or not set(raw_names) <= available:
            raise AdmissionError("verdict requires already durable raw evidence")
        return self._write(name, canonical({"raw_names": raw_names, "verdict": value}), "verdict")

    def terminal(self, status: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
        self.budget.finish()
        result = self._write("TERMINAL.json", canonical({
            "identity": IDENTITY, "status": status, "details": details or {},
            "records": primitive(self.records), "write_attempts": primitive(self.write_attempts),
            "resources_before_terminal": self.budget.sample(),
            "partial_evidence_retained": status != "SUCCESS", "scientific_credit": 0,
            "filesystem_durability_boundary": FILESYSTEM_DURABILITY_BOUNDARY,
            "terminal_acknowledgment": (
                "Complete-looking bytes alone are not a successful terminal acknowledgment; "
                "writer completion and successful launcher status are both required."),
            "limitation": ("SIGKILL, OOM, disk failure or exhausted hard caps "
                           "can prevent finalization"),
        }), "terminal")
        self.closed = True
        return result


def _ast_function_keys(path: Path, relative: str) -> set[tuple[str, str]]:
    result = set()

    def walk(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                result.add((relative, name))
                if not isinstance(child, ast.ClassDef):
                    walk(child, name + ".<locals>.")
                else:
                    walk(child, name + ".")
            else:
                walk(child, prefix)

    walk(ast.parse(path.read_bytes()), "")
    return result


class PassiveCallMonitor:
    """Before-body profile counters on this thread and subsequently created owners.

    No model method is replaced. Scalar records and a bounded code-key cache are retained.
    A failed profile poisons the budget. The runner must check at every owner dispatch,
    including after an expected exception; Python disables a callback that raises.
    Finite admission checks plus hard OS limits do not promise zero-gap real-time enforcement.
    """

    def __init__(self, root: Path, call_plan: Mapping[str, int] | None, budget: ResourceBudget,
                 writer: ExclusiveEvidenceWriter | None = None, *,
                 targets: Mapping[str, tuple[str, str]] | None = None,
                 allowed_functions: set[tuple[str, str]] | None = None) -> None:
        self.root = source_root(root)
        self.caps = dict(CALL_CAPS if call_plan is None else call_plan)
        if any(type(v) is not int or v < 0 for v in self.caps.values()):
            raise AdmissionError("invalid passive call cap")
        self.targets = dict(CALL_TARGETS if targets is None else targets)
        if not set(self.targets) <= self.caps.keys():
            raise AdmissionError("uncapped model call target")
        self.lookup = {tuple(value): key for key, value in self.targets.items()}
        if len(self.lookup) != len(self.targets):
            raise AdmissionError("duplicate passive target")
        self.counts = dict.fromkeys(self.caps, 0)
        self.budget, self.writer = budget, writer
        # CodeType equality/hash are structural. Keep an identity witness so equal
        # but distinct code and recycled ids never share a classification entry.
        # Trusted source code objects do not retain frames or function globals;
        # retention is finite and released at exit. Arbitrarily injected process
        # code is outside this source-bound observer's contract.
        # A cache hit never bypasses per-event policy.
        self._code_keys: dict[int, tuple[types.CodeType, tuple[str, str]]] = {}
        self._events_until_check = PROFILE_CHECK_INTERVAL
        self._active = False
        self._thread_ids: set[int] = set()
        self._capture = 0
        self.events: list[dict[str, Any]] = []
        self.births: list[dict[str, Any]] = []
        self._weak_resources: dict[int, weakref.ReferenceType] = {}
        self.returned = dict.fromkeys(self.caps, 0)
        self.ancillary_rngs = 0
        self._pending_calls: dict[tuple[int, int], dict[str, Any]] = {}
        self._pending_shells: dict[tuple[int, int], dict[str, Any]] = {}
        self._allocation_keys = {
            ("scripts/g0_joint_ownership.py", "_construct"),
            ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes"),
            ("src/sparkbrain/v032/runtime.py", "<module>"),
        }
        self._allocation_files = {str(self.root / key[0]) for key in self._allocation_keys}
        self._lock = threading.RLock()
        self.allowed_functions = allowed_functions
        if allowed_functions is None:
            self.allowed_functions = set()
            contract_path = self.root / CONTRACT
            runtime_paths = []
            if contract_path.exists() or contract_path.is_symlink():
                contract = read_json(confined_path(self.root, CONTRACT, "profile contract"))
                runtime_paths = list(contract["runtime_sources_sha256"])
            elif (self.root / "src/sparkbrain").exists():
                # Explicit source-only stand-in roots may omit the production contract.
                pending = [confined_path(self.root, "src/sparkbrain", "synthetic runtime",
                                         directory=True)]
                while pending:
                    for path in pending.pop().iterdir():
                        self.budget.check()
                        info = path_metadata(path, "synthetic profile dependency")
                        if stat.S_ISDIR(info.st_mode):
                            pending.append(path)
                        elif path.suffix == ".py":
                            runtime_paths.append(path.relative_to(self.root).as_posix())
            selected = runtime_paths + ["scripts/g0_joint_ownership.py",
                                        "scripts/run_g0_joint_eligibility.py",
                                        "scripts/g0_execution_support.py"]
            for relative in selected:
                self.budget.check()
                path = self.root / relative
                if path.exists() or path.is_symlink():
                    checked = confined_path(self.root, relative, "profile source")
                    self.allowed_functions.update(_ast_function_keys(checked, relative))

    def before(self, name: str) -> None:
        with self._lock:
            self.budget.check()
            if name not in self.caps:
                self.budget.poison(f"unknown model call or resource birth: {name}")
            if self.counts[name] >= self.caps[name]:
                self.budget.poison(f"call cap reached before body: {name}")
            self.counts[name] += 1
            self._thread_ids.add(threading.get_ident())
            self._event("call_attempt", name, attempt=self.counts[name])
            # Durable logging can consume the soft reserve before this body starts.
            self.budget.check()

    def _event(self, kind: str, name: str, **details: Any) -> None:
        value = primitive({"sequence": len(self.events) + 1, "kind": kind, "name": name,
                           "thread": threading.get_ident(), **details})
        if self.writer is not None:
            self.writer.raw_json(f"passive-event-{value['sequence']:06d}.json", value)
        self.events.append(value)

    def _record_birth(self, name: str, value: Any, key: tuple[str, str]) -> None:
        cls = type(value)
        record = {"birth_id": len(self.births) + 1, "name": name,
                  "runtime_id": id(value), "type": cls.__module__ + "." + cls.__qualname__,
                  "source_route": list(key), "thread": threading.get_ident()}
        previous = self._weak_resources.get(id(value))
        if previous is not None and previous() is not None:
            self.budget.poison("resource constructor reused a still-live identity")
        try:
            self._weak_resources[id(value)] = weakref.ref(value)
        except TypeError:
            self.budget.poison("resource birth does not support required weak observation")
        self._event("resource_birth", name, **{key: val for key, val in record.items()
                                              if key != "name"})
        self.births.append(record)

    def _called(self, frame: Any, name: str, *, birth: bool = False) -> None:
        self.before(name)
        token = (threading.get_ident(), id(frame))
        self._pending_calls[token] = {"name": name, "birth": birth,
                                      "source_route": list(self._key(frame))}

    def check(self) -> dict[str, Any]:
        return self.budget.check()

    def snapshot(self) -> dict[str, Any]:
        self._weak_resources = {key: ref for key, ref in self._weak_resources.items()
                                if ref() is not None}
        result = {"counts": dict(self.counts), "caps": dict(self.caps),
                "threads_seen": sorted(self._thread_ids), "counts_before_body": True,
                "failure": self.budget.failure, "returned": dict(self.returned),
                "births": primitive(self.births), "events": primitive(self.events),
                "ancillary_rngs": self.ancillary_rngs,
                "live_resource_ids": sorted(self._weak_resources),
                "pending_calls": primitive(list(self._pending_calls.values())),
                "pending_shells": primitive(list(self._pending_shells.values()))}
        if self.caps.keys() == CALL_CAPS.keys():
            result["protocol_counts"] = protocol_call_caps(self.counts)
        return result

    def _key(self, frame: Any) -> tuple[str, str]:
        code = frame.f_code
        identity = id(code)
        cached = self._code_keys.get(identity)
        if cached is not None:
            if cached[0] is not code:
                self.budget.poison("passive code identity changed while retained")
            return cached[1]
        if len(self._code_keys) >= CODE_KEY_CACHE_LIMIT:
            self.budget.poison("passive code-key cache capacity reached")
        try:
            relative = Path(code.co_filename).relative_to(self.root).as_posix()
        except ValueError:
            relative = ""
        key = relative, code.co_qualname
        self._code_keys[identity] = (code, key)
        return key

    def _profile(self, frame: Any, event: str, arg: Any) -> None:
        try:
            self._events_until_check -= 1
            if self._events_until_check <= 0:
                self._events_until_check = PROFILE_CHECK_INTERVAL
                # Finite, output-independent sampling. Profiling callbacks are
                # nonrecursive; sampling itself writes no observer evidence.
                self.budget.check()
            output_before = self.budget.output_bytes
            self._profile_inner(frame, event, arg)
            # Only instrumentation that charged output needs a post-log sample.
            # No-output events only use the finite periodic checkpoint above.
            if self.budget.output_bytes != output_before:
                self.budget.check()
        except BudgetExceeded as exc:
            self.budget.failure = self.budget.failure or str(exc)
            self._detach_hooks()
            raise
        except BaseException as exc:
            self.budget.failure = (self.budget.failure
                                   or "passive instrumentation failed: " + type(exc).__name__)
            self._detach_hooks()
            raise BudgetExceeded(self.budget.failure) from None

    def _profile_inner(self, frame: Any, event: str, arg: Any) -> None:
        key = self._key(frame)
        name = self.lookup.get(key)
        if event == "call":
            if key[0].startswith("src/sparkbrain/"):
                # Comprehensions/lambdas inherit an already admitted source function.
                if key not in self.allowed_functions and frame.f_code.co_name not in {
                        "<module>", "<listcomp>", "<dictcomp>", "<setcomp>",
                        "<genexpr>", "<lambda>"}:
                    self.budget.poison("unknown runtime call route: " + ":".join(key))
            if name is not None:
                self._called(frame, name, birth=name in {
                    "v03_init", "v05_init", "facade_init", "m1_init", "predictive_init",
                    "scope_init", "scope_router_init"})
            if name == "direct_checkpoint_load_bytes" and self.writer is not None:
                raw = frame.f_locals.get("raw")
                if type(raw) is not bytes:
                    self.budget.poison("native load input must be exact raw bytes")
                self.writer.raw_bytes(
                    f"native-load-input-{self.counts[name]:04d}.json", raw)
            if key == ("src/sparkbrain/v032/checkpoint.py", "_publish_noreplace"):
                raw = frame.f_locals.get("payload")
                if type(raw) is not bytes:
                    self.budget.poison("unsupported native checkpoint byte payload")
                self.budget.reserve_output(len(raw))
            if (frame.f_globals.get("__name__") == "pathlib"
                    and frame.f_code.co_name == "open" and frame.f_back is not None
                    and self._key(frame.f_back) == CALL_TARGETS["pilot_checkpoint_save"]):
                raw = frame.f_back.f_locals.get("pilot_raw")
                if type(raw) is not bytes:
                    self.budget.poison("unsupported native pilot checkpoint byte payload")
                self.budget.reserve_output(len(raw))
            if frame.f_code.co_name == "__init__" and frame.f_globals.get("__name__") == "random":
                parent = self._key(frame.f_back) if frame.f_back else ("", "")
                if parent in {
                    ("src/sparkbrain/v03/runtime.py", "IntegratedV03Brain._initialize_runtime"),
                    ("src/sparkbrain/v032/checkpoint.py", "_decode"),
                    ("scripts/g0_joint_ownership.py", "_construct"),
                }:
                    self._called(frame, "model_rng", birth=True)
                elif parent == ("src/sparkbrain/v05/topology.py", "layered_reservoir_topology"):
                    self._called(frame, "topology_rng", birth=True)
                elif parent[0].startswith("src/sparkbrain/"):
                    self.budget.poison("unknown model RNG birth route")
                else:
                    self.ancillary_rngs += 1
                    self._event("ancillary_rng", "stdlib_rng", source_route=list(parent))
                # tempfile/stdlib RNGs are ancillary, never silently model-owned.
            if frame.f_code.co_name == "RLock" and frame.f_globals.get("__name__") == "threading":
                parent = self._key(frame.f_back) if frame.f_back else ("", "")
                if parent == ("src/sparkbrain/v032/runtime.py", "_shared_step_lock"):
                    self._called(frame, "model_lock", birth=True)
                elif parent[0].startswith("src/sparkbrain/"):
                    self.budget.poison("unknown model synchronization birth route")
        elif event == "c_call" and getattr(arg, "__name__", "") == "allocate_lock":
            if key == ("src/sparkbrain/v032/runtime.py", "<module>"):
                self.before("registry_guard")
                self._pending_shells[(threading.get_ident(), id(frame))] = {
                    "name": "registry_guard", "local": "_LOCK_REGISTRY_GUARD",
                    "source_route": list(key), "returned": False}
            elif key[0].startswith("src/sparkbrain/"):
                self.budget.poison("unknown model lock allocation route")
        elif event == "c_call" and getattr(arg, "__name__", "") == "__new__":
            if key == ("scripts/g0_joint_ownership.py", "_construct"):
                cls = frame.f_locals.get("cls")
            elif key == ("src/sparkbrain/v032/checkpoint.py",
                          "DirectCheckpointManager._load_bytes"):
                cls = frame.f_locals.get("brain_class")
            else:
                cls = None
            if (type(cls) is type and cls.__module__ == "sparkbrain.v03.runtime"
                    and cls.__name__ == "IntegratedV03Brain"):
                self.before("rawbrain_shell")
                self._pending_shells[(threading.get_ident(), id(frame))] = {
                    "name": "rawbrain_shell", "local": "clone" if key[0].startswith("scripts/")
                    else "brain", "source_route": list(key), "returned": False}
            elif (type(cls) is type and cls.__module__ == "sparkbrain.v05.brain"
                  and cls.__name__ == "IntegratedV05Brain"):
                self.before("v05_shell")
                self._pending_shells[(threading.get_ident(), id(frame))] = {
                    "name": "v05_shell", "local": "clone", "source_route": list(key),
                    "returned": False}
            elif (key[0].startswith("src/sparkbrain/") and key not in {
                    ("src/sparkbrain/v032/checkpoint.py", "_decode"),
                    ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes")}):
                self.budget.poison("unknown model shell allocation route")
            # Do not retain cls/frame/arg after this callback.
        elif (event in {"c_return", "c_exception"}
              and getattr(arg, "__name__", "") in {"__new__", "allocate_lock"}):
            token = (threading.get_ident(), id(frame))
            pending = self._pending_shells.get(token)
            if pending:
                if event == "c_exception":
                    self._event("call_exception", pending["name"])
                    del self._pending_shells[token]
                else:
                    pending["returned"] = True
        elif event == "return":
            token = (threading.get_ident(), id(frame))
            pending = self._pending_calls.pop(token, None)
            if pending is not None:
                opcode = frame.f_code.co_code[frame.f_lasti]
                normal = dis.opname[opcode].startswith("RETURN_")
                counter = pending["name"]
                if normal:
                    self.returned[counter] += 1
                    self._event("call_return", counter, source_route=pending["source_route"])
                    if pending["birth"]:
                        value = arg if counter == "model_lock" else frame.f_locals.get("self")
                        if value is None:
                            self.budget.poison("missing successful resource return")
                        self._record_birth(counter, value, tuple(pending["source_route"]))
                else:
                    self._event("call_exception", counter, source_route=pending["source_route"])
                if normal and self.writer is not None:
                    if name == "direct_checkpoint_save":
                        self._capture_file(Path(frame.f_locals["path"]))
                    elif name == "pilot_checkpoint_save":
                        directory = source_root(Path(frame.f_locals["directory"]))
                        for item in sorted(directory.iterdir()):
                            info = path_metadata(item, "native checkpoint")
                            if not stat.S_ISREG(info.st_mode):
                                self.budget.poison("unsupported native checkpoint output")
                            self._capture_file(item)

    def _trace(self, frame: Any, event: str, arg: Any) -> Any:
        # Only exact reviewed allocation callers receive line tracing. C profile
        # c_return reports the allocator, not its result. At the next line the
        # ordinary STORE_FAST has completed; inspect only that source-declared local.
        if frame.f_code.co_filename not in self._allocation_files:
            return None
        try:
            if self._key(frame) not in self._allocation_keys:
                return None
            output_before = self.budget.output_bytes
            token = (threading.get_ident(), id(frame))
            pending = self._pending_shells.get(token)
            if pending and pending["returned"] and event in {"line", "return"}:
                value = frame.f_locals.get(pending["local"])
                if value is None:
                    self.budget.poison("successful shell allocation has no assigned local")
                self.returned[pending["name"]] += 1
                self._event("call_return", pending["name"],
                            source_route=pending["source_route"])
                self._record_birth(pending["name"], value, tuple(pending["source_route"]))
                del self._pending_shells[token]
            if self.budget.output_bytes != output_before:
                self.budget.check()
        except BudgetExceeded as exc:
            self.budget.failure = self.budget.failure or str(exc)
            self._detach_hooks()
            raise
        except BaseException as exc:
            self.budget.failure = (
                self.budget.failure
                or "passive allocation observation failed: " + type(exc).__name__)
            self._detach_hooks()
            raise BudgetExceeded(self.budget.failure) from None
        return self._trace

    def _capture_file(self, path: Path) -> None:
        parent = source_root(path.parent)
        checked = confined_path(parent, path.name, "native checkpoint")
        size = checked.stat().st_size
        cap = self.budget.limits["output_bytes"] - self.budget.reserves["output_bytes"]
        if size > cap - self.budget.output_bytes:
            self.budget.poison("native checkpoint exceeds remaining evidence envelope")
        self._capture += 1
        name = f"native-checkpoint-{self._capture:04d}-{path.name}"
        self.writer.raw_bytes(name, checked.read_bytes())

    def __enter__(self) -> PassiveCallMonitor:
        if "registry_guard" in self.caps:
            require_passive_lock_api()
        if (self._active or sys.getprofile() is not None or threading.getprofile() is not None
                or sys.gettrace() is not None or threading.gettrace() is not None):
            raise AdmissionError("existing profiling hooks are outside the dedicated-runner scope")
        self._active = True
        threading.settrace(self._trace)
        sys.settrace(self._trace)
        threading.setprofile(self._profile)
        sys.setprofile(self._profile)
        return self

    def _detach_hooks(self) -> None:
        # A callback can fail on the call event entering __exit__, before its
        # body runs. Detach here as well as on ordinary context exit. Other
        # already-running owners still obey the sticky dispatch budget checks.
        sys.setprofile(None)
        threading.setprofile(None)
        sys.settrace(None)
        threading.settrace(None)
        self._active = False
        self._code_keys.clear()

    def __exit__(self, *_: Any) -> None:
        self._detach_hooks()
