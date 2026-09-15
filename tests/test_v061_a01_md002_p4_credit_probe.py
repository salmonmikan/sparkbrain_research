from __future__ import annotations

import pytest

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig
from sparkbrain.v061_a01.credit_bridge import (
    A01CausalCreditStatus,
    A01LocalTemporalExpectation,
    A01TransientCreditBridge,
)
from sparkbrain.v061_a01.md002_p4_credit_probe import probe_merged_lineage_credit


def _external(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    parent_event_ids: tuple[str, ...] = (),
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
        parent_event_ids=parent_event_ids,
    )


def _boundary(
    event_id: str,
    time_ms: float,
    *,
    source_proposal_ids: tuple[str, ...],
) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=time_ms,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=0,
        source_proposal_ids=source_proposal_ids,
        generation_depth=1,
        source_state_hash="state:shared",
    )


def _proposal(proposal_id: str, target: str) -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id=proposal_id,
        created_at_ms=10.0,
        target=target,
        predicted_arrival_ms=20.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="state:shared",
        local_path_ids=(f"local:A->{target}",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )


def _prepared_bridge() -> tuple[
    A01TransientCreditBridge,
    UntypedBoundaryConsistency,
    ProvenanceLedger,
]:
    expectation = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    expectation.observe_external_transition(
        _external("train-a-b-source", 0.0, "A"),
        _external("train-a-b-target", 5.0, "B"),
    )
    expectation.observe_external_transition(
        _external("train-a-c-source", 10.0, "A"),
        _external("train-a-c-target", 15.0, "C"),
    )

    ledger = ProvenanceLedger()
    ledger.register_proposal(_proposal("proposal-b", "B"))
    ledger.register_proposal(_proposal("proposal-c", "C"))
    consistency = UntypedBoundaryConsistency(ledger)

    prior_boundary = _boundary(
        "boundary-prior",
        30.0,
        source_proposal_ids=("proposal-b",),
    )
    prior_external = _external(
        "external-prior",
        35.0,
        "world:x",
        parent_event_ids=(prior_boundary.event_id,),
    )
    consistency.register_boundary(prior_boundary)
    ledger.register_external(prior_external)
    prior_resolution = consistency.observe_external(prior_external)
    assert prior_resolution.status == "externally-consistent"

    return (
        A01TransientCreditBridge(expectation, consistency, ledger),
        consistency,
        ledger,
    )


def _run(target: str):
    bridge, consistency, ledger = _prepared_bridge()
    merged = _boundary(
        "boundary-merged",
        40.0,
        source_proposal_ids=("proposal-b", "proposal-c"),
    )
    external = _external(
        "external-probe",
        45.0,
        target,
        parent_event_ids=(merged.event_id,),
    )
    consistency.register_boundary(merged)
    ledger.register_external(external)
    return probe_merged_lineage_credit(
        bridge,
        boundary=merged,
        external=external,
    )


def test_p4_development_probe_observes_exact_match_credit_applied_en_bloc() -> None:
    observation = _run("world:x")

    assert observation.status == A01CausalCreditStatus.EXACT_MATCH.value
    assert observation.source_proposal_ids == ("proposal-b", "proposal-c")
    assert observation.credited_path_ids == ("local:A->B", "local:A->C")
    assert observation.changed_path_ids == observation.credited_path_ids
    assert observation.credit_scope == "all-resolved-paths"
    assert dict(observation.path_reliability_before) == {
        "local:A->B": 0.5,
        "local:A->C": 0.5,
    }
    assert dict(observation.path_reliability_after) == pytest.approx(
        {
            "local:A->B": 2.0 / 3.0,
            "local:A->C": 2.0 / 3.0,
        }
    )
    assert observation.development_only is True
    assert observation.formal_p4_result is None


def test_p4_development_probe_observes_contradiction_credit_applied_en_bloc() -> None:
    observation = _run("world:y")

    assert observation.status == A01CausalCreditStatus.EXACT_CONTRADICTION.value
    assert observation.changed_path_ids == observation.credited_path_ids
    assert observation.credit_scope == "all-resolved-paths"
    assert dict(observation.path_reliability_after) == pytest.approx(
        {
            "local:A->B": 1.0 / 3.0,
            "local:A->C": 1.0 / 3.0,
        }
    )
    assert observation.formal_p4_result is None


def test_p4_development_probe_rejects_singleton_ancestry() -> None:
    bridge, consistency, ledger = _prepared_bridge()
    boundary = _boundary(
        "boundary-singleton",
        40.0,
        source_proposal_ids=("proposal-b",),
    )
    external = _external(
        "external-singleton",
        45.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    consistency.register_boundary(boundary)
    ledger.register_external(external)

    with pytest.raises(ValueError, match="requires plural source ancestry"):
        probe_merged_lineage_credit(bridge, boundary=boundary, external=external)


def test_p4_development_probe_rejects_fallback_pairing() -> None:
    bridge, consistency, ledger = _prepared_bridge()
    boundary = _boundary(
        "boundary-fallback",
        40.0,
        source_proposal_ids=("proposal-b", "proposal-c"),
    )
    external = _external("external-fallback", 45.0, "world:x")
    consistency.register_boundary(boundary)
    ledger.register_external(external)

    with pytest.raises(ValueError, match="requires exact-parent evidence"):
        probe_merged_lineage_credit(bridge, boundary=boundary, external=external)
