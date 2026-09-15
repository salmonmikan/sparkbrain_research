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


def _boundary(source_ids: tuple[str, ...]) -> BoundaryEvent:
    return BoundaryEvent(
        event_id="boundary-same-id",
        time_ms=40.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark:boundary-same-id",
        source_unit_id=0,
        source_proposal_ids=source_ids,
        generation_depth=1,
        source_state_hash="state:shared",
    )


def test_p4_probe_rejects_boundary_payload_mismatch() -> None:
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
    ledger = ProvenanceLedger()
    for proposal_id, target in (("proposal-b", "B"), ("proposal-c", "C")):
        ledger.register_proposal(
            EndogenousPulseProposal(
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
        )
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
