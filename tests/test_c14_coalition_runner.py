from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_c14_coalition_gate.py"
SPEC = importlib.util.spec_from_file_location("run_c14_coalition_gate", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def protocol() -> dict:
    return json.loads(
        (ROOT / "artifacts" / "v03" / "c14_coalition_gate" / "protocol.json").read_text(
            encoding="utf-8"
        )
    )


def test_fixed_logit_and_complete_fixture_hashes_match_freeze() -> None:
    value = protocol()
    fixed = runner._sha256_bytes(runner._canonical(runner.fixed_logit_payload(value)).encode())
    assert fixed == value["frozen_logits"]["sha256"]
    expected = value["final_pre_execution_freeze"]["fixture_generator"][
        "full_fixture_sha256_by_seed"
    ]
    assert {str(seed): runner.fixture_sha256(value, seed) for seed in value["seeds"]} == expected


def test_runner_guard_refuses_before_output_or_git_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "official-output"
    disabled_protocol = protocol()
    disabled_protocol["dependencies"]["runner_execution_allowed"] = False

    def forbidden_git(*args, **kwargs):
        raise AssertionError("source-pin-disabled runner must not access Git")

    disabled_bytes = json.dumps(disabled_protocol).encode("utf-8")
    monkeypatch.setattr(Path, "read_bytes", lambda self: disabled_bytes)
    monkeypatch.setattr(runner, "_git", forbidden_git)
    with pytest.raises(RuntimeError, match="disabled until the source-pin amendment"):
        runner.run(
            root=ROOT,
            protocol_path=(ROOT / "artifacts" / "v03" / "c14_coalition_gate" / "protocol.json"),
            output=output,
            source_commit="0" * 40,
        )
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


def test_runner_rejects_noncanonical_protocol_path_before_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    copied = tmp_path / "protocol.json"
    copied.write_text(json.dumps(protocol()), encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_git",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("Git must not run")),
    )
    with pytest.raises(RuntimeError, match="repository-fixed canonical path"):
        runner.run(
            root=ROOT,
            protocol_path=copied,
            output=tmp_path / "output",
            source_commit="0" * 40,
        )


def test_protocol_amendment_allows_only_pin_fields() -> None:
    base = copy.deepcopy(protocol())
    base["dependencies"].pop("c14_protocol_base_commit")
    base["dependencies"].pop("c14_protocol_base_sha256")
    base["dependencies"]["c14_source_pin"] = (
        "pending separate preregistration amendment after source-only commit "
        "and before any runner execution"
    )
    base["dependencies"]["runner_execution_allowed"] = False
    current = copy.deepcopy(base)
    current["dependencies"]["c14_protocol_base_commit"] = "79dfa6c" + "0" * 33
    current["dependencies"]["c14_protocol_base_sha256"] = "1" * 64
    current["dependencies"]["c14_source_pin"] = "2" * 40
    current["dependencies"]["runner_execution_allowed"] = True
    runner._validate_protocol_amendment(current, base)

    current["coalition_score"]["weights"]["activation"] = 0.99
    with pytest.raises(RuntimeError, match="beyond the authorized pin"):
        runner._validate_protocol_amendment(current, base)


def valid_candidate_term() -> dict[str, object]:
    value = protocol()
    fields = value["final_pre_execution_freeze"]["raw_artifact_contract"][
        "candidate_terms_required_fields"
    ]
    row: dict[str, object] = {field: 0.0 for field in fields}
    row.update(
        {
            "contradiction_evidence_ids": [],
            "entity_key": "object-a",
            "evidence_count": 2,
            "hypothesis_id": "hypothesis-alpha",
            "independent_group_count": 2,
            "source_count": 2,
            "stability": 2,
            "support_evidence_ids": ["evidence-a", "evidence-b"],
            "support_evidence_times": [10.0, 10.0],
        }
    )
    return row


def test_schema_helpers_reject_unknown_nonfinite_and_invalid_penalty() -> None:
    value = protocol()
    candidate = valid_candidate_term()
    runner._validate_candidate_term(candidate, value, "candidate")
    candidate["unknown"] = 1
    with pytest.raises(RuntimeError, match="missing or unknown keys"):
        runner._validate_candidate_term(candidate, value, "candidate")

    candidate = valid_candidate_term()
    candidate["score"] = float("nan")
    with pytest.raises(RuntimeError, match="finite number"):
        runner._validate_candidate_term(candidate, value, "candidate")

    candidate = valid_candidate_term()
    candidate["weighted_contradiction"] = 0.1
    with pytest.raises(RuntimeError, match="positive penalty"):
        runner._validate_candidate_term(candidate, value, "candidate")

    decision = {
        "citations": [],
        "ignited": False,
        "margin": 0.1,
        "reason": "score_below_threshold",
        "runner_up_score": 0.2,
        "score": 0.3,
        "winner_entity": None,
        "winner_hypothesis": None,
    }
    runner._validate_decision(decision, value, "decision")
    decision["extra"] = True
    with pytest.raises(RuntimeError, match="missing or unknown keys"):
        runner._validate_decision(decision, value, "decision")


def test_failed_seed_rows_recalculate_each_seed_independently(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = {"seeds": [2701, 2702]}
    raw = [{"seed": 2701}, {"seed": 2702}]
    removal = [{"seed": 2701}, {"seed": 2702}]

    def fake_gates(rows, removed, protocol_value, *, call_graph_probe):
        seed = rows[0]["seed"]
        assert removed[0]["seed"] == seed
        assert call_graph_probe
        return [{"gate_id": "seed-specific", "passed": seed == 2702}]

    monkeypatch.setattr(runner, "_engineering_gates", fake_gates)
    assert runner._failed_seed_rows(
        raw=raw,
        removal=removal,
        protocol=value,
        call_graph_probe=True,
    ) == [{"reasons": ["seed-specific"], "seed": 2701}]


def test_runtime_call_graph_probe_depends_on_score_mutation() -> None:
    assert runner._call_graph_probe()


def test_metric_rows_use_nested_decisions_for_cross_condition_metrics() -> None:
    value = protocol()
    rows: list[dict[str, object]] = []
    case_order = value["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
    decisions = {
        "G1_evidence_coalition": {
            "ignited": True,
            "reason": "ignited",
            "score": 0.8,
            "winner_hypothesis": "hypothesis-alpha",
        },
        "G0_probability_margin": {
            "ignited": False,
            "reason": "score_below_threshold",
            "score": 0.3,
            "winner_hypothesis": None,
        },
        "G1_no_coalition_ablation": {
            "ignited": False,
            "reason": "no_coalitions",
            "score": 0.0,
            "winner_hypothesis": None,
        },
    }
    for condition in value["conditions"]:
        for seed in value["seeds"]:
            for case_id in case_order:
                rows.append(
                    {
                        "case_id": case_id,
                        "comparators": {
                            "independent_support_baseline": {"decision": {"score": 0.4}},
                            "primary_support_only": {"decision": {"score": 0.5}},
                        },
                        "condition_id": condition,
                        "decision": decisions[condition],
                        "expected_winner": "hypothesis-alpha",
                        "primary": True,
                        "seed": seed,
                    }
                )

    aggregate, seed_rows = runner._metric_rows(rows, value)

    assert len(aggregate) == 24
    assert len(seed_rows) == 120
    aggregate_cross = [
        row
        for row in aggregate
        if row["metric"]
        in {
            "g1_vs_g0_decision_difference_rate",
            "g1_vs_no_coalition_decision_difference_rate",
        }
    ]
    seed_cross = [
        row
        for row in seed_rows
        if row["metric"]
        in {
            "g1_vs_g0_decision_difference_rate",
            "g1_vs_no_coalition_decision_difference_rate",
        }
    ]
    assert len(aggregate_cross) == 6
    assert len(seed_cross) == 30
    assert all(row["value"] == 1.0 for row in aggregate_cross + seed_cross)
    assert all(
        row["denominator"] == len(case_order) * len(value["seeds"])
        for row in aggregate_cross
    )
    assert all(row["denominator"] == len(case_order) for row in seed_cross)


def test_in_memory_evaluation_reaches_all_metric_and_gate_aggregates() -> None:
    value = protocol()
    fixture_hashes = {
        str(seed): runner.fixture_sha256(value, int(seed)) for seed in value["seeds"]
    }

    raw, removal = runner._run_evaluation(
        protocol=value,
        fixture_hashes=fixture_hashes,
        fixed_hash=value["frozen_logits"]["sha256"],
    )
    aggregate, seed_rows = runner._metric_rows(raw, value)
    paired = runner._paired_statistics(raw, value)
    call_graph_probe = runner._call_graph_probe()
    gates = runner._engineering_gates(
        raw,
        removal,
        value,
        call_graph_probe=call_graph_probe,
    )
    failed = runner._failed_seed_rows(
        raw=raw,
        removal=removal,
        protocol=value,
        call_graph_probe=call_graph_probe,
    )

    assert len(raw) == 360
    assert len(removal) == 15
    assert len(aggregate) == 24
    assert len(seed_rows) == 120
    assert len(paired) == 4
    assert len(gates) == 12
    assert isinstance(failed, list)


def test_expected_source_scope_and_exact_six_files_are_frozen() -> None:
    value = protocol()
    assert (
        tuple(value["final_pre_execution_freeze"]["manifest_contract"]["source_diff_scope"])
        == runner.SOURCE_PATHS
    )
    assert runner.EXPECTED_FILES == set(value["expected_files"])
