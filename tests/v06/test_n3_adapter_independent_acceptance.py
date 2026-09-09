"""Independent engineering acceptance; never invokes a development/world runner."""

from __future__ import annotations

import unittest
from copy import deepcopy

from sparkbrain.v061_a01.recurrent_adapter import N3CausalTrace

_case = unittest.TestCase()

PATHS = ("opaque-independent-71", "opaque-independent-19")


def test_independent_history_and_readout_are_live_and_inspection_is_pure():
    model = N3CausalTrace(PATHS)
    model.advance((PATHS[0],))
    model.observe_causal_evidence((PATHS[0],), matched=True)
    before = deepcopy(model.state_dict())
    reliability = model.causal_reliability(PATHS[0])
    assert reliability != 0.5
    for _ in range(3):
        assert model.causal_reliability(PATHS[0]) == reliability
        model.learned_state_dict()
        model.state_dict()
    assert model.state_dict() == before
    model.advance(())
    assert model.causal_reliability(PATHS[0]) != reliability


def test_independent_checkpoint_continuation_and_no_implicit_reset():
    model = N3CausalTrace(PATHS)
    model.advance((PATHS[0],))
    model.advance(())
    model.observe_causal_evidence((PATHS[0],), matched=False)
    restored = N3CausalTrace.from_state_dict(deepcopy(model.state_dict()))
    assert restored.state_dict() == model.state_dict()
    for active in ((PATHS[1],), (), (PATHS[0], PATHS[1])):
        restored.advance(active)
        model.advance(active)
        assert restored.state_dict() == model.state_dict()
        assert [restored.causal_reliability(p) for p in PATHS] == [
            model.causal_reliability(p) for p in PATHS
        ]


def test_independent_renaming_preserves_slot_semantics():
    renamed = ("z-independent", "a-independent")
    model = N3CausalTrace(PATHS)
    other = N3CausalTrace(renamed)
    for slots in ((0,), (), (1,), (0, 1), ()):
        model.advance(tuple(PATHS[i] for i in slots))
        other.advance(tuple(renamed[i] for i in slots))
    model.observe_causal_evidence((PATHS[1],), matched=False)
    other.observe_causal_evidence((renamed[1],), matched=False)
    assert [model.causal_reliability(p) for p in PATHS] == [
        other.causal_reliability(p) for p in renamed
    ]


def test_independent_unknown_and_duplicate_inputs_fail_without_mutation():
    model = N3CausalTrace(PATHS)
    for bad in (("not-registered",), (PATHS[0], PATHS[0])):
        before = deepcopy(model.state_dict())
        with _case.assertRaises((ValueError, KeyError)):
            model.advance(bad)
        assert model.state_dict() == before
        with _case.assertRaises((ValueError, KeyError)):
            model.observe_causal_evidence(bad, matched=True)
        assert model.state_dict() == before


def test_independent_extra_supervision_is_not_an_input():
    model = N3CausalTrace(PATHS)
    before = deepcopy(model.state_dict())
    with _case.assertRaises(TypeError):
        model.observe_causal_evidence((PATHS[0],), matched=True, expected_winner=PATHS[0])
    assert model.state_dict() == before


def test_independent_fixed_recurrence_causally_affects_continuation():
    recurrent = N3CausalTrace(PATHS)
    ablated = N3CausalTrace(PATHS)
    ablated.fixed = (0.0, 0.0)  # Engineering intervention, never an outcome-selected model.
    recurrent.advance((PATHS[0],))
    ablated.advance((PATHS[0],))
    recurrent.advance(())
    ablated.advance(())
    assert recurrent.hidden != ablated.hidden
    recurrent.weights = (0.5, 0.5)
    ablated.weights = (0.5, 0.5)
    assert [recurrent.causal_reliability(p) for p in PATHS] != [
        ablated.causal_reliability(p) for p in PATHS
    ]


def test_independent_restore_rejects_nonfinite_and_missing_accounting():
    model = N3CausalTrace(PATHS)
    for key, bad in (
        ("hidden", [float("nan"), 0.0]),
        ("weights", [float("inf"), 0.0]),
        ("counters", {}),
        ("tick", 65),
    ):
        value = deepcopy(model.state_dict())
        value[key] = bad
        with _case.assertRaises((ValueError, KeyError)):
            N3CausalTrace.from_state_dict(value)


if __name__ == "__main__":
    suite = unittest.TestSuite(
        unittest.FunctionTestCase(value)
        for name, value in sorted(globals().items())
        if name.startswith("test_")
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
