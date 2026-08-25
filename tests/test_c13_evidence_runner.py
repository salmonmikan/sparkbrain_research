from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

import sparkbrain
from sparkbrain.v03_seed import (
    E0_GLOBAL,
    E1_ORACLE_ENTITY,
    EvidenceLedger,
    EvidenceRecord,
    aggregate_condition_rows,
    build_evidence_fixture,
    decide_g0,
    fixture_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "artifacts" / "v03" / "c13_evidence_entity" / "protocol.json"
EXPECTED_HASHES = {
    2601: "9b0ea285b09f736910f868d4dbbcdfcb7f87209f673a1da33c5634f54d99135a",
    2602: "116d71f4509e23f43806e1d3838b1dd2151fe366c0e8ea7258cba7e1d5960371",
    2603: "79b1926328f5c1109d1b868344a5e2152a6cd5db59a7e88db1e5859d9e33d3bb",
    2604: "45ea4f2c9a614fb93abb81366703ae1e4e54b79fef4347cc5999972a757cabb8",
    2605: "e6fb2a8758b5d2e8f0c0aa2d32e50917d4aad47be9f9f14a5ceb8e82b561f827",
}


def runner_module():
    path = ROOT / "scripts" / "run_c13_evidence_entity.py"
    spec = importlib.util.spec_from_file_location("run_c13_evidence_entity", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_record(
    ledger: EvidenceLedger, evidence_id: str, hypothesis: str, strength: float
) -> None:
    sample_id = f"sample:{evidence_id}"
    spark_id = f"spark:{evidence_id}"
    ledger.register_sample(sample_id)
    ledger.register_spark(spark_id, (sample_id,))
    ledger.add(
        EvidenceRecord(
            evidence_id=evidence_id,
            source_id=evidence_id,
            entity_key="object-a",
            hypothesis_id=hypothesis,
            time=0.0,
            polarity="support",
            strength=strength,
            parent_spark_ids=(spark_id,),
        )
    )


def test_import_resolves_to_c13_worktree() -> None:
    assert Path(sparkbrain.__file__).resolve().is_relative_to(ROOT)


def test_fixture_hashes_exactly_match_final_freeze() -> None:
    assert {
        seed: fixture_sha256(build_evidence_fixture(seed))
        for seed in EXPECTED_HASHES
    } == EXPECTED_HASHES


def test_g0_uses_lexical_tie_break_and_abstains_without_margin() -> None:
    empty = EvidenceLedger()
    abstained = decide_g0(empty, entity_key="object-a", now=0.0)
    assert abstained.abstained and abstained.winner is None and abstained.citations == ()

    ledger = EvidenceLedger()
    add_record(ledger, "ev-left", "state-left", 1.0)
    add_record(ledger, "ev-right", "state-right", 1.0)
    decision = decide_g0(ledger, entity_key="object-a", now=0.0)
    assert decision.winner == "state-left"
    assert decision.citations == ("ev-left",)


def test_condition_aggregation_rejects_missing_or_mixed_ids() -> None:
    with pytest.raises(ValueError, match="requires condition_id"):
        aggregate_condition_rows([{"seed": 2601}], condition_id=E0_GLOBAL)
    with pytest.raises(ValueError, match="must not be merged"):
        aggregate_condition_rows(
            [{"condition_id": E0_GLOBAL}, {"condition_id": E1_ORACLE_ENTITY}],
            condition_id=E0_GLOBAL,
        )


def test_e1_non_target_snapshots_are_byte_identical_and_e0_is_separate() -> None:
    runner = runner_module()
    fixture = build_evidence_fixture(2601)
    e0_metrics, e0_rows, _ = runner._run_seed(
        condition_id=E0_GLOBAL, fixture=fixture
    )
    e1_metrics, e1_rows, _ = runner._run_seed(
        condition_id=E1_ORACLE_ENTITY, fixture=fixture
    )
    assert e0_metrics["condition_id"] == E0_GLOBAL
    assert e1_metrics["condition_id"] == E1_ORACLE_ENTITY
    assert e0_rows and e1_rows
    assert all(row["cross_talk_event"] for row in e0_rows)
    assert all(not row["cross_talk_event"] for row in e1_rows)
    assert all(row["non_target_snapshot_byte_identical"] for row in e1_rows)
    assert all(
        row["non_target_snapshot_before_sha256"]
        == row["non_target_snapshot_after_sha256"]
        for row in e1_rows
    )


def test_runner_refuses_nonempty_output(tmp_path: Path) -> None:
    runner = runner_module()
    output = tmp_path / "occupied"
    output.mkdir()
    marker = output / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="new or empty"):
        runner.run(
            root=ROOT,
            protocol_path=PROTOCOL,
            output=output,
            source_commit="0" * 40,
        )
    assert marker.read_text(encoding="utf-8") == "keep"


def test_atomic_staging_cleans_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = runner_module()
    monkeypatch.setattr(runner, "_verify_dependencies", lambda *_args: {})

    def fail_write(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("injected write failure")

    monkeypatch.setattr(runner, "_write_jsonl", fail_write)
    output = tmp_path / "partial"
    with pytest.raises(RuntimeError, match="injected write failure"):
        runner.run(
            root=ROOT,
            protocol_path=PROTOCOL,
            output=output,
            source_commit="0" * 40,
        )
    assert not output.exists()
    assert list(tmp_path.glob(".partial.staging-*")) == []


def test_runner_writes_exact_eight_files_with_no_e2_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = runner_module()
    monkeypatch.setattr(runner, "_verify_dependencies", lambda *_args: {})
    output = tmp_path / "result"
    result = runner.run(
        root=ROOT,
        protocol_path=PROTOCOL,
        output=output,
        source_commit="0" * 40,
    )
    assert result["acceptance_passed"] is True
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    metrics = json.loads(
        (output / "entity_condition_metrics.json").read_text(encoding="utf-8")
    )
    assert metrics["e2_execution_rows"] == 0
    assert set(metrics["conditions"]) == {E0_GLOBAL, E1_ORACLE_ENTITY}
