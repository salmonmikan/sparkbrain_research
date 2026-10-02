"""Model-free schedule fixtures; these are never real M1/producer evidence."""
from __future__ import annotations

import copy
import importlib.abc
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from scripts.g0_joint_ownership import SourceRegistry, TypeSpec
from scripts.m1_path_pilot import (
    COUNTS,
    ArmIneligible,
    PathError,
    StandInSchedule,
    native_vector,
    require_native_clearance,
)

ROOT = Path(__file__).resolve().parents[1]


class DenyModels(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("model import forbidden in narrow fixture")
        return None


@pytest.fixture(autouse=True)
def no_model_imports():
    blocker = DenyModels()
    sys.meta_path.insert(0, blocker)
    yield
    sys.meta_path.remove(blocker)


@dataclass
class Producer:
    calls: list = field(default_factory=list)


@dataclass
class Consumer:
    observations: list = field(default_factory=list)
    receipts: list = field(default_factory=list)
    pending: dict | None = None


class Backend:
    def __init__(self, *, failure=None):
        self.failure = failure
        self.disposals = 0
        self.observe_calls = 0

    def producer(self):
        return Producer()

    def m1(self):
        return Consumer()

    def dictionary(self, root):
        return dictionary_fixture(3)

    def process(self, root, observation, acquisition):
        root["producer"].calls.append(observation["occurrence_id"])
        root["raw_history"].append(observation["occurrence_id"])
        if acquisition:
            return {"acquisition": True}
        pulses = observation["pulses"]
        a = next(p["time_ms"] for p in pulses if p["channel"] == "A")
        c = next(p["time_ms"] for p in pulses if p["channel"] == "C")
        return {"export": {
            "schema": "v05-history-export-1", "binding": root["dictionary"]["binding"],
            "occurrence_id": observation["occurrence_id"],
            "decision_ms": observation["start_ms"] + 72.0,
            "accepted": True, "status": "accepted_match",
            "features": [1.0, 0.0, 0.0] if a < c else [0.0, 1.0, 0.0],
        }}

    def check_capacity(self, root, **kwargs):
        assert kwargs == {"dimensions": 8, "context_scalars": 8}

    def observe(self, root, observation):
        self.observe_calls += 1
        if self.failure == self.observe_calls:
            raise RuntimeError("synthetic terminal failure")
        m1 = root["m1"]
        assert m1.pending is None
        m1.pending = observation
        m1.observations.append(observation)
        prediction = observation["sensory_values"]["temporal_000"]
        prediction -= observation["sensory_values"]["temporal_001"]
        route = observation["routing_features"][1] - observation["routing_features"][2]
        decision = "abstain"
        if prediction * route > 0:
            decision = "act_alpha" if prediction > 0 else "act_beta"
        return {"decision": decision, "prediction": prediction, "route": route}

    def outcome(self, root, receipt):
        m1 = root["m1"]
        assert m1.pending["event_id"] == receipt["event_id"]
        m1.receipts.append(copy.deepcopy(receipt))
        m1.pending = None
        return {"committed": True}

    def save_predictive(self, root):
        return json.dumps(root["m1"].__dict__, sort_keys=True).encode()

    def load_predictive(self, payload):
        return json.loads(payload)

    def compare_predictive(self, root, restored):
        assert restored == root["m1"].__dict__

    def dispose_readback(self, restored):
        self.disposals += 1


def fixture_inputs():
    pulse = {"channel": "A", "time_ms": 8.0, "magnitude": 1.18, "polarity": 1,
             "source_id": "probe-input", "metadata": {}, "location": None,
             "novelty": 0.0, "prediction_error": 0.0}
    records = []
    for index in range(68):
        start = min(index, 66) * 200.0
        pulses = []
        for channel, offset in (("A", 8), ("C", 15), ("F", 13), ("Q", 40),
                                ("I", 25), ("J", 30)):
            if index in (65, 67):
                channel = {"A": "C", "C": "A"}.get(channel, channel)
            pulses.append(dict(pulse, channel=channel, time_ms=start + offset, metadata={}))
        records.append({"occurrence_id": f"m1-path-20261002-{min(index,66):06d}",
                        "start_ms": start, "pulses": sorted(pulses, key=lambda p: p["time_ms"])})
    teaching = {arm: [{"receipt_id": f"m1-path-20261002-{arm}-receipt-{64 + i:06d}",
                       "event_id": records[64 + i]["occurrence_id"],
                       "outcome": 0.8 if i == 0 else -0.8,
                       "delivery_ms": records[64 + i]["start_ms"] + 100.0}
                      for i in range(2)] for arm in ("S", "R")}
    return records, teaching


def setup(backend=None):
    records, teaching = fixture_inputs()
    registry = SourceRegistry((TypeSpec(Producer, "fake-producer", ("calls",)),
                               TypeSpec(Consumer, "fake-m1",
                                        ("observations", "receipts", "pending"))))
    evidence = {}
    def emit(name, value):
        assert name not in evidence
        evidence[name] = ({"fixture_graph_was_received": True} if "graph" in value
                          else copy.deepcopy({k: v for k, v in value.items() if k != "root"}))
    runner = StandInSchedule(backend or Backend(), registry, records, teaching, emit)
    return runner, evidence


def test_complete_counts_crossings_sham_and_no_query_feedback():
    runner, evidence = setup()
    result = runner.execute()
    assert result["counts"] == COUNTS
    assert runner.backend.disposals == 10
    assert len([k for k in evidence if k.endswith("-checkpoint-readback")]) == 10
    observes = [evidence[f"observe-{i:02d}"] for i in range(1, 15)]
    for offset in (0, 7):
        primary_a, primary_b, ab, ba, sham = observes[offset + 2:offset + 7]
        assert primary_a["observation"] == sham["observation"]
        assert primary_a["action"] == sham["action"]
        assert ab["action"]["decision"] == ba["action"]["decision"] == "abstain"
        assert primary_a["action"]["decision"] == "act_alpha"
        assert primary_b["action"]["decision"] == "act_beta"
    assert len([k for k in evidence if k.endswith("-revision")]) == 4
    assert runner.live == {} and runner.candidates == [] and runner.owners == {}
    assert result["classification"] == "SOFTWARE_FIXTURE_ONLY"
    with pytest.raises(PathError, match="one-shot"):
        runner.execute()


def test_terminal_failure_is_counted_and_never_retried():
    runner, evidence = setup(Backend(failure=3))
    with pytest.raises(RuntimeError, match="terminal failure"):
        runner.execute()
    assert runner.counts["m1_observe"] == 3
    assert runner.counts["m1_outcome"] == 2
    assert runner.counts["producer_process"] == 67
    assert runner.live == {} and runner.candidates == []
    assert any(v.get("returned") is False for v in evidence.values())


def test_native_clearance_is_unconditionally_disabled():
    with pytest.raises(PathError, match="native execution disabled"):
        require_native_clearance()


def dictionary_fixture(n):
    return {"binding": {"N": n, "projection_version": "fixture",
                        "source_pin": "fixture-origin", "canonical_prototypes": list(range(n)),
                        "dictionary_sha256": "fixture"},
            "coordinates": list(range(n)), "collisions": []}


def test_native_rejection_no_rescale_or_coordinate_truncation():
    observation = fixture_inputs()[0][64]
    export = {"schema": "v05-history-export-1", "binding": dictionary_fixture(3)["binding"],
              "occurrence_id": observation["occurrence_id"],
              "decision_ms": observation["start_ms"] + 72, "accepted": True,
              "status": "accepted_match", "features": [0.0, 0.75, 0.0]}
    dictionary = dictionary_fixture(3)
    assert native_vector(export, dictionary, observation) == [0, .75, 0, 0, 0, 0, 0]
    with pytest.raises(PathError, match="truncated"):
        native_vector(dict(export, features=[0, .75]), dictionary, observation)
    with pytest.raises(ArmIneligible, match="native_match_tie"):
        native_vector(dict(export, accepted=False, status="native_match_tie"),
                      dictionary, observation)
    with pytest.raises(ArmIneligible, match="capacity"):
        native_vector(dict(export, binding=dictionary_fixture(8)["binding"]),
                      dictionary_fixture(8), observation)


def test_failed_writer_prevents_publication_and_further_calls():
    runner, _ = setup()
    emit = runner.emit
    def failure(name, value):
        if name == "S-teach-0-observe-publication":
            raise OSError("fixture evidence full")
        emit(name, value)
    runner.emit = failure
    with pytest.raises(OSError, match="evidence full"):
        runner.execute()
    assert runner.counts["m1_observe"] == 1 and runner.counts["m1_outcome"] == 0
    assert runner.live == {} and runner.candidates == []


def test_module_import_does_not_import_model_in_fresh_interpreter():
    program = '''
import importlib.abc, sys
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name == 'sparkbrain' or name.startswith('sparkbrain.'):
            raise AssertionError('native import forbidden')
sys.meta_path.insert(0, Deny())
from scripts.m1_path_pilot import require_native_clearance, PathError
try: require_native_clearance()
except PathError: pass
else: raise AssertionError('native admission unexpectedly opened')
assert not any(x == 'sparkbrain' or x.startswith('sparkbrain.') for x in sys.modules)
'''
    subprocess.run([sys.executable, "-B", "-c", program], cwd=ROOT, check=True)


def test_acquired_dictionary_ineligibility_stops_native_before_consumer_and_continues_raw():
    runner, _ = setup()
    runner.backend.dictionary = lambda root: dictionary_fixture(0)
    result = runner.execute()
    assert result["results"]["S"] == {"status": "ineligible", "reason": "no_mature_dictionary"}
    assert result["counts"]["producer_process"] == 64
    assert result["counts"]["m1_roots"] == 1
    assert result["counts"]["m1_observe"] == 7
    assert result["counts"]["external_clone"] == 9
    assert result["counts"]["m1_outcome"] == 2
    assert set(result["results"]["R"]) == {"A", "B"}


def test_acquisition_preserved_before_dictionary_failure():
    runner, evidence = setup()
    def failed(root):
        raise ValueError("synthetic dictionary failure")
    runner.backend.dictionary = failed
    with pytest.raises(ValueError, match="dictionary failure"):
        runner.execute()
    assert "acquisition-complete-before-dictionary" in evidence
    assert evidence["acquisition-complete-before-dictionary"]["counts"]["producer_process"] == 64
    assert runner.counts["m1_roots"] == 0
    assert runner.live == {}


def test_terminal_model_error_preserves_partial_graph_before_disposal():
    runner, evidence = setup(Backend(failure=3))
    with pytest.raises(RuntimeError, match="terminal failure"):
        runner.execute()
    assert evidence["terminal-error-before-cleanup"]["counts"]["m1_observe"] == 3
    assert any(name.startswith("terminal-partial-graph-S-query-A") for name in evidence)
    assert runner.live == {}
