"""Build the reproducible R01-12 post-formal review manifest.

Only retained repository manifests are consumed.  R01-12D raw rows were not
preserved locally, so this generator deliberately does not reconstruct or
invent development family/phase metrics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV_PATH = ROOT / "artifacts/research/rv01/r01_12d/development_result_manifest.json"
FORMAL_PATH = ROOT / "artifacts/research/rv01/r01_12f/formal_result_manifest.json"
OUTPUT_PATH = ROOT / "artifacts/research/rv01/r01_12_postformal/review_manifest.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _weighted_first_hop(formal: dict, architecture: str) -> float:
    numerator = 0.0
    denominator = 0
    for row in formal["families"].values():
        count = int(row["final_route_probe_count"])
        numerator += count * float(row[f"{architecture}_mean_first_hop_coverage"])
        denominator += count
    if denominator != int(formal["cardinality"]["final_route_probe_count"]):
        raise RuntimeError("formal family route cardinality does not match manifest")
    return numerator / denominator


def _formal_family_metrics(formal: dict) -> dict:
    result: dict[str, dict] = {}
    for family, row in sorted(formal["families"].items()):
        routes = int(row["final_route_probe_count"])
        result[family] = {
            "field": {
                "contamination_per_route": row["field_contamination_count"] / routes,
                "exact_route_recovery_rate": row["field_exact_routes_recovered"] / routes,
                "first_hop_coverage": row["field_mean_first_hop_coverage"],
                "ordered_retention": row["field_route_weighted_ordered_retention"],
            },
            "reservoir": {
                "contamination_per_route": row["reservoir_contamination_count"] / routes,
                "exact_route_recovery_rate": row["reservoir_exact_routes_recovered"] / routes,
                "first_hop_coverage": row["reservoir_mean_first_hop_coverage"],
                "ordered_retention": row["reservoir_route_weighted_ordered_retention"],
            },
        }
    return result


def build_manifest() -> dict:
    dev = _load(DEV_PATH)
    formal = _load(FORMAL_PATH)
    dev_aggregate = dev["aggregate"]
    formal_aggregate = formal["aggregate"]
    dev_routes = int(dev_aggregate["route_count"])
    formal_routes = int(formal["cardinality"]["final_route_probe_count"])

    if dev["experiment_id"] != "R01-12D":
        raise RuntimeError("unexpected development experiment")
    if formal["candidate_id"] != "rv01-r01-12-interference-heldout-v1":
        raise RuntimeError("unexpected formal candidate")
    if formal["execution"]["execution_policy"] if "execution_policy" in formal["execution"] else None:
        raise RuntimeError("execution policy unexpectedly nested")
    if formal["execution_policy"] != "one-way-no-rerun":
        raise RuntimeError("formal evidence is not marked one-way/no-rerun")

    return {
        "aggregate": {
            "development": {
                "field": {
                    "contamination_count": dev_aggregate["field_contamination_count"],
                    "contamination_per_route": dev_aggregate["field_contamination_count"] / dev_routes,
                    "exact_route_count": dev_aggregate["field_exact_route_count"],
                    "exact_route_recovery_rate": dev_aggregate["field_exact_route_count"] / dev_routes,
                    "ordered_retention": dev_aggregate["field_mean_ordered_retention_route_weighted"],
                },
                "reservoir": {
                    "contamination_count": dev_aggregate["reservoir_contamination_count"],
                    "contamination_per_route": dev_aggregate["reservoir_contamination_count"] / dev_routes,
                    "exact_route_count": dev_aggregate["reservoir_exact_route_count"],
                    "exact_route_recovery_rate": dev_aggregate["reservoir_exact_route_count"] / dev_routes,
                    "ordered_retention": dev_aggregate["reservoir_mean_ordered_retention_route_weighted"],
                },
            },
            "formal": {
                "field": {
                    "contamination_count": formal_aggregate["field_contamination_count"],
                    "contamination_per_route": formal_aggregate["field_contamination_count"] / formal_routes,
                    "exact_route_count": formal_aggregate["field_exact_routes_recovered"],
                    "exact_route_recovery_rate": formal_aggregate["field_exact_routes_recovered"] / formal_routes,
                    "first_hop_coverage": _weighted_first_hop(formal, "field"),
                    "ordered_retention": formal_aggregate["field_route_weighted_ordered_retention"],
                },
                "reservoir": {
                    "contamination_count": formal_aggregate["reservoir_contamination_count"],
                    "contamination_per_route": formal_aggregate["reservoir_contamination_count"] / formal_routes,
                    "exact_route_count": formal_aggregate["reservoir_exact_routes_recovered"],
                    "exact_route_recovery_rate": formal_aggregate["reservoir_exact_routes_recovered"] / formal_routes,
                    "first_hop_coverage": _weighted_first_hop(formal, "reservoir"),
                    "ordered_retention": formal_aggregate["reservoir_route_weighted_ordered_retention"],
                },
            },
        },
        "analysis_boundary": {
            "architecture_modified": False,
            "development_raw_rows_retained": False,
            "formal_candidate_consumed": True,
            "formal_rerun_permitted": False,
            "raw_result_modified": False,
            "threshold_tuning_performed": False,
        },
        "development": {
            "execution_source_sha": dev["execution_source_sha"],
            "experiment_id": dev["experiment_id"],
            "result_payload_hash": dev["result_payload_hash"],
            "route_probe_count": dev_routes,
            "world_count": dev_aggregate["world_count"],
        },
        "formal": {
            "candidate_id": formal["candidate_id"],
            "raw_sha256": formal["result_binding"]["raw_result_file_sha256"],
            "route_probe_count": formal_routes,
            "source_git_sha": formal["execution"]["frozen_source_git_sha"],
            "world_count": formal["cardinality"]["world_count"],
        },
        "formal_family_metrics": _formal_family_metrics(formal),
        "hypothesis_verdicts": {
            "A_field_is_generally_stronger_memory_substrate": "NOT_SUPPORTED_AS_GENERAL_SELECTIVE_MEMORY_SUPERIORITY",
            "B_field_has_high_coverage_but_low_precision": "SUPPORTED_BEST_FIT",
            "C_difference_is_only_overactivation": "VIABLE_BUT_UNRESOLVED_BY_R01_12",
        },
        "reproducibility_boundary": {
            "development_family_metrics_generated": False,
            "development_reason": "raw per-world/per-probe rows are not retained locally",
            "formal_family_metrics_source": "retained formal_result_manifest.json",
            "training_role_diagnostics_generated": False,
        },
        "schema_version": "rv01-r01-12-postformal-review-v2",
        "trace_availability": {
            "development_intermediate_phase_trace": False,
            "direct_phase_by_phase_architecture_comparison": False,
            "formal_field_intermediate_phase_trace": True,
            "formal_reservoir_intermediate_phase_trace": False,
        },
    }


def _render(value: dict) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = _render(build_manifest())
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            raise SystemExit("R01-12 post-formal review manifest is stale")
        print("R01-12 post-formal review manifest: PASS")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
