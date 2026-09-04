from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryPhase,
    PerturbationSeedSpec,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    ARTIFACT_PATHS,
    EXECUTION_COMMAND,
    build_freeze_record,
    frozen_manifest_for_test,
    require_execution_seal,
    validate_execution_seal,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
)

_FAKE_FROZEN_SHA = "a" * 40


def _synthetic_frozen_manifest():
    current = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    return frozen_manifest_for_test(current, code_ref=_FAKE_FROZEN_SHA)


def test_current_manifest_cannot_issue_an_executable_seal() -> None:
    current = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    record = build_freeze_record(current, approval="not-approved")
    report = validate_execution_seal(current, record)
    assert report.manifest_ready is False
    assert report.code_ref_matches is False
    assert report.execution_allowed is False
    with pytest.raises(RuntimeError, match="remains prohibited"):
        require_execution_seal(current, record)


def test_complete_synthetic_freeze_record_validates_without_running_capability() -> None:
    manifest = _synthetic_frozen_manifest()
    record = build_freeze_record(manifest, approval="unit-test-freeze-review")
    report = validate_execution_seal(manifest, record)
    assert report.manifest_ready is True
    assert report.code_ref_matches is True
    assert report.world_generation_matches is True
    assert report.world_grid_matches is True
    assert report.seeds_fresh_and_exact is True
    assert report.thresholds_match is True
    assert report.exclusions_match is True
    assert report.result_schema_matches is True
    assert report.resource_schema_matches is True
    assert report.adapter_inventory_matches is True
    assert report.execution_command_matches is True
    assert report.artifact_paths_match is True
    assert report.approval_present is True
    assert report.execution_allowed is True
    assert len(report.seal_hash) == 64


def test_any_frozen_hash_change_fails_closed() -> None:
    manifest = _synthetic_frozen_manifest()
    record = build_freeze_record(manifest, approval="unit-test-freeze-review")
    mutations = (
        replace(record, world_grid_hash="0" * 64),
        replace(record, manifest_hash="0" * 64),
        replace(record, thresholds_hash="0" * 64),
        replace(record, exclusions_hash="0" * 64),
        replace(record, result_schema_hash="0" * 64),
        replace(record, resource_schema_hash="0" * 64),
        replace(record, adapter_inventory_hash="0" * 64),
        replace(record, execution_command_hash="0" * 64),
        replace(record, artifact_path_hash="0" * 64),
        replace(record, world_generation_id="wrong-generation"),
        replace(record, approval=""),
    )
    for changed in mutations:
        report = validate_execution_seal(manifest, changed)
        assert report.execution_allowed is False
        with pytest.raises(RuntimeError, match="remains prohibited"):
            require_execution_seal(manifest, changed)


def test_quarantined_seed_set_can_never_validate_as_fresh() -> None:
    manifest = _synthetic_frozen_manifest()
    contaminated = replace(
        manifest,
        seeds=tuple(
            PerturbationSeedSpec(
                seed=seed,
                structural_token=f"quarantined:{seed}",
            )
            for seed in QUARANTINED_HELDOUT_SEEDS
        ),
    )
    record = build_freeze_record(contaminated, approval="unit-test-freeze-review")
    report = validate_execution_seal(contaminated, record)
    assert report.manifest_ready is True
    assert report.seeds_fresh_and_exact is False
    assert report.execution_allowed is False


def test_freeze_contract_names_all_required_outputs_and_command() -> None:
    assert HELDOUT_SEEDS == tuple(range(1000, 1010))
    assert WORLD_GENERATION_ID == "v06-confirmatory-candidate-002"
    assert EXECUTION_COMMAND.startswith("python -m ")
    assert len(ARTIFACT_PATHS) == 5
    assert len(set(ARTIFACT_PATHS)) == len(ARTIFACT_PATHS)
    assert all(path.startswith("artifacts/v06/confirmatory/") for path in ARTIFACT_PATHS)
