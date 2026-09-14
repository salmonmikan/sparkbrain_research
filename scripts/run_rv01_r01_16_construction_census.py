from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.research.rv01_r01_16_construction_census import run_construction_census
from sparkbrain.research.rv01_r01_16_development_package import (
    R0116SourceManifest,
    R0116SourceManifestEntry,
)


def _load_manifest(path: Path) -> R0116SourceManifest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("R01-16 source manifest input must be an object")
    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, list):
        raise ValueError("R01-16 source manifest entries must be a list")
    manifest = R0116SourceManifest(
        source_git_sha=str(payload.get("source_git_sha", "")),
        entries=tuple(
            R0116SourceManifestEntry(path=str(row["path"]), sha256=str(row["sha256"]))
            for row in raw_entries
            if isinstance(row, dict)
        ),
    )
    if len(manifest.entries) != len(raw_entries):
        raise ValueError("R01-16 source manifest entries must all be objects")
    manifest.validate()
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the one-shot R01-16 construction census")
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    output_dir = run_construction_census(
        repo_root=args.repo_root,
        source_manifest=_load_manifest(args.source_manifest),
    )
    complete = json.loads((output_dir / "COMPLETE.json").read_text(encoding="utf-8"))
    print(json.dumps({"output_dir": str(output_dir), "complete": complete}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
