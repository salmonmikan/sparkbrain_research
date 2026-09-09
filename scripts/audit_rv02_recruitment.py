"""Post-execution RD001 raw reconstruction; never executes a model or repairs a run."""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def equal(actual: float, expected: float, reason: str) -> None:
    require(math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-12,
                                                  abs_tol=1e-12), reason)


def verify_probe_metrics(probe: dict, unit_count: int) -> dict:
    """Rebuild fixed RD001 potentials and hidden aggregates from event-group records."""
    require(probe["horizon_ms"] in (40.0, 160.0), "undeclared horizon")
    equal(probe["final_clock_ms"], 100.0 + probe["horizon_ms"], "probe clock")
    rows = probe["arrival_observations"]
    keys = [(r["time_ms"], r["target_id"]) for r in rows]
    require(keys == sorted(set(keys)), "duplicate or unordered event groups")
    states = defaultdict(lambda: (0.0, 0.0, 0.0))
    by_unit = defaultdict(list)
    spike_keys = []
    for row in rows:
        time, target = row["time_ms"], row["target_id"]
        require(type(target) is int and 0 <= target < unit_count, "invalid target")
        require(100.0 <= time <= probe["final_clock_ms"], "out-of-horizon event")
        count = row["arrival_count"]
        require(type(count) is int and count > 0, "invalid arrival count")
        positive, negative = row["positive_current"], row["negative_current"]
        require(math.isfinite(positive) and positive >= 0, "invalid positive current")
        require(math.isfinite(negative) and negative >= 0, "invalid negative current")
        pc = row["positive_current_arrival_count"]
        require(type(pc) is int and 0 <= pc <= count, "positive-arrival count")
        require((pc > 0) == (positive > 0), "zero current counted as positive")
        stored, last_time, refractory_until = states[target]
        decayed = stored * math.exp(-(time-last_time)/18.0)
        refractory = time < refractory_until
        net = positive-negative
        integrated = min(0.0, net) if refractory else net
        before_reset = decayed+integrated
        fired = not refractory and before_reset+1e-12 >= 0.5
        equal(row["decayed_potential"], decayed, "decayed potential")
        equal(row["integrated_net_current"], integrated, "integrated current")
        equal(row["potential_before_reset"], before_reset, "pre-reset potential")
        equal(row["threshold"], 0.5, "changed threshold")
        equal(row["refractory_suppressed_net_positive"],
              max(0.0, net) if refractory else 0.0, "refractory suppression")
        require(row["refractory"] is refractory and row["spiked"] is fired,
                "refractory/spiking semantics")
        after = 0.0 if fired else before_reset
        equal(row["potential_after_event"], after, "post-event potential")
        states[target] = (after, time, time+1.25 if fired else refractory_until)
        if fired:
            spike_keys.append((time, target))
        by_unit[target].append(row)
    require(spike_keys == [(s["time_ms"], s["unit_id"]) for s in probe["spikes"]],
            "raw spike/event mismatch")
    require(probe["actual_spikes"] == len(spike_keys) <= 512, "spike budget/count")
    require(probe["actual_arrivals"] == sum(r["arrival_count"] for r in rows) <= 4096,
            "arrival budget/count")
    require([r["unit_id"] for r in probe["hidden_units"]] == list(range(36, unit_count)),
            "hidden unit inventory")
    require(probe["queue_drained"] is (probe["final_queue_size"] == 0), "queue state")
    fields = ("arrival_count", "positive_current", "negative_current", "integrated_net_current",
              "refractory_suppressed_net_positive", "positive_current_arrival_count")
    for hidden in probe["hidden_units"]:
        unit = hidden["unit_id"]
        observations = by_unit[unit]
        for field in fields:
            equal(hidden[field], sum(r[field] for r in observations), "hidden " + field)
        require(hidden["spike_count"] == sum(r["spiked"] for r in observations), "hidden spikes")
        ratio = max((r["potential_before_reset"]/r["threshold"] for r in observations),
                    default=None)
        if ratio is None:
            require(hidden["maximum_potential_threshold_ratio"] is None, "silent ratio not null")
        else:
            equal(hidden["maximum_potential_threshold_ratio"], ratio, "hidden peak ratio")
        stored, last_time, _ = states[unit]
        equal(hidden["stored_final_potential"], stored, "hidden stored potential")
        equal(hidden["last_update_ms"], last_time, "hidden last update")
        equal(hidden["projected_final_potential"],
              stored*math.exp(-(probe["final_clock_ms"]-last_time)/18.0), "hidden projection")
    return {"hidden_positive_current_units": sum(r["positive_current"] > 0
                                                for r in probe["hidden_units"]),
            "hidden_spikes": sum(r["spike_count"] for r in probe["hidden_units"]),
            "hidden_positive_current": sum(r["positive_current"] for r in probe["hidden_units"]),
            "queue_drained": probe["queue_drained"]}


def audit_bundle(output: Path, source_root: Path = ROOT) -> dict:
    spec = importlib.util.spec_from_file_location(
        "rd001_saved_verifier", source_root / "scripts/run_rv02_recruitment.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    verified = runner.verify_bundle(output, source_root=source_root)
    require(verified["complete_cells"] == 18 and verified["complete_probes"] == 252,
            "incomplete diagnosis cannot be accepted")
    manifest = json.loads((output / "manifest.json").read_text())
    require(manifest["cell_timeout_seconds"] == 60 and manifest["total_timeout_seconds"] == 600
            and manifest["memory_limit_bytes"] == 1024**3, "resource contract mismatch")
    raw = gzip.decompress((output / "raw_cells.jsonl.gz").read_bytes())
    rows = [json.loads(line) for line in raw.splitlines()]
    conditions = defaultdict(list)
    boundary_equal = []
    maximum_arrivals = maximum_spikes = 0
    for row in rows:
        result = row["result"]
        require(0 <= row["wall_seconds"] <= 60, "cell elapsed ceiling")
        require(0 <= result["peak_rss_kib"] <= 1024**2, "RSS ceiling")
        n = result["audit"]["unit_count"]
        probes = [("positive_control", result["positive_control"])]
        for route in result["route_probes"]:
            probes.extend((name, route[name]) for name in ("natural", "extended", "boundary_zero"))
            boundary_equal.append(route["boundary_visible_final_state_equal"])
        for name, probe in probes:
            conditions[name].append(verify_probe_metrics(probe, n))
            maximum_arrivals = max(maximum_arrivals, probe["actual_arrivals"])
            maximum_spikes = max(maximum_spikes, probe["actual_spikes"])
        for training in result["training_rows"]:
            require(training["external_unit"] < 36, "hidden external teaching")
            for update in training["updates"]:
                require(update["source_id"] < 36 and update["target_id"] < 36,
                        "hidden learning update")
    require(sum(r["wall_seconds"] for r in rows) <= 600, "aggregate elapsed ceiling")
    return {**verified, "engineering_accepted": True, "formal_execution_allowed": False,
            "source_git_sha": manifest["source_git_sha"],
            "maximum_probe_arrivals": maximum_arrivals, "maximum_probe_spikes": maximum_spikes,
            "boundary_visible_state_equal_count": sum(boundary_equal),
            "conditions": {name: {"probes": len(values),
                           "probes_with_positive_hidden_current": sum(
                               r["hidden_positive_current_units"] > 0 for r in values),
                           "hidden_spikes": sum(r["hidden_spikes"] for r in values),
                           "queue_drained_probes": sum(r["queue_drained"] for r in values)}
                           for name, values in sorted(conditions.items())}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit_bundle(args.output), sort_keys=True, indent=2))
