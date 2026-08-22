# ruff: noqa: E402 -- skip optional learned/structural modules before importing them.
from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sparkbrain.model import EventKind
from sparkbrain.protocols import BrainBackend
from sparkbrain.structural.backend import StructuralBrainBackend
from sparkbrain.structural.config import StructuralConfig
from sparkbrain.structural.contracts import StructuralStats
from sparkbrain.structural.controller import StructuralController
from sparkbrain.structural.experiment import _specificity_gate

CHECKPOINT = Path("artifacts/phase2/learned-routing-v1/main/checkpoint.pt")


def config(**changes) -> StructuralConfig:
    values = {
        "seed": 83,
        "source_modules": 12,
        "max_modules": 16,
        "max_active_edges": 80,
        "active_k": 4,
        "max_events_per_boundary": 10,
        "max_events_total": 30,
        **changes,
    }
    return StructuralConfig(**values)


def backend(**changes) -> StructuralBrainBackend:
    return StructuralBrainBackend.from_c04_checkpoint(CHECKPOINT, config(**changes))


def inject(brain: StructuralBrainBackend, evidence: str = "meow", time: float = 1.0) -> None:
    brain.schedule(
        time=time,
        kind=EventKind.STIMULUS,
        source="sensor:test",
        target=None,
        strength=1.0,
        evidence_id=f"e:{time}",
        evidence_label=evidence,
    )
    brain.run()


def empty_stats(size: int) -> StructuralStats:
    return StructuralStats(
        [0.0] * size,
        [[0.0] * size for _ in range(size)],
        [[0.0] * size for _ in range(size)],
        [0.0] * size,
    )


def test_structural_backend_satisfies_c01_and_counts_actual_edges() -> None:
    brain = backend()
    assert isinstance(brain, BrainBackend)
    inject(brain)
    record = brain.prediction_record()
    assert len(record.selected_modules) == brain.structural_config.active_k
    assert brain.work.evaluated_edges == len(record.evidence_path)
    assert brain.work.evaluated_edges <= brain.structural_config.active_k**2
    assert brain.work.state_updates == brain.structural_config.active_k


def test_fixed_capacity_never_resizes_parameter_tensors() -> None:
    brain = backend()
    shapes = {key: tuple(value.shape) for key, value in brain.structural_model.state_dict().items()}
    brain.controller.queue_event(boundary=1, kind="duplicate", source_slot=0, target_slot=12)
    brain.apply_boundary(1)
    after = {
        key: tuple(value.shape) for key, value in brain.structural_model.state_dict().items()
    }
    assert after == shapes
    assert int(brain.structural_model.active_module_mask.sum()) == 13


def test_all_structural_event_kinds_have_bounded_effects() -> None:
    brain = backend()
    controller = brain.controller
    controller.queue_event(boundary=1, kind="create", target_slot=12)
    controller.apply_boundary(1)
    controller.queue_event(boundary=2, kind="duplicate", source_slot=0, target_slot=13)
    controller.apply_boundary(2)
    controller.queue_event(boundary=3, kind="split", source_slot=1, target_slot=14)
    controller.apply_boundary(3)
    controller.queue_event(boundary=4, kind="edge_grow", source_slot=0, target_slot=2)
    controller.apply_boundary(4)
    controller.queue_event(boundary=5, kind="edge_prune", source_slot=2, target_slot=3)
    controller.apply_boundary(5)
    controller.queue_event(boundary=6, kind="merge", source_slot=0, target_slot=1)
    controller.apply_boundary(6)
    controller.queue_event(boundary=7, kind="module_prune", source_slot=3)
    controller.apply_boundary(7)
    assert {event.kind for event in controller.history if event.status == "applied"} == {
        "create",
        "duplicate",
        "split",
        "merge",
        "edge_grow",
        "edge_prune",
        "module_prune",
    }
    assert (
        int(brain.structural_model.active_module_mask.sum())
        <= brain.structural_config.max_modules
    )
    assert (
        int(brain.structural_model.active_edge_mask.sum())
        <= brain.structural_config.max_active_edges
    )
    assert any(row.tombstone_reason == "merged" for row in controller.tombstones)


def test_boundary_priority_and_sequence_are_deterministic() -> None:
    first = backend()
    second = backend()
    for brain in (first, second):
        brain.controller.queue_event(
            boundary=1, kind="duplicate", source_slot=0, target_slot=12
        )
        brain.controller.queue_event(boundary=1, kind="edge_prune", source_slot=2, target_slot=3)
        brain.apply_boundary(1)
    assert [event.kind for event in first.controller.history] == ["edge_prune", "duplicate"]
    assert [event.to_dict() for event in first.controller.history] == [
        event.to_dict() for event in second.controller.history
    ]
    assert torch.equal(
        first.structural_model.active_module_mask, second.structural_model.active_module_mask
    )


def test_split_rng_is_seed_deterministic() -> None:
    first = backend()
    second = backend()
    for brain in (first, second):
        brain.controller.queue_event(boundary=1, kind="split", source_slot=0, target_slot=12)
        brain.apply_boundary(1)
    assert torch.equal(
        first.structural_model.router.weight[12], second.structural_model.router.weight[12]
    )


def test_event_and_capacity_budgets_reject_without_partial_mutation() -> None:
    brain = backend(max_events_total=1, max_events_per_boundary=1)
    brain.controller.queue_event(boundary=1, kind="create", target_slot=12)
    brain.controller.queue_event(boundary=1, kind="create", target_slot=13)
    brain.apply_boundary(1)
    assert brain.controller.events_applied == 1
    assert brain.controller.events_rejected == 1
    assert int(brain.structural_model.active_module_mask.sum()) == 13
    assert any(event.rejection == "boundary_budget" for event in brain.controller.history)


def test_discovery_contract_has_no_world_function_or_truth_fields() -> None:
    names = set(StructuralStats.__dataclass_fields__)
    assert names == {"routing_load", "coactivation", "edge_credit", "confidence_delta"}
    brain = backend()
    stats = empty_stats(brain.structural_config.max_modules)
    stats.routing_load[0] = 100.0
    queued = brain.controller.discover(stats, next_boundary=1)
    assert queued
    assert all("world" not in event.reason and "truth" not in event.reason for event in queued)


def test_candidate_group_is_multiplicity_preserving_and_label_free() -> None:
    brain = backend()
    stats = empty_stats(brain.structural_config.max_modules)
    stats.routing_load[2] = 5.0
    stats.routing_load[5] = 4.0
    assert brain.controller.candidate_group(stats, size=2) == (2, 5)


def test_homeostasis_reduces_overloaded_router_bias() -> None:
    brain = backend()
    stats = empty_stats(brain.structural_config.max_modules)
    stats.routing_load[:12] = [1.0] * 12
    stats.routing_load[0] = 12.0
    before = float(brain.structural_model.router.bias[0].detach())
    brain.controller.apply_homeostasis(stats)
    assert float(brain.structural_model.router.bias[0].detach()) < before
    assert brain.controller.homeostatic_updates == 1


def test_optional_reward_eligibility_is_explicit() -> None:
    disabled = backend()
    disabled.apply_reward_eligibility(1.0)
    assert sum(map(sum, disabled.structural_stats().edge_credit)) == 0.0
    enabled = backend(reward_eligibility=True)
    enabled.apply_reward_eligibility(1.0)
    assert sum(map(sum, enabled.structural_stats().edge_credit)) > 0.0


def test_checkpoint_restores_pending_events_rng_optimizer_and_runtime_queue() -> None:
    original = backend()
    inject(original)
    original.controller.queue_event(boundary=2, kind="split", source_slot=0, target_slot=12)
    original.schedule(
        time=2.0,
        kind=EventKind.STIMULUS,
        source="sensor:pending",
        target=None,
        evidence_id="pending",
        evidence_label="bark",
        strength=1.0,
    )
    optimizer = torch.optim.Adam(original.structural_model.parameters(), lr=0.0)
    original.optimizer_state = optimizer.state_dict()
    payload = json.loads(json.dumps(original.state_dict()))
    restored = backend()
    restored.load_state_dict(payload)
    assert restored.controller.state_dict() == original.controller.state_dict()
    assert restored.optimizer_state == json.loads(json.dumps(original.optimizer_state))
    original.apply_boundary(2)
    restored.apply_boundary(2)
    original.run()
    restored.run()
    assert restored.prediction_record() == original.prediction_record()
    original_frame = asdict(original.inspect_snapshot(external_event="same"))
    restored_frame = asdict(restored.inspect_snapshot(external_event="same"))
    original_frame["stats"].pop("wall_clock_seconds")
    restored_frame["stats"].pop("wall_clock_seconds")
    assert restored_frame == original_frame


def test_controller_rejects_duplicate_pending_sequence_on_load() -> None:
    brain = backend()
    brain.controller.queue_event(boundary=1, kind="create", target_slot=12)
    brain.controller.queue_event(boundary=2, kind="create", target_slot=13)
    state = brain.controller.state_dict()
    state["pending"][1]["sequence"] = state["pending"][0]["sequence"]
    with pytest.raises(ValueError, match="unique"):
        StructuralController(brain.structural_config, brain.structural_model).load_state_dict(state)


def test_minimum_module_and_degree_safeguards() -> None:
    brain = backend(min_live_modules=12)
    brain.controller.queue_event(boundary=1, kind="module_prune", source_slot=0)
    brain.apply_boundary(1)
    assert brain.controller.history[0].rejection == "minimum_modules"
    isolated = backend()
    isolated.structural_model.active_edge_mask[:, 0] = False
    isolated.structural_model.active_edge_mask[0, 0] = True
    isolated.controller.queue_event(boundary=1, kind="edge_prune", source_slot=0, target_slot=0)
    isolated.apply_boundary(1)
    assert isolated.controller.history[0].rejection == "minimum_in_degree"


def test_structural_config_round_trip_and_validation() -> None:
    value = config()
    assert StructuralConfig.from_dict(value.to_dict()) == value
    with pytest.raises(ValueError):
        replace(value, max_modules=10).validate()


def test_checkpoint_rejects_structural_config_mismatch() -> None:
    original = backend()
    payload = original.state_dict()
    restored = backend(homeostasis_rate=0.01)
    with pytest.raises(ValueError, match="config"):
        restored.load_state_dict(payload)


def test_specificity_gate_fixes_target_on_dev_and_caps_test_collateral() -> None:
    passed = _specificity_gate(
        {"target": 0.2, "other": 0.05},
        {"target": 0.1, "other": 0.01},
        target_minimum=0.05,
        collateral_maximum=0.02,
    )
    assert passed["passed"] is True
    assert passed["dev_target_world"] == "target"
    collateral_failure = _specificity_gate(
        {"target": 0.2, "other": 0.05},
        {"target": 0.1, "other": 0.03},
        target_minimum=0.05,
        collateral_maximum=0.02,
    )
    assert collateral_failure["passed"] is False


def test_specificity_gate_fails_closed_without_unique_dev_target() -> None:
    tied = _specificity_gate(
        {"first": 0.2, "second": 0.2},
        {"first": 0.3, "second": 0.0},
        target_minimum=0.05,
        collateral_maximum=0.02,
    )
    assert tied["passed"] is False
    assert tied["dev_target_world"] is None
