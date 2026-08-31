from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from .contract import ComparatorKind
from .worlds import (
    CX01Family,
    DEVELOPMENT_GENERATION_ID,
    DEVELOPMENT_SEEDS,
    HISTORICALLY_EXPOSED_SEEDS,
    CX01World,
    build_world,
)


CX01_COMPARATOR_INVENTORY = (
    ComparatorKind.G3_FIRST_ORDER,
    ComparatorKind.G4_ASSEMBLY,
    ComparatorKind.G5_TYPED,
    ComparatorKind.G6_VARIABLE_ORDER,
    ComparatorKind.G7_HTM_TEMPORAL_MEMORY,
    ComparatorKind.G8_PREDICTION,
    ComparatorKind.G8_REPLAY,
)


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class CandidateSpec:
    generation_id: str
    seeds: tuple[int, ...]
    protocol_version: str = "cx01-comparator-protocol-1"

    def validate(self) -> None:
        if not self.generation_id or self.generation_id == DEVELOPMENT_GENERATION_ID:
            raise ValueError("formal candidate requires a fresh non-development generation")
        if not self.generation_id.startswith("cx01-candidate-"):
            raise ValueError("candidate generation id must use cx01-candidate-* namespace")
        if len(self.seeds) < 10 or len(set(self.seeds)) != len(self.seeds):
            raise ValueError("formal candidate requires at least ten unique seeds")
        forbidden = set(DEVELOPMENT_SEEDS).union(HISTORICALLY_EXPOSED_SEEDS)
        if forbidden.intersection(self.seeds):
            raise ValueError("candidate seeds overlap exposed/development evidence")
        if any(seed < 0 for seed in self.seeds):
            raise ValueError("candidate seeds must be non-negative")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "generation_id": self.generation_id,
            "protocol_version": self.protocol_version,
            "seeds": list(self.seeds),
        }

    def specification_hash(self) -> str:
        return _digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class CandidateDeclaration:
    generation_id: str
    family: CX01Family
    seed: int
    kind: ComparatorKind
    world_hash: str
    status: str = "unscored"
    capability_result_present: bool = False
    measurements_present: bool = False

    def validate(self) -> None:
        if self.status != "unscored":
            raise ValueError("candidate declaration cannot contain a score")
        if self.capability_result_present or self.measurements_present:
            raise ValueError("candidate declaration must remain outcome-blind")
        if len(self.world_hash) != 64:
            raise ValueError("candidate declaration requires a SHA-256 world hash")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["family"] = self.family.value
        value["kind"] = self.kind.value
        return value


def build_candidate_grid(spec: CandidateSpec) -> tuple[CX01World, ...]:
    spec.validate()
    return tuple(
        build_world(spec.generation_id, family, seed)
        for family in CX01Family
        for seed in spec.seeds
    )


def candidate_grid_hash(spec: CandidateSpec) -> str:
    return _digest(
        {
            "candidate": spec.state_dict(),
            "worlds": [world.state_dict() for world in build_candidate_grid(spec)],
        }
    )


def build_outcome_blind_declarations(
    spec: CandidateSpec,
) -> tuple[CandidateDeclaration, ...]:
    declarations = tuple(
        CandidateDeclaration(
            generation_id=spec.generation_id,
            family=world.family,
            seed=world.seed,
            kind=kind,
            world_hash=world.specification_hash(),
        )
        for world in build_candidate_grid(spec)
        for kind in CX01_COMPARATOR_INVENTORY
    )
    for row in declarations:
        row.validate()
    return declarations


def declaration_bundle_hash(spec: CandidateSpec) -> str:
    return _digest(
        [row.state_dict() for row in build_outcome_blind_declarations(spec)]
    )
