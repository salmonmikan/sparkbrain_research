"""Write a deterministic static observation from the live v0.3 Brain Lab adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.lab.v03_service import V03LabManager  # noqa: E402
from sparkbrain.v03 import V03BrainConfig  # noqa: E402
from sparkbrain.v03_seed import SensorySample  # noqa: E402

PARENT_RUN_ID = "b9a76f8735b246859da1722ef301e521"
CHILD_RUN_ID = "625663dccb3a4a1382069fcd4562061e"


def _sample(index: int) -> SensorySample:
    return SensorySample(
        sample_id=f"brain-lab-artifact:{index}",
        time=float(index),
        source_id=f"local-source-{index}",
        modality="artifact",
        values={f"signal-{index}": 1.0},
        omitted_channels=() if index == 0 else ("signal-0",),
        metadata={"text": "local stable target"},
    )


def build_artifact() -> dict:
    manager = V03LabManager()
    parent = manager.create_run(V03BrainConfig(), run_id=PARENT_RUN_ID)
    parent.step(_sample(0), goal_bias={}, world_feedback={})
    parent_state = parent.step(
        _sample(1),
        goal_bias={"artifact:signal-1": 0.5},
        world_feedback={
            "status": "observed",
            "text": "local environment changed",
            "values": {"reward_signal": 0.25},
        },
    )
    evidence_id = parent_state["observation"]["evidence_ids"][0]
    child = manager.fork_with_evidence_removal(
        parent.run_id,
        evidence_id=evidence_id,
        at_time=2.0,
        reason="static Brain Lab causal observation",
        child_run_id=CHILD_RUN_ID,
    )
    document = {
        "comparison": manager.compare(parent.run_id, child.run_id),
        "parent": parent.public_state(),
        "schema_version": "0.3",
        "status": "engineering_static_observation_not_scientific",
    }
    observation = document["parent"]["observation"]
    required = {
        "action",
        "attributions",
        "beliefs",
        "causal_evidence_removal",
        "coalition_decomposition",
        "concept_candidates",
        "entity_assignments",
        "evidence",
        "evidence_ids",
        "evidence_support_contradiction_correlation",
        "ignored_channels",
        "no_ignition",
        "organ_monitor_candidates",
        "perceptual_sparks",
        "raw_input",
        "revision_transitions",
        "runtime_origin",
        "runtime_trace",
        "world_feedback",
    }
    if set(observation) != required:
        raise RuntimeError("Brain Lab static observation inventory drifted")
    if document["parent"]["oracle_autonomous_boundary"]["c19_status"] != "blocked":
        raise RuntimeError("Brain Lab artifact must preserve the C19 blocked boundary")
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = build_artifact()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            document,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote engineering-only Brain Lab artifact: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
