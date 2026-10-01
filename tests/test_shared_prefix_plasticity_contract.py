"""Zero-dynamics tests only: model/base entry points are tripwired for every test."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/shared_prefix_plasticity_probe.py"
SPEC = importlib.util.spec_from_file_location("shared_prefix_contract_tests", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
probe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = probe
SPEC.loader.exec_module(probe)


@pytest.fixture(autouse=True)
def no_dynamics():
    with probe.zero_dynamics():
        yield


def payload():
    return {
        "config": {"enable_weight_learning": True, "enable_delay_learning": True},
        "plasticity": {
            "config": {"enable_weight_learning": True, "enable_delay_learning": True},
            "eligibility": {"1:2": 0.75},
            "reward_trace": 1.25,
            "update_count": 17,
        },
        "base": {
            "payload": {"connections": [{"weight": 1, "delay_ms": 2.5}]},
            "sha256": "untouched-transport-hash",
        },
        "trace": [{"state_hash": "retained", "flags": {"other_flag": True}}],
    }


def test_vendor_exact_bytes_and_provenance():
    assert probe.sha(probe.VENDOR) == probe.VENDOR_SHA256
    expected = probe.git("show", f"{probe.PREDECESSOR_COMMIT}:scripts/temporal_reuse_loop_probe.py")
    assert probe.VENDOR.read_bytes() == expected


def test_tripwires_are_installed_without_invoking_them():
    p = probe.predecessor()
    assert p.Model.__init__.__name__ == "forbidden"
    assert p.Model.predict.__name__ == "forbidden"
    assert p.Model.outcome.__name__ == "forbidden"
    assert p.IntegratedV05Brain.process_episode.__name__ == "forbidden"


def test_configuration_is_pure_and_preserves_inherited_caps():
    c = probe.frozen_configuration()
    assert c["seeds"] == [910073, 910074]
    assert c["v05"]["enable_homeostasis"] and c["v05"]["enable_receptor_bank"]
    assert c["wrapper"]["learn_field"] and c["wrapper"]["learn_assembly"]
    assert c["v05"]["enable_action"] is False
    assert c["assembly"]["max_candidates"] == 32
    assert c["field"]["max_events_per_run"] == 120000
    assert c["field"]["max_spikes_per_run"] == 20000
    assert c["plasticity"]["max_updates_per_step"] == 2000
    assert c["budget"]["max_predicts"] == c["budget"]["max_outcomes"] == 768
    assert 2 * (64 + 4 * 32 + 2 * 96) == 768


def test_input_generation_deterministic_disjoint_and_label_blind():
    p = probe.predecessor()
    for seed in probe.SEEDS:
        rows = [p.occurrence(seed, "prefix", i) for i in range(64)]
        suffix = [p.occurrence(seed, "return", i) for i in range(32)]
        assert [r["outcome"] for r in rows] == [0] * 32 + [1] * 32
        assert all(r["outcome"] == 0 for r in suffix)
        assert suffix == [p.occurrence(seed, "return", i) for i in range(32)]
        assert len({r["occurrence_id"] for r in rows + suffix}) == 96
        for r in rows + suffix:
            assert set(p.observation(r)) == {"occurrence_id", "start_ms", "pulses"}
            assert r["receipt_time_ms"] == r["start_ms"] + 80
            assert max(q["time_ms"] for q in r["pulses"]) == r["start_ms"] + 40
    assert p.occurrence(probe.SEEDS[0], "return", 0) != p.occurrence(probe.SEEDS[1], "return", 0)


def test_only_four_flags_are_normalized():
    a, b = payload(), payload()
    b["config"]["enable_weight_learning"] = False
    b["plasticity"]["config"]["enable_delay_learning"] = False
    assert probe.normalized_payload(a) == probe.normalized_payload(b)
    for key, value in (("eligibility", {"1:2": 0.76}), ("reward_trace", 1), ("update_count", 18)):
        changed = copy.deepcopy(b)
        changed["plasticity"][key] = value
        assert probe.normalized_payload(a) != probe.normalized_payload(changed)
    for section in ("base", "trace"):
        changed = copy.deepcopy(b)
        changed[section] = {}
        assert probe.normalized_payload(a) != probe.normalized_payload(changed)
    assert a == payload()


def test_normalization_rejects_nonboolean_flags():
    value = payload()
    value["config"]["enable_weight_learning"] = 1
    with pytest.raises(RuntimeError, match="not boolean"):
        probe.normalized_payload(value)


def test_flag_replace_changes_only_declared_paths():
    p = probe.predecessor()
    from sparkbrain.v05.plasticity import V05PlasticityConfig

    class FakeBrain:
        config = p.V05BrainConfig(enable_action=False)
        plasticity = SimpleNamespace(config=V05PlasticityConfig())

        def state_dict(self):
            result = payload()
            result["config"] = asdict(self.config)
            result["plasticity"]["config"] = asdict(self.plasticity.config)
            return result

    brain = FakeBrain()
    before = copy.deepcopy(brain.state_dict())
    result = probe.set_flags(brain, False, False)
    assert not brain.config.enable_weight_learning
    assert not brain.plasticity.config.enable_delay_learning
    assert probe.normalized_payload(before) == probe.normalized_payload(brain.state_dict())
    assert result["before_sha256"] != result["after_sha256"]
    assert brain.state_dict()["plasticity"]["eligibility"] == {"1:2": 0.75}


def candidate_payload():
    counts = {
        "a": {"0": 5},
        "b": {"0": 2, "1": 3},
        "tie": {"0": 3, "1": 3},
        "empty": {},
        "immature": {"1": 10},
    }
    return {
        "assemblies": {
            "config": {"mature_episodes": 3},
            "candidates": {k: {"episode_count": 2 if k == "immature" else 3} for k in counts},
        },
        "predictor": {"counts": counts},
    }


def test_strict_mature_prefix_associations_and_identifiability():
    result = probe.associations(candidate_payload())
    assert result["A"] == ["a"] and result["B"] == ["b"]
    assert result["neither"] == ["empty", "immature", "tie"]
    assert result["A_set_size"] == result["B_set_size"] == 1
    assert result["B_routing_identifiable"] and result["A_to_B_crossover_identifiable"]
    value = candidate_payload()
    value["predictor"]["counts"]["b"] = {"0": 3, "1": 3}
    result = probe.associations(value)
    assert result["B_set_size"] == 0 and not result["B_routing_identifiable"]
    assert not result["A_to_B_crossover_identifiable"]


def row(aid=None, *, p1=0.5, native=None, patterns=(), mature=True):
    return {
        "assembly_id": aid,
        "mature": mature,
        "p1": p1,
        "native": native,
        "outcome": 0,
        "raw_result": {"patterns": [{"ordered_units": list(pattern)} for pattern in patterns]},
    }


def test_frozen_B_selection_counts_tied_native_zero_readout():
    rows = [
        row("b", p1=0.5, native=0),
        row("b", p1=0.4, native=0),
        row(None),
        row("b", mature=False),
    ]
    result = probe.metrics(rows, {"A": ["a"], "B": ["b"]})
    assert result["B_selected_count"] == 2
    assert result["first_B_selection"] == 0
    assert result["initial_B_misrouting"] is True
    assert result["first_A_to_B_crossover"] is None
    assert result["first_A_recall"] == 0


def test_crossover_requires_earlier_A_not_just_any_B():
    result = probe.metrics([row("b"), row("a"), row("b")], {"A": ["a"], "B": ["b"]})
    assert result["first_B_selection"] == 0
    assert result["first_A_to_B_crossover"] == 2


def test_order_endpoint_requires_sole_pattern_and_strictly_earlier_forward():
    rows = [
        row(patterns=[[56, 45]]),
        row(patterns=[[45, 56], [56, 45]]),
        row(patterns=[[45, 56]]),
        row(patterns=[[56, 45]]),
    ]
    result = probe.metrics(rows, {"A": [], "B": []})
    assert result["first_order_swap"] == 3
    assert result["multi_pattern_indices"] == [1]
    assert result["B_selected_count"] == 0 and result["first_B_selection"] is None
    assert result["B_routing_identifiable"] is False


def test_loss_contributions_add_and_abstention_is_wrong():
    values = [row(p1=0.8, native=1), row(p1=0.5), row(p1=0.2, native=0)]
    result = probe.metrics(values, {"A": [], "B": []})
    assert result["native_accuracy"] == 1 / 3
    assert result["coverage"] == 2 / 3
    assert result["brier"] == pytest.approx(
        sum(
            result[k]
            for k in (
                "wrong_brier_contribution",
                "abstain_brier_contribution",
                "correct_brier_contribution",
            )
        )
    )


def test_factorial_signs_and_nullable_indices_excluded():
    values = {
        branch: dict.fromkeys(probe.CONTRAST_ENDPOINTS, value)
        for branch, value in zip(probe.BRANCHES, [10, 4, 3, 2], strict=True)
    }
    for v in values.values():
        v["first_B_selection"] = None
    output = probe.contrasts(values)
    assert output["B_selected_count"] == {
        "W_at_D+": 6,
        "W_at_D-": 1,
        "D_at_W+": 7,
        "D_at_W-": 2,
        "interaction": 5,
    }
    assert "first_B_selection" not in output


def test_budget_rejects_overrun_or_duplicate_receipt():
    b = probe.CallBudget(1)
    with pytest.raises(RuntimeError, match="outcome without"):
        b.reserve_outcome()
    b.reserve_predict()
    with pytest.raises(RuntimeError, match="pending"):
        b.reserve_predict()
    b.reserve_outcome()
    with pytest.raises(RuntimeError, match="prediction count"):
        b.reserve_predict()
    with pytest.raises(RuntimeError, match="outcome without"):
        b.reserve_outcome()


def test_first_projection_preserves_required_observables_and_excludes_post_hash():
    raw = {
        "emitted_pulses": [{"time_ms": 1.25}],
        "v04_result": {"spikes": []},
        "patterns": [],
        "assembly_activations": [],
        "prediction": {"confidence": 0.5},
        "state_hash": "intentional_difference",
    }
    r = {
        "raw_result": raw,
        "p1": 0.5,
        "native": 0,
        "selected_readout_counts": {"0": 2, "1": 2},
        "candidate_decisions": [],
    }
    before = probe.first_projection(r)
    raw["state_hash"] = "another"
    assert probe.first_projection(r) == before
    changed = copy.deepcopy(r)
    changed["raw_result"]["emitted_pulses"][0]["time_ms"] += 1e-12
    assert probe.first_projection(changed) != before


def test_candidate_observer_is_pure_and_retains_each_actual_bank():
    from sparkbrain.v05.assemblies import AssemblyCandidate, AssemblyConfig, TemporalAssemblyMemory
    from sparkbrain.v05.contracts import ActivityPattern

    pattern = ActivityPattern("p", 0, 1, (45, 56), (0, 4), (45, 56), 2)
    candidate = AssemblyCandidate("a", pattern, 3, {"e1", "e2", "e3"}, 0, 1)
    memory = TemporalAssemblyMemory(AssemblyConfig(max_candidates=32), {"a": candidate})
    model = SimpleNamespace(
        brain=SimpleNamespace(assemblies=memory, predictor=SimpleNamespace(counts={"a": {"0": 1}}))
    )
    original_method = TemporalAssemblyMemory.best_match
    before = copy.deepcopy(memory.state_dict())
    with probe.observe_matches(model, {"A": ["a"], "B": [], "neither": []}) as records:
        assert memory.best_match(pattern)[0].assembly_id == "a"
        assert memory.state_dict() == before
        # A manual hand-built bank change simulates different decision boundaries.
        memory.candidates["b"] = AssemblyCandidate("b", pattern, 1, {"e4"}, 13000, 13001)
        memory.best_match(pattern)
    assert TemporalAssemblyMemory.best_match is original_method
    assert len(records[0]["candidates"]) == 1
    assert len(records[1]["candidates"]) == 2
    assert records[1]["top_minus_second_margin"] == 0
    assert records[0]["candidates"][0]["origin"]["frozen_prefix_association"] == "A"


def test_eligibility_empty_transients_and_all_five_adversarial_cases():
    p = probe.predecessor()

    def fake():
        def edge(delay, target):
            return SimpleNamespace(delay_ms=delay, target_id=target)

        return SimpleNamespace(
            base=SimpleNamespace(
                field=SimpleNamespace(_queue=[], outgoing={1: [edge(1, 2), edge(2, 3)]}),
                burst_detector=SimpleNamespace(
                    _window=[], _emitted_keys=set(), config=SimpleNamespace(window_ms=8)
                ),
                cascade_tracker=SimpleNamespace(_pending=[]),
            )
        )

    assert p.eligibility(fake(), 200)["eligible"]
    cases = [
        lambda b: b.base.field._queue.append(1),
        lambda b: b.base.cascade_tracker._pending.append(1),
        lambda b: b.base.burst_detector._window.append(SimpleNamespace(time_ms=192)),
        lambda b: b.base.burst_detector._emitted_keys.add((199000, 200000)),
        lambda b: b.base.field.outgoing[1].reverse(),
    ]
    for modify in cases:
        brain = fake()
        modify(brain)
        assert not p.eligibility(brain, 200)["eligible"]


def test_write_no_clobber_and_output_cap(tmp_path, monkeypatch):
    path = tmp_path / "a.json"
    probe.write(path, {"ok": 1})
    with pytest.raises(FileExistsError):
        probe.write(path, {"ok": 2})
    monkeypatch.setenv("SHARED_PREFIX_OUTPUT_ROOT", str(tmp_path))
    monkeypatch.setattr(probe, "output_bytes", lambda root: 1024 * probe.MIB)
    with pytest.raises(RuntimeError, match="output bytes"):
        probe.write(tmp_path / "b.json", {})


def test_prepare_never_constructs_model_and_does_not_clobber(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, "dependency_inventory", lambda: {"fixture": True})
    freeze = tmp_path / "freeze"
    result = probe.prepare(freeze)
    assert len(result["files"]) == 6
    manifest = json.loads((freeze / "manifest.json").read_text())
    assert manifest["preparation_predictions"] == manifest["preparation_outcomes"] == 0
    assert manifest["preparation_model_constructions"] == 0
    probe.verify_freeze(freeze)
    with pytest.raises(RuntimeError, match="already exists"):
        probe.prepare(freeze)
    (freeze / "inputs-910073-prefix.json").write_text("[]")
    with pytest.raises(RuntimeError, match="hash mismatch"):
        probe.verify_freeze(freeze)


def test_gate_denies_unapproved_review_before_production_import(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, "verify_freeze", lambda *a, **k: {"sources": {}})
    monkeypatch.setattr(probe, "git", lambda *a: b"fake-head\n")
    monkeypatch.setattr(probe, "sha", lambda *a: "manifest-hash")
    monkeypatch.setattr(probe, "predecessor", lambda: pytest.fail("production import too early"))
    review, publication = tmp_path / "review.json", tmp_path / "pub.json"
    review.write_text(
        json.dumps({"approved_for_execution": False, "output_root": str(probe.PLANNED_OUTPUT)})
    )
    publication.write_text("{}")
    with pytest.raises(RuntimeError, match="not approved"):
        probe.verify_execution_gate(tmp_path, review, publication)


def test_worker_rejects_used_directory_before_any_gate_or_model(tmp_path, monkeypatch):
    (tmp_path / "job.json").write_text("{}")
    (tmp_path / "calls.jsonl").write_text("partial\n")
    monkeypatch.setattr(probe, "predecessor", lambda: pytest.fail("model imported"))
    with pytest.raises(RuntimeError, match="not fresh"):
        probe.worker({}, tmp_path)


def test_direct_worker_must_pass_same_execution_gate(tmp_path, monkeypatch):
    (tmp_path / "job.json").write_text("{}")

    def denied(*args, **kwargs):
        raise RuntimeError("review required")

    monkeypatch.setattr(probe, "verify_execution_gate", denied)
    monkeypatch.setattr(probe, "predecessor", lambda: pytest.fail("model imported"))
    with pytest.raises(RuntimeError, match="review required"):
        probe.worker(
            {"freeze": str(tmp_path), "review": "missing", "publication": "missing"}, tmp_path
        )


def test_source_has_no_hidden_guard_or_extra_arms():
    tree = ast.parse(SCRIPT.read_text())
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert "guards" not in names and "smoke" not in names
    assert probe.SEEDS == (910073, 910074)
    assert len(probe.BRANCHES) == 4
    predict_calls = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "predict"
    ]
    outcome_calls = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "outcome"
    ]
    assert len(predict_calls) == len(outcome_calls) == 1


def test_deadline_network_nonfinite_fail_closed():
    with pytest.raises(RuntimeError, match="no remaining"):
        with probe.deadline(0, 1):
            pytest.fail("entered empty budget")
    with pytest.raises(RuntimeError, match="network_disabled"):
        probe.deny_network("socket.connect", ())
    with pytest.raises(ValueError):
        probe.canonical({"nan": float("nan")})


def test_child_cpu_charge_decrements_fractional_timer(monkeypatch):
    calls = []
    monkeypatch.setattr(probe.signal, "getitimer", lambda which: (1.0, 0))
    monkeypatch.setattr(probe.signal, "setitimer", lambda *args: calls.append(args))
    probe.charge_child_cpu(0.25)
    assert calls == [(probe.signal.ITIMER_PROF, 0.75)]
    with pytest.raises(RuntimeError, match="child-inclusive"):
        probe.charge_child_cpu(1)


def test_cpu_clock_includes_waited_children(monkeypatch):
    monkeypatch.setattr(probe.time, "process_time", lambda: 2.0)
    monkeypatch.setattr(probe, "child_cpu", lambda: 3.0)
    assert probe.cpu_clock() == 5.0


def test_fixed_reservations_contain_only_planned_jobs():
    plan = probe.planned_reservations()
    assert len(plan) == 14
    assert [j["job"] for j in plan[:2]] == ["910073-prefix", "910074-prefix"]
    assert [j["pairs"] for j in plan] == [64, 64] + [32] * 4 + [96] * 2 + [32] * 4 + [96] * 2
    assert plan[-1]["cumulative_pairs"] == 768
    assert len({j["job"] for j in plan}) == 14
