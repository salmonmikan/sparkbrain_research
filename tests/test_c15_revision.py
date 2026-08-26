from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch

from sparkbrain.v03_learned import (
    ABSTENTION_THRESHOLD_GRID,
    CHECKPOINT_EPOCHS,
    CONDITION_ORDER,
    MODEL_SEEDS,
    OBJECTIVE_ORDER,
    TEMPERATURE_GRID,
    C15RevisionModel,
    CalibrationScore,
    CheckpointScore,
    ObjectiveTarget,
    ObjectiveWeights,
    RevisionModelConfig,
    RevisionModelOutput,
    TrainingEpisode,
    TrainingTarget,
    WeightedCETarget,
    compute_objective_losses,
    objective_gradient_statistics,
    select_calibration,
    select_checkpoint,
)
from sparkbrain.v03_seed import (
    BELIEF_ORDER,
    C15_E0_GLOBAL,
    C15_E1_ORACLE_ENTITY,
    EXPECTED_FULL_FIXTURE_SHA256,
    EXPECTED_SPLIT_MANIFEST_SHA256,
    EvidenceLedger,
    FixtureEvidence,
    FixtureVariant,
    RevisionBeliefField,
    RevisionController,
    RevisionFixtureEpisode,
    RevisionHeadOutput,
    RevisionObservation,
    RevisionTarget,
    TransitionKind,
    add_fixture_evidence,
    assert_frozen_fixture_hashes,
    build_full_fixture,
    fixture_evidence_to_record,
    full_fixture_sha256,
    map_attribution_target_ids,
    split_manifest_sha256,
)


def _opaque(prefix: str, text: str) -> str:
    return f"{prefix}-{hashlib.sha256(('c15-reserved|' + text).encode()).hexdigest()[:16]}"


def _reserved_evidence(
    *,
    entity_key: str,
    tag: str,
    hypothesis_id: str,
    polarity: str,
    strength: float,
    time: float,
    source_tag: str | None = None,
    group_tag: str | None = None,
) -> FixtureEvidence:
    evidence = FixtureEvidence(
        correlation_group=_opaque("grp", group_tag or tag),
        entity_key=entity_key,
        evidence_id=_opaque("ev", tag),
        hypothesis_id=hypothesis_id,
        polarity=polarity,
        source_id=_opaque("src", source_tag or tag),
        strength=strength,
        time=time,
    )
    evidence.validate()
    return evidence


def _reserved_episode(world: str = "maintain", *, index: int = 0) -> RevisionFixtureEpisode:
    if world not in {"maintain", "update", "recover", "insufficient"}:
        raise ValueError("unsupported reserved world")
    entity = _opaque("ent", str(index))
    a, b, c = BELIEF_ORDER

    def stage_a(stage: int) -> tuple[FixtureEvidence, ...]:
        return (
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|0|a",
                hypothesis_id=a,
                polarity="support",
                strength=1.0,
                time=float(stage * 10),
            ),
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|1|a",
                hypothesis_id=a,
                polarity="support",
                strength=0.9,
                time=float(stage * 10 + 1),
            ),
        )

    def stage_b(stage: int) -> tuple[FixtureEvidence, ...]:
        return (
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|0|b",
                hypothesis_id=b,
                polarity="support",
                strength=1.0,
                time=float(stage * 10),
            ),
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|1|b",
                hypothesis_id=b,
                polarity="support",
                strength=0.9,
                time=float(stage * 10 + 1),
            ),
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|2|a-neg",
                hypothesis_id=a,
                polarity="contradict",
                strength=0.85,
                time=float(stage * 10 + 2),
            ),
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|{stage}|3|a-neg",
                hypothesis_id=a,
                polarity="contradict",
                strength=0.8,
                time=float(stage * 10 + 3),
            ),
        )

    context = (stage_a(0), stage_b(1)) if world == "recover" else (stage_a(0),)
    if world == "update":
        assessment = stage_b(2)
        previous, target, transition, sufficient = a, b, "update", True
    elif world == "recover":
        assessment_rows = list(stage_a(2))
        assessment_rows.extend(
            (
                _reserved_evidence(
                    entity_key=entity,
                    tag=f"{index}|2|2|b-neg",
                    hypothesis_id=b,
                    polarity="contradict",
                    strength=0.85,
                    time=22.0,
                ),
                _reserved_evidence(
                    entity_key=entity,
                    tag=f"{index}|2|3|b-neg",
                    hypothesis_id=b,
                    polarity="contradict",
                    strength=0.8,
                    time=23.0,
                ),
            )
        )
        assessment = tuple(assessment_rows)
        previous, target, transition, sufficient = b, a, "recover", True
    elif world == "insufficient":
        assessment = (
            _reserved_evidence(
                entity_key=entity,
                tag=f"{index}|2|0|weak-a",
                hypothesis_id=a,
                polarity="support",
                strength=0.35,
                time=20.0,
            ),
        )
        previous, target, transition, sufficient = (
            a,
            a,
            "insufficient_information",
            False,
        )
    else:
        assessment = stage_a(2)
        previous, target, transition, sufficient = a, a, "maintain", True
    targets = tuple(
        row.evidence_id
        for row in assessment
        if row.hypothesis_id == target and row.polarity == "support"
    )
    distractor = _reserved_evidence(
        entity_key=entity,
        tag=f"{index}|2|4|distractor",
        hypothesis_id=c,
        polarity="support",
        strength=0.25,
        time=24.0,
    )
    correlated = assessment[0]
    correlated_copy = FixtureEvidence(
        correlation_group=correlated.correlation_group,
        entity_key=correlated.entity_key,
        evidence_id=_opaque("ev", f"{index}|correlated-copy"),
        hypothesis_id=correlated.hypothesis_id,
        polarity=correlated.polarity,
        source_id=correlated.source_id,
        strength=correlated.strength,
        time=correlated.time,
    )
    variants = (
        FixtureVariant(assessment, targets, "base"),
        FixtureVariant((*assessment, distractor), targets, "irrelevant_distractor"),
        FixtureVariant((*assessment, assessment[0]), targets, "same_id_duplicate"),
        FixtureVariant((*assessment, correlated_copy), targets, "correlated_copy"),
    )
    return RevisionFixtureEpisode(
        context_stages=context,
        entity_key=entity,
        episode_id=_opaque("ep", f"{index}|{world}"),
        episode_seed=99_002 + index,
        family_id=_opaque("fam", f"{index}|{world}"),
        previous_truth=previous,
        sufficient_information=sufficient,
        target_truth=target,
        transition_target=transition,
        variants=variants,
        world=world,
    )


def _heads(
    winner: str,
    *,
    maintain: float = 1.0,
    update: float = 1.0,
    recovery: float = 1.0,
    abstention: float = 0.0,
) -> RevisionHeadOutput:
    probabilities = {belief: 0.1 for belief in BELIEF_ORDER}
    probabilities[winner] = 0.8
    return RevisionHeadOutput(
        probabilities,
        maintain,
        update,
        recovery,
        abstention,
    )


def _observation(
    episode,
    evidence,
    heads: RevisionHeadOutput,
    *,
    time: float,
    entity_condition: str = C15_E1_ORACLE_ENTITY,
) -> RevisionObservation:
    return RevisionObservation(
        entity_key=episode.entity_key,
        time=time,
        evidence=tuple(evidence),
        entity_condition=entity_condition,
        heads=heads,
    )


def _model_output():
    torch.manual_seed(99_002)
    model = C15RevisionModel(RevisionModelConfig())
    features = torch.zeros((5, 12), dtype=torch.float32)
    features[0, 0] = 1.0
    features[1, 1] = 1.0
    mask = torch.tensor([True, True, False, False, False])
    output = model.forward_visible(
        entity_key="ent-opaque",
        features=features,
        evidence_ids=("ev-a", "ev-b", None, None, None),
        padding_mask=mask,
    )
    return model, output


def _zero_model_output() -> tuple[C15RevisionModel, RevisionModelOutput]:
    torch.manual_seed(99_002)
    model = C15RevisionModel()
    output = RevisionModelOutput(
        entity_key="ent-reserved",
        belief_logits=torch.zeros(3, requires_grad=True),
        maintain_logit=torch.zeros((), requires_grad=True),
        update_logit=torch.zeros((), requires_grad=True),
        recovery_logit=torch.zeros((), requires_grad=True),
        abstention_logit=torch.zeros((), requires_grad=True),
        attribution_logits=torch.zeros(5, requires_grad=True),
        attribution_mask=torch.tensor([True, True, False, False, False]),
        evidence_ids=("ev-z", "ev-a", None, None, None),
        router_probabilities=torch.full((5, 4), 0.25, requires_grad=True),
        selected_modules=torch.tensor([[0, 1]] * 5),
        hidden_state=torch.zeros(16, requires_grad=True),
    )
    return model, output


def test_frozen_split_and_full_fixture_hashes_match_protocol() -> None:
    protocol = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "artifacts/v03/c15_revision_v4/protocol.json"
        )
        .read_text(encoding="utf-8")
    )
    assert protocol["protocol_id"] == "c15-revision-objectives-v4"
    assert EXPECTED_SPLIT_MANIFEST_SHA256 == protocol["seeds"]["split_manifest_sha256"]
    assert EXPECTED_FULL_FIXTURE_SHA256 == protocol["seeds"]["full_fixture_sha256"]
    assert_frozen_fixture_hashes()
    for split in ("train", "dev", "test"):
        assert split_manifest_sha256(split) == EXPECTED_SPLIT_MANIFEST_SHA256[split]
        assert full_fixture_sha256(split) == EXPECTED_FULL_FIXTURE_SHA256[split]
        assert build_full_fixture(split)[0].episode_seed == protocol["splits"][split][
            "episode_seed_base"
        ]
    assert len(build_full_fixture("train")) == 64
    assert len(build_full_fixture("dev")) == len(build_full_fixture("test")) == 32
    assert MODEL_SEEDS == tuple(protocol["seeds"]["model"]) == (2951, 2952, 2953, 2954, 2955)


@pytest.mark.parametrize(
    ("field_name", "invalid"),
    (
        ("strength", True),
        ("strength", "1.0"),
        ("strength", float("nan")),
        ("strength", -0.1),
        ("time", False),
        ("time", "0.0"),
        ("time", float("inf")),
        ("time", -0.1),
    ),
)
def test_fixture_evidence_rejects_non_numeric_bool_and_nonfinite_values(
    field_name: str, invalid: object
) -> None:
    values = {
        "entity_key": _opaque("ent", "invalid-number"),
        "tag": "invalid-number",
        "hypothesis_id": "alpha",
        "polarity": "support",
        "strength": 1.0,
        "time": 0.0,
    }
    values[field_name] = invalid
    with pytest.raises(ValueError, match=f"fixture evidence {field_name}"):
        _reserved_evidence(**values)


def test_observation_caches_canonical_metadata_against_nested_mutation() -> None:
    episode = _reserved_episode()
    source_metadata = {"nested": {"values": [1, 2], "flag": True}}
    observation = RevisionObservation(
        entity_key=episode.entity_key,
        time=5.0,
        evidence=episode.context_stages[0],
        entity_condition=C15_E1_ORACLE_ENTITY,
        heads=_heads(episode.target_truth),
        metadata=source_metadata,
    )
    payload_before = observation.to_canonical_json()
    hash_before = observation.input_hash
    source_metadata["nested"]["values"].append(3)
    observation.metadata["nested"]["values"].append(4)
    assert observation.to_canonical_json() == payload_before
    assert observation.input_hash == hash_before
    assert RevisionObservation.from_canonical_json(payload_before).input_hash == hash_before


def test_e0_e1_mapping_preserves_duplicate_and_correlation_identity() -> None:
    episode = _reserved_episode()
    base = episode.variants[0].assessment_deliveries[0]
    duplicate = episode.variants[2].assessment_deliveries[-1]
    correlated = episode.variants[3].assessment_deliveries[-1]

    e1 = fixture_evidence_to_record(base, entity_condition=C15_E1_ORACLE_ENTITY)
    e0 = fixture_evidence_to_record(base, entity_condition=C15_E0_GLOBAL)
    e0_duplicate = fixture_evidence_to_record(duplicate, entity_condition=C15_E0_GLOBAL)
    e0_correlated = fixture_evidence_to_record(correlated, entity_condition=C15_E0_GLOBAL)

    assert (e1.entity_key, e1.evidence_id) == (base.entity_key, base.evidence_id)
    assert e0.entity_key == "__global__"
    assert e0.evidence_id == e0_duplicate.evidence_id
    assert e0_correlated.evidence_id != e0.evidence_id
    assert e0_correlated.correlation_group == e0.correlation_group
    assert e0_correlated.source_id == e0.source_id
    assert e0.parent_spark_ids != e1.parent_spark_ids

    mapped = map_attribution_target_ids(
        episode.variants[0].attribution_targets,
        entity_condition=C15_E0_GLOBAL,
    )
    expected = tuple(
        fixture_evidence_to_record(row, entity_condition=C15_E0_GLOBAL).evidence_id
        for row in episode.variants[0].assessment_deliveries
        if row.evidence_id in episode.variants[0].attribution_targets
    )
    assert mapped == expected


def test_same_id_redelivery_is_ledger_noop_after_e0_adaptation() -> None:
    episode = _reserved_episode()
    original = episode.variants[2].assessment_deliveries[0]
    duplicate = episode.variants[2].assessment_deliveries[-1]
    ledger = EvidenceLedger()
    seen: set[str] = set()
    add_fixture_evidence(
        ledger,
        original,
        entity_condition=C15_E0_GLOBAL,
        seen_evidence_ids=seen,
    )
    before = ledger.active_state_hash()
    add_fixture_evidence(
        ledger,
        duplicate,
        entity_condition=C15_E0_GLOBAL,
        seen_evidence_ids=seen,
    )
    assert ledger.active_state_hash() == before
    assert len(ledger.rows()) == 1
    assert ledger.audit_rows()[-1].action == "redelivery_noop"


def test_target_is_truth_history_derived_and_strictly_serializable() -> None:
    target = RevisionTarget.from_truth_history(
        ("alpha", "beta"),
        truth_belief="alpha",
        causal_source_count=2,
        causal_group_count=2,
    )
    assert target.transition is TransitionKind.RECOVER
    assert target.recovery_opportunity
    payload = target.to_canonical_json()
    assert RevisionTarget.from_canonical_json(payload) == target

    insufficient = RevisionTarget.from_truth_history(
        ("alpha", "beta"),
        truth_belief="alpha",
        causal_source_count=1,
        causal_group_count=2,
    )
    assert insufficient.transition is TransitionKind.INSUFFICIENT_INFORMATION
    assert not insufficient.recovery_opportunity
    with pytest.raises(ValueError, match="strict canonical"):
        RevisionTarget.from_canonical_json(payload + " ")


@pytest.mark.parametrize(
    "forbidden",
    (
        "truth",
        "target",
        "label",
        "expected",
        "transition_target",
        "test_only",
        "episode_seed",
        "truth_belief",
        "previous_truth_belief",
        "sufficient_information",
        "recovery_opportunity",
        "belief_index",
    ),
)
def test_production_observation_recursively_rejects_target_leakage(
    forbidden: str,
) -> None:
    episode = _reserved_episode()
    with pytest.raises(ValueError, match="forbidden production field"):
        _observation(
            episode,
            episode.context_stages[0],
            _heads(episode.target_truth),
            time=5.0,
        ).__class__(
            entity_key=episode.entity_key,
            time=5.0,
            evidence=episode.context_stages[0],
            entity_condition=C15_E1_ORACLE_ENTITY,
            heads=_heads(episode.target_truth),
            metadata={"nested": [{forbidden: "evaluator-owned"}]},
        )


def test_model_rejects_nested_truth_before_runtime_mutation() -> None:
    model = C15RevisionModel()
    fixture = {
        "entity_key": "ent-opaque",
        "features": [[0.0] * 12 for _ in range(5)],
        "evidence_ids": ["ev-a", None, None, None, None],
        "padding_mask": [True, False, False, False, False],
        "metadata": {"nested": {"truth": "alpha"}},
    }
    with pytest.raises(ValueError, match="forbidden evaluator field"):
        model.forward_fixture(fixture)
    assert model.runtime_state("ent-opaque") is None


def test_continuous_a_b_a_recovery_without_checkpoint_restore() -> None:
    episode = _reserved_episode("recover")
    controller = RevisionController()
    a_truth = episode.target_truth
    b_truth = episode.previous_truth

    establish_a = controller.process_stage(
        _observation(
            episode,
            episode.context_stages[0],
            _heads(a_truth),
            time=5.0,
        )
    )
    establish_b = controller.process_stage(
        _observation(
            episode,
            episode.context_stages[1],
            _heads(b_truth),
            time=15.0,
        )
    )
    recover_a = controller.process_stage(
        _observation(
            episode,
            episode.variants[0].assessment_deliveries,
            _heads(a_truth),
            time=25.0,
        )
    )

    assert establish_a.belief_key == a_truth
    assert establish_b.belief_key == b_truth
    assert recover_a.belief_key == a_truth
    assert recover_a.predicted_transition is TransitionKind.RECOVER
    assert recover_a.state_after.history == (a_truth, b_truth, a_truth)
    assert recover_a.state_before.activations[a_truth] > 0.0
    assert any(
        row.action == "deactivate" and row.reason == "c15_stage_scope"
        for row in controller.ledger.audit_rows()
    )


def test_stage_scope_leaves_other_entity_active() -> None:
    first, second = _reserved_episode(index=1), _reserved_episode(index=2)
    controller = RevisionController()
    controller.process_stage(
        _observation(
            first,
            first.context_stages[0],
            _heads(first.target_truth),
            time=5.0,
        )
    )
    first_ids = {
        row.evidence_id
        for row in controller.ledger.rows(active_only=True)
        if row.entity_key == first.entity_key
    }
    controller.process_stage(
        _observation(
            second,
            second.context_stages[0],
            _heads(second.target_truth),
            time=5.0,
        )
    )
    assert first_ids
    assert all(controller.ledger.is_active(evidence_id) for evidence_id in first_ids)


def test_inactive_prior_id_reappearance_fails_atomically() -> None:
    episode = _reserved_episode("update")
    controller = RevisionController()
    controller.process_stage(
        _observation(
            episode,
            episode.context_stages[0],
            _heads(episode.previous_truth),
            time=5.0,
        )
    )
    controller.process_stage(
        _observation(
            episode,
            episode.variants[0].assessment_deliveries,
            _heads(episode.target_truth),
            time=25.0,
        )
    )
    ledger_before = controller.ledger.serialize_state()
    belief_before = controller.belief_field.serialize_state()
    stability_before = dict(controller.gate._c14_stability)
    signatures_before = dict(controller.gate._c14_signatures)

    with pytest.raises(ValueError, match="cannot restore prior inactive evidence"):
        controller.process_stage(
            _observation(
                episode,
                episode.context_stages[0],
                _heads(episode.previous_truth),
                time=35.0,
            )
        )

    assert controller.ledger.serialize_state() == ledger_before
    assert controller.belief_field.serialize_state() == belief_before
    assert controller.gate._c14_stability == stability_before
    assert controller.gate._c14_signatures == signatures_before


def test_same_id_duplicate_is_noop_within_controller_stage() -> None:
    episode = _reserved_episode()
    controller = RevisionController()
    controller.process_stage(
        _observation(
            episode,
            episode.context_stages[0],
            _heads(episode.target_truth),
            time=5.0,
        )
    )
    decision = controller.process_stage(
        _observation(
            episode,
            episode.variants[2].assessment_deliveries,
            _heads(episode.target_truth),
            time=25.0,
        )
    )
    active = tuple(
        row
        for row in controller.ledger.rows(active_only=True)
        if row.entity_key == episode.entity_key
    )
    assert len(active) == len(episode.variants[0].assessment_deliveries)
    assert controller.ledger.audit_rows()[-1].action == "redelivery_noop"
    assert decision.proposal.ignited


def test_c14_proposal_precedes_veto_and_no_ignition_retains_entity() -> None:
    episode = _reserved_episode()
    controller = RevisionController()
    decision = controller.process_stage(
        _observation(
            episode,
            episode.context_stages[0],
            _heads(episode.target_truth, abstention=1.0),
            time=5.0,
        )
    )
    assert decision.gate_passes[0].reason == "insufficient_stability"
    assert decision.proposal.ignited
    assert not decision.ignited
    assert decision.reason == "learned_insufficient_information"
    assert decision.evaluated_entity_key == episode.entity_key
    assert decision.object_key is None
    assert decision.state_before.state_hash == decision.state_after.state_hash


def test_context_uses_c14_proposal_while_assessment_retains_learned_veto() -> None:
    episode = _reserved_episode()
    observation = _observation(
        episode,
        episode.context_stages[0],
        _heads(episode.target_truth, abstention=1.0),
        time=5.0,
    )

    context = RevisionController().process_stage(observation, stage_role="context")
    assessment = RevisionController().process_stage(observation, stage_role="assessment")

    assert context.proposal.ignited and context.ignited
    assert context.belief_key == episode.target_truth
    assert context.state_after.history == (episode.target_truth,)
    assert assessment.proposal.ignited and not assessment.ignited
    assert assessment.reason == "learned_insufficient_information"
    assert assessment.state_before.state_hash == assessment.state_after.state_hash
    assert context.input_hash == assessment.input_hash == observation.input_hash


def test_invalid_stage_role_is_rejected_before_controller_mutation() -> None:
    episode = _reserved_episode()
    controller = RevisionController()
    ledger_before = controller.ledger.serialize_state()
    belief_before = controller.belief_field.serialize_state()

    with pytest.raises(ValueError, match="stage_role must be context or assessment"):
        controller.process_stage(
            _observation(
                episode,
                episode.context_stages[0],
                _heads(episode.target_truth),
                time=5.0,
            ),
            stage_role="invalid",
        )

    assert controller.ledger.serialize_state() == ledger_before
    assert controller.belief_field.serialize_state() == belief_before
    assert controller.gate._c14_stability == {}
    assert controller.gate._c14_signatures == {}


def test_transition_head_veto_decays_once_without_clearing_winner() -> None:
    episode = _reserved_episode()
    controller = RevisionController()
    accepted = controller.process_stage(
        _observation(
            episode,
            episode.context_stages[0],
            _heads(episode.target_truth),
            time=5.0,
        )
    )
    vetoed = controller.process_stage(
        _observation(
            episode,
            episode.variants[0].assessment_deliveries,
            _heads(episode.target_truth, maintain=0.49),
            time=25.0,
        )
    )
    before = accepted.state_after.activations[episode.target_truth]
    after = vetoed.state_after.activations[episode.target_truth]
    assert vetoed.proposal.ignited and not vetoed.ignited
    assert vetoed.reason == "maintain_head_below_threshold"
    assert vetoed.state_after.winner == episode.target_truth
    assert after == pytest.approx(before * 0.88)
    assert vetoed.state_after.citations == accepted.state_after.citations


def test_belief_state_is_entity_isolated_and_strictly_replayable() -> None:
    first, second = _reserved_episode(index=3), _reserved_episode(index=4)
    controller = RevisionController()
    controller.process_stage(
        _observation(
            first,
            first.context_stages[0],
            _heads(first.target_truth),
            time=5.0,
        )
    )
    first_before = controller.belief_field.snapshot(first.entity_key)
    controller.process_stage(
        _observation(
            second,
            second.context_stages[0],
            _heads(second.target_truth),
            time=5.0,
        )
    )
    assert controller.belief_field.snapshot(first.entity_key) == first_before

    payload = controller.belief_field.serialize_state()
    restored = RevisionBeliefField.from_serialized_state(payload)
    assert restored.serialize_state() == payload
    before_inspection = restored.serialize_state()
    restored.snapshot("ent-never-seen")
    assert restored.serialize_state() == before_inspection
    with pytest.raises(ValueError, match="strict canonical"):
        RevisionBeliefField.from_serialized_state(payload + "\n")


@pytest.mark.parametrize(
    ("condition_id", "objective_id"),
    tuple((f"no_{objective_id}", objective_id) for objective_id in OBJECTIVE_ORDER),
)
def test_each_objective_has_an_exact_zero_weight_ablation(
    condition_id: str,
    objective_id: str,
) -> None:
    assert condition_id in CONDITION_ORDER
    weights = ObjectiveWeights.for_condition(condition_id).as_dict()
    assert weights[objective_id] == 0.0
    assert all(value > 0.0 for other_id, value in weights.items() if other_id != objective_id)


def test_nine_objectives_are_separate_and_zero_weight_gradients_are_zero() -> None:
    model, output = _model_output()
    target = ObjectiveTarget(
        belief_index=0,
        previous_belief_index=1,
        transition_target="recover",
        sufficient_information=True,
        previous_probabilities=torch.tensor([0.2, 0.7, 0.1]),
        restored_prior_activation=0.12,
        attribution_target_ids=("ev-a",),
    )
    weights = ObjectiveWeights.for_condition("no_recovery")
    bundle = compute_objective_losses(
        model=model,
        assessment=output,
        episode_outputs=(output,),
        target=target,
        weights=weights,
    )
    assert tuple(bundle.terms) == OBJECTIVE_ORDER
    assert all(math.isfinite(float(term.raw_loss.detach())) for term in bundle.terms.values())
    rows = objective_gradient_statistics(model, bundle)
    assert rows["recovery"].weight == 0.0
    assert rows["recovery"].weighted_contribution == 0.0
    assert rows["recovery"].weighted_gradient_l2 == 0.0
    assert rows["recovery"].unweighted_gradient_l2 > 0.0


def test_one_weighted_ce_has_no_auxiliary_weighted_contribution() -> None:
    model, output = _model_output()
    forbidden_transition_target = ObjectiveTarget(
        belief_index=0,
        previous_belief_index=0,
        transition_target="maintain",
        sufficient_information=True,
        previous_probabilities=torch.tensor([0.6, 0.2, 0.2]),
        restored_prior_activation=0.0,
        attribution_target_ids=("ev-a",),
    )
    weights = ObjectiveWeights.for_condition("one_weighted_ce")
    with pytest.raises(ValueError, match="must not receive transition objectives"):
        compute_objective_losses(
            model=model,
            assessment=output,
            episode_outputs=(output,),
            target=forbidden_transition_target,
            weights=weights,
            one_weighted_ce=True,
        )
    bundle = compute_objective_losses(
        model=model,
        assessment=output,
        episode_outputs=(output,),
        target=WeightedCETarget(belief_index=0, sufficient_information=True),
        weights=weights,
        one_weighted_ce=True,
    )
    assert bundle.baseline_loss is not None
    assert torch.equal(bundle.total_loss, bundle.baseline_loss)
    assert all(term.weight == 0.0 for term in bundle.terms.values())
    assert all(float(term.weighted_contribution) == 0.0 for term in bundle.terms.values())


def test_model_architecture_parameter_count_and_router_tie_break_are_exact() -> None:
    torch.manual_seed(99_002)
    model = C15RevisionModel()
    assert sum(parameter.numel() for parameter in model.parameters()) == 3_132
    with torch.no_grad():
        model.router.weight.zero_()
        model.router.bias.zero_()
    output = model.forward_visible(
        entity_key="ent-reserved",
        features=torch.zeros((5, 12)),
        evidence_ids=("ev-a", "ev-b", None, None, None),
        padding_mask=torch.tensor([True, True, False, False, False]),
    )
    assert torch.equal(output.router_probabilities, torch.full((5, 4), 0.25))
    assert torch.equal(output.selected_modules, torch.tensor([[0, 1]] * 5))


def test_padding_is_non_contributing_and_all_padding_is_rejected() -> None:
    torch.manual_seed(99_002)
    model = C15RevisionModel()
    mask = torch.tensor([True, True, False, False, False])
    base = torch.zeros((5, 12))
    base[0, 0] = 1.0
    base[1, 1] = 1.0
    changed_padding = base.clone()
    changed_padding[2:] = 10_000.0
    first = model.forward_visible(
        entity_key="ent-reserved",
        features=base,
        evidence_ids=("ev-a", "ev-b", None, None, None),
        padding_mask=mask,
    )
    model.reset_runtime()
    second = model.forward_visible(
        entity_key="ent-reserved",
        features=changed_padding,
        evidence_ids=("ev-a", "ev-b", None, None, None),
        padding_mask=mask,
    )
    assert torch.equal(first.hidden_state, second.hidden_state)
    assert torch.equal(first.belief_logits, second.belief_logits)
    assert torch.equal(first.attribution_logits[mask], second.attribution_logits[mask])
    with pytest.raises(ValueError, match="at least one non-padding"):
        model.forward_visible(
            entity_key="ent-reserved",
            features=base,
            evidence_ids=(None, None, None, None, None),
            padding_mask=torch.zeros(5, dtype=torch.bool),
        )


def test_entity_runtime_is_isolated_detachable_and_resettable() -> None:
    torch.manual_seed(99_002)
    model = C15RevisionModel()
    features = torch.zeros((5, 12))
    mask = torch.tensor([True, False, False, False, False])
    model.forward_visible(
        entity_key="ent-a",
        features=features,
        evidence_ids=("ev-a", None, None, None, None),
        padding_mask=mask,
    )
    state_a = model.runtime_state("ent-a")
    model.forward_visible(
        entity_key="ent-b",
        features=features + 1.0,
        evidence_ids=("ev-b", None, None, None, None),
        padding_mask=mask,
    )
    assert torch.equal(model.runtime_state("ent-a"), state_a)
    assert model.runtime_state("ent-b") is not None
    model.detach_runtime()
    assert not model._entity_states["ent-a"].requires_grad
    assert not model._entity_states["ent-b"].requires_grad
    model.reset_runtime()
    assert model.runtime_state("ent-a") is None
    assert model.runtime_state("ent-b") is None


def test_target_permutation_changes_loss_not_production_input_or_prediction() -> None:
    torch.manual_seed(99_002)
    model = C15RevisionModel()
    fixture = {
        "entity_key": "ent-reserved",
        "features": [[0.0] * 12 for _ in range(5)],
        "evidence_ids": ["ev-a", None, None, None, None],
        "padding_mask": [True, False, False, False, False],
    }
    first = model.forward_fixture(fixture)
    model.reset_runtime()
    second = model.forward_fixture(fixture)
    assert torch.equal(first.belief_logits, second.belief_logits)
    common = {
        "transition_target": "maintain",
        "sufficient_information": True,
        "previous_probabilities": torch.tensor([0.5, 0.3, 0.2]),
        "restored_prior_activation": 0.0,
        "attribution_target_ids": ("ev-a",),
    }
    alpha = ObjectiveTarget(belief_index=0, previous_belief_index=0, **common)
    beta = ObjectiveTarget(belief_index=1, previous_belief_index=1, **common)
    alpha_loss = compute_objective_losses(
        model=model,
        assessment=first,
        episode_outputs=(first,),
        target=alpha,
        weights=ObjectiveWeights(),
    ).total_loss
    beta_loss = compute_objective_losses(
        model=model,
        assessment=second,
        episode_outputs=(second,),
        target=beta,
        weights=ObjectiveWeights(),
    ).total_loss
    assert not torch.equal(alpha_loss, beta_loss)


@pytest.mark.parametrize(
    ("history", "truth", "sources", "groups", "expected"),
    (
        (("alpha",), "alpha", 1, 2, TransitionKind.INSUFFICIENT_INFORMATION),
        (("alpha", "beta"), "alpha", 2, 2, TransitionKind.RECOVER),
        (("alpha",), "beta", 2, 2, TransitionKind.UPDATE),
        (("alpha",), "alpha", 2, 2, TransitionKind.MAINTAIN),
    ),
)
def test_transition_precedence_is_exact(
    history: tuple[str, ...],
    truth: str,
    sources: int,
    groups: int,
    expected: TransitionKind,
) -> None:
    target = RevisionTarget.from_truth_history(
        history,
        truth_belief=truth,
        causal_source_count=sources,
        causal_group_count=groups,
    )
    assert target.transition is expected


@pytest.mark.parametrize(
    ("world", "head_name", "rejected_reason"),
    (
        ("maintain", "maintain", "maintain_head_below_threshold"),
        ("update", "update", "update_head_below_threshold"),
        ("recover", "recovery", "recovery_head_below_threshold"),
    ),
)
def test_transition_veto_boundary_is_049_reject_05_accept(
    world: str, head_name: str, rejected_reason: str
) -> None:
    def assess(probability: float):
        episode = _reserved_episode(world)
        controller = RevisionController()
        for stage_index, stage in enumerate(episode.context_stages):
            winner = (
                episode.previous_truth
                if stage_index == len(episode.context_stages) - 1
                else episode.target_truth
            )
            controller.process_stage(
                _observation(
                    episode,
                    stage,
                    _heads(winner),
                    time=float(stage_index * 10 + 5),
                )
            )
        head_values = {"maintain": 1.0, "update": 1.0, "recovery": 1.0}
        head_values[head_name] = probability
        return controller.process_stage(
            _observation(
                episode,
                episode.variants[0].assessment_deliveries,
                _heads(episode.target_truth, **head_values),
                time=25.0,
            )
        )

    rejected = assess(0.49)
    accepted = assess(0.5)
    assert rejected.proposal.ignited and not rejected.ignited
    assert rejected.reason == rejected_reason
    assert accepted.proposal.ignited and accepted.ignited


def test_context_cannot_force_a_c14_rejection_with_learned_heads() -> None:
    episode = _reserved_episode("insufficient")
    decision = RevisionController().process_stage(
        _observation(
            episode,
            episode.variants[0].assessment_deliveries,
            _heads(
                episode.target_truth,
                maintain=1.0,
                update=1.0,
                recovery=1.0,
                abstention=0.0,
            ),
            time=25.0,
        ),
        stage_role="context",
    )
    assert not decision.proposal.ignited
    assert not decision.ignited
    assert decision.reason == decision.proposal.reason


def test_nine_zero_logit_losses_match_preregistered_analytic_values() -> None:
    model, output = _zero_model_output()
    common = {
        "belief_index": 0,
        "previous_belief_index": 1,
        "sufficient_information": True,
        "previous_probabilities": torch.tensor([1.0, 0.0, 0.0]),
        "restored_prior_activation": 0.12,
        "attribution_target_ids": ("ev-z",),
    }

    def losses(transition: str) -> dict[str, float]:
        bundle = compute_objective_losses(
            model=model,
            assessment=output,
            episode_outputs=(output,),
            target=ObjectiveTarget(transition_target=transition, **common),
            weights=ObjectiveWeights(),
        )
        return {key: float(term.raw_loss.detach()) for key, term in bundle.terms.items()}

    maintain = losses("maintain")
    update = losses("update")
    recovery = losses("recover")
    assert maintain["belief"] == pytest.approx(math.log(3.0))
    assert maintain["calibration"] == pytest.approx(2.0 / 3.0)
    assert maintain["maintain"] == pytest.approx(math.log(2.0) + 4.0 / 9.0)
    assert update["update"] == pytest.approx(2.0 * math.log(2.0))
    assert recovery["recovery"] == pytest.approx(math.log(2.0) + 0.03)
    assert maintain["no_ignition"] == pytest.approx(math.log(2.0))
    assert maintain["attribution"] == pytest.approx(math.log(2.0))
    assert maintain["sparsity"] == pytest.approx(1.0)
    assert maintain["load_balance"] == pytest.approx(0.0)


def test_insufficient_rows_mask_only_the_preregistered_objectives() -> None:
    model, output = _zero_model_output()
    target = ObjectiveTarget(
        belief_index=0,
        previous_belief_index=0,
        transition_target="insufficient_information",
        sufficient_information=False,
        previous_probabilities=torch.tensor([1.0, 0.0, 0.0]),
        restored_prior_activation=0.0,
        attribution_target_ids=("ev-z",),
    )
    bundle = compute_objective_losses(
        model=model,
        assessment=output,
        episode_outputs=(output,),
        target=target,
        weights=ObjectiveWeights(),
    )
    for objective_id in ("belief", "maintain", "update", "recovery", "calibration"):
        assert bundle.terms[objective_id].eligible_count == 0
        assert float(bundle.terms[objective_id].raw_loss.detach()) == 0.0
    assert bundle.terms["no_ignition"].eligible_count == 1
    assert float(bundle.terms["no_ignition"].raw_loss.detach()) == pytest.approx(math.log(2.0))
    assert bundle.terms["attribution"].eligible_count == 2
    assert bundle.terms["sparsity"].eligible_count == 2
    assert bundle.terms["load_balance"].eligible_count == 2


def test_weighted_ce_target_type_is_fail_closed_in_both_directions() -> None:
    model, output = _zero_model_output()
    separated = ObjectiveTarget(
        belief_index=0,
        previous_belief_index=0,
        transition_target="maintain",
        sufficient_information=True,
        previous_probabilities=torch.tensor([1.0, 0.0, 0.0]),
        restored_prior_activation=0.0,
        attribution_target_ids=("ev-z",),
    )
    baseline = WeightedCETarget(belief_index=0, sufficient_information=True)
    with pytest.raises(ValueError, match="must not receive transition objectives"):
        compute_objective_losses(
            model=model,
            assessment=output,
            episode_outputs=(output,),
            target=separated,
            weights=ObjectiveWeights.for_condition("one_weighted_ce"),
            one_weighted_ce=True,
        )
    with pytest.raises(ValueError, match="require the frozen transition target"):
        compute_objective_losses(
            model=model,
            assessment=output,
            episode_outputs=(output,),
            target=baseline,
            weights=ObjectiveWeights(),
        )


def test_training_episode_accepts_only_exact_separated_or_weighted_ce_target() -> None:
    call = {
        "entity_key": "ent-reserved",
        "features": [[0.0] * 12 for _ in range(5)],
        "evidence_ids": ["ev-z", None, None, None, None],
        "padding_mask": [True, False, False, False, False],
    }
    envelope = {
        "episode_id": _opaque("ep", "training-envelope"),
        "variant_id": "base",
        "input_track": "I1_local_compositional",
        "entity_condition": "E1_oracle_entity",
        "model_calls": [call, call],
        "assessment_index": 1,
    }
    separated = TrainingEpisode.from_fixture(
        {
            **envelope,
            "target": {
                "belief_index": 0,
                "previous_belief_index": 0,
                "transition_target": "maintain",
                "sufficient_information": True,
                "attribution_target_ids": ["ev-z", "ev-a"],
            },
        }
    )
    assert isinstance(separated.target, TrainingTarget)
    assert separated.target.attribution_target_ids == ("ev-z", "ev-a")
    baseline = TrainingEpisode.from_fixture(
        {
            **envelope,
            "target": {"belief_index": 0, "sufficient_information": True},
        }
    )
    assert isinstance(baseline.target, WeightedCETarget)
    with pytest.raises(ValueError, match="missing or unknown fields"):
        TrainingEpisode.from_fixture(
            {
                **envelope,
                "target": {
                    "belief_index": 0,
                    "sufficient_information": True,
                    "transition_target": "maintain",
                },
            }
        )


def test_checkpoint_and_calibration_tie_breaks_are_exact() -> None:
    checkpoint = select_checkpoint(
        [
            CheckpointScore(epoch=epoch, weighted_objective_total=1.0)
            for epoch in reversed(CHECKPOINT_EPOCHS)
        ]
    )
    assert checkpoint.epoch == 2
    calibration = select_calibration(
        [
            CalibrationScore(
                temperature=temperature,
                abstention_threshold=threshold,
                belief_brier=0.5,
                abstention_brier=0.5,
            )
            for temperature in reversed(TEMPERATURE_GRID)
            for threshold in reversed(ABSTENTION_THRESHOLD_GRID)
        ]
    )
    assert (calibration.temperature, calibration.abstention_threshold) == (0.75, 0.4)
