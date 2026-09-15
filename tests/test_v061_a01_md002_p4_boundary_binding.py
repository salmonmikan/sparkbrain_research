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
    A01LocalTemporalExpectation,
    A01TransientCreditBridge,
)
from sparkbrain.v061_a01.md002_p4_credit_probe import probe_merged_lineage_credit


def _boundary(
    source_ids: tuple[str, ...],
    *,
    event_id: str = "boundary-same-id",
    time_ms: float = 40.0,
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
        source_proposal_ids=source_ids,
        generation_depth=1,
        source_state_hash="state:shared",
    )


def _proposal(
    proposal_id: str,
    target: str,
    *,
    local_path_ids: tuple[str, ...] | None = None,
) -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id=proposal_id,
        created_at_ms=10.0,
        target=target,
        predicted_arrival_ms=20.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="state:shared",
        local_path_ids=local_path_ids or (f"local:A->{target}",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )


def _expectation() -> A01LocalTemporalExpectation:
    expectation = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    expectation.observe_external_transition(
        RuntimePulse("train-a", 0.0, "A", 1.0, 1, EventOrigin.EXTERNAL),
        RuntimePulse("train-b", 5.0, "B", 1.0, 1, EventOrigin.EXTERNAL),
    )
    expectation.observe_external_transition(
        RuntimePulse("train-a2", 10.0, "A", 1.0, 1, EventOrigin.EXTERNAL),
        RuntimePulse("train-c", 15.0, "C", 1.0, 1, EventOrigin.EXTERNAL),
    )
    return expectation


def _ledger() -> ProvenanceLedger:
    ledger = ProvenanceLedger()
    ledger.register_proposal(_proposal("proposal-b", "B"))
    ledger.register_proposal(_proposal("proposal-c", "C"))
    return ledger


def test_p4_probe_rejects_boundary_payload_mismatch() -> None:
    expectation = _expectation()
    ledger = _ledger()
    consistency = UntypedBoundaryConsistency(ledger)
    registered = _boundary(("proposal-b",))
    supplied = _boundary(("proposal-b", "proposal-c"))
    consistency.register_boundary(registered)
    external = RuntimePulse(
        "external-mismatch",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(registered.event_id,),
    )
    ledger.register_external(external)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)

    with pytest.raises(ValueError, match="must match registered pending boundary"):
        probe_merged_lineage_credit(bridge, boundary=supplied, external=external)


def test_p4_probe_rejects_reused_external_evidence() -> None:
    expectation = _expectation()
    ledger = _ledger()
    consistency = UntypedBoundaryConsistency(ledger)
    first = _boundary(
        ("proposal-b", "proposal-c"),
        event_id="boundary-a",
        time_ms=41.0,
    )
    second = _boundary(
        ("proposal-b", "proposal-c"),
        event_id="boundary-b",
        time_ms=40.0,
    )
    consistency.register_boundary(first)
    consistency.register_boundary(second)
    external = RuntimePulse(
        "external-shared",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(first.event_id,),
    )
    ledger.register_external(external)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)

    probe_merged_lineage_credit(bridge, boundary=first, external=external)

    second_external = RuntimePulse(
        "external-shared",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(second.event_id,),
    )
    with pytest.raises(ValueError, match="external evidence must not be reused"):
        probe_merged_lineage_credit(
            bridge,
            boundary=second,
            external=second_external,
        )


def test_p4_probe_rejects_ambiguous_exact_parent_before_mutation() -> None:
    expectation = _expectation()
    ledger = _ledger()
    consistency = UntypedBoundaryConsistency(ledger)
    first = _boundary(
        ("proposal-b", "proposal-c"),
        event_id="boundary-a",
        time_ms=41.0,
    )
    second = _boundary(
        ("proposal-b", "proposal-c"),
        event_id="boundary-b",
        time_ms=40.0,
    )
    consistency.register_boundary(first)
    consistency.register_boundary(second)
    external = RuntimePulse(
        "external-ambiguous",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(first.event_id, second.event_id),
    )
    ledger.register_external(external)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)

    with pytest.raises(ValueError, match="one unambiguous selected exact parent"):
        probe_merged_lineage_credit(bridge, boundary=second, external=external)

    pending = consistency.state_dict()["pending"]
    assert set(pending) == {first.event_id, second.event_id}
    assert consistency.resolutions == []


def test_p4_probe_validates_unknown_proposal_before_consuming_boundary() -> None:
    expectation = _expectation()
    ledger = _ledger()
    consistency = UntypedBoundaryConsistency(ledger)
    boundary = _boundary(("proposal-b", "proposal-missing"))
    consistency.register_boundary(boundary)
    external = RuntimePulse(
        "external-unknown-proposal",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)

    with pytest.raises(ValueError, match="references unknown proposal"):
        probe_merged_lineage_credit(bridge, boundary=boundary, external=external)

    assert boundary.event_id in consistency.state_dict()["pending"]
    assert consistency.resolutions == []


def test_p4_probe_validates_unknown_path_before_consuming_boundary() -> None:
    expectation = _expectation()
    ledger = ProvenanceLedger()
    ledger.register_proposal(_proposal("proposal-b", "B"))
    ledger.register_proposal(
        _proposal(
            "proposal-z",
            "Z",
            local_path_ids=("local:A->Z",),
        )
    )
    consistency = UntypedBoundaryConsistency(ledger)
    boundary = _boundary(("proposal-b", "proposal-z"))
    consistency.register_boundary(boundary)
    external = RuntimePulse(
        "external-unknown-path",
        45.0,
        "world:x",
        1.0,
        1,
        EventOrigin.EXTERNAL,
        parent_event_ids=(boundary.event_id,),
    )
    ledger.register_external(external)
    bridge = A01TransientCreditBridge(expectation, consistency, ledger)

    with pytest.raises(ValueError, match="references unknown local paths"):
        probe_merged_lineage_credit(bridge, boundary=boundary, external=external)

    assert boundary.event_id in consistency.state_dict()["pending"]
    assert consistency.resolutions == []
