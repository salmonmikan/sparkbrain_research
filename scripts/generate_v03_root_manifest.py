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

from sparkbrain.release import write_release_manifest, write_release_metadata  # noqa: E402
from sparkbrain.release_v03_artifacts import build_v03_root_manifest  # noqa: E402


def _tracked_paths() -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
    return [path for path in result.stdout.decode("utf-8").split("\0") if path]


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
            os.replace(manifest_output, args.output)
            os.replace(metadata_output, args.metadata_output)
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
