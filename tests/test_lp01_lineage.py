from __future__ import annotations

from sparkbrain.lp01_lineage import (
    build_indexes,
    construction_digest,
    destroy_provenance,
    generate_history,
    present_state_digest,
)


def test_explicit_parent_table_matches_actual_lineage() -> None:
    roots, events, live = generate_history(seed=4101, live_nodes=24, history_events=72)
    actual, explicit, _ = build_indexes(roots, events, recent_window=16)
    ancestors = roots + tuple(event.child for event in events[:24])
    for ancestor in ancestors:
        assert actual.descendants_of(ancestor, live).descendants == explicit.descendants_of(
            ancestor, live
        ).descendants


def test_provenance_destroyed_control_changes_ancestry_but_not_present_digest() -> None:
    roots, events, live = generate_history(seed=4103, live_nodes=24, history_events=72)
    destroyed_events = destroy_provenance(roots, events, seed=904103)
    actual, _, _ = build_indexes(roots, events, recent_window=16)
    destroyed, _, _ = build_indexes(roots, destroyed_events, recent_window=16)

    assert construction_digest(roots, events, live) != construction_digest(
        roots, destroyed_events, live
    )
    assert present_state_digest(seed=4103, live_ids=live, recent_token="fixed") == (
        present_state_digest(seed=4103, live_ids=live, recent_token="fixed")
    )
    ancestors = roots + tuple(event.child for event in events[:36])
    assert any(
        actual.descendants_of(ancestor, live).descendants
        != destroyed.descendants_of(ancestor, live).descendants
        for ancestor in ancestors
    )


def test_recent_window_is_bounded_and_can_forget_old_ancestry() -> None:
    roots, events, live = generate_history(seed=4109, live_nodes=24, history_events=72)
    actual, _, recent = build_indexes(roots, events, recent_window=16)
    root = roots[0]
    assert len(recent.events) == 16
    assert set(recent.descendants_of(root, live).descendants).issubset(
        set(actual.descendants_of(root, live).descendants)
    )
