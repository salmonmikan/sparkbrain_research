"""Central test-tier classification; keep small runner correctness tests in the default suite."""

from __future__ import annotations

from pathlib import Path

import pytest

SCIENTIFIC_MODULES = {
    "test_c15_revision.py",
    "test_c16_concepts.py",
    "test_c17_organs.py",
}

REPRODUCTION_MODULES = {
    "test_clean_room_release.py",
    "test_release.py",
    "test_release_archive_mode.py",
    "test_release_artifacts.py",
    "test_release_candidate.py",
    "test_review_bundle.py",
    "test_v03_private_review_bundle.py",
    "test_v03_release_artifacts.py",
    "test_v03_release_compatibility.py",
}

EXTERNAL_MODULES = {
    "test_c19_external_validation.py",
    "test_c19_readiness_bundle.py",
    "test_external_model_evaluation.py",
    "test_external_validation.py",
}

INTEGRATION_MODULES = {
    "test_brain_lab_api.py",
    "test_brain_lab_e2e.py",
    "test_brain_lab_service.py",
}

REPRODUCTION_NODEIDS = {
    (
        "test_c17_organ_runner.py",
        "test_reproduce_parent_orchestrates_two_attested_workers",
    ),
}


def classify_filename(filename: str, test_name: str) -> tuple[str, ...]:
    """Return the marker names for one collected test without moving its module."""
    if (filename, test_name) in REPRODUCTION_NODEIDS:
        return ("reproduction", "slow")
    if filename in SCIENTIFIC_MODULES:
        return ("scientific", "slow")
    if filename in REPRODUCTION_MODULES:
        return ("reproduction", "slow")
    if filename in EXTERNAL_MODULES:
        return ("external", "slow")
    if filename in INTEGRATION_MODULES:
        return ("integration",)
    return ()


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Assign tiers from module responsibility without moving test files."""
    for item in items:
        filename = Path(str(item.fspath)).name
        for marker in classify_filename(filename, item.name):
            item.add_marker(getattr(pytest.mark, marker))
