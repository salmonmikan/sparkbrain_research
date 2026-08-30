from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
    require_execution_seal,
)
from .v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
    ExternalFreezeEnvelope,
)

_STARTED_MARKER = "STARTED.json"
_ALLOWED_CONTROL_FILES = frozenset(
    {
        "freeze_envelope.json",
        "freeze_envelope.sha256",
        "environment_lock.json",
        "environment_lock.sha256",
        "independent_verification.json",
        "independent_verification.sha256",
    }
)


def _run_git(source: Path, *arguments: str, check: bool = True) -> str:
    completed = subprocess.run(
        ("git", "-C", str(source), *arguments),
        check=check,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _directory_entries(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    return tuple(sorted(row.name for row in path.iterdir()))


@dataclass(frozen=True, slots=True)
class ExternalLaunchGateReport:
    source_checkout_absolute: bool
    source_checkout_clean: bool
    source_sha_matches: bool
    source_is_detached: bool
    envelope_valid: bool
    execution_seal_valid: bool
    control_layout_valid: bool
    raw_output_empty: bool
    analysis_output_empty: bool
    execution_counter_zero: bool
    started_marker_absent: bool
    execution_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_external_launch_gate(
    envelope: ExternalFreezeEnvelope,
    freeze_record: ConfirmatoryFreezeRecord,
    *,
    manifest,
) -> ExternalLaunchGateReport:
    """Validate the final machine gate without opening candidate worlds."""

    envelope_valid = True
    try:
        envelope.validate()
    except ValueError:
        envelope_valid = False

    source = Path(envelope.detached_checkout)
    layout = ExternalArtifactLayout(**envelope.artifact_layout)
    try:
        layout.validate(source_checkout=source)
        layout_valid = True
    except ValueError:
        layout_valid = False
    control_root, raw_root, analysis_root = layout.resolved()

    source_checkout_absolute = source.is_absolute()
    source_checkout_clean = False
    source_sha_matches = False
    source_is_detached = False
    if source_checkout_absolute and source.exists():
        try:
            source_checkout_clean = _run_git(source, "status", "--porcelain") == ""
            source_sha_matches = (
                _run_git(source, "rev-parse", "HEAD") == envelope.source_git_sha
            )
            symbolic = subprocess.run(
                ("git", "-C", str(source), "symbolic-ref", "-q", "HEAD"),
                check=False,
                capture_output=True,
                text=True,
            )
            source_is_detached = symbolic.returncode != 0
        except (OSError, subprocess.CalledProcessError):
            pass

    execution_seal_valid = False
    try:
        require_execution_seal(manifest, freeze_record)
        execution_seal_valid = (
            freeze_record.state_dict() == envelope.freeze_record
            and freeze_record.code_ref == envelope.source_git_sha
        )
    except (RuntimeError, ValueError):
        pass

    control_entries = set(_directory_entries(control_root))
    control_layout_valid = (
        layout_valid
        and control_entries.issubset(_ALLOWED_CONTROL_FILES)
        and "freeze_envelope.json" in control_entries
    )
    raw_output_empty = not _directory_entries(raw_root)
    analysis_output_empty = not _directory_entries(analysis_root)
    counter_file = control_root / "candidate_execution_counter.json"
    execution_counter_zero = envelope.execution_counter_initial == 0
    if counter_file.exists():
        try:
            counter_state = json.loads(counter_file.read_text(encoding="utf-8"))
            execution_counter_zero = int(counter_state["count"]) == 0
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            execution_counter_zero = False
    started_marker_absent = not (control_root / _STARTED_MARKER).exists()

    checks = (
        source_checkout_absolute,
        source_checkout_clean,
        source_sha_matches,
        source_is_detached,
        envelope_valid,
        execution_seal_valid,
        control_layout_valid,
        raw_output_empty,
        analysis_output_empty,
        execution_counter_zero,
        started_marker_absent,
    )
    return ExternalLaunchGateReport(
        source_checkout_absolute=source_checkout_absolute,
        source_checkout_clean=source_checkout_clean,
        source_sha_matches=source_sha_matches,
        source_is_detached=source_is_detached,
        envelope_valid=envelope_valid,
        execution_seal_valid=execution_seal_valid,
        control_layout_valid=control_layout_valid,
        raw_output_empty=raw_output_empty,
        analysis_output_empty=analysis_output_empty,
        execution_counter_zero=execution_counter_zero,
        started_marker_absent=started_marker_absent,
        execution_allowed=all(checks),
    )


def require_external_launch_gate(
    envelope: ExternalFreezeEnvelope,
    freeze_record: ConfirmatoryFreezeRecord,
    *,
    manifest,
) -> ExternalLaunchGateReport:
    report = validate_external_launch_gate(
        envelope,
        freeze_record,
        manifest=manifest,
    )
    if not report.execution_allowed:
        raise RuntimeError("external confirmatory launch gate remains closed")
    return report


def claim_one_way_execution(
    envelope: ExternalFreezeEnvelope,
    report: ExternalLaunchGateReport,
) -> Path:
    """Create the irreversible STARTED marker after all launch checks pass."""

    if not report.execution_allowed:
        raise RuntimeError("cannot claim execution before launch gate passes")
    control_root = Path(envelope.artifact_layout["control_root"])
    control_root.mkdir(parents=True, exist_ok=True)
    marker = control_root / _STARTED_MARKER
    payload = {
        "envelope_hash": envelope.envelope_hash(),
        "source_git_sha": envelope.source_git_sha,
        "state": "STARTED",
    }
    encoded = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )
    descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(marker, 0o444)
    return marker
