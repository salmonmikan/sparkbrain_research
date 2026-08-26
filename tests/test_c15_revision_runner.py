from __future__ import annotations

import copy
import importlib.util
import json
import multiprocessing
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "artifacts" / "v03" / "c15_revision" / "protocol.json"
RUNNER_PATH = ROOT / "scripts" / "run_c15_revision.py"
SPEC = importlib.util.spec_from_file_location("run_c15_revision", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def protocol() -> dict:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def _rejected_decision() -> dict[str, object]:
    return {
        "ignited": False,
        "belief_key": None,
        "object_key": None,
        "score": 0.0,
        "margin": 0.0,
        "reason": "score_below_threshold",
        "citation_ids": [],
    }


def _state(*, entity_key: str = "entity-a") -> dict[str, object]:
    return {
        "activations": {"alpha": 0.0, "beta": 0.0, "gamma": 0.0},
        "citations": [],
        "entity_key": entity_key,
        "history": [],
        "state_hash": "0" * 64,
        "winner": None,
    }


def _stage(index: int, role: str) -> dict[str, object]:
    decision = _rejected_decision()
    return {
        "stage_index": index,
        "stage_role": role,
        "delivery_rows": [
            {
                "evidence_id": f"evidence-{index}",
                "source_id": "source-a",
                "correlation_group": "group-a",
                "entity_key": "entity-a",
                "hypothesis_id": "alpha",
                "polarity": "support",
                "strength": 1.0,
                "time": float(index),
                "redelivery": False,
            }
        ],
        "input_hash": "1" * 64,
        "gate_passes": [
            {"pass_index": 1, "proposal": copy.deepcopy(decision)},
            {"pass_index": 2, "proposal": copy.deepcopy(decision)},
        ],
        "proposal": copy.deepcopy(decision),
        "learned_decision": copy.deepcopy(decision),
        "state_before": _state(),
        "state_after": _state(),
    }


def valid_raw_row(*, fixture_index: int = 0, model_seed: int = 99001) -> dict[str, object]:
    from sparkbrain.v03_seed.revision_worlds import build_split_manifest

    fixture = sorted(build_split_manifest("dev"), key=lambda row: row.episode_id)[fixture_index]
    return {
        "schema_version": "0.3",
        "split": "dev",
        "condition_id": "full_separated",
        "input_track": "I1_local_compositional",
        "entity_condition": "E1_oracle_entity",
        "model_seed": model_seed,
        "episode_id": fixture.episode_id,
        "episode_seed": fixture.episode_seed,
        "family_id": fixture.family_id,
        "world": fixture.world,
        "variant_id": "base",
        "evaluated_entity_key": "entity-a",
        "truth_belief": "alpha",
        "previous_truth_belief": "alpha",
        "transition_target": "maintain",
        "sufficient_information": True,
        "recovery_opportunity": False,
        "predicted_belief": None,
        "predicted_transition": "insufficient_information",
        "ignited": False,
        "no_ignition_probability": 1.0,
        "belief_probabilities": {"alpha": 1.0, "beta": 0.0, "gamma": 0.0},
        "transition_probabilities": {
            "insufficient_information": 1.0,
            "maintain": 0.0,
            "recover": 0.0,
            "update": 0.0,
        },
        "reason": "score_below_threshold",
        "cited_evidence_ids": [],
        "attribution_targets": [],
        "attribution_probabilities": [
            {"evidence_id": None, "probability": None} for _ in range(5)
        ],
        "state_before": _state(),
        "state_after": _state(),
        "stage_trace": [_stage(0, "context"), _stage(2, "assessment")],
        "state_lineage_hash": "2" * 64,
        "checkpoint_restored": False,
        "recovery_latency_steps": None,
        "input_hash": "3" * 64,
        "target_hash": "4" * 64,
        "protocol_compliant": True,
    }


def test_disabled_guard_precedes_git_and_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value = protocol()
    value["dependencies"]["runner_execution_allowed"] = False
    payload = runner._canonical(value).encode()
    output = tmp_path / "output"
    original = Path.read_bytes

    def read_bytes(path: Path) -> bytes:
        if path.resolve() == PROTOCOL_PATH.resolve():
            return payload
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    monkeypatch.setattr(
        runner,
        "_git",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("Git accessed")),
    )
    monkeypatch.setattr(
        runner,
        "_git_bytes",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("Git accessed")),
    )
    with pytest.raises(RuntimeError, match="disabled until the source-pin amendment"):
        runner.run(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output=output,
            source_commit="0" * 40,
        )
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


def test_noncanonical_protocol_is_rejected_before_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    copied = tmp_path / "protocol.json"
    copied.write_text(runner._canonical(protocol()), encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_git",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("Git accessed")),
    )
    with pytest.raises(RuntimeError, match="repository-fixed canonical path"):
        runner.run(
            root=ROOT,
            protocol_path=copied,
            output=tmp_path / "output",
            source_commit="0" * 40,
        )


def test_protocol_amendment_allows_exactly_four_dependency_fields() -> None:
    base = protocol()
    current = copy.deepcopy(base)
    current["dependencies"]["c15_protocol_base_commit"] = runner.BASE_PROTOCOL_COMMIT
    current["dependencies"]["c15_protocol_base_sha256"] = "1" * 64
    current["dependencies"]["c15_source_pin"] = "2" * 40
    current["dependencies"]["runner_execution_allowed"] = True
    runner._validate_protocol_amendment(current, base)

    current["protocol_id"] = "tampered"
    with pytest.raises(RuntimeError, match="beyond the authorized pin"):
        runner._validate_protocol_amendment(current, base)


def test_source_scope_and_protected_hash_tamper_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value = protocol()
    monkeypatch.setattr(runner, "_git", lambda *_args: "src/not-authorized.py")
    with pytest.raises(RuntimeError, match="unauthorized paths"):
        runner._validate_source_scope(
            root=ROOT,
            protocol=value,
            source_commit="1" * 40,
            base_commit=runner.BASE_PROTOCOL_COMMIT,
        )

    protected = {}
    for index in range(28):
        relative = f"protected/file-{index}.txt"
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(index), encoding="utf-8")
        protected[relative] = runner._sha256_file(path)
    minimal = {"protected_files": protected}
    assert len(runner._validate_protected_hashes(tmp_path, minimal)) == 28
    (tmp_path / "protected" / "file-3.txt").write_text("tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="protected file hash changed"):
        runner._validate_protected_hashes(tmp_path, minimal)


def test_source_scope_rejects_working_bytes_that_differ_from_pin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value = protocol()
    authorized = value["source_control"]["c15_authorized_paths_before_pin"]
    for relative in authorized:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"pinned")
    (tmp_path / authorized[0]).write_bytes(b"dirty")

    def git(_root: Path, *args: str) -> str:
        if args[:2] == ("diff", "--name-only") and args[2] == runner.BASE_PROTOCOL_COMMIT:
            return authorized[0]
        return ""

    monkeypatch.setattr(runner, "_git", git)
    monkeypatch.setattr(runner, "_git_bytes", lambda *_args: b"pinned")
    with pytest.raises(RuntimeError, match="working source differs from its pin"):
        runner._validate_source_scope(
            root=tmp_path,
            protocol=value,
            source_commit="1" * 40,
            base_commit=runner.BASE_PROTOCOL_COMMIT,
        )


def test_v2_fixture_hash_mismatch_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    from sparkbrain.v03_seed import revision_worlds

    value = protocol()
    expected_full = value["seeds"]["full_fixture_sha256"]
    expected_manifest = value["seeds"]["split_manifest_sha256"]
    monkeypatch.setattr(
        revision_worlds,
        "full_fixture_sha256",
        lambda split: "0" * 64 if split == "dev" else expected_full[split],
    )
    monkeypatch.setattr(
        revision_worlds,
        "split_manifest_sha256",
        lambda split: expected_manifest[split],
    )
    with pytest.raises(RuntimeError, match="full fixture hash mismatch for dev"):
        runner._validate_fixture_hashes(value)


def test_frozen_cardinalities_and_each_validator_rejects_wrong_count() -> None:
    value = protocol()
    contracts = value["artifacts"]["derived_contracts"]
    assert value["artifacts"]["raw_row_count"] == 21_760
    assert contracts["loss_ablation_metrics.json"]["training_step_rows"] == 23_040
    assert contracts["confusion_matrices.json"]["seed_rows"] == 170
    assert contracts["confusion_matrices.json"]["aggregate_rows"] == 34
    assert contracts["loss_ablation_metrics.json"]["objective_rows"] == 540
    assert contracts["loss_ablation_metrics.json"]["condition_seed_rows"] == 60
    assert contracts["pareto_frontier.json"]["seed_points"] == 60

    with pytest.raises(RuntimeError, match="raw row cardinality"):
        runner._validate_raw_rows([], value)
    loss = {
        field: []
        for field in contracts["loss_ablation_metrics.json"]["exact_top_level_fields"]
    }
    loss.update(
        {
            "schema_version": "0.3",
            "protocol_id": value["protocol_id"],
            "source_commit": "0" * 40,
            "objective_order": contracts["loss_ablation_metrics.json"][
                "training_step_objective_keys"
            ],
            "scientific_gates": {},
        }
    )
    with pytest.raises(RuntimeError, match="training step row cardinality"):
        runner._validate_loss_metrics(loss, value)


def test_raw_schema_unknown_nonfinite_and_sort_rejection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from sparkbrain.v03_seed import revision_worlds

    value = protocol()
    fixtures = tuple(
        sorted(
            revision_worlds.build_split_manifest("dev"),
            key=lambda row: row.episode_id,
        )[:2]
    )
    monkeypatch.setattr(
        revision_worlds,
        "build_split_manifest",
        lambda split: fixtures if split == "dev" else (),
    )
    value["artifacts"]["raw_row_count"] = 2
    value["conditions"]["order"] = ["full_separated"]
    value["conditions"]["diagnostic_full_only_cells"] = []
    value["seeds"]["model"] = [99001]
    value["variants"]["order"] = ["base"]
    value["failure_contract"]["successful_seed_cardinality"]["raw_rows_per_seed"] = 2
    rows = [valid_raw_row(fixture_index=0), valid_raw_row(fixture_index=1)]
    runner._validate_raw_rows(rows, value)

    unknown = copy.deepcopy(rows[0])
    unknown["unknown"] = True
    with pytest.raises(RuntimeError, match="missing or unknown keys"):
        runner._validate_raw_rows([unknown, rows[1]], value)

    nonfinite = copy.deepcopy(rows[0])
    nonfinite["belief_probabilities"]["alpha"] = float("nan")  # type: ignore[index]
    with pytest.raises(RuntimeError, match="finite JSON"):
        runner._validate_raw_rows([nonfinite, rows[1]], value)

    with pytest.raises(RuntimeError, match="canonical order"):
        runner._validate_raw_rows(list(reversed(rows)), value)

    duplicate = [rows[0], copy.deepcopy(rows[0])]
    with pytest.raises(RuntimeError, match="duplicate canonical composite key"):
        runner._validate_raw_rows(duplicate, value)


def test_confusion_recalculates_only_from_raw_rows() -> None:
    value = protocol()
    rows = [
        {
            "transition_target": "maintain",
            "predicted_transition": "maintain",
            "predicted_belief": "alpha",
            "truth_belief": "alpha",
            "checkpoint_restored": False,
            "recovery_latency_steps": None,
            "ignited": True,
        },
        {
            "transition_target": "maintain",
            "predicted_transition": "update",
            "predicted_belief": "beta",
            "truth_belief": "alpha",
            "checkpoint_restored": False,
            "recovery_latency_steps": None,
            "ignited": True,
        },
        {
            "transition_target": "update",
            "predicted_transition": "insufficient_information",
            "predicted_belief": None,
            "truth_belief": "beta",
            "checkpoint_restored": False,
            "recovery_latency_steps": None,
            "ignited": False,
        },
        {
            "transition_target": "recover",
            "predicted_transition": "recover",
            "predicted_belief": "gamma",
            "truth_belief": "gamma",
            "checkpoint_restored": False,
            "recovery_latency_steps": 2,
            "ignited": True,
        },
    ]
    result = runner._confusion_row(rows, protocol=value, identity={})
    assert result["row_count"] == 4
    assert result["unnecessary_revision_count"] == 1
    assert result["unnecessary_revision_denominator"] == 2
    assert result["missed_revision_count"] == 1
    assert result["missed_revision_denominator"] == 2
    assert result["recovery_successes"] == 1
    assert result["recovery_latency_observed_mean"] == 2.0


def test_confusion_validator_rejects_nested_unknown_nonfinite_and_sort() -> None:
    value = protocol()
    rows = []
    for seed in (99001, 99002):
        rows.append(
            {
                "split": "dev",
                "condition_id": "full_separated",
                "input_track": "I1_local_compositional",
                "entity_condition": "E1_oracle_entity",
                "model_seed": seed,
                "transition_target": "maintain",
                "predicted_transition": "maintain",
                "predicted_belief": "alpha",
                "truth_belief": "alpha",
                "checkpoint_restored": False,
                "recovery_latency_steps": None,
                "ignited": True,
            }
        )
    artifact = runner._confusion_artifact(rows, protocol=value, source_commit="0" * 40)
    contract = value["artifacts"]["derived_contracts"]["confusion_matrices.json"]
    contract["seed_rows"] = 2
    contract["aggregate_rows"] = 1
    value["seeds"]["model"] = [99001, 99002]
    cardinality = value["failure_contract"]["successful_seed_cardinality"]
    cardinality["confusion_seed_rows_per_seed"] = 1
    cardinality["aggregate_rows_when_any_seed_succeeds"] = 1
    runner._validate_tabular_artifact(
        artifact, protocol=value, artifact_name="confusion_matrices.json"
    )

    unsorted = copy.deepcopy(artifact)
    unsorted["seed_rows"].reverse()
    with pytest.raises(RuntimeError, match="order is not canonical"):
        runner._validate_tabular_artifact(
            unsorted, protocol=value, artifact_name="confusion_matrices.json"
        )

    unknown = copy.deepcopy(artifact)
    unknown["seed_rows"][0]["transition_confusion"]["maintain"]["unknown"] = 0
    with pytest.raises(RuntimeError, match="missing or unknown keys"):
        runner._validate_tabular_artifact(
            unknown, protocol=value, artifact_name="confusion_matrices.json"
        )

    nonfinite = copy.deepcopy(artifact)
    nonfinite["seed_rows"][0]["coverage"] = float("inf")
    with pytest.raises(RuntimeError, match="finite JSON"):
        runner._validate_tabular_artifact(
            nonfinite, protocol=value, artifact_name="confusion_matrices.json"
        )


def test_generated_validator_recalculates_confusion_from_raw(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = protocol()
    common = {
        "schema_version": "0.3",
        "protocol_id": value["protocol_id"],
        "source_commit": "0" * 40,
        "failed_seeds": [],
    }
    objective_config = dict(common)
    confusion = {
        **common,
        "seed_rows": [{} for _ in range(170)],
        "aggregate_rows": [{} for _ in range(34)],
    }
    calibration = copy.deepcopy(confusion)
    loss = {
        **common,
        "training_step_rows": [],
        "condition_seed_rows": [],
        "objective_rows": [],
        "engineering_gates": [],
        "scientific_gates": {},
    }
    pareto = dict(common)
    monkeypatch.setattr(runner, "_validate_raw_rows", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(runner, "_validate_objective_config", lambda *_args: None)
    monkeypatch.setattr(runner, "_validate_tabular_artifact", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(runner, "_validate_loss_metrics", lambda *_args: None)
    monkeypatch.setattr(runner, "_validate_pareto", lambda *_args: None)
    monkeypatch.setattr(
        runner, "_objective_config_artifact", lambda *_args, **_kwargs: objective_config
    )
    monkeypatch.setattr(
        runner,
        "_confusion_artifact",
        lambda *_args, **_kwargs: {**confusion, "aggregate_rows": [{"recalculated": True}]},
    )
    with pytest.raises(RuntimeError, match="confusion artifact does not exactly recalculate"):
        runner._validate_generated_artifacts(
            protocol=value,
            raw=[],
            objective_config=objective_config,
            confusion=confusion,
            calibration=calibration,
            loss_metrics=loss,
            pareto=pareto,
        )


def test_bootstrap_blocks_and_pareto_directions(monkeypatch: pytest.MonkeyPatch) -> None:
    value = protocol()
    value["seeds"]["model"] = [99001]
    value["splits"]["world_order"] = ["synthetic-world"]
    value["determinism"]["bootstrap_resamples"] = 20
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = ["synthetic"]
    rows = [
        {
            "split": "test",
            "input_track": "I1_local_compositional",
            "entity_condition": "E1_oracle_entity",
            "model_seed": 99001,
            "world": "synthetic-world",
            "episode_id": f"episode-{index}",
            "episode_seed": index,
            "effect": float(index),
        }
        for index in range(8)
    ]
    monkeypatch.setattr(
        runner,
        "_comparison_effect",
        lambda _comparison, selected, protocol: sum(float(row["effect"]) for row in selected)
        / len(selected),
    )
    intervals = runner._bootstrap_intervals(rows, protocol=value)
    assert intervals["synthetic"]["effect"] == 3.5
    assert intervals["synthetic"]["resamples"] == 20
    assert intervals["synthetic"]["lower"] <= intervals["synthetic"]["upper"]

    dimensions = [
        {"metric": "error", "direction": "minimize"},
        {"metric": "success", "direction": "maximize"},
    ]
    assert runner._dominates(
        {"error": 0.1, "success": 0.9},
        {"error": 0.2, "success": 0.8},
        dimensions,
    )
    assert not runner._dominates(
        {"error": 0.2, "success": 0.9},
        {"error": 0.1, "success": 0.8},
        dimensions,
    )


def _synthetic_statistics_rows(value: dict, *, mode: str = "normal") -> list[dict]:
    rows = []
    for world in value["splits"]["world_order"]:
        for index in range(8):
            target = "insufficient_information" if world == "insufficient" else world
            for condition in value["conditions"]["order"]:
                for variant in value["variants"]["order"]:
                    ignited = target != "insufficient_information"
                    if mode == "all_abstain":
                        ignited = False
                    elif mode == "zero_tp":
                        ignited = target == "insufficient_information"
                    elif mode == "single_decision":
                        ignited = world == "maintain" and index == 0
                    rows.append({
                        "split": "test",
                        "input_track": "I1_local_compositional",
                        "entity_condition": "E1_oracle_entity",
                        "model_seed": 99001,
                        "world": world,
                        "episode_id": f"reserved-{world}-{index}",
                        "episode_seed": 990100 + index,
                        "condition_id": condition,
                        "variant_id": variant,
                        "transition_target": target,
                        "predicted_transition": (
                            target if ignited and target != "insufficient_information"
                            else "maintain" if ignited else "insufficient_information"
                        ),
                        "predicted_belief": "alpha" if ignited else None,
                        "truth_belief": "alpha",
                        "ignited": ignited,
                        "checkpoint_restored": False,
                        "recovery_latency_steps": 1 if ignited and target == "recover" else None,
                        "no_ignition_probability": 0.25 if ignited else 0.75,
                        "belief_probabilities": {"alpha": 0.6, "beta": 0.3, "gamma": 0.1},
                    })
    return rows


def _statistics_protocol(*, resamples: int = 8) -> dict:
    value = protocol()
    value["seeds"]["model"] = [99001]
    value["determinism"]["bootstrap_resamples"] = resamples
    return value


def test_nullable_statistics_preserve_all_abstain_and_zero_tp_formulas() -> None:
    value = _statistics_protocol()
    abstain = _synthetic_statistics_rows(value, mode="all_abstain")
    base = runner._primary_base_rows(abstain, "full_separated")
    confusion = runner._confusion_row(base, protocol=value, identity={})
    calibration = runner._calibration_row(base, identity={})
    assert confusion["no_ignition_precision"] == 0.25
    assert confusion["no_ignition_recall"] == 1.0
    assert confusion["no_ignition_f1"] == 0.4
    assert calibration["decided_count"] == 0
    assert calibration["coverage"] == 0.0
    assert calibration["ece"] is None
    assert runner._comparison_effect(
        "full_minus_weighted_ce_ece", abstain, protocol=value
    ) is None

    zero_tp = _synthetic_statistics_rows(value, mode="zero_tp")
    confusion = runner._confusion_row(
        runner._primary_base_rows(zero_tp, "full_separated"), protocol=value, identity={}
    )
    assert confusion["no_ignition_tp"] == 0
    assert confusion["no_ignition_fp"] == 24
    assert confusion["no_ignition_fn"] == 8
    assert confusion["no_ignition_precision"] == confusion["no_ignition_recall"] == 0.0
    assert confusion["no_ignition_f1"] is None
    assert runner._comparison_effect(
        "full_minus_weighted_ce_no_ignition_f1", zero_tp, protocol=value
    ) is None
    no_abstention = [dict(row, ignited=True) for row in base]
    confusion = runner._confusion_row(no_abstention, protocol=value, identity={})
    assert confusion["no_ignition_precision"] is None
    assert confusion["no_ignition_recall"] == 0.0
    assert confusion["no_ignition_f1"] is None


@pytest.mark.parametrize("left,right", [(None, 0.5), (0.5, None), (None, None)])
def test_nullable_paired_effect_rejects_either_undefined_operand(left, right) -> None:
    assert runner._nullable_difference(left, right) is None


def test_bootstrap_finite_point_with_undefined_resamples_keeps_point_only() -> None:
    import random

    value = _statistics_protocol(resamples=64)
    value["conditions"]["order"] = ["full_separated", "one_weighted_ce"]
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = [
        "full_minus_weighted_ce_ece"
    ]
    rows = _synthetic_statistics_rows(value, mode="single_decision")
    result = runner._bootstrap_intervals(rows, protocol=value)
    interval = result["full_minus_weighted_ce_ece"]
    rng = random.Random(value["determinism"]["bootstrap_seed"])
    undefined = 0
    for _ in range(64):
        rng.randrange(1)
        has_decision = False
        for world in value["splits"]["world_order"]:
            selected = [rng.randrange(8) for _ in range(8)]
            has_decision |= world == "maintain" and 0 in selected
        undefined += not has_decision
    assert 0 < undefined < 64
    assert interval == {
        "effect": 0.0, "lower": None, "upper": None,
        "resamples": 64, "bootstrap_seed": value["determinism"]["bootstrap_seed"],
        "defined_resamples": 64 - undefined, "undefined_resamples": undefined,
    }
    runner._validate_bootstrap_intervals(result, protocol=value, failed=False)


def test_bootstrap_consumes_all_10000_draws_and_shared_rng_after_undefined(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import random

    value = _statistics_protocol(resamples=10000)
    value["splits"]["world_order"] = ["reserved"]
    comparisons = ["synthetic_first", "synthetic_second"]
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = comparisons
    rows = [{
        "split": "test", "input_track": "I1_local_compositional",
        "entity_condition": "E1_oracle_entity", "model_seed": 99001,
        "world": "reserved", "episode_id": str(index), "episode_seed": index,
    } for index in range(8)]
    seen = {name: [] for name in comparisons}

    def effect(name, selected, *, protocol):
        indices = tuple(int(row["episode_id"]) for row in selected)
        seen[name].append(indices)
        if name == comparisons[0] and len(seen[name]) == 1:
            return None
        return sum(indices) / len(indices)

    monkeypatch.setattr(runner, "_comparison_effect", effect)
    result = runner._bootstrap_intervals(rows, protocol=value)
    rng = random.Random(value["determinism"]["bootstrap_seed"])
    for name in comparisons:
        expected = []
        for _ in range(10000):
            rng.randrange(1)
            expected.append(tuple(rng.randrange(8) for _ in range(8)))
        assert seen[name][:-1] == expected
        assert seen[name][-1] == tuple(range(8))
    first, second = (result[name] for name in comparisons)
    assert first["effect"] == second["effect"] == 3.5
    assert first["defined_resamples"] == 9999
    assert first["undefined_resamples"] == 1
    assert first["lower"] is first["upper"] is None
    assert second["defined_resamples"] == 10000
    assert second["undefined_resamples"] == 0
    effects = sorted(sum(indices) / 8 for indices in seen[comparisons[1]][:-1])
    assert second["lower"] == runner._percentile(effects, 0.025)
    assert second["upper"] == runner._percentile(effects, 0.975)
    runner._validate_bootstrap_intervals(result, protocol=value, failed=False)


def test_bootstrap_undefined_point_nulls_bounds_even_if_draws_defined(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = _statistics_protocol(resamples=3)
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = ["synthetic"]
    rows = _synthetic_statistics_rows(value)
    effects = iter([0.1, 0.2, 0.3, None])
    monkeypatch.setattr(runner, "_comparison_effect", lambda *_args, **_kwargs: next(effects))
    result = runner._bootstrap_intervals(rows, protocol=value)
    assert result["synthetic"]["effect"] is None
    assert result["synthetic"]["lower"] is result["synthetic"]["upper"] is None
    assert result["synthetic"]["defined_resamples"] == 3
    assert result["synthetic"]["undefined_resamples"] == 0
    runner._validate_bootstrap_intervals(result, protocol=value, failed=False)


@pytest.mark.parametrize("finite_improvement", [False, True])
def test_null_point_gates_fail_and_strict_improvement_uses_finite_only(
    monkeypatch: pytest.MonkeyPatch, finite_improvement: bool,
) -> None:
    value = _statistics_protocol()
    rows = _synthetic_statistics_rows(value)
    metric_keys = value["artifacts"]["derived_contracts"]["pareto_frontier.json"]["metrics_fields"]

    def metrics(selected, *, protocol):
        result = dict.fromkeys(metric_keys)
        if finite_improvement:
            result["unnecessary_revision_rate"] = (
                0.0 if selected[0]["condition_id"] == "full_separated" else 0.1
            )
        return result

    monkeypatch.setattr(runner, "_pareto_metrics", metrics)
    monkeypatch.setattr(runner, "_bootstrap_intervals", lambda *_args, **_kwargs: {})
    support = runner._scientific_support(rows, protocol=value)
    assert support["residual_gate"] == {
        "full_recovery_rate": None, "no_residual_recovery_rate": None, "passed": False,
    }
    assert support["weighted_ce_noninferiority"]["ece"]["effect_full_minus_weighted_ce"] is None
    assert support["weighted_ce_noninferiority"]["ece"]["passed"] is False
    assert support["strict_improvement"]["effects"]["ece"] is None
    assert support["strict_improvement"]["passed"] is finite_improvement
    assert support["all_gates_passed"] is False
    assert support["status"] == "not_supported"


def test_all_abstain_statistics_validate_with_null_intervals() -> None:
    value = _statistics_protocol(resamples=2)
    artifact = runner._pareto_artifact(
        _synthetic_statistics_rows(value, mode="all_abstain"),
        protocol=value, source_commit="0" * 40,
    )
    runner._validate_pareto(artifact, value)
    support = artifact["scientific_support"]
    assert support["weighted_ce_noninferiority"]["ece"]["passed"] is False
    assert support["status"] == "not_supported"
    interval = support["bootstrap_intervals"]["full_minus_weighted_ce_ece"]
    assert interval["defined_resamples"] == 0
    assert interval["undefined_resamples"] == 2

    tampered = copy.deepcopy(artifact)
    tampered["scientific_support"]["weighted_ce_noninferiority"]["ece"]["passed"] = True
    with pytest.raises(RuntimeError, match="does not recalculate"):
        runner._validate_pareto(tampered, value)


@pytest.mark.parametrize("change", [
    {"defined_resamples": -1}, {"defined_resamples": True},
    {"defined_resamples": 7}, {"defined_resamples": None},
    {"undefined_resamples": None}, {"lower": 0.0}, {"extra": 0},
])
def test_nullable_interval_validator_rejects_bad_counts_bounds_and_keys(change: dict) -> None:
    value = _statistics_protocol(resamples=8)
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = ["synthetic"]
    interval = {
        "effect": 0.1, "lower": None, "upper": None,
        "resamples": 8, "bootstrap_seed": value["determinism"]["bootstrap_seed"],
        "defined_resamples": 5, "undefined_resamples": 3,
    }
    runner._validate_bootstrap_intervals({"synthetic": interval}, protocol=value, failed=False)
    interval.update(change)
    with pytest.raises(RuntimeError):
        runner._validate_bootstrap_intervals({"synthetic": interval}, protocol=value, failed=False)


def test_failed_seed_intervals_have_exact_seven_fields_without_bootstrap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = _statistics_protocol()

    def forbidden(*_args, **_kwargs):
        pytest.fail("failed seeds must not execute bootstrap")

    monkeypatch.setattr(runner, "_bootstrap_intervals", forbidden)
    failed = [{
        "model_seed": 99001, "phase": "training", "condition_id": "full_separated",
        "error_type": "SyntheticFailure",
        "error_hash": runner._sha256_bytes(
            runner._canonical(["training", "full_separated", "SyntheticFailure"]).encode()
        ),
    }]
    artifact = runner._pareto_artifact(
        [], protocol=value, source_commit="0" * 40, failed_seeds=failed
    )
    runner._validate_pareto(artifact, value)
    intervals = artifact["scientific_support"]["bootstrap_intervals"]
    for interval in intervals.values():
        assert interval == {
            "effect": None, "lower": None, "upper": None,
            "resamples": 8, "bootstrap_seed": value["determinism"]["bootstrap_seed"],
            "defined_resamples": None, "undefined_resamples": None,
        }
    broken = copy.deepcopy(intervals)
    next(iter(broken.values()))["defined_resamples"] = 0
    with pytest.raises(RuntimeError, match="failure fields must be null"):
        runner._validate_bootstrap_intervals(broken, protocol=value, failed=True)


@pytest.mark.parametrize("bounds", [(None, None), (None, 0.2), (0.3, 0.2)])
def test_defined_bootstrap_requires_both_ordered_finite_bounds(bounds) -> None:
    value = _statistics_protocol(resamples=8)
    value["determinism"]["bootstrap_algorithm"]["comparison_order"] = ["synthetic"]
    interval = {
        "effect": 0.1, "lower": bounds[0], "upper": bounds[1],
        "resamples": 8, "bootstrap_seed": value["determinism"]["bootstrap_seed"],
        "defined_resamples": 8, "undefined_resamples": 0,
    }
    with pytest.raises(RuntimeError, match="requires ordered finite bounds"):
        runner._validate_bootstrap_intervals({"synthetic": interval}, protocol=value, failed=False)


def test_seed_failures_are_atomic_sorted_and_message_free(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from sparkbrain.v03_learned import training
    from sparkbrain.v03_seed import revision_worlds

    value = protocol()
    value["seeds"]["model"] = [99001, 99002]
    monkeypatch.setattr(revision_worlds, "build_full_fixture", lambda _split: ())

    def fail_training(*_args: object, model_seed: int, **_kwargs: object) -> None:
        raise ValueError(f"local secret path for {model_seed}")

    monkeypatch.setattr(training, "train_condition", fail_training)
    raw, objective_config, loss, failed = runner._run_training_and_evaluation(
        protocol=value,
        source_commit="0" * 40,
    )
    assert raw == []
    assert loss["training_step_rows"] == []
    assert loss["condition_seed_rows"] == []
    assert loss["objective_rows"] == []
    assert [row["model_seed"] for row in failed] == [99001, 99002]
    assert all(row["phase"] == "training" for row in failed)
    assert all(row["condition_id"] == "full_separated" for row in failed)
    assert all(row["error_type"] == "ValueError" for row in failed)
    assert all("local" not in runner._canonical(row) for row in failed)
    assert objective_config["failed_seeds"] == loss["failed_seeds"] == failed
    assert len(loss["engineering_gates"]) == 8
    assert not all(row["passed"] for row in loss["engineering_gates"])


def test_training_preparation_failure_resets_phase_for_each_condition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from sparkbrain.v03_learned import training
    from sparkbrain.v03_seed import revision_worlds

    value = protocol()
    value["seeds"]["model"] = [99001]
    value["conditions"]["order"] = ["full_separated", "no_belief"]
    monkeypatch.setattr(revision_worlds, "build_full_fixture", lambda _split: ())

    model = SimpleNamespace(
        load_state_dict=lambda _state: None,
        eval=lambda: None,
    )
    snapshot = SimpleNamespace(state_dict={}, sha256="0" * 64)
    result = SimpleNamespace(
        training_step_rows=(),
        checkpoints={2: snapshot},
        model=model,
        parameter_count=3132,
    )
    monkeypatch.setattr(training, "train_condition", lambda *_args, **_kwargs: result)
    monkeypatch.setattr(training, "select_checkpoint", lambda _scores: SimpleNamespace(epoch=2))
    monkeypatch.setattr(
        training,
        "select_calibration",
        lambda _scores: SimpleNamespace(temperature=1.0, abstention_threshold=0.5),
    )
    monkeypatch.setattr(runner, "_checkpoint_scores", lambda *_args, **_kwargs: ())
    monkeypatch.setattr(runner, "_calibration_scores", lambda *_args, **_kwargs: ())

    calls = 0

    def fail_second_preparation(_episodes: object) -> str:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("condition preparation failed")
        return "0" * 64

    monkeypatch.setattr(runner, "_training_input_hash", fail_second_preparation)
    raw, _objective_config, loss, failed = runner._run_training_and_evaluation(
        protocol=value,
        source_commit="0" * 40,
    )

    assert raw == []
    assert loss["training_step_rows"] == []
    assert loss["condition_seed_rows"] == []
    assert failed == [
        {
            "model_seed": 99001,
            "phase": "training",
            "condition_id": "no_belief",
            "error_type": "RuntimeError",
            "error_hash": runner._sha256_bytes(
                runner._canonical(
                    ["training", "no_belief", "RuntimeError"]
                ).encode()
            ),
        }
    ]


def test_zero_success_failure_writes_exact_eight_and_empty_jsonl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value = protocol()
    value["seeds"]["model"] = [99001]
    error_type = "SyntheticFailure"
    failed = [
        {
            "model_seed": 99001,
            "phase": "training",
            "condition_id": "full_separated",
            "error_type": error_type,
            "error_hash": runner._sha256_bytes(
                runner._canonical(["training", "full_separated", error_type]).encode()
            ),
        }
    ]
    objective_config = runner._objective_config_artifact(
        [], protocol=value, source_commit="0" * 40, failed_seeds=failed
    )
    loss = {
        "schema_version": "0.3",
        "protocol_id": value["protocol_id"],
        "source_commit": "0" * 40,
        "objective_order": value["artifacts"]["derived_contracts"][
            "loss_ablation_metrics.json"
        ]["training_step_objective_keys"],
        "training_step_rows": [],
        "condition_seed_rows": [],
        "objective_rows": [],
        "engineering_gates": runner._engineering_gates(
            [], [], [], protocol=value, failed_seeds=failed
        ),
        "scientific_gates": {},
        "failed_seeds": failed,
    }
    monkeypatch.setattr(
        runner,
        "_run_training_and_evaluation",
        lambda **_kwargs: ([], objective_config, loss, failed),
    )
    output = tmp_path / "staged"
    result = runner._generate(
        output=output,
        protocol=value,
        protocol_bytes=runner._canonical(value).encode(),
        source_commit="0" * 40,
    )
    assert result["engineering_status"] == "implementation_failure"
    assert result["scientific_status"] == "not_evaluated_implementation_failure"
    assert result["failed_seeds"] == failed
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    assert (output / "per_transition_predictions.jsonl").read_bytes() == b""
    pareto = json.loads((output / "pareto_frontier.json").read_text(encoding="utf-8"))
    assert pareto["seed_points"] == []
    assert pareto["aggregate_points"] == []
    assert pareto["pairwise_dominance"] == []
    assert pareto["scientific_support"] == runner._failure_scientific_support(value)


def _stub_preflight(*_args: object, **_kwargs: object) -> tuple[dict, bytes, dict, dict]:
    value = protocol()
    return value, runner._canonical(value).encode(), {}, {}


def test_nonempty_output_is_preserved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "occupied"
    output.mkdir()
    marker = output / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    monkeypatch.setattr(runner, "_preflight", _stub_preflight)
    with pytest.raises(RuntimeError, match="new or empty"):
        runner.run(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output=output,
            source_commit="0" * 40,
        )
    assert marker.read_text(encoding="utf-8") == "keep"


def test_forced_failure_cleans_staging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "partial"
    monkeypatch.setattr(runner, "_preflight", _stub_preflight)

    def fail(*, output: Path, **_kwargs: object) -> dict[str, object]:
        output.mkdir(parents=True, exist_ok=True)
        (output / "partial.json").write_text("{}", encoding="utf-8")
        raise RuntimeError("injected failure")

    monkeypatch.setattr(runner, "_generate_isolated", fail)
    with pytest.raises(RuntimeError, match="injected failure"):
        runner.run(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output=output,
            source_commit="0" * 40,
        )
    assert not output.exists()
    assert list(tmp_path.glob(".partial.staging-*")) == []


def test_exact_eight_files_are_published_atomically(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "result"
    monkeypatch.setattr(runner, "_preflight", _stub_preflight)

    def generate(*, output: Path, **_kwargs: object) -> dict[str, object]:
        output.mkdir(parents=True, exist_ok=True)
        for name in runner.EXPECTED_FILES:
            (output / name).write_text("{}\n", encoding="utf-8")
        return {
            "engineering_passed": True,
            "scientific_status": "not_supported",
            "failed_seeds": [],
        }

    monkeypatch.setattr(runner, "_generate_isolated", generate)
    result = runner.run(
        root=ROOT,
        protocol_path=PROTOCOL_PATH,
        output=output,
        source_commit="0" * 40,
    )
    assert result["engineering_passed"] is True
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    assert list(tmp_path.glob(".result.staging-*")) == []


@pytest.mark.parametrize("existing_empty", [False, True])
def test_real_spawn_timeout_never_publishes_and_cleans_only_after_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, existing_empty: bool
) -> None:
    output = tmp_path / "timeout"
    if existing_empty:
        output.mkdir()
    context = multiprocessing.get_context("spawn")
    workers = []

    def sleeping_process(**_kwargs: object) -> object:
        # Use a picklable stdlib target; no official fixture/model/controller is executed.
        worker = context.Process(target=time.sleep, args=(30,), daemon=True)
        workers.append(worker)
        return worker

    monkeypatch.setattr(
        runner.multiprocessing, "get_context",
        lambda _method: SimpleNamespace(Pipe=context.Pipe, Process=sleeping_process),
    )
    value = protocol()
    value["determinism"]["official_run_timeout_seconds"] = 0.1
    monkeypatch.setattr(
        runner, "_preflight", lambda **_kwargs: (value, b"{}", {}, {})
    )
    started = time.monotonic()
    with pytest.raises(runner.C15RunTimeoutError, match="deadline"):
        runner.run(
            root=ROOT, protocol_path=PROTOCOL_PATH, output=output, source_commit="0" * 40
        )
    assert time.monotonic() - started < 15
    assert len(workers) == 1
    assert workers[0]._closed  # Process.close refuses a live worker.
    assert output.exists() is existing_empty
    if existing_empty:
        assert list(output.iterdir()) == []
    assert list(tmp_path.glob(".timeout.staging-*")) == []


def test_deadline_rejects_exit_confirmed_late_and_uses_frozen_escalation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []
    worker = SimpleNamespace(
        exitcode=None,
        join=lambda seconds: calls.append(("join", seconds)),
        is_alive=lambda: True,
        terminate=lambda: calls.append(("terminate",)),
        kill=lambda: calls.append(("kill",)),
    )
    clock = iter([10.0, 11.0])
    monkeypatch.setattr(runner.time, "monotonic", lambda: next(clock))
    with pytest.raises(runner.C15RunTimeoutError) as error:
        runner._wait_for_worker(worker, deadline=10.5, grace_seconds=5)
    assert error.value.worker_alive is True
    assert calls == [("join", 0.5), ("terminate",), ("join", 5), ("kill",), ("join", 5)]

    calls.clear()
    worker.exitcode = 0
    worker.is_alive = lambda: False
    clock = iter([10.0, 11.0])
    with pytest.raises(runner.C15RunTimeoutError):
        runner._wait_for_worker(worker, deadline=10.5, grace_seconds=5)
    assert calls == [("join", 0.5)]


def test_live_worker_staging_is_quarantined_and_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "quarantine"
    monkeypatch.setattr(runner, "_preflight", _stub_preflight)

    def fail(**kwargs: object) -> dict[str, object]:
        (kwargs["output"] / "partial.json").write_text("{}", encoding="utf-8")
        raise runner.C15RunTimeoutError("C15RunTimeoutError", worker_alive=True)

    monkeypatch.setattr(runner, "_generate_isolated", fail)
    with pytest.raises(runner.C15RunTimeoutError):
        runner.run(
            root=ROOT, protocol_path=PROTOCOL_PATH, output=output, source_commit="0" * 40
        )
    stages = list(tmp_path.glob(".quarantine.staging-*"))
    assert len(stages) == 1
    assert (stages[0] / "partial.json").is_file()
    assert str(stages[0].resolve()) in capsys.readouterr().err
    assert not output.exists()


def test_timeout_cli_exit_code_is_124(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(**_kwargs: object) -> dict[str, object]:
        raise runner.C15RunTimeoutError("C15RunTimeoutError: deadline")

    monkeypatch.setattr(runner, "run", fail)
    monkeypatch.setattr(sys, "argv", ["runner", "--output", "unused", "--source-commit", "0" * 40])
    assert runner.main() == 124
    assert "C15RunTimeoutError" in capsys.readouterr().err


@pytest.mark.parametrize("broken_method", ["terminate", "kill", "join", "is_alive"])
def test_process_control_errors_preserve_unconfirmed_worker_staging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, broken_method: str
) -> None:
    def fail(*_args: object) -> None:
        raise OSError("injected process control error")

    worker = SimpleNamespace(
        start=lambda: None, exitcode=None, join=lambda _seconds: None,
        terminate=lambda: None, kill=lambda: None, is_alive=lambda: True,
    )
    setattr(worker, broken_method, fail)
    connection = SimpleNamespace(close=lambda: None)
    context = SimpleNamespace(
        Process=lambda **_kwargs: worker, Pipe=lambda **_kwargs: (connection, connection)
    )
    monkeypatch.setattr(runner.multiprocessing, "get_context", lambda _method: context)
    monkeypatch.setattr(runner, "_preflight", _stub_preflight)
    output = tmp_path / "control-error"
    with pytest.raises(runner.C15WorkerError) as error:
        runner.run(
            root=ROOT, protocol_path=PROTOCOL_PATH, output=output, source_commit="0" * 40
        )
    assert error.value.worker_alive is True
    assert not output.exists()
    assert len(list(tmp_path.glob(".control-error.staging-*"))) == 1


def test_surviving_worker_cli_bypasses_unbounded_atexit_join(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(**_kwargs: object) -> dict[str, object]:
        raise runner.C15RunTimeoutError("C15RunTimeoutError: quarantined", worker_alive=True)

    def exit_now(code: int) -> None:
        raise SystemExit(code)

    monkeypatch.setattr(runner, "run", fail)
    monkeypatch.setattr(runner.os, "_exit", exit_now)
    monkeypatch.setattr(sys, "argv", ["runner", "--output", "unused", "--source-commit", "0" * 40])
    with pytest.raises(SystemExit) as result:
        runner.main()
    assert result.value.code == 124
    assert "quarantined" in capsys.readouterr().err


def test_actual_generation_worker_is_spawn_importable_without_evaluation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend(str(ROOT))
    module = importlib.import_module("scripts.run_c15_revision")
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    # Missing required arguments fail before _generate enters any fixture/model code.
    worker = context.Process(target=module._generation_worker, args=(sender, {}), daemon=True)
    try:
        deadline = time.monotonic() + 10
        worker.start()
        sender.close()
        module._wait_for_worker(worker, deadline=deadline, grace_seconds=5)
        assert worker.exitcode == 1
        assert not worker.is_alive()
        with pytest.raises((EOFError, OSError)):
            receiver.recv()
    finally:
        module._stop_worker(worker, grace_seconds=5)
        worker.close()
        sender.close()
        receiver.close()
