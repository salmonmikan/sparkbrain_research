from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition, ConfirmatoryManifest


class PrivilegedInformation(StrEnum):
    EXPLICIT_ASSEMBLY_STATE = "explicit-assembly-state"
    TYPED_PREDICTION_HEAD = "typed-prediction-head"
    TYPED_BOUNDARY_HEAD = "typed-boundary-head"
    TYPED_MEMORY_HEAD = "typed-memory-head"
    SCALAR_REWARD = "scalar-reward"


@dataclass(frozen=True, slots=True)
class ConditionResourceRecord:
    """One condition's execution/resource inventory for one world and seed.

    The record is evaluator metadata. It is never passed into the Primary
    runtime or used to select an internal event.
    """

    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    observed_training_events: int
    generated_internal_events: int
    persistent_state_entries: int
    intervention_count: int
    parameter_count: int
    wall_clock_ms: float
    normal_field_threshold_present: bool
    normal_field_threshold_crossings: int
    threshold_bypassed: bool
    explicit_assembly_entries: int
    typed_head_count: int
    scalar_reward_observations: int
    privileged_information: tuple[PrivilegedInformation, ...] = ()

    @property
    def key(self) -> tuple[str, int, ConfirmatoryCondition]:
        return (self.family_id, self.seed, self.condition)

    def validate(self) -> None:
        if not self.family_id or self.seed < 0:
            raise ValueError("resource record identity must be valid")
        integer_fields = (
            "observed_training_events",
            "generated_internal_events",
            "persistent_state_entries",
            "intervention_count",
            "parameter_count",
            "normal_field_threshold_crossings",
            "explicit_assembly_entries",
            "typed_head_count",
            "scalar_reward_observations",
        )
        if any(getattr(self, name) < 0 for name in integer_fields):
            raise ValueError("resource counts must be non-negative")
        if not math.isfinite(float(self.wall_clock_ms)) or self.wall_clock_ms < 0:
            raise ValueError("wall_clock_ms must be finite and non-negative")
        if len(set(self.privileged_information)) != len(
            self.privileged_information
        ):
            raise ValueError("privileged information entries must be unique")
        if (
            self.normal_field_threshold_crossings > 0
            and not self.normal_field_threshold_present
        ):
            raise ValueError("threshold crossings require an ordinary Field threshold")
        if self.normal_field_threshold_present and self.threshold_bypassed:
            raise ValueError("a condition cannot both use and bypass the Field threshold")
        self._validate_condition_contract()

    def _validate_condition_contract(self) -> None:
        if self.condition in {
            ConfirmatoryCondition.PRIMARY,
            ConfirmatoryCondition.NO_ENDOGENOUS,
            ConfirmatoryCondition.RANDOM_MATCHED,
            ConfirmatoryCondition.READOUT_ONLY,
            ConfirmatoryCondition.SHUFFLED_RELATION,
        }:
            if self.explicit_assembly_entries != 0:
                raise ValueError("Primary/control conditions cannot use Assembly state")
            if self.typed_head_count != 0 or self.scalar_reward_observations != 0:
                raise ValueError("Primary/control conditions cannot use typed heads or reward")
            if self.privileged_information:
                raise ValueError("Primary/control conditions cannot receive privileged information")
        elif self.condition is ConfirmatoryCondition.G3_RECURRENT:
            if self.explicit_assembly_entries != 0 or self.typed_head_count != 0:
                raise ValueError("G3 must remain generic and untyped")
            if self.scalar_reward_observations != 0 or self.privileged_information:
                raise ValueError("G3 cannot receive Assembly or typed/reward privilege")
            if self.normal_field_threshold_present:
                raise ValueError("G3 is an external predictor, not a Field runtime")
            if not self.threshold_bypassed:
                raise ValueError("G3 must explicitly report Field-threshold bypass")
        elif self.condition is ConfirmatoryCondition.G4_ASSEMBLY:
            expected = {PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE}
            if self.explicit_assembly_entries < 1:
                raise ValueError("G4 must report explicit Assembly state")
            if self.typed_head_count != 0 or self.scalar_reward_observations != 0:
                raise ValueError("G4 cannot hide typed-head or reward privilege")
            if set(self.privileged_information) != expected:
                raise ValueError("G4 privilege inventory must identify Assembly state")
            if self.normal_field_threshold_present:
                raise ValueError("G4 comparator does not use the Primary Field threshold")
            if not self.threshold_bypassed:
                raise ValueError("G4 must explicitly report Field-threshold bypass")
        elif self.condition is ConfirmatoryCondition.G5_TYPED:
            required = {
                PrivilegedInformation.TYPED_PREDICTION_HEAD,
                PrivilegedInformation.TYPED_BOUNDARY_HEAD,
                PrivilegedInformation.TYPED_MEMORY_HEAD,
                PrivilegedInformation.SCALAR_REWARD,
            }
            if self.typed_head_count < 3:
                raise ValueError("G5 must report its typed functional heads")
            if self.scalar_reward_observations < 1:
                raise ValueError("G5 must report privileged scalar reward observations")
            if set(self.privileged_information) != required:
                raise ValueError("G5 privilege inventory is incomplete")
            if self.normal_field_threshold_present:
                raise ValueError("G5 comparator does not use the Primary Field threshold")
            if not self.threshold_bypassed:
                raise ValueError("G5 must explicitly report Field-threshold bypass")
        else:
            raise ValueError(f"unsupported condition: {self.condition.value}")

    def metric_dict(self) -> dict[str, float]:
        self.validate()
        return {
            "resource_explicit_assembly_entries": float(
                self.explicit_assembly_entries
            ),
            "resource_generated_internal_events": float(
                self.generated_internal_events
            ),
            "resource_intervention_count": float(self.intervention_count),
            "resource_normal_field_threshold_crossings": float(
                self.normal_field_threshold_crossings
            ),
            "resource_normal_field_threshold_present": float(
                self.normal_field_threshold_present
            ),
            "resource_observed_training_events": float(
                self.observed_training_events
            ),
            "resource_parameter_count": float(self.parameter_count),
            "resource_persistent_state_entries": float(
                self.persistent_state_entries
            ),
            "resource_privileged_information_count": float(
                len(self.privileged_information)
            ),
            "resource_scalar_reward_observations": float(
                self.scalar_reward_observations
            ),
            "resource_threshold_bypassed": float(self.threshold_bypassed),
            "resource_typed_head_count": float(self.typed_head_count),
            "resource_wall_clock_ms": float(self.wall_clock_ms),
        }

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["condition"] = self.condition.value
        value["privileged_information"] = [
            row.value for row in self.privileged_information
        ]
        return value


@dataclass(frozen=True, slots=True)
class ResourceMatrixCoverage:
    expected_record_count: int
    observed_record_count: int
    duplicate_keys: tuple[str, ...]
    missing_keys: tuple[str, ...]
    unexpected_keys: tuple[str, ...]
    invalid_records: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _key_text(key: tuple[str, int, ConfirmatoryCondition]) -> str:
    return f"{key[0]}|{key[1]}|{key[2].value}"


def assess_resource_matrix(
    manifest: ConfirmatoryManifest,
    records: tuple[ConditionResourceRecord, ...],
) -> ResourceMatrixCoverage:
    expected = {
        (family.family_id, seed.seed, condition.condition)
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
    }
    observed = [row.key for row in records]
    counts = Counter(observed)
    duplicates = tuple(
        sorted(_key_text(key) for key, count in counts.items() if count > 1)
    )
    observed_set = set(observed)
    missing = tuple(sorted(_key_text(key) for key in expected - observed_set))
    unexpected = tuple(sorted(_key_text(key) for key in observed_set - expected))
    invalid: list[str] = []
    for row in records:
        try:
            row.validate()
        except ValueError as exc:
            invalid.append(f"{_key_text(row.key)}:{exc}")
    return ResourceMatrixCoverage(
        expected_record_count=len(expected),
        observed_record_count=len(records),
        duplicate_keys=duplicates,
        missing_keys=missing,
        unexpected_keys=unexpected,
        invalid_records=tuple(sorted(invalid)),
        complete=(
            len(records) == len(expected)
            and not duplicates
            and not missing
            and not unexpected
            and not invalid
        ),
    )
