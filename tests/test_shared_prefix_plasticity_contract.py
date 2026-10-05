"""Zero-dynamics tests only: model/base entry points are tripwired for every test."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import py_compile
import sys
import zipfile
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

    monkeypatch.setattr(probe, "require_supervised_worker", lambda *a: None)
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


def test_stdlib_inventory_includes_loadable_cached_and_standalone_bytecode(tmp_path, monkeypatch):
    stdlib = tmp_path / "stdlib"
    stdlib.mkdir()
    source = stdlib / "example.py"
    source.write_text("VALUE = 1\n")
    cached = stdlib / "__pycache__/example.cpython-312.pyc"
    standalone = stdlib / "standalone.pyc"
    py_compile.compile(str(source), cfile=str(cached), doraise=True)
    py_compile.compile(str(source), cfile=str(standalone), doraise=True)
    excluded = stdlib / "site-packages/example.pyc"
    excluded.parent.mkdir()
    excluded.write_bytes(cached.read_bytes())
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    inventory = probe.dependency_inventory()
    assert set(inventory["stdlib_files"]) == {
        "example.py",
        "__pycache__/example.cpython-312.pyc",
        "standalone.pyc",
    }
    assert inventory["stdlib_files"]["__pycache__/example.cpython-312.pyc"] == probe.sha(cached)
    assert "-B only disables writes" in inventory["bytecode_policy"]
    assert "not full-machine attestation" in inventory["scope_limit"]


def test_bytecode_tampering_fails_data_only_freeze_verification(tmp_path, monkeypatch):
    stdlib = tmp_path / "stdlib"
    stdlib.mkdir()
    source = stdlib / "example.py"
    source.write_text("VALUE = 1\n")
    cached = stdlib / "__pycache__/example.cpython-312.pyc"
    py_compile.compile(str(source), cfile=str(cached), doraise=True)
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    freeze = tmp_path / "fixture-freeze"
    probe.prepare(freeze)
    probe.verify_freeze(freeze)
    cached.write_bytes(cached.read_bytes() + b"tampered")
    with pytest.raises(RuntimeError, match="dependency mismatch"):
        probe.verify_freeze(freeze)


def cap_roots(monkeypatch):
    for key in ("SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"):
        monkeypatch.setenv(key, str(probe.PLANNED_OUTPUT))


@pytest.mark.parametrize("missing", ["SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"])
def test_worker_cap_roots_must_both_exist_before_job_read(tmp_path, monkeypatch, missing):
    cap_roots(monkeypatch)
    monkeypatch.delenv(missing)
    monkeypatch.setattr(
        probe, "read", lambda *a: pytest.fail("read happened before cap validation")
    )
    with pytest.raises(RuntimeError, match="missing output-cap root"):
        probe.worker_main(tmp_path)


@pytest.mark.parametrize("wrong", ["SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"])
def test_worker_rejects_mismatched_cap_roots(tmp_path, monkeypatch, wrong):
    cap_roots(monkeypatch)
    monkeypatch.setenv(wrong, str(tmp_path))
    with pytest.raises(RuntimeError, match="mismatched output-cap root"):
        probe.validate_output_roots(probe.PLANNED_OUTPUT)


def test_driver_initializes_both_roots_but_never_repairs_conflicts(tmp_path, monkeypatch):
    for key in ("SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"):
        monkeypatch.delenv(key, raising=False)
    probe.validate_output_roots(probe.PLANNED_OUTPUT, initialize=True)
    assert os.environ["SHARED_PREFIX_OUTPUT_ROOT"] == str(probe.PLANNED_OUTPUT)
    assert os.environ["SPARK_PROBE_OUTPUT_ROOT"] == str(probe.PLANNED_OUTPUT)
    monkeypatch.setenv("SPARK_PROBE_OUTPUT_ROOT", str(tmp_path))
    with pytest.raises(RuntimeError, match="mismatched"):
        probe.validate_output_roots(probe.PLANNED_OUTPUT, initialize=True)
    assert os.environ["SPARK_PROBE_OUTPUT_ROOT"] == str(tmp_path)


def test_unsupervised_worker_fails_before_gate_or_model(tmp_path, monkeypatch):
    (tmp_path / "job.json").write_text("{}")
    monkeypatch.setattr(probe, "verify_execution_gate", lambda *a: pytest.fail("gate reached"))
    with pytest.raises(RuntimeError, match="live driver supervision"):
        probe.worker({}, tmp_path)


def test_worker_main_requires_inherited_supervisor_before_setting_limits(tmp_path, monkeypatch):
    cap_roots(monkeypatch)
    monkeypatch.setattr(probe, "validate_execution_environment", lambda: None)
    (tmp_path / "job.json").write_text("{}")
    monkeypatch.setattr(probe, "process_limits", lambda *a: pytest.fail("limits changed"))
    with pytest.raises(RuntimeError, match="inherited driver supervision"):
        probe.worker_main(tmp_path)


def supervisor_fixture(tmp_path):
    job = {"cpu_limit": 119.0, "wall_limit": 179.0}
    header = {
        "schema": "shared-prefix-supervision-1",
        "parent_pid": 123,
        "job_sha256": probe.digest(job),
        "directory": str(tmp_path.resolve()),
        "output_root": str(probe.PLANNED_OUTPUT),
        "cpu_limit": 119.0,
        "wall_limit": 179.0,
        "issued_monotonic": 100.0,
        "wall_stop_monotonic": 279.0,
    }
    return job, header


def test_supervisor_envelope_clips_to_remaining_local_wall(tmp_path):
    job, header = supervisor_fixture(tmp_path)
    assert probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=200) == (
        119.0,
        79.0,
    )


@pytest.mark.parametrize("value", [float("inf"), float("nan"), 120.0, -1.0, True])
def test_supervisor_rejects_invalid_cpu_allowance(tmp_path, value):
    job, header = supervisor_fixture(tmp_path)
    job["cpu_limit"] = header["cpu_limit"] = value
    if isinstance(value, float) and not probe.math.isfinite(value):
        # Invalid nonfinite JSON is already rejected by canonical; a decoded
        # envelope is checked independently before any timer/model operation.
        header["job_sha256"] = "irrelevant"
        with pytest.raises(ValueError):
            probe.digest(job)
        return
    header["job_sha256"] = probe.digest(job)
    with pytest.raises(RuntimeError, match="outside local bound"):
        probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=101)


def test_job_cannot_supply_future_deadline(tmp_path):
    job, header = supervisor_fixture(tmp_path)
    job["wall_deadline_monotonic"] = 1e100
    header["job_sha256"] = probe.digest(job)
    with pytest.raises(RuntimeError, match="caller-supplied job deadline forbidden"):
        probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=101)
    del job["wall_deadline_monotonic"]
    header["job_sha256"] = probe.digest(job)
    header["wall_stop_monotonic"] = 1e100
    with pytest.raises(RuntimeError, match="deadline outside local bound"):
        probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=101)


def test_supervisor_rejects_job_substitution_and_expiry(tmp_path):
    job, header = supervisor_fixture(tmp_path)
    with pytest.raises(RuntimeError, match="job mismatch"):
        probe.validate_supervisor_envelope(
            header, {**job, "arm": "X"}, tmp_path, parent_pid=123, now=101
        )
    with pytest.raises(RuntimeError, match="deadline outside local bound"):
        probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=279)
    with pytest.raises(RuntimeError, match="parent PID"):
        probe.validate_supervisor_envelope(header, job, tmp_path, parent_pid=124, now=101)


def test_supervisor_requires_real_run_parent_command():
    command = [
        sys.executable,
        "-B",
        "-S",
        "-P",
        str(SCRIPT),
        "run",
        "--output",
        str(probe.PLANNED_OUTPUT),
    ]
    probe.validate_driver_command(command, SCRIPT.parent, Path(sys.executable))
    for changed in (
        [*command[:5], "worker", *command[6:]],
        [sys.executable, "-c", "pass"],
        [*command[:4], "/tmp/not-the-runner.py", *command[5:]],
    ):
        with pytest.raises(RuntimeError):
            probe.validate_driver_command(changed, SCRIPT.parent, Path(sys.executable))


def test_live_supervision_refuses_closed_pipe_or_changed_parent(tmp_path, monkeypatch):
    cap_roots(monkeypatch)
    monkeypatch.setattr(probe.os, "getppid", lambda: 123)
    monkeypatch.setattr(probe, "process_start_ticks", lambda pid: "start")
    monkeypatch.setattr(probe.time, "monotonic", lambda: 101.0)
    monkeypatch.setattr(probe.select, "select", lambda *a: ([], [], []))
    supervisor = probe.WorkerSupervisor(19, 123, "start", "hash", tmp_path, 119, 279)
    supervisor.check_live()
    monkeypatch.setattr(probe.select, "select", lambda *a: ([19], [], []))
    with pytest.raises(RuntimeError, match="pipe closed or changed"):
        supervisor.check_live()
    monkeypatch.setattr(probe.os, "getppid", lambda: 124)
    with pytest.raises(RuntimeError, match="supervision lost"):
        supervisor.check_live()


def test_synthetic_pipe_acceptance_installs_mocked_parent_death_guard(tmp_path, monkeypatch):
    cap_roots(monkeypatch)
    job, header = supervisor_fixture(tmp_path)
    read_fd, writer_fd = os.pipe()
    header.update({"parent_start_ticks": "start", "writer_fd": writer_fd})
    real_readlink = os.readlink
    real_executable = str(Path(sys.executable).resolve())
    real_read_bytes = Path.read_bytes
    monkeypatch.setattr(probe.os, "getppid", lambda: 123)
    monkeypatch.setattr(probe, "process_start_ticks", lambda pid: "start")
    monkeypatch.setattr(probe.time, "monotonic", lambda: 101.0)
    command = [
        sys.executable,
        "-B",
        "-S",
        "-P",
        str(SCRIPT),
        "run",
        "--output",
        str(probe.PLANNED_OUTPUT),
    ]

    def fake_read_bytes(path):
        if str(path) == "/proc/123/cmdline":
            return b"\0".join(arg.encode() for arg in command) + b"\0"
        return real_read_bytes(path)

    def fake_readlink(path):
        mapping = {
            "/proc/123/cwd": str(SCRIPT.parent),
            "/proc/123/exe": real_executable,
            f"/proc/123/fd/{writer_fd}": real_readlink(f"/proc/self/fd/{writer_fd}"),
        }
        return mapping.get(str(path)) or real_readlink(path)

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)
    monkeypatch.setattr(probe.os, "readlink", fake_readlink)
    calls = []
    monkeypatch.setattr(
        probe.ctypes,
        "CDLL",
        lambda *a, **k: SimpleNamespace(prctl=lambda *args: calls.append(args) or 0),
    )
    try:
        os.write(writer_fd, (probe.canonical(header) + "\n").encode())
        supervisor = probe.accept_supervision(read_fd, job, tmp_path)
        assert supervisor.cpu_limit == 119
        assert calls == [(1, probe.signal.SIGKILL, 0, 0, 0)]
        supervisor.check_job(job, tmp_path)
    finally:
        os.close(read_fd)
        os.close(writer_fd)


def test_optional_stdlib_zip_absence_presence_and_hash_are_bound(tmp_path, monkeypatch):
    stdlib = tmp_path / "stdlib"
    stdlib.mkdir()
    archive = stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip"
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    absent = probe.dependency_inventory()["optional_stdlib_zip"]
    assert absent == {"path": str(archive), "present": False, "sha256": None}
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("marker.py", "VALUE = 1\n")
    present = probe.dependency_inventory()["optional_stdlib_zip"]
    assert present == {"path": str(archive), "present": True, "sha256": probe.sha(archive)}
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("marker.py", "VALUE = 2\n")
    assert probe.dependency_inventory()["optional_stdlib_zip"]["sha256"] != present["sha256"]


def test_adding_previously_absent_stdlib_zip_breaks_freeze(tmp_path, monkeypatch):
    stdlib = tmp_path / "stdlib"
    stdlib.mkdir()
    archive = stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip"
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    freeze = tmp_path / "fixture-freeze"
    probe.prepare(freeze)
    probe.verify_freeze(freeze)
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("marker.py", "VALUE = 1\n")
    with pytest.raises(RuntimeError, match="dependency mismatch"):
        probe.verify_freeze(freeze)


def test_optional_stdlib_zip_path_cannot_be_a_directory(tmp_path, monkeypatch):
    stdlib = tmp_path / "stdlib"
    stdlib.mkdir()
    archive = stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip"
    archive.mkdir()
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    with pytest.raises(RuntimeError, match="zip path is not a readable file"):
        probe.dependency_inventory()


def execution_environment_fixture(monkeypatch, tmp_path):
    flags = {
        name: getattr(probe.sys.flags, name)
        for name in dir(probe.sys.flags)
        if not name.startswith("_")
    }
    flags.update(no_site=1, safe_path=True, optimize=0, ignore_environment=0, isolated=0)
    monkeypatch.setattr(probe.sys, "flags", SimpleNamespace(**flags))
    monkeypatch.setattr(probe.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(probe.sys, "pycache_prefix", None)
    monkeypatch.setattr(probe.sys, "_xoptions", {})
    monkeypatch.setenv("PYTHONHASHSEED", "0")
    for key in list(os.environ):
        if key.startswith("PYTHON") and key not in {"PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE"}:
            monkeypatch.delenv(key)
    # This fixture exercises validation policy, not the checkout's current cache
    # state. Ordinary CI tests may already have generated real runtime bytecode.
    root = tmp_path / "isolated-project"
    (root / "src").mkdir(parents=True)
    vendor = root / "artifacts/source/predecessor.py"
    vendor.parent.mkdir(parents=True)
    vendor.write_text("# Environment-validation fixture; never imported.\n")
    stdlib = tmp_path / "isolated-stdlib"
    (stdlib / "lib-dynload").mkdir(parents=True)
    monkeypatch.setattr(probe, "ROOT", root)
    monkeypatch.setattr(probe, "VENDOR", vendor)
    monkeypatch.setattr(probe.sysconfig, "get_path", lambda name: str(stdlib))
    monkeypatch.setattr(probe.sys, "path", [str(stdlib), str(stdlib / "lib-dynload")])


def test_bound_execution_mode_accepts_plain_unoptimized_flags(monkeypatch, tmp_path):
    execution_environment_fixture(monkeypatch, tmp_path)
    probe.validate_execution_environment()


@pytest.mark.parametrize(
    "setting,value,message",
    [
        ("pycache_prefix", "/tmp/alternate-cache", "alternate pycache prefix"),
        ("_xoptions", {"dev": True}, "Python -X options"),
        ("optimize", 1, "optimized interpreter"),
        ("ignore_environment", 1, "ignore PYTHONHASHSEED"),
        ("isolated", 1, "ignore PYTHONHASHSEED"),
    ],
)
def test_execution_rejects_unbound_interpreter_modes(
    monkeypatch, tmp_path, setting, value, message
):
    execution_environment_fixture(monkeypatch, tmp_path)
    if setting in {"pycache_prefix", "_xoptions"}:
        monkeypatch.setattr(probe.sys, setting, value)
    else:
        monkeypatch.setattr(probe.sys.flags, setting, value)
    monkeypatch.setattr(probe, "predecessor", lambda: pytest.fail("production imported"))
    with pytest.raises(RuntimeError, match=message):
        probe.validate_execution_environment()
    assert os.environ["PYTHONHASHSEED"] == "0"


@pytest.mark.parametrize("cache_kind", ["runtime", "vendor"])
def test_execution_rejects_controlled_cache_files(monkeypatch, tmp_path, cache_kind):
    execution_environment_fixture(monkeypatch, tmp_path)
    cache_root = probe.ROOT / "src" if cache_kind == "runtime" else probe.VENDOR.parent
    cache = cache_root / "__pycache__/fixture.cpython-311.pyc"
    cache.parent.mkdir()
    cache.write_bytes(b"presence-only bytecode fixture; never imported")
    monkeypatch.setattr(probe, "predecessor", lambda: pytest.fail("production imported"))
    with pytest.raises(RuntimeError, match=f"{cache_kind} bytecode caches must be absent"):
        probe.validate_execution_environment()
    assert cache.read_bytes() == b"presence-only bytecode fixture; never imported"
