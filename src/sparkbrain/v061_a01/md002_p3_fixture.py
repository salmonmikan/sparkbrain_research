"""Execution-disabled return-address transplant fixture for A01 MD-002 P3.

This module prepares the three P3 pre-attribution arms from actual serialized
A01 L/F/C/R checkpoints.  It does not apply evidence, score capability, or open
the MD-002 execution gate.

The scientific isolation is fail-closed:
- baseline and donor must have byte-identical local/Field/consistency state;
- both must carry explicitly observed, genuinely different return-address state;
- the transplanted arm is constructed from baseline L/F/C plus donor R only;
- all three arms carry byte-identical admissible external evidence;
- restore validation delegates to the existing state restore adapter, which
  reconstructs actual runtime objects and verifies byte-identical round trips.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .md002_fixtures import FrozenPartitionBytes, P2WorldArmInput
from .md002_protocol import StatePartitionSnapshot, bytes_sha256
from .md002_restore_adapter import RestoredA01P2Arm, restore_a01_p2_arm
from .md002_state_binding import canonical_bytes

P3ArmName = Literal["baseline", "donor", "transplanted"]


@dataclass(frozen=True, slots=True)
class P3ArmInput:
    """One P3 pre-attribution arm; capability remains unopened."""

    arm: P3ArmName
    partitions: FrozenPartitionBytes
    admissible_external_evidence: bytes

    def validate(self) -> None:
        if self.arm not in ("baseline", "donor", "transplanted"):
            raise ValueError("invalid P3 arm")
        self.partitions.validate()
        if self.partitions.return_address is None:
            raise ValueError("P3 requires explicitly observed return-address state")
        if type(self.admissible_external_evidence) is not bytes:
            raise TypeError("P3 admissible external evidence must be immutable bytes")
        if not self.admissible_external_evidence:
            raise ValueError("P3 requires non-empty admissible external evidence")

    def snapshot(self) -> StatePartitionSnapshot:
        self.validate()
        return self.partitions.snapshot()

    @property
    def admissible_external_evidence_sha256(self) -> str:
        self.validate()
        return bytes_sha256(self.admissible_external_evidence)


@dataclass(frozen=True, slots=True)
class P3ReturnAddressFixture:
    """Prospective three-arm R-only transplant construction."""

    baseline: FrozenPartitionBytes
    donor: FrozenPartitionBytes
    admissible_external_evidence: bytes

    def validate(self) -> None:
        self.baseline.validate()
        self.donor.validate()
        if self.baseline.return_address is None or self.donor.return_address is None:
            raise ValueError("P3 baseline and donor require observed R state")
        for name in ("local", "field", "consistency"):
            if getattr(self.baseline, name) != getattr(self.donor, name):
                raise ValueError(f"P3 donor drifted from baseline in {name}")
        if self.baseline.return_address == self.donor.return_address:
            raise ValueError("P3 donor R must differ from baseline R")
        if type(self.admissible_external_evidence) is not bytes:
            raise TypeError("P3 admissible external evidence must be immutable bytes")
        if not self.admissible_external_evidence:
            raise ValueError("P3 requires non-empty admissible external evidence")

    def arm(self, name: P3ArmName) -> P3ArmInput:
        self.validate()
        if name == "baseline":
            partitions = self.baseline.restored_copy()
        elif name == "donor":
            partitions = self.donor.restored_copy()
        elif name == "transplanted":
            partitions = FrozenPartitionBytes(
                local=bytes(self.baseline.local),
                field=bytes(self.baseline.field),
                consistency=bytes(self.baseline.consistency),
                return_address=bytes(self.donor.return_address),
            )
        else:
            raise ValueError("invalid P3 arm")
        value = P3ArmInput(
            arm=name,
            partitions=partitions,
            admissible_external_evidence=bytes(self.admissible_external_evidence),
        )
        value.validate()
        return value

    def validate_isolation(self) -> None:
        """Prove the prospective transplant differs only in R."""

        baseline = self.arm("baseline")
        donor = self.arm("donor")
        transplanted = self.arm("transplanted")
        if transplanted.partitions.local != baseline.partitions.local:
            raise RuntimeError("P3 transplanted arm changed local state")
        if transplanted.partitions.field != baseline.partitions.field:
            raise RuntimeError("P3 transplanted arm changed Field state")
        if transplanted.partitions.consistency != baseline.partitions.consistency:
            raise RuntimeError("P3 transplanted arm changed consistency state")
        if transplanted.partitions.return_address != donor.partitions.return_address:
            raise RuntimeError("P3 transplanted arm did not receive donor R")
        evidence = {
            baseline.admissible_external_evidence_sha256,
            donor.admissible_external_evidence_sha256,
            transplanted.admissible_external_evidence_sha256,
        }
        if len(evidence) != 1:
            raise RuntimeError("P3 arms do not carry byte-identical external evidence")


def restore_p3_arm(arm_input: P3ArmInput) -> RestoredA01P2Arm:
    """Reconstruct actual L/F/C/R state and verify byte-identical round trip.

    The P2 restore adapter is intentionally reused only as a state serializer /
    deserializer verifier.  The synthetic world relation is an inert marker and
    no evidence or world action is executed here.
    """

    arm_input.validate()
    probe = P2WorldArmInput(
        arm="control",
        partitions=arm_input.partitions.restored_copy(),
        world_relation=canonical_bytes(
            {"mode": "p3-state-round-trip-only", "p3_arm": arm_input.arm}
        ),
        admissible_external_evidence=bytes(arm_input.admissible_external_evidence),
    )
    restored = restore_a01_p2_arm(probe)
    # restore_a01_p2_arm already proves exact L/F/C/R and evidence round-trip.
    return restored


__all__ = [
    "P3ArmInput",
    "P3ArmName",
    "P3ReturnAddressFixture",
    "restore_p3_arm",
]
