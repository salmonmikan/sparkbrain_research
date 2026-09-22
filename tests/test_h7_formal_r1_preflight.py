from __future__ import annotations

import pytest

from sparkbrain.learned.h7_formal_r1 import FormalIntegrityError
from sparkbrain.learned.h7_formal_r1_preflight import (
    RuntimeFreezeManifest,
    SeedCollisionAudit,
    SeedInventory,
    pip_freeze_digest,
)


def _runtime(**overrides: object) -> RuntimeFreezeManifest:
    values = {
        "python_patch": "3.11.13",
        "torch_version": "2.13.0",
        "os_runner_family": "ubuntu-24.04",
        "os_image_identifier": "gh-actions-ubuntu-24.04@sha256:" + "1" * 64,
        "pip_freeze_sha256": pip_freeze_digest("torch==2.13.0\nnumpy==2.3.0\n"),
        "device": "cpu",
        "cpu_threads": 1,
        "python_hash_seed": "0",
        "omp_num_threads": "1",
        "mkl_num_threads": "1",
        "torch_deterministic_algorithms": True,
    }
    values.update(overrides)
    return RuntimeFreezeManifest(**values)  # type: ignore[arg-type]


def test_runtime_manifest_requires_exact_freeze_material() -> None:
    manifest = _runtime()
    manifest.assert_formal_r1_contract()
    assert len(manifest.digest()) == 64
    with pytest.raises(FormalIntegrityError, match="exact image identifier"):
        _runtime(os_image_identifier="ubuntu-24.04").assert_formal_r1_contract()
    with pytest.raises(FormalIntegrityError, match="Python 3.11 patch"):
        _runtime(python_patch="3.11").assert_formal_r1_contract()
    with pytest.raises(FormalIntegrityError, match="torch version drift"):
        _runtime(torch_version="2.13.1").assert_formal_r1_contract()


def test_pip_freeze_digest_is_order_insensitive_but_content_sensitive() -> None:
    first = pip_freeze_digest("b==2\na==1\n")
    second = pip_freeze_digest("a==1\nb==2\n")
    assert first == second
    assert first != pip_freeze_digest("a==1\nb==3\n")


def _inventory(*, complete: bool = True, start: int = 100, end: int = 120) -> SeedInventory:
    return SeedInventory.from_ranges(
        inventory_id="PRIOR-EXPOSED-SURFACES-SENTINEL",
        source_sha256="a" * 64,
        complete=complete,
        ranges_inclusive=((start, end),),
    )


def test_seed_collision_audit_fails_closed_on_incomplete_inventory() -> None:
    audit = SeedCollisionAudit(
        audited_roles={"formal_evaluation": (1000, 1001)},
        inventories=(_inventory(complete=False),),
    )
    with pytest.raises(FormalIntegrityError, match="completeness is not established"):
        audit.run()


def test_seed_collision_audit_rejects_prior_and_internal_overlap() -> None:
    prior = SeedCollisionAudit(
        audited_roles={"formal_evaluation": (119, 1000)},
        inventories=(_inventory(),),
    )
    with pytest.raises(FormalIntegrityError, match="seed collision detected"):
        prior.run()

    internal = SeedCollisionAudit(
        audited_roles={"fit": (1000, 1001), "evaluation": (1001, 1002)},
        inventories=(_inventory(),),
    )
    with pytest.raises(FormalIntegrityError, match="seed collision detected"):
        internal.run()


def test_seed_collision_audit_passes_only_with_complete_disjoint_inventory() -> None:
    result = SeedCollisionAudit(
        audited_roles={
            "fit": (1000, 1001),
            "calibration": (2000,),
            "evaluation": (3000, 3001),
            "native_training": (4000,),
        },
        inventories=(_inventory(),),
    ).run()
    assert result["status"] == "PASS_NO_COLLISIONS"
    assert result["complete_inventory_required"] is True
    assert result["scientific_result"] is None
    assert result["formal_identity"] is None
