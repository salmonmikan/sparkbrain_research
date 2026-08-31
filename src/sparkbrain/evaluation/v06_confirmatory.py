from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from typing import Any

from sparkbrain.v06.foundation import digest

_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class ConfirmatoryPhase(StrEnum):
    QUALIFICATION = "qualification"
    CONFIRMATORY = "confirmatory"


class ConfirmatoryCondition(StrEnum):
    PRIMARY = "primary"
    NO_ENDOGENOUS = "no-endogenous"
    RANDOM_MATCHED = "random-endogenous-matched"
    READOUT_ONLY = "readout-only"
    SHUFFLED_RELATION = "shuffled-relation"
    G3_RECURRENT = "g3-recurrent"
    G4_ASSEMBLY = "g4-assembly-conditioned"
    G5_TYPED = "g5-typed-functional-heads"


class EvidenceDomain(StrEnum):
    ENDOGENOUS_ORIGIN = "endogenous-origin"
    STATE_DEPENDENCE = "state-dependence"
    AUTONOMOUS_CHAIN = "autonomous-chain"
    BOUNDARY_EFFECT = "boundary-effect"
    RELATION_STABILIZATION = "relation-stabilization"
    REVERSAL_REACQUISITION = "reversal-reacquisition"
    RELATION_REENTRY = "relation-reentry"
    PERSISTENCE_LOCUS = "persistence-locus"
    TAXONOMY_NON_INTERFERENCE = "taxonomy-non-interference"


REQUIRED_CONDITIONS = tuple(ConfirmatoryCondition)
REQUIRED_EVIDENCE_DOMAINS = tuple(EvidenceDomain)


@dataclass(frozen=True, slots=True)
class WorldFamilySpec:
    family_id: str
    held_out: bool
    perturbation_axes: tuple[str, ...]
    description: str

    def validate(self) -> None:
        if not self.family_id or not self.description:
            raise ValueError("world family identifiers and descriptions must be non-empty")
        if not self.perturbation_axes:
            raise ValueError("each world family requires at least one perturbation axis")
        if len(set(self.perturbation_axes)) != len(self.perturbation_axes):
            raise ValueError("world perturbation axes must be unique")


@dataclass(frozen=True, slots=True)
class PerturbationSeedSpec:
    seed: int
    structural_token: str

    def validate(self) -> None:
        if self.seed < 0 or not self.structural_token:
            raise ValueError("seed and structural token must be valid")


@dataclass(frozen=True, slots=True)
class ConditionRegistration:
    condition: ConfirmatoryCondition
    adapter_path: str | None
    adapter_ready: bool
    isolated_from_primary: bool
    engineering_evidence_available: bool
    notes: str

    def validate(self) -> None:
        if self.adapter_ready and not self.adapter_path:
            raise ValueError(f"{self.condition.value} is ready without an adapter path")
        if not self.notes:
            raise ValueError("condition notes must be non-empty")
        if self.condition in {
            ConfirmatoryCondition.G3_RECURRENT,
            ConfirmatoryCondition.G4_ASSEMBLY,
            ConfirmatoryCondition.G5_TYPED,
        }:
            if self.adapter_path and not self.adapter_path.startswith("sparkbrain.baselines."):
                raise ValueError("G3/G4/G5 adapters must remain under sparkbrain.baselines")
            if self.adapter_ready and not self.isolated_from_primary:
                raise ValueError("a ready comparator must be isolated from the Primary path")


@dataclass(frozen=True, slots=True)
class ConfirmatoryThresholds:
    minimum_overall_success_fraction: float = 0.80
    minimum_each_family_success_fraction: float = 0.70
    maximum_null_false_positive_fraction: float = 0.10
    minimum_selective_effect: float = 0.50
    required_taxonomy_hash_match_fraction: float = 1.0
    maximum_self_confirmation_violations: int = 0

    def validate(self) -> None:
        for name in (
            "minimum_overall_success_fraction",
            "minimum_each_family_success_fraction",
            "maximum_null_false_positive_fraction",
            "minimum_selective_effect",
            "required_taxonomy_hash_match_fraction",
        ):
            value = float(getattr(self, name))
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.maximum_self_confirmation_violations != 0:
            raise ValueError("v0.6 confirmatory runs require zero self-confirmation violations")


@dataclass(frozen=True, slots=True)
class ConfirmatoryManifest:
    protocol_version: str
    phase: ConfirmatoryPhase
    code_ref: str
    world_families: tuple[WorldFamilySpec, ...]
    seeds: tuple[PerturbationSeedSpec, ...]
    conditions: tuple[ConditionRegistration, ...]
    evidence_domains: tuple[EvidenceDomain, ...]
    thresholds: ConfirmatoryThresholds
    exclusions: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "code_ref": self.code_ref,
            "conditions": [
                {
                    **asdict(row),
                    "condition": row.condition.value,
                }
                for row in self.conditions
            ],
            "evidence_domains": [row.value for row in self.evidence_domains],
            "exclusions": list(self.exclusions),
            "phase": self.phase.value,
            "protocol_version": self.protocol_version,
            "seeds": [asdict(row) for row in self.seeds],
            "thresholds": asdict(self.thresholds),
            "world_families": [asdict(row) for row in self.world_families],
        }

    def manifest_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ConfirmatoryReadinessReport:
    phase: ConfirmatoryPhase
    manifest_hash: str
    code_ref_frozen: bool
    family_count: int
    required_family_count: int
    seed_count: int
    required_seed_count: int
    missing_conditions: tuple[str, ...]
    unavailable_adapters: tuple[str, ...]
    isolation_violations: tuple[str, ...]
    missing_evidence_domains: tuple[str, ...]
    shape_errors: tuple[str, ...]
    ready: bool

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["phase"] = self.phase.value
        return value


@dataclass(frozen=True, slots=True)
class ConfirmatoryResultRecord:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    evidence_domain: EvidenceDomain
    passed: bool
    metrics: tuple[tuple[str, float], ...] = ()

    @property
    def key(self) -> tuple[str, int, ConfirmatoryCondition, EvidenceDomain]:
        return (
            self.family_id,
            self.seed,
            self.condition,
            self.evidence_domain,
        )


@dataclass(frozen=True, slots=True)
class ConfirmatoryCoverageReport:
    expected_record_count: int
    observed_record_count: int
    duplicate_keys: tuple[str, ...]
    missing_keys: tuple[str, ...]
    unexpected_keys: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ConfirmatoryOutcome:
    primary_overall_success_fraction: float
    primary_minimum_family_success_fraction: float
    primary_supported: bool
    supported_comparators: tuple[str, ...]
    comparator_only_success: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _condition_registrations() -> tuple[ConditionRegistration, ...]:
    return (
        ConditionRegistration(
            ConfirmatoryCondition.PRIMARY,
            "sparkbrain.evaluation.v06_confirmatory_primary.run_condition",
            False,
            True,
            True,
            "Canonical engineering probes exist; parameterized world-family adapter is pending.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.NO_ENDOGENOUS,
            "sparkbrain.evaluation.v06_confirmatory_controls.run_no_endogenous",
            False,
            True,
            True,
            "Engineering no-generation controls exist; unified confirmatory adapter is pending.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.RANDOM_MATCHED,
            "sparkbrain.evaluation.v06_confirmatory_controls.run_random_matched",
            False,
            True,
            False,
            "Count/energy/time-matched random endogenous control is not yet implemented.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.READOUT_ONLY,
            "sparkbrain.evaluation.v06_confirmatory_controls.run_readout_only",
            False,
            True,
            True,
            "Readout-only engineering controls exist; unified adapter is pending.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.SHUFFLED_RELATION,
            "sparkbrain.evaluation.v06_confirmatory_controls.run_shuffled_relation",
            False,
            True,
            False,
            "Shuffled anonymous relation-state control is not yet implemented.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.G3_RECURRENT,
            "sparkbrain.baselines.v06.g3_recurrent.run_condition",
            False,
            True,
            False,
            "Generic recurrent comparator adapter is not yet implemented.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.G4_ASSEMBLY,
            "sparkbrain.baselines.v06.g4_assembly.run_condition",
            False,
            True,
            False,
            "Explicit Assembly-conditioned comparator adapter is not yet implemented.",
        ),
        ConditionRegistration(
            ConfirmatoryCondition.G5_TYPED,
            "sparkbrain.baselines.v06.g5_typed.run_condition",
            False,
            True,
            False,
            "Typed functional-head comparator adapter is not yet implemented.",
        ),
    )


def build_draft_confirmatory_manifest(
    phase: ConfirmatoryPhase,
    *,
    code_ref: str = "UNFROZEN",
) -> ConfirmatoryManifest:
    if phase is ConfirmatoryPhase.QUALIFICATION:
        families = (
            WorldFamilySpec(
                "identifier-permutation",
                False,
                ("unit-permutation", "port-permutation"),
                "Permute anonymous unit and outbound-port identities.",
            ),
            WorldFamilySpec(
                "temporal-perturbation",
                False,
                ("lag-jitter", "episode-spacing"),
                "Vary local lags and inter-episode timing within frozen bounds.",
            ),
            WorldFamilySpec(
                "field-gain-perturbation",
                False,
                ("threshold-offset", "magnitude-scale"),
                "Vary ordinary Field threshold and current scale within frozen bounds.",
            ),
        )
        seeds = tuple(
            PerturbationSeedSpec(seed, f"qualification-{seed}")
            for seed in range(3)
        )
    else:
        families = (
            WorldFamilySpec(
                "heldout-sparse-permutation",
                True,
                ("sparse-unit-permutation", "port-permutation"),
                "Held-out sparse anonymous topology and identity permutation.",
            ),
            WorldFamilySpec(
                "heldout-lag-dispersion",
                True,
                ("lag-dispersion", "episode-spacing"),
                "Held-out timing dispersion and nonuniform episode spacing.",
            ),
            WorldFamilySpec(
                "heldout-threshold-band",
                True,
                ("threshold-band", "magnitude-scale"),
                "Held-out ordinary threshold and magnitude regime.",
            ),
            WorldFamilySpec(
                "heldout-branch-competition",
                True,
                ("branch-count", "branch-confidence"),
                "Held-out competing anonymous alternatives.",
            ),
            WorldFamilySpec(
                "heldout-contingency-cycles",
                True,
                ("reversal-cycle", "raw-target-permutation"),
                "Held-out external contingency reversal and reacquisition cycles.",
            ),
        )
        seeds = tuple(
            PerturbationSeedSpec(seed, f"confirmatory-{seed}")
            for seed in range(100, 110)
        )
    return ConfirmatoryManifest(
        protocol_version="v06-amendment-003-draft-1",
        phase=phase,
        code_ref=code_ref,
        world_families=families,
        seeds=seeds,
        conditions=_condition_registrations(),
        evidence_domains=REQUIRED_EVIDENCE_DOMAINS,
        thresholds=ConfirmatoryThresholds(),
        exclusions=(
            "No semantic labels, scalar reward, or correct-action target in Primary runtime.",
            "No evaluator-selected winning anonymous relation.",
            "No post-freeze threshold, family, seed, or exclusion edits.",
            "Comparator-only success is not reinterpreted as Primary success.",
        ),
    )


def assess_confirmatory_readiness(
    manifest: ConfirmatoryManifest,
) -> ConfirmatoryReadinessReport:
    shape_errors: list[str] = []
    try:
        manifest.thresholds.validate()
    except ValueError as exc:
        shape_errors.append(str(exc))
    for row in manifest.world_families:
        try:
            row.validate()
        except ValueError as exc:
            shape_errors.append(f"world:{row.family_id}:{exc}")
    for row in manifest.seeds:
        try:
            row.validate()
        except ValueError as exc:
            shape_errors.append(f"seed:{row.seed}:{exc}")
    for row in manifest.conditions:
        try:
            row.validate()
        except ValueError as exc:
            shape_errors.append(f"condition:{row.condition.value}:{exc}")

    family_ids = [row.family_id for row in manifest.world_families]
    seed_values = [row.seed for row in manifest.seeds]
    condition_values = [row.condition for row in manifest.conditions]
    evidence_values = list(manifest.evidence_domains)
    if len(set(family_ids)) != len(family_ids):
        shape_errors.append("duplicate world family IDs")
    if len(set(seed_values)) != len(seed_values):
        shape_errors.append("duplicate perturbation seeds")
    if len(set(condition_values)) != len(condition_values):
        shape_errors.append("duplicate condition registrations")
    if len(set(evidence_values)) != len(evidence_values):
        shape_errors.append("duplicate evidence domains")

    required_family_count = 3 if manifest.phase is ConfirmatoryPhase.QUALIFICATION else 5
    required_seed_count = 3 if manifest.phase is ConfirmatoryPhase.QUALIFICATION else 10
    if manifest.phase is ConfirmatoryPhase.CONFIRMATORY and any(
        not row.held_out for row in manifest.world_families
    ):
        shape_errors.append("confirmatory world families must all be held out")

    registered = set(condition_values)
    missing_conditions = tuple(
        row.value for row in REQUIRED_CONDITIONS if row not in registered
    )
    unavailable = tuple(
        row.condition.value for row in manifest.conditions if not row.adapter_ready
    )
    isolation = tuple(
        row.condition.value
        for row in manifest.conditions
        if row.condition
        in {
            ConfirmatoryCondition.G3_RECURRENT,
            ConfirmatoryCondition.G4_ASSEMBLY,
            ConfirmatoryCondition.G5_TYPED,
        }
        and not row.isolated_from_primary
    )
    missing_domains = tuple(
        row.value for row in REQUIRED_EVIDENCE_DOMAINS if row not in evidence_values
    )
    code_ref_frozen = bool(_SHA_PATTERN.fullmatch(manifest.code_ref))
    ready = (
        code_ref_frozen
        and len(manifest.world_families) >= required_family_count
        and len(manifest.seeds) >= required_seed_count
        and not missing_conditions
        and not unavailable
        and not isolation
        and not missing_domains
        and not shape_errors
    )
    return ConfirmatoryReadinessReport(
        phase=manifest.phase,
        manifest_hash=manifest.manifest_hash(),
        code_ref_frozen=code_ref_frozen,
        family_count=len(manifest.world_families),
        required_family_count=required_family_count,
        seed_count=len(manifest.seeds),
        required_seed_count=required_seed_count,
        missing_conditions=missing_conditions,
        unavailable_adapters=unavailable,
        isolation_violations=isolation,
        missing_evidence_domains=missing_domains,
        shape_errors=tuple(shape_errors),
        ready=ready,
    )


def with_all_adapters_ready(
    manifest: ConfirmatoryManifest,
) -> ConfirmatoryManifest:
    """Test helper for validating a complete frozen manifest shape."""

    return replace(
        manifest,
        conditions=tuple(
            replace(row, adapter_ready=True, isolated_from_primary=True)
            for row in manifest.conditions
        ),
    )


def _format_key(
    key: tuple[str, int, ConfirmatoryCondition, EvidenceDomain],
) -> str:
    return f"{key[0]}|{key[1]}|{key[2].value}|{key[3].value}"


def assess_result_coverage(
    manifest: ConfirmatoryManifest,
    records: Iterable[ConfirmatoryResultRecord],
) -> ConfirmatoryCoverageReport:
    expected = {
        (family.family_id, seed.seed, condition.condition, evidence)
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
        for evidence in manifest.evidence_domains
    }
    rows = tuple(records)
    counts = Counter(row.key for row in rows)
    observed = set(counts)
    duplicates = tuple(
        sorted(_format_key(key) for key, count in counts.items() if count > 1)
    )
    missing = tuple(sorted(_format_key(key) for key in expected - observed))
    unexpected = tuple(sorted(_format_key(key) for key in observed - expected))
    return ConfirmatoryCoverageReport(
        expected_record_count=len(expected),
        observed_record_count=len(rows),
        duplicate_keys=duplicates,
        missing_keys=missing,
        unexpected_keys=unexpected,
        complete=not duplicates and not missing and not unexpected,
    )


def _success_fraction(rows: Iterable[ConfirmatoryResultRecord]) -> float:
    values = tuple(rows)
    if not values:
        return 0.0
    return sum(row.passed for row in values) / len(values)


def score_confirmatory_results(
    manifest: ConfirmatoryManifest,
    records: Iterable[ConfirmatoryResultRecord],
) -> ConfirmatoryOutcome:
    readiness = assess_confirmatory_readiness(manifest)
    if not readiness.ready:
        raise RuntimeError("confirmatory manifest is not execution-ready")
    rows = tuple(records)
    coverage = assess_result_coverage(manifest, rows)
    if not coverage.complete:
        raise RuntimeError("confirmatory result matrix is incomplete")

    primary_rows = tuple(
        row for row in rows if row.condition is ConfirmatoryCondition.PRIMARY
    )
    overall = _success_fraction(primary_rows)
    family_fractions = tuple(
        _success_fraction(row for row in primary_rows if row.family_id == family.family_id)
        for family in manifest.world_families
    )
    minimum_family = min(family_fractions, default=0.0)
    primary_supported = (
        overall >= manifest.thresholds.minimum_overall_success_fraction
        and minimum_family
        >= manifest.thresholds.minimum_each_family_success_fraction
    )

    supported_comparators: list[str] = []
    for condition in (
        ConfirmatoryCondition.G3_RECURRENT,
        ConfirmatoryCondition.G4_ASSEMBLY,
        ConfirmatoryCondition.G5_TYPED,
    ):
        condition_rows = tuple(row for row in rows if row.condition is condition)
        condition_overall = _success_fraction(condition_rows)
        condition_families = tuple(
            _success_fraction(
                row for row in condition_rows if row.family_id == family.family_id
            )
            for family in manifest.world_families
        )
        if (
            condition_overall >= manifest.thresholds.minimum_overall_success_fraction
            and min(condition_families, default=0.0)
            >= manifest.thresholds.minimum_each_family_success_fraction
        ):
            supported_comparators.append(condition.value)

    comparator_only = not primary_supported and bool(supported_comparators)
    if primary_supported and supported_comparators:
        interpretation = "primary-and-comparator-supported; uniqueness not established"
    elif primary_supported:
        interpretation = "primary-supported under frozen thresholds"
    elif comparator_only:
        interpretation = "comparator-only success; negative for Primary hypothesis"
    else:
        interpretation = "neither Primary nor required comparator supported"
    return ConfirmatoryOutcome(
        primary_overall_success_fraction=overall,
        primary_minimum_family_success_fraction=minimum_family,
        primary_supported=primary_supported,
        supported_comparators=tuple(supported_comparators),
        comparator_only_success=comparator_only,
        interpretation=interpretation,
    )


def frozen_manifest_copy(
    manifest: ConfirmatoryManifest,
    *,
    code_ref: str,
) -> ConfirmatoryManifest:
    if not _SHA_PATTERN.fullmatch(code_ref):
        raise ValueError("code_ref must be a full lowercase 40-character Git SHA")
    return replace(manifest, code_ref=code_ref)


def manifest_summary(manifest: ConfirmatoryManifest) -> Mapping[str, Any]:
    readiness = assess_confirmatory_readiness(manifest)
    return {
        "manifest_hash": readiness.manifest_hash,
        "phase": readiness.phase.value,
        "ready": readiness.ready,
        "world_family_count": readiness.family_count,
        "seed_count": readiness.seed_count,
        "unavailable_adapters": list(readiness.unavailable_adapters),
    }
