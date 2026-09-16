from __future__ import annotations

import json

import pytest

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
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
