from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from sparkbrain.v03 import V03BrainConfig
from sparkbrain.v03_seed import SensorySample

from .models import (
    ComparisonRequest,
    CreateRunRequest,
    ImportRunRequest,
    InjectEventRequest,
    InterventionRequest,
    V03CreateRunRequest,
    V03EvidenceRemovalRequest,
    V03SampleRequest,
)
from .service import LabManager
from .v03_service import V03LabManager

PACKAGE_STATIC = Path(__file__).with_name("static")


def create_app(*, artifact_root: str | Path = "artifacts/brain_lab/runs") -> FastAPI:
    manager = LabManager(artifact_root)
    v03_manager = V03LabManager()
    app = FastAPI(
        title="SparkBrain Local Brain Lab",
        version="0.1",
        docs_url="/api/docs",
        redoc_url=None,
    )
    app.state.manager = manager
    app.state.v03_manager = v03_manager

    def run_or_404(run_id: str):
        try:
            return manager.get(run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def v03_run_or_404(run_id: str):
        try:
            return v03_manager.get(run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok", "bind_policy": "127.0.0.1", "remote_services": False}

    @app.post("/api/runs", status_code=201)
    def create_run(request: CreateRunRequest) -> dict:
        return manager.create_run(seed=request.seed, blind=request.blind).public_state()

    @app.get("/api/runs")
    def list_runs() -> list[dict]:
        return [run.public_state() for run in manager.runs.values()]

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict:
        return run_or_404(run_id).public_state()

    @app.post("/api/runs/{run_id}/step")
    def step(run_id: str) -> dict:
        return run_or_404(run_id).step()

    @app.post("/api/runs/{run_id}/run")
    def run_remaining(run_id: str) -> dict:
        return run_or_404(run_id).run_remaining()

    @app.post("/api/runs/{run_id}/pause")
    def pause(run_id: str) -> dict:
        return run_or_404(run_id).pause()

    @app.post("/api/runs/{run_id}/reset")
    def reset(run_id: str) -> dict:
        return run_or_404(run_id).reset()

    @app.post("/api/runs/{run_id}/events")
    def inject(run_id: str, request: InjectEventRequest) -> dict:
        try:
            return run_or_404(run_id).inject(
                target=request.target,
                label=request.label,
                strength=request.strength,
                event_time=request.time,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/runs/{run_id}/fork", status_code=201)
    def fork(run_id: str, request: InterventionRequest) -> dict:
        run_or_404(run_id)
        try:
            return manager.fork(run_id, request.model_dump()).public_state()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/comparisons")
    def compare(request: ComparisonRequest) -> dict:
        try:
            return manager.compare(request.left_run_id, request.right_run_id, request.cursor)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/runs/{run_id}/export")
    def export(run_id: str) -> dict:
        run_or_404(run_id)
        try:
            bundle, path = manager.write_export(run_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {"path": str(path), "bundle": bundle}

    @app.post("/api/import", status_code=201)
    def import_run(request: ImportRunRequest) -> dict:
        try:
            return manager.import_bundle(request.bundle).public_state()
        except (KeyError, TypeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/api/runs/{run_id}/events/stream")
    def stream(run_id: str) -> StreamingResponse:
        run = run_or_404(run_id)

        def current_frame():
            payload = {
                "type": "frame",
                "run_id": run.run_id,
                "event_index": run.event_index,
                "state": run.public_state(),
            }
            yield f"event: frame\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"

        return StreamingResponse(current_frame(), media_type="text/event-stream")

    @app.post("/api/v03/runs", status_code=201)
    def create_v03_run(request: V03CreateRunRequest) -> dict:
        try:
            config = V03BrainConfig(**request.model_dump())
            return v03_manager.create_run(config).public_state()
        except (NotImplementedError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/api/v03/runs")
    def list_v03_runs() -> list[dict]:
        return [run.public_state() for run in v03_manager.runs.values()]

    @app.get("/api/v03/runs/{run_id}")
    def get_v03_run(run_id: str) -> dict:
        return v03_run_or_404(run_id).public_state()

    def v03_step_response(run_id: str, request: V03SampleRequest) -> dict:
        try:
            sample = SensorySample(
                sample_id=request.sample_id,
                time=request.time,
                source_id=request.source_id,
                modality=request.modality,
                values=request.values,
                correlation_group=request.correlation_group,
                entity_hint=request.entity_hint,
                metadata=request.metadata,
                omitted_channels=tuple(request.omitted_channels),
            )
            return v03_run_or_404(run_id).step(
                sample,
                goal_bias=request.goal_bias,
                world_feedback=request.world_feedback,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/v03/runs/{run_id}/step")
    def step_v03(run_id: str, request: V03SampleRequest) -> dict:
        return v03_step_response(run_id, request)

    @app.post("/api/v03/runs/{run_id}/events")
    def inject_v03(run_id: str, request: V03SampleRequest) -> dict:
        return v03_step_response(run_id, request)

    @app.post("/api/v03/runs/{run_id}/pause")
    def pause_v03(run_id: str) -> dict:
        return v03_run_or_404(run_id).pause()

    @app.post("/api/v03/runs/{run_id}/reset")
    def reset_v03(run_id: str) -> dict:
        return v03_run_or_404(run_id).reset()

    @app.post("/api/v03/runs/{run_id}/fork", status_code=201)
    def fork_v03(run_id: str, request: V03EvidenceRemovalRequest) -> dict:
        v03_run_or_404(run_id)
        try:
            return v03_manager.fork_with_evidence_removal(
                run_id,
                evidence_id=request.evidence_id,
                at_time=request.time,
                reason=request.reason,
            ).public_state()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/v03/comparisons")
    def compare_v03(request: ComparisonRequest) -> dict:
        try:
            return v03_manager.compare(request.left_run_id, request.right_run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(PACKAGE_STATIC / "index.html")

    app.mount("/static", StaticFiles(directory=PACKAGE_STATIC), name="static")
    return app


app = create_app()
