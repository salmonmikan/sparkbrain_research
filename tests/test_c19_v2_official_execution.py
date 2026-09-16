from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.v03_external_validation.official_execution import (
    EXECUTION_HARNESS_ID,
    FROZEN_PROTOCOL_HEAD,
    ExecutionAdmission,
    OneWayExecutionHarness,
    PreservationReceipt,
    RawBundle,
    RuntimeBoundary,
    reconstruct_raw_jsonl,
    runtime_manifest,
    validate_executor_registry,
    write_raw_jsonl_no_clobber,
)
from sparkbrain.v03_external_validation.official_protocol import BASELINES, expected_row_inventory


def synthetic_executor(row, examples):
    return [
        {
            "record_id": str(example["record_id"]),
            "source_index": int(example["source_index"]),
            "pair_index": int(example["pair_index"]),
            "prediction": "A",
            "metadata": {"synthetic": True, "row_kind": row["row_kind"]},
        }
        for example in examples
    ]


def baseline_registry():
    return {name: synthetic_executor for name in BASELINES}


def test_runtime_manifest_binds_frozen_protocol_and_blocks_network() -> None:
    manifest = runtime_manifest()
    assert manifest["execution_harness_id"] == EXECUTION_HARNESS_ID
    assert manifest["frozen_protocol_head"] == FROZEN_PROTOCOL_HEAD
    assert manifest["network_allowed"] is False
    assert manifest["official_fit_tune_select_allowed"] is False
    assert manifest["stdlib_only_harness"] is True


def test_official_admission_fails_closed_without_analyst_started_and_exact_package() -> None:
    admission = ExecutionAdmission(
        scope="official_one_way",
        evidence_analyst_commit=None,
        exact_package_commit=None,
        started_ref=None,
    )
    with pytest.raises(ValueError, match="fresh Analyst admission"):
        admission.validate()


def test_runtime_boundary_rejects_network_or_official_tuning() -> None:
    with pytest.raises(ValueError, match="network-blocked"):
        RuntimeBoundary(network_allowed=True).validate()
    with pytest.raises(ValueError, match="fit/tune/select"):
        RuntimeBoundary(official_fit_tune_select_allowed=True).validate()


def test_executor_registry_requires_all_five_frozen_baselines() -> None:
    incomplete = baseline_registry()
    incomplete.pop(next(iter(incomplete)))
    with pytest.raises(ValueError, match="frozen five"):
        validate_executor_registry(synthetic_executor, incomplete)


def test_synthetic_harness_executes_exact_55_rows_without_targets() -> None:
    written: list[RawBundle] = []
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())
    raw = harness.acquire(
        admission=ExecutionAdmission.synthetic_dev(),
        examples=({"record_id": "synthetic-1", "source_index": 0, "pair_index": 0},),
        condition_executor=synthetic_executor,
        baseline_executors=baseline_registry(),
        raw_writer=written.append,
    )
    assert len(expected_row_inventory()) == 55
    assert len(raw.records) == 55
    assert {record["row_id"] for record in raw.records} == {
        row["row_id"] for row in expected_row_inventory()
    }
    assert written == [raw]


def test_raw_target_leakage_fails_closed() -> None:
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())

    def leaking_executor(row, examples):
        rows = synthetic_executor(row, examples)
        rows[0]["metadata"]["ground_truth"] = "A"
        return rows

    with pytest.raises(ValueError, match="target leakage"):
        harness.acquire(
            admission=ExecutionAdmission.synthetic_dev(),
            examples=({"record_id": "synthetic-1", "source_index": 0, "pair_index": 0},),
            condition_executor=leaking_executor,
            baseline_executors={name: leaking_executor for name in BASELINES},
            raw_writer=lambda raw: None,
        )


def test_no_clobber_blocks_second_acquisition() -> None:
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())
    kwargs = {
        "admission": ExecutionAdmission.synthetic_dev(),
        "examples": ({"record_id": "synthetic-1", "source_index": 0, "pair_index": 0},),
        "condition_executor": synthetic_executor,
        "baseline_executors": baseline_registry(),
        "raw_writer": lambda raw: None,
    }
    harness.acquire(**kwargs)
    with pytest.raises(RuntimeError, match="no-clobber"):
        harness.acquire(**kwargs)


def test_preservation_is_required_before_scoring_and_digest_is_bound() -> None:
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())
    raw = harness.acquire(
        admission=ExecutionAdmission.synthetic_dev(),
        examples=({"record_id": "synthetic-1", "source_index": 0, "pair_index": 0},),
        condition_executor=synthetic_executor,
        baseline_executors=baseline_registry(),
        raw_writer=lambda bundle: None,
    )
    with pytest.raises(RuntimeError, match="preserved before scoring"):
        harness.score(evaluator_targets={}, scorer=lambda bundle, targets: {})

    receipt = harness.preserve(
        preserver=lambda bundle: PreservationReceipt(
            raw_sha256=bundle.sha256,
            preserve_ref="synthetic-preserve:fixture",
            immutable=True,
        )
    )
    assert receipt.raw_sha256 == raw.sha256
    scored = harness.score(
        evaluator_targets={"synthetic": True},
        scorer=lambda bundle, targets: {
            "raw_sha256": bundle.sha256,
            "target_fixture": targets["synthetic"],
        },
    )
    assert scored == {"raw_sha256": raw.sha256, "target_fixture": True}


def test_raw_jsonl_is_no_clobber_and_reconstructable(tmp_path: Path) -> None:
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())
    output = tmp_path / "raw.jsonl"
    raw = harness.acquire(
        admission=ExecutionAdmission.synthetic_dev(),
        examples=({"record_id": "synthetic-1", "source_index": 0, "pair_index": 0},),
        condition_executor=synthetic_executor,
        baseline_executors=baseline_registry(),
        raw_writer=lambda bundle: write_raw_jsonl_no_clobber(output, bundle),
    )
    reconstructed = reconstruct_raw_jsonl(output, expected_sha256=raw.sha256)
    assert reconstructed == raw
    with pytest.raises(FileExistsError):
        write_raw_jsonl_no_clobber(output, raw)
