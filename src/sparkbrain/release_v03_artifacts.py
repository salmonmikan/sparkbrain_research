"""C20 source-only generation for the final v0.3 release evidence layer.

The generator writes to a caller-selected destination.  It does not alter the
historical v0.2.1 evidence tree and does not infer a C19 outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from sparkbrain.release import build_release_manifest, build_release_metadata, sha256_file

V03_RELEASE_RELATIVE = "artifacts/release/v0.3"
V03_EVIDENCE_SCHEMA = "sparkbrain-v03-evidence-map-v1"
V03_SOURCE_MANIFEST_SCHEMA = "sparkbrain-v03-release-source-manifest-v1"
V03_RELEASE_REPORT_SCHEMA = "sparkbrain-v03-release-report-v1"
V03_RELEASE_METADATA_SCHEMA = "sparkbrain-v03-release-metadata-v1"
V03_PRIMARY_SUBSET_SCHEMA = "sparkbrain-v03-primary-subset-v1"
V03_REPRODUCTION_MANIFEST_SCHEMA = "sparkbrain-v03-reproduction-manifest-v1"
V03_SOURCE_LICENSE_INVENTORY_SCHEMA = "sparkbrain-v03-source-license-inventory-v1"
C19_BLOCKED_ARTIFACTS = (
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/attribution_rows.jsonl",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/baseline_matching.json",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/failure_examples.jsonl",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/frozen_protocol.json",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/metrics_by_condition.json",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/paired_statistics.json",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/raw_predictions.jsonl",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/report.md",
    "artifacts/v03/c19_external_validation/blocked-readiness-v1/run_manifest.jsonl",
)

_V03_ENTRIES = (
    (
        "EV-V03-C11",
        "accepted",
        "C11 five-seed input-bottleneck diagnosis; no evidence-grade upgrade.",
        ("CL-003", "CL-004"),
        (
            "artifacts/v03/c11_input_diagnosis/diagnostic_manifest.json",
            "artifacts/v03/c11_input_diagnosis/metrics_by_input_track.json",
            "artifacts/v03/c11_input_diagnosis/failure_examples.jsonl",
        ),
    ),
    (
        "EV-V03-C12",
        "accepted",
        "Synthetic sensory-gate engineering evidence only; no biological perception claim.",
        ("CL-011",),
        (
            "artifacts/v03/c12_sensory_field/protocol.json",
            "artifacts/v03/c12_sensory_field/ablation_metrics.json",
            "artifacts/v03/c12_sensory_field/report.md",
        ),
    ),
    (
        "EV-V03-C13",
        "accepted",
        "Oracle entity scope is a condition-separated synthetic diagnosis, not autonomous binding.",
        ("CL-001",),
        (
            "artifacts/v03/c13_evidence_entity/protocol.json",
            "artifacts/v03/c13_evidence_entity/entity_condition_metrics.json",
            "artifacts/v03/c13_evidence_entity/evidence_invariant_tests.json",
        ),
    ),
    (
        "EV-V03-C14",
        "accepted",
        "Fixed-logit Coalition intervention evidence only; no external-performance claim.",
        ("CL-002",),
        (
            "artifacts/v03/c14_coalition_gate/protocol.json",
            "artifacts/v03/c14_coalition_gate/gate_ablation_metrics.json",
            "artifacts/v03/c14_coalition_gate/causal_evidence_removal.jsonl",
        ),
    ),
    (
        "EV-V03-C15",
        "negative",
        "Engineering acceptance does not support residual superiority or a claim-grade increase.",
        ("CL-003", "CL-004", "CL-006"),
        (
            "artifacts/v03/c15_revision_v4/protocol.json",
            "artifacts/v03/c15_revision_v4/loss_ablation_metrics.json",
            "artifacts/v03/c15_revision_v4/report.md",
        ),
    ),
    (
        "EV-V03-C16",
        "accepted",
        "Bounded synthetic candidate evidence; no semantic or biological interpretation.",
        (),
        (
            "artifacts/v03/c16_proto_concepts/protocol.json",
            "artifacts/v03/c16_proto_concepts/candidate_metrics.json",
            "artifacts/v03/c16_proto_concepts/failure_examples.jsonl",
        ),
    ),
    (
        "EV-V03-C17",
        "negative",
        "C17 v2 engineering completion is a candidate-absence scientific negative; "
        "CL-008 remains E0.",
        ("CL-008",),
        (
            "artifacts/v03/c17_functional_organs_v2/preregistration.json",
            "artifacts/v03/c17_functional_organs_v2/acceptance_matrix.json",
            "artifacts/v03/c17_functional_organs_v2/report.md",
        ),
    ),
    (
        "EV-V03-C18",
        "accepted",
        "Deterministic trace/checkpoint observability only; no scientific support claim.",
        ("CL-011",),
        (
            "artifacts/v03/c18_brain_lab_v6/preregistration.json",
            "artifacts/v03/c18_brain_lab_v6/checkpoint_manifest.json",
            "artifacts/v03/c18_brain_lab_v6/report.md",
        ),
    ),
    (
        "EV-V02-C06-NEGATIVE",
        "negative",
        "Retained official external negative result; no measured frontier improvement.",
        ("CL-007",),
        (
            "artifacts/external_validation/c06-final-official/run_manifest.json",
            "artifacts/external_validation/c06-final-official/belief_r_metrics.json",
        ),
    ),
    (
        "EV-V02-C08-NEGATIVE",
        "negative",
        "Retained structural-plasticity negative; no emergent-organ claim.",
        ("CL-008",),
        (
            "artifacts/phase3/structural-plasticity-v1/main/gate-matrix.json",
            "artifacts/phase3/structural-plasticity-v1/main/negative-findings.json",
        ),
    ),
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _revision(value: str) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise ValueError("source_revision must be a full lowercase Git SHA")
    return value


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_files(root: Path, paths: Iterable[str]) -> None:
    missing = [relative for relative in paths if not (root / relative).is_file()]
    if missing:
        raise ValueError("v0.3 evidence source files are missing: " + ", ".join(sorted(missing)))


def build_v03_evidence_map(
    root: Path,
    *,
    source_revision: str,
) -> dict[str, Any]:
    revision = _revision(source_revision)
    from sparkbrain.v03_external_validation.readiness import validate_bundle

    c19_paths = C19_BLOCKED_ARTIFACTS
    try:
        validate_bundle(
            root / "artifacts/v03/c19_external_validation/blocked-readiness-v1", root=root
        )
    except (OSError, ValueError) as exc:
        raise ValueError(f"C19 blocked readiness semantic pin is invalid: {exc}") from exc
    entries = []
    for entry_id, status, boundary, claim_ids, artifacts in _V03_ENTRIES:
        _require_files(root, artifacts)
        entries.append(
            {
                "id": entry_id,
                "status": status,
                "claim_ids": list(claim_ids),
                "artifacts": list(artifacts),
                "boundary": boundary,
            }
        )
    _require_files(root, c19_paths)
    entries.append(
        {
            "id": "EV-V03-C19",
            "status": "blocked",
            "claim_ids": ["CL-007"],
            "artifacts": list(c19_paths),
            "boundary": (
                "C19/G09 is not accepted and science is not_evaluated: the truth-free "
                "Belief-R-to-I2 adapter and a new official-evaluation protocol are absent."
            ),
        }
    )
    return {
        "schema_version": V03_EVIDENCE_SCHEMA,
        "source_revision": revision,
        "entries": entries,
    }


def validate_v03_evidence_map(root: Path, payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["v0.3 evidence map must be a JSON object"]
    problems: list[str] = []
    if set(payload) != {"schema_version", "source_revision", "entries"}:
        problems.append("v0.3 evidence map fields do not match fixed schema")
    if payload.get("schema_version") != V03_EVIDENCE_SCHEMA:
        problems.append("unsupported v0.3 evidence-map schema version")
    try:
        _revision(payload.get("source_revision"))
    except (TypeError, ValueError):
        problems.append("v0.3 evidence map source_revision must be a full lowercase Git SHA")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        return [*problems, "v0.3 evidence map entries must be an array"]
    expected_ids = {entry[0] for entry in _V03_ENTRIES} | {"EV-V03-C19"}
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        required = {"id", "status", "claim_ids", "artifacts", "boundary"}
        if not isinstance(entry, dict) or set(entry) != required:
            problems.append(f"v0.3 evidence entries[{index}] has invalid fields")
            continue
        entry_id = entry["id"]
        if not isinstance(entry_id, str) or entry_id not in expected_ids or entry_id in seen:
            problems.append(f"v0.3 evidence entries[{index}] has an invalid id")
        seen.add(entry_id)
        if entry["status"] not in {"accepted", "blocked", "negative"}:
            problems.append(f"v0.3 evidence {entry_id} has an invalid status")
        if not isinstance(entry["claim_ids"], list) or not all(
            isinstance(value, str) for value in entry["claim_ids"]
        ):
            problems.append(f"v0.3 evidence {entry_id} claim_ids must be a string array")
        if not isinstance(entry["artifacts"], list) or not all(
            isinstance(value, str) for value in entry["artifacts"]
        ):
            problems.append(f"v0.3 evidence {entry_id} artifacts must be a string array")
        elif entry_id == "EV-V03-C19" and (
            entry["status"] != "blocked"
            or tuple(entry["artifacts"]) != C19_BLOCKED_ARTIFACTS
        ):
            problems.append("blocked C19 evidence must carry the exact-nine readiness artifact pin")
        else:
            for relative in entry["artifacts"]:
                if not (root / relative).is_file():
                    problems.append(f"v0.3 evidence artifact is missing: {relative}")
        if not isinstance(entry["boundary"], str) or not entry["boundary"].strip():
            problems.append(f"v0.3 evidence {entry_id} boundary must be non-empty")
    if seen != expected_ids:
        problems.append("v0.3 evidence ids do not match the fixed C11-C19 inventory")
    try:
        from sparkbrain.v03_external_validation.readiness import validate_bundle

        validate_bundle(
            root / "artifacts/v03/c19_external_validation/blocked-readiness-v1", root=root
        )
    except (OSError, ValueError) as exc:
        problems.append(f"C19 blocked readiness semantic pin is invalid: {exc}")
    return sorted(set(problems))


def _render_results_table(evidence: dict[str, Any]) -> str:
    lines = [
        "# SparkBrain v0.3 release evidence summary",
        "",
        "This table is generated from the v0.3 evidence map. It does not change claim grades.",
        "",
        "| Evidence | Release status | Boundary |",
        "| --- | --- | --- |",
    ]
    for entry in evidence["entries"]:
        lines.append(f"| {entry['id']} | {entry['status']} | {entry['boundary']} |")
    return "\n".join(lines) + "\n"


def _render_results_figure(evidence: dict[str, Any]) -> str:
    colors = {"accepted": "#2e7d32", "negative": "#c62828", "blocked": "#6d6d6d"}
    height = 48 + 28 * len(evidence["entries"])
    bars = []
    for index, entry in enumerate(evidence["entries"]):
        y = 24 + index * 28
        bars.append(
            f'<text x="8" y="{y + 14}" font-size="12">{entry["id"]}</text>'
            f'<rect x="150" y="{y}" width="180" height="18" fill="{colors[entry["status"]]}"/>'
            f'<text x="338" y="{y + 14}" font-size="12">{entry["status"]}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="460" height="{height}" '
        'viewBox="0 0 460 '
        f'{height}"><title>SparkBrain v0.3 evidence status</title>{"".join(bars)}</svg>\n'
    )


def _render_claim_boundary_figure(evidence: dict[str, Any]) -> str:
    rows = [
        entry
        for entry in evidence["entries"]
        if entry["status"] in {"blocked", "negative"}
    ]
    height = 48 + 28 * len(rows)
    labels = "".join(
        f'<text x="8" y="{24 + index * 28}" font-size="12">'
        f'{entry["id"]}: {entry["status"]}</text>'
        for index, entry in enumerate(rows)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="460" height="{height}" '
        f'viewBox="0 0 460 {height}"><title>SparkBrain v0.3 claim boundaries</title>'
        f'{labels}</svg>\n'
    )


def build_v03_primary_subset(evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": V03_PRIMARY_SUBSET_SCHEMA,
        "source_revision": evidence["source_revision"],
        "full_evaluation": False,
        "entries": [
            {
                "id": entry["id"],
                "status": entry["status"],
                "claim_ids": entry["claim_ids"],
            }
            for entry in evidence["entries"]
        ],
        "boundary": "This is a release index, not a performance evaluation or claim-grade upgrade.",
    }


def build_v03_reproduction_manifest(source_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": V03_REPRODUCTION_MANIFEST_SCHEMA,
        "package_version": "0.3.0",
        "source_revision": source_manifest["source_revision"],
        "source_manifest": f"{V03_RELEASE_RELATIVE}/source_manifest.json",
        "source_manifest_sha256": _hash_bytes(_canonical_json(source_manifest).encode("utf-8")),
        "network_operations": [],
        "public_archive_created": False,
        "source_checkout": {"core.autocrlf": "false"},
        "commands": [
            "python scripts/local_readiness_check.py",
            "python scripts/build_v03_private_review_bundle.py --output <PATH> "
            "--source-date-epoch <EPOCH> --source-revision <HEAD>",
        ],
    }


def build_v03_source_license_inventory(root: Path, *, source_revision: str) -> dict[str, Any]:
    dependency_names = []
    for raw in (root / "requirements-release.lock").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "==" in line:
            dependency_names.append(line.split("==", 1)[0])
    return {
        "schema_version": V03_SOURCE_LICENSE_INVENTORY_SCHEMA,
        "package_version": "0.3.0",
        "source_revision": _revision(source_revision),
        "project_license_status": "owner-decision-pending",
        "packages": [
            {"name": "sparkbrain-research", "license": "NOASSERTION"},
            *[{"name": name, "license": "NOASSERTION"} for name in dependency_names],
        ],
    }


def build_v03_release_metadata(source_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": V03_RELEASE_METADATA_SCHEMA,
        "package_version": "0.3.0",
        "source_revision": source_manifest["source_revision"],
        "source_manifest": f"{V03_RELEASE_RELATIVE}/source_manifest.json",
        "source_manifest_sha256": _hash_bytes(_canonical_json(source_manifest).encode("utf-8")),
        "distribution": "private-review-candidate",
        "public_release_blocked": True,
        "blocker": "project license has not been selected by the repository owner",
    }


def build_v03_sbom(root: Path, *, source_revision: str) -> dict[str, Any]:
    packages = []
    for raw in (root / "requirements-release.lock").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "==" not in line:
            continue
        name, version = line.split("==", 1)
        packages.append(
            {
                "SPDXID": f"SPDXRef-Package-{re.sub(r'[^A-Za-z0-9.-]', '-', name)}",
                "name": name,
                "versionInfo": version,
                "downloadLocation": "NOASSERTION",
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
            }
        )
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "sparkbrain-research-v0.3.0-release-candidate",
        "documentNamespace": f"urn:sparkbrain:v03:sbom:{_revision(source_revision)}",
        "creationInfo": {"creators": ["Tool: scripts/generate_v03_release_artifacts.py"]},
        "packages": [
            {
                "SPDXID": "SPDXRef-Package-SparkBrain",
                "name": "sparkbrain-research",
                "versionInfo": "0.3.0",
                "downloadLocation": "NOASSERTION",
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "comment": "Project license is intentionally owner-blocked.",
            },
            *packages,
        ],
    }


def build_v03_source_manifest(
    root: Path, *, source_revision: str, generated_files: Iterable[Path]
) -> dict[str, Any]:
    relative_files = sorted(path.relative_to(root).as_posix() for path in generated_files)
    return {
        "schema_version": V03_SOURCE_MANIFEST_SCHEMA,
        "package_version": "0.3.0",
        "source_revision": _revision(source_revision),
        "files": [
            {"path": relative, "sha256": sha256_file(root / relative)}
            for relative in relative_files
        ],
    }


def build_v03_root_manifest(
    root: Path,
    *,
    source_revision: str,
    generated_at: str,
    paths: Iterable[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build final root-manifest payloads without writing self-referential files."""

    manifest = build_release_manifest(
        root,
        source_revision=_revision(source_revision),
        generated_at=generated_at,
        paths=paths,
    )
    manifest_path = root / "PACKAGE_MANIFEST.json"
    if manifest_path.exists():
        raise ValueError("v0.3 root manifest generation requires a staged output root")
    manifest_path.write_text(_canonical_json(manifest), encoding="utf-8", newline="\n")
    try:
        metadata = build_release_metadata(root, manifest_path)
    finally:
        manifest_path.unlink()
    return manifest, metadata


def generate_v03_release_artifacts(
    root: Path,
    *,
    output_root: Path,
    source_revision: str,
) -> dict[str, str]:
    """Generate v0.3 release evidence into a clean staging root."""

    release_dir = output_root / V03_RELEASE_RELATIVE
    release_dir.mkdir(parents=True, exist_ok=False)
    evidence = build_v03_evidence_map(
        root,
        source_revision=source_revision,
    )
    evidence_path = release_dir / "evidence_map.json"
    table_path = release_dir / "release_report.md"
    figure_path = release_dir / "release_figure.svg"
    boundary_figure_path = release_dir / "claim_boundary_figure.svg"
    sbom_path = release_dir / "sbom.spdx.json"
    primary_subset_path = release_dir / "primary_subset.json"
    license_inventory_path = release_dir / "source_license_inventory.json"
    evidence_path.write_text(_canonical_json(evidence), encoding="utf-8", newline="\n")
    table_path.write_text(_render_results_table(evidence), encoding="utf-8", newline="\n")
    figure_path.write_text(_render_results_figure(evidence), encoding="utf-8", newline="\n")
    boundary_figure_path.write_text(
        _render_claim_boundary_figure(evidence), encoding="utf-8", newline="\n"
    )
    sbom_path.write_text(
        _canonical_json(build_v03_sbom(root, source_revision=source_revision)),
        encoding="utf-8",
        newline="\n",
    )
    primary_subset_path.write_text(
        _canonical_json(build_v03_primary_subset(evidence)), encoding="utf-8", newline="\n"
    )
    license_inventory_path.write_text(
        _canonical_json(build_v03_source_license_inventory(root, source_revision=source_revision)),
        encoding="utf-8",
        newline="\n",
    )
    source_manifest = build_v03_source_manifest(
        output_root,
        source_revision=source_revision,
        generated_files=(
            evidence_path,
            table_path,
            figure_path,
            boundary_figure_path,
            sbom_path,
            primary_subset_path,
            license_inventory_path,
        ),
    )
    source_manifest_path = release_dir / "source_manifest.json"
    source_manifest_path.write_text(
        _canonical_json(source_manifest), encoding="utf-8", newline="\n"
    )
    reproduction_manifest_path = release_dir / "reproduction_manifest.json"
    reproduction_manifest_path.write_text(
        _canonical_json(build_v03_reproduction_manifest(source_manifest)),
        encoding="utf-8",
        newline="\n",
    )
    release_metadata_path = release_dir / "release_metadata.json"
    release_metadata_path.write_text(
        _canonical_json(build_v03_release_metadata(source_manifest)),
        encoding="utf-8",
        newline="\n",
    )
    return {
        path.relative_to(output_root).as_posix(): sha256_file(path)
        for path in (
            evidence_path,
            table_path,
            figure_path,
            boundary_figure_path,
            sbom_path,
            primary_subset_path,
            license_inventory_path,
            source_manifest_path,
            reproduction_manifest_path,
            release_metadata_path,
        )
    }
