"""Data-only verifier tests; synthetic dictionaries/files never execute a model."""

from __future__ import annotations

import ast
import base64
import copy
import hashlib
import importlib.util
import io
import json
import math
import subprocess
import sys
import tarfile
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/verify_plasticity_retention_run.py"
SPEC = importlib.util.spec_from_file_location("retention_verifier_tests", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True) + "\n").encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def delta_case():
    return (
        [
            {"source_id": 7, "target_id": 8, "plastic": True},
            {"source_id": 4, "target_id": 5, "plastic": True},
            {"source_id": 2, "target_id": 1, "plastic": True},
            {"source_id": 1, "target_id": 3, "plastic": False},
            {"source_id": 1, "target_id": 2, "plastic": True},
        ],
        [
            {"unit_id": 5, "time_ms": 20.0},
            {"unit_id": 2, "time_ms": 10.0},
            {"unit_id": 1, "time_ms": 0.0},
            {"unit_id": 4, "time_ms": 20.0},
            {"unit_id": 3, "time_ms": 30.0},
        ],
        {
            "max_updates_per_step": 10,
            "tau_plus_ms": 10.0,
            "tau_minus_ms": 20.0,
            "depression_ratio": 0.5,
        },
    )


def make_audit(*, decay=0.9, writes=True):
    arm = {"eligibility_decay": decay, "learning_rate": 0.2, "enable_weight_learning": writes}
    before = {"1:2": 1.0, "2:1": -1.0, "9:10": 2.0, "11:12": 1e-9}
    weights = {"1:2": 1.3, "2:1": -1.3, "9:10": 0.2}
    updates, changes, expected = [], [], {}
    for key, value in (("1:2", 1.0), ("2:1", -1.0)):
        carry = decay * value
        eligibility = carry + value
        proposal = weights[key] + 0.2 * eligibility
        target = max(-1.4, min(1.4, proposal)) if writes else weights[key]
        change = target - weights[key]
        updates.append(
            {
                "edge": key,
                "pre_eligibility": value,
                "decayed_carry": carry,
                "current_delta": value,
                "eligibility_after": eligibility,
                "weight_before": weights[key],
                "unclipped_proposal": proposal,
                "weight_expected": target,
                "actual_delta_weight": change,
                "weight_write_enabled": writes,
                "clipped": bool(writes and target != proposal),
            }
        )
        expected[key] = eligibility
        changes.append(change)
    if decay:
        expected["9:10"] = 2.0 * decay
    audit = {
        "pre_eligibility": copy.deepcopy(before),
        "post_eligibility": expected,
        "updates": updates,
        "actual_weight_abs_change": math.fsum(abs(v) for v in changes),
        "actual_weight_signed_change": math.fsum(changes),
        "changed_weights": sum(v != 0 for v in changes),
        "clipped_weights": 2 if writes else 0,
        "delays_unchanged": True,
        "delay_map_sha256": "d" * 64,
        "observer_pair_evaluations": 2,
        "eligible_edge_work": 2,
        "extra_apply_calls": 0,
    }
    return audit, arm, before, weights


@pytest.fixture
def loaded_case(tmp_path):
    root, stdlib = tmp_path / "source", tmp_path / "stdlib"
    modules = {
        "__main__": "scripts/run_plasticity_retention.py",
        "retention_support": "scripts/plasticity_retention_support.py",
        "retention_contract": "scripts/plasticity_retention_contract.py",
        "retention_published_predecessor": "scripts/temporal_reuse_loop_probe.py",
        "sparkbrain": "src/sparkbrain/__init__.py",
        "sparkbrain.v04": "src/sparkbrain/v04/__init__.py",
        "sparkbrain.v04.contracts": "src/sparkbrain/v04/contracts.py",
        "sparkbrain.v05": "src/sparkbrain/v05/__init__.py",
        "sparkbrain.v05.brain": "src/sparkbrain/v05/brain.py",
        "sparkbrain.v05.plasticity": "src/sparkbrain/v05/plasticity.py",
    }
    frozen = {
        "execution_source_root": str(root),
        "sources": {path: hashlib.sha256(path.encode()).hexdigest() for path in modules.values()},
    }
    dependencies = {"stdlib_path": str(stdlib), "stdlib_files": {"json/__init__.py": "a" * 64}}
    record = {
        name: str(root / path) + ":" + frozen["sources"][path] for name, path in modules.items()
    }
    record.update(
        {
            "json": str(stdlib / "json/__init__.py") + ":" + "a" * 64,
            "sys": "interpreter:built-in",
            "_frozen_importlib": "interpreter:frozen",
        }
    )
    return record, frozen, dependencies


def test_verifier_source_and_import_are_model_free():
    roots = set()
    for node in ast.walk(ast.parse(SOURCE.read_text())):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0
            roots.add(node.module.split(".")[0])
    assert roots <= sys.stdlib_module_names
    code = """
import builtins, runpy, sys
original = builtins.__import__
def guard(name, *args, **kwargs):
    if name.startswith('sparkbrain') or 'temporal_reuse_loop_probe' in name:
        raise AssertionError('forbidden runtime import: ' + name)
    return original(name, *args, **kwargs)
builtins.__import__ = guard
runpy.run_path(sys.argv[1])
assert not any(name.startswith('sparkbrain') for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", code, str(SOURCE)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr


def test_current_deltas_reconstruct_signed_work_without_mutating_inputs(delta_case):
    edges, spikes, config = delta_case
    before = copy.deepcopy(delta_case)
    assert TOOL.current_deltas(edges, spikes, config) == [
        ("1:2", math.exp(-1)),
        ("2:1", -0.5 * math.exp(-0.5)),
    ]
    assert delta_case == before
    assert TOOL.delta_accounting(edges, spikes, config)[1] == 3


@pytest.mark.parametrize("limit,expected_count", [(0, 0), (1, 1), (2, 2)])
def test_current_deltas_enforce_sorted_nonzero_update_cap(delta_case, limit, expected_count):
    edges, spikes, config = delta_case
    config["max_updates_per_step"] = limit
    result = TOOL.current_deltas(edges, spikes, config)
    assert len(result) == expected_count
    if result:
        assert result[0][0] == "1:2"
    assert TOOL.delta_accounting(edges, spikes, config)[1] == expected_count


def test_current_deltas_preserve_cancellation_and_equal_time_no_write(delta_case):
    _, _, config = delta_case
    config.update(tau_minus_ms=10.0, depression_ratio=1.0)
    edges = [{"source_id": 1, "target_id": 2, "plastic": True}]
    spikes = [{"unit_id": 1, "time_ms": t} for t in (2.0, 0.0, 1.0)]
    spikes.append({"unit_id": 2, "time_ms": 1.0})
    assert TOOL.current_deltas(edges, spikes, config) == []
    assert TOOL.delta_accounting(edges, spikes, config)[1] == 3
    assert TOOL.current_deltas(edges, [], config) == []


@pytest.mark.parametrize("decay,writes", [(0.9, True), (0.0, True), (0.9, False)])
def test_verify_audit_reconstructs_carry_clipping_and_frozen_weight_cases(decay, writes):
    audit, arm, before, weights = make_audit(decay=decay, writes=writes)
    unchanged = copy.deepcopy((audit, arm, before))
    TOOL.verify_audit(audit, arm, before, weights, "d" * 64)
    assert (audit, arm, before) == unchanged
    assert weights == {"1:2": 1.4 if writes else 1.3, "2:1": -1.4 if writes else -1.3, "9:10": 0.2}


@pytest.mark.parametrize(
    "key,value",
    [
        ("pre_eligibility", 2.0),
        ("decayed_carry", 0.0),
        ("current_delta", 0.0),
        ("eligibility_after", 7.0),
        ("weight_before", 0.0),
        ("unclipped_proposal", 3.0),
        ("weight_expected", 0.0),
        ("actual_delta_weight", 0.0),
        ("weight_write_enabled", False),
        ("clipped", False),
    ],
)
def test_verify_audit_rejects_tampered_update_fields(key, value):
    audit, arm, before, weights = make_audit()
    audit["updates"][0][key] = value
    with pytest.raises(RuntimeError):
        TOOL.verify_audit(audit, arm, before, weights, "d" * 64)


@pytest.mark.parametrize(
    "key,value",
    [
        ("pre_eligibility", {}),
        ("post_eligibility", {}),
        ("actual_weight_abs_change", 0),
        ("actual_weight_signed_change", 1),
        ("changed_weights", 0),
        ("clipped_weights", 0),
        ("delays_unchanged", False),
        ("delay_map_sha256", "e" * 64),
        ("eligible_edge_work", 1),
        ("extra_apply_calls", 1),
    ],
)
def test_verify_audit_rejects_disconnected_history_totals_or_delays(key, value):
    audit, arm, before, weights = make_audit()
    audit[key] = value
    with pytest.raises(RuntimeError):
        TOOL.verify_audit(audit, arm, before, weights, "d" * 64)


@pytest.mark.parametrize("corruption", ["duplicate", "unknown"])
def test_verify_audit_rejects_duplicate_and_unknown_updated_edges(corruption):
    audit, arm, before, weights = make_audit()
    if corruption == "duplicate":
        audit["updates"].append(copy.deepcopy(audit["updates"][0]))
    else:
        audit["updates"][0]["edge"] = "100:101"
    with pytest.raises(RuntimeError, match="unknown/duplicate"):
        TOOL.verify_audit(audit, arm, before, weights, "d" * 64)


@pytest.mark.parametrize("case", ["none", "empty_counts", "tie", "majority"])
def test_prediction_selection_native_and_laplace_probabilities_are_distinct(case):
    supplied = {
        "start_ms": 100.0,
        "pulses": [
            {"time_ms": 102.0, "channel": "Q"},
            {"time_ms": 101.0, "channel": "A"},
        ],
    }
    activations = [
        {
            "assembly_id": "immature",
            "mature": False,
            "suppressed": False,
            "similarity": 1.0,
            "episode_count": 100,
        },
        {
            "assembly_id": "suppressed",
            "mature": True,
            "suppressed": True,
            "similarity": 1.0,
            "episode_count": 100,
        },
    ]
    if case != "none":
        activations += [
            {
                "assembly_id": "y",
                "mature": True,
                "suppressed": False,
                "similarity": 0.8,
                "episode_count": 2,
            },
            {
                "assembly_id": "w",
                "mature": True,
                "suppressed": False,
                "similarity": 0.8,
                "episode_count": 3,
            },
            {
                "assembly_id": "x",
                "mature": True,
                "suppressed": False,
                "similarity": 0.8,
                "episode_count": 3,
            },
        ]
    counts = {"0": 2, "1": 5} if case == "majority" else {"0": 2, "1": 2}
    if case == "empty_counts":
        counts = {}
    aid = None if case == "none" else "x"
    label = "1" if case == "majority" else "0" if case == "tie" else None
    probability = 6 / 9 if case == "majority" else 0.5
    confidence = 5 / 7 if case == "majority" else 0.5 if case == "tie" else 0.0
    row = {
        "assembly_id": aid,
        "mature": aid is not None,
        "native": int(label) if label is not None else None,
        "p1": probability,
        "raw_result": {
            "assembly_activations": activations,
            "prediction": {"assembly_id": aid, "value": label, "confidence": confidence},
            "raw_pulses": sorted(supplied["pulses"], key=lambda p: (p["time_ms"], p["channel"])),
            "end_ms": 172.0,
        },
    }
    TOOL.verify_prediction(row, supplied, {"x": counts, "y": {"0": 100}})
    row["raw_result"]["prediction"]["confidence"] += 0.01
    with pytest.raises(RuntimeError, match="native/selection/readout"):
        TOOL.verify_prediction(row, supplied, {"x": counts, "y": {"0": 100}})


def assembly_pattern(start=0.0, units=(1, 2), bins=(0, 2)):
    sequence = [list(pair) for pair in zip(units, bins, strict=True)]
    payload = {
        "sequence": sequence,
        "source_cascade_id": f"cascade-{start}",
        "source_kind": "internal_reservoir",
    }
    return {
        "pattern_id": "pattern-" + TOOL.digest(payload)[:16],
        "start_ms": start,
        "end_ms": start + 1,
        "ordered_units": list(units),
        "relative_bins": list(bins),
        "unit_ids": sorted(set(units)),
        "spike_count": len(units),
        "source_cascade_id": payload["source_cascade_id"],
        "source_kind": "internal_reservoir",
    }


def assembly_candidate(pattern, aid="assembly-0001", episodes=("prefix",), occurrences=None):
    occurrences = len(episodes) if occurrences is None else occurrences
    return {
        "assembly_id": aid,
        "prototype": copy.deepcopy(pattern),
        "occurrences": occurrences,
        "episode_ids": sorted(episodes),
        "episode_count": len(episodes),
        "first_seen_ms": pattern["end_ms"],
        "last_seen_ms": pattern["end_ms"],
        "similarity_sum": float(occurrences),
        "mean_similarity": 1.0,
    }


def assembly_activation(candidate, pattern, *, mature=False, suppressed=False):
    return {
        "assembly_id": candidate["assembly_id"],
        "pattern_id": pattern["pattern_id"],
        "time_ms": pattern["end_ms"],
        "similarity": 1.0,
        "occurrences": candidate["occurrences"],
        "episode_count": candidate["episode_count"],
        "mature": mature,
        "unit_ids": candidate["prototype"]["unit_ids"],
        "suppressed": suppressed,
    }


def assembly_state(candidates=None, **config):
    settings = {
        "similarity_threshold": 0.66,
        "mature_episodes": 2,
        "max_candidates": 2,
        "stale_after_ms": 10.0,
        "immature_stale_episodes": 1,
    }
    settings.update(config)
    return {
        "config": settings,
        "candidates": candidates or {},
        "suppressed": [],
        "next_id": len(candidates or {}) + 1,
    }


@pytest.fixture
def prototype_history_case():
    prototype, current = assembly_pattern(), assembly_pattern(20.0)
    prior = assembly_candidate(prototype)
    prefix = assembly_state({"assembly-0001": prior})
    updated = assembly_candidate(prototype, episodes=("prefix", "suffix-1"))
    updated["last_seen_ms"] = current["end_ms"]
    final = copy.deepcopy(prefix)
    final["candidates"]["assembly-0001"] = updated
    rows = [
        {
            "occurrence_id": "suffix-1",
            "raw_result": {
                "patterns": [current],
                "assembly_activations": [assembly_activation(updated, current, mature=True)],
            },
            "candidate_prototypes": {"assembly-0001": prototype},
        }
    ]
    return rows, prefix, final, {"enable_assembly": True, "min_pattern_spikes": 2}


def test_prototypes_remain_fixed_to_prefix_with_source_valid_metadata(prototype_history_case):
    before = copy.deepcopy(prototype_history_case)
    TOOL.verify_prototype_history(*prototype_history_case)
    assert prototype_history_case == before


def test_suppressed_candidate_keeps_its_fixed_prototype_and_suppressed_activation(
    prototype_history_case,
):
    rows, prefix, final, brain_config = prototype_history_case
    prefix["suppressed"] = final["suppressed"] = ["assembly-0001"]
    rows[0]["raw_result"]["assembly_activations"][0]["suppressed"] = True
    TOOL.verify_prototype_history(rows, prefix, final, brain_config)


def test_equal_prototype_matches_use_stable_assembly_identifier_tiebreak(prototype_history_case):
    rows, prefix, final, brain_config = prototype_history_case
    other = copy.deepcopy(prefix["candidates"]["assembly-0001"])
    other["assembly_id"] = "assembly-0002"
    prefix["candidates"]["assembly-0002"] = copy.deepcopy(other)
    final["candidates"]["assembly-0002"] = copy.deepcopy(other)
    prefix["next_id"] = final["next_id"] = 3
    rows[0]["candidate_prototypes"]["assembly-0002"] = copy.deepcopy(other["prototype"])
    TOOL.verify_prototype_history(rows, prefix, final, brain_config)
    rows[0]["raw_result"]["assembly_activations"][0]["assembly_id"] = "assembly-0002"
    with pytest.raises(RuntimeError, match="activation/prototype history"):
        TOOL.verify_prototype_history(rows, prefix, final, brain_config)


def test_new_prototype_comes_from_first_creating_pattern_and_counts_unique_episodes():
    first, second = assembly_pattern(), assembly_pattern(5)
    created = assembly_candidate(first, episodes=("suffix-1",))
    repeated = assembly_candidate(first, episodes=("suffix-1",), occurrences=2)
    repeated["last_seen_ms"] = second["end_ms"]
    prefix = assembly_state()
    final = assembly_state({"assembly-0001": repeated})
    rows = [
        {
            "occurrence_id": "suffix-1",
            "candidate_prototypes": {"assembly-0001": first},
            "raw_result": {
                "patterns": [first, second],
                "assembly_activations": [
                    assembly_activation(created, first),
                    assembly_activation(repeated, second),
                ],
            },
        }
    ]
    TOOL.verify_prototype_history(
        rows, prefix, final, {"enable_assembly": True, "min_pattern_spikes": 2}
    )
    rows[0]["candidate_prototypes"]["assembly-0001"] = second
    with pytest.raises(RuntimeError, match="candidate prototype history"):
        TOOL.verify_prototype_history(
            rows, prefix, final, {"enable_assembly": True, "min_pattern_spikes": 2}
        )


@pytest.mark.parametrize("case", ["stale_immature", "mature", "boundary", "spare_capacity"])
def test_prototype_pruning_requires_failed_match_capacity_immaturity_and_strict_age(case):
    old = assembly_pattern()
    current = assembly_pattern(10 if case == "boundary" else 20, units=(3, 4))
    episodes = ("prefix-1", "prefix-2") if case == "mature" else ("prefix-1",)
    candidate = assembly_candidate(old, episodes=episodes)
    prefix = assembly_state(
        {"assembly-0001": candidate}, max_candidates=2 if case == "spare_capacity" else 1
    )
    prefix["suppressed"] = ["assembly-0001"]
    final = copy.deepcopy(prefix)
    activations = []
    if case in ("stale_immature", "spare_capacity"):
        if case == "stale_immature":
            final["candidates"] = {}
            final["suppressed"] = []
        created = assembly_candidate(current, aid="assembly-0002", episodes=("suffix-1",))
        final["candidates"]["assembly-0002"] = created
        final["next_id"] = 3
        activations = [assembly_activation(created, current)]
    rows = [
        {
            "occurrence_id": "suffix-1",
            "candidate_prototypes": {aid: c["prototype"] for aid, c in final["candidates"].items()},
            "raw_result": {"patterns": [current], "assembly_activations": activations},
        }
    ]
    TOOL.verify_prototype_history(
        rows, prefix, final, {"enable_assembly": True, "min_pattern_spikes": 2}
    )


@pytest.mark.parametrize(
    "corruption",
    [
        "rewrite",
        "drop",
        "invent",
        "activation_units",
        "pattern",
        "next_id",
        "final_metadata",
        "final_config",
    ],
)
def test_prototype_history_rejects_disconnected_records(prototype_history_case, corruption):
    rows, prefix, final, brain_config = prototype_history_case
    if corruption == "rewrite":
        rows[0]["candidate_prototypes"]["assembly-0001"] = assembly_pattern(999)
    elif corruption == "drop":
        rows[0]["candidate_prototypes"] = {}
    elif corruption == "invent":
        rows[0]["candidate_prototypes"]["assembly-0999"] = assembly_pattern(999)
    elif corruption == "activation_units":
        rows[0]["raw_result"]["assembly_activations"][0]["unit_ids"] = [3, 4]
    elif corruption == "pattern":
        rows[0]["raw_result"]["patterns"][0] = assembly_pattern(20, units=(3, 4))
    elif corruption == "next_id":
        final["next_id"] += 1
    elif corruption == "final_metadata":
        final["candidates"]["assembly-0001"]["occurrences"] += 1
    else:
        final["config"]["max_candidates"] += 1
    with pytest.raises(RuntimeError, match="prototype history"):
        TOOL.verify_prototype_history(rows, prefix, final, brain_config)


def test_no_pattern_or_below_threshold_pattern_cannot_prune_existing_candidate():
    prototype = assembly_pattern()
    prefix = assembly_state({"assembly-0001": assembly_candidate(prototype)}, max_candidates=1)
    rows = [
        {
            "occurrence_id": "suffix-1",
            "candidate_prototypes": {"assembly-0001": prototype},
            "raw_result": {
                "patterns": [assembly_pattern(99, units=(7,), bins=(0,))],
                "assembly_activations": [],
            },
        }
    ]
    TOOL.verify_prototype_history(
        rows, prefix, copy.deepcopy(prefix), {"enable_assembly": True, "min_pattern_spikes": 2}
    )
    rows[0]["candidate_prototypes"] = {}
    with pytest.raises(RuntimeError, match="candidate prototype history"):
        TOOL.verify_prototype_history(
            rows, prefix, copy.deepcopy(prefix), {"enable_assembly": True, "min_pattern_spikes": 2}
        )


def test_pattern_score_recalculates_order_units_timing_and_partial_subsequences():
    left = assembly_pattern()
    assert TOOL.pattern_score(left, assembly_pattern(100)) == 1.0
    assert TOOL.pattern_score(left, assembly_pattern(units=(3, 4))) == 0.2
    assert TOOL.pattern_score(left, assembly_pattern(bins=(0, 4))) == 0.8 + 0.2 * math.exp(-0.5)
    partial = assembly_pattern(units=(1, 9, 2), bins=(0, 1, 2))
    assert TOOL.pattern_score(left, partial) == pytest.approx(0.55 * (2 / 3) + 0.25 * (2 / 3) + 0.2)


def call_events():
    return [
        {"kind": "outer", "phase": "intent", "number": 1},
        {"kind": "inner", "phase": "intent", "number": 1},
        {"kind": "inner", "phase": "return", "number": 1},
        {"kind": "inner", "phase": "intent", "number": 2},
        {"kind": "inner", "phase": "return", "number": 2},
        {"kind": "outer", "phase": "return", "number": 1},
    ]


def test_call_counts_require_complete_ordered_nested_journal():
    events = call_events()
    before = copy.deepcopy(events)
    assert TOOL.count_calls(events, {"outer": 1, "inner": 2, "forbidden": 0}) == {
        "outer": 1,
        "inner": 2,
    }
    assert events == before


@pytest.mark.parametrize("number", [True, 1.0, "1", None])
def test_call_ordinals_must_be_integers_not_bool_or_coercible_values(number):
    events = call_events()
    events[0]["number"] = number
    with pytest.raises(RuntimeError, match="method ordinal type"):
        TOOL.count_calls(events, {"outer": 1, "inner": 2})


@pytest.mark.parametrize(
    "corruption",
    [
        "unclosed",
        "return_first",
        "crossed",
        "skip_ordinal",
        "reused_ordinal",
        "over_budget",
        "unknown_kind",
        "error",
        "unknown_phase",
        "missing_call",
    ],
)
def test_call_counts_reject_invalid_or_incomplete_journals(corruption):
    events = call_events()
    if corruption == "unclosed":
        events.pop()
    elif corruption == "return_first":
        events.insert(0, {"kind": "outer", "phase": "return", "number": 1})
    elif corruption == "crossed":
        events[2], events[-1] = events[-1], events[2]
    elif corruption == "skip_ordinal":
        events[1]["number"] = 2
    elif corruption == "reused_ordinal":
        events[3]["number"] = 1
    elif corruption == "over_budget":
        events += [{"kind": "outer", "phase": "intent", "number": 2}]
    elif corruption == "unknown_kind":
        events[1]["kind"] = "other"
    elif corruption == "error":
        events[2]["phase"] = "error"
    elif corruption == "unknown_phase":
        events[2]["phase"] = "complete"
    else:
        del events[3:5]
    with pytest.raises(RuntimeError):
        TOOL.count_calls(events, {"outer": 1, "inner": 2})


def test_verify_loaded_accepts_only_frozen_origin_and_digest_membership(loaded_case):
    record, frozen, dependencies = loaded_case
    TOOL.verify_loaded(record, frozen, dependencies)


@pytest.mark.parametrize("corruption", ["omit", "builtin", "wrong_runtime_file"])
def test_required_runtime_names_cannot_be_omitted_or_rebound(loaded_case, corruption):
    record, frozen, dependencies = loaded_case
    if corruption == "omit":
        record.pop("sparkbrain.v05.brain")
    elif corruption == "builtin":
        record["sparkbrain.v05.brain"] = "interpreter:built-in"
    else:
        record["sparkbrain.v04.contracts"] = record["sparkbrain.v05.brain"]
    with pytest.raises(RuntimeError):
        TOOL.verify_loaded(record, frozen, dependencies)


@pytest.mark.parametrize(
    "corruption",
    ["empty", "source_digest", "source_path", "stdlib_digest", "outside", "interpreter_kind"],
)
def test_verify_loaded_rejects_missing_or_unpinned_bindings(loaded_case, corruption):
    record, frozen, dependencies = loaded_case
    if corruption == "empty":
        record.clear()
    elif corruption == "source_digest":
        record["sparkbrain.v05.brain"] = record["sparkbrain.v05.brain"].rsplit(":", 1)[0] + ":bad"
    elif corruption == "source_path":
        record["sparkbrain.v05.brain"] = (
            frozen["execution_source_root"] + "/unlisted.py:" + "a" * 64
        )
    elif corruption == "stdlib_digest":
        record["json"] = record["json"].rsplit(":", 1)[0] + ":bad"
    elif corruption == "outside":
        record["json"] = "/another-installation/json.py:" + "a" * 64
    else:
        record["sys"] = "interpreter:unreviewed"
    with pytest.raises(RuntimeError):
        TOOL.verify_loaded(record, frozen, dependencies)


@pytest.mark.parametrize(
    "manifest,commit", [("", "a" * 40), ("a" * 64, ""), ("a" * 63, "b" * 40), ("a" * 64, "b" * 39)]
)
def test_verify_requires_both_independent_pins_before_reading_artifacts(
    tmp_path, monkeypatch, manifest, commit
):
    def forbidden_read(_path):
        pytest.fail("missing independent pins must fail before artifact reads")

    monkeypatch.setattr(TOOL, "sha", forbidden_read)
    with pytest.raises(RuntimeError, match="explicit authority pins"):
        TOOL.verify(tmp_path / "output", tmp_path / "freeze", manifest, commit)


def test_verify_rejects_tampered_freeze_against_caller_pin(tmp_path):
    freeze = tmp_path / "freeze"
    expected = write_json(freeze / "manifest.json", {"schema": "reviewed"})
    write_json(freeze / "manifest.json", {"schema": "altered"})
    with pytest.raises(RuntimeError, match="authoritative freeze pin"):
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40)


def test_verify_rejects_tampered_dependencies_against_frozen_pin(tmp_path):
    freeze = tmp_path / "freeze"
    dependency_pin = write_json(freeze / "dependencies.json", {"stdlib": "reviewed"})
    expected = write_json(
        freeze / "manifest.json",
        {
            "generated": {"dependencies.json": dependency_pin},
            "sources": {},
        },
    )
    write_json(freeze / "dependencies.json", {"stdlib": "altered"})
    with pytest.raises(RuntimeError, match="dependency authority pin"):
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40)


def test_verify_rejects_auditor_source_changes_even_with_intact_freeze(tmp_path, monkeypatch):
    freeze, root = tmp_path / "freeze", tmp_path / "source"
    dependency_pin = write_json(freeze / "dependencies.json", {})
    source_pin = write_json(root / "audit.json", {"reviewed": True})
    expected = write_json(
        freeze / "manifest.json",
        {
            "generated": {"dependencies.json": dependency_pin},
            "sources": {"audit.json": source_pin},
        },
    )
    write_json(root / "audit.json", {"reviewed": False})
    monkeypatch.setattr(TOOL, "ROOT", root)
    with pytest.raises(RuntimeError, match="frozen audit/source mismatch"):
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40)


def test_verify_rejects_preparation_changes_against_independent_input_pins(tmp_path, monkeypatch):
    freeze, preparation = tmp_path / "freeze", tmp_path / "preparation"
    dependency_pin = write_json(freeze / "dependencies.json", {})
    expected = write_json(
        freeze / "manifest.json",
        {
            "generated": {"dependencies.json": dependency_pin},
            "sources": {},
        },
    )
    expected_input = write_json(preparation / "inputs.json", {"reviewed": True})
    write_json(preparation / "inputs.json", {"reviewed": False})
    monkeypatch.setattr(TOOL, "PINS", {"inputs.json": expected_input})
    monkeypatch.setattr(TOOL, "PREPARATION", preparation)
    with pytest.raises(RuntimeError, match="published input authority pin"):
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40)


@pytest.mark.parametrize("omitted", ["--expected-manifest-sha256", "--expected-source-commit"])
def test_verifier_cli_cannot_infer_missing_authority_pin(tmp_path, omitted):
    arguments = {
        "--output": str(tmp_path / "output"),
        "--freeze": str(tmp_path / "freeze"),
        "--expected-manifest-sha256": "a" * 64,
        "--expected-source-commit": "b" * 40,
    }
    arguments.pop(omitted)
    command = [sys.executable, "-B", str(SOURCE)]
    for key, value in arguments.items():
        command.extend([key, value])
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    assert result.returncode == 2
    assert omitted in result.stderr
    assert not (tmp_path / "output").exists()


def write_lines(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def seal_fixture(output):
    write_json(
        output / "file-manifest.json",
        {
            str(path.relative_to(output)): TOOL.sha(path)
            for path in output.rglob("*")
            if path.is_file()
            and path not in (output / "file-manifest.json", output / "result.json")
        },
    )


def synthetic_calls(v05, pairs):
    """Construct journal data only; no function from a model is ever called."""
    counts, events = Counter(), []

    def begin(kind):
        counts[kind] += 1
        events.append({"kind": kind, "phase": "intent", "number": counts[kind]})

    def end(kind):
        events.append({"kind": kind, "phase": "return", "number": counts[kind]})

    begin("wrapper_load")
    begin("wrapper_init")
    if v05:
        begin("v05_init")
        end("v05_init")
    end("wrapper_init")
    if v05:
        begin("native_load")
        begin("v05_init")
        end("v05_init")
        end("native_load")
    end("wrapper_load")
    for _ in range(pairs):
        begin("predict")
        if v05:
            begin("v05_episode")
            begin("apply")
            end("apply")
            end("v05_episode")
        end("predict")
        begin("outcome")
        if v05:
            begin("v05_outcome")
            end("v05_outcome")
        end("outcome")
    return events, dict(counts)


@pytest.fixture(scope="module")
def synthetic_retained_run(tmp_path_factory):
    """A fabricated validator fixture, never a retention execution or result.

    Only the already-published prefix JSON is decoded. Subsequent dictionaries
    contain synthetic no-spike/no-selection rows; no checkpoint loader or model
    is imported. This tests consistency checks, not authenticity or run fidelity.
    """
    root = tmp_path_factory.mktemp("synthetic-retention-validator")
    output, freeze = root / "synthetic-output", root / "synthetic-freeze"
    output.mkdir()
    jobs_record = TOOL.read(TOOL.PREPARATION / "jobs.json")
    jobs = jobs_record["jobs"]
    inputs = TOOL.read(TOOL.PREPARATION / "inputs.json")["streams"]
    prefix_records = TOOL.read(TOOL.PREPARATION / "prefix_sources.json")
    protocol = TOOL.read(ROOT / "protocols/plasticity_retention_bounded_v1.json")
    transport = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
    parts = TOOL.read(transport / "transport_manifest.json")["parts"]
    archive = b"".join(base64.b64decode((transport / part["path"]).read_bytes()) for part in parts)
    assert hashlib.sha256(archive).hexdigest() == prefix_records["archive_sha256"]
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as stream:
        for name, prefix in prefix_records["prefixes"].items():
            destination = output / "prefixes" / name
            destination.mkdir(parents=True)
            for member in prefix["checkpoint_members"]:
                source = stream.extractfile(member)
                assert source is not None
                raw = source.read()
                assert hashlib.sha256(raw).hexdigest() == prefix["files_sha256"][member]
                (destination / Path(member).name).write_bytes(raw)
    modules = {
        "sparkbrain.v05.brain": "src/sparkbrain/v05/brain.py",
        "sparkbrain.v05.plasticity": "src/sparkbrain/v05/plasticity.py",
        "retention_published_predecessor": "scripts/temporal_reuse_loop_probe.py",
        "retention_contract": "scripts/plasticity_retention_contract.py",
    }
    source_pins = {path: TOOL.sha(ROOT / path) for path in modules.values()}
    dep_pin = write_json(
        freeze / "dependencies.json",
        {
            "stdlib_path": str(root / "synthetic-stdlib"),
            "stdlib_files": {},
        },
    )
    manifest_pin = write_json(
        freeze / "manifest.json",
        {
            "synthetic_validator_fixture": True,
            "execution_source_root": str(ROOT),
            "sources": source_pins,
            "generated": {"dependencies.json": dep_pin},
        },
    )
    source_commit = "a" * 40
    gate = {
        "source_commit": source_commit,
        "manifest_sha256": manifest_pin,
        "synthetic_validator_fixture": True,
    }
    write_json(output / "execution-gate.json", gate)
    write_json(output / "job-plan.json", jobs_record)
    loaded = {name: str(ROOT / path) + ":" + source_pins[path] for name, path in modules.items()}
    groups, reservations, costs = {}, [], []
    cumulative = 0
    for job in jobs:
        work = output / "jobs" / job["job_id"]
        work.mkdir(parents=True)
        v05 = job["family"] == "v05"
        envelope = {
            "plan": job,
            "binding": gate,
            "cpu_limit": job["cpu_seconds"],
            "wall_limit": job["wall_seconds"],
        }
        write_json(work / "job.json", envelope)
        events, calls = synthetic_calls(v05, job["pairs"])
        write_lines(work / "calls.jsonl", events)
        for name in ("loaded-before-construction.json", "loaded-after-methods.json"):
            write_json(work / name, loaded)
        for channel in ("stdout", "stderr"):
            (work / (channel + ".bin")).write_bytes(b"")
        wrapper = TOOL.read(output / "prefixes" / job["prefix"] / "wrapper.json")
        brain, delays, eligibility = None, {}, {}
        if v05:
            brain = TOOL.read(output / "prefixes" / job["prefix"] / "brain.json")["payload"]
            before_hash = TOOL.digest(brain, newline=True)
            arm = protocol["arms"][job["arm"]]
            brain["config"].update(
                enable_weight_learning=arm["enable_weight_learning"], enable_delay_learning=False
            )
            brain["plasticity"]["config"].update(arm, enable_delay_learning=False)
            write_json(
                work / "configuration.json",
                {
                    "before_sha256": before_hash,
                    "after_sha256": TOOL.digest(brain, newline=True),
                    "brain_config": brain["config"],
                    "plasticity_config": brain["plasticity"]["config"],
                },
            )
            edges = brain["base"]["payload"]["field"]["connections"]
            delays = {f"{e['source_id']}:{e['target_id']}": e["delay_ms"] for e in edges}
            eligibility = brain["plasticity"]["eligibility"]
        rows, receipts, audits = [], [], []
        for index, supplied in enumerate(inputs[job["stream"]]):
            obs = {key: supplied[key] for key in ("occurrence_id", "start_ms", "pulses")}
            row = {
                "synthetic_validator_fixture": True,
                "index": index,
                "p1": 0.5,
                "native": None,
                "occurrence_id": supplied["occurrence_id"],
                "outcome": supplied["outcome"],
                "input_sha256": TOOL.digest(obs),
                "query_time_ms": supplied["start_ms"] + 72,
                "receipt_time_ms": supplied["receipt_time_ms"],
                "actual_weight_abs_change": 0,
            }
            if v05:
                post = {
                    key: value * arm["eligibility_decay"]
                    for key, value in eligibility.items()
                    if abs(value * arm["eligibility_decay"]) >= 1e-8
                }
                audits.append(
                    {
                        "index": index,
                        "pre_eligibility": eligibility,
                        "post_eligibility": post,
                        "updates": [],
                        "actual_weight_abs_change": 0,
                        "actual_weight_signed_change": 0,
                        "changed_weights": 0,
                        "clipped_weights": 0,
                        "delays_unchanged": True,
                        "delay_map_sha256": TOOL.digest(delays, newline=True),
                        "observer_pair_evaluations": 0,
                        "eligible_edge_work": 0,
                        "extra_apply_calls": 0,
                    }
                )
                eligibility = post
                brain["plasticity"]["eligibility"] = eligibility
                brain["episode_index"] += 1
                row.update(
                    {
                        "assembly_id": None,
                        "mature": False,
                        "readout_counts_before_receipt": copy.deepcopy(
                            brain["predictor"]["counts"]
                        ),
                        "candidate_prototypes": {
                            aid: copy.deepcopy(candidate["prototype"])
                            for aid, candidate in brain["assemblies"]["candidates"].items()
                        },
                        "raw_result": {
                            "emitted_pulses": [],
                            "v04_result": {"spikes": []},
                            "raw_pulses": sorted(
                                supplied["pulses"], key=lambda p: (p["time_ms"], p["channel"])
                            ),
                            "end_ms": supplied["start_ms"] + 72,
                            "patterns": [],
                            "assembly_activations": [],
                            "prediction": {"assembly_id": None, "value": None, "confidence": 0.0},
                        },
                    }
                )
            rows.append(row)
            wrapper["receipts"][supplied["occurrence_id"]] = supplied["outcome"]
            receipts.append(
                {
                    "index": index,
                    "occurrence_id": supplied["occurrence_id"],
                    "outcome": supplied["outcome"],
                    "wrapper_sha256": TOOL.digest(wrapper, newline=True),
                    "brain_sha256": TOOL.digest(brain, newline=True) if v05 else None,
                    "readout_counts_after_receipt": copy.deepcopy(brain["predictor"]["counts"])
                    if v05
                    else None,
                }
            )
        write_lines(work / "predictions.jsonl", rows)
        write_lines(work / "receipts.jsonl", receipts)
        if v05:
            write_lines(work / "apply.jsonl", audits)
        write_json(work / "final-state.json", {"wrapper": wrapper, "brain": brain})
        write_json(
            work / "result.json",
            {
                "status": "complete",
                "job_sha256": TOOL.digest(envelope),
                "completed_pairs": job["pairs"],
                "measurement_failed": False,
                "worker_cpu_seconds": 0.5,
                "worker_wall_seconds": 0.5,
                "worker_peak_rss_kib": 1024,
                "calls": {
                    "intents": calls,
                    "returns": calls,
                    "errors": {},
                    "observation_failed": False,
                },
            },
        )
        groups.setdefault(job["stream"].split("-")[0], {}).setdefault(job["condition"], {})[
            job["arm"]
        ] = rows
        cumulative += job["pairs"]
        reservations.append(
            {"job_id": job["job_id"], "pairs": job["pairs"], "cumulative_pairs": cumulative}
        )
        costs.append(
            {
                "job_id": job["job_id"],
                "exit_code": 0,
                "failure": None,
                "timed_out": False,
                "worker_cpu_seconds": 1.0,
                "driver_cpu_seconds": 0.1,
                "wall_seconds_before_cost": 1.0,
                "worker_peak_rss_kib": 1024,
                "driver_peak_rss_kib": 1024,
                "capture_consumed_bytes": {"stdout": 0, "stderr": 0},
                "capture_retained_bytes": {"stdout": 0, "stderr": 0},
                "known_discarded_bytes": {"stdout": 0, "stderr": 0},
                "unread_pipe_bytes": 0,
            }
        )
    scorer_spec = importlib.util.spec_from_file_location(
        "retention_synthetic_fixture_scorer", ROOT / "scripts/plasticity_retention_contract.py"
    )
    assert scorer_spec is not None and scorer_spec.loader is not None
    scorer = importlib.util.module_from_spec(scorer_spec)
    scorer_spec.loader.exec_module(scorer)
    scores = {seed: scorer.evaluate_fixture(rows, protocol) for seed, rows in groups.items()}
    assert not any(score["bounded_gate"] for score in scores.values())
    write_json(output / "scores.json", scores)
    write_lines(output / "reservations.jsonl", reservations)
    write_lines(output / "job-costs.jsonl", costs)
    write_json(
        output / "result.json",
        {
            "synthetic_validator_fixture": True,
            "status": "complete",
            "jobs_completed": 26,
            "pairs_completed": 768,
            "reserved_pairs": 768,
            "scientific_credit": 0,
            "measurement_failed": False,
            "aggregate_cpu_seconds": 30.0,
            "wall_seconds": 40.0,
            "bounded_gate": False,
            "job_costs": costs,
        },
    )
    seal_fixture(output)
    return output, freeze, manifest_pin, source_commit


def test_synthetic_retained_run_verifies_data_consistency_without_running_models(
    synthetic_retained_run,
):
    result = TOOL.verify(*synthetic_retained_run)
    assert result["valid_completion"] is True
    assert result["pairs"] == 768 and result["model_calls_during_audit"] == 0
    assert result["calls"]["predict"] == result["calls"]["outcome"] == 768
    assert result["calls"]["v05_init"] == 36
    assert "not rerun fidelity" in result["scope"]


@pytest.mark.parametrize(
    "corruption,message",
    [
        ("config", "configuration intervention"),
        ("final_config", "final configuration"),
        ("cost", "worker resource/capture"),
        ("negative_cost", "invalid worker cost"),
        ("readout", "readout history"),
        ("capture", "capture size"),
        ("pair_work", "observer pair-work"),
        ("clipped", "clipping total"),
        ("loaded", "required loaded module"),
        ("aggregate", "aggregate CPU omits"),
        ("p1", "probability/readout"),
        ("native", "native/selection/readout"),
        ("raw_input", "raw model input/time"),
        ("first_observable", "first-suffix"),
        ("prototype_row", "candidate prototype history"),
        ("prototype_final", "final assembly/prototype history"),
    ],
)
def test_resealed_synthetic_tampering_fails_semantic_audit(
    synthetic_retained_run, corruption, message
):
    output = synthetic_retained_run[0]
    work = output / "jobs" / "910075-return-C"
    changed = {}

    def retain(path):
        changed.setdefault(path, path.read_bytes())
        return path

    try:
        if corruption in ("config", "final_config", "prototype_final"):
            path = work / ("configuration.json" if corruption == "config" else "final-state.json")
            value = TOOL.read(path)
            if corruption == "prototype_final":
                candidate = next(iter(value["brain"]["assemblies"]["candidates"].values()))
                candidate["prototype"]["start_ms"] += 0.1
            else:
                config = (
                    value["brain_config"] if corruption == "config" else value["brain"]["config"]
                )
                config["enable_delay_learning"] = True
            write_json(retain(path), value)
            if corruption in ("final_config", "prototype_final"):
                receipts_path = work / "receipts.jsonl"
                receipts = TOOL.lines(receipts_path)
                receipts[-1]["brain_sha256"] = TOOL.digest(value["brain"], newline=True)
                write_lines(retain(receipts_path), receipts)
        elif corruption in ("cost", "negative_cost"):
            cost_path, terminal_path = output / "job-costs.jsonl", output / "result.json"
            costs, terminal = TOOL.lines(cost_path), TOOL.read(terminal_path)
            costs[0]["worker_cpu_seconds"] = 17 if corruption == "cost" else -1
            terminal["job_costs"] = costs
            terminal["aggregate_cpu_seconds"] = 100
            write_lines(retain(cost_path), costs)
            write_json(retain(terminal_path), terminal)
        elif corruption in (
            "readout",
            "p1",
            "native",
            "raw_input",
            "first_observable",
            "prototype_row",
        ):
            path = work / "predictions.jsonl"
            rows = TOOL.lines(path)
            if corruption == "readout":
                rows[0]["readout_counts_before_receipt"] = {}
                assert (
                    rows[0]["readout_counts_before_receipt"]
                    != rows[1]["readout_counts_before_receipt"]
                )
            elif corruption == "p1":
                rows[0]["p1"] = 0.75
            elif corruption == "native":
                rows[0]["native"] = 1
            elif corruption == "raw_input":
                rows[0]["raw_result"]["raw_pulses"][0]["magnitude"] += 0.1
            elif corruption == "prototype_row":
                next(iter(rows[0]["candidate_prototypes"].values()))["start_ms"] += 0.1
            else:
                rows[0]["raw_result"]["emitted_pulses"] = [{"synthetic_disagreement": True}]
            write_lines(retain(path), rows)
        elif corruption == "capture":
            retain(work / "stdout.bin").write_bytes(b"unreported capture")
        elif corruption in ("pair_work", "clipped"):
            path = work / "apply.jsonl"
            audits = TOOL.lines(path)
            key = "observer_pair_evaluations" if corruption == "pair_work" else "clipped_weights"
            audits[0][key] = 1
            write_lines(retain(path), audits)
        elif corruption == "loaded":
            path = work / "loaded-before-construction.json"
            value = TOOL.read(path)
            value["sparkbrain.v05.brain"] = "interpreter:built-in"
            write_json(retain(path), value)
        else:
            path = output / "result.json"
            value = TOOL.read(path)
            value["aggregate_cpu_seconds"] = 1
            write_json(retain(path), value)
        seal_fixture(output)
        with pytest.raises(RuntimeError, match=message):
            TOOL.verify(*synthetic_retained_run)
    finally:
        for path, raw in changed.items():
            path.write_bytes(raw)
        seal_fixture(output)
