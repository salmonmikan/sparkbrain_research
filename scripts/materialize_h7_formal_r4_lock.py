from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from email.parser import Parser
from pathlib import Path

EXPECTED_PYTHON = "3.11.16"
EXPECTED_IMAGE_OS = "ubuntu24"
EXPECTED_IMAGE_VERSION = "20260907.300.1"
EXPECTED_PLATFORM_RELEASE = "6.17.0-1022-azure"
EXPECTED_MACHINE = "x86_64"
EXPECTED_RUNNER_ARCH = "X64"
_FORBIDDEN = {"pytest", "ruff", "jsonschema", "fastapi", "uvicorn", "httpx"}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalize_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def read_specs(path: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.count("==") != 1:
            raise SystemExit(f"non-exact requirement forbidden: {line}")
        name, version = line.split("==", 1)
        key = normalize_name(name)
        if key in result:
            raise SystemExit(f"duplicate package: {name}")
        if key in _FORBIDDEN:
            raise SystemExit(f"development tooling forbidden from scientific runtime: {name}")
        result[key] = (name, version)
    if not result:
        raise SystemExit("scientific runtime package set is empty")
    return result


def wheel_metadata(
    path: Path, specs: dict[str, tuple[str, str]]
) -> tuple[str, str]:
    matches: list[tuple[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        candidates = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        for candidate in candidates:
            metadata = Parser().parsestr(archive.read(candidate).decode("utf-8"))
            name = metadata.get("Name")
            version = metadata.get("Version")
            if not name or not version:
                continue
            key = normalize_name(name)
            expected = specs.get(key)
            if expected is not None and version == expected[1]:
                matches.append((name, version))
    if len(matches) != 1:
        raise SystemExit(
            f"wheel has ambiguous selected-package METADATA: {path.name}; matches={matches!r}"
        )
    return matches[0]


def assert_runtime_host() -> None:
    observed = {
        "python": platform.python_version(),
        "image_os": os.environ.get("ImageOS", ""),
        "image_version": os.environ.get("ImageVersion", ""),
        "platform_release": platform.release(),
        "machine": platform.machine(),
        "runner_arch": os.environ.get("RUNNER_ARCH", ""),
    }
    expected = {
        "python": EXPECTED_PYTHON,
        "image_os": EXPECTED_IMAGE_OS,
        "image_version": EXPECTED_IMAGE_VERSION,
        "platform_release": EXPECTED_PLATFORM_RELEASE,
        "machine": EXPECTED_MACHINE,
        "runner_arch": EXPECTED_RUNNER_ARCH,
    }
    if observed != expected:
        raise SystemExit(f"R4 lock materialization host drift: observed={observed!r} expected={expected!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--versions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    assert_runtime_host()
    specs = read_specs(args.versions)
    versions_bytes = args.versions.read_bytes()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="h7-r4-wheelhouse-") as temp_dir:
        wheelhouse = Path(temp_dir)
        command = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--disable-pip-version-check",
            "--no-deps",
            "--only-binary=:all:",
            "--dest",
            str(wheelhouse),
            "--requirement",
            str(args.versions),
        ]
        subprocess.run(command, check=True)
        wheels = sorted(wheelhouse.glob("*.whl"))
        if len(wheels) != len(specs):
            raise SystemExit(
                f"wheel count mismatch: downloaded={len(wheels)} expected={len(specs)}"
            )

        records: list[dict[str, str | int]] = []
        seen: set[str] = set()
        lock_lines: list[tuple[str, str]] = []
        for wheel in wheels:
            name, version = wheel_metadata(wheel, specs)
            key = normalize_name(name)
            expected_name, expected_version = specs[key]
            if version != expected_version:
                raise SystemExit(
                    f"version drift for {name}: downloaded={version} expected={expected_version}"
                )
            if key in seen:
                raise SystemExit(f"multiple wheel artifacts selected for {name}")
            seen.add(key)
            digest = sha256_bytes(wheel.read_bytes())
            records.append(
                {
                    "normalized_name": key,
                    "declared_name": expected_name,
                    "metadata_name": name,
                    "version": version,
                    "wheel_filename": wheel.name,
                    "wheel_sha256": digest,
                    "wheel_size_bytes": wheel.stat().st_size,
                }
            )
            lock_lines.append((key, f"{name}=={version} --hash=sha256:{digest}"))

        missing = sorted(set(specs) - seen)
        if missing:
            raise SystemExit("missing wheels: " + ", ".join(missing))

    lock_text = "# H7 FORMAL-R4 exact scientific runtime wheel lock\n" + "\n".join(
        line for _, line in sorted(lock_lines)
    ) + "\n"
    lock_bytes = lock_text.encode("utf-8")
    lock_path = args.output_dir / "scientific-runtime.lock"
    manifest_path = args.output_dir / "scientific-runtime-manifest.json"
    lock_path.write_bytes(lock_bytes)

    manifest = {
        "schema_version": 2,
        "kind": "H7_FORMAL_R4_SCIENTIFIC_RUNTIME_WHEEL_LOCK_MANIFEST_V1",
        "authority_generation": "EVA-20260923T001221+0900-R81-4885D9DE",
        "development_revision": "H7-FORMAL-R4-REPRODUCIBLE-RUNTIME-PACKAGE-LOCK-AND-PREIDENTITY-REVALIDATION",
        "materialization_policy": {
            "exact_versions_selected_before_materialization": True,
            "single_prospectively_fixed_package_set": True,
            "dependency_resolution": False,
            "binary_wheels_only": True,
            "development_tooling_excluded": sorted(_FORBIDDEN),
            "editable_project_install": False,
        },
        "host_binding": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "runner_image_os": os.environ.get("ImageOS", ""),
            "runner_image_version": os.environ.get("ImageVersion", ""),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "platform_machine": platform.machine(),
            "runner_arch": os.environ.get("RUNNER_ARCH", ""),
        },
        "versions_file_sha256": sha256_bytes(versions_bytes),
        "lock_sha256": sha256_bytes(lock_bytes),
        "package_count": len(records),
        "packages": sorted(records, key=lambda item: str(item["normalized_name"])),
        "evidentiary_status": "NON_EVIDENTIARY_FORMAL_PREIDENTITY_RESOURCE_LOCK_MATERIALIZATION",
        "one_way_actions_performed": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    shutil.rmtree(args.output_dir / "wheelhouse", ignore_errors=True)
    print(json.dumps({"lock_sha256": manifest["lock_sha256"], "package_count": len(records)}))


if __name__ == "__main__":
    main()
