from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
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
    frozen = json.loads(
        (root / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    for relative in PRIMARY_INPUTS:
        actual = sha256_file(root / relative)
        expected = frozen["inputs"].get(relative)
        if actual != expected:
            raise ValueError(f"primary input hash mismatch: {relative}")
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
    release_dir = output / "artifacts/release"
    release_dir.mkdir(parents=True, exist_ok=True)
    table = release_dir / "primary_results.md"
    figure = release_dir / "primary_results.svg"
    table.write_text(render_primary_table(rows), encoding="utf-8", newline="\n")
    figure.write_text(render_primary_figure(rows), encoding="utf-8", newline="\n")
    outputs = {
        "artifacts/release/primary_results.md": sha256_file(table),
        "artifacts/release/primary_results.svg": sha256_file(figure),
    }
    if outputs != frozen["outputs"]:
        raise ValueError(f"primary output hash mismatch: {outputs!r}")
    manifest: dict[str, object] = {
        "schema_version": "c10-clean-room-run-v1",
        "source_revision": source_revision(root),
        "command": "python scripts/reproduce_release.py --offline --output <PATH>",
        "offline_mode": offline,
        "network_operations": [],
        "python": platform.python_version(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "inputs": frozen["inputs"],
        "outputs": outputs,
        "primary_subset_is_full_evaluation": False,
        "readiness_stdout": readiness.stdout.splitlines(),
        "duration_seconds": round(time.perf_counter() - start, 6),
        "status": "pass",
    }
    (output / "run_manifest.json").write_text(
        _canonical_json(manifest), encoding="utf-8", newline="\n"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the frozen CPU release smoke subset")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--offline", action="store_true", default=False)
    args = parser.parse_args()
    if not args.offline:
        raise SystemExit("release reproduction requires the explicit --offline acknowledgement")
    result = reproduce(ROOT, args.output.resolve(), offline=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
