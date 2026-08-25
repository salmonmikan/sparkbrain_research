from __future__ import annotations

from dataclasses import dataclass

from .contracts import OrganAssessment, OrganEvidence


@dataclass(frozen=True, slots=True)
class OrganGateConfig:
    minimum_seed_consistency: int = 3
    minimum_structural_cohesion: float = 0.55
    minimum_functional_selectivity: float = 0.20
    minimum_held_out_reuse: float = 0.20
    minimum_targeted_impairment: float = 0.05
    minimum_excess_impairment: float = 0.03
    maximum_unrelated_collateral: float = 0.02

    def validate(self) -> None:
        if self.minimum_seed_consistency < 1:
            raise ValueError("minimum_seed_consistency must be positive")
        for name in (
            "minimum_structural_cohesion",
            "minimum_functional_selectivity",
            "minimum_held_out_reuse",
            "minimum_targeted_impairment",
            "minimum_excess_impairment",
            "maximum_unrelated_collateral",
        ):
            value = getattr(self, name)
            if value < 0.0:
                raise ValueError(f"{name} must be non-negative")


def assess_organ_candidate(
    evidence: OrganEvidence,
    config: OrganGateConfig | None = None,
) -> OrganAssessment:
    """Reject graph clusters that lack functional and causal evidence."""

    active = config or OrganGateConfig()
    active.validate()
    checks = {
        "seed_consistency": evidence.seed_consistency >= active.minimum_seed_consistency,
        "structural_cohesion": evidence.structural_cohesion >= active.minimum_structural_cohesion,
        "functional_selectivity": (
            evidence.functional_selectivity >= active.minimum_functional_selectivity
        ),
        "held_out_reuse": evidence.held_out_reuse >= active.minimum_held_out_reuse,
        "causal_necessity": (
            evidence.targeted_impairment >= active.minimum_targeted_impairment
            and evidence.targeted_impairment - evidence.matched_random_impairment
            >= active.minimum_excess_impairment
        ),
        "bounded_collateral": (
            evidence.unrelated_collateral <= active.maximum_unrelated_collateral
        ),
    }
    passed = tuple(name for name, passed in checks.items() if passed)
    failed = tuple(name for name, passed in checks.items() if not passed)
    return OrganAssessment(
        accepted=not failed,
        passed_gates=passed,
        failed_gates=failed,
        reason=(
            "functional_organ_supported"
            if not failed
            else "organ_claim_rejected:" + ",".join(failed)
        ),
    )
