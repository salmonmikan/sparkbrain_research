from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import pytest

from sparkbrain.v03_seed import (
    E0_GLOBAL,
    E1_ORACLE_ENTITY,
    EntityBinding,
    EvidenceAuditRow,
    EvidenceLedger,
    EvidenceRecord,
    PerceptualSpark,
    SlotMetricRow,
    bind_entity,
    derive_binding_id,
    derive_evidence_id,
    permutation_invariant_slot_metrics,
)


def record(
    evidence_id: str,
    *,
    polarity: str = "support",
    correlation_group: str | None = None,
    parents: tuple[str, ...] = (),
    spark_id: str = "spark-1",
    entity_key: str = "object-a",
    time: float = 0.0,
) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        source_id="source-primary",
        entity_key=entity_key,
        hypothesis_id="state-left",
        time=time,
        polarity=polarity,
        strength=1.0,
        correlation_group=correlation_group,
        parent_evidence_ids=parents,
        parent_spark_ids=(spark_id,),
        metadata={"fixture": "c13"},
    )


def ledger_with_lineage(*spark_ids: str) -> EvidenceLedger:
    ledger = EvidenceLedger()
    for spark_id in spark_ids or ("spark-1",):
        sample_id = f"sample:{spark_id}"
        ledger.register_sample(sample_id)
        ledger.register_spark(spark_id, (sample_id,))
    return ledger


def spark(*, slot: str | None = "object-a") -> PerceptualSpark:
    return PerceptualSpark(
        spark_id="spark-1",
        feature_id="symbolic:state",
        time=0.0,
        activation=1.0,
        salience=1.0,
        prediction_error=1.0,
        threshold=0.5,
        evidence_id="spark-evidence-1",
        source_id="source-primary",
        entity_slot=slot,
        parents=("sample:spark-1",),
    )


def test_strict_contract_round_trips_and_identity_derivations() -> None:
    item = record("ev-1")
    assert EvidenceRecord.from_canonical_json(item.to_canonical_json()) == item
    with pytest.raises(ValueError):
        EvidenceRecord.from_canonical_json(item.to_canonical_json() + " ")

    binding = bind_entity(spark(), condition_id=E1_ORACLE_ENTITY, entity_hint="hint-a")
    assert EntityBinding.from_canonical_json(binding.to_canonical_json()) == binding
    assert binding.binding_id == derive_binding_id(
        parent_spark_id="spark-1",
        entity_hint="hint-a",
        entity_slot="object-a",
        assignment_status="assigned",
    )
    first = derive_evidence_id(
        spark_evidence_id="spark-evidence-1",
        hypothesis_id="state-left",
        polarity="support",
    )
    second = derive_evidence_id(
        spark_evidence_id="spark-evidence-1",
        hypothesis_id="state-left",
        polarity="contradict",
    )
    assert first.startswith("ev-") and len(first) == 67 and first != second


@pytest.mark.parametrize(
    "mutation",
    [
        {"polarity": "contradict"},
        {"correlation_group": "cg:changed"},
        {"parent_evidence_ids": ("ev-parent",)},
        {"time": 1.0},
        {"strength": 2.0},
        {"metadata": {"fixture": "changed"}},
        {"source_id": "source-changed"},
        {"entity_key": "object-b"},
        {"hypothesis_id": "state-right"},
        {"parent_spark_ids": ("spark-changed",)},
    ],
)
def test_same_id_payload_mutations_are_rejected_atomically(
    mutation: dict[str, object],
) -> None:
    ledger = ledger_with_lineage()
    original = record("ev-1")
    ledger.add(original)
    state_before = ledger.active_state_hash()
    audit_before = ledger.audit_chain_hash()
    with pytest.raises(ValueError):
        ledger.add(replace(original, **mutation), delivered_at=2.0)
    assert ledger.resolve("ev-1") == original
    assert ledger.active_state_hash() == state_before
    assert ledger.audit_chain_hash() != audit_before
    assert ledger.audit_rows()[-1].action == "rejection"


def test_late_exact_redelivery_is_a_complete_no_op_except_audit() -> None:
    ledger = ledger_with_lineage()
    item = record("ev-1")
    ledger.add(item)
    state_before = ledger.active_state_hash()
    summary_before = ledger.summary("state-left", object_key="object-a", now=50.0)
    audit_before = ledger.audit_chain_hash()
    ledger.add(item, delivered_at=50.0)
    assert ledger.resolve("ev-1").to_canonical_json() == item.to_canonical_json()
    assert ledger.summary("state-left", object_key="object-a", now=50.0) == summary_before
    assert ledger.active_state_hash() == state_before
    assert ledger.audit_chain_hash() != audit_before
    assert ledger.duplicate_deliveries == {"ev-1": 1}


def test_invalid_payload_rejection_hash_uses_only_deterministic_envelope() -> None:
    attempted = {"evidence_id": "ev-invalid", "metadata": {"bad": {1, 2}}}
    payload_hashes = []
    for _ in range(2):
        ledger = EvidenceLedger()
        state_before = ledger.active_state_hash()
        with pytest.raises(ValueError):
            ledger.add(attempted)
        audit = ledger.audit_rows()[-1]
        payload_hashes.append(audit.payload_hash)
        assert audit.action == "rejection"
        assert audit.active_state_hash_before == state_before
        assert audit.active_state_hash_after == state_before
        assert ledger.active_state_hash() == state_before
    assert payload_hashes[0] == payload_hashes[1]


def test_legacy_unknown_parent_rejection_changes_only_audit() -> None:
    from sparkbrain.v03_seed import EvidenceContribution

    ledger = EvidenceLedger()
    before = json.loads(ledger.serialize_state())
    with pytest.raises(ValueError, match="unknown parent evidence"):
        ledger.add(
            EvidenceContribution(
                "legacy-child",
                "legacy-source",
                "state-left",
                0.0,
                support=1.0,
                parent_ids=("missing-parent",),
            )
        )
    after = json.loads(ledger.serialize_state())
    for key in (
        "active",
        "duplicate_deliveries",
        "records",
        "sample_ids",
        "spark_to_samples",
    ):
        assert after[key] == before[key]
    assert len(after["audit"]) == len(before["audit"]) + 1


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("evidence_id", 1),
        ("evidence_id", "   "),
        ("source_id", 1),
        ("source_id", "\t"),
        ("entity_key", 1),
        ("entity_key", " "),
        ("hypothesis_id", 1),
        ("hypothesis_id", "\n"),
    ],
)
def test_evidence_identity_fields_require_nonblank_strings(
    field: str, invalid: object
) -> None:
    with pytest.raises(ValueError):
        replace(record("ev-1"), **{field: invalid}).validate()


def test_unknown_self_and_cycle_lineage_fail_closed() -> None:
    ledger = ledger_with_lineage()
    with pytest.raises(ValueError, match="unknown parent evidence"):
        ledger.add(record("ev-child", parents=("ev-missing",)))
    with pytest.raises(ValueError, match="cite itself"):
        ledger.add(record("ev-self", parents=("ev-self",)))

    ledger.add(record("ev-a"))
    ledger.add(record("ev-b"))
    state = json.loads(ledger.serialize_state())
    state["records"]["ev-a"]["parent_evidence_ids"] = ["ev-b"]
    state["records"]["ev-b"]["parent_evidence_ids"] = ["ev-a"]
    tampered = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with pytest.raises(ValueError, match="invalid EvidenceLedger state"):
        EvidenceLedger.from_serialized_state(tampered)


def test_transitive_deactivate_restore_preserves_descendants_and_fixed_snapshot() -> None:
    ledger = ledger_with_lineage("spark-1", "spark-2", "spark-3")
    ancestor = record("ev-a", spark_id="spark-1")
    child = record("ev-b", parents=("ev-a",), spark_id="spark-2")
    grandchild = record("ev-c", parents=("ev-b",), spark_id="spark-3")
    for item in (ancestor, child, grandchild):
        ledger.add(item)
    descendant_bytes = tuple(
        ledger.resolve(key).to_canonical_json() for key in ("ev-b", "ev-c")
    )
    state_before = ledger.active_state_hash()
    summary_before = ledger.summary("state-left", object_key="object-a", now=10.0)
    audit_before = ledger.audit_chain_hash()

    ledger.deactivate("ev-a", at_time=10.0)
    assert ledger.rows() == ()
    assert tuple(
        ledger.resolve(key).to_canonical_json() for key in ("ev-b", "ev-c")
    ) == descendant_bytes
    ledger.restore("ev-a", at_time=10.0)

    assert ledger.active_state_hash() == state_before
    assert ledger.summary("state-left", object_key="object-a", now=10.0) == summary_before
    assert ledger.audit_chain_hash() not in {audit_before, "0" * 64}
    assert tuple(
        ledger.resolve(key).to_canonical_json() for key in ("ev-b", "ev-c")
    ) == descendant_bytes


def test_neutral_is_traceable_but_excluded_from_summary_votes() -> None:
    ledger = ledger_with_lineage()
    neutral = record("ev-neutral", polarity="neutral")
    ledger.add(neutral)
    summary = ledger.summary("state-left", object_key="object-a", now=0.0)
    assert ledger.resolve("ev-neutral") == neutral
    assert summary.effective_support == summary.effective_contradiction == 0.0
    assert summary.support_ids == summary.contradiction_ids == ()


def test_audit_rows_have_exact_fields_and_strict_hash_chain_round_trip() -> None:
    ledger = ledger_with_lineage()
    ledger.add(record("ev-1"))
    ledger.add(record("ev-1"), delivered_at=1.0)
    expected = {
        "action",
        "active_state_hash_after",
        "active_state_hash_before",
        "after_active",
        "audit_hash",
        "audit_id",
        "before_active",
        "branch_id",
        "event_time",
        "evidence_id",
        "payload_hash",
        "previous_audit_hash",
        "reason",
        "schema_version",
        "sequence",
    }
    previous = "0" * 64
    for row in ledger.audit_rows():
        assert set(json.loads(row.to_canonical_json())) == expected
        assert EvidenceAuditRow.from_canonical_json(row.to_canonical_json()) == row
        assert row.previous_audit_hash == previous
        previous = row.audit_hash
    restored = EvidenceLedger.from_serialized_state(ledger.serialize_state())
    assert restored.serialize_state() == ledger.serialize_state()


def test_serialized_record_key_must_equal_nested_evidence_id() -> None:
    ledger = ledger_with_lineage()
    ledger.add(record("ev-1"))
    state = json.loads(ledger.serialize_state())
    state["records"]["ev-other"] = state["records"].pop("ev-1")
    state["active"]["ev-other"] = state["active"].pop("ev-1")
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with pytest.raises(ValueError, match="invalid EvidenceLedger state"):
        EvidenceLedger.from_serialized_state(payload)


def test_rehashed_semantic_audit_tamper_is_rejected() -> None:
    ledger = ledger_with_lineage()
    ledger.add(record("ev-1"))
    ledger.deactivate("ev-1", at_time=1.0)
    state = json.loads(ledger.serialize_state())
    audit = state["audit"][-1]
    audit["before_active"] = False
    unsigned = {key: value for key, value in audit.items() if key != "audit_hash"}
    audit["audit_hash"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with pytest.raises(ValueError, match="invalid EvidenceLedger state"):
        EvidenceLedger.from_serialized_state(payload)


def test_binding_conditions_are_separate_and_e2_is_rejected() -> None:
    percept = spark()
    global_binding = bind_entity(
        percept, condition_id=E0_GLOBAL, entity_hint="object-a"
    )
    oracle_binding = bind_entity(
        percept, condition_id=E1_ORACLE_ENTITY, entity_hint="object-a"
    )
    assert global_binding.entity_key == "__global__"
    assert oracle_binding.entity_key == "object-a"
    with pytest.raises(ValueError):
        bind_entity(percept, condition_id="E2_learned", entity_hint="object-a")
    with pytest.raises(ValueError):
        bind_entity(spark(slot=None), condition_id=E1_ORACLE_ENTITY, entity_hint=None)


def test_slot_metrics_are_optimal_rectangular_and_pure_rename_invariant() -> None:
    rows = [
        SlotMetricRow(0, "slot-x", "object-a", "assigned"),
        SlotMetricRow(1, "slot-y", "object-b", "assigned"),
        SlotMetricRow(2, "slot-x", "object-a", "assigned"),
        SlotMetricRow(3, None, "object-c", "unassigned"),
        SlotMetricRow(4, None, "object-c", "uncertain"),
    ]
    renamed = [
        replace(
            row,
            predicted_slot={"slot-x": "renamed-z", "slot-y": "renamed-a"}.get(
                row.predicted_slot
            ),
        )
        if row.assignment_status == "assigned"
        else row
        for row in rows
    ]
    metrics = permutation_invariant_slot_metrics(rows)
    renamed_metrics = permutation_invariant_slot_metrics(renamed)
    invariant_keys = set(metrics) - {"matching"}
    assert {key: metrics[key] for key in invariant_keys} == {
        key: renamed_metrics[key] for key in invariant_keys
    }
    assert metrics["matched_accuracy"] == 1.0
    assert metrics["assigned_coverage"] == 0.6
    assert metrics["unassigned_rate"] == metrics["uncertain_rate"] == 0.2
