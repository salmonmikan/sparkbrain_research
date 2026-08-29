from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import ConditionResourceRecord


@dataclass(frozen=True, slots=True)
class HeldoutConditionExecution:
    """One condition's complete result/resource payload for one held-out world.

    ``semantic_hash`` deliberately excludes wall-clock time. It is suitable for
    deterministic replay checks without pretending that scheduler timing is a
    deterministic cognitive output.
    """

    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    world_specification_hash: str
    records: tuple[ConfirmatoryResultRecord, ...]
    resource: ConditionResourceRecord
    semantic_hash: str

    def validate(self) -> None:
        if len(self.records) != len(EvidenceDomain):
            raise ValueError("held-out execution must emit every evidence domain")
        if {row.evidence_domain for row in self.records} != set(EvidenceDomain):
            raise ValueError("held-out execution has incomplete evidence-domain coverage")
        if len({row.key for row in self.records}) != len(self.records):
            raise ValueError("held-out execution contains duplicate result keys")
        if any(
            row.family_id != self.family_id
            or row.seed != self.seed
            or row.condition is not self.condition
            for row in self.records
        ):
            raise ValueError("held-out execution result identity mismatch")
        if self.resource.key != (self.family_id, self.seed, self.condition):
            raise ValueError("held-out execution resource identity mismatch")
        self.resource.validate()
        if not self.world_specification_hash or len(self.semantic_hash) != 64:
            raise ValueError("held-out execution hashes must be present")

    @property
    def passed_domains(self) -> tuple[EvidenceDomain, ...]:
        return tuple(row.evidence_domain for row in self.records if row.passed)

    def state_dict(self) -> dict[str, Any]:
        return {
            "condition": self.condition.value,
            "family_id": self.family_id,
            "passed_domains": [row.value for row in self.passed_domains],
            "records": [row.state_dict() for row in self.records],
            "resource": self.resource.state_dict(),
            "seed": self.seed,
            "semantic_hash": self.semantic_hash,
            "world_specification_hash": self.world_specification_hash,
        }


@dataclass(frozen=True, slots=True)
class HeldoutPreflightReport:
    expected_execution_count: int
    observed_execution_count: int
    expected_result_count: int
    observed_result_count: int
    expected_resource_count: int
    observed_resource_count: int
    duplicate_execution_keys: tuple[str, ...]
    missing_execution_keys: tuple[str, ...]
    invalid_executions: tuple[str, ...]
    semantic_replay_mismatches: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_result_records(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
    passed: dict[EvidenceDomain, bool],
    metrics: dict[str, float],
) -> tuple[ConfirmatoryResultRecord, ...]:
    missing = set(EvidenceDomain) - set(passed)
    unexpected = set(passed) - set(EvidenceDomain)
    if missing or unexpected:
        raise ValueError(
            "held-out passed-domain mapping must cover exactly EvidenceDomain"
        )
    metric_rows = tuple(sorted((str(key), float(value)) for key, value in metrics.items()))
    return tuple(
        ConfirmatoryResultRecord(
            family_id=parameters.family_id,
            seed=parameters.seed,
            condition=condition,
            evidence_domain=domain,
            passed=bool(passed[domain]),
            metrics=metric_rows,
        )
        for domain in EvidenceDomain
    )


def execution_key_text(
    family_id: str,
    seed: int,
    condition: ConfirmatoryCondition,
) -> str:
    return f"{family_id}|{seed}|{condition.value}"
