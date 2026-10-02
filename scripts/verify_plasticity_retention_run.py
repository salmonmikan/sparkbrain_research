#!/usr/bin/env python3
"""Data-only audit of the one retention run; never imports model or execution runner."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "artifacts/research/plasticity_retention_preparation_20261001"
PINS = {
    "inputs.json": "6e9ae9652cf4593e4401e9ce149d1ff178007065c732c2950e904efb523b3773",
    "jobs.json": "e67c82326a43856aa4628c45d21ebd5cd8d9edf7b09c76c232982052544db1d6",
    "prefix_sources.json": "d9bc263106921a4c862e540795fb56c02565b8d8f370a88b570814448ee33dc9",
}
PROTOCOL_SHA = "79a37f24eda0a5b82bb6f6e3428f48442a593f10dcb729dc3d67b30014ec0fb3"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def read(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value, *, newline=False) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256((raw + ("\n" if newline else "")).encode()).hexdigest()


def lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def verify_audit_interpreter(dependencies: dict) -> None:
    require(
        dependencies.get("python_version") == sys.version
        and dependencies.get("executable_sha256") == sha(Path(sys.executable).resolve()),
        "audit interpreter differs from frozen execution interpreter",
    )


def verify_authority_records(
    gate: dict, expected_commit: str, expected_manifest: str, output_root: str
) -> None:
    """Check retained authority statements; their authenticity is externally established."""
    flags = {
        "review": "source_review_approved",
        "publication": "verified_published",
        "approval": "approved_for_execution",
    }
    require(
        gate.get("source_commit") == expected_commit
        and gate.get("manifest_sha256") == expected_manifest,
        "run is not bound to expected source publication",
    )
    records = gate.get("records")
    require(isinstance(records, dict) and set(records) == set(flags), "authority record inventory")
    for kind, flag in flags.items():
        record = records[kind]
        require(isinstance(record, dict) and record.get(flag) is True, kind + " authority flag")
        require(
            record.get("source_commit") == expected_commit
            and record.get("manifest_sha256") == expected_manifest
            and record.get("output_root") == output_root
            and type(record.get("ceiling_pairs")) is int
            and record["ceiling_pairs"] == 768,
            kind + " authority scope binding",
        )
        require(
            all(
                type(record.get(key)) is str and bool(record[key].strip())
                for key in ("record_url", "recorded_by")
            ),
            kind + " authority provenance",
        )


def verify_retained_records(
    output: Path,
    gate: dict,
    expected_commit: str,
    expected_manifest: str,
    output_root: str,
    expected_record_hashes: dict,
) -> tuple[dict, dict]:
    verify_authority_records(gate, expected_commit, expected_manifest, output_root)
    require(Path(output_root).is_absolute(), "authority output root must be absolute")
    files = gate.get("record_files")
    require(
        isinstance(files, dict) and set(files) == {"review", "publication", "approval"},
        "retained authority file inventory",
    )
    paths, hashes = {}, {}
    for kind, record in files.items():
        relative = "authority-records/" + kind + ".json"
        require(
            isinstance(record, dict)
            and set(record) == {"path", "sha256", "bytes"}
            and record["path"] == relative
            and type(record["bytes"]) is int,
            "retained authority file descriptor",
        )
        path = output / relative
        require(
            sha(path) == expected_record_hashes[kind], "independent authority record pin: " + kind
        )
        require(
            path.stat().st_size == record["bytes"]
            and sha(path) == record["sha256"]
            and read(path) == gate["records"][kind],
            "retained authority bytes/record binding",
        )
        paths[kind] = str(Path(output_root) / relative)
        hashes[kind] = record["sha256"]
    return paths, hashes


def memory_raster(supplied: dict) -> list[float]:
    """Recalculate the public wrapper's fixed normalized time/channel representation."""
    channels = "ACFHIJKLMQ"
    values = [0.0] * (41 * len(channels))
    for pulse in supplied["pulses"]:
        relative = pulse["time_ms"] - supplied["start_ms"]
        require(0 <= relative <= 40, "memory raster time bound")
        offset = channels.index(pulse["channel"]) * 41
        lower = math.floor(relative)
        fraction = relative - lower
        values[offset + lower] += pulse["magnitude"] * (1 - fraction)
        if fraction:
            values[offset + lower + 1] += pulse["magnitude"] * fraction
    total = sum(values)
    require(total > 0, "empty memory raster")
    return [value / total for value in values]


def verify_memory_history(
    arm: str,
    rows: list[dict],
    receipts: list[dict],
    observations: list[dict],
    prefix: dict,
    final: dict,
) -> None:
    """Recalculate H/R dictionary arithmetic only; never load or invoke a model."""
    require(arm in ("H", "R") and prefix["arm"] == arm, "ordinary-memory arm binding")
    state = json.loads(json.dumps(prefix))
    for row, receipt, supplied in zip(rows, receipts, observations, strict=True):
        occurrence = supplied["occurrence_id"]
        require(
            state["pending"] is None and occurrence not in state["receipts"],
            "memory occurrence is not fresh",
        )
        x = memory_raster(supplied)
        state["pending"] = {"id": occurrence, "x": x}
        if arm == "H":
            nearest = sorted(
                enumerate(state["memory"]),
                key=lambda pair: (
                    sum(abs(a - b) for a, b in zip(x, pair[1]["x"], strict=True)),
                    pair[0],
                ),
            )[:3]
            p1 = (1 + sum(item["y"] for _, item in nearest)) / (2 + len(nearest))
            comparisons = slots = len(state["memory"])
        else:
            prototypes = state["prototypes"]
            comparisons = len(prototypes) + int(bool(prototypes))
            distances = [
                sum(abs(a - b) for a, b in zip(x, item["x"], strict=True)) for item in prototypes
            ]
            nearest_id = min(range(len(prototypes)), key=lambda i: (distances[i], i), default=None)
            if nearest_id is None or (distances[nearest_id] > 0.25 and len(prototypes) < 32):
                nearest_id = len(prototypes)
                prototypes.append({"x": x.copy(), "n": 0, "counts": [0, 0]})
            proto = prototypes[nearest_id]
            p1 = (1 + proto["counts"][1]) / (2 + sum(proto["counts"]))
            state["pending"]["prototype"] = nearest_id
            slots = len(prototypes)
        native = None if p1 == 0.5 else int(p1 > 0.5)
        require(
            row["p1"] == p1
            and row["native"] == native
            and row["prototype_comparisons"] == comparisons
            and row["representation_slots"] == slots
            and row["actual_weight_abs_change"] == 0,
            "ordinary-memory prediction/accounting mismatch",
        )
        require(
            row["operational_sha256"] == digest({"wrapper": state, "brain": None})
            and row["live_state_bytes"]
            == len(
                (
                    json.dumps(state, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
                ).encode()
            ),
            "ordinary-memory pending state binding",
        )
        outcome = supplied["outcome"]
        if arm == "H":
            state["memory"] = (state["memory"] + [{"x": x, "y": outcome}])[-32:]
        else:
            proto = state["prototypes"][state["pending"]["prototype"]]
            n = proto["n"]
            proto["x"] = [(a * n + b) / (n + 1) for a, b in zip(proto["x"], x, strict=True)]
            proto["n"] += 1
            proto["counts"][outcome] += 1
        state["receipts"][occurrence] = outcome
        state["pending"] = None
        require(
            receipt["wrapper_sha256"] == digest(state, newline=True)
            and receipt["brain_sha256"] is None
            and receipt["readout_counts_after_receipt"] is None,
            "ordinary-memory receipt state binding",
        )
    require(final == state, "ordinary-memory final state mismatch")


def count_calls(events: list[dict], limits: dict) -> dict:
    stack = []
    intents, returns = Counter(), Counter()
    for row in events:
        kind, phase, number = row["kind"], row["phase"], row["number"]
        require(type(number) is int, "method ordinal type")
        require(
            kind in limits and phase in ("intent", "return"),
            "incomplete/error method event",
        )
        if phase == "intent":
            require(number == intents[kind] + 1 and number <= limits[kind], "method intent ordinal")
            intents[kind] += 1
            stack.append((kind, number))
        else:
            require(stack and stack.pop() == (kind, number), "nested method return order")
            returns[kind] += 1
    require(
        not stack and dict(intents) == dict(returns) == {k: v for k, v in limits.items() if v},
        "method completion totals",
    )
    return dict(returns)


def delta_accounting(edges: list[dict], spikes: list[dict], config: dict) -> tuple[list, int]:
    times: dict[int, list[float]] = {}
    for spike in sorted(spikes, key=lambda row: (row["time_ms"], row["unit_id"])):
        times.setdefault(spike["unit_id"], []).append(spike["time_ms"])
    result = []
    pair_work = 0
    for edge in sorted(edges, key=lambda row: (row["source_id"], row["target_id"])):
        if len(result) >= config["max_updates_per_step"]:
            break
        if not edge["plastic"]:
            continue
        delta = 0.0
        for before in times.get(edge["source_id"], []):
            for after in times.get(edge["target_id"], []):
                pair_work += 1
                lag = after - before
                if lag > 0:
                    delta += math.exp(-lag / config["tau_plus_ms"])
                elif lag < 0:
                    delta -= config["depression_ratio"] * math.exp(lag / config["tau_minus_ms"])
        if delta != 0:
            result.append((f"{edge['source_id']}:{edge['target_id']}", delta))
    return result, pair_work


def current_deltas(edges: list[dict], spikes: list[dict], config: dict) -> list:
    return delta_accounting(edges, spikes, config)[0]


def verify_loaded(record: dict, frozen: dict, dependencies: dict) -> None:
    root = Path(frozen["execution_source_root"])
    stdlib = Path(dependencies["stdlib_path"])
    require(bool(record), "missing loaded module records")
    required = {
        "sparkbrain.v05.brain": "src/sparkbrain/v05/brain.py",
        "sparkbrain.v05.plasticity": "src/sparkbrain/v05/plasticity.py",
        "retention_published_predecessor": "scripts/temporal_reuse_loop_probe.py",
    }
    for name, relative in required.items():
        require(
            record.get(name) == str(root / relative) + ":" + frozen["sources"][relative],
            "required loaded module binding: " + name,
        )
    for name, binding in record.items():
        if name == "sparkbrain" or name.startswith("sparkbrain."):
            filename = binding.rsplit(":", 1)[0]
            relative = "src/" + name.replace(".", "/")
            require(
                filename in (str(root / (relative + ".py")), str(root / relative / "__init__.py")),
                "runtime module name/origin mismatch",
            )
        if binding.startswith("interpreter:"):
            require(
                binding in ("interpreter:None", "interpreter:built-in", "interpreter:frozen"),
                "invalid interpreter module binding",
            )
            continue
        filename, pin = binding.rsplit(":", 1)
        path = Path(filename)
        if path.is_relative_to(root):
            require(
                frozen["sources"].get(str(path.relative_to(root))) == pin, "loaded source binding"
            )
        else:
            require(
                path.is_relative_to(stdlib)
                and dependencies["stdlib_files"].get(str(path.relative_to(stdlib))) == pin,
                "loaded dependency binding",
            )


def verify_audit(
    audit: dict, arm: dict, before_e: dict, weights: dict, fixed_delay_hash: str
) -> None:
    require(audit["pre_eligibility"] == before_e, "eligibility history disconnected")
    expected = {
        key: value * arm["eligibility_decay"]
        for key, value in before_e.items()
        if abs(value * arm["eligibility_decay"]) >= 1e-8
    }
    changes = []
    edges = set()
    for update in audit["updates"]:
        key = update["edge"]
        require(key in weights and key not in edges, "unknown/duplicate updated edge")
        edges.add(key)
        require(
            update["pre_eligibility"] == before_e.get(key, 0)
            and update["decayed_carry"] == expected.get(key, 0)
            and update["current_delta"] != 0,
            "eligibility decomposition",
        )
        value = expected.get(key, 0) + update["current_delta"]
        require(
            update["eligibility_after"] == value and update["weight_before"] == weights[key],
            "weight/eligibility history",
        )
        expected[key] = value
        proposal = weights[key] + arm["learning_rate"] * value
        target = max(-1.4, min(1.4, proposal)) if arm["enable_weight_learning"] else weights[key]
        change = target - weights[key]
        require(
            update["unclipped_proposal"] == proposal
            and update["weight_expected"] == target
            and update["actual_delta_weight"] == change
            and update["weight_write_enabled"] is arm["enable_weight_learning"]
            and update["clipped"] == bool(arm["enable_weight_learning"] and target != proposal),
            "actual weight proposal/write/clipping mismatch",
        )
        changes.append(change)
        weights[key] = target
    require(
        audit["post_eligibility"] == expected
        and audit["actual_weight_abs_change"] == math.fsum(abs(v) for v in changes)
        and audit["actual_weight_signed_change"] == math.fsum(changes)
        and audit["changed_weights"] == sum(v != 0 for v in changes),
        "apply totals",
    )
    require(
        audit["clipped_weights"] == sum(u["clipped"] for u in audit["updates"]),
        "clipping total mismatch",
    )
    require(
        audit["delays_unchanged"] is True
        and audit["delay_map_sha256"] == fixed_delay_hash
        and audit["extra_apply_calls"] == 0
        and audit["eligible_edge_work"] == len(edges),
        "delay/apply work mismatch",
    )


def verify_prediction(row: dict, supplied: dict, readout: dict) -> None:
    raw = row["raw_result"]
    usable = [a for a in raw["assembly_activations"] if a["mature"] and not a["suppressed"]]
    selected = max(
        usable, key=lambda a: (a["similarity"], a["episode_count"], a["assembly_id"]), default=None
    )
    aid = selected["assembly_id"] if selected else None
    counts = readout.get(aid, {}) if aid else {}
    total = sum(counts.values())
    label = max(sorted(counts), key=lambda item: counts[item]) if total > 0 else None
    native = int(label) if label is not None else None
    expected_prediction = {
        "assembly_id": aid,
        "value": label,
        "confidence": counts[label] / total if label is not None else 0.0,
    }
    require(
        row["assembly_id"] == aid
        and row["mature"] == bool(selected)
        and row["native"] == native
        and raw["prediction"] == expected_prediction,
        "native/selection/readout mismatch",
    )
    require(
        row["p1"] == (1 + counts.get("1", 0)) / (2 + counts.get("0", 0) + counts.get("1", 0)),
        "probability/readout mismatch",
    )
    require(
        raw["raw_pulses"] == sorted(supplied["pulses"], key=lambda p: (p["time_ms"], p["channel"]))
        and raw["end_ms"] == supplied["start_ms"] + 72,
        "raw model input/time mismatch",
    )


def first_observables(row: dict) -> dict:
    raw = row["raw_result"]
    return {
        "p1": row["p1"],
        "native": row["native"],
        "assembly_id": row["assembly_id"],
        "mature": row["mature"],
        "emitted_pulses": raw["emitted_pulses"],
        "spikes": raw["v04_result"]["spikes"],
        "patterns": raw["patterns"],
        "activations": raw["assembly_activations"],
        "prediction": raw["prediction"],
    }


def pattern_score(left: dict, right: dict) -> float:
    """Recalculate retained-pattern similarity from data, without a runtime import."""
    a, b = left["ordered_units"], right["ordered_units"]
    previous = list(range(len(b) + 1))
    for i, unit in enumerate(a, start=1):
        current = [i]
        for j, other in enumerate(b, start=1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (unit != other)))
        previous = current
    edit = 1.0 - previous[-1] / max(len(a), len(b)) if a or b else 1.0
    units_a, units_b = set(left["unit_ids"]), set(right["unit_ids"])
    overlap = len(units_a & units_b) / max(1, len(units_a | units_b))
    if not units_a and not units_b:
        overlap = 1.0
    bins_a, bins_b = left["relative_bins"], right["relative_bins"]
    timing = 0.0
    if not bins_a and not bins_b:
        timing = 1.0
    elif bins_a and bins_b:
        if len(bins_a) == len(bins_b):
            error = sum(abs(x - y) for x, y in zip(bins_a, bins_b, strict=True)) / len(bins_a)
            timing = math.exp(-error / 2.0)
        else:
            short, long = (left, right) if len(a) < len(b) else (right, left)
            if len(short["ordered_units"]) >= 2:
                for indices in combinations(
                    range(len(long["ordered_units"])), len(short["ordered_units"])
                ):
                    if [long["ordered_units"][i] for i in indices] != short["ordered_units"]:
                        continue
                    selected = [long["relative_bins"][i] for i in indices]
                    selected = [value - selected[0] for value in selected]
                    short_bins = [
                        value - short["relative_bins"][0] for value in short["relative_bins"]
                    ]
                    error = sum(
                        abs(x - y) for x, y in zip(selected, short_bins, strict=True)
                    ) / len(short_bins)
                    timing = max(timing, math.exp(-error / 4.0))
    return 0.55 * edit + 0.25 * overlap + 0.20 * timing


def verify_prototype_history(
    rows: list[dict], prefix: dict, final: dict, brain_config: dict
) -> None:
    """Bind fixed prototypes and assembly bookkeeping to retained creation patterns.

    This recalculates data-level matching/allocation/pruning only. It does not
    regenerate spikes or establish that the supplied patterns came from a run.
    """
    state = json.loads(json.dumps(prefix))
    config, candidates = state["config"], state["candidates"]
    suppressed = set(state["suppressed"])
    for row in rows:
        activations = []
        patterns = row["raw_result"]["patterns"] if brain_config["enable_assembly"] else []
        for pattern in patterns:
            require(
                all(
                    key in pattern
                    for key in (
                        "pattern_id",
                        "spike_count",
                        "end_ms",
                        "ordered_units",
                        "relative_bins",
                        "unit_ids",
                    )
                ),
                "prototype creation pattern incomplete",
            )
            if pattern["spike_count"] < brain_config["min_pattern_spikes"]:
                continue
            scored = [
                (pattern_score(candidate["prototype"], pattern), aid)
                for aid, candidate in candidates.items()
            ]
            similarity, aid = (
                min(scored, key=lambda pair: (-pair[0], pair[1])) if scored else (0, None)
            )
            time_ms = pattern["end_ms"]
            if aid is None or similarity < config["similarity_threshold"]:
                # Pruning is permitted only on a failed match at capacity, at
                # that pattern's time. Staleness alone never removes a row.
                if len(candidates) >= config["max_candidates"]:
                    removable = [
                        key
                        for key, candidate in candidates.items()
                        if candidate["episode_count"] <= config["immature_stale_episodes"]
                        and time_ms - candidate["last_seen_ms"] > config["stale_after_ms"]
                    ]
                    for key in removable:
                        del candidates[key]
                        suppressed.discard(key)
                if len(candidates) >= config["max_candidates"]:
                    continue
                aid = f"assembly-{state['next_id']:04d}"
                state["next_id"] += 1
                require(aid not in candidates, "assembly identifier reused")
                candidate = {
                    "assembly_id": aid,
                    "prototype": json.loads(json.dumps(pattern)),
                    "occurrences": 1,
                    "episode_ids": [row["occurrence_id"]],
                    "episode_count": 1,
                    "first_seen_ms": time_ms,
                    "last_seen_ms": time_ms,
                    "similarity_sum": 1.0,
                    "mean_similarity": 1.0,
                }
                candidates[aid] = candidate
                similarity = 1.0
            else:
                candidate = candidates[aid]
                candidate["occurrences"] += 1
                candidate["episode_ids"] = sorted(
                    set(candidate["episode_ids"]) | {row["occurrence_id"]}
                )
                candidate["episode_count"] = len(candidate["episode_ids"])
                candidate["last_seen_ms"] = time_ms
                candidate["similarity_sum"] += similarity
                candidate["mean_similarity"] = (
                    candidate["similarity_sum"] / candidate["occurrences"]
                )
            activations.append(
                {
                    "assembly_id": aid,
                    "pattern_id": pattern["pattern_id"],
                    "time_ms": time_ms,
                    "similarity": similarity,
                    "occurrences": candidate["occurrences"],
                    "episode_count": candidate["episode_count"],
                    "mature": candidate["episode_count"] >= config["mature_episodes"],
                    "unit_ids": candidate["prototype"]["unit_ids"],
                    "suppressed": aid in suppressed,
                }
            )
        require(
            row["raw_result"]["assembly_activations"] == activations,
            "assembly activation/prototype history mismatch",
        )
        require(
            row["candidate_prototypes"] == {aid: c["prototype"] for aid, c in candidates.items()},
            "candidate prototype history mismatch",
        )
    state["suppressed"] = sorted(suppressed)
    require(final == state, "final assembly/prototype history mismatch")


def verify(
    output: Path,
    freeze: Path,
    expected_manifest: str,
    expected_commit: str,
    expected_record_hashes: dict,
) -> dict:
    # Caller pins must come from independently read-back reviewed publication records.
    # The retained run's own manifest is never accepted as its authority.
    require(len(expected_manifest) == 64 and len(expected_commit) == 40, "explicit authority pins")
    require(
        isinstance(expected_record_hashes, dict)
        and set(expected_record_hashes) == {"review", "publication", "approval"}
        and all(
            type(value) is str
            and len(value) == 64
            and all(char in "0123456789abcdef" for char in value)
            for value in expected_record_hashes.values()
        ),
        "independent authority record pins required",
    )
    require(sha(freeze / "manifest.json") == expected_manifest, "authoritative freeze pin")
    frozen = read(freeze / "manifest.json")
    require(
        sha(freeze / "dependencies.json") == frozen["generated"]["dependencies.json"],
        "dependency authority pin",
    )
    dependencies = read(freeze / "dependencies.json")
    verify_audit_interpreter(dependencies)
    for name, value in frozen["sources"].items():
        require(sha(ROOT / name) == value, "frozen audit/source mismatch: " + name)
    for name, value in PINS.items():
        require(sha(PREPARATION / name) == value, "published input authority pin")
    protocol_path = ROOT / "protocols/plasticity_retention_bounded_v1.json"
    require(sha(protocol_path) == PROTOCOL_SHA, "published protocol authority pin")
    protocol, jobs = read(protocol_path), read(PREPARATION / "jobs.json")["jobs"]
    inputs, prefixes = (
        read(PREPARATION / "inputs.json")["streams"],
        read(PREPARATION / "prefix_sources.json")["prefixes"],
    )
    require(not any(p.is_symlink() for p in output.rglob("*")), "retained output symlink")
    terminal, gate = read(output / "result.json"), read(output / "execution-gate.json")
    attempt = frozen.get("attempt_id")
    prior_pairs = frozen.get("previous_attempt", {}).get("audited_model_pairs")
    allocation = frozen.get("combined_model_allocation_ceiling")
    require(
        type(attempt) is str
        and bool(attempt)
        and type(prior_pairs) is int
        and prior_pairs == 0
        and type(allocation) is int
        and allocation == 768,
        "pinned prospective attempt accounting",
    )
    require(
        type(terminal.get("attempt_id")) is str
        and terminal["attempt_id"] == attempt
        and type(terminal.get("prior_attempt_audited_model_pairs")) is int
        and terminal["prior_attempt_audited_model_pairs"] == prior_pairs,
        "terminal attempt/accounting mismatch",
    )
    authority_paths, authority_hashes = verify_retained_records(
        output,
        gate,
        expected_commit,
        expected_manifest,
        frozen["planned_output"],
        expected_record_hashes,
    )
    require(
        terminal["status"] == "complete"
        and terminal["jobs_completed"] == 26
        and terminal["pairs_completed"] == terminal["reserved_pairs"] == 768
        and terminal["scientific_credit"] == 0
        and not terminal["measurement_failed"],
        "run incomplete; preserve partial evidence, do not score",
    )
    require(
        all(
            type(terminal[key]) in (float, int)
            and math.isfinite(terminal[key])
            and terminal[key] >= 0
            for key in ("aggregate_cpu_seconds", "wall_seconds")
        ),
        "invalid aggregate resource measurement",
    )
    require(
        terminal["aggregate_cpu_seconds"] + 2 <= 360 and terminal["wall_seconds"] + 5 <= 480,
        "aggregate resource ceiling",
    )
    members = {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()}
    inventory = read(output / "file-manifest.json")
    require(
        set(members) == set(inventory) | {"file-manifest.json", "result.json"}, "raw file inventory"
    )
    require(all(members[name] == value for name, value in inventory.items()), "raw file digest")
    require(
        sum(p.stat().st_size for p in output.rglob("*") if p.is_file()) <= 256 * 1024**2,
        "output total ceiling",
    )
    terminal_paths = {"result.json", "job-costs.jsonl"} | {
        "jobs/" + job["job_id"] + "/result.json" for job in jobs
    }
    require(
        sum((output / name).stat().st_size for name in members if name not in terminal_paths)
        <= 252 * 1024**2,
        "ordinary output ceiling",
    )
    require(
        (output / "result.json").stat().st_size + (output / "job-costs.jsonl").stat().st_size
        <= 524288,
        "driver terminal allowance",
    )
    require(
        all(
            (output / "jobs" / job["job_id"] / "result.json").stat().st_size <= 131072
            for job in jobs
        ),
        "worker terminal allowance",
    )
    require(read(output / "job-plan.json")["jobs"] == jobs, "job plan changed")
    require(
        {p.name for p in (output / "jobs").iterdir()} == {j["job_id"] for j in jobs},
        "job inventory",
    )
    cumulative = 0
    expected_reservations = []
    for job in jobs:
        cumulative += job["pairs"]
        expected_reservations.append(
            {"job_id": job["job_id"], "pairs": job["pairs"], "cumulative_pairs": cumulative}
        )
    require(lines(output / "reservations.jsonl") == expected_reservations, "reservations changed")
    costs = lines(output / "job-costs.jsonl")
    require(costs == terminal["job_costs"] and len(costs) == 26, "job cost ledger")
    require(
        terminal["aggregate_cpu_seconds"] >= math.fsum(c["worker_cpu_seconds"] for c in costs),
        "aggregate CPU omits worker costs",
    )
    groups: dict[str, dict] = {}
    totals = Counter()
    memory_rows_reconstructed = 0
    apply_rows_recomputed = 0
    for job, cost in zip(jobs, costs, strict=True):
        work = output / "jobs" / job["job_id"]
        envelope, result = read(work / "job.json"), read(work / "result.json")
        require(envelope["plan"] == job and envelope["binding"] == gate, "job source/input binding")
        require(
            envelope.get("record_paths") == authority_paths
            and envelope.get("record_sha256") == authority_hashes,
            "job retained authority binding",
        )
        require(
            result["job_sha256"] == digest(envelope)
            and result["status"] == "complete"
            and result["completed_pairs"] == job["pairs"],
            "job result identity",
        )
        require(
            cost["job_id"] == job["job_id"]
            and cost["exit_code"] == 0
            and not cost["failure"]
            and cost["worker_cpu_seconds"] <= job["cpu_seconds"]
            and cost["wall_seconds_before_cost"] + 0.1 <= job["wall_seconds"]
            and all(v <= 65536 for v in cost["capture_consumed_bytes"].values())
            and all(v == 0 for v in cost["known_discarded_bytes"].values())
            and cost["unread_pipe_bytes"] == 0,
            "worker resource/capture failure",
        )
        verify_loaded(read(work / "loaded-before-construction.json"), frozen, dependencies)
        verify_loaded(read(work / "loaded-after-methods.json"), frozen, dependencies)
        require(
            cost["timed_out"] is False
            and all(
                type(cost[key]) in (float, int) and math.isfinite(cost[key]) and cost[key] >= 0
                for key in (
                    "worker_cpu_seconds",
                    "driver_cpu_seconds",
                    "wall_seconds_before_cost",
                    "worker_peak_rss_kib",
                    "driver_peak_rss_kib",
                )
            ),
            "invalid worker cost",
        )
        for channel in ("stdout", "stderr"):
            require(
                cost["capture_retained_bytes"][channel]
                == cost["capture_consumed_bytes"][channel]
                == (work / (channel + ".bin")).stat().st_size,
                "capture size mismatch",
            )
        v05, n = job["family"] == "v05", job["pairs"]
        limits = {
            "wrapper_load": 1,
            "wrapper_init": 1,
            "v05_init": 2 if v05 else 0,
            "native_load": int(v05),
            "predict": n,
            "outcome": n,
            "v05_episode": n if v05 else 0,
            "apply": n if v05 else 0,
            "v05_outcome": n if v05 else 0,
        }
        calls = count_calls(lines(work / "calls.jsonl"), limits)
        require(
            result["calls"]["returns"] == result["calls"]["intents"] == calls
            and not result["calls"]["errors"]
            and not result["calls"]["observation_failed"],
            "terminal call counts",
        )
        totals.update(calls)
        prefix = output / "prefixes" / job["prefix"]
        for member in prefixes[job["prefix"]]["checkpoint_members"]:
            require(
                sha(prefix / Path(member).name) == prefixes[job["prefix"]]["files_sha256"][member],
                "published prefix bytes changed",
            )
        rows, receipts = lines(work / "predictions.jsonl"), lines(work / "receipts.jsonl")
        require(len(rows) == len(receipts) == n, "row/receipt completeness")
        for index, (row, receipt, supplied) in enumerate(
            zip(rows, receipts, inputs[job["stream"]], strict=True)
        ):
            obs = {k: supplied[k] for k in ("occurrence_id", "start_ms", "pulses")}
            require(
                row["index"] == receipt["index"] == index
                and row["occurrence_id"] == receipt["occurrence_id"] == supplied["occurrence_id"]
                and row["outcome"] == receipt["outcome"] == supplied["outcome"]
                and row["input_sha256"] == digest(obs)
                and row["query_time_ms"] == supplied["start_ms"] + 72
                and row["receipt_time_ms"] == supplied["receipt_time_ms"],
                "paired raw input binding",
            )
        final_state = read(work / "final-state.json")
        final_wrapper = final_state["wrapper"]
        prefix_wrapper = read(prefix / "wrapper.json")
        expected_receipts = dict(prefix_wrapper["receipts"])
        expected_receipts.update({r["occurrence_id"]: r["outcome"] for r in rows})
        require(
            final_wrapper["pending"] is None
            and final_wrapper["receipts"] == expected_receipts
            and receipts[-1]["wrapper_sha256"] == digest(final_wrapper, newline=True),
            "final wrapper/receipt closure",
        )
        if not v05:
            require(final_state["brain"] is None, "ordinary-memory final brain must be absent")
            verify_memory_history(
                job["arm"], rows, receipts, inputs[job["stream"]], prefix_wrapper, final_wrapper
            )
            memory_rows_reconstructed += len(rows)
        if v05:
            require(
                receipts[-1]["brain_sha256"] == digest(final_state["brain"], newline=True),
                "final brain receipt hash",
            )
            payload = read(prefix / "brain.json")["payload"]
            config_record = read(work / "configuration.json")
            expected_state = json.loads(json.dumps(payload))
            arm = protocol["arms"][job["arm"]]
            expected_state["config"].update(
                enable_weight_learning=arm["enable_weight_learning"], enable_delay_learning=False
            )
            expected_state["plasticity"]["config"].update(arm, enable_delay_learning=False)
            require(
                config_record["before_sha256"] == digest(payload, newline=True)
                and config_record["after_sha256"] == digest(expected_state, newline=True)
                and config_record["brain_config"] == expected_state["config"]
                and config_record["plasticity_config"] == expected_state["plasticity"]["config"],
                "configuration intervention binding",
            )
            verify_prototype_history(
                rows,
                payload["assemblies"],
                final_state["brain"]["assemblies"],
                expected_state["config"],
            )
            edges = payload["base"]["payload"]["field"]["connections"]
            weights = {f"{e['source_id']}:{e['target_id']}": e["weight"] for e in edges}
            delays = {f"{e['source_id']}:{e['target_id']}": e["delay_ms"] for e in edges}
            readout = payload["predictor"]["counts"]
            for row, receipt in zip(rows, receipts, strict=True):
                supplied = inputs[job["stream"]][row["index"]]
                verify_prediction(row, supplied, readout)
                require(
                    row["readout_counts_before_receipt"] == readout, "readout history disconnected"
                )
                readout = json.loads(json.dumps(readout))
                selected = row["assembly_id"]
                if selected is not None:
                    counts = readout.setdefault(selected, {})
                    label = str(row["outcome"])
                    counts[label] = counts.get(label, 0) + 1
                require(
                    receipt["readout_counts_after_receipt"] == readout, "readout receipt update"
                )
            require(final_state["brain"]["predictor"]["counts"] == readout, "final readout closure")
            eligibility = payload["plasticity"]["eligibility"]
            require(payload["plasticity"]["reward_trace"] == 1, "reward assumption")
            audits = lines(work / "apply.jsonl")
            require(len(audits) == n, "apply accounting completeness")
            for index, audit in enumerate(audits):
                require(
                    audit["index"] == index
                    and audit["actual_weight_abs_change"]
                    == rows[index]["actual_weight_abs_change"],
                    "apply row identity",
                )
                require(
                    [(u["edge"], u["current_delta"]) for u in audit["updates"]]
                    == current_deltas(
                        edges,
                        rows[index]["raw_result"]["v04_result"]["spikes"],
                        payload["plasticity"]["config"],
                    ),
                    "current STDP/spike mismatch",
                )
                require(
                    audit["observer_pair_evaluations"]
                    == delta_accounting(
                        edges,
                        rows[index]["raw_result"]["v04_result"]["spikes"],
                        payload["plasticity"]["config"],
                    )[1],
                    "observer pair-work mismatch",
                )
                verify_audit(
                    audit,
                    protocol["arms"][job["arm"]],
                    eligibility,
                    weights,
                    digest(delays, newline=True),
                )
                eligibility = audit["post_eligibility"]
            apply_rows_recomputed += len(audits)
            final = read(work / "final-state.json")["brain"]
            require(
                final["config"] == expected_state["config"]
                and final["plasticity"]["config"] == expected_state["plasticity"]["config"],
                "final configuration changed",
            )
            final_edges = final["base"]["payload"]["field"]["connections"]
            require(
                {f"{e['source_id']}:{e['target_id']}": e["weight"] for e in final_edges} == weights
                and {f"{e['source_id']}:{e['target_id']}": e["delay_ms"] for e in final_edges}
                == delays
                and final["plasticity"]["eligibility"] == eligibility
                and final["plasticity"]["reward_trace"] == 1,
                "final plasticity state mismatch",
            )
        seed = job["stream"].split("-")[0]
        groups.setdefault(seed, {}).setdefault(job["condition"], {})[job["arm"]] = rows
    # Load only the pure scorer; source bytes were independently pinned above.
    spec = importlib.util.spec_from_file_location(
        "retention_data_scorer", ROOT / "scripts/plasticity_retention_contract.py"
    )
    require(spec is not None and spec.loader is not None, "scorer unavailable")
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    for conditions in groups.values():
        for condition, arms in conditions.items():
            firsts = [
                first_observables(arms[arm][0])
                for arm in protocol["conditions"][condition]["v05_arms"]
            ]
            require(all(first == firsts[0] for first in firsts), "first-suffix observable mismatch")
    scores = {seed: scorer.evaluate_fixture(rows, protocol) for seed, rows in groups.items()}
    require(scores == read(output / "scores.json"), "raw-to-score mismatch")
    for seed, conditions in groups.items():
        for condition, arms in conditions.items():
            for arm, rows in arms.items():
                measured = scores[seed]["metrics"][condition][arm]
                require(
                    measured["brier"]
                    == math.fsum((row["p1"] - row["outcome"]) ** 2 for row in rows) / len(rows)
                    and measured["correct"] == sum(row["native"] == row["outcome"] for row in rows),
                    "independent metric arithmetic",
                )
    require(
        terminal["bounded_gate"] == all(score["bounded_gate"] for score in scores.values()),
        "gate mismatch",
    )
    return {
        "valid_completion": True,
        "attempt_id": attempt,
        "prior_attempt_audited_model_pairs": prior_pairs,
        "combined_model_allocation_ceiling": allocation,
        "pairs": 768,
        "calls": dict(totals),
        "runtime_model_method_calls_during_audit": 0,
        "ordinary_memory_rows_reconstructed": memory_rows_reconstructed,
        "v05_apply_rows_recomputed": apply_rows_recomputed,
        "manifest_sha256": expected_manifest,
        "source_commit": expected_commit,
        "authority_record_sha256": expected_record_hashes,
        "scope": "data/source integrity audit; not rerun fidelity or scientific promotion; "
        "retained authority statements require independent authenticity verification",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--expected-source-commit", required=True)
    for kind in ("review", "publication", "approval"):
        parser.add_argument(
            "--expected-" + kind + "-sha256",
            required=True,
            help="SHA-256 of the independently verified original "
            + kind
            + " record; never obtain this authority pin from the retained package",
        )
    args = parser.parse_args()
    print(
        json.dumps(
            verify(
                args.output,
                args.freeze,
                args.expected_manifest_sha256,
                args.expected_source_commit,
                {
                    kind: getattr(args, "expected_" + kind + "_sha256")
                    for kind in ("review", "publication", "approval")
                },
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
