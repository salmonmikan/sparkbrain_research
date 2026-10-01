"""Read-only arithmetic on retained PR169 JSON. Never imports SparkBrain."""

import argparse
import copy
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def similarity(a, b):
    left, right = a["ordered_units"], b["ordered_units"]
    prev = list(range(len(right) + 1))
    for i, x in enumerate(left, 1):
        cur = [i]
        for j, y in enumerate(right, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (x != y)))
        prev = cur
    edit = 1 - prev[-1] / max(len(left), len(right))
    sa, sb = set(a["unit_ids"]), set(b["unit_ids"])
    jac = len(sa & sb) / max(1, len(sa | sb))
    ta, tb = a["relative_bins"], b["relative_bins"]
    if len(ta) == len(tb):
        timing = math.exp(
            -sum(abs(x - y) for x, y in zip(ta, tb, strict=True)) / len(ta) / 2
        )
    else:
        short, long = (a, b) if len(left) < len(right) else (b, a)
        timing = 0.0
        if len(short["ordered_units"]) >= 2:
            for ix in itertools.combinations(
                range(len(long["ordered_units"])), len(short["ordered_units"])
            ):
                if [long["ordered_units"][i] for i in ix] != short["ordered_units"]:
                    continue
                selected = [long["relative_bins"][i] for i in ix]
                selected = [x - selected[0] for x in selected]
                bins = [x - short["relative_bins"][0] for x in short["relative_bins"]]
                error = sum(
                    abs(x - y) for x, y in zip(selected, bins, strict=True)
                ) / len(bins)
                timing = max(timing, math.exp(-error / 4))
    return {
        "edit": edit,
        "jaccard": jac,
        "timing": timing,
        "total": 0.55 * edit + 0.25 * jac + 0.20 * timing,
    }


def audit(root):
    manifest = json.loads((root / "manifest.json").read_text())
    for rel, expected in manifest["files"].items():
        require(
            hashlib.sha256((root / rel).read_bytes()).hexdigest() == expected,
            f"hash mismatch: {rel}",
        )
    result = {
        "source_pin": "0bcb2c1b23c29e5107111343a757c57c1f7bbb41",
        "manifest_sha256": hashlib.sha256(
            (root / "manifest.json").read_bytes()
        ).hexdigest(),
        "retained_manifest_files_verified": len(manifest["files"]),
        "model_calls": 0,
        "scientific_credit": 0,
        "cases": {},
    }
    for seed, arm, phase in itertools.product(
        (910071, 910072), ("S", "F"), ("return", "interleaved")
    ):
        key = f"{seed}-{arm}-{phase}"
        prefix = json.loads(
            (root / f"{seed}-{arm}-prefix/checkpoint/brain.json").read_text()
        )["payload"]
        final = json.loads((root / key / "checkpoint/brain.json").read_text())[
            "payload"
        ]
        bank = copy.deepcopy(prefix["assemblies"]["candidates"])
        counts = copy.deepcopy(prefix["predictor"]["counts"])
        next_id = prefix["assemblies"]["next_id"]
        records = [
            json.loads(s) for s in (root / key / "raw.jsonl").read_text().splitlines()
        ]
        field_before = prefix["base"]["payload"]["field"]
        field_after = final["base"]["payload"]["field"]
        receptor_ids = set(field_before["receptor_ids"])
        internal_ids = set()
        reasons, outcome_groups, cue_counts, summaries = (
            Counter(),
            Counter(),
            Counter(),
            [],
        )
        losses = Counter()
        for i, row in enumerate(records):
            raw = row["raw_result"]
            internal = [
                s
                for s in raw["v04_result"]["spikes"]
                if s["unit_id"] not in receptor_ids
            ]
            internal_ids.update(s["unit_id"] for s in internal)
            if not raw["patterns"]:
                require(len(internal) < 2, f"{key}:{i}: unexplained absence of pattern")
            require(
                len(raw["patterns"]) <= 1,
                "unexpected multiple patterns; expand audit explicitly",
            )
            pre_scores = {}
            activation = None
            if raw["patterns"]:
                pattern = raw["patterns"][0]
                pre_scores = {
                    k: similarity(v["prototype"], pattern) for k, v in bank.items()
                }
                nearest = min(pre_scores, key=lambda k: (-pre_scores[k]["total"], k))
                score = pre_scores[nearest]["total"]
                if score < prefix["assemblies"]["config"]["similarity_threshold"]:
                    nearest = f"assembly-{next_id:04d}"
                    next_id += 1
                    bank[nearest] = {
                        "prototype": copy.deepcopy(pattern),
                        "episode_count": 1,
                    }
                    score = 1.0
                else:
                    bank[nearest]["episode_count"] += 1
                act = raw["assembly_activations"][0]
                require(act["assembly_id"] == nearest, f"{key}:{i}: candidate")
                require(
                    abs(act["similarity"] - score) < 1e-14, f"{key}:{i}: similarity"
                )
                require(
                    act["episode_count"] == bank[nearest]["episode_count"],
                    f"{key}:{i}: maturity count",
                )
                mature = (
                    bank[nearest]["episode_count"]
                    >= prefix["assemblies"]["config"]["mature_episodes"]
                )
                require(act["mature"] == mature, f"{key}:{i}: maturity flag")
                activation = nearest if mature else None
            require(activation == row["assembly_id"], f"{key}:{i}: selected activation")
            table = counts.get(activation, {})
            p1 = (1 + table.get("1", 0)) / (2 + sum(table.values()))
            value = max(sorted(table), key=lambda k: table[k]) if table else None
            confidence = table[value] / sum(table.values()) if table else 0.0
            require(p1 == row["p1"], f"{key}:{i}: p1")
            require(
                (None if value is None else int(value)) == row["native"],
                f"{key}:{i}: native",
            )
            require(
                confidence == raw["prediction"]["confidence"], f"{key}:{i}: confidence"
            )
            classification = (
                "abstain"
                if value is None
                else ("correct" if int(value) == row["outcome"] else "wrong")
            )
            outcome_groups[classification] += 1
            losses[classification] += (p1 - row["outcome"]) ** 2 / len(records)
            reason = (
                "no_pattern"
                if not raw["patterns"]
                else "immature"
                if activation is None
                else "empty_readout"
                if value is None
                else "prediction"
            )
            reasons[reason] += 1
            emitted = {
                x["metadata"].get("origin_channel"): x for x in raw["emitted_pulses"]
            }
            original = {x["channel"]: x for x in raw["raw_pulses"]}
            for channel in ("A", "F", "C", "Q"):
                if channel in emitted:
                    cue_counts[channel] += 1
                    require(
                        emitted[channel]["time_ms"] == original[channel]["time_ms"],
                        f"{key}:{i}: cue time",
                    )
            summaries.append(
                {
                    "index": i,
                    "assembly_id": activation,
                    "outcome": row["outcome"],
                    "p1": p1,
                    "native": row["native"],
                    "confidence": confidence,
                    "counts_before": copy.deepcopy(table),
                    "reason": reason,
                    "patterns": raw["patterns"],
                    "scores_before": pre_scores,
                    "internal_spikes": internal,
                    "changed_weights": row["changed_weights"],
                    "changed_delays": row["changed_delays"],
                    "spike_count": raw["stability"]["spike_count"],
                    "mean_threshold": raw["stability"]["mean_threshold"],
                }
            )
            if activation is not None:
                t = counts.setdefault(activation, {})
                target = str(row["outcome"])
                t[target] = t.get(target, 0) + 1
        require(counts == final["predictor"]["counts"], f"{key}: final readout")
        require(
            set(bank) == set(final["assemblies"]["candidates"]),
            f"{key}: final candidate inventory",
        )
        for k, v in bank.items():
            require(
                v["prototype"] == final["assemblies"]["candidates"][k]["prototype"],
                f"{key}: immutable prototype",
            )
            require(
                v["episode_count"]
                == final["assemblies"]["candidates"][k]["episode_count"],
                f"{key}: final maturity",
            )
        edge_before = {
            (e["source_id"], e["target_id"]): e for e in field_before["connections"]
        }
        edge_after = {
            (e["source_id"], e["target_id"]): e for e in field_after["connections"]
        }
        require(set(edge_before) == set(edge_after), f"{key}: topology changed")
        changed_edges = [
            {"before": edge_before[k], "after": v}
            for k, v in edge_after.items()
            if edge_before[k] != v
        ]
        result["cases"][key] = {
            "rows": len(records),
            "brier": sum(losses.values()),
            "outcome_groups": dict(outcome_groups),
            "brier_contributions": dict(losses),
            "reasons": dict(reasons),
            "cue_emission_counts": dict(cue_counts),
            "prefix_counts": prefix["predictor"]["counts"],
            "final_counts": counts,
            "internal_firing_unit_ids": sorted(internal_ids),
            "edges_among_firing_internal_units": [
                list(k)
                for k in edge_before
                if k[0] in internal_ids and k[1] in internal_ids
            ],
            "changed_connection_parameters": changed_edges,
            "row_audit": summaries,
        }
    result["ordinary_memory_cases"] = {}
    for seed, arm, phase in itertools.product(
        (910071, 910072), ("Q", "H", "R"), ("return", "interleaved")
    ):
        key = f"{seed}-{arm}-{phase}"
        records = [
            json.loads(s) for s in (root / key / "raw.jsonl").read_text().splitlines()
        ]
        groups = Counter(
            "abstain"
            if r["native"] is None
            else "correct"
            if r["native"] == r["outcome"]
            else "wrong"
            for r in records
        )
        result["ordinary_memory_cases"][key] = {
            "rows": len(records),
            "brier": sum((r["p1"] - r["outcome"]) ** 2 for r in records) / len(records),
            "outcome_groups": dict(groups),
        }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = audit(args.root)
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}))
    for name, case in report["cases"].items():
        print(
            name,
            json.dumps(
                {
                    k: v
                    for k, v in case.items()
                    if k not in {"row_audit", "prefix_counts", "final_counts"}
                }
            ),
        )
