"""EXPLORATORY / NON_EVIDENTIARY delayed-outcome credit-slot probe."""

from __future__ import annotations

from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.contracts import AssemblyActivation


def _activation(assembly_id: str, unit_id: int) -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id=assembly_id,
        pattern_id=f"pattern-{assembly_id}",
        time_ms=float(unit_id),
        similarity=1.0,
        occurrences=3,
        episode_count=3,
        mature=True,
        unit_ids=(unit_id,),
    )


def _make_pending(brain: IntegratedV05Brain, activation: AssemblyActivation) -> None:
    brain.pending_activation = activation
    brain.pending_action = brain.action_policy.choose(activation, explore=False)


def test_delayed_outcome_is_rebound_to_latest_pending_identity() -> None:
    activation_a = _activation("assembly-A", 101)
    activation_b = _activation("assembly-B", 102)

    immediate = IntegratedV05Brain()
    _make_pending(immediate, activation_a)
    immediate.learn_outcome(next_event="event-A", reward=1.0)

    assert immediate.predictor.counts == {"assembly-A": {"event-A": 1}}
    assert immediate.action_policy.scores["assembly-A"]["action-0"] == 0.30

    deferred = IntegratedV05Brain()
    _make_pending(deferred, activation_a)
    _make_pending(deferred, activation_b)
    deferred.learn_outcome(next_event="event-A", reward=1.0)

    assert deferred.predictor.counts == {"assembly-B": {"event-A": 1}}
    assert "assembly-A" not in deferred.predictor.counts
    assert deferred.action_policy.scores["assembly-A"]["action-0"] == 0.0
    assert deferred.action_policy.scores["assembly-B"]["action-0"] == 0.30
