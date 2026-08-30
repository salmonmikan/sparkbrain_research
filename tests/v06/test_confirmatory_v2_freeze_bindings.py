from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory_adapter_registry_v2 import (
    ADAPTERS_V2,
    ADAPTER_PATHS_V2,
    validate_adapter_registry_v2,
)
from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_bundle_v2 import (
    _ADAPTER_SOURCE_PATHS,
    _CONTRACT_SOURCE_PATHS,
    combined_training_schedule_hash,
)
from sparkbrain.evaluation.v06_confirmatory_schedule_contract import (
    training_schedule_grid_hash,
)

_SOURCE_SHA = "a" * 40


def test_v2_registry_paths_are_exact_executed_callable_paths() -> None:
    validate_adapter_registry_v2()
    assert set(ADAPTERS_V2) == set(ADAPTER_PATHS_V2)
    assert {
        condition: f"{adapter.__module__}.{adapter.__name__}"
        for condition, adapter in ADAPTERS_V2.items()
    } == ADAPTER_PATHS_V2


def test_candidate_manifest_uses_the_formal_v2_registry_exactly() -> None:
    manifest = build_candidate_manifest(source_code_sha=_SOURCE_SHA)
    assert {
        row.condition: row.adapter_path for row in manifest.conditions
    } == ADAPTER_PATHS_V2
    assert all(row.adapter_ready for row in manifest.conditions)


def test_freeze_inventory_hashes_the_registry_executed_by_formal_runner() -> None:
    assert (
        "src/sparkbrain/evaluation/v06_confirmatory_adapter_registry_v2.py"
        in _ADAPTER_SOURCE_PATHS
    )
    assert (
        "src/sparkbrain/evaluation/v06_confirmatory_adapter_registry.py"
        not in _ADAPTER_SOURCE_PATHS
    )
    assert (
        "src/sparkbrain/evaluation/v06_confirmatory_execute_external_v2.py"
        in _CONTRACT_SOURCE_PATHS
    )
    assert (
        "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
        in _CONTRACT_SOURCE_PATHS
    )
    assert (
        "src/sparkbrain/evaluation/v06_confirmatory_normalized_resource_v2.py"
        in _CONTRACT_SOURCE_PATHS
    )


def test_frozen_schedule_hash_is_the_formal_world_schedule_grid_hash() -> None:
    assert combined_training_schedule_hash() == training_schedule_grid_hash()
