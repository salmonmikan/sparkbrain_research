from __future__ import annotations

import hashlib
import json
import stat
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_freeze_bundle_v2 import ExternalFreezeBundleV2
from .v06_confirmatory_normalized_resource_v2 import NormalizedResourceRecordV2

_EXPECTED_EXECUTIONS = 50 * len(ConfirmatoryCondition)
_EXPECTED_RECORDS = _EXPECTED_EXECUTIONS * len(EvidenceDomain)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_hash(root: Path) -> str:
    rows = []
    for path in sorted(row for row in root.rglob("*") if row.is_file()):
        rows.append(
            {
                "path": str(path.relative_to(root)),
                "sha256": _sha256_file(path),
                "size": path.stat().st_size,
            }
        )
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(payload).hexdigest()


def _is_read_only(path: Path) -> bool:
    return path.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH) == 0


@dataclass(frozen=True, slots=True)
class VerifiedExternalRawEvidenceV2:
    run_id: str
    raw_root: str
    raw_tree_hash: str
    envelope_hash: str
    source_git_sha: str
    execution_count: int
    evidence_record_count: int
    resource_record_count: int
    execution_ids: tuple[str, ...]
    world_keys: tuple[tuple[str, int], ...]
    condition_values: tuple[str, ...]
    all_files_read_only: bool
    top_level_checksums_valid: bool
    execution_checksums_valid: bool
    identities_valid: bool
    normalized_resources_valid: bool
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["execution_ids"] = list(self.execution_ids)
        value["world_keys"] = [list(row) for row in self.world_keys]
        value["condition_values"] = list(self.condition_values)
        return value


def verify_external_raw_evidence_v2(
    bundle: ExternalFreezeBundleV2,
) -> VerifiedExternalRawEvidenceV2:
    bundle.validate_for_execution()
    run_id = f"candidate-002-{bundle.bundle_hash()[:20]}"
    raw_root = Path(bundle.artifact_layout["raw_root"]) / run_id
    if not raw_root.is_dir() or not (raw_root / "RAW_COMPLETE").is_file():
        raise RuntimeError("immutable RAW_COMPLETE evidence is unavailable")
    if (raw_root / ".transactions").exists():
        raise RuntimeError("transaction working state entered immutable raw evidence")

    top_checksums = json.loads(
        (raw_root / "checksums.json").read_text(encoding="utf-8")
    )
    top_level_checksums_valid = all(
        top_checksums.get(name) == _sha256_file(raw_root / name)
        for name in ("raw_manifest.json", "resources.jsonl", "results.jsonl")
    )
    manifest = json.loads(
        (raw_root / "raw_manifest.json").read_text(encoding="utf-8")
    )
    envelope_hash = str(manifest.get("envelope_hash", ""))
    source_git_sha = str(manifest.get("source_git_sha", ""))
    execution_count = int(manifest.get("execution_count", -1))
    evidence_record_count = int(manifest.get("evidence_record_count", -1))
    resource_record_count = int(manifest.get("resource_record_count", -1))

    execution_root = raw_root / "executions"
    execution_paths = tuple(
        sorted(row for row in execution_root.iterdir() if row.is_dir())
    )
    execution_ids: list[str] = []
    world_keys: set[tuple[str, int]] = set()
    conditions: set[str] = set()
    identities_valid = True
    execution_checksums_valid = True
    normalized_resources_valid = True
    result_count_from_executions = 0
    resource_count_from_executions = 0

    for path in execution_paths:
        execution_ids.append(path.name)
        metadata = json.loads((path / "metadata.json").read_text(encoding="utf-8"))
        checksums = json.loads((path / "checksums.json").read_text(encoding="utf-8"))
        execution_checksums_valid = execution_checksums_valid and all(
            checksums.get(name) == _sha256_file(path / name)
            for name in ("metadata.json", "resource.json", "results.jsonl")
        )
        identities_valid = identities_valid and all(
            (
                metadata.get("execution_id") == path.name,
                metadata.get("envelope_hash") == bundle.bundle_hash(),
                metadata.get("source_git_sha") == bundle.source_git_sha,
                metadata.get("manifest_hash") == bundle.manifest_hash,
                metadata.get("world_generation_id") == bundle.world_generation_id,
                metadata.get("world_grid_hash") == bundle.world_grid_hash,
            )
        )
        family_id = str(metadata.get("family_id", ""))
        seed = int(metadata.get("seed", -1))
        condition = str(metadata.get("condition", ""))
        world_keys.add((family_id, seed))
        conditions.add(condition)
        result_rows = tuple(
            json.loads(line)
            for line in (path / "results.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        result_count_from_executions += len(result_rows)
        identities_valid = identities_valid and len(result_rows) == int(
            metadata.get("record_count", -1)
        )
        identities_valid = identities_valid and all(
            row.get("family_id") == family_id
            and int(row.get("seed", -1)) == seed
            and row.get("condition") == condition
            for row in result_rows
        )
        resource_payload = json.loads(
            (path / "resource.json").read_text(encoding="utf-8")
        )
        resource_count_from_executions += 1
        normalized_state = resource_payload.get("normalized")
        if not isinstance(normalized_state, dict):
            normalized_resources_valid = False
        else:
            try:
                normalized = NormalizedResourceRecordV2(
                    **{
                        **normalized_state,
                        "architecture_privileged_information": tuple(
                            normalized_state[
                                "architecture_privileged_information"
                            ]
                        ),
                    }
                )
                normalized.validate()
                normalized_resources_valid = normalized_resources_valid and all(
                    (
                        normalized.execution_id == path.name,
                        normalized.family_id == family_id,
                        normalized.seed == seed,
                        normalized.condition == condition,
                        normalized.world_specification_hash
                        == metadata.get("world_specification_hash"),
                    )
                )
            except (KeyError, TypeError, ValueError):
                normalized_resources_valid = False

    expected_conditions = {row.value for row in ConfirmatoryCondition}
    identities_valid = identities_valid and all(
        (
            len(execution_ids) == len(set(execution_ids)) == _EXPECTED_EXECUTIONS,
            len(world_keys) == 50,
            conditions == expected_conditions,
            result_count_from_executions == _EXPECTED_RECORDS,
            resource_count_from_executions == _EXPECTED_EXECUTIONS,
            execution_count == _EXPECTED_EXECUTIONS,
            evidence_record_count == _EXPECTED_RECORDS,
            resource_record_count == _EXPECTED_EXECUTIONS,
            envelope_hash == bundle.bundle_hash(),
            source_git_sha == bundle.source_git_sha,
        )
    )
    all_files_read_only = _is_read_only(raw_root) and all(
        _is_read_only(path) for path in raw_root.rglob("*")
    )
    complete = all(
        (
            top_level_checksums_valid,
            execution_checksums_valid,
            identities_valid,
            normalized_resources_valid,
            all_files_read_only,
        )
    )
    report = VerifiedExternalRawEvidenceV2(
        run_id=run_id,
        raw_root=str(raw_root),
        raw_tree_hash=_tree_hash(raw_root),
        envelope_hash=envelope_hash,
        source_git_sha=source_git_sha,
        execution_count=execution_count,
        evidence_record_count=evidence_record_count,
        resource_record_count=resource_record_count,
        execution_ids=tuple(execution_ids),
        world_keys=tuple(sorted(world_keys)),
        condition_values=tuple(sorted(conditions)),
        all_files_read_only=all_files_read_only,
        top_level_checksums_valid=top_level_checksums_valid,
        execution_checksums_valid=execution_checksums_valid,
        identities_valid=identities_valid,
        normalized_resources_valid=normalized_resources_valid,
        complete=complete,
    )
    if not complete:
        raise RuntimeError("external raw evidence verification failed")
    return report
