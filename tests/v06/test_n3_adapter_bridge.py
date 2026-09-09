"""Reserved engineering probes, never the frozen N3-DEV-001 case matrix."""

import unittest
from copy import deepcopy

from sparkbrain.v06.foundation import EventOrigin
from sparkbrain.v061_a01.credit_bridge import A01TransientCreditBridge
from sparkbrain.v061_a01.mechanism_discrimination import (
    PATH_A,
    PATH_B,
    PRIOR_TARGET,
    TARGET_A,
    _boundary,
    _external,
    _fixture,
    _proposal,
)
from sparkbrain.v061_a01.recurrent_adapter import N3LocalTemporalExpectation


class BridgeEngineeringTests(unittest.TestCase):
    def make_fixture(self, learn_prior=True):
        fixture = _fixture(learn_prior=learn_prior)
        fixture.expectation = N3LocalTemporalExpectation(fixture.expectation, (PATH_A, PATH_B))
        fixture.bridge = A01TransientCreditBridge(
            fixture.expectation, fixture.consistency, fixture.ledger
        )
        proposal = _proposal("engineering:p", path_id=PATH_A, target=TARGET_A)
        fixture.ledger.register_proposal(proposal)
        boundary = _boundary("engineering:b", 21.0, proposal_ids=(proposal.proposal_id,))
        fixture.consistency.register_boundary(boundary)
        fixture.expectation.trace.advance((PATH_A,))
        return fixture, boundary

    def test_external_only_and_fallback_does_not_learn(self):
        for exact in (False, True):
            fixture, boundary = self.make_fixture()
            external = _external(
                "engineering:e",
                23.0,
                PRIOR_TARGET,
                parent_event_ids=(boundary.event_id,) if exact else (),
            )
            fixture.ledger.register_external(external)
            before = fixture.expectation.learned_state_dict()
            fixture.bridge.observe_external(boundary, external)
            self.assertEqual(before != fixture.expectation.learned_state_dict(), exact)

    def test_no_prior_cannot_train(self):
        fixture, boundary = self.make_fixture(learn_prior=False)
        external = _external(
            "engineering:no-prior", 23.0, PRIOR_TARGET, parent_event_ids=(boundary.event_id,)
        )
        fixture.ledger.register_external(external)
        before = fixture.expectation.learned_state_dict()
        fixture.bridge.observe_external(boundary, external)
        self.assertEqual(before, fixture.expectation.learned_state_dict())

    def test_replay_rejected_no_update_and_restore(self):
        fixture, boundary = self.make_fixture()
        replay = _external(
            "engineering:replay",
            23.0,
            PRIOR_TARGET,
            parent_event_ids=(boundary.event_id,),
            origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        )
        fixture.ledger.register_event(replay)
        before = deepcopy(fixture.expectation.state_dict())
        with self.assertRaises(ValueError):
            fixture.bridge.observe_external(boundary, replay)
        self.assertEqual(before, fixture.expectation.state_dict())
        restored = N3LocalTemporalExpectation.from_state_dict(before)
        self.assertEqual(before, restored.state_dict())
        with self.assertRaises(ValueError):
            N3LocalTemporalExpectation.from_learned_state_dict(
                fixture.expectation.learned_state_dict()
            )


if __name__ == "__main__":
    unittest.main()
