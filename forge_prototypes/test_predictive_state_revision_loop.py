from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).with_name("predictive_state_revision_loop.py")
SPEC = importlib.util.spec_from_file_location("predictive_state_revision_loop", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PredictiveStateRevisionLoopTests(unittest.TestCase):
    def test_split_then_reuse_preserves_prior_hypothesis(self) -> None:
        bank = MODULE.PredictiveStateBank(context_gate=0.35, reuse_error=0.35)
        sequence = (
            ((0.00, 0.00), 1.00),
            ((0.05, -0.03), 1.10),
            ((-0.04, 0.02), 0.90),
            ((0.02, 0.01), -1.00),
            ((-0.03, -0.02), -0.90),
            ((0.01, 0.03), 1.05),
        )
        decisions = [bank.observe(context, outcome) for context, outcome in sequence]
        self.assertEqual(decisions[3].action, "split")
        self.assertEqual(decisions[5].action, "reuse")
        self.assertEqual(decisions[5].state_id, "state-001")
        self.assertEqual(len(bank.states), 2)

    def test_new_context_creates_distinct_state(self) -> None:
        bank = MODULE.PredictiveStateBank(context_gate=0.35, reuse_error=0.35)
        bank.observe((0.0, 0.0), 1.0)
        decision = bank.observe((2.0, 2.0), 1.0)
        self.assertEqual(decision.action, "create")
        self.assertEqual(decision.state_count, 2)

    def test_single_state_overwrite_is_worse_on_return(self) -> None:
        result = MODULE.run_demo()
        self.assertLess(
            result["return_to_prior_state_bank_error"],
            result["return_to_prior_state_single_state_error"],
        )
        self.assertAlmostEqual(result["return_to_prior_state_bank_error"], 0.05)
        self.assertAlmostEqual(
            result["return_to_prior_state_single_state_error"],
            1.50625,
        )


if __name__ == "__main__":
    unittest.main()
