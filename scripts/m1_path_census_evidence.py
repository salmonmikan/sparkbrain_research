"""Read-only validation of prospective PassiveCensus evidence, never a model run.

The gate binds an ordered file per emitted event, the unmodified ``snapshot()``
JSON and an independently retained closed-session terminal manifest. No such
native evidence is bundled. A future launcher must produce this exact envelope;
self-consistent JSON is not a substitute for its separate execution authority.
"""

from __future__ import annotations

import ast
import re
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
FEATURE_TYPE = "sparkbrain.v03_seed.sensory_field:_FeatureState"
SENSORY_SOURCE = "src/sparkbrain/v03_seed/sensory_field.py"
FEATURE_COPY = ("stdlib/copyreg.py", "__newobj__")
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


def _feature_copy_witness(tree: ast.Module, node: ast.ClassDef, require) -> None:
    """Only the frozen default-allocation _states transaction supports copyreg shells.

    The frozen PassiveCensus implementation separately checks the live stdlib
    stack, exact class/function identities, source line, memo and _states values.
    This read-only witness never treats a generic copyreg route as that proof.
    """
    hooks = {
        "__new__",
        "__reduce__",
        "__reduce_ex__",
        "__getstate__",
        "__setstate__",
        "__copy__",
        "__deepcopy__",
        "__del__",
    }
    require(
        not node.bases
        and _dataclass(node)
        and not any(
            isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and member.name in hooks
            for member in node.body
        ),
        "feature-state copy route requires default allocation without custom hooks",
    )
    require(
        any(
            isinstance(item, ast.Import)
            and any(alias.name == "copy" and alias.asname is None for alias in item.names)
            for item in tree.body
        ),
        "sensory copy module binding differs",
    )
    owners = [
        item
        for item in tree.body
        if isinstance(item, ast.ClassDef) and item.name == "AdaptiveSensoryField"
    ]
    require(len(owners) == 1, "sensory transaction source class missing")
    methods = [
        item
        for item in owners[0].body
        if isinstance(item, ast.FunctionDef) and item.name == "observe_with_trace"
    ]
    require(len(methods) == 1, "sensory transaction source method missing")
    assignments = [
        item
        for item in methods[0].body
        if isinstance(item, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "working_states"
            for target in item.targets
        )
    ]
    expected = ast.parse("copy.deepcopy(self._states)", mode="eval").body
    require(
        len(assignments) == 1
        and len(assignments[0].targets) == 1
        and ast.dump(assignments[0].value, include_attributes=False)
        == ast.dump(expected, include_attributes=False),
        "sensory copy route differs from exact working_states deepcopy(_states) callsite",
    )


def _validate_raw_census_evidence(root: Path, freeze: dict, contract: dict, census: dict) -> None:
    """Derive counts/routes from complete source-bound raw attempts and successes.

    ``profiler_evidence`` has exactly schema/census_implementation/eligibility_plan/
    stdlib_sources/call_targets/call_caps/events/snapshot/terminal. The terminal has
    exactly schema/status/source_contract_sha256/eligibility_call_plan/snapshot/
    events/event_count/final_sequence/closed/pending_calls/pending_shells/failure.
    Its event list, reviewed plan and snapshot binding
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
            "eligibility_plan",
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
        and {"enum.py", "random.py", "threading.py", "dataclasses.py", "copy.py", "copyreg.py"}
        <= stdlib.keys(),
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
        if name == FEATURE_TYPE:
            _require(
                path == SENSORY_SOURCE and name in retained,
                "feature-state copy class lacks its exact retained source binding",
            )
            _feature_copy_witness(tree, node, _require)
            _require(
                {
                    FEATURE_COPY,
                    ("stdlib/copy.py", "_reconstruct"),
                    ("stdlib/copy.py", "deepcopy"),
                    ("stdlib/copy.py", "_deepcopy_dict"),
                }
                <= functions,
                "frozen stdlib feature-copy source functions are missing",
            )
            allowed[name]["shell"].add(FEATURE_COPY)
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
            "eligibility_call_plan",
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
        "eligibility_call_plan": profile["eligibility_plan"],
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


CALL_PLAN = (
    "artifacts/research/assembly_m1_path_v1_20261002/three_observation_call_plan.json"
)
PROPOSAL = "docs/research/assembly_m1_three_observation_eligibility_proposal_20261002.md"
PROPOSAL_SHA256 = "a4cb26b00b803176bd3c338f10da861466454ae95c69b5ad0065da330d279ebb"
PROBE_IDENTITY = "assembly-m1-three-observation-eligibility-v1-20261002"
MANDATORY_UNMET = (
    "successful_G0_and_repaired_source_reconciliation",
    "separate_probe_authority_and_dedicated_owner_launcher",
    "weak_registry_object_birth_census",
    "complete_reviewed_finite_per_type_caps",
    "arm_bound_predecessor_graph_and_checkpoint_evidence",
    "fixed_resource_environment_and_finalization_envelope",
)
CONDITIONAL_UNMET = (
    "third_B_endpoint_if_required",
    "AB_BA_AA_control_endpoints_if_required",
    "nonempty_integrated_concept_subtree_if_required",
)
RESOURCE_SUCCESS = {"model_rng": 28, "topology_rng": 1, "model_lock": 28, "registry_guard": 1}
RESOURCE_ROUTE_SUCCESS = (
    ("model_rng", "src/sparkbrain/v03/runtime.py", "IntegratedV03Brain._initialize_runtime", 2),
    ("model_rng", "scripts/g0_joint_ownership.py", "_construct", 12),
    ("model_rng", "src/sparkbrain/v032/checkpoint.py", "_decode", 14),
    ("topology_rng", "src/sparkbrain/v05/topology.py", "layered_reservoir_topology", 1),
    ("model_lock", "src/sparkbrain/v032/runtime.py", "_shared_step_lock", 28),
    ("registry_guard", "src/sparkbrain/v032/runtime.py", "<module>", 1),
)


def _validate_eligibility_plan(root: Path, freeze: dict, contract: dict, census: dict) -> dict:
    """Bind the separately parent-reviewed source proposal, never caller-selected floors."""
    from scripts.m1_path_admission import (
        SOURCE_COMMIT,
        _binding,
        _keys,
        _read_binding,
        _require,
        canonical,
        digest,
        parse_json,
    )
    from scripts.m1_path_inputs import teaching_schedule

    bound = _binding(contract.get("eligibility_call_plan"), "contract eligibility call plan")
    profile = census["profiler_evidence"]
    _require(
        bound["path"] == CALL_PLAN and profile.get("eligibility_plan") == bound,
        "profiler eligibility plan differs from exact source-contract binding",
    )
    for item in (bound, {"path": PROPOSAL, "sha256": PROPOSAL_SHA256}):
        _require(
            contract["preparation_sources_sha256"].get(item["path"]) == item["sha256"]
            and freeze["source_files_sha256"].get(item["path"]) == item["sha256"],
            "eligibility plan/proposal is absent from complete frozen preparation inventory",
        )
    plan = parse_json(_read_binding(root, bound, "reviewed prospective call plan"))
    _keys(
        plan,
        {
            "schema",
            "identity",
            "classification",
            "runtime_execution_authorized",
            "scientific_credit",
            "proposal",
            "runtime_source_commit",
            "runtime_sources_sha256",
            "support_sources_sha256",
            "inputs",
            "teaching",
            "configuration",
            "call_targets",
            "successful_calls",
            "resource_route_success_calls",
            "planned_endpoints",
            "mandatory_unmet_obligations",
            "conditional_unmet_coverage",
            "emergency_ceilings",
        },
        "reviewed prospective call plan",
    )
    _require(
        plan["schema"] == "m1-three-observation-prospective-call-plan-v1"
        and plan["identity"] == PROBE_IDENTITY
        and plan["classification"] == "SOURCE_ONLY_UNEXECUTED_NON_EVIDENTIARY"
        and plan["runtime_execution_authorized"] is False
        and type(plan["scientific_credit"]) is int
        and plan["scientific_credit"] == 0
        and plan["runtime_source_commit"] == SOURCE_COMMIT,
        "eligibility plan source-only identity/scope differs",
    )
    _require(
        plan["proposal"] == {"path": PROPOSAL, "sha256": PROPOSAL_SHA256},
        "eligibility plan does not bind the parent-reviewed proposal",
    )
    proposal = _read_binding(root, plan["proposal"], "parent-reviewed proposal").decode("utf-8")
    targets, success = {}, {}
    for line in proposal.splitlines():
        match = re.fullmatch(
            r"\| ([a-z0-9_]+) \| ((?:src/|scripts/)[^ ]+) \| ([^ ]+) \| ([0-9]+) \|", line
        )
        if match:
            name, path, qualname, count = match.groups()
            _require(name not in targets, "duplicate native call in approved proposal")
            targets[name] = [path, qualname]
            success[name] = int(count)
    _require(len(targets) == 35, "approved native call table is incomplete")
    success.update(RESOURCE_SUCCESS)
    _require(
        canonical(plan["call_targets"]) == canonical(targets)
        and canonical(plan["successful_calls"]) == canonical(success),
        "eligibility call map/vector differs from the approved 35+4-key proposal",
    )
    expected_routes = [
        {"name": name, "route": [path, qualname], "count": count}
        for name, path, qualname, count in RESOURCE_ROUTE_SUCCESS
    ]
    _require(
        canonical(plan["resource_route_success_calls"]) == canonical(expected_routes),
        "eligibility resource route vector differs from the source derivation",
    )
    _require(
        plan["mandatory_unmet_obligations"] == list(MANDATORY_UNMET)
        and plan["conditional_unmet_coverage"] == list(CONDITIONAL_UNMET)
        and plan["planned_endpoints"]
        == ["S:C5:third_A", "S:C6:unadvanced_clone", "R:C5:third_A", "R:C6:unadvanced_clone"]
        and plan["emergency_ceilings"] == "REQUIRE_SEPARATE_REVIEWED_FREEZE_NOT_DERIVED_HERE",
        "fixed unmet obligations/coverage or emergency boundary cannot be erased or broadened",
    )
    _require(
        plan["runtime_sources_sha256"] == contract["runtime_sources_sha256"],
        "eligibility plan refers to different repaired runtime sources",
    )
    support = plan["support_sources_sha256"]
    expected_support = {path for path, _ in targets.values() if path.startswith("scripts/")}
    expected_support.update({"scripts/m1_path_inputs.py", "scripts/m1_path_native.py"})
    _keys(support, expected_support, "eligibility support source witnesses")
    for path, sha in support.items():
        _require(
            contract["preparation_sources_sha256"].get(path) == sha
            and freeze["source_files_sha256"].get(path) == sha,
            "eligibility support source is outside exact freeze",
        )
        _read_binding(root, {"path": path, "sha256": sha}, "eligibility support source")
    inputs = _keys(
        plan["inputs"],
        {"path", "sha256", "selected_indices", "selected_rows_sha256", "row_hash_encoding"},
        "eligibility inputs",
    )
    _require(
        {key: inputs[key] for key in ("path", "sha256")} == freeze["inputs"]
        and canonical(inputs["selected_indices"]) == canonical(list(range(67)))
        and inputs["row_hash_encoding"] == "exact_input_line_plus_LF",
        "eligibility exposure differs from first 67 unchanged input rows",
    )
    rows = _read_binding(root, freeze["inputs"], "eligibility input file").splitlines()
    _require(
        len(rows) == 68
        and inputs["selected_rows_sha256"] == [digest(row + b"\n") for row in rows[:67]],
        "eligibility selected literal row hashes differ",
    )
    _require(plan["teaching"] == freeze["teaching"], "eligibility teaching binding differs")
    evaluator = parse_json(
        _read_binding(root, plan["teaching"]["evaluator"], "eligibility evaluator")
    )
    _require(
        digest(canonical(teaching_schedule(evaluator))) == plan["teaching"]["subset_sha256"],
        "eligibility teaching receipts differ",
    )
    _require(
        canonical(plan["configuration"]) == canonical(freeze["configuration"]),
        "eligibility source configuration differs",
    )
    _require(
        canonical(profile["call_targets"]) == canonical(targets),
        "raw census requires the complete exact eligibility native call map",
    )
    caps = _keys(profile["call_caps"], set(success), "complete eligibility call/resource caps")
    _require(
        all(type(cap) is int and cap >= success[name] for name, cap in caps.items()),
        "eligibility caps cannot cover the required successful exposure",
    )
    return plan


def validate_census_evidence(root: Path, freeze: dict, contract: dict, census: dict) -> dict:
    """Check exact reviewed probe exposure and raw consistency, report unmet gates.

    This is a software consistency result only. In particular the guard's single
    allocation does not attest the uninstrumented weak registry object birth.
    Positive native eligibility is separately denied by admission while the fixed
    mandatory obligations remain unresolved. Conditional endpoint/concept coverage
    remains unobserved whenever that coverage is required by a later approval.
    """
    from scripts.m1_path_admission import _read_binding, _require, canonical, parse_json

    plan = _validate_eligibility_plan(root, freeze, contract, census)
    _validate_raw_census_evidence(root, freeze, contract, census)
    profile = census["profiler_evidence"]
    snapshot = parse_json(_read_binding(root, profile["snapshot"], "raw eligibility snapshot"))
    _require(
        canonical(snapshot["call_attempts"]) == canonical(plan["successful_calls"])
        and canonical(snapshot["call_returns"]) == canonical(plan["successful_calls"]),
        "raw attempts/normal returns do not equal exact successful eligibility call vector",
    )
    resources = Counter(
        (event["name"], *event["route"])
        for event in snapshot["events"]
        if event["kind"] == "call_attempt" and event["name"] in RESOURCE_ROUTES
    )
    _require(
        resources
        == Counter(
            {
                (name, path, qualname): count
                for name, path, qualname, count in RESOURCE_ROUTE_SUCCESS
            }
        ),
        "raw resource routes do not equal exact successful eligibility resource vector",
    )
    return {
        "status": "SOURCE_BOUND_CENSUS_SOFTWARE_VALIDATION_ONLY",
        "runtime_execution_authorized": False,
        "scientific_credit": 0,
        "mandatory_unmet_obligations": list(MANDATORY_UNMET),
        "conditional_unmet_coverage": list(CONDITIONAL_UNMET),
    }
