"""Construction-only MD-002 guards; no A01/N1/N3 capability execution."""

from __future__ import annotations

from dataclasses import replace

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
    post_state = post or pre
    evidence_hash = h(evidence)
    competition_hash = h(f"competition:{execution_id}")
    output_hash = h(f"output:{execution_id}")
    trace = (
        {
            "type": "md002-arm-record",
            "execution_id": execution_id,
            "pre_attribution": pre.state_dict(),
            "post_attribution": post_state.state_dict(),
            "admissible_external_evidence_sha256": evidence_hash,
            "competition_sha256": competition_hash,
            "output_sha256": output_hash,
        },
    )
    return ExecutedArmRecord(
        execution_id=execution_id,
        pre_attribution=pre,
        post_attribution=post_state,
        admissible_external_evidence_sha256=evidence_hash,
        competition_sha256=competition_hash,
        output_sha256=output_hash,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
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


def test_p3_requires_trace_bound_third_arm_with_only_donor_r_and_post_l_update():
    baseline_pre = state(address="baseline-r")
    donor_pre = state(address="donor-r")
    transplant_pre = state(address="donor-r")
    transplant_post = state(local="updated-l", address="donor-r")
    baseline = arm("baseline", baseline_pre)
    donor = arm("donor", donor_pre)
    transplanted = arm("transplant", transplant_pre, post=transplant_post)
    ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_donor_execution_substitution_even_if_id_is_relabelled():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    relabelled = replace(donor, execution_id="transplant")
    with pytest.raises(ValueError, match="retained runtime record"):
        ReturnAddressTransplant(baseline, donor, relabelled).validate()


def test_p3_rejects_donor_with_hidden_lfc_drift():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(local="donor-l", address="donor-r"))
    transplanted = arm(
        "transplant",
        state(address="donor-r"),
        post=state(local="updated-l", address="donor-r"),
    )
    with pytest.raises(ValueError, match="donor must match baseline"):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_hidden_lfc_drift_in_transplant():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm(
        "transplant",
        state(local="illicit", address="donor-r"),
        post=state(local="updated-l", address="donor-r"),
    )
    with pytest.raises(ValueError):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_missing_post_attribution_l_update():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm("transplant", state(address="donor-r"))
    with pytest.raises(ValueError, match="post-attribution L update"):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def test_p3_rejects_different_external_evidence_between_arms():
    baseline = arm("baseline", state(address="baseline-r"))
    donor = arm("donor", state(address="donor-r"))
    transplanted = arm(
        "transplant",
        state(address="donor-r"),
        post=state(local="updated-l", address="donor-r"),
        evidence="different",
    )
    with pytest.raises(ValueError, match="byte-identical"):
        ReturnAddressTransplant(baseline, donor, transplanted).validate()


def ancestry_record(boundary, before, after):
    payload = {
        "boundary_source_proposal_ids": boundary,
        "active_lineages_before": before,
        "active_lineages_after": after,
    }
    trace = (
        {
            "type": "md002-merged-ancestry-measurement",
            "measurement": payload,
        },
    )
    return MergedAncestryObservation(
        boundary_source_proposal_ids=boundary,
        active_lineages_before=before,
        active_lineages_after=after,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
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
    tampered = replace(record, measurement_record_sha256=h("not-the-record"))
    with pytest.raises(ValueError, match="measurement record digest"):
        tampered.validate()


def test_p4_rejects_measurement_not_present_in_retained_trace():
    record = ancestry_record(("p:a", "p:b"), ("p:a", "p:b"), ("p:a",))
    unrelated_trace = ({"type": "other", "measurement": record.measurement_payload()},)
    unbound = replace(
        record,
        runtime_trace=unrelated_trace,
        runtime_trace_sha256=canonical_sha256(unrelated_trace),
    )
    with pytest.raises(ValueError, match="not bound to the retained runtime trace"):
        unbound.validate()


def test_p5_binds_identical_a01_n1_n3_evidence_without_claim():
    evidence = h("anonymous-evidence-stream")
    ComparatorEvidenceBinding(evidence, evidence, evidence).validate()


def test_p5_rejects_comparator_input_privilege():
    with pytest.raises(ValueError):
        ComparatorEvidenceBinding(h("a"), h("a"), h("different")).validate()


def counter_trace(samples):
    return tuple(
        {
            "type": "md002-counter-sample",
            "sample": sample.state_dict(),
        }
        for sample in samples
    )


def test_dynamic_metrics_are_parsed_from_bound_runtime_trace():
    samples = (
        DynamicCounterSample(10, False, 100, 200, 155, 16),
        DynamicCounterSample(11, False, 102, 203, 160, 32),
        DynamicCounterSample(12, True, 105, 207, 164, 24),
    )
    trace = counter_trace(samples)
    measured = MeasuredDynamicCounters(trace, canonical_sha256(trace))
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
    trace = counter_trace(samples)
    with pytest.raises(ValueError, match="trace digest"):
        MeasuredDynamicCounters(trace, h("fabricated-trace")).validate()

    with pytest.raises(ValueError, match="state update counter"):
        MeasuredDynamicCounters(trace, canonical_sha256(trace)).validate()


def test_execution_gate_cannot_be_authorized_by_caller_controlled_flags_or_payloads():
    with pytest.raises(PermissionError, match="artifact digest is not pinned"):
        MD002ExecutionGate().require_authorized()

    fake_review = b'{"approved":true}'
    fake_authority = b'{"approved":true}'
    with pytest.raises(PermissionError, match="artifact digest is not pinned"):
        MD002ExecutionGate(
            technical_review_artifact=fake_review,
            execution_authority_artifact=fake_authority,
        ).require_authorized()
