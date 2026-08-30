from __future__ import annotations

from pathlib import Path

from sparkbrain.research.rv01.baseline import (
    FROZEN_RUNTIME_BLOBS,
    FROZEN_V06_CI_RUN_ID,
    FROZEN_V06_CODE_SHA,
    run_frozen_v06_baseline,
    verify_frozen_runtime_fingerprints,
)


def test_frozen_v06_runtime_blob_fingerprints_match() -> None:
    report = verify_frozen_runtime_fingerprints()
    assert report.frozen_code_sha == FROZEN_V06_CODE_SHA
    assert len(report.rows) == len(FROZEN_RUNTIME_BLOBS)
    assert report.mismatch_paths == ()
    assert report.complete is True


def test_fingerprint_check_fails_closed_for_a_missing_repository_root(
    tmp_path: Path,
) -> None:
    report = verify_frozen_runtime_fingerprints(tmp_path)
    assert report.complete is False
    assert report.mismatch_paths == tuple(sorted(FROZEN_RUNTIME_BLOBS))
    assert all(row.observed_git_blob_sha is None for row in report.rows)


def test_frozen_v06_canonical_behavior_is_reproduced() -> None:
    report = run_frozen_v06_baseline()
    assert report.frozen_code_sha == FROZEN_V06_CODE_SHA
    assert report.frozen_ci_run_id == FROZEN_V06_CI_RUN_ID
    assert report.reproduced is True
    assert report.state_candidate is True
    assert report.chain_candidate is True
    assert report.boundary_candidate is True
    assert report.revision_candidate is True

    summary = report.canonical_summary
    assert summary["state"] == {
        "alternate_targets": ("unit:2",),
        "no_history_event_count": 0,
        "reference_targets": ("unit:1",),
        "replay_targets": ("unit:1",),
    }
    assert summary["chain"]["sham_main_units"] == (1, 2, 3)
    assert summary["chain"]["targeted_main_units"] == (1,)
    assert summary["chain"]["matched_random_main_units"] == (1, 2, 3)
    assert summary["chain"]["root_reinjection_suppressed_units"] == ()
    assert summary["chain"]["selective_effect"] == 1.0

    assert summary["boundary"]["sham_main_boundary_count"] == 3
    assert summary["boundary"]["targeted_main_boundary_count"] == 0
    assert summary["boundary"]["matched_random_main_boundary_count"] == 3
    assert summary["boundary"]["sham_main_external_count"] == 3
    assert summary["boundary"]["internal_only_link_count"] == 0

    assert summary["revision"]["reversal_crossing_episode"] == 2
    assert summary["revision"]["reacquisition_crossing_episode"] == 2
    assert summary["revision"]["acquired_old_reliability"] == 0.8
    assert summary["revision"]["reversed_old_reliability"] == 0.5
    assert summary["revision"]["reversed_new_reliability"] == 0.8


def test_frozen_baseline_replay_is_deterministic() -> None:
    first = run_frozen_v06_baseline()
    second = run_frozen_v06_baseline()
    assert first.canonical_summary_hash == second.canonical_summary_hash
    assert first.canonical_summary == second.canonical_summary
    assert first.fingerprints == second.fingerprints
