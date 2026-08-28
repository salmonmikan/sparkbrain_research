from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from sparkbrain.lab.app import create_app
from sparkbrain.v03 import V03BrainConfig


def client(tmp_path) -> TestClient:
    return TestClient(create_app(artifact_root=tmp_path))


def _sample(*, sample_id: str = "lab:0", omitted: bool = False) -> dict:
    return {
        "sample_id": sample_id,
        "time": 0.0,
        "source_id": "local-brain-lab",
        "modality": "fixture",
        "values": {} if omitted else {"tone": 1.0},
        "metadata": {"text": "local stable target"},
        "omitted_channels": ["tone"] if omitted else [],
    }


def test_v03_brain_lab_observes_live_runtime_trace_and_boundaries(tmp_path) -> None:
    with client(tmp_path) as api:
        created = api.post("/api/v03/runs", json={})
        assert created.status_code == 201
        run = created.json()
        assert len(run["run_id"]) == 32
        assert api.post("/api/v03/runs", json={}).json()["run_id"] != run["run_id"]
        assert run["backend"] == "integrated-v03-reference"
        assert run["oracle_autonomous_boundary"] == {
            "classification": "autonomous_local_reference",
            "oracle_diagnostic": False,
            "concept_and_organ": "observer_only",
            "c19_status": "blocked",
        }

        first = api.post(f"/api/v03/runs/{run['run_id']}/step", json=_sample())
        assert first.status_code == 200
        stepped = api.post(
            f"/api/v03/runs/{run['run_id']}/step",
            json=_sample(sample_id="lab:1", omitted=True),
        )
        assert stepped.status_code == 200
        observation = stepped.json()["observation"]
        assert observation["runtime_origin"] == "live_integrated_v03_runtime"
        assert observation["raw_input"]["sample_id"] == "lab:1"
        assert observation["ignored_channels"]["channels"] == ["tone"]
        assert observation["runtime_trace"]["event_hashes"]
        for key in (
            "perceptual_sparks",
            "entity_assignments",
            "evidence_ids",
            "coalition_decomposition",
            "no_ignition",
            "beliefs",
            "revision_transitions",
            "concept_candidates",
            "organ_monitor_candidates",
            "action",
            "world_feedback",
        ):
            assert key in observation
        assert observation["organ_monitor_candidates"] == {
            "mode": "observation_only",
            "status": "not_evaluated",
        }


def test_v03_lab_run_id_override_is_explicit_and_collision_safe(tmp_path) -> None:
    app = create_app(artifact_root=tmp_path)
    manager = app.state.v03_manager
    first = manager.create_run(V03BrainConfig(), run_id="fixed-test-run")
    assert first.run_id == "fixed-test-run"
    with pytest.raises(ValueError, match="already exists"):
        manager.create_run(V03BrainConfig(), run_id="fixed-test-run")


def test_v03_oracle_requires_explicit_diagnostic_permission(tmp_path) -> None:
    with client(tmp_path) as api:
        denied = api.post("/api/v03/runs", json={"entity_track": "E1_oracle_entity"})
        assert denied.status_code == 422
        allowed = api.post(
            "/api/v03/runs",
            json={"entity_track": "E1_oracle_entity", "allow_oracle_diagnostics": True},
        )
        assert allowed.status_code == 201
        assert allowed.json()["oracle_autonomous_boundary"]["classification"] == "oracle_diagnostic"
        unavailable = api.post("/api/v03/runs", json={"entity_track": "E2_learned_slots"})
        assert unavailable.status_code == 422


def test_v03_causal_removal_is_an_explicit_non_runtime_trace_fork(tmp_path) -> None:
    with client(tmp_path) as api:
        parent = api.post("/api/v03/runs", json={}).json()
        stepped = api.post(
            f"/api/v03/runs/{parent['run_id']}/events", json=_sample(sample_id="lab:fork")
        ).json()
        evidence_id = stepped["observation"]["evidence_ids"][0]
        child = api.post(
            f"/api/v03/runs/{parent['run_id']}/fork",
            json={"evidence_id": evidence_id, "time": 1.0},
        )
        assert child.status_code == 201
        child_state = child.json()
        removal = child_state["observation"]["causal_evidence_removal"]
        assert child_state["parent_run_id"] == parent["run_id"]
        assert removal["evidence_id"] == evidence_id
        assert removal["before_active_state_hash"] != removal["after_active_state_hash"]
        assert removal["trace_origin"] == "lab_counterfactual_observer_not_runtime_trace"

        compared = api.post(
            "/api/v03/comparisons",
            json={"left_run_id": parent["run_id"], "right_run_id": child_state["run_id"]},
        )
        assert compared.status_code == 200
        assert compared.json()["comparison_origin"] == "lab_observer_not_runtime_trace"


def test_v03_rejects_evaluator_owned_raw_input(tmp_path) -> None:
    with client(tmp_path) as api:
        run = api.post("/api/v03/runs", json={}).json()
        invalid = _sample()
        invalid["metadata"] = {"truth": "forbidden"}
        response = api.post(f"/api/v03/runs/{run['run_id']}/step", json=invalid)
        assert response.status_code == 422
