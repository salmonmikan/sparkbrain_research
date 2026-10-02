"""Verify the ONE pinned history-export archive using saved data and stdlib only.

SavedGraph is source-adapted from verify_v05_acquired_ownership_evidence.py.
Native similarity arithmetic and input/raster recipes are source-adapted from the
pinned assemblies.py / PR169 / PR182 sources, operating only on primitive values.
No model or probe import, checkpoint restore, dynamic reproduction or archive
extraction occurs. Archived Python is inert bytes. Full graph labels preserve
saved alias shape; live `is`, execution, fresh memos, ownership and limit enforcement
remain source-backed recorded claims, not independently observed live facts.

This checks a fixed inherited fixture's representation prerequisite only. Native
L2 and raw410 L1 are different metrics; neither establishes an assembly advantage,
M1 contribution, learned benefit, joint atomicity, novelty or scientific evidence.
"""

from __future__ import annotations

import ast
import base64
import hashlib
import io
import itertools
import json
import math
import random
import tarfile
from collections.abc import Iterable
from decimal import ROUND_HALF_EVEN, Context, Decimal
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/v05_history_export_20261002"
TRANSPORT_SHA256 = "9824a11334e8516634017ddff603452e8e259bb61a40d0f6d89307554eb3c6c3"
ARCHIVE_SHA256 = "c9f929895b8a9011a9540359d80a87e9241da6914ac027469072a6b597c23bb5"
MANIFEST_SHA256 = "01fa163844cd373d355030cad63ce0f1bc495d78004fb183929575bb9a556194"
SOURCE = "1d5b6de3b99f7eded5ced4f1c11bbc96393129e6"
RUNTIME_SOURCE = "9b1179aa18060436e4a05f2ff21f4cffc098f79d"
SEEDS = (910071, 910072)
BRANCHES = ("A", "B", "A_repeat", "B_repeat")
CHANNELS = list("ACFHIJKLMQ")
CANONICAL_FIELDS = ("ordered_units", "relative_bins", "unit_ids", "spike_count", "source_kind")
PROJECTION_VERSION = "native-strongest-canonical-mature-1"
COUNTS = {
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
LIMITS = {
    "address_space_bytes": 536870912,
    "artifact_bytes": 100663296,
    "cpu_seconds": 120,
    "wall_seconds": 180,
}
RESERVE = {
    "cpu_seconds": 3,
    "wall_seconds": 10,
    "artifact_bytes": 4194304,
    "address_space_bytes": 2097152,
}
FROZEN = {
    "graph_schema.json": "af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69",
    "implementation_freeze.json": (
        "2b49e5025259cde2a421fe2257b50927413bac00e655dc0431b6589c3e482222"
    ),
    "inputs.jsonl": "69a25de3c3aef84743d45494a1193df0eac695b4d0c8a0beb8f07fad5129ee39",
    "interface_design.md": "5037c313204d34153cbb016bf0141ebc00b2e9855a6543263a4e59e178dd1a46",
    "protocol.json": "48b2925fac2fb56200e59a9fb88df60c18868d5553e4390fe6c47864b6ac9c82",
    "protocol.md": "d0e3e9e30d5c11bc95aada3d69e7ca9f761b7031a28a8303fffca8abd1ef30e6",
    "reuse_acquired_probe.py": "d24730db318749deba4428ea7d26d283181bc3a91353d268eb2528f23db2bc7d",
    "reuse_temporal_contract.md": (
        "83fe87ded3ac1b2797d46f64070f0197ef37db953d202099dcdefd4aca243f15"
    ),
    "reuse_temporal_probe.py": "28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae",
    "runner.py": "1035374574a1528f76d8b6e7aefafb80265b37414322f6d3b675aafc045e671a",
    "tests.py": "b4ec360d73193c13a12c9cdbe7fb72a0cae0cb2cfef5b6624be59873dba05262",
}
FREEZE_PATHS = {
    "graph_schema.json": "artifacts/research/v05_owned_state_20261001/source_map.json",
    "implementation_freeze.json": (
        "artifacts/research/v05_history_export_20261002/implementation_freeze.json"
    ),
    "inputs.jsonl": "artifacts/research/v05_history_export_20261002/inputs.jsonl",
    "interface_design.md": "docs/research/assembly_m1_interface_design_20261001.md",
    "protocol.json": "artifacts/research/v05_history_export_20261002/protocol.json",
    "protocol.md": "docs/research/v05_history_export_protocol_20261002.md",
    "reuse_acquired_probe.py": "scripts/v05_acquired_ownership_probe.py",
    "reuse_temporal_contract.md": "docs/research/temporal_reuse_loop_contract_20261001.md",
    "reuse_temporal_probe.py": "scripts/temporal_reuse_loop_probe.py",
    "runner.py": "scripts/v05_history_export_probe.py",
    "tests.py": "tests/test_v05_history_export_runner.py",
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


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = dict(items)
        check(len(result) == len(items), "duplicate JSON key")
        return result

    def invalid(value: str) -> None:
        raise ValueError(f"nonfinite JSON: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


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
        self._paths: dict[str, Any] = {}
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

        if path not in self._paths:
            self._paths[path] = resolve(ast.parse(path, mode="eval").body)
        return self._paths[path]

    def get(self, path: str) -> Any:
        return self.value(self.at(path))

    def items(self, path: str) -> list[Any]:
        return self.nodes[self.at(path)["ref"]]["items"]

    def subtree(self, path: str, root: str) -> dict[str, Any]:
        """Readdress a saved subgraph, retaining every type, order and reference alias."""
        nodes: list[dict[str, Any]] = []
        seen: dict[int, int] = {}

        def visit(token: Any, name: str) -> Any:
            if isinstance(token, list):
                return token
            original = token["ref"]
            if original in seen:
                return {"ref": seen[original]}
            index = seen[original] = len(nodes)
            source = self.nodes[original]
            node = dict(source, node=index, path=name)
            nodes.append(node)
            if "fields" in source:
                node["fields"] = {
                    key: visit(value, name + "." + key) for key, value in source["fields"].items()
                }
            elif source["type"] == "dict":
                node["items"] = [
                    [visit(key, f"{name}.key[{i}]"), visit(value, f"{name}.value[{i}]")]
                    for i, (key, value) in enumerate(source["items"])
                ]
            else:
                node["items"] = [
                    visit(value, f"{name}.set[{i}]" if source["type"] == "set" else f"{name}[{i}]")
                    for i, value in enumerate(source["items"])
                ]
            return {"ref": index}

        token = visit(self.at(path), root)
        return {
            "complete": True,
            "format": "typed-reference-graph-1",
            "nodes": nodes,
            "root": token,
        }


def _read_archive(compressed: bytes) -> dict[str, bytes]:
    """Bounded regular-file reader. Production checks the archive pin before this call."""
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
            check(
                0 <= item.size <= 8 * 1024**2 and total <= 52 * 1024**2 and len(members) < 1868,
                "oversize archive",
            )
            check(
                item.uid == item.gid == item.mtime == 0 and item.mode == 0o644,
                "archive metadata mismatch",
            )
            stream = archive.extractfile(item)
            check(stream is not None, "unreadable archive member")
            members[item.name] = stream.read(item.size + 1)
            check(len(members[item.name]) == item.size, "truncated archive member")
    check(list(members) == sorted(members), "archive ordering mismatch")
    return members


def _load_transport(artifact: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    def read_bounded(path: Path, limit: int) -> bytes:
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
        check(len(data) <= limit, "oversize transport file")
        return data

    raw = read_bounded(artifact / "transport_manifest.json", 16384)
    check(sha(raw) == TRANSPORT_SHA256, "original transport manifest mismatch")
    transport = read_json(raw)
    check(
        transport["schema"] == "v05-history-export-transport-1"
        and transport["archive_sha256"] == ARCHIVE_SHA256
        and transport["source_commit"] == SOURCE,
        "original archive binding mismatch",
    )
    parts = transport["parts"]
    check(
        [p["path"] for p in parts] == [f"evidence-{i:03d}.b64" for i in range(36)],
        "transport parts mismatch",
    )
    encoded = []
    for part in parts:
        content = read_bounded(artifact / part["path"], part["bytes"])
        check(
            len(content) == part["bytes"] and sha(content) == part["sha256"],
            "transport part hash/size mismatch",
        )
        encoded.append(b"".join(content.split()))
    compressed = base64.b64decode(b"".join(encoded), validate=True)
    check(
        len(compressed) == transport["archive_bytes"] == 1282948
        and sha(compressed) == ARCHIVE_SHA256,
        "original archive hash/size mismatch",
    )
    return _read_archive(compressed), transport


def _verify_manifests(members: dict[str, bytes], transport: dict[str, Any]) -> dict[str, Any]:
    check(len(members) == transport["archive_files"] == 1868, "archive inventory mismatch")
    outer = read_json(members["archive_manifest.json"])
    check(
        outer["schema"] == "v05-history-export-archive-1"
        and outer["source_commit"] == SOURCE
        and outer["manifest_excludes_itself"] is True
        and outer["raw_files"] == 1856
        and outer["freeze_source_paths"] == FREEZE_PATHS,
        "outer archive binding mismatch",
    )
    check(
        set(outer["members"]) == set(members) - {"archive_manifest.json"},
        "outer inventory mismatch",
    )
    for name, record in outer["members"].items():
        check(
            record == {"bytes": len(members[name]), "sha256": sha(members[name])},
            f"outer hash/size mismatch: {name}",
        )
    raw = {
        name.removeprefix("run/"): value
        for name, value in members.items()
        if name.startswith("run/")
    }
    check(len(raw) == transport["raw_files"] == 1856, "raw file count mismatch")
    check(
        sum(map(len, raw.values())) == transport["raw_bytes"] == 47357199, "raw byte count mismatch"
    )
    check(
        sha(raw["manifest.json"]) == transport["raw_manifest_sha256"] == MANIFEST_SHA256,
        "original raw manifest mismatch",
    )
    manifest = read_json(raw["manifest.json"])
    check(
        manifest["manifest_excludes_itself"] is True
        and set(manifest["files"]) == set(raw) - {"manifest.json"},
        "raw inventory mismatch",
    )
    for name, record in manifest["files"].items():
        # complete_json is also EvidenceWriter.write_bytes' byte-completion flag.
        check(record["complete_json"] is True, "incomplete raw write")
        check(
            record["bytes"] == len(raw[name]) and record["sha256"] == sha(raw[name]),
            f"raw hash/size mismatch: {name}",
        )
    return {
        name: [read_json(line) for line in data.splitlines()]
        if name == "literal-inputs.jsonl"
        else read_json(data)
        for name, data in raw.items()
    }


def _verify_bindings(members: dict[str, bytes], rows: dict[str, Any]) -> tuple[dict, dict]:
    check(
        {name for name in members if not name.startswith("run/")}
        == {"archive_manifest.json"} | {"freeze/" + name for name in FROZEN},
        "freeze inventory mismatch",
    )
    for name, digest in FROZEN.items():
        check(sha(members["freeze/" + name]) == digest, f"frozen binding mismatch: {name}")
    protocol, freeze, schema = (
        read_json(members["freeze/" + name])
        for name in ("protocol.json", "implementation_freeze.json", "graph_schema.json")
    )
    check(
        members["run/source-freeze.json"] == members["freeze/implementation_freeze.json"]
        and members["run/literal-inputs.jsonl"] == members["freeze/inputs.jsonl"],
        "raw/freeze bytes mismatch",
    )
    for key, filename in {
        "protocol_sha256": "protocol.json",
        "document_sha256": "protocol.md",
        "inputs_sha256": "inputs.jsonl",
    }.items():
        check(
            freeze[key] == rows["preflight.json"][key] == FROZEN[filename],
            f"preflight/freeze binding mismatch: {key}",
        )
    check(
        rows["preflight.json"]["implementation_freeze_sha256"]
        == FROZEN["implementation_freeze.json"],
        "implementation freeze mismatch",
    )
    check(
        freeze["configuration_sha256"] == sha(canonical(protocol["configuration"]))
        and rows["configuration-preflight.json"] == protocol["configuration"],
        "configuration binding mismatch",
    )
    check(
        freeze["implementation_sources_sha256"]
        == {FREEZE_PATHS[name]: FROZEN[name] for name in ("runner.py", "tests.py")},
        "runner/test binding mismatch",
    )
    check(
        freeze["reuse_sources_sha256"]
        == protocol["reuse_sources_sha256"]
        == {
            FREEZE_PATHS[name]: FROZEN[name]
            for name in (
                "graph_schema.json",
                "interface_design.md",
                "reuse_temporal_contract.md",
                "reuse_temporal_probe.py",
                "reuse_acquired_probe.py",
            )
        },
        "reuse binding mismatch",
    )
    package = freeze["package_sources_sha256"]
    check(
        len(package) == 157
        and package
        == protocol["package_sources_sha256"]
        == rows["preflight.json"]["package_sources_sha256"]
        and freeze["source_pin"]
        == protocol["source_pin"]
        == rows["preflight.json"]["source_pin"]
        == RUNTIME_SOURCE,
        "runtime source manifest mismatch",
    )
    check(
        freeze["graph_schema_sha256"]
        == protocol["graph_schema"]["sha256"]
        == FROZEN["graph_schema.json"]
        and all(package.get(path) == record["sha256"] for path, record in schema["files"].items()),
        "schema source mismatch",
    )
    origins = rows["loaded-source-origins.json"]
    for suffix in ("", "-before-construction", "-after-plan"):
        check(rows[f"loaded-source-origins{suffix}.json"] == origins, "loaded origins changed")
    for module, path in origins.items():
        check(
            path in package
            and path
            in (
                "src/" + module.replace(".", "/") + ".py",
                "src/" + module.replace(".", "/") + "/__init__.py",
            ),
            "loaded source mismatch",
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


def _verify_graphs(rows: dict[str, Any], allowed: dict[str, list[str]]) -> dict[str, SavedGraph]:
    inventories = {
        name: SavedGraph(row, allowed) for name, row in rows.items() if name.startswith("graph-")
    }
    check(len(inventories) == 279, "complete graph inventory mismatch")
    digests = {}
    for name, graph in inventories.items():
        digests[name] = sha(canonical(graph.graph))
        check(name == "graph-" + digests[name] + ".json", "graph digest mismatch")
    pointers = {}
    for name, pointer in rows.items():
        if not name.endswith("-graph.json"):
            continue
        graph = inventories[pointer["inventory_file"]]
        digest = digests[pointer["inventory_file"]]
        check(
            pointer
            == {
                "inventory_file": "graph-" + digest + ".json",
                "canonical_inventory_sha256": digest,
                "node_count": len(graph.nodes),
                "mutable_identity_count": sum(n["type"] != "tuple" for n in graph.nodes),
                "oracle": "complete typed/reference bytes; hash only addresses retained inventory",
            },
            "graph pointer mismatch",
        )
        pointers[name.removesuffix("-graph.json")] = graph
    check(
        len(pointers) == 620
        and {id(g) for g in pointers.values()} == {id(g) for g in inventories.values()},
        "graph pointer coverage mismatch",
    )
    return pointers


def _expected_observation(seed: int, index: int, branch: str | None, serial: int) -> dict:
    """Recompute only the published outcome-blind input recipe, never a producer."""
    key = "prefix" if branch is None else "probe"
    rng = random.Random(int(sha(f"{seed}|{key}|{index}".encode()), 16))
    start = float(index * 200) if branch is None else 12800.0
    pulses = []

    def pulse(at: float, channel: str, magnitude: float) -> dict:
        return {
            "time_ms": at,
            "channel": channel,
            "magnitude": magnitude,
            "polarity": 1,
            "location": None,
            "novelty": 0.0,
            "prediction_error": 0.0,
            "source_id": "probe-input",
            "metadata": {},
        }

    for _ in range(2):
        channel = "HIJKLM"[rng.randrange(6)]
        pulses.append(pulse(start + rng.uniform(0, 36), channel, 0.025))
    jitter = [0.0] * 3 if branch is None else [rng.uniform(-0.35, 0.35) for _ in range(3)]
    cue = int(index >= 32) if branch is None else int(branch.startswith("B"))
    for channel, offset, delta in zip(("AFC", "CFA")[cue], (8, 13, 15), jitter, strict=True):
        pulses.append(pulse(start + offset + delta, channel, 1.18))
    pulses.append(pulse(start + 40, "Q", 1.18))
    return {
        "occurrence_id": f"history-export-20261002-{serial:06d}",
        "start_ms": start,
        "pulses": sorted(pulses, key=lambda p: (p["time_ms"], p["channel"])),
    }


def _raster(observation: dict) -> list[float]:
    vector = [0.0] * 410
    for pulse in observation["pulses"]:
        relative = pulse["time_ms"] - observation["start_ms"]
        magnitude = pulse["magnitude"]
        check(
            math.isfinite(relative)
            and 0 <= relative <= 40
            and math.isfinite(magnitude)
            and magnitude >= 0,
            "raw cutoff/value violation",
        )
        low = math.floor(relative)
        fraction = relative - low
        offset = CHANNELS.index(pulse["channel"]) * 41
        vector[offset + low] += magnitude * (1 - fraction)
        if fraction:
            vector[offset + low + 1] += magnitude * fraction
    total = _recorded_float_sum(vector)
    check(math.isfinite(total) and total > 0, "invalid raw total")
    return [value / total for value in vector]


def _recorded_float_sum(values: Iterable[float]) -> float:
    """Reproduce CPython 3.12.14 sum's finite-float path on at most 410 cells.

    The recorded run used CPython 3.12; 3.11's left sum changes 51 raster totals.
    Use its Neumaier correction explicitly, preserving exact saved-value comparisons
    without relying on the verifier host's sum or substituting math.fsum.
    Source: https://github.com/python/cpython/blob/v3.12.14/Python/bltinmodule.c#L2464-L2497
    This is only the finite, float-only, non-overflowing subset needed by this archive.
    Integer timing-bin/count sums elsewhere retain their exact integer arithmetic.
    """
    total, correction = 0.0, 0.0
    for index, value in enumerate(values):
        check(
            index < 410 and type(value) is float and math.isfinite(value),
            "recorded float sum input outside bounded domain",
        )
        updated = total + value
        if abs(total) >= abs(value):
            correction += (total - updated) + value
        else:
            correction += (value - updated) + total
        total = updated
        check(math.isfinite(total) and math.isfinite(correction), "recorded float sum overflow")
    result = total + correction if correction else total
    check(math.isfinite(result), "recorded float sum overflow")
    return result


def _content(pattern: dict) -> list[Any]:
    return [pattern[key] for key in CANONICAL_FIELDS]


def _dictionary(bank: dict) -> dict:
    candidates = sorted(
        (_content(candidate["prototype"]), identifier)
        for identifier, candidate in bank["candidates"].items()
        if len(candidate["episode_ids"]) >= bank["config"]["mature_episodes"]
    )
    contents = [content for content, _ in candidates]
    collisions = []
    for i, content in enumerate(contents):
        if content in contents[:i]:
            continue
        identifiers = [identifier for value, identifier in candidates if content == value]
        if len(identifiers) > 1:
            collisions.append(identifiers)
    return {
        "binding": {
            "projection_version": PROJECTION_VERSION,
            "source_pin": RUNTIME_SOURCE,
            "N": len(contents),
            "canonical_prototypes": contents,
            "dictionary_sha256": sha(canonical(contents)),
        },
        "coordinates": [
            {"assembly_id": identifier, "canonical": content} for content, identifier in candidates
        ],
        "collisions": collisions,
    }


def _recorded_exp(value: float) -> float:
    """Certify binary64 exp rounding for this archive's bounded timing arguments.

    All 24 checked query-score evaluations (eight distinct arguments in [-4, 0])
    agree with correctly rounded exp. Preserve the rounded binary64 argument exactly;
    do not replace it with the original rational timing error. Decimal.exp is
    correctly rounded to ROUND_HALF_EVEN, independently of the platform's libm:
    https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.exp
    Its adjacent context values enclose the exact result. Accept only if both
    endpoints round to the same binary64 value; no tolerance or fallback is used.
    This certifies only the fixed archive, not general native-runtime portability.
    """
    check(
        type(value) is float and math.isfinite(value) and -4.0 <= value <= 0.0,
        "recorded exp input outside bounded domain",
    )
    context = Context(prec=100, rounding=ROUND_HALF_EVEN, Emin=-999, Emax=999, traps=[])
    result = context.exp(Decimal.from_float(value))
    lower, upper = float(context.next_minus(result)), float(context.next_plus(result))
    check(lower == upper, "recorded exp lacks unique binary64 rounding")
    return lower


def _similarity(left: dict, right: dict) -> float:
    """Pinned native arithmetic on saved primitive patterns; no model code executes."""
    a, b = left["ordered_units"], right["ordered_units"]
    previous = list(range(len(b) + 1))
    for i, value in enumerate(a, 1):
        current = [i]
        for j, other in enumerate(b, 1):
            current.append(
                min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (value != other))
            )
        previous = current
    edit = 1.0 - previous[-1] / max(len(a), len(b)) if a or b else 1.0
    sa, sb = set(left["unit_ids"]), set(right["unit_ids"])
    jaccard = len(sa & sb) / max(1, len(sa | sb)) if sa or sb else 1.0
    la, lb = left["relative_bins"], right["relative_bins"]
    if not la or not lb:
        timing = 1.0 if not la and not lb else 0.0
    elif len(la) == len(lb):
        timing = _recorded_exp(
            -sum(abs(x - y) for x, y in zip(la, lb, strict=True)) / len(la) / 2.0
        )
    else:
        short, long = (left, right) if len(a) < len(b) else (right, left)
        timing = 0.0
        if len(short["ordered_units"]) >= 2:
            for indices in itertools.combinations(
                range(len(long["ordered_units"])), len(short["ordered_units"])
            ):
                if [long["ordered_units"][i] for i in indices] != short["ordered_units"]:
                    continue
                selected = [long["relative_bins"][i] for i in indices]
                selected = [x - selected[0] for x in selected]
                short_bins = [x - short["relative_bins"][0] for x in short["relative_bins"]]
                error = sum(abs(x - y) for x, y in zip(selected, short_bins, strict=True))
                timing = max(timing, _recorded_exp(-error / len(short_bins) / 4.0))
    return 0.55 * edit + 0.25 * jaccard + 0.20 * timing


def _verify_export(
    graph: SavedGraph, dictionary: dict, observation: dict, exported: dict, matching: dict
) -> None:
    bank = graph.get("brain.assemblies")
    check(_dictionary(bank) == dictionary, "query dictionary changed")
    n = dictionary["binding"]["N"]
    check(0 < n <= 32 and not dictionary["collisions"], "unusable fixed dictionary")
    last = len(graph.items("brain.results")) - 1
    path = f"brain.results[{last}]"
    result = graph.get(path)
    audit: dict[str, Any] = {"patterns": [], "strongest_ties": [], "withheld_reasons": []}
    expected = []
    for i, pattern in enumerate(result["patterns"]):
        if pattern["spike_count"] < graph.get("brain.config.min_pattern_spikes"):
            audit["patterns"].append({"index": i, "accepted_internal_pattern": False})
            continue
        scores = [
            {
                "assembly_id": key,
                "canonical": _content(candidate["prototype"]),
                "episode_ids": sorted(candidate["episode_ids"]),
                "episode_count": len(candidate["episode_ids"]),
                "mature": len(candidate["episode_ids"]) >= bank["config"]["mature_episodes"],
                "suppressed": key in bank["suppressed"],
                "score": _similarity(candidate["prototype"], pattern),
            }
            for key, candidate in bank["candidates"].items()
        ]
        check(
            scores
            and all(math.isfinite(row["score"]) and 0 <= row["score"] <= 1 for row in scores),
            "invalid native scores",
        )
        best = max(row["score"] for row in scores)
        ties = sorted(row["assembly_id"] for row in scores if row["score"] == best)
        check(len(ties) == 1, "native match tie in accepted export")
        key = ties[0]
        audit["patterns"].append(
            {
                "index": i,
                "pattern_id": pattern["pattern_id"],
                "canonical": _content(pattern),
                "accepted_internal_pattern": True,
                "scores": scores,
                "best_ties": ties,
                "best_score": best,
                "native_id_tiebreak_winner": key,
            }
        )
        if best < bank["config"]["similarity_threshold"]:
            continue
        candidate = bank["candidates"][key]
        expected.append(
            {
                "assembly_id": key,
                "pattern_id": pattern["pattern_id"],
                "time_ms": pattern["end_ms"],
                "similarity": best,
                "occurrences": candidate["occurrences"],
                "episode_count": len(candidate["episode_ids"]),
                "mature": len(candidate["episode_ids"]) >= bank["config"]["mature_episodes"],
                "unit_ids": candidate["prototype"]["unit_ids"],
                "suppressed": key in bank["suppressed"],
            }
        )
    check(result["assembly_activations"] == expected, "native activation/score mismatch")
    usable = [(i, row) for i, row in enumerate(expected) if row["mature"] and not row["suppressed"]]
    selected = max(
        usable,
        key=lambda pair: (pair[1]["similarity"], pair[1]["episode_count"], pair[1]["assembly_id"]),
        default=None,
    )
    pending_token = graph.at("brain.pending_activation")
    pending = graph.get("brain.pending_activation")
    features = [0.0] * n
    if selected is not None:
        index, winner = selected
        check(
            pending_token == graph.at(f"{path}.assembly_activations[{index}]"),
            "pending activation reference mismatch",
        )
        audit["strongest_ties"] = [
            {
                "activation_index": i,
                "assembly_id": row["assembly_id"],
                "pattern_id": row["pattern_id"],
            }
            for i, row in usable
            if (row["similarity"], row["episode_count"])
            == (winner["similarity"], winner["episode_count"])
        ]
        check(len(audit["strongest_ties"]) == 1, "native strongest tie in accepted export")
        positions = [
            i
            for i, row in enumerate(dictionary["coordinates"])
            if row["assembly_id"] == winner["assembly_id"]
        ]
        check(len(positions) == 1, "winner dictionary binding mismatch")
        features[positions[0]] = winner["similarity"]
        audit["winner_canonical"] = _content(bank["candidates"][winner["assembly_id"]]["prototype"])
    else:
        check(pending is None, "unexpected pending activation")
        audit["winner_canonical"] = None
    audit["pending_is_native_strongest"] = True
    audit["pending_returned_identity_indices"] = [
        i
        for i, token in enumerate(graph.items(path + ".assembly_activations"))
        if token == pending_token
    ]
    check(canonical(matching) == canonical(audit), "matching audit mismatch")
    check(
        canonical(exported)
        == canonical(
            {
                "schema": "v05-history-export-1",
                "occurrence_id": observation["occurrence_id"],
                "decision_ms": result["end_ms"],
                "accepted": True,
                "status": "accepted_match" if pending is not None else "accepted_no_match",
                "features": features,
                "binding": dictionary["binding"],
            }
        ),
        "detached native export mismatch",
    )


def _verify_aliases(graph: SavedGraph, witness: dict) -> None:
    candidates = graph.get("brain.assemblies.candidates")
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


def _configuration(graph: SavedGraph) -> dict:
    return {key: graph.get("brain." + path) for key, path in CONFIG_PATHS.items()}


def _verify_learning(graph: SavedGraph, learning: SavedGraph) -> None:
    for field in ("assemblies", "plasticity", "homeostasis", "predictor", "action_policy"):
        check(
            graph.subtree("brain." + field, "component")
            == learning.subtree(f"learning[{field!r}]", "component"),
            "learning projection component mismatch",
        )
    check(
        learning.get("learning['configuration']") == _configuration(graph),
        "learning configuration mismatch",
    )
    weights = [
        [list(key), edge["weight"], edge["delay_ms"]]
        for key, edge in graph.get("brain.base.field.connections").items()
    ]
    thresholds = [
        [key, unit["base_threshold"]] for key, unit in graph.get("brain.base.field.units").items()
    ]
    check(
        learning.get("learning['weights_delays']") == weights
        and learning.get("learning['thresholds']") == thresholds,
        "frozen weights/delays/thresholds mismatch",
    )


def _verify_semantics(rows: dict[str, Any], graphs: dict[str, SavedGraph], protocol: dict) -> dict:
    """Reconcile every fixed-plan call/copy/mutation with complete saved graphs and rows."""
    records = rows["literal-inputs.jsonl"]
    check(len(records) == 136, "literal input count mismatch")
    counts = dict.fromkeys(COUNTS, 0)
    used_graphs: set[str] = set()
    used_equalities: set[str] = set()
    attempts: set[str] = set()
    resources = [rows["preflight.json"]["resources"]]
    changes = 0

    def graph(label: str) -> SavedGraph:
        used_graphs.add(label)
        return graphs[label]

    def digest(label: str) -> str:
        return rows[label + "-graph.json"]["canonical_inventory_sha256"]

    def same(label: str, current: str, before: str) -> None:
        used_equalities.add(label + "-equality.json")
        check(graph(current).graph == graph(before).graph, f"full graph changed: {label}")
        check(
            rows[label + "-equality.json"]
            == {
                "before": digest(before),
                "after": digest(current),
                "exact_typed_bytes_equal": True,
            },
            "equality prior/after binding mismatch",
        )

    def root_exact(label: str, root: str) -> None:
        check(
            rows[label + "-owner.json"] == {"owner_is_acquired_root": True, "commits": 0},
            "recorded owner pointer mismatch",
        )
        same(label, label, root)

    def attempt(label: str, increments: dict[str, int]) -> dict:
        for key, value in increments.items():
            counts[key] += value
        name = label + "-attempt.json"
        attempts.add(name)
        row = rows[name]
        check(row["counts_including_attempt"] == counts, "attempt count/order mismatch")
        if "resources" in row:
            resources.append(row["resources"])
        return row

    def pairwise(label: str) -> None:
        expected = [
            {"left": a, "right": b, "shared_mutable_paths": []}
            for a, b in itertools.combinations(("root", *BRANCHES), 2)
        ]
        check(rows[label + "-isolation.json"] == expected, "recorded pairwise isolation mismatch")

    def step(label: str, row: dict, retained: SavedGraph, index: int) -> None:
        observation = row["observation"]
        caller = graph(label + "-caller")
        check(caller.get("caller") == observation["pulses"], "caller/raw input mismatch")
        check(
            len({caller.at(f"caller[{i}].metadata")["ref"] for i in range(6)}) == 6,
            "caller metadata not six distinct graph objects",
        )
        same(label + "-input-copy", label + "-ingress", label + "-caller")
        same(label + "-caller-unmodified", label + "-caller-after", label + "-caller")
        check(
            rows[label + "-ingress-isolation.json"] == {"shared_mutable_paths": []},
            "recorded ingress isolation mismatch",
        )
        check(
            rows[label + "-raw410.json"]
            == {
                "observation": observation,
                "channels": CHANNELS,
                "bins": 41,
                "values": _raster(observation),
                "outcome_blind": True,
            },
            "causal raw raster mismatch",
        )
        submitted = attempt(
            label,
            {
                "total_process_attempts": 1,
                row["phase"] + "_process_attempts": 1,
                "submitted_pulses": 6,
            },
        )
        check(
            submitted["record"] == row
            and submitted["flags"] == protocol["call_flags"][row["phase"]],
            "call input/flags mismatch",
        )
        returned = graph(label + "-raw-return")
        check(
            returned.nodes[0]["type"] == "sparkbrain.v05.contracts.V05StepResult"
            and returned.get("result.raw_pulses") == observation["pulses"]
            and returned.get("result.end_ms") == observation["start_ms"] + 72
            and returned.get("result.metadata") == {"episode_id": observation["occurrence_id"]},
            "complete returned input/receipt/clock mismatch",
        )
        check(
            returned.graph == retained.subtree(f"brain.results[{index}]", "result"),
            "raw return/retained complete graph mismatch",
        )
        check(
            retained.at(f"brain.results[{index}].v04_result")
            == retained.at(f"brain.base.results[{index}]"),
            "retained v04 reference mismatch",
        )

    summaries = []
    for si, seed in enumerate(SEEDS):
        prefix = f"seed-{seed}"
        seed_records = records[si * 68 : (si + 1) * 68]
        constructor = attempt(prefix + "-constructor", {"roots": 1})
        check(
            constructor["configuration"] == protocol["configuration"], "constructor config mismatch"
        )
        initial = graph(prefix + "-initial")
        check(
            initial.get("brain.results") == [] and initial.get("brain.assemblies.candidates") == {},
            "fresh root saved state mismatch",
        )
        root_label = prefix + "-acquired"
        acquired = graph(root_label)
        check(len(acquired.items("brain.results")) == 64, "acquired result count mismatch")
        check(
            _configuration(initial)
            == _configuration(acquired)
            == protocol["configuration"]
            == rows[prefix + "-actual-configuration.json"],
            "actual configuration mismatch",
        )
        for i, row in enumerate(seed_records):
            branch = None if i < 64 else BRANCHES[i - 64]
            observation = _expected_observation(
                seed, i if i < 64 else 0, branch, si * 65 + min(i, 64)
            )
            expected = {
                "seed": seed,
                "phase": "acquisition" if i < 64 else "query",
                "observation": observation,
                **({"index": i} if i < 64 else {"branch": branch}),
            }
            check(row == expected, "literal input recipe/order mismatch")
            if i < 64:
                step(f"{prefix}-acquire-{i:02d}", row, acquired, i)
        _verify_aliases(acquired, rows[prefix + "-acquired-alias-witnesses.json"])
        learning = graph(prefix + "-frozen-learning")
        _verify_learning(acquired, learning)
        bank = acquired.get("brain.assemblies")
        check(
            graph(prefix + "-candidate-inventory").graph
            == acquired.subtree("brain.assemblies", "assemblies"),
            "candidate inventory mismatch",
        )
        check(
            len(bank["candidates"]) <= bank["config"]["max_candidates"] == 32
            and bank["config"]["mature_episodes"] == 3,
            "maturity/capacity configuration mismatch",
        )
        for key, candidate in bank["candidates"].items():
            ids = [
                seed_records[i]["observation"]["occurrence_id"]
                for i in range(64)
                if any(
                    row["assembly_id"] == key
                    for row in acquired.get(f"brain.results[{i}].assembly_activations")
                )
            ]
            check(
                candidate["assembly_id"] == key
                and candidate["episode_ids"] == sorted(set(ids))
                and candidate["occurrences"] == len(ids),
                "candidate acquisition episode mismatch",
            )
        dictionary = _dictionary(bank)
        check(
            rows[prefix + "-dictionary.json"] == dictionary, "mature canonical dictionary mismatch"
        )
        for branch in BRANCHES:
            label = prefix + "-copy-" + branch
            check(
                attempt(label, {"whole_brain_copies": 1})["fresh_memo"] is True,
                "recorded fresh copy memo mismatch",
            )
            same(label, label, root_label)
        root_exact(prefix + "-root-after-copies", root_label)
        pairwise(prefix + "-all-copies-before-queries")
        outputs, rasters, query_graphs = {}, {}, {}
        for row in seed_records[64:]:
            branch = row["branch"]
            label = prefix + "-query-" + branch
            candidate_label = label + "-candidate"
            candidate = graph(candidate_label)
            query_graphs[branch] = candidate
            check(len(candidate.items("brain.results")) == 65, "query result count mismatch")
            step(label, row, candidate, 64)
            _verify_aliases(candidate, rows[label + "-alias-witnesses.json"])
            root_exact(label + "-root-after-query", root_label)
            _verify_learning(candidate, graph(label + "-learning"))
            same(label + "-learning-frozen", label + "-learning", prefix + "-frozen-learning")
            pairwise(label + "-live-graphs")
            exported = rows[label + "-export.json"]
            outputs[branch] = exported
            rasters[branch] = _raster(row["observation"])
            _verify_export(
                candidate, dictionary, row["observation"], exported, rows[label + "-matching.json"]
            )
            check(
                graph(label + "-external-input").graph == graph(label + "-caller").graph,
                "actual external input changed before mutation",
            )
            check(
                rows[label + "-export-isolation.json"]
                == {
                    "shared_mutable_count": 0,
                    "candidate_inventory": digest(candidate_label),
                    "caller_inventory": digest(label + "-external-input"),
                    "frozen_dictionary_included": True,
                },
                "recorded export isolation mismatch",
            )
            mutated = graph(label + "-mutated-callers")
            expected_pulses = []
            for index in range(8):
                target = (
                    f"caller[{index}].metadata"
                    if index < 6
                    else ("export.features" if index == 6 else "export.binding")
                )
                before = {} if index < 6 else exported["features" if index == 6 else "binding"]
                after = (
                    before + [-1.0] if index == 6 else dict(before, external_mutation_probe=True)
                )
                record = attempt(f"{label}-mutation-{index}", {"external_object_mutations": 1})
                check(
                    record["actual_target_path"] == target and record["before"] == before,
                    "mutation actual target/before mismatch",
                )
                check(
                    rows[f"{label}-mutation-{index}-returned.json"]
                    == {"actual_target_path": target, "after": after}
                    and before != after,
                    "mutation actual change missing",
                )
                changes += 1
                if index < 6:
                    expected_pulses.append(
                        dict(row["observation"]["pulses"][index], metadata=after)
                    )
            check(
                mutated.get("caller") == expected_pulses
                and len({mutated.at(f"caller[{i}].metadata")["ref"] for i in range(6)}) == 6,
                "actual six caller mutations mismatch",
            )
            check(
                rows[label + "-mutated-diagnostic-export.json"]
                == dict(
                    exported,
                    features=exported["features"] + [-1.0],
                    binding=dict(exported["binding"], external_mutation_probe=True),
                ),
                "actual detached export mutations mismatch",
            )
            same(
                label + "-candidate-after-eight-mutations",
                label + "-candidate-after-eight-mutations",
                candidate_label,
            )
            root_exact(label + "-root-after-eight-mutations", root_label)
            dictionary_hash = sha(canonical(dictionary))
            check(
                rows[label + "-frozen-dictionary-guard.json"]
                == {
                    "exact_canonical_bytes_unchanged": True,
                    "before_sha256": dictionary_hash,
                    "after_sha256": dictionary_hash,
                },
                "frozen dictionary byte guard mismatch",
            )
        root_exact(prefix + "-final-root", root_label)
        repeats = {
            b: {
                "full_native_graph_equal": query_graphs[b].graph
                == query_graphs[b + "_repeat"].graph,
                "complete_export_equal": canonical(outputs[b]) == canonical(outputs[b + "_repeat"]),
            }
            for b in ("A", "B")
        }
        check(all(all(value.values()) for value in repeats.values()), "exact repeat mismatch")
        n = dictionary["binding"]["N"]
        distance = math.dist(outputs["A"]["features"], outputs["B"]["features"])
        summary = {
            "seed": seed,
            "status": "producer_contrast_observed" if distance else "producer_alias",
            "dimension": n,
            "single_candidate": n == 1,
            "vectors": {b: outputs[b]["features"] for b in BRANCHES},
            "export_statuses": {b: outputs[b]["status"] for b in BRANCHES},
            "repeats": repeats,
            "euclidean_distance": distance,
            "ownership_guards": "passed",
            "future_m1_capacity": "future_m1_capacity_blocked"
            if n > 7
            else "default_capacity_only",
            "source_only_scope_birth_reference": 0.25,
            "distance_exceeds_source_reference": distance > 0.25,
            "raw410_l1": _recorded_float_sum(
                abs(a - b) for a, b in zip(rasters["A"], rasters["B"], strict=True)
            ),
            "raw410_exact_repeats": {b: rasters[b] == rasters[b + "_repeat"] for b in ("A", "B")},
            "actual_m1_execution": "not_performed",
            "learned_consumer_benefit": "not_tested",
            "joint_atomicity": "not_tested",
            "scientific_credit": 0,
            "claim_ceiling": "Representation prerequisite for fixed inherited histories only",
        }
        check(rows[prefix + "-summary.json"] == summary, "derived seed summary mismatch")
        summaries.append(summary)
    check(counts == COUNTS and changes == 64, "fixed plan counts mismatch")
    check(
        attempts == {name for name in rows if name.endswith("-attempt.json")},
        "unexpected/missing attempt",
    )
    check(
        used_graphs == set(graphs)
        and used_equalities == {name for name in rows if name.endswith("-equality.json")},
        "unverified graph/equality",
    )
    terminal = rows["terminal.json"]
    check(
        terminal["status"] == "fixed_plan_complete"
        and terminal["counts"] == counts
        and terminal["seed_results"] == summaries
        and terminal["incomplete_files"] == []
        and terminal["no_retry"] is True
        and terminal["scientific_credit"] == 0,
        "terminal consistency mismatch",
    )
    resources.extend((terminal["resources"], rows["manifest.json"]["resources_before_manifest"]))
    _verify_resources(rows, protocol, resources)
    return {
        "counts": counts,
        "external_object_changes": changes,
        "seed_results": summaries,
        "last_pre_manifest_sample": resources[-1],
    }


def _verify_resources(rows: dict, protocol: dict, samples: list[dict]) -> None:
    preflight, freeze = rows["preflight.json"], rows["source-freeze.json"]
    check(
        preflight["python"].startswith("3.12.14 ") and preflight["platform"] == "linux",
        "recorded interpreter/arithmetic binding mismatch",
    )
    check(
        preflight["limits"] == LIMITS
        and preflight["finalization_reserves_inside_limits"] == RESERVE
        and preflight["max_counts"] == protocol["max_counts"] == COUNTS,
        "resource/count limits binding mismatch",
    )
    check({key: protocol["limits"][key] for key in LIMITS} == LIMITS, "protocol limits mismatch")
    check(
        preflight["argv"]
        == [
            "scripts/v05_history_export_probe.py",
            "--run-reviewed",
            "--output",
            freeze["output_directory"],
            "--source-freeze",
            FREEZE_PATHS["implementation_freeze.json"],
            "--source-freeze-sha256",
            FROZEN["implementation_freeze.json"],
        ],
        "recorded launch mismatch",
    )
    timeout = preflight["external_timeout"]
    check(
        timeout["parent_argv"] == ["timeout", "-s", "KILL", "180s", *timeout["process_argv"]]
        and timeout["process_argv"][1:] == ["-B", *preflight["argv"]]
        and timeout["pythonhashseed"] == freeze["pythonhashseed"] == "0"
        and timeout["hash_randomization_flag"] == 0,
        "recorded timeout/environment mismatch",
    )
    previous = dict.fromkeys(("cpu_seconds", "wall_seconds", "peak_rss_bytes"), 0)
    for sample in samples:
        check(
            sample["address_space_limit_bytes"] == LIMITS["address_space_bytes"]
            and sample["wall_origin_monotonic"] == samples[0]["wall_origin_monotonic"]
            and sample["cpu_origin"] == "RUSAGE_SELF process lifetime"
            and sample["wall_origin"] == "Linux process start ticks; precision 1/SC_CLK_TCK",
            "resource origin/actual limit mismatch",
        )
        for key in previous:
            limit = LIMITS["address_space_bytes"] if key == "peak_rss_bytes" else LIMITS[key]
            check(
                math.isfinite(sample[key]) and previous[key] <= sample[key] < limit,
                "resource samples out of order/limit",
            )
            previous[key] = sample[key]
    files = rows["manifest.json"]["files"]
    check(
        rows["terminal.json"]["artifact_bytes_before_terminal"]
        == sum(record["bytes"] for name, record in files.items() if name != "terminal.json")
        and 47357199 < LIMITS["artifact_bytes"],
        "evidence byte accounting mismatch",
    )


def verify(artifact: Path = ARTIFACT) -> dict[str, Any]:
    members, transport = _load_transport(artifact)
    rows = _verify_manifests(members, transport)
    protocol, allowed = _verify_bindings(members, rows)
    graphs = _verify_graphs(rows, allowed)
    result = _verify_semantics(rows, graphs, protocol)
    return {
        "status": "verified_fixed_history_export",
        "archive_sha256": ARCHIVE_SHA256,
        "raw_manifest_sha256": MANIFEST_SHA256,
        "archive_files": 1868,
        "raw_files": 1856,
        "complete_graphs": 279,
        "graph_pointers": 620,
        "complete_returns": 136,
        "model_execution": False,
        "scientific_credit": 0,
        "verification_scope": (
            "saved-data consistency; live identities/execution are source-backed records"
        ),
        "resource_scope": "last pre-manifest observation, not whole-process totals",
        "comparison_scope": "raw410 L1 and native L2 are not comparable advantage metrics",
        "portable_arithmetic": (
            "Explicit CPython 3.12.14 finite-float sum for raster normalization and raw410 L1; "
            "certified Decimal exp rounding for the fixed archive's native timing scores; "
            "saved values and exact equality unchanged"
        ),
        **result,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True, indent=2, allow_nan=False))
