"""Isolated NON_EVIDENTIARY temporal-reuse diagnostic; never a historical runner.

See docs/research/temporal_reuse_loop_contract_20261001.md. Production runtime is
imported unchanged. The orchestrator runs guards before training, then all prefix
eligibility checks before any measured suffix or intervention.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import json
import math
import os
import platform
import random
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.v04.contracts import SignalPulse, SpikeEvent  # noqa: E402
from sparkbrain.v05.assemblies import AssemblyConfig  # noqa: E402
from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig  # noqa: E402

SEEDS = (910071, 910072)
ARMS = ("Q", "H", "R", "S", "F")
CHANNELS = tuple("ACFHIJKLMQ")
MIB = 1024 * 1024
CAP_STATE = 64 * MIB
CONTRACT = ROOT / "docs/research/temporal_reuse_loop_contract_20261001.md"


def deny_network(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith("socket."):
        raise RuntimeError("network_disabled: Python socket audit event")


def output_bound(additional_bytes: int = 0, *, terminal: bool = False) -> None:
    root = os.environ.get("SPARK_PROBE_OUTPUT_ROOT")
    if root:
        size = sum(p.stat().st_size for p in Path(root).rglob("*") if p.is_file())
        limit = (1024 if terminal else 1023) * MIB
        require(size + additional_bytes <= limit, "resource_limit: total output")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    text = canonical(value) + "\n"
    output_bound(
        len(text.encode()),
        terminal=path.name
        in {"report.json", "result.json", "manifest.json", "execution-cost.json"},
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())


def append_json(path: Path, value: Any) -> None:
    text = canonical(value) + "\n"
    output_bound(len(text.encode()), terminal=path.name == "job-costs.jsonl")
    with path.open("a", encoding="utf-8") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def hard_label(p1: float) -> int | None:
    return None if p1 == 0.5 else int(p1 > 0.5)


def pulse(time_ms: float, channel: str, magnitude: float) -> dict[str, Any]:
    return SignalPulse(
        time_ms=time_ms, channel=channel, magnitude=magnitude, source_id="probe-input"
    ).as_dict()


def occurrence(seed: int, key: str, index: int, *, cue: int | None = None) -> dict[str, Any]:
    """Evaluator-owned generator. Only pulses/start/opaque ID enter a model."""
    rng_seed = int(hashlib.sha256(f"{seed}|{key}|{index}".encode()).hexdigest(), 16)
    rng = random.Random(rng_seed)
    cycle = index if key == "prefix" else 64 + index
    if key == "probe":
        cycle = 64
    start = float(cycle * 200)
    rows: list[dict[str, Any]] = []
    for _ in range(2):
        channel = "HIJKLM"[rng.randrange(6)]
        rows.append(pulse(start + rng.uniform(0, 36), channel, 0.025))
    jitter = [0.0] * 3 if key == "prefix" else [rng.uniform(-0.35, 0.35) for _ in range(3)]
    drawn = (
        rng.randrange(2) if key == "interleaved" else (int(index >= 32) if key == "prefix" else 0)
    )
    target = drawn if cue is None else cue
    for channel, offset, delta in zip(("AFC", "CFA")[target], (8, 13, 15), jitter, strict=True):
        rows.append(pulse(start + offset + delta, channel, 1.18))
    rows.append(pulse(start + 40, "Q", 1.18))
    rows.sort(key=lambda item: (item["time_ms"], item["channel"]))
    return {
        "occurrence_id": f"occ-{cycle:06d}",
        "start_ms": start,
        "pulses": rows,
        "outcome": target,
        "receipt_time_ms": start + 80,
    }


def observation(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row[key] for key in ("occurrence_id", "start_ms", "pulses")}


def raster(obs: dict[str, Any]) -> list[float]:
    values = [0.0] * (41 * len(CHANNELS))
    for row in obs["pulses"]:
        relative = row["time_ms"] - obs["start_ms"]
        require(0 <= relative <= 40, "observation time outside allowed prefix")
        at = CHANNELS.index(row["channel"]) * 41
        lower = math.floor(relative)
        frac = relative - lower
        values[at + lower] += row["magnitude"] * (1 - frac)
        if frac:
            values[at + lower + 1] += row["magnitude"] * frac
    total = sum(values)
    require(total > 0, "empty raster")
    return [value / total for value in values]


def distance(left: list[float], right: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(left, right, strict=True))


def parameter_state(brain: IntegratedV05Brain) -> dict[str, tuple[float, float]]:
    return {
        f"{a}:{b}": (edge.weight, edge.delay_ms)
        for (a, b), edge in sorted(brain.base.field.connections.items())
    }


def eligibility(brain: IntegratedV05Brain, next_start: float) -> dict[str, Any]:
    field = brain.base.field
    detector = brain.base.burst_detector
    bad_order = [
        source
        for source, edges in field.outgoing.items()
        if edges != sorted(edges, key=lambda edge: (edge.delay_ms, edge.target_id))
    ]
    facts = {
        "queue_length": len(field._queue),
        "pending_cascade_spikes": len(brain.base.cascade_tracker._pending),
        "burst_times": [row.time_ms for row in detector._window],
        "burst_window_ms": detector.config.window_ms,
        "max_emitted_key_ms": max((b / 1000 for _, b in detector._emitted_keys), default=None),
        "noncanonical_outgoing_sources": bad_order,
        "next_start_ms": next_start,
    }
    facts["eligible"] = (
        not field._queue
        and not brain.base.cascade_tracker._pending
        and not bad_order
        and all(row.time_ms < next_start - detector.config.window_ms for row in detector._window)
        and all(max(key) / 1000 < next_start for key in detector._emitted_keys)
    )
    return facts


class Model:
    def __init__(self, arm: str):
        require(arm in ARMS, "unknown arm")
        self.arm = arm
        self.brain = None
        if arm in ("S", "F"):
            self.brain = IntegratedV05Brain(
                V05BrainConfig(
                    topology_seed=41,
                    enable_action=False,
                    enable_weight_learning=arm == "S",
                    enable_delay_learning=arm == "S",
                ),
                assembly_config=AssemblyConfig(max_candidates=32),
            )
        self.counts = [0, 0]
        self.memory: list[dict[str, Any]] = []
        self.prototypes: list[dict[str, Any]] = []
        self.pending: dict[str, Any] | None = None
        self.receipts: dict[str, int] = {}

    def state(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "counts": self.counts,
            "memory": self.memory,
            "prototypes": self.prototypes,
            "pending": self.pending,
            "receipts": self.receipts,
        }

    def checkpoint_bytes(self) -> int:
        size = len((canonical(self.state()) + "\n").encode())
        if self.brain:
            payload = self.brain.state_dict()
            size += len(
                (canonical({"payload": payload, "sha256": digest(payload)}) + "\n").encode()
            )
        require(size <= CAP_STATE, "resource_limit: full checkpoint bytes")
        return size

    def predict(self, obs: dict[str, Any], *, learn: bool = True) -> dict[str, Any]:
        require(set(obs) == {"occurrence_id", "start_ms", "pulses"}, "forbidden observation field")
        require(self.pending is None, "previous outcome not delivered")
        for row in obs["pulses"]:
            require(set(row) == set(pulse(0, "Q", 1)), "forbidden pulse field")
            require(
                row["source_id"] == "probe-input" and not row["metadata"], "input metadata leak"
            )
            require(row["polarity"] == 1 and row["location"] is None, "pulse attribute leak")
            require(row["novelty"] == 0 and row["prediction_error"] == 0, "modulation leak")
            require(row["channel"] in CHANNELS, "unknown channel")
            require(
                obs["start_ms"] <= row["time_ms"] <= obs["start_ms"] + 40,
                "observation outside query prefix",
            )
        out: dict[str, Any] = {
            "input_sha256": digest(obs),
            "occurrence_id": obs["occurrence_id"],
            "query_time_ms": obs["start_ms"] + 72,
        }
        self.pending = {"id": obs["occurrence_id"]}
        if self.brain:
            before = parameter_state(self.brain)
            result = self.brain.process_episode(
                [SignalPulse(**row) for row in obs["pulses"]],
                episode_id=obs["occurrence_id"],
                learn_assembly=learn,
                learn_field=learn,
                explore_action=False,
            )
            require(result.end_ms == obs["start_ms"] + 72, "query cutoff violated")
            activation = self.brain.pending_activation
            table = (
                self.brain.predictor.counts.get(activation.assembly_id, {}) if activation else {}
            )
            n0, n1 = table.get("0", 0), table.get("1", 0)
            p1 = (1 + n1) / (2 + n0 + n1)
            after = parameter_state(self.brain)
            out.update(
                {
                    "native": None
                    if result.prediction.value is None
                    else int(result.prediction.value),
                    "assembly_id": activation.assembly_id if activation else None,
                    "mature": bool(activation and activation.mature),
                    "raw_result": result.as_dict(),
                    "weights_delays_before": digest(before),
                    "weights_delays_after": digest(after),
                    "changed_weights": sum(before[k][0] != after[k][0] for k in before),
                    "changed_delays": sum(before[k][1] != after[k][1] for k in before),
                    "eligibility_update_work": self.brain.plasticity.update_count,
                    "field_arrivals": self.brain.base.field.total_arrivals,
                    "field_spikes": self.brain.base.field.total_spikes,
                    "representation_slots": len(self.brain.assemblies.candidates),
                    "candidate_comparisons_upper_bound": len(result.patterns) * 32,
                }
            )
        elif self.arm == "Q":
            p1 = (1 + self.counts[1]) / (2 + sum(self.counts))
        else:
            x = raster(obs)
            self.pending["x"] = x
            if self.arm == "H":
                nearest = sorted(
                    enumerate(self.memory), key=lambda pair: (distance(x, pair[1]["x"]), pair[0])
                )[:3]
                p1 = (1 + sum(item["y"] for _, item in nearest)) / (2 + len(nearest))
                out["prototype_comparisons"] = len(self.memory)
            else:
                comparisons = len(self.prototypes) + int(bool(self.prototypes))
                nearest_id = min(
                    range(len(self.prototypes)),
                    key=lambda i: (distance(x, self.prototypes[i]["x"]), i),
                    default=None,
                )
                if nearest_id is None or (
                    distance(x, self.prototypes[nearest_id]["x"]) > 0.25
                    and len(self.prototypes) < 32
                ):
                    # Allocation is observation-driven and does not see the pending target.
                    nearest_id = len(self.prototypes)
                    self.prototypes.append({"x": x.copy(), "n": 0, "counts": [0, 0]})
                proto = self.prototypes[nearest_id]
                p1 = (1 + proto["counts"][1]) / (2 + sum(proto["counts"]))
                self.pending["prototype"] = nearest_id
                out["prototype_comparisons"] = comparisons
        out["p1"] = p1
        if not self.brain:
            out["native"] = hard_label(p1)
            out["representation_slots"] = (
                len(self.memory) if self.arm == "H" else len(self.prototypes)
            )
        operational = {
            "wrapper": self.state(),
            "brain": self.brain.state_dict() if self.brain else None,
        }
        serialized = canonical(operational).encode()
        require(len(serialized) <= CAP_STATE, "resource_limit: live state")
        out["operational_sha256"] = hashlib.sha256(serialized).hexdigest()
        out["live_state_bytes"] = self.checkpoint_bytes()
        return out

    def outcome(self, occurrence_id: str, value: int) -> bool:
        require(value in (0, 1), "invalid outcome")
        if occurrence_id in self.receipts:
            require(self.receipts[occurrence_id] == value, "conflicting receipt")
            return False
        require(self.pending is not None and self.pending["id"] == occurrence_id, "unknown receipt")
        if self.brain:
            self.brain.learn_outcome(next_event=str(value), reward=None)
        elif self.arm == "Q":
            self.counts[value] += 1
        elif self.arm == "H":
            self.memory.append({"x": self.pending["x"], "y": value})
            self.memory = self.memory[-32:]
        else:
            proto = self.prototypes[self.pending["prototype"]]
            n = proto["n"]
            proto["x"] = [
                (a * n + b) / (n + 1) for a, b in zip(proto["x"], self.pending["x"], strict=True)
            ]
            proto["n"] += 1
            proto["counts"][value] += 1
        self.receipts[occurrence_id] = value
        self.pending = None
        return True

    def save(self, directory: Path) -> int:
        expected_size = self.checkpoint_bytes()
        output_bound(expected_size)
        directory.mkdir(parents=True, exist_ok=False)
        if self.brain:
            self.brain.save_checkpoint(directory / "brain.json")
        write_json(directory / "wrapper.json", self.state())
        size = sum(path.stat().st_size for path in directory.iterdir())
        require(size <= CAP_STATE, "resource_limit: checkpoint bytes")
        require(size == expected_size, "checkpoint byte accounting mismatch")
        return size

    @classmethod
    def load(cls, directory: Path) -> Model:
        state = read_json(directory / "wrapper.json")
        model = cls(state["arm"])
        for key in ("counts", "memory", "prototypes", "pending", "receipts"):
            setattr(model, key, state[key])
        if model.brain:
            model.brain = IntegratedV05Brain.load_checkpoint(directory / "brain.json")
        return model


def select_target(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, list[int]] = {}
    for row in rows:
        aid = row.get("assembly_id")
        if aid and row.get("mature"):
            counts.setdefault(aid, [0, 0])[row["outcome"]] += 1
    candidates = [aid for aid, count in counts.items() if count[0] >= 8 and count[1] == 0]
    target = min(candidates, key=lambda aid: (-counts[aid][0], aid), default=None)
    matches = (
        []
        if target is None
        else [
            aid
            for aid, count in counts.items()
            if aid != target
            and count[1] >= 8
            and count[0] == 0
            and abs(count[1] - counts[target][0]) <= 0.25 * counts[target][0]
        ]
    )
    matched = min(
        matches, key=lambda aid: (abs(counts[aid][1] - counts[target][0]), aid), default=None
    )
    return {
        "target": target,
        "matched": matched,
        "prefix_counts": counts,
        "status": "identifiable" if target and matched else "intervention_not_identifiable",
    }


@contextlib.contextmanager
def deadline(cpu: float, wall: float):
    def stop(signum: int, frame: Any) -> None:
        raise TimeoutError(f"resource_limit: signal {signum}")

    require(cpu > 0 and wall > 0, "resource_limit: no remaining time")
    begun_cpu, begun_wall = time.process_time(), time.monotonic()
    previous_cpu = signal.getitimer(signal.ITIMER_PROF)[0]
    previous_wall = signal.getitimer(signal.ITIMER_REAL)[0]
    old_prof = signal.signal(signal.SIGPROF, stop)
    old_alarm = signal.signal(signal.SIGALRM, stop)
    signal.setitimer(signal.ITIMER_PROF, min(cpu, previous_cpu) if previous_cpu else cpu)
    signal.setitimer(signal.ITIMER_REAL, min(wall, previous_wall) if previous_wall else wall)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_PROF, 0)
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGPROF, old_prof)
        signal.signal(signal.SIGALRM, old_alarm)
        if previous_cpu:
            remaining = previous_cpu - (time.process_time() - begun_cpu)
            require(remaining > 0, "resource_limit: enclosing CPU deadline")
            signal.setitimer(signal.ITIMER_PROF, remaining)
        if previous_wall:
            remaining = previous_wall - (time.monotonic() - begun_wall)
            require(remaining > 0, "resource_limit: enclosing wall deadline")
            signal.setitimer(signal.ITIMER_REAL, remaining)


def run_sequence(model: Model, inputs: list[dict[str, Any]], path: Path) -> list[dict[str, Any]]:
    rows = []
    for supplied in inputs:
        row = model.predict(observation(supplied))
        row.update({"outcome": supplied["outcome"], "receipt_time_ms": supplied["receipt_time_ms"]})
        # Durable raw prediction precedes feedback or aggregate scoring.
        append_json(path, row)
        model.outcome(supplied["occurrence_id"], supplied["outcome"])
        rows.append(row)
    return rows


def fixture_spike(unit: int, at: float) -> SpikeEvent:
    return SpikeEvent(at, unit, 1.0, 0.5, float(unit), 0.0, ("fixture",), 0.0, 0.0, 1.0, 0.0)


def guards(directory: Path) -> dict[str, Any]:
    """Hand-constructed fixtures only; no diagnostic generator or historical runner."""
    model = Model("S")
    brain = model.brain
    require(brain is not None, "fixture missing brain")
    edge = brain.base.field.outgoing[0][0]
    before = parameter_state(brain)
    brain.plasticity.apply(
        brain.base.field, [fixture_spike(0, 0), fixture_spike(edge.target_id, 1.5)]
    )
    require(before != parameter_state(brain), "fixture must contain learned changes")
    require(eligibility(brain, 200)["eligible"], "learned fixture not eligible")
    model.save(directory / "guard-checkpoint")
    restored = Model.load(directory / "guard-checkpoint")
    obs = {
        "occurrence_id": "fixture-0",
        "start_ms": 200.0,
        "pulses": [
            pulse(208, "A", 1.18),
            pulse(213, "F", 1.18),
            pulse(215, "C", 1.18),
            pulse(240, "Q", 1.18),
        ],
    }
    left, right = model.predict(obs, learn=False), restored.predict(obs, learn=False)
    write_json(directory / "guard-continuation-pair.json", {"direct": left, "restored": right})
    require(left == right, "checkpoint continuation returned outputs differ")
    require(
        brain.state_dict() == restored.brain.state_dict(), "checkpoint operational state differs"
    )
    model.outcome("fixture-0", 0)
    before_receipt = digest(brain.state_dict())
    require(not model.outcome("fixture-0", 0), "duplicate receipt learned")
    require(before_receipt == digest(brain.state_dict()), "duplicate altered model")
    model.save(directory / "guard-receipt-checkpoint")
    receipt_copy = Model.load(directory / "guard-receipt-checkpoint")
    require(receipt_copy.state() == model.state(), "wrapper receipts not restored")
    require(not receipt_copy.outcome("fixture-0", 0), "restored receipt learned again")
    next_obs = copy.deepcopy(obs)
    next_obs["occurrence_id"] = "fixture-pending"
    next_obs["start_ms"] += 200
    for row in next_obs["pulses"]:
        row["time_ms"] += 200
    model.predict(next_obs, learn=False)
    model.save(directory / "guard-pending-checkpoint")
    pending_copy = Model.load(directory / "guard-pending-checkpoint")
    require(pending_copy.state() == model.state(), "pending wrapper not restored")
    pending_copy.outcome("fixture-pending", 1)

    def rejected(fn: Any, label: str) -> None:
        try:
            fn()
        except (RuntimeError, TimeoutError, MemoryError):
            return
        raise RuntimeError(f"guard failed to reject {label}")

    forbidden = copy.deepcopy(obs)
    forbidden["target"] = 1
    rejected(lambda: Model("Q").predict(forbidden), "evaluator target")
    forbidden = copy.deepcopy(obs)
    forbidden["pulses"][0]["time_ms"] = 281
    rejected(lambda: Model("Q").predict(forbidden), "future pulse")
    forbidden = copy.deepcopy(obs)
    forbidden["pulses"][0]["metadata"] = {"regime": "A"}
    rejected(lambda: Model("Q").predict(forbidden), "metadata cue")
    opposite = copy.deepcopy(obs)
    opposite["pulses"][0]["channel"], opposite["pulses"][2]["channel"] = "C", "A"

    def without(value: dict[str, Any]) -> dict[str, Any]:
        return {**value, "pulses": [p for p in value["pulses"] if p["channel"] not in "ACF"]}

    require(without(obs) == without(opposite), "removed pair not byte-identical")
    require(raster(obs) != raster(opposite), "intact swapped pair unexpectedly equal")

    def cpu_overrun() -> None:
        with deadline(0.01, 1):
            while True:
                hashlib.sha256(b"bounded guard").digest()

    def wall_overrun() -> None:
        with deadline(1, 0.01):
            time.sleep(0.1)

    rejected(cpu_overrun, "CPU overrun")
    rejected(wall_overrun, "wall overrun")
    require(resource.getrlimit(resource.RLIMIT_AS)[0] == 512 * MIB, "address cap missing")
    rejected(lambda: bytearray(512 * MIB), "address-space overrun")
    rejected(lambda: output_bound(1024 * MIB + 1), "output overrun")
    rejected(lambda: deny_network("socket.__new__", ()), "network event")
    for problem in ("queue", "cascade", "burst", "order", "emitted"):
        bad = Model("S").brain
        require(bad is not None, "missing boundary fixture")
        if problem == "queue":
            bad.base.field.schedule_pulse(SignalPulse(**pulse(200, "Q", 1.18)))
        elif problem == "cascade":
            bad.base.cascade_tracker._pending.append(fixture_spike(16, 199))
        elif problem == "burst":
            bad.base.burst_detector._window.append(fixture_spike(16, 195))
        elif problem == "order":
            bad.base.field.outgoing[0].reverse()
        else:
            bad.base.burst_detector._emitted_keys.add((199000, 200000))
        require(not eligibility(bad, 200)["eligible"], f"ineligible {problem} accepted")
    # Predictions, rather than provenance-bearing hashes, must survive ID renaming.
    for arm in ARMS:
        a, b = Model(arm), Model(arm)
        for i in range(4):
            template = {
                "occurrence_id": f"x-{i}",
                "start_ms": float(i * 200),
                "pulses": [
                    pulse(i * 200 + t, ch, 1.18)
                    for t, ch in ((8, "A"), (13, "F"), (15, "C"), (40, "Q"))
                ],
            }
            other = copy.deepcopy(template)
            other["occurrence_id"] = f"opaque-{100 - i}"
            first, second = a.predict(template), b.predict(other)
            require(
                (first["p1"], first["native"]) == (second["p1"], second["native"]), "ID leakage"
            )
            a.outcome(template["occurrence_id"], 0)
            b.outcome(other["occurrence_id"], 0)
            require(not a.outcome(template["occurrence_id"], 0), "duplicate learned")
    return {
        "status": "passed",
        "source": "hand_constructed_fixtures",
        "checks": [
            "learned_delay_quiet_continuation",
            "five_boundary_rejections",
            "receipt_idempotency",
            "ID_renaming_prediction_invariance",
            "nonempty_wrapper_receipt_and_pending_restore",
            "paired_input_equality_and_input_isolation",
            "CPU_wall_address_output_and_network_guards",
        ],
    }


def worker(job: dict[str, Any], directory: Path) -> dict[str, Any]:
    stage, arm = job["stage"], job.get("arm")
    if stage == "guards":
        return guards(directory)
    if stage == "prefix":
        model = Model(arm)
        rows = run_sequence(model, job["inputs"], directory / "raw.jsonl")
        result = {
            "status": "completed",
            "target": select_target(rows) if model.brain else None,
            "eligibility": eligibility(model.brain, 12800) if model.brain else {"eligible": True},
        }
        result["checkpoint_bytes"] = model.save(directory / "checkpoint")
        return result
    if stage == "suffix":
        model = Model.load(Path(job["checkpoint"]))
        run_sequence(model, job["inputs"], directory / "raw.jsonl")
        return {"status": "completed", "checkpoint_bytes": model.save(directory / "checkpoint")}
    require(stage == "forks", "unknown stage")
    target = job["target"]
    count, skipped = 0, []
    for index, pair in enumerate(job["pairs"]):
        for cue, supplied in enumerate(pair):
            states = ["sham", "targeted", "matched", "observer"] if arm in ("S", "F") else ["sham"]
            for intervention in states:
                if intervention in ("targeted", "matched") and target["status"] != "identifiable":
                    skipped.append([index, cue, intervention])
                    continue
                started_cpu, started_wall = time.process_time(), time.monotonic()
                with deadline(10, 15):
                    model = Model.load(Path(job["checkpoint"]))
                    if intervention in ("targeted", "matched"):
                        aid = target["target" if intervention == "targeted" else "matched"]
                        model.brain.suppress_assembly(aid)
                    row = model.predict(observation(supplied), learn=False)
                    row.update(
                        {
                            "pair": index,
                            "cue": cue,
                            "intervention": intervention,
                            "outcome": cue,
                            "removed": False,
                        }
                    )
                    append_json(directory / "raw.jsonl", row)
                    model.checkpoint_bytes()
                    append_json(
                        directory / "costs.jsonl",
                        {
                            "pair": index,
                            "cue": cue,
                            "intervention": intervention,
                            "cpu_before_cost_write": time.process_time() - started_cpu,
                            "wall_before_cost_write": time.monotonic() - started_wall,
                        },
                    )
                count += 1
            removed = observation(supplied)
            removed["pulses"] = [row for row in removed["pulses"] if row["channel"] not in "ACF"]
            started_cpu, started_wall = time.process_time(), time.monotonic()
            with deadline(10, 15):
                model = Model.load(Path(job["checkpoint"]))
                row = model.predict(removed, learn=False)
                row.update(
                    {
                        "pair": index,
                        "cue": cue,
                        "intervention": "sham",
                        "outcome": cue,
                        "removed": True,
                    }
                )
                append_json(directory / "raw.jsonl", row)
                model.checkpoint_bytes()
                append_json(
                    directory / "costs.jsonl",
                    {
                        "pair": index,
                        "cue": cue,
                        "removed": True,
                        "cpu_before_cost_write": time.process_time() - started_cpu,
                        "wall_before_cost_write": time.monotonic() - started_wall,
                    },
                )
            count += 1
    return {"status": "completed", "forks": count, "skipped_slots": skipped}


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def metrics(data: list[dict[str, Any]]) -> dict[str, Any]:
    losses = [(row["p1"] - row["outcome"]) ** 2 for row in data]
    return {
        "n": len(data),
        "brier": sum(losses) / len(losses),
        "coverage": sum(row["native"] is not None for row in data) / len(data),
        "accuracy_all": sum(row["native"] == row["outcome"] for row in data) / len(data),
        "first_p1": data[0]["p1"],
        "first_loss": losses[0],
        "first_four_brier": sum(losses[:4]) / min(4, len(losses)),
    }


def summarize(directory: Path) -> dict[str, Any]:
    report: dict[str, Any] = {"status": "completed", "scientific_credit": 0, "seeds": {}}
    for seed in SEEDS:
        entry: dict[str, Any] = {"arms": {}, "causal": {}}
        for arm in ARMS:
            entry["arms"][arm] = {
                key: metrics(rows(directory / f"{seed}-{arm}-{key}" / "raw.jsonl"))
                for key in ("return", "interleaved")
            }
            raw = rows(directory / f"{seed}-{arm}-forks" / "raw.jsonl")
            grouped = {(r["pair"], r["cue"], r["intervention"], r["removed"]): r for r in raw}
            cue_directions, removals, displays = [], [], []
            for i in range(8):
                a, b = (grouped[(i, c, "sham", False)] for c in (0, 1))
                cue_directions.append(b["p1"] > a["p1"])
                a, b = (grouped[(i, c, "sham", True)] for c in (0, 1))
                removals.append(
                    (a["input_sha256"], a["p1"], a["native"], a["operational_sha256"])
                    == (b["input_sha256"], b["p1"], b["native"], b["operational_sha256"])
                )
                if arm in ("S", "F"):
                    for c in (0, 1):
                        a, b = (grouped[(i, c, state, False)] for state in ("sham", "observer"))
                        displays.append(
                            (a["p1"], a["native"], a["operational_sha256"])
                            == (b["p1"], b["native"], b["operational_sha256"])
                        )
            causal: dict[str, Any] = {
                "cue_directions": sum(cue_directions),
                "removed_equal": all(removals),
                "observer_equal": all(displays) if displays else None,
            }
            if arm in ("S", "F"):
                selection = read_json(directory / f"{seed}-{arm}-prefix" / "result.json")["target"]
                causal["selection"] = selection
                if selection["status"] == "identifiable":
                    impairments = {}
                    for c in (0, 1):
                        for state in ("targeted", "matched"):
                            vals = [
                                (
                                    (grouped[(i, c, state, False)]["p1"] - c) ** 2
                                    - (grouped[(i, c, "sham", False)]["p1"] - c) ** 2
                                )
                                for i in range(8)
                            ]
                            impairments[f"{c}_{state}"] = sum(vals) / 8
                            if c == 1 and state == "targeted":
                                causal["absolute_B_collateral"] = sum(abs(v) for v in vals) / 8
                    causal["impairment"] = impairments
                    causal["targeted_minus_matched_A"] = (
                        impairments["0_targeted"] - impairments["0_matched"]
                    )
            entry["causal"][arm] = causal
        s = entry["arms"]["S"]
        causal = entry["causal"]["S"]
        entry["all_control_guards_passed"] = all(
            value["removed_equal"] and value["observer_equal"] is not False
            for value in entry["causal"].values()
        )
        entry["integration_proposal_gate"] = (
            all(
                s[key]["brier"] <= entry["arms"][arm][key]["brier"] - 0.02
                for key in ("return", "interleaved")
                for arm in ("H", "R")
            )
            and 1 - s["return"]["first_p1"] >= 0.75
            and causal.get("targeted_minus_matched_A", -math.inf) >= 0.05
            and causal.get("absolute_B_collateral", math.inf) <= 0.02
            and causal["cue_directions"] >= 6
            and causal["removed_equal"]
            and causal["observer_equal"]
            and entry["all_control_guards_passed"]
        )
        report["seeds"][str(seed)] = entry
    report["integration_proposal_gate_both_seeds"] = all(
        entry["integration_proposal_gate"] for entry in report["seeds"].values()
    )
    return report


def orchestrate(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    os.environ["SPARK_PROBE_OUTPUT_ROOT"] = str(directory)
    started, cpu_start = time.monotonic(), time.process_time()
    spent_cpu = 0.0
    job_records = []
    report_pending: dict[str, Any] = {"status": "stopped", "scientific_credit": 0}
    write_json(
        directory / "environment.json",
        {
            "python": sys.version,
            "platform": platform.platform(),
            "hashseed": os.environ.get("PYTHONHASHSEED"),
            "network_guard": "Python socket audit denial; OS network namespace unavailable",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "seeds": SEEDS,
            "arms": ARMS,
            "rng_seed_conversion": "int(sha256(utf8(seed|key|index)).hexdigest(),16)",
        },
    )

    def launch(
        name: str, job: dict[str, Any], cpu: float = 120, wall: float = 180
    ) -> dict[str, Any]:
        nonlocal spent_cpu
        total_cpu = spent_cpu + time.process_time() - cpu_start
        require(
            total_cpu < 1798 and time.monotonic() - started < 2695, "resource_limit: global time"
        )
        require(
            sum(p.stat().st_size for p in directory.rglob("*") if p.is_file()) < 1024 * MIB,
            "resource_limit: total output",
        )
        work = directory / name
        work.mkdir()
        job["cpu_limit"] = min(cpu, 1798 - total_cpu)
        job["wall_limit"] = min(wall, 2695 - (time.monotonic() - started))
        write_json(work / "job.json", job)
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        wall_start = time.monotonic()
        proc = None
        timed_out = False
        try:
            with (work / "process.log").open("x") as log:
                proc = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()), "--worker", str(work)],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    env={**os.environ, "PYTHONHASHSEED": "0"},
                    timeout=max(0.01, job["wall_limit"] + 1),
                    check=False,
                )
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            cost = {
                "name": name,
                "cpu": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                "wall": time.monotonic() - wall_start,
                "exit_code": proc.returncode if proc else None,
                "timed_out": timed_out,
            }
            spent_cpu += cost["cpu"]
            append_json(directory / "job-costs.jsonl", cost)
            job_records.append(cost)
        require(not timed_out, f"resource_limit: child wall timeout:{name}")
        require(proc is not None, f"worker_failed:{name}:no process")
        if proc.returncode in (-signal.SIGXCPU, -signal.SIGKILL):
            raise RuntimeError(f"resource_limit: child termination:{name}:{proc.returncode}")
        result = read_json(work / "result.json") if (work / "result.json").exists() else {}
        if result.get("status") == "resource_limit":
            raise RuntimeError(f"resource_limit: {name}:{result.get('error')}")
        require(proc.returncode == 0, f"worker_failed:{name}:{proc.returncode}:{result}")
        result["cost"] = cost
        require(result["status"] in ("passed", "completed"), f"worker_failed:{name}:{result}")
        require(
            cost["cpu"] <= cpu and cost["wall"] <= wall,
            f"resource_limit: inclusive trajectory:{name}",
        )
        require(spent_cpu + time.process_time() - cpu_start <= 1798, "resource_limit: total CPU")
        require(time.monotonic() - started <= 2695, "resource_limit: total wall")
        output_bound()
        return result

    try:
        launch("guards", {"stage": "guards"})
        prefixes = {}
        for seed in SEEDS:
            inputs = [occurrence(seed, "prefix", i) for i in range(64)]
            write_json(directory / f"inputs-{seed}-prefix.json", inputs)
            for arm in ARMS:
                name = f"{seed}-{arm}-prefix"
                prefixes[(seed, arm)] = launch(
                    name, {"stage": "prefix", "arm": arm, "inputs": inputs}
                )
        bad = {
            f"{seed}-{arm}": result["eligibility"]
            for (seed, arm), result in prefixes.items()
            if not result["eligibility"]["eligible"]
        }
        if bad:
            report_pending = {
                "status": "checkpoint_boundary_ineligible",
                "failures": bad,
                "scientific_credit": 0,
                "measured_suffixes": 0,
                "causal_forks": 0,
            }
            return
        for seed in SEEDS:
            for key in ("return", "interleaved"):
                inputs = [occurrence(seed, key, i) for i in range(32)]
                write_json(directory / f"inputs-{seed}-{key}.json", inputs)
                for arm in ARMS:
                    prefix = prefixes[(seed, arm)]
                    launch(
                        f"{seed}-{arm}-{key}",
                        {
                            "stage": "suffix",
                            "arm": arm,
                            "inputs": inputs,
                            "checkpoint": str(directory / f"{seed}-{arm}-prefix" / "checkpoint"),
                        },
                        120 - prefix["cost"]["cpu"],
                        180 - prefix["cost"]["wall"],
                    )
            pairs = [[occurrence(seed, "probe", i, cue=cue) for cue in (0, 1)] for i in range(8)]
            write_json(directory / f"inputs-{seed}-pairs.json", pairs)
            for arm in ARMS:
                launch(
                    f"{seed}-{arm}-forks",
                    {
                        "stage": "forks",
                        "arm": arm,
                        "pairs": pairs,
                        "target": prefixes[(seed, arm)]["target"],
                        "checkpoint": str(directory / f"{seed}-{arm}-prefix" / "checkpoint"),
                    },
                    1200,
                    1800,
                )
        # Raw files are closed and durable before aggregate computation.
        with deadline(
            1798 - (spent_cpu + time.process_time() - cpu_start),
            2695 - (time.monotonic() - started),
        ):
            report_pending = summarize(directory)
    except Exception as exc:
        report_pending = {
            "status": "resource_limit" if "resource_limit" in str(exc) else "stopped",
            "error": repr(exc),
            "scientific_credit": 0,
        }
        raise
    finally:
        files: dict[str, str] = {}
        inventory_complete = False
        try:
            with deadline(
                1798 - (spent_cpu + time.process_time() - cpu_start),
                2695 - (time.monotonic() - started),
            ):
                for path in sorted(directory.rglob("*")):
                    if path.is_file() and path.name not in {
                        "manifest.json",
                        "execution-cost.json",
                        "report.json",
                    }:
                        files[str(path.relative_to(directory))] = hashlib.sha256(
                            path.read_bytes()
                        ).hexdigest()
                inventory_complete = True
        except Exception as exc:
            report_pending = {
                "status": "resource_limit",
                "error": f"final inventory: {exc!r}",
                "scientific_credit": 0,
            }
        # Headroom is reserved INSIDE all outer caps. The last bounded writes cannot
        # report their own exact duration or recursively hash themselves.
        with deadline(2, 5):
            write_json(
                directory / "manifest.json",
                {
                    "complete": inventory_complete,
                    "files": files,
                    "excluded_closure_files": [
                        "manifest.json",
                        "execution-cost.json",
                        "report.json",
                    ],
                },
            )
            measured_cpu = spent_cpu + time.process_time() - cpu_start
            measured_wall = time.monotonic() - started
            if measured_cpu + 2 > 1800 or measured_wall + 5 > 2700:
                report_pending = {
                    "status": "resource_limit",
                    "error": "final closure headroom exhausted",
                    "scientific_credit": 0,
                }
            write_json(
                directory / "execution-cost.json",
                {
                    "cpu_before_closure_record": measured_cpu,
                    "wall_before_closure_record": measured_wall,
                    "cpu_conservative_upper_bound": measured_cpu + 2,
                    "wall_conservative_upper_bound": measured_wall + 5,
                    "closure_reserve_cpu": 2,
                    "closure_reserve_wall": 5,
                    "jobs": job_records,
                },
            )
            report_pending["requires_zero_process_exit"] = True
            write_json(directory / "report.json", report_pending)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", type=Path)
    args = parser.parse_args()
    sys.addaudithook(deny_network)
    if args.worker:
        directory = args.worker.resolve()
        job = read_json(directory / "job.json")
        resource.setrlimit(resource.RLIMIT_AS, (512 * MIB, 512 * MIB))
        begun_cpu, begun_wall = time.process_time(), time.monotonic()
        cpu_hard = math.ceil(time.process_time() + job["cpu_limit"]) + 1
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_hard, cpu_hard + 1))
        try:
            with deadline(job["cpu_limit"], job["wall_limit"]):
                result = worker(job, directory)
                result.update(
                    {
                        "cpu_before_result_write": time.process_time() - begun_cpu,
                        "wall_before_result_write": time.monotonic() - begun_wall,
                        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                    }
                )
                write_json(directory / "result.json", result)
        except Exception as exc:
            if not (directory / "result.json").exists():
                status = (
                    "resource_limit"
                    if isinstance(exc, (MemoryError, TimeoutError)) or "resource_limit" in str(exc)
                    else "failed"
                )
                write_json(directory / "result.json", {"status": status, "error": repr(exc)})
            raise
    else:
        require(args.output is not None, "--output is required")
        orchestrate(args.output.resolve())


if __name__ == "__main__":
    main()
