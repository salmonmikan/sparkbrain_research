from __future__ import annotations

from copy import deepcopy

import pytest

pytest.importorskip("torch")
pytest.importorskip("snntorch")

from sparkbrain.model import BrainConfig, EventKind  # noqa: I001
from sparkbrain.protocols import BrainBackend
from sparkbrain.spiking import LIFConfig, SnnTorchLIFHybridBackend, run_spiking_scenario
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
