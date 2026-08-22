from __future__ import annotations

from sparkbrain.lab.service import LabManager, prepare_relevant_graph
from sparkbrain.serialization import state_hash


def test_pause_step_reset_is_deterministic(tmp_path) -> None:
    manager = LabManager(tmp_path)
    run = manager.create_run(seed=17)
    initial_hash = state_hash(run.brain)
    assert run.pause()["status"] == "paused"
    assert state_hash(run.brain) == initial_hash

    first = run.step()["current_frame"]
    run.reset()
    assert state_hash(run.brain) == initial_hash
    repeated = run.step()["current_frame"]
    assert repeated == first


def test_intervention_fork_preserves_parent_and_changes_behavior(tmp_path) -> None:
    manager = LabManager(tmp_path)
    parent = manager.create_run()
    for _ in range(3):
        parent.step()
    parent_hash = state_hash(parent.brain)
    parent_trace = list(parent.brain.trace)

    child = manager.fork(
        parent.run_id,
        {
            "kind": "ablate_edge",
            "source": "sensory:plastic_seam",
            "target": "hypothesis:toy",
            "value": None,
        },
    )
    assert child.parent_run_id == parent.run_id
    assert child.fork_base_hash == parent_hash
    assert state_hash(parent.brain) == parent_hash
    assert parent.brain.trace == parent_trace

    parent.run_remaining()
    child.run_remaining()
    parent_predictions = [frame.prediction for frame in parent.brain.trace]
    child_predictions = [frame.prediction for frame in child.brain.trace]
    assert parent_predictions != child_predictions
    assert parent_predictions[4] == "toy"
    assert child_predictions[4] != "toy"


def test_comparison_is_synchronized_and_future_safe(tmp_path) -> None:
    manager = LabManager(tmp_path)
    left = manager.create_run()
    right = manager.create_run()
    for _ in range(3):
        left.step()
        right.step()
    result = manager.compare(left.run_id, right.run_id, cursor=99)
    assert result["synchronized"] is True
    assert result["cursor"] == 2
    assert result["left"]["time"] == result["right"]["time"]


def test_export_import_round_trip_and_blind_sanitization(tmp_path) -> None:
    manager = LabManager(tmp_path)
    visible = manager.create_run(blind=False)
    visible.run_remaining()
    visible_export = visible.export_bundle()
    visible_restored = manager.import_bundle(visible_export)
    assert state_hash(visible_restored.brain) == state_hash(visible.brain)
    assert visible_restored.export_bundle()["trace"] == visible_export["trace"]

    run = manager.create_run(blind=True)
    run.run_remaining()
    exported, path = manager.write_export(run.run_id)
    assert path.is_file()
    assert all(frame["truth"] is None for frame in exported["trace"])
    assert all(frame["truth"] is None for frame in exported["checkpoint"]["trace"])

    restored = manager.import_bundle(exported)
    assert state_hash(restored.brain) != state_hash(run.brain)
    assert restored.brain.prediction == run.brain.prediction
    assert restored.event_index == run.event_index


def test_relevant_subset_never_invents_ids() -> None:
    graph = {
        "nodes": [{"id": f"s{index}"} for index in range(10)],
        "edges": [{"source": "s0", "target": "s1", "weight": 1.0}],
    }
    subset = prepare_relevant_graph(
        graph,
        {"fired": ["s9"], "sparks": [{"id": "s9", "activation": 1.0}]},
        node_limit=3,
    )
    source_ids = {row["id"] for row in graph["nodes"]}
    assert {row["id"] for row in subset["nodes"]} <= source_ids
    assert subset["nodes"][0]["id"] == "s9"


def test_large_graph_relevant_subset_meets_preparation_budget(tmp_path) -> None:
    result = LabManager(tmp_path).performance_sample()
    assert result["source_nodes"] == 2_000
    assert result["source_edges"] == 10_000
    assert result["render_nodes"] <= 250
    assert result["render_edges"] <= 600
    assert result["within_prepare_budget"] is True
