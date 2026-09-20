"""EXPLORATORY / NON_EVIDENTIARY.

Bounded SUB Discovery probe for CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01.
The fixed contract and terminal/API semantic preflight live in
analysis/exploratory/v05_context_conditioned_prediction/PROSPECTIVE.md.
"""

from __future__ import annotations

from sparkbrain.v05 import AssemblyActivation, AssemblyPredictor


def _activation(assembly_id: str, unit_id: int) -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id=assembly_id,
        pattern_id=f"pattern-{assembly_id}",
        time_ms=0.0,
        similarity=1.0,
        occurrences=3,
        episode_count=3,
        mature=True,
        unit_ids=(unit_id,),
        suppressed=False,
    )


def test_context_conditioned_prediction_reduces_to_current_assembly_lookup() -> None:
    predictor = AssemblyPredictor()
    context_a = _activation("assembly-A", 1)
    context_b = _activation("assembly-B", 2)
    current_x = _activation("assembly-X", 3)

    # Prospectively fixed balanced training schedule. The context call is the
    # immediately preceding native prediction-component exposure; only X is
    # outcome-associated.
    for _ in range(4):
        predictor.predict(context_a)
        predictor.observe(current_x, "future-A")
    for _ in range(4):
        predictor.predict(context_b)
        predictor.observe(current_x, "future-B")

    counts = predictor.state_dict()["counts"]
    assert counts == {"assembly-X": {"future-A": 4, "future-B": 4}}

    # The fixed ordinary comparator uses the repository predictor's exact
    # current-assembly table and deterministic tie behavior over sorted labels.
    x_table = counts["assembly-X"]
    ordinary_value = max(sorted(x_table), key=lambda item: x_table[item])
    assert ordinary_value == "future-A"

    state_before_a = predictor.state_dict()
    predictor.predict(context_a)
    assert predictor.state_dict() == state_before_a
    x_after_a = predictor.predict(current_x)
    assert predictor.state_dict() == state_before_a

    state_before_b = predictor.state_dict()
    predictor.predict(context_b)
    assert predictor.state_dict() == state_before_b
    x_after_b = predictor.predict(current_x)
    assert predictor.state_dict() == state_before_b

    # Prospectively bound terminal: FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP_EXPLAINS.
    assert x_after_a.assembly_id == "assembly-X"
    assert x_after_b.assembly_id == "assembly-X"
    assert x_after_a.value == ordinary_value
    assert x_after_b.value == ordinary_value
    assert x_after_a.value == x_after_b.value == "future-A"
    assert x_after_a.confidence == x_after_b.confidence == 0.5
