from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import ProvenanceLedger
from sparkbrain.v06.persistence_locus import (
    reset_anonymous_consistency,
    transplant_anonymous_consistency,
)

from .v06_relation_reentry_probe import (
    RelationReentryAssessment,
    RelationReentryCondition,
    _build_relation_state,
    _run_reentry,
)


@dataclass(frozen=True, slots=True)
class IsolatedRelationReentrySuite:
    acquisition: RelationReentryCondition
    reversal: RelationReentryCondition
    returned: RelationReentryCondition
    consistency_reset: RelationReentryCondition
    reversal_transplant: RelationReentryCondition
    no_reentry: RelationReentryCondition
    assessment: RelationReentryAssessment

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_isolated_relation_reentry_suite() -> IsolatedRelationReentrySuite:
    """Run each condition with an independent ledger and identical later Field.

    Independent ledgers ensure that trigger and proposal identities from one
    condition cannot affect another. The trained relation component itself is
    the only state transplanted into the transplant condition.
    """

    acquisition_targets = ("unit:8",) * 3
    reversal_targets = acquisition_targets + ("unit:9",) * 3
    returned_targets = reversal_targets + ("unit:8",) * 3

    acquisition = _run_reentry(
        condition_id="acquisition",
        relation_targets=acquisition_targets,
        consistency=_build_relation_state(acquisition_targets),
    )
    reversal = _run_reentry(
        condition_id="reversal",
        relation_targets=reversal_targets,
        consistency=_build_relation_state(reversal_targets),
    )
    returned = _run_reentry(
        condition_id="returned",
        relation_targets=returned_targets,
        consistency=_build_relation_state(returned_targets),
    )

    reset_source = _build_relation_state(acquisition_targets)
    reset_state = reset_anonymous_consistency(
        reset_source.ledger,
        config=reset_source.config,
    )
    consistency_reset = _run_reentry(
        condition_id="consistency-reset",
        relation_targets=acquisition_targets,
        consistency=reset_state,
    )

    transplant_source = _build_relation_state(reversal_targets)
    transplant_state = reset_anonymous_consistency(
        ProvenanceLedger(),
        config=transplant_source.config,
    )
    transplant_report = transplant_anonymous_consistency(
        transplant_source,
        transplant_state,
    )
    reversal_transplant = _run_reentry(
        condition_id="reversal-transplant",
        relation_targets=reversal_targets,
        consistency=transplant_state,
        transplant_report=transplant_report,
    )

    no_reentry = _run_reentry(
        condition_id="no-reentry",
        relation_targets=acquisition_targets,
        consistency=_build_relation_state(acquisition_targets),
        enable_reentry=False,
    )

    conditions = (
        acquisition,
        reversal,
        returned,
        consistency_reset,
        reversal_transplant,
        no_reentry,
    )
    initial_field_hashes = {row.field_state_hash_before for row in conditions}
    lowered = str([row.runtime_state for row in conditions]).lower()
    forbidden = (
        "assembly_id",
        "relation_type",
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "correct_action",
        "scalar_reward",
        "outcome_label",
        "functional_role",
        "meaning_state",
    )
    values = {
        "identical_later_field_state": len(initial_field_hashes) == 1,
        "acquisition_selects_unit_8": (
            acquisition.endogenous_field_units == (8,)
            and acquisition.boundary_port_ids == ("port:8",)
        ),
        "reversal_selects_unit_9": (
            reversal.endogenous_field_units == (9,)
            and reversal.boundary_port_ids == ("port:9",)
        ),
        "return_selects_unit_8": (
            returned.endogenous_field_units == (8,)
            and returned.boundary_port_ids == ("port:8",)
        ),
        "reversal_changes_later_field_trace": (
            acquisition.field_state_hash_after != reversal.field_state_hash_after
        ),
        "reversal_changes_boundary_trace": (
            acquisition.boundary_port_ids != reversal.boundary_port_ids
        ),
        "reset_removes_effect": (
            not consistency_reset.reentry_accepted
            and consistency_reset.endogenous_field_units == ()
            and consistency_reset.boundary_port_ids == ()
        ),
        "transplant_transfers_effect": (
            reversal_transplant.endogenous_field_units == (9,)
            and reversal_transplant.boundary_port_ids == ("port:9",)
            and reversal_transplant.transplant_report is not None
            and reversal_transplant.transplant_report.copied_link_count == 2
        ),
        "no_reentry_removes_effect": (
            not no_reentry.reentry_accepted
            and no_reentry.endogenous_field_units == ()
            and no_reentry.boundary_port_ids == ()
        ),
        "consistency_is_read_only": all(row.consistency_unchanged for row in conditions),
        "no_external_or_positive_update_leak": all(
            row.external_observation_delta == 0 and row.positive_update_delta == 0
            for row in conditions
        ),
        "runtime_taxonomy_free": not any(term in lowered for term in forbidden),
    }
    assessment = RelationReentryAssessment(
        **values,
        engineering_candidate=all(values.values()),
    )
    return IsolatedRelationReentrySuite(
        acquisition=acquisition,
        reversal=reversal,
        returned=returned,
        consistency_reset=consistency_reset,
        reversal_transplant=reversal_transplant,
        no_reentry=no_reentry,
        assessment=assessment,
    )
