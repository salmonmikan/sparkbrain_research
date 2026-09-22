from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
from pathlib import Path

import torch

import sparkbrain
from sparkbrain.learned.h7_formal_r3_executor import (
    synthetic_nonprotected_realization_probe,
)


ROOT = Path("artifacts/formal_h7_r5")
R4_ROOT = Path("artifacts/formal_h7_r4")
AUTHORITY = "EVA-20260923T065834+0900-R88-D5A7C219"
REVISION = (
    "H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-"
    "PROVISIONING-PROVENANCE-SPLIT"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _git_blob(path: str) -> str:
    args = ["git", "hash-object", path]
    return subprocess.check_output(args, text=True).strip()


def _fail(label: str, observed: object, expected: object) -> None:
    raise SystemExit(f"{label}: {observed!r} != {expected!r}")


def main() -> None:
    contract_path = ROOT / "resource_contract.json"
    contract = json.loads(contract_path.read_text())
    scientific = contract["scientific_runtime_identity"]
    provenance = contract["provisioning_provenance"]

    if contract["authority_generation"] != AUTHORITY:
        _fail("R5 Analyst authority drift", contract["authority_generation"], AUTHORITY)
    if contract["development_revision"] != REVISION:
        _fail("R5 development revision drift", contract["development_revision"], REVISION)
    hard_stop = contract["one_way_hard_stop"]
    if not all(value is False for value in hard_stop.values()):
        raise SystemExit("R5 one-way hard-stop state drift")

    expected_files = [
        (
            R4_ROOT / "scientific-runtime.lock",
            scientific["package_lock"]["sha256"],
        ),
        (
            R4_ROOT / "scientific-runtime-manifest.json",
            scientific["package_manifest"]["sha256"],
        ),
        (
            R4_ROOT / "scientific-runtime.versions",
            scientific["package_versions"]["sha256"],
        ),
    ]
    for path, expected in expected_files:
        observed = _sha256(path)
        if observed != expected:
            _fail("R5 inherited content-addressed runtime drift", observed, expected)

    manifest_path = R4_ROOT / "scientific-runtime-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    package_manifest = scientific["package_manifest"]
    if manifest["package_count"] != package_manifest["package_count"]:
        _fail(
            "R5 package-count drift",
            manifest["package_count"],
            package_manifest["package_count"],
        )

    checks = [
        (
            "R5 Python version drift",
            platform.python_version(),
            scientific["python_version"],
        ),
        (
            "R5 Python implementation drift",
            platform.python_implementation(),
            scientific["python_implementation"],
        ),
        (
            "R5 machine architecture drift",
            platform.machine(),
            scientific["platform_machine"],
        ),
        (
            "R5 runner architecture drift",
            os.environ.get("RUNNER_ARCH", ""),
            scientific["runner_arch"],
        ),
    ]
    for label, observed, expected in checks:
        if observed != expected:
            _fail(label, observed, expected)

    installed = {
        _normalise(dist.metadata["Name"]): dist.version
        for dist in importlib.metadata.distributions()
        if dist.metadata.get("Name")
    }
    expected_packages = {
        item["normalized_name"]: item["version"]
        for item in manifest["packages"]
    }
    for name, version in expected_packages.items():
        observed = installed.get(name)
        if observed != version:
            _fail(f"R5 installed package drift: {name}", observed, version)

    forbidden = {
        _normalise(name)
        for name in manifest["materialization_policy"][
            "development_tooling_excluded"
        ]
    }
    present_forbidden = forbidden & set(installed)
    if present_forbidden:
        raise SystemExit(
            f"R5 protected runtime contains dev tooling: {present_forbidden}"
        )

    torch_checks = [
        (
            "R5 torch distribution version drift",
            importlib.metadata.version("torch"),
            scientific["torch_distribution_version"],
        ),
        (
            "R5 torch module version drift",
            str(torch.__version__),
            scientific["torch_module_version"],
        ),
        (
            "R5 torch git version drift",
            str(torch.version.git_version),
            scientific["torch_git_version"],
        ),
        (
            "R5 torch CUDA build version drift",
            str(torch.version.cuda),
            scientific["torch_cuda_build_version"],
        ),
    ]
    for label, observed, expected in torch_checks:
        if observed != expected:
            _fail(label, observed, expected)

    torch.set_num_threads(scientific["torch_num_threads"])
    deterministic = scientific["torch_deterministic_algorithms"]
    torch.use_deterministic_algorithms(deterministic)
    if torch.get_num_threads() != scientific["torch_num_threads"]:
        raise SystemExit("R5 torch thread contract drift")
    if torch.are_deterministic_algorithms_enabled() is not deterministic:
        raise SystemExit("R5 deterministic-algorithm contract drift")
    device_type = torch.tensor([1.0]).device.type
    if device_type != scientific["device_contract"]:
        _fail("R5 CPU device contract drift", device_type, scientific["device_contract"])

    source = Path(sparkbrain.__file__).resolve()
    checkout_source = Path(os.environ["GITHUB_WORKSPACE"]).resolve() / "src"
    if not source.is_relative_to(checkout_source):
        raise SystemExit(f"R5 source checkout drift: {source}")
    if "site-packages" in str(source):
        raise SystemExit(f"R5 source unexpectedly loaded from site-packages: {source}")

    executor_path = "src/sparkbrain/learned/h7_formal_r3_executor.py"
    observed_executor = _git_blob(executor_path)
    expected_executor = contract["source_and_component_binding"][
        "scientific_executor_blob"
    ]
    if observed_executor != expected_executor:
        _fail("R5 scientific executor blob drift", observed_executor, expected_executor)

    record = importlib.metadata.distribution("torch").read_text("RECORD")
    if record is None:
        raise SystemExit("R5 torch RECORD provenance unavailable")
    record_sha256 = hashlib.sha256(record.encode()).hexdigest()

    result = synthetic_nonprotected_realization_probe()
    expected_probe = {
        "protected_evaluation_accessed": False,
        "scoring_performed": False,
        "scientific_result": None,
    }
    observed_probe = {key: result.get(key) for key in expected_probe}
    if observed_probe != expected_probe:
        _fail("R5 preidentity hard-stop drift", observed_probe, expected_probe)

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
            "executor_blob": observed_executor,
        },
        "provisioning_provenance": {
            "classification": provenance["classification"],
            "runner_image_os": os.environ.get("ImageOS", ""),
            "runner_image_version": os.environ.get("ImageVersion", ""),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "torch_distribution_record_sha256": record_sha256,
        },
        "synthetic_probe": observed_probe,
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
