from __future__ import annotations

from pathlib import Path

from sparkbrain.evaluation.v061_world_to_transition_audit import (
    audit_world_to_transition_dependency,
)


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def test_local_transition_learning_exists_but_relation_path_does_not_call_it() -> None:
    audit = audit_world_to_transition_dependency(_repository_root())
    assert audit.local_transition_learning_exists is True
    assert audit.relation_modules_reference_local_expectation is False
    assert audit.relation_modules_call_transition_learning is False
    assert audit.primary_relation_functions_call_transition_learning is False
    assert audit.direct_world_to_transition_dependency_present is False
    assert audit.missing_world_to_transition_path_confirmed is True


def test_audit_covers_the_four_required_architecture_modules() -> None:
    audit = audit_world_to_transition_dependency(_repository_root())
    assert {row.relative_path for row in audit.modules} == {
        "src/sparkbrain/v06/local_expectation.py",
        "src/sparkbrain/v06/consistency.py",
        "src/sparkbrain/v06/relation_reentry.py",
        "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py",
    }


def test_primary_contains_transition_learning_outside_relation_functions() -> None:
    audit = audit_world_to_transition_dependency(_repository_root())
    primary = next(
        row
        for row in audit.modules
        if row.relative_path.endswith("v06_confirmatory_heldout_primary.py")
    )
    assert "observe_external_transition" in primary.called_attributes
    relation_function_calls = {
        called
        for function_name, calls in primary.function_calls
        if any(fragment in function_name for fragment in ("relation", "reentry"))
        for called in calls
    }
    assert "observe_external_transition" not in relation_function_calls


def test_relation_reentry_is_downstream_of_consistency_and_reinjection_only() -> None:
    audit = audit_world_to_transition_dependency(_repository_root())
    reentry = next(
        row
        for row in audit.modules
        if row.relative_path.endswith("relation_reentry.py")
    )
    assert "consistency" in " ".join(reentry.imported_modules)
    assert "reinjection" in " ".join(reentry.imported_modules)
    assert "local_expectation" not in " ".join(reentry.imported_modules)
    assert "schedule" in reentry.called_attributes
    assert "observe_external_transition" not in reentry.called_attributes


def test_audit_is_observer_only_and_deterministic() -> None:
    first = audit_world_to_transition_dependency(_repository_root())
    second = audit_world_to_transition_dependency(_repository_root())
    assert first == second
    lowered = str(first.state_dict()).lower()
    for forbidden in (
        "candidate execution",
        "score_strict_confirmatory_results",
        "correct_action",
        "reward_value",
        "meaning_state",
    ):
        assert forbidden not in lowered
