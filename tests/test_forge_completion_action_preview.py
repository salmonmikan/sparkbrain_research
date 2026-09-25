from forge_prototypes.completion_action_preview import (
    CompletionActionPreview,
    CompletionActionPreviewConfig,
)
from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory
from sparkbrain.v05.action import AssemblyActionPolicy


def _pattern(name: str, units: tuple[int, ...], bins: tuple[int, ...]) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=name,
        start_ms=0.0,
        end_ms=float(bins[-1]),
        ordered_units=units,
        relative_bins=bins,
        unit_ids=tuple(sorted(set(units))),
        spike_count=len(units),
    )


def _mature(
    memory: TemporalAssemblyMemory,
    pattern: ActivityPattern,
    prefix: str,
):
    memory.observe(pattern, time_ms=0.0, episode_id=f"{prefix}-1")
    activation = memory.observe(pattern, time_ms=10.0, episode_id=f"{prefix}-2")
    assert activation is not None
    assert activation.mature is True
    return activation


def _set_scores(
    policy: AssemblyActionPolicy,
    assembly_id: str,
    *,
    action_0: float,
    action_1: float,
    withhold: float,
) -> None:
    policy.scores[assembly_id] = {
        "action-0": action_0,
        "action-1": action_1,
        "withhold": withhold,
    }


def test_weak_partial_cue_previews_learned_action_without_policy_mutation() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    activation = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _set_scores(
        policy,
        activation.assembly_id,
        action_0=0.70,
        action_1=0.10,
        withhold=0.0,
    )
    policy.visits[activation.assembly_id] = 4
    policy.pending = (activation.assembly_id, "action-1")

    cue = _pattern("partial-a", (1, 3), (0, 2))
    assert memory.observe(
        cue,
        time_ms=cue.end_ms,
        episode_id="native-check",
        learn=False,
    ) is None

    memory_before = memory.state_dict()
    policy_before = policy.state_dict()
    result = CompletionActionPreview(memory, policy).preview(cue)

    assert result.route == "completion"
    assert result.assembly_id == activation.assembly_id
    assert result.action == "action-0"
    assert result.action_margin == 0.60
    assert round(result.confidence, 6) == 0.60
    assert result.completion is not None
    assert result.completion.missing_unit_ids == (2, 4)
    assert memory.state_dict() == memory_before
    assert policy.state_dict() == policy_before


def test_naive_policy_choose_is_not_a_read_only_preview() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    activation = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _set_scores(
        policy,
        activation.assembly_id,
        action_0=0.70,
        action_1=0.10,
        withhold=0.0,
    )
    before = policy.state_dict()

    chosen = policy.choose(activation, explore=False)

    assert chosen.action == "action-0"
    assert policy.state_dict() != before
    assert policy.visits[activation.assembly_id] == 1
    assert policy.pending == (activation.assembly_id, "action-0")


def test_ambiguous_completion_abstains_without_action_state_mutation() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    first = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    second = _mature(
        memory,
        _pattern("full-b", (1, 5, 3, 6), (0, 1, 2, 3)),
        "b",
    )
    _set_scores(policy, first.assembly_id, action_0=0.8, action_1=0.1, withhold=0.0)
    _set_scores(policy, second.assembly_id, action_0=0.1, action_1=0.8, withhold=0.0)
    before = policy.state_dict()

    result = CompletionActionPreview(memory, policy).preview(
        _pattern("ambiguous", (1, 3), (0, 2))
    )

    assert result.route == "abstain"
    assert result.action is None
    assert result.reason == "ambiguous_candidate"
    assert result.completion is not None
    assert result.completion.margin == 0.0
    assert policy.state_dict() == before


def test_action_tie_abstains_even_when_completion_is_unique() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    activation = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _set_scores(
        policy,
        activation.assembly_id,
        action_0=0.4,
        action_1=0.4,
        withhold=0.0,
    )
    before = policy.state_dict()

    result = CompletionActionPreview(
        memory,
        policy,
        config=CompletionActionPreviewConfig(min_action_margin=0.05),
    ).preview(_pattern("partial-a", (1, 3), (0, 2)))

    assert result.route == "abstain"
    assert result.reason == "ambiguous_action"
    assert result.action is None
    assert result.action_margin == 0.0
    assert policy.state_dict() == before


def test_strong_partial_cue_uses_native_route_without_policy_mutation() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    activation = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _set_scores(
        policy,
        activation.assembly_id,
        action_0=0.60,
        action_1=0.10,
        withhold=0.0,
    )
    before = policy.state_dict()

    result = CompletionActionPreview(memory, policy).preview(
        _pattern("strong-partial", (1, 2, 3), (0, 1, 2))
    )

    assert result.route == "native"
    assert result.action == "action-0"
    assert result.completion is None
    assert round(result.confidence, 6) == 0.80
    assert policy.state_dict() == before


def test_missing_action_history_abstains() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    policy = AssemblyActionPolicy()
    _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )

    result = CompletionActionPreview(memory, policy).preview(
        _pattern("partial-a", (1, 3), (0, 2))
    )

    assert result.route == "abstain"
    assert result.action is None
    assert result.reason == "no_action_history"
