"""Verify the one pinned acquired-ownership archive without importing a model.

This checks saved artifact consistency, with live identity/transaction evidence supplied
by the reviewed frozen runner. JSON reference labels preserve observable alias shape;
they cannot independently prove live Python identities, execution or owner assignment.
Runtime source manifests bind reviewed code; the archive does not contain all runtime
source blobs. Native/output hashes are not ownership oracles. No dynamic reproduction,
universal deepcopy, checkpoint, M1, predictor/action-learning or scientific claim follows.
"""

from __future__ import annotations

import ast
import base64
import hashlib
import io
import itertools
import json
import math
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/v05_acquired_ownership_20261001"
ARCHIVE_SHA256 = "632088e5618a035aec5a6b2fb6ba7ab1dd34510de53bac3b17fd681546ce7e0b"
MANIFEST_SHA256 = "1643c08681d6ffd59aa839c05a28632770635fedd105e6b467aa9ed656243e95"
SOURCE = "6dd7e8a014d66232509355687b14579c03838962"
BEFORE_SHA256 = "e7d18fd8f59c399a8d3fb136e73f273220f8293625d8e463051f3b5cc019482d"
FROZEN = {
    "graph_schema.json": "af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69",
    "implementation_freeze.json": (
        "a1e405e6669d879d570d01d443e21df1c149a93f1c064790e15adae7462fe629"
    ),
    "protocol.json": "723859ed058957a4bf832ef09a8b42407e5fde3b0a5d8186de1edcd5f39c0a3f",
    "protocol.md": "d615192f97484ea61ccb96021b236b09fc1540f728e5f5c05c822b392b8509ff",
    "reuse_owned_probe.py": "4ac7f630a0f1094a0952df28b0ec3313ecd5ae885d9c4b1d135bea7904f13913",
    "reuse_paired_probe.py": "4b41b470bdf38ac2e7044f31345b6fc306bdb149a93c49316a926cdb3c78eeed",
    "runner.py": "d24730db318749deba4428ea7d26d283181bc3a91353d268eb2528f23db2bc7d",
    "tests.py": "af6b0f2bebc7314b90c2d4bb0d937bd02ea64d89650cbdf35f95afbf23b93f1c",
}
BRANCHES = ("export_abort", "event_cap_abort", "direct_reference", "commit")
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
COUNTS = {
    "aborted_transactions": 2,
    "expected_processing_exceptions": 1,
    "fresh_roots": 1,
    "native_loads": 0,
    "outcome_calls": 0,
    "owner_commits": 1,
    "process_attempts": 7,
    "process_returns": 6,
    "submitted_raw_pulses": 14,
    "whole_brain_copy_attempts": 4,
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _read_archive(compressed: bytes) -> dict[str, bytes]:
    """Read only safe regular tar members in memory; never extract or execute them."""
    members: dict[str, bytes] = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:xz") as archive:
        for item in archive:
            path = PurePosixPath(item.name)
            check(
                item.isfile()
                and not path.is_absolute()
                and ".." not in path.parts
                and str(path) == item.name
                and "\\" not in item.name,
                "unsafe archive member",
            )
            check(item.name not in members, "duplicate archive member")
            total += item.size
            check(0 <= item.size and total <= 32 * 1024**2, "oversize archive")
            stream = archive.extractfile(item)
            check(stream is not None, "unreadable archive member")
            members[item.name] = stream.read()
            check(len(members[item.name]) == item.size, "truncated archive member")
    return members


def _verify_manifests(members: dict[str, bytes], transport: dict[str, Any]) -> dict[str, Any]:
    check(len(members) == transport["archive_files"] == 169, "archive inventory mismatch")
    outer = json.loads(members["archive_manifest.json"])
    check(outer["schema"] == "v05-acquired-ownership-archive-1", "archive schema mismatch")
    check(outer["source_commit"] == transport["source_commit"] == SOURCE, "source mismatch")
    check(
        set(outer["files"]) == set(members) - {"archive_manifest.json"}, "outer inventory mismatch"
    )
    for name, expected in outer["files"].items():
        check(
            len(members[name]) == expected["bytes"] and sha(members[name]) == expected["sha256"],
            f"outer hash/size mismatch: {name}",
        )
    raw = {
        name.removeprefix("run/"): value
        for name, value in members.items()
        if name.startswith("run/")
    }
    check(len(raw) == transport["raw_files"] == 160, "raw file count mismatch")
    check(
        sum(map(len, raw.values())) == transport["raw_bytes"] == 5812592, "raw byte count mismatch"
    )
    check(sha(raw["manifest.json"]) == MANIFEST_SHA256, "original raw manifest mismatch")
    inner = json.loads(raw["manifest.json"])
    check(inner["manifest_excludes_itself"] is True, "manifest self-exclusion mismatch")
    check(set(inner["files"]) == set(raw) - {"manifest.json"}, "raw inventory mismatch")
    for name, expected in inner["files"].items():
        check(expected["complete_json"] is True, "incomplete raw JSON")
        check(
            len(raw[name]) == expected["bytes"] and sha(raw[name]) == expected["sha256"],
            f"raw hash/size mismatch: {name}",
        )
    return {name: json.loads(value) for name, value in raw.items()}


def _verify_bindings(members: dict[str, bytes], rows: dict[str, Any]) -> tuple[dict, dict]:
    check(
        {name for name in members if not name.startswith("run/")}
        == {"archive_manifest.json"} | {"freeze/" + name for name in FROZEN},
        "freeze inventory mismatch",
    )
    for name, digest in FROZEN.items():
        check(sha(members["freeze/" + name]) == digest, f"frozen binding mismatch: {name}")
    protocol, freeze, schema = (
        json.loads(members["freeze/" + name])
        for name in ("protocol.json", "implementation_freeze.json", "graph_schema.json")
    )
    preflight = rows["preflight.json"]
    for key, name in {
        "protocol_sha256": "protocol.json",
        "runner_sha256": "runner.py",
        "source_freeze_sha256": "implementation_freeze.json",
        "graph_schema_sha256": "graph_schema.json",
    }.items():
        check(preflight[key] == FROZEN[name], f"preflight binding mismatch: {key}")
    check(
        preflight["protocol"] == protocol and preflight["source_freeze"] == freeze,
        "preflight content mismatch",
    )
    check(
        freeze["protocol_sha256"] == FROZEN["protocol.json"]
        and freeze["graph_schema_sha256"]
        == protocol["graph_schema"]["sha256"]
        == FROZEN["graph_schema.json"],
        "protocol/schema binding mismatch",
    )
    implementation = {
        "scripts/v05_acquired_ownership_probe.py": FROZEN["runner.py"],
        "tests/test_v05_acquired_ownership_runner.py": FROZEN["tests.py"],
    }
    reuse = {
        "scripts/v05_owned_state_probe.py": FROZEN["reuse_owned_probe.py"],
        "scripts/v05_paired_coverage_probe.py": FROZEN["reuse_paired_probe.py"],
    }
    check(
        freeze["implementation_sources_sha256"] == implementation
        and freeze["reuse_sources_sha256"] == reuse,
        "implementation/reuse binding mismatch",
    )
    package = freeze["package_sources_sha256"]
    check(
        len(package) == 157
        and package == protocol["package_sources_sha256"]
        and protocol["source_pin"]
        == freeze["runtime_source_pin"]
        == "9549a2bf6bc76cb7b5714742f3ed54decd618263",
        "runtime manifest binding mismatch",
    )
    check(
        all(package.get(path) == record["sha256"] for path, record in schema["files"].items())
        and all(path in package for path in rows["imported-sources.json"].values()),
        "schema/import binding mismatch",
    )
    allowed = {
        path.removeprefix("src/").removesuffix(".py").replace("/", ".") + "." + name: record[
            "declared_fields"
        ]
        for path, source in schema["files"].items()
        for name, record in source["classes"].items()
    }
    check(
        len(allowed) == 50
        and all(
            not record["custom_copy_hooks"]
            for source in schema["files"].values()
            for record in source["classes"].values()
        ),
        "known-class schema mismatch",
    )
    return protocol, allowed


class SavedGraph:
    """Inspect saved node labels and values only; never instantiate runtime classes."""

    def __init__(self, graph: dict[str, Any], allowed: dict[str, list[str]]) -> None:
        check(
            set(graph) == {"complete", "format", "nodes", "root"}
            and graph["complete"] is True
            and graph["format"] == "typed-reference-graph-1",
            "incomplete/unknown graph",
        )
        self.graph, self.nodes = graph, graph["nodes"]
        check(type(self.nodes) is list and bool(self.nodes), "empty graph")
        visited: set[int] = set()

        def visit(token: Any, path: str) -> None:
            if type(token) is list:
                primitives = {
                    "NoneType": type(None),
                    "bool": bool,
                    "int": int,
                    "str": str,
                    "float": float,
                }
                check(
                    len(token) == 2
                    and token[0] in primitives
                    and type(token[1]) is primitives[token[0]],
                    "invalid typed primitive",
                )
                check(token[0] != "float" or math.isfinite(token[1]), "nonfinite primitive")
                return
            check(
                type(token) is dict
                and set(token) == {"ref"}
                and type(token["ref"]) is int
                and 0 <= token["ref"] < len(self.nodes),
                "invalid graph reference",
            )
            index = token["ref"]
            if index in visited:
                return
            check(index == len(visited), "noncanonical graph traversal order")
            visited.add(index)
            node = self.nodes[index]
            check(
                node["node"] == index and type(node["node"]) is int and node["path"] == path,
                "graph node/path mismatch",
            )
            kind = node["type"]
            keys = {"node", "path", "type"}
            if kind in ("dict", "list", "tuple", "set", "deque"):
                keys.add("items")
                check(type(node["items"]) is list, "invalid container items")
                if kind == "deque":
                    keys.add("maxlen")
                    limit = node["maxlen"]
                    check(
                        limit is None or type(limit) is int and limit >= len(node["items"]),
                        "invalid deque capacity",
                    )
                for i, item in enumerate(node["items"]):
                    if kind == "dict":
                        check(type(item) is list and len(item) == 2, "invalid dictionary pair")
                        visit(item[0], f"{path}.key[{i}]")
                        visit(item[1], f"{path}.value[{i}]")
                    else:
                        visit(item, f"{path}.set[{i}]" if kind == "set" else f"{path}[{i}]")
            else:
                keys |= {"fields", "observed_fields"}
                check(
                    kind in allowed
                    and node["observed_fields"] == sorted(allowed[kind])
                    and list(node["fields"]) == sorted(allowed[kind]),
                    "unknown class or missing/extra graph field",
                )
                for name, value in node["fields"].items():
                    visit(value, f"{path}.{name}")
            check(set(node) == keys, "unexpected graph node fields")

        root = graph["root"]
        check(root == {"ref": 0}, "invalid graph root")
        visit(root, self.nodes[0]["path"])
        check(len(visited) == len(self.nodes), "unreachable graph nodes")
        # Validate hashable dict keys and the frozen set domain without normalizing order.
        for node in self.nodes:
            if node["type"] == "dict":
                keys = [self.key(pair[0]) for pair in node["items"]]
                check(len(set(keys)) == len(keys), "duplicate dictionary key")
            if node["type"] == "set":
                items = [self.key(item) for item in node["items"]]
                check(
                    all(
                        type(v) in (int, str)
                        or type(v) is tuple
                        and len(v) == 2
                        and all(type(i) is int for i in v)
                        for v in items
                    ),
                    "invalid set member",
                )
                check(
                    len(set(items)) == len(items)
                    and items == sorted(items, key=lambda v: (type(v).__name__, canonical(v))),
                    "invalid set membership/order",
                )

    def key(self, token: Any) -> Any:
        if type(token) is list:
            return token[1]
        node = self.nodes[token["ref"]]
        check(node["type"] == "tuple", "unhashable graph key")
        return tuple(self.key(item) for item in node["items"])

    def value(self, token: Any) -> Any:
        """A value projection for comparison; identity comparisons always use references."""
        if type(token) is list:
            return token[1]
        node = self.nodes[token["ref"]]
        if "fields" in node:
            return {key: self.value(value) for key, value in node["fields"].items()}
        if node["type"] == "dict":
            return {self.key(key): self.value(value) for key, value in node["items"]}
        return [self.value(item) for item in node["items"]]

    def at(self, path: str) -> Any:
        def resolve(expr: ast.AST) -> Any:
            if isinstance(expr, ast.Name):
                check(expr.id == self.nodes[0]["path"], "wrong graph path root")
                return self.graph["root"]
            check(isinstance(expr, (ast.Attribute, ast.Subscript)), "unsupported graph path")
            parent = resolve(expr.value)
            node = self.nodes[parent["ref"]]
            if isinstance(expr, ast.Attribute):
                return node["fields"][expr.attr]
            key = ast.literal_eval(expr.slice)
            if node["type"] == "dict":
                return next(value for item, value in node["items"] if self.key(item) == key)
            check(type(key) is int and key >= 0, "invalid sequence path")
            return node["items"][key]

        return resolve(ast.parse(path, mode="eval").body)

    def get(self, path: str) -> Any:
        return self.value(self.at(path))

    def items(self, path: str) -> list[Any]:
        return self.nodes[self.at(path)["ref"]]["items"]


def _verify_graphs(rows: dict[str, Any], allowed: dict[str, list[str]]) -> dict[str, SavedGraph]:
    inventories = {
        name: SavedGraph(row, allowed) for name, row in rows.items() if name.startswith("graph-")
    }
    check(len(inventories) == 17, "graph inventory count mismatch")
    for name, graph in inventories.items():
        check(name == "graph-" + sha(canonical(graph.graph)) + ".json", "graph digest mismatch")
    pointers = {}
    for name, pointer in rows.items():
        if not name.endswith("-graph.json"):
            continue
        graph = inventories[pointer["inventory_file"]]
        digest = sha(canonical(graph.graph))
        check(
            pointer
            == {
                "inventory_file": "graph-" + digest + ".json",
                "inventory_sha256": digest,
                "node_count": len(graph.nodes),
                "mutable_identity_count": sum(n["type"] != "tuple" for n in graph.nodes),
                "oracle": "exact complete typed/reference bytes; hashes only address stored bytes",
            },
            "graph pointer mismatch",
        )
        pointers[name.removesuffix("-graph.json")] = graph
    check(
        {id(g) for g in pointers.values()} == {id(g) for g in inventories.values()},
        "unreferenced graph inventory",
    )
    return pointers


def _clocks(graph: SavedGraph) -> dict[str, Any]:
    get = graph.get
    field = "brain.base.field."
    queue = get(field + "_queue")
    return {
        "field_end_ms": get(field + "current_time_ms"),
        "receptor_Q": get("brain.receptors.channels").get("Q"),
        "unit_clocks": [
            {
                key: unit[key]
                for key in ("unit_id", "last_update_ms", "last_spike_ms", "refractory_until_ms")
            }
            for unit in get(field + "units").values()
        ],
        "candidate_clocks": [
            {key: candidate[key] for key in ("assembly_id", "first_seen_ms", "last_seen_ms")}
            for candidate in get("brain.assemblies.candidates").values()
        ],
        "queue_heap_layout": [{"time_ms": t, "counter": c, "arrival": a} for t, c, a in queue],
        "queue_counter": get(field + "_counter"),
        **{
            key: get(field + key)
            for key in ("total_arrivals", "last_run_arrivals", "total_spikes", "last_run_spikes")
        },
    }


def _verify_observation(graph: SavedGraph, observation: dict[str, Any]) -> None:
    check(
        observation["clocks_and_processing"] == _clocks(graph), "graph/clock observation mismatch"
    )
    candidates = graph.get("brain.assemblies.candidates")
    check(
        observation["candidate_episode_sets"]
        == {key: sorted(row["episode_ids"]) for key, row in candidates.items()},
        "candidate observation mismatch",
    )
    witness = observation["identity"]
    check(
        witness["basis"] == "Live `is` checks, supported by full typed/reference inventories",
        "identity witness basis mismatch",
    )
    results = graph.items("brain.results")
    base_results = graph.items("brain.base.results")

    def matches(token: Any, attribute: str) -> list[str]:
        return [
            f"brain.results[{i}].{attribute}[{j}]"
            for i in range(len(results))
            for j, item in enumerate(graph.items(f"brain.results[{i}].{attribute}"))
            if item == token
        ]

    expected_prototypes = {
        key: {
            "source": f"brain.assemblies.candidates[{key!r}].prototype",
            "retained_paths": matches(
                graph.at(f"brain.assemblies.candidates[{key!r}].prototype"), "patterns"
            ),
        }
        for key in candidates
    }
    check(
        witness["candidate_prototypes"] == expected_prototypes
        and all(row["retained_paths"] for row in expected_prototypes.values()),
        "candidate prototype alias mismatch",
    )
    pending = graph.at("brain.pending_activation")
    check(
        witness["pending_activation_paths"] == matches(pending, "assembly_activations")
        and witness["pending_action_paths"]
        == [
            f"brain.results[{i}].action"
            for i in range(len(results))
            if graph.at(f"brain.results[{i}].action") == graph.at("brain.pending_action")
        ],
        "pending alias mismatch",
    )
    check(
        witness["v04_result_links"]
        == [
            {
                "source": f"brain.results[{i}].v04_result",
                "retained_paths": [
                    f"brain.base.results[{j}]"
                    for j, token in enumerate(base_results)
                    if token == graph.at(f"brain.results[{i}].v04_result")
                ],
            }
            for i in range(len(results))
        ]
        and len(base_results) == len(results)
        and all(
            graph.at(f"brain.results[{i}].v04_result") == base_results[i]
            for i in range(len(results))
        ),
        "retained result alias mismatch",
    )
    for section, attribute, sources in (
        (
            "emitted_input_links",
            "input_pulses",
            [
                f"brain.results[{i}].emitted_pulses[{j}]"
                for i in range(len(results))
                for j in range(len(graph.items(f"brain.results[{i}].emitted_pulses")))
            ],
        ),
        (
            "buffered_spike_links",
            "spikes",
            [
                f"brain.base.{component}[{i}]"
                for component in ("burst_detector._window", "cascade_tracker._pending")
                for i in range(len(graph.items("brain.base." + component)))
            ],
        ),
    ):
        expected = [
            {
                "source": source,
                "retained_paths": [
                    f"brain.base.results[{i}].{attribute}[{j}]"
                    for i in range(len(base_results))
                    for j, token in enumerate(graph.items(f"brain.base.results[{i}].{attribute}"))
                    if token == graph.at(source)
                ],
            }
            for source in sources
        ]
        check(witness[section] == expected, "input/buffer alias mismatch")
        if section == "emitted_input_links":
            check(all(row["retained_paths"] for row in expected), "missing emitted input alias")
    edges = []
    for key, token in graph.items("brain.base.field.connections"):
        source, target = graph.key(key)
        edges.append(
            {
                "connection_key": [source, target],
                **{
                    direction + "_paths": [
                        f"brain.base.field.{direction}[{unit}][{i}]"
                        for i, item in enumerate(
                            graph.items(f"brain.base.field.{direction}[{unit}]")
                        )
                        if item == token
                    ]
                    for direction, unit in (("outgoing", source), ("incoming", target))
                },
            }
        )
    check(
        witness["connection_links"] == edges
        and all(row["incoming_paths"] and row["outgoing_paths"] for row in edges),
        "connection adjacency alias mismatch",
    )
    memory = witness["cascade_memory_link"]
    check(
        memory
        == {
            "source": "brain.base.cascade_tracker.memory",
            "target": "brain.base.assembly_memory",
            "same_object": True,
        }
        and graph.at(memory["source"]) == graph.at(memory["target"]),
        "memory alias mismatch",
    )
    for kind in ("unit", "connection"):
        expected = []
        for i, token in enumerate(graph.items(f"brain.base._topology.{kind}s")):
            value = graph.value(token)
            initial = f"brain.base._topology.{kind}s[{i}]"
            key = value["unit_id"] if kind == "unit" else (value["source_id"], value["target_id"])
            live = f"brain.base.field.{kind}s[{key!r}]"
            row = {"initial_path": initial, "separate": graph.at(initial) != graph.at(live)}
            row.update({"live_path": live} if kind == "unit" else {"live_key": list(key)})
            expected.append(row)
        check(
            witness[f"topology_{kind}_separation"] == expected
            and all(row["separate"] for row in expected),
            "initial/live topology alias mismatch",
        )


def _verify_maturity(graph: SavedGraph, gate: dict[str, Any], ids: list[str]) -> None:
    pending = graph.get("brain.pending_activation")
    candidates = graph.get("brain.assemblies.candidates")
    check(
        type(pending) is dict
        and pending["mature"] is True
        and pending["suppressed"] is False
        and set(candidates) == {pending["assembly_id"]},
        "actual mature pending absent",
    )
    key = pending["assembly_id"]
    candidate = candidates[key]
    check(
        set(candidate["episode_ids"]) == set(ids)
        and candidate["assembly_id"] == key
        and candidate["occurrences"] == len(ids)
        and pending["occurrences"] == len(ids)
        and pending["episode_count"] == len(ids)
        and [r["metadata"]["episode_id"] for r in graph.get("brain.results")] == ids
        and not graph.get("brain.assemblies.suppressed")
        and not graph.get("brain.suppressed_unit_ids"),
        "actual maturity episode mismatch",
    )
    paths = [
        f"brain.results[{i}].assembly_activations[{j}]"
        for i in range(len(ids))
        for j, token in enumerate(graph.items(f"brain.results[{i}].assembly_activations"))
        if token == graph.at("brain.pending_activation")
    ]
    prototype = {
        "source": f"brain.assemblies.candidates[{key!r}].prototype",
        "retained_paths": [
            f"brain.results[{i}].patterns[{j}]"
            for i in range(len(ids))
            for j, token in enumerate(graph.items(f"brain.results[{i}].patterns"))
            if token == graph.at(f"brain.assemblies.candidates[{key!r}].prototype")
        ],
    }
    check(
        paths == [f"brain.results[{len(ids) - 1}].assembly_activations[0]"]
        and prototype["retained_paths"],
        "maturity reference alias mismatch",
    )
    check(
        gate
        == {
            "covered": True,
            "expected_episode_ids": ids,
            "pending_activation_paths": paths,
            "candidate_prototype": prototype,
            "checks": dict.fromkeys(
                (
                    "exact_retained_episodes",
                    "actual_mature_unsuppressed_pending",
                    "exact_candidate_episode_set",
                    "pending_in_newest_result",
                    "prototype_in_retained_result",
                    "no_suppression",
                ),
                True,
            ),
        },
        "maturity gate mismatch",
    )


def _mutable_paths(value: Any, path: str = "export") -> list[str]:
    if type(value) is dict:
        return [path] + [
            child for key, item in value.items() for child in _mutable_paths(item, f"{path}.{key}")
        ]
    if type(value) is list:
        return [path] + [
            child for i, item in enumerate(value) for child in _mutable_paths(item, f"{path}[{i}]")
        ]
    check(value is None or type(value) in (bool, int, float, str), "nonprimitive export")
    return []


def _verify_raw(
    rows: dict[str, Any], protocol: dict[str, Any], graphs: dict[str, SavedGraph]
) -> dict[str, Any]:
    def data(label: str) -> bytes:
        return canonical(graphs[label].graph)

    before = data("acquired-beforestate")
    check(sha(before) == BEFORE_SHA256, "original acquired graph mismatch")
    for name, observation in rows.items():
        if name.endswith("-observations.json"):
            _verify_observation(graphs[name.removesuffix("-observations.json")], observation)
    fresh = graphs["fresh-root"]
    check(
        not fresh.get("brain.results")
        and not fresh.get("brain.base.results")
        and not fresh.get("brain.assemblies.candidates")
        and fresh.get("brain.pending_activation") is None
        and fresh.get("brain.base.field.current_time_ms") == 0.0,
        "nonfresh initial root",
    )
    configs = {name: fresh.get("brain." + path) for name, path in CONFIG_PATHS.items()}
    check(
        configs == rows["actual-twelve-constructor-configs.json"] == protocol["configuration"],
        "constructor configuration mismatch",
    )
    check(rows["constructor-attempt.json"]["attempt"] == 1, "constructor count mismatch")
    counts = dict.fromkeys(COUNTS, 0)
    counts["fresh_roots"] = 1
    ids = [f"acquired-ownership-20261001-{i:02}" for i in range(1, 5)]
    episodes = [
        {
            "episode_id": ids[i],
            "pulses": [
                {
                    "channel": "Q",
                    "location": None,
                    "magnitude": 1.2,
                    "metadata": {},
                    "novelty": 0.0,
                    "polarity": 1,
                    "prediction_error": 0.0,
                    "source_id": "acquired-ownership-probe",
                    "time_ms": t,
                }
                for t in (8.0 + 200 * i, 12.0 + 200 * i)
            ],
        }
        for i in range(4)
    ]
    check(
        protocol["prefix"] == episodes[:3]
        and protocol["suffix"] == episodes[3]
        and [row["name"] for row in protocol["branches"]] == list(BRANCHES),
        "fixed inputs/branch order mismatch",
    )
    flags = {"explore_action": False, "learn_assembly": True, "learn_field": True, "metadata": {}}
    check(protocol["process_episode_flags"] == flags, "process flags mismatch")

    def attempt(label: str, index: int) -> None:
        row = rows[label + "-attempt.json"]
        check(
            row["counts_before"] == counts
            and row["episode"] == episodes[index]
            and row["flags"] == flags,
            "call accounting/input mismatch",
        )
        check(
            graphs[label + "-caller"].get("caller") == episodes[index]["pulses"]
            and data(label + "-caller") == data(label + "-detached-input")
            and rows[label + "-input-detachment.json"]
            == {"complete_typed_bytes_equal": True, "shared_mutable_paths": []},
            "input detachment mismatch",
        )
        counts["process_attempts"] += 1
        counts["submitted_raw_pulses"] += 2
        if label == "event_cap_abort":
            return
        counts["process_returns"] += 1
        graph = graphs[label + "-after-return"]
        result = graphs[label + "-raw-return"].get("result")
        check(
            result == graph.get(f"brain.results[{index}]")
            and len(graph.items("brain.results")) == index + 1
            and graph.get("brain._episode_index") == index + 1
            and result["raw_pulses"] == episodes[index]["pulses"],
            "raw return mismatch",
        )
        clock = rows[label + "-clock-gate.json"]
        observed = _clocks(graph)
        end = 44.0 + 200 * index
        check(
            clock
            == {
                "actual_field_end_ms": end,
                "expected_field_end_ms": end,
                "expected_receptor_Q_last_ms": end - 32.0,
                "actual_receptor_Q": observed["receptor_Q"],
            }
            and observed["field_end_ms"] == end
            and observed["receptor_Q"]["last_time_ms"] == end - 32.0,
            "successful clock mismatch",
        )

    for i in range(3):
        attempt(f"prefix-{i + 1}", i)
    first = graphs["prefix-1-after-return"]
    check(
        first.get("brain.pending_activation") is None
        and all(
            len(c["episode_ids"]) < 3 for c in first.get("brain.assemblies.candidates").values()
        )
        and all(a["mature"] is False for a in first.get("brain.results[0].assembly_activations"))
        and rows["prefix-1-immaturity-gate.json"]
        == dict.fromkeys(("pending_null", "no_mature_candidates", "no_mature_activations"), True),
        "first immaturity mismatch",
    )
    check(data("prefix-3-after-return") == before, "acquired prefix mismatch")
    _verify_maturity(
        graphs["acquired-beforestate"], rows["acquired-prefix-maturity-gate.json"], ids[:3]
    )
    for branch in BRANCHES:
        label = "copy-" + branch
        check(rows[label + "-attempt.json"]["counts_before"] == counts, "copy accounting mismatch")
        counts["whole_brain_copy_attempts"] += 1
        check(
            data(label) == before
            and rows[label + "-equality.json"]
            == {
                "before_inventory": BEFORE_SHA256,
                "copy_inventory": BEFORE_SHA256,
                "complete_typed_bytes_equal": True,
            },
            "copy equality mismatch",
        )
    for name, row in rows.items():
        if name.endswith("-original-equality.json"):
            check(
                data(name.removesuffix("-equality.json")) == before
                and row
                == {
                    "before_inventory": BEFORE_SHA256,
                    "current_inventory": BEFORE_SHA256,
                    "exact_typed_bytes_equal": True,
                    "owner_is_original_root": True,
                },
                "original/owner equality mismatch",
            )
    names = ("root",) + BRANCHES
    check(
        all(data("pairwise-" + name) == before for name in names)
        and rows["pairwise-mutable-isolation.json"]
        == [
            {"left": left, "right": right, "shared_mutable_paths": []}
            for left, right in itertools.combinations(names, 2)
        ],
        "pairwise isolation mismatch",
    )

    for branch in BRANCHES:
        attempt(branch, 3)
        if branch == "event_cap_abort":
            counts["expected_processing_exceptions"] += 1
            counts["aborted_transactions"] += 1
        else:
            graph = graphs[branch + "-after-return"]
            _verify_maturity(graph, rows[branch + "-maturity-gate.json"], ids)
            check(
                data(branch + "-after-export") == data(branch + "-after-return") != before,
                "advanced/export graph mismatch",
            )
            output = rows[branch + "-export.json"]
            check(
                output
                == rows[branch + "-raw-values.json"]
                == graphs[branch + "-raw-return"].get("result"),
                "detached output mismatch",
            )
            check(
                rows[branch + "-export-isolation.json"]
                == {
                    "mutable_export_paths": _mutable_paths(output),
                    "shared_mutable_export_paths": [],
                    "source": "src/sparkbrain/v05/contracts.py:114-129; JSON detached tree",
                },
                "export isolation mismatch",
            )
            if branch == "export_abort":
                counts["aborted_transactions"] += 1
    counts["owner_commits"] += 1
    _verify_fault(rows, graphs)
    error = rows["export_abort-injected-error.json"]
    check(
        error["type"] == "InjectedExportValidationError"
        and error["message"] == "acquired-ownership-export-boundary-20261001",
        "export injected error mismatch",
    )
    check(
        rows["export-injection-boundary.json"]
        == {
            "fault": "InjectedExportValidationError",
            "commit_count": 0,
            "placement": "after processing, raw/graph/output preservation and validation",
            "complete_advanced_graph": sha(data("export_abort-after-return")),
        },
        "export fault boundary mismatch",
    )
    commit = data("commit-after-return")
    check(
        commit == data("direct_reference-after-return") == data("export_abort-after-return")
        and rows["commit-export.json"]
        == rows["direct_reference-export.json"]
        == rows["export_abort-export.json"]
        and rows["precommit-direct-equality.json"]
        == {
            "checks": dict.fromkeys(
                (
                    "candidate_advanced",
                    "complete_detached_output_equal",
                    "complete_typed_graph_bytes_equal",
                ),
                True,
            ),
            "commit_graph": sha(commit),
            "direct_graph": sha(commit),
            "owner_commits_before": 0,
        },
        "direct/commit equality mismatch",
    )
    _verify_mutations(rows, graphs)
    check(
        data("postreturn-committed") == commit and data("postreturn-old-root") == before,
        "postreturn graph mutation leaked",
    )
    terminal = rows["terminal.json"]
    check(
        counts == COUNTS == terminal["counts"]
        and terminal["constructor_attempts"] == 1
        and terminal["status"] == "restricted_acquired_ownership_observed"
        and terminal["successful_owner_return_observed"] is True,
        "terminal accounting mismatch",
    )
    check(
        terminal["scientific_credit"] == protocol["scientific_credit"] == 0
        and terminal["classification"]
        == protocol["classification"]
        == "EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY"
        and terminal["native_output_hashes_are_ownership_oracles"] is False
        and terminal["no_retry"] is True,
        "claim boundary mismatch",
    )
    return {
        "status": "verified_fixed_acquired_ownership",
        "archive_files": 169,
        "raw_files": 160,
        "complete_graphs": 17,
        "counts": counts,
        "mature_prefix_episodes": 3,
        "mature_suffix_episodes": 4,
        "external_metadata_changes": 9,
        "scientific_credit": 0,
        "model_execution": False,
        "identity_basis": "reviewed live identity checks; saved reference/alias consistency only",
        "limits": "No dynamic reproduction, universal deepcopy/checkpoint, M1, "
        "or predictor/action guarantee",
    }


def _verify_fault(rows: dict[str, Any], graphs: dict[str, SavedGraph]) -> None:
    exact, configured, failed = (
        graphs[label]
        for label in (
            "event-cap-exact-copy",
            "event-cap-after-config",
            "event-cap-final-failed-state",
        )
    )
    check(
        canonical(exact.graph) == canonical(graphs["acquired-beforestate"].graph)
        and canonical(configured.graph)
        != canonical(failed.graph)
        == canonical(graphs["event_cap_abort-after-processing-error"].graph),
        "fault graph mutation missing",
    )
    before_config = exact.get("brain.base.field.config")
    after_config = configured.get("brain.base.field.config")
    check(
        after_config == dict(before_config, max_events_per_run=1)
        and rows["event-cap-config-change.json"]
        == {"before": before_config, "after": after_config},
        "fault configuration mismatch",
    )
    # In this fixed archive the replacement has the same traversal/alias shape. Require
    # the cap value to be the only changed token in the complete after-config inventory.
    expected_configured = json.loads(canonical(exact.graph))
    config_node = exact.at("brain.base.field.config")["ref"]
    expected_configured["nodes"][config_node]["fields"]["max_events_per_run"] = ["int", 1]
    check(expected_configured == configured.graph, "mutation beyond fault config replacement")
    before, after = _clocks(configured), _clocks(failed)
    check(
        before["receptor_Q"]["observations"] == 6
        and after["receptor_Q"]["observations"] == 8
        and before["receptor_Q"]["last_time_ms"] == 412.0
        and after["receptor_Q"]["last_time_ms"] == 612.0
        and before["total_arrivals"] == 150
        and after["total_arrivals"] == 152
        and after["last_run_arrivals"] == 2
        and before["field_end_ms"] == after["field_end_ms"] == 444.0
        and before["total_spikes"] == after["total_spikes"] == 30
        and after["last_run_spikes"] == 0
        and before["queue_counter"] == 150
        and after["queue_counter"] == 154
        and before["queue_heap_layout"] == []
        and [
            (row["time_ms"], row["counter"], row["arrival"]["time_ms"], row["arrival"]["target_id"])
            for row in after["queue_heap_layout"]
        ]
        == [(612.0, 153, 612.0, 0), (612.0, 154, 612.0, 1)],
        "actual processing mutation mismatch",
    )
    gate = rows["event-cap-genuine-fault-gate.json"]
    check(
        gate["before_processing"] == before
        and gate["after_error"] == after
        and gate["exact_clone_inventory"] == sha(canonical(exact.graph))
        and gate["after_config_inventory"] == sha(canonical(configured.graph))
        and gate["failed_inventory"] == sha(canonical(failed.graph))
        and gate["checks"]
        == dict.fromkeys(
            (
                "Q_last_time_612",
                "Q_two_observations",
                "arrival_scheduling_advanced",
                "changed_beyond_config",
                "queue_changed",
                "two_actual_arrival_pops",
            ),
            True,
        ),
        "fault mutation gate mismatch",
    )
    error = rows["event_cap_abort-processing-error.json"]
    check(
        error["type"] == "RuntimeError"
        and error["message"] == "max_events_per_run exceeded"
        and 'raise RuntimeError("max_events_per_run exceeded")' in error["traceback"]
        and "src/sparkbrain/v04/field.py" in error["traceback"],
        "genuine processing error mismatch",
    )


def _verify_mutations(rows: dict[str, Any], graphs: dict[str, SavedGraph]) -> None:
    before, after = (rows[f"postreturn-control-{part}.json"] for part in ("before", "after"))
    check(
        before["export"] == rows["commit-export.json"]
        and before["caller_pulses"] == graphs["commit-caller"].get("caller")
        and after["caller_pulses"] == graphs["postreturn-mutated-callers"].get("caller")
        and after["export"] == graphs["postreturn-mutated-export"].get("export"),
        "external control graph mismatch",
    )

    def targets(control: dict) -> list[tuple[str, dict]]:
        output = control["export"]
        return (
            [
                (f"caller[{i}].metadata", p["metadata"])
                for i, p in enumerate(control["caller_pulses"])
            ]
            + [("export.metadata", output["metadata"])]
            + [
                (f"export.{section}[{i}].metadata", p["metadata"])
                for section in ("raw_pulses", "emitted_pulses")
                for i, p in enumerate(output[section])
            ]
            + [
                (f"export.v04_result.input_pulses[{i}].metadata", p["metadata"])
                for i, p in enumerate(output["v04_result"]["input_pulses"])
            ]
        )

    old, new = targets(before), targets(after)
    check(
        len(old) == len(new) == 9
        and before["targets"] == [{"path": path, "value": value} for path, value in old],
        "external mutation target mismatch",
    )
    expected_after = json.loads(
        canonical({key: before[key] for key in ("caller_pulses", "export")})
    )
    for _, metadata in targets(expected_after):
        metadata.update(after_return={"owned_probe": [1, 2, 3]})
    check(after == expected_after, "unrequested external control mutation")
    changes = []
    for (path, previous), (new_path, current) in zip(old, new, strict=True):
        check(
            path == new_path
            and current == dict(previous, after_return={"owned_probe": [1, 2, 3]})
            and canonical(previous) != canonical(current),
            "external metadata mutation absent",
        )
        changes.append(
            {
                "path": path,
                "before_bytes": canonical(previous).decode(),
                "after_bytes": canonical(current).decode(),
                "changed": True,
            }
        )
    check(
        rows["postreturn-control-changes.json"] == changes
        and rows["postreturn-isolation-gate.json"]
        == dict.fromkeys(
            (
                "committed_graph_exact",
                "every_target_changed",
                "old_root_graph_exact",
                "owner_is_commit_candidate",
            ),
            True,
        ),
        "postreturn mutation/isolation gate mismatch",
    )


def verify(directory: Path = ARTIFACT) -> dict[str, Any]:
    """Verify only the pinned original archive; no override can admit a replacement run."""
    transport = json.loads((directory / "transport_manifest.json").read_bytes())
    check(
        transport["schema"] == "v05-acquired-ownership-transport-1"
        and transport["encoding"] == "base64-then-xz-tar",
        "transport schema mismatch",
    )
    check(
        [part["path"] for part in transport["parts"]]
        == [f"evidence-{i:03d}.b64" for i in range(4)],
        "unexpected transport parts",
    )
    encoded = []
    for part in transport["parts"]:
        raw = (directory / part["path"]).read_bytes()
        check(len(raw) == part["bytes"] and sha(raw) == part["sha256"], "part hash/size mismatch")
        encoded.append(b"".join(raw.splitlines()))
    compressed = base64.b64decode(b"".join(encoded), validate=True)
    check(
        sha(compressed) == ARCHIVE_SHA256 == transport["archive_sha256"],
        "original archive binding mismatch",
    )
    check(len(compressed) == transport["archive_bytes"] == 136964, "archive size mismatch")
    check(transport["model_execution_for_packaging"] is False, "packaging boundary mismatch")
    members = _read_archive(compressed)
    rows = _verify_manifests(members, transport)
    protocol, allowed = _verify_bindings(members, rows)
    return _verify_raw(rows, protocol, _verify_graphs(rows, allowed))


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
