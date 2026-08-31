from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory_execution_seal import ConfirmatoryFreezeRecord

_EXTERNAL_FREEZE_VERSION = "v06-external-freeze-envelope-1"
_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


@dataclass(frozen=True, slots=True)
class ExternalArtifactLayout:
    """Absolute, source-external control/raw/analysis locations.

    The three roots are deliberately outside the detached source checkout. This
    lets the launcher require a clean source tree while raw evidence is written
    and sealed elsewhere.
    """

    control_root: str
    raw_root: str
    analysis_root: str

    def resolved(self) -> tuple[Path, Path, Path]:
        return tuple(  # type: ignore[return-value]
            _resolved(Path(value))
            for value in (
                self.control_root,
                self.raw_root,
                self.analysis_root,
            )
        )

    def validate(self, *, source_checkout: Path) -> None:
        source = _resolved(source_checkout)
        roots = self.resolved()
        if any(not Path(value).is_absolute() for value in asdict(self).values()):
            raise ValueError("all confirmatory artifact roots must be absolute")
        if len(set(roots)) != 3:
            raise ValueError("control, raw, and analysis roots must be distinct")
        if any(_is_relative_to(root, source) for root in roots):
            raise ValueError("confirmatory artifacts must remain outside source checkout")
        for root in roots:
            for other in roots:
                if root == other:
                    continue
                if _is_relative_to(root, other):
                    raise ValueError("confirmatory artifact roots cannot be nested")

    def state_dict(self) -> dict[str, str]:
        control, raw, analysis = self.resolved()
        return {
            "analysis_root": str(analysis),
            "control_root": str(control),
            "raw_root": str(raw),
        }

    def layout_hash(self) -> str:
        return _digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ExternalFreezeEnvelope:
    envelope_version: str
    source_git_sha: str
    detached_checkout: str
    freeze_record: dict[str, Any]
    freeze_record_hash: str
    artifact_layout: dict[str, str]
    artifact_layout_hash: str
    execution_counter_initial: int
    created_by: str

    def validate(self) -> None:
        if self.envelope_version != _EXTERNAL_FREEZE_VERSION:
            raise ValueError("unexpected external freeze envelope version")
        if not _SHA_PATTERN.fullmatch(self.source_git_sha):
            raise ValueError("source_git_sha must be a lowercase 40-character SHA")
        checkout = Path(self.detached_checkout)
        if not checkout.is_absolute():
            raise ValueError("detached checkout path must be absolute")
        if not self.created_by.strip():
            raise ValueError("external freeze envelope requires a builder identity")
        if self.execution_counter_initial != 0:
            raise ValueError("fresh confirmatory execution counter must begin at zero")
        if self.freeze_record_hash != _digest(self.freeze_record):
            raise ValueError("freeze record hash mismatch")
        if self.artifact_layout_hash != _digest(self.artifact_layout):
            raise ValueError("artifact layout hash mismatch")
        if self.freeze_record.get("code_ref") != self.source_git_sha:
            raise ValueError("freeze record must reference the detached source SHA")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def envelope_hash(self) -> str:
        return _digest(self.state_dict())


def build_external_freeze_envelope(
    freeze_record: ConfirmatoryFreezeRecord,
    *,
    source_checkout: Path,
    artifact_layout: ExternalArtifactLayout,
    created_by: str,
) -> ExternalFreezeEnvelope:
    """Build an external envelope without changing the source Git SHA.

    The envelope may be stored in an immutable object store or a separate
    control directory. It references, but is not committed into, the source
    checkout whose SHA is executed.
    """

    source = _resolved(source_checkout)
    artifact_layout.validate(source_checkout=source)
    freeze_state = freeze_record.state_dict()
    layout_state = artifact_layout.state_dict()
    envelope = ExternalFreezeEnvelope(
        envelope_version=_EXTERNAL_FREEZE_VERSION,
        source_git_sha=freeze_record.code_ref,
        detached_checkout=str(source),
        freeze_record=freeze_state,
        freeze_record_hash=_digest(freeze_state),
        artifact_layout=layout_state,
        artifact_layout_hash=_digest(layout_state),
        execution_counter_initial=0,
        created_by=created_by,
    )
    envelope.validate()
    return envelope


def write_external_freeze_envelope(
    envelope: ExternalFreezeEnvelope,
    *,
    path: Path,
) -> str:
    """Create an immutable external envelope using exclusive atomic creation."""

    envelope.validate()
    target = _resolved(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = (_canonical_json(envelope.state_dict()) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(target, flags, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(target, 0o444)
    return hashlib.sha256(encoded).hexdigest()


def read_external_freeze_envelope(path: Path) -> ExternalFreezeEnvelope:
    state = json.loads(_resolved(path).read_text(encoding="utf-8"))
    envelope = ExternalFreezeEnvelope(**state)
    envelope.validate()
    return envelope


def verify_external_envelope_file(path: Path) -> tuple[ExternalFreezeEnvelope, str]:
    target = _resolved(path)
    payload = target.read_bytes()
    envelope = read_external_freeze_envelope(target)
    return envelope, hashlib.sha256(payload).hexdigest()
