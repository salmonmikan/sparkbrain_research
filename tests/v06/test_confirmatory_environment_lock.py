from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory_environment import (
    ENVIRONMENT_LOCK_VERSION,
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
    environment_lock_from_state,
    verify_environment_lock,
)


def _synthetic_lock() -> ConfirmatoryEnvironmentLock:
    distributions = (
        "pip==24.0",
        "setuptools==70.0.0",
        "sparkbrain-research==0.3.2.dev0",
    )
    from sparkbrain.v06.foundation import digest

    return ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation="CPython",
        python_version="3.11.9",
        python_executable_sha256="a" * 64,
        platform_system="Linux",
        platform_release="6.8.0-test",
        platform_machine="x86_64",
        os_release=(("ID", "ubuntu"), ("VERSION_ID", "24.04")),
        runner_os="Linux",
        runner_arch="X64",
        runner_image_os="ubuntu24",
        runner_image_version="20260825.1.0",
        python_hash_seed="0",
        timezone="UTC",
        locale_name="C.UTF-8",
        installed_distributions=distributions,
        installed_distributions_hash=digest(list(distributions)),
        rng_contract_hash=RNG_CONTRACT.contract_hash(),
    )


def test_rng_contract_is_fixed_and_hashable() -> None:
    RNG_CONTRACT.validate()
    assert RNG_CONTRACT.algorithm == "python.random.Random-MT19937"
    assert RNG_CONTRACT.global_rng_allowed is False
    assert RNG_CONTRACT.python_hash_seed == "0"
    assert len(RNG_CONTRACT.contract_hash()) == 64


def test_environment_lock_round_trips_and_matches_exactly() -> None:
    lock = _synthetic_lock()
    lock.validate()
    restored = environment_lock_from_state(lock.state_dict())
    assert restored == lock
    report = verify_environment_lock(lock, restored)
    assert report.exact_match is True
    assert report.mismatched_fields == ()
    assert report.expected_hash == report.observed_hash == lock.environment_hash()


def test_any_environment_or_dependency_change_is_visible() -> None:
    lock = _synthetic_lock()
    changed = replace(lock, python_version="3.11.10")
    report = verify_environment_lock(lock, changed)
    assert report.exact_match is False
    assert report.mismatched_fields == ("python_version",)

    changed_distributions = replace(
        lock,
        installed_distributions=("pip==25.0",),
        installed_distributions_hash="0" * 64,
    )
    with pytest.raises(ValueError, match="distribution hash mismatch"):
        changed_distributions.validate()


def test_policy_rejects_wrong_python_hash_seed_timezone_or_locale() -> None:
    lock = _synthetic_lock()
    with pytest.raises(ValueError, match="PYTHONHASHSEED"):
        replace(lock, python_hash_seed="random").validate()
    with pytest.raises(ValueError, match="timezone"):
        replace(lock, timezone="Asia/Tokyo").validate()
    with pytest.raises(ValueError, match="locale"):
        replace(lock, locale_name="en_US.UTF-8").validate()


def test_candidate_world_generator_uses_local_rng_only() -> None:
    path = Path(
        "src/sparkbrain/evaluation/v06_confirmatory_heldout_spec.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"))
    random_attribute_calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "random"
    }
    assert "Random" in random_attribute_calls
    assert random_attribute_calls.isdisjoint(
        {
            "choice",
            "choices",
            "randint",
            "random",
            "randrange",
            "sample",
            "seed",
            "shuffle",
            "uniform",
        }
    )
