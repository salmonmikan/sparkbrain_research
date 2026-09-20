from __future__ import annotations

from sparkbrain.v05 import (
    ActionPolicyConfig,
    ActivityPattern,
    AssemblyActionPolicy,
    AssemblyPredictor,
    TemporalAssemblyMemory,
    pattern_similarity,
)


def _pattern(
    pattern_id: str,
    ordered_units: tuple[int, ...],
    relative_bins: tuple[int, ...],
) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=pattern_id,
        start_ms=0.0,
        end_ms=float(relative_bins[-1]),
        ordered_units=ordered_units,
        relative_bins=relative_bins,
        unit_ids=tuple(sorted(set(ordered_units))),
        spike_count=len(ordered_units),
        source_cascade_id="synthetic",
        source_kind="internal_reservoir",
    )


def test_partial_assembly_function_is_matched_by_fixed_nearest_neighbor_lookup() -> None:
    full = _pattern("full", (10, 11, 12, 13), (0, 2, 4, 6))
    partial = _pattern("partial", (10, 12, 13), (0, 4, 6))
    scrambled = _pattern("scrambled", (13, 12, 10), (0, 4, 6))

    memory = TemporalAssemblyMemory()
    mature = None
    for index in range(3):
        mature = memory.observe(
            full,
            time_ms=float(index),
            episode_id=f"seed-{index}",
            learn=True,
        )
    assert mature is not None
    assert mature.mature

    predictor = AssemblyPredictor()
    predictor.observe(mature, "future-X")

    policy = AssemblyActionPolicy(ActionPolicyConfig(exploration_visits=0))
    learned_action = policy.choose(mature, explore=False)
    assert learned_action.action == "action-0"
    policy.reward(1.0)

    partial_activation = memory.observe(
        partial,
        time_ms=10.0,
        episode_id="partial-probe",
        learn=False,
    )
    assert partial_activation is not None
    assert partial_activation.mature
    assert partial_activation.assembly_id == mature.assembly_id

    partial_prediction = predictor.predict(partial_activation)
    partial_action = policy.choose(partial_activation, explore=False)
    assert partial_prediction.value == "future-X"
    assert partial_prediction.confidence == 1.0
    assert partial_action.action == "action-0"

    threshold = memory.config.similarity_threshold
    ordinary_similarity = pattern_similarity(full, partial)
    ordinary_accepts = ordinary_similarity >= threshold
    ordinary_prediction = "future-X" if ordinary_accepts else None
    ordinary_action = "action-0" if ordinary_accepts else "withhold"

    assert ordinary_accepts
    assert ordinary_prediction == partial_prediction.value
    assert ordinary_action == partial_action.action

    scrambled_activation = memory.observe(
        scrambled,
        time_ms=11.0,
        episode_id="scrambled-probe",
        learn=False,
    )
    ordinary_scrambled_accepts = pattern_similarity(full, scrambled) >= threshold
    assert scrambled_activation is None
    assert not ordinary_scrambled_accepts
