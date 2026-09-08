from __future__ import annotations

import pytest

from sparkbrain.comparison.cx01.formal_identifiability import (
    audit_formal_world_identifiability,
)
from sparkbrain.comparison.cx01.formal_revision import build_revised_formal_world
from sparkbrain.comparison.cx01.worlds import CX01Family


@pytest.mark.parametrize(
    "generation_id",
    (
        "cx01-fixture-scoring-001",
        "cx01-fixture-prepare-001",
        "cx01-fixture-seal-001",
    ),
)
def test_cycle_generator_is_identifiable_across_reserved_fixture_band(
    generation_id: str,
) -> None:
    target_cardinalities: set[int] = set()
    for seed in range(5000, 5200):
        world = build_revised_formal_world(
            generation_id,
            CX01Family.CYCLE,
            seed,
        )
        assessment = audit_formal_world_identifiability(world)
        assert assessment["passed"] is True
        assert assessment["gates"]["global_majority_conflict"] is True
        target_cardinalities.add(
            len({phase.target for phase in world.cycle_phases})
        )

    assert target_cardinalities == {3, 4}


def test_candidate_002_cycle_band_passes_without_capability_execution() -> None:
    worlds = tuple(
        build_revised_formal_world(
            "cx01-candidate-002",
            CX01Family.CYCLE,
            seed,
        )
        for seed in range(370110, 370120)
    )

    assert all(
        audit_formal_world_identifiability(world)["passed"]
        for world in worlds
    )
    assert {len({phase.target for phase in world.cycle_phases}) for world in worlds} == {
        3,
        4,
    }
