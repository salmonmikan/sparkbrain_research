"""Dormant PR188 schedule implementation; model-free stand-in tests only.

Native launch is deliberately unavailable. This source candidate is not an executable
freeze, real G0, checkpoint eligibility, or authority to construct a runtime. The
future native launcher must supply the separately reviewed graph/resource/envelope
binding; neither a backend flag nor this schedule's successful test can admit it.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable
from typing import Any

from scripts.g0_joint_ownership import SourceRegistry, _Walk, capture_graph, clone_joint
from scripts.m1_path_inputs import adapt, encode_raw_order, validate_observation

IDENTITY = "assembly-m1-path-v1-20261002"
SOURCE_COMMIT = "46bbd9b8b28c2404c73f028f8736ed83c3b5c3fe"
NATIVE_EXECUTION_ENABLED = False
COUNTS = {
    "producer_roots": 1, "producer_process": 68, "m1_roots": 2,
    "m1_observe": 14, "m1_outcome": 4, "external_clone": 18,
    "explicit_checkpoint_save": 10, "explicit_checkpoint_load": 10,
}


class PathError(ValueError):
    """Malformed source plan or terminal integrity failure; no retry."""


class ArmIneligible(PathError):
    """Declared representation incompatibility, never a wrong-answer result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PathError(message)


def detach(value: Any) -> Any:
    """Only exact finite JSON primitives; no user hooks or model references escape."""
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if type(value) in (list, tuple):
        return [detach(item) for item in value]
    if type(value) is dict and all(type(k) is str for k in value):
        return {k: detach(v) for k, v in value.items()}
    raise PathError("unknown/nonfinite outward value")


def canonical(value: Any) -> bytes:
    return (json.dumps(detach(value), sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def native_vector(exported: dict, dictionary: dict, observation: dict) -> list[float]:
    """Retain every mature coordinate, native scale and tie/collision disposition."""
    exported, dictionary = detach(exported), detach(dictionary)
    require(type(dictionary) is dict and set(dictionary) == {
        "binding", "coordinates", "collisions"},
            "unexpected native dictionary fields")
    require(type(dictionary["binding"]) is dict and set(dictionary["binding"]) == {
        "projection_version", "source_pin", "N", "canonical_prototypes", "dictionary_sha256"
    }, "unexpected native binding fields")
    require(type(exported) is dict and set(exported) == {
        "schema", "occurrence_id", "decision_ms", "accepted", "status", "features", "binding"
    }, "unexpected native export schema")
    require(exported["schema"] == "v05-history-export-1", "native projection schema")
    require(exported["binding"] == dictionary["binding"], "native dictionary binding changed")
    require(exported["occurrence_id"] == observation["occurrence_id"]
            and exported["decision_ms"] == observation["start_ms"] + 72.0,
            "native observation/time binding changed")
    n = dictionary["binding"]["N"]
    require(type(n) is int and n >= 0, "invalid coordinate count")
    if n == 0:
        raise ArmIneligible("no_mature_dictionary")
    if n > 7:
        raise ArmIneligible("native_coordinate_capacity")
    if dictionary["collisions"]:
        raise ArmIneligible("canonical_collision")
    if exported["accepted"] is not True:
        require(exported["status"] in {
            "no_mature_dictionary", "canonical_collision", "native_match_tie",
            "native_strongest_tie", "value_error", "binding_error"
        }, "unknown native rejection category")
        if exported["status"] in {"value_error", "binding_error"}:
            raise PathError(exported["status"])
        raise ArmIneligible(exported["status"])
    require(exported["status"] in {"accepted_match", "accepted_no_match"},
            "unknown accepted native category")
    require(type(dictionary["coordinates"]) is list and len(dictionary["coordinates"]) == n
            and type(dictionary["binding"]["canonical_prototypes"]) is list
            and len(dictionary["binding"]["canonical_prototypes"]) == n,
            "incomplete canonical native coordinate dictionary")
    features = exported["features"]
    require(type(features) is list and len(features) == n, "native coordinates were truncated")
    require(all(type(x) in (int, float) and math.isfinite(x) and 0 <= x <= 1
                for x in features), "native similarity was rescaled or malformed")
    return features + [0.0] * (7 - n)


def require_native_clearance() -> None:
    """Fail before imports, constructors, checkpoints, STARTED or one-shot reservation."""
    raise PathError(
        "native execution disabled: successful G0 source-delta reconciliation, exact "
        "three-observation graph/checkpoint eligibility, reviewed environment/resource/"
        "finalization freeze, and separate execution clearance are all still required"
    )


class PathSchedule:
    """Exercise transaction/order semantics with either stand-ins or a sealed native port.

    All predecessors stay live until reverse-allocation disposal. Pure snapshots
    include the entire root; inspection hashes merely address retained graph bytes.
    No counters here stand in for a native call profiler or native resource evidence.
    """

    def __init__(self, backend: Any, registry: SourceRegistry, observations: list[dict],
                 teaching: dict, emit: Callable[[str, dict], None], *,
                 permit: Any = None, resources: Any = None, budget: Any = None) -> None:
        require(type(registry) is SourceRegistry, "exact source registry required")
        self.native = registry.domain == "VERIFIED_SOURCE_PREPARATION"
        if self.native:
            from scripts.m1_path_admission import require_permit
            require_permit(permit)
            require(type(backend).__module__ == "scripts.m1_path_native",
                    "native backend must use the exact reviewed adapter")
            require(resources is not None and budget is not None,
                    "native resource boundary and budget are mandatory")
        else:
            require(registry.domain == "SYNTHETIC_MODEL_FREE" and permit is None
                    and resources is None, "unknown backend admission domain")
            require(type(backend).__module__ in {"tests.test_m1_path_pilot", "test_m1_path_pilot"},
                    "only dedicated software-fixture backend admitted")
        self.resources, self.budget = resources, budget
        require(len(observations) == 68, "exactly 68 literal windows required")
        for row in observations:
            validate_observation(row)
        require(set(teaching) == {"S", "R"}, "exact teaching arms")
        for arm, rows in teaching.items():
            require(type(rows) is list and len(rows) == 2, "two teaching receipts per arm")
            for i, row in enumerate(rows):
                require(type(row) is dict and set(row) == {
                    "receipt_id", "event_id", "outcome", "delivery_ms"
                }, "unexpected teaching receipt fields")
                require(row["event_id"] == observations[64 + i]["occurrence_id"]
                        and row["outcome"] == (0.8 if i == 0 else -0.8)
                        and row["delivery_ms"] == observations[64 + i]["start_ms"] + 100.0,
                        "teaching binding or delivery time changed")
                require(row["receipt_id"] == f"m1-path-20261002-{arm}-receipt-{64 + i:06d}",
                        "teaching receipt identity changed")
        self.backend, self.registry, self.emit = backend, registry, emit
        self.observations, self.teaching = detach(observations), detach(teaching)
        self.counts = dict.fromkeys(COUNTS, 0)
        self.live: dict[str, dict] = {}
        self.candidates: list[Any] = []
        self.owners: dict[str, str] = {}
        self.results: dict[str, Any] = {}
        self.sequence = 0
        self.terminal = False
        if self.native:
            self.backend.configure_graph_context(
                self.registry, self.resources, lambda: tuple(self.live.values()))

    def record(self, name: str, value: Any) -> None:
        if self.budget is not None:
            self.budget.check()
        self.emit(name, detach(value))

    def call(self, name: str, method: Callable, *args: Any, **kwargs: Any) -> Any:
        if self.resources is not None:
            self.resources.owner.assert_owner()
        require(not self.terminal and name in COUNTS, "unknown/terminal operation")
        require(self.counts[name] < COUNTS[name], "attempt cap exceeded: " + name)
        self.counts[name] += 1
        self.sequence += 1
        number = self.sequence
        self.record(f"attempt-{number:03d}", {"operation": name, "counts": self.counts})
        try:
            result = method(*args, **kwargs)
        except BaseException as error:
            self.record(f"return-{number:03d}", {
                "returned": False, "error_type": type(error).__name__, "error": str(error)
            })
            raise
        self.record(f"return-{number:03d}", {"returned": True})
        return result

    def snapshot(self, root: Any) -> dict:
        if self.budget is not None:
            self.budget.check()
        walk = _Walk(root, self.registry, self.resources)
        if self.resources is not None:
            capture_graph(root, self.registry, self.resources,
                          retained_roots=tuple(v for v in self.live.values() if v is not root))
        return {"graph": {"root": walk.snapshot.root, "nodes": walk.snapshot.nodes},
                "identities": sorted(walk.indices.items()),
                "mutable_ids": sorted(walk.snapshot.mutable_ids),
                "resources": [] if self.resources is None else self.resources.ledger().bindings}

    def preserve(self, label: str) -> dict:
        before = {name: self.snapshot(root) for name, root in self.live.items()}
        for name, value in before.items():
            self.record(label + "-" + name, value)
        return before

    def unchanged(self, before: dict) -> None:
        for name, state in before.items():
            current = self.snapshot(self.live[name])
            require(all(current[key] == state[key] for key in
                        ("graph", "identities", "mutable_ids")),
                    "retained owner graph/identity changed")
            require(set(state["resources"]) <= set(current["resources"]),
                    "retained resource binding changed")

    def clone(self, source_name: str, label: str) -> dict:
        before = self.preserve(label + "-before")
        source = self.live[source_name]
        candidate = self.call("external_clone", clone_joint, source, self.registry, self.resources,
                              retained_roots=tuple(v for k, v in self.live.items()
                                                   if k != source_name))
        self.unchanged(before)
        self.candidates.append(candidate)
        self.live[label] = candidate.root
        return candidate.root

    def process(self, root: dict, observation: dict, acquisition: bool) -> dict:
        validate_observation(observation)  # All pulses checked before either component moves.
        external = detach(observation)
        before_external = detach(external)
        result = self.call("producer_process", self.backend.process, root, external, acquisition)
        require(external == before_external, "producer mutated caller input")
        self.record(f"producer-{self.counts['producer_process']:03d}", result)
        return detach(result)

    def publish(self, arm: str, label: str) -> None:
        self.record(label + "-publish-ready", self.snapshot(self.live[label]))
        self.record(label + "-publication", {"arm": arm, "old": self.owners[arm], "new": label})
        self.owners[arm] = label

    def observe(self, root: dict, observation: dict, predictive: list, routing: list) -> dict:
        wire = adapt(observation, predictive, routing)
        # The full observation is detached before the exact native/stand-in method.
        external = detach(wire)
        action = self.call("m1_observe", self.backend.observe, root, detach(wire))
        require(external == wire, "caller adaptation changed")
        self.record(f"observe-{self.counts['m1_observe']:02d}", {
            "observation": wire, "action": action, "root": self.snapshot(root)
        })
        return {"observation": wire, "action": detach(action)}

    def features(self, arm: str, root: dict, observation: dict) -> list:
        if arm == "S":
            result = self.process(root, observation, False)
            return native_vector(result["export"], root["dictionary"], observation)
        encoded = encode_raw_order(observation)
        if encoded["status"] != "accepted":
            raise ArmIneligible(encoded["status"])
        root["raw_history"].append(detach(observation))
        return encoded["vector"]

    def checkpoint(self, root: dict, label: str) -> None:
        before = self.preserve(label + "-checkpoint-before")
        payload = self.call("explicit_checkpoint_save", self.backend.save_predictive, root)
        self.record(label + "-checkpoint-bytes", {
            "hex": payload.hex(), "sha256": hashlib.sha256(payload).hexdigest()
        })
        baseline = None if self.resources is None else self.resources.ledger()
        restored = self.call("explicit_checkpoint_load", self.backend.load_predictive, payload)
        self.live[label + "-readback"] = restored
        try:
            self.backend.compare_predictive(root, restored)
            self.record(label + "-checkpoint-readback", {"compatibility_verified": True})
        finally:
            self.backend.dispose_readback(restored)
            del self.live[label + "-readback"]
            del restored
            if self.resources is not None:
                self.resources.verify_cleanup(baseline)
        self.unchanged(before)

    def teach_arm(self, arm: str) -> None:
        for index in range(2):
            label = f"{arm}-teach-{index}-observe"
            protected = self.preserve(label + "-protected")
            root = self.clone(self.owners[arm], label)
            features = self.features(arm, root, self.observations[64 + index])
            self.observe(root, self.observations[64 + index], features, features)
            self.unchanged(protected)
            self.publish(arm, label)
            label = f"{arm}-teach-{index}-outcome"
            protected = self.preserve(label + "-protected")
            root = self.clone(self.owners[arm], label)
            row = self.teaching[arm][index]
            require(row["delivery_ms"] > (self.observations[64 + index]["start_ms"] + 72),
                    "outcome must be later than action")
            receipt = {k: v for k, v in row.items() if k != "delivery_ms"}
            revision = self.call("m1_outcome", self.backend.outcome, root, detach(receipt))
            self.record(label + "-revision", {"receipt": row, "revision": revision})
            self.unchanged(protected)
            self.publish(arm, label)

    def query_arm(self, arm: str) -> None:
        trained = self.owners[arm]
        outputs, vectors = {}, {}
        for index, branch in enumerate(("A", "B")):
            label = f"{arm}-query-{branch}"
            protected = self.preserve(label + "-protected")
            root = self.clone(trained, label)
            vectors[branch] = self.features(arm, root, self.observations[66 + index])
            outputs[branch] = self.observe(root, self.observations[66 + index],
                                           vectors[branch], vectors[branch])
            outputs[branch]["m1_graph"] = capture_graph(
                root["m1"], self.registry, self.resources,
                retained_roots=tuple(self.live.values()))
            self.checkpoint(root, label)
            self.unchanged(protected)
        # The observation skeleton is copied from factual A, including event and time.
        for branch, p, r in (("AB", "A", "B"), ("BA", "B", "A"), ("AA_sham", "A", "A")):
            label = f"{arm}-control-{branch}"
            protected = self.preserve(label + "-protected")
            root = self.clone(trained, label)
            producer_before = self.snapshot({k: v for k, v in root.items() if k != "m1"})
            result = self.observe(root, self.observations[66], vectors[p], vectors[r])
            require(self.snapshot({k: v for k, v in root.items() if k != "m1"})["graph"]
                    == producer_before["graph"], "control advanced producer/raw state")
            if branch == "AA_sham":
                require(result == {k: v for k, v in outputs["A"].items() if k != "m1_graph"},
                        "A/A sham observation or output drift")
                require(capture_graph(root["m1"], self.registry, self.resources,
                                      retained_roots=tuple(self.live.values())).equivalent(
                    outputs["A"]["m1_graph"]), "A/A sham complete M1 aftergraph drift")
            self.checkpoint(root, label)
            self.unchanged(protected)
        self.results[arm] = {branch: {k: v for k, v in row.items() if k != "m1_graph"}
                             for branch, row in outputs.items()}

    def execute(self) -> dict:
        require(not self.live and not self.terminal, "schedule is one-shot")
        native = root = producer = None
        error_record = None
        result = None
        try:
            producer = self.call("producer_roots", self.backend.producer)
            native = {"producer": producer, "m1": None, "raw_history": [], "dictionary": None}
            del producer
            self.live["S-initial"] = native
            for observation in self.observations[:64]:
                self.process(native, observation, True)
            self.record("acquisition-complete-before-dictionary", {
                "root": self.snapshot(native), "counts": dict(self.counts)})
            native["dictionary"] = detach(self.backend.dictionary(native))
            self.record("acquired-complete-graph", {
                "root": self.snapshot(native), "dictionary": native["dictionary"],
                "counts": dict(self.counts)})
            dictionary = native["dictionary"]
            n = dictionary["binding"]["N"]
            require(type(n) is int and n >= 0, "invalid acquired dictionary cardinality")
            native_ineligible = ("no_mature_dictionary" if n == 0 else
                                 "native_coordinate_capacity" if n > 7 else
                                 "canonical_collision" if dictionary["collisions"] else None)
            if native_ineligible is not None:
                self.results["S"] = {"status": "ineligible", "reason": native_ineligible}
            # No acquired producer copy or clone is smuggled into initialization.
            for arm in ("S", "R"):
                if arm in self.results:
                    continue
                if arm == "R":
                    self.live["R-initial"] = {"producer": None, "m1": None,
                        "raw_history": detach(self.observations[:64]), "dictionary": None}
                root = self.live[arm + "-initial"]
                root["m1"] = self.call("m1_roots", self.backend.m1)
                self.backend.check_capacity(root, dimensions=8, context_scalars=8)
                self.owners[arm] = arm + "-initial"
            for arm in ("S", "R"):
                if arm in self.results:
                    continue
                try:
                    self.teach_arm(arm)
                    self.query_arm(arm)
                except ArmIneligible as error:
                    self.results[arm] = {"status": "ineligible", "reason": str(error)}
                    error.__traceback__ = None
            if all("status" not in result for result in self.results.values()):
                require(self.counts == COUNTS, "successful schedule exposure mismatch")
            result = detach({"classification": ("NATIVE_NON_EVIDENTIARY" if self.native
                                                 else "SOFTWARE_FIXTURE_ONLY"),
                             "results": self.results, "counts": self.counts,
                             "native_execution": self.native})
        except BaseException as error:
            error_record = (type(error), str(error))
            error.__traceback__ = None
            error.__context__ = None
            error.__cause__ = None
            try:
                if self.budget is not None:
                    self.budget.finish()
                self.record("terminal-error-before-cleanup", {
                    "error_type": error_record[0].__name__, "error": error_record[1],
                    "counts": dict(self.counts), "owners": dict(self.owners)})
                self.preserve("terminal-partial-graph")
            except BaseException as preservation_error:
                # Failed finalization never converts a partial attempt into success.
                message = error_record[1] + "; terminal preservation failed: "
                message += type(preservation_error).__name__ + ": " + str(preservation_error)
                error_record = (PathError, message)
                preservation_error.__traceback__ = None
        finally:
            native = root = None
            self.terminal = True
            self.owners.clear()
            for candidate in reversed(self.candidates):
                for name in [key for key, root in self.live.items() if root is candidate.root]:
                    del self.live[name]
                candidate.discard_and_verify()
            self.candidates.clear()
            self.live.clear()
            if self.resources is not None:
                from scripts.g0_joint_ownership import ResourceLedger
                self.resources.verify_cleanup(ResourceLedger(()))
        if error_record is not None:
            cls, message = error_record
            if self.native:
                raise PathError(f"terminal {cls.__name__}: {message}") from None
            raise cls(message) from None
        return result


# Compatibility name for the dedicated model-free tests; admission is still exact-domain.
StandInSchedule = PathSchedule
