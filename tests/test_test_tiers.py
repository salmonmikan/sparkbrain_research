from __future__ import annotations

from conftest import classify_filename


def test_scientific_models_are_separate_from_small_runner_correctness() -> None:
    assert classify_filename("test_c17_organs.py", "test_fixture_schema_identity") == (
        "scientific",
        "slow",
    )
    assert classify_filename("test_c17_organ_runner.py", "test_disabled_preregistration") == ()


def test_expensive_reproduction_orchestration_is_not_a_developer_regression() -> None:
    assert classify_filename(
        "test_c17_organ_runner.py", "test_reproduce_parent_orchestrates_two_attested_workers"
    ) == ("reproduction", "slow")


def test_external_and_local_service_boundaries_are_distinguished() -> None:
    assert classify_filename("test_c19_readiness_bundle.py", "test_bundle") == ("external", "slow")
    assert classify_filename("test_brain_lab_api.py", "test_api") == ("integration",)
