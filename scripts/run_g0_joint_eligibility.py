#!/usr/bin/env python3
"""Prospective G0 runner: source-only preparation, NOT real execution evidence.

The execution engine is tested only with model-free stand-ins. Real imports are
confined to load_real_runtime, which requires a sealed independently authorized
ExecutionPermit. Source publication, preparation tests, and local JSON booleans do
not authorize execution. No consumed identity or historical runner is invoked.

Native export/config helpers are source-adapted (not imported or executed) from
scripts/v05_history_export_probe.py, SHA-256
1035374574a1528f76d8b6e7aefafb80265b37414322f6d3b675aafc045e671a (PR182).
The native strongest-canonical all-mature coordinate rule is unchanged.

Source-only invocation from the repository root:
python -B -s -m scripts.run_g0_joint_eligibility --check-source
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import hashlib
import importlib
import importlib.machinery
import json
import math
import random
import sys
import types
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).absolute().parents[1]))

from scripts.g0_execution_objects import (  # noqa: E402
    G0_V2,
    HISTORICAL_G0,
    ExecutionObject,
    bind_object_registry,
    object_binding,
    object_digest,
    require_object,
)
from scripts.g0_joint_ownership import (  # noqa: E402
    ResourceBoundary,
    SerialOwner,
    SourceRegistry,
    _Walk,
    capture_graph,
    clone_joint,
)

SOURCE_ONLY = True
IDENTITY = "assembly-m1-g0-v1-20261002"
ARTIFACT_ROOT = "artifacts/research/assembly_m1_g0_v1_20261002"
SOURCE_PIN = "b9caed4797c9cd8217361b6e523864aabdd4cbcc"
PROJECTION_VERSION = "native-strongest-canonical-mature-1"
CANONICAL_FIELDS = ("ordered_units", "relative_bins", "unit_ids", "spike_count", "source_kind")
ACTIVATION_FIELDS = (
    "assembly_id", "pattern_id", "time_ms", "similarity", "occurrences",
    "episode_count", "mature", "unit_ids", "suppressed",
)
EXPECTED = {"clone_joint": 14, "producer.process_episode": 70, "m1.observe": 5,
            "m1.apply_outcome": 6, "producer.constructor": 1, "m1.constructor": 1}
CALL_PLAN = (
    (1, "bootstrap_observe"), (2, "bootstrap_outcome"),
    (3, "pair_clone_first"), (4, "pair_clone_second"),
    (5, "abort_after_producer"), (6, "abort_after_m1"),
    (7, "export_validation_failure"), (8, "reference_observe"),
    (9, "publish_observe"), (10, "fault_after_predictive_revision"),
    (11, "reference_outcome"), (12, "publish_outcome"),
    (13, "identical_receipt_replay"), (14, "receipt_identity_conflict"),
)


class BindingError(ValueError):
    """Frozen input/source mismatch before model dynamics."""


class InvariantError(RuntimeError):
    """Terminal unsupported graph, resource or atomicity failure."""


def require(condition: bool, message: str, error: type[Exception] = BindingError) -> None:
    if not condition:
        raise error(message)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def detach(value: Any) -> Any:
    primitive_tree(value)
    return json.loads(canonical(value))


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

def config_arguments(key: str, settings: dict[str, Any]) -> dict[str, Any]:
    """Restore the sole tuple-valued native config from its JSON wire representation."""
    arguments = copy.deepcopy(settings)
    if key == "action":
        require(type(arguments["actions"]) is list, "action wire format must be a list")
        arguments["actions"] = tuple(arguments["actions"])
    return arguments

def actual_configuration(brain: Any) -> dict[str, Any]:
    configs = {}
    for name, path in CONFIG_PATHS.items():
        value = brain
        for part in path.split("."):
            value = getattr(value, part)
        require(dataclasses.is_dataclass(value), f"{name} config is not a dataclass")
        configs[name] = dataclasses.asdict(value)
    return configs

def canonical_content(prototype: Any) -> tuple[Any, ...]:
    return tuple(getattr(prototype, field) for field in CANONICAL_FIELDS)

def freeze_dictionary(bank: Any, *,
                      object_spec: ExecutionObject = HISTORICAL_G0) -> dict[str, Any]:
    """Bind every mature prototype once, preserving collisions and native-ID audit rows."""
    object_spec = require_object(object_spec)
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
                    "source_pin": object_spec.runtime_origin_commit,
                    **object_binding(object_spec),
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

def export_native(
    brain: Any,
    result: Any,
    observation: dict[str, Any],
    dictionary: dict[str, Any],
    similarity: Any,
    *, object_spec: ExecutionObject = HISTORICAL_G0,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Audit native matching, then detach its actual pending activation without reweighting.

    The injected similarity callable is the pinned native pure function in reviewed
    execution. Tests supply plain fake objects/functions and never import that model.
    """
    object_spec = require_object(object_spec)
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
    if freeze_dictionary(bank, object_spec=object_spec) != dictionary:
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


def validate_observation(row: Any) -> None:
    """Model-free ingress shape check; no constructor or component method is called."""
    require(type(row) is dict and set(row) == {"occurrence_id", "start_ms", "pulses"},
            "unexpected observation schema")
    require(type(row["occurrence_id"]) is str and bool(row["occurrence_id"]), "opaque event ID")
    require(type(row["start_ms"]) in (int, float) and math.isfinite(row["start_ms"])
            and row["start_ms"] >= 0, "invalid start clock")
    require(type(row["pulses"]) is list and len(row["pulses"]) == 6, "six frozen pulses")
    fields = {"time_ms", "channel", "magnitude", "polarity", "location", "novelty",
              "prediction_error", "source_id", "metadata"}
    for pulse in row["pulses"]:
        require(type(pulse) is dict and set(pulse) == fields, "unexpected pulse schema")
        require(type(pulse["channel"]) is str and pulse["channel"], "channel")
        for name in ("time_ms", "magnitude", "novelty", "prediction_error"):
            require(type(pulse[name]) in (float, int) and math.isfinite(pulse[name]),
                    "nonfinite pulse")
        require(row["start_ms"] <= pulse["time_ms"] <= row["start_ms"] + 40,
                "pulse outside frozen window")
        require(pulse["magnitude"] >= 0 and type(pulse["polarity"]) is int
                and pulse["polarity"] == 1 and pulse["location"] is None, "pulse value")
        require(pulse["metadata"] == {} and type(pulse["metadata"]) is dict
                and pulse["source_id"] == "probe-input", "pulse metadata")
        require(pulse["novelty"] == pulse["prediction_error"] == 0.0, "pulse modulation")


def validate_inputs(records: Any) -> None:
    require(type(records) is list and len(records) == 66, "exactly 66 literal input rows")
    for index, record in enumerate(records):
        require(type(record) is dict and record.get("seed") == 910071, "single exposed seed")
        require(record.get("phase") == ("acquisition" if index < 64 else "query"),
                "frozen phase order")
        row = record.get("observation")
        validate_observation(row)
        require(row["occurrence_id"] == f"g0-20261002-{index:06d}", "literal opaque ID")
        require(row["start_ms"] == index * 200, "literal clock schedule")
        if index < 64:
            require(record.get("index") == index, "complete acquisition index")
    shifted = copy.deepcopy(records[64]["observation"])
    shifted["occurrence_id"] = records[65]["observation"]["occurrence_id"]
    shifted["start_ms"] += 200
    for pulse in shifted["pulses"]:
        pulse["time_ms"] += 200
    require(shifted == records[65]["observation"], "post-bootstrap fixed A +200ms pulse shape")


def validate_export(exported: Any, dictionary: dict, *, capacity: int = 8) -> None:
    primitive_tree(exported)
    require(set(exported) == {"schema", "occurrence_id", "decision_ms", "accepted",
                             "status", "features", "binding"}, "export schema")
    require(exported["schema"] == "v05-history-export-1", "native export schema")
    require(exported["accepted"] is True, "native export rejected", InvariantError)
    require(exported["binding"] == dictionary["binding"], "coordinate binding drift")
    features = exported["features"]
    require(type(features) is list and len(features) == dictionary["binding"]["N"],
            "complete native coordinate vector")
    require(1 <= len(features) and 1 + len(features) <= capacity,
            "native dictionary exceeds actual M1 capacity")
    require(all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in features),
            "invalid native coordinate value")
    require(type(exported["decision_ms"]) in (int, float)
            and math.isfinite(exported["decision_ms"]), "decision clock")


def validate_sensory_values(sensory: Any, native_count: int) -> None:
    expected = {"signal", *(f"assembly_{i:03d}" for i in range(native_count))}
    require(type(sensory) is dict and set(sensory) == expected,
            "privileged or unexpected sensory names")
    require(all(type(value) in (float, int) and math.isfinite(value)
                for value in sensory.values()), "nonfinite sensory values")
    require(sensory["signal"] == 0.1, "fixed base signal")


def injected_abort(boundary: str) -> None:
    raise RuntimeError("injected abort " + boundary)


def exception_record(error: BaseException) -> dict[str, str]:
    return {"type": type(error).__name__, "message": str(error)}


class ExecutionEngine:
    """One fixed 14-candidate plan. Dependency injection is for model-free tests only.

    Runtime adapters return detached primitive outputs and explicit caller inputs;
    the engine never treats native checkpoints or JSON outputs as graph oracles.
    The actual native route is selected only by run_authorized after gate admission.
    """

    def __init__(self, runtime: Any, registry: SourceRegistry, resources: ResourceBoundary | None,
                 writer: Any, budget: Any, records: dict, *,
                 object_spec: ExecutionObject = HISTORICAL_G0) -> None:
        self._object_spec = require_object(object_spec)
        if object_spec is G0_V2 or hasattr(registry, "execution_object_sha256"):
            require(getattr(registry, "execution_object_sha256", None)
                    == object_digest(object_spec),
                    "registry execution object differs")
        if object_spec is G0_V2 or hasattr(writer, "_object_spec"):
            require(getattr(writer, "_object_spec", None) is object_spec,
                    "writer execution object differs")
        records, self.receipts = normalize_plan(records)
        self.runtime, self.registry, self.resources = runtime, registry, resources
        self.writer, self.budget, self.records = writer, budget, copy.deepcopy(records)
        self.counts = dict.fromkeys(EXPECTED, 0)
        self.live: dict[str, dict] = {}
        self.candidates: dict[int, Any] = {}
        self.pointer: tuple[dict, int] | None = None
        self.stage = "not_started"
        self.sequence = 0
        self.graph_files: dict[str, str] = {}

    def write(self, label: str, data: Any) -> None:
        self.writer.raw_json(label + ".json", data)

    def attempt(self, name: str, detail: dict | None = None) -> None:
        self.budget.check()
        require(name in EXPECTED and self.counts[name] < EXPECTED[name],
                "call ceiling exceeded: " + name, InvariantError)
        self.counts[name] += 1
        self.sequence += 1
        self.write(f"attempt-{self.sequence:03d}", {"stage": self.stage, "operation": name,
                   "counts": dict(self.counts), "detail": detail,
                   "resources": self.budget.sample()})

    def call(self, name: str, operation: Any, *args: Any, **kwargs: Any) -> Any:
        self.attempt(name)
        number = self.sequence
        try:
            result = operation(*args, **kwargs)
        except BaseException as error:
            record = exception_record(error)
            # Preserve before eliminating exception frames that can retain native bases.
            self.write(f"return-{number:03d}", {"returned": False, "error": record})
            raise
        self.write(f"return-{number:03d}", {"returned": True})
        return result

    def retained(self, root: Any) -> tuple[Any, ...]:
        return tuple(value for value in self.live.values() if value is not root)

    def capture(self, label: str, root: Any) -> dict:
        self.budget.check()
        # _Walk is the exact pinned adapter's traversal; only primitive indices escape.
        walk = _Walk.__new__(_Walk)
        try:
            _Walk.__init__(walk, root, self.registry, self.resources)
            snapshot = capture_graph(root, self.registry, self.resources,
                                     retained_roots=self.retained(root))
            graph = {"root": snapshot.root, "nodes": snapshot.nodes}
            encoded = canonical(graph)
            digest = hashlib.sha256(encoded.encode()).hexdigest()
            if digest not in self.graph_files:
                filename = "graph-" + digest
                self.write(filename, graph)
                self.graph_files[digest] = filename + ".json"
            result = {"graph": graph, "identity_nodes": tuple(sorted(walk.indices.items())),
                      "mutable_ids": tuple(sorted(snapshot.mutable_ids)),
                      "resources": (() if self.resources is None else
                                    self.resources.ledger().bindings)}
            self.write(label + "-witness", {"graph_file": self.graph_files[digest],
                       "graph_sha256": digest, "identity_nodes": result["identity_nodes"],
                       "mutable_ids": result["mutable_ids"], "resources": result["resources"],
                       "owner_pointer": None if self.pointer is None else id(self.pointer[0]),
                       "owner_generation": None if self.pointer is None else self.pointer[1]})
            return result
        except BaseException as error:
            self.write(label + "-partial-graph", {"nodes": getattr(walk, "nodes", []),
                       "identity_nodes": tuple(sorted(getattr(walk, "indices", {}).items())),
                       "error": exception_record(error)})
            raise
        finally:
            # Do not retain object tables while disposal is verified.
            del walk

    def preserve(self, label: str, *, exclude: Any = None) -> dict[str, dict]:
        return {name: self.capture(label + "-" + name, value)
                for name, value in self.live.items() if value is not exclude}

    def unchanged(self, label: str, before: dict[str, dict]) -> None:
        for name, prior in before.items():
            after = self.capture(label + "-" + name, self.live[name])
            require(after["graph"] == prior["graph"]
                    and after["identity_nodes"] == prior["identity_nodes"],
                    "retained graph/identity changed: " + name, InvariantError)
            # Added candidate bindings are permitted; all prior live resources remain exact.
            require(set(prior["resources"]) <= set(after["resources"]),
                    "retained lock mapping changed", InvariantError)

    def clone(self, number: int, source: dict) -> Any:
        self.stage = CALL_PLAN[number - 1][1]
        require(number == self.counts["clone_joint"] + 1, "candidate schedule order")
        candidate = self.call("clone_joint", clone_joint, source, self.registry, self.resources,
                              retained_roots=self.retained(source))
        self.candidates[number] = candidate
        self.live[f"candidate-{number:02d}"] = candidate.root
        self.capture(f"candidate-{number:02d}-cloned", candidate.root)
        return candidate

    def discard(self, number: int) -> None:
        self.capture(f"candidate-{number:02d}-before-disposal", self.candidates[number].root)
        del self.live[f"candidate-{number:02d}"]
        self.candidates[number].discard_and_verify()
        del self.candidates[number]
        self.write(f"candidate-{number:02d}-disposed", {"lifo_cleanup_verified": True,
                   "resources": [] if self.resources is None else self.resources.ledger().bindings})

    def publish(self, number: int) -> None:
        root = self.candidates[number].root
        require(self.pointer is not None, "missing initial owner")
        next_pointer = (root, self.pointer[1] + 1)
        self.capture(f"candidate-{number:02d}-publish-ready", root)
        self.write(f"candidate-{number:02d}-publication", {
            "from_pointer": id(self.pointer[0]), "to_pointer": id(root),
            "from_generation": self.pointer[1], "to_generation": next_pointer[1],
            "pending": root["pending"], "receipts": root["receipts"],
            "all_required_evidence_precedes_publication": True})
        self.budget.check()
        self.pointer = next_pointer  # The sole owner-publication assignment.

    def process(self, root: dict, record: dict, *, acquisition: bool = False) -> dict:
        validate_observation(record["observation"])
        external = self.call("producer.process_episode", self.runtime.process,
                             root, record["observation"], acquisition=acquisition)
        self.write(f"operation-{self.sequence:03d}-producer", external["raw"])
        return external

    def mutate(self, label: str, external: dict, root: dict) -> None:
        before = self.preserve(label + "-preserved")
        outward = external["raw"]
        external_ids = set(primitive_tree(outward))
        for state in before.values():
            require(not external_ids.intersection(state["mutable_ids"]),
                    "detached output aliases owner", InvariantError)
        self.write(label + "-external-before", self.runtime.external_snapshot(external))
        self.runtime.mutate_external(external)
        self.write(label + "-external-after", self.runtime.external_snapshot(external))
        self.unchanged(label + "-after-mutation", before)
        self.capture(label + "-current", root)

    def observe(self, root: dict, record: dict, external: dict) -> None:
        exported = external["raw"]["export"]
        validate_export(exported, root["dictionary"], capacity=self.runtime.capacity(root))
        require(exported["occurrence_id"] == record["observation"]["occurrence_id"],
                "export/event binding")
        action = self.call("m1.observe", self.runtime.observe, root, exported, external)
        self.write(f"operation-{self.sequence:03d}-action", action)
        self.write(f"operation-{self.sequence:03d}-pending", root["pending"])
        retained = self.preserve(f"action-{self.sequence:03d}-preserved")
        action_ids = set(primitive_tree(action))
        require(not any(action_ids.intersection(row["mutable_ids"]) for row in retained.values()),
                "action output aliases owner", InvariantError)
        mutate_primitive_tree(action)
        self.write(f"operation-{self.sequence:03d}-action-mutated", action)
        self.unchanged(f"action-{self.sequence:03d}-after-mutation", retained)

    def outcome(self, root: dict, receipt: dict, *, fault: bool = False) -> dict:
        result = self.call("m1.apply_outcome", self.runtime.outcome, root, receipt, fault=fault)
        self.write(f"operation-{self.sequence:03d}-revision", result)
        self.write(f"operation-{self.sequence:03d}-receipts", root["receipts"])
        retained = self.preserve(f"revision-{self.sequence:03d}-preserved")
        result_ids = set(primitive_tree(result))
        require(not any(result_ids.intersection(row["mutable_ids"]) for row in retained.values()),
                "revision output aliases owner", InvariantError)
        returned = detach(result)
        mutate_primitive_tree(result)
        self.write(f"operation-{self.sequence:03d}-revision-mutated", result)
        self.unchanged(f"revision-{self.sequence:03d}-after-mutation", retained)
        return returned

    def expected_failure(self, label: str, operation: Any, expected_type: type,
                         message: str) -> None:
        matched = False
        try:
            operation()
        except Exception as error:
            record = exception_record(error)
            matched = type(error) is expected_type and message in str(error)
            error.__traceback__ = None
            self.write(label + "-expected-failure", {"matched": matched, "error": record})
        self.budget.check()
        require(matched, "missing or wrong planned failure: " + label, InvariantError)

    def negative_preflight(self) -> None:
        counts = dict(self.counts)
        malformed = copy.deepcopy(self.records[65]["observation"])
        malformed["pulses"][0]["magnitude"] = "not-a-number"
        exported = {"schema": "v05-history-export-1", "occurrence_id": "negative-only",
                    "decision_ms": 0.0, "accepted": True, "status": "accepted_no_match",
                    "features": [0.0], "binding": {"N": 1}}
        nonfinite = copy.deepcopy(exported)
        nonfinite["features"][0] = float("nan")
        nonfinite_evidence = copy.deepcopy(exported)
        nonfinite_evidence["features"][0] = {"exact_float_kind": "nan"}
        oversized = dict(exported, features=[0.0] * 8, binding={"N": 8})
        bad_schema = dict(exported, schema="invalid")
        privileged = {"signal": 0.1, "truth": 1.0}
        cases = (
            ("malformed_primitive_pulse", malformed,
             lambda: validate_observation(malformed), BindingError, "nonfinite pulse"),
            ("privileged_sensory_name", privileged,
             lambda: validate_sensory_values(privileged, 1), BindingError, "sensory names"),
            ("nonfinite_export", nonfinite_evidence,
             lambda: validate_export(nonfinite, {"binding": {"N": 1}}),
             InvariantError, "nonfinite export"),
            ("native_coordinate_capacity_exceeds_actual_M1_headroom", oversized,
             lambda: validate_export(oversized, {"binding": {"N": 8}}),
             BindingError, "capacity"),
            ("schema_mismatch", bad_schema,
             lambda: validate_export(bad_schema, {"binding": {"N": 1}}), BindingError, "schema"),
        )
        for name, raw, operation, expected_type, message in cases:
            self.write("negative-" + name + "-input", {
                "input": raw, "expected_error": expected_type.__name__,
                "expected_message": message, "before_counts": counts,
                "nonfinite_encoding": "exact_float_kind describes the actual in-memory NaN"})
            self.expected_failure("negative-" + name, operation, expected_type, message)
        require(counts == self.counts and all(value == 0 for value in counts.values()),
                "negative preflight advanced a component", InvariantError)
        self.write("negative-preflight", {"components_advanced": False, "counts": counts,
                                          "case_count": len(cases)})

    def abort_cleanup(self) -> dict:
        """Terminal, non-dynamical cleanup while the dedicated owner is still alive.

        Any disposal/audit defect is retained as a failure. Releasing strong roots
        after a failed proof is best-effort disposal, never a repaired success.
        """
        import gc

        self.pointer = None
        errors = []
        disposed = []
        for number in sorted(self.candidates, reverse=True):
            candidate = self.candidates[number]
            self.live.pop(f"candidate-{number:02d}", None)
            try:
                candidate.discard_and_verify()
                disposed.append(number)
            except BaseException as error:
                errors.append({"candidate": number, "error": exception_record(error)})
                error.__traceback__ = None
                # Drop the entire failed candidate, including native rollback replacements.
                # Never alter the native weak registry or adapter's proof stack.
                candidate.root = None
            del self.candidates[number]
            del candidate
        self.live.clear()
        gc.collect()
        bindings = []
        if self.resources is not None:
            try:
                self.resources.verify_cleanup(type(self.resources.ledger())(()))
                bindings = list(self.resources.ledger().bindings)
                require(not self.resources._candidate_stack, "unclosed candidate proof stack",
                        InvariantError)
            except BaseException as error:
                errors.append({"candidate": None, "error": exception_record(error)})
                error.__traceback__ = None
        return {"status": "verified" if not errors else "failed", "disposed_lifo": disposed,
                "errors": errors, "final_resource_bindings": bindings,
                "all_runner_strong_roots_released": not self.live and not self.candidates
                and self.pointer is None}

    def execute(self) -> dict:
        self.negative_preflight()
        self.stage = "construct_initial"
        # The native factory implements constructors separately so both attempts are visible.
        producer = self.call("producer.constructor", self.runtime.construct_producer)
        m1 = self.call("m1.constructor", self.runtime.construct_m1)
        root = {"producer": producer, "m1": m1, "clock": {"decision_ms": 0.0},
                "dictionary": None, "pending": None, "receipts": {}}
        del producer, m1
        self.live["initial"] = root
        self.pointer = (root, 0)
        self.capture("initial", root)
        for index, record in enumerate(self.records[:64]):
            self.stage = f"acquisition-{index:02d}"
            external = self.process(root, record, acquisition=True)
            self.mutate(self.stage, external, root)
            del external
        root["dictionary"] = self.runtime.freeze_dictionary(root)
        self.write("frozen-dictionary", root["dictionary"])
        require(root["dictionary"]["binding"]["N"] > 0
                and not root["dictionary"]["collisions"], "absent or colliding dictionary")
        require(1 + root["dictionary"]["binding"]["N"] <= self.runtime.capacity(root),
                "native dictionary exceeds actual M1 capacity")
        acquired = self.preserve("acquired")
        first = self.clone(1, root)
        external = self.process(first.root, self.records[64])
        self.observe(first.root, self.records[64], external)
        self.mutate("bootstrap-observe", external, first.root)
        del external
        self.unchanged("bootstrap-source", acquired)
        self.publish(1)
        bootstrap_receipt = self.receipts["bootstrap"]
        before = self.preserve("bootstrap-outcome-source")
        second = self.clone(2, first.root)
        revision = self.outcome(second.root, bootstrap_receipt)
        require(revision.get("committed") is True, "bootstrap outcome not committed")
        require(self.runtime.nonempty(second.root), "bootstrap M1/receipt state must be nonempty")
        self.unchanged("bootstrap-outcome-retained", before)
        self.publish(2)
        bootstrap = second.root
        del first, second
        before = self.preserve("nonempty-source")
        self.clone(3, bootstrap)
        self.clone(4, bootstrap)  # candidate 3 is an explicitly retained root.
        self.preserve("pairwise-live")  # capture each with every other root declared.
        self.discard(4)
        self.discard(3)
        self.unchanged("pairwise-retained", before)
        reference_graph = None
        for number in range(5, 10):
            before = self.preserve(f"case-{number:02d}-source")
            protected_pointer = self.pointer
            candidate = self.clone(number, bootstrap)
            external = self.process(candidate.root, self.records[65])
            if number != 5:
                self.observe(candidate.root, self.records[65], external)
            if number in (5, 6):
                boundary = "after_producer_before_m1" if number == 5 else "after_m1_before_publish"
                self.write(f"case-{number:02d}-abort-boundary", {
                    "boundary": boundary, "owner_pointer": id(self.pointer[0]),
                    "owner_generation": self.pointer[1], "counts": dict(self.counts)})
                self.expected_failure(f"case-{number:02d}-abort",
                                      lambda boundary=boundary: injected_abort(boundary),
                                      RuntimeError, "injected abort " + boundary)
            if number == 7:
                # Independent post-M1 outward validation rejection; mutate only the export.
                external["raw"]["export"]["schema"] = "invalid-post-advance-schema"
                self.write("case-07-invalid-export-before-validation", external["raw"]["export"])
                self.expected_failure(
                    "case-07-export",
                    lambda export=external["raw"]["export"],
                    dictionary=candidate.root["dictionary"]: validate_export(export, dictionary),
                    BindingError, "schema")
            self.mutate(f"case-{number:02d}", external, candidate.root)
            del external
            self.unchanged(f"case-{number:02d}-retained", before)
            require(self.pointer is protected_pointer, "prepublication owner pointer changed",
                    InvariantError)
            after = self.capture(f"case-{number:02d}-after", candidate.root)
            if number == 8:
                reference_graph = after["graph"]
            if number == 9:
                require(after["graph"] == reference_graph, "observe/reference full graph mismatch",
                        InvariantError)
                self.write("observe-reference-equality", {"complete_typed_graph_equal": True})
                self.publish(9)
            else:
                self.discard(number)
            del candidate
        pending = self.pointer[0]
        teaching = self.receipts["teach"]
        before = self.preserve("fault-source")
        fault_pointer = self.pointer
        self.clone(10, pending)
        self.expected_failure("fault-real-after-predictive", lambda: self.outcome(
            self.candidates[10].root, teaching, fault=True), RuntimeError,
            "injected after predictive revision")
        self.unchanged("fault-retained", before)
        owner_unchanged = (self.pointer is fault_pointer
                           and self.pointer[0] is pending
                           and self.pointer[1] == fault_pointer[1])
        self.write("fault-owner-boundary", {
            "before_owner_pointer": id(fault_pointer[0]),
            "before_owner_generation": fault_pointer[1],
            "exact_owner_pointer_and_generation_preserved": owner_unchanged,
            "native_rollback_equivalence": "not_tested",
            "required_candidate_disposition": "discard_entire_candidate"})
        require(owner_unchanged, "fault changed owner pointer or generation", InvariantError)
        # Only the outer transaction is required here. The failed candidate's native
        # rollback graph is not compared or certified, and is discarded in full.
        self.discard(10)
        del fault_pointer
        reference_graph = None
        for number in (11, 12):
            before = self.preserve(f"outcome-{number}-source")
            candidate = self.clone(number, pending)
            revision = self.outcome(candidate.root, teaching)
            require(revision.get("committed") is True, "outcome not committed")
            after = self.capture(f"outcome-{number}-after", candidate.root)
            self.unchanged(f"outcome-{number}-retained", before)
            if number == 11:
                reference_graph = after["graph"]
                self.discard(11)
            else:
                require(after["graph"] == reference_graph, "outcome/reference full graph mismatch",
                        InvariantError)
                self.write("outcome-reference-equality", {"complete_typed_graph_equal": True})
                self.publish(12)
            del candidate
        committed = self.pointer[0]
        pointer = self.pointer
        for number in (13, 14):
            before = self.preserve(f"receipt-{number}-source")
            candidate = self.clone(number, committed)
            graph = self.capture(f"receipt-{number}-before", candidate.root)
            if number == 13:
                self.outcome(candidate.root, teaching)
            else:
                conflict = self.receipts["conflict"]
                self.expected_failure("receipt-conflict", lambda conflict=conflict: self.outcome(
                    self.candidates[14].root, conflict), ValueError, "receipt identity conflict")
            after = self.capture(f"receipt-{number}-after", candidate.root)
            require(graph["graph"] == after["graph"]
                    and graph["identity_nodes"] == after["identity_nodes"]
                    and self.pointer is pointer, "replay/conflict mutated graph or pointer",
                    InvariantError)
            self.unchanged(f"receipt-{number}-retained", before)
            self.discard(number)
            del candidate
        require(self.counts == EXPECTED, "incomplete fixed schedule", InvariantError)
        result = {"status": "bounded_plan_complete", "identity": self._object_spec.identity,
                  **object_binding(self._object_spec),
                  "scientific_credit": 0, "expected": EXPECTED, "actual": dict(self.counts),
                  "owner_generation": self.pointer[1], "case_count": 14,
                  "runtime_domain": self.registry.domain,
                  "efficacy": "not_tested", "acquisition_necessity": "not_tested",
                  "learned_benefit": "not_tested", "max_continuation_observes": 2,
                  "native_rollback_equivalence": "not_tested"}
        self.write("plan-complete-before-cleanup", result)
        # Retained committed predecessors were deliberately live throughout the proof.
        self.pointer = None
        del pending, committed, bootstrap, root, pointer, protected_pointer
        for number in (12, 9, 2, 1):
            self.discard(number)
        self.live.clear()
        if self.resources is not None:
            self.resources.verify_cleanup(type(self.resources.ledger())(()))
        self.write("final-cleanup", {"all_live_roots_released": True})
        return result


class NativeRuntime:
    """Source-pinned native bindings, constructed only by the sealed-gate loader."""

    def __init__(self, permit: Any, modules: dict[str, Any], configuration: dict,
                 m1_configuration: dict, *, admission: Any, budget: Any) -> None:
        from scripts.g0_execution_support import advance_runtime_admission
        advance_runtime_admission(permit, admission, budget, "bound")
        self.permit, self.modules, self.configuration = permit, modules, configuration
        self.m1_configuration = m1_configuration
        self.prepared = {}
        for key, (relative, name) in CONFIG_TYPES.items():
            module_name = "sparkbrain." + relative.removesuffix(".py").replace("/", ".")
            self.prepared[key] = getattr(modules[module_name], name)(
                **config_arguments(key, configuration[key]))
        require(canonical({k: dataclasses.asdict(v) for k, v in self.prepared.items()})
                == canonical(configuration), "actual prepared configuration drift")

    def construct_producer(self) -> Any:
        cls = self.modules["sparkbrain.v05.brain"].IntegratedV05Brain
        producer = cls(copy.deepcopy(self.prepared["brain"]), **{
            key + "_config": copy.deepcopy(self.prepared[key])
            for key in ("receptor", "assembly", "homeostasis", "plasticity", "action")})
        require(canonical(actual_configuration(producer)) == canonical(self.configuration),
                "actual producer configuration drift")
        return producer

    def construct_m1(self) -> Any:
        m1 = self.modules["sparkbrain.system_build.integrated_m1"].IntegratedM1Pilot()
        base = m1.predictive.reference_brain._brain
        require(base.config.input_track == "I1_local_compositional"
                and base.config.entity_track == "E0_global"
                and base._provided_revision_model is None,
                "actual M1 must remain default I1/E0 without supplied revision model")
        actual = {"v03": dataclasses.asdict(base.config),
                  "predictive": dataclasses.asdict(m1.predictive.config),
                  "scope": dataclasses.asdict(m1.scoped.config)}
        require(canonical(actual) == canonical(self.m1_configuration),
                "complete actual M1 configuration drift")
        return m1

    @staticmethod
    def capacity(root: dict) -> int:
        return min(8, root["m1"].scoped.config.maximum_dimensions,
                   root["m1"].predictive.config.max_context_scalars)

    def freeze_dictionary(self, root: dict) -> dict:
        return freeze_dictionary(root["producer"].assemblies,
                                 object_spec=self.permit.object_spec)

    def process(self, root: dict, observation: dict, *, acquisition: bool) -> dict:
        pulse_type = self.modules["sparkbrain.v04.contracts"].SignalPulse
        callers = tuple(pulse_type(**copy.deepcopy(row)) for row in observation["pulses"])
        require([row.as_dict() for row in callers] == observation["pulses"], "caller pulses drift")
        # Native dataclass input is detached before producer admission, including metadata.
        owned = tuple(pulse_type(**row.as_dict()) for row in callers)
        require(not {id(p.metadata) for p in callers} & {id(p.metadata) for p in owned},
                "pulse metadata ingress alias")
        result = root["producer"].process_episode(
            owned, episode_id=observation["occurrence_id"], learn_assembly=acquisition,
            learn_field=acquisition, explore_action=False, metadata={})
        root["clock"]["decision_ms"] = result.end_ms
        require(result.end_ms == observation["start_ms"] + 72.0, "native decision clock drift")
        raw = {"result": json.loads(canonical(result.as_dict())),
               "observation": detach(observation)}
        if not acquisition:
            exported, audit = export_native(root["producer"], result, observation,
                                            root["dictionary"], self.modules[
                                                "sparkbrain.v05.assemblies"].pattern_similarity,
                                            object_spec=self.permit.object_spec)
            raw["export"], raw["matching"] = detach(exported), json.loads(canonical(audit))
        return {"raw": raw, "caller_pulses": callers, "caller_sensory": None}

    def observe(self, root: dict, exported: dict, external: dict) -> dict:
        sensory = {"signal": 0.1, **{f"assembly_{i:03d}": float(value)
                                     for i, value in enumerate(exported["features"])}}
        validate_sensory_values(sensory, len(exported["features"]))
        external["caller_sensory"] = sensory
        features = (0.1, *exported["features"])
        observation = self.modules["sparkbrain.system_build.integrated_m1"].M1Observation(
            exported["occurrence_id"], exported["decision_ms"] / 1000.0,
            copy.deepcopy(sensory), tuple(features))
        require(observation.sensory_values is not sensory, "sensory ingress alias")
        action = root["m1"].observe(observation)
        root["pending"] = {"event_id": observation.event_id, "time": observation.time,
                           "native_export": detach(exported),
                           "sensory_values": copy.deepcopy(sensory),
                           "routing_features": list(features)}
        return detach(action.as_dict())

    def outcome(self, root: dict, receipt: dict, *, fault: bool = False) -> dict:
        native = self.modules["sparkbrain.system_build.integrated_m1"].M1OutcomeReceipt(**receipt)
        revision = root["m1"].apply_outcome(
            native, _fault_at="after_predictive_revision" if fault else None)
        outward = detach(revision.as_dict())
        if receipt["receipt_id"] not in root["receipts"]:
            require(root["pending"] is not None and
                    root["pending"]["event_id"] == receipt["event_id"], "pending receipt binding")
            root["receipts"][receipt["receipt_id"]] = {
                "receipt": detach(receipt), "pending": root["pending"],
                "revision": detach(outward)}
            root["pending"] = None
        return outward

    @staticmethod
    def nonempty(root: dict) -> bool:
        return bool(root["m1"].predictive._states and root["m1"].scoped._routes
                    and root["m1"]._receipt_bindings and root["receipts"])

    @staticmethod
    def external_snapshot(external: dict) -> dict:
        return {"caller_pulses": [row.as_dict() for row in external["caller_pulses"]],
                "caller_sensory": copy.deepcopy(external["caller_sensory"]),
                "output": detach(external["raw"])}

    @staticmethod
    def mutate_external(external: dict) -> None:
        for pulse in external["caller_pulses"]:
            pulse.metadata["caller_after_preservation"] = {"nested": [991.0]}
        if external["caller_sensory"] is not None:
            external["caller_sensory"]["signal"] = -999.0
            external["caller_sensory"]["caller_after_preservation"] = 991.0
        mutate_primitive_tree(external["raw"])


def mutate_primitive_tree(tree: Any) -> None:
    """Mutate each actual outward container after its bytes have been preserved."""
    if type(tree) is dict:
        for value in tuple(tree.values()):
            mutate_primitive_tree(value)
        tree["caller_after_preservation"] = "mutation"
    elif type(tree) is list:
        for value in tuple(tree):
            mutate_primitive_tree(value)
        tree.append("caller_after_preservation")


def normalize_plan(plan: Any) -> tuple[list[dict], dict]:
    """Validate primary frozen JSON, never generate or adapt literal pulses at execution."""
    require(type(plan) is dict and set(plan) == {"acquisition", "queries", "receipts"},
            "primary literal input schema")
    require(type(plan["acquisition"]) is list and len(plan["acquisition"]) == 64,
            "64 literal acquisition inputs")
    names = {"bootstrap", "abort_producer", "abort_m1", "export_failure",
             "reference_observe", "publish_observe"}
    require(type(plan["queries"]) is dict and set(plan["queries"]) == names, "query schedule")
    query = plan["queries"]
    require(all(query[name] == query["publish_observe"] for name in names - {"bootstrap"}),
            "all five independent query branches require identical literal input")
    records = [{"seed": 910071, "phase": "acquisition", "index": index, "observation": row}
               for index, row in enumerate(plan["acquisition"])]
    records += [{"seed": 910071, "phase": "query", "observation": query[name]}
                for name in ("bootstrap", "publish_observe")]
    validate_inputs(records)
    receipts = plan["receipts"]
    require(type(receipts) is dict and set(receipts) == {"bootstrap", "teach", "conflict"},
            "receipt schedule")
    for name, index, receipt_id, value in (
        ("bootstrap", 64, "g0-receipt-000001", 0.8),
        ("teach", 65, "g0-receipt-000002", 0.8),
        ("conflict", 65, "g0-receipt-000002", -0.8),
    ):
        require(receipts[name] == {"receipt_id": receipt_id,
                                  "event_id": records[index]["observation"]["occurrence_id"],
                                  "outcome": value}, "literal receipt mismatch")
    return copy.deepcopy(records), detach(receipts)


def verify_native_module_origin(root: Path, name: str, module: Any) -> None:
    """Pure exact-source origin check, including packages and config-only modules."""
    from scripts.verify_g0_joint_source_contract import confined_path, source_root

    root = source_root(root)
    require(type(name) is str and (name == "sparkbrain" or name.startswith("sparkbrain.")),
            "native module name differs")
    require(type(module) is types.ModuleType, "native binding is not an exact module")
    expected = root / "src" / Path(*name.split("."))
    expected = (expected / "__init__.py" if "__path__" in vars(module)
                else expected.with_suffix(".py"))
    confined_path(root, expected.relative_to(root).as_posix(), "loaded native source")
    spec = vars(module).get("__spec__")
    require(type(spec) is importlib.machinery.ModuleSpec
            and type(spec.loader) is importlib.machinery.SourceFileLoader
            and vars(module).get("__name__") == name and spec.name == name
            and vars(module).get("__loader__") is spec.loader
            and spec.loader.name == name and spec.loader.path == str(expected)
            and vars(module).get("__file__") == str(expected) and spec.origin == str(expected),
            "native source origin mismatch")


def load_real_runtime(permit: Any, *, admission: Any = None,
                      budget: Any = None) -> tuple[NativeRuntime, SourceRegistry, dict]:
    """The sole dormant native import boundary. No self-issued execution authority."""
    from scripts.g0_execution_support import AdmissionError, advance_runtime_admission
    if admission is None or budget is None:
        raise AdmissionError("unissued or unprepared runtime admission for native imports")
    advance_runtime_admission(permit, admission, budget, "importing")
    root = permit.root
    require(not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules),
            "native modules must not be preloaded")
    require(sys.dont_write_bytecode, "native execution requires -B")
    # An empty per-attempt cache prefix prevents loading stale .pyc, even under -B.
    from scripts.g0_execution_support import read_json
    from scripts.verify_g0_joint_source_contract import confined_path, source_root
    require(sys.pycache_prefix is not None, "dedicated bytecode cache prefix required")
    cache = source_root(Path(sys.pycache_prefix))
    require(not any(cache.iterdir()), "dedicated empty bytecode cache prefix required")
    object_spec = permit.object_spec
    contract = read_json(confined_path(root, object_spec.contract_relative, "source contract"))
    protocol = read_json(confined_path(root, object_spec.protocol_relative, "protocol"))
    modules = {}
    classes = [random.Random]
    sys.path.insert(0, str(root / "src"))
    for relative, record in sorted(contract["files"].items()):
        budget.check()
        module_name = relative.removeprefix("src/").removesuffix(".py").replace("/", ".")
        module = importlib.import_module(module_name)
        modules[module_name] = module
        classes.extend(getattr(module, name) for name in record["classes"])
    # Config-only modules may be outside the selected class-bearing subset.
    for relative, _ in CONFIG_TYPES.values():
        budget.check()
        name = "sparkbrain." + relative.removesuffix(".py").replace("/", ".")
        modules[name] = importlib.import_module(name)
    for name, module in tuple(sys.modules.items()):
        budget.check()
        if name == "sparkbrain" or name.startswith("sparkbrain."):
            verify_native_module_origin(root, name, module)
    # Deliberately retain the independent post-import source/class audit. Its
    # scan is profiled cheaply and finite event checks protect no-output work.
    budget.check()
    registry = bind_object_registry(root, tuple(classes), object_spec)
    budget.check()
    advance_runtime_admission(permit, admission, budget, "loaded")
    runtime = NativeRuntime(permit, modules, protocol["producer_configuration"],
                            protocol["m1_configuration"], admission=admission, budget=budget)
    return runtime, registry, modules


def native_resource_boundary(owner: SerialOwner, modules: dict) -> ResourceBoundary:
    facade = modules["sparkbrain.v032.runtime"]
    return ResourceBoundary(owner, facade._LOCK_REGISTRY, facade._LOCK_REGISTRY_GUARD,
                            raw_type=modules["sparkbrain.v03.runtime"].IntegratedV03Brain,
                            facade_type=facade.IntegratedV032Brain,
                            facade_factory=facade.IntegratedV032Brain,
                            factory_source_tag="pinned:v032:IntegratedV032Brain")


def execute_reviewed(permit: Any, output: Path) -> dict:
    """Dormant complete orchestration for a later externally authorized dedicated process.

    Preparation tests replace admission, limits, profiler and native loading with
    explicit model-free stand-ins; they never mint a real permit. Native execution
    requires a permit bound to the output directory, reviewed freeze and fresh identity.
    No approval file or successful execution record is supplied by this preparation.
    """
    from scripts.g0_execution_support import (
        CALL_CAPS,
        ExclusiveEvidenceWriter,
        PassiveCallMonitor,
        ResourceBudget,
        consume_execution_permit,
        install_runtime_limits,
        protocol_call_caps,
        read_json,
        require_execution_permit,
        runtime_admission,
        validate_completed_lifecycle,
        verify_mapped_libraries,
    )
    from scripts.verify_g0_joint_source_contract import confined_path, source_root

    budget = ResourceBudget()
    require_execution_permit(permit, checkpoint=budget.check)
    object_spec = permit.object_spec
    root = permit.root
    output = source_root(output.parent) / output.name
    require(output == permit.output_directory, "output differs from independently approved target")
    consume_execution_permit(permit, output, budget=budget)
    writer = ExclusiveEvidenceWriter(output, object_spec.identity, budget,
                                     object_spec=object_spec)
    monitor = None
    engine = None
    result = None
    failure = None
    abort_cleanup = None
    try:
        launch = install_runtime_limits(permit, budget=budget)
        budget.bind_timeout_parent(launch)
        writer.raw_json("launch-environment.json", {
            "hard_timeout": launch, "environment": permit.freeze["environment"],
            "identity": object_spec.identity, **object_binding(object_spec),
            "scope": "NON_EVIDENTIARY_ENGINEERING_ONLY",
            "max_continuation_observes": 2, "scientific_credit": 0})
        freeze_path = confined_path(root, permit.freeze_path.relative_to(root).as_posix(), "freeze")
        approval_path = confined_path(root, permit.approval_path.relative_to(root).as_posix(),
                                      "external approval")
        writer.raw_bytes("source-freeze.json", freeze_path.read_bytes())
        writer.raw_bytes("independent-execution-approval.json", approval_path.read_bytes())
        source_copies = []
        for index, (relative, digest) in enumerate(sorted(
                permit.freeze["source_files_sha256"].items())):
            budget.check()
            path = confined_path(root, relative, "frozen execution source")
            raw = path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == digest, "source changed before copy")
            name = f"frozen-source-{index:04d}-" + path.name
            writer.raw_bytes(name, raw)
            source_copies.append({"source": relative, "copy": name, "sha256": digest})
        writer.raw_json("source-copy-index.json", source_copies)
        protocol_path = confined_path(root, object_spec.protocol_relative, "protocol")
        input_path = confined_path(root, object_spec.inputs_relative, "literal inputs")
        protocol = read_json(protocol_path)
        plan = read_json(input_path)
        normalize_plan(plan)
        require(protocol["identity"] == object_spec.identity, "protocol identity")
        require(protocol["call_caps"] == protocol_call_caps(), "protocol/passive call-cap mismatch")
        writer.raw_bytes("literal-inputs.json", input_path.read_bytes())
        writer.raw_json("configuration.json", {"producer": protocol["producer_configuration"],
                                               "m1": protocol["m1_configuration"]})
        cache = output / "empty_bytecode_cache"
        cache.mkdir(mode=0o700, exist_ok=False)
        sys.pycache_prefix = str(cache)
        budget.check()
        with runtime_admission(permit, budget) as admission, \
                PassiveCallMonitor(root, CALL_CAPS, budget, writer,
                                   object_spec=object_spec) as monitor:
            runtime, registry, modules = load_real_runtime(
                permit, admission=admission, budget=budget)
            writer.raw_json("mapped-libraries-after-import.json",
                            verify_mapped_libraries(permit.freeze["environment"],
                                                    checkpoint=budget.check))
            monitor.check()
            # Install profiler before SerialOwner creates its dedicated thread.
            with SerialOwner() as owner:
                def construct_engine() -> ExecutionEngine:
                    boundary = native_resource_boundary(owner, modules)
                    return ExecutionEngine(runtime, registry, boundary, writer, budget, plan,
                                           object_spec=object_spec)
                monitor.check()
                engine = owner.call(construct_engine)
                monitor.check()
                try:
                    result = owner.call(engine.execute)
                    monitor.check()
                except BaseException as error:
                    # SerialOwner scrubs the failed worker traceback before it crosses
                    # this boundary, so it cannot keep any candidate's native base alive.
                    error.__traceback__ = None
                    budget.finish()
                    abort_cleanup = owner.call(engine.abort_cleanup)
                    writer.raw_json("failure-owner-cleanup.json", abort_cleanup)
                    raise
            actual = monitor.snapshot()
            writer.raw_json("actual-calls-and-resources.json", actual)
            lifecycle = validate_completed_lifecycle(actual, object_spec=object_spec)
            writer.raw_json("completed-lifecycle-validation.json", lifecycle)
        # Recheck the full dependency environment only after hooks are removed.
        # This detects final integrity drift; it is not continuous protection
        # against concurrent source/dependency mutation during a trusted run.
        require(not budget.finalizing, "success validation cannot spend terminal reserve")
        require_execution_permit(permit, checkpoint=budget.check)
        writer.raw_json("mapped-libraries-before-verdict.json",
                        verify_mapped_libraries(permit.freeze["environment"],
                                                checkpoint=budget.check))
        writer.verdict("engineering-verdict.json", {
            **result, "completed_lifecycle": lifecycle, "native_lifecycle_expected": CALL_CAPS,
            "native_lifecycle_actual": actual["counts"],
            "scope": "bounded_owner_isolation_and_publication_only",
            "longer_continuation_compatibility": "not_tested",
            "canonical_scientific_evidence": False},
            raw_names=["plan-complete-before-cleanup.json", "final-cleanup.json",
                       "actual-calls-and-resources.json", "literal-inputs.json",
                       "source-copy-index.json", "completed-lifecycle-validation.json",
                       "mapped-libraries-after-import.json",
                       "mapped-libraries-before-verdict.json"])
    except BaseException as error:
        failure = exception_record(error)
        error.__traceback__ = None
        budget.finish()
        if monitor is not None:
            writer.raw_json("partial-actual-calls.json", monitor.snapshot())
        writer.raw_json("terminal-failure.json", {
            "error": failure, "stage": "preflight" if engine is None else engine.stage,
            "top_level_counts": {} if engine is None else engine.counts,
            "owner_generation": None if engine is None or engine.pointer is None
            else engine.pointer[1], "no_retry_or_resume": True,
            "failure_cleanup": abort_cleanup})
    terminal = {"result": result if failure is None else None, "failure": failure,
                "identity": object_spec.identity, **object_binding(object_spec),
                "scientific_credit": 0, "no_retry_or_resume": True,
                "complete_evidence_required": True}
    # Any failure here propagates: retained STARTED/partial files are not a success.
    writer.terminal("SUCCESS" if failure is None else "STOPPED", terminal)
    return terminal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-source", action="store_true")
    parser.add_argument("--run-reviewed", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    args = parser.parse_args()
    if args.run_reviewed:
        parser.error("real execution requires an externally issued sealed ExecutionPermit; "
                     "local source/review/approval JSON and this CLI cannot authorize it")
    if args.check_source:
        from scripts.g0_execution_support import verify_preparation
        result = verify_preparation(args.root, ARTIFACT_ROOT + "/freeze.json")
        print(canonical(result))
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
