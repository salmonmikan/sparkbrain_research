from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sparkbrain.v03_external_validation.implementation_binding import (
    BINDING_ID,
    baseline_registry,
    binding_manifest,
    condition_executor,
)
from sparkbrain.v03_external_validation.official_execution import (
    ExecutionAdmission,
    OneWayExecutionHarness,
    RuntimeBoundary,
)

ROOT = Path(__file__).parents[1]
BINDING_PATH = ROOT / "artifacts/v03/c19_external_validation/v2/implementation_binding.json"


def _examples():
    return (
        {
            "record_id": "synthetic-pair-0-step-0",
            "source_index": 0,
            "pair_index": 0,
            "step_index": 0,
            "question": (
                "Ada is a bird. If Ada is a bird, Ada flies. "
                "What necessarily had to follow?"
            ),
            "choices": ("Ada flies", "Ada does not fly", "Nothing follows"),
        },
        {
            "record_id": "synthetic-pair-0-step-1",
            "source_index": 1,
            "pair_index": 0,
            "step_index": 1,
            "question": (
                "Ada is a bird. Ada is injured. If Ada is injured, Ada does not fly. "
                "What necessarily had to follow?"
            ),
            "choices": ("Ada flies", "Ada does not fly", "Nothing follows"),
        },
    )


def _condition_row(gate: str):
    return {
        "row_kind": "c19_condition",
        "input_track": "I2_truth_free_symbolic_surface",
        "gate": gate,
        "entity": "E0_global",
        "seed": 15901,
    }


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def test_i2_representation_is_byte_identical_across_g0_and_g1() -> None:
    g0 = condition_executor(_condition_row("G0_probability_margin"), _examples())[0]
    g1 = condition_executor(_condition_row("G1_coalition"), _examples())[0]
    assert g0["metadata"]["representation_sha256"] == g1["metadata"]["representation_sha256"]
    assert g0["metadata"]["binding_id"] == BINDING_ID
    assert g1["metadata"]["binding_id"] == BINDING_ID


def test_direct_and_explicit_state_baselines_receive_exact_i2_bytes() -> None:
    registry = baseline_registry()
    rows = {}
    for kind in ("direct_stateless", "explicit_state_probabilistic"):
        rows[kind] = registry[kind](
            {"row_kind": "baseline", "baseline_kind": kind, "seed": 15901},
            _examples(),
        )[0]
    c19 = condition_executor(_condition_row("G1_coalition"), _examples())[0]
    expected = c19["metadata"]["representation_sha256"]
    assert rows["direct_stateless"]["metadata"]["representation_sha256"] == expected
    assert rows["explicit_state_probabilistic"]["metadata"]["representation_sha256"] == expected


def test_binding_manifest_freezes_confound_and_claim_boundaries() -> None:
    manifest = binding_manifest()
    confounds = manifest["representation_confounds"]
    assert confounds["I2_G0_G1_byte_identity_required"] is True
    assert confounds["direct_stateless_exact_I2"] is True
    assert confounds["explicit_state_probabilistic_exact_I2"] is True
    assert confounds["persistent_state_novelty_claim_allowed"] is False
    assert confounds["isolation_axis_tested"] is False
    assert manifest["official_fit_tune_select"] is False


def test_bound_executors_run_the_exact_55_row_synthetic_harness() -> None:
    written = []
    harness = OneWayExecutionHarness(boundary=RuntimeBoundary())
    raw = harness.acquire(
        admission=ExecutionAdmission.synthetic_dev(),
        examples=_examples(),
        condition_executor=condition_executor,
        baseline_executors=baseline_registry(),
        raw_writer=written.append,
    )
    assert len(raw.records) == 55
    assert written == [raw]
    assert all(record["metadata"]["binding_id"] == BINDING_ID for record in raw.records)


def test_binding_artifact_matches_exact_source_input_and_runtime_blobs() -> None:
    value = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    assert value["binding_id"] == BINDING_ID
    assert value["official_execution_allowed"] is False
    paths = {
        "implementation_binding.py": ROOT
        / "src/sparkbrain/v03_external_validation/implementation_binding.py",
        "test_c19_v2_implementation_binding.py": ROOT
        / "tests/test_c19_v2_implementation_binding.py",
        "truth_free_adapter.py": ROOT
        / "src/sparkbrain/v03_external_validation/truth_free_adapter.py",
        "input_diagnosis.py": ROOT / "src/sparkbrain/v03_seed/input_diagnosis.py",
        "coalition.py": ROOT / "src/sparkbrain/v03_seed/coalition.py",
        "official_execution.py": ROOT
        / "src/sparkbrain/v03_external_validation/official_execution.py",
        "official_protocol.json": ROOT
        / "artifacts/v03/c19_external_validation/v2/official_protocol.json",
        "pyproject.toml": ROOT / "pyproject.toml",
    }
    assert set(value["bound_source_blobs"]) == set(paths)
    for name, path in paths.items():
        assert _git_blob_sha1(path) == value["bound_source_blobs"][name]
    runtime = value["runtime_binding"]
    assert runtime["official_python_implementation"] == "CPython"
    assert runtime["official_python_version"] == "3.11.16"
    assert runtime["external_runtime_dependencies_required_by_bound_executors"] == []
    assert value["resource_matching_policy"]["parameter_match_asserted"] is False
    assert value["resource_matching_policy"]["compute_match_asserted"] is False
