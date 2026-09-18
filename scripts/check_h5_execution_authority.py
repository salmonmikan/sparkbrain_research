#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/h5/formal_contract.json"
AUTHORITY_PATH = ROOT / "configs/experiments/h5/execution_authority.json"

EXPECTED_ANALYST = "f373fe3dfcddc14405d81cabadf0cb2682a659d0"
EXPECTED_MAILBOX = "4630decbda55d31ec8f44ac1435950b261225fd5"
EXPECTED_SCIENCE_HEAD = "520fc8391d9ebb02584a16ec466a1bf168548ea9"
EXPECTED_IDENTITY = "h5-event-routing-work-reduction-official-v1"
EXPECTED_PROTOCOL = "h5-event-routing-work-reduction-formal-contract-v2"
EXPECTED_CONTRACT_BLOB = "1911d4560f4e2774fd725df26ba8cb25b03e2c5f"
EXPECTED_H5_MODULE_BLOB = "572f00f7a7361a89a54b647a2e2dca875c9b4829"
EXPECTED_CHECKER_BLOB = "2ff3abb91d7214a9d4e8877ef1c6a992e78bdddd"
EXPECTED_RUNNER_BLOB = "42a44384d08d680e3767541efce92b0f54edb9ee"
EXPECTED_PRESERVER_BLOB = "0f3b013025737373e8bec91056c5369f23a3266f"
EXPECTED_WORKFLOW_BLOB = "37f8dc1817a4587749c0896727dc4f10187ff50e"
EXPECTED_CONTROL_REF = (
    "control/h5-event-routing-work-reduction-started-v1-20260918"
)
EXPECTED_PRESERVE_REF = (
    "preserve/h5-event-routing-work-reduction-raw-"
    "h5-event-routing-work-reduction-official-v1"
)
EXPECTED_EVIDENCE_TAG = (
    "evidence/h5-event-routing-work-reduction-"
    "h5-event-routing-work-reduction-official-v1"
)
EXPECTED_SOURCE_BLOBS = {
    "src/sparkbrain/engine.py": "48fa64414f539ec4a00acc9e25ffc9b1d26a4982",
    "src/sparkbrain/model.py": "ab450dba5943fa9184e66c00a4e992d6588bf6a5",
    "pyproject.toml": "49d47f3d65f67f1c0a6b82a3f7fc2d0364e2a88c",
    "src/sparkbrain/h5_work.py": EXPECTED_H5_MODULE_BLOB,
}


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return value


def _blob(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    contract = _read(CONTRACT_PATH)
    authority = _read(AUTHORITY_PATH)

    _require(
        authority["status"] == "PRE_START_AUTHORIZED_CONDITIONAL",
        "H5 authority status mismatch",
    )
    _require(
        authority["evidence_analyst_commit"] == EXPECTED_ANALYST,
        "H5 Analyst authority mismatch",
    )
    _require(
        authority["evidence_analyst_mailbox_tip"] == EXPECTED_MAILBOX,
        "H5 Analyst mailbox tip mismatch",
    )
    _require(
        authority["reviewed_scientific_head"] == EXPECTED_SCIENCE_HEAD,
        "H5 reviewed scientific head mismatch",
    )
    _require(
        authority["formal_identity"] == EXPECTED_IDENTITY,
        "H5 identity mismatch",
    )
    _require(
        authority["protocol_id"] == EXPECTED_PROTOCOL,
        "H5 protocol mismatch",
    )
    _require(
        authority["scientific_contract_immutable"] is True,
        "H5 scientific contract must remain immutable",
    )
    _require(authority["no_retry"] is True, "H5 no-retry invariant changed")
    _require(
        authority["formal_contract_git_blob"] == EXPECTED_CONTRACT_BLOB,
        "H5 formal contract authority mismatch",
    )
    _require(
        authority["h5_module_git_blob"] == EXPECTED_H5_MODULE_BLOB,
        "H5 module authority mismatch",
    )
    _require(
        authority["scientific_checker_git_blob"] == EXPECTED_CHECKER_BLOB,
        "H5 scientific checker authority mismatch",
    )
    _require(
        authority["official_runner_git_blob"] == EXPECTED_RUNNER_BLOB,
        "H5 official runner authority mismatch",
    )
    _require(
        authority["preserver_git_blob"] == EXPECTED_PRESERVER_BLOB,
        "H5 preserver authority mismatch",
    )
    _require(
        authority["one_way_workflow_git_blob"] == EXPECTED_WORKFLOW_BLOB,
        "H5 one-way workflow authority mismatch",
    )
    _require(
        authority["control_ref"] == EXPECTED_CONTROL_REF,
        "H5 control ref mismatch",
    )
    _require(
        authority["preserve_ref"] == EXPECTED_PRESERVE_REF,
        "H5 preserve ref mismatch",
    )
    _require(
        authority["evidence_tag"] == EXPECTED_EVIDENCE_TAG,
        "H5 evidence tag mismatch",
    )

    _require(
        contract["schema"] == EXPECTED_PROTOCOL,
        "H5 frozen protocol changed",
    )
    _require(
        contract["phase"]
        == "H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW",
        "H5 frozen scientific phase changed",
    )
    _require(
        contract["execution_authorized"] is False,
        "H5 scientific contract was rewritten for execution",
    )
    _require(
        contract["formal_identity"] is None,
        "H5 frozen scientific contract identity changed",
    )
    _require(
        _blob("configs/experiments/h5/formal_contract.json")
        == EXPECTED_CONTRACT_BLOB,
        "H5 formal contract blob drift",
    )
    _require(
        _blob("scripts/check_h5_formal_contract.py") == EXPECTED_CHECKER_BLOB,
        "H5 scientific checker blob drift",
    )
    _require(
        _blob("scripts/run_h5_official.py") == EXPECTED_RUNNER_BLOB,
        "H5 official runner blob drift",
    )
    _require(
        _blob("scripts/preserve_h5_boundary.py") == EXPECTED_PRESERVER_BLOB,
        "H5 preserver blob drift",
    )
    _require(
        _blob(".github/workflows/h5-formal-one-way.yml")
        == EXPECTED_WORKFLOW_BLOB,
        "H5 one-way workflow blob drift",
    )

    actual_source = {path: _blob(path) for path in EXPECTED_SOURCE_BLOBS}
    _require(actual_source == EXPECTED_SOURCE_BLOBS, "H5 source binding drift")
    source = contract["source_binding"]
    _require(
        source["engine_blob"] == EXPECTED_SOURCE_BLOBS["src/sparkbrain/engine.py"],
        "H5 engine contract binding drift",
    )
    _require(
        source["model_blob"] == EXPECTED_SOURCE_BLOBS["src/sparkbrain/model.py"],
        "H5 model contract binding drift",
    )
    _require(
        source["package_blob"] == EXPECTED_SOURCE_BLOBS["pyproject.toml"],
        "H5 package contract binding drift",
    )
    _require(
        source["h5_module_blob"] == EXPECTED_H5_MODULE_BLOB,
        "H5 module contract binding drift",
    )

    _require(
        contract["runtime_binding"]["python"] == "CPython 3.11.10",
        "H5 runtime binding drift",
    )
    _require(
        contract["candidate"]["implementation"] == "AuditedSparkBrain",
        "H5 candidate binding drift",
    )
    comparator = contract["comparator"]
    _require(
        comparator["implementation"] == "DenseEagerSparkBrain",
        "H5 comparator binding drift",
    )
    _require(
        comparator["inherits_candidate_engine"] is False
        and comparator["invokes_candidate_transition_path"] is False,
        "H5 comparator independence drift",
    )

    sparse = contract["formal_test_workloads"]["sparse_primary"]
    dense = contract["formal_test_workloads"]["dense_control"]
    _require(sparse["cell_count"] == 144, "H5 sparse cardinality drift")
    _require(dense["cell_count"] == 8, "H5 dense-control cardinality drift")
    _require(len(sparse["seeds"]) == 8, "H5 seed cardinality drift")
    _require(
        sparse["families"] == ["uniform", "clustered", "bursty"],
        "H5 workload family drift",
    )
    _require(sparse["sizes"] == [128, 384], "H5 workload size drift")
    _require(
        sparse["activity_fractions"] == [0.01, 0.05, 0.15],
        "H5 sparse activity drift",
    )
    _require(
        dense["activity_fractions"] == [1.0],
        "H5 dense-control activity drift",
    )

    quality = contract["quality_guard"]
    for field in (
        "logical_activation_max_abs_error_lte",
        "logical_threshold_max_abs_error_lte",
        "refractory_max_abs_error_lte",
        "eligibility_max_abs_error_lte",
    ):
        _require(quality[field] == 1e-10, f"H5 quality tolerance drift: {field}")

    statistic = contract["primary_statistic"]
    bootstrap = statistic["bootstrap"]
    _require(statistic["cluster_unit"] == "workload_seed", "H5 cluster drift")
    _require(bootstrap["replicates"] == 10000, "H5 bootstrap count drift")
    _require(bootstrap["seed"] == 75001, "H5 bootstrap seed drift")
    _require(bootstrap["quantile"] == "Type-7", "H5 quantile drift")

    rules = contract["decision_rule"]
    _require(">= 0.20" in rules["pass"], "H5 PASS CI margin drift")
    _require(">= 0.10" in rules["pass"], "H5 activity PASS margin drift")
    _require("<= 0.05" in rules["fail"], "H5 FAIL margin drift")
    _require(
        contract["raw_preservation_contract"]["required_before_scoring"]
        is True,
        "H5 raw-before-score contract weakened",
    )
    _require(
        contract["raw_preservation_contract"][
            "independent_refetch_digest_required_before_score"
        ]
        is True,
        "H5 preserve/refetch contract weakened",
    )

    print("H5 execution authority: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
