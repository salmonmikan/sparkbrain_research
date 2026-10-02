"""Model-free literal, encoder and wire checks; every SparkBrain import is blocked."""

from __future__ import annotations

import builtins
import copy
import importlib.abc
import importlib.util
import json
import math
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/m1_path_inputs.py"


@contextmanager
def runtime_imports_blocked():
    original = builtins.__import__

    def guard(name, *args, **kwargs):
        if name == "sparkbrain" or name.startswith("sparkbrain."):
            raise AssertionError(f"forbidden model import: {name}")
        return original(name, *args, **kwargs)

    class Blocker(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
                raise AssertionError(f"forbidden model import: {fullname}")
            return None

    blocker = Blocker()
    builtins.__import__ = guard
    sys.meta_path.insert(0, blocker)
    try:
        yield
    finally:
        builtins.__import__ = original
        sys.meta_path.remove(blocker)


with runtime_imports_blocked():
    SPEC = importlib.util.spec_from_file_location("m1_path_inputs_under_test", SCRIPT)
    assert SPEC is not None and SPEC.loader is not None
    TOOL = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(TOOL)


@pytest.fixture(autouse=True)
def block_runtime():
    with runtime_imports_blocked():
        yield


@pytest.fixture(scope="module")
def prepared():
    with runtime_imports_blocked():
        return TOOL.build()


@pytest.fixture(scope="module")
def rows(prepared):
    return [json.loads(line) for line in prepared["inputs.jsonl"].splitlines()]


@pytest.fixture
def observation(rows):
    return copy.deepcopy(rows[66])


def cue(observation, channel):
    return next(p for p in observation["pulses"] if p["channel"] == channel)


def test_all_import_paths_block_runtime():
    with pytest.raises(AssertionError, match="forbidden model import"):
        builtins.__import__("sparkbrain")
    with pytest.raises(AssertionError, match="forbidden model import"):
        importlib.util.find_spec("sparkbrain.never_import_this")


def test_prepared_bytes_exact_and_build_read_only(prepared, monkeypatch):
    def forbidden_write(*args, **kwargs):
        raise AssertionError("build must not write")

    monkeypatch.setattr(Path, "write_bytes", forbidden_write)
    monkeypatch.setattr(Path, "write_text", forbidden_write)
    assert TOOL.build() == prepared
    assert set(prepared) == {"inputs.jsonl", "evaluator.json"}
    TOOL.check(TOOL.DEFAULT, prepared)
    evaluator = json.loads(prepared["evaluator.json"])
    assert evaluator["classification"] == "SOURCE_ONLY_UNEXECUTED_NONCANONICAL_NON_EVIDENTIARY"
    assert evaluator["execution_authorized"] is False
    assert evaluator["scientific_credit"] == 0


def test_exact_one_first_seed_prefix_retained_except_ids(rows):
    source = TOOL.read_source_literals()["run/inputs-910071-prefix.json"]
    assert len(source) == 64 and len(rows) == 68
    for index, (original, row) in enumerate(zip(source, rows[:64], strict=True)):
        assert row == {
            "occurrence_id": f"m1-path-20261002-{index:06d}",
            "start_ms": original["start_ms"],
            "pulses": original["pulses"],
        }
    assert len({r["occurrence_id"] for r in rows}) == 67


def test_first_pair_only_literal_shifts_and_nuisance_preserved(rows):
    pair = TOOL.read_source_literals()["run/inputs-910071-pairs.json"][0]
    for index, which, shift in ((64, 0, 0.0), (65, 1, 200.0), (66, 0, 400.0), (67, 1, 400.0)):
        expected = copy.deepcopy(pair[which]["pulses"])
        for pulse in expected:
            pulse["time_ms"] += shift
        assert rows[index]["pulses"] == expected
        assert rows[index]["start_ms"] == pair[which]["start_ms"] + shift
    assert rows[66]["occurrence_id"] == rows[67]["occurrence_id"] == "m1-path-20261002-000066"
    for a, b in zip(rows[66]["pulses"], rows[67]["pulses"], strict=True):
        expected = {**a, "channel": {"A": "C", "C": "A"}.get(a["channel"], a["channel"])}
        assert b == expected
    assert rows[66]["pulses"][0]["time_ms"] == 13200.031067481343
    assert rows[66]["pulses"][4]["time_ms"] == 13221.494814587282


def test_no_evaluator_metadata_in_any_observation(rows):
    for row in rows:
        assert set(row) == {"occurrence_id", "start_ms", "pulses"}
        assert len(row["pulses"]) == 6
        for pulse in row["pulses"]:
            assert set(pulse) == TOOL.PULSE_KEYS
            assert pulse["metadata"] == {}
            assert pulse["source_id"] == "probe-input"
            assert pulse["novelty"] == pulse["prediction_error"] == 0.0
            assert pulse["polarity"] == 1 and pulse["location"] is None
        assert TOOL.encode_raw_order(row)["status"] == "accepted"


def test_teaching_feedback_and_query_targets_only_evaluator(prepared, rows):
    evaluator = json.loads(prepared["evaluator.json"])
    assert evaluator["source"]["prefix_seed"] == 910071
    assert evaluator["source"]["pair_index"] == 0
    assert evaluator["source"]["member_sha256"] == TOOL.SOURCE_MEMBERS
    assert evaluator["acquisition_input_indices"] == list(range(64))
    assert evaluator["producer_windows"] == 68
    receipts = []
    for index, (row, outcome) in enumerate(
        zip(evaluator["teaching"], (0.8, -0.8), strict=True), 64
    ):
        assert row["input_index"] == index and row["outcome"] == outcome
        assert row["event_id"] == rows[index]["occurrence_id"]
        assert row["decision_time_ms"] == rows[index]["start_ms"] + 72
        assert row["delivery_time_ms"] == rows[index]["start_ms"] + 100
        assert row["delivery_time_ms"] > row["decision_time_ms"]
        assert set(row["receipt_ids"]) == {"S", "R"}
        receipts.extend(row["receipt_ids"].values())
    assert len(receipts) == len(set(receipts)) == 4
    queries = evaluator["queries"]
    assert [q["target_action"] for q in queries] == ["act_alpha", "act_beta"]
    assert [q["signed_outcome_target"] for q in queries] == [0.8, -0.8]
    assert all(q["feedback_allowed"] is False for q in queries)
    assert queries[0]["decision_time_ms"] == queries[1]["decision_time_ms"] == 13272.0
    assert queries[0]["event_id"] == queries[1]["event_id"]
    assert evaluator["controls"]["observation_binding_from_input_index"] == 66
    assert evaluator["controls"]["producer_advances"] == 0
    assert evaluator["controls"]["feedback_allowed"] is False
    for forbidden in (b"outcome", b"target", b"receipt", b"audit_label", b"alpha", b"beta"):
        assert forbidden not in prepared["inputs.jsonl"]


def test_fixed_order_coordinates_without_labels_or_list_order(observation):
    assert TOOL.encode_raw_order(observation) == {
        "status": "accepted",
        "vector": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }
    observation["occurrence_id"] = "renamed-opaque-id"
    observation["pulses"].reverse()
    assert TOOL.encode_raw_order(observation)["vector"][0] == 1.0
    a, c = cue(observation, "A"), cue(observation, "C")
    a["time_ms"], c["time_ms"] = c["time_ms"], a["time_ms"]
    assert TOOL.encode_raw_order(observation) == {
        "status": "accepted",
        "vector": [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }


def test_exact_tie_and_adjacent_float_are_different_cases(observation):
    a, c = cue(observation, "A"), cue(observation, "C")
    c["time_ms"] = a["time_ms"]
    assert TOOL.encode_raw_order(observation) == {"status": "ambiguous_order", "vector": None}
    c["time_ms"] = math.nextafter(a["time_ms"], math.inf)
    assert TOOL.encode_raw_order(observation)["vector"][0] == 1.0
    c["time_ms"] = math.nextafter(a["time_ms"], -math.inf)
    assert TOOL.encode_raw_order(observation)["vector"][1] == 1.0


@pytest.mark.parametrize("channel", ["A", "C"])
@pytest.mark.parametrize("kind", ["missing", "multiple", "zero", "negative_magnitude", "negative"])
def test_all_cue_domain_violations_have_no_vector(observation, channel, kind):
    pulse = cue(observation, channel)
    if kind == "missing":
        observation["pulses"].remove(pulse)
    elif kind == "multiple":
        observation["pulses"].append(copy.deepcopy(pulse))
    elif kind == "negative":
        pulse["polarity"] = -1
    else:
        pulse["magnitude"] = 0.0 if kind == "zero" else -1.0
    assert TOOL.encode_raw_order(observation) == {"status": "out_of_domain", "vector": None}


@pytest.mark.parametrize("field", ["time_ms", "magnitude", "novelty", "prediction_error"])
@pytest.mark.parametrize("value", [True, "1", None, float("nan"), float("inf"), -float("inf")])
def test_numeric_fields_reject_bool_nonfinite_and_malformed(observation, field, value):
    observation["pulses"][-1][field] = value
    with pytest.raises(ValueError, match="malformed_input"):
        TOOL.encode_raw_order(observation)


@pytest.mark.parametrize(
    "mutation",
    [
        {"channel": "Z"},
        {"metadata": {"target": "alpha"}},
        {"metadata": []},
        {"source_id": "hidden-label"},
        {"location": [0, 0]},
        {"novelty": 0.1},
        {"prediction_error": 0.1},
        {"polarity": True},
        {"polarity": 0},
        {"polarity": 1.0},
    ],
)
def test_all_pulse_fields_validated_including_nuisance(observation, mutation):
    nuisance = next(p for p in observation["pulses"] if p["channel"] in "HIJKLM")
    nuisance.update(mutation)
    with pytest.raises(ValueError):
        TOOL.encode_raw_order(observation)


@pytest.mark.parametrize("past", [True, False])
def test_window_boundaries_inclusive_and_no_future_tolerance(observation, past):
    at = observation["start_ms"] + (0 if past else 40)
    nuisance = next(p for p in observation["pulses"] if p["channel"] in "HIJKLM")
    nuisance["time_ms"] = at
    assert TOOL.encode_raw_order(observation)["status"] == "accepted"
    nuisance["time_ms"] = math.nextafter(at, -math.inf if past else math.inf)
    with pytest.raises(ValueError, match="causal_input_violation"):
        TOOL.encode_raw_order(observation)


@pytest.mark.parametrize("domain", ["zero", "missing", "tie", "negative"])
def test_later_future_pulse_cannot_hide_behind_earlier_cue_rejection(observation, domain):
    a = cue(observation, "A")
    if domain == "missing":
        observation["pulses"].remove(a)
    elif domain == "tie":
        a["time_ms"] = cue(observation, "C")["time_ms"]
    elif domain == "negative":
        a["polarity"] = -1
    else:
        a["magnitude"] = 0.0
    observation["pulses"][-1]["time_ms"] = observation["start_ms"] + 41
    original = copy.deepcopy(observation)
    with pytest.raises(ValueError, match="causal_input_violation"):
        TOOL.encode_raw_order(observation)
    assert observation == original


@pytest.mark.parametrize("value", [-1, True, "0", float("nan"), float("inf"), 1e308])
def test_malformed_window_rejected(observation, value):
    observation["start_ms"] = value
    with pytest.raises(ValueError, match="malformed_input"):
        TOOL.validate_observation(observation)


def test_exact_key_and_container_contract(observation):
    for key in ("target", "regime", "outcome", "current_sensory", "label"):
        bad = {**observation, key: 0}
        with pytest.raises(ValueError, match="unexpected fields"):
            TOOL.encode_raw_order(bad)
    observation["pulses"][0]["future"] = False
    with pytest.raises(ValueError, match="unexpected fields"):
        TOOL.encode_raw_order(observation)


def test_empty_and_multiple_cues_never_choose_first_last(observation):
    observation["pulses"] = []
    assert TOOL.encode_raw_order(observation) == {"status": "out_of_domain", "vector": None}


def test_raster_retains_exact_historical_interpolation(prepared, rows):
    retained = json.loads(prepared["evaluator.json"])["raster_retention"]
    assert retained["channel_order"] == list("ACFHIJKLMQ")
    assert retained["bins_per_channel"] == 41
    assert len(retained["input_rows"]) == 68
    for index, (row, stored) in enumerate(zip(rows, retained["input_rows"], strict=True)):
        expected = [0.0] * 410
        for pulse in row["pulses"]:
            relative = pulse["time_ms"] - row["start_ms"]
            floor = math.floor(relative)
            fraction = relative - floor
            offset = "ACFHIJKLMQ".index(pulse["channel"]) * 41
            expected[offset + floor] += pulse["magnitude"] * (1 - fraction)
            if fraction:
                expected[offset + math.ceil(relative)] += pulse["magnitude"] * fraction
        total = sum(expected)
        expected = [value / total for value in expected]
        assert stored["input_index"] == index
        assert stored["observation_sha256"] == TOOL.sha(TOOL.canonical(row))
        assert stored["values"] == TOOL.raster(row) == expected
        assert math.isclose(sum(expected), 1, abs_tol=1e-15)


def test_fractional_raster_and_last_bin(observation):
    a = cue(observation, "A")
    a.update(time_ms=observation["start_ms"] + 8.25, magnitude=1.0)
    observation["pulses"] = [a]
    values = TOOL.raster(observation)
    assert len(values) == 410 and values[8:10] == [0.75, 0.25]
    assert sum(values) == 1.0
    a["time_ms"] = observation["start_ms"] + 40
    assert TOOL.raster(observation)[40] == 1.0


def test_exact_detached_two_inlet_adaptation_and_sham(observation, rows):
    p = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    r = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    adapted = TOOL.adapt(observation, p, r)
    assert set(adapted) == {"event_id", "time", "sensory_values", "routing_features"}
    assert adapted["event_id"] == "m1-path-20261002-000066" and adapted["time"] == 13.272
    assert adapted["sensory_values"] == {
        "signal": 0.0,
        **{f"temporal_{i:03d}": x for i, x in enumerate(p)},
    }
    assert adapted["routing_features"] == [0.0, *r]
    assert len(adapted["routing_features"]) == len(adapted["sensory_values"]) == 8
    assert TOOL.adapt(rows[66], p, p) == TOOL.adapt(copy.deepcopy(rows[66]), p.copy(), p.copy())
    pair = TOOL.adapt(rows[67], p, r)
    assert pair == adapted
    p[0] = r[1] = 0.5
    observation["occurrence_id"] = "mutated"
    assert adapted["sensory_values"]["temporal_000"] == 1.0
    assert adapted["routing_features"][2] == 1.0
    for row in rows[64:]:
        wire = TOOL.adapt(row, [0.0] * 7, [0.0] * 7)
        assert wire["sensory_values"]["signal"] == wire["routing_features"][0] == 0.0


@pytest.mark.parametrize(
    "bad", [[], [0.0] * 6, [0.0] * 8, [True] * 7, [float("nan")] * 7, [-0.1] * 7, [1.1] * 7]
)
@pytest.mark.parametrize("inlet", ["predictive", "routing"])
def test_adaptation_rejects_bad_feature_vectors(observation, bad, inlet):
    with pytest.raises(ValueError):
        TOOL.adapt(
            observation,
            bad if inlet == "predictive" else [0.0] * 7,
            bad if inlet == "routing" else [0.0] * 7,
        )


def test_safe_explicit_write_check_no_clobber_and_no_history_change(tmp_path, prepared):
    target = tmp_path / "new"
    TOOL.write_new(target, prepared)
    TOOL.check(target, prepared)
    (target / "other_source_preparation.json").write_text("{}\n")
    TOOL.check(target, prepared)
    with pytest.raises(ValueError, match="no clobber"):
        TOOL.write_new(target, prepared)
    with pytest.raises(ValueError, match="overlap"):
        TOOL.write_new(TOOL.SOURCE / "forbidden", prepared)
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path / "absent")
    with pytest.raises(ValueError, match="symlink"):
        TOOL.write_new(alias, prepared)


def test_cli_check_blocks_all_model_imports_and_requires_explicit_operation():
    code = """
import builtins, importlib.abc, runpy, sys
original = builtins.__import__
def guard(name, *args, **kwargs):
    if name == "sparkbrain" or name.startswith("sparkbrain."):
        raise AssertionError("forbidden model import: " + name)
    return original(name, *args, **kwargs)
class Blocker(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("forbidden model import: " + fullname)
        return None
builtins.__import__ = guard
sys.meta_path.insert(0, Blocker())
sys.argv = [SCRIPT, "--check"]
runpy.run_path(SCRIPT, run_name="__main__")
assert not any(name == "sparkbrain" or name.startswith("sparkbrain.") for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", "SCRIPT=" + repr(str(SCRIPT)) + "\n" + code],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["model_calls"] == 0
    no_operation = subprocess.run(
        [sys.executable, "-B", str(SCRIPT)], capture_output=True, text=True, check=False
    )
    assert no_operation.returncode == 2
    assert "required" in no_operation.stderr


def test_teaching_schedule_projects_only_frozen_receipts(prepared):
    evaluator = json.loads(prepared["evaluator.json"])
    source = copy.deepcopy(evaluator)
    schedule = TOOL.teaching_schedule(evaluator)
    assert set(schedule) == {"S", "R"}
    for arm, rows in schedule.items():
        assert len(rows) == 2
        for index, (row, outcome) in enumerate(zip(rows, (0.8, -0.8), strict=True), 64):
            assert row == {
                "receipt_id": f"m1-path-20261002-{arm}-receipt-{index:06d}",
                "event_id": f"m1-path-20261002-{index:06d}",
                "outcome": outcome,
                "delivery_ms": float(index * 200 + 100),
            }
    assert evaluator == source
    assert TOOL.teaching_schedule({"teaching": evaluator["teaching"]}) == schedule
    evaluator["queries"] = object()  # Query fields are never inspected by this projection.
    assert TOOL.teaching_schedule(evaluator) == schedule
    schedule["S"][0]["outcome"] = 100.0
    assert evaluator["teaching"][0]["outcome"] == 0.8


@pytest.mark.parametrize("change", ["sign", "receipt", "delivery", "event", "extra", "bool"])
def test_teaching_schedule_rejects_undeclared_receipts(prepared, change):
    evaluator = json.loads(prepared["evaluator.json"])
    row = evaluator["teaching"][0]
    if change == "sign":
        row["outcome"] = -0.8
    elif change == "receipt":
        row["receipt_ids"]["S"] = row["receipt_ids"]["R"]
    elif change == "delivery":
        row["delivery_time_ms"] = row["decision_time_ms"]
    elif change == "event":
        row["event_id"] = "m1-path-20261002-000066"
    elif change == "extra":
        row["target"] = "alpha"
    else:
        row["outcome"] = True
    with pytest.raises(ValueError, match="frozen teaching row"):
        TOOL.teaching_schedule(evaluator)
