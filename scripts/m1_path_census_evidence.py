"""Read-only validation of prospective PassiveCensus evidence, never a model run.

The gate binds an ordered file per emitted event, the unmodified ``snapshot()``
JSON and an independently retained closed-session terminal manifest. No such
native evidence is bundled. A future launcher must produce this exact envelope;
self-consistent JSON is not a substitute for its separate execution authority.
"""

from __future__ import annotations

import ast
import sysconfig
from collections import Counter, defaultdict
from pathlib import Path

from scripts.verify_g0_joint_source_contract import class_spec, confined_path, source_root

CENSUS_SOURCE = "scripts/m1_path_census.py"
CLONE = ("scripts/g0_joint_ownership.py", "_construct")
DECODE = ("src/sparkbrain/v032/checkpoint.py", "_decode")
LOAD = ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes")
RAW_TYPE = "sparkbrain.v03.runtime:IntegratedV03Brain"
FACADE_TYPE = "sparkbrain.v032.runtime:IntegratedV032Brain"
RESOURCE_ROUTES = {
    "model_rng": {
        ("src/sparkbrain/v03/runtime.py", "IntegratedV03Brain._initialize_runtime"),
        DECODE,
        CLONE,
    },
    "topology_rng": {("src/sparkbrain/v05/topology.py", "layered_reservoir_topology")},
    "model_lock": {("src/sparkbrain/v032/runtime.py", "_shared_step_lock")},
    "registry_guard": {("src/sparkbrain/v032/runtime.py", "<module>")},
}
RESOURCE_TYPES = {
    "model_rng": ("random:Random", "init"),
    "topology_rng": ("random:Random", "init"),
    "model_lock": ("_thread:RLock", "init"),
    "registry_guard": ("_thread:lock", "shell"),
}


def _functions(tree: ast.AST) -> set[str]:
    result = set()

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                walk(child, prefix + child.name + ".")
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                result.add(name)
                walk(child, name + ".<locals>.")
            else:
                walk(child, prefix)

    walk(tree, "")
    return result


def _dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        call = decorator if isinstance(decorator, ast.Call) else None
        target = decorator.func if call else decorator
        if not (
            isinstance(target, ast.Name)
            and target.id == "dataclass"
            or isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "dataclasses"
            and target.attr == "dataclass"
        ):
            continue
        if call and any(
            key.arg == "init" and isinstance(key.value, ast.Constant) and key.value.value is False
            for key in call.keywords
        ):
            return False
        return True
    return False


def _codec_types(tree, require):
    constants, registry, objects = {}, None, None
    for node in tree.body:
        if (
            not isinstance(node, ast.Assign)
            or len(node.targets) != 1
            or not isinstance(node.targets[0], ast.Name)
        ):
            continue
        name = node.targets[0].id
        if isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            constants[name] = node.value.value
        elif name == "_CLASSES":
            call = node.value
            require(
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "frozenset"
                and len(call.args) == 1
                and not call.keywords
                and isinstance(call.args[0], ast.Set),
                "unsupported source codec class registry",
            )
            registry = set()
            for item in call.args[0].elts:
                value = (
                    constants.get(item.id)
                    if isinstance(item, ast.Name)
                    else (item.value if isinstance(item, ast.Constant) else None)
                )
                require(type(value) is str, "nonliteral source codec class registry")
                registry.add(value)
        elif name == "_OBJECT_ATTRS":
            require(isinstance(node.value, ast.Dict), "unsupported source codec object registry")
            objects = set()
            for item in node.value.keys:
                require(
                    isinstance(item, ast.Constant) and type(item.value) is str,
                    "nonliteral source codec object type",
                )
                objects.add(item.value)
    require(registry is not None and objects is not None, "source codec registries missing")
    require(objects <= registry, "source codec object registry exceeds class registry")
    return registry, objects


def validate_census_evidence(root: Path, freeze: dict, contract: dict, census: dict) -> None:
    """Derive counts/routes from complete source-bound raw attempts and successes.

    ``profiler_evidence`` has exactly schema/census_implementation/stdlib_sources/
    call_targets/call_caps/events/snapshot/terminal. The terminal has exactly
    schema/status/source_contract_sha256/snapshot/events/event_count/final_sequence/
    closed/pending_calls/pending_shells/failure. Its event list and snapshot binding
    must match the gate, and every referenced file is in ``raw_evidence`` exactly once.
    Exception, poisoned, open and pending sessions cannot prove positive eligibility.
    """
    from scripts.m1_path_admission import (
        _binding,
        _keys,
        _read_absolute_binding,
        _read_binding,
        _relative,
        _require,
        canonical,
        parse_json,
    )

    root = source_root(root)
    profile = _keys(
        census["profiler_evidence"],
        {
            "schema",
            "census_implementation",
            "stdlib_sources",
            "call_targets",
            "call_caps",
            "events",
            "snapshot",
            "terminal",
        },
        "profiler evidence",
    )
    _require(
        profile["schema"] == "m1-path-passive-census-evidence-v1",
        "unsupported profiler evidence schema",
    )
    implementation = _binding(profile["census_implementation"], "census implementation")
    _require(
        implementation["path"] == CENSUS_SOURCE
        and freeze["source_files_sha256"].get(CENSUS_SOURCE) == implementation["sha256"],
        "profiler implementation is outside the exact freeze",
    )
    _read_binding(root, implementation, "census implementation")
    trees, functions = {}, set()

    def source(path, expected):
        if path not in trees:
            _require(
                freeze["source_files_sha256"].get(path) == expected,
                "route source is absent from exact freeze: " + path,
            )
            raw = _read_binding(root, {"path": path, "sha256": expected}, "route source")
            tree = ast.parse(raw, filename=path)
            trees[path] = tree
            functions.update((path, name) for name in _functions(tree))
        return trees[path]

    # Every callable source must belong to the reviewed runtime/support closure.
    admitted = {**contract["runtime_sources_sha256"], **contract["preparation_sources_sha256"]}
    for path, sha in admitted.items():
        if path.endswith(".py") and not path.startswith("tests/"):
            source(path, sha)
    _require(
        CLONE in functions and DECODE in functions and LOAD in functions,
        "reviewed shell allocation functions are missing",
    )
    stdlib = profile["stdlib_sources"]
    _require(
        type(stdlib) is dict
        and {"enum.py", "random.py", "threading.py", "dataclasses.py"} <= stdlib.keys(),
        "complete constructor stdlib source bindings missing",
    )
    stdlib_root = source_root(Path(sysconfig.get_path("stdlib")))
    for relative, binding in stdlib.items():
        _relative(relative, "stdlib route source")
        _keys(binding, {"path", "sha256"}, "stdlib route source")
        expected = confined_path(stdlib_root, relative, "stdlib route source")
        _require(
            binding.get("path") == str(expected), "stdlib binding is not the current frozen root"
        )
        raw = _read_absolute_binding(binding, "stdlib route source")
        tree = ast.parse(raw, filename=str(expected))
        trees["stdlib/" + relative] = tree
        functions.update(("stdlib/" + relative, name) for name in _functions(tree))
    _require(
        ("stdlib/enum.py", "Enum.__init__") in functions, "reviewed Python Enum initializer missing"
    )
    registry, objects = _codec_types(trees[DECODE[0]], _require)
    retained = {
        path[4:-3].replace("/", ".") + ":" + name
        for path, row in contract["files"].items()
        for name in row["classes"]
    }
    excluded = set(contract["excluded_constructor_types"])
    allowed = {
        name: {"init": set(), "shell": set()} for name in census["observed_eligibility_per_type"]
    }
    for name, record in contract["allocation_type_sources"].items():
        _keys(record, {"path", "sha256", "witness"}, "allocation source witness")
        path = record["path"]
        _require(
            contract["runtime_sources_sha256"].get(path) == record["sha256"],
            "allocation route differs from full runtime source inventory",
        )
        tree = source(path, record["sha256"])
        module, cls = name.split(":")
        actual_module = path.removeprefix("src/").removesuffix(".py").replace("/", ".")
        _require(actual_module.removesuffix(".__init__") == module, "class module/source mismatch")
        matches = [
            node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == cls
        ]
        _require(
            len(matches) == 1 and class_spec(matches[0]) == record["witness"],
            "allocation class AST witness differs",
        )
        node = matches[0]
        if name in excluded:
            continue
        own_init = any(
            isinstance(child, ast.FunctionDef) and child.name == "__init__" for child in node.body
        )
        if own_init:
            allowed[name]["init"].add((path, cls + ".__init__"))
        elif _dataclass(node):
            allowed[name]["init"].add((path, cls + ".__init__[dataclass-generated]"))
        elif name in contract["import_enum_initializations"]:
            _require(
                len(node.bases) == 1
                and isinstance(node.bases[0], ast.Name)
                and node.bases[0].id == "StrEnum",
                "non-StrEnum inherited initializer",
            )
            allowed[name]["init"].add(("stdlib/enum.py", "Enum.__init__"))
        if name in retained and name != FACADE_TYPE:
            allowed[name]["shell"].add(CLONE)
        if name in registry and (name in objects or _dataclass(node)):
            allowed[name]["shell"].add(DECODE)
        if name == RAW_TYPE:
            allowed[name]["shell"].add(LOAD)
    for resource, routes in RESOURCE_ROUTES.items():
        name, kind = RESOURCE_TYPES[resource]
        for route in routes:
            _require(
                route in functions or resource == "registry_guard" and route[0] in trees,
                "resource parent source function is missing",
            )
            allowed[name][kind].add(route)

    targets, caps = profile["call_targets"], profile["call_caps"]
    _require(
        type(targets) is dict
        and type(caps) is dict
        and set(caps) == set(targets) | set(RESOURCE_ROUTES)
        and not set(targets) & set(RESOURCE_ROUTES),
        "incomplete profiler call/resource caps",
    )
    _require(
        all(
            type(name) is str and bool(name) and type(cap) is int and cap >= 0
            for name, cap in caps.items()
        ),
        "malformed profiler call caps",
    )

    def route(value):
        _require(
            type(value) is list
            and len(value) == 2
            and all(type(item) is str and bool(item) for item in value),
            "malformed event route",
        )
        _relative(value[0], "event source")
        return tuple(value)

    target_routes = {name: route(value) for name, value in targets.items()}
    _require(
        len(set(target_routes.values())) == len(target_routes)
        and all(value in functions for value in target_routes.values()),
        "call target is outside admitted source functions",
    )
    bindings = profile["events"]
    _require(
        type(bindings) is list and bool(bindings), "complete raw census event manifest missing"
    )
    events = []
    for index, binding in enumerate(bindings, 1):
        _binding(binding, "raw census event")
        _require(
            Path(binding["path"]).name == f"census-{index:07d}.json",
            "raw census event filenames are not contiguous",
        )
        events.append(parse_json(_read_binding(root, binding, "raw census event")))
    snapshot = parse_json(_read_binding(root, profile["snapshot"], "raw census snapshot"))
    terminal = parse_json(_read_binding(root, profile["terminal"], "closed census terminal"))
    _keys(
        terminal,
        {
            "schema",
            "status",
            "source_contract_sha256",
            "snapshot",
            "events",
            "event_count",
            "final_sequence",
            "closed",
            "pending_calls",
            "pending_shells",
            "failure",
        },
        "closed census terminal",
    )
    expected_terminal = {
        "schema": "m1-path-passive-census-terminal-v1",
        "status": "SUCCESS",
        "source_contract_sha256": freeze["source_contract"]["sha256"],
        "snapshot": profile["snapshot"],
        "events": bindings,
        "event_count": len(events),
        "final_sequence": len(events),
        "closed": True,
        "pending_calls": 0,
        "pending_shells": 0,
        "failure": None,
    }
    _require(
        canonical(terminal) == canonical(expected_terminal),
        "profiler terminal is incomplete, pending, failed or has a different event manifest",
    )
    required_raw = [*bindings, profile["snapshot"], profile["terminal"]]
    _require(
        len({item["path"] for item in required_raw}) == len(required_raw)
        and sorted(canonical(item) for item in census["raw_evidence"])
        == sorted(canonical(item) for item in required_raw),
        "raw evidence does not exactly bind all profiler events/snapshot/terminal",
    )
    _keys(
        snapshot,
        {
            "call_attempts",
            "call_returns",
            "types",
            "pending_calls",
            "pending_shells",
            "failure",
            "events",
        },
        "raw PassiveCensus snapshot",
    )
    _require(
        canonical(snapshot["events"]) == canonical(events)
        and type(snapshot["pending_calls"]) is int
        and snapshot["pending_calls"] == 0
        and type(snapshot["pending_shells"]) is int
        and snapshot["pending_shells"] == 0
        and snapshot["failure"] is None,
        "raw census snapshot is incomplete or poisoned",
    )
    calls, returns = dict.fromkeys(caps, 0), dict.fromkeys(caps, 0)
    types = {name: {"init": 0, "shell": 0, "init_return": 0, "shell_return": 0} for name in allowed}
    pending_types, pending_calls = defaultdict(list), defaultdict(list)
    type_routes, resource_calls = Counter(), Counter()
    births = 0
    owner_thread = None
    for sequence, event in enumerate(events, 1):
        _require(
            type(event) is dict
            and type(event.get("sequence")) is int
            and event["sequence"] == sequence
            and type(event.get("thread")) is int
            and event["thread"] > 0,
            "malformed or noncontiguous raw census event",
        )
        kind, thread = event.get("kind"), event["thread"]
        fields = {
            "type_attempt": {"type", "allocation", "route", "count"},
            "type_birth": {"type", "allocation", "route", "birth", "runtime_id"},
            "call_attempt": {"name", "route", "count"},
            "call_return": {"name"},
            "ancillary_rng": {"route"},
        }
        _require(type(kind) is str and kind in fields, "unknown/exception profiler event")
        _keys(event, {"sequence", "kind", "thread"} | fields[kind], "raw census event")
        if kind != "ancillary_rng":
            if owner_thread is None:
                owner_thread = thread
            _require(
                thread == owner_thread, "model census events differ from dedicated owner thread"
            )
        if kind in {"type_attempt", "type_birth"}:
            name, allocation = event["type"], event["allocation"]
            _require(
                type(name) is str
                and name in allowed
                and type(allocation) is str
                and allocation in {"init", "shell"},
                "unknown census allocation type/kind",
            )
            current = route(event["route"])
            _require(
                current in allowed[name][allocation],
                "constructor/allocation route is outside exact source support: " + name,
            )
            key = (thread, name, allocation)
            if kind == "type_attempt":
                resource = next(
                    (
                        resource
                        for resource, pair in RESOURCE_TYPES.items()
                        if pair == (name, allocation) and current in RESOURCE_ROUTES[resource]
                    ),
                    None,
                )
                if resource is not None:
                    _require(
                        bool(pending_calls[(thread, resource)])
                        and pending_calls[(thread, resource)][-1] == current,
                        "resource type attempt lacks its active matching source call",
                    )
                types[name][allocation] += 1
                _require(
                    type(event["count"]) is int and event["count"] == types[name][allocation],
                    "raw type attempt counter is not cumulative",
                )
                pending_types[key].append(current)
                type_routes[(name, *current, allocation)] += 1
            else:
                births += 1
                _require(
                    type(event["birth"]) is int
                    and event["birth"] == births
                    and type(event["runtime_id"]) is int
                    and event["runtime_id"] > 0,
                    "malformed/noncontiguous allocation birth",
                )
                _require(
                    bool(pending_types[key]) and pending_types[key].pop() == current,
                    "allocation birth has no matching outstanding attempt",
                )
                types[name][allocation + "_return"] += 1
        elif kind == "call_attempt":
            name, current = event["name"], route(event["route"])
            _require(
                type(name) is str
                and name in caps
                and (
                    current in RESOURCE_ROUTES[name]
                    if name in RESOURCE_ROUTES
                    else current == target_routes[name]
                ),
                "unadmitted profiler call route",
            )
            calls[name] += 1
            _require(
                type(event["count"]) is int
                and event["count"] == calls[name]
                and calls[name] <= caps[name],
                "raw call count exceeds or differs from cap",
            )
            pending_calls[(thread, name)].append(current)
            if name in RESOURCE_TYPES:
                typename, allocation = RESOURCE_TYPES[name]
                resource_calls[(typename, *current, allocation)] += 1
        elif kind == "call_return":
            name = event["name"]
            _require(
                type(name) is str and name in caps and bool(pending_calls[(thread, name)]),
                "call return has no matching outstanding attempt",
            )
            pending_calls[(thread, name)].pop()
            returns[name] += 1
        else:
            current = route(event["route"])
            _require(
                not current[0].startswith("src/sparkbrain/") and current in functions,
                "ancillary RNG route is unbound or model-owned",
            )
            _require(
                not any(current in routes for routes in RESOURCE_ROUTES.values()),
                "model resource route cannot be relabeled as ancillary RNG",
            )
    _require(
        not any(pending_types.values()) and not any(pending_calls.values()),
        "raw census event stream has pending attempts",
    )
    actual_resources = Counter(
        {
            key: count
            for key, count in type_routes.items()
            if key[0] in {value[0] for value in RESOURCE_TYPES.values()}
        }
    )
    _require(actual_resources == resource_calls, "resource type attempts and source calls differ")
    _require(
        canonical(snapshot["types"]) == canonical(types)
        and canonical(snapshot["call_attempts"]) == canonical(calls)
        and canonical(snapshot["call_returns"]) == canonical(returns),
        "raw snapshot counts differ from profiler events",
    )
    observed = {
        name: {kind: row[kind] for kind in ("init", "shell")} for name, row in types.items()
    }
    claimed_routes = Counter()
    for row in census["observed_routes"]:
        key = tuple(row[name] for name in ("type", "path", "qualname", "kind"))
        claimed_routes[key] = row["count"]
    _require(
        canonical(observed) == canonical(census["observed_eligibility_per_type"])
        and claimed_routes == type_routes,
        "claimed census totals/routes differ from raw attempts",
    )
