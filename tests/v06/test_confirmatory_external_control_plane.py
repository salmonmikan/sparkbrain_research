from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)

_FAKE_SHA = "a" * 40


def test_current_manifest_stays_fail_closed_until_candidate_builder() -> None:
    current = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=_FAKE_SHA,
    )
    current_readiness = assess_confirmatory_readiness(current)
    assert current.code_ref == _FAKE_SHA
    assert current_readiness.ready is False
    assert all(row.adapter_ready is False for row in current.conditions)

    candidate = build_candidate_manifest(source_code_sha=_FAKE_SHA)
    candidate_readiness = assess_confirmatory_readiness(candidate)
    expected_exclusion = (
        "Seal storage may occur after the source commit; "
        "execution uses detached source SHA."
    )
    assert candidate.code_ref == _FAKE_SHA
    assert candidate_readiness.ready is True
    assert all(row.adapter_ready is True for row in candidate.conditions)
    assert expected_exclusion in candidate.exclusions


@pytest.mark.parametrize(
    "invalid_sha",
    (
        "",
        "a" * 39,
        "a" * 41,
        "A" * 40,
        "g" * 40,
        "not-a-git-sha",
    ),
)
def test_candidate_manifest_rejects_noncanonical_source_sha(invalid_sha: str) -> None:
    with pytest.raises(ValueError, match="full lowercase Git SHA"):
        build_candidate_manifest(source_code_sha=invalid_sha)


def test_external_layout_rejects_relative_nested_and_source_internal_paths(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(ValueError, match="absolute"):
        ExternalArtifactLayout(
            control_root="control",
            raw_root=str((tmp_path / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)
    with pytest.raises(ValueError, match="outside source"):
        ExternalArtifactLayout(
            control_root=str((source / "control").resolve()),
            raw_root=str((tmp_path / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)
    with pytest.raises(ValueError, match="cannot be nested"):
        ExternalArtifactLayout(
            control_root=str((tmp_path / "external").resolve()),
            raw_root=str((tmp_path / "external" / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)
