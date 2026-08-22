from __future__ import annotations

import json
import platform
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.model import BrainConfig, EventKind  # noqa: E402
from sparkbrain.spiking import (  # noqa: E402
    LIFConfig,
    SnnTorchLIFHybridBackend,
    run_spiking_scenario,
)
from sparkbrain.visualizer import write_trace  # noqa: E402
from sparkbrain.worlds import SwitchWorld, run_scenario  # noqa: E402

OUTPUT = ROOT / "artifacts/spiking"
EXPECTED = [None, "cat", "cat", "cat", "toy", "toy", "cat"]


def write_utf8_lf(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def distinct(labels: list[str]) -> list[str]:
    result: list[str] = []
    for label in labels:
        if not result or result[-1] != label:
            result.append(label)
    return result


def first_index(predictions: list[str | None], label: str, start: int = 0) -> int | None:
    return next(
        (index for index in range(start, len(predictions)) if predictions[index] == label),
        None,
    )


def main() -> None:
    import snntorch
    import torch

    events = SwitchWorld.canonical_scenario()
    started = time.perf_counter()
    rate, rate_frames = run_scenario(events)
    rate_seconds = time.perf_counter() - started

    started = time.perf_counter()
    spike, spike_frames = run_spiking_scenario(events)
    spike_seconds = time.perf_counter() - started

    negative = SnnTorchLIFHybridBackend(lif_config=LIFConfig(spike_threshold=1.1))
    negative, negative_frames = run_spiking_scenario(events, backend=negative)

    ablated = SnnTorchLIFHybridBackend()
    edge = next(
        edge
        for edge in ablated.connections
        if edge.source == "sensory:plastic_seam" and edge.target == "hypothesis:toy"
    )
    edge.weight = 0.0
    ablated, _ = run_spiking_scenario(events, backend=ablated)

    duplicate = SnnTorchLIFHybridBackend(
        BrainConfig(ignition_threshold=10.0, stability_evaluations=1)
    )
    for target in ("sensory:meow", "sensory:purr"):
        duplicate.schedule(
            time=1.0,
            kind=EventKind.STIMULUS,
            source=target,
            target=target,
            strength=1.0,
            priority=0,
            evidence_id="same-id",
            evidence_label="cat",
            metadata={"sensor": target.removeprefix("sensory:"), "origin_kind": "external"},
        )
    duplicate.run()
    duplicate_diversity = next(
        item.diversity
        for item in duplicate.last_coalitions
        if item.hypothesis_id == "hypothesis:cat"
    )

    rate_predictions = [frame.prediction for frame in rate_frames]
    spike_predictions = [frame.prediction for frame in spike_frames]
    rate_labels = distinct([item.label for item in rate.ignitions])
    spike_labels = distinct([item.label for item in spike.ignitions])
    rate_toy = first_index(rate_predictions, "toy")
    spike_toy = first_index(spike_predictions, "toy")
    rate_recovery = first_index(rate_predictions, "cat", start=(rate_toy or 0) + 1)
    spike_recovery = first_index(spike_predictions, "cat", start=(spike_toy or 0) + 1)
    ablated_toy = [item.time for item in ablated.ignitions if item.label == "toy"]
    control_toy = [item.time for item in spike.ignitions if item.label == "toy"]

    checks = {
        "exact_prediction_sequence": spike_predictions == EXPECTED,
        "exact_distinct_ignitions": spike_labels == ["cat", "toy", "cat"],
        "first_event_no_ignition": spike_predictions[0] is None,
        "switch_latency_within_one": abs((spike_toy or 0) - (rate_toy or 0)) <= 1,
        "recovery_latency_within_one": (
            rate_recovery is not None
            and spike_recovery is not None
            and abs(spike_recovery - rate_recovery) <= 1
        ),
        "final_recovery": spike_predictions[-1] == "cat",
        "workspace_capacity": all(
            len(frame.workspace) <= spike.config.workspace_slots for frame in spike_frames
        ),
        "duplicate_diversity_exact": duplicate_diversity == 1,
        "edge_ablation_direction": (
            len(ablated_toy) <= len(control_toy)
            and (not ablated_toy or ablated_toy[0] >= control_toy[0])
        ),
    }
    payload = {
        "schema": "c07-spiking-comparison-v1",
        "seed": 7,
        "backend_boundary": (
            "snnTorch LIF sensory encoding; rate evidence graph, hypothesis state, "
            "Coalition, ignition, and Workspace"
        ),
        "versions": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "snntorch": snntorch.__version__,
            "device": "cpu",
        },
        "lif_config": asdict(spike.lif_config),
        "tolerances_frozen_before_comparison": {
            "predictions": EXPECTED,
            "distinct_ignitions": ["cat", "toy", "cat"],
            "switch_and_recovery_index_delta_max": 1,
            "duplicate_diversity": 1,
            "workspace_capacity": spike.config.workspace_slots,
            "edge_ablation": "TOY no earlier and count no greater",
        },
        "rate": {
            "predictions": rate_predictions,
            "distinct_ignitions": rate_labels,
            "stats": asdict(rate.stats),
            "wall_clock_seconds": rate_seconds,
        },
        "spiking": {
            "predictions": spike_predictions,
            "distinct_ignitions": spike_labels,
            "stats": asdict(spike.stats),
            "spikes": spike.spike_count,
            "messages": spike.message_count,
            "raw_spike_events": spike.spike_events,
            "wall_clock_seconds": spike_seconds,
        },
        "checks": checks,
        "negative_result": {
            "condition": "spike_threshold=1.1 with unit currents",
            "predictions": [frame.prediction for frame in negative_frames],
            "interpretation": (
                "No sensory spikes and no beliefs; equivalence is parameter-sensitive."
            ),
        },
        "edge_ablation": {
            "removed": "sensory:plastic_seam -> hypothesis:toy",
            "control_toy_ignitions": control_toy,
            "ablated_toy_ignitions": ablated_toy,
        },
        "duplicate_evidence": {"evidence_id": "same-id", "diversity": duplicate_diversity},
        "claim_boundary": (
            "Activity and local runtime are separate descriptive measurements. "
            "They do not measure or imply energy efficiency."
        ),
    }
    if not all(checks.values()):
        raise SystemExit(f"C07 comparison failed frozen tolerances: {checks}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_utf8_lf(
        OUTPUT / "c07_comparison.json",
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )
    write_trace(rate, OUTPUT / "rate_trace.json")
    write_trace(spike, OUTPUT / "spike_trace.json")
    report = f"""# C07 Rate-to-Spiking Comparison

Generated by `python scripts/run_spiking_comparison.py`.

## Result

- Frozen behavioral checks: {sum(checks.values())}/{len(checks)} passed.
- Rate predictions: `{rate_predictions}`
- Hybrid predictions: `{spike_predictions}`
- Hybrid spikes/messages: {spike.spike_count}/{spike.message_count}
- Rate local CPU wall-clock: {rate_seconds:.6f} seconds
- Hybrid local CPU wall-clock: {spike_seconds:.6f} seconds

## Boundary and negative result

This is an snnTorch LIF sensory encoder with rate/algorithmic hypothesis, Coalition,
ignition, and Workspace logic. It is not fully spiking. Raising the fixed LIF threshold
to 1.1 produced no sensory spikes and no predictions, showing parameter-sensitive failure.

Activity counts and wall-clock are reported separately. Neither is a physical-energy
measurement and no energy-efficiency conclusion is permitted.
"""
    write_utf8_lf(OUTPUT / "c07_report.md", report)
    print(f"C07 frozen checks: {sum(checks.values())}/{len(checks)} PASS")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
