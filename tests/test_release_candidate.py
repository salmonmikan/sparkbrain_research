from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

import pytest

from sparkbrain.release_candidate import (
    CANDIDATE_MANIFEST_NAME,
    build_candidate_and_review_archives,
    build_canonical_reproduction_manifest,
    validate_canonical_reproduction_manifest,
    validate_network_client_boundary,
)


REVISION = "a" * 40


def _fixture_root(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "result.md").write_text("evidence\n", encoding="utf-8")
    (root / "src.py").write_text("import json\n", encoding="utf-8")
    return root


def test_canonical_manifest_is_deterministic_and_separates_runtime_facts(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    first = build_canonical_reproduction_manifest(
        root, source_revision=REVISION, paths=["src.py", "docs/result.md"]
    )
    second = build_canonical_reproduction_manifest(
        root, source_revision=REVISION, paths=["docs/result.md", "src.py"]
    )
    assert first == second
    assert "duration_seconds" not in first
    assert "platform" not in first
    assert validate_canonical_reproduction_manifest(first) == []


def test_manifest_validation_rejects_order_hash_size_and_revision_tampering(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    manifest = build_canonical_reproduction_manifest(
        root, source_revision=REVISION, paths=["docs/result.md", "src.py"]
    )
    manifest["files"].reverse()
    manifest["files"][0]["sha256"] = "A" * 64
    manifest["files"][0]["size"] = -1
    manifest["source_revision"] = "not-a-sha"
    problems = validate_canonical_reproduction_manifest(manifest)
    assert "candidate manifest file paths must be sorted" in problems
    assert any("sha256 must be lowercase" in problem for problem in problems)
    assert any("size must be a non-negative integer" in problem for problem in problems)
    assert "source_revision must be a full lowercase Git SHA" in problems


def test_transaction_creates_valid_candidate_and_review_archives(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    candidate = tmp_path / "out" / "candidate.zip"
    review = tmp_path / "out" / "review.zip"
    result = build_candidate_and_review_archives(
        root,
        source_revision=REVISION,
        paths=["docs/result.md", "src.py"],
        candidate_output=candidate,
        review_output=review,
        source_date_epoch=1_700_000_000,
        network_boundary_paths=[root / "src.py"],
    )
    assert result["candidate"] == str(candidate)
    assert candidate.is_file() and candidate.with_suffix(".zip.sha256").is_file()
    assert review.is_file() and review.with_suffix(".zip.sha256").is_file()
    with zipfile.ZipFile(candidate) as archive:
        manifest = json.loads(archive.read(CANDIDATE_MANIFEST_NAME))
        assert validate_canonical_reproduction_manifest(manifest) == []
        assert archive.namelist() == ["docs/result.md", "src.py", CANDIDATE_MANIFEST_NAME]


def test_existing_output_and_network_client_fail_closed_without_mutation(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    candidate = tmp_path / "out" / "candidate.zip"
    review = tmp_path / "out" / "review.zip"
    candidate.parent.mkdir()
    candidate.write_bytes(b"keep")
    with pytest.raises(ValueError, match="already exists"):
        build_candidate_and_review_archives(
            root,
            source_revision=REVISION,
            paths=["docs/result.md"],
            candidate_output=candidate,
            review_output=review,
            source_date_epoch=1_700_000_000,
        )
    assert candidate.read_bytes() == b"keep"

    candidate.unlink()
    (root / "src.py").write_text("import socket\n", encoding="utf-8")
    assert validate_network_client_boundary([root / "src.py"])
    with pytest.raises(ValueError, match="network boundary failed"):
        build_candidate_and_review_archives(
            root,
            source_revision=REVISION,
            paths=["docs/result.md"],
            candidate_output=candidate,
            review_output=review,
            source_date_epoch=1_700_000_000,
            network_boundary_paths=[root / "src.py"],
        )
    assert not candidate.exists() and not review.exists()


def test_publish_failure_rolls_back_every_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _fixture_root(tmp_path)
    candidate = tmp_path / "out" / "candidate.zip"
    review = tmp_path / "out" / "review.zip"
    original_replace = os.replace

    def fail_review_publish(source: object, destination: object) -> None:
        if Path(destination) == review:
            raise OSError("injected review publish failure")
        original_replace(source, destination)

    monkeypatch.setattr("sparkbrain.release_candidate.os.replace", fail_review_publish)
    with pytest.raises(OSError, match="injected review publish failure"):
        build_candidate_and_review_archives(
            root,
            source_revision=REVISION,
            paths=["docs/result.md"],
            candidate_output=candidate,
            review_output=review,
            source_date_epoch=1_700_000_000,
        )
    assert not candidate.exists()
    assert not candidate.with_suffix(".zip.sha256").exists()
    assert not review.exists()
    assert not review.with_suffix(".zip.sha256").exists()
    assert list((tmp_path / "out").glob(".candidate-release-staging-*")) == []
