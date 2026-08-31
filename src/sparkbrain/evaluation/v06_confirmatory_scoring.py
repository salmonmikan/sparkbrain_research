from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryResultRecord,
    EvidenceDomain,
    assess_confirmatory_readiness,
    assess_result_coverage,
)

_NULL_CONDITIONS = frozenset(
    {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
    }
)
_CONTROL_CONDITIONS = frozenset(
    {
        *_NULL_CONDITIONS,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }
)
_COMPARATOR_CONDITIONS = (
    ConfirmatoryCondition.G3_RECURRENT,
    ConfirmatoryCondition.G4_ASSEMBLY,
    ConfirmatoryCondition.G5_TYPED,
)
_PRIMARY_SAFETY_CONDITIONS = frozenset(
    {
        ConfirmatoryCondition.PRIMARY,
        *_CONTROL_CONDITIONS,
    }
)
_CAPABILITY_DOMAINS = tuple(
    row
    for row in EvidenceDomain
    if row is not EvidenceDomain.TAXONOMY_NON_INTERFERENCE
)
_SHUFFLED_SENSITIVE_DOMAINS = frozenset(
    {
        EvidenceDomain.RELATION_REENTRY,
        EvidenceDomain.PERSISTENCE_LOCUS,
    }
)

_GROUP_KEY = tuple[str, int, ConfirmatoryCondition]


@dataclass(frozen=True, slots=True)
class StrictMetricCoverageReport:
    group_count: int
    missing_metric_keys: tuple[str, ...]
    inconsistent_metric_groups: tuple[str, ...]
    nonfinite_metric_keys: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StrictConfirmatoryOutcome:
    primary_overall_success_fraction: float
    primary_minimum_family_success_fraction: float
    primary_raw_supported: bool
    null_false_positive_fraction: float
    minimum_selective_effect: float
    taxonomy_hash_match_fraction: float
    self_confirmation_violations: int
    control_contract_fraction: float
    control_and_safety_gates_passed: bool
    primary_supported: bool
    supported_comparators: tuple[str, ...]
    comparator_only_success: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _group_label(key: _GROUP_KEY) -> str:
    family_id, seed, condition = key
    return f"{family_id}|{seed}|{condition.value}"


def _required_metrics(condition: ConfirmatoryCondition) -> frozenset[str]:
    common = {"self_confirmation_violations", "taxonomy_hash_match"}
    if condition is ConfirmatoryCondition.PRIMARY:
        return frozenset(
            {
                *common,
                "boundary_matched_impairment",
                "boundary_targeted_impairment",
                "chain_matched_impairment",
                "chain_targeted_impairment",
            }
        )
    if condition in _CONTROL_CONDITIONS:
        return frozenset({*common, "control_contract_passed"})
    if condition in _COMPARATOR_CONDITIONS:
        return frozenset(common)
    raise ValueError(f"unsupported confirmatory condition: {condition.value}")


def _group_metrics(
    records: tuple[ConfirmatoryResultRecord, ...],
) -> tuple[dict[_GROUP_KEY, dict[str, float]], tuple[str, ...]]:
    grouped: dict[_GROUP_KEY, tuple[tuple[str, float], ...]] = {}
    inconsistent: list[str] = []
    for record in records:
        key = (record.family_id, record.seed, record.condition)
        metrics = tuple(sorted(record.metrics))
        existing = grouped.get(key)
        if existing is None:
            grouped[key] = metrics
        elif metrics != existing:
            inconsistent.append(_group_label(key))
    return (
        {key: dict(metrics) for key, metrics in grouped.items()},
        tuple(sorted(set(inconsistent))),
    )


def assess_strict_metric_coverage(
    manifest: ConfirmatoryManifest,
    records: tuple[ConfirmatoryResultRecord, ...],
) -> StrictMetricCoverageReport:
    expected_groups = {
        (family.family_id, seed.seed, condition.condition)
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
    }
    metrics_by_group, inconsistent = _group_metrics(records)
    missing: list[str] = []
    nonfinite: list[str] = []
    for key in sorted(expected_groups, key=lambda row: (row[0], row[1], row[2].value)):
        metrics = metrics_by_group.get(key, {})
        for metric_name in sorted(_required_metrics(key[2])):
            metric_key = f"{_group_label(key)}|{metric_name}"
            if metric_name not in metrics:
                missing.append(metric_key)
                continue
            value = metrics[metric_name]
            if not math.isfinite(float(value)):
                nonfinite.append(metric_key)
    return StrictMetricCoverageReport(
        group_count=len(metrics_by_group),
        missing_metric_keys=tuple(missing),
        inconsistent_metric_groups=inconsistent,
        nonfinite_metric_keys=tuple(nonfinite),
        complete=(
            set(metrics_by_group) == expected_groups
            and not missing
            and not inconsistent
            and not nonfinite
        ),
    )


def _condition_success(
    records: tuple[ConfirmatoryResultRecord, ...],
    condition: ConfirmatoryCondition,
) -> tuple[float, float]:
    rows = tuple(record for record in records if record.condition is condition)
    overall = sum(row.passed for row in rows) / len(rows)
    by_family: defaultdict[str, list[ConfirmatoryResultRecord]] = defaultdict(list)
    for row in rows:
        by_family[row.family_id].append(row)
    family_values = tuple(
        sum(row.passed for row in family_rows) / len(family_rows)
        for _, family_rows in sorted(by_family.items())
    )
    return overall, min(family_values)


def _null_false_positive_fraction(
    records: tuple[ConfirmatoryResultRecord, ...],
) -> float:
    rows = tuple(
        record
        for record in records
        if (
            record.condition in _NULL_CONDITIONS
            and record.evidence_domain in _CAPABILITY_DOMAINS
        )
        or (
            record.condition is ConfirmatoryCondition.SHUFFLED_RELATION
            and record.evidence_domain in _SHUFFLED_SENSITIVE_DOMAINS
        )
    )
    if not rows:
        raise RuntimeError("strict confirmatory scoring found no null-control cells")
    return sum(row.passed for row in rows) / len(rows)


def _minimum_selective_effect(
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
) -> float:
    effects: list[float] = []
    for key, metrics in metrics_by_group.items():
        if key[2] is not ConfirmatoryCondition.PRIMARY:
            continue
        effects.extend(
            (
                metrics["chain_targeted_impairment"]
                - metrics["chain_matched_impairment"],
                metrics["boundary_targeted_impairment"]
                - metrics["boundary_matched_impairment"],
            )
        )
    if not effects:
        raise RuntimeError("strict confirmatory scoring found no Primary selective effects")
    return min(effects)


def _condition_metrics(
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
    conditions: frozenset[ConfirmatoryCondition],
) -> dict[_GROUP_KEY, dict[str, float]]:
    return {
        key: metrics
        for key, metrics in metrics_by_group.items()
        if key[2] in conditions
    }


def _metric_fraction(
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
    metric_name: str,
) -> float:
    values = [metrics[metric_name] for metrics in metrics_by_group.values()]
    if not values:
        raise RuntimeError(f"strict confirmatory scoring found no {metric_name} values")
    return sum(values) / len(values)


def _self_confirmation_violations(
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
) -> int:
    total = sum(
        metrics["self_confirmation_violations"]
        for metrics in metrics_by_group.values()
    )
    if not float(total).is_integer():
        raise RuntimeError("self-confirmation violation count must be integral")
    return int(total)


def _control_contract_fraction(
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
) -> float:
    values = [
        metrics["control_contract_passed"]
        for key, metrics in metrics_by_group.items()
        if key[2] in _CONTROL_CONDITIONS
    ]
    if not values:
        raise RuntimeError("strict confirmatory scoring found no control contracts")
    return sum(values) / len(values)


def _comparator_supported(
    records: tuple[ConfirmatoryResultRecord, ...],
    metrics_by_group: dict[_GROUP_KEY, dict[str, float]],
    manifest: ConfirmatoryManifest,
    condition: ConfirmatoryCondition,
) -> bool:
    overall, minimum_family = _condition_success(records, condition)
    condition_metrics = {
        key: metrics
        for key, metrics in metrics_by_group.items()
        if key[2] is condition
    }
    taxonomy = _metric_fraction(condition_metrics, "taxonomy_hash_match")
    violations = _self_confirmation_violations(condition_metrics)
    return (
        overall >= manifest.thresholds.minimum_overall_success_fraction
        and minimum_family
        >= manifest.thresholds.minimum_each_family_success_fraction
        and taxonomy
        >= manifest.thresholds.required_taxonomy_hash_match_fraction
        and violations
        <= manifest.thresholds.maximum_self_confirmation_violations
    )


def score_strict_confirmatory_results(
    manifest: ConfirmatoryManifest,
    records: tuple[ConfirmatoryResultRecord, ...],
) -> StrictConfirmatoryOutcome:
    """Score only a complete, frozen, metric-complete confirmatory matrix.

    Primary support is gated by the Primary and its four null/control
    conditions. Comparator taxonomy or self-confirmation failures invalidate
    that comparator only; an isolated comparator cannot veto otherwise clean
    Primary evidence.
    """

    readiness = assess_confirmatory_readiness(manifest)
    if not readiness.ready:
        raise RuntimeError("confirmatory manifest is not execution-ready")
    coverage = assess_result_coverage(manifest, records)
    if not coverage.complete:
        raise RuntimeError("confirmatory result matrix is incomplete")
    metric_coverage = assess_strict_metric_coverage(manifest, records)
    if not metric_coverage.complete:
        raise RuntimeError("confirmatory metric contract is incomplete")

    metrics_by_group, _ = _group_metrics(records)
    primary_overall, primary_minimum_family = _condition_success(
        records,
        ConfirmatoryCondition.PRIMARY,
    )
    primary_raw_supported = (
        primary_overall
        >= manifest.thresholds.minimum_overall_success_fraction
        and primary_minimum_family
        >= manifest.thresholds.minimum_each_family_success_fraction
    )
    null_fraction = _null_false_positive_fraction(records)
    minimum_selective_effect = _minimum_selective_effect(metrics_by_group)
    primary_safety_metrics = _condition_metrics(
        metrics_by_group,
        _PRIMARY_SAFETY_CONDITIONS,
    )
    taxonomy_fraction = _metric_fraction(
        primary_safety_metrics,
        "taxonomy_hash_match",
    )
    violations = _self_confirmation_violations(primary_safety_metrics)
    control_fraction = _control_contract_fraction(metrics_by_group)
    control_and_safety_gates_passed = (
        null_fraction
        <= manifest.thresholds.maximum_null_false_positive_fraction
        and minimum_selective_effect
        >= manifest.thresholds.minimum_selective_effect
        and taxonomy_fraction
        >= manifest.thresholds.required_taxonomy_hash_match_fraction
        and violations
        <= manifest.thresholds.maximum_self_confirmation_violations
        and math.isclose(control_fraction, 1.0, rel_tol=0.0, abs_tol=1e-12)
    )
    primary_supported = primary_raw_supported and control_and_safety_gates_passed

    supported_comparators = tuple(
        condition.value
        for condition in _COMPARATOR_CONDITIONS
        if _comparator_supported(records, metrics_by_group, manifest, condition)
    )
    comparator_only = bool(supported_comparators) and not primary_supported

    if primary_supported and not supported_comparators:
        interpretation = "Primary supported under the frozen scope; tested comparators unsupported."
    elif primary_supported and supported_comparators:
        interpretation = (
            "Primary and at least one comparator are supported; architectural uniqueness is not "
            "established."
        )
    elif comparator_only:
        interpretation = (
            "Comparator-only success is negative for the Primary SparkBrain hypothesis under the "
            "frozen scope."
        )
    elif primary_raw_supported and not control_and_safety_gates_passed:
        interpretation = (
            "Primary raw success is rejected because at least one null, selectivity, "
            "Primary/control taxonomy, Primary/control self-confirmation, or control-contract "
            "gate failed."
        )
    else:
        interpretation = "The tested capability is unsupported under the frozen scope."

    return StrictConfirmatoryOutcome(
        primary_overall_success_fraction=primary_overall,
        primary_minimum_family_success_fraction=primary_minimum_family,
        primary_raw_supported=primary_raw_supported,
        null_false_positive_fraction=null_fraction,
        minimum_selective_effect=minimum_selective_effect,
        taxonomy_hash_match_fraction=taxonomy_fraction,
        self_confirmation_violations=violations,
        control_contract_fraction=control_fraction,
        control_and_safety_gates_passed=control_and_safety_gates_passed,
        primary_supported=primary_supported,
        supported_comparators=supported_comparators,
        comparator_only_success=comparator_only,
        interpretation=interpretation,
    )
