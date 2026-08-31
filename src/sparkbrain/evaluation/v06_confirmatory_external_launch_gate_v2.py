from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory_environment_lock_v2 import (
    capture_environment_lock_v2,
    environment_locks_equal,
)
from .v06_confirmatory_external_freeze import ExternalArtifactLayout
from .v06_confirmatory_external_verification_v2 import (
    _environment_from_state,
    independently_verify_external_bundle_v2,
)
from .v06_confirmatory_freeze_bundle_v2 import ExternalFreezeBundleV2

_ALLOWED_CONTROL_FILES = frozenset(
    {
        "candidate_execution_counter.json",
        "environment_lock.json",
        "environment_lock.sha256",
        "freeze_bundle.json",
        "freeze_bundle.sha256",
        "independent_verification.json",
        "independent_verification.sha256",
    }
)
_STARTED_MARKER = "STARTED.json"
_STARTED_COUNTER = "candidate_execution_counter.1.json"


def _git(source: Path, *arguments: str, check: bool = True) -> str:
    return subprocess.run(
        ("git", "-C", str(source), *arguments),
        check=check,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _entries(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    return tuple(sorted(row.name for row in path.iterdir()))


def _read_counter(path: Path, bundle_hash: str) -> bool:
    if not path.is_file():
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value == {"bundle_hash": bundle_hash, "count": 0}
    except json.JSONDecodeError:
        return False


@dataclass(frozen=True, slots=True)
class ExternalLaunchGateReportV2:
    bundle_execution_ready: bool
    source_checkout_exists: bool
    source_checkout_clean: bool
    source_sha_matches: bool
    source_is_detached: bool
    independent_rebuild_matches: bool
    environment_matches: bool
    control_package_exact: bool
    candidate_counter_zero: bool
    raw_root_empty: bool
    analysis_root_empty: bool
    started_marker_absent: bool
    started_counter_absent: bool
    execution_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_external_launch_gate_v2(
    bundle: ExternalFreezeBundleV2,
) -> ExternalLaunchGateReportV2:
    """Rebuild and verify every frozen input before candidate import."""

    bundle_execution_ready = True
    try:
        bundle.validate_for_execution()
    except ValueError:
        bundle_execution_ready = False

    source = Path(bundle.source_checkout)
    source_checkout_exists = source.is_absolute() and source.is_dir()
    source_checkout_clean = False
    source_sha_matches = False
    source_is_detached = False
    if source_checkout_exists:
        try:
            source_checkout_clean = _git(source, "status", "--porcelain") == ""
            source_sha_matches = _git(source, "rev-parse", "HEAD") == bundle.source_git_sha
            attached = subprocess.run(
                ("git", "-C", str(source), "symbolic-ref", "-q", "HEAD"),
                check=False,
                capture_output=True,
                text=True,
            )
            source_is_detached = attached.returncode != 0
        except (OSError, subprocess.CalledProcessError):
            pass

    environment_matches = False
    independent_rebuild_matches = False
    if bundle_execution_ready and source_checkout_exists:
        try:
            observed_environment = capture_environment_lock_v2()
            expected_environment = _environment_from_state(bundle.environment_lock)
            environment_matches = environment_locks_equal(
                expected_environment,
                observed_environment,
            )
            _, verification = independently_verify_external_bundle_v2(
                bundle,
                source_root=source,
                environment_lock=observed_environment,
                reviewer=bundle.reviewer or "missing-reviewer",
                issue_approval=False,
            )
            independent_rebuild_matches = verification.verification_passed
        except (OSError, RuntimeError, ValueError):
            pass

    layout = ExternalArtifactLayout(**bundle.artifact_layout)
    try:
        layout.validate(source_checkout=source)
        layout_valid = True
    except ValueError:
        layout_valid = False
    control_root, raw_root, analysis_root = layout.resolved()
    control_entries = set(_entries(control_root))
    control_package_exact = (
        layout_valid
        and control_entries == _ALLOWED_CONTROL_FILES
        and not (control_root / _STARTED_MARKER).exists()
        and not (control_root / _STARTED_COUNTER).exists()
    )
    bundle_hash = bundle.bundle_hash()
    candidate_counter_zero = _read_counter(
        control_root / "candidate_execution_counter.json",
        bundle_hash,
    )
    raw_root_empty = not _entries(raw_root)
    analysis_root_empty = not _entries(analysis_root)
    started_marker_absent = not (control_root / _STARTED_MARKER).exists()
    started_counter_absent = not (control_root / _STARTED_COUNTER).exists()
    checks = (
        bundle_execution_ready,
        source_checkout_exists,
        source_checkout_clean,
        source_sha_matches,
        source_is_detached,
        independent_rebuild_matches,
        environment_matches,
        control_package_exact,
        candidate_counter_zero,
        raw_root_empty,
        analysis_root_empty,
        started_marker_absent,
        started_counter_absent,
    )
    return ExternalLaunchGateReportV2(
        bundle_execution_ready=bundle_execution_ready,
        source_checkout_exists=source_checkout_exists,
        source_checkout_clean=source_checkout_clean,
        source_sha_matches=source_sha_matches,
        source_is_detached=source_is_detached,
        independent_rebuild_matches=independent_rebuild_matches,
        environment_matches=environment_matches,
        control_package_exact=control_package_exact,
        candidate_counter_zero=candidate_counter_zero,
        raw_root_empty=raw_root_empty,
        analysis_root_empty=analysis_root_empty,
        started_marker_absent=started_marker_absent,
        started_counter_absent=started_counter_absent,
        execution_allowed=all(checks),
    )


def require_external_launch_gate_v2(
    bundle: ExternalFreezeBundleV2,
) -> ExternalLaunchGateReportV2:
    report = validate_external_launch_gate_v2(bundle)
    if not report.execution_allowed:
        raise RuntimeError("candidate-003 launch gate remains closed")
    return report


def _write_exclusive(path: Path, value: object) -> None:
    payload = (
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)


def claim_external_one_way_execution_v2(
    bundle: ExternalFreezeBundleV2,
    report: ExternalLaunchGateReportV2,
) -> tuple[Path, Path]:
    """Irreversibly consume the zero counter after the gate passes."""

    if not report.execution_allowed:
        raise RuntimeError("cannot claim candidate execution while launch gate is closed")
    control_root = Path(bundle.artifact_layout["control_root"])
    marker = control_root / _STARTED_MARKER
    counter = control_root / _STARTED_COUNTER
    state = {
        "bundle_hash": bundle.bundle_hash(),
        "source_git_sha": bundle.source_git_sha,
        "state": "STARTED",
    }
    _write_exclusive(marker, state)
    try:
        _write_exclusive(
            counter,
            {"bundle_hash": bundle.bundle_hash(), "count": 1},
        )
    except BaseException:
        # The STARTED marker deliberately remains. A partial claim is terminal
        # and cannot be retried as a fresh confirmatory execution.
        raise
    return marker, counter
