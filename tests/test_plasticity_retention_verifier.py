"""Data-only verifier tests; synthetic dictionaries/files never execute a model."""

from __future__ import annotations

import ast
import base64
import contextlib
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
AUTHORITY_KINDS = ("review", "publication", "approval")
DUMMY_RECORD_PINS = {kind: "c" * 64 for kind in AUTHORITY_KINDS}
RESERVED_OBSERVATIONS = set()
RESERVED_MEMORY_PREFIXES = set()


def observation_fingerprint(value):
    return TOOL.digest({"start_ms": value["start_ms"], "pulses": value["pulses"]})


@pytest.fixture(scope="module", autouse=True)
def prevent_reserved_baseline_exposure():
    """Hash-only guards; never feed reserved inputs or states to baseline arithmetic."""
    preparation = ROOT / "artifacts/research/plasticity_retention_preparation_20261001"
    streams = json.loads((preparation / "inputs.json").read_bytes())["streams"]
    reserved_rows = [row for rows in streams.values() for row in rows]
    RESERVED_OBSERVATIONS.update(observation_fingerprint(row) for row in reserved_rows)
    prefixes = json.loads((preparation / "prefix_sources.json").read_bytes())["prefixes"]
    transport = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
    parts = json.loads((transport / "transport_manifest.json").read_bytes())["parts"]
    archive = b"".join(base64.b64decode((transport / part["path"]).read_bytes()) for part in parts)
    reserved_prefixes = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as stream:
        for name, record in prefixes.items():
            if not name.endswith(("-H", "-R")):
                continue
            member = next(
                value for value in record["checkpoint_members"] if value.endswith("wrapper.json")
            )
            source = stream.extractfile(member)
            assert source is not None
            raw = source.read()
            assert hashlib.sha256(raw).hexdigest() == record["files_sha256"][member]
            value = json.loads(raw)
            reserved_prefixes.append(value)
            RESERVED_MEMORY_PREFIXES.add(TOOL.digest(value, newline=True))
    raster, history = TOOL.memory_raster, TOOL.verify_memory_history

    def guarded_raster(supplied):
        assert observation_fingerprint(supplied) not in RESERVED_OBSERVATIONS, (
            "reserved study observation"
        )
        return raster(supplied)

    def guarded_history(arm, rows, receipts, observations, prefix, final):
        assert TOOL.digest(prefix, newline=True) not in RESERVED_MEMORY_PREFIXES, (
            "reserved study prefix"
        )
        return history(arm, rows, receipts, observations, prefix, final)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(TOOL, "memory_raster", guarded_raster)
        patch.setattr(TOOL, "verify_memory_history", guarded_history)
        yield reserved_rows[0], reserved_prefixes[0]


def interpreter_record():
    return {
        "python_version": sys.version,
        "executable_sha256": hashlib.sha256(
            Path(sys.executable).resolve().read_bytes()
        ).hexdigest(),
    }


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
        TOOL.verify(tmp_path / "output", tmp_path / "freeze", manifest, commit, DUMMY_RECORD_PINS)


def test_verify_rejects_tampered_freeze_against_caller_pin(tmp_path):
    freeze = tmp_path / "freeze"
    expected = write_json(freeze / "manifest.json", {"schema": "reviewed"})
    write_json(freeze / "manifest.json", {"schema": "altered"})
    with pytest.raises(RuntimeError, match="authoritative freeze pin"):
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40, DUMMY_RECORD_PINS)


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
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40, DUMMY_RECORD_PINS)


def test_verify_rejects_auditor_source_changes_even_with_intact_freeze(tmp_path, monkeypatch):
    freeze, root = tmp_path / "freeze", tmp_path / "source"
    dependency_pin = write_json(freeze / "dependencies.json", interpreter_record())
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
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40, DUMMY_RECORD_PINS)


def test_verify_rejects_preparation_changes_against_independent_input_pins(tmp_path, monkeypatch):
    freeze, preparation = tmp_path / "freeze", tmp_path / "preparation"
    dependency_pin = write_json(freeze / "dependencies.json", interpreter_record())
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
        TOOL.verify(tmp_path / "output", freeze, expected, "a" * 40, DUMMY_RECORD_PINS)


@pytest.mark.parametrize(
    "omitted",
    [
        "--expected-manifest-sha256",
        "--expected-source-commit",
        "--expected-review-sha256",
        "--expected-publication-sha256",
        "--expected-approval-sha256",
    ],
)
def test_verifier_cli_cannot_infer_missing_authority_pin(tmp_path, omitted):
    arguments = {
        "--output": str(tmp_path / "output"),
        "--freeze": str(tmp_path / "freeze"),
        "--expected-manifest-sha256": "a" * 64,
        "--expected-source-commit": "b" * 40,
        **{"--expected-" + kind + "-sha256": pin for kind, pin in DUMMY_RECORD_PINS.items()},
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


def synthetic_memory_step(state, supplied):
    """Make toy baseline records only; callers must supply non-study dictionaries."""
    assert observation_fingerprint(supplied) not in RESERVED_OBSERVATIONS, (
        "reserved study observation"
    )
    assert TOOL.digest(state, newline=True) not in RESERVED_MEMORY_PREFIXES, "reserved study prefix"
    vector = [0.0 for _ in range(410)]
    for pulse in supplied["pulses"]:
        t = pulse["time_ms"] - supplied["start_ms"]
        lo = int(t)
        frac = t - lo
        base = "ACFHIJKLMQ".index(pulse["channel"]) * 41
        vector[base + lo] += pulse["magnitude"] * (1 - frac)
        if frac:
            vector[base + lo + 1] += pulse["magnitude"] * frac
    denominator = sum(vector)
    vector = [v / denominator for v in vector]
    state["pending"] = {"id": supplied["occurrence_id"], "x": vector}
    if state["arm"] == "H":
        ranked = sorted(
            (sum(abs(v - x) for v, x in zip(vector, item["x"], strict=True)), i)
            for i, item in enumerate(state["memory"])
        )
        neighbors = [state["memory"][i] for _, i in ranked[:3]]
        probability = (1 + sum(item["y"] for item in neighbors)) / (2 + len(neighbors))
        comparisons = slots = len(state["memory"])
    else:
        comparisons = len(state["prototypes"]) + int(bool(state["prototypes"]))
        distances = [
            sum(abs(v - x) for v, x in zip(vector, item["x"], strict=True))
            for item in state["prototypes"]
        ]
        at = min(range(len(distances)), key=lambda i: (distances[i], i), default=None)
        if at is None or (distances[at] > 0.25 and len(distances) < 32):
            at = len(distances)
            state["prototypes"].append({"x": list(vector), "n": 0, "counts": [0, 0]})
        state["pending"]["prototype"] = at
        selected = state["prototypes"][at]
        probability = (1 + selected["counts"][1]) / (2 + sum(selected["counts"]))
        slots = len(state["prototypes"])
    fields = {
        "p1": probability,
        "native": None if probability == 0.5 else int(probability > 0.5),
        "prototype_comparisons": comparisons,
        "representation_slots": slots,
        "operational_sha256": TOOL.digest({"wrapper": state, "brain": None}),
        "live_state_bytes": len(
            (json.dumps(state, sort_keys=True, separators=(",", ":")) + "\n").encode()
        ),
        "actual_weight_abs_change": 0,
    }
    if state["arm"] == "H":
        state["memory"].append({"x": vector, "y": supplied["outcome"]})
        state["memory"] = state["memory"][-32:]
    else:
        selected = state["prototypes"][state["pending"]["prototype"]]
        count = selected["n"]
        selected["x"] = [
            (old * count + value) / (count + 1)
            for old, value in zip(selected["x"], vector, strict=True)
        ]
        selected["n"] += 1
        selected["counts"][supplied["outcome"]] += 1
    state["receipts"][supplied["occurrence_id"]] = supplied["outcome"]
    state["pending"] = None
    return fields


def synthetic_authority_gate(commit, manifest, output):
    gate = {
        "source_commit": commit,
        "manifest_sha256": manifest,
        "synthetic_validator_fixture": True,
        "records": {},
        "record_files": {},
    }
    for kind, flag in (
        ("review", "source_review_approved"),
        ("publication", "verified_published"),
        ("approval", "approved_for_execution"),
    ):
        value = {
            "synthetic_validator_fixture": True,
            flag: True,
            "source_commit": commit,
            "manifest_sha256": manifest,
            "output_root": str(output),
            "ceiling_pairs": 768,
            "record_url": "https://example.invalid/synthetic-validator/" + kind,
            "recorded_by": "synthetic pytest fixture, never an operational approval",
        }
        relative = "authority-records/" + kind + ".json"
        pin = write_json(output / relative, value)
        gate["records"][kind] = value
        gate["record_files"][kind] = {
            "path": relative,
            "sha256": pin,
            "bytes": (output / relative).stat().st_size,
        }
    return gate


@pytest.fixture(scope="module")
def synthetic_retained_run(tmp_path_factory, request):
    """A fabricated validator fixture, never a retention execution or result.

    Every prefix, observation and authority record is synthetic. Test-only pins
    replace production paths before verify() can read anything. H/R calculations
    never see published study prefixes or reserved suffix inputs.
    """
    root = tmp_path_factory.mktemp("synthetic-retention-validator")
    output, freeze = root / "synthetic-output", root / "synthetic-freeze"
    output.mkdir()
    protocol = TOOL.read(ROOT / "protocols/plasticity_retention_bounded_v1.json")
    protocol["synthetic_validator_fixture"] = True
    auditor_root, preparation = root / "synthetic-source", root / "synthetic-preparation"
    inputs, jobs, prefix_records = {}, [], {"prefixes": {}}
    for fixture in (100001, 100002):
        for family in ("S", "H", "R"):
            name = f"synthetic-{fixture}-{family}"
            destination = output / "prefixes" / name
            vector = [1.0] + [0.0] * 409
            wrapper = {
                "arm": family,
                "counts": [0, 0],
                "memory": [],
                "prototypes": [],
                "pending": None,
                "receipts": {},
            }
            if family == "H":
                wrapper["memory"] = [{"x": vector, "y": 0}]
            elif family == "R":
                wrapper["prototypes"] = [{"x": vector, "n": 2, "counts": [1, 1]}]
            members = {"wrapper.json": wrapper}
            if family == "S":
                prototype = assembly_pattern()
                members["brain.json"] = {
                    "payload": {
                        "config": {
                            "enable_weight_learning": True,
                            "enable_delay_learning": True,
                            "enable_assembly": True,
                            "min_pattern_spikes": 2,
                        },
                        "plasticity": {
                            "config": {
                                **protocol["arms"]["C"],
                                "max_updates_per_step": 2,
                                "tau_plus_ms": 18.0,
                                "tau_minus_ms": 24.0,
                                "depression_ratio": 0.75,
                                "enable_delay_learning": True,
                            },
                            "reward_trace": 1.0,
                            "eligibility": {"1:2": 0.25},
                        },
                        "base": {
                            "payload": {
                                "field": {
                                    "connections": [
                                        {
                                            "source_id": 1,
                                            "target_id": 2,
                                            "weight": 0.3,
                                            "delay_ms": 2.0,
                                            "plastic": True,
                                        }
                                    ]
                                }
                            }
                        },
                        "predictor": {"counts": {"assembly-0001": {"0": 2}}},
                        "assemblies": assembly_state(
                            {
                                "assembly-0001": assembly_candidate(
                                    prototype, episodes=("toy-prefix-1", "toy-prefix-2")
                                )
                            }
                        ),
                        "episode_index": 0,
                    }
                }
            prefix = {"checkpoint_members": [], "files_sha256": {}}
            for filename, content in members.items():
                member = name + "/" + filename
                prefix["checkpoint_members"].append(member)
                prefix["files_sha256"][member] = write_json(destination / filename, content)
            prefix_records["prefixes"][name] = prefix
        for condition, count, arms in (
            ("return", 32, ("C", "L", "G", "Fw", "H", "R")),
            ("stationary", 16, ("C", "L")),
            ("novel", 32, ("C", "L", "Fw", "H", "R")),
        ):
            stream = f"{fixture}-{condition}"
            rows = []
            for index in range(count):
                outcome = index % 2 if condition == "novel" else int(condition == "stationary")
                start = 1000.0 + 100 * index
                rows.append(
                    {
                        "occurrence_id": f"synthetic-occ-{index:06d}",
                        "start_ms": start,
                        "pulses": [
                            {
                                "channel": "A" if outcome == 0 else "C",
                                "magnitude": 1.0,
                                "time_ms": start + (index % 3) * 0.25,
                            },
                            {"channel": "Q", "magnitude": 1.0, "time_ms": start + 40},
                        ],
                        "outcome": outcome,
                        "receipt_time_ms": start + 80,
                    }
                )
            inputs[stream] = rows
            for arm in arms:
                v05 = arm not in ("H", "R")
                jobs.append(
                    {
                        "arm": arm,
                        "condition": condition,
                        "cpu_seconds": 16 if v05 else 3,
                        "wall_seconds": 20 if v05 else 5,
                        "family": "v05" if v05 else "ordinary_memory",
                        "pairs": count,
                        "job_id": stream + "-" + arm,
                        "stream": stream,
                        "prefix": f"synthetic-{fixture}-" + ("S" if v05 else arm),
                    }
                )
    jobs_record = {"synthetic_validator_fixture": True, "execution_authorized": False, "jobs": jobs}
    pins = {
        "inputs.json": write_json(preparation / "inputs.json", {"streams": inputs}),
        "jobs.json": write_json(preparation / "jobs.json", jobs_record),
        "prefix_sources.json": write_json(preparation / "prefix_sources.json", prefix_records),
    }
    protocol_pin = write_json(
        auditor_root / "protocols/plasticity_retention_bounded_v1.json", protocol
    )
    patch = pytest.MonkeyPatch()
    request.addfinalizer(patch.undo)
    patch.setattr(TOOL, "ROOT", auditor_root)
    patch.setattr(TOOL, "PREPARATION", preparation)
    patch.setattr(TOOL, "PINS", pins)
    patch.setattr(TOOL, "PROTOCOL_SHA", protocol_pin)
    modules = {
        "sparkbrain.v05.brain": "src/sparkbrain/v05/brain.py",
        "sparkbrain.v05.plasticity": "src/sparkbrain/v05/plasticity.py",
        "retention_published_predecessor": "scripts/temporal_reuse_loop_probe.py",
        "retention_contract": "scripts/plasticity_retention_contract.py",
    }
    source_pins = {}
    for path in modules.values():
        target = auditor_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if path == "scripts/plasticity_retention_contract.py":
            target.write_bytes((ROOT / path).read_bytes())
        else:
            target.write_text("# Synthetic origin artifact; never imported or executed.\n")
        source_pins[path] = TOOL.sha(target)
    dep_pin = write_json(
        freeze / "dependencies.json",
        {
            "stdlib_path": str(root / "synthetic-stdlib"),
            "stdlib_files": {},
            **interpreter_record(),
        },
    )
    manifest_pin = write_json(
        freeze / "manifest.json",
        {
            "synthetic_validator_fixture": True,
            "execution_source_root": str(auditor_root),
            "planned_output": str(output),
            "sources": source_pins,
            "generated": {"dependencies.json": dep_pin},
        },
    )
    source_commit = "a" * 40
    gate = synthetic_authority_gate(source_commit, manifest_pin, output)
    write_json(output / "execution-gate.json", gate)
    write_json(output / "job-plan.json", jobs_record)
    loaded = {
        name: str(auditor_root / path) + ":" + source_pins[path] for name, path in modules.items()
    }
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
            "record_paths": {
                kind: str(output / item["path"]) for kind, item in gate["record_files"].items()
            },
            "record_sha256": {kind: item["sha256"] for kind, item in gate["record_files"].items()},
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
            if not v05:
                row.update(synthetic_memory_step(wrapper, supplied))
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
    independent_record_pins = {kind: item["sha256"] for kind, item in gate["record_files"].items()}
    return output, freeze, manifest_pin, source_commit, independent_record_pins


def test_synthetic_retained_run_verifies_data_consistency_without_running_models(
    synthetic_retained_run,
):
    result = TOOL.verify(*synthetic_retained_run)
    assert result["valid_completion"] is True
    assert result["pairs"] == 768 and result["runtime_model_method_calls_during_audit"] == 0
    assert result["ordinary_memory_rows_reconstructed"] == 256
    assert result["v05_apply_rows_recomputed"] == 512
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
    work = output / "jobs" / "100001-return-C"
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


@pytest.mark.parametrize("kind", AUTHORITY_KINDS)
@pytest.mark.parametrize("value", [False, 1, "true", None])
def test_authority_flags_require_exact_true(tmp_path, kind, value):
    gate = synthetic_authority_gate("a" * 40, "b" * 64, tmp_path)
    flag = {
        "review": "source_review_approved",
        "publication": "verified_published",
        "approval": "approved_for_execution",
    }[kind]
    gate["records"][kind][flag] = value
    with pytest.raises(RuntimeError, match="authority flag"):
        TOOL.verify_authority_records(gate, "a" * 40, "b" * 64, str(tmp_path))


@pytest.mark.parametrize("kind", AUTHORITY_KINDS)
@pytest.mark.parametrize(
    "field,value",
    [
        ("source_commit", "c" * 40),
        ("manifest_sha256", "c" * 64),
        ("output_root", "/other"),
        ("ceiling_pairs", 769),
        ("ceiling_pairs", 768.0),
        ("record_url", " "),
        ("record_url", True),
        ("recorded_by", ""),
        ("recorded_by", 7),
    ],
)
def test_authority_scope_and_provenance_are_bound_to_external_expectations(
    tmp_path, kind, field, value
):
    gate = synthetic_authority_gate("a" * 40, "b" * 64, tmp_path)
    gate["records"][kind][field] = value
    with pytest.raises(RuntimeError, match="authority (scope|provenance)"):
        TOOL.verify_authority_records(gate, "a" * 40, "b" * 64, str(tmp_path))


@pytest.mark.parametrize(
    "pins", [None, {}, {"review": "c" * 64}, dict.fromkeys(AUTHORITY_KINDS, "not a hash")]
)
def test_external_authority_record_pins_are_required_before_artifact_reads(
    tmp_path, monkeypatch, pins
):
    monkeypatch.setattr(TOOL, "sha", lambda _: pytest.fail("must reject before artifact reads"))
    with pytest.raises(RuntimeError, match="independent authority record pins required"):
        TOOL.verify(tmp_path, tmp_path, "a" * 64, "b" * 40, pins)


def toy_memory_case(arm, *, memory=None, prototypes=None):
    prefix = {
        "arm": arm,
        "counts": [0, 0],
        "memory": memory or [],
        "prototypes": prototypes or [],
        "pending": None,
        "receipts": {},
    }
    supplied = {
        "occurrence_id": "toy-only-1",
        "start_ms": 100.0,
        "pulses": [{"channel": "A", "time_ms": 100.0, "magnitude": 1.0}],
        "outcome": 0,
    }
    final = copy.deepcopy(prefix)
    row = synthetic_memory_step(final, supplied)
    receipt = {
        "wrapper_sha256": TOOL.digest(final, newline=True),
        "brain_sha256": None,
        "readout_counts_after_receipt": None,
    }
    return row, receipt, supplied, prefix, final


def test_memory_raster_interpolates_channel_bins_and_normalizes_without_mutation():
    supplied = {
        "start_ms": 100.0,
        "pulses": [
            {"channel": "A", "time_ms": 100.25, "magnitude": 2.0},
            {"channel": "C", "time_ms": 101.0, "magnitude": 1.0},
        ],
    }
    original = copy.deepcopy(supplied)
    expected = [0.0] * 410
    expected[0], expected[1], expected[42] = 0.5, 1 / 6, 1 / 3
    assert TOOL.memory_raster(supplied) == expected
    assert supplied == original


def test_h_nearest_three_breaks_equal_distance_by_memory_index():
    vector = [1.0] + [0.0] * 409
    memory = [{"x": vector, "y": value} for value in (0, 1, 1, 0)]
    row, receipt, supplied, prefix, final = toy_memory_case("H", memory=memory)
    assert row["p1"] == 0.6 and row["native"] == 1
    assert row["prototype_comparisons"] == row["representation_slots"] == 4
    TOOL.verify_memory_history("H", [row], [receipt], [supplied], prefix, final)
    assert final["memory"][-1] == {"x": vector, "y": 0}


def test_h_retains_only_latest_32_receipts():
    vector = [1.0] + [0.0] * 409
    memory = [{"x": vector, "y": index % 2} for index in range(32)]
    row, receipt, supplied, prefix, final = toy_memory_case("H", memory=memory)
    TOOL.verify_memory_history("H", [row], [receipt], [supplied], prefix, final)
    assert final["memory"] == prefix["memory"][1:] + [{"x": vector, "y": 0}]


def test_r_nearest_tie_updates_first_prototype_only():
    vector = [1.0] + [0.0] * 409
    prototypes = [{"x": vector, "n": 2, "counts": [0, 2]}, {"x": vector, "n": 4, "counts": [4, 0]}]
    row, receipt, supplied, prefix, final = toy_memory_case("R", prototypes=prototypes)
    assert row["p1"] == 0.75 and row["native"] == 1
    TOOL.verify_memory_history("R", [row], [receipt], [supplied], prefix, final)
    assert final["prototypes"][0]["counts"] == [1, 2]
    assert final["prototypes"][1] == prefix["prototypes"][1]


@pytest.mark.parametrize(
    "offset,capacity,creates", [(0.125, 1, False), (0.126, 1, True), (1.0, 32, False)]
)
def test_r_allocation_threshold_capacity_and_running_centroid(offset, capacity, creates):
    vector = [1.0 - offset, offset] + [0.0] * 408
    prototypes = [{"x": vector, "n": 2, "counts": [1, 1]} for _ in range(capacity)]
    row, receipt, supplied, prefix, final = toy_memory_case("R", prototypes=prototypes)
    TOOL.verify_memory_history("R", [row], [receipt], [supplied], prefix, final)
    assert len(final["prototypes"]) == capacity + int(creates)
    selected = final["prototypes"][-1] if creates else final["prototypes"][0]
    if creates:
        assert selected == {"x": [1.0] + [0.0] * 409, "n": 1, "counts": [1, 0]}
    else:
        assert selected["x"][0] == ((1 - offset) * 2 + 1) / 3
        assert selected["x"][1] == offset * 2 / 3
        assert selected["counts"] == [2, 1] and selected["n"] == 3


@pytest.mark.parametrize("arm", ["H", "R"])
@pytest.mark.parametrize("corruption", ["p1", "native", "pending", "bytes", "receipt", "final"])
def test_memory_reconstruction_rejects_disconnected_predictions_and_states(arm, corruption):
    row, receipt, supplied, prefix, final = toy_memory_case(arm)
    if corruption == "p1":
        row["p1"] = 0.75
    elif corruption == "native":
        row["native"] = 1
    elif corruption == "pending":
        row["operational_sha256"] = "0" * 64
    elif corruption == "bytes":
        row["live_state_bytes"] += 1
    elif corruption == "receipt":
        receipt["wrapper_sha256"] = "0" * 64
    else:
        final["counts"][0] += 1
    with pytest.raises(RuntimeError, match="ordinary-memory"):
        TOOL.verify_memory_history(arm, [row], [receipt], [supplied], prefix, final)


def test_real_preparation_pins_are_checked_only_as_bytes_without_evaluating_rows():
    real_pins = {
        "inputs.json": "6e9ae9652cf4593e4401e9ce149d1ff178007065c732c2950e904efb523b3773",
        "jobs.json": "e67c82326a43856aa4628c45d21ebd5cd8d9edf7b09c76c232982052544db1d6",
        "prefix_sources.json": "d9bc263106921a4c862e540795fb56c02565b8d8f370a88b570814448ee33dc9",
    }
    preparation = ROOT / "artifacts/research/plasticity_retention_preparation_20261001"
    for name, pin in real_pins.items():
        assert hashlib.sha256((preparation / name).read_bytes()).hexdigest() == pin


def test_reserved_case_tripwires_stop_before_reconstruction(prevent_reserved_baseline_exposure):
    observation, prefix = prevent_reserved_baseline_exposure
    with pytest.raises(AssertionError, match="reserved study observation"):
        TOOL.memory_raster(observation)
    with pytest.raises(AssertionError, match="reserved study prefix"):
        TOOL.verify_memory_history(prefix["arm"], [], [], [], prefix, {})


@pytest.mark.parametrize("corruption", ["version", "executable"])
def test_auditor_interpreter_must_match_frozen_arithmetic_environment(corruption):
    dependencies = interpreter_record()
    TOOL.verify_audit_interpreter(dependencies)
    dependencies["python_version" if corruption == "version" else "executable_sha256"] = "changed"
    with pytest.raises(RuntimeError, match="audit interpreter differs"):
        TOOL.verify_audit_interpreter(dependencies)


@contextlib.contextmanager
def changed_fixture_files(output):
    originals = {}

    def remember(path):
        originals.setdefault(path, path.read_bytes())
        return path

    try:
        yield remember
    finally:
        for path, raw in originals.items():
            path.write_bytes(raw)
        seal_fixture(output)


def rewrite_synthetic_scores(output, remember):
    """Keep derived scores coherent with tampered toy predictions, never study rows."""
    spec = importlib.util.spec_from_file_location(
        "toy_resealed_scorer", TOOL.ROOT / "scripts/plasticity_retention_contract.py"
    )
    assert spec is not None and spec.loader is not None
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    groups = {}
    for job in TOOL.read(output / "job-plan.json")["jobs"]:
        rows = TOOL.lines(output / "jobs" / job["job_id"] / "predictions.jsonl")
        assert all(row["synthetic_validator_fixture"] is True for row in rows)
        groups.setdefault(job["stream"].split("-")[0], {}).setdefault(job["condition"], {})[
            job["arm"]
        ] = rows
    protocol = TOOL.read(TOOL.ROOT / "protocols/plasticity_retention_bounded_v1.json")
    scores = {seed: scorer.evaluate_fixture(rows, protocol) for seed, rows in groups.items()}
    write_json(remember(output / "scores.json"), scores)
    terminal = TOOL.read(output / "result.json")
    terminal["bounded_gate"] = all(score["bounded_gate"] for score in scores.values())
    write_json(remember(output / "result.json"), terminal)


@pytest.mark.parametrize("kind", AUTHORITY_KINDS)
def test_coherent_authority_resealing_cannot_replace_external_original_record_pin(
    synthetic_retained_run, kind
):
    output = synthetic_retained_run[0]
    independent_pins = copy.deepcopy(synthetic_retained_run[4])
    with changed_fixture_files(output) as remember:
        gate = TOOL.read(output / "execution-gate.json")
        record = gate["records"][kind]
        record["recorded_by"] = "different synthetic origin, never operational approval"
        path = output / gate["record_files"][kind]["path"]
        pin = write_json(remember(path), record)
        gate["record_files"][kind].update(sha256=pin, bytes=path.stat().st_size)
        write_json(remember(output / "execution-gate.json"), gate)
        for job in TOOL.read(output / "job-plan.json")["jobs"]:
            work = output / "jobs" / job["job_id"]
            envelope = TOOL.read(work / "job.json")
            envelope["binding"] = gate
            envelope["record_sha256"][kind] = pin
            write_json(remember(work / "job.json"), envelope)
            result = TOOL.read(work / "result.json")
            result["job_sha256"] = TOOL.digest(envelope)
            write_json(remember(work / "result.json"), result)
        seal_fixture(output)
        assert synthetic_retained_run[4] == independent_pins
        with pytest.raises(RuntimeError, match="independent authority record pin: " + kind):
            TOOL.verify(*synthetic_retained_run)


@pytest.mark.parametrize("field", ["record_paths", "record_sha256"])
def test_job_authority_must_match_retained_bytes_even_after_job_hash_resealed(
    synthetic_retained_run, field
):
    output = synthetic_retained_run[0]
    work = output / "jobs" / "100001-return-C"
    with changed_fixture_files(output) as remember:
        envelope = TOOL.read(work / "job.json")
        envelope[field]["approval"] = (
            "/different-synthetic-record" if field == "record_paths" else "e" * 64
        )
        write_json(remember(work / "job.json"), envelope)
        result = TOOL.read(work / "result.json")
        result["job_sha256"] = TOOL.digest(envelope)
        write_json(remember(work / "result.json"), result)
        seal_fixture(output)
        with pytest.raises(RuntimeError, match="job retained authority binding"):
            TOOL.verify(*synthetic_retained_run)


@pytest.mark.parametrize("arm", ["H", "R"])
@pytest.mark.parametrize("corruption", ["prediction", "receipt", "final", "pending"])
def test_coherent_toy_memory_resealing_cannot_override_baseline_arithmetic(
    synthetic_retained_run, arm, corruption
):
    output = synthetic_retained_run[0]
    work = output / "jobs" / ("100001-return-" + arm)
    with changed_fixture_files(output) as remember:
        if corruption in ("prediction", "pending"):
            path = work / "predictions.jsonl"
            rows = TOOL.lines(path)
            if corruption == "prediction":
                rows[0]["p1"] = 0.99
                rows[0]["native"] = 1
            else:
                rows[0]["operational_sha256"] = "0" * 64
            write_lines(remember(path), rows)
            rewrite_synthetic_scores(output, remember)
        else:
            receipt_path = work / "receipts.jsonl"
            receipts = TOOL.lines(receipt_path)
            if corruption == "receipt":
                receipts[0]["wrapper_sha256"] = "0" * 64
            else:
                path = work / "final-state.json"
                value = TOOL.read(path)
                if arm == "H":
                    value["wrapper"]["memory"][0]["y"] ^= 1
                else:
                    value["wrapper"]["prototypes"][0]["counts"][0] += 1
                    value["wrapper"]["prototypes"][0]["n"] += 1
                write_json(remember(path), value)
                receipts[-1]["wrapper_sha256"] = TOOL.digest(value["wrapper"], newline=True)
            write_lines(remember(receipt_path), receipts)
        seal_fixture(output)
        with pytest.raises(RuntimeError, match="ordinary-memory"):
            TOOL.verify(*synthetic_retained_run)
