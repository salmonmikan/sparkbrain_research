from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import classify_filename

ROOT = Path(__file__).resolve().parents[1]


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
    assert classify_filename("test_v031_brain_lab_api.py", "test_v03_api") == (
        "integration",
    )
    collected = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-m",
            "integration",
            "tests/test_v031_brain_lab_api.py",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert collected.returncode == 0
    assert "5 tests collected" in collected.stdout
