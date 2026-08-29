from __future__ import annotations

import pytest

from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import (
    SparseLocalTransitionAdaptation,
    SparseTransitionConfig,
)


def pulse(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    magnitude: float = 0.8,
    polarity: int = 1,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(event_id, time_ms, target, magnitude, polarity, origin)


def trained() -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=2, minimum_confidence=0.1)
    )
    model.observe_external_transition(
        pulse("a1", 0, "unit:1"),
        pulse("b1", 5, "unit:2", magnitude=0.6),
    )
    model.observe_external_transition(
        pulse("a2", 20, "unit:1"),
        pulse("b2", 25, "unit:2", magnitude=0.8),
    )
    return model


def test_prepare_registers_proposal_chain_and_uncommitted_eligibility() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    rows = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)
    assert len(rows) == 1
    row = rows[0]
    assert row.proposal.proposal_id in ledger.proposals
    assert row.chain_id in ledger.chains
    assert ledger.eligibilities[row.eligibility_id].committed is False
    assert ledger.committed_positive_updates == 0
    assert g2.path_confidence_scale(row.path_id) == 1.0


def test_proposal_generation_alone_does_not_adapt_path() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    before = g2.state_hash()
    rows = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)
    assert rows
    assert g2.confirmed_count == 0
    assert g2.state_dict()["paths"] == {}
    assert g2.state_hash() != before


def test_matching_external_event_commits_and_strengthens_only_local_path() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    row = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)[0]
    result = g2.resolve_external(
        row.proposal.proposal_id,
        pulse("external", 106, "unit:2", magnitude=0.8),
    )
    assert result.matched is True
    assert result.confidence_after > result.confidence_before
    assert ledger.committed_positive_updates == 1
    assert ledger.external_observation_count == 1
    assert g2.confirmed_count == 1


def test_endogenous_event_cannot_resolve_or_strengthen_path() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    row = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)[0]
    with pytest.raises(ValueError, match="external observation"):
        g2.resolve_external(
            row.proposal.proposal_id,
            pulse("endo:x", 105, "unit:2", origin=EventOrigin.ENDOGENOUS_CONFIRMED),
        )
    assert g2.path_confidence_scale(row.path_id) == 1.0
    assert ledger.committed_positive_updates == 0


def test_wrong_external_target_reduces_path_reliability_without_positive_commit() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    row = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)[0]
    result = g2.resolve_external(row.proposal.proposal_id, pulse("external", 105, "unit:9"))
    assert result.matched is False
    assert result.confidence_after < result.confidence_before
    assert ledger.committed_positive_updates == 0
    assert g2.contradicted_count == 1


def test_confirmed_timing_and_magnitude_corrections_affect_next_proposal() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(
        trained(), ledger, SparseTransitionConfig(learning_rate=0.5)
    )
    first = g2.prepare(pulse("source-1", 100, "unit:1"), origin_state_hash="s" * 64)[0]
    g2.resolve_external(
        first.proposal.proposal_id,
        pulse("external-1", 107, "unit:2", magnitude=0.9),
    )
    second = g2.prepare(pulse("source-2", 200, "unit:1"), origin_state_hash="t" * 64)[0]
    assert second.proposal.predicted_arrival_ms == pytest.approx(206.0)
    assert second.proposal.magnitude == pytest.approx(0.8)
    assert g2.path_confidence_scale(second.path_id) > 1.0
    assert second.proposal.confidence >= first.proposal.confidence


def test_sparse_paths_remain_directional() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    assert g2.prepare(pulse("reverse", 100, "unit:2"), origin_state_hash="s" * 64) == ()
    assert g2.state_dict()["paths"] == {}


def test_state_round_trip_after_resolution_is_deterministic() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    row = g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)[0]
    g2.resolve_external(row.proposal.proposal_id, pulse("external", 105, "unit:2", magnitude=0.7))
    state = g2.state_dict()
    restored = SparseLocalTransitionAdaptation.from_state_dict(state, ledger=ProvenanceLedger())
    assert restored.state_dict() == state
    assert restored.state_hash() == g2.state_hash()
    assert "assembly_id" not in str(state).lower()
    assert "motif_id" not in str(state).lower()


def test_pending_budget_fails_closed_before_partial_registration() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(
        trained(), ledger, SparseTransitionConfig(maximum_pending=1)
    )
    first = g2.prepare(pulse("source-1", 100, "unit:1"), origin_state_hash="s" * 64)
    assert len(first) == 1
    before = ledger.state_hash()
    with pytest.raises(RuntimeError, match="budget"):
        g2.prepare(pulse("source-2", 200, "unit:1"), origin_state_hash="t" * 64)
    assert ledger.state_hash() == before


def test_pending_transition_expires_without_path_adaptation() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    row = g2.prepare(
        pulse("source", 100, "unit:1"),
        origin_state_hash="s" * 64,
    )[0]
    expired = g2.expire_pending(row.proposal.valid_until_ms + 1)
    assert expired == (row.proposal.proposal_id,)
    assert g2.state_dict()["pending"] == {}
    assert g2.state_dict()["paths"] == {}
    assert ledger.committed_positive_updates == 0


def test_pending_state_restore_requires_matching_provenance_ledger() -> None:
    ledger = ProvenanceLedger()
    g2 = SparseLocalTransitionAdaptation(trained(), ledger)
    g2.prepare(pulse("source", 100, "unit:1"), origin_state_hash="s" * 64)
    with pytest.raises(ValueError, match="matching provenance ledger"):
        SparseLocalTransitionAdaptation.from_state_dict(
            g2.state_dict(),
            ledger=ProvenanceLedger(),
        )
