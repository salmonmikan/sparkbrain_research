from __future__ import annotations

import pytest

from scripts.verify_v061_a01_md002_p4_candidate_001_artifacts import (
    _verify_active_lineages_against_ledger,
    _verify_changed_paths_from_states,
)


def _merged_row() -> dict[str, object]:
    return {
        "condition_spec": {"boundary_mode": "merged"},
        "retained_runtime_trace": [
            {
                "type": "md002-p4-active-lineages",
                "phase": "before",
                "proposal_ids": ["proposal-a", "proposal-b"],
                "measurement_time_ms": 40.0,
                "derivation": "ledger-proposal-temporal-validity-v1",
            },
            {
                "type": "md002-p4-active-lineages",
                "phase": "after",
                "proposal_ids": ["proposal-a", "proposal-b"],
                "measurement_time_ms": 45.0,
                "derivation": "ledger-proposal-temporal-validity-v1",
            },
        ],
        "ledger_state": {
            "proposals": {
                "proposal-a": {
                    "proposal_id": "proposal-a",
                    "created_at_ms": 20.0,
                    "valid_until_ms": 120.0,
                },
                "proposal-b": {
                    "proposal_id": "proposal-b",
                    "created_at_ms": 20.0,
                    "valid_until_ms": 120.0,
                },
            }
        },
        "pre": {"path_reliability": {"path-a": 0.5, "path-b": 0.5}},
        "post": {"path_reliability": {"path-a": 0.5, "path-b": 0.5}},
        "changed_path_ids": [],
    }


def test_independent_active_lineages_accept_rederived_retained_ledger_state() -> None:
    row = _merged_row()
    _verify_active_lineages_against_ledger(
        row,
        execution_id="p4-merged-confirmation",
    )


def test_independent_active_lineages_reject_expired_proposal_marked_active() -> None:
    row = _merged_row()
    ledger = row["ledger_state"]
    assert isinstance(ledger, dict)
    proposals = ledger["proposals"]
    assert isinstance(proposals, dict)
    proposal_a = proposals["proposal-a"]
    assert isinstance(proposal_a, dict)
    proposal_a["valid_until_ms"] = 39.0

    with pytest.raises(
        ValueError,
        match="active-lineage before differs from retained ledger",
    ):
        _verify_active_lineages_against_ledger(
            row,
            execution_id="p4-merged-confirmation",
        )


def test_independent_changed_paths_accept_exact_recomputation() -> None:
    row = _merged_row()
    post = row["post"]
    assert isinstance(post, dict)
    reliability = post["path_reliability"]
    assert isinstance(reliability, dict)
    reliability["path-a"] = 0.75
    row["changed_path_ids"] = ["path-a"]

    _verify_changed_paths_from_states(
        row,
        execution_id="p4-merged-separating-confirmation-a",
    )


def test_independent_changed_paths_reject_acquisition_declared_empty_change() -> None:
    row = _merged_row()
    post = row["post"]
    assert isinstance(post, dict)
    reliability = post["path_reliability"]
    assert isinstance(reliability, dict)
    reliability["path-a"] = 0.75

    with pytest.raises(
        ValueError,
        match="changed path IDs disagree with retained pre/post states",
    ):
        _verify_changed_paths_from_states(
            row,
            execution_id="p4-merged-separating-confirmation-a",
        )
