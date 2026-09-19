"""EXPLORATORY / NON_EVIDENTIARY config-binding diagnostic for SUB cycle 1."""

from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig


def _shape_snapshot(config: V05BrainConfig) -> dict[str, object]:
    brain = IntegratedV05Brain(config)
    unit_ids = tuple(sorted(brain.base.field.units))
    receptor_ids = tuple(sorted(brain.base.field.receptor_ids))
    return {
        "declared": (brain.config.width, brain.config.height, brain.config.receptor_rows),
        "base_declared": (
            brain.base.config.width,
            brain.base.config.height,
            brain.base.config.receptor_rows,
        ),
        "unit_ids": unit_ids,
        "receptor_ids": receptor_ids,
        "unit_count": len(unit_ids),
        "receptor_count": len(receptor_ids),
        "reservoir_count": len(unit_ids) - len(receptor_ids),
        "connection_count": len(brain.base.field.connections),
    }


def test_v05_dimension_config_is_accepted_but_does_not_bind_explicit_topology() -> None:
    default = _shape_snapshot(V05BrainConfig(topology_seed=41))
    alternate = _shape_snapshot(
        V05BrainConfig(width=12, height=10, receptor_rows=2, topology_seed=41)
    )

    assert default["declared"] == (8, 8, 1)
    assert alternate["declared"] == (12, 10, 2)
    assert alternate["base_declared"] == (12, 10, 2)

    # The explicit layered v0.5 topology keeps its independent defaults:
    # 16 receptors + an 8x6 reservoir, regardless of these accepted config values.
    assert default["unit_count"] == alternate["unit_count"] == 64
    assert default["receptor_count"] == alternate["receptor_count"] == 16
    assert default["reservoir_count"] == alternate["reservoir_count"] == 48
    assert default["unit_ids"] == alternate["unit_ids"]
    assert default["receptor_ids"] == alternate["receptor_ids"]
    assert default["connection_count"] == alternate["connection_count"]
