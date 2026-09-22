from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
from pathlib import Path

import sparkbrain
import torch

from sparkbrain.learned.h7_formal_r3_executor import (
    synthetic_nonprotected_realization_probe,
)


ROOT = Path("artifacts/formal_h7_r5")
R4_ROOT = Path("artifacts/formal_h7_r4")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "hash-object", path], text=True
    ).strip()


def main() -> None:
    contract = json.loads((ROOT / "resource_contract.json").read_text())
    scientific = contract["scientific_runtime_identity"]
    provenance = contract["provisioning_provenance"]

    if contract["authority_generation"] != "EVA-20260923T065834+0900-R88-D5A7C219":
        raise SystemExit("R5 Analyst authority drift")
    if contract["development_revision"] != (
        "H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-"
        "PROVISIONING-PROVENANCE-SPLIT"
    ):
        raise SystemExit("R5 development revision drift")
    if not all(value is False for value in contract["one_way_hard_stop"].values()):
        raise SystemExit("R5 one-way hard-stop state drift")

    expected_files = {
        R4_ROOT / "scientific-runtime.lock": scientific["package_lock"]["sha256"],
        R4_ROOT / "scientific-runtime-manifest.json": scientific["package_manifest"][
            "sha256"
        ],
        R4_ROOT / "scientific-runtime.versions": scientific["package_versions"][
            "sha256"
        ],
    }
    for path, expected in expected_files.items():
        observed = _sha256(path)
        if observed != expected:
            raise SystemExit(f"R5 inherited content-addressed runtime drift: {path} {observed}")

    manifest = json.loads((R4_ROOT / "scientific-runtime-manifest.json").read_text())
    if manifest["package_count"] != scientific["package_manifest"]["package_count"]:
        raise SystemExit("R5 package-count drift")

    if platform.python_version() != scientific["python_version"]:
        raise SystemExit("R5 Python version drift")
    if platform.python_implementation() != scientific["python_implementation"]:
        raise SystemExit("R5 Python implementation drift")
    if platform.machine() != scientific["platform_machine"]:
        raise SystemExit("R5 machine architecture drift")
    if os.environ.get("RUNNER_ARCH", "") != scientific["runner_arch"]:
        raise SystemExit("R5 runner architecture drift")

    installed = {
        _normalise(dist.metadata["Name"]): dist.version
        for dist in importlib.metadata.distributions()
        if dist.metadata.get("Name")
    }
    expected_packages = {
        item["normalized_name"]: item["version"] for item in manifest["packages"]
    }
    for name, version in expected_packages.items():
        if installed.get(name) != version:
            raise SystemExit(
                f"R5 installed package drift: {name} {installed.get(name)!r} != {version!r}"
            )

    forbidden = {
        _normalise(name)
        for name in manifest["materialization_policy"]["development_tooling_excluded"]
    }
    if forbidden & set(installed):
        raise SystemExit(f"R5 protected runtime contains dev tooling: {forbidden & set(installed)}")

    if importlib.metadata.version("torch") != scientific["torch_distribution_version"]:
        raise SystemExit("R5 torch distribution version drift")
    if str(torch.__version__) != scientific["torch_module_version"]:
        raise SystemExit("R5 torch module version drift")
    if str(torch.version.git_version) != scientific["torch_git_version"]:
        raise SystemExit("R5 torch git version drift")
    if str(torch.version.cuda) != scientific["torch_cuda_build_version"]:
        raise SystemExit("R5 torch CUDA build version drift")

    torch.set_num_threads(scientific["torch_num_threads"])
    torch.use_deterministic_algorithms(scientific["torch_deterministic_algorithms"])
    if torch.get_num_threads() != 1:
        raise SystemExit("R5 torch thread contract drift")
    if not torch.are_deterministic_algorithms_enabled():
        raise SystemExit("R5 torch deterministic-algorithm contract drift")
    if torch.tensor([1.0]).device.type != scientific["device_contract"]:
        raise SystemExit("R5 CPU device contract drift")

    source = Path(sparkbrain.__file__).resolve()
    checkout = Path(os.environ["GITHUB_WORKSPACE"]).resolve()
    if not source.is_relative_to(checkout / "src") or "site-packages" in str(source):
        raise SystemExit(f"R5 exact-checkout source loading drift: {source}")
    executor_path = "src/sparkbrain/learned/h7_formal_r3_executor.py"
    if _git_blob(executor_path) != contract["source_and_component_binding"][
        "scientific_executor_blob"
    ]:
        raise SystemExit("R5 scientific executor blob drift")

    record = importlib.metadata.distribution("torch").read_text("RECORD")
    if record is None:
        raise SystemExit("R5 torch RECORD provenance unavailable")
    observed_record_sha256 = hashlib.sha256(record.encode()).hexdigest()

    result = synthetic_nonprotected_realization_probe()
    expected_probe = {
        "protected_evaluation_accessed": False,
        "scoring_performed": False,
        "scientific_result": None,
    }
    observed_probe = {key: result.get(key) for key in expected_probe}
    if observed_probe != expected_probe:
        raise SystemExit(f"R5 preidentity hard-stop drift: {observed_probe!r}")

    output = {
        "evidentiary_status": "NON_RESULT_PREIDENTITY_DIAGNOSTIC",
        "scientific_runtime_identity": {
            "lock_sha256": scientific["package_lock"]["sha256"],
            "manifest_sha256": scientific["package_manifest"]["sha256"],
            "versions_sha256": scientific["package_versions"]["sha256"],
            "python_version": platform.python_version(),
            "torch_distribution_version": importlib.metadata.version("torch"),
            "torch_module_version": str(torch.__version__),
            "torch_git_version": str(torch.version.git_version),
            "torch_cuda_build_version": str(torch.version.cuda),
            "executor_blob": _git_blob(executor_path),
        },
        "provisioning_provenance": {
            "classification": provenance["classification"],
            "runner_image_os": os.environ.get("ImageOS", ""),
            "runner_image_version": os.environ.get("ImageVersion", ""),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "torch_distribution_record_sha256": observed_record_sha256,
        },
        "synthetic_probe": observed_probe,
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
