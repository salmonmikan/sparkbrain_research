from __future__ import annotations

import argparse
import json
import subprocess
import sys
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
    args = parser.parse_args()
    if args.output.exists() or args.metadata_output.exists():
        raise SystemExit("final v0.3 root manifest outputs must not already exist")
    staging = args.output.parent / ".v03-root-manifest-stage"
    staging.mkdir(exist_ok=False)
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
        write_release_manifest(args.output, manifest)
        write_release_metadata(args.metadata_output, metadata)
    finally:
        for path in sorted(staging.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        staging.rmdir()
    print(json.dumps({"manifest": str(args.output), "metadata": str(args.metadata_output)}))
