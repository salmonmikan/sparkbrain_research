"""EXPLORATORY / NON_EVIDENTIARY.

Bounded SUB Discovery probe for CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01.
The fixed contract lives in
analysis/exploratory/v05_presemantic_function_transfer/PROSPECTIVE.md.
"""

from __future__ import annotations

from sparkbrain.v05 import (
    ActivityPattern,
    AssemblyConfig,
    AssemblyPredictor,
    TemporalAssemblyMemory,
    pattern_similarity,
)


def _pattern(name: str, ordered: tuple[int, ...]) -> ActivityPattern:
    bins = (0, 1, 2, 3)
    return ActivityPattern(
        name,
        0.0,
        3.0,
        ordered,
        bins,
        tuple(sorted(set(ordered))),
        len(ordered),
    )


def test_presemantic_cluster_function_transfer_reduces_to_fixed_prototype_lookup() -> None:
    prototype = _pattern("prototype-a", (1, 2, 3, 4))
    labeled_exemplar = _pattern("labeled-b", (1, 1, 2, 3))
    transfer_target = _pattern("target-c", (1, 1, 3, 4))

    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=3))
    predictor = AssemblyPredictor()
    threshold = memory.config.similarity_threshold

    # Construction constraints fixed prospectively.
    prototype_to_labeled = pattern_similarity(prototype, labeled_exemplar)
    prototype_to_target = pattern_similarity(prototype, transfer_target)
    labeled_to_target = pattern_similarity(labeled_exemplar, transfer_target)
    assert prototype_to_labeled >= threshold
    assert prototype_to_target >= threshold
    assert labeled_to_target < threshold

    # Form an anonymous pre-semantic Assembly before attaching any outcome.
    mature = None
    for index in range(3):
        mature = memory.observe(
            prototype,
            time_ms=float(index),
            episode_id=f"presemantic-{index}",
        )
    assert mature is not None and mature.mature
    assert predictor.counts == {}

    # A later cluster member receives the first semantic association.
    labeled_activation = memory.observe(
        labeled_exemplar,
        time_ms=3.0,
        episode_id="labeled-exemplar",
        learn=False,
    )
    assert labeled_activation is not None and labeled_activation.mature
    predictor.observe(labeled_activation, "future-X")

    # A different, never-labeled member inherits the Assembly-level function.
    target_activation = memory.observe(
        transfer_target,
        time_ms=4.0,
        episode_id="transfer-target",
        learn=False,
    )
    assert target_activation is not None and target_activation.mature
    assert target_activation.assembly_id == labeled_activation.assembly_id
    prediction = predictor.predict(target_activation)
    assert prediction.next_event == "future-X"
    assert prediction.confidence == 1.0

    # Direct exemplar similarity cannot explain the transfer, but the fixed
    # pre-semantic prototype cluster plus ordinary label lookup can.
    assert labeled_to_target < threshold
    assert prototype_to_target >= threshold
    ordinary_cluster_lookup_prediction = "future-X" if prototype_to_target >= threshold else None
    assert ordinary_cluster_lookup_prediction == prediction.next_event
