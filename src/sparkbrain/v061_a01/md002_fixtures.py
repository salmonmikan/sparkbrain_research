"""Prospective reset/restore fixtures for A01 MD-002; no capability execution.

The P2 correction requires both arms to start from byte-identical local (L),
Field (F), consistency (C), and transient return-address (R) state while only
an anonymous external world relation changes.  This module freezes the raw
serialized partition bytes once and produces both arm inputs from that single
checkpoint.  It deliberately contains no A01 runner and applies no evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .md002_protocol import (
    StatePartitionSnapshot,
    WorldOnlyInterventionPair,
    bytes_sha256,
)

ArmName = Literal["control", "intervention"]


def _require_bytes(value: bytes, name: str, *, allow_empty: bool = False) -> None:
    if type(value) is not bytes:
        raise TypeError(f"{name} must be immutable bytes")
    if not allow_empty and not value:
        raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True, slots=True)
class FrozenPartitionBytes:
    """One exact serialized L/F/C/R checkpoint used by both P2 arms."""

    local: bytes
    field: bytes
    consistency: bytes
    return_address: bytes | None

    def validate(self) -> None:
        _require_bytes(self.local, "local")
        _require_bytes(self.field, "field")
        _require_bytes(self.consistency, "consistency")
        if self.return_address is not None:
            _require_bytes(self.return_address, "return_address", allow_empty=True)

    def snapshot(self) -> StatePartitionSnapshot:
        self.validate()
        value = StatePartitionSnapshot(
            local_sha256=bytes_sha256(self.local),
            field_sha256=bytes_sha256(self.field),
            consistency_sha256=bytes_sha256(self.consistency),
            return_address_sha256=(
                None
                if self.return_address is None
                else bytes_sha256(self.return_address)
            ),
        )
        value.validate()
        return value

    def restored_copy(self) -> FrozenPartitionBytes:
        """Return a fresh immutable checkpoint value with identical bytes."""

        self.validate()
        # bytes(value) is intentionally explicit: callers never receive a
        # mutable object or an arm-specific checkpoint source.
        return FrozenPartitionBytes(
            local=bytes(self.local),
            field=bytes(self.field),
            consistency=bytes(self.consistency),
            return_address=(
                None if self.return_address is None else bytes(self.return_address)
            ),
        )


@dataclass(frozen=True, slots=True)
class P2WorldArmInput:
    """One pre-evidence arm input restored from the common checkpoint."""

    arm: ArmName
    partitions: FrozenPartitionBytes
    world_relation: bytes
    admissible_external_evidence: bytes

    def validate(self) -> None:
        if self.arm not in ("control", "intervention"):
            raise ValueError("invalid P2 arm")
        self.partitions.validate()
        _require_bytes(self.world_relation, "world_relation")
        _require_bytes(
            self.admissible_external_evidence,
            "admissible_external_evidence",
        )

    @property
    def world_relation_sha256(self) -> str:
        self.validate()
        return bytes_sha256(self.world_relation)

    @property
    def admissible_external_evidence_sha256(self) -> str:
        self.validate()
        return bytes_sha256(self.admissible_external_evidence)


@dataclass(frozen=True, slots=True)
class P2WorldOnlyFixture:
    """Freeze one local checkpoint and vary only anonymous world-relation bytes."""

    checkpoint: FrozenPartitionBytes
    control_world_relation: bytes
    intervention_world_relation: bytes
    admissible_external_evidence: bytes

    def validate(self) -> None:
        self.checkpoint.validate()
        _require_bytes(self.control_world_relation, "control_world_relation")
        _require_bytes(
            self.intervention_world_relation,
            "intervention_world_relation",
        )
        _require_bytes(
            self.admissible_external_evidence,
            "admissible_external_evidence",
        )
        if bytes_sha256(self.control_world_relation) == bytes_sha256(
            self.intervention_world_relation
        ):
            raise ValueError("P2 fixture requires a genuinely changed world relation")

    def arm(self, name: ArmName) -> P2WorldArmInput:
        self.validate()
        if name == "control":
            relation = self.control_world_relation
        elif name == "intervention":
            relation = self.intervention_world_relation
        else:
            raise ValueError("invalid P2 arm")
        value = P2WorldArmInput(
            arm=name,
            partitions=self.checkpoint.restored_copy(),
            world_relation=bytes(relation),
            admissible_external_evidence=bytes(self.admissible_external_evidence),
        )
        value.validate()
        return value

    def prospective_contract(self) -> WorldOnlyInterventionPair:
        """Bind the reset fixture to the already fail-closed MD-002 P2 contract."""

        control = self.arm("control")
        intervention = self.arm("intervention")
        if control.partitions != intervention.partitions:
            raise RuntimeError("P2 reset/restore did not reproduce the common checkpoint")
        if (
            control.admissible_external_evidence
            != intervention.admissible_external_evidence
        ):
            raise RuntimeError("P2 arms do not carry byte-identical external evidence")
        pair = WorldOnlyInterventionPair(
            control=control.partitions.snapshot(),
            intervention=intervention.partitions.snapshot(),
            control_world_relation_sha256=control.world_relation_sha256,
            intervention_world_relation_sha256=intervention.world_relation_sha256,
            admissible_external_evidence_sha256=(
                control.admissible_external_evidence_sha256
            ),
        )
        pair.validate()
        return pair


__all__ = [
    "FrozenPartitionBytes",
    "P2WorldArmInput",
    "P2WorldOnlyFixture",
]
