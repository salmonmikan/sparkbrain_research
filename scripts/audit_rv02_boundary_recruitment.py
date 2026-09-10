"""Independent RD002 retained-raw acceptance: no model execution or repair."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


OLD = load_script("rd002_inherited_arithmetic", ROOT / "scripts/audit_rv02_recruitment.py")
require = OLD.require


def reconstruct_score(probe, route, unit_count):
    """Independent expression of the frozen existing subsequence task convention."""
    generated = [s["unit_id"] for s in probe["spikes"] if s["time_ms"] > 100.0]
    visible = [u for u in generated if 0 <= u < 36]
    expected = list(route[1:])
    matched = 0
    for unit in visible:
        if matched < len(expected) and unit == expected[matched]:
            matched += 1
    errors = sum(u not in route for u in visible)
    got, wanted = Counter(visible), Counter(expected)
    return {
        "generated_units": visible,
        "ordered_retention": matched / len(expected),
        "exact_sequence_recovered": visible == expected,
        "rv01_compatible_exact_route": matched == len(expected) and errors == 0,
        "raw_contamination": errors,
        "contamination_per_active_unit": errors / len(set(generated)) if generated else None,
        "contamination_per_total_unit": errors / unit_count,
        "contamination_per_recovered_route_unit": errors / matched if matched else None,
        "contamination_per_candidate_activity": errors / len(visible) if visible else None,
        "missing_expected_count": len(expected) - matched,
        "repeated_expected_unit_spikes": sum(max(0, got[u] - 1) for u in set(expected)),
        "cue_recurrence_spikes": got[route[0]],
        "excess_route_event_count": sum(max(0, got[u] - wanted[u]) for u in set(route)),
    }


def verify_probe(probe, score, route, unit_count):
    metrics = OLD.verify_probe_metrics(probe, unit_count)
    require(
        probe["actual_arrivals"] < 4096 and probe["actual_spikes"] < 512,
        "RD002 hitting native bound is incomplete",
    )
    expected = reconstruct_score(probe, route, unit_count)
    require(json.loads(json.dumps(score)) == expected, "task score reconstruction mismatch")
    require(
        probe["observer_equivalence"] is True
        and probe["observed_state_hash"] == probe["reference_state_hash"],
        "observer noninterference",
    )
    require(
        probe["probe_connection_hash_before"] == probe["probe_connection_hash_after"],
        "probe learning",
    )
    return metrics


def audit_bundle(output, source_root=ROOT):
    runner = load_script(
        "rd002_retained_verifier", source_root / "scripts/run_rv02_boundary_recruitment.py"
    )
    verified = runner.verify_bundle(output, source_root=source_root)
    manifest = json.loads((output / "manifest.json").read_text())
    rows = [
        json.loads(line)
        for line in gzip.decompress((output / "raw_cells.jsonl.gz").read_bytes()).splitlines()
    ]
    old_compressed = (source_root / "artifacts/research/rv02/rd001/raw_cells.jsonl.gz").read_bytes()
    require(
        hashlib.sha256(old_compressed).hexdigest()
        == "d6507a988a3a2763742714993d2b420f735bf9fc76b45c308ce26b397d96e07e",
        "retained RD001 compressed identity",
    )
    old_raw = gzip.decompress(old_compressed)
    require(
        hashlib.sha256(old_raw).hexdigest()
        == "d786fd242c1c6621b39a6700096536a96109a67333222304412be90e5e510d9d",
        "retained RD001 raw identity",
    )
    old_rows = [json.loads(line) for line in old_raw.splitlines()]
    require(
        manifest["cell_timeout_seconds"] == 60
        and manifest["total_timeout_seconds"] == 600
        and manifest["memory_limit_bytes"] == 1024**3,
        "manifest resource contract",
    )
    old_cells = {(r["family"], r["scale"]): r["result"] for r in old_rows}
    require(len(rows) == 18 and all(r["status"] == "complete" for r in rows), "incomplete cells")
    groups = {}
    baseline_matches = 0
    maximum_arrivals = maximum_spikes = 0
    for row in rows:
        cell = row["result"]
        old_cell = old_cells[(row["family"], row["scale"])]
        require(cell["training_rows"] == old_cell["training_rows"], "training differs from RD001")
        require(cell["audit"] == old_cell["audit"], "fixed world/topology differs")
        require(0 <= row["wall_seconds"] <= 60, "wall ceiling")
        require(0 <= cell["peak_rss_kib"] <= 1024**2, "memory ceiling")
        require(
            cell["changed_hidden_edges"] == [] and cell["hidden_external_trace_count"] == 0,
            "hidden learning boundary",
        )
        count = cell["audit"]["unit_count"]
        require(
            [u["unit_id"] for u in cell["trained_state"]["units"]] == list(range(count)),
            "trained units",
        )
        require(
            all(
                u["base_threshold"] == 0.5
                and u["potential"] == 0
                and u["adaptation"] == 0
                and u["spike_count"] == 0
                for u in cell["trained_state"]["units"]
            ),
            "initial unit dynamics",
        )
        require(len(cell["trained_state"]["connections"]) == count * 8, "edge slots")
        by_identity = {(p["gain"], p["route_index"]): p for p in cell["route_probes"]}
        for pair in cell["route_probes"]:
            gain, index = pair["gain"], pair["route_index"]
            connections = cell["trained_state"]["connections"]
            gained = copy.deepcopy(connections)
            changes = []
            for edge in gained:
                if edge["source_id"] < 36 <= edge["target_id"]:
                    changes.append(
                        {
                            "edge": [edge["source_id"], edge["target_id"]],
                            "old_weight": edge["weight"],
                            "new_weight": edge["weight"] * gain,
                        }
                    )
                    edge["weight"] *= gain
            require(pair["gain_interventions"] == changes, "gain isolation records")

            def connection_digest(edges):
                return hashlib.sha256(
                    json.dumps(
                        edges, sort_keys=True, separators=(",", ":"), allow_nan=False
                    ).encode()
                ).hexdigest()

            require(
                cell["trained_connection_hash"] == connection_digest(connections), "trained hash"
            )
            require(
                pair["natural"]["initial_connection_hash"] == connection_digest(gained),
                "gained hash",
            )
            require(
                pair["natural"]["probe_connection_hash_before"] == connection_digest(gained),
                "natural isolation",
            )
            cut = copy.deepcopy(gained)
            cut_changes = []
            for edge in cut:
                if (edge["source_id"] < 36) != (edge["target_id"] < 36):
                    cut_changes.append(
                        {
                            "edge": [edge["source_id"], edge["target_id"]],
                            "old_weight": edge["weight"],
                        }
                    )
                    edge["weight"] = 0.0
            require(
                pair["boundary_zero"]["boundary_interventions"] == cut_changes,
                "cut isolation records",
            )
            require(
                pair["boundary_zero"]["probe_connection_hash_before"] == connection_digest(cut),
                "cut isolated hash",
            )
            # World route membership is supplied by the verifier's fixed audit, never scores.
            world = next(
                w
                for w in runner.development_worlds(runner.ScaleStudyConfig())
                if w["family"] == row["family"]
            )
            route = world["routes"][index]
            for name in ("natural", "boundary_zero"):
                probe = pair[name]
                require(probe["status"] == "complete", "incomplete probe")
                metrics = verify_probe(probe, probe["behavior"], route, count)
                groups.setdefault((gain, name), []).append((probe, metrics))
                maximum_arrivals = max(maximum_arrivals, probe["actual_arrivals"])
                maximum_spikes = max(maximum_spikes, probe["actual_spikes"])
            require(
                pair["boundary_visible_trace_equal"]
                is (pair["natural"]["visible_trace"] == pair["boundary_zero"]["visible_trace"]),
                "trace comparison",
            )
            require(
                pair["boundary_visible_final_state_equal"]
                is (
                    pair["natural"]["visible_final_state"]
                    == pair["boundary_zero"]["visible_final_state"]
                ),
                "state comparison",
            )
            baseline = by_identity[(1.0, index)]
            for key in (
                "spikes",
                "arrival_observations",
                "hidden_units",
                "visible_final_state",
                "observed_state_hash",
                "reference_state_hash",
                "probe_connection_hash_before",
            ):
                require(
                    pair["boundary_zero"][key] == baseline["boundary_zero"][key],
                    "cut controls differ across gain",
                )
            if gain == 1.0:
                prior = old_cell["route_probes"][index]["natural"]
                require(
                    all(pair["natural"][key] == value for key, value in prior.items()),
                    "baseline not byte-equivalent to retained RD001 natural",
                )
                baseline_matches += 1
    require(
        sum(len(v) for v in groups.values()) == 468 and baseline_matches == 78, "probe completeness"
    )
    require(sum(r["wall_seconds"] for r in rows) <= 600, "total wall ceiling")
    conditions = {
        f"{gain:g}:{name}": {
            "probes": len(values),
            "hidden_spiking_probes": sum(m["hidden_spikes"] > 0 for _, m in values),
            "hidden_spikes": sum(m["hidden_spikes"] for _, m in values),
            "strict_exact_probes": sum(
                p["behavior"]["exact_sequence_recovered"] for p, _ in values
            ),
            "raw_contamination": sum(p["behavior"]["raw_contamination"] for p, _ in values),
            "excess_route_events": sum(
                p["behavior"]["excess_route_event_count"] for p, _ in values
            ),
            "queue_drained_probes": sum(m["queue_drained"] for _, m in values),
        }
        for (gain, name), values in sorted(groups.items())
    }
    return {
        **verified,
        "engineering_accepted": True,
        "formal_execution_allowed": False,
        "source_git_sha": manifest["source_git_sha"],
        "baseline_exact_matches": baseline_matches,
        "maximum_probe_arrivals": maximum_arrivals,
        "maximum_probe_spikes": maximum_spikes,
        "conditions": conditions,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit_bundle(args.output), sort_keys=True, indent=2))
