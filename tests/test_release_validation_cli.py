from __future__ import annotations

import json
import sys

import pytest

import scripts.validate_release as validation_cli


def _categories(*, integrity: list[str] | None = None) -> dict[str, list[str]]:
    return {
        "integrity_problems": integrity or [],
        "preparation_problems": [],
        "owner_blockers": [
            "project license has not been selected by the repository owner"
        ],
        "evidence_blockers": [],
    }


def test_preparation_only_fails_closed_for_integrity_problem(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        validation_cli,
        "release_validation",
        lambda root: _categories(integrity=["sha256 mismatch: README.md"]),
    )
    monkeypatch.setattr(sys, "argv", ["validate_release.py", "--preparation-only"])

    with pytest.raises(SystemExit) as exc_info:
        validation_cli.main()

    assert exc_info.value.code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "invalid"
    assert payload["preparation_status"] == "fail"
    assert payload["integrity_problems"] == ["sha256 mismatch: README.md"]
    assert payload["problems"] == [
        "sha256 mismatch: README.md",
        "project license has not been selected by the repository owner",
    ]


def test_preparation_only_allows_owner_license_blocker(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(validation_cli, "release_validation", lambda root: _categories())
    monkeypatch.setattr(sys, "argv", ["validate_release.py", "--preparation-only"])

    validation_cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "blocked"
    assert payload["preparation_status"] == "pass"
    assert payload["problems"] == payload["owner_blockers"]
