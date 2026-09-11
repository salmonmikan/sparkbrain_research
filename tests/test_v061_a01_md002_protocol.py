"""Construction-only MD-002 guards; no A01/N1/N3 capability execution."""

from __future__ import annotations

import pytest

from sparkbrain.v061_a01.md002_protocol import (
    ComparatorEvidenceBinding,
    DynamicCounterSample,
    ExecutedArmRecord,
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


def arm(execution_id: str, pre: StatePartitionSnapshot, *, post=None, evidence="evidence"):
    return ExecutedArmRecord(
        execution_id=execution_id,
        pre_attribution=pre,
        post_attribution=post or pre,
        admissible_external_evidence_sha256=h(evidence),
        competition_sha256=h(f"competition:{execution_id}"),
        output_sha256=h(f"output:{execution_id}"),
        runtime_trace_sha256=h(f"trace:{execution_id}"),
    )


def test_p2_changes_world_relation_while_all_pre_evidence_state_stays_matched():
    pair = WorldOnlyInterventionPair(
        control=state(),
        intervention=state(),
        control_world_relation_sha256=h("relation-a"),
        intervention_world_relation_sha256=h("relation-b"),
        admissible_external_evidence_sha256=h("external-evidence"),
    )
    pair.validate()


@pytest.mark.parametrize("field", ["local", "field", "consistency", "address"])
def test_p2_rejects_any_pre_evidence_state_drift(field):
    values = dict(local="l", field="f", consistency="c", address="r")
    values[field] = f"changed-{field}"
    pair = WorldOnlyInterventionPair(
        control=state(),
        intervention=state(**values),
        control_world_relation_sha256=h("relation-a"),
        intervention_world_relation_sha256=h("relation-b"),
        admissible_external_evidence_sha256=h("external-evidence"),
    )
    with pytest.raises(ValueError):
        pair.validate()


def test_p3_requires_independently_executed_third_arm_with_only_donor_r():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm(
        "donor",
        state(local="donor-l", field="donor-f", consistency="donor-c", address="donor-r"),
    )
    transplanted = arm("transplant", state(address="donor-r"))
    ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_donor_execution_substitution():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm("donor", state(address="donor-r"))
    with pytest.raises(ValueError, match="three independently identified"):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_hidden_lfc_drift():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm("transplant", state(local="illicit", address="donor-r"))
    with pytest.raises(ValueError):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_different_external_evidence_between_arms():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm("transplant", state(address="donor-r"), evidence="different")
    with pytest.raises(ValueError, match="byte-identical"):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def ancestry_record(boundary, before, after):
    payload = {
        "boundary_source_proposal_ids": boundary,
        "active_lineages_before": before,
        "active_lineages_after": after,
    }
    return MergedAncestryObservation(
        boundary_source_proposal_ids=boundary,
        active_lineages_before=before,
        active_lineages_after=after,
        runtime_trace_sha256=h("runtime-trace"),
        measurement_record_sha256=canonical_sha256(payload),
    )


def test_p4_requires_measured_plural_boundary_ancestry_to_continue():
    ancestry_record(
        ("p:a", "p:b"),
        ("p:a", "p:b", "p:c"),
        ("p:b", "p:c"),
    ).validate()


def test_p4_rejects_post_state_that_loses_all_source_ancestry():
    with pytest.raises(ValueError, match="lost all merged"):
        ancestry_record(
            ("p:a", "p:b"),
            ("p:a", "p:b", "p:c"),
            ("p:c",),
        ).validate()


def test_p4_rejects_unbound_lineage_or_tampered_measurement_digest():
    with pytest.raises(ValueError, match="unbound unrelated"):
        ancestry_record(
            ("p:a", "p:b"),
            ("p:a", "p:b"),
            ("p:a", "unrelated"),
        ).validate()

    record = ancestry_record(("p:a", "p:b"), ("p:a", "p:b"), ("p:a",))
    tampered = MergedAncestryObservation(
        record.boundary_source_proposal_ids,
        record.active_lineages_before,
        record.active_lineages_after,
        record.runtime_trace_sha256,
        h("not-the-record"),
    )
    with pytest.raises(ValueError, match="digest"):
        tampered.validate()


def test_p5_binds_identical_a01_n1_n3_evidence_without_claim():
    evidence = h("anonymous-evidence-stream")
    ComparatorEvidenceBinding(evidence, evidence, evidence).validate()


def test_p5_rejects_comparator_input_privilege():
    with pytest.raises(ValueError):
        ComparatorEvidenceBinding(h("a"), h("a"), h("different")).validate()


def test_dynamic_metrics_are_derived_from_bound_runtime_trace():
    samples = (
        DynamicCounterSample(10, False, 100, 200, 155, 16),
        DynamicCounterSample(11, False, 102, 203, 160, 32),
        DynamicCounterSample(12, True, 105, 207, 164, 24),
    )
    trace = canonical_sha256([sample.state_dict() for sample in samples])
    measured = MeasuredDynamicCounters(samples, trace)
    measured.validate()
    assert measured.external_effect_latency_steps == 2
    assert measured.state_update_count == 5
    assert measured.router_operation_count == 7
    assert measured.persistent_state_bytes == 164
    assert measured.peak_transient_state_bytes == 32


def test_dynamic_metrics_reject_tampered_or_nonmonotonic_trace():
    samples = (
        DynamicCounterSample(0, False, 2, 3, 10, 4),
        DynamicCounterSample(1, True, 1, 4, 10, 5),
    )
    with pytest.raises(ValueError, match="trace digest"):
        MeasuredDynamicCounters(samples, h("fabricated-trace")).validate()

    trace = canonical_sha256([sample.state_dict() for sample in samples])
    with pytest.raises(ValueError, match="state update counter"):
        MeasuredDynamicCounters(samples, trace).validate()


def test_execution_is_fail_closed_until_both_reviews_exist():
    with pytest.raises(PermissionError):
        MD002ExecutionGate().require_authorized()
    with pytest.raises(PermissionError):
        MD002ExecutionGate(independent_technical_review=True).require_authorized()
    MD002ExecutionGate(
        independent_technical_review=True,
        execution_authority=True,
    ).require_authorized()
