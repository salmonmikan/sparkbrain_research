from __future__ import annotations

from pathlib import Path

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_adapter_review import (
    EXPECTED_PRIVILEGES,
    EXPECTED_THRESHOLD_BYPASS,
    adapter_source_inventory_hash,
    expected_privilege_inventory_hash,
    expected_threshold_mode_hash,
    review_adapter_sources,
)


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def test_real_adapter_source_review_is_complete() -> None:
    report = review_adapter_sources(_repository_root())
    assert report.complete is True, report.state_dict()
    assert report.missing_source_paths == ()
    assert report.unknown_parameter_members == ()
    assert report.missing_required_fields == ()
    assert report.candidate_builder_imports == ()
    assert report.forbidden_comparator_imports == ()
    assert report.missing_validation_calls == ()
    assert report.missing_specification_hash_calls == ()


def test_each_condition_has_a_hashed_field_read_inventory() -> None:
    report = review_adapter_sources(_repository_root())
    inventories = {row.condition: row for row in report.inventories}
    assert set(inventories) == set(ConfirmatoryCondition)
    for condition, row in inventories.items():
        assert row.source_paths
        assert row.source_hashes
        assert all(len(source_hash) == 64 for _, source_hash in row.source_hashes)
        assert set(row.required_parameter_fields).issubset(row.parameter_fields_read)
        assert row.calls_validate is True
        assert row.calls_specification_hash is True
        assert row.expected_privileges == EXPECTED_PRIVILEGES[condition]
        assert row.threshold_bypassed is EXPECTED_THRESHOLD_BYPASS[condition]
    assert len(adapter_source_inventory_hash(_repository_root())) == 64


def test_comparators_do_not_import_primary_runtime_or_candidate_builders() -> None:
    report = review_adapter_sources(_repository_root())
    for row in report.inventories:
        assert row.candidate_builder_imports == ()
        if row.condition in {
            ConfirmatoryCondition.G3_RECURRENT,
            ConfirmatoryCondition.G4_ASSEMBLY,
            ConfirmatoryCondition.G5_TYPED,
        }:
            assert row.forbidden_comparator_imports == ()
            assert not any(
                module.startswith("sparkbrain.v06")
                for module in row.imported_modules
            )


def test_input_omissions_are_explicitly_inventory_visible() -> None:
    report = review_adapter_sources(_repository_root())
    inventories = {row.condition: row for row in report.inventories}
    primary = inventories[ConfirmatoryCondition.PRIMARY]
    g3 = inventories[ConfirmatoryCondition.G3_RECURRENT]
    assert "threshold" in primary.parameter_fields_read
    assert "evaluation_lags_ms" in primary.parameter_fields_read
    assert "threshold" in g3.parameter_fields_not_directly_read
    assert "evaluation_lags_ms" in g3.parameter_fields_not_directly_read
    assert g3.threshold_bypassed is True


def test_privilege_and_threshold_mode_inventories_are_hashable() -> None:
    assert len(expected_privilege_inventory_hash()) == 64
    assert len(expected_threshold_mode_hash()) == 64
