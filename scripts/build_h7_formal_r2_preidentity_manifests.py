from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.learned.h7_formal_r2_runner import (
    build_package_manifest,
    build_runtime_manifest,
    configure_runtime,
    preidentity_preflight,
)


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    configure_runtime()
    preflight = preidentity_preflight(root)
    runtime = build_runtime_manifest()
    package = build_package_manifest(root)
    _write(args.output_dir / "preidentity.json", preflight)
    _write(args.output_dir / "runtime_manifest.json", runtime)
    _write(args.output_dir / "package_manifest.json", package)
    print(
        json.dumps(
            {
                "status": "H7_FORMAL_R2_PREIDENTITY_MANIFESTS_MATERIALIZED",
                "runtime_manifest_sha256": runtime["manifest_sha256"],
                "package_manifest_sha256": package["manifest_sha256"],
                "scientific_result": None,
                "formal_identity": None,
                "protected_evaluation_access": False,
                "scoring_performed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
