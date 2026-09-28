from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_matched_replacement import (
    MatchedEnvelopeLoop,
    build_replacement_ladder_report,
    run_to_target,
)


def test_replacement_ladder_uses_one_configured_envelope() -> None:
    report = build_replacement_ladder_report()

    assert report.replacement_ladder_complete is True
    assert report.configured_envelope_matched is True
    assert report.feedback_delay_envelope_matched is True
    assert report.topology_resource_envelope_matched is True
    assert {row.variant for row in report.rows} == {
        "structured",
        "rewired",
        "random_sparse",
        "reactive",
    }


def test_structured_and_reactive_reach_target_with_same_trace() -> None:
    report = build_replacement_ladder_report()
    rows = {row.variant: row for row in report.rows}

    for variant in ("structured", "reactive"):
        row = rows[variant]
        assert row.reached_target is True
        assert row.position_trace == (2, 1, 0, -1)
        assert row.feedback_delay_steps == 1
        assert row.max_feedback_delay_steps == 1
        assert row.event_budget_per_controller_call == 4096
        assert row.replay_exact is True


@pytest.mark.parametrize("variant", ["structured", "reactive"])
def test_delay_over_budget_fails_closed_after_first_step(
    variant: str,
) -> None:
    loop = MatchedEnvelopeLoop(
        WorldState(position=2, target=-1),
        variant=variant,
        feedback_delay_steps=2,
        max_feedback_delay_steps=1,
    )
    first = loop.step()
    checkpoint_after_first = loop.checkpoint()
    second = loop.step()

    assert first.accepted is True
    assert first.after.world.position == 1
    assert second.accepted is False
    assert second.reason == "feedback delay exceeds matched budget"
    assert second.after == first.after
    assert loop.checkpoint() == checkpoint_after_first


@pytest.mark.parametrize("variant", ["structured", "reactive"])
def test_checkpoint_restore_replays_exact_history(variant: str) -> None:
    loop = MatchedEnvelopeLoop(
        WorldState(position=2, target=-1),
        variant=variant,
    )
    checkpoint = loop.checkpoint()
    first = run_to_target(loop)
    first_tokens = tuple(item.after.token() for item in first)

    loop.restore(checkpoint)
    second = run_to_target(loop)

    assert tuple(item.after.token() for item in second) == first_tokens


def test_checkpoint_rejects_replacement_variant_mismatch() -> None:
    structured = MatchedEnvelopeLoop(
        WorldState(position=2, target=-1),
        variant="structured",
    )
    reactive = MatchedEnvelopeLoop(
        WorldState(position=2, target=-1),
        variant="reactive",
    )

    with pytest.raises(ValueError, match="replacement variant"):
        reactive.restore(structured.checkpoint())


def test_internal_activity_mismatch_remains_explicit() -> None:
    report = build_replacement_ladder_report()

    assert report.activity_instrumentation_commensurate_across_all is False
    assert report.strict_activity_resource_match is False
    assert report.remaining_gap_codes == (
        "REACTIVE_INTERNAL_ACTIVITY_BASIS_NOT_COMMENSURATE",
        "STRICT_INTERNAL_ACTIVITY_RESOURCE_MATCH_OPEN",
    )


def test_report_is_deterministic() -> None:
    first = build_replacement_ladder_report().summary()
    second = build_replacement_ladder_report().summary()

    assert json.dumps(first, sort_keys=True) == json.dumps(
        second,
        sort_keys=True,
    )
