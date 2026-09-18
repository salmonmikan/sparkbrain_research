from __future__ import annotations

import argparse
import heapq
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from .engine import SparkBrain
from .model import BrainConfig, EventKind, Spark, SparkKind


GRAPH_OFFSETS = (1, 7, 23, 61)
GRAPH_WEIGHTS = (0.18, 0.16, 0.14, 0.12)


@dataclass(slots=True)
class WorkCounter:
    queue_pushes: int = 0
    queue_pops: int = 0
    source_touches: int = 0
    destination_touches: int = 0
    state_touches: int = 0
    state_decay_evaluations: int = 0
    threshold_relax_evaluations: int = 0
    eligibility_edge_touches: int = 0
    eligibility_multiplications: int = 0
    route_edge_checks: int = 0
    message_traversals: int = 0
    activation_additions: int = 0
    eligibility_additions: int = 0
    threshold_additions: int = 0
    sequence_additions: int = 0
    residual_multiplications: int = 0
    fanout_bookkeeping: int = 0

    def total(self) -> int:
        return sum(asdict(self).values())

    def validate(self) -> None:
        for name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"invalid work counter {name}={value!r}")


class AuditedSparkBrain(SparkBrain):
    """SparkBrain with symmetric primitive work accounting.

    The candidate uses the reference engine's event-routed lazy semantics.  The
    dense comparator executes the same semantics but additionally materializes
    every Spark and evaluates every graph edge at every queued event.  Those
    dense scans intentionally do not change outputs.
    """

    def __init__(self, *, dense_scan: bool, config: BrainConfig) -> None:
        super().__init__(config)
        self.dense_scan = dense_scan
        self.work = WorkCounter()

    def schedule(
        self,
        *,
        time: float,
        kind: EventKind,
        source: str,
        target: str | None,
        strength: float = 0.0,
        priority: int = 10,
        evidence_id: str | None = None,
        evidence_label: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        self.work.queue_pushes += 1
        self.work.sequence_additions += 1
        super().schedule(
            time=time,
            kind=kind,
            source=source,
            target=target,
            strength=strength,
            priority=priority,
            evidence_id=evidence_id,
            evidence_label=evidence_label,
            metadata=metadata,
        )

    def run(self, *, max_events: int = 1_000_000) -> None:
        processed = 0
        while self._queue:
            if processed >= max_events:
                raise RuntimeError("H5 workload exceeded prospectively fixed max_events")
            event = heapq.heappop(self._queue)
            self.work.queue_pops += 1
            self.time = event.time
            if self.dense_scan:
                for spark in self.sparks.values():
                    self._touch(spark, event.time)
                self.work.route_edge_checks += len(self.connections)
            self._decay_eligibilities()
            self._process_event(event)
            processed += 1

    def _touch(self, spark: Spark, now: float) -> None:
        dt = max(0.0, now - spark.last_update)
        self.work.state_touches += 1
        if dt > 0.0 and spark.decay_tau > 0.0:
            self.work.state_decay_evaluations += 1
        if dt > 0.0 and self.config.threshold_relaxation_tau > 0.0:
            self.work.threshold_relax_evaluations += 1
        super()._touch(spark, now)

    def _decay_eligibilities(self) -> None:
        edge_count = len(self.connections)
        self.work.eligibility_edge_touches += edge_count
        self.work.eligibility_multiplications += edge_count
        super()._decay_eligibilities()

    def _process_event(self, event) -> None:
        self.work.source_touches += 1
        if event.target is not None:
            self.work.destination_touches += 1
            self.work.activation_additions += 1
        super()._process_event(event)

    def _fire(self, spark: Spark, event) -> bool:
        outgoing = len(self.edges_out.get(spark.id, []))
        self.work.route_edge_checks += outgoing
        self.work.message_traversals += outgoing
        self.work.eligibility_additions += outgoing
        self.work.threshold_additions += 1
        self.work.residual_multiplications += 1
        self.work.fanout_bookkeeping += 1
        return super()._fire(spark, event)


def build_brain(*, size: int, dense_scan: bool, seed: int) -> AuditedSparkBrain:
    if size < 64:
        raise ValueError("H5 graph size must be >= 64")
    config = BrainConfig(
        random_seed=seed,
        ignition_threshold=1e9,
        ignition_margin=1e9,
        min_support_sources=99,
        stability_evaluations=99,
        propagation_delay=0.01,
    )
    brain = AuditedSparkBrain(dense_scan=dense_scan, config=config)
    for index in range(size):
        brain.add_spark(
            Spark(
                id=f"s{index}",
                label=f"s{index}",
                kind=SparkKind.FEATURE,
                organ="h5",
                threshold=1.0,
                base_threshold=1.0,
                decay_tau=3.0,
            )
        )
    for index in range(size):
        for offset, weight in zip(GRAPH_OFFSETS, GRAPH_WEIGHTS, strict=True):
            brain.connect(
                f"s{index}",
                f"s{(index + offset) % size}",
                weight,
                delay=0.01,
                plastic=False,
                label="h5_circulant",
            )
    return brain


def _targets_for_tick(
    *,
    family: str,
    size: int,
    activity_fraction: float,
    tick: int,
    rng: random.Random,
) -> list[int]:
    if not 0.0 < activity_fraction <= 1.0:
        raise ValueError("activity_fraction must be in (0, 1]")
    count = max(1, min(size, round(size * activity_fraction)))
    if family == "uniform":
        return sorted(rng.sample(range(size), count))
    if family == "clustered":
        center = rng.randrange(size)
        start = center - count // 2
        return sorted({(start + offset) % size for offset in range(count)})
    if family == "bursty":
        if tick % 4 != 0:
            return []
        burst_count = max(1, min(size, count * 4))
        return sorted(rng.sample(range(size), burst_count))
    raise ValueError(f"unknown H5 workload family: {family}")


def schedule_workload(
    brain: AuditedSparkBrain,
    *,
    family: str,
    size: int,
    activity_fraction: float,
    horizon: int,
    seed: int,
) -> int:
    rng = random.Random(seed)
    scheduled = 0
    for tick in range(horizon):
        for target_index in _targets_for_tick(
            family=family,
            size=size,
            activity_fraction=activity_fraction,
            tick=tick,
            rng=rng,
        ):
            brain.inject_stimulus(
                target=f"s{target_index}",
                label="h5",
                time=float(tick),
                strength=1.05,
                source="h5_world",
                evidence_id=f"h5:{seed}:{tick}:{target_index}",
            )
            scheduled += 1
    return scheduled


def logical_activation(brain: AuditedSparkBrain, spark: Spark) -> float:
    dt = max(0.0, brain.time - spark.last_update)
    if dt <= 0.0 or spark.decay_tau <= 0.0:
        return spark.activation
    return spark.activation * math.exp(-dt / spark.decay_tau)


def snapshot(brain: AuditedSparkBrain) -> dict:
    return {
        "time": brain.time,
        "events_processed": brain.stats.events_processed,
        "activations": {
            spark_id: logical_activation(brain, spark)
            for spark_id, spark in sorted(brain.sparks.items())
        },
        "fired_counts": {
            spark_id: spark.fired_count
            for spark_id, spark in sorted(brain.sparks.items())
        },
        "queue_empty": not brain._queue,
    }


def run_cell(
    *,
    family: str,
    size: int,
    activity_fraction: float,
    horizon: int,
    seed: int,
) -> dict:
    candidate = build_brain(size=size, dense_scan=False, seed=seed)
    dense = build_brain(size=size, dense_scan=True, seed=seed)
    candidate_external = schedule_workload(
        candidate,
        family=family,
        size=size,
        activity_fraction=activity_fraction,
        horizon=horizon,
        seed=seed,
    )
    dense_external = schedule_workload(
        dense,
        family=family,
        size=size,
        activity_fraction=activity_fraction,
        horizon=horizon,
        seed=seed,
    )
    if candidate_external != dense_external:
        raise AssertionError("paired H5 workloads diverged before execution")
    candidate.run()
    dense.run()
    candidate.work.validate()
    dense.work.validate()
    candidate_snapshot = snapshot(candidate)
    dense_snapshot = snapshot(dense)
    max_abs_error = max(
        abs(candidate_snapshot["activations"][key] - dense_snapshot["activations"][key])
        for key in candidate_snapshot["activations"]
    )
    fired_exact = candidate_snapshot["fired_counts"] == dense_snapshot["fired_counts"]
    events_exact = (
        candidate_snapshot["events_processed"] == dense_snapshot["events_processed"]
    )
    queue_exact = candidate_snapshot["queue_empty"] and dense_snapshot["queue_empty"]
    if candidate.work.queue_pushes != candidate.work.queue_pops:
        raise AssertionError("candidate queue accounting does not close")
    if dense.work.queue_pushes != dense.work.queue_pops:
        raise AssertionError("dense queue accounting does not close")
    return {
        "family": family,
        "size": size,
        "activity_fraction": activity_fraction,
        "horizon": horizon,
        "seed": seed,
        "external_events": candidate_external,
        "candidate_work": candidate.work.total(),
        "dense_work": dense.work.total(),
        "candidate_counters": asdict(candidate.work),
        "dense_counters": asdict(dense.work),
        "max_abs_activation_error": max_abs_error,
        "fired_counts_exact": fired_exact,
        "events_processed_exact": events_exact,
        "queue_empty_exact": queue_exact,
    }


def quality_pass(row: dict, *, tolerance: float = 1e-10) -> bool:
    return bool(
        row["max_abs_activation_error"] <= tolerance
        and row["fired_counts_exact"]
        and row["events_processed_exact"]
        and row["queue_empty_exact"]
    )


def type7_quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("quantile requires at least one value")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def score_rows(
    rows: list[dict],
    *,
    bootstrap_seed: int = 75001,
    bootstrap_replicates: int = 10_000,
) -> dict:
    if not rows:
        raise ValueError("H5 scoring requires rows")
    if not all(quality_pass(row) for row in rows):
        return {"classification": "INVALID_QUALITY_GUARD"}
    sparse_rows = [row for row in rows if not row.get("dense_control", False)]
    seed_ids = sorted({int(row["seed"]) for row in sparse_rows})
    if not seed_ids:
        raise ValueError("H5 scoring requires sparse TEST rows")

    def reduction(row: dict) -> float:
        dense_work = float(row["dense_work"])
        if dense_work <= 0.0:
            raise ValueError("dense work must be positive")
        return 1.0 - float(row["candidate_work"]) / dense_work

    per_seed = {
        seed: sum(reduction(row) for row in sparse_rows if int(row["seed"]) == seed)
        / sum(1 for row in sparse_rows if int(row["seed"]) == seed)
        for seed in seed_ids
    }
    point = sum(per_seed.values()) / len(per_seed)
    rng = random.Random(bootstrap_seed)
    bootstrap = []
    for _ in range(bootstrap_replicates):
        sampled = [rng.choice(seed_ids) for _ in seed_ids]
        bootstrap.append(sum(per_seed[seed] for seed in sampled) / len(sampled))
    ci = [type7_quantile(bootstrap, 0.025), type7_quantile(bootstrap, 0.975)]
    activity_means = {}
    for activity in sorted({float(row["activity_fraction"]) for row in sparse_rows}):
        subset = [row for row in sparse_rows if float(row["activity_fraction"]) == activity]
        activity_means[str(activity)] = sum(reduction(row) for row in subset) / len(subset)

    if ci[0] >= 0.20 and all(value >= 0.10 for value in activity_means.values()):
        classification = "PASS_WORK_REDUCTION"
    elif ci[1] <= 0.05 or all(value <= 0.0 for value in activity_means.values()):
        classification = "FAIL_NO_USEFUL_WORK_REDUCTION"
    else:
        classification = "INCONCLUSIVE"
    return {
        "classification": classification,
        "primary_mean_work_reduction": point,
        "primary_ci95": ci,
        "activity_mean_reductions": activity_means,
        "cluster_unit": "workload_seed",
        "bootstrap_replicates": bootstrap_replicates,
        "bootstrap_seed": bootstrap_seed,
    }


def canonical_raw_json(rows: list[dict]) -> str:
    ordered = sorted(
        rows,
        key=lambda row: (
            row["family"],
            int(row["size"]),
            float(row["activity_fraction"]),
            int(row["horizon"]),
            int(row["seed"]),
        ),
    )
    return json.dumps(ordered, sort_keys=True, separators=(",", ":")) + "\n"


def dev_validate() -> list[dict]:
    rows = []
    for family in ("uniform", "clustered", "bursty"):
        row = run_cell(
            family=family,
            size=64,
            activity_fraction=0.08,
            horizon=4,
            seed=1709,
        )
        if not quality_pass(row):
            raise AssertionError(f"H5 DEV equivalence failed for {family}")
        if row["dense_counters"]["route_edge_checks"] < row["candidate_counters"][
            "route_edge_checks"
        ]:
            raise AssertionError("dense comparator edge accounting is not a superset")
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev-validate", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.dev_validate:
        parser.error("only --dev-validate is authorized before formal identity")
    rows = dev_validate()
    payload = canonical_raw_json(rows)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
