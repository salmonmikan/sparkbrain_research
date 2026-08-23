from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import (  # noqa: E402
    RELEASE_METADATA_PATH,
    build_release_manifest,
    build_release_metadata,
    write_release_manifest,
    write_release_metadata,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the deterministic release file manifest")
    parser.add_argument("--output", type=Path, default=ROOT / "PACKAGE_MANIFEST.json")
    parser.add_argument("--metadata-output", type=Path, default=ROOT / RELEASE_METADATA_PATH)
    parser.add_argument("--generated-at")
    parser.add_argument("--source-revision")
    args = parser.parse_args()

    revision = args.source_revision or subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    generated_at = args.generated_at or datetime.now(UTC).isoformat()
    manifest = build_release_manifest(
        ROOT,
        generated_at=generated_at,
        source_revision=revision,
    )
    write_release_manifest(args.output, manifest)
    metadata = build_release_metadata(ROOT, args.output)
    write_release_metadata(args.metadata_output, metadata)
    print(
        f"wrote {args.output} with {manifest['file_count']} files and "
        f"{args.metadata_output}"
    )


if __name__ == "__main__":
    main()
