from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from sparkbrain.v04.brain import IntegratedV04Brain, V04BrainConfig
from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v04.transduction import TemporalExpectationTracker
from sparkbrain.v04.worlds import noisy_motif_stream, repetition_train

CONTRACT_PATH = Path(
    "analysis/architecture/temporal_batch_partition_cycle1_contract_20260920.json"
)
ARMS = ("WHOLE_BATCH", "MIDPOINT_TWO_BATCH", "EVENT_TIME_CAUSAL")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True).strip()


def pulse_rows(pulses: Iterable[SignalPulse]) -> list[dict[str, Any]]:
    return [pulse.as_dict() for pulse in pulses]


def pulse_key(pulse: SignalPulse) -> tuple[float, str, float, int]:
    return (pulse.time_ms, pulse.channel, pulse.magnitude, pulse.polarity)


def compact_pulse(pulse: SignalPulse) -> dict[str, Any]:
    return {
        "time_ms": pulse.time_ms,
        "channel": pulse.channel,
        "magnitude": pulse.magnitude,
        "polarity": pulse.polarity,
    }


def build_timelines() -> dict[str, tuple[SignalPulse, ...]]:
    return {
        "repetition_train_defaults": repetition_train(),
        "noisy_motif_stream_defaults": noisy_motif_stream(),
    }


def midpoint_boundary(pulses: tuple[SignalPulse, ...]) -> int:
    boundary = len(pulses) // 2
    while (
        0 < boundary < len(pulses)
        and pulses[boundary - 1].time_ms == pulses[boundary].time_ms
    ):
        boundary += 1
    if boundary <= 0 or boundary >= len(pulses):
        raise RuntimeError("midpoint partition failed to produce two non-empty batches")
    return boundary


def tracker_from_contract(contract: dict[str, Any]) -> TemporalExpectationTracker:
    semantics = contract["expectation_semantics"]
    return TemporalExpectationTracker(
        tolerance_fraction=float(semantics["tolerance_fraction"]),
        min_observations=int(semantics["min_observations"]),
        alpha=float(semantics["alpha"]),
    )


def tracker_state(tracker: TemporalExpectationTracker) -> dict[str, Any]:
    return {
        "last_time": dict(sorted(tracker.last_time.items())),
        "interval": dict(sorted(tracker.interval.items())),
        "observations": dict(sorted(tracker.observations.items())),
        "emitted_deadline": dict(sorted(tracker.emitted_deadline.items())),
    }


def derive_schedule(
    pulses: tuple[SignalPulse, ...],
    arm: str,
    final_horizon: float,
    contract: dict[str, Any],
) -> tuple[tuple[SignalPulse, ...], dict[str, Any], dict[str, Any]]:
    tracker = tracker_from_contract(contract)
    omissions: list[SignalPulse] = []

    if arm == "WHOLE_BATCH":
        for pulse in pulses:
            tracker.observe(pulse)
        omissions.extend(tracker.poll(until_ms=final_horizon))
        partition = {
            "arm": arm,
            "batches": [list(range(len(pulses)))],
            "poll_boundaries_ms": [final_horizon],
        }
    elif arm == "MIDPOINT_TWO_BATCH":
        boundary = midpoint_boundary(pulses)
        first = pulses[:boundary]
        second = pulses[boundary:]
        for pulse in first:
            tracker.observe(pulse)
        first_poll = first[-1].time_ms
        omissions.extend(tracker.poll(until_ms=first_poll))
        for pulse in second:
            tracker.observe(pulse)
        omissions.extend(tracker.poll(until_ms=final_horizon))
        partition = {
            "arm": arm,
            "boundary_index": boundary,
            "batches": [list(range(boundary)), list(range(boundary, len(pulses)))],
            "poll_boundaries_ms": [first_poll, final_horizon],
        }
    elif arm == "EVENT_TIME_CAUSAL":
        grouped: dict[float, list[SignalPulse]] = defaultdict(list)
        for pulse in pulses:
            grouped[pulse.time_ms].append(pulse)
        groups: list[dict[str, Any]] = []
        for time_ms in sorted(grouped):
            omissions.extend(tracker.poll(until_ms=time_ms))
            rows = sorted(grouped[time_ms], key=lambda row: row.channel)
            for pulse in rows:
                tracker.observe(pulse)
            groups.append(
                {
                    "time_ms": time_ms,
                    "channels": [pulse.channel for pulse in rows],
                }
            )
        omissions.extend(tracker.poll(until_ms=final_horizon))
        partition = {
            "arm": arm,
            "timestamp_groups": groups,
            "poll_before_each_external_timestamp": True,
            "final_poll_ms": final_horizon,
        }
    else:
        raise RuntimeError(f"unknown arm: {arm}")

    ordered = tuple(sorted(omissions, key=lambda row: (row.time_ms, row.channel)))
    return ordered, tracker_state(tracker), partition


def replay(
    external: tuple[SignalPulse, ...],
    omissions: tuple[SignalPulse, ...],
    final_horizon: float,
    contract: dict[str, Any],
) -> dict[str, Any]:
    replay_cfg = contract["isolation_replay"]["brain_config"]
    brain = IntegratedV04Brain(
        V04BrainConfig(
            topology_seed=int(replay_cfg["topology_seed"]),
            enable_expectations=bool(replay_cfg["enable_expectations"]),
            enable_plasticity=bool(replay_cfg["enable_plasticity"]),
        )
    )
    combined = tuple(
        sorted(external + omissions, key=lambda row: (row.time_ms, row.channel))
    )
    last_time = combined[-1].time_ms if combined else 0.0
    settle_ms = final_horizon - last_time
    if settle_ms < 0:
        raise RuntimeError("replay pulse exceeds fixed final horizon")
    result = brain.ingest_pulses(combined, settle_ms=settle_ms)
    observable = {
        "spikes": [row.as_dict() for row in result.spikes],
        "bursts": [row.as_dict() for row in result.bursts],
        "cascades": [row.as_dict() for row in result.cascades],
        "ignitions": [row.as_dict() for row in result.ignitions],
        "action": result.action,
        "field_state_hash": result.field_state_hash,
        "trace_hash": result.trace_hash,
    }
    observable["sha256"] = digest(observable)
    return observable


def symmetric_difference(
    current: tuple[SignalPulse, ...],
    causal: tuple[SignalPulse, ...],
) -> dict[str, Any]:
    current_map = {pulse_key(pulse): compact_pulse(pulse) for pulse in current}
    causal_map = {pulse_key(pulse): compact_pulse(pulse) for pulse in causal}
    current_only = sorted(set(current_map) - set(causal_map))
    causal_only = sorted(set(causal_map) - set(current_map))
    return {
        "arm_only": [current_map[key] for key in current_only],
        "event_time_causal_only": [causal_map[key] for key in causal_only],
    }


def verify_contract(contract: dict[str, Any]) -> dict[str, Any]:
    if contract["candidate_id"] != "CAND-TEMPORAL-BATCH-PARTITION-01":
        raise RuntimeError("candidate binding mismatch")
    if contract["research_layer"] != "ARCHITECTURE_STUDY":
        raise RuntimeError("research layer mismatch")
    if contract["evidentiary_status"] != "NON_EVIDENTIARY":
        raise RuntimeError("evidentiary status mismatch")
    if contract["analyst_authority"] != "862dd62cdce58f06e5c782b4b54212d93e40212e":
        raise RuntimeError("Analyst authority mismatch")
    if not contract["data_authority"]["official_test_forbidden"]:
        raise RuntimeError("official TEST must remain forbidden")
    if float(contract["final_horizon"]["offset_ms"]) != 35.0:
        raise RuntimeError("final horizon mismatch")
    if tuple(contract["partition_arms"]) != ARMS:
        raise RuntimeError("partition arm binding mismatch")

    for path, expected in contract["source_binding"].items():
        if path == "main_sha":
            continue
        observed = git_blob(path)
        if observed != expected:
            raise RuntimeError(f"source blob mismatch for {path}: {observed} != {expected}")

    timelines = build_timelines()
    observed_timelines: dict[str, Any] = {}
    for family, pulses in timelines.items():
        fixed = contract["timeline_families"][family]
        rows = pulse_rows(pulses)
        observed_digest = digest(rows)
        if len(pulses) != int(fixed["expected_pulse_count"]):
            raise RuntimeError(f"pulse count mismatch for {family}")
        if observed_digest != fixed["expected_timeline_sha256"]:
            raise RuntimeError(
                f"timeline digest mismatch for {family}: "
                f"{observed_digest} != {fixed['expected_timeline_sha256']}"
            )
        observed_timelines[family] = {
            "pulse_count": len(pulses),
            "sha256": observed_digest,
            "last_external_time_ms": pulses[-1].time_ms,
            "midpoint_boundary": midpoint_boundary(pulses),
        }

    return {
        "candidate_id": contract["candidate_id"],
        "contract_sha256": digest(contract),
        "main_sha": contract["source_binding"]["main_sha"],
        "timelines": observed_timelines,
    }


def write_json_fsync(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_jsonl_fsync(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(canonical(row) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_family[row["family"]].append(row)

    family_summary: dict[str, Any] = {}
    unexpected_downstream_without_schedule = False
    any_schedule_difference = False
    functional_difference = False

    for family, family_rows in sorted(by_family.items()):
        if {row["arm"] for row in family_rows} != set(ARMS):
            raise RuntimeError(f"incomplete arm set for {family}")
        schedule_digests = {row["omission_schedule_sha256"] for row in family_rows}
        replay_digests = {row["replay_observable_sha256"] for row in family_rows}
        schedule_differs = len(schedule_digests) > 1
        replay_differs = len(replay_digests) > 1
        any_schedule_difference = any_schedule_difference or schedule_differs
        functional_difference = functional_difference or (schedule_differs and replay_differs)
        unexpected_downstream_without_schedule = (
            unexpected_downstream_without_schedule
            or (not schedule_differs and replay_differs)
        )
        family_summary[family] = {
            "schedule_differs_across_arms": schedule_differs,
            "replay_differs_across_arms": replay_differs,
            "omission_schedule_sha256_by_arm": {
                row["arm"]: row["omission_schedule_sha256"] for row in family_rows
            },
            "replay_observable_sha256_by_arm": {
                row["arm"]: row["replay_observable_sha256"] for row in family_rows
            },
        }

    if unexpected_downstream_without_schedule:
        outcome = "MIXED"
    elif not any_schedule_difference:
        if all(not row["replay_differs_across_arms"] for row in family_summary.values()):
            outcome = "NO_BATCH_PARTITION_EFFECT"
        else:
            outcome = "MIXED"
    elif functional_difference:
        outcome = "FUNCTIONAL_BATCH_PARTITION_EFFECT"
    else:
        outcome = "SCHEDULER_ONLY_PARTITION_EFFECT"

    return {
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_STUDY",
        "mapped_outcome": outcome,
        "family_summary": family_summary,
        "raw_row_count": len(rows),
    }


def run(output_dir: Path) -> None:
    contract = load_contract()
    preflight = verify_contract(contract)
    timelines = build_timelines()
    rows: list[dict[str, Any]] = []

    for family, external in timelines.items():
        final_horizon = external[-1].time_ms + float(contract["final_horizon"]["offset_ms"])
        schedules: dict[str, tuple[SignalPulse, ...]] = {}
        states: dict[str, dict[str, Any]] = {}
        partitions: dict[str, dict[str, Any]] = {}
        for arm in ARMS:
            schedule, state, partition = derive_schedule(
                external,
                arm,
                final_horizon,
                contract,
            )
            schedules[arm] = schedule
            states[arm] = state
            partitions[arm] = partition

        causal = schedules["EVENT_TIME_CAUSAL"]
        for arm in ARMS:
            observable = replay(external, schedules[arm], final_horizon, contract)
            omissions = [compact_pulse(pulse) for pulse in schedules[arm]]
            row = {
                "family": family,
                "arm": arm,
                "external_timeline_sha256": digest(pulse_rows(external)),
                "partition_definition": partitions[arm],
                "final_horizon_ms": final_horizon,
                "omission_pulses": omissions,
                "omission_schedule_sha256": digest(omissions),
                "final_expectation_state": states[arm],
                "symmetric_difference_from_event_time_causal": symmetric_difference(
                    schedules[arm],
                    causal,
                ),
                "replay_spikes": observable["spikes"],
                "replay_bursts": observable["bursts"],
                "replay_cascades": observable["cascades"],
                "replay_ignitions": observable["ignitions"],
                "replay_action": observable["action"],
                "replay_field_state_hash": observable["field_state_hash"],
                "replay_trace_hash": observable["trace_hash"],
                "replay_observable_sha256": observable["sha256"],
            }
            rows.append(row)

    metadata = {
        "candidate_id": contract["candidate_id"],
        "research_layer": contract["research_layer"],
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_STUDY",
        "analyst_authority": contract["analyst_authority"],
        "source_main_sha": contract["source_binding"]["main_sha"],
        "contract_sha256": preflight["contract_sha256"],
        "raw_before_interpretation": True,
        "official_test_opened": False,
        "formal_identity": None,
        "started": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_fsync(output_dir / "metadata.json", metadata)
    write_jsonl_fsync(output_dir / "raw.jsonl", rows)

    persisted_rows = load_jsonl(output_dir / "raw.jsonl")
    summary = summarize(persisted_rows)
    summary["raw_sha256"] = hashlib.sha256(
        (output_dir / "raw.jsonl").read_bytes()
    ).hexdigest()
    write_json_fsync(output_dir / "summary.json", summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    contract = load_contract()
    preflight = verify_contract(contract)
    if args.preflight_only:
        print(json.dumps(preflight, indent=2, sort_keys=True))
    else:
        if args.output_dir is None:
            parser.error("--output-dir is required unless --preflight-only is used")
        run(args.output_dir)
