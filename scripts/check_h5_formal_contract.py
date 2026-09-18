from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/h5/formal_contract.json"


def git_blob(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    require(
        contract["phase"] == "H5_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW",
        "H5 phase must stop at Analyst review",
    )
    require(contract["execution_authorized"] is False, "H5 execution must remain blocked")
    require(contract["formal_identity"] is None, "H5 identity must remain unassigned")

    source = contract["source_binding"]
    for path_key, blob_key in (
        ("engine_path", "engine_blob"),
        ("model_path", "model_blob"),
        ("package_path", "package_blob"),
        ("h5_module_path", "h5_module_blob"),
    ):
        actual = git_blob(source[path_key])
        require(actual == source[blob_key], f"blob mismatch for {source[path_key]}")

    workloads = contract["formal_test_workloads"]
    sparse = workloads["sparse_primary"]
    dense = workloads["dense_control"]
    require(sparse["cell_count"] == 144, "unexpected sparse TEST cardinality")
    require(dense["cell_count"] == 8, "unexpected dense-control TEST cardinality")
    require(dense["activity_fractions"] == [1.0], "dense control must be fully active")
    require(
        sparse["activity_fractions"] == [0.01, 0.05, 0.15],
        "sparse activity regimes changed",
    )
    require(len(sparse["seeds"]) == 8, "formal TEST seed count changed")

    quality = contract["quality_guard"]
    require(
        quality["logical_activation_max_abs_error_lte"] == 1e-10,
        "quality tolerance changed",
    )
    require(quality["fired_count_vector"] == "exact", "fired-count guard weakened")
    require(quality["events_processed"] == "exact", "event-count guard weakened")

    work = contract["audited_work"]
    require(work["candidate_bookkeeping_included"] is True, "candidate work omitted")
    require(work["dense_common_work_included"] is True, "common dense work omitted")
    required_counters = {
        "queue_pushes",
        "queue_pops",
        "source_touches",
        "destination_touches",
        "state_touches",
        "state_decay_evaluations",
        "threshold_relax_evaluations",
        "eligibility_edge_touches",
        "eligibility_multiplications",
        "route_edge_checks",
        "message_traversals",
        "activation_additions",
        "eligibility_additions",
        "threshold_additions",
        "sequence_additions",
        "residual_multiplications",
        "fanout_bookkeeping",
    }
    require(set(work["counter_fields"]) == required_counters, "work counter schema changed")

    statistic = contract["primary_statistic"]
    require(statistic["cluster_unit"] == "workload_seed", "cluster unit changed")
    require(statistic["bootstrap"]["replicates"] == 10000, "bootstrap count changed")
    require(statistic["bootstrap"]["seed"] == 75001, "bootstrap seed changed")
    require(statistic["bootstrap"]["quantile"] == "Type-7", "quantile changed")

    integrity = contract["pre_start_integrity"]
    require(integrity["formal_identity_is_intentionally_unassigned"] is True, "identity armed")
    require(integrity["formal_test_forbidden_before_started"] is True, "TEST boundary weakened")
    require(integrity["raw_before_score"] is True, "raw-before-score weakened")
    require(
        integrity["preserve_before_read_for_scoring"] is True,
        "preserve-before-read weakened",
    )
    print("H5 formal-contract proposal is internally consistent and execution remains blocked")


if __name__ == "__main__":
    main()
