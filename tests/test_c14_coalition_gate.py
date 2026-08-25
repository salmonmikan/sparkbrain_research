from __future__ import annotations

import math
from dataclasses import replace

import pytest

from sparkbrain.v03_seed import (
    CoalitionGate,
    EvidenceLedger,
    EvidenceRecord,
    V03ReferenceLoop,
    derive_evidence_id,
)
from sparkbrain.v03_seed import coalition as coalition_module
from sparkbrain.v03_seed.coalition import C14_BOUNDED_MODE


class NoopInterpreter:
    def interpret(self, spark: object) -> tuple[()]:
        return ()


def add_record(
    ledger: EvidenceLedger,
    role: str,
    *,
    hypothesis: str = "hypothesis-alpha",
    polarity: str = "support",
    strength: float = 1.0,
    source: str | None = None,
    group: str | None = None,
    time: float = 10.0,
) -> EvidenceRecord:
    sample_id = f"sample:{role}"
    spark_id = f"spark:{role}"
    ledger.register_sample(sample_id)
    ledger.register_spark(spark_id, (sample_id,))
    record = EvidenceRecord(
        evidence_id=derive_evidence_id(
            spark_evidence_id=f"spark-evidence:{role}",
            hypothesis_id=hypothesis,
            polarity=polarity,
        ),
        source_id=source or f"source:{role}",
        entity_key="object-a",
        hypothesis_id=hypothesis,
        time=time,
        polarity=polarity,
        strength=strength,
        correlation_group=group or f"group:{role}",
        parent_spark_ids=(spark_id,),
    )
    ledger.add(record)
    return record


def activations(alpha: float = 0.72, beta: float = 0.28) -> dict[tuple[str, str], float]:
    return {
        ("object-a", "hypothesis-alpha"): alpha,
        ("object-a", "hypothesis-beta"): beta,
    }


def settled(ledger: EvidenceLedger, *, now: float = 10.0):
    gate = CoalitionGate()
    gate.evaluate(activations(), ledger, now=now, mode=C14_BOUNDED_MODE)
    return gate.evaluate(activations(), ledger, now=now, mode=C14_BOUNDED_MODE)


def test_c14_scores_all_candidates_after_stability_update() -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "alpha-a", source="source-a", group="group-a")
    add_record(ledger, "alpha-b", source="source-b", group="group-b")
    gate = CoalitionGate()

    first = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    second = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)

    assert not first.ignited and first.reason == "insufficient_stability"
    assert second.ignited and second.belief_key == "hypothesis-alpha"
    assert [row.stability for row in second.coalitions] == [2, 2]
    top = second.coalitions[0]
    expected = 0.25 * 0.72 + 0.25 * (1.0 - math.exp(-2.0)) + 0.05 + 0.05 + 0.10 + 0.20
    assert top.score == pytest.approx(expected)
    assert top.score == pytest.approx(
        top.weighted_activation
        + top.weighted_support
        + top.weighted_source_diversity
        + top.weighted_group_diversity
        + top.weighted_stability
        + top.weighted_recency
        + top.weighted_contradiction
        + top.weighted_redundancy
    )


def test_equal_candidate_stability_produces_margin_reason() -> None:
    ledger = EvidenceLedger()
    for suffix, source, group in (("a", "source-a", "group-a"), ("b", "source-b", "group-b")):
        add_record(
            ledger,
            f"alpha-{suffix}",
            strength=0.2,
            source=source,
            group=group,
        )
    beta_strength = 0.7341427164006862
    for suffix, source, group in (("a", "source-c", "group-c"), ("b", "source-d", "group-d")):
        add_record(
            ledger,
            f"beta-{suffix}",
            hypothesis="hypothesis-beta",
            strength=beta_strength,
            source=source,
            group=group,
        )
    gate = CoalitionGate()
    gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    result = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    assert not result.ignited
    assert result.reason == "margin_below_threshold"
    assert result.coalitions[0].belief_key == "hypothesis-alpha"
    assert result.coalitions[0].score == pytest.approx(result.coalitions[1].score)
    assert [row.stability for row in result.coalitions] == [2, 2]


def test_nonfinite_rejection_is_atomic_for_c14_gate_state() -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "alpha-a")
    add_record(ledger, "alpha-b")
    gate = CoalitionGate()
    first = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    assert first.coalitions[0].stability == 1

    with pytest.raises(ValueError):
        gate.evaluate(activations(alpha=float("nan")), ledger, now=10.0, mode=C14_BOUNDED_MODE)

    second = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    assert second.coalitions[0].stability == 2


def test_actual_c14_evaluate_calls_side_effect_free_decision_helper(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "alpha-a")
    add_record(ledger, "alpha-b")
    gate = CoalitionGate()
    calls = []
    original = coalition_module.decide_c14

    def traced(coalitions):
        calls.append(coalitions)
        return original(coalitions)

    monkeypatch.setattr(coalition_module, "decide_c14", traced)
    gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    result = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    assert len(calls) == 2
    assert result == original(calls[-1])

    low = replace(calls[-1][0], score=0.54)
    high = replace(low, score=0.56)
    assert original((low,)).reason == "score_below_threshold"
    assert original((high,)).ignited


def test_reason_priority_checks_evidence_before_score() -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "alpha-only")
    gate = CoalitionGate()
    gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    result = gate.evaluate(activations(), ledger, now=10.0, mode=C14_BOUNDED_MODE)
    assert result.coalitions[0].score > 0.55
    assert result.reason == "insufficient_evidence"


def test_frozen_structural_contradiction_recency_and_score_reasons() -> None:
    same_source = EvidenceLedger()
    add_record(same_source, "same-source-a", source="source-a", group="group-a")
    add_record(same_source, "same-source-b", source="source-a", group="group-b")
    assert settled(same_source).reason == "insufficient_sources"

    correlated = EvidenceLedger()
    add_record(correlated, "correlated-a", source="source-a", group="group-a")
    add_record(correlated, "correlated-b", source="source-b", group="group-a")
    assert settled(correlated).reason == "insufficient_independent_groups"

    contradicted = EvidenceLedger()
    add_record(contradicted, "support-a", source="source-a", group="group-a")
    add_record(contradicted, "support-b", source="source-b", group="group-b")
    add_record(
        contradicted,
        "contradiction",
        polarity="contradict",
        strength=2.0,
        source="source-c",
        group="group-c",
    )
    assert settled(contradicted).reason == "excessive_contradiction"

    old = EvidenceLedger()
    add_record(old, "old-a", source="source-a", group="group-a", time=0.0)
    add_record(old, "old-b", source="source-b", group="group-b", time=0.0)
    assert settled(old, now=100.0).reason == "insufficient_recency"

    weak = EvidenceLedger()
    add_record(
        weak,
        "weak-a",
        source="source-a",
        group="group-a",
        strength=0.05,
        time=65.0,
    )
    add_record(
        weak,
        "weak-b",
        source="source-b",
        group="group-b",
        strength=0.05,
        time=65.0,
    )
    weak_result = settled(weak, now=100.0)
    assert weak_result.coalitions[0].normalized_recency >= 0.30
    assert weak_result.reason == "score_below_threshold"


def test_remove_and_exact_restore_recover_decision_and_terms() -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "necessary-a", source="source-a", group="group-a")
    removed_record = add_record(ledger, "necessary-b", source="source-b", group="group-b")
    baseline_hash = ledger.active_state_hash()
    baseline = settled(ledger)
    ledger.deactivate(removed_record.evidence_id, at_time=10.0)
    removed = settled(ledger)
    ledger.restore(removed_record.evidence_id, at_time=10.0)
    restored = settled(ledger)

    assert baseline.ignited
    assert removed.reason == "insufficient_evidence"
    assert ledger.active_state_hash() == baseline_hash
    assert restored == baseline


def test_settle_override_replaces_belief_activation_on_every_evaluation() -> None:
    ledger = EvidenceLedger()
    add_record(ledger, "alpha-a")
    add_record(ledger, "alpha-b")
    loop = V03ReferenceLoop(NoopInterpreter(), ledger=ledger)
    override = {"hypothesis-alpha": 0.72, "hypothesis-beta": 0.28}

    first = loop.settle(
        now=10.0,
        object_key="object-a",
        activation_overrides=override,
        gate_mode=C14_BOUNDED_MODE,
    )
    second = loop.settle(
        now=10.0,
        object_key="object-a",
        activation_overrides=override,
        gate_mode=C14_BOUNDED_MODE,
    )

    assert not first.ignited
    assert second.ignited
    assert [row.activation for row in first.coalitions] == [0.72, 0.28]
    assert [row.activation for row in second.coalitions] == [0.72, 0.28]
    alpha = next(
        row for row in loop.belief_field.ranked("object-a") if row.belief_key == "hypothesis-alpha"
    )
    assert alpha.activation > 0.0
    assert alpha.ignition_count == 1


def test_invalid_settle_input_does_not_register_candidates() -> None:
    loop = V03ReferenceLoop(NoopInterpreter(), ledger=EvidenceLedger())
    with pytest.raises(ValueError):
        loop.settle(
            now=float("nan"),
            object_key="object-a",
            activation_overrides={"hypothesis-alpha": 0.72, "hypothesis-beta": 0.28},
            gate_mode=C14_BOUNDED_MODE,
        )
    assert loop.belief_field.ranked("object-a") == ()


@pytest.mark.parametrize("mode", ["G0_probability_margin", "G1_no_coalition_ablation"])
def test_probability_controls_have_no_coalition_terms(mode: str) -> None:
    loop = V03ReferenceLoop(NoopInterpreter(), ledger=EvidenceLedger())
    result = loop.settle(
        now=10.0,
        object_key="object-a",
        activation_overrides={"hypothesis-alpha": 0.72, "hypothesis-beta": 0.28},
        gate_mode=mode,
    )
    assert result.ignited
    assert result.belief_key == "hypothesis-alpha"
    assert result.score == 0.72
    assert result.margin == pytest.approx(0.44)
    assert result.coalitions == ()
