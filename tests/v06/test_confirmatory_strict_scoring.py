from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    EvidenceDomain,
    build_draft_confirmatory_manifest,
    frozen_manifest_copy,
    with_all_adapters_ready,
)
from sparkbrain.evaluation.v06_confirmatory_scoring import (
    assess_strict_metric_coverage,
    score_strict_confirmatory_results,
)

_FAKE_SHA = "b" * 40
_NULL_CONDITIONS = {
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
}
_EARLY_SHUFFLED_DOMAINS = {
    EvidenceDomain.ENDOGENOUS_ORIGIN,
    EvidenceDomain.STATE_DEPENDENCE,
    EvidenceDomain.AUTONOMOUS_CHAIN,
    EvidenceDomain.BOUNDARY_EFFECT,
    EvidenceDomain.RELATION_STABILIZATION,
    EvidenceDomain.REVERSAL_REACQUISITION,
    EvidenceDomain.TAXONOMY_NON_INTERFERENCE,
}


def _manifest():
    return frozen_manifest_copy(
        with_all_adapters_ready(
            build_draft_confirmatory_manifest(
                ConfirmatoryPhase.QUALIFICATION
            )
        ),
        code_ref=_FAKE_SHA,
    )


def _metrics(condition: ConfirmatoryCondition) -> tuple[tuple[str, float], ...]:
    values = {
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": 1.0,
    }
    if condition is ConfirmatoryCondition.PRIMARY:
        values.update(
            {
                "boundary_matched_impairment": 0.0,
                "boundary_targeted_impairment": 1.0,
                "chain_matched_impairment": 0.0,
                "chain_targeted_impairment": 1.0,
            }
        )
    elif condition in {
        *_NULL_CONDITIONS,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }:
        values["control_contract_passed"] = 1.0
    return tuple(sorted(values.items()))


def _passed(
    condition: ConfirmatoryCondition,
    domain: EvidenceDomain,
    *,
    primary_passed: bool,
    comparator_passed: ConfirmatoryCondition | None,
) -> bool:
    if condition is ConfirmatoryCondition.PRIMARY:
        return primary_passed
    if condition in _NULL_CONDITIONS:
        return domain is EvidenceDomain.TAXONOMY_NON_INTERFERENCE
    if condition is ConfirmatoryCondition.SHUFFLED_RELATION:
        return domain in _EARLY_SHUFFLED_DOMAINS
    if condition in {
        ConfirmatoryCondition.G3_RECURRENT,
        ConfirmatoryCondition.G4_ASSEMBLY,
        ConfirmatoryCondition.G5_TYPED,
    }:
        return condition is comparator_passed
    raise AssertionError(condition)


def _records(
    *,
    primary_passed: bool = True,
    comparator_passed: ConfirmatoryCondition | None = None,
) -> tuple[ConfirmatoryResultRecord, ...]:
    manifest = _manifest()
    return tuple(
        ConfirmatoryResultRecord(
            family_id=family.family_id,
            seed=seed.seed,
            condition=condition.condition,
            evidence_domain=domain,
            passed=_passed(
                condition.condition,
                domain,
                primary_passed=primary_passed,
                comparator_passed=comparator_passed,
            ),
            metrics=_metrics(condition.condition),
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
        for domain in manifest.evidence_domains
    )


def _replace_group_metrics(
    records: tuple[ConfirmatoryResultRecord, ...],
    *,
    family_id: str,
    seed: int,
    condition: ConfirmatoryCondition,
    changes: dict[str, float | None],
) -> tuple[ConfirmatoryResultRecord, ...]:
    result = []
    for row in records:
        if (
            row.family_id == family_id
            and row.seed == seed
            and row.condition is condition
        ):
            metrics = dict(row.metrics)
            for key, value in changes.items():
                if value is None:
                    metrics.pop(key, None)
                else:
                    metrics[key] = value
            row = replace(row, metrics=tuple(sorted(metrics.items())))
        result.append(row)
    return tuple(result)


def test_clean_complete_matrix_passes_every_strict_gate() -> None:
    outcome = score_strict_confirmatory_results(_manifest(), _records())
    assert outcome.primary_raw_supported is True
    assert outcome.null_false_positive_fraction == 0.0
    assert outcome.minimum_selective_effect == 1.0
    assert outcome.taxonomy_hash_match_fraction == 1.0
    assert outcome.self_confirmation_violations == 0
    assert outcome.control_contract_fraction == 1.0
    assert outcome.control_and_safety_gates_passed is True
    assert outcome.primary_supported is True
    assert outcome.supported_comparators == ()


def test_null_false_positives_reject_raw_primary_success() -> None:
    records = tuple(
        replace(row, passed=True)
        if row.condition is ConfirmatoryCondition.NO_ENDOGENOUS
        else row
        for row in _records()
    )
    outcome = score_strict_confirmatory_results(_manifest(), records)
    assert outcome.primary_raw_supported is True
    assert outcome.null_false_positive_fraction > 0.10
    assert outcome.control_and_safety_gates_passed is False
    assert outcome.primary_supported is False
    assert "raw success is rejected" in outcome.interpretation


def test_subthreshold_selective_effect_rejects_primary_support() -> None:
    records = _records()
    for family in _manifest().world_families:
        for seed in _manifest().seeds:
            records = _replace_group_metrics(
                records,
                family_id=family.family_id,
                seed=seed.seed,
                condition=ConfirmatoryCondition.PRIMARY,
                changes={
                    "boundary_targeted_impairment": 0.40,
                    "chain_targeted_impairment": 0.40,
                },
            )
    outcome = score_strict_confirmatory_results(_manifest(), records)
    assert outcome.minimum_selective_effect == pytest.approx(0.40)
    assert outcome.primary_supported is False


def test_any_primary_taxonomy_hash_mismatch_fails_the_one_point_zero_gate() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.PRIMARY,
        changes={"taxonomy_hash_match": 0.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.taxonomy_hash_match_fraction < 1.0
    assert outcome.primary_supported is False


def test_one_primary_self_confirmation_violation_fails_closed() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.PRIMARY,
        changes={"self_confirmation_violations": 1.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.self_confirmation_violations == 1
    assert outcome.primary_supported is False


def test_one_control_self_confirmation_violation_fails_primary_safety() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.RANDOM_MATCHED,
        changes={"self_confirmation_violations": 1.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.self_confirmation_violations == 1
    assert outcome.primary_supported is False


def test_comparator_self_confirmation_failure_does_not_veto_clean_primary() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(comparator_passed=ConfirmatoryCondition.G3_RECURRENT),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.G3_RECURRENT,
        changes={"self_confirmation_violations": 1.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.self_confirmation_violations == 0
    assert outcome.primary_supported is True
    assert outcome.supported_comparators == ()


def test_comparator_taxonomy_failure_does_not_veto_clean_primary() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(comparator_passed=ConfirmatoryCondition.G5_TYPED),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.G5_TYPED,
        changes={"taxonomy_hash_match": 0.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.taxonomy_hash_match_fraction == 1.0
    assert outcome.primary_supported is True
    assert outcome.supported_comparators == ()


def test_failed_control_contract_rejects_primary_support() -> None:
    manifest = _manifest()
    records = _replace_group_metrics(
        _records(),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.RANDOM_MATCHED,
        changes={"control_contract_passed": 0.0},
    )
    outcome = score_strict_confirmatory_results(manifest, records)
    assert outcome.control_contract_fraction < 1.0
    assert outcome.primary_supported is False


def test_missing_or_inconsistent_metrics_block_scoring() -> None:
    manifest = _manifest()
    missing = _replace_group_metrics(
        _records(),
        family_id=manifest.world_families[0].family_id,
        seed=manifest.seeds[0].seed,
        condition=ConfirmatoryCondition.PRIMARY,
        changes={"chain_targeted_impairment": None},
    )
    coverage = assess_strict_metric_coverage(manifest, missing)
    assert coverage.complete is False
    assert any(
        "chain_targeted_impairment" in row
        for row in coverage.missing_metric_keys
    )
    with pytest.raises(RuntimeError, match="metric contract is incomplete"):
        score_strict_confirmatory_results(manifest, missing)

    one_row_changed = list(_records())
    first = one_row_changed[0]
    one_row_changed[0] = replace(
        first,
        metrics=tuple(
            sorted(
                {
                    **dict(first.metrics),
                    "chain_targeted_impairment": 0.75,
                }.items()
            )
        ),
    )
    inconsistent = assess_strict_metric_coverage(
        manifest,
        tuple(one_row_changed),
    )
    assert inconsistent.complete is False
    assert inconsistent.inconsistent_metric_groups


def test_comparator_only_support_remains_negative_for_primary() -> None:
    outcome = score_strict_confirmatory_results(
        _manifest(),
        _records(
            primary_passed=False,
            comparator_passed=ConfirmatoryCondition.G3_RECURRENT,
        ),
    )
    assert outcome.primary_supported is False
    assert outcome.supported_comparators == ("g3-recurrent",)
    assert outcome.comparator_only_success is True
    assert "negative for the Primary" in outcome.interpretation


def test_incomplete_matrix_cannot_reach_metric_scoring() -> None:
    records = _records()
    with pytest.raises(RuntimeError, match="matrix is incomplete"):
        score_strict_confirmatory_results(_manifest(), records[:-1])
