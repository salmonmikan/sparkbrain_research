from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory import ConfirmatoryManifest
from .v06_confirmatory_environment import (
    ConfirmatoryEnvironmentLock,
    EnvironmentVerificationReport,
    verify_environment_lock,
)
from .v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
    ExecutionSealReport,
    validate_execution_seal,
)


@dataclass(frozen=True, slots=True)
class GitWorkspaceState:
    head_sha: str
    status_porcelain: str
    symbolic_ref: str | None
    detached_head: bool

    @property
    def clean(self) -> bool:
        return not self.status_porcelain.strip()

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LaunchGateReport:
    seal_report: ExecutionSealReport
    environment_report: EnvironmentVerificationReport
    workspace_clean: bool
    detached_head: bool
    current_sha_matches_source: bool
    output_directory_empty: bool
    execution_counter_zero: bool
    start_marker_absent: bool
    launch_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            "current_sha_matches_source": self.current_sha_matches_source,
            "detached_head": self.detached_head,
            "environment_report": self.environment_report.state_dict(),
            "execution_counter_zero": self.execution_counter_zero,
            "launch_allowed": self.launch_allowed,
            "output_directory_empty": self.output_directory_empty,
            "seal_report": self.seal_report.state_dict(),
            "start_marker_absent": self.start_marker_absent,
            "workspace_clean": self.workspace_clean,
        }


def _git(repository_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", "-C", str(repository_root), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def inspect_git_workspace(repository_root: Path) -> GitWorkspaceState:
    repository_root = repository_root.resolve()
    head = _git(repository_root, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise RuntimeError(f"cannot read Git HEAD: {head.stderr.strip()}")
    status = _git(repository_root, "status", "--porcelain=v1", "--untracked-files=all")
    if status.returncode != 0:
        raise RuntimeError(f"cannot read Git status: {status.stderr.strip()}")
    symbolic = _git(repository_root, "symbolic-ref", "--quiet", "--short", "HEAD")
    symbolic_ref = symbolic.stdout.strip() if symbolic.returncode == 0 else None
    return GitWorkspaceState(
        head_sha=head.stdout.strip(),
        status_porcelain=status.stdout,
        symbolic_ref=symbolic_ref,
        detached_head=symbolic_ref is None,
    )


def _directory_empty(path: Path) -> bool:
    return not path.exists() or not any(path.iterdir())


def _execution_counter_zero(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        state = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return state.get("candidate_execution_count") == 0


def validate_launch_gate(
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
    expected_environment: ConfirmatoryEnvironmentLock,
    *,
    repository_root: Path,
    output_root: Path,
    execution_counter_path: Path,
    start_marker_path: Path,
    workspace: GitWorkspaceState | None = None,
    observed_environment: ConfirmatoryEnvironmentLock | None = None,
) -> LaunchGateReport:
    repository_root = repository_root.resolve()
    workspace_state = workspace or inspect_git_workspace(repository_root)
    environment_report = verify_environment_lock(
        expected_environment,
        observed_environment,
    )
    seal_report = validate_execution_seal(
        manifest,
        freeze_record,
        repository_root=repository_root,
        environment_lock=expected_environment,
    )
    checks = {
        "workspace_clean": workspace_state.clean,
        "detached_head": workspace_state.detached_head,
        "current_sha_matches_source": (
            workspace_state.head_sha == freeze_record.source_code_sha
        ),
        "output_directory_empty": _directory_empty(output_root),
        "execution_counter_zero": _execution_counter_zero(
            execution_counter_path
        ),
        "start_marker_absent": not start_marker_path.exists(),
    }
    launch_allowed = all(
        (
            seal_report.execution_allowed,
            environment_report.exact_match,
            *checks.values(),
        )
    )
    return LaunchGateReport(
        seal_report=seal_report,
        environment_report=environment_report,
        workspace_clean=checks["workspace_clean"],
        detached_head=checks["detached_head"],
        current_sha_matches_source=checks["current_sha_matches_source"],
        output_directory_empty=checks["output_directory_empty"],
        execution_counter_zero=checks["execution_counter_zero"],
        start_marker_absent=checks["start_marker_absent"],
        launch_allowed=launch_allowed,
    )


def require_launch_gate(
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
    expected_environment: ConfirmatoryEnvironmentLock,
    *,
    repository_root: Path,
    output_root: Path,
    execution_counter_path: Path,
    start_marker_path: Path,
) -> LaunchGateReport:
    report = validate_launch_gate(
        manifest,
        freeze_record,
        expected_environment,
        repository_root=repository_root,
        output_root=output_root,
        execution_counter_path=execution_counter_path,
        start_marker_path=start_marker_path,
    )
    if not report.launch_allowed:
        raise RuntimeError("confirmatory launch gate failed closed")
    return report


def claim_one_way_execution(
    start_marker_path: Path,
    *,
    freeze_record: ConfirmatoryFreezeRecord,
    launch_report: LaunchGateReport,
) -> None:
    """Create an exclusive marker immediately before candidate worlds are read."""

    if not launch_report.launch_allowed:
        raise RuntimeError("cannot claim execution without a passing launch gate")
    start_marker_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "candidate_execution_count": 1,
        "seal_hash": freeze_record.seal_hash(),
        "source_code_sha": freeze_record.source_code_sha,
        "status": "STARTED",
    }
    descriptor = os.open(
        start_marker_path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o444,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        start_marker_path.unlink(missing_ok=True)
        raise
