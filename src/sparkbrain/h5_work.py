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
    scheduler_writes: int = 0
    scheduler_reads: int = 0
    target_state_accesses: int = 0
    state_materializations: int = 0
    state_decay_evaluations: int = 0
    threshold_relax_evaluations: int = 0
    eligibility_edge_touches: int = 0
    eligibility_multiplications: int = 0
    route_edge_checks: int = 0
    message_traversals: int = 0
    activation_additions: int = 0
    eligibility_additions: int = 0
    threshold_additions: int = 0
    residual_multiplications: int = 0
    fanout_index_lookups: int = 0

    def total(self) -> int:
        return sum(asdict(self).values())

    def validate(self) -> None:
        for name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"invalid work counter {name}={value!r}")


class AuditedSparkBrain(SparkBrain):
    """Reference event-routed candidate with implementation-faithful work counts."""

    def __init__(self, *, config: BrainConfig) -> None:
        super().__init__(config)
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
        self.work.scheduler_writes += 1
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
                raise RuntimeError(
                    "H5 workload exceeded prospectively fixed max_events"
                )
            event = heapq.heappop(self._queue)
            self.work.scheduler_reads += 1
            self.time = event.time
            self._decay_eligibilities()
            self._process_event(event)
            processed += 1

    def _touch(self, spark: Spark, now: float) -> None:
        dt = max(0.0, now - spark.last_update)
        self.work.state_materializations += 1
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
        if event.target is not None:
            self.work.target_state_accesses += 1
            self.work.activation_additions += 1
        super()._process_event(event)

    def _fire(self, spark: Spark, event) -> bool:
        outgoing = len(self.edges_out.get(spark.id, []))
        self.work.fanout_index_lookups += 1
        self.work.route_edge_checks += outgoing
        self.work.message_traversals += outgoing
        self.work.eligibility_additions += outgoing
        self.work.threshold_additions += 1
        self.work.residual_multiplications += 1
        return super()._fire(spark, event)


@dataclass(slots=True)
class DenseEvent:
    priority: int
    target_index: int
    strength: float


class DenseEagerSparkBrain:
    """Standalone dense/eager H5 comparator.

    This implementation does not inherit from or invoke SparkBrain's event
    transition path. It directly materializes the full node state at each
    distinct event time and applies the same H5 state equations using compact
    arrays and a calendar of time buckets.
    """

    def __init__(self, *, size: int, seed: int) -> None:
        if size < 64:
            raise ValueError("H5 graph size must be >= 64")
        self.size = size
        self.config = h5_config(seed)
        self.work = WorkCounter()
        self.time = 0.0
        self.events_processed = 0

        self.activations = [0.0] * size
        self.thresholds = [1.0] * size
        self.refractory_until = [0.0] * size
        self.last_fire: list[float | None] = [None] * size
        self.fired_counts = [0] * size
        self.eligibilities = [0.0] * (size * len(GRAPH_OFFSETS))

        self._calendar: dict[float, dict[int, list[DenseEvent]]] = {}
        self._times: list[float] = []

    def schedule(
        self,
        *,
        time: float,
        priority: int,
        target_index: int,
        strength: float,
    ) -> None:
        if time < self.time - 1e-9:
            raise ValueError(
                f"Cannot schedule an event in the past: {time} < {self.time}"
            )
        if not 0 <= target_index < self.size:
            raise IndexError(f"Unknown dense target index: {target_index}")
        bucket = self._calendar.get(time)
        if bucket is None:
            bucket = {}
            self._calendar[time] = bucket
            heapq.heappush(self._times, time)
        bucket.setdefault(priority, []).append(
            DenseEvent(
                priority=priority,
                target_index=target_index,
                strength=strength,
            )
        )
        self.work.scheduler_writes += 1

    def inject_stimulus(
        self,
        *,
        target_index: int,
        time: float,
        strength: float,
    ) -> None:
        self.schedule(
            time=time,
            priority=0,
            target_index=target_index,
            strength=strength,
        )

    def _materialize_all(self, now: float) -> None:
        dt = max(0.0, now - self.time)
        if dt <= 0.0:
            self.time = now
            return
        activation_decay = math.exp(-dt / 3.0)
        threshold_relax = math.exp(-dt / self.config.threshold_relaxation_tau)
        for index in range(self.size):
            self.work.state_materializations += 1
            self.work.state_decay_evaluations += 1
            self.work.threshold_relax_evaluations += 1
            self.activations[index] *= activation_decay
            self.thresholds[index] = 1.0 + (
                self.thresholds[index] - 1.0
            ) * threshold_relax
        self.time = now

    def _decay_eligibilities(self) -> None:
        factor = self.config.eligibility_decay
        for index, value in enumerate(self.eligibilities):
            self.work.eligibility_edge_touches += 1
            self.work.eligibility_multiplications += 1
            self.eligibilities[index] = value * factor

    def _fire(self, source_index: int) -> None:
        pre_activation = self.activations[source_index]
        self.last_fire[source_index] = self.time
        self.fired_counts[source_index] += 1
        self.refractory_until[source_index] = (
            self.time + self.config.refractory_period
        )
        self.thresholds[source_index] += self.config.homeostatic_increment
        self.work.threshold_additions += 1

        self.activations[source_index] = (
            pre_activation * self.config.post_fire_residual
        )
        self.work.residual_multiplications += 1

        eligibility_increment = max(
            0.0,
            min(
                1.0,
                pre_activation / max(self.thresholds[source_index], 1e-6),
            ),
        )
        edge_base = source_index * len(GRAPH_OFFSETS)
        for slot, (offset, weight) in enumerate(
            zip(GRAPH_OFFSETS, GRAPH_WEIGHTS, strict=True)
        ):
            self.work.route_edge_checks += 1
            self.work.message_traversals += 1
            self.work.eligibility_additions += 1
            edge_index = edge_base + slot
            self.eligibilities[edge_index] += eligibility_increment
            self.schedule(
                time=self.time + 0.01,
                priority=20,
                target_index=(source_index + offset) % self.size,
                strength=weight,
            )

    def _process_event(self, event: DenseEvent) -> None:
        self.events_processed += 1
        self.work.target_state_accesses += 1
        self.work.activation_additions += 1
        target = event.target_index
        self.activations[target] += event.strength
        if (
            self.activations[target] >= self.thresholds[target]
            and self.time >= self.refractory_until[target]
        ):
            self._fire(target)

    def run(self, *, max_events: int = 1_000_000) -> None:
        processed = 0
        while self._times:
            now = heapq.heappop(self._times)
            bucket = self._calendar.pop(now)
            self._materialize_all(now)
            for priority in sorted(bucket):
                for event in bucket[priority]:
                    if processed >= max_events:
                        raise RuntimeError(
                            "H5 workload exceeded prospectively fixed max_events"
                        )
                    self.work.scheduler_reads += 1
                    self._decay_eligibilities()
                    self._process_event(event)
                    processed += 1

    @property
    def queue_empty(self) -> bool:
        return not self._times and not self._calendar


def h5_config(seed: int) -> BrainConfig:
    return BrainConfig(
        random_seed=seed,
        ignition_threshold=1e9,
        ignition_margin=1e9,
        min_support_sources=99,
        stability_evaluations=99,
        propagation_delay=0.01,
    )


def build_candidate(*, size: int, seed: int) -> AuditedSparkBrain:
    if size < 64:
        raise ValueError("H5 graph size must be >= 64")
    brain = AuditedSparkBrain(config=h5_config(seed))
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


def workload_events(
    *,
    family: str,
    size: int,
    activity_fraction: float,
    horizon: int,
    seed: int,
) -> list[tuple[float, int]]:
    rng = random.Random(seed)
    events: list[tuple[float, int]] = []
    for tick in range(horizon):
        targets = _targets_for_tick(
            family=family,
            size=size,
            activity_fraction=activity_fraction,
            tick=tick,
            rng=rng,
        )
        events.extend((float(tick), target_index) for target_index in targets)
    return events


def schedule_candidate_workload(
    brain: AuditedSparkBrain,
    *,
    events: list[tuple[float, int]],
    seed: int,
) -> None:
    for time, target_index in events:
        brain.inject_stimulus(
            target=f"s{target_index}",
            label="h5",
            time=time,
            strength=1.05,
            source="h5_world",
            evidence_id=f"h5:{seed}:{time:.6f}:{target_index}",
        )


def schedule_dense_workload(
    brain: DenseEagerSparkBrain,
    *,
    events: list[tuple[float, int]],
) -> None:
    for time, target_index in events:
        brain.inject_stimulus(
            target_index=target_index,
            time=time,
            strength=1.05,
        )


def logical_activation(brain: AuditedSparkBrain, spark: Spark) -> float:
    dt = max(0.0, brain.time - spark.last_update)
    if dt <= 0.0 or spark.decay_tau <= 0.0:
        return spark.activation
    return spark.activation * math.exp(-dt / spark.decay_tau)


def logical_threshold(brain: AuditedSparkBrain, spark: Spark) -> float:
    dt = max(0.0, brain.time - spark.last_update)
    if dt <= 0.0 or brain.config.threshold_relaxation_tau <= 0.0:
        return spark.threshold
    relax = math.exp(-dt / brain.config.threshold_relaxation_tau)
    return spark.base_threshold + (
        spark.threshold - spark.base_threshold
    ) * relax


def candidate_snapshot(brain: AuditedSparkBrain) -> dict:
    return {
        "time": brain.time,
        "events_processed": brain.stats.events_processed,
        "activations": [
            logical_activation(brain, brain.sparks[f"s{index}"])
            for index in range(len(brain.sparks))
        ],
        "thresholds": [
            logical_threshold(brain, brain.sparks[f"s{index}"])
            for index in range(len(brain.sparks))
        ],
        "refractory_until": [
            brain.sparks[f"s{index}"].refractory_until
            for index in range(len(brain.sparks))
        ],
        "last_fire": [
            brain.sparks[f"s{index}"].last_fire
            for index in range(len(brain.sparks))
        ],
        "fired_counts": [
            brain.sparks[f"s{index}"].fired_count
            for index in range(len(brain.sparks))
        ],
        "eligibilities": [edge.eligibility for edge in brain.connections],
        "queue_empty": not brain._queue,
    }


def dense_snapshot(brain: DenseEagerSparkBrain) -> dict:
    return {
        "time": brain.time,
        "events_processed": brain.events_processed,
        "activations": list(brain.activations),
        "thresholds": list(brain.thresholds),
        "refractory_until": list(brain.refractory_until),
        "last_fire": list(brain.last_fire),
        "fired_counts": list(brain.fired_counts),
        "eligibilities": list(brain.eligibilities),
        "queue_empty": brain.queue_empty,
    }


def _max_abs_difference(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise AssertionError("H5 paired state vectors have different lengths")
    return max((abs(a - b) for a, b in zip(left, right, strict=True)), default=0.0)


def run_cell(
    *,
    family: str,
    size: int,
    activity_fraction: float,
    horizon: int,
    seed: int,
) -> dict:
    events = workload_events(
        family=family,
        size=size,
        activity_fraction=activity_fraction,
        horizon=horizon,
        seed=seed,
    )
    candidate = build_candidate(size=size, seed=seed)
    dense = DenseEagerSparkBrain(size=size, seed=seed)
    schedule_candidate_workload(candidate, events=events, seed=seed)
    schedule_dense_workload(dense, events=events)

    candidate.run()
    dense.run()
    candidate.work.validate()
    dense.work.validate()

    candidate_state = candidate_snapshot(candidate)
    dense_state = dense_snapshot(dense)
    last_fire_exact = candidate_state["last_fire"] == dense_state["last_fire"]
    fired_exact = (
        candidate_state["fired_counts"] == dense_state["fired_counts"]
    )
    events_exact = (
        candidate_state["events_processed"] == dense_state["events_processed"]
    )
    queue_exact = (
        candidate_state["queue_empty"] and dense_state["queue_empty"]
    )
    if candidate.work.scheduler_writes != candidate.work.scheduler_reads:
        raise AssertionError("candidate scheduler accounting does not close")
    if dense.work.scheduler_writes != dense.work.scheduler_reads:
        raise AssertionError("dense scheduler accounting does not close")

    return {
        "family": family,
        "size": size,
        "activity_fraction": activity_fraction,
        "horizon": horizon,
        "seed": seed,
        "external_events": len(events),
        "candidate_work": candidate.work.total(),
        "dense_work": dense.work.total(),
        "candidate_counters": asdict(candidate.work),
        "dense_counters": asdict(dense.work),
        "max_abs_activation_error": _max_abs_difference(
            candidate_state["activations"],
            dense_state["activations"],
        ),
        "max_abs_threshold_error": _max_abs_difference(
            candidate_state["thresholds"],
            dense_state["thresholds"],
        ),
        "max_abs_refractory_error": _max_abs_difference(
            candidate_state["refractory_until"],
            dense_state["refractory_until"],
        ),
        "max_abs_eligibility_error": _max_abs_difference(
            candidate_state["eligibilities"],
            dense_state["eligibilities"],
        ),
        "last_fire_exact": last_fire_exact,
        "fired_counts_exact": fired_exact,
        "events_processed_exact": events_exact,
        "queue_empty_exact": queue_exact,
        "dense_algorithm": "standalone_dense_eager_calendar",
    }


def quality_pass(row: dict, *, tolerance: float = 1e-10) -> bool:
    return bool(
        row["max_abs_activation_error"] <= tolerance
        and row["max_abs_threshold_error"] <= tolerance
        and row["max_abs_refractory_error"] <= tolerance
        and row["max_abs_eligibility_error"] <= tolerance
        and row["last_fire_exact"]
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
        seed: sum(
            reduction(row)
            for row in sparse_rows
            if int(row["seed"]) == seed
        )
        / sum(
            1
            for row in sparse_rows
            if int(row["seed"]) == seed
        )
        for seed in seed_ids
    }
    point = sum(per_seed.values()) / len(per_seed)
    rng = random.Random(bootstrap_seed)
    bootstrap = []
    for _ in range(bootstrap_replicates):
        sampled = [rng.choice(seed_ids) for _ in seed_ids]
        bootstrap.append(
            sum(per_seed[seed] for seed in sampled) / len(sampled)
        )
    ci = [
        type7_quantile(bootstrap, 0.025),
        type7_quantile(bootstrap, 0.975),
    ]
    activity_means = {}
    activities = sorted(
        {float(row["activity_fraction"]) for row in sparse_rows}
    )
    for activity in activities:
        subset = [
            row
            for row in sparse_rows
            if float(row["activity_fraction"]) == activity
        ]
        activity_means[str(activity)] = (
            sum(reduction(row) for row in subset) / len(subset)
        )

    if ci[0] >= 0.20 and all(
        value >= 0.10 for value in activity_means.values()
    ):
        classification = "PASS_WORK_REDUCTION"
    elif ci[1] <= 0.05 or all(
        value <= 0.0 for value in activity_means.values()
    ):
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
    return json.dumps(
        ordered,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


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
        if row["dense_algorithm"] != "standalone_dense_eager_calendar":
            raise AssertionError("dense comparator algorithm identity drifted")
        if row["dense_counters"]["fanout_index_lookups"] != 0:
            raise AssertionError("dense comparator inherited candidate fanout lookup")
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
