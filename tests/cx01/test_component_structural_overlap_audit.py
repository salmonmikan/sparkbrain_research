from __future__ import annotations

from sparkbrain.comparison.cx01.candidate import (
    CandidateSpec,
    build_candidate_grid,
    candidate_component_structure_audit,
)
from sparkbrain.comparison.cx01.structural_components import (
    STRUCTURAL_AXES,
    component_structural_report,
    structural_component_signatures,
)
from sparkbrain.comparison.cx01.worlds import (
    DEVELOPMENT_GENERATION_ID,
    CX01Family,
    build_world,
)


def _candidate_002() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-candidate-002",
        seeds=tuple(range(370110, 370120)),
    )


def test_component_signatures_canonicalize_anonymous_tokens() -> None:
    for family in CX01Family:
        first = structural_component_signatures(
            build_world(DEVELOPMENT_GENERATION_ID, family, 3000)
        )
        second = structural_component_signatures(
            build_world(DEVELOPMENT_GENERATION_ID, family, 3001)
        )
        assert first["topology"] == second["topology"]
        assert first["timing"] == second["timing"]
        assert first["contingency"] == second["contingency"]
        if family is not CX01Family.CYCLE:
            assert first["exposure_schedule"] == second["exposure_schedule"]
            assert first["full"] == second["full"]
        else:
            assert first["exposure_schedule"] != second["exposure_schedule"]
            assert first["full"] != second["full"]
        assert first["token_assignment"] != second["token_assignment"]


def test_component_audit_rejects_new_labels_on_development_structure() -> None:
    relabeled_development = tuple(
        build_world("cx01-fixture-relabeled-development", family, seed)
        for family in CX01Family
        for seed in range(5000, 5010)
    )
    report = component_structural_report(relabeled_development)

    assert report["passed"] is False
    for family in CX01Family:
        row = report["family_rows"][family.value]
        assert row["axes"]["full"]["development_overlap_count"] >= 1
        assert row["axes"]["full"]["passed"] is False


def test_candidate_002_has_seed_dependent_component_novelty() -> None:
    candidate = _candidate_002()
    worlds = build_candidate_grid(candidate)
    report = candidate_component_structure_audit(candidate)

    assert report["passed"] is True
    assert report["world_count"] == len(CX01Family) * len(candidate.seeds)
    assert len(worlds) == report["world_count"]
    assert all(row["passed"] for row in report["world_rows"])
    assert all(
        row["non_token_novel_axis_count"] >= 2
        for row in report["world_rows"]
    )

    for family in CX01Family:
        family_row = report["family_rows"][family.value]
        assert family_row["passed"] is True
        assert family_row["axes"]["topology"]["formal_unique_count"] >= 2
        assert family_row["axes"]["timing"]["formal_unique_count"] >= 2
        assert (
            family_row["axes"]["exposure_schedule"]["formal_unique_count"]
            >= 2
        )
        assert family_row["axes"]["full"]["development_overlap_count"] == 0
        assert family_row["axes"]["full"]["formal_unique_count"] >= 5


def test_component_audit_exposes_each_requested_overlap_axis() -> None:
    report = candidate_component_structure_audit(_candidate_002())
    for family in CX01Family:
        axes = report["family_rows"][family.value]["axes"]
        assert "topology" in axes
        assert "timing" in axes
        assert "exposure_schedule" in axes
        assert "contingency" in axes
        for axis in STRUCTURAL_AXES:
            assert "applicable" in axes[axis]
            assert "development_overlap_count" in axes[axis]
            assert "formal_novel_count" in axes[axis]
            assert "formal_unique_count" in axes[axis]


def test_non_applicable_contingency_axis_is_not_falsely_failed() -> None:
    report = candidate_component_structure_audit(_candidate_002())
    for family in (
        CX01Family.HIGH_ORDER,
        CX01Family.TIMING,
        CX01Family.SELECTIVITY,
    ):
        contingency = report["family_rows"][family.value]["axes"]["contingency"]
        assert contingency["applicable"] is False
        assert contingency["novelty_required"] is False
        assert contingency["passed"] is True
