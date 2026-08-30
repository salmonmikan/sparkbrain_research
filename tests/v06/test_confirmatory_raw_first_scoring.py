from __future__ import annotations

import inspect
from dataclasses import replace
from pathlib import Path

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_artifacts import RawRunReceipt
from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment import (
    ENVIRONMENT_LOCK_VERSION,
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    build_freeze_record,
)
from sparkbrain.evaluation.v06_confirmatory_raw_evidence import VerifiedRawEvidence
from sparkbrain.evaluation.v06_confirmatory_resource_accounting import (
    RESOURCE_ACCOUNTING_VERSION,
    NormalizedConditionResourceRecord,
    ResourceDecisionUse,
)
from sparkbrain.evaluation.v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
)
from sparkbrain.evaluation.v06_confirmatory_score_raw import (
    analysis_contract_hash,
    build_analysis_summary,
    score_raw_cli,
)
from sparkbrain.v06.foundation import digest

_SOURCE_SHA = "a" * 40
_SHUFFLED_POSITIVE = {
    EvidenceDomain.ENDOGENOUS_ORIGIN,
    EvidenceDomain.STATE_DEPENDENCE,
    EvidenceDomain.AUTONOMOUS_CHAIN,
    EvidenceDomain.BOUNDARY_EFFECT,
    EvidenceDomain.RELATION_STABILIZATION,
    EvidenceDomain.REVERSAL_REACQUISITION,
    EvidenceDomain.TAXONOMY_NON_INTERFERENCE,
}


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _environment() -> ConfirmatoryEnvironmentLock:
    distributions = ("sparkbrain-research==0.3.2.dev0",)
    return ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation="CPython",
        python_version="3.11.9",
        python_executable_sha256="b" * 64,
        platform_system="Linux",
        platform_release="6.8.0-analysis-test",
        platform_machine="x86_64",
        os_release=(("ID", "ubuntu"), ("VERSION_ID", "24.04")),
        runner_os="Linux",
        runner_arch="X64",
        runner_image_os="ubuntu24",
        runner_image_version="20260825.1.0",
        python_hash_seed="0",
        timezone="UTC",
        locale_name="C.UTF-8",
        installed_distributions=distributions,
        installed_distributions_hash=digest(list(distributions)),
        rng_contract_hash=RNG_CONTRACT.contract_hash(),
    )


def _passed(condition: ConfirmatoryCondition, domain: EvidenceDomain) -> bool:
    if condition is ConfirmatoryCondition.PRIMARY:
        return True
    if condition in {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
    }:
        return domain is EvidenceDomain.TAXONOMY_NON_INTERFERENCE
    if condition is ConfirmatoryCondition.SHUFFLED_RELATION:
        return domain in _SHUFFLED_POSITIVE
    return True


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
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }:
        values["control_contract_passed"] = 1.0
    return tuple(sorted(values.items()))


def _privileges(condition: ConfirmatoryCondition):
    if condition is ConfirmatoryCondition.G4_ASSEMBLY:
        return (PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,)
    if condition is ConfirmatoryCondition.G5_TYPED:
        return (
            PrivilegedInformation.TYPED_PREDICTION_HEAD,
            PrivilegedInformation.TYPED_BOUNDARY_HEAD,
            PrivilegedInformation.TYPED_MEMORY_HEAD,
            PrivilegedInformation.SCALAR_REWARD,
        )
    return ()


def _raw_resource(
    family_id: str,
    seed: int,
    condition: ConfirmatoryCondition,
) -> ConditionResourceRecord:
    field_condition = condition in {
        ConfirmatoryCondition.PRIMARY,
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }
    return ConditionResourceRecord(
        family_id=family_id,
        seed=seed,
        condition=condition,
        observed_training_events=10,
        generated_internal_events=0 if condition is ConfirmatoryCondition.NO_ENDOGENOUS else 2,
        persistent_state_entries=5,
        intervention_count=1,
        parameter_count=7,
        wall_clock_ms=1.0,
        normal_field_threshold_present=field_condition,
        normal_field_threshold_crossings=1 if field_condition else 0,
        threshold_bypassed=not field_condition,
        explicit_assembly_entries=(
            2 if condition is ConfirmatoryCondition.G4_ASSEMBLY else 0
        ),
        typed_head_count=(
            4 if condition is ConfirmatoryCondition.G5_TYPED else 0
        ),
        scalar_reward_observations=(
            3 if condition is ConfirmatoryCondition.G5_TYPED else 0
        ),
        privileged_information=_privileges(condition),
    )


def _normalized(raw: ConditionResourceRecord) -> NormalizedConditionResourceRecord:
    operation_proxy = (
        raw.observed_training_events
        + raw.generated_internal_events
        + raw.intervention_count
        + raw.normal_field_threshold_crossings
    )
    return NormalizedConditionResourceRecord(
        family_id=raw.family_id,
        seed=raw.seed,
        condition=raw.condition,
        accounting_version=RESOURCE_ACCOUNTING_VERSION,
        decision_use=ResourceDecisionUse.DESCRIPTIVE_ONLY,
        adapter_observed_training_event_proxy=raw.observed_training_events,
        adapter_generated_event_proxy=raw.generated_internal_events,
        adapter_intervention_event_proxy=raw.intervention_count,
        adapter_mutable_state_scalar_proxy=raw.parameter_count,
        adapter_persistent_state_entry_proxy=raw.persistent_state_entries,
        adapter_logical_operation_proxy_units=operation_proxy,
        wall_clock_ns=1_000,
        process_cpu_ns=900,
        peak_traced_memory_bytes=2_000,
        canonical_output_bytes=500,
        normal_field_threshold_present=raw.normal_field_threshold_present,
        normal_field_threshold_crossings=raw.normal_field_threshold_crossings,
        threshold_bypassed=raw.threshold_bypassed,
        explicit_assembly_entries=raw.explicit_assembly_entries,
        typed_head_count=raw.typed_head_count,
        scalar_reward_observations=raw.scalar_reward_observations,
        privileged_information_count=len(raw.privileged_information),
    )


def _evidence():
    manifest = build_candidate_manifest(source_code_sha=_SOURCE_SHA)
    results = tuple(
        ConfirmatoryResultRecord(
            family_id=family.family_id,
            seed=seed.seed,
            condition=registration.condition,
            evidence_domain=domain,
            passed=_passed(registration.condition, domain),
            metrics=_metrics(registration.condition),
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for registration in manifest.conditions
        for domain in manifest.evidence_domains
    )
    raw_resources = tuple(
        _raw_resource(
            family.family_id,
            seed.seed,
            registration.condition,
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for registration in manifest.conditions
    )
    normalized = tuple(_normalized(row) for row in raw_resources)
    execution_ids = tuple(
        f"synthetic-{index:03d}" for index in range(len(raw_resources))
    )
    receipt = RawRunReceipt(
        run_id="synthetic-raw-first-test",
        final_directory="/immutable/synthetic",
        execution_count=len(raw_resources),
        result_record_count=len(results),
        raw_resource_count=len(raw_resources),
        normalized_resource_count=len(normalized),
        raw_manifest_hash="c" * 64,
        run_checksums_hash="d" * 64,
        immutable_permissions_applied=True,
    )
    evidence = VerifiedRawEvidence(
        run_id=receipt.run_id,
        raw_directory=receipt.final_directory,
        freeze_seal_hash="e" * 64,
        source_code_sha=_SOURCE_SHA,
        manifest_hash=manifest.manifest_hash(),
        world_generation_id="v06-confirmatory-candidate-002",
        receipt=receipt,
        results=results,
        raw_resources=raw_resources,
        normalized_resources=normalized,
        execution_ids=execution_ids,
        world_specification_hashes=tuple(
            (
                f"{family.family_id}|{seed.seed}",
                digest((family.family_id, seed.seed)),
            )
            for family in manifest.world_families
            for seed in manifest.seeds
        ),
        immutable_and_complete=True,
    )
    evidence.validate(manifest)
    freeze = build_freeze_record(
        manifest,
        source_code_sha=_SOURCE_SHA,
        repository_root=_repository_root(),
        environment_lock=_environment(),
        approval_id="APPROVED:analysis-test:0123456789abcdef",
    )
    return manifest, freeze, evidence


def test_preregistered_analysis_scores_only_verified_complete_raw_records() -> None:
    manifest, freeze, evidence = _evidence()
    summary, outcome = build_analysis_summary(evidence, manifest, freeze)
    assert len(evidence.results) == 3_600
    assert len(evidence.raw_resources) == 400
    assert len(evidence.normalized_resources) == 400
    assert outcome.primary_supported is True
    assert outcome.supported_comparators == (
        "g3-recurrent",
        "g4-assembly-conditioned",
        "g5-typed-functional-heads",
    )
    assert summary["resource_accounting"]["affects_capability_result"] is False
    assert summary["resource_accounting"]["decision_use"] == "descriptive-only"
    assert len(summary["resource_accounting"]["policy_hash"]) == 64
    assert summary["analysis_contract_hash"] == analysis_contract_hash()


def test_extreme_descriptive_resource_values_do_not_change_capability_result() -> None:
    manifest, freeze, evidence = _evidence()
    _, baseline = build_analysis_summary(evidence, manifest, freeze)
    changed_resources = tuple(
        replace(
            row,
            wall_clock_ns=10**18,
            process_cpu_ns=10**18,
            peak_traced_memory_bytes=10**18,
            canonical_output_bytes=10**12,
        )
        for row in evidence.normalized_resources
    )
    changed = replace(evidence, normalized_resources=changed_resources)
    _, rescored = build_analysis_summary(changed, manifest, freeze)
    assert rescored == baseline


def test_raw_first_scorer_source_has_no_capability_adapter_or_world_execution() -> None:
    source = Path(
        "src/sparkbrain/evaluation/v06_confirmatory_score_raw.py"
    ).read_text(encoding="utf-8")
    assert "run_registered_condition" not in source
    assert "build_heldout_world_grid" not in source
    assert "v06_confirmatory_heldout_primary" not in source
    cli_source = inspect.getsource(score_raw_cli)
    assert cli_source.index("evidence = load_verified_raw_evidence(") < (
        cli_source.index("return write_analysis_transaction(")
    )
    assert "raw evidence changed during scoring" in source
