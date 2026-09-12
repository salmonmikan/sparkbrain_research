"""Exact-checkout verifier for the prospective RV01 R01-16 package.

The existing development-package contract binds a Git SHA and byte hashes for
boundary-critical source paths. This module verifies those declarations against
the actual checkout before any later construction/capability runner is allowed
to treat the manifest as evidence. It grants no execution authority.
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .rv01_r01_16_development_package import R0116SourceManifest

_SOURCE_BINDING_PATH = "src/sparkbrain/research/rv01_r01_16_source_binding.py"


@dataclass(frozen=True, slots=True)
class R0116VerifiedSourceCheckout:
    source_git_sha: str
    source_manifest_sha256: str
    verified_paths: tuple[str, ...]

    def state_dict(self) -> dict[str, object]:
        return {
            "source_git_sha": self.source_git_sha,
            "source_manifest_sha256": self.source_manifest_sha256,
            "verified_paths": list(self.verified_paths),
            "tracked_checkout_clean": True,
            "source_bytes_verified": True,
            "execution_authority_granted": False,
        }


def _git(repo_root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(f"R01-16 source checkout requires git: {exc}") from exc
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise RuntimeError(f"R01-16 source checkout verification failed: {detail}")
    return result.stdout.strip()


def verify_r01_16_source_checkout(
    repo_root: Path,
    manifest: R0116SourceManifest,
) -> R0116VerifiedSourceCheckout:
    """Fail closed unless the checkout exactly realizes the bound source manifest."""

    manifest.validate()
    manifest_paths = {row.path for row in manifest.entries}
    if _SOURCE_BINDING_PATH not in manifest_paths:
        raise ValueError("R01-16 source manifest must bind the source verifier itself")

    root = repo_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("R01-16 repository root must be a directory")

    head = _git(root, "rev-parse", "HEAD")
    if head != manifest.source_git_sha:
        raise ValueError(
            "R01-16 source Git SHA mismatch: "
            f"expected {manifest.source_git_sha}, got {head}"
        )

    tracked_status = _git(root, "status", "--porcelain", "--untracked-files=no")
    if tracked_status:
        raise ValueError("R01-16 source checkout has modified tracked files")

    verified: list[str] = []
    for entry in sorted(manifest.entries, key=lambda row: row.path):
        candidate = root / entry.path
        try:
            resolved = candidate.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ValueError(f"R01-16 source path is missing: {entry.path}") from exc
        if not resolved.is_relative_to(root):
            raise ValueError(f"R01-16 source path escapes repository root: {entry.path}")
        if not resolved.is_file():
            raise ValueError(f"R01-16 source path is not a regular file: {entry.path}")
        actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
        if actual != entry.sha256:
            raise ValueError(
                f"R01-16 source digest mismatch for {entry.path}: "
                f"expected {entry.sha256}, got {actual}"
            )
        verified.append(entry.path)

    result = R0116VerifiedSourceCheckout(
        source_git_sha=head,
        source_manifest_sha256=manifest.manifest_sha256,
        verified_paths=tuple(verified),
    )
    if tuple(verified) != tuple(sorted(row.path for row in manifest.entries)):
        raise RuntimeError("R01-16 verified source path order drifted")
    return result


__all__ = ["R0116VerifiedSourceCheckout", "verify_r01_16_source_checkout"]
