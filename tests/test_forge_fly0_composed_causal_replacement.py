from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_composed_causal_replacement import (
    ComposedCausalReplacementLoop,
    build_composed_causal_report,
    run_to_target,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState

_ALL_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_all_variants_reach_target_and_replay_exact(
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


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
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


def test_report_exposes_repaired_functional_surface_without_overclaim() -> None:
    report = build_composed_causal_report()

    assert report["functional_variants"] == _ALL_VARIANTS
    assert report["baseline_incapable_variants"] == ()
    assert report["composed_causal_variants"] == _ALL_VARIANTS
    assert report["replacement_ladder_functionally_matched"] is True
    assert report["all_variants_replay_exact"] is True
    assert report["remaining_gap_codes"] == ()


def test_report_is_deterministic() -> None:
    first = build_composed_causal_report()
    second = build_composed_causal_report()

    assert json.dumps(first, sort_keys=True) == json.dumps(
        second,
        sort_keys=True,
    )


def test_checkpoint_binds_semantic_surface_and_topology_provenance() -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant="random_sparse",
    )
    payload = json.loads(loop.checkpoint())

    assert payload["schema_version"] == 2
    assert (
        payload["semantic_surface_contract"]["version"]
        == "fly0-semantic-surface-v1"
    )
    assert (
        payload["semantic_surface_fingerprint"]
        == loop.semantic_surface_fingerprint
    )
    assert payload["topology_fingerprint"] == loop.topology_fingerprint
    assert payload["randomization_seed"] == 2802

    payload["semantic_surface_contract"]["version"] = "tampered"
    with pytest.raises(ValueError, match="semantic-surface contract"):
        loop.restore(json.dumps(payload, sort_keys=True))


def test_checkpoint_rejects_topology_fingerprint_tamper() -> None:
    loop = ComposedCausalReplacementLoop(
        WorldState(position=2, target=-1),
        variant="structured",
    )
    payload = json.loads(loop.checkpoint())
    payload["topology_fingerprint"] = "0" * 64

    with pytest.raises(ValueError, match="topology fingerprint"):
        loop.restore(json.dumps(payload, sort_keys=True))


def test_report_exposes_semantic_surface_and_topology_provenance() -> None:
    report = build_composed_causal_report()

    assert (
        report["semantic_surface_contract"]["version"]
        == "fly0-semantic-surface-v1"
    )
    assert len(report["semantic_surface_fingerprint"]) == 64
    fingerprints = report["topology_fingerprints"]
    assert fingerprints["structured"] is not None
    assert fingerprints["rewired"] is not None
    assert fingerprints["random_sparse"] is not None
    assert fingerprints["reactive"] is None
    assert len(
        {
            fingerprints["structured"],
            fingerprints["rewired"],
            fingerprints["random_sparse"],
        }
    ) == 3
