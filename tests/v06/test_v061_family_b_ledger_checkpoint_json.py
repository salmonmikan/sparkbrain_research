from __future__ import annotations

import json

import pytest

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    DistributedFieldTraceState,
    ExternalEvidenceLedger,
)


def test_consumed_evidence_ids_restore_after_json_checkpoint_round_trip() -> None:
    ledger = ExternalEvidenceLedger()
    ledger.consume_once("ev:json-checkpoint")

    decoded = json.loads(json.dumps(ledger.export_consumed_ids()))
    restored = ExternalEvidenceLedger.from_consumed_ids(decoded)

    assert decoded == ["ev:json-checkpoint"]
    assert restored.export_consumed_ids() == ("ev:json-checkpoint",)
    with pytest.raises(ValueError, match="external evidence ID already consumed"):
        restored.consume_once("ev:json-checkpoint")


def test_field_carrier_json_round_trip_restores_immutable_vectors() -> None:
    state = DistributedFieldTraceState.zeros().deposit_local_activity(
        (1.0, 0.0, 0.0, 0.0)
    )
    state = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:carrier-json",
        evidence_ledger=ExternalEvidenceLedger(),
    )

    decoded = json.loads(json.dumps(state.export_field_carrier()))
    restored = DistributedFieldTraceState.from_field_carrier(decoded)

    assert isinstance(restored.eligibility, tuple)
    assert isinstance(restored.credit, tuple)
    assert restored.export_field_carrier() == state.export_field_carrier()

    decoded[1][0] = -999.0
    assert restored.credit[0] == state.credit[0]
