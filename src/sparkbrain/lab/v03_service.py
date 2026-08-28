from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sparkbrain.v03 import IntegratedV03Brain, V03BrainConfig
from sparkbrain.v03_seed import SensorySample


def _json_copy(value: object) -> Any:
    return json.loads(json.dumps(value, allow_nan=False, ensure_ascii=False, sort_keys=True))


def _belief_observation(brain: IntegratedV03Brain) -> dict[str, Any]:
    inspection = brain.inspect()["beliefs"]
    rows: dict[str, Any] = {}
    for entity, state in inspection.items():
        activations = state["activations"]
        winner = state["winner"]
        rows[entity] = {
            "current_belief": winner,
            "residual_beliefs": [
                {"belief_key": key, "activation": value}
                for key, value in activations.items()
                if key != winner
            ],
        }
    return rows


def _entity_observation(
    sample: Mapping[str, Any], result: Mapping[str, Any]
) -> list[dict[str, Any]]:
    return [
        {
            "assignment_status": "assigned" if spark["entity_slot"] else "unassigned",
            "entity_hint": sample["entity_hint"],
            "entity_slot": spark["entity_slot"],
            "parent_spark_id": spark["spark_id"],
        }
        for spark in result["sparks"]
    ]


def _observation(
    brain: IntegratedV03Brain,
    result: Mapping[str, Any] | None,
    *,
    causal_evidence_removal: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    inspection = brain.inspect()
    inventory = brain.component_inventory()
    result = result or {}
    sample = brain.history[-1]["sample"] if brain.history else None
    decisions = list(result.get("decisions", []))
    evidence_rows = inventory["evidence"]["records"]
    return {
        "runtime_origin": "live_integrated_v03_runtime",
        "raw_input": sample,
        "ignored_channels": {
            "channels": [] if sample is None else sample["omitted_channels"],
            "reason": "explicit sensory omissions only; no inferred ignored channels",
        },
        "perceptual_sparks": result.get("sparks", []),
        "entity_assignments": [] if sample is None else _entity_observation(sample, result),
        "evidence_ids": sorted(inventory["evidence"]["records"]),
        "evidence_support_contradiction_correlation": [
            {
                "correlation_group": row["correlation_group"],
                "contradiction": row["strength"] if row["polarity"] == "contradict" else 0.0,
                "evidence_id": evidence_id,
                "polarity": row["polarity"],
                "support": row["strength"] if row["polarity"] == "support" else 0.0,
            }
            for evidence_id, row in sorted(evidence_rows.items())
        ],
        "evidence": inventory["evidence"],
        "coalition_decomposition": decisions,
        "no_ignition": [
            {
                "belief_key": row["belief_key"],
                "entity_key": row["object_key"],
                "reason": row["reason"],
            }
            for row in decisions
            if not row["ignited"]
        ],
        "beliefs": _belief_observation(brain),
        "revision_transitions": result.get(
            "revision_transitions", inspection["revision_transitions"]
        ),
        "attributions": result.get("attributions", inspection["attributions"]),
        "concept_candidates": result.get("concept_observations", inventory["concept"]),
        "organ_monitor_candidates": result.get("organ_observation", inventory["organ"]),
        "action": result.get("action", inspection["action"]),
        "world_feedback": result.get("world_feedback", inspection["world_feedback"]),
        "runtime_trace": inventory["trace"],
        "causal_evidence_removal": causal_evidence_removal,
    }


@dataclass(slots=True)
class V03LabRun:
    run_id: str
    config: V03BrainConfig
    brain: IntegratedV03Brain
    status: str = "paused"
    parent_run_id: str | None = None
    fork_base_hash: str | None = None
    last_result: dict[str, Any] | None = None
    causal_evidence_removal: dict[str, Any] | None = None

    @classmethod
    def create(cls, config: V03BrainConfig, *, run_id: str | None = None) -> V03LabRun:
        resolved_run_id = uuid.uuid4().hex if run_id is None else run_id
        if not isinstance(resolved_run_id, str) or not resolved_run_id:
            raise ValueError("run_id must be a non-empty string")
        return cls(
            run_id=resolved_run_id,
            config=config,
            brain=IntegratedV03Brain(config),
        )

    def step(
        self,
        sample: SensorySample,
        *,
        goal_bias: Mapping[str, float],
        world_feedback: Mapping[str, Any],
    ) -> dict[str, Any]:
        self.last_result = self.brain.step(
            sample, goal_bias=goal_bias, world_feedback=world_feedback
        ).as_dict()
        self.status = "paused"
        return self.public_state()

    def pause(self) -> dict[str, Any]:
        self.status = "paused"
        return self.public_state()

    def reset(self) -> dict[str, Any]:
        self.brain = IntegratedV03Brain(self.config)
        self.status = "paused"
        self.last_result = None
        self.causal_evidence_removal = None
        return self.public_state()

    def public_state(self) -> dict[str, Any]:
        return {
            "backend": "integrated-v03-reference",
            "run_id": self.run_id,
            "status": self.status,
            "parent_run_id": self.parent_run_id,
            "fork_base_hash": self.fork_base_hash,
            "config": self.config.as_dict(),
            "oracle_autonomous_boundary": {
                "classification": (
                    "oracle_diagnostic"
                    if self.config.allow_oracle_diagnostics
                    else "autonomous_local_reference"
                ),
                "oracle_diagnostic": self.config.allow_oracle_diagnostics,
                "concept_and_organ": "observer_only",
                "c19_status": "blocked",
            },
            "observation": _observation(
                self.brain,
                self.last_result,
                causal_evidence_removal=self.causal_evidence_removal,
            ),
        }


class V03LabManager:
    """In-memory, local-only adapter over the live v0.3 runtime."""

    def __init__(self) -> None:
        self.runs: dict[str, V03LabRun] = {}

    def create_run(
        self, config: V03BrainConfig, *, run_id: str | None = None
    ) -> V03LabRun:
        run = V03LabRun.create(config, run_id=run_id)
        if run.run_id in self.runs:
            raise ValueError(f"v0.3 run already exists: {run.run_id}")
        self.runs[run.run_id] = run
        return run

    def get(self, run_id: str) -> V03LabRun:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise KeyError(f"Unknown v0.3 run: {run_id}") from exc

    def fork_with_evidence_removal(
        self,
        run_id: str,
        *,
        evidence_id: str,
        at_time: float,
        reason: str,
        child_run_id: str | None = None,
    ) -> V03LabRun:
        parent = self.get(run_id)
        resolved_child_run_id = uuid.uuid4().hex if child_run_id is None else child_run_id
        if not isinstance(resolved_child_run_id, str) or not resolved_child_run_id:
            raise ValueError("child_run_id must be a non-empty string")
        if resolved_child_run_id in self.runs:
            raise ValueError(f"v0.3 run already exists: {resolved_child_run_id}")
        checkpoint = parent.brain.checkpoint(f"brain-lab:{parent.run_id}")
        child = V03LabRun(
            run_id=resolved_child_run_id,
            config=parent.config,
            brain=IntegratedV03Brain.restore(checkpoint),
            parent_run_id=parent.run_id,
            fork_base_hash=checkpoint["final_state_hash"],
            last_result=_json_copy(parent.last_result),
        )
        before = child.brain.ledger.active_state_hash()
        child.brain.ledger.deactivate(evidence_id, at_time=at_time, reason=reason)
        child.causal_evidence_removal = {
            "evidence_id": evidence_id,
            "before_active_state_hash": before,
            "after_active_state_hash": child.brain.ledger.active_state_hash(),
            "reason": reason,
            "time": at_time,
            "trace_origin": "lab_counterfactual_observer_not_runtime_trace",
        }
        self.runs[child.run_id] = child
        return child

    def compare(self, left_run_id: str, right_run_id: str) -> dict[str, Any]:
        left = self.get(left_run_id)
        right = self.get(right_run_id)
        return {
            "comparison_origin": "lab_observer_not_runtime_trace",
            "left": left.public_state(),
            "right": right.public_state(),
        }
