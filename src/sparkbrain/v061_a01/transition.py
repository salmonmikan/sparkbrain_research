from __future__ import annotations

from typing import Any

from sparkbrain.v06.foundation import ProvenanceLedger, validate_runtime_mapping
from sparkbrain.v06.local_transition import (
    LocalPathAdaptation,
    PendingLocalTransition,
    SparseLocalTransitionAdaptation,
    SparseTransitionConfig,
)

from .credit_bridge import A01LocalTemporalExpectation


class A01SparseLocalTransitionAdaptation(SparseLocalTransitionAdaptation):
    """G2 restore path that retains A01-augmented G1 local state."""

    @classmethod
    def from_state_dict(
        cls,
        value: dict[str, Any],
        *,
        ledger: ProvenanceLedger,
    ) -> A01SparseLocalTransitionAdaptation:
        validate_runtime_mapping(value, path="g2.local_transition")
        model = cls(
            A01LocalTemporalExpectation.from_state_dict(value["expectation"]),
            ledger,
            SparseTransitionConfig(**value["config"]),
        )
        model._paths = {
            str(path_id): LocalPathAdaptation.from_state_dict(state)
            for path_id, state in value["paths"].items()
        }
        pending_rows = {
            str(proposal_id): PendingLocalTransition(**pending)
            for proposal_id, pending in value["pending"].items()
        }
        for proposal_id, pending in pending_rows.items():
            if proposal_id not in ledger.proposals:
                raise ValueError(
                    "restoring pending A01 G2 state requires a matching provenance ledger"
                )
            if pending.chain_id not in ledger.chains:
                raise ValueError(
                    "restoring pending A01 G2 state requires a matching provenance ledger"
                )
            if pending.eligibility_id not in ledger.eligibilities:
                raise ValueError(
                    "restoring pending A01 G2 state requires a matching provenance ledger"
                )
        model._pending = pending_rows
        model.prepared_count = int(value["prepared_count"])
        model.confirmed_count = int(value["confirmed_count"])
        model.contradicted_count = int(value["contradicted_count"])
        return model
