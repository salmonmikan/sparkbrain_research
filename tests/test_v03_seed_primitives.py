from __future__ import annotations

import pytest

from sparkbrain.v03_seed import (
    AdaptiveSensoryField,
    CoalitionGate,
    CoalitionGateConfig,
    EvidenceContribution,
    EvidenceLedger,
    OnlineConceptFormer,
    SensorySample,
    compositional_text_features,
    sparse_cosine_similarity,
    symbolic_metadata_features,
    whole_string_hash_features,
)


def sample(index: int, value: float, *, feature: str = "tick") -> SensorySample:
    return SensorySample(
        sample_id=f"sample:{index}",
        time=float(index),
        source_id="sensor:a",
        modality="audio",
        values={feature: value},
    )


def test_repetition_is_suppressed_and_change_recovers_salience() -> None:
    field = AdaptiveSensoryField()
    counts = [len(field.observe(sample(index, 1.0))) for index in range(4)]
    changed = field.observe(sample(4, 0.0))
    assert counts[0] == 1
    assert sum(counts[1:]) < 3
    assert changed and changed[0].prediction_error > 0


def test_goal_bias_can_select_an_otherwise_quiet_feature() -> None:
    field = AdaptiveSensoryField()
    field.observe(sample(0, 1.0, feature="black_dot"))
    field.observe(sample(1, 1.0, feature="black_dot"))
    comparison = AdaptiveSensoryField.from_serialized_state(field.serialize_state())
    quiet = field.observe(sample(2, 0.4, feature="black_dot"))
    biased = comparison.observe(
        sample(2, 0.4, feature="black_dot"), goal_bias={"audio:black_dot": 2.0}
    )
    assert quiet == ()
    assert biased and biased[0].feature_id == "audio:black_dot"


def test_compositional_features_share_structure_across_small_rewording() -> None:
    first = set(compositional_text_features("The cat is on the table"))
    second = set(compositional_text_features("A cat is on that table"))
    unrelated = set(compositional_text_features("Rain changes the river"))
    assert len(first & second) > len(first & unrelated)


def test_symbolic_oracle_features_are_explicitly_structured() -> None:
    features = symbolic_metadata_features(
        {
            "symbolic_event": {
                "kind": "assert",
                "literal": {"predicate": "bird", "entity": "ada", "positive": True},
            }
        }
    )
    assert "sym:kind:assert" in features
    assert "sym:predicate:bird" in features
    with pytest.raises(ValueError):
        symbolic_metadata_features({})


def test_repeated_coactivation_forms_a_label_free_concept_candidate() -> None:
    former = OnlineConceptFormer()
    for time in range(4):
        former.observe({"vision:fur", "audio:meow", "touch:warm"}, time=float(time))
    candidates = former.candidates()
    assert candidates
    assert {"vision:fur", "audio:meow", "touch:warm"} <= set(candidates[0].members)
    assert candidates[0].reuse_count >= 1


def test_duplicate_evidence_id_is_not_an_independent_vote() -> None:
    ledger = EvidenceLedger()
    row = EvidenceContribution("e1", "vision", "cat", 0.0, support=1.0)
    ledger.add(row)
    ledger.add(row, delivered_at=1.0)
    summary = ledger.summary("cat", object_key=None, now=1.0)
    assert summary.unique_evidence_count == 1
    assert summary.independent_group_count == 1
    assert ledger.duplicate_deliveries["e1"] == 1


def test_correlated_variants_are_discounted_and_not_independent() -> None:
    ledger = EvidenceLedger()
    for index in range(3):
        ledger.add(
            EvidenceContribution(
                f"e{index}",
                f"sensor:{index}",
                "cat",
                0.0,
                support=1.0,
                correlation_group="same-camera-frame",
            )
        )
    summary = ledger.summary("cat", object_key=None, now=0.0)
    assert summary.source_count == 3
    assert summary.independent_group_count == 1
    assert summary.effective_support < 3.0
    assert summary.redundancy > 0


def test_coalition_requires_independent_evidence_and_stability() -> None:
    ledger = EvidenceLedger()
    gate = CoalitionGate(CoalitionGateConfig(ignition_threshold=1.2))
    ledger.add(EvidenceContribution("v1", "vision", "cat", 0.0, support=0.9))
    one_source = gate.evaluate({(None, "cat"): 0.7, (None, "dog"): 0.2}, ledger, now=0.0)
    assert not one_source.ignited
    assert one_source.reason in {"insufficient_sources", "insufficient_independent_groups"}

    ledger.add(EvidenceContribution("a1", "audio", "cat", 0.0, support=0.9))
    first = gate.evaluate({(None, "cat"): 0.7, (None, "dog"): 0.2}, ledger, now=1.0)
    second = gate.evaluate({(None, "cat"): 0.7, (None, "dog"): 0.2}, ledger, now=2.0)
    assert not first.ignited and first.reason == "insufficient_stability"
    assert second.ignited and second.belief_key == "cat"


def test_contradiction_can_block_ignition() -> None:
    ledger = EvidenceLedger()
    gate = CoalitionGate(CoalitionGateConfig(stability_steps=1))
    ledger.add(EvidenceContribution("v1", "vision", "cat", 0.0, support=0.8))
    ledger.add(EvidenceContribution("a1", "audio", "cat", 0.0, support=0.8))
    ledger.add(EvidenceContribution("x1", "touch", "cat", 0.0, contradiction=2.5))
    result = gate.evaluate({(None, "cat"): 0.7, (None, "toy"): 0.3}, ledger, now=0.0)
    assert not result.ignited


def test_entity_scoped_beliefs_do_not_cross_talk() -> None:
    from sparkbrain.v03_seed import PersistentBeliefField

    field = PersistentBeliefField()
    field.seed("object-a", "cat", activation=0.8)
    field.seed("object-b", "toy", activation=0.8)
    assert field.winner("object-a") == "cat"
    assert field.winner("object-b") == "toy"


def test_graph_cluster_alone_is_not_accepted_as_an_organ() -> None:
    from sparkbrain.v03_seed import OrganEvidence, assess_organ_candidate

    assessment = assess_organ_candidate(
        OrganEvidence(
            candidate_id="cluster-a",
            seed_consistency=3,
            structural_cohesion=0.9,
            functional_selectivity=0.4,
            held_out_reuse=0.3,
            targeted_impairment=0.01,
            matched_random_impairment=0.01,
            unrelated_collateral=0.0,
        )
    )
    assert not assessment.accepted
    assert "causal_necessity" in assessment.failed_gates


def test_reference_loop_ignites_only_after_independent_support_and_stability() -> None:
    from sparkbrain.v03_seed import EvidenceContribution, V03ReferenceLoop

    class Interpreter:
        def interpret(self, spark):
            belief = "cat" if spark.feature_id.endswith(("fur", "meow")) else "toy"
            yield EvidenceContribution(
                evidence_id=spark.evidence_id,
                source_id=spark.source_id,
                belief_key=belief,
                time=spark.time,
                support=0.9,
                object_key=spark.entity_slot,
                correlation_group=spark.correlation_group,
            )

    loop = V03ReferenceLoop(Interpreter())
    first = loop.process(
        SensorySample("vision-1", 0.0, "vision", "vision", {"fur": 1.0}, entity_hint="a")
    )
    second = loop.process(
        SensorySample("audio-1", 1.0, "audio", "audio", {"meow": 1.0}, entity_hint="a")
    )
    settled = loop.settle(now=2.0, object_key="a")
    assert first.beliefs.get("a") is None
    assert not second.decisions[0].ignited
    assert settled.ignited and settled.belief_key == "cat"
    assert loop.belief_field.winner("a") == "cat"


def test_local_features_preserve_rewording_overlap_better_than_whole_hash() -> None:
    left = "The cat is on the table"
    right = "A cat is on that table"
    legacy = sparse_cosine_similarity(
        whole_string_hash_features(left), whole_string_hash_features(right)
    )
    local = sparse_cosine_similarity(
        compositional_text_features(left), compositional_text_features(right)
    )
    assert local > legacy
    assert local > 0.1


def test_surface_overlap_does_not_resolve_negation_semantics() -> None:
    positive = compositional_text_features("Ada is a bird")
    negative = compositional_text_features("Ada is not a bird")
    score = sparse_cosine_similarity(positive, negative)
    # This intentionally records the diagnostic encoder's limitation: high
    # overlap is not evidence that the propositions have the same meaning.
    assert score > 0.4


def test_multichannel_sample_emits_distinct_correlated_evidence() -> None:
    field = AdaptiveSensoryField()
    sparks = field.observe(
        SensorySample(
            sample_id="frame-1",
            time=0.0,
            source_id="camera-a",
            modality="vision",
            values={"edge-left": 1.0, "edge-right": 1.0},
        )
    )
    assert len(sparks) == 2
    assert len({spark.evidence_id for spark in sparks}) == 2
    assert {spark.correlation_group for spark in sparks} == {"sample:frame-1"}
    assert {spark.parents for spark in sparks} == {("frame-1",)}


def test_evidence_identity_cannot_change_source_or_correlation_group() -> None:
    ledger = EvidenceLedger()
    ledger.add(
        EvidenceContribution(
            "e1", "vision-a", "cat", 0.0, support=0.8, correlation_group="frame-a"
        )
    )
    with pytest.raises(ValueError):
        ledger.add(
            EvidenceContribution(
                "e1", "vision-b", "cat", 1.0, support=0.8, correlation_group="frame-a"
            )
        )
    with pytest.raises(ValueError):
        ledger.add(
            EvidenceContribution(
                "e1", "vision-a", "cat", 1.0, support=0.8, correlation_group="frame-b"
            )
        )


def test_contradiction_does_not_satisfy_support_diversity_gate() -> None:
    ledger = EvidenceLedger()
    gate = CoalitionGate(CoalitionGateConfig(ignition_threshold=0.1, stability_steps=1))
    ledger.add(EvidenceContribution("support", "vision", "cat", 0.0, support=1.0))
    ledger.add(EvidenceContribution("against", "audio", "cat", 0.0, contradiction=0.1))
    result = gate.evaluate({(None, "cat"): 1.0}, ledger, now=0.0)
    assert not result.ignited
    assert result.reason in {"insufficient_sources", "insufficient_independent_groups"}
    assert result.coalitions[0].source_count == 1
    assert result.coalitions[0].independent_group_count == 1


def test_reference_loop_reset_clears_evidence_state() -> None:
    from sparkbrain.v03_seed import EvidenceContribution, V03ReferenceLoop

    class Interpreter:
        def interpret(self, spark):
            yield EvidenceContribution(
                evidence_id=spark.evidence_id,
                source_id=spark.source_id,
                belief_key="cat",
                time=spark.time,
                support=0.9,
                object_key=spark.entity_slot,
                correlation_group=spark.correlation_group,
            )

    loop = V03ReferenceLoop(Interpreter())
    loop.process(
        SensorySample("vision-1", 0.0, "vision", "vision", {"fur": 1.0}, entity_hint="a")
    )
    assert loop.ledger.rows()
    loop.reset()
    assert loop.ledger.rows() == ()
    assert loop.belief_field.winner("a") is None


def test_removing_required_evidence_reverses_ignition() -> None:
    ledger = EvidenceLedger()
    gate = CoalitionGate(
        CoalitionGateConfig(ignition_threshold=1.2, stability_steps=1)
    )
    ledger.add(EvidenceContribution("vision-1", "vision", "cat", 0.0, support=0.9))
    ledger.add(EvidenceContribution("audio-1", "audio", "cat", 0.0, support=0.9))
    before = gate.evaluate({(None, "cat"): 0.7, (None, "dog"): 0.2}, ledger, now=0.0)
    assert before.ignited and before.belief_key == "cat"

    ledger.remove("audio-1")
    after = gate.evaluate({(None, "cat"): 0.7, (None, "dog"): 0.2}, ledger, now=1.0)
    assert not after.ignited
    assert after.reason in {"insufficient_sources", "insufficient_independent_groups"}
