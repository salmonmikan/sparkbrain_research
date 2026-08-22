from __future__ import annotations

import json

from fastapi.testclient import TestClient

from sparkbrain.lab.app import create_app
from sparkbrain.serialization import state_hash


def client(tmp_path) -> TestClient:
    return TestClient(create_app(artifact_root=tmp_path))


def test_api_schema_validation_and_unknown_ids(tmp_path) -> None:
    with client(tmp_path) as api:
        created = api.post("/api/runs", json={"seed": 7, "unknown": True})
        assert created.status_code == 422
        run = api.post("/api/runs", json={"seed": 7}).json()
        invalid = api.post(
            f"/api/runs/{run['run_id']}/events",
            json={"target": "missing", "label": "x", "strength": 1.0},
        )
        assert invalid.status_code == 422


def test_blind_mode_prevents_truth_leakage_across_api_and_export(tmp_path) -> None:
    with client(tmp_path) as api:
        run = api.post("/api/runs", json={"blind": True}).json()
        final = api.post(f"/api/runs/{run['run_id']}/run").json()
        assert all(frame["truth"] is None for frame in final["trace"])
        exported = api.post(f"/api/runs/{run['run_id']}/export").json()["bundle"]
        serialized = json.dumps(exported)
        assert '"truth": "cat"' not in serialized
        assert '"truth": "toy"' not in serialized


def test_sse_reconnect_does_not_mutate_run(tmp_path) -> None:
    app = create_app(artifact_root=tmp_path)
    with TestClient(app) as api:
        run = api.post("/api/runs", json={}).json()
        run_id = run["run_id"]
        managed = app.state.manager.get(run_id)
        before = state_hash(managed.brain)
        response = api.get(f"/api/runs/{run_id}/events/stream")
        assert response.status_code == 200
        assert "event: frame" in response.text
        assert state_hash(managed.brain) == before


def test_export_import_api_round_trip(tmp_path) -> None:
    with client(tmp_path) as api:
        run = api.post("/api/runs", json={}).json()
        run = api.post(f"/api/runs/{run['run_id']}/run").json()
        exported = api.post(f"/api/runs/{run['run_id']}/export").json()
        restored = api.post("/api/import", json={"bundle": exported["bundle"]})
        assert restored.status_code == 201
        assert restored.json()["prediction"] == "cat"
        assert restored.json()["event_index"] == 7


def test_loopback_health_contract(tmp_path) -> None:
    with client(tmp_path) as api:
        health = api.get("/api/health").json()
        assert health == {"status": "ok", "bind_policy": "127.0.0.1", "remote_services": False}
