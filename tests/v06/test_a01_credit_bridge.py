from __future__ import annotations

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig
from sparkbrain.v061_a01 import (
    A01CausalCreditStatus,
    A01LocalTemporalExpectation,
    A01SparseLocalTransitionAdaptation,
    A01TransientCreditBridge,
)


def _external(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    parent_event_ids: tuple[str, ...] = (),
    polarity: int = 1,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=polarity,
        origin=EventOrigin.EXTERNAL,
        parent_event_ids=parent_event_ids,
    )


def _boundary(
    event_id: str,
    time_ms: float,
    *,
    proposal_ids: tuple[str, ...] = (),
    port_id: str = "port:p",
) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=time_ms,
        port_id=port_id,
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=2,
        source_proposal_ids=proposal_ids,
        generation_depth=1,
        source_state_hash="field-state",
    )


def _expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.0,
        )
    )
    for index in range(2):
        source = _external(f"train-a-b-source:{index}", index * 20.0, "A")
        target = _external(f"train-a-b-target:{index}", index * 20.0 + 5.0, "B")
        model.observe_external_transition(source, target)
    for index in range(2):
        source = _external(f"train-a-c-source:{index}", 100.0 + index * 20.0, "A")
        target = _external(f"train-a-c-target:{index}", 105.0 + index * 20.0, "C")
        model.observe_external_transition(source, target)
    return model


def _proposal(
    proposal_id: str,
    *,
    path_id: str,
    parent_proposal_ids: tuple[str, ...] = (),
) -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id=proposal_id,
        created_at_ms=1.0,
        target="B",
        predicted_arrival_ms=6.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        parent_proposal_ids=parent_proposal_ids,
        local_path_ids=(path_id,),
        generation_depth=1,
        valid_until_ms=30.0,
        energy_cost=0.1,
    )


def _learn_prior_relation(
    ledger: ProvenanceLedger,
    consistency: UntypedBoundaryConsistency,
    *,
    target: str = "world:x",
    polarity: int = 1,
) -> None:
    boundary = _boundary("boundary:prior", 10.0)
    consistency.register_boundary(boundary)
    external = _external(
        "external:prior",
        12.0,
        target,
        parent_event_ids=(boundary.event_id,),
        polarity=polarity,
    )
    ledger.register_external(external)
    resolution = consistency.observe_external(external)
    assert resolution.boundary_event_id == boundary.event_id


def _bridge_fixture() -> tuple[
    A01LocalTemporalExpectation,
    ProvenanceLedger,
    UntypedBoundaryConsistency,
    A01TransientCreditBridge,
]:
    expectation = _expectation()
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency(ledger)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)
    return expectation, ledger, consistency, bridge


def test_a01_neutral_prior_preserves_base_g1_confidence() -> None:
    model = _expectation()
    source = _external("probe:a", 300.0, "A")
    rows = model.proposals_for(source, origin_state_hash="field-state")
    by_target = {row.target: row for row in rows}
    assert by_target["B"].confidence == 0.5
    assert by_target["C"].confidence == 0.5
    assert model.causal_reliability("local:A->B") == 0.5
    assert model.causal_gain("local:A->B") == 1.0


def test_a01_positive_support_changes_only_the_supported_local_path() -> None:
    model = _expectation()
    model.observe_causal_evidence(("local:A->B",), matched=True)
    source = _external("probe:a", 300.0, "A")
    rows = model.proposals_for(source, origin_state_hash="field-state")
    by_target = {row.target: row for row in rows}
    assert by_target["B"].confidence > 0.5
    assert by_target["C"].confidence == 0.5
    assert model.causal_reliability("local:A->B") == 2.0 / 3.0


def test_a01_local_state_roundtrip_preserves_causal_support() -> None:
    model = _expectation()
    model.observe_causal_evidence(("local:A->B",), matched=True)
    model.observe_causal_evidence(("local:A->B",), matched=False)
    restored = A01LocalTemporalExpectation.from_state_dict(model.state_dict())
    assert restored.state_dict() == model.state_dict()
    assert restored.learned_state_dict() == model.learned_state_dict()
    assert restored.causal_reliability("local:A->B") == 0.5


def test_a01_g2_roundtrip_retains_augmented_g1_state() -> None:
    expectation = _expectation()
    expectation.observe_causal_evidence(("local:A->B",), matched=True)
    ledger = ProvenanceLedger()
    transition = A01SparseLocalTransitionAdaptation(expectation, ledger)

    restored = A01SparseLocalTransitionAdaptation.from_state_dict(
        transition.state_dict(),
        ledger=ledger,
    )

    assert isinstance(restored.expectation, A01LocalTemporalExpectation)
    assert restored.state_dict() == transition.state_dict()
    assert restored.expectation.causal_reliability("local:A->B") == 2.0 / 3.0


def test_a01_exact_parent_match_updates_actual_historical_path() -> None:
    expectation, ledger, consistency, bridge = _bridge_fixture()
    _learn_prior_relation(ledger, consistency)
    proposal = _proposal("proposal:current", path_id="local:A->B")
    ledger.register_proposal(proposal)
    boundary = _boundary(
        "boundary:current",
        20.0,
        proposal_ids=(proposal.proposal_id,),
    )
    consistency.register_boundary(boundary)
    external = _external(
        "external:current",
        22.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)

    resolution = bridge.observe_external(boundary, external)

    assert resolution.status is A01CausalCreditStatus.EXACT_MATCH
    assert resolution.positive_credit_applied is True
    assert resolution.path_ids == ("local:A->B",)
    assert resolution.path_reliability_before == (("local:A->B", 0.5),)
    assert resolution.path_reliability_after == (("local:A->B", 2.0 / 3.0),)
    assert expectation.causal_support("local:A->B").external_consistent_count == 1


def test_a01_exact_parent_contradiction_weakens_actual_historical_path() -> None:
    expectation, ledger, consistency, bridge = _bridge_fixture()
    _learn_prior_relation(ledger, consistency)
    proposal = _proposal("proposal:current", path_id="local:A->B")
    ledger.register_proposal(proposal)
    boundary = _boundary(
        "boundary:current",
        20.0,
        proposal_ids=(proposal.proposal_id,),
    )
    consistency.register_boundary(boundary)
    external = _external(
        "external:current",
        22.0,
        "world:y",
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)

    resolution = bridge.observe_external(boundary, external)

    assert resolution.status is A01CausalCreditStatus.EXACT_CONTRADICTION
    assert resolution.contradiction_credit_applied is True
    assert expectation.causal_support("local:A->B").external_contradicted_count == 1
    assert expectation.causal_reliability("local:A->B") == 1.0 / 3.0


def test_a01_fallback_pairing_never_creates_upstream_credit() -> None:
    expectation, ledger, consistency, bridge = _bridge_fixture()
    _learn_prior_relation(ledger, consistency)
    proposal = _proposal("proposal:current", path_id="local:A->B")
    ledger.register_proposal(proposal)
    boundary = _boundary(
        "boundary:current",
        20.0,
        proposal_ids=(proposal.proposal_id,),
    )
    consistency.register_boundary(boundary)
    external = _external("external:current", 22.0, "world:x")
    ledger.register_external(external)

    resolution = bridge.observe_external(boundary, external)

    assert resolution.status is A01CausalCreditStatus.FALLBACK_PAIRED_NO_CREDIT
    assert resolution.consistency_resolution.boundary_event_id == boundary.event_id
    assert expectation.causal_reliability("local:A->B") == 0.5


def test_a01_exact_parent_without_prior_relation_abstains() -> None:
    expectation, ledger, consistency, bridge = _bridge_fixture()
    proposal = _proposal("proposal:current", path_id="local:A->B")
    ledger.register_proposal(proposal)
    boundary = _boundary(
        "boundary:current",
        20.0,
        proposal_ids=(proposal.proposal_id,),
    )
    consistency.register_boundary(boundary)
    external = _external(
        "external:current",
        22.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)

    resolution = bridge.observe_external(boundary, external)

    assert resolution.status is A01CausalCreditStatus.ABSTAINED_NO_PRIOR
    assert expectation.causal_reliability("local:A->B") == 0.5


def test_a01_causal_ancestry_credits_every_recorded_local_path() -> None:
    expectation, ledger, consistency, bridge = _bridge_fixture()
    _learn_prior_relation(ledger, consistency)
    parent = _proposal("proposal:parent", path_id="local:A->B")
    child = _proposal(
        "proposal:child",
        path_id="local:A->C",
        parent_proposal_ids=(parent.proposal_id,),
    )
    ledger.register_proposal(parent)
    ledger.register_proposal(child)
    boundary = _boundary(
        "boundary:current",
        20.0,
        proposal_ids=(child.proposal_id,),
    )
    consistency.register_boundary(boundary)
    external = _external(
        "external:current",
        22.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)

    resolution = bridge.observe_external(boundary, external)

    assert resolution.status is A01CausalCreditStatus.EXACT_MATCH
    assert resolution.path_ids == ("local:A->B", "local:A->C")
    assert expectation.causal_reliability("local:A->B") == 2.0 / 3.0
    assert expectation.causal_reliability("local:A->C") == 2.0 / 3.0


def test_a01_bridge_rejects_internal_events_as_causal_evidence() -> None:
    _, ledger, consistency, bridge = _bridge_fixture()
    boundary = _boundary("boundary:current", 20.0)
    consistency.register_boundary(boundary)
    internal = RuntimePulse(
        event_id="endo:internal",
        time_ms=22.0,
        target="world:x",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_event(internal)

    try:
        bridge.observe_external(boundary, internal)
    except ValueError as exc:
        assert "only external events" in str(exc)
    else:
        raise AssertionError("A01 accepted an internal event as causal evidence")
