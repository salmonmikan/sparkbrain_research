from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)

QUALIFICATION_FAMILIES = (
    "identifier-permutation",
    "temporal-perturbation",
    "field-gain-perturbation",
)
QUALIFICATION_SEEDS = (0, 1, 2)


@dataclass(frozen=True, slots=True)
class ComparatorWorldParameters:
    family_id: str
    seed: int
    main_path: tuple[int, int, int, int]
    alternate_path: tuple[int, int, int, int]
    control_path: tuple[int, int, int, int]
    old_target: int
    new_target: int
    main_port: str
    control_port: str
    transition_lag_ms: float
    boundary_lag_ms: float
    threshold: float
    cue_magnitude: float
    relation_reentry_gain: float
    episode_spacing_ms: float
    unit_count: int = 13

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def world_parameters(family_id: str, seed: int) -> ComparatorWorldParameters:
    """Reproduce the frozen qualification world without importing Primary code."""

    if family_id not in QUALIFICATION_FAMILIES:
        raise ValueError(f"unknown qualification world family: {family_id}")
    if seed not in QUALIFICATION_SEEDS:
        raise ValueError(f"unsupported qualification seed: {seed}")
    rng_seed = int(_digest({"family_id": family_id, "seed": seed})[:16], 16)
    rng = random.Random(rng_seed)
    roles = list(range(13))
    rng.shuffle(roles)

    if family_id == "identifier-permutation":
        lag_ms = 5.0
        boundary_lag_ms = 10.0
        threshold = 0.5
        cue_magnitude = 1.0
        main_port = f"port:{100 + roles[0]}"
        control_port = f"port:{200 + roles[7]}"
    elif family_id == "temporal-perturbation":
        lag_ms = float(4 + seed)
        boundary_lag_ms = float(8 + seed * 2)
        threshold = 0.5
        cue_magnitude = 1.0
        main_port = "port:7"
        control_port = "port:9"
    else:
        lag_ms = 5.0
        boundary_lag_ms = 10.0
        threshold = (0.44, 0.50, 0.56)[seed]
        cue_magnitude = threshold + 0.44
        main_port = "port:7"
        control_port = "port:9"

    spacing = max(70.0, 6.0 * lag_ms + boundary_lag_ms + 20.0)
    return ComparatorWorldParameters(
        family_id=family_id,
        seed=seed,
        main_path=(roles[0], roles[1], roles[2], roles[3]),
        alternate_path=(roles[0], roles[4], roles[5], roles[6]),
        control_path=(roles[7], roles[8], roles[9], roles[10]),
        old_target=roles[11],
        new_target=roles[12],
        main_port=main_port,
        control_port=control_port,
        transition_lag_ms=lag_ms,
        boundary_lag_ms=boundary_lag_ms,
        threshold=threshold,
        cue_magnitude=cue_magnitude,
        relation_reentry_gain=threshold / 0.60,
        episode_spacing_ms=spacing,
    )


@dataclass(frozen=True, slots=True)
class ComparatorWorldEvidence:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    passed_domains: tuple[EvidenceDomain, ...]
    metrics: tuple[tuple[str, float], ...]

    @property
    def all_passed(self) -> bool:
        return frozenset(self.passed_domains) == frozenset(EvidenceDomain)

    def domain_passed(self, domain: EvidenceDomain) -> bool:
        return domain in self.passed_domains

    def records(self) -> tuple[ConfirmatoryResultRecord, ...]:
        return tuple(
            ConfirmatoryResultRecord(
                family_id=self.family_id,
                seed=self.seed,
                condition=self.condition,
                evidence_domain=domain,
                passed=self.domain_passed(domain),
                metrics=self.metrics,
            )
            for domain in EvidenceDomain
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "all_passed": self.all_passed,
            "condition": self.condition.value,
            "family_id": self.family_id,
            "metrics": dict(self.metrics),
            "passed_domains": [row.value for row in self.passed_domains],
            "seed": self.seed,
        }
