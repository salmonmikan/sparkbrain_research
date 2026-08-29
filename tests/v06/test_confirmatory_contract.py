from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    EvidenceDomain,
    assess_confirmatory_readiness,
    assess_result_coverage,
    build_draft_confirmatory_manifest,
    frozen_manifest_copy,
    score_confirmatory_results,
    with_all_adapters_ready,
)

_FAKE_SHA = "a" * 40


def test_qualification_and_confirmatory_world_seed_minima_are_explicit() -> None:
    qualification = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    confirmatory = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    assert len(qualification.world_families) == 3
    assert len(qualification.seeds) == 3
    assert all(not row.held_out for row in qualification.world_families)
    assert len(confirmatory.world_families) == 5
    assert len(confirmatory.seeds) == 10
    assert all(row.held_out for row in confirmatory.world_families)


def test_draft_manifest_fails_closed_until_code_and_every_adapter_are_frozen() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.ready is False
    assert readiness.code_ref_frozen is False
    assert set(readiness.unavailable_adapters) == {
        row.value for row in ConfirmatoryCondition
    }
    assert readiness.missing_conditions == ()
    assert readiness.missing_evidence_domains == ()


def test_full_adapter_shape_can_become_ready_only_with_a_frozen_sha() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    adapters_ready = with_all_adapters_ready(manifest)
    assert assess_confirmatory_readiness(adapters_ready).ready is False
    frozen = frozen_manifest_copy(adapters_ready, code_ref=_FAKE_SHA)
    readiness = assess_confirmatory_readiness(frozen)
    assert readiness.ready is True
    assert readiness.code_ref_frozen is True
    assert readiness.family_count == readiness.required_family_count == 3
    assert readiness.seed_count == readiness.required_seed_count == 3


def test_manifest_hash_changes_when_a_threshold_or_world_changes() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION,
        code_ref=_FAKE_SHA,
    )
    changed_threshold = replace(
        manifest,
        thresholds=replace(
            manifest.thresholds,
            minimum_overall_success_fraction=0.81,
        ),
    )
    changed_world = replace(
        manifest,
        world_families=(
            replace(
                manifest.world_families[0],
                description="Changed after freeze and therefore a new manifest.",
            ),
            *manifest.world_families[1:],
        ),
    )
    assert manifest.manifest_hash() != changed_threshold.manifest_hash()
    assert manifest.manifest_hash() != changed_world.manifest_hash()


def _all_records(
    manifest,
    *,
    primary_passed: bool,
    comparator_passed: ConfirmatoryCondition | None = None,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return tuple(
        ConfirmatoryResultRecord(
            family_id=family.family_id,
            seed=seed.seed,
            condition=condition.condition,
            evidence_domain=evidence,
            passed=(
                primary_passed
                if condition.condition is ConfirmatoryCondition.PRIMARY
                else condition.condition is comparator_passed
            ),
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
        for evidence in manifest.evidence_domains
    )


def test_result_matrix_requires_every_family_seed_condition_and_domain() -> None:
    manifest = frozen_manifest_copy(
        with_all_adapters_ready(
            build_draft_confirmatory_manifest(
                ConfirmatoryPhase.QUALIFICATION
            )
        ),
        code_ref=_FAKE_SHA,
    )
    records = _all_records(manifest, primary_passed=True)
    complete = assess_result_coverage(manifest, records)
    assert complete.complete is True
    assert complete.expected_record_count == 3 * 3 * 8 * 9

    missing = assess_result_coverage(manifest, records[:-1])
    assert missing.complete is False
    assert len(missing.missing_keys) == 1

    duplicate = assess_result_coverage(manifest, (*records, records[0]))
    assert duplicate.complete is False
    assert len(duplicate.duplicate_keys) == 1


def test_incomplete_or_unready_confirmatory_data_cannot_be_scored() -> None:
    draft = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    with pytest.raises(RuntimeError, match="not execution-ready"):
        score_confirmatory_results(draft, ())

    frozen = frozen_manifest_copy(
        with_all_adapters_ready(draft),
        code_ref=_FAKE_SHA,
    )
    records = _all_records(frozen, primary_passed=True)
    with pytest.raises(RuntimeError, match="matrix is incomplete"):
        score_confirmatory_results(frozen, records[:-1])


def test_primary_support_and_comparator_support_are_reported_separately() -> None:
    manifest = frozen_manifest_copy(
        with_all_adapters_ready(
            build_draft_confirmatory_manifest(
                ConfirmatoryPhase.QUALIFICATION
            )
        ),
        code_ref=_FAKE_SHA,
    )
    primary = score_confirmatory_results(
        manifest,
        _all_records(manifest, primary_passed=True),
    )
    assert primary.primary_supported is True
    assert primary.supported_comparators == ()
    assert primary.comparator_only_success is False

    both = score_confirmatory_results(
        manifest,
        _all_records(
            manifest,
            primary_passed=True,
            comparator_passed=ConfirmatoryCondition.G3_RECURRENT,
        ),
    )
    assert both.primary_supported is True
    assert both.supported_comparators == ("g3-recurrent",)
    assert "uniqueness not established" in both.interpretation


def test_comparator_only_success_is_a_negative_primary_outcome() -> None:
    manifest = frozen_manifest_copy(
        with_all_adapters_ready(
            build_draft_confirmatory_manifest(
                ConfirmatoryPhase.QUALIFICATION
            )
        ),
        code_ref=_FAKE_SHA,
    )
    result = score_confirmatory_results(
        manifest,
        _all_records(
            manifest,
            primary_passed=False,
            comparator_passed=ConfirmatoryCondition.G5_TYPED,
        ),
    )
    assert result.primary_supported is False
    assert result.supported_comparators == ("g5-typed-functional-heads",)
    assert result.comparator_only_success is True
    assert "negative for Primary" in result.interpretation


def test_frozen_sha_and_comparator_isolation_are_validated() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    with pytest.raises(ValueError, match="40-character Git SHA"):
        frozen_manifest_copy(manifest, code_ref="short")

    broken = replace(
        manifest,
        code_ref=_FAKE_SHA,
        conditions=tuple(
            replace(
                row,
                adapter_ready=True,
                isolated_from_primary=(
                    False
                    if row.condition is ConfirmatoryCondition.G4_ASSEMBLY
                    else True
                ),
            )
            for row in manifest.conditions
        ),
    )
    readiness = assess_confirmatory_readiness(broken)
    assert readiness.ready is False
    assert readiness.isolation_violations == ("g4-assembly-conditioned",)


def test_required_evidence_domains_are_not_replaced_by_missing_middle_alone() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION,
        code_ref=_FAKE_SHA,
    )
    missing = replace(
        manifest,
        evidence_domains=(EvidenceDomain.ENDOGENOUS_ORIGIN,),
    )
    readiness = assess_confirmatory_readiness(missing)
    assert readiness.ready is False
    assert "relation-reentry" in readiness.missing_evidence_domains
    assert "persistence-locus" in readiness.missing_evidence_domains
