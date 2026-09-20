"""EXPLORATORY / NON_EVIDENTIARY delayed action-responsibility probe."""

from sparkbrain.v05.action import ActionPolicyConfig, AssemblyActionPolicy
from sparkbrain.v05.contracts import AssemblyActivation


def _activation(assembly_id: str, pattern_id: str, time_ms: float) -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id=assembly_id,
        pattern_id=pattern_id,
        time_ms=time_ms,
        similarity=1.0,
        occurrences=3,
        episode_count=3,
        mature=True,
        unit_ids=(1, 2, 3),
        suppressed=False,
    )


def _policy() -> AssemblyActionPolicy:
    return AssemblyActionPolicy(ActionPolicyConfig(exploration_visits=0))


def test_delayed_reward_reduces_to_one_slot_last_action_pending_register() -> None:
    """A later eligible choice overwrites responsibility for a delayed scalar reward."""
    assembly_a = _activation("assembly-A", "pattern-A", 1.0)
    assembly_b = _activation("assembly-B", "pattern-B", 2.0)

    immediate = _policy()
    immediate_a = immediate.choose(assembly_a, explore=False)
    assert immediate_a.action == "action-0"
    assert immediate.pending == ("assembly-A", "action-0")
    immediate.reward(1.0)
    assert immediate.scores["assembly-A"]["action-0"] == 0.30

    delayed = _policy()
    delayed_a = delayed.choose(assembly_a, explore=False)
    delayed_b = delayed.choose(assembly_b, explore=False)
    assert delayed_a.action == "action-0"
    assert delayed_b.action == "action-0"
    assert delayed.pending == ("assembly-B", "action-0")

    delayed.reward(1.0)

    observed = {
        "assembly-A": delayed.scores["assembly-A"]["action-0"],
        "assembly-B": delayed.scores["assembly-B"]["action-0"],
    }
    ordinary_last_pending_comparator = {
        "assembly-A": 0.0,
        "assembly-B": 0.30,
    }
    assert observed == ordinary_last_pending_comparator
