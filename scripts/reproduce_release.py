from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import _canonical_json, sha256_file  # noqa: E402
from sparkbrain.release_artifacts import (  # noqa: E402
    PRIMARY_INPUTS,
    primary_rows,
    render_primary_figure,
    render_primary_table,
    source_revision,
)


def reproduce(root: Path, output: Path, *, offline: bool = True) -> dict[str, object]:
    start = time.perf_counter()
    if output.is_symlink():
        raise ValueError(f"reproduction output must not be a symlink: {output}")
    if output.exists():
        if not output.is_dir():
            raise ValueError(f"reproduction output path already exists: {output}")
        if any(output.iterdir()):
            raise ValueError(f"reproduction output directory is not empty: {output}")
        raise ValueError(
            "reproduction output directory must not already exist; "
            "provide a new empty path so the result can be committed atomically"
        )

    frozen = json.loads(
        (root / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    if frozen.get("schema_version") != "c10-primary-subset-v1":
        raise ValueError("unsupported primary subset schema version")
    inputs = frozen.get("inputs")
    expected_outputs = frozen.get("outputs")
    if not isinstance(inputs, dict) or not isinstance(expected_outputs, dict):
        raise ValueError("primary subset inputs and outputs must be objects")

    for relative in PRIMARY_INPUTS:
        actual = sha256_file(root / relative)
        expected = inputs.get(relative)
        if actual != expected:
            raise ValueError(f"primary input hash mismatch: {relative}")

    revision = source_revision(root)
    readiness = subprocess.run(
        [sys.executable, "scripts/local_readiness_check.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "NO_PROXY": "*", "no_proxy": "*"},
    )
    if readiness.returncode:
        raise RuntimeError("local readiness failed: " + readiness.stdout + readiness.stderr)

    rows = primary_rows(root)
    rendered = {
        "artifacts/release/primary_results.md": render_primary_table(rows),
        "artifacts/release/primary_results.svg": render_primary_figure(rows),
    }
    outputs = {
        relative: hashlib.sha256(content.encode("utf-8")).hexdigest()
        for relative, content in rendered.items()
    }
    if outputs != expected_outputs:
        raise ValueError(f"primary output hash mismatch: {outputs!r}")

    manifest: dict[str, object] = {
        "schema_version": "c10-clean-room-run-v1",
        "source_revision": revision,
        "command": "python scripts/reproduce_release.py --offline --output <PATH>",
        "offline_mode": offline,
        "network_operations": [],
        "python": platform.python_version(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "inputs": inputs,
        "outputs": outputs,
        "primary_subset_is_full_evaluation": False,
        "readiness_stdout": readiness.stdout.splitlines(),
        "duration_seconds": round(time.perf_counter() - start, 6),
        "status": "pass",
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    try:
        for relative, content in rendered.items():
            destination = staging / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8", newline="\n")
        staged_outputs = {
            relative: sha256_file(staging / relative) for relative in rendered
        }
        if staged_outputs != outputs:
            raise RuntimeError(f"staged primary output hash mismatch: {staged_outputs!r}")
        (staging / "run_manifest.json").write_text(
            _canonical_json(manifest), encoding="utf-8", newline="\n"
        )
        if output.exists():
            raise FileExistsError(f"reproduction output appeared during generation: {output}")
        staging.rename(output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the frozen CPU release smoke subset")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--offline", action="store_true", default=False)
    args = parser.parse_args()
    if not args.offline:
        raise SystemExit("release reproduction requires the explicit --offline acknowledgement")
    try:
        result = reproduce(ROOT, args.output.resolve(), offline=True)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"release reproduction failed: {exc}") from None
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
