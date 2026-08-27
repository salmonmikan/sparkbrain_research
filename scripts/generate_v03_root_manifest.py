from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import (  # noqa: E402
    validate_v03_generated_release_evidence,
    write_release_manifest,
    write_release_metadata,
)
from sparkbrain.release_v03_artifacts import (  # noqa: E402
    V03_RELEASE_RELATIVE,
    build_v03_root_manifest,
)

V03_GENERATED_ARTIFACTS = {
    f"{V03_RELEASE_RELATIVE}/{name}"
    for name in (
        "evidence_map.json",
        "release_report.md",
        "release_figure.svg",
        "claim_boundary_figure.svg",
        "sbom.spdx.json",
        "source_license_inventory.json",
        "primary_subset.json",
        "source_manifest.json",
        "reproduction_manifest.json",
        "release_metadata.json",
    )
}


def _tracked_paths() -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
    return [path for path in result.stdout.decode("utf-8").split("\0") if path]


def _require_artifact_integration(source_revision: str) -> None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=False, capture_output=True
    )
    if result.returncode:
        raise ValueError("v0.3 root manifest requires a readable Git HEAD")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_revision, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if ancestor.returncode:
        raise ValueError("v0.3 root manifest source_revision must be an ancestor of Git HEAD")
    for command in (("git", "diff", "--quiet"), ("git", "diff", "--cached", "--quiet")):
        state = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
        if state.returncode not in {0, 1}:
            raise ValueError("v0.3 root manifest could not inspect tracked source state")
        if state.returncode:
            raise ValueError("v0.3 root manifest requires a clean tracked source tree")
    tracked = set(_tracked_paths())
    missing = sorted(V03_GENERATED_ARTIFACTS - tracked)
    if missing:
        raise ValueError(
            "v0.3 root manifest requires tracked generated artifacts: " + ", ".join(missing)
        )
    problems = validate_v03_generated_release_evidence(ROOT)
    if problems:
        raise ValueError(
            "v0.3 root manifest generated artifacts are invalid: " + "; ".join(problems)
        )


def _restore(path: Path, original: bytes | None) -> None:
    if original is None:
        path.unlink(missing_ok=True)
        return
    with tempfile.NamedTemporaryFile(
        prefix=".v03-restore-", dir=path.parent, delete=False
    ) as handle:
        staged = Path(handle.name)
        handle.write(original)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def _publish_manifest_group(
    manifest_staged: Path,
    manifest_output: Path,
    metadata_staged: Path,
    metadata_output: Path,
) -> None:
    """Publish both root bindings or restore their pre-generation byte pair."""

    originals = {
        manifest_output: manifest_output.read_bytes() if manifest_output.exists() else None,
        metadata_output: metadata_output.read_bytes() if metadata_output.exists() else None,
    }
    try:
        os.replace(manifest_staged, manifest_output)
        os.replace(metadata_staged, metadata_output)
    except OSError as exc:
        try:
            _restore(manifest_output, originals[manifest_output])
            _restore(metadata_output, originals[metadata_output])
        except OSError as restore_exc:
            raise RuntimeError("v0.3 root manifest group restore failed") from restore_exc
        raise RuntimeError("v0.3 root manifest group publish failed and was restored") from exc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write final v0.3 root release manifest and metadata"
    )
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "PACKAGE_MANIFEST.json")
    parser.add_argument("--metadata-output", type=Path, default=ROOT / "RELEASE_METADATA.json")
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="replace the historical root manifests only after final C20 source is fixed",
    )
    args = parser.parse_args()
    try:
        _require_artifact_integration(args.source_revision)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if (args.output.exists() or args.metadata_output.exists()) and not args.replace_existing:
        raise SystemExit("existing root manifests require --replace-existing")
    staging = Path(tempfile.mkdtemp(prefix=".v03-root-manifest-stage-", dir=args.output.parent))
    try:
        for path in _tracked_paths():
            if path in {"PACKAGE_MANIFEST.json", "RELEASE_METADATA.json"}:
                continue
            source = ROOT / path
            target = staging / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        manifest, metadata = build_v03_root_manifest(
            staging,
            source_revision=args.source_revision,
            generated_at=args.generated_at,
            paths=_tracked_paths(),
        )
        with tempfile.NamedTemporaryFile(
            prefix=".v03-package-manifest-", dir=args.output.parent, delete=False
        ) as temporary:
            manifest_output = Path(temporary.name)
        with tempfile.NamedTemporaryFile(
            prefix=".v03-release-metadata-", dir=args.metadata_output.parent, delete=False
        ) as temporary:
            metadata_output = Path(temporary.name)
        try:
            write_release_manifest(manifest_output, manifest)
            write_release_metadata(metadata_output, metadata)
            _publish_manifest_group(
                manifest_output,
                args.output,
                metadata_output,
                args.metadata_output,
            )
        finally:
            manifest_output.unlink(missing_ok=True)
            metadata_output.unlink(missing_ok=True)
    finally:
        for path in sorted(staging.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        staging.rmdir()
    print(json.dumps({"manifest": str(args.output), "metadata": str(args.metadata_output)}))
