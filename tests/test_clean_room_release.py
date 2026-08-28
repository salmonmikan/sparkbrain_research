from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from sparkbrain.release import (
    RELEASE_METADATA_PATH,
    package_version,
    release_mode,
    sha256_file,
    tracked_release_paths,
)
from sparkbrain.release_v03_artifacts import release_relative_for_version

ROOT = Path(__file__).resolve().parents[1]
CHILD_SENTINEL = "SPARKBRAIN_CLEAN_ROOM_CHILD"


def _run(
    command: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"command failed ({result.returncode}): {command!r}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "Traceback" not in result.stderr
    return result


def _run_failure(
    command: list[str], *, cwd: Path, expected: str
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert expected in result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    return result


def _copy_tracked_worktree(source: Path, destination: Path) -> None:
    listed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=source,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    for relative in (item for item in listed.split("\0") if item):
        source_path = source / relative
        destination_path = destination / relative
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)

    # These corrective artifacts may be untracked during the local pre-commit run.
    for relative in (
        "RELEASE_METADATA.json",
        "scripts/build_review_bundle.py",
        "tests/test_clean_room_release.py",
        "tests/test_release_archive_mode.py",
        "tests/test_review_bundle.py",
    ):
        source_path = source / relative
        if source_path.is_file():
            destination_path = destination / relative
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)


def _build_fixture_archive(repository: Path, archive_path: Path) -> None:
    paths = tracked_release_paths(repository)
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for relative in [*paths, "PACKAGE_MANIFEST.json", RELEASE_METADATA_PATH]:
            archive.write(repository / relative, arcname=relative)


def _tampered_copy(source: Path, parent: Path, name: str) -> Path:
    destination = parent / name
    shutil.copytree(source, destination)
    return destination


def _assert_reproduction_preflight_failure(
    root: Path, output: Path, *, expected: str
) -> None:
    _run_failure(
        [
            sys.executable,
            "scripts/reproduce_release.py",
            "--offline",
            "--output",
            str(output),
        ],
        cwd=root,
        expected=expected,
    )
    assert not output.exists()
    assert list(output.parent.glob(f".{output.name}.staging-*")) == []


@pytest.mark.skipif(
    os.environ.get(CHILD_SENTINEL) == "1" or release_mode(ROOT) == "archive",
    reason="the outer repository test already verifies the extracted archive suite",
)
def test_no_git_archive_runs_full_clean_room_contract(tmp_path: Path) -> None:
    fixture_repo = tmp_path / "fixture-repository"
    fixture_repo.mkdir()
    _copy_tracked_worktree(ROOT, fixture_repo)

    _run(["git", "init", "--quiet"], cwd=fixture_repo)
    _run(["git", "config", "user.name", "SparkBrain test fixture"], cwd=fixture_repo)
    _run(["git", "config", "user.email", "fixture.invalid@example.invalid"], cwd=fixture_repo)
    # The source repository intentionally tracks selected generated evidence below ignored
    # artifact directories. Preserve that exact tracked fixture set in the temporary repo.
    _run(["git", "add", "--force", "--all"], cwd=fixture_repo)
    _run(["git", "commit", "--quiet", "-m", "clean-room fixture"], cwd=fixture_repo)

    release_relative = release_relative_for_version(package_version(fixture_repo))
    if (fixture_repo / release_relative / "evidence_map.json").is_file():
        shutil.rmtree(fixture_repo / release_relative)
        _run(["git", "add", "--update"], cwd=fixture_repo)
        _run(["git", "commit", "--quiet", "-m", "fixture source pin"], cwd=fixture_repo)
        revision = _run(["git", "rev-parse", "HEAD"], cwd=fixture_repo).stdout.strip()
        _run(
            [
                sys.executable,
                "scripts/generate_v03_release_artifacts.py",
                "--output-root",
                str(fixture_repo),
                "--source-revision",
                revision,
            ],
            cwd=fixture_repo,
        )
        _run(["git", "add", "--force", release_relative], cwd=fixture_repo)
        _run(["git", "commit", "--quiet", "-m", "fixture v0.3 artifacts"], cwd=fixture_repo)
        _run(
            [
                sys.executable,
                "scripts/generate_v03_root_manifest.py",
                "--source-revision",
                revision,
                "--generated-at",
                "2026-08-28T00:00:00+00:00",
                "--replace-existing",
            ],
            cwd=fixture_repo,
        )
        _run(
            ["git", "add", "PACKAGE_MANIFEST.json", RELEASE_METADATA_PATH], cwd=fixture_repo
        )
        _run(["git", "commit", "--quiet", "-m", "fixture v0.3 root bindings"], cwd=fixture_repo)
    else:
        revision = _run(["git", "rev-parse", "HEAD"], cwd=fixture_repo).stdout.strip()
        _run([sys.executable, "scripts/generate_release_artifacts.py"], cwd=fixture_repo)
        _run(
            [
                sys.executable,
                "scripts/generate_release_manifest.py",
                "--generated-at",
                "2026-08-24T00:00:00+00:00",
                "--source-revision",
                revision,
            ],
            cwd=fixture_repo,
        )

    fixture_validation = _run(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=fixture_repo,
    )
    fixture_payload = json.loads(fixture_validation.stdout)
    assert fixture_payload["integrity_problems"] == []
    assert fixture_payload["preparation_problems"] == []
    assert fixture_payload["evidence_blockers"] == []

    archive_path = tmp_path / "fixture-release.zip"
    _build_fixture_archive(fixture_repo, archive_path)
    extracted = tmp_path / "extracted-release"
    extracted.mkdir()
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert all(".git" not in Path(name).parts for name in archive.namelist())
        archive.extractall(extracted)

    assert not (extracted / ".git").exists()

    output = tmp_path / "reproduced-release"
    child_env = {
        **os.environ,
        "NO_PROXY": "*",
        "no_proxy": "*",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    _run([sys.executable, "scripts/local_readiness_check.py"], cwd=extracted, env=child_env)
    reproduction = _run(
        [
            sys.executable,
            "scripts/reproduce_release.py",
            "--offline",
            "--output",
            str(output),
        ],
        cwd=extracted,
        env=child_env,
    )
    reproduction_payload = json.loads(reproduction.stdout)
    assert reproduction_payload["status"] == "pass"

    frozen = json.loads(
        (extracted / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    for relative, expected in frozen["outputs"].items():
        assert sha256_file(output / relative) == expected

    validation = _run(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=extracted,
        env=child_env,
    )
    validation_payload = json.loads(validation.stdout)
    assert validation_payload["status"] == "blocked"
    assert validation_payload["preparation_status"] == "pass"
    assert validation_payload["integrity_problems"] == []
    assert validation_payload["preparation_problems"] == []
    assert validation_payload["evidence_blockers"] == []
    assert validation_payload["owner_blockers"] == [
        "project license has not been selected by the repository owner"
    ]
    assert validation_payload["problems"] == validation_payload["owner_blockers"]

    readme_tamper = _tampered_copy(extracted, tmp_path, "tamper-readme")
    with (readme_tamper / "README.md").open("ab") as handle:
        handle.write(b"tamper")
    _run_failure(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=readme_tamper,
        expected="sha256 mismatch: README.md",
    )

    missing_file = _tampered_copy(extracted, tmp_path, "tamper-missing")
    (missing_file / "README.md").unlink()
    _run_failure(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=missing_file,
        expected="missing or non-regular release file: README.md",
    )

    unexpected_file = _tampered_copy(extracted, tmp_path, "tamper-unexpected")
    (unexpected_file / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
    _run_failure(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=unexpected_file,
        expected="archive tree contains unexpected files",
    )

    metadata_revision = _tampered_copy(extracted, tmp_path, "tamper-metadata-revision")
    metadata_path = metadata_revision / RELEASE_METADATA_PATH
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["source_revision"] = "b" * 40
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    _run_failure(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=metadata_revision,
        expected="release metadata source_revision does not match PACKAGE_MANIFEST.json",
    )
    _assert_reproduction_preflight_failure(
        metadata_revision,
        tmp_path / "metadata-revision-output",
        expected="release metadata source_revision does not match PACKAGE_MANIFEST.json",
    )

    metadata_hash = _tampered_copy(extracted, tmp_path, "tamper-metadata-hash")
    metadata_path = metadata_hash / RELEASE_METADATA_PATH
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["manifest_sha256"] = "0" * 64
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    _run_failure(
        [sys.executable, "scripts/validate_release.py", "--preparation-only"],
        cwd=metadata_hash,
        expected="release metadata manifest_sha256 does not match PACKAGE_MANIFEST.json",
    )
    _assert_reproduction_preflight_failure(
        metadata_hash,
        tmp_path / "metadata-hash-output",
        expected="release metadata manifest_sha256 does not match PACKAGE_MANIFEST.json",
    )

    evidence_revision = _tampered_copy(extracted, tmp_path, "tamper-evidence-revision")
    evidence_path = evidence_revision / "artifacts/release/evidence_map.json"
    if (evidence_revision / "artifacts/release/v0.3/evidence_map.json").is_file():
        evidence_path = evidence_revision / "artifacts/release/v0.3/evidence_map.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["source_revision"] = "b" * 40
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    _assert_reproduction_preflight_failure(
        evidence_revision,
        tmp_path / "evidence-revision-output",
        expected="release source_revision values do not match",
    )

    primary_input = _tampered_copy(extracted, tmp_path, "tamper-primary-input")
    with (primary_input / "artifacts/benchmarks/benchmark_aggregate.csv").open("ab") as handle:
        handle.write(b"tamper")
    _assert_reproduction_preflight_failure(
        primary_input,
        tmp_path / "primary-input-output",
        expected="sha256 mismatch: artifacts/benchmarks/benchmark_aggregate.csv",
    )

    _run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=extracted,
        env=child_env,
    )
