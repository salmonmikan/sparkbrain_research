"""Read-only prospective admission for the repaired M1 path, never execution authority.

There is deliberately no approved execution freeze. A flag, synthetic test, source
contract or this validator cannot grant clearance. In particular, the constructor
census and launcher/finalization implementation still need separately reviewed,
observed evidence. File binding assumes a trusted, non-mutating source tree; it is
not attestation of arbitrary monkey-patching of a running Python process.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
import os
import platform
import stat
import sys
import sysconfig
import threading
import types
import weakref
from collections.abc import Callable
from pathlib import Path
from typing import Any

from scripts.verify_g0_joint_source_contract import confined_path, path_metadata, source_root
from scripts.verify_m1_path_source import CONTRACT, verify

IDENTITY = "assembly-m1-path-v1-20261002"
SOURCE_COMMIT = "46bbd9b8b28c2404c73f028f8736ed83c3b5c3fe"
ARTIFACT_ROOT = "artifacts/research/assembly_m1_path_v1_20261002"
APPROVED_FREEZE_SHA256: str | None = None
RESOURCE_KEYS = {"cpu_seconds", "wall_seconds", "address_space_bytes", "output_bytes"}
# These are proposed source-route totals, NOT observed census results or budgets.
PROSPECTIVE_SUCCESS_COUNTS = {
    "facade_init": 58,
    "rawbrain_shell": 56,
    "producer_shell": 9,
    "predictive_init": 12,
    "scope_init": 2,
    "router_init": 2,
}
PROSPECTIVE_ROLLBACK_ADDITIONS = {
    "terminal_rollbacks": 2,
    "predictive_load": 2,
    "facade_init": 2,
    "rawbrain_shell": 2,
    "model_rng": 2,
    "scope_init": 4,
    "router_init": 8,
}
FREEZE_KEYS = {
    "schema",
    "identity",
    "source_commit",
    "runtime_execution_authorized",
    "source_contract",
    "source_files_sha256",
    "inputs",
    "teaching",
    "configuration",
    "environment",
    "gates",
    "limits",
    "finalization_reserves",
    "launcher",
    "ownership",
    "one_shot",
}
GATE_NAMES = {
    "g0",
    "source_delta_reconciliation",
    "three_observation_eligibility",
    "constructor_census",
}
ENVIRONMENT_KEYS = {
    "schema",
    "implementation",
    "version",
    "executable",
    "executable_sha256",
    "prefix",
    "base_prefix",
    "platform",
    "machine",
    "cache_tag",
    "flags",
    "sys_path",
    "environment_sha256",
    "dependency_roots",
    "dependency_inventory_sha256",
    "dependency_files",
    "native_code_sha256",
    "mapped_code_sha256",
    "external_import_archives",
    "venv_configuration_sha256",
}


class AdmissionError(ValueError):
    """A missing or mismatched admission requirement; no retry or fallback implied."""


def primitive(value: Any) -> Any:
    """Detach only exact, finite JSON values; never execute conversion hooks."""
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if type(value) in (tuple, list):
        return [primitive(item) for item in value]
    if type(value) is dict and all(type(key) is str for key in value):
        return {key: primitive(item) for key, item in value.items()}
    raise AdmissionError("only exact finite JSON primitives are supported")


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            primitive(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AdmissionError(message)


def _keys(value: Any, expected: set[str], label: str) -> dict:
    _require(type(value) is dict and set(value) == expected, label + " fields differ")
    return value


def _sha(value: Any, label: str) -> str:
    _require(
        type(value) is str
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        label + " missing SHA-256",
    )
    return value


def _pairs(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def parse_json(raw: bytes) -> Any:
    try:
        return primitive(json.loads(raw, object_pairs_hook=_pairs))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise AdmissionError("invalid UTF-8 JSON") from exc


def _relative(value: Any, label: str) -> str:
    _require(type(value) is str and bool(value), label + " missing path")
    path = Path(value)
    _require(
        not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == value
        and value != ".",
        label + " noncanonical path",
    )
    return value


def _hash_map(value: Any, label: str) -> dict:
    _require(type(value) is dict and bool(value), label + " missing inventory")
    for name, sha in value.items():
        _relative(name, label)
        _sha(sha, label)
    return value


def _binding(value: Any, label: str) -> dict:
    _keys(value, {"path", "sha256"}, label)
    _relative(value["path"], label)
    _sha(value["sha256"], label)
    return value


def _read_binding(root: Path, value: Any, label: str) -> bytes:
    binding = _binding(value, label)
    raw = confined_path(root, binding["path"], label).read_bytes()
    _require(digest(raw) == binding["sha256"], label + " bytes differ")
    return raw


def _evidence_files(root: Path, values: Any, label: str) -> None:
    _require(type(values) is list and bool(values), label + " has no raw evidence")
    names = []
    for value in values:
        _read_binding(root, value, label)
        names.append(value["path"])
    _require(len(names) == len(set(names)), label + " duplicates evidence")


def validate_freeze_schema(freeze: Any) -> dict:
    """Pure schema validation, with no defaults, authority or eligibility inference."""
    freeze = primitive(freeze)
    _keys(freeze, FREEZE_KEYS, "execution freeze")
    _require(
        freeze["schema"] == "m1-path-execution-freeze-v1"
        and freeze["identity"] == IDENTITY
        and freeze["source_commit"] == SOURCE_COMMIT
        and freeze["runtime_execution_authorized"] is False,
        "freeze identity/source-only boundary differs",
    )
    _hash_map(freeze["source_files_sha256"], "complete source")
    for name, path in (("source_contract", CONTRACT), ("inputs", ARTIFACT_ROOT + "/inputs.jsonl")):
        _binding(freeze[name], name)
        _require(freeze[name]["path"] == path, name + " canonical path differs")
    teaching = _keys(freeze["teaching"], {"evaluator", "subset_sha256"}, "teaching")
    _binding(teaching["evaluator"], "evaluator")
    _require(
        teaching["evaluator"]["path"] == ARTIFACT_ROOT + "/evaluator.json",
        "evaluator canonical path differs",
    )
    _sha(teaching["subset_sha256"], "truth-minimized teaching subset")
    _keys(freeze["gates"], GATE_NAMES, "required gates")
    for name, binding in freeze["gates"].items():
        _binding(binding, name)
    _require(
        type(freeze["configuration"]) is dict and bool(freeze["configuration"]),
        "source configuration missing",
    )
    environment = _keys(freeze["environment"], ENVIRONMENT_KEYS, "full execution environment")
    _require(
        environment["schema"] == "m1-path-python-environment-v1"
        and environment["implementation"] == "CPython"
        and environment["platform"] == "linux",
        "unsupported interpreter/native environment",
    )
    for key in ("executable_sha256", "environment_sha256", "dependency_inventory_sha256"):
        _sha(environment[key], key)
    _require(
        type(environment["dependency_files"]) is int and environment["dependency_files"] > 0,
        "missing complete dependency inventory",
    )
    for key in ("version", "machine", "cache_tag"):
        _require(
            type(environment[key]) is str and bool(environment[key]), "missing environment " + key
        )
    for key in ("executable", "prefix", "base_prefix"):
        _require(
            type(environment[key]) is str and Path(environment[key]).is_absolute(),
            "environment path must be absolute: " + key,
        )
    for key in ("dependency_roots", "sys_path"):
        _require(
            type(environment[key]) is list
            and bool(environment[key])
            and all(type(path) is str and Path(path).is_absolute() for path in environment[key]),
            "invalid environment paths: " + key,
        )
    flags = environment["flags"]
    _require(
        type(flags) is dict
        and flags.get("dont_write_bytecode") == 1
        and flags.get("no_user_site") == 1
        and all(type(value) is int for value in flags.values()),
        "dedicated interpreter must use -B and -s",
    )
    for key in ("native_code_sha256", "mapped_code_sha256", "external_import_archives"):
        _require(type(environment[key]) is dict, "invalid environment inventory: " + key)
        for path, sha in environment[key].items():
            _require(type(path) is str and Path(path).is_absolute(), "nonabsolute dependency path")
            if key != "external_import_archives" or sha is not None:
                _sha(sha, key)
    _require(bool(environment["mapped_code_sha256"]), "no native mapping inventory")
    if environment["venv_configuration_sha256"] is not None:
        _sha(environment["venv_configuration_sha256"], "venv configuration")
    limits = _keys(freeze["limits"], RESOURCE_KEYS, "fixed limits")
    reserves = _keys(freeze["finalization_reserves"], RESOURCE_KEYS, "finalization reserves")
    for key, cap in limits.items():
        reserve = reserves[key]
        _require(
            type(cap) is int and type(reserve) is int and 0 < reserve < cap,
            "missing exact positive limit/reserve: " + key,
        )
    launcher = _keys(
        freeze["launcher"],
        {
            "implementation",
            "authority_verifier",
            "runtime_verifier",
            "hard_wall_executable",
            "hard_wall_sha256",
            "offline",
            "fresh_process",
            "no_bytecode",
            "no_user_site",
            "sanitize_environment",
            "raw_before_verdict",
            "exclusive_output",
            "partial_evidence_retained",
            "no_retry",
        },
        "launcher",
    )
    _binding(launcher["implementation"], "launcher implementation")
    _sha(launcher["hard_wall_sha256"], "hard wall executable")
    _require(
        type(launcher["hard_wall_executable"]) is str
        and Path(launcher["hard_wall_executable"]).is_absolute(),
        "hard wall executable requires an absolute path",
    )
    for key in ("authority_verifier", "runtime_verifier"):
        _require(
            type(launcher[key]) is str and launcher[key].isidentifier(),
            "launcher verifier must be a source-bound module-level function",
        )
    for key in set(launcher) - {
        "implementation",
        "authority_verifier",
        "runtime_verifier",
        "hard_wall_executable",
        "hard_wall_sha256",
    }:
        _require(launcher[key] is True, "missing launcher obligation: " + key)
    _require(
        canonical(freeze["ownership"])
        == canonical(
            {
                "dedicated_serial_owner": True,
                "owner_thread_cleanup": True,
                "reverse_allocation_cleanup": True,
                "zero_live_resources_at_success": True,
                "no_model_references_escape": True,
            }
        ),
        "owner-thread cleanup contract differs",
    )
    _require(
        canonical(freeze["one_shot"])
        == canonical(
            {
                "identity": IDENTITY,
                "durable_exclusive_reservation": True,
                "reserve_before_native_import": True,
                "failure_consumes_identity": True,
            }
        ),
        "one-shot contract differs",
    )
    return freeze


def _tree_inventory(directory: Path) -> dict[str, str]:
    """Inspect only explicitly selected interpreter roots, never a home-tree search."""
    root = source_root(directory)
    pending, result = [root], {}
    while pending:
        for child in sorted(pending.pop().iterdir()):
            info = path_metadata(child, "interpreter dependency")
            if stat.S_ISDIR(info.st_mode):
                if child.parent == root and child.name in {"site-packages", "dist-packages"}:
                    continue
                pending.append(child)
            elif child.suffix in {
                ".py",
                ".pyc",
                ".pyo",
                ".so",
                ".pyd",
                ".dll",
                ".dylib",
                ".pth",
                ".egg-link",
                ".zip",
            } or child.parent.name.endswith((".dist-info", ".egg-info")):
                result[child.relative_to(root).as_posix()] = digest(child.read_bytes())
    return result


def mapped_code_snapshot() -> dict[str, str]:
    """Read only actual executable file mappings; no memory or unrelated documents."""
    _require(sys.platform == "linux", "native library admission requires Linux /proc")
    result = {}
    for line in Path("/proc/self/maps").read_text().splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) != 6 or "x" not in fields[1] or not fields[5].startswith("/"):
            continue
        name = fields[5]
        _require(not name.endswith(" (deleted)"), "deleted native executable mapping")
        path = Path(name)
        raw = confined_path(source_root(path.parent), path.name, "mapped library").read_bytes()
        _require(raw.startswith(b"\x7fELF"), "unreviewed executable mapping kind")
        result[name] = digest(raw)
    _require(bool(result), "native executable mappings unavailable")
    return result


def environment_snapshot(root: Path) -> dict:
    """Explicit interpreter/stdlib/package/code inventory; never import runtime code.

    This can be expensive. It is opt-in read-only preparation, never called by
    module import. Unknown import roots fail instead of scanning private trees.
    """
    root = source_root(root)
    _require(
        platform.python_implementation() == "CPython" and sys.version_info >= (3, 11),
        "reviewed CPython 3.11+ required",
    )
    executable = Path(sys.executable).resolve(strict=True)
    executable = confined_path(source_root(executable.parent), executable.name, "interpreter")
    roots = sorted(
        {
            str(source_root(Path(sysconfig.get_path(key))))
            for key in ("stdlib", "platstdlib", "purelib", "platlib")
        }
    )
    source_paths = {root, root / "src", root / "scripts"}
    imports, archives = [], {}
    for entry in sys.path:
        path = Path(entry or Path.cwd()).absolute()
        _require(".." not in path.parts, "noncanonical import search path")
        imports.append(str(path))
        if path in source_paths or any(
            path == Path(item) or path.is_relative_to(Path(item)) for item in roots
        ):
            if path.exists():
                path_metadata(path, "import root")
            continue
        expected_zip = Path(sysconfig.get_path("stdlib")).parent / (
            f"python{sys.version_info.major}{sys.version_info.minor}.zip"
        )
        _require(path == expected_zip, "unknown import root; private-tree scans forbidden")
        archives[str(path)] = (
            digest(
                confined_path(source_root(path.parent), path.name, "stdlib archive").read_bytes()
            )
            if path.exists()
            else None
        )
    inventories = {directory: _tree_inventory(Path(directory)) for directory in roots}
    native = {
        str(Path(directory) / name): sha
        for directory, files in inventories.items()
        for name, sha in files.items()
        if name.endswith((".so", ".pyd", ".dll", ".dylib"))
    }
    flags = {
        name: getattr(sys.flags, name)
        for name in dir(sys.flags)
        if not name.startswith("_") and type(getattr(sys.flags, name)) is int
    }
    # The launcher must sanitize its environment. This hash binds its complete
    # process environment without copying secret values into the freeze/report.
    return {
        "schema": "m1-path-python-environment-v1",
        "implementation": "CPython",
        "version": sys.version,
        "executable": str(executable),
        "executable_sha256": digest(executable.read_bytes()),
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "platform": sys.platform,
        "machine": platform.machine(),
        "cache_tag": sys.implementation.cache_tag,
        "flags": flags,
        "sys_path": imports,
        "environment_sha256": digest(canonical(dict(os.environ))),
        "dependency_roots": roots,
        "dependency_inventory_sha256": digest(canonical(inventories)),
        "dependency_files": sum(len(files) for files in inventories.values()),
        "native_code_sha256": native,
        "mapped_code_sha256": mapped_code_snapshot(),
        "external_import_archives": archives,
        "venv_configuration_sha256": (
            digest(confined_path(source_root(Path(sys.prefix)), "pyvenv.cfg", "venv").read_bytes())
            if sys.prefix != sys.base_prefix
            else None
        ),
    }


def verify_mapped_libraries(environment: dict) -> None:
    declared = {
        **environment["native_code_sha256"],
        **environment["mapped_code_sha256"],
        environment["executable"]: environment["executable_sha256"],
    }
    for name, sha in mapped_code_snapshot().items():
        _require(declared.get(name) == sha, "new or changed native executable mapping")


def _verify_gates(root: Path, freeze: dict, contract: dict) -> None:
    common = {
        "schema",
        "status",
        "source_contract_sha256",
        "inputs_sha256",
        "configuration_sha256",
        "raw_evidence",
    }
    gates = {
        name: parse_json(_read_binding(root, binding, name))
        for name, binding in freeze["gates"].items()
    }
    for name, gate in gates.items():
        extra = {
            "g0": {"runtime_sources_sha256", "terminal"},
            "source_delta_reconciliation": {
                "from_runtime_sources_sha256",
                "to_runtime_sources_sha256",
                "changed_paths",
                "g0_evidence_sha256",
                "review_reference",
            },
            "three_observation_eligibility": {"arms", "observations_per_arm"},
            "constructor_census": {
                "observed_eligibility_per_type",
                "derived_success_counts",
                "prospective_rollback_additions",
                "prospective_type_caps",
                "derivation_reference",
                "observed_routes",
                "unobserved_routes",
            },
        }[name]
        _keys(gate, common | extra, name + " evidence")
        _require(
            gate["schema"] == "m1-path-" + name.replace("_", "-") + "-v1",
            name + " evidence schema differs",
        )
        _require(
            gate["status"]
            == {
                "g0": "SUCCESS",
                "source_delta_reconciliation": "RECONCILED",
                "three_observation_eligibility": "OBSERVED_ELIGIBLE",
                "constructor_census": "REVIEWED_DERIVATION_WITH_OBSERVED_ELIGIBILITY",
            }[name],
            name + " gate not satisfied",
        )
        _sha(gate["source_contract_sha256"], name + " source contract")
        if name != "g0":
            _require(
                gate["source_contract_sha256"] == freeze["source_contract"]["sha256"],
                name + " refers to a different source contract",
            )
        for key in ("inputs_sha256", "configuration_sha256"):
            _sha(gate[key], name + " " + key)
        if name != "g0":
            _require(
                gate["inputs_sha256"] == freeze["inputs"]["sha256"]
                and gate["configuration_sha256"] == digest(canonical(freeze["configuration"])),
                name + " input/configuration binding differs",
            )
        _evidence_files(root, gate["raw_evidence"], name)
    g0 = gates["g0"]
    _hash_map(g0["runtime_sources_sha256"], "observed G0 runtime")
    terminal = parse_json(_read_binding(root, g0["terminal"], "G0 terminal"))
    _require(
        type(terminal) is dict
        and terminal.get("status") == "SUCCESS"
        and terminal.get("identity") == "assembly-m1-g0-v1-20261002",
        "G0 terminal is not successful actual G0",
    )
    delta = gates["source_delta_reconciliation"]
    old, new = g0["runtime_sources_sha256"], contract["runtime_sources_sha256"]
    _require(
        delta["from_runtime_sources_sha256"] == old
        and delta["to_runtime_sources_sha256"] == new
        and delta["g0_evidence_sha256"] == freeze["gates"]["g0"]["sha256"],
        "G0 source delta does not reconcile the exact observed and proposed runtimes",
    )
    changed = sorted(key for key in old.keys() | new.keys() if old.get(key) != new.get(key))
    _require(
        delta["changed_paths"] == changed
        and type(delta["review_reference"]) is str
        and bool(delta["review_reference"]),
        "source delta review is incomplete",
    )
    eligibility = gates["three_observation_eligibility"]
    _require(
        type(eligibility["observations_per_arm"]) is int
        and eligibility["observations_per_arm"] == 3,
        "exact three-observation proof missing",
    )
    _keys(eligibility["arms"], {"S", "R"}, "eligible arms")
    for arm in eligibility["arms"].values():
        _keys(arm, {"fullgraph_verified", "checkpoint_roundtrip_verified", "evidence"}, "arm")
        _require(
            arm["fullgraph_verified"] is True and arm["checkpoint_roundtrip_verified"] is True,
            "actual fullgraph/checkpoint eligibility not established",
        )
        _evidence_files(root, arm["evidence"], "arm eligibility")
    census = gates["constructor_census"]
    _require(
        canonical(census["derived_success_counts"]) == canonical(PROSPECTIVE_SUCCESS_COUNTS)
        and canonical(census["prospective_rollback_additions"])
        == canonical(PROSPECTIVE_ROLLBACK_ADDITIONS),
        "source-derived constructor/shell totals do not reconcile the proposed call plan",
    )
    _require(
        type(census["derivation_reference"]) is str and bool(census["derivation_reference"]),
        "reviewed finite per-type cap derivation is missing",
    )
    _require(census["unobserved_routes"] == [], "unobserved constructor/shell routes remain")
    allocation_types = contract.get("allocation_type_sources")
    _require(
        type(allocation_types) is dict and bool(allocation_types),
        "complete allocation-type source inventory is missing",
    )
    _require(
        all(
            type(name) is str
            and name.startswith("sparkbrain.")
            and name.count(":") == 1
            and name.split(":", 1)[1].isidentifier()
            for name in allocation_types
        ),
        "invalid allocation-type inventory key",
    )
    # Retained graph schemas are intentionally narrower: transient return values
    # (e.g. SensoryChannelDecision/V032StepResult) are also actual constructors.
    # The source verifier binds this separate complete top-level class inventory.
    expected_classes = set(allocation_types)
    expected_classes.update({"random:Random", "_thread:lock", "_thread:RLock"})
    # Observations here belong to the independently approved eligibility check,
    # NOT an already completed instance of the not-yet-admitted 68-window pilot.
    for field in ("observed_eligibility_per_type", "prospective_type_caps"):
        _keys(census[field], expected_classes, field)
        for row in census[field].values():
            _keys(row, {"init", "shell"}, "per-type census row")
            _require(
                all(type(value) is int and value >= 0 for value in row.values()),
                "invalid observed count or prospective cap",
            )
    excluded = contract.get("excluded_constructor_types")
    _require(
        type(excluded) is list
        and all(type(name) is str and name in allocation_types for name in excluded)
        and excluded == sorted(set(excluded)),
        "source-verified excluded constructor inventory is missing or malformed",
    )
    # Source class coverage is not allocator coverage. Inherited constructors
    # without a declared Python __init__ remain excluded until a reviewed schema
    # and instrumentation change. Zero caps constrain admission; the separate
    # before-call source guard supplies the demonstrated C-allocation boundary.
    for name in excluded:
        for field in ("observed_eligibility_per_type", "prospective_type_caps"):
            _require(
                census[field][name] == {"init": 0, "shell": 0},
                "excluded constructor requires zero observed counts and caps: " + name,
            )
    enum_imports = contract.get("import_enum_initializations")
    _keys(
        enum_imports,
        {
            "sparkbrain.model:SparkKind",
            "sparkbrain.model:EventKind",
            "sparkbrain.v03_seed.revision:TransitionKind",
        },
        "source-verified import enum initialization inventory",
    )
    _require(
        type(enum_imports) is dict
        and bool(enum_imports)
        and all(
            type(name) is str
            and name in allocation_types
            and name not in excluded
            and type(count) is int
            and count > 0
            for name, count in enum_imports.items()
        ),
        "source-verified import enum initialization inventory is missing or malformed",
    )
    # These exact StrEnum classes have a countable inherited Python Enum.__init__.
    # Source verification derives singleton counts from their declared members;
    # this exception never admits other inherited constructors or guesses shells.
    for name, count in enum_imports.items():
        for field in ("observed_eligibility_per_type", "prospective_type_caps"):
            _require(
                census[field][name]["init"] >= count,
                "import enum initialization coverage is below its source-derived floor: " + name,
            )
    routes = census["observed_routes"]
    _require(type(routes) is list and bool(routes), "actual observed constructor routes missing")
    totals = {name: {"init": 0, "shell": 0} for name in expected_classes}
    seen = set()
    for row in routes:
        _keys(row, {"type", "path", "qualname", "kind", "count"}, "observed route")
        _relative(row["path"], "observed route")
        _require(
            row["type"] in totals
            and row["kind"] in {"init", "shell"}
            and type(row["qualname"]) is str
            and bool(row["qualname"])
            and type(row["count"]) is int
            and row["count"] > 0,
            "invalid observed constructor/shell route",
        )
        key = tuple(row[name] for name in ("type", "path", "qualname", "kind"))
        _require(key not in seen, "duplicate observed constructor/shell route")
        seen.add(key)
        totals[row["type"]][row["kind"]] += row["count"]
    _require(
        totals == census["observed_eligibility_per_type"],
        "route counts do not equal complete observed eligibility census",
    )


def verify_preparation(root: Path, freeze_relative: str, *, check_environment: bool = True) -> dict:
    """Read-only prospective validation; a successful return is not a permit."""
    root = source_root(root)
    freeze_relative = _relative(freeze_relative, "freeze")
    raw = confined_path(root, freeze_relative, "execution freeze").read_bytes()
    freeze = validate_freeze_schema(parse_json(raw))
    verified = verify(root)  # New repaired-source verifier, never historical G0 verify.
    contract = parse_json(_read_binding(root, freeze["source_contract"], "source contract"))
    _require(
        verified["contract_sha256"] == freeze["source_contract"]["sha256"],
        "verified source contract differs from freeze",
    )
    inventory = freeze["source_files_sha256"]
    required = {
        CONTRACT,
        "scripts/m1_path_admission.py",
        "scripts/m1_path_native.py",
        "scripts/m1_path_pilot.py",
        "scripts/m1_path_inputs.py",
        "scripts/m1_path_census.py",
        "scripts/verify_m1_path_source.py",
        "scripts/g0_joint_ownership.py",
        "scripts/verify_g0_joint_source_contract.py",
        "tests/test_m1_path_admission.py",
    }
    for key in ("runtime_sources_sha256", "runtime_schema_sha256", "preparation_sources_sha256"):
        for name, sha in contract[key].items():
            _require(inventory.get(name) == sha, "full runtime/preparation hash missing: " + name)
        required.update(contract[key])
    for binding in (
        freeze["inputs"],
        freeze["teaching"]["evaluator"],
        freeze["launcher"]["implementation"],
        *freeze["gates"].values(),
    ):
        required.add(binding["path"])
        _require(
            inventory.get(binding["path"]) == binding["sha256"],
            "frozen binding absent from complete inventory",
        )
    _require(
        freeze_relative not in inventory and required <= inventory.keys(),
        "self-referential or incomplete source inventory",
    )
    for name, sha in inventory.items():
        _require(
            digest(confined_path(root, name, "frozen source").read_bytes()) == sha,
            "frozen source bytes changed: " + name,
        )
    from scripts.m1_path_inputs import teaching_schedule, validate_observation
    from scripts.m1_path_native import source_configuration

    rows = [
        parse_json(line) for line in _read_binding(root, freeze["inputs"], "inputs").splitlines()
    ]
    _require(len(rows) == 68, "exact 68 input windows required")
    for row in rows:
        validate_observation(row)
    evaluator = parse_json(_read_binding(root, freeze["teaching"]["evaluator"], "evaluator"))
    _require(
        digest(canonical(teaching_schedule(evaluator))) == freeze["teaching"]["subset_sha256"],
        "truth-minimized teaching subset differs",
    )
    _require(
        canonical(source_configuration(root)) == canonical(freeze["configuration"]),
        "frozen source configuration differs",
    )
    _verify_gates(root, freeze, contract)
    for directory in ("src/sparkbrain", "scripts"):
        pending = [confined_path(root, directory, "source directory", directory=True)]
        while pending:
            for child in pending.pop().iterdir():
                info = path_metadata(child, "source bytecode")
                if stat.S_ISDIR(info.st_mode):
                    pending.append(child)
                else:
                    _require(child.suffix not in {".pyc", ".pyo"}, "preexisting source bytecode")
    if check_environment:
        actual = environment_snapshot(root)
        declared = primitive(freeze["environment"])
        # Native imports may map inventoried extension/system libraries. Those
        # mappings are checked independently; they cannot expand the allowlist.
        actual.pop("mapped_code_sha256")
        declared.pop("mapped_code_sha256")
        _require(
            canonical(declared) == canonical(actual),
            "interpreter/stdlib/native environment differs",
        )
        verify_mapped_libraries(freeze["environment"])
    return {
        "status": "PROSPECTIVE_VALIDATION_ONLY",
        "runtime_execution_authorized": False,
        "scientific_credit": 0,
        "freeze_sha256": digest(raw),
        "freeze": freeze,
        "environment_checked": check_environment,
    }


_PERMITS: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


class Permit:
    """Opaque capability: construction, copying and attribute injection cannot mint one."""

    __slots__ = ("__weakref__",)

    def __new__(cls) -> Permit:
        raise AdmissionError("only separately verified execution admission can issue a permit")

    @property
    def root(self) -> Path:
        return _permit_record(self)["root"]

    @property
    def freeze(self) -> dict:
        return primitive(_permit_record(self)["verified"]["freeze"])

    @property
    def identity(self) -> str:
        _permit_record(self)
        return IDENTITY

    def __reduce_ex__(self, protocol: int) -> Any:
        raise AdmissionError("execution permits cannot be copied or serialized")


def _permit_record(permit: Permit) -> dict:
    _require(type(permit) is Permit and permit in _PERMITS, "unissued execution permit")
    return _PERMITS[permit]


def require_permit(permit: Permit) -> Permit:
    _require(APPROVED_FREEZE_SHA256 is not None, "no reviewed execution freeze is approved")
    record = _permit_record(permit)
    _require(
        record["pid"] == os.getpid()
        and record["state"] == "ACTIVE"
        and record["owner"] is threading.current_thread(),
        "permit is inactive or outside its original process/owner thread",
    )
    try:
        current = verify_preparation(record["root"], record["freeze_relative"])
        _require(
            current == record["verified"] and current["freeze_sha256"] == APPROVED_FREEZE_SHA256,
            "execution freeze changed after admission",
        )
        _require(
            digest(
                confined_path(
                    record["root"], record["authority_relative"], "external authority"
                ).read_bytes()
            )
            == record["authority_sha256"],
            "external authority changed after admission",
        )
    except BaseException:
        record["state"] = "POISONED"
        raise
    return permit


def authorize_execution(
    root: Path,
    freeze_relative: str,
    authority_relative: str,
    expected_authority_sha256: str,
    authority_verifier: Callable[[dict], bool] | None = None,
) -> Permit:
    """Prospective ISSUED capability, unusable until actual launch/owner attestation.

    The source-pinned external authority verifier is part of the reviewed trusted
    launcher. A local JSON claim or arbitrary callback is not accepted. None of
    this is reachable while APPROVED_FREEZE_SHA256 remains None.
    """
    _require(APPROVED_FREEZE_SHA256 is not None, "no reviewed execution freeze is approved")
    _require(callable(authority_verifier), "independent external authority verifier required")
    _sha(expected_authority_sha256, "external authority")
    _require(
        not any(name == "sparkbrain" or name.startswith("sparkbrain.") for name in sys.modules),
        "fresh native imports required",
    )
    root = source_root(root)
    verified = verify_preparation(root, freeze_relative)
    _require(verified["freeze_sha256"] == APPROVED_FREEZE_SHA256, "unapproved execution freeze")
    authority = parse_json(
        _read_binding(
            root,
            {"path": authority_relative, "sha256": expected_authority_sha256},
            "external authority",
        )
    )
    _keys(
        authority,
        {
            "schema",
            "identity",
            "freeze_sha256",
            "source_inventory_sha256",
            "source_contract_sha256",
            "actual_execution_authorized",
            "synthetic",
            "user_approval_reference",
            "publication_reference",
            "review",
            "output_directory",
            "execution_nonce",
            "identity_ledger",
            "identity_previously_consumed",
        },
        "external authority",
    )
    freeze = verified["freeze"]
    _require(
        authority["schema"] == "m1-path-execution-authority-v1"
        and authority["identity"] == IDENTITY
        and authority["freeze_sha256"] == verified["freeze_sha256"]
        and authority["source_inventory_sha256"] == digest(canonical(freeze["source_files_sha256"]))
        and authority["source_contract_sha256"] == freeze["source_contract"]["sha256"]
        and authority["actual_execution_authorized"] is True
        and authority["synthetic"] is False
        and authority["identity_previously_consumed"] is False,
        "authority does not bind exact source/freeze/unused identity",
    )
    for key in ("user_approval_reference", "publication_reference", "execution_nonce"):
        _require(type(authority[key]) is str and bool(authority[key]), "missing authority " + key)
    review = _keys(
        authority["review"], {"reference", "freeze_sha256", "unresolved_findings"}, "review"
    )
    _require(
        type(review["reference"]) is str
        and bool(review["reference"])
        and review["freeze_sha256"] == verified["freeze_sha256"]
        and type(review["unresolved_findings"]) is int
        and review["unresolved_findings"] == 0,
        "exact-freeze review is missing or has unresolved findings",
    )
    output = authority["output_directory"]
    _require(
        type(output) is str and Path(output).is_absolute(), "absolute output directory required"
    )
    output_path = source_root(Path(output).parent) / Path(output).name
    _require(not output_path.exists() and not output_path.is_symlink(), "output already consumed")
    ledger = parse_json(_read_absolute_binding(authority["identity_ledger"], "identity ledger"))
    _keys(ledger, {"schema", "identities"}, "identity ledger")
    _require(
        ledger["schema"] == "m1-path-identity-ledger-v1"
        and type(ledger["identities"]) is dict
        and ledger["identities"].get(IDENTITY) == {"state": "UNCONSUMED"},
        "authoritative one-shot identity is missing or consumed",
    )
    _verify_callback(root, freeze, authority_verifier, "authority_verifier")
    _require(
        authority_verifier(primitive(authority)) is True,
        "separate external execution authority not verified",
    )
    permit = object.__new__(Permit)
    _PERMITS[permit] = {
        "root": root,
        "verified": verified,
        "freeze_relative": freeze_relative,
        "authority_relative": authority_relative,
        "authority_sha256": expected_authority_sha256,
        "authority": authority,
        "pid": os.getpid(),
        "issuer": threading.current_thread(),
        "owner": None,
        "state": "ISSUED",
        "claim_attempted": False,
    }
    return permit


def _read_absolute_binding(value: Any, label: str) -> bytes:
    _keys(value, {"path", "sha256"}, label)
    path = value["path"]
    _require(type(path) is str and Path(path).is_absolute(), label + " must be absolute")
    _sha(value["sha256"], label)
    path = Path(path)
    raw = confined_path(source_root(path.parent), path.name, label).read_bytes()
    _require(digest(raw) == value["sha256"], label + " bytes changed")
    return raw


def _verify_callback(root: Path, freeze: dict, callback: Any, field: str) -> None:
    _require(type(callback) is types.FunctionType, "reviewed source-bound verifier required")
    launcher = freeze["launcher"]
    name = launcher[field]
    module = sys.modules.get(callback.__module__)
    _require(
        type(module) is types.ModuleType
        and callback.__qualname__ == name
        and vars(module).get(name) is callback,
        "verifier is not the exact reviewed binding",
    )
    expected = confined_path(root, launcher["implementation"]["path"], "launcher implementation")
    _require(
        Path(callback.__code__.co_filename) == expected
        and inspect.getsourcefile(callback) == str(expected),
        "verifier source differs from reviewed launcher",
    )
    _read_binding(root, launcher["implementation"], "launcher implementation")


def claim_owner(
    permit: Permit, launch_attestation: dict, launch_verifier: Callable[[dict], bool]
) -> Permit:
    """Activate exactly once on the dedicated owner after actual launcher checks.

    The reviewed verifier must inspect installed limits/hooks, durable reservation,
    fresh imports, raw-before-decode profiling and finalization readiness itself.
    Attestation flags alone never satisfy this boundary. Failed activation poisons
    this process-local capability; it cannot release/reset a durable reservation.
    """
    _require(APPROVED_FREEZE_SHA256 is not None, "no reviewed execution freeze is approved")
    record = _permit_record(permit)
    _require(
        record["pid"] == os.getpid()
        and record["state"] == "ISSUED"
        and not record["claim_attempted"],
        "permit already claimed/poisoned or wrong process",
    )
    record["claim_attempted"] = True
    record["state"] = "POISONED"
    _require(
        threading.current_thread() is not record["issuer"]
        and threading.current_thread() is not threading.main_thread(),
        "activation requires a distinct dedicated owner thread",
    )
    freeze = record["verified"]["freeze"]
    attestation = primitive(launch_attestation)
    _keys(
        attestation,
        {
            "schema",
            "identity",
            "freeze_sha256",
            "output_directory",
            "execution_nonce",
            "reservation",
            "limits",
            "finalization_reserves",
            "profile_manifest",
            "owner_thread_id",
            "process_id",
        },
        "actual launch",
    )
    authority = record["authority"]
    _require(
        attestation["schema"] == "m1-path-actual-launch-v1"
        and attestation["identity"] == IDENTITY
        and attestation["freeze_sha256"] == APPROVED_FREEZE_SHA256
        and attestation["output_directory"] == authority["output_directory"]
        and attestation["execution_nonce"] == authority["execution_nonce"]
        and canonical(attestation["limits"]) == canonical(freeze["limits"])
        and canonical(attestation["finalization_reserves"])
        == canonical(freeze["finalization_reserves"])
        and type(attestation["owner_thread_id"]) is int
        and attestation["owner_thread_id"] == threading.get_ident()
        and type(attestation["process_id"]) is int
        and attestation["process_id"] == os.getpid(),
        "actual launch differs from exact authority/owner/budget",
    )
    reservation = parse_json(
        _read_absolute_binding(attestation["reservation"], "durable reservation")
    )
    _keys(
        reservation,
        {"identity", "freeze_sha256", "execution_nonce", "output_directory", "state"},
        "durable reservation",
    )
    _require(
        reservation
        == {
            "identity": IDENTITY,
            "freeze_sha256": APPROVED_FREEZE_SHA256,
            "execution_nonce": authority["execution_nonce"],
            "output_directory": authority["output_directory"],
            "state": "STARTED",
        },
        "actual one-shot reservation differs",
    )
    _read_absolute_binding(attestation["profile_manifest"], "actual profile manifest")
    _verify_callback(record["root"], freeze, launch_verifier, "runtime_verifier")
    _require(
        launch_verifier(primitive(attestation)) is True,
        "actual launcher/profiler/limits/finalization were not independently verified",
    )
    record["owner"] = threading.current_thread()
    record["state"] = "ACTIVE"
    record["launch_attestation"] = attestation
    return require_permit(permit)


def close_permit(permit: Permit) -> None:
    """Irrevocably revoke on the exact owner; does not assert successful cleanup."""
    record = _permit_record(permit)
    _require(
        record["pid"] == os.getpid() and record["owner"] is threading.current_thread(),
        "permit revocation requires its original owner",
    )
    record["state"] = "CLOSED"


def bind_source_registry(permit: Permit, loaded_classes: tuple[type, ...]) -> Any:
    """Bind already loaded exact classes to the NEW contract without importing native code."""
    require_permit(permit)
    import random

    from scripts.g0_joint_ownership import SourceRegistry, TypeSpec

    root = permit.root
    verified = verify(root)
    raw = confined_path(root, CONTRACT, "new source contract").read_bytes()
    _require(
        digest(raw) == verified["contract_sha256"], "source contract changed after verification"
    )
    contract = parse_json(raw)
    _require(type(loaded_classes) is tuple, "loaded class inventory must be an exact tuple")
    expected = {(path, name) for path, row in contract["files"].items() for name in row["classes"]}
    seen, specs = set(), []
    for loaded in loaded_classes:
        _require(type(loaded) is type, "loaded registry requires exact class objects")
        if loaded is random.Random:
            key = ("stdlib", "random.Random")
            spec = TypeSpec(loaded, "stdlib:random.Random:exact-state-v1", ("gauss_next",))
        else:
            module = sys.modules.get(loaded.__module__)
            _require(
                type(module) is types.ModuleType
                and loaded.__qualname__ == loaded.__name__
                and vars(module).get(loaded.__name__) is loaded,
                "loaded class is not its exact module-level binding",
            )
            relative = "src/" + loaded.__module__.replace(".", "/") + ".py"
            key = (relative, loaded.__name__)
            _require(key in expected, "class absent from new source contract")
            path = confined_path(root, relative, "runtime class source")
            try:
                paths = (Path(vars(module)["__file__"]), Path(inspect.getsourcefile(loaded)))
                for actual in paths:
                    _require(
                        confined_path(
                            root, actual.relative_to(root).as_posix(), "loaded class source"
                        )
                        == path,
                        "loaded class/module path differs from verified source root",
                    )
            except (KeyError, TypeError, ValueError) as exc:
                raise AdmissionError("loaded class/module source path is unavailable") from exc
            row = contract["files"][relative]
            _require(digest(path.read_bytes()) == row["sha256"], "full class source hash changed")
            witness = row["classes"][loaded.__name__]
            slots = tuple(witness["slot_fields"])
            spec = TypeSpec(
                loaded,
                f"{relative}:{loaded.__name__}@{row['sha256']}",
                None if slots else tuple(witness["dict_fields"]),
                slots,
            )
        _require(key not in seen, "duplicate exact class in loaded registry")
        seen.add(key)
        specs.append(spec)
    _require(seen == expected | {("stdlib", "random.Random")}, "incomplete loaded class inventory")
    registry = object.__new__(SourceRegistry)
    # Preserve the existing exact resource-binding checks in validate_resources.
    registry.domain = "VERIFIED_SOURCE_PREPARATION"
    registry.contract_sha256 = verified["contract_sha256"]
    registry.source_root = root
    registry._populate(tuple(specs))
    return registry
