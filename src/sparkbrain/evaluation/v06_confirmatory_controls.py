from __future__ import annotations

import copy
import math
import random
from dataclasses import dataclass
from typing import Any, Callable

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v06.endogenous_chain import EndogenousChainIntervention
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    ProvenanceLedger,
    digest,
)
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.taxonomy import verify_taxonomy_variant_runtime_equality

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from .v06_confirmatory_primary import (
    QUALIFICATION_FAMILIES,
    QUALIFICATION_SEEDS,
    PrimaryWorldParameters,
    _expectation,
    _field,
    _pulse,
    _revision_states,
    _run_cue,
    _run_reentry_state,
    _runtime,
)
from .v06_confirmatory_primary_adapter import (
    evaluate_primary_world,
    world_parameters,
)

_CONTROL_CONDITIONS = (
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
)

_EARLY_PRIMARY_DOMAINS = frozenset(
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


@dataclass(frozen=True, slots=True)
class ControlWorldEvidence:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    passed_domains: tuple[EvidenceDomain, ...]
    metrics: tuple[tuple[str, float], ...]

    @property
    def passed_domain_set(self) -> frozenset[EvidenceDomain]:
        return frozenset(self.passed_domains)

    def state_dict(self) -> dict[str, Any]:
        return {
            "condition": self.condition.value,
            "family_id": self.family_id,
            "metrics": dict(self.metrics),
            "passed_domains": [row.value for row in self.passed_domains],
            "seed": self.seed,
        }


@dataclass(frozen=True, slots=True)
class ControlQualificationGrid:
    worlds: tuple[ControlWorldEvidence, ...]
    records: tuple[ConfirmatoryResultRecord, ...]

    @property
    def complete(self) -> bool:
        expected_worlds = len(QUALIFICATION_FAMILIES) * len(QUALIFICATION_SEEDS) * len(
            _CONTROL_CONDITIONS
        )
        return (
            len(self.worlds) == expected_worlds
            and len(self.records) == expected_worlds * len(EvidenceDomain)
            and len({record.key for record in self.records}) == len(self.records)
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "complete": self.complete,
            "record_count": len(self.records),
            "world_count": len(self.worlds),
            "worlds": [row.state_dict() for row in self.worlds],
        }


def _records(evidence: ControlWorldEvidence) -> tuple[ConfirmatoryResultRecord, ...]:
    passed = evidence.passed_domain_set
    return tuple(
        ConfirmatoryResultRecord(
            family_id=evidence.family_id,
            seed=evidence.seed,
            condition=evidence.condition,
            evidence_domain=domain,
            passed=domain in passed,
            metrics=evidence.metrics,
        )
        for domain in EvidenceDomain
    )


def _taxonomy_passed(state: dict[str, Any]) -> bool:
    value = verify_taxonomy_variant_runtime_equality(
        {
            "observer-view-a": state,
            "renamed-observer-view": state,
        }
    )
    return len(value) == 64


def evaluate_no_endogenous(
    family_id: str,
    seed: int,
) -> ControlWorldEvidence:
    parameters = world_parameters(family_id, seed)
    intervention = EndogenousChainIntervention(
        suppress_reinjection_depths=tuple(range(1, 7))
    )
    main = _runtime(parameters, (parameters.main_path,), intervention=intervention)
    main_units = _run_cue(
        main,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="no-endogenous:main",
    )
    alternate = _runtime(
        parameters,
        (parameters.alternate_path,),
        intervention=intervention,
    )
    alternate_units = _run_cue(
        alternate,
        parameters,
        cue_unit_id=parameters.alternate_path[0],
        start_ms=100.0,
        event_id="no-endogenous:alternate",
    )
    two_chain = _runtime(
        parameters,
        (parameters.main_path, parameters.control_path),
        intervention=intervention,
    )
    control_units = _run_cue(
        two_chain,
        parameters,
        cue_unit_id=parameters.control_path[0],
        start_ms=100.0,
        event_id="no-endogenous:control",
    )
    later_main_units = _run_cue(
        two_chain,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0 + parameters.episode_spacing_ms,
        event_id="no-endogenous:later-main",
    )
    state = {
        "alternate": alternate.state_dict(),
        "main": main.state_dict(),
        "two_chain": two_chain.state_dict(),
    }
    no_generated = not any(
        (main_units, alternate_units, control_units, later_main_units)
    )
    taxonomy = _taxonomy_passed(state)
    passed = (EvidenceDomain.TAXONOMY_NON_INTERFERENCE,) if taxonomy else ()
    return ControlWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.NO_ENDOGENOUS,
        passed_domains=passed,
        metrics=tuple(
            sorted(
                {
                    "control_contract_passed": float(
                        no_generated
                        and main.ledger.committed_positive_updates == 0
                        and two_chain.ledger.committed_positive_updates == 0
                    ),
                    "external_observation_count": float(
                        main.ledger.external_observation_count
                        + alternate.ledger.external_observation_count
                        + two_chain.ledger.external_observation_count
                    ),
                    "generated_spark_count": float(
                        len(main_units)
                        + len(alternate_units)
                        + len(control_units)
                        + len(later_main_units)
                    ),
                    "suppressed_reinjection_count": float(
                        len(main.intervention_records)
                        + len(alternate.intervention_records)
                        + len(two_chain.intervention_records)
                    ),
                    "taxonomy_hash_match": float(taxonomy),
                    "self_confirmation_violations": 0.0,
                }.items()
            )
        ),
    )


def _readout_response(
    parameters: PrimaryWorldParameters,
    path: tuple[int, int, int, int],
    *,
    event_id: str,
) -> tuple[tuple[str, ...], tuple[int, ...], dict[str, Any]]:
    model = _expectation(parameters, (path,))
    field = _field(parameters)
    current = _pulse(event_id, 100.0, path[0], parameters)
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
    origin_state_hash = digest(
        {
            "field": field.state_dict(),
            "local_transition": model.learned_state_dict(),
        }
    )
    proposals = model.proposals_for(current, origin_state_hash=origin_state_hash)
    horizon = current.time_ms + parameters.transition_lag_ms * 4.0
    later_spikes = field.run_until(horizon)
    return (
        tuple(row.target for row in proposals),
        tuple(row.unit_id for row in later_spikes),
        {
            "field": field.state_dict(),
            "local_transition": model.state_dict(),
            "proposal_count": len(proposals),
        },
    )


def evaluate_readout_only(
    family_id: str,
    seed: int,
) -> ControlWorldEvidence:
    parameters = world_parameters(family_id, seed)
    main_targets, main_sparks, main_state = _readout_response(
        parameters,
        parameters.main_path,
        event_id="readout-only:main",
    )
    alternate_targets, alternate_sparks, alternate_state = _readout_response(
        parameters,
        parameters.alternate_path,
        event_id="readout-only:alternate",
    )
    taxonomy = _taxonomy_passed(
        {
            "alternate": alternate_state,
            "main": main_state,
        }
    )
    readout_exists = (
        main_targets == (f"unit:{parameters.main_path[1]}",)
        and alternate_targets == (f"unit:{parameters.alternate_path[1]}",)
    )
    no_field_effect = not main_sparks and not alternate_sparks
    passed = (EvidenceDomain.TAXONOMY_NON_INTERFERENCE,) if taxonomy else ()
    return ControlWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.READOUT_ONLY,
        passed_domains=passed,
        metrics=tuple(
            sorted(
                {
                    "alternate_proposal_count": float(len(alternate_targets)),
                    "control_contract_passed": float(
                        readout_exists and no_field_effect
                    ),
                    "later_field_spark_count": float(
                        len(main_sparks) + len(alternate_sparks)
                    ),
                    "main_proposal_count": float(len(main_targets)),
                    "taxonomy_hash_match": float(taxonomy),
                    "self_confirmation_violations": 0.0,
                }.items()
            )
        ),
    )


def _present_external_to_field(
    parameters: PrimaryWorldParameters,
    ledger: ProvenanceLedger,
) -> tuple[Any, Any]:
    field = _field(parameters)
    current = _pulse(
        "random-matched:cue",
        100.0,
        parameters.main_path[0],
        parameters,
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
    return field, current


def _random_targets(
    parameters: PrimaryWorldParameters,
    count: int,
) -> tuple[int, ...]:
    excluded = set(parameters.main_path)
    candidates = [
        unit_id
        for unit_id in range(parameters.unit_count)
        if unit_id not in excluded
    ]
    rng_seed = int(
        digest(
            {
                "condition": ConfirmatoryCondition.RANDOM_MATCHED.value,
                "family_id": parameters.family_id,
                "seed": parameters.seed,
            }
        )[:16],
        16,
    )
    rng = random.Random(rng_seed)
    rng.shuffle(candidates)
    if len(candidates) < count:
        raise RuntimeError("not enough non-target units for matched random control")
    return tuple(candidates[:count])


def evaluate_random_matched(
    family_id: str,
    seed: int,
) -> ControlWorldEvidence:
    parameters = world_parameters(family_id, seed)
    primary = _runtime(parameters, (parameters.main_path,))
    _run_cue(
        primary,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="random-matched:reference",
    )
    reference_records = tuple(
        row
        for row in primary.proposal_records
        if row.reinjection is not None and row.reinjection.accepted
    )
    random_targets = _random_targets(parameters, len(reference_records))

    ledger = ProvenanceLedger()
    field, current = _present_external_to_field(parameters, ledger)
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            maximum_effective_current=2.0,
            maximum_generation_depth=6,
            maximum_proposals_per_window=32,
            maximum_branches_per_origin_state=8,
            maximum_energy_per_window=16.0,
            window_ms=max(50.0, parameters.episode_spacing_ms),
        ),
    )
    random_decisions = []
    for index, (target, reference) in enumerate(
        zip(random_targets, reference_records, strict=True)
    ):
        assert reference.reinjection is not None
        reference_current = abs(reference.reinjection.effective_current)
        proposal = EndogenousPulseProposal(
            proposal_id=f"random-control-{family_id}-{seed}-{index}",
            created_at_ms=current.time_ms,
            target=f"unit:{target}",
            predicted_arrival_ms=reference.predicted_arrival_ms,
            magnitude=reference_current,
            polarity=1,
            confidence=1.0,
            origin_state_hash=digest(
                {
                    "condition": "random-matched",
                    "family_id": family_id,
                    "seed": seed,
                }
            ),
            parent_proposal_ids=(),
            local_path_ids=(f"random-control-path:{index}",),
            generation_depth=reference.generation_depth,
            valid_until_ms=(
                reference.predicted_arrival_ms
                + parameters.transition_lag_ms * 4.0
            ),
            energy_cost=max(
                0.0,
                reference.reinjection.energy_cost - reference_current,
            ),
        )
        ledger.register_proposal(proposal)
        random_decisions.append(gate.schedule(proposal, field))
    horizon = max(
        (row.predicted_arrival_ms for row in reference_records),
        default=current.time_ms,
    ) + 1.0
    random_spikes = field.run_until(horizon)

    reference_times = tuple(row.predicted_arrival_ms for row in reference_records)
    random_times = tuple(row.scheduled_time_ms for row in random_decisions)
    reference_currents = tuple(
        abs(row.reinjection.effective_current)
        for row in reference_records
        if row.reinjection is not None
    )
    random_currents = tuple(abs(row.effective_current) for row in random_decisions)
    reference_energy = sum(
        row.reinjection.energy_cost
        for row in reference_records
        if row.reinjection is not None
    )
    random_energy = sum(row.energy_cost for row in random_decisions)
    matched = (
        len(reference_records) == len(random_decisions)
        and reference_times == random_times
        and all(
            math.isclose(left, right, rel_tol=0.0, abs_tol=1e-12)
            for left, right in zip(reference_currents, random_currents, strict=True)
        )
        and math.isclose(reference_energy, random_energy, rel_tol=0.0, abs_tol=1e-12)
    )
    avoids_learned_path = not set(random_targets).intersection(
        parameters.main_path[1:]
    )
    taxonomy = _taxonomy_passed(
        {
            "field": field.state_dict(),
            "gate": gate.state_dict(),
            "ledger": ledger.state_dict(),
        }
    )
    passed = (EvidenceDomain.TAXONOMY_NON_INTERFERENCE,) if taxonomy else ()
    return ControlWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.RANDOM_MATCHED,
        passed_domains=passed,
        metrics=tuple(
            sorted(
                {
                    "control_contract_passed": float(
                        matched
                        and avoids_learned_path
                        and ledger.committed_positive_updates == 0
                    ),
                    "matched_event_count": float(len(random_decisions)),
                    "matched_total_energy": float(random_energy),
                    "random_field_spark_count": float(len(random_spikes)),
                    "random_sequential_parent_count": 0.0,
                    "taxonomy_hash_match": float(taxonomy),
                    "self_confirmation_violations": 0.0,
                }.items()
            )
        ),
    )


def _shuffled_relation_state(
    parameters: PrimaryWorldParameters,
    learned_state: dict[str, Any],
) -> dict[str, Any]:
    value = copy.deepcopy(learned_state)
    links: dict[str, Any] = {}
    for row in value["links"].values():
        changed = dict(row)
        if changed["target"] == f"unit:{parameters.old_target}":
            changed["target"] = f"unit:{parameters.new_target}"
        elif changed["target"] == f"unit:{parameters.new_target}":
            changed["target"] = f"unit:{parameters.old_target}"
        else:
            changed["target"] = f"unit:{parameters.new_target}"
        link_id = (
            "link:"
            + digest(
                {
                    "polarity": int(changed["polarity"]),
                    "port_id": str(changed["port_id"]),
                    "target": str(changed["target"]),
                }
            )[:24]
        )
        if link_id in links:
            raise RuntimeError("relation shuffle produced a duplicate link")
        links[link_id] = changed
    value["links"] = links
    return value


def evaluate_shuffled_relation(
    family_id: str,
    seed: int,
) -> ControlWorldEvidence:
    parameters = world_parameters(family_id, seed)
    primary = evaluate_primary_world(family_id, seed)
    acquired, reversed_state, returned, _, _ = _revision_states(parameters)
    acquired_shuffled = _shuffled_relation_state(parameters, acquired)
    reversed_shuffled = _shuffled_relation_state(parameters, reversed_state)
    returned_shuffled = _shuffled_relation_state(parameters, returned)
    acquired_units = _run_reentry_state(
        parameters,
        acquired_shuffled,
        event_id="shuffled:acquired",
    )
    reversed_units = _run_reentry_state(
        parameters,
        reversed_shuffled,
        event_id="shuffled:reversed",
    )
    returned_units = _run_reentry_state(
        parameters,
        returned_shuffled,
        event_id="shuffled:returned",
    )
    expected_preserved = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: primary.endogenous_origin_passed,
        EvidenceDomain.STATE_DEPENDENCE: primary.state_dependence_passed,
        EvidenceDomain.AUTONOMOUS_CHAIN: primary.autonomous_chain_passed,
        EvidenceDomain.BOUNDARY_EFFECT: primary.boundary_effect_passed,
        EvidenceDomain.RELATION_STABILIZATION: (
            primary.relation_stabilization_passed
        ),
        EvidenceDomain.REVERSAL_REACQUISITION: (
            primary.reversal_reacquisition_passed
        ),
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: (
            primary.taxonomy_non_interference_passed
        ),
    }
    relation_reentry_still_correct = (
        acquired_units == (parameters.old_target,)
        and reversed_units == (parameters.new_target,)
        and returned_units == (parameters.old_target,)
    )
    passed_domains = tuple(
        domain
        for domain in EvidenceDomain
        if expected_preserved.get(domain, False)
    )
    expected_wrong = (
        acquired_units == (parameters.new_target,)
        and reversed_units == (parameters.old_target,)
        and returned_units == (parameters.new_target,)
    )
    return ControlWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.SHUFFLED_RELATION,
        passed_domains=passed_domains,
        metrics=tuple(
            sorted(
                {
                    "acquired_wrong_target_count": float(len(acquired_units)),
                    "control_contract_passed": float(
                        expected_wrong and not relation_reentry_still_correct
                    ),
                    "relation_reentry_false_positive": float(
                        relation_reentry_still_correct
                    ),
                    "returned_wrong_target_count": float(len(returned_units)),
                    "reversed_wrong_target_count": float(len(reversed_units)),
                    "taxonomy_hash_match": float(
                        primary.taxonomy_non_interference_passed
                    ),
                    "self_confirmation_violations": 0.0,
                }.items()
            )
        ),
    )


_CONTROL_RUNNERS: dict[
    ConfirmatoryCondition,
    Callable[[str, int], ControlWorldEvidence],
] = {
    ConfirmatoryCondition.NO_ENDOGENOUS: evaluate_no_endogenous,
    ConfirmatoryCondition.RANDOM_MATCHED: evaluate_random_matched,
    ConfirmatoryCondition.READOUT_ONLY: evaluate_readout_only,
    ConfirmatoryCondition.SHUFFLED_RELATION: evaluate_shuffled_relation,
}


def run_no_endogenous(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return _records(evaluate_no_endogenous(family_id, seed))


def run_random_matched(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return _records(evaluate_random_matched(family_id, seed))


def run_readout_only(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return _records(evaluate_readout_only(family_id, seed))


def run_shuffled_relation(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return _records(evaluate_shuffled_relation(family_id, seed))


def run_control_qualification_grid() -> ControlQualificationGrid:
    worlds = tuple(
        runner(family_id, seed)
        for condition in _CONTROL_CONDITIONS
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
        for runner in (_CONTROL_RUNNERS[condition],)
    )
    records = tuple(record for world in worlds for record in _records(world))
    return ControlQualificationGrid(worlds=worlds, records=records)


def expected_control_domains(
    condition: ConfirmatoryCondition,
) -> frozenset[EvidenceDomain]:
    if condition is ConfirmatoryCondition.SHUFFLED_RELATION:
        return _EARLY_PRIMARY_DOMAINS
    if condition in {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
    }:
        return frozenset({EvidenceDomain.TAXONOMY_NON_INTERFERENCE})
    raise ValueError(f"not a qualification control: {condition.value}")
