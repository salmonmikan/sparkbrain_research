"""Execution-disabled source/runtime package binding for prospective A01 MD-002.

This module fixes package identity before any capability result can be opened.  It
binds the exact source commit, boundary-critical source hashes, protocol/matrix
identities, the selected N3 source/config identity, and the exact runtime command.
It does not create an execution seal, STARTED state, capability output, score, or
scientific result.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from .md002_protocol import MD002_ID

MD002_OUTPUT_ROOT = "artifacts/v061/a01/md002/development"

_REQUIRED_SOURCE_PATHS = frozenset(
    {
        "src/sparkbrain/v061_a01/credit_bridge.py",
        "src/sparkbrain/v061_a01/md002_bound_world.py",
        "src/sparkbrain/v061_a01/md002_fixtures.py",
        "src/sparkbrain/v061_a01/md002_p2_attribution_kernel.py",
        "src/sparkbrain/v061_a01/md002_p2_schedule.py",
        "src/sparkbrain/v061_a01/md002_p3_development_plan.py",
        "src/sparkbrain/v061_a01/md002_p3_fixture.py",
        "src/sparkbrain/v061_a01/md002_p3_harness.py",
        "src/sparkbrain/v061_a01/md002_p4_fixture.py",
        "src/sparkbrain/v061_a01/md002_p4_trace_binding.py",
        "src/sparkbrain/v061_a01/md002_protocol.py",
        "src/sparkbrain/v061_a01/md002_restore_adapter.py",
        "src/sparkbrain/v061_a01/md002_state_binding.py",
        "src/sparkbrain/v061_a01/md002_world_fixture.py",
        "src/sparkbrain/v061_a01/mechanism_discrimination.py",
        "src/sparkbrain/v061_a01/recurrent_adapter.py",
        "src/sparkbrain/v061_a01/recurrent_development.py",
    }
)


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _require_sha256(value: str, *, label: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")


def _require_git_sha(value: str, *, label: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a 40-character lowercase Git SHA")


def _require_identity(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


def _require_safe_repo_path(value: str) -> None:
    _require_identity(value, label="source path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value != path.as_posix():
        raise ValueError(f"unsafe or non-canonical repository path: {value}")


@dataclass(frozen=True, slots=True)
class MD002SourceManifest:
    """Exact source identity for one prospective MD-002 package."""

    source_git_sha: str
    file_sha256: tuple[tuple[str, str], ...]

    def validate(self) -> None:
        _require_git_sha(self.source_git_sha, label="source_git_sha")
        if not self.file_sha256:
            raise ValueError("MD-002 source manifest cannot be empty")
        paths: list[str] = []
        for row in self.file_sha256:
            if not isinstance(row, tuple) or len(row) != 2:
                raise TypeError("source manifest rows must be (path, sha256) tuples")
            path, digest = row
            _require_safe_repo_path(path)
            _require_sha256(digest, label=f"source digest for {path}")
            paths.append(path)
        if tuple(sorted(paths)) != tuple(paths):
            raise ValueError("MD-002 source manifest paths must be sorted canonically")
        if len(paths) != len(set(paths)):
            raise ValueError("MD-002 source manifest paths must be unique")
        missing = sorted(_REQUIRED_SOURCE_PATHS - set(paths))
        if missing:
            raise ValueError(f"MD-002 source manifest is missing critical paths: {missing}")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "source_git_sha": self.source_git_sha,
            "files": [
                {"path": path, "sha256": digest}
                for path, digest in self.file_sha256
            ],
        }

    @property
    def manifest_sha256(self) -> str:
        return _sha256(self.state_dict())


@dataclass(frozen=True, slots=True)
class MD002RuntimeBinding:
    """Exact interpreter and command identity, with no authority semantics."""

    python_implementation: str
    python_version: str
    python_executable: str
    command: tuple[str, ...]

    def validate(self) -> None:
        for label, value in (
            ("python_implementation", self.python_implementation),
            ("python_version", self.python_version),
            ("python_executable", self.python_executable),
        ):
            _require_identity(value, label=label)
        if not self.command or any(
            not isinstance(value, str) or not value for value in self.command
        ):
            raise ValueError("MD-002 runtime command must contain non-empty string arguments")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "python_implementation": self.python_implementation,
            "python_version": self.python_version,
            "python_executable": self.python_executable,
            "command": list(self.command),
        }

    @property
    def runtime_sha256(self) -> str:
        return _sha256(self.state_dict())


@dataclass(frozen=True, slots=True)
class MD002ExecutionDisabledPackage:
    """Prospective package identity; capability remains explicitly unopened."""

    source_manifest: MD002SourceManifest
    runtime: MD002RuntimeBinding
    protocol_sha256: str
    matrix_sha256: str
    n3_source_git_sha: str
    n3_config_sha256: str
    resource_matching_policy_sha256: str
    raw_artifact_schema_sha256: str

    def validate(self) -> None:
        self.source_manifest.validate()
        self.runtime.validate()
        for label in (
            "protocol_sha256",
            "matrix_sha256",
            "n3_config_sha256",
            "resource_matching_policy_sha256",
            "raw_artifact_schema_sha256",
        ):
            _require_sha256(getattr(self, label), label=label)
        _require_git_sha(self.n3_source_git_sha, label="n3_source_git_sha")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": "v061-a01-md002-execution-disabled-package-v1",
            "md002_id": MD002_ID,
            "source_manifest": self.source_manifest.state_dict(),
            "source_manifest_sha256": self.source_manifest.manifest_sha256,
            "runtime": self.runtime.state_dict(),
            "runtime_sha256": self.runtime.runtime_sha256,
            "protocol_sha256": self.protocol_sha256,
            "matrix_sha256": self.matrix_sha256,
            "n3_source_git_sha": self.n3_source_git_sha,
            "n3_config_sha256": self.n3_config_sha256,
            "resource_matching_policy_sha256": self.resource_matching_policy_sha256,
            "raw_artifact_schema_sha256": self.raw_artifact_schema_sha256,
            "capability_output_opened": False,
            "execution_seal_issued": False,
            "started": False,
            "formal_execution_allowed": False,
        }

    @property
    def package_sha256(self) -> str:
        return _sha256(self.state_dict())

    @property
    def output_relpath(self) -> str:
        """One deterministic no-clobber namespace for this exact package identity."""

        return f"{MD002_OUTPUT_ROOT}/package-{self.package_sha256}"


__all__ = [
    "MD002ExecutionDisabledPackage",
    "MD002RuntimeBinding",
    "MD002SourceManifest",
    "MD002_OUTPUT_ROOT",
]
