"""Read-only engineering verification of reserved protocol-v2 fixture packages.

Expected values must come from the caller's reviewed fixture contract, never
from the package being checked. This is not formal approval or source-checkout
attestation. Formal candidates are refused before preparation or seed selection.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from .candidate import CandidatePurpose, CandidateSpec
from .prepare import prepare_outcome_blind_bundle

PREPARED_FILES = frozenset({
    "candidate.json",
    "declarations.jsonl",
    "formal_seed_selection.json",
    "formal_structure_audit.json",
    "formal_identifiability_audit.json",
    "freeze_manifest.json",
})


def verify_reserved_fixture_bundle(
    *,
    output_dir: Path,
    expected_candidate: CandidateSpec,
    expected_source_git_sha: str,
    expected_builder: str,
    expected_execution_command: str,
    expected_artifact_root: str,
) -> dict[str, str]:
    """Reconstruct and compare all six canonical payloads; return raw digests.

The existing prepare path reconstructs worlds, declarations, audits, and every
freeze binding without instantiating comparator capability. Exact byte equality
also rejects extra keys, duplicate JSON keys, scalar coercions, altered status,
and cardinality errors. No package-supplied checksum or success flag is trusted.
The directory must be quiescent during this local check.
"""
    expected_candidate.validate()
    if expected_candidate.purpose is not CandidatePurpose.STRUCTURE_FIXTURE:
        raise ValueError("verification is restricted to reserved structure fixtures")
    if output_dir.is_symlink() or not output_dir.is_dir():
        raise ValueError("package must be a real directory")
    entries = {entry.name: entry for entry in output_dir.iterdir()}
    if set(entries) != PREPARED_FILES:
        raise ValueError("package must contain exactly the six protocol-v2 payloads")
    if any(entry.is_symlink() or not entry.is_file() for entry in entries.values()):
        raise ValueError("every payload must be a regular file, not a symlink")

    with TemporaryDirectory(prefix="cx01-reserved-verification-") as temporary:
        reference = Path(temporary) / "reference"
        prepare_outcome_blind_bundle(
            generation_id=expected_candidate.generation_id,
            seeds=expected_candidate.seeds,
            purpose=expected_candidate.purpose,
            source_git_sha=expected_source_git_sha,
            builder=expected_builder,
            execution_command=expected_execution_command,
            artifact_root=expected_artifact_root,
            output_dir=reference,
        )
        digests = {}
        for name in sorted(PREPARED_FILES):
            payload = entries[name].read_bytes()
            if payload != (reference / name).read_bytes():
                raise ValueError(f"payload differs from reviewed fixture reconstruction: {name}")
            digests[name] = hashlib.sha256(payload).hexdigest()
    return digests
