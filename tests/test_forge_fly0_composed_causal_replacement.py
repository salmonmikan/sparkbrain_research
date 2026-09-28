from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_composed_causal_replacement import (
    ComposedCausalReplacementLoop,
    build_composed_causal_report,
    run_to_target,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState

_FUNCTIONAL_VARIANTS = ("structured", "reactive")
_BASELINE_INCAPABLE_VARIANTS = ("rewired", "random_sparse")
_ALL_VARIANTS = (*_FUNCTIONAL_VARIANTS, *_BASELINE_INCAPABLE_VARIANTS)


@pytest.mark.parametrize("variant", _FUNCTIONAL_VARIANTS)
def test_functional_variants_reach_target_and_replay_exact(
    variant: str,
) -> None:
    initial = WorldState(position=2, target=-1)
    loop = ComposedCausalReplacementLoop(initial, variant=variant)
    checkpoint = loop.checkpoint()

    first = run_to_target(loop)
    first_tokens = tuple(item.after.token() for item in first)

    assert [item.accepted for item in first] == [True, True, True]
    assert (
        initial.position,
        *(item.after.world.position for item in first),
    ) == (2, 1, 0, -1)

    loop.restore(checkpoint)
    second = run_to_target(loop)

    assert tuple(item.after.token() for item in second) == first_tokens


@pytest.mark.parametrize("variant", _BASELINE_INCAPABLE_VARIANTS)
def test_matched_topology_controls_fail_closed_before_progress(
    variant: str,
) -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant=variant,
    )
    checkpoint = loop.checkpoint()
    before = loop.snapshot

    first = run_to_target(loop)

    assert len(first) == 1
    assert first[0].accepted is False
    assert first[0].reason == "action arbitration requires one active module"
    assert first[0].after == before
    assert loop.snapshot == before

    loop.restore(checkpoint)
    second = run_to_target(loop)
    assert tuple(item.after.token() for item in second) == tuple(
        item.after.token() for item in first
    )


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_observation_cut_fails_closed_before_progress(variant: str) -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant=variant,
        mask_observation=True,
    )
    before = loop.snapshot

    result = loop.step()

    assert result.accepted is False
    assert result.reason == "action arbitration requires one active module"
    assert result.after == before
    assert loop.snapshot == before


@pytest.mark.parametrize("variant", _FUNCTIONAL_VARIANTS)
def test_feedback_cut_blocks_second_modulation(variant: str) -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant=variant,
        mask_feedback=True,
    )

    first = loop.step()
    second = loop.step()

    assert first.accepted is True
    assert first.after.world.position == 1
    assert second.accepted is False
    assert second.reason == "ascending feedback insufficient for modulation"
    assert second.after == first.after
    assert loop.snapshot == first.after


@pytest.mark.parametrize("variant", _BASELINE_INCAPABLE_VARIANTS)
def test_feedback_cut_is_not_attributable_when_baseline_already_fails(
    variant: str,
) -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant=variant,
        mask_feedback=True,
    )

    first = loop.step()

    assert first.accepted is False
    assert first.reason == "action arbitration requires one active module"
    assert first.after == first.before


def test_checkpoint_binds_both_causal_cut_contracts() -> None:
    intact = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant="structured",
    )
    observation_cut = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant="structured",
        mask_observation=True,
    )
    feedback_cut = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant="structured",
        mask_feedback=True,
    )

    with pytest.raises(ValueError, match="observation-mask contract"):
        observation_cut.restore(intact.checkpoint())
    with pytest.raises(ValueError, match="feedback-mask contract"):
        feedback_cut.restore(intact.checkpoint())


def test_report_exposes_functional_mismatch_without_overclaim() -> None:
    report = build_composed_causal_report()

    assert report["functional_variants"] == ("structured", "reactive")
    assert report["baseline_incapable_variants"] == (
        "rewired",
        "random_sparse",
    )
    assert report["composed_causal_variants"] == ("structured", "reactive")
    assert report["replacement_ladder_functionally_matched"] is False
    assert report["all_variants_replay_exact"] is True
    assert report["remaining_gap_codes"] == (
        "REWIRED_BASELINE_FUNCTIONAL_CAPABILITY_ABSENT",
        "RANDOM_SPARSE_BASELINE_FUNCTIONAL_CAPABILITY_ABSENT",
        "FOUR_WAY_COMPOSED_CAUSAL_COMPARISON_BLOCKED_BY_BASELINE_CAPABILITY",
    )


def test_report_is_deterministic() -> None:
    first = build_composed_causal_report()
    second = build_composed_causal_report()

    assert json.dumps(first, sort_keys=True) == json.dumps(
        second,
        sort_keys=True,
    )
