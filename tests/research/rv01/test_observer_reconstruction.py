from __future__ import annotations

from pathlib import Path

from sparkbrain.research.rv01.observer_reconstruction import (
    PhysicalTrajectoryObserver,
    run_observer_reconstruction_suite,
)


def test_physically_disjoint_routes_can_share_observer_cluster() -> None:
    suite = run_observer_reconstruction_suite()
    a, b, _ = suite.trajectories
    mapping = dict(suite.default_observer.trajectory_to_cluster)
    assert set(a.training_path).isdisjoint(b.training_path)
    assert a.connection_state_hash != b.connection_state_hash
    assert a.intact_later_units == (1, 2, 3)
    assert b.intact_later_units == (5, 6, 7)
    assert a.intact_later_times_ms != b.intact_later_times_ms
    assert mapping[a.trajectory_id] == mapping[b.trajectory_id]
    assert suite.assessment.physically_disjoint_routes_share_cluster is True
    assert suite.assessment.physically_distinct_timing_shares_cluster is True


def test_same_observer_cluster_requires_same_raw_consequence_and_causal_loss() -> None:
    suite = run_observer_reconstruction_suite()
    a, b, c = suite.trajectories
    mapping = dict(suite.default_observer.trajectory_to_cluster)
    assert a.raw_external_target_id == b.raw_external_target_id == "external:12"
    assert c.raw_external_target_id == "external:13"
    assert a.targeted_boundary_impairment == 1.0
    assert b.targeted_boundary_impairment == 1.0
    assert c.targeted_boundary_impairment == 1.0
    assert mapping[a.trajectory_id] == mapping[b.trajectory_id]
    assert mapping[c.trajectory_id] != mapping[a.trajectory_id]
    assert (
        suite.assessment.different_external_consequence_separates_cluster
        is True
    )
    assert suite.assessment.equal_cluster_has_equal_causal_signature is True


def test_targeted_edge_intervention_removes_terminal_boundary_effect() -> None:
    suite = run_observer_reconstruction_suite()
    for row in suite.trajectories:
        assert row.intact_boundary_count == 1
        assert row.targeted_boundary_count == 0
        assert row.training_path[-1] in row.intact_later_units
        assert row.training_path[-1] not in row.targeted_later_units
        assert row.targeted_downstream_impairment == 1.0
        assert row.targeted_runtime_hash != row.intact_runtime_hash


def test_observer_and_taxonomy_rename_do_not_change_runtime_bundle() -> None:
    suite = run_observer_reconstruction_suite()
    default = suite.default_observer
    renamed = suite.renamed_observer
    assert (
        default.runtime_bundle_hash_before
        == default.runtime_bundle_hash_after
        == renamed.runtime_bundle_hash_before
        == renamed.runtime_bundle_hash_after
        == suite.runtime_only_hash
    )
    assert dict(default.trajectory_to_cluster) == dict(
        renamed.trajectory_to_cluster
    )
    assert tuple(row.observer_label for row in default.clusters) != tuple(
        row.observer_label for row in renamed.clusters
    )
    assert suite.assessment.observer_does_not_change_runtime_bundle is True
    assert (
        suite.assessment.taxonomy_rename_preserves_cluster_membership
        is True
    )
    assert suite.assessment.observer_removal_preserves_runtime_bundle is True


def test_observer_clusters_are_post_hoc_and_not_runtime_state() -> None:
    suite = run_observer_reconstruction_suite()
    runtime_lowered = str(
        [row.state_dict() for row in suite.trajectories]
    ).lower()
    observer_lowered = str(suite.default_observer.state_dict()).lower()
    assert "observer-cluster" not in runtime_lowered
    assert "observer-cluster" in observer_lowered
    assert (
        suite.assessment.runtime_contains_no_functional_equivalence_state
        is True
    )


def test_r01_10_supports_relation_candidate_not_concept_or_meaning() -> None:
    assessment = run_observer_reconstruction_suite().assessment
    assert assessment.reconstructed_relation_candidate_supported is True
    assert assessment.concept_or_meaning_claim_supported is False
    assert assessment.engineering_candidate is True


def test_observer_reconstruction_is_deterministic() -> None:
    first = run_observer_reconstruction_suite()
    second = run_observer_reconstruction_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash


def test_observer_object_has_no_runtime_write_method() -> None:
    observer = PhysicalTrajectoryObserver()
    assert not hasattr(observer, "schedule")
    assert not hasattr(observer, "reinjection")
    assert not hasattr(observer, "observe_external")
    assert not hasattr(observer, "update_connection")


def test_observer_module_imports_no_explicit_assembly_or_semantic_runtime() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "observer_reconstruction.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "TemporalAssembly" not in source
    assert "semantic_state" not in source
    assert "correct_action" not in source
    assert "scalar_reward" not in source
