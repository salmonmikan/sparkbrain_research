from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

pytest.importorskip("torch")
pytest.importorskip("snntorch")

from sparkbrain.model import BrainConfig, EventKind  # noqa: I001
from sparkbrain.protocols import BrainBackend
from sparkbrain.spiking import LIFConfig, SnnTorchLIFHybridBackend, run_spiking_scenario
from sparkbrain.visualizer import write_trace
from sparkbrain.worlds import SwitchWorld


EXPECTED = [None, "cat", "cat", "cat", "toy", "toy", "cat"]


def distinct_ignitions(backend: SnnTorchLIFHybridBackend) -> list[str]:
    labels: list[str] = []
    for ignition in backend.ignitions:
        if not labels or labels[-1] != ignition.label:
            labels.append(ignition.label)
    return labels


def test_backend_conforms_to_c01_protocol_and_frozen_canonical_contract() -> None:
    backend, frames = run_spiking_scenario(SwitchWorld.canonical_scenario())
    assert isinstance(backend, BrainBackend)
    assert [frame.prediction for frame in frames] == EXPECTED
    assert distinct_ignitions(backend) == ["cat", "toy", "cat"]
    assert frames[0].prediction is None
    assert frames[-1].prediction == "cat"
    assert backend.spike_count == 7
    assert backend.message_count == 7
    assert backend.stats.events_processed > backend.lif_steps
    assert all(len(frame.workspace) <= backend.config.workspace_slots for frame in frames)


def test_duplicate_evidence_keeps_one_independent_support() -> None:
    backend = SnnTorchLIFHybridBackend(
        BrainConfig(ignition_threshold=10.0, stability_evaluations=1)
    )
    for target in ("sensory:meow", "sensory:purr"):
        backend.schedule(
            time=1.0,
            kind=EventKind.STIMULUS,
            source=target,
            target=target,
            strength=1.0,
            priority=0,
            evidence_id="same-id",
            evidence_label="cat",
            metadata={
                "sensor": target.removeprefix("sensory:"),
                "origin_kind": "external",
            },
        )
    backend.run()
    coalition = next(
        item for item in backend.last_coalitions if item.hypothesis_id == "hypothesis:cat"
    )
    assert coalition.diversity == 1


def test_workspace_capacity_one_and_inspection_non_interference() -> None:
    backend = SnnTorchLIFHybridBackend(BrainConfig(workspace_slots=1))
    backend, _ = run_spiking_scenario(SwitchWorld.canonical_scenario(), backend=backend)
    before = deepcopy(backend.state_dict())
    backend.inspect_snapshot(external_event="inspection", truth="cat")
    after = backend.state_dict()
    before["cpu_seconds"] = after["cpu_seconds"]
    assert before == after
    assert len(backend.workspace) == 1
    assert backend.workspace[0].label == "cat"


def test_edge_ablation_has_predeclared_direction() -> None:
    control, _ = run_spiking_scenario(SwitchWorld.canonical_scenario())
    ablated = SnnTorchLIFHybridBackend()
    edge = next(
        edge
        for edge in ablated.connections
        if edge.source == "sensory:plastic_seam" and edge.target == "hypothesis:toy"
    )
    edge.weight = 0.0
    ablated, _ = run_spiking_scenario(SwitchWorld.canonical_scenario(), backend=ablated)
    control_toy = [item.time for item in control.ignitions if item.label == "toy"]
    ablated_toy = [item.time for item in ablated.ignitions if item.label == "toy"]
    assert len(ablated_toy) <= len(control_toy)
    assert not ablated_toy or ablated_toy[0] >= control_toy[0]


def test_backend_state_round_trip_and_high_threshold_negative_result() -> None:
    backend, _ = run_spiking_scenario(SwitchWorld.canonical_scenario()[:3])
    restored = SnnTorchLIFHybridBackend()
    restored.load_state_dict(backend.state_dict())
    assert restored.state_dict()["engine_state"] == backend.state_dict()["engine_state"]

    negative = SnnTorchLIFHybridBackend(lif_config=LIFConfig(spike_threshold=1.1))
    _, frames = run_spiking_scenario(SwitchWorld.canonical_scenario(), backend=negative)
    assert all(frame.prediction is None for frame in frames)


def _schedule_subthreshold_pair(
    backend: SnnTorchLIFHybridBackend, times: tuple[float, float]
) -> None:
    for index, event_time in enumerate(times):
        backend.schedule(
            time=event_time,
            kind=EventKind.STIMULUS,
            source="ordering-test",
            target="sensory:fur",
            strength=0.6,
            priority=0,
            evidence_id=f"ordered:{index}",
            evidence_label="fur",
            metadata={"origin_kind": "external", "sensor": "fur"},
        )


def test_lif_encoding_follows_event_time_not_schedule_call_order() -> None:
    future_first = SnnTorchLIFHybridBackend()
    _schedule_subthreshold_pair(future_first, (2.0, 1.0))
    assert future_first.spike_events == []
    future_first.run()

    chronological = SnnTorchLIFHybridBackend()
    _schedule_subthreshold_pair(chronological, (1.0, 2.0))
    chronological.run()

    assert [row["time"] for row in future_first.spike_events] == [2.0]
    assert future_first.spike_events == chronological.spike_events


@pytest.mark.parametrize(
    ("first_priority", "second_priority", "expected_spiking_current"),
    [(0, 1, 0.55), (1, 0, 0.65)],
)
def test_equal_time_lif_encoding_follows_priority_then_sequence(
    first_priority: int,
    second_priority: int,
    expected_spiking_current: float,
) -> None:
    backend = SnnTorchLIFHybridBackend()
    for strength, priority in ((0.65, first_priority), (0.55, second_priority)):
        backend.schedule(
            time=1.0,
            kind=EventKind.STIMULUS,
            source="ordering-test",
            target="sensory:fur",
            strength=strength,
            priority=priority,
            evidence_id=f"priority:{priority}:{strength}",
            evidence_label="fur",
            metadata={"origin_kind": "external", "sensor": "fur"},
        )
    backend.run()
    assert [row["input_current"] for row in backend.spike_events] == [
        expected_spiking_current
    ]

    same_priority = SnnTorchLIFHybridBackend()
    for strength in (0.55, 0.65):
        same_priority.schedule(
            time=1.0,
            kind=EventKind.STIMULUS,
            source="ordering-test",
            target="sensory:fur",
            strength=strength,
            priority=0,
            evidence_id=f"sequence:{strength}",
            evidence_label="fur",
            metadata={"origin_kind": "external", "sensor": "fur"},
        )
    same_priority.run()
    assert [row["input_current"] for row in same_priority.spike_events] == [0.65]


def test_pending_lif_events_checkpoint_and_continue_identically() -> None:
    original = SnnTorchLIFHybridBackend()
    _schedule_subthreshold_pair(original, (1.0, 2.0))
    with pytest.raises(RuntimeError, match="Event limit exceeded"):
        original.run(max_events=1)
    assert original.spike_events == []
    assert original.membrane["sensory:fur"] == pytest.approx(0.6)
    checkpoint = original.state_dict()

    restored = SnnTorchLIFHybridBackend()
    restored.load_state_dict(checkpoint)
    original.run()
    restored.run()

    restored.cpu_seconds = original.cpu_seconds
    assert restored.state_dict() == original.state_dict()


def test_reset_clears_hybrid_and_engine_episode_state() -> None:
    backend, _ = run_spiking_scenario(SwitchWorld.canonical_scenario()[:2])
    backend.reset(seed=19)
    state = backend.state_dict()
    assert state["membrane"] == {}
    assert state["filtered_spikes"] == {}
    assert state["spike_events"] == []
    assert state["spike_count"] == state["message_count"] == state["lif_steps"] == 0
    assert state["engine_state"]["config"]["random_seed"] == 19
    assert state["engine_state"]["queue"] == []
    assert state["engine_state"]["trace"] == []


def test_spiking_trace_export_validates_against_c01_schema(tmp_path) -> None:
    backend, _ = run_spiking_scenario(SwitchWorld.canonical_scenario())
    output = write_trace(backend, tmp_path / "spike_trace.json")
    payload = json.loads(output.read_text(encoding="utf-8"))
    schema = json.loads(Path("schemas/trace-v0.2.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
