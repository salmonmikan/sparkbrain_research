from forge_prototypes.assembly_completion import AssemblyCompletionProbe
from forge_prototypes.completion_predictor_bridge import CompletionPredictorBridge
from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory
from sparkbrain.v05.prediction import AssemblyPredictor


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


def _train_predictor(
    predictor: AssemblyPredictor,
    activation,
    primary: str,
    secondary: str | None = None,
) -> None:
    predictor.observe(activation, primary)
    predictor.observe(activation, primary)
    if secondary is not None:
        predictor.observe(activation, secondary)


def test_weak_partial_cue_recovers_existing_prediction_without_mutation() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    predictor = AssemblyPredictor()
    full = _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3))
    activation = _mature(memory, full, "a")
    _train_predictor(predictor, activation, "next-x", "next-y")

    cue = _pattern("partial-a", (1, 3), (0, 2))
    assert memory.observe(
        cue,
        time_ms=cue.end_ms,
        episode_id="native-check",
        learn=False,
    ) is None

    memory_before = memory.state_dict()
    predictor_before = predictor.state_dict()
    result = CompletionPredictorBridge(memory, predictor).predict(cue)

    assert result.route == "completion"
    assert result.assembly_id == "assembly-0001"
    assert result.prediction.value == "next-x"
    assert round(result.prediction.confidence, 6) == round(2 / 3, 6)
    assert result.completion is not None
    assert result.completion.missing_unit_ids == (2, 4)
    assert memory.state_dict() == memory_before
    assert predictor.state_dict() == predictor_before


def test_ambiguous_weak_cue_abstains_instead_of_using_tie_break_lookup() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    predictor = AssemblyPredictor()

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
    _train_predictor(predictor, first, "next-a")
    _train_predictor(predictor, second, "next-b")

    cue = _pattern("ambiguous", (1, 3), (0, 2))
    result = CompletionPredictorBridge(memory, predictor).predict(cue)

    assert result.route == "abstain"
    assert result.reason == "ambiguous_candidate"
    assert result.prediction.value is None
    assert result.completion is not None
    assert result.completion.margin == 0.0

    lowered = TemporalAssemblyMemory(
        AssemblyConfig(similarity_threshold=0.55, mature_episodes=2)
    )
    _mature(
        lowered,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _mature(
        lowered,
        _pattern("full-b", (1, 5, 3, 6), (0, 1, 2, 3)),
        "b",
    )
    naive = lowered.observe(
        cue,
        time_ms=cue.end_ms,
        episode_id="naive-lowered-threshold",
        learn=False,
    )
    assert naive is not None
    assert naive.assembly_id == "assembly-0001"


def test_stronger_partial_cue_stays_on_native_path() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    predictor = AssemblyPredictor()
    activation = _mature(
        memory,
        _pattern("full-a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _train_predictor(predictor, activation, "next-x")

    cue = _pattern("strong-partial", (1, 2, 3), (0, 1, 2))
    result = CompletionPredictorBridge(
        memory,
        predictor,
        completion=AssemblyCompletionProbe(memory),
    ).predict(cue)

    assert result.route == "native"
    assert result.assembly_id == "assembly-0001"
    assert result.prediction.value == "next-x"
    assert result.completion is None
