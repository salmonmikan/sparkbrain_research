from __future__ import annotations

import builtins
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from sparkbrain.v03 import (
    ENGINEERING_METRICS,
    ENGINEERING_VARIANTS,
    ENGINEERING_WORLDS,
    IntegratedV03Brain,
    SensorySample,
    V03BrainConfig,
    evaluate_engineering_runtime,
    validate_engineering_evaluation,
)
from sparkbrain.v03.runtime import ABLATIONS, ACTION_TYPES
from sparkbrain.v03_seed import EvidenceContribution


def sample(index: int, *, text: str = "stable target", channel: str | None = None) -> SensorySample:
    return SensorySample(
        sample_id=f"corrective:{index}",
        time=float(index),
        source_id=f"source-{index}",
        modality="corrective",
        values={channel or f"channel-{index}": 1.0},
        metadata={"text": text},
    )


def ignite(brain: IntegratedV03Brain) -> tuple[object, object]:
    return brain.step(sample(0)), brain.step(sample(1))


def test_config_round_trip_supports_exact_seven_ablations() -> None:
    assert ABLATIONS == (
        "no_residual",
        "no_maintain_objective",
        "no_revision_objective",
        "no_recovery_objective",
        "one_weighted_ce",
        "no_attribution",
        "no_coalition",
    )
    config = V03BrainConfig(ablations=ABLATIONS)
    assert V03BrainConfig.from_dict(config.as_dict()) == config
    with pytest.raises(ValueError, match="unsupported ablations"):
        IntegratedV03Brain(V03BrainConfig(ablations=("invented_ablation",)))
    with pytest.raises(ValueError, match="non-empty strings"):
        V03BrainConfig.from_dict({**V03BrainConfig().as_dict(), "ablations": [False]})


@pytest.mark.parametrize("ablation", ["no_revision_objective", "no_coalition"])
def test_revision_and_coalition_ablations_block_their_paths(ablation: str) -> None:
    brain = IntegratedV03Brain(V03BrainConfig(ablations=(ablation,)))
    _, result = ignite(brain)
    assert result.action is None
    assert result.revision_transitions[0]["accepted"] is False
    if ablation == "no_revision_objective":
        assert result.revision_transitions[0]["transition"] == "revise"
    else:
        assert result.decisions[0].reason == "coalition_ablation"
        assert result.decisions[0].coalitions == ()


def test_no_residual_clears_persistent_winner_before_a_quiet_step() -> None:
    brain = IntegratedV03Brain(V03BrainConfig(ablations=("no_residual",)))
    ignite(brain)
    result = brain.step(sample(2, channel="channel-1"))
    assert result.sparks == ()
    assert result.beliefs["__global__"] is None


def test_maintain_and_weighted_ce_ablations_take_distinct_routes() -> None:
    no_maintain = IntegratedV03Brain(
        V03BrainConfig(ablations=("no_maintain_objective",))
    )
    ignite(no_maintain)
    withheld = no_maintain.step(sample(2))
    assert withheld.revision_transitions[0]["transition"] == "maintain"
    assert withheld.revision_transitions[0]["accepted"] is False
    assert withheld.action_type == "withhold"

    weighted = IntegratedV03Brain(V03BrainConfig(ablations=("one_weighted_ce",)))
    ignite(weighted)
    revised = weighted.step(sample(2))
    assert revised.revision_transitions[0]["transition"] == "revise"
    assert revised.revision_transitions[0]["accepted"] is True


def test_no_recovery_objective_vetoes_recovery_after_no_ignition() -> None:
    brain = IntegratedV03Brain(V03BrainConfig(ablations=("no_recovery_objective",)))
    _, established = ignite(brain)
    belief = established.beliefs["__global__"]
    assert belief is not None
    brain.ledger.add(
        EvidenceContribution(
            "temporary-contradiction",
            "counter-source",
            belief,
            2.0,
            contradiction=10.0,
        )
    )
    blocked = brain.step(sample(2))
    assert not blocked.decisions[0].ignited
    brain.ledger.remove("temporary-contradiction")
    recovery = brain.step(sample(3))
    assert recovery.revision_transitions[0]["transition"] == "recover"
    assert recovery.revision_transitions[0]["accepted"] is False


def test_no_attribution_removes_only_attribution_output() -> None:
    baseline = IntegratedV03Brain()
    _, baseline_result = ignite(baseline)
    ablated = IntegratedV03Brain(V03BrainConfig(ablations=("no_attribution",)))
    _, ablated_result = ignite(ablated)
    assert baseline_result.attributions[0]["rows"]
    assert ablated_result.attributions[0]["rows"] == []
    assert ablated_result.decisions[0].ignited == baseline_result.decisions[0].ignited
    assert ablated.belief_field.ranked(None)[0].cited_evidence_ids == ()


def test_all_six_action_types_are_distinguishable() -> None:
    seen: set[str] = set()
    observe = IntegratedV03Brain()
    observe.step(sample(0, channel="steady"))
    seen.add(observe.step(sample(1, channel="steady")).action_type)

    default = IntegratedV03Brain()
    first, second = ignite(default)
    seen.update((first.action_type, second.action_type))
    seen.add(default.step(sample(2)).action_type)

    oracle = IntegratedV03Brain(
        V03BrainConfig(input_track="I2_symbolic_oracle", allow_oracle_diagnostics=True)
    )
    oracle_sample = SensorySample(
        "oracle-action",
        0.0,
        "oracle-source",
        "symbolic",
        {"event": 1.0},
        metadata={
            "symbolic_event": {
                "kind": "literal",
                "literal": {"entity": "a", "positive": True, "predicate": "opens"},
            }
        },
    )
    seen.add(oracle.step(oracle_sample).action_type)

    task = IntegratedV03Brain(V03BrainConfig(action_prefix="task_specific"))
    _, task_result = ignite(task)
    seen.add(task_result.action_type)
    assert seen == set(ACTION_TYPES)


def test_i3_uses_actual_c15_revision_controller_state() -> None:
    brain = IntegratedV03Brain(V03BrainConfig(input_track="I3_truth_free_revision"))
    brain.step(sample(0))
    result = brain.step(sample(1))
    assert result.revision_controller_status == "connected_actual_c15_revision_controller"
    assert result.revision_transitions[0]["controller_status"] == (
        "connected_actual_c15_revision_controller"
    )
    controller = brain.component_inventory()["model"]["revision_controller_state"]
    assert controller is not None
    assert controller["seen_evidence_ids"]


def test_i3_objective_and_structural_ablations_reach_actual_controller_boundary() -> None:
    no_revision = IntegratedV03Brain(
        V03BrainConfig(
            input_track="I3_truth_free_revision",
            ablations=("no_revision_objective",),
        )
    )
    first = no_revision.step(sample(0))
    second = no_revision.step(sample(1))
    assert first.revision_transitions[0]["transition"] == "insufficient_information"
    assert second.revision_transitions[0]["transition"] == "revise"
    assert second.revision_transitions[0]["accepted"] is False
    controller = no_revision.component_inventory()["model"]["revision_controller_state"]
    assert len(controller["seen_evidence_ids"]) == 1

    no_attribution = IntegratedV03Brain(
        V03BrainConfig(
            input_track="I3_truth_free_revision",
            ablations=("no_attribution",),
        )
    )
    no_attribution.step(sample(0))
    attributed = no_attribution.step(sample(1))
    assert attributed.revision_transitions[0]["accepted"] is True
    assert attributed.attributions[0]["rows"] == []
    controller = no_attribution.component_inventory()["model"][
        "revision_controller_state"
    ]
    assert all(not state["citations"] for state in controller["belief"]["states"].values())

    no_coalition = IntegratedV03Brain(
        V03BrainConfig(
            input_track="I3_truth_free_revision",
            ablations=("no_coalition",),
        )
    )
    no_coalition.step(sample(0))
    blocked = no_coalition.step(sample(1))
    assert blocked.decisions[0].reason == "coalition_ablation"
    controller = no_coalition.component_inventory()["model"][
        "revision_controller_state"
    ]
    assert controller["seen_evidence_ids"] == []


def test_i3_fails_closed_when_optional_torch_runtime_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_import = builtins.__import__

    def blocked_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "torch":
            raise ModuleNotFoundError("torch intentionally unavailable")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    with pytest.raises(RuntimeError, match="optional torch runtime"):
        IntegratedV03Brain(V03BrainConfig(input_track="I3_truth_free_revision"))


def test_engineering_evaluation_has_exact_metric_inventory_and_is_deterministic() -> None:
    first = evaluate_engineering_runtime()
    second = evaluate_engineering_runtime()
    assert first == second
    assert first["status"] == "engineering_only_not_scientific"
    assert tuple(first["world_ids"]) == ENGINEERING_WORLDS
    assert tuple(row["variant_id"] for row in first["variants"]) == ENGINEERING_VARIANTS
    assert len(first["rows"]) == len(ENGINEERING_WORLDS) * len(ENGINEERING_VARIANTS)
    for variant in ENGINEERING_VARIANTS:
        metrics = first["metrics"][variant]
        assert tuple(metrics) == ENGINEERING_METRICS
        assert len(metrics) == 15
        assert set(metrics["revision"]) == {"precision", "recall"}
        assert set(metrics["recovery"]) == {"latency", "rate"}
        assert set(metrics["invariance"]) == {"distractor", "duplicate"}
        assert metrics["checkpoint_continuation_equality"] is True

    full_recovery = next(
        row
        for row in first["rows"]
        if row["variant_id"] == "full" and row["world_id"] == "recovery"
    )
    assert first["metrics"]["full"]["recovery"] == {
        "latency": full_recovery["recovery_latency"],
        "rate": float(full_recovery["recovery_success"]),
    }
    assert first["metrics"]["no_recovery_objective"]["recovery"]["rate"] == 0.0
    entity_rows = [
        row
        for row in first["rows"]
        if row["world_id"] == "multi_entity_cross_talk"
    ]
    assert all(row["entity_cross_talk_opportunities"] == 1 for row in entity_rows)
    assert all(
        first["metrics"][row["variant_id"]]["entity_cross_talk"]
        == float(row["entity_cross_talk_events"])
        for row in entity_rows
    )
    full_rows = {
        row["world_id"]: row
        for row in first["rows"]
        if row["variant_id"] == "full"
    }
    assert full_rows["goal_biased_search"]["goal_bias_effect"] is True
    assert full_rows["action_feedback"]["feedback_evidence_returned"] is True
    assert full_rows["continuous_novelty"]["distractor_invariant"] is True
    for world in ENGINEERING_WORLDS:
        assert len(
            {
                row["input_sequence_hash"]
                for row in first["rows"]
                if row["world_id"] == world
            }
        ) == 1


def test_engineering_evaluation_validator_rejects_contract_drift() -> None:
    result = evaluate_engineering_runtime()
    broken = copy.deepcopy(result)
    broken["metrics"]["full"]["scientific_superiority"] = True
    with pytest.raises(ValueError, match="metric inventory drifted"):
        validate_engineering_evaluation(broken)
    broken = copy.deepcopy(result)
    broken["status"] = "scientifically_validated"
    with pytest.raises(ValueError, match="must remain non-scientific"):
        validate_engineering_evaluation(broken)


def test_engineering_evaluation_cli_writes_canonical_revalidated_json(
    tmp_path: Path,
) -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts/run_v031_integrated_evaluation.py"),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    target = tmp_path / "v031_integrated_engineering_evaluation.json"
    payload = target.read_bytes()
    document = json.loads(payload.decode("utf-8"))
    validate_engineering_evaluation(document)
    assert payload == (
        json.dumps(
            document,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    assert "engineering-only" in completed.stdout


def test_corrective_checkpoint_rejects_ablation_inventory_tamper() -> None:
    brain = IntegratedV03Brain(V03BrainConfig(ablations=("no_attribution",)))
    ignite(brain)
    checkpoint = brain.checkpoint("corrective")
    restored = IntegratedV03Brain.restore(checkpoint)
    assert restored.config.ablations == ("no_attribution",)
    broken = copy.deepcopy(checkpoint)
    broken["config"]["ablations"] = ["no_coalition"]
    with pytest.raises(ValueError, match="hash mismatch"):
        IntegratedV03Brain.restore(broken)
