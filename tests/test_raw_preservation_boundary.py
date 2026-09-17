from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def _run(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _git(*args: str, cwd: Path) -> str:
    return _run("git", *args, cwd=cwd).stdout.strip()


def _fixture_repo(tmp_path: Path) -> tuple[Path, Path, str]:
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    _run("git", "init", "--bare", str(remote), cwd=tmp_path)
    _run("git", "init", "-b", "main", str(work), cwd=tmp_path)
    _git("config", "user.name", "readiness-test", cwd=work)
    _git("config", "user.email", "readiness-test@example.invalid", cwd=work)
    (work / "README.md").write_text("synthetic readiness base\n", encoding="utf-8")
    _git("add", "README.md", cwd=work)
    _git("commit", "-m", "readiness base", cwd=work)
    base = _git("rev-parse", "HEAD", cwd=work)
    _git("remote", "add", "origin", str(remote), cwd=work)
    _git("push", "origin", "main", cwd=work)
    return remote, work, base


def test_missing_destination_is_created_and_refetched_exactly(tmp_path: Path) -> None:
    remote, work, base = _fixture_repo(tmp_path)
    payload = tmp_path / "synthetic_raw.jsonl"
    payload.write_text('{"row":1,"value":"alpha"}\n{"row":2,"value":"beta"}\n', encoding="utf-8")
    payload_digest = hashlib.sha256(payload.read_bytes()).hexdigest()
    manifest = tmp_path / "synthetic_manifest.json"
    manifest.write_text(
        json.dumps({"kind": "synthetic", "payload_sha256": payload_digest}, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    result = tmp_path / "result.json"
    script = Path(__file__).parents[1] / "scripts" / "preserve_raw_boundary.py"
    branch = "readiness/test-preservation"
    destination = "artifacts/readiness/synthetic-probe"

    _run(
        sys.executable,
        str(script),
        "--payload",
        str(payload),
        "--manifest",
        str(manifest),
        "--base-commit",
        base,
        "--branch",
        branch,
        "--destination",
        destination,
        "--result",
        str(result),
        cwd=work,
    )

    recorded = json.loads(result.read_text(encoding="utf-8"))
    assert recorded["payload_sha256"] == payload_digest
    assert recorded["preservation_commit"] == _git(
        "ls-remote", "origin", f"refs/heads/{branch}", cwd=work
    ).split()[0]

    verify = tmp_path / "verify"
    _run("git", "clone", "--branch", branch, str(remote), str(verify), cwd=tmp_path)
    assert (verify / destination / payload.name).read_bytes() == payload.read_bytes()
    assert (verify / destination / manifest.name).read_bytes() == manifest.read_bytes()

    collision = _run(
        sys.executable,
        str(script),
        "--payload",
        str(payload),
        "--manifest",
        str(manifest),
        "--base-commit",
        base,
        "--branch",
        branch,
        "--destination",
        destination,
        cwd=work,
        check=False,
    )
    assert collision.returncode != 0
    assert "already exists" in collision.stderr
