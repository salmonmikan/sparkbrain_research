"""Model-free retention accounting tests: only pure helpers and tiny fake objects."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/plasticity_retention_contract.py"
SPEC = importlib.util.spec_from_file_location("retention_contract_tests", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)
PROTOCOL = json.loads((ROOT / "protocols/plasticity_retention_bounded_v1.json").read_bytes())


@dataclass
class Edge:
    source_id: int
    target_id: int
    weight: float
    delay_ms: float = 3.0
    plastic: bool = True


@dataclass(frozen=True)
class Spike:
    unit_id: int
    time_ms: float


def fake_apply_state(**config):
    settings = {
        "eligibility_decay": 0.9,
        "max_updates_per_step": 10,
        "tau_plus_ms": 10.0,
        "tau_minus_ms": 10.0,
        "depression_ratio": 1.0,
        "learning_rate": 0.2,
        "min_weight": 0.0,
        "max_weight": 1.0,
        "enable_weight_learning": True,
    }
    settings.update(config)
    # Deliberately unsorted; only the first two edges have nonzero current STDP.
    edges = [
        Edge(7, 8, 0.5),
        Edge(4, 5, 0.5),
        Edge(2, 1, 0.05, 7.0),
        Edge(1, 3, 0.5, plastic=False),
        Edge(1, 2, 0.95),
    ]
    field = SimpleNamespace(connections={(e.source_id, e.target_id): e for e in edges})
    controller = SimpleNamespace(
        config=SimpleNamespace(**settings),
        eligibility={"1:2": 0.5, "2:1": -0.5, "4:5": 3.0, "7:8": 2.0, "9:10": 1e-9},
        reward_trace=2.0,
        update_count=11,
    )
    spikes = [Spike(5, 20.0), Spike(2, 10.0), Spike(1, 0.0), Spike(4, 20.0)]
    return field, controller, spikes


def recorded_after_state(field, controller) -> None:
    """Manually supply a tiny expected observation; never invoke a model apply method."""
    delta = math.exp(-1)
    controller.eligibility = {
        "1:2": 0.45 + delta,
        "2:1": -0.45 - delta,
        "4:5": 2.7,
        "7:8": 1.8,
    }
    field.connections[1, 2].weight = 1.0
    field.connections[2, 1].weight = 0.0
    controller.update_count = 13


def scored_rows(outcomes, *, error=0.5, correct_per_label=None):
    seen = {0: 0, 1: 0}
    result = []
    for outcome in outcomes:
        correct = correct_per_label is None or seen[outcome] < correct_per_label[outcome]
        result.append(
            {
                "outcome": outcome,
                "native": outcome if correct else 1 - outcome,
                "p1": error if outcome == 0 else 1 - error,
                "actual_weight_abs_change": 0.001,
            }
        )
        seen[outcome] += 1
    return result


@pytest.fixture
def passing_rows():
    balanced = [0, 1] * 8
    novel_local = scored_rows(balanced, correct_per_label=(4, 4))
    novel_local += scored_rows(balanced, error=0.1, correct_per_label=(6, 6))
    return {
        "return": {
            "C": scored_rows([0] * 32),
            "L": scored_rows([0] * 32, error=0.1),
            "G": scored_rows([0] * 32, error=0.4),
            "Fw": scored_rows([0] * 32),
            "H": scored_rows([0] * 32),
            "R": scored_rows([0] * 32),
        },
        "stationary": {arm: scored_rows([1] * 16, error=0.1) for arm in ("C", "L")},
        "novel": {
            "C": scored_rows(balanced * 2, error=0.2, correct_per_label=(12, 12)),
            "L": novel_local,
            "Fw": scored_rows(balanced * 2),
            "H": scored_rows(balanced * 2),
            "R": scored_rows(balanced * 2),
        },
    }


def test_helper_source_and_import_have_no_runtime_dependency() -> None:
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


def test_audit_distinguishes_carry_current_delta_clipping_and_inactive_edges() -> None:
    field, controller, spikes = fake_apply_state()
    before = copy.deepcopy((field, controller, spikes))
    audit = TOOL.audit_apply_before(field, spikes, controller)
    assert (field, controller, spikes) == before
    assert audit["observer_pair_evaluations"] == 3
    assert [row["edge"] for row in audit["updates"]] == ["1:2", "2:1"]
    positive, negative = audit["updates"]
    delta = math.exp(-1)
    assert positive["pre_eligibility"] == 0.5
    assert positive["decayed_carry"] == 0.45
    assert positive["current_delta"] == delta
    assert positive["eligibility_after"] == 0.45 + delta
    assert positive["unclipped_proposal"] == 0.95 + 0.4 * (0.45 + delta)
    assert positive["weight_expected"] == 1.0 and positive["clipped"] is True
    assert negative["current_delta"] == -delta
    assert negative["weight_expected"] == 0.0 and negative["clipped"] is True
    assert audit["expected_eligibility"]["4:5"] == 2.7
    assert audit["expected_eligibility"]["7:8"] == 1.8
    assert "9:10" not in audit["expected_eligibility"]
    recorded_after_state(field, controller)
    after_state = copy.deepcopy((field, controller))
    result = TOOL.audit_apply_after(audit, field, controller, 2)
    assert (field, controller) == after_state
    assert result["changed_weights"] == result["clipped_weights"] == 2
    assert result["actual_weight_abs_change"] == pytest.approx(0.1)
    assert result["actual_weight_signed_change"] == pytest.approx(0.0, abs=1e-15)
    assert result["eligible_edge_work"] == 2 and result["extra_apply_calls"] == 0
    assert result["delays_unchanged"] is True
    assert result["delay_map_sha256"] == TOOL.digest(audit["delays_before"])


def test_local_eligibility_removes_carry_without_carry_only_weight_writes() -> None:
    field, controller, spikes = fake_apply_state(eligibility_decay=0.0)
    audit = TOOL.audit_apply_before(field, spikes, controller)
    delta = math.exp(-1)
    assert audit["expected_eligibility"] == {"1:2": delta, "2:1": -delta}
    assert all(row["decayed_carry"] == 0.0 for row in audit["updates"])
    assert [row["pre_eligibility"] for row in audit["updates"]] == [0.5, -0.5]
    assert controller.eligibility["7:8"] == 2.0


@pytest.mark.parametrize("arm", ["C", "L", "G", "Fw"])
def test_registered_arm_arithmetic_keeps_reward_and_current_stdp_explicit(arm):
    field, controller, _ = fake_apply_state(**PROTOCOL["arms"][arm])
    field.connections = {(1, 2): Edge(1, 2, 0.5)}
    controller.eligibility = {"1:2": 2.0}
    spikes = [Spike(2, 10.0), Spike(1, 0.0)]
    audit = TOOL.audit_apply_before(field, spikes, controller)
    (row,) = audit["updates"]
    carry = 0.0 if arm == "L" else 1.8
    rate = 0.0001 if arm == "G" else 0.001
    eligibility = carry + math.exp(-1)
    proposal = 0.5 + rate * 2.0 * eligibility
    expected_weight = 0.5 if arm == "Fw" else proposal
    assert row["decayed_carry"] == carry
    assert row["eligibility_after"] == eligibility
    assert row["unclipped_proposal"] == proposal
    assert row["weight_expected"] == expected_weight
    assert row["clipped"] is False
    controller.eligibility = {"1:2": eligibility}
    controller.update_count += 1
    field.connections[1, 2].weight = expected_weight
    result = TOOL.audit_apply_after(audit, field, controller, 1)
    assert result["actual_weight_signed_change"] == expected_weight - 0.5
    assert result["extra_apply_calls"] == 0


def test_frozen_weights_still_audit_eligibility_and_eligible_work() -> None:
    field, controller, spikes = fake_apply_state(enable_weight_learning=False)
    audit = TOOL.audit_apply_before(field, spikes, controller)
    for row in audit["updates"]:
        assert row["weight_expected"] == row["weight_before"]
        assert row["unclipped_proposal"] != row["weight_before"]
        assert row["weight_write_enabled"] is False and row["clipped"] is False
    controller.eligibility = {
        "1:2": 0.45 + math.exp(-1),
        "2:1": -0.45 - math.exp(-1),
        "4:5": 2.7,
        "7:8": 1.8,
    }
    controller.update_count = 13
    result = TOOL.audit_apply_after(audit, field, controller, 2)
    assert result["eligible_edge_work"] == 2
    assert result["actual_weight_abs_change"] == result["changed_weights"] == 0


def test_apply_work_cap_uses_sorted_eligible_edges() -> None:
    field, controller, spikes = fake_apply_state(max_updates_per_step=1)
    audit = TOOL.audit_apply_before(field, spikes, controller)
    assert [row["edge"] for row in audit["updates"]] == ["1:2"]
    assert audit["observer_pair_evaluations"] == 1
    assert audit["expected_eligibility"]["2:1"] == -0.45


def test_equal_time_and_cancelled_pairs_decay_but_do_not_write_weights() -> None:
    field = SimpleNamespace(connections={(1, 2): Edge(1, 2, 0.5)})
    _, controller, _ = fake_apply_state()
    controller.eligibility = {"1:2": 2.0}
    spikes = [Spike(2, 1.0), Spike(1, 2.0), Spike(1, 0.0), Spike(1, 1.0)]
    audit = TOOL.audit_apply_before(field, spikes, controller)
    assert audit["updates"] == []
    assert audit["expected_eligibility"] == {"1:2": 1.8}
    assert audit["observer_pair_evaluations"] == 3


@pytest.mark.parametrize(
    "corruption,message",
    [
        ("eligibility", "eligibility observer"),
        ("returned", "apply/work count"),
        ("count", "apply/work count"),
        ("weight", "weight writes"),
        ("inactive_weight", "weight writes"),
        ("delay", "delay write"),
    ],
)
def test_apply_audit_rejects_mismatched_actual_observations(corruption, message) -> None:
    field, controller, spikes = fake_apply_state()
    audit = TOOL.audit_apply_before(field, spikes, controller)
    recorded_after_state(field, controller)
    returned = 2
    if corruption == "eligibility":
        controller.eligibility["7:8"] += 0.1
    elif corruption == "returned":
        returned = 1
    elif corruption == "count":
        controller.update_count += 1
    elif corruption == "weight":
        field.connections[1, 2].weight = 0.99
    elif corruption == "inactive_weight":
        field.connections[7, 8].weight = 0.6
    else:
        field.connections[7, 8].delay_ms += 1
    with pytest.raises(RuntimeError, match=message):
        TOOL.audit_apply_after(audit, field, controller, returned)


def test_metrics_include_abstention_loss_and_exact_bin_endpoints() -> None:
    rows = [
        {"p1": 0.0, "outcome": 0, "native": 0},
        {"p1": 0.25, "outcome": 1, "native": None},
        {"p1": 0.5, "outcome": 0, "native": 1},
        {"p1": 0.75, "outcome": 1, "native": 1},
        {"p1": 1.0, "outcome": 0, "native": None},
    ]
    result = TOOL.metrics(rows)
    assert result["n"] == 5
    assert result["brier"] == (0 + 0.5625 + 0.25 + 0.0625 + 1) / 5
    assert (result["correct"], result["wrong"], result["abstain"]) == (2, 1, 2)
    assert result["coverage"] == 3 / 5
    assert result["correct_per_total"] == 2 / 5
    assert result["correct_per_nonabstaining"] == 2 / 3
    assert [b["count"] for b in result["calibration"]] == [1, 1, 1, 2]
    assert result["calibration"][-1]["mean_probability"] == 0.875
    assert result["calibration"][-1]["outcome_fraction"] == 0.5
    assert result["first"] == rows[0]


def test_all_abstention_and_empty_bins_remain_undefined() -> None:
    result = TOOL.metrics([{"p1": 0.5, "outcome": 1, "native": None}])
    assert result["correct_per_nonabstaining"] is None
    assert result["coverage"] == result["correct"] == result["wrong"] == 0
    assert result["abstain"] == 1 and result["brier"] == 0.25
    for index in (0, 1, 3):
        assert result["calibration"][index]["count"] == 0
        assert result["calibration"][index]["mean_probability"] is None
        assert result["calibration"][index]["outcome_fraction"] is None
    with pytest.raises(RuntimeError, match="empty"):
        TOOL.metrics([])


@pytest.mark.parametrize(
    "key,value",
    [
        ("outcome", True),
        ("outcome", 1.0),
        ("outcome", 2),
        ("native", False),
        ("native", 0.0),
        ("native", -1),
        ("p1", True),
        ("p1", "0.5"),
        ("p1", float("nan")),
        ("p1", float("inf")),
        ("p1", -0.01),
        ("p1", 1.01),
    ],
)
def test_invalid_score_values_fail_closed(key, value) -> None:
    row = {"p1": 0.5, "outcome": 0, "native": 0, key: value}
    with pytest.raises(RuntimeError):
        TOOL.metrics([row])


def test_complete_synthetic_gate_is_bounded_and_does_not_grant_scientific_credit(passing_rows):
    before = copy.deepcopy(passing_rows)
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["bounded_gate"] is True
    assert result["primary_C_L"] is result["secondary_G_L"] is True
    assert result["stationary_preserved"] is result["novel_preserved"] is True
    assert result["novel_acquisition"] is True
    assert result["novel_ceiling_inconclusive"] is False
    assert result["scientific_credit"] == 0
    assert "no general or unique-mediation claim" in result["claim_limit"]
    assert passing_rows == before


def test_equal_c_and_l_fail_even_when_attenuation_control_is_worse(passing_rows):
    passing_rows["return"]["C"] = copy.deepcopy(passing_rows["return"]["L"])
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["secondary_G_L"] is True
    assert result["primary_C_L"] is result["bounded_gate"] is False


def test_secondary_gain_contrast_is_required_independently(passing_rows):
    passing_rows["return"]["G"] = copy.deepcopy(passing_rows["return"]["L"])
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["primary_C_L"] is True
    assert result["secondary_G_L"] is result["bounded_gate"] is False


@pytest.mark.parametrize("above", [False, True])
def test_primary_brier_gate_compares_unrounded_values(passing_rows, above):
    error = math.nextafter(math.sqrt(0.03), math.inf if above else 0.0)
    passing_rows["return"]["C"] = scored_rows([0] * 32, error=error)
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    scores = result["metrics"]["return"]
    difference = scores["C"]["brier"] - scores["L"]["brier"]
    assert round(difference, 2) == 0.02
    assert (difference >= 0.02) is above
    assert result["primary_C_L"] is result["bounded_gate"] is above


@pytest.mark.parametrize("regression", ["correct", "coverage", "brier"])
def test_primary_return_requires_all_three_constraints(passing_rows, regression):
    if regression == "correct":
        passing_rows["return"]["L"][0]["native"] = 1
    elif regression == "coverage":
        for row in passing_rows["return"]["C"]:
            row["native"] = 1
        passing_rows["return"]["L"][0]["native"] = None
    else:
        passing_rows["return"]["C"] = scored_rows([0] * 32, error=0.15)
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["primary_C_L"] is result["bounded_gate"] is False


@pytest.mark.parametrize("regression", ["correct", "coverage", "brier"])
def test_stationary_preservation_is_required(passing_rows, regression):
    if regression == "correct":
        for row in passing_rows["stationary"]["L"][:2]:
            row["native"] = 0
    elif regression == "coverage":
        passing_rows["stationary"]["L"][0]["native"] = None
    else:
        passing_rows["stationary"]["L"] = scored_rows([1] * 16, error=0.5)
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["primary_C_L"] is True
    assert result["stationary_preserved"] is result["bounded_gate"] is False


def test_novel_total_accuracy_cannot_hide_failure_of_one_label(passing_rows):
    passing_rows["novel"]["L"][16:] = scored_rows([0, 1] * 8, error=0.1, correct_per_label=(8, 5))
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["novel_late"]["correct"] == 13
    assert result["novel_late"]["coverage"] == 1.0
    assert result["novel_preserved"] is True
    assert result["novel_acquisition"] is result["bounded_gate"] is False


@pytest.mark.parametrize("regression", ["gain", "coverage", "weight", "brier"])
def test_novel_acquisition_requires_improvement_and_actual_weight_change(passing_rows, regression):
    novel = passing_rows["novel"]["L"]
    if regression == "gain":
        novel[:16] = scored_rows([0, 1] * 8, correct_per_label=(6, 5))
    elif regression == "coverage":
        novel[30]["native"] = None  # An already wrong row: correct count stays 12.
    elif regression == "weight":
        for row in novel:
            row.pop("actual_weight_abs_change")
    else:
        novel[:16] = scored_rows([0, 1] * 8, error=0.16, correct_per_label=(4, 4))
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["novel_late"]["correct"] == 12
    assert result["novel_acquisition"] is result["bounded_gate"] is False


@pytest.mark.parametrize("ceiling", ["correct", "brier"])
def test_early_novel_ceiling_is_inconclusive_and_cannot_pass(passing_rows, ceiling):
    passing_rows["novel"]["L"][:16] = scored_rows(
        [0, 1] * 8,
        error=0.14 if ceiling == "brier" else 0.5,
        correct_per_label=(8, 7) if ceiling == "correct" else (4, 4),
    )
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["novel_ceiling_inconclusive"] is True
    assert result["bounded_gate"] is False


def test_fourteen_correct_early_rows_are_below_ceiling_and_allow_acquisition(passing_rows):
    novel = passing_rows["novel"]["L"]
    novel[:16] = scored_rows([0, 1] * 8, correct_per_label=(7, 7))
    novel[16:] = scored_rows([0, 1] * 8, error=0.1)
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["novel_ceiling_inconclusive"] is False
    assert result["novel_acquisition"] is result["bounded_gate"] is True


@pytest.mark.parametrize("regression", ["correct", "coverage", "brier"])
def test_novel_preservation_is_required_even_when_acquisition_passes(passing_rows, regression):
    novel = passing_rows["novel"]
    if regression == "correct":
        novel["C"][16:] = scored_rows([0, 1] * 8, error=0.2)
    elif regression == "coverage":
        novel["L"][14]["native"] = None
        novel["L"][30]["native"] = None
    else:
        novel["L"][16:] = scored_rows([0, 1] * 8, error=0.3, correct_per_label=(6, 6))
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["novel_acquisition"] is True
    assert result["novel_preserved"] is result["bounded_gate"] is False


@pytest.mark.parametrize("start", [0, 16])
def test_novel_requires_balance_in_each_half(passing_rows, start):
    passing_rows["novel"]["L"][start]["outcome"] = 1
    with pytest.raises(RuntimeError, match="novel balance"):
        TOOL.evaluate_fixture(passing_rows, PROTOCOL)


@pytest.mark.parametrize("count", [31, 33])
def test_novel_requires_exact_row_count(passing_rows, count):
    novel = passing_rows["novel"]["L"]
    if count == 31:
        novel.pop()
    else:
        novel.append(copy.deepcopy(novel[-1]))
    with pytest.raises(RuntimeError, match="novel row count"):
        TOOL.evaluate_fixture(passing_rows, PROTOCOL)


@pytest.mark.parametrize("terminal", [False, True])
def test_output_admission_checks_projected_total_before_writing(tmp_path, monkeypatch, terminal):
    cap = PROTOCOL["resources"]["output_total_bytes" if terminal else "ordinary_output_bytes"]
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=10)
    monkeypatch.setattr(writer, "total", lambda: cap - 3)
    writer.raw(tmp_path / "exact", b"123", terminal=terminal)
    assert (tmp_path / "exact").read_bytes() == b"123"
    with pytest.raises(RuntimeError, match="output admission ceiling"):
        writer.raw(tmp_path / "absent" / "over", b"1234", terminal=terminal)
    assert not (tmp_path / "absent").exists()


def test_terminal_allowance_is_cumulative_and_inside_total_cap(tmp_path, monkeypatch):
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=4)
    writer.raw(tmp_path / "terminal", b"abc", terminal=True)
    with pytest.raises(RuntimeError, match="terminal allowance"):
        writer.raw(tmp_path / "terminal", b"de", terminal=True, append=True)
    assert writer.terminal_written == 3
    assert (tmp_path / "terminal").read_bytes() == b"abc"
    monkeypatch.setattr(writer, "total", lambda: PROTOCOL["resources"]["output_total_bytes"])
    with pytest.raises(RuntimeError, match="output admission ceiling"):
        writer.raw(tmp_path / "last", b"d", terminal=True)
    assert not (tmp_path / "last").exists()
    assert writer.terminal_written == 3


def test_output_total_includes_nested_files_and_append_bytes(tmp_path):
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=20)
    writer.raw(tmp_path / "nested" / "stdout", b"abc")
    writer.raw(tmp_path / "nested" / "stdout", b"de", append=True)
    writer.json(tmp_path / "terminal.json", {"ok": True}, terminal=True)
    assert (tmp_path / "nested" / "stdout").read_bytes() == b"abcde"
    assert writer.total() == 5 + len(TOOL.canonical({"ok": True}))


def test_output_is_no_clobber_and_failure_preserves_terminal_channel(tmp_path):
    checks = []
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=20, live=lambda: checks.append("live"))
    writer.raw(tmp_path / "existing", b"original")
    with pytest.raises(FileExistsError):
        writer.raw(tmp_path / "existing", b"replacement")
    assert writer.measurement_failed is True
    assert (tmp_path / "existing").read_bytes() == b"original"
    with pytest.raises(RuntimeError, match="measurement failure latched"):
        writer.raw(tmp_path / "later", b"blocked")
    checks_before_terminal = list(checks)
    writer.json(tmp_path / "failure.json", {"failed": True}, terminal=True)
    assert checks == checks_before_terminal
    assert json.loads((tmp_path / "failure.json").read_bytes()) == {"failed": True}
    assert not (tmp_path / "later").exists()


def test_output_flush_failure_latches_after_partial_bytes_without_retry(tmp_path, monkeypatch):
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=20)

    def fail(_fd):
        raise OSError("synthetic fsync failure")

    with monkeypatch.context() as patch:
        patch.setattr(os, "fsync", fail)
        with pytest.raises(OSError, match="synthetic"):
            writer.raw(tmp_path / "partial", b"already written")
    assert (tmp_path / "partial").read_bytes() == b"already written"
    assert writer.measurement_failed is True
    writer.raw(tmp_path / "failure", b"failure", terminal=True)
    assert writer.total() == len(b"already writtenfailure")


def test_output_rejects_escape_and_symlink_before_mutation(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    writer = TOOL.OutputWriter(root, terminal_limit=20)
    with pytest.raises(RuntimeError, match="escaped root"):
        writer.raw(tmp_path / "outside", b"x")
    target = root / "target"
    target.write_bytes(b"keep")
    alias = root / "alias"
    alias.symlink_to(target)
    with pytest.raises(RuntimeError, match="escaped root"):
        writer.raw(alias, b"x", append=True)
    assert target.read_bytes() == b"keep"
    assert not (tmp_path / "outside").exists()


def test_nonfinite_json_is_rejected_and_latches_measurement_failure(tmp_path):
    writer = TOOL.OutputWriter(tmp_path, terminal_limit=20)
    with pytest.raises(ValueError):
        writer.json(tmp_path / "nan.json", {"value": float("nan")})
    assert writer.measurement_failed is True
    assert not (tmp_path / "nan.json").exists()


def test_liveness_failure_precedes_ordinary_write_but_allows_terminal_metadata(tmp_path):
    def expired():
        raise RuntimeError("synthetic deadline expired")

    writer = TOOL.OutputWriter(tmp_path, terminal_limit=20, live=expired)
    with pytest.raises(RuntimeError, match="deadline expired"):
        writer.json(tmp_path / "ordinary.json", {"value": 1})
    assert writer.measurement_failed is True
    assert not (tmp_path / "ordinary.json").exists()
    writer.json(tmp_path / "terminal.json", {"stopped": True}, terminal=True)
    assert json.loads((tmp_path / "terminal.json").read_bytes()) == {"stopped": True}


def test_call_ledger_intent_precedes_function_and_completion_counts_are_separate():
    emitted = []
    ledger = TOOL.CallLedger(emitted.append, {"prediction": 1})

    def method(value, *, extra):
        assert ledger.intents == {"prediction": 1}
        assert ledger.returns == {}
        assert emitted == [{"kind": "prediction", "phase": "intent", "number": 1}]
        return value + extra

    assert ledger.call("prediction", method, 3, extra=4) == 7
    ledger.require_observed()
    assert ledger.summary()["intents"] == ledger.summary()["returns"] == {"prediction": 1}
    assert ledger.summary()["errors"] == {}
    assert [event["phase"] for event in emitted] == ["intent", "return"]
    with pytest.raises(RuntimeError, match="method limit"):
        ledger.call("prediction", lambda: pytest.fail("over-budget method entered"))
    with pytest.raises(RuntimeError, match="method limit"):
        ledger.call("unallocated", lambda: pytest.fail("unallocated method entered"))
    assert len(emitted) == 2


def test_failed_top_level_intent_never_enters_method():
    def fail(_event):
        raise OSError("intent observation unavailable")

    ledger = TOOL.CallLedger(fail, {"prediction": 1})
    with pytest.raises(OSError, match="intent observation"):
        ledger.call("prediction", lambda: pytest.fail("unadmitted method entered"))
    assert ledger.intents == ledger.returns == ledger.errors == {}
    assert ledger.events == [{"kind": "prediction", "phase": "intent", "number": 1}]
    assert ledger.observation_failed is True
    with pytest.raises(RuntimeError, match="observation failed"):
        ledger.require_observed()


@pytest.mark.parametrize("method_fails", [False, True])
def test_failed_completion_observation_preserves_original_result_or_error(method_fails):
    failure = ValueError("model-free method error")

    def emit(event):
        if event["phase"] != "intent":
            raise OSError("completion observation unavailable")

    ledger = TOOL.CallLedger(emit, {"prediction": 2})

    def method():
        if method_fails:
            raise failure
        return "original result"

    if method_fails:
        with pytest.raises(ValueError) as caught:
            ledger.call("prediction", method)
        assert caught.value is failure
    else:
        assert ledger.call("prediction", method) == "original result"
    assert ledger.intents == {"prediction": 1}
    assert ledger.errors["prediction"] == int(method_fails)
    assert ledger.returns["prediction"] == int(not method_fails)
    with pytest.raises(RuntimeError, match="observation failed"):
        ledger.require_observed()
    with pytest.raises(RuntimeError, match="no next method"):
        ledger.call("prediction", lambda: pytest.fail("next top-level method entered"))


@pytest.mark.parametrize("failed_phase", ["intent", "return", "error"])
def test_nested_observation_failure_finishes_admitted_outer_method(failed_phase):
    executed = []
    unavailable = False

    def emit(event):
        nonlocal unavailable
        if event["kind"] == "apply" and event["phase"] == failed_phase:
            unavailable = True
        if unavailable:
            raise OSError("all later observation writes fail")

    ledger = TOOL.CallLedger(emit, {"prediction": 2, "apply": 1, "readout": 1})
    failure = ValueError("nested method error")

    def apply():
        executed.append("apply")
        if failed_phase == "error":
            raise failure
        return 3

    def readout():
        executed.append("readout")
        return 4

    def prediction():
        try:
            ledger.call("apply", apply)
        except ValueError as error:
            assert error is failure
        value = ledger.call("readout", readout)
        executed.append("prediction completed")
        return value

    assert ledger.call("prediction", prediction) == 4
    assert executed == ["apply", "readout", "prediction completed"]
    assert ledger.intents == {"prediction": 1, "apply": 1, "readout": 1}
    assert ledger.returns["prediction"] == ledger.returns["readout"] == 1
    assert ledger.returns["apply"] == int(failed_phase != "error")
    assert ledger.errors["apply"] == int(failed_phase == "error")
    assert [(event["kind"], event["phase"]) for event in ledger.events] == [
        ("prediction", "intent"),
        ("apply", "intent"),
        ("apply", "error" if failed_phase == "error" else "return"),
        ("readout", "intent"),
        ("readout", "return"),
        ("prediction", "return"),
    ]
    with pytest.raises(RuntimeError, match="observation failed"):
        ledger.require_observed()
    with pytest.raises(RuntimeError, match="no next method"):
        ledger.call("prediction", lambda: pytest.fail("next top-level method entered"))
    assert ledger.intents["prediction"] == 1


def test_nested_observation_failure_does_not_waive_method_limit():
    def emit(event):
        if event["kind"] == "apply" and event["phase"] == "return":
            raise OSError("observation failed")

    ledger = TOOL.CallLedger(emit, {"prediction": 1, "apply": 1})

    def prediction():
        ledger.call("apply", lambda: None)
        ledger.call("apply", lambda: pytest.fail("over-budget nested method entered"))

    with pytest.raises(RuntimeError, match="method limit"):
        ledger.call("prediction", prediction)
    assert ledger.intents == {"prediction": 1, "apply": 1}
    assert ledger.errors == {"prediction": 1}


def test_nested_failure_retains_outer_exception_and_bounded_error_record():
    failure = ValueError("x" * 5000)

    def emit(event):
        if event["phase"] != "intent":
            raise OSError("observation unavailable")

    ledger = TOOL.CallLedger(emit, {"prediction": 2, "apply": 1})

    def prediction():
        ledger.call("apply", lambda: None)
        raise failure

    with pytest.raises(ValueError) as caught:
        ledger.call("prediction", prediction)
    assert caught.value is failure
    assert ledger.events[-1]["error_type"] == "ValueError"
    assert ledger.events[-1]["error"] == "x" * 4096
    assert ledger.errors == {"prediction": 1}
    with pytest.raises(RuntimeError, match="no next method"):
        ledger.call("prediction", lambda: pytest.fail("next top-level method entered"))


@pytest.mark.parametrize("error_type", [TimeoutError, MemoryError])
def test_resource_failure_interrupts_admitted_outer_method(error_type):
    failure = error_type("synthetic resource limit")

    def emit(event):
        if event["kind"] == "apply" and event["phase"] == "return":
            raise failure

    ledger = TOOL.CallLedger(emit, {"prediction": 1, "apply": 1})

    def prediction():
        ledger.call("apply", lambda: None)
        pytest.fail("resource failure must stop the outer method immediately")

    with pytest.raises(error_type) as caught:
        ledger.call("prediction", prediction)
    assert caught.value is failure
    assert ledger.intents == {"prediction": 1, "apply": 1}
    assert ledger.returns == {"apply": 1}
    assert ledger.errors == {"prediction": 1}


def test_paired_wrong_to_abstain_swap_cannot_pass_overall(passing_rows):
    control = scored_rows([0] * 32)
    local = scored_rows([0] * 32)
    for i in range(32):
        control[i].update(native=1 if i < 16 else None, p1=0.9 if i < 16 else 0.5)
        local[i].update(native=None if i < 16 else 1, p1=0.5 if i < 16 else 0.51)
    passing_rows["return"].update(C=control, L=local, G=scored_rows([0] * 32, error=0.9))
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["primary_C_L"] is result["secondary_G_L"] is True
    assert (
        result["metrics"]["return"]["C"]["correct"]
        == result["metrics"]["return"]["L"]["correct"]
        == 0
    )
    assert (
        result["metrics"]["return"]["C"]["coverage"]
        == result["metrics"]["return"]["L"]["coverage"]
        == 0.5
    )
    assert result["paired_return_native_C_to_L"]["wrong_to_abstain"] == 16
    assert result["paired_return_native_C_to_L"]["abstain_to_wrong"] == 16
    assert result["return_only_wrong_to_abstain"] is True
    assert result["bounded_gate"] is False


@pytest.mark.parametrize("corrected_index", [0, 31])
def test_actual_native_correction_is_distinct_from_abstention_only(passing_rows, corrected_index):
    control = scored_rows([0] * 32)
    local = scored_rows([0] * 32)
    for i in range(32):
        control[i].update(native=1 if i < 16 else None, p1=0.9 if i < 16 else 0.5)
        local[i].update(native=None if i < 16 else 1, p1=0.5 if i < 16 else 0.51)
    local[corrected_index].update(native=0, p1=0.1)
    passing_rows["return"].update(C=control, L=local, G=scored_rows([0] * 32, error=0.9))
    result = TOOL.evaluate_fixture(passing_rows, PROTOCOL)
    assert result["return_only_wrong_to_abstain"] is False
    assert result["bounded_gate"] is True


def test_paired_native_transitions_reject_misaligned_targets():
    with pytest.raises(RuntimeError, match="target mismatch"):
        TOOL.paired_native_transitions([{"native": 0, "outcome": 0}], [{"native": 0, "outcome": 1}])
