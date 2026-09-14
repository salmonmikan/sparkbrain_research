"""Fail-closed retained-history reconstruction for prospective RV01 R01-16.

The collision authority is deliberately limited to repository-retained consumed
or reserved seed/world execution identities. Earlier RV01 source exploration is
not erased or claimed absent; the retained namespace boundary is separately
bound and audited.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .rv01.activity_matched_contract import (
    R01_13_DEVELOPMENT_SEEDS,
    R01_13_HELD_OUT_SEEDS,
)
from .rv01.interference_contract import (
    DEVELOPMENT_SEEDS,
    HELD_OUT_SEEDS,
    InterferenceFamily,
)
from .rv01.post_spike_suppression_contract import (
    R01_15_DEVELOPMENT_SEEDS,
    R01_15_HELD_OUT_SEEDS,
)
from .rv01.traversal_dynamics_contract import (
    R01_14_DEVELOPMENT_SEEDS,
    R01_14_HELD_OUT_SEEDS,
)
from .rv01_r01_16_development_package import R0116CollisionRegistry

_BINDINGS_PATH = "docs/research/RV01_R01_16_RETAINED_HISTORY_BINDINGS.json"
_BOUNDARY_AUDIT_PATH = (
    "docs/research/RV01_R01_12_RETAINED_NAMESPACE_BOUNDARY_AUDIT_20260915.json"
)
_R01_15_IDENTITY_AUDIT_PATH = (
    "docs/research/RV01_R01_15_RAW_ARTIFACT_IDENTITY_AUDIT_20260914.json"
)

_EVIDENCE_BLOBS = {
    _BOUNDARY_AUDIT_PATH: "2fa75567a8a9048a8dc48c237545e5185c435db0",
    "src/sparkbrain/research/rv01/interference_contract.py": (
        "d1fd0aa35a5b33e6d2908d8208758c9d91f0ed81"
    ),
    "artifacts/research/rv01/r01_12d/development_result_manifest.json": (
        "4f8151b2d599a23bbb96ee536b6b7830df7ff928"
    ),
    "artifacts/research/rv01/r01_12f/formal_result_manifest.json": (
        "d8321e18561c3e1a2feeeea9ab94f6c54e0e926a"
    ),
    "artifacts/research/rv01/r01_12f/heldout_formal_result.json": (
        "46871db1c895f47a2913a2feeeea9ab94f6c54e0e926a"
    ),
    "src/sparkbrain/research/rv01/activity_matched_contract.py": (
        "27a640681da2e05337a771633e16f89af3bf7412"
    ),
    "artifacts/research/rv01/r01_13/development_result.json": (
        "3a8caf5f7d4d8826adb1c5cfdae4c2fca9062ea4"
    ),
    "src/sparkbrain/research/rv01/traversal_dynamics_contract.py": (
        "93e7ea99839e91d53a4a2a50ff80704313d68a9c"
    ),
    "artifacts/research/rv01/r01_14/development_result.json": (
        "2da5688525b4a18a1056a259e301e0d9651ae9da"
    ),
    "src/sparkbrain/research/rv01/post_spike_suppression_contract.py": (
        "551528b1b3d26bd8d94095f3a683c2fee144411a"
    ),
    "docs/research/RV01_R01_15_DEVELOPMENT_RESULT.md": (
        "bd158008359ae0b54cf67a817fcd12c099b0b8a4"
    ),
    _R01_15_IDENTITY_AUDIT_PATH: "1b961fa8f63cd512a0aa31ae0e29d0f7b8043cc1",
}


def _git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _family_values() -> tuple[str, ...]:
    return tuple(member.value for member in InterferenceFamily)


def _world_ids(
    *,
    prefix: str | None,
    development_seeds: tuple[int, ...],
    held_out_seeds: tuple[int, ...],
) -> tuple[str, ...]:
    values: list[str] = []
    for phase, seeds in (
        ("development", development_seeds),
        ("held-out", held_out_seeds),
    ):
        for family in _family_values():
            for seed in seeds:
                stem = f"{phase}:{family}:{seed}"
                values.append(stem if prefix is None else f"{prefix}:{stem}")
    return tuple(values)


def known_retained_namespace() -> tuple[tuple[int, ...], tuple[str, ...]]:
    """Return the exact repository-retained R01-12..R01-15 namespace."""

    seed_ids = tuple(
        sorted(
            {
                *DEVELOPMENT_SEEDS,
                *HELD_OUT_SEEDS,
                *R01_13_DEVELOPMENT_SEEDS,
                *R01_13_HELD_OUT_SEEDS,
                *R01_14_DEVELOPMENT_SEEDS,
                *R01_14_HELD_OUT_SEEDS,
                *R01_15_DEVELOPMENT_SEEDS,
                *R01_15_HELD_OUT_SEEDS,
            }
        )
    )
    world_ids = tuple(
        sorted(
            {
                *_world_ids(
                    prefix=None,
                    development_seeds=DEVELOPMENT_SEEDS,
                    held_out_seeds=HELD_OUT_SEEDS,
                ),
                *_world_ids(
                    prefix="r01-13",
                    development_seeds=R01_13_DEVELOPMENT_SEEDS,
                    held_out_seeds=R01_13_HELD_OUT_SEEDS,
                ),
                *_world_ids(
                    prefix="r01-14",
                    development_seeds=R01_14_DEVELOPMENT_SEEDS,
                    held_out_seeds=R01_14_HELD_OUT_SEEDS,
                ),
                *_world_ids(
                    prefix="r01-15",
                    development_seeds=R01_15_DEVELOPMENT_SEEDS,
                    held_out_seeds=R01_15_HELD_OUT_SEEDS,
                ),
            }
        )
    )
    return seed_ids, world_ids


def _collect_world_ids(value: Any) -> set[str]:
    values: set[str] = set()
    if isinstance(value, dict):
        world_id = value.get("world_id")
        if isinstance(world_id, str) and world_id:
            values.add(world_id)
        world_ids = value.get("world_ids")
        if isinstance(world_ids, list):
            values.update(
                item for item in world_ids if isinstance(item, str) and item
            )
        for child in value.values():
            values.update(_collect_world_ids(child))
    elif isinstance(value, list):
        for child in value:
            values.update(_collect_world_ids(child))
    return values


def _seed_from_world_id(world_id: str) -> int | None:
    try:
        return int(world_id.rsplit(":", 1)[1])
    except (IndexError, ValueError):
        return None


def _expected_phase_worlds(
    *,
    prefix: str | None,
    phase: str,
    seeds: tuple[int, ...],
) -> tuple[str, ...]:
    values = []
    for family in _family_values():
        for seed in seeds:
            stem = f"{phase}:{family}:{seed}"
            values.append(stem if prefix is None else f"{prefix}:{stem}")
    return tuple(sorted(values))


def _verify_world_rows(
    payload: Any,
    *,
    expected_world_ids: tuple[str, ...],
    expected_seeds: tuple[int, ...],
) -> bool:
    world_ids = tuple(sorted(_collect_world_ids(payload)))
    if not world_ids:
        return False
    derived_seeds = {
        seed
        for world_id in world_ids
        if (seed := _seed_from_world_id(world_id)) is not None
    }
    return world_ids == expected_world_ids and tuple(sorted(derived_seeds)) == tuple(
        sorted(expected_seeds)
    )


def _verify_retained_namespace_boundary(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise ValueError("R01 retained namespace boundary audit must be an object")
    if payload.get("schema") != "rv01-r01-12-retained-namespace-boundary-audit-v1":
        raise ValueError("unexpected R01 retained namespace boundary audit schema")
    if payload.get("status") != "VERIFIED_REPOSITORY_RETAINED_NAMESPACE_BOUNDARY":
        raise ValueError("R01 retained namespace boundary audit is not verified")
    if payload.get("audit_scope") != (
        "repository-retained seed/world execution identity history only"
    ):
        raise ValueError("R01 retained namespace boundary audit scope changed")

    boundary = payload.get("boundary")
    if not isinstance(boundary, dict):
        raise ValueError("R01 retained namespace boundary payload is missing")
    expected_boundary = {
        "first_contract_commit": "b68b920ee088db4547ac3fb7907d9c46f1b19837",
        "first_contract_path": "src/sparkbrain/research/rv01/interference_contract.py",
        "first_contract_blob_sha": "d1fd0aa35a5b33e6d2908d8208758c9d91f0ed81",
        "parent_commit": "4d4d0a6978e5cfaa1c9667c18b5fb2a59933d0e3",
        "parent_tree": "df45f991cb4a74448cefb9428c19c2c1e73541fe",
    }
    if boundary != expected_boundary:
        raise ValueError("R01 retained namespace boundary identity changed")

    checks = payload.get("parent_snapshot_checks")
    if checks != {
        "interference_contract_path_present": False,
        "artifacts_research_directory_present": False,
        "github_workflows": ["ci.yml"],
        "rv01_source_directory_present": True,
    }:
        raise ValueError("R01 retained namespace parent snapshot checks changed")

    interpretation = payload.get("interpretation")
    if not isinstance(interpretation, dict):
        raise ValueError("R01 retained namespace interpretation is missing")
    if interpretation.get("earlier_rv01_source_work_existed") is not True:
        raise ValueError("R01 boundary audit must retain earlier source-work history")
    if (
        interpretation.get(
            "earlier_repository_retained_seed_world_execution_namespace_is_claimed_absent"
        )
        is not True
    ):
        raise ValueError("pre-R01-12 retained namespace boundary is not discharged")
    if payload.get("execution_authority_granted") is not False:
        raise ValueError("R01 retained namespace audit cannot grant execution authority")
    if payload.get("scientific_result_modified") is not False:
        raise ValueError("R01 retained namespace audit cannot modify scientific results")


def _verify_r01_15_identity_audit(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise ValueError("R01-15 identity audit must be an object")
    if payload.get("schema") != "rv01-r01-15-raw-artifact-identity-audit-v1":
        raise ValueError("unexpected R01-15 identity audit schema")
    if payload.get("status") != "VERIFIED_IDENTITY_BOOKKEEPING_ONLY":
        raise ValueError("R01-15 identity audit is not verified bookkeeping")
    if payload.get("rerun_performed") is not False:
        raise ValueError("R01-15 identity audit indicates a rerun")
    if payload.get("scientific_result_modified") is not False:
        raise ValueError("R01-15 identity audit indicates scientific-result modification")

    artifact = payload.get("artifact")
    if not isinstance(artifact, dict):
        raise ValueError("R01-15 identity audit artifact binding is missing")
    expected_artifact = {
        "artifact_id": 10268643645,
        "artifact_name": "rv01-r01-15-development-34612398956",
        "artifact_zip_sha256": (
            "e349381d95fd47e09830e45723fa306419698fd226c8d87a1a7f3d7f77b9fe13"
        ),
        "freeze_ref": "freeze/rv01-r01-15-development-source",
        "frozen_source_git_sha": "a46096458446e3d101c5a951dba4efd7db1ee0ae",
        "raw_result_sha256": (
            "e849acbd2a9acc14d87fdec58be398b6c4b1e53ec6b33aa5a77ace43d56d1dac"
        ),
        "workflow_run_id": 34612398956,
    }
    if artifact != expected_artifact:
        raise ValueError("R01-15 raw artifact identity binding changed")

    observed = payload.get("observed_development")
    if not isinstance(observed, dict):
        raise ValueError("R01-15 observed development identity ledger is missing")
    observed_seeds = tuple(sorted(int(seed) for seed in observed.get("seed_ids", ())))
    if observed_seeds != tuple(sorted(R01_15_DEVELOPMENT_SEEDS)):
        raise ValueError("R01-15 observed development seeds do not match contract")
    expected_world_ids = _expected_phase_worlds(
        prefix="r01-15",
        phase="development",
        seeds=R01_15_DEVELOPMENT_SEEDS,
    )
    if not _verify_world_rows(
        observed,
        expected_world_ids=expected_world_ids,
        expected_seeds=R01_15_DEVELOPMENT_SEEDS,
    ):
        raise ValueError("R01-15 raw development world ledger is incomplete")

    held_out = payload.get("reserved_held_out")
    if not isinstance(held_out, dict):
        raise ValueError("R01-15 held-out reservation ledger is missing")
    if held_out.get("executed") is not False:
        raise ValueError("R01-15 held-out identity unexpectedly reports execution")
    held_out_seeds = tuple(sorted(int(seed) for seed in held_out.get("seed_ids", ())))
    if held_out_seeds != tuple(sorted(R01_15_HELD_OUT_SEEDS)):
        raise ValueError("R01-15 reserved held-out seeds do not match contract")


@dataclass(frozen=True, slots=True)
class RetainedHistorySnapshot:
    source_paths: tuple[str, ...]
    consumed_or_reserved_seed_ids: tuple[int, ...]
    consumed_or_reserved_world_ids: tuple[str, ...]
    verified_evidence_classes: tuple[str, ...]
    unresolved_evidence_classes: tuple[str, ...]

    @property
    def authoritative_complete(self) -> bool:
        return not self.unresolved_evidence_classes

    def state_dict(self) -> dict[str, object]:
        return {
            "schema": "rv01-r01-16-retained-history-snapshot-v1",
            "authority": "repository-retained-seed-history",
            "source_paths": list(self.source_paths),
            "consumed_or_reserved_seed_ids": list(
                self.consumed_or_reserved_seed_ids
            ),
            "consumed_or_reserved_world_ids": list(
                self.consumed_or_reserved_world_ids
            ),
            "verified_evidence_classes": list(self.verified_evidence_classes),
            "unresolved_evidence_classes": list(self.unresolved_evidence_classes),
            "authoritative_complete": self.authoritative_complete,
        }

    def to_collision_registry(self) -> R0116CollisionRegistry:
        if not self.authoritative_complete:
            raise ValueError(
                "R01-16 retained history remains incomplete; collision registry "
                "cannot be opened"
            )
        return R0116CollisionRegistry(
            registry_id="rv01-r01-16-retained-history-v1",
            source_paths=self.source_paths,
            consumed_or_reserved_seed_ids=self.consumed_or_reserved_seed_ids,
            consumed_or_reserved_world_ids=self.consumed_or_reserved_world_ids,
            authoritative_complete=True,
        )


def build_retained_history_snapshot(repo_root: Path) -> RetainedHistorySnapshot:
    """Verify retained bytes and reconstruct the authoritative collision namespace."""

    root = repo_root.resolve(strict=True)
    for relative, expected_blob in _EVIDENCE_BLOBS.items():
        path = root / relative
        if not path.is_file():
            raise ValueError(f"missing retained RV01 evidence: {relative}")
        actual_blob = _git_blob_sha(path.read_bytes())
        if actual_blob != expected_blob:
            raise ValueError(
                f"retained RV01 evidence bytes changed for {relative}: "
                f"expected {expected_blob}, got {actual_blob}"
            )

    _verify_retained_namespace_boundary(_load_json(root / _BOUNDARY_AUDIT_PATH))
    verified = ["pre-r01-12-repository-retained-identity-boundary"]
    unresolved: list[str] = []

    r01_12d = _load_json(
        root / "artifacts/research/rv01/r01_12d/development_result_manifest.json"
    )
    observed_r01_12d = tuple(
        sorted(str(row["world_id"]) for row in r01_12d["world_hashes"])
    )
    expected_r01_12d = _expected_phase_worlds(
        prefix=None,
        phase="development",
        seeds=DEVELOPMENT_SEEDS,
    )
    if observed_r01_12d != expected_r01_12d:
        raise ValueError("R01-12D retained world identities do not match its contract")
    verified.append("r01-12-development-contract-and-manifest")

    r01_12f = _load_json(
        root / "artifacts/research/rv01/r01_12f/heldout_formal_result.json"
    )
    if _verify_world_rows(
        r01_12f,
        expected_world_ids=_expected_phase_worlds(
            prefix=None,
            phase="held-out",
            seeds=HELD_OUT_SEEDS,
        ),
        expected_seeds=HELD_OUT_SEEDS,
    ):
        verified.append("r01-12-held-out-formal-world-ledger")
    else:
        unresolved.append(
            "r01-12-held-out-formal-world-ledger-not-explicitly-recovered"
        )

    r01_13 = _load_json(root / "artifacts/research/rv01/r01_13/development_result.json")
    if _verify_world_rows(
        r01_13,
        expected_world_ids=_expected_phase_worlds(
            prefix="r01-13",
            phase="development",
            seeds=R01_13_DEVELOPMENT_SEEDS,
        ),
        expected_seeds=R01_13_DEVELOPMENT_SEEDS,
    ):
        verified.append("r01-13-development-world-ledger")
    else:
        unresolved.append("r01-13-development-world-ledger-not-explicitly-recovered")

    r01_14 = _load_json(root / "artifacts/research/rv01/r01_14/development_result.json")
    if _verify_world_rows(
        r01_14,
        expected_world_ids=_expected_phase_worlds(
            prefix="r01-14",
            phase="development",
            seeds=R01_14_DEVELOPMENT_SEEDS,
        ),
        expected_seeds=R01_14_DEVELOPMENT_SEEDS,
    ):
        verified.append("r01-14-development-world-ledger")
    else:
        unresolved.append("r01-14-development-world-ledger-not-explicitly-recovered")

    _verify_r01_15_identity_audit(_load_json(root / _R01_15_IDENTITY_AUDIT_PATH))
    verified.extend(
        (
            "r01-15-frozen-contract-and-fixed-result-report",
            "r01-15-raw-development-world-identity-audit",
            "r01-15-reserved-held-out-identity-audit",
        )
    )

    seed_ids, world_ids = known_retained_namespace()
    return RetainedHistorySnapshot(
        source_paths=tuple(sorted((*_EVIDENCE_BLOBS, _BINDINGS_PATH))),
        consumed_or_reserved_seed_ids=seed_ids,
        consumed_or_reserved_world_ids=world_ids,
        verified_evidence_classes=tuple(sorted(verified)),
        unresolved_evidence_classes=tuple(sorted(set(unresolved))),
    )


__all__ = [
    "RetainedHistorySnapshot",
    "build_retained_history_snapshot",
    "known_retained_namespace",
]
