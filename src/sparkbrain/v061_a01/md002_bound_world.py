"""Typed anonymous-world binding for prospective A01 MD-002 P2.

This module closes the construction gap between the byte-bound L/F/C/R checkpoint
and the anonymous external-world permutation. It performs no capability
execution and applies no external evidence. The resulting fixture remains an
execution-disabled input package for a later development-only P2 runner.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import RuntimePulse

from .credit_bridge import A01LocalTemporalExpectation
from .md002_fixtures import P2WorldOnlyFixture
from .md002_state_binding import LiveReturnAddressState, build_bound_a01_p2_fixture
from .md002_world_fixture import P2AnonymousWorldPermutation


def build_typed_a01_p2_world_fixture(
    *,
    expectation: A01LocalTemporalExpectation,
    field_state: Mapping[str, Any] | TemporalExcitableField,
    consistency: UntypedBoundaryConsistency,
    return_address: LiveReturnAddressState,
    world_permutation: P2AnonymousWorldPermutation,
    admissible_external_evidence: tuple[RuntimePulse, ...],
) -> P2WorldOnlyFixture:
    """Bind one typed anonymous world permutation to one exact A01 checkpoint.

    The live BoundaryEvent is required because P2 is specifically an external
    consequence of an anonymous proposal lineage. Both world arms must contain
    the exact proposal key carried by that pending boundary. No world response is
    generated here; that remains a later runner operation.
    """

    world_permutation.validate()
    boundary = return_address.boundary
    proposal_ids = tuple(boundary.source_proposal_ids)
    if len(proposal_ids) != 1:
        raise ValueError("typed P2 fixture requires exactly one live boundary proposal")
    proposal_id = proposal_ids[0]
    if proposal_id not in world_permutation.control.mapping:
        raise ValueError("typed P2 control world does not contain the live boundary proposal")
    if proposal_id not in world_permutation.intervention.mapping:
        raise ValueError(
            "typed P2 intervention world does not contain the live boundary proposal"
        )

    state = field_state.state_dict() if isinstance(field_state, TemporalExcitableField) else field_state
    return build_bound_a01_p2_fixture(
        expectation=expectation,
        field_state=state,
        consistency=consistency,
        return_address=return_address,
        control_world_relation=world_permutation.control.state_dict(),
        intervention_world_relation=world_permutation.intervention.state_dict(),
        admissible_external_evidence=admissible_external_evidence,
    )


__all__ = ["build_typed_a01_p2_world_fixture"]
