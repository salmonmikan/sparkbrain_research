"""Construction-only MD-002 guards; no A01/N1/N3 capability execution."""

from __future__ import annotations

import pytest

from sparkbrain.v061_a01.md002_protocol import (
    ComparatorEvidenceBinding,
    MD002ExecutionGate,
    MeasuredDynamicCounters,
    MergedAncestryObservation,
    ReturnAddressTransplant,
    StatePartitionSnapshot,
    WorldOnlyInterventionPair,
    canonical_sha256,
)


def h(value: str) -> str:
    return canonical_sha256(value)


def state(*, local="l", field="f", consistency="c", address="r"):
    return StatePartitionSnapshot(h(local), h(field), h(consistency), h(address))


def test_p2_allows_only_world_relation_consistency_change():
    pair = WorldOnlyInterventionPair(
        control=state(consistency="world-a"),
        intervention=state(consistency="world-b"),
        control_world_relation_sha256=h("relation-a"),
        intervention_world_relation_sha256=h("relation-b"),
        admissible_external_evidence_sha256=h("external-evidence"),
    )
    pair.validate()


@pytest.mark.parametrize("field", ["local", "field", "address"])
def test_p2_rejects_nonworld_state_drift(field):
    values = dict(local="l", field="f", consistency="world-b", address="r")
    values[field] = f"changed-{field}"
    pair = WorldOnlyInterventionPair(
        control=state(consistency="world-a"),
        intervention=state(**values),
        control_world_relation_sha256=h("relation-a"),
        intervention_world_relation_sha256=h("relation-b"),
        admissible_external_evidence_sha256=h("external-evidence"),
    )
    with pytest.raises(ValueError):
        pair.validate()


def test_p3_requires_real_third_arm_with_only_donor_r():
    baseline = state(address="baseline-r")
    donor = state(local="donor-l", field="donor-f", consistency="donor-c", address="donor-r")
    transplanted = state(address="donor-r")
    ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_hidden_lfc_drift():
    baseline = state(address="baseline-r")
    donor = state(address="donor-r")
    transplanted = state(local="illicit", address="donor-r")
    with pytest.raises(ValueError):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p4_requires_measured_plural_boundary_ancestry():
    MergedAncestryObservation(
        boundary_source_proposal_ids=("p:a", "p:b"),
        active_lineages_before=("p:a", "p:b", "p:c"),
        active_lineages_after=("p:b", "p:c"),
        measured_from_runtime=True,
    ).validate()


def test_p4_rejects_supplied_or_singleton_ancestry():
    with pytest.raises(ValueError):
        MergedAncestryObservation(
            boundary_source_proposal_ids=("p:a",),
            active_lineages_before=("p:a",),
            active_lineages_after=("p:a",),
            measured_from_runtime=False,
        ).validate()


def test_p5_binds_identical_a01_n1_n3_evidence_without_claim():
    evidence = h("anonymous-evidence-stream")
    ComparatorEvidenceBinding(evidence, evidence, evidence).validate()


def test_p5_rejects_comparator_input_privilege():
    with pytest.raises(ValueError):
        ComparatorEvidenceBinding(h("a"), h("a"), h("different")).validate()


def test_dynamic_metrics_must_be_measured():
    MeasuredDynamicCounters(1, 2, 3, 155, 64, True).validate()
    with pytest.raises(ValueError):
        MeasuredDynamicCounters(1, 2, 3, 155, 64, False).validate()


def test_execution_is_fail_closed_until_both_reviews_exist():
    with pytest.raises(PermissionError):
        MD002ExecutionGate().require_authorized()
    with pytest.raises(PermissionError):
        MD002ExecutionGate(independent_technical_review=True).require_authorized()
    MD002ExecutionGate(
        independent_technical_review=True,
        execution_authority=True,
    ).require_authorized()
