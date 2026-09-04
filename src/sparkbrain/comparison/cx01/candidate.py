from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .contract import ComparatorKind
from .worlds import (
    DEVELOPMENT_GENERATION_ID,
    HISTORICALLY_EXPOSED_SEEDS,
    CX01Family,
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

# The complete CX01 development/test band is permanently non-formal. This
# deliberately covers development worlds, unit-test worlds, manual diagnostics,
# and structure-fixture worlds so no already-exposed seed can later return as
# held-out evidence.
CX01_NONFORMAL_SEEDS = frozenset(range(3000, 6000))

# Reserved subset for schema/freeze/control-plane fixtures.
STRUCTURE_FIXTURE_SEEDS = frozenset(range(5000, 5200))


class CandidatePurpose(StrEnum):
    FORMAL = "formal"
    STRUCTURE_FIXTURE = "structure-fixture"


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
    purpose: CandidatePurpose = CandidatePurpose.FORMAL
    protocol_version: str = "cx01-comparator-protocol-1"

    def validate(self) -> None:
        if not self.generation_id or self.generation_id == DEVELOPMENT_GENERATION_ID:
            raise ValueError("candidate requires a fresh non-development generation")
        if len(self.seeds) < 10 or len(set(self.seeds)) != len(self.seeds):
            raise ValueError("candidate requires at least ten unique seeds")
        if any(seed < 0 for seed in self.seeds):
            raise ValueError("candidate seeds must be non-negative")

        if set(HISTORICALLY_EXPOSED_SEEDS).intersection(self.seeds):
            raise ValueError("candidate seeds overlap historical confirmatory evidence")

        if self.purpose is CandidatePurpose.FORMAL:
            if not self.generation_id.startswith("cx01-candidate-"):
                raise ValueError("formal generation id must use cx01-candidate-* namespace")
            if CX01_NONFORMAL_SEEDS.intersection(self.seeds):
                raise ValueError("formal candidate cannot reuse CX01 development/test seed band")
        elif self.purpose is CandidatePurpose.STRUCTURE_FIXTURE:
            if not self.generation_id.startswith("cx01-fixture-"):
                raise ValueError("fixture generation id must use cx01-fixture-* namespace")
            if not set(self.seeds).issubset(STRUCTURE_FIXTURE_SEEDS):
                raise ValueError("structure fixture must stay inside reserved fixture seed band")
        else:
            raise ValueError(f"unsupported candidate purpose: {self.purpose}")

    def require_formal(self) -> None:
        self.validate()
        if self.purpose is not CandidatePurpose.FORMAL:
            raise RuntimeError("structure fixture cannot enter formal capability execution")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "generation_id": self.generation_id,
            "protocol_version": self.protocol_version,
            "purpose": self.purpose.value,
            "seeds": list(self.seeds),
        }

    def specification_hash(self) -> str:
        return _digest(self.state_dict())

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> CandidateSpec:
        spec = cls(
            generation_id=str(state["generation_id"]),
            seeds=tuple(int(seed) for seed in state["seeds"]),
            purpose=CandidatePurpose(str(state.get("purpose", CandidatePurpose.FORMAL.value))),
            protocol_version=str(state.get("protocol_version", "cx01-comparator-protocol-1")),
        )
        spec.validate()
        return spec


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
    return _digest([row.state_dict() for row in build_outcome_blind_declarations(spec)])
