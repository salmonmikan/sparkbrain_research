from __future__ import annotations

from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd005_construction_runner as runner


def test_legacy_direct_cli_is_disabled_before_input_or_output(tmp_path: Path) -> None:
    missing_input = tmp_path / "missing-construction-input.json"
    repo_root = tmp_path / "repo"

    with pytest.raises(RuntimeError, match="legacy RD005 construction CLI is disabled"):
        runner.main(
            [
                "--input",
                str(missing_input),
                "--repo-root",
                str(repo_root),
            ]
        )

    assert not missing_input.exists()
    assert not (repo_root / "artifacts").exists()
