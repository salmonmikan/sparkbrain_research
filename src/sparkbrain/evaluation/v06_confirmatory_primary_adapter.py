from __future__ import annotations

from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from .v06_confirmatory_primary import (
    QUALIFICATION_FAMILIES,
    QUALIFICATION_SEEDS,
    PrimaryQualificationGrid,
    PrimaryWorldEvidence,
    PrimaryWorldParameters,
    _autonomous_chain,
    _boundary_and_stabilization,
    _relation_reentry_and_persistence,
    _revision_states,
    _state_and_origin,
)
from .v06_confirmatory_primary import (
    world_parameters as _base_world_parameters,
)


def world_parameters(family_id: str, seed: int) -> PrimaryWorldParameters:
    """Return the reviewed qualification parameters.

    Reliability 0.5 must remain sub-threshold, while the return-state
    reliability 7/11 and acquired reliability 0.8 must cross threshold. The
    structural gain boundary is therefore normalized by 0.60 rather than 0.65.
    """

    row = _base_world_parameters(family_id, seed)
    return replace(
        row,
        relation_reentry_gain=row.threshold / 0.60,
    )


def evaluate_primary_world(
    family_id: str,
    seed: int,
) -> PrimaryWorldEvidence:
    parameters = world_parameters(family_id, seed)
    origin, state, origin_metrics = _state_and_origin(parameters)
    chain, chain_metrics = _autonomous_chain(parameters)
    boundary, stabilization, taxonomy, boundary_metrics = (
        _boundary_and_stabilization(parameters)
    )
    acquired, reversed_state, returned, revision, revision_metrics = (
        _revision_states(parameters)
    )
    reentry, persistence, reentry_metrics = _relation_reentry_and_persistence(
        parameters,
        acquired,
        reversed_state,
        returned,
    )
    metrics = tuple(
        sorted(
            {
                **origin_metrics,
                **chain_metrics,
                **boundary_metrics,
                **revision_metrics,
                **reentry_metrics,
                "boundary_lag_ms": parameters.boundary_lag_ms,
                "relation_reentry_gain": parameters.relation_reentry_gain,
                "threshold": parameters.threshold,
                "transition_lag_ms": parameters.transition_lag_ms,
            }.items()
        )
    )
    return PrimaryWorldEvidence(
        family_id=family_id,
        seed=seed,
        endogenous_origin_passed=origin,
        state_dependence_passed=state,
        autonomous_chain_passed=chain,
        boundary_effect_passed=boundary,
        relation_stabilization_passed=stabilization,
        reversal_reacquisition_passed=revision,
        relation_reentry_passed=reentry,
        persistence_locus_passed=persistence,
        taxonomy_non_interference_passed=taxonomy,
        metrics=metrics,
    )


def records_from_evidence(
    evidence: PrimaryWorldEvidence,
) -> tuple[ConfirmatoryResultRecord, ...]:
    passed = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: evidence.endogenous_origin_passed,
        EvidenceDomain.STATE_DEPENDENCE: evidence.state_dependence_passed,
        EvidenceDomain.AUTONOMOUS_CHAIN: evidence.autonomous_chain_passed,
        EvidenceDomain.BOUNDARY_EFFECT: evidence.boundary_effect_passed,
        EvidenceDomain.RELATION_STABILIZATION: (
            evidence.relation_stabilization_passed
        ),
        EvidenceDomain.REVERSAL_REACQUISITION: (
            evidence.reversal_reacquisition_passed
        ),
        EvidenceDomain.RELATION_REENTRY: evidence.relation_reentry_passed,
        EvidenceDomain.PERSISTENCE_LOCUS: evidence.persistence_locus_passed,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: (
            evidence.taxonomy_non_interference_passed
        ),
    }
    return tuple(
        ConfirmatoryResultRecord(
            family_id=evidence.family_id,
            seed=evidence.seed,
            condition=ConfirmatoryCondition.PRIMARY,
            evidence_domain=domain,
            passed=passed[domain],
            metrics=evidence.metrics,
        )
        for domain in EvidenceDomain
    )


def run_condition(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return records_from_evidence(evaluate_primary_world(family_id, seed))


def run_primary_qualification_grid() -> PrimaryQualificationGrid:
    worlds = tuple(
        evaluate_primary_world(family_id, seed)
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
    )
    records = tuple(
        record for world in worlds for record in records_from_evidence(world)
    )
    return PrimaryQualificationGrid(worlds=worlds, records=records)
