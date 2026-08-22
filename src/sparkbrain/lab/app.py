from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .models import (
    ComparisonRequest,
    CreateRunRequest,
    ImportRunRequest,
    InjectEventRequest,
    InterventionRequest,
)
from .service import LabManager

PACKAGE_STATIC = Path(__file__).with_name("static")


def create_app(*, artifact_root: str | Path = "artifacts/brain_lab/runs") -> FastAPI:
    manager = LabManager(artifact_root)
    app = FastAPI(
        title="SparkBrain Local Brain Lab",
        version="0.1",
        docs_url="/api/docs",
        redoc_url=None,
    )
    app.state.manager = manager

    def run_or_404(run_id: str):
        try:
            return manager.get(run_id)
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

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(PACKAGE_STATIC / "index.html")

    app.mount("/static", StaticFiles(directory=PACKAGE_STATIC), name="static")
    return app


app = create_app()
