from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / (
    "artifacts/v03/c19_external_validation/v2/official_v2/package_contract.json"
)
ADMISSION = ROOT / (
    "artifacts/v03/c19_external_validation/v2/official_v2/admission_binding.json"
)
V03 = ROOT / "src/sparkbrain/v03_external_validation"


def _blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_official_v2_package_binds_exact_current_execution_surface() -> None:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))

    assert package["status"] == (
        "prestart_complete_waiting_exact_head_ci_and_fresh_reconciliation"
    )
    assert package["admission_binding_blob"] == _blob(ADMISSION)
    assert package["evidence_analyst_authority"] == admission[
        "evidence_analyst_authority"
    ]
    assert package["planned_official_identity"] == admission[
        "planned_official_identity"
    ]

    v2_paths = {
        "official_protocol_v2.py": V03 / "official_protocol_v2.py",
        "official_execution_v2.py": V03 / "official_execution_v2.py",
        "official_io_v2.py": V03 / "official_io_v2.py",
        "official_scoring_v2.py": V03 / "official_scoring_v2.py",
        "run_c19_official_v2.py": ROOT / "scripts/run_c19_official_v2.py",
        "c19-official-v2-one-way.yml": (
            ROOT / ".github/workflows/c19-official-v2-one-way.yml"
        ),
        "test_c19_official_v2_scoring.py": (
            ROOT / "tests/test_c19_official_v2_scoring.py"
        ),
    }
    for name, path in v2_paths.items():
        assert package["v2_source_blobs"][name] == _blob(path)

    bound_paths = [
        (
            "belief_r_parser",
            ROOT / "src/sparkbrain/external_validation/belief_r.py",
        ),
        ("episode_envelope", ROOT / "src/sparkbrain/tasks/schema.py"),
        ("truth_free_input_adapter", V03 / "truth_free_adapter.py"),
        ("condition_and_baseline_binding", V03 / "implementation_binding.py"),
        ("target_blind_io_bridge", V03 / "official_io_v2.py"),
        ("v2_raw_writer_and_reconstructor", V03 / "official_execution_v2.py"),
    ]
    source_binding = admission["source_parser_envelope_input_binding"]
    for key, path in bound_paths:
        assert source_binding[key]["git_blob_sha1"] == _blob(path)

    runtime = admission["runtime_binding"]
    assert runtime["two_phase_runner"]["git_blob_sha1"] == _blob(
        ROOT / "scripts/run_c19_official_v2.py"
    )
    assert runtime["one_way_workflow"]["git_blob_sha1"] == _blob(
        ROOT / ".github/workflows/c19-official-v2-one-way.yml"
    )

    source_spec = admission["source_parser_envelope_input_binding"][
        "belief_r_source_spec"
    ]
    assert source_spec["git_blob_sha1"] == _blob(
        ROOT / "configs/external_validation/belief_r.json"
    )
    assert source_spec["expected_pairs"] == 1744
    assert source_spec["expected_update_pairs"] == 1074
    assert source_binding["target_blind_io_bridge"]["final_source_index"] == 1
    assert source_binding["target_blind_io_bridge"]["final_step_index"] == 1

    preservation = admission["immutable_raw_preservation_binding"]
    assert preservation["expected_raw_record_count"] == 55 * 1744
    assert preservation["force_update_forbidden"] is True
    assert preservation["same_identity_retry_after_started"] is False
