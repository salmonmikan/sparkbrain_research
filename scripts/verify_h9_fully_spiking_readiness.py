from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "artifacts" / "spiking" / "h9_fully_spiking_readiness"
READINESS = PACKAGE / "readiness.json"

EXPECTED_STATUS = "PRE_START_UNDERSPECIFIED"
EXPECTED_SCHEMA = "h9-fully-spiking-readiness-v1"
REQUIRED_GAPS = {
    "FULLY_SPIKING_OPERATIONAL_BOUNDARY",
    "NON_SENSORY_NEURON_AND_SYNAPSE_MODEL",
    "REPRESENTATION_AND_DECODER_MAPPING",
    "PARAMETER_AND_TUNING_BUDGET",
    "PRIMARY_COMPARATOR_AND_CLAIM",
    "SUCCESSOR_TOLERANCE_AUTHORITY",
    "TRAINING_OR_PLASTICITY_REGIME",
    "EXACT_RUNTIME_AND_RANDOMNESS",
}


def fail(message: str) -> None:
    raise SystemExit(f"H9 READINESS FAILED: {message}")


def git_blob_sha(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", "--", path],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"cannot hash source binding {path}: {result.stderr.strip()}")
    return result.stdout.strip()


def require_marker(path: str, marker: str) -> None:
    content = (ROOT / path).read_text(encoding="utf-8")
    if marker not in content:
        fail(f"{path} lost required marker: {marker!r}")


def main() -> None:
    value = json.loads(READINESS.read_text(encoding="utf-8"))

    if value.get("schema") != EXPECTED_SCHEMA:
        fail("unexpected readiness schema")
    if value.get("status") != EXPECTED_STATUS:
        fail("readiness package must remain PRE_START_UNDERSPECIFIED")
    if value.get("execution_allowed") is not False:
        fail("execution must remain disabled")
    if value.get("completion", {}).get("scientific_execution_performed") is not False:
        fail("readiness package cannot claim scientific execution")
    if value.get("completion", {}).get("identity_consumed") is not False:
        fail("readiness package cannot consume an identity")
    if value.get("hypothesis", {}).get("fresh_successor_identity") is not None:
        fail("fresh successor identity must remain unset while science is underspecified")

    bindings = value.get("source_bindings")
    if not isinstance(bindings, dict) or not bindings:
        fail("source_bindings missing")
    for path, expected in bindings.items():
        actual = git_blob_sha(path)
        if actual != expected:
            fail(f"source binding drift for {path}: expected {expected}, got {actual}")

    gaps = value.get("missing_scientific_choices")
    if not isinstance(gaps, list):
        fail("missing_scientific_choices must be a list")
    observed = {item.get("id") for item in gaps if isinstance(item, dict)}
    if observed != REQUIRED_GAPS:
        fail(f"unexpected scientific-gap inventory: {sorted(observed)}")

    boundary = value.get("existing_boundary_inventory", {})
    if boundary.get("fully_spiking_backend_present") is not False:
        fail("package must not claim a fully-spiking backend exists")
    for component in (
        "signed_evidence_graph",
        "hypothesis_state",
        "coalition_scoring",
        "ignition",
        "broadcast",
        "workspace",
    ):
        if boundary.get(component) != "RATE_ALGORITHMIC":
            fail(f"historical hybrid boundary drift for {component}")

    require_marker(
        "docs/HYPOTHESES_AND_FALSIFICATION.md",
        "### H9 — A spiking substrate can preserve theory-level behavior",
    )
    require_marker(
        "docs/codex/C07_SPIKING_BACKEND.md",
        "hybrid vs fully spiking boundary comparison",
    )
    require_marker(
        "src/sparkbrain/spiking.py",
        "not a fully spiking cognitive architecture",
    )
    require_marker(
        "src/sparkbrain/spiking.py",
        "self.engine = build_reference_brain(config)",
    )
    require_marker(
        "artifacts/spiking/c07_report.md",
        "It is not fully spiking.",
    )

    print(
        "H9 readiness verified: PRE_START_UNDERSPECIFIED; "
        f"{len(bindings)} source bindings; {len(REQUIRED_GAPS)} unresolved choices"
    )


if __name__ == "__main__":
    main()
