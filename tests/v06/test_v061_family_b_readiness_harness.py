from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.evaluation.v061_family_b_readiness_harness import (
    FamilyBGen1ReadinessFixture,
    load_readiness_fixture,
    run_construction_readiness,
)

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "fixtures"
    / "v061_a01_family_b_gen1_readiness_input.json"
)


def test_fixed_readiness_fixture_passes_all_construction_checks() -> None:
    fixture = load_readiness_fixture(FIXTURE_PATH)
    result = run_construction_readiness(fixture)

    assert result.fixture_id == "v061-a01-bgen1-readiness-input-v1"
    assert result.all_construction_checks_pass


def test_readiness_fixture_fails_closed_on_dimension_drift() -> None:
    fixture = load_readiness_fixture(FIXTURE_PATH)
    invalid = FamilyBGen1ReadinessFixture(
        fixture_id=fixture.fixture_id,
        width=fixture.width,
        decay=fixture.decay,
        left_activity=(1.0,),
        right_activity=fixture.right_activity,
        plural_activity=fixture.plural_activity,
        left_boundary_return=fixture.left_boundary_return,
        right_boundary_return=fixture.right_boundary_return,
        confirmation_sign=fixture.confirmation_sign,
        contradiction_sign=fixture.contradiction_sign,
    )

    with pytest.raises(ValueError, match="all readiness vectors must match fixture width"):
        run_construction_readiness(invalid)
