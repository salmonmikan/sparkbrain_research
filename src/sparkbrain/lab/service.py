from __future__ import annotations

import math
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig
from sparkbrain.serialization import canonical_json, state_hash
from sparkbrain.worlds import SwitchEvent, SwitchWorld, build_reference_brain

MAX_EXTERNAL_EVENTS = 10_000
MAX_EXPORT_BYTES = 25 * 1024 * 1024
IMPORT_TOP_LEVEL_KEYS = {
    "schema_version",
    "lab_version",
    "run",
    "event_manifest",
    "checkpoint",
    "trace",
    "figure_data",
}
IMPORT_RUN_KEYS = {
    "run_id",
    "seed",
    "blind",
    "event_index",
    "status",
    "parent_run_id",
    "intervention_patch",
    "fork_base_hash",
    "injections",
}


def _frame_dict(frame: Any, *, blind: bool) -> dict[str, Any]:
    row = asdict(frame) if not isinstance(frame, dict) else dict(frame)
    if blind:
        row["truth"] = None
    return row


def _blind_sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (None if key == "truth" else _blind_sanitize(child))
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_blind_sanitize(child) for child in value]
    return value


def _require_exact_keys(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{location} keys mismatch: missing={sorted(expected - actual)} "
            f"unknown={sorted(actual - expected)}"
        )
    return value


def _has_visible_truth(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            (key == "truth" and child is not None) or _has_visible_truth(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(_has_visible_truth(child) for child in value)
    return False


def prepare_relevant_graph(
    graph: dict[str, list[dict[str, Any]]],
    frame: dict[str, Any] | None,
    *,
    node_limit: int = 250,
    edge_limit: int = 600,
) -> dict[str, list[dict[str, Any]]]:
    """Return a deterministic active-first subset without touching engine state."""

    active_ids: set[str] = set()
    if frame:
        active_ids.update(frame.get("fired", []))
        active_ids.update(
            row["id"]
            for row in frame.get("sparks", [])
            if abs(float(row.get("activation", 0.0))) > 0.01
        )
        for row in frame.get("workspace", []):
            active_ids.add(str(row.get("hypothesis_id", "")))
    nodes = sorted(
        graph.get("nodes", []),
        key=lambda row: (row.get("id") not in active_ids, str(row.get("id"))),
    )[:node_limit]
    node_ids = {str(row["id"]) for row in nodes}
    edges = [
        row
        for row in graph.get("edges", [])
        if row.get("source") in node_ids and row.get("target") in node_ids
    ][:edge_limit]
    return {"nodes": nodes, "edges": edges}


@dataclass(slots=True)
class LabRun:
    run_id: str
    seed: int
    blind: bool
    brain: SparkBrain
    manifest: list[SwitchEvent]
    event_index: int = 0
    status: str = "paused"
    parent_run_id: str | None = None
    intervention_patch: dict[str, Any] | None = None
    fork_base_hash: str | None = None
    injections: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def create(cls, *, seed: int, blind: bool) -> LabRun:
        return cls(
            run_id=uuid.uuid4().hex,
            seed=seed,
            blind=blind,
            brain=build_reference_brain(BrainConfig(random_seed=seed)),
            manifest=SwitchWorld.canonical_scenario(),
        )

    def step(self) -> dict[str, Any]:
        if self.event_index >= len(self.manifest):
            self.status = "complete"
            return self.public_state()
        item = self.manifest[self.event_index]
        self.brain.inject_stimulus(
            target=f"sensory:{item.evidence}",
            label=item.evidence,
            time=item.time,
            source=f"sensor:{item.evidence}",
            evidence_id=f"event:{self.event_index}:{item.evidence}",
            metadata={"sensor": item.evidence, "truth": item.truth, "note": item.note},
        )
        self.brain.run()
        self.brain.snapshot(external_event=item.evidence, truth=item.truth)
        self.event_index += 1
        self.status = "complete" if self.event_index == len(self.manifest) else "paused"
        return self.public_state()

    def run_remaining(self) -> dict[str, Any]:
        self.status = "running"
        while self.event_index < len(self.manifest) and self.status == "running":
            self.step()
            if self.event_index < len(self.manifest):
                self.status = "running"
        if self.event_index == len(self.manifest):
            self.status = "complete"
        return self.public_state()

    def pause(self) -> dict[str, Any]:
        self.status = "paused"
        return self.public_state()

    def reset(self) -> dict[str, Any]:
        self.brain = build_reference_brain(BrainConfig(random_seed=self.seed))
        self.event_index = 0
        self.status = "paused"
        self.injections = []
        return self.public_state()

    def inject(
        self,
        *,
        target: str,
        label: str,
        strength: float,
        event_time: float | None,
    ) -> dict[str, Any]:
        if target not in self.brain.sparks:
            raise ValueError(f"Unknown Spark: {target}")
        if not math.isfinite(strength):
            raise ValueError("strength must be finite")
        if len(self.injections) >= MAX_EXTERNAL_EVENTS:
            raise ValueError("external event budget exceeded")
        resolved_time = max(self.brain.time + 0.001, event_time or 0.0)
        evidence_id = f"lab-injection:{len(self.injections)}:{label}"
        self.brain.inject_stimulus(
            target=target,
            label=label,
            time=resolved_time,
            source="brain-lab",
            evidence_id=evidence_id,
            metadata={"sensor": label, "note": "manual injection"},
            strength=strength,
        )
        self.brain.run()
        self.brain.snapshot(external_event=label, truth=None)
        self.injections.append(
            {"target": target, "label": label, "strength": strength, "time": resolved_time}
        )
        return self.public_state()

    def public_state(self) -> dict[str, Any]:
        frames = [_frame_dict(frame, blind=self.blind) for frame in self.brain.trace]
        current = frames[-1] if frames else _frame_dict(
            self.brain.inspect_snapshot(external_event="unresolved", truth=None), blind=self.blind
        )
        graph = prepare_relevant_graph(self.brain.export_graph(), current)
        state = self.brain.state_dict(include_trace=False)
        spark_details = {row["id"]: row for row in state["sparks"]}
        return {
            "run_id": self.run_id,
            "seed": self.seed,
            "blind": self.blind,
            "status": self.status,
            "event_index": self.event_index,
            "event_count": len(self.manifest),
            "parent_run_id": self.parent_run_id,
            "intervention_patch": self.intervention_patch,
            "fork_base_hash": self.fork_base_hash,
            "prediction": self.brain.prediction,
            "current_frame": current,
            "trace": frames,
            "graph": graph,
            "full_graph_counts": {
                "nodes": len(self.brain.sparks),
                "edges": len(self.brain.connections),
            },
            "spark_details": spark_details,
            "workspace": [asdict(row) for row in self.brain.workspace],
            "ignitions": [asdict(row) for row in self.brain.ignitions],
            "broadcast_listeners": sorted(self.brain.broadcast_listeners),
        }

    def export_bundle(self) -> dict[str, Any]:
        bundle = {
            "schema_version": "0.2",
            "lab_version": "0.1",
            "run": {
                "run_id": self.run_id,
                "seed": self.seed,
                "blind": self.blind,
                "event_index": self.event_index,
                "status": self.status,
                "parent_run_id": self.parent_run_id,
                "intervention_patch": self.intervention_patch,
                "fork_base_hash": self.fork_base_hash,
                "injections": self.injections,
            },
            "event_manifest": [asdict(row) for row in self.manifest],
            "checkpoint": self.brain.state_dict(),
            "trace": [_frame_dict(row, blind=self.blind) for row in self.brain.trace],
            "figure_data": {
                "graph": self.brain.export_graph(),
                "frames": [_frame_dict(row, blind=self.blind) for row in self.brain.trace],
            },
        }
        return _blind_sanitize(bundle) if self.blind else bundle


class LabManager:
    def __init__(self, artifact_root: str | Path) -> None:
        self.artifact_root = Path(artifact_root).resolve()
        self.runs: dict[str, LabRun] = {}

    def create_run(self, *, seed: int = 7, blind: bool = False) -> LabRun:
        run = LabRun.create(seed=seed, blind=blind)
        self.runs[run.run_id] = run
        return run

    def get(self, run_id: str) -> LabRun:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise KeyError(f"Unknown run: {run_id}") from exc

    def fork(self, run_id: str, patch: dict[str, Any]) -> LabRun:
        parent = self.get(run_id)
        base_state = parent.brain.state_dict()
        child = LabRun(
            run_id=uuid.uuid4().hex,
            seed=parent.seed,
            blind=parent.blind,
            brain=SparkBrain.from_state_dict(base_state),
            manifest=list(parent.manifest),
            event_index=parent.event_index,
            status="paused",
            parent_run_id=parent.run_id,
            intervention_patch=dict(patch),
            fork_base_hash=state_hash(parent.brain),
            injections=list(parent.injections),
        )
        self._apply_intervention(child.brain, patch)
        self.runs[child.run_id] = child
        return child

    @staticmethod
    def _apply_intervention(brain: SparkBrain, patch: dict[str, Any]) -> None:
        kind = patch["kind"]
        if kind in {"ablate_edge", "edit_edge"}:
            matches = [
                edge
                for edge in brain.connections
                if edge.source == patch["source"] and edge.target == patch["target"]
            ]
            if len(matches) != 1:
                raise ValueError("edge intervention must identify exactly one edge")
            matches[0].weight = 0.0 if kind == "ablate_edge" else float(patch["value"])
        elif kind in {"clamp_spark", "ablate_spark", "set_threshold"}:
            spark_id = str(patch["spark_id"])
            if spark_id not in brain.sparks:
                raise ValueError(f"Unknown Spark: {spark_id}")
            spark = brain.sparks[spark_id]
            if kind == "clamp_spark":
                spark.activation = float(patch["value"])
            elif kind == "ablate_spark":
                spark.activation = 0.0
                spark.threshold = 1_000_000.0
            else:
                value = float(patch["value"])
                if value <= 0 or not math.isfinite(value):
                    raise ValueError("threshold must be finite and > 0")
                spark.threshold = value
                spark.base_threshold = value
        elif kind == "suppress_organ":
            matches = [spark for spark in brain.sparks.values() if spark.organ == patch["organ"]]
            if not matches:
                raise ValueError(f"Unknown organ: {patch['organ']}")
            for spark in matches:
                spark.activation = 0.0
                spark.threshold = 1_000_000.0
        else:
            raise ValueError(f"Unsupported intervention: {kind}")

    def compare(self, left_id: str, right_id: str, cursor: int) -> dict[str, Any]:
        left = self.get(left_id)
        right = self.get(right_id)
        max_cursor = max(0, min(len(left.brain.trace), len(right.brain.trace)) - 1)
        resolved = min(cursor, max_cursor)
        return {
            "cursor": resolved,
            "synchronized": True,
            "left": _frame_dict(left.brain.trace[resolved], blind=left.blind)
            if left.brain.trace
            else None,
            "right": _frame_dict(right.brain.trace[resolved], blind=right.blind)
            if right.brain.trace
            else None,
        }

    def write_export(self, run_id: str) -> tuple[dict[str, Any], Path]:
        run = self.get(run_id)
        bundle = run.export_bundle()
        text = canonical_json(bundle) + "\n"
        if len(text.encode("utf-8")) > MAX_EXPORT_BYTES:
            raise ValueError("export exceeds local artifact size limit")
        output_dir = (self.artifact_root / run_id).resolve()
        if self.artifact_root not in output_dir.parents:
            raise ValueError("invalid export path")
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "brain_lab_export.json"
        path.write_text(text, encoding="utf-8", newline="")
        return bundle, path

    def import_bundle(self, bundle: dict[str, Any]) -> LabRun:
        try:
            serialized = canonical_json(bundle).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError("Brain Lab import must be finite JSON") from exc
        if len(serialized) > MAX_EXPORT_BYTES:
            raise ValueError("import exceeds local artifact size limit")
        _require_exact_keys(bundle, IMPORT_TOP_LEVEL_KEYS, "bundle")
        if bundle.get("schema_version") != "0.2" or bundle.get("lab_version") != "0.1":
            raise ValueError("unsupported Brain Lab export version")
        raw = _require_exact_keys(bundle["run"], IMPORT_RUN_KEYS, "bundle.run")
        if isinstance(raw["seed"], bool) or not isinstance(raw["seed"], int):
            raise ValueError("bundle.run.seed must be an integer")
        if not isinstance(raw["blind"], bool):
            raise ValueError("bundle.run.blind must be a boolean")
        if isinstance(raw["event_index"], bool) or not isinstance(raw["event_index"], int):
            raise ValueError("bundle.run.event_index must be an integer")
        if raw["status"] not in {"paused", "running", "complete"}:
            raise ValueError("bundle.run.status is invalid")
        if not isinstance(raw["run_id"], str):
            raise ValueError("bundle.run.run_id must be a string")
        for key in ("parent_run_id", "fork_base_hash"):
            if raw[key] is not None and not isinstance(raw[key], str):
                raise ValueError(f"bundle.run.{key} must be a string or null")
        if raw["intervention_patch"] is not None and not isinstance(
            raw["intervention_patch"], dict
        ):
            raise ValueError("bundle.run.intervention_patch must be an object or null")
        if not isinstance(raw["injections"], list) or len(raw["injections"]) > MAX_EXTERNAL_EVENTS:
            raise ValueError("bundle.run.injections must be a bounded array")
        for index, item in enumerate(raw["injections"]):
            injection = _require_exact_keys(
                item, {"target", "label", "strength", "time"}, f"run.injections[{index}]"
            )
            if not isinstance(injection["target"], str) or not isinstance(
                injection["label"], str
            ):
                raise ValueError("injection target and label must be strings")
            for key in ("strength", "time"):
                value = injection[key]
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                ):
                    raise ValueError(f"injection {key} must be finite")

        manifest_payload = bundle["event_manifest"]
        if not isinstance(manifest_payload, list) or len(manifest_payload) > MAX_EXTERNAL_EVENTS:
            raise ValueError("bundle.event_manifest must be a bounded array")
        manifest: list[SwitchEvent] = []
        previous_time = -1.0
        for index, item in enumerate(manifest_payload):
            row = _require_exact_keys(
                item, {"time", "evidence", "truth", "note"}, f"event_manifest[{index}]"
            )
            event_time = row["time"]
            if (
                isinstance(event_time, bool)
                or not isinstance(event_time, int | float)
                or not math.isfinite(event_time)
                or event_time < previous_time
            ):
                raise ValueError("event manifest times must be finite and nondecreasing")
            if not isinstance(row["evidence"], str) or not isinstance(row["note"], str):
                raise ValueError("event manifest evidence and note must be strings")
            if raw["blind"]:
                if row["truth"] is not None:
                    raise ValueError("blind event manifest contains visible truth")
            elif not isinstance(row["truth"], str):
                raise ValueError("event manifest truth must be a string")
            previous_time = float(event_time)
            manifest.append(
                SwitchEvent(
                    time=float(event_time),
                    evidence=row["evidence"],
                    truth=row["truth"],
                    note=row["note"],
                )
            )
        if not 0 <= raw["event_index"] <= len(manifest):
            raise ValueError("bundle.run.event_index is outside the event manifest")

        if not isinstance(bundle["checkpoint"], dict):
            raise ValueError("bundle.checkpoint must be an object")
        brain = SparkBrain.from_state_dict(bundle["checkpoint"])
        if raw["seed"] != brain.config.random_seed:
            raise ValueError("bundle seed does not match checkpoint config")
        if not isinstance(bundle["trace"], list):
            raise ValueError("bundle.trace must be an array")
        if bundle["trace"] != bundle["checkpoint"].get("trace"):
            raise ValueError("bundle trace does not match checkpoint trace")
        figure = _require_exact_keys(bundle["figure_data"], {"graph", "frames"}, "figure_data")
        if figure["frames"] != bundle["trace"]:
            raise ValueError("figure frames do not match the exported trace")
        if figure["graph"] != brain.export_graph():
            raise ValueError("figure graph does not match the checkpoint graph")
        if raw["blind"] and _has_visible_truth(bundle):
            raise ValueError("blind import contains visible truth")

        run = LabRun(
            run_id=uuid.uuid4().hex,
            seed=raw["seed"],
            blind=raw["blind"],
            brain=brain,
            manifest=manifest,
            event_index=raw["event_index"],
            status="paused",
            parent_run_id=raw.get("parent_run_id"),
            intervention_patch=raw.get("intervention_patch"),
            fork_base_hash=raw.get("fork_base_hash"),
            injections=list(raw.get("injections", [])),
        )
        self.runs[run.run_id] = run
        return run

    def performance_sample(self) -> dict[str, Any]:
        nodes = [
            {"id": f"spark:{index}", "label": str(index), "kind": "feature", "organ": "test"}
            for index in range(2_000)
        ]
        edges = [
            {
                "source": f"spark:{index % 2_000}",
                "target": f"spark:{(index + 1) % 2_000}",
                "weight": 0.1,
            }
            for index in range(10_000)
        ]
        frame = {"fired": ["spark:0"], "sparks": [{"id": "spark:0", "activation": 1.0}]}
        started = time.perf_counter()
        subset = prepare_relevant_graph({"nodes": nodes, "edges": edges}, frame)
        elapsed_ms = (time.perf_counter() - started) * 1_000
        return {
            "source_nodes": len(nodes),
            "source_edges": len(edges),
            "render_nodes": len(subset["nodes"]),
            "render_edges": len(subset["edges"]),
            "subset_prepare_ms": round(elapsed_ms, 6),
            "frame_budget_ms_60fps": 16.666667,
            "within_prepare_budget": elapsed_ms < 16.666667,
            "note": (
                "Measures deterministic relevant-subset preparation, "
                "not browser paint time or energy."
            ),
        }
