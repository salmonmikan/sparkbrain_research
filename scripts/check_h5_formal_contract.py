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
        contract["phase"]
        == "H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW",
        "H5 phase must stop at revised-comparator Analyst review",
    )
    require(
        contract["execution_authorized"] is False,
        "H5 execution must remain blocked",
    )
    require(
        contract["formal_identity"] is None,
        "H5 identity must remain unassigned",
    )
    require(
        contract["analyst_authority_commit"]
        == "fc1717f54ac045f29557e839268fc3b0f622acdf",
        "H5 semantic rework authority drifted",
    )

    source = contract["source_binding"]
    for path_key, blob_key in (
        ("engine_path", "engine_blob"),
        ("model_path", "model_blob"),
        ("package_path", "package_blob"),
        ("h5_module_path", "h5_module_blob"),
    ):
        actual = git_blob(source[path_key])
        require(
            actual == source[blob_key],
            f"blob mismatch for {source[path_key]}",
        )

    comparator = contract["comparator"]
    require(
        comparator["implementation"] == "DenseEagerSparkBrain",
        "standalone dense comparator class drifted",
    )
    require(
        comparator["inherits_candidate_engine"] is False,
        "dense comparator must not inherit candidate engine",
    )
    require(
        comparator["invokes_candidate_transition_path"] is False,
        "dense comparator must not invoke candidate transition path",
    )

    workloads = contract["formal_test_workloads"]
    sparse = workloads["sparse_primary"]
    dense = workloads["dense_control"]
    require(sparse["cell_count"] == 144, "unexpected sparse TEST cardinality")
    require(dense["cell_count"] == 8, "unexpected dense-control TEST cardinality")
    require(
        dense["activity_fractions"] == [1.0],
        "dense control must be fully active",
    )
    require(
        sparse["activity_fractions"] == [0.01, 0.05, 0.15],
        "sparse activity regimes changed",
    )
    require(len(sparse["seeds"]) == 8, "formal TEST seed count changed")

    quality = contract["quality_guard"]
    for field in (
        "logical_activation_max_abs_error_lte",
        "logical_threshold_max_abs_error_lte",
        "refractory_max_abs_error_lte",
        "eligibility_max_abs_error_lte",
    ):
        require(quality[field] == 1e-10, f"quality tolerance changed: {field}")
    require(
        quality["last_fire_vector"] == "exact",
        "last-fire guard weakened",
    )
    require(
        quality["fired_count_vector"] == "exact",
        "fired-count guard weakened",
    )
    require(
        quality["events_processed"] == "exact",
        "event-count guard weakened",
    )

    work = contract["audited_work"]
    require(
        work["candidate_bookkeeping_included"] is True,
        "candidate work omitted",
    )
    require(
        work["dense_common_work_included"] is True,
        "common dense work omitted",
    )
    required_counters = {
        "scheduler_writes",
        "scheduler_reads",
        "target_state_accesses",
        "state_materializations",
        "state_decay_evaluations",
        "threshold_relax_evaluations",
        "eligibility_edge_touches",
        "eligibility_multiplications",
        "route_edge_checks",
        "message_traversals",
        "activation_additions",
        "eligibility_additions",
        "threshold_additions",
        "residual_multiplications",
        "fanout_index_lookups",
    }
    require(
        set(work["counter_fields"]) == required_counters,
        "work counter schema changed",
    )

    statistic = contract["primary_statistic"]
    require(
        statistic["cluster_unit"] == "workload_seed",
        "cluster unit changed",
    )
    require(
        statistic["bootstrap"]["replicates"] == 10000,
        "bootstrap count changed",
    )
    require(
        statistic["bootstrap"]["seed"] == 75001,
        "bootstrap seed changed",
    )
    require(
        statistic["bootstrap"]["quantile"] == "Type-7",
        "quantile changed",
    )

    rules = contract["decision_rule"]
    require(">= 0.20" in rules["pass"], "PASS margin changed")
    require(">= 0.10" in rules["pass"], "activity PASS gate changed")
    require("<= 0.05" in rules["fail"], "FAIL margin changed")

    integrity = contract["pre_start_integrity"]
    require(
        integrity["formal_identity_is_intentionally_unassigned"] is True,
        "identity armed",
    )
    require(
        integrity["formal_test_forbidden_before_started"] is True,
        "TEST boundary weakened",
    )
    require(integrity["raw_before_score"] is True, "raw-before-score weakened")
    require(
        integrity["preserve_before_read_for_scoring"] is True,
        "preserve-before-read weakened",
    )
    print(
        "H5 revised dense comparator is bound, internally consistent, "
        "and execution remains blocked"
    )


if __name__ == "__main__":
    main()
