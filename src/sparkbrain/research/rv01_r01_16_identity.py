"""Execution-disabled identity binding for prospective RV01 R01-16 development.

This module binds only a fresh exposed-development namespace. It does not build a
Field, train a learner, run a probe, inspect a capability result, create a
held-out/formal candidate, or grant execution authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass

R01_16_PROTOCOL_ID = "rv01-r01-16-propagation-factorization-v1"
R01_16_FAMILIES = (
    "disjoint-routes",
    "shared-cue-branches",
    "shared-prefix-branches",
    "edge-reversal",
    "dense-route-load",
)
R01_16_DEVELOPMENT_SEEDS = (141700, 141701, 141702, 141703, 141704)
R01_16_WORLD_SALT = "rv01-r01-16-fresh-world-grid-v1"
R01_16_UNIT_COUNT = 96
R01_16_FORMAL_AUTHORITY = False
R01_16_HELD_OUT_AUTHORITY = False

# Immediate predecessor namespaces are permanently excluded from R01-16
# development. A future capability-enabling layer must additionally supply the
# complete retained consumed/reserved registry to assert_no_seed_collisions().
R01_15_DEVELOPMENT_SEEDS = frozenset(range(141500, 141505))
R01_15_RESERVED_HELD_OUT_SEEDS = frozenset(range(141600, 141610))
R01_16_FIXED_EXCLUSIONS = R01_15_DEVELOPMENT_SEEDS | R01_15_RESERVED_HELD_OUT_SEEDS


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _is_exact_int(value: object) -> bool:
    return type(value) is int


@dataclass(frozen=True, slots=True)
class R0116DevelopmentIdentity:
    """One prospectively named development world before world construction."""

    family: str
    seed: int
    unit_count: int = R01_16_UNIT_COUNT

    def validate(self) -> None:
        if self.family not in R01_16_FAMILIES:
            raise ValueError("R01-16 family is not part of the fixed registered family set")
        if not _is_exact_int(self.seed):
            raise TypeError("R01-16 seed must be an exact non-boolean int")
        if not _is_exact_int(self.unit_count):
            raise TypeError("R01-16 unit_count must be an exact non-boolean int")
        if self.seed not in R01_16_DEVELOPMENT_SEEDS:
            raise ValueError("R01-16 seed is outside the fixed development namespace")
        if self.seed in R01_16_FIXED_EXCLUSIONS:
            raise ValueError("R01-16 development seed collides with the R01-15 namespace")
        if self.unit_count != R01_16_UNIT_COUNT:
            raise ValueError("R01-16 fixes development worlds at 96 anonymous units")

    @property
    def world_id(self) -> str:
        self.validate()
        return f"r01-16:development:{self.family}:{self.seed}"

    @property
    def identity_sha256(self) -> str:
        self.validate()
        return _digest(
            {
                "family": self.family,
                "phase": "development",
                "protocol_id": R01_16_PROTOCOL_ID,
                "salt": R01_16_WORLD_SALT,
                "seed": self.seed,
                "unit_count": self.unit_count,
            }
        )

    def state_dict(self) -> dict[str, object]:
        return {
            "family": self.family,
            "formal_authority": R01_16_FORMAL_AUTHORITY,
            "held_out_authority": R01_16_HELD_OUT_AUTHORITY,
            "identity_sha256": self.identity_sha256,
            "phase": "development",
            "protocol_id": R01_16_PROTOCOL_ID,
            "seed": self.seed,
            "unit_count": self.unit_count,
            "world_id": self.world_id,
            "world_salt": R01_16_WORLD_SALT,
        }


def development_identity_grid() -> tuple[R0116DevelopmentIdentity, ...]:
    """Return the complete ordered fixed-family x fixed-seed development grid."""

    rows = tuple(
        R0116DevelopmentIdentity(family=family, seed=seed)
        for family in R01_16_FAMILIES
        for seed in R01_16_DEVELOPMENT_SEEDS
    )
    for row in rows:
        row.validate()
    if len(rows) != len(R01_16_FAMILIES) * len(R01_16_DEVELOPMENT_SEEDS):
        raise RuntimeError("R01-16 development identity grid cardinality drifted")
    if len({row.world_id for row in rows}) != len(rows):
        raise RuntimeError("R01-16 development world IDs are not unique")
    if len({row.identity_sha256 for row in rows}) != len(rows):
        raise RuntimeError("R01-16 development identity hashes are not unique")
    return rows


def assert_no_seed_collisions(consumed_or_reserved: Iterable[int]) -> None:
    """Fail closed if the fixed development seeds collide with any retained registry.

    The caller must pass the complete consumed/reserved seed registry before a
    future capability layer may use this namespace. The function deliberately
    does not infer that registry from mutable repository text.
    """

    registry = set(consumed_or_reserved)
    if any(not _is_exact_int(seed) for seed in registry):
        raise TypeError("retained seed registry must contain exact non-boolean ints")
    collisions = sorted(set(R01_16_DEVELOPMENT_SEEDS).intersection(registry))
    if collisions:
        raise ValueError(f"R01-16 development seed collision(s): {collisions}")


__all__ = [
    "R01_16_DEVELOPMENT_SEEDS",
    "R01_16_FAMILIES",
    "R01_16_FIXED_EXCLUSIONS",
    "R01_16_FORMAL_AUTHORITY",
    "R01_16_HELD_OUT_AUTHORITY",
    "R01_16_PROTOCOL_ID",
    "R01_16_UNIT_COUNT",
    "R01_16_WORLD_SALT",
    "R0116DevelopmentIdentity",
    "assert_no_seed_collisions",
    "development_identity_grid",
]
