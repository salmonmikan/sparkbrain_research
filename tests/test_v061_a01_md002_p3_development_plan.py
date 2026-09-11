from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.v061_a01.md002_fixtures import FrozenPartitionBytes
from sparkbrain.v061_a01.md002_p3_development_plan import build_p3_development_plan
from sparkbrain.v061_a01.md002_p3_fixture import P3ReturnAddressFixture


def _fixture() -> P3ReturnAddressFixture:
    return P3ReturnAddressFixture(
        baseline=FrozenPartitionBytes(
            local=b"same-local",
            field=b"same-field",
            consistency=b"same-consistency",
            return_address=b"baseline-return-address",
        ),
        donor=FrozenPartitionBytes(
            local=b"same-local",
            field=b"same-field",
            consistency=b"same-consistency",
            return_address=b"donor-return-address",
        ),
        admissible_external_evidence=b"fixed-external-evidence",
    )


def test_p3_plan_binds_exact_three_r_only_conditions() -> None:
    rows = build_p3_development_plan(_fixture())

    assert tuple(row.condition_id for row in rows) == (
        "p3-baseline",
        "p3-donor",
        "p3-transplanted",
    )
    by_arm = {row.arm: row for row in rows}
    baseline = by_arm["baseline"].arm_input.partitions
    donor = by_arm["donor"].arm_input.partitions
    transplanted = by_arm["transplanted"].arm_input.partitions

    assert baseline.local == donor.local == transplanted.local
    assert baseline.field == donor.field == transplanted.field
    assert baseline.consistency == donor.consistency == transplanted.consistency
    assert baseline.return_address != donor.return_address
    assert transplanted.return_address == donor.return_address
    assert len({row.admissible_external_evidence_sha256 for row in rows}) == 1
    assert len({row.observation_schema_sha256 for row in rows}) == 1
    assert len({row.negative_stop_schema_sha256 for row in rows}) == 1


def test_p3_plan_contract_contains_no_predeclared_capability_outcome() -> None:
    rows = build_p3_development_plan(_fixture())

    schema = rows[0].observation_schema.decode("utf-8")
    assert '"execution_authority":false' in schema
    assert '"expected_outcome":null' in schema
    assert '"score":null' in schema
    stop = rows[0].negative_stop_schema.decode("utf-8")
    assert '"same_identity_rerun_for_rescue":false' in stop
    assert '"formal_or_held_out_authority":false' in stop


def test_p3_plan_rejects_observation_contract_drift() -> None:
    row = build_p3_development_plan(_fixture())[0]
    drifted = replace(row, observation_schema=b"drift")

    with pytest.raises(ValueError, match="observation contract drifted"):
        drifted.validate()


def test_p3_plan_rejects_non_r_donor_drift_before_construction() -> None:
    fixture = P3ReturnAddressFixture(
        baseline=FrozenPartitionBytes(
            local=b"baseline-local",
            field=b"same-field",
            consistency=b"same-consistency",
            return_address=b"baseline-return-address",
        ),
        donor=FrozenPartitionBytes(
            local=b"donor-local",
            field=b"same-field",
            consistency=b"same-consistency",
            return_address=b"donor-return-address",
        ),
        admissible_external_evidence=b"fixed-external-evidence",
    )

    with pytest.raises(ValueError, match="donor drifted from baseline in local"):
        build_p3_development_plan(fixture)
