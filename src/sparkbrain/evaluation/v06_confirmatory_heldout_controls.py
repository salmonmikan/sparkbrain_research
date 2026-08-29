from __future__ import annotations

import copy
import math
import random
import time
from collections.abc import Callable, Mapping
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v06.endogenous_chain import EndogenousChainIntervention
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    ProvenanceLedger,
    digest,
)
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.taxonomy import verify_taxonomy_variant_runtime_equality

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
    build_result_records,
    result_record_state,
)
from .v06_confirmatory_heldout_primary import (
    active_paths,
    build_field,
    build_runtime,
    evaluation_horizon,
    external_pulse,
    leaf_count,
    relation_cycles,
    reentry_units,
    run_condition as run_primary_condition,
    run_cue,
    train_expectation,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import ConditionResourceRecord


CONTROL_CONDITIONS = (
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
)

PRESERVED_SHUFFLE_DOMAINS = frozenset(
    {
        EvidenceDomain.ENDOGENOUS_ORIGIN,
        EvidenceDomain.STATE_DEPENDENCE,
        EvidenceDomain.AUTONOMOUS_CHAIN,
        EvidenceDomain.BOUNDARY_EFFECT,
        EvidenceDomain.RELATION_STABILIZATION,
        EvidenceDomain.REVERSAL_REACQUISITION,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE,
    }
)


def taxonomy_matches(state: dict[str, Any]) -> bool:
    return len(
        verify_taxonomy_variant_runtime_equality(
            {
                "observer-a": state,
                "renamed-observer": state,
            }
        )
    ) == 64


def build_execution(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
    passed: dict[EvidenceDomain, bool],
    metrics: dict[str, float],
    resource: ConditionResourceRecord,
) -> HeldoutConditionExecution:
    records = build_result_records(parameters, condition, passed, metrics)
    semantic_hash = digest(
        {
            "records": [result_record_state(row) for row in records],
            "resource": {
                key: value
                for key, value in resource.state_dict().items()
                if key != "wall_clock_ms"
            },
            "world_specification_hash": parameters.specification_hash(),
        }
    )
    execution = HeldoutConditionExecution(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=condition,
        world_specification_hash=parameters.specification_hash(),
        records=records,
        resource=resource,
        semantic_hash=semantic_hash,
    )
    execution.validate()
    return execution


def false_domains(taxonomy: bool) -> dict[EvidenceDomain, bool]:
    return {
        domain: (
            domain is EvidenceDomain.TAXONOMY_NON_INTERFERENCE and taxonomy
        )
        for domain in EvidenceDomain
    }


def run_no_endogenous(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    started = time.perf_counter()
    intervention = EndogenousChainIntervention(
        suppress_reinjection_depths=tuple(range(1, 9))
    )
    runtimes = tuple(
        build_runtime(
            parameters,
            (path,),
            intervention=intervention,
        )
        for path in (
            parameters.main_path,
            parameters.alternate_path,
            parameters.control_path,
        )
    )
    paths = (
        parameters.main_path,
        parameters.alternate_path,
        parameters.control_path,
    )
    results = tuple(
        run_cue(
            runtime,
            parameters,
            cue_unit_id=path[0],
            start_ms=100.0,
            event_id=f"heldout:no-endogenous:{index}",
        )
        for index, (runtime, path) in enumerate(zip(runtimes, paths, strict=True))
    )
    generated = sum(len(row.units) for row in results)
    state = {
        str(index): runtime.state_dict()
        for index, runtime in enumerate(runtimes)
    }
    taxonomy = taxonomy_matches(state)
    contract = bool(
        generated == 0
        and all(runtime.ledger.committed_positive_updates == 0 for runtime in runtimes)
    )
    metrics = {
        "control_contract_passed": float(contract),
        "heldout_no_endogenous_generated_count": float(generated),
        "heldout_no_endogenous_suppression_count": float(
            sum(len(runtime.intervention_records) for runtime in runtimes)
        ),
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
    }
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.NO_ENDOGENOUS,
        observed_training_events=sum(
            runtime.expectation.external_transition_count for runtime in runtimes
        ),
        generated_internal_events=generated,
        persistent_state_entries=leaf_count(state),
        intervention_count=sum(
            len(runtime.intervention_records) for runtime in runtimes
        ),
        parameter_count=parameters.unit_count * 3 + leaf_count(state),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        ordinary_field_threshold_crossings=generated,
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )
    return build_execution(
        parameters,
        ConfirmatoryCondition.NO_ENDOGENOUS,
        false_domains(taxonomy),
        metrics,
        resource,
    )


def readout_path(
    parameters: HeldoutWorldParameters,
    path: tuple[int, int, int, int],
    event_id: str,
) -> tuple[tuple[str, ...], int, dict[str, Any], int]:
    model = train_expectation(parameters, (path,))
    field = build_field(parameters)
    current = external_pulse(parameters, event_id, 100.0, path[0])
    field.schedule_arrival(
        SynapticArrival(
            time_ms=current.time_ms,
            target_id=path[0],
            current=current.magnitude,
            source_id=None,
            pulse_id=current.event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    field.run_until(current.time_ms)
    proposals = model.proposals_for(
        current,
        origin_state_hash=digest(
            {
                "field": field.state_dict(),
                "local_transition": model.learned_state_dict(),
            }
        ),
    )
    later_spikes = field.run_until(
        evaluation_horizon(parameters, current.time_ms)
    )
    state = {
        "field": field.state_dict(),
        "local_transition": model.state_dict(),
        "proposal_count": len(proposals),
    }
    return (
        tuple(row.target for row in proposals),
        len(later_spikes),
        state,
        model.external_transition_count,
    )


def run_readout_only(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    started = time.perf_counter()
    main_targets, main_spikes, main_state, main_training = readout_path(
        parameters,
        parameters.main_path,
        "heldout:readout:main",
    )
    alternate_targets, alternate_spikes, alternate_state, alternate_training = (
        readout_path(
            parameters,
            parameters.alternate_path,
            "heldout:readout:alternate",
        )
    )
    state = {"alternate": alternate_state, "main": main_state}
    taxonomy = taxonomy_matches(state)
    contract = bool(
        f"unit:{parameters.main_path[1]}" in main_targets
        and f"unit:{parameters.alternate_path[1]}" in alternate_targets
        and main_spikes == 0
        and alternate_spikes == 0
    )
    metrics = {
        "control_contract_passed": float(contract),
        "heldout_readout_alternate_proposal_count": float(len(alternate_targets)),
        "heldout_readout_later_field_spark_count": float(
            main_spikes + alternate_spikes
        ),
        "heldout_readout_main_proposal_count": float(len(main_targets)),
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
    }
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.READOUT_ONLY,
        observed_training_events=main_training + alternate_training,
        generated_internal_events=len(main_targets) + len(alternate_targets),
        persistent_state_entries=leaf_count(state),
        intervention_count=0,
        parameter_count=leaf_count(state),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        ordinary_field_threshold_crossings=0,
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )
    return build_execution(
        parameters,
        ConfirmatoryCondition.READOUT_ONLY,
        false_domains(taxonomy),
        metrics,
        resource,
    )


def random_targets(
    parameters: HeldoutWorldParameters,
    count: int,
) -> tuple[int, ...]:
    excluded = set(parameters.main_path)
    candidates = [
        unit_id
        for unit_id in (*parameters.distractor_unit_ids, *parameters.active_unit_ids)
        if unit_id not in excluded
    ]
    if not candidates:
        raise RuntimeError("held-out random control has no non-main target")
    rng = random.Random(
        int(
            digest(
                {
                    "condition": "heldout-random-matched",
                    "family_id": parameters.family_id,
                    "seed": parameters.seed,
                }
            )[:16],
            16,
        )
    )
    rng.shuffle(candidates)
    return tuple(candidates[index % len(candidates)] for index in range(count))


def run_random_matched(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    started = time.perf_counter()
    reference = build_runtime(parameters, active_paths(parameters))
    run_cue(
        reference,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="heldout:random:reference",
    )
    reference_rows = tuple(
        row
        for row in reference.proposal_records
        if row.reinjection is not None and row.reinjection.accepted
    )
    targets = random_targets(parameters, len(reference_rows))

    ledger = ProvenanceLedger()
    field = build_field(parameters)
    current = external_pulse(
        parameters,
        "heldout:random:cue",
        100.0,
        parameters.main_path[0],
    )
    ledger.register_external(current)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=current.time_ms,
            target_id=parameters.main_path[0],
            current=current.magnitude,
            source_id=None,
            pulse_id=current.event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    field.run_until(current.time_ms)
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=1.0,
            maximum_effective_current=256.0,
            maximum_generation_depth=8,
            maximum_energy_per_window=512.0,
            maximum_proposals_per_window=128,
            maximum_branches_per_origin_state=128,
            window_ms=max(parameters.episode_spacings_ms),
        ),
    )
    decisions = []
    for index, (target, reference_row) in enumerate(
        zip(targets, reference_rows, strict=True)
    ):
        assert reference_row.reinjection is not None
        effective_current = abs(reference_row.reinjection.effective_current)
        proposal = EndogenousPulseProposal(
            proposal_id=(
                f"heldout-random:{parameters.family_id}:{parameters.seed}:{index}"
            ),
            created_at_ms=current.time_ms,
            target=f"unit:{target}",
            predicted_arrival_ms=reference_row.predicted_arrival_ms,
            magnitude=effective_current,
            polarity=1,
            confidence=1.0,
            origin_state_hash=digest(
                {
                    "condition": "heldout-random-matched",
                    "family_id": parameters.family_id,
                    "seed": parameters.seed,
                }
            ),
            local_path_ids=(f"heldout-random-path:{index}",),
            generation_depth=reference_row.generation_depth,
            valid_until_ms=reference_row.predicted_arrival_ms + 50.0,
            energy_cost=max(
                0.0,
                reference_row.reinjection.energy_cost - effective_current,
            ),
        )
        ledger.register_proposal(proposal)
        decisions.append(gate.schedule(proposal, field))
    horizon = max(
        (row.predicted_arrival_ms for row in reference_rows),
        default=current.time_ms,
    ) + 1.0
    random_spikes = field.run_until(horizon)
    reference_times = tuple(row.predicted_arrival_ms for row in reference_rows)
    random_times = tuple(row.scheduled_time_ms for row in decisions)
    reference_currents = tuple(
        abs(row.reinjection.effective_current)
        for row in reference_rows
        if row.reinjection is not None
    )
    random_currents = tuple(abs(row.effective_current) for row in decisions)
    reference_energy = sum(
        row.reinjection.energy_cost
        for row in reference_rows
        if row.reinjection is not None
    )
    random_energy = sum(row.energy_cost for row in decisions)
    matched = bool(
        len(reference_rows) == len(decisions)
        and reference_times == random_times
        and all(
            math.isclose(left, right, rel_tol=0.0, abs_tol=1e-12)
            for left, right in zip(reference_currents, random_currents, strict=True)
        )
        and math.isclose(
            reference_energy,
            random_energy,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    avoids_main = not set(targets).intersection(parameters.main_path[1:])
    state = {
        "field": field.state_dict(),
        "gate": gate.state_dict(),
        "ledger": ledger.state_dict(),
    }
    taxonomy = taxonomy_matches(state)
    contract = bool(
        matched
        and avoids_main
        and ledger.committed_positive_updates == 0
    )
    metrics = {
        "control_contract_passed": float(contract),
        "heldout_random_field_spark_count": float(len(random_spikes)),
        "heldout_random_matched_event_count": float(len(decisions)),
        "heldout_random_matched_total_energy": float(random_energy),
        "heldout_random_sequential_parent_count": 0.0,
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
    }
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.RANDOM_MATCHED,
        observed_training_events=reference.expectation.external_transition_count,
        generated_internal_events=len(random_spikes),
        persistent_state_entries=leaf_count(state),
        intervention_count=0,
        parameter_count=parameters.unit_count * 3 + leaf_count(state),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        ordinary_field_threshold_crossings=len(random_spikes),
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )
    return build_execution(
        parameters,
        ConfirmatoryCondition.RANDOM_MATCHED,
        false_domains(taxonomy),
        metrics,
        resource,
    )


def rotate_relation_state(
    parameters: HeldoutWorldParameters,
    state: dict[str, Any],
) -> dict[str, Any]:
    value = copy.deepcopy(state)
    rotation = {
        f"unit:{parameters.old_target}": f"unit:{parameters.new_target}",
        f"unit:{parameters.new_target}": f"unit:{parameters.third_target}",
        f"unit:{parameters.third_target}": f"unit:{parameters.old_target}",
    }
    for row in value["links"].values():
        target = str(row["target"])
        row["target"] = rotation.get(target, target)
    return value


def run_shuffled_relation(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    started = time.perf_counter()
    primary = run_primary_condition(parameters)
    primary_pass = {
        row.evidence_domain: row.passed for row in primary.records
    }
    relation = relation_cycles(parameters)
    shuffled = tuple(
        rotate_relation_state(parameters, snapshot)
        for snapshot in relation.snapshots
    )
    responses = tuple(
        reentry_units(
            parameters,
            state,
            event_id=f"heldout:shuffled:{index}",
        )
        for index, state in enumerate(shuffled)
    )
    correct = tuple(
        response == (target,)
        for response, target in zip(
            responses,
            parameters.contingency_cycle_targets,
            strict=True,
        )
    )
    wrong_present = all(responses)
    taxonomy = primary_pass[EvidenceDomain.TAXONOMY_NON_INTERFERENCE]
    passed = {
        domain: (
            primary_pass[domain]
            if domain in PRESERVED_SHUFFLE_DOMAINS
            else False
        )
        for domain in EvidenceDomain
    }
    passed[EvidenceDomain.TAXONOMY_NON_INTERFERENCE] = taxonomy
    contract = bool(not any(correct) and wrong_present)
    metrics = {
        "control_contract_passed": float(contract),
        "heldout_shuffled_correct_reentry_fraction": float(
            sum(correct) / len(correct)
        ),
        "heldout_shuffled_response_count": float(
            sum(len(response) for response in responses)
        ),
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
    }
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.SHUFFLED_RELATION,
        observed_training_events=primary.resource.observed_training_events,
        generated_internal_events=(
            primary.resource.generated_internal_events
            + sum(len(response) for response in responses)
        ),
        persistent_state_entries=primary.resource.persistent_state_entries,
        intervention_count=primary.resource.intervention_count + len(responses),
        parameter_count=primary.resource.parameter_count,
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        ordinary_field_threshold_crossings=(
            primary.resource.ordinary_field_threshold_crossings
            + sum(len(response) for response in responses)
        ),
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )
    return build_execution(
        parameters,
        ConfirmatoryCondition.SHUFFLED_RELATION,
        passed,
        metrics,
        resource,
    )


RUNNERS: dict[
    ConfirmatoryCondition,
    Callable[[HeldoutWorldParameters], HeldoutConditionExecution],
] = {
    ConfirmatoryCondition.NO_ENDOGENOUS: run_no_endogenous,
    ConfirmatoryCondition.RANDOM_MATCHED: run_random_matched,
    ConfirmatoryCondition.READOUT_ONLY: run_readout_only,
    ConfirmatoryCondition.SHUFFLED_RELATION: run_shuffled_relation,
}


def run_condition(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    try:
        runner = RUNNERS[condition]
    except KeyError as error:
        raise ValueError(f"not a held-out control: {condition.value}") from error
    return runner(parameters)
