from __future__ import annotations

import hashlib

import pytest

from sparkbrain.learned.h7_formal_r1 import FormalIntegrityError
from sparkbrain.learned.h7_formal_r3 import (
    EVALUATION_EPISODES,
    EVALUATION_EPISODES_PER_WORLD,
    STEPS_PER_EPISODE,
    WORLDS,
)
from sparkbrain.learned.h7_formal_r3_executor import (
    ProtectedEpisodeSpec,
    validate_protected_evaluation_plan,
)


def _opaque(index: int, step: int) -> str:
    return hashlib.sha256(f"synthetic-{index}-{step}".encode()).hexdigest()


def _plan() -> list[ProtectedEpisodeSpec]:
    return [
        ProtectedEpisodeSpec(
            world=WORLDS[index % len(WORLDS)],
            seed=50_000_000 + index,
            opaque_target_ids=tuple(_opaque(index, step) for step in range(STEPS_PER_EPISODE)),
        )
        for index in range(EVALUATION_EPISODES)
    ]


def test_protected_plan_validates_only_shape_and_concealed_binding_structure() -> None:
    plan = _plan()
    validate_protected_evaluation_plan(plan)
    counts = {world: sum(spec.world == world for spec in plan) for world in WORLDS}
    assert set(counts.values()) == {EVALUATION_EPISODES_PER_WORLD}


def test_protected_plan_rejects_world_assignment_drift() -> None:
    plan = _plan()
    plan[1] = ProtectedEpisodeSpec(
        world=WORLDS[0],
        seed=plan[1].seed,
        opaque_target_ids=plan[1].opaque_target_ids,
    )
    with pytest.raises(FormalIntegrityError, match="per-world count drift"):
        validate_protected_evaluation_plan(plan)


def test_protected_plan_rejects_duplicate_seed() -> None:
    plan = _plan()
    plan[1] = ProtectedEpisodeSpec(
        world=plan[1].world,
        seed=plan[0].seed,
        opaque_target_ids=plan[1].opaque_target_ids,
    )
    with pytest.raises(FormalIntegrityError, match="duplicate seeds"):
        validate_protected_evaluation_plan(plan)


def test_protected_plan_rejects_malformed_opaque_id() -> None:
    plan = _plan()
    bad_ids = list(plan[0].opaque_target_ids)
    bad_ids[0] = "not-a-sha256"
    plan[0] = ProtectedEpisodeSpec(
        world=plan[0].world,
        seed=plan[0].seed,
        opaque_target_ids=tuple(bad_ids),
    )
    with pytest.raises(FormalIntegrityError, match="opaque target id"):
        validate_protected_evaluation_plan(plan)


def test_executor_module_does_not_expose_public_r2_evaluation_seed_constant() -> None:
    import sparkbrain.learned.h7_formal_r3_executor as executor

    assert not hasattr(executor, "EVALUATION_SEEDS")
