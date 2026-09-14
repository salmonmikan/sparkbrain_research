"""Fail-closed retained-history reconstruction for prospective RV01 R01-16.

This module reconstructs only identity material that is explicitly bound by
retained repository evidence. It deliberately keeps the resulting snapshot
non-authoritative while any evidence class remains unresolved.
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

_EVIDENCE_BLOBS = {
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
        "46871db1c895f47a2913a2a0eb59f92ecc4e7a23"
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
}

_PRE_R01_12_UNRESOLVED = "pre-r01-12-retained-identity-history-not-yet-enumerated"
_R01_15_RAW_UNRESOLVED = (
    "r01-15-raw-development-world-ledger-not-retained-in-repository"
)


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
    """Return the exact currently reconstructed R01-12..R01-15 namespace."""

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


def _find_world_rows(value: Any) -> tuple[dict[str, Any], ...]:
    if isinstance(value, dict):
        worlds = value.get("worlds")
        if isinstance(worlds, list) and worlds:
            rows = tuple(row for row in worlds if isinstance(row, dict))
            if len(rows) == len(worlds) and all(
                "world_id" in row and "seed" in row for row in rows
            ):
                return rows
        for child in value.values():
            rows = _find_world_rows(child)
            if rows:
                return rows
    elif isinstance(value, list):
        for child in value:
            rows = _find_world_rows(child)
            if rows:
                return rows
    return ()


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
    rows = _find_world_rows(payload)
    if not rows:
        return False
    world_ids = tuple(sorted({str(row["world_id"]) for row in rows}))
    seeds = tuple(sorted({int(row["seed"]) for row in rows}))
    return world_ids == expected_world_ids and seeds == tuple(sorted(expected_seeds))


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
    """Verify retained bytes and reconstruct the known collision namespace."""

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

    verified = ["r01-12-development-contract-and-manifest"]

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

    unresolved = [_PRE_R01_12_UNRESOLVED]

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

    verified.append("r01-15-frozen-contract-and-fixed-result-report")
    unresolved.append(_R01_15_RAW_UNRESOLVED)

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
