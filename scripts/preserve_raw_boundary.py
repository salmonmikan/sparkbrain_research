#!/usr/bin/env python3
"""Fail-closed Git preservation primitive for target-blind raw bytes.

This utility is intentionally science-agnostic. It creates a new remote branch from an
exact base commit, writes payload and manifest bytes beneath a fresh destination, pushes
without force, and verifies the remote ref resolves to the exact local preservation commit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        capture_output=True,
        text=True,
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_destination(raw: str) -> Path:
    dest = Path(raw)
    if dest.is_absolute() or ".." in dest.parts or raw in {"", "."}:
        raise SystemExit("destination must be a non-root relative repository path")
    return dest


def _remote_branch_sha(remote: str, branch: str) -> str | None:
    result = _git("ls-remote", "--exit-code", "--heads", remote, branch, check=False)
    if result.returncode == 2:
        return None
    if result.returncode != 0:
        raise SystemExit(
            f"unable to inspect remote branch {remote}/{branch}: {result.stderr.strip()}"
        )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise SystemExit(f"ambiguous remote branch resolution for {remote}/{branch}")
    return lines[0].split()[0]


def preserve(
    *,
    payload: Path,
    manifest: Path,
    base_commit: str,
    branch: str,
    destination: Path,
    remote: str,
    commit_message: str,
) -> dict[str, str]:
    if not payload.is_file() or not manifest.is_file():
        raise SystemExit("payload and manifest must both be regular files")
    if payload.name == manifest.name:
        raise SystemExit("payload and manifest filenames must differ")

    _git("cat-file", "-e", f"{base_commit}^{{commit}}")
    if _remote_branch_sha(remote, branch) is not None:
        raise SystemExit(f"remote preservation branch already exists: {branch}")

    payload_digest = _sha256(payload)
    manifest_digest = _sha256(manifest)

    _git("switch", "--create", branch, base_commit)
    destination.mkdir(parents=True, exist_ok=True)
    payload_dest = destination / payload.name
    manifest_dest = destination / manifest.name
    if payload_dest.exists() or manifest_dest.exists():
        raise SystemExit("destination file collision; refusing to overwrite preserved bytes")

    shutil.copyfile(payload, payload_dest)
    shutil.copyfile(manifest, manifest_dest)
    if _sha256(payload_dest) != payload_digest or _sha256(manifest_dest) != manifest_digest:
        raise SystemExit("local copied-byte digest mismatch before commit")

    _git("add", "--", str(payload_dest), str(manifest_dest))
    staged = _git("diff", "--cached", "--name-only").stdout.splitlines()
    expected = {str(payload_dest), str(manifest_dest)}
    if set(staged) != expected:
        raise SystemExit(f"unexpected staged preservation paths: {staged}")

    _git("commit", "-m", commit_message)
    preservation_commit = _git("rev-parse", "HEAD").stdout.strip()
    _git("push", remote, f"HEAD:refs/heads/{branch}")

    remote_sha = _remote_branch_sha(remote, branch)
    if remote_sha != preservation_commit:
        raise SystemExit(
            "remote preservation ref mismatch: "
            f"observed={remote_sha} expected={preservation_commit}"
        )

    return {
        "base_commit": base_commit,
        "branch": branch,
        "destination": destination.as_posix(),
        "manifest_sha256": manifest_digest,
        "payload_sha256": payload_digest,
        "preservation_commit": preservation_commit,
        "remote": remote,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument(
        "--commit-message",
        default="readiness: preserve synthetic raw boundary probe",
    )
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    result = preserve(
        payload=args.payload,
        manifest=args.manifest,
        base_commit=args.base_commit,
        branch=args.branch,
        destination=_validate_destination(args.destination),
        remote=args.remote,
        commit_message=args.commit_message,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
