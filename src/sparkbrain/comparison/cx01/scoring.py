from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from .worlds import CX01Family


@dataclass(frozen=True, slots=True)
class FamilyEvidence:
    family: CX01Family
    correct_probes: int = 0
    total_probes: int = 0
    brier_score: float | None = None
    log_loss: float | None = None
    cycle_correct_fraction: float | None = None
    maximum_reacquisition_observations: int | None = None
    selective_effect: float | None = None
    self_confirmation_violations: int = 0

    def validate(self) -> None:
        if self.correct_probes < 0 or self.total_probes < 0:
            raise ValueError("probe counts must be non-negative")
        if self.correct_probes > self.total_probes:
            raise ValueError("correct probe count cannot exceed total")
        for value in (
            self.brier_score,
            self.log_loss,
            self.cycle_correct_fraction,
            self.selective_effect,
        ):
            if value is not None and not math.isfinite(value):
                raise ValueError("family evidence values must be finite")
        if self.cycle_correct_fraction is not None and not 0 <= self.cycle_correct_fraction <= 1:
            raise ValueError("cycle correct fraction must be in [0, 1]")
        if (
            self.maximum_reacquisition_observations is not None
            and self.maximum_reacquisition_observations < 0
        ):
            raise ValueError("reacquisition observations must be non-negative")
        if self.self_confirmation_violations < 0:
            raise ValueError("self-confirmation violations must be non-negative")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["family"] = self.family.value
        return value


@dataclass(frozen=True, slots=True)
class FamilyDecision:
    family: CX01Family
    passed: bool
    gates: tuple[tuple[str, bool], ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "family": self.family.value,
            "passed": self.passed,
            "gates": [{"name": name, "passed": passed} for name, passed in self.gates],
        }


def decide_family(evidence: FamilyEvidence) -> FamilyDecision:
    """Apply non-compensatory family gates.

    A strong result in one family can never compensate for failure in another.
    """

    evidence.validate()
    accuracy = evidence.correct_probes / max(1, evidence.total_probes)
    if evidence.family is CX01Family.HIGH_ORDER:
        gates = (("high-order-discrimination", evidence.total_probes > 0 and accuracy == 1.0),)
    elif evidence.family is CX01Family.TIMING:
        gates = (
            ("timing-conditioned-discrimination", evidence.total_probes > 0 and accuracy == 1.0),
        )
    elif evidence.family is CX01Family.CYCLE:
        gates = (
            (
                "cycle-correct-fraction",
                evidence.cycle_correct_fraction is not None
                and evidence.cycle_correct_fraction >= 0.80,
            ),
            (
                "bounded-reacquisition",
                evidence.maximum_reacquisition_observations is not None
                and evidence.maximum_reacquisition_observations <= 2,
            ),
        )
    elif evidence.family is CX01Family.BRANCH:
        gates = (
            ("branch-top1", evidence.total_probes > 0 and accuracy == 1.0),
            (
                "branch-brier",
                evidence.brier_score is not None and evidence.brier_score <= 0.10,
            ),
            (
                "branch-log-loss",
                evidence.log_loss is not None and evidence.log_loss <= 1.20,
            ),
        )
    elif evidence.family is CX01Family.SELECTIVITY:
        gates = (
            (
                "selective-effect",
                evidence.selective_effect is not None and evidence.selective_effect >= 0.50,
            ),
        )
    else:
        gates = (
            ("loop-output-valid", evidence.total_probes > 0 and accuracy == 1.0),
            ("no-self-confirmation", evidence.self_confirmation_violations == 0),
        )
    return FamilyDecision(evidence.family, all(passed for _, passed in gates), gates)


def brier_score(expected: dict[str, float], observed: dict[str, float]) -> float:
    """Compute the same Brier definition with a canonical token summation order."""

    tokens = sorted(set(expected).union(observed))
    return sum((observed.get(token, 0.0) - expected.get(token, 0.0)) ** 2 for token in tokens)


def cross_entropy(expected: dict[str, float], observed: dict[str, float]) -> float:
    """Compute cross entropy in canonical token order for byte-stable evidence."""

    floor = 1e-12
    return -sum(
        expected[token] * math.log(max(floor, observed.get(token, 0.0)))
        for token in sorted(expected)
        if expected[token] > 0
    )
