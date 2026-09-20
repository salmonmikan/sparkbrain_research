from sparkbrain.v05.action import AssemblyActionPolicy
from sparkbrain.v05.contracts import AssemblyActivation


def _mature_activation() -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id="assembly-eval",
        pattern_id="pattern-eval",
        time_ms=10.0,
        similarity=1.0,
        occurrences=3,
        episode_count=3,
        mature=True,
        unit_ids=(1, 2, 3),
        suppressed=False,
    )


def test_nonlearning_action_visit_carryover_shifts_next_exploration_slot() -> None:
    activation = _mature_activation()
    control = AssemblyActionPolicy()
    treated = AssemblyActionPolicy()

    control_training = control.choose(activation, explore=True)
    treated_evaluation = treated.choose(activation, explore=False)
    treated_training = treated.choose(activation, explore=True)

    assert control_training.action == "action-0"
    assert control.visits[activation.assembly_id] == 1

    assert treated_evaluation.action == "action-0"
    assert treated_training.action == "action-1"
    assert treated.visits[activation.assembly_id] == 2

    # Fixed ordinary comparator: the non-exploratory call consumes one visit,
    # so the resumed exploratory call uses actions[1 % len(actions)].
    assert treated_training.action == treated.config.actions[1 % len(treated.config.actions)]
    assert treated_training.action != control_training.action
