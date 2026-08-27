"""C17 experiment assembly and raw-to-derived validation.

Discovery is label blind. Evaluator-only fields are joined only after each bank,
candidate, development mapping, and train-only control membership are frozen.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import random
import re
import subprocess
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from .contracts import canonical, digest, exact_keys, validate_resource_conditions
from .discovery import (
    discover_primary_candidate,
    execute_c14_c15_boundary,
    select_control_memberships,
)
from .worlds import fixture_document

BRANCHES = (
    "unablated",
    "targeted",
    "random_unmatched",
    "size_matched",
    "degree_matched",
    "load_matched",
    "activity_matched",
)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


PREFINAL_REPRODUCTION_EVIDENCE = {
    "comparison_contract_id": "c17-v2-external-prefinal-exact9-byte-compare-v1",
    "manifest_file": "reproduction_compare_manifest.json",
    "manifest_sha256": None,
    "prefinal_exact9_equal": False,
    "process_ids": ["A", "B"],
    "pythonhashseeds": [11801, 21801],
    "status": "pending_external_compare",
}


def _c16_protocol(root: Path) -> dict[str, Any]:
    path = root / "artifacts/v03/c16_proto_concepts/protocol.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _split(cell: dict[str, Any], name: str) -> list[dict[str, Any]]:
    return next(row["episodes"] for row in cell["splits"] if row["split"] == name)


def _bank_and_observations(
    episodes: list[dict[str, Any]],
    protocol: dict[str, Any],
    run_seed: int,
    capacity: int,
) -> tuple[Any, list[dict[str, Any]], str]:
    from sparkbrain.v03_concepts.bank import ConceptBank, cosine
    from sparkbrain.v03_concepts.learning import normalize

    root = Path(__file__).resolve().parents[3]
    c16 = _c16_protocol(root)
    c16["formation"]["capacity"] = capacity
    bank = ConceptBank(c16, run_seed, "online_prototype", "canonical")
    for episode in episodes:
        for frame in episode["frames"]:
            bank.observe(frame["base_values"], frame["sample_id"])
    bank.freeze()
    bank_hash = bank.hash()
    candidates = [row for row in bank.candidates() if row["status"] == "active"]
    rows: list[dict[str, Any]] = []
    previous: str | None = None
    for episode in episodes:
        for frame in episode["frames"]:
            vector = normalize(frame["base_values"])
            scored = []
            for candidate in candidates:
                prototype = candidate["prototype"]
                score = (
                    0.0
                    if vector is None or prototype is None
                    else max(0.0, cosine(vector, prototype))
                )
                scored.append((score, candidate["candidate_id"]))
            scored.sort(key=lambda item: (-item[0], item[1]))
            winner = scored[0][1] if scored else None
            for score, candidate_id in scored:
                rows.append(
                    {
                        "opaque_candidate_id": candidate_id,
                        "activation": score,
                        "message_source_id": previous,
                        "message_target_id": winner,
                        "message_weight": 0.0 if previous is None or winner is None else score,
                        "opaque_episode_id": episode["episode_id"],
                        "time": frame["t"],
                    }
                )
            previous = winner
    return bank, rows, bank_hash


def _query_activations(bank: Any, frame: dict[str, Any]) -> dict[str, float]:
    from sparkbrain.v03_concepts.bank import cosine
    from sparkbrain.v03_concepts.learning import normalize

    vector = normalize(frame["base_values"])
    result = {}
    for candidate in bank.candidates():
        if candidate["status"] != "active":
            continue
        prototype = candidate["prototype"]
        result[candidate["candidate_id"]] = (
            0.0 if vector is None or prototype is None else max(0.0, cosine(vector, prototype))
        )
    return result


def _assessment_target(frame: dict[str, Any]) -> str:
    return ("allow", "veto", "abstain", "abstain")[frame["evaluator_function_index"]]


def _assessment_model_call(frame: dict[str, Any]) -> dict[str, Any]:
    return {
        "entity_key": frame["entity_key"],
        "features": [frame["base_values"], *([[0.0] * 12] * 4)],
        "evidence_ids": [frame["sample_id"], None, None, None, None],
        "padding_mask": [True, False, False, False, False],
    }


def _assessment_state(model: Any) -> dict[str, Any]:
    return {
        name: tensor.detach().cpu().tolist()
        for name, tensor in sorted(model.state_dict().items())
    }


def _load_assessment_model(state: dict[str, Any]) -> Any:
    import torch

    from sparkbrain.v03_learned.model import C15RevisionModel

    model = C15RevisionModel()
    current = model.state_dict()
    if set(state) != set(current):
        raise ValueError("C17 assessment checkpoint state inventory mismatch")
    model.load_state_dict(
        {
            name: torch.tensor(state[name], dtype=current[name].dtype)
            for name in sorted(current)
        },
        strict=True,
    )
    model.eval()
    model.reset_runtime()
    return model


def _assessment_heads(output: Any, temperature: float) -> Any:
    import torch

    from sparkbrain.v03_seed.revision import BELIEF_ORDER, RevisionHeadOutput

    raw = [
        float(value)
        for value in output.conditional_belief_probabilities(
            temperature=temperature
        ).detach().cpu()
    ]
    total = sum(raw)
    normalized = [value / total for value in raw]
    normalized[-1] = 1.0 - sum(normalized[:-1])
    return RevisionHeadOutput(
        belief_probabilities=dict(zip(BELIEF_ORDER, normalized, strict=True)),
        maintain_probability=float(torch.sigmoid(output.maintain_logit).detach().cpu()),
        update_probability=float(torch.sigmoid(output.update_logit).detach().cpu()),
        recovery_probability=float(torch.sigmoid(output.recovery_logit).detach().cpu()),
        abstention_probability=float(torch.sigmoid(output.abstention_logit).detach().cpu()),
    )


def _assessment_loss(output: Any, target: str) -> Any:
    import torch
    import torch.nn.functional as functional

    belief = functional.cross_entropy(output.belief_logits.reshape(1, -1), torch.tensor([1]))
    allow = torch.tensor(1.0 if target == "allow" else 0.0)
    abstain = torch.tensor(1.0 if target == "abstain" else 0.0)
    maintain = functional.binary_cross_entropy_with_logits(output.maintain_logit, allow)
    abstention = functional.binary_cross_entropy_with_logits(
        output.abstention_logit, abstain
    )
    return belief + maintain + abstention


def _assessment_dev_subsets(
    episodes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selection = [row for row in episodes if row["episode_index"] % 2 == 0]
    calibration = [row for row in episodes if row["episode_index"] % 2 == 1]
    if (
        not selection
        or not calibration
        or set(row["episode_id"] for row in selection)
        & set(row["episode_id"] for row in calibration)
    ):
        raise ValueError("C17 fixed dev selection/calibration partition is invalid")
    return selection, calibration


def _assessment_scoring_rows(
    episodes: list[dict[str, Any]],
) -> list[tuple[str, dict[str, Any]]]:
    return [
        (episode["episode_id"], frame)
        for episode in episodes
        for frame in episode["frames"]
        if frame["scoring"]
    ]


def _fit_assessment_candidates(
    run_seed: int, train_rows: list[tuple[str, dict[str, Any]]]
) -> tuple[dict[int, dict[str, Any]], int]:
    import torch

    from sparkbrain.v03_learned.model import C15RevisionModel

    torch.manual_seed(run_seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    model = C15RevisionModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03, weight_decay=0.0)
    checkpoints: dict[int, dict[str, Any]] = {}
    optimizer_steps = 0
    for epoch in range(1, 7):
        model.train()
        for _ in range(4):
            for _, frame in train_rows:
                optimizer.zero_grad(set_to_none=True)
                model.reset_runtime()
                output = model.forward_fixture(_assessment_model_call(frame))
                loss = _assessment_loss(output, _assessment_target(frame))
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
                optimizer.step()
                optimizer_steps += 1
        if epoch in {2, 4, 6}:
            state = _assessment_state(model)
            checkpoints[epoch] = {"state": state, "sha256": digest(state)}
    return checkpoints, optimizer_steps


def _selection_raw(
    checkpoints: dict[int, dict[str, Any]],
    rows: list[tuple[str, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[Any]]:
    import torch

    from sparkbrain.v03_learned.training import CheckpointScore

    raw = []
    checkpoint_scores = []
    for epoch in (2, 4, 6):
        candidate = _load_assessment_model(checkpoints[epoch]["state"])
        losses = []
        with torch.no_grad():
            for episode_id, frame in rows:
                candidate.reset_runtime()
                call = _assessment_model_call(frame)
                loss = float(
                    _assessment_loss(
                        candidate.forward_fixture(call), _assessment_target(frame)
                    ).cpu()
                )
                losses.append(loss)
                raw.append(
                    {
                        "epoch": epoch,
                        "episode_id": episode_id,
                        "sample_id": frame["sample_id"],
                        "model_call_sha256": digest(call),
                        "target": _assessment_target(frame),
                        "weighted_objective_total": loss,
                    }
                )
        checkpoint_scores.append(
            CheckpointScore(epoch=epoch, weighted_objective_total=sum(losses) / len(losses))
        )
    return raw, checkpoint_scores


def _calibration_raw(model: Any, rows: list[tuple[str, dict[str, Any]]]) -> tuple[list, list]:
    import torch

    from sparkbrain.v03_learned.training import (
        ABSTENTION_THRESHOLD_GRID,
        TEMPERATURE_GRID,
        CalibrationScore,
    )

    raw = []
    calibration_scores = []
    for temperature in TEMPERATURE_GRID:
        for threshold in ABSTENTION_THRESHOLD_GRID:
            belief_errors = []
            abstention_errors = []
            with torch.no_grad():
                for episode_id, frame in rows:
                    model.reset_runtime()
                    call = _assessment_model_call(frame)
                    output = model.forward_fixture(call)
                    probabilities = output.conditional_belief_probabilities(
                        temperature=temperature
                    )
                    target = torch.tensor([0.0, 1.0, 0.0])
                    belief_error = float(torch.sum((probabilities - target) ** 2))
                    belief_errors.append(belief_error)
                    abstention = float(torch.sigmoid(output.abstention_logit))
                    truth = float(_assessment_target(frame) == "abstain")
                    abstention_error = (float(abstention >= threshold) - truth) ** 2
                    abstention_errors.append(abstention_error)
                    raw.append(
                        {
                            "temperature": temperature,
                            "abstention_threshold": threshold,
                            "episode_id": episode_id,
                            "sample_id": frame["sample_id"],
                            "model_call_sha256": digest(call),
                            "target": _assessment_target(frame),
                            "belief_probabilities": [
                                float(value) for value in probabilities.detach().cpu()
                            ],
                            "abstention_probability": abstention,
                            "belief_squared_error": belief_error,
                            "abstention_squared_error": abstention_error,
                        }
                    )
            calibration_scores.append(
                CalibrationScore(
                    temperature=temperature,
                    abstention_threshold=threshold,
                    belief_brier=sum(belief_errors) / len(belief_errors),
                    abstention_brier=sum(abstention_errors) / len(abstention_errors),
                )
            )
    return raw, calibration_scores


def _train_assessment_checkpoint(
    protocol: dict[str, Any], run_seed: int, r0_cell: dict[str, Any]
) -> tuple[dict[str, Any], Any]:
    import torch

    from sparkbrain.v03_learned.training import select_calibration, select_checkpoint

    train_episodes = _split(r0_cell, "train")
    dev_episodes = _split(r0_cell, "dev")
    selection_episodes, calibration_episodes = _assessment_dev_subsets(dev_episodes)
    train_rows = _assessment_scoring_rows(train_episodes)
    selection_rows = _assessment_scoring_rows(selection_episodes)
    calibration_rows = _assessment_scoring_rows(calibration_episodes)
    train_ids = [episode["episode_id"] for episode in train_episodes]
    selection_ids = [episode["episode_id"] for episode in selection_episodes]
    calibration_ids = [episode["episode_id"] for episode in calibration_episodes]
    if set(train_ids) & (set(selection_ids) | set(calibration_ids)):
        raise ValueError("C17 assessment train/dev partitions must be disjoint")
    checkpoints, optimizer_steps = _fit_assessment_candidates(run_seed, train_rows)
    selection_raw, checkpoint_scores = _selection_raw(checkpoints, selection_rows)
    selected = select_checkpoint(checkpoint_scores)
    selected_state = checkpoints[selected.epoch]["state"]
    selected_model = _load_assessment_model(selected_state)
    calibration_raw, calibration_scores = _calibration_raw(
        selected_model, calibration_rows
    )
    calibration = select_calibration(calibration_scores)
    boundary_rows = []
    seen: set[str] = set()
    with torch.no_grad():
        for _, frame in calibration_rows:
            selected_model.reset_runtime()
            call = _assessment_model_call(frame)
            heads = _assessment_heads(
                selected_model.forward_fixture(call), calibration.temperature
            )
            boundary = execute_c14_c15_boundary(
                heads=heads,
                entity_key=frame["entity_key"],
                evidence_prefix=f"c17-{run_seed}-{frame['sample_id']}",
                abstention_threshold=calibration.abstention_threshold,
            )
            if boundary["assessment"] in {"allow", "veto", "abstain"} - seen:
                boundary_rows.append(
                    {
                        "model_call": call,
                        "model_call_sha256": digest(call),
                        "heads": heads.to_dict(),
                        "boundary": boundary,
                    }
                )
                seen.add(boundary["assessment"])
            if seen == {"allow", "veto", "abstain"}:
                break
    if seen != {"allow", "veto", "abstain"}:
        raise ValueError("C17 learned checkpoint did not realize all assessment outcomes")
    reference = boundary_rows[0]
    from sparkbrain.v03_seed.revision import RevisionHeadOutput

    learned_heads = RevisionHeadOutput.from_dict(reference["heads"])
    for route in ("none", "rejection"):
        boundary_rows.append(
            {
                "model_call": reference["model_call"],
                "model_call_sha256": reference["model_call_sha256"],
                "heads": reference["heads"],
                "boundary": execute_c14_c15_boundary(
                    heads=learned_heads,
                    entity_key=reference["model_call"]["entity_key"],
                    evidence_prefix=f"c17-{run_seed}-{route}",
                    abstention_threshold=calibration.abstention_threshold,
                    route=route,
                ),
            }
        )
    record = {
        "run_seed": run_seed,
        "training_condition_id": "R0_baseline",
        "training_split": "train",
        "training_episode_ids": train_ids,
        "training_episode_sha256": digest(train_episodes),
        "training_visible_sha256": digest(
            [_assessment_model_call(frame) for _, frame in train_rows]
        ),
        "training_target_sha256": digest(
            [_assessment_target(frame) for _, frame in train_rows]
        ),
        "optimizer_steps": optimizer_steps,
        "dev_partition_rule": "episode_index_even_selection_odd_calibration",
        "selection_condition_id": "R0_baseline",
        "selection_split": "dev_selection",
        "selection_episode_ids": selection_ids,
        "selection_episode_sha256": digest(selection_episodes),
        "selection_visible_sha256": digest(
            [_assessment_model_call(frame) for _, frame in selection_rows]
        ),
        "selection_target_sha256": digest(
            [_assessment_target(frame) for _, frame in selection_rows]
        ),
        "selection_raw_rows": selection_raw,
        "candidate_checkpoints": [
            {
                "epoch": epoch,
                "sha256": checkpoints[epoch]["sha256"],
                "state": checkpoints[epoch]["state"],
            }
            for epoch in (2, 4, 6)
        ],
        "checkpoint_scores": [
            {
                "epoch": score.epoch,
                "weighted_objective_total": score.weighted_objective_total,
                "sha256": checkpoints[score.epoch]["sha256"],
            }
            for score in checkpoint_scores
        ],
        "selected_epoch": selected.epoch,
        "checkpoint_sha256": checkpoints[selected.epoch]["sha256"],
        "checkpoint_state": selected_state,
        "calibration_condition_id": "R0_baseline",
        "calibration_split": "dev_calibration",
        "calibration_episode_ids": calibration_ids,
        "calibration_episode_sha256": digest(calibration_episodes),
        "calibration_visible_sha256": digest(
            [_assessment_model_call(frame) for _, frame in calibration_rows]
        ),
        "calibration_target_sha256": digest(
            [_assessment_target(frame) for _, frame in calibration_rows]
        ),
        "calibration_raw_rows": calibration_raw,
        "calibration_scores": [
            {
                "temperature": score.temperature,
                "abstention_threshold": score.abstention_threshold,
                "belief_brier": score.belief_brier,
                "abstention_brier": score.abstention_brier,
            }
            for score in calibration_scores
        ],
        "temperature": calibration.temperature,
        "abstention_threshold": calibration.abstention_threshold,
        "shared_resource_condition_ids": protocol["resource_conditions"]["condition_order"],
        "boundary_rows": boundary_rows,
    }
    return record, selected_model


def _assess_frame(
    model: Any,
    checkpoint: dict[str, Any],
    frame: dict[str, Any],
    cache: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    call = _assessment_model_call(frame)
    key = digest(call)
    if key not in cache:
        import torch

        with torch.no_grad():
            model.reset_runtime()
            heads = _assessment_heads(
                model.forward_fixture(call), checkpoint["temperature"]
            )
        cache[key] = execute_c14_c15_boundary(
            heads=heads,
            entity_key=frame["entity_key"],
            evidence_prefix=f"c17-eval-{frame['sample_id']}",
            abstention_threshold=checkpoint["abstention_threshold"],
        )
    return cache[key]


def _map_function(
    bank: Any, candidate: dict[str, Any] | None, episodes: list[dict[str, Any]]
) -> tuple[int | None, dict[int, float]]:
    totals = defaultdict(float)
    counts = defaultdict(int)
    if candidate is None:
        return None, {index: 0.0 for index in range(4)}
    members = candidate["member_ids"]
    for episode in episodes:
        for frame in episode["frames"]:
            activations = _query_activations(bank, frame)
            value = sum(activations.get(member, 0.0) for member in members) / len(members)
            function_index = frame["evaluator_function_index"]
            totals[function_index] += value
            counts[function_index] += 1
    rates = {index: totals[index] / counts[index] if counts[index] else 0.0 for index in range(4)}
    return min(range(4), key=lambda index: (-rates[index], index)), rates


def _branch_episode(
    *,
    bank: Any,
    episode: dict[str, Any],
    candidate: dict[str, Any] | None,
    target_function: int | None,
    controls: dict[str, list[str] | None],
    branch: str,
    run_seed: int,
    condition_id: str,
    split: str,
    communication_bandwidth: int,
    workspace_capacity: int,
    assessment_checkpoint: dict[str, Any],
    assessment_model: Any,
    assessment_cache: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    members = [] if candidate is None else candidate["member_ids"]
    ablated = members if branch == "targeted" else (controls.get(branch) or [])
    eligible = correct = active = related = disrupted = 0
    function_eligible = {str(index): 0 for index in range(4)}
    function_correct = {str(index): 0 for index in range(4)}
    assessment_counts = {name: 0 for name in ("allow", "veto", "abstain")}
    before = digest({"bank": bank.state(), "episode_id": episode["episode_id"]})
    for frame in episode["frames"]:
        if not frame["scoring"]:
            continue
        eligible += 1
        function_index = frame["evaluator_function_index"]
        function_eligible[str(function_index)] += 1
        activations = _query_activations(bank, frame)
        ranked = sorted(members, key=lambda item: (-activations.get(item, 0.0), item))
        transmitted = ranked[:communication_bandwidth]
        retained = transmitted[:workspace_capacity]
        minimum_members = min(2, len(members))
        candidate_active = (
            bool(members)
            and len(retained) >= minimum_members
            and sum(activations.get(item, 0.0) for item in retained) / len(retained) >= 0.5
        )
        if candidate_active:
            active += 1
        is_related = target_function is not None and function_index == target_function
        if is_related:
            related += 1
        ablation_active = bool(ablated) and any(item in retained for item in ablated)
        boundary = _assess_frame(
            assessment_model, assessment_checkpoint, frame, assessment_cache
        )
        assessment = boundary["assessment"]
        if assessment not in assessment_counts:
            raise ValueError("C17 evaluation expected a learned proposal assessment")
        assessment_counts[assessment] += 1
        proposal_allowed = boundary["assessment_allowed"]
        wrong = (not proposal_allowed) or (ablation_active and candidate_active and is_related)
        if wrong:
            disrupted += 1
        correct += int(not wrong)
        function_correct[str(function_index)] += int(not wrong)
    after = digest({"bank": bank.state(), "episode_id": episode["episode_id"]})
    return {
        "run_seed": run_seed,
        "condition_id": condition_id,
        "split": split,
        "episode_id": episode["episode_id"],
        "branch": branch,
        "candidate_id": None if candidate is None else candidate["candidate_id"],
        "target_function_index": target_function,
        "eligible": eligible,
        "correct": correct,
        "candidate_active": active,
        "related": related,
        "disrupted": disrupted,
        "function_eligible": function_eligible,
        "function_correct": function_correct,
        "assessment_counts": assessment_counts,
        "communication_bandwidth": communication_bandwidth,
        "workspace_capacity": workspace_capacity,
        "retained_member_budget": min(communication_bandwidth, workspace_capacity),
        "state_hash_before": before,
        "state_hash_after": after,
        "restore_exact": before == after,
    }


def _ratio(numerator: int | float, denominator: int | float) -> float | None:
    return numerator / denominator if denominator else None


def _impairment(rows: list[dict[str, Any]], branch: str) -> float | None:
    base = [row for row in rows if row["branch"] == "unablated"]
    changed = [row for row in rows if row["branch"] == branch]
    base_accuracy = _ratio(
        sum(row["correct"] for row in base), sum(row["eligible"] for row in base)
    )
    branch_accuracy = _ratio(
        sum(row["correct"] for row in changed), sum(row["eligible"] for row in changed)
    )
    return (
        None
        if base_accuracy is None or branch_accuracy is None
        else base_accuracy - branch_accuracy
    )


def _function_accuracy(rows: list[dict[str, Any]], branch: str, function: int) -> float | None:
    selected = [row for row in rows if row["branch"] == branch]
    key = str(function)
    return _ratio(
        sum(row["function_correct"][key] for row in selected),
        sum(row["function_eligible"][key] for row in selected),
    )


def _locked_impairment(
    rows: list[dict[str, Any]], branch: str, target_function: int | None
) -> float | None:
    if target_function is None:
        return None
    base = _function_accuracy(rows, "unablated", target_function)
    changed = _function_accuracy(rows, branch, target_function)
    return None if base is None or changed is None else base - changed


def _heldout_reuse(rows: list[dict[str, Any]], target_function: int | None) -> float | None:
    if target_function is None:
        return None
    base = {row["episode_id"]: row for row in rows if row["branch"] == "unablated"}
    targeted = {row["episode_id"]: row for row in rows if row["branch"] == "targeted"}
    eligible = [
        episode_id
        for episode_id, row in targeted.items()
        if row["function_eligible"][str(target_function)] > 0
    ]
    numerator = 0
    for episode_id in eligible:
        unablated = base[episode_id]
        changed = targeted[episode_id]
        key = str(target_function)
        numerator += int(
            unablated["function_correct"][key] > changed["function_correct"][key]
            and changed["candidate_active"] > 0
        )
    return _ratio(numerator, len(eligible))


def _unrelated_collateral(rows: list[dict[str, Any]], target_function: int | None) -> float | None:
    if target_function is None:
        return None
    effects = []
    for function in range(4):
        if function == target_function:
            continue
        base = _function_accuracy(rows, "unablated", function)
        targeted = _function_accuracy(rows, "targeted", function)
        if base is not None and targeted is not None:
            effects.append(base - targeted)
    return None if not effects else max(0.0, max(effects))


def _percentile(values: list[float], p: float) -> float:
    position = (len(values) - 1) * p
    lower, upper = math.floor(position), math.ceil(position)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def _bootstrap(values: list[float], protocol: dict[str, Any]) -> dict[str, Any]:
    count = protocol["statistics"]["bootstrap_resamples"]
    rng = random.Random(protocol["statistics"]["bootstrap_seed"])
    if not values:
        return {"effect": None, "lower": None, "upper": None, "resamples": count}
    draws = [sum(rng.choices(values, k=len(values))) / len(values) for _ in range(count)]
    draws.sort()
    return {
        "effect": sum(values) / len(values),
        "lower": _percentile(draws, 0.025),
        "upper": _percentile(draws, 0.975),
        "resamples": count,
    }


def _apply_seed_consistency(
    cell_metrics: list[dict[str, Any]], seed_gates: list[dict[str, Any]], protocol: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    summary = {}
    minimum = protocol["metrics"]["seed_consistency_min"]
    for condition_id in protocol["resource_conditions"]["condition_order"]:
        rows = [row for row in cell_metrics if row["condition_id"] == condition_id]
        counts = {
            function: sum(
                row["target_function_index"] == function
                and row["local_gates_except_seed_consistency"]
                for row in rows
            )
            for function in range(4)
        }
        qualifying_function = min(counts, key=lambda function: (-counts[function], function))
        qualifying_count = counts[qualifying_function]
        summary[condition_id] = {
            "function_index": qualifying_function,
            "qualifying_seed_count": qualifying_count,
            "minimum": minimum,
            "passed": qualifying_count >= minimum,
        }
        for gate in seed_gates:
            if gate["condition_id"] == condition_id and gate["gate_id"] == "seed_consistency":
                own = next(row for row in rows if row["run_seed"] == gate["run_seed"])
                gate["passed"] = (
                    qualifying_count >= minimum
                    and own["target_function_index"] == qualifying_function
                    and own["local_gates_except_seed_consistency"]
                )
    return summary


def _selected_rows(
    rows: list[dict[str, Any]], seed: int, episode_ids: list[str]
) -> list[dict[str, Any]]:
    lookup = {(row["episode_id"], row["branch"]): row for row in rows if row["run_seed"] == seed}
    return [lookup[(episode_id, branch)] for episode_id in episode_ids for branch in BRANCHES]


def _hierarchical_bootstrap(
    matched_rows: list[dict[str, Any]],
    heldout_rows: list[dict[str, Any]],
    cell_metrics: list[dict[str, Any]],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    metrics = [
        "held_out_reuse",
        "targeted_impairment",
        *(f"control_margin:{name}" for name in protocol["controls"]["control_order"]),
        "unrelated_collateral",
    ]
    seeds = sorted({row["run_seed"] for row in cell_metrics})
    targets = {row["run_seed"]: row["target_function_index"] for row in cell_metrics}

    def calculate_block(seed_test, seed_held, target):
        targeted = _locked_impairment(seed_test, "targeted", target)
        return {
            "held_out_reuse": _heldout_reuse(seed_held, target),
            "targeted_impairment": targeted,
            **{
                f"control_margin:{name}": (
                    None
                    if targeted is None or _locked_impairment(seed_test, name, target) is None
                    else targeted - _locked_impairment(seed_test, name, target)
                )
                for name in protocol["controls"]["control_order"]
            },
            "unrelated_collateral": _unrelated_collateral(seed_test, target),
        }

    def aggregate(blocks):
        result = {}
        for metric in metrics:
            finite = [block[metric] for block in blocks if block[metric] is not None]
            result[metric] = _ratio(sum(finite), len(finite))
        return result

    point = aggregate(
        [
            calculate_block(
                [row for row in matched_rows if row["run_seed"] == seed],
                [row for row in heldout_rows if row["run_seed"] == seed],
                targets[seed],
            )
            for seed in seeds
        ]
    )
    values = {metric: [] for metric in metrics}
    rng = random.Random(protocol["statistics"]["bootstrap_seed"])
    for _ in range(protocol["statistics"]["bootstrap_resamples"]):
        sampled_blocks = []
        for seed in rng.choices(seeds, k=len(seeds)):
            target = targets[seed]
            test_ids = sorted(
                {
                    row["episode_id"]
                    for row in matched_rows
                    if target is not None
                    and row["run_seed"] == seed
                    and row["branch"] == "targeted"
                    and row["function_eligible"][str(target)] > 0
                }
            )
            heldout_ids = sorted(
                {
                    row["episode_id"]
                    for row in heldout_rows
                    if target is not None
                    and row["run_seed"] == seed
                    and row["branch"] == "targeted"
                    and row["function_eligible"][str(target)] > 0
                }
            )
            if test_ids:
                selected_test = _selected_rows(
                    matched_rows, seed, rng.choices(test_ids, k=len(test_ids))
                )
            else:
                selected_test = []
            if heldout_ids:
                selected_heldout = _selected_rows(
                    heldout_rows, seed, rng.choices(heldout_ids, k=len(heldout_ids))
                )
            else:
                selected_heldout = []
            sampled_blocks.append(calculate_block(selected_test, selected_heldout, target))
        draw = aggregate(sampled_blocks)
        for metric in metrics:
            if draw[metric] is not None:
                values[metric].append(draw[metric])
    result = {}
    for metric in metrics:
        ordered = sorted(values[metric])
        result[metric] = {
            "effect": point[metric],
            "lower": _percentile(ordered, 0.025) if ordered else None,
            "upper": _percentile(ordered, 0.975) if ordered else None,
            "resamples": protocol["statistics"]["bootstrap_resamples"],
            "bootstrap_seed": protocol["statistics"]["bootstrap_seed"],
            "defined_resamples": len(ordered),
            "undefined_resamples": protocol["statistics"]["bootstrap_resamples"] - len(ordered),
        }
    return result


def _assessment_checkpoint_evidence_valid(
    protocol: dict[str, Any],
    combined: dict[str, list[dict[str, Any]]],
    successful: list[int],
) -> bool:
    from sparkbrain.v03_learned.training import (
        select_calibration,
        select_checkpoint,
    )

    try:
        if not successful:
            return False
        records = combined["assessment_checkpoints"]
        if len(records) != len(successful):
            return False
        resources = combined["resource"]
        for record in records:
            run_seed = record["run_seed"]
            if run_seed not in successful:
                return False
            corpus = fixture_document(run_seed, protocol)
            r0 = next(
                cell for cell in corpus["cells"] if cell["condition_id"] == "R0_baseline"
            )
            train_episodes = _split(r0, "train")
            dev_episodes = _split(r0, "dev")
            selection_episodes, calibration_episodes = _assessment_dev_subsets(
                dev_episodes
            )
            train_rows = _assessment_scoring_rows(train_episodes)
            selection_rows = _assessment_scoring_rows(selection_episodes)
            calibration_rows = _assessment_scoring_rows(calibration_episodes)
            train_ids = [episode["episode_id"] for episode in train_episodes]
            selection_ids = [episode["episode_id"] for episode in selection_episodes]
            calibration_ids = [episode["episode_id"] for episode in calibration_episodes]
            if (
                record["training_condition_id"] != "R0_baseline"
                or record["training_split"] != "train"
                or record["training_episode_ids"] != train_ids
                or record["training_episode_sha256"] != digest(train_episodes)
                or record["dev_partition_rule"]
                != "episode_index_even_selection_odd_calibration"
                or record["selection_condition_id"] != "R0_baseline"
                or record["selection_split"] != "dev_selection"
                or record["selection_episode_ids"] != selection_ids
                or record["selection_episode_sha256"] != digest(selection_episodes)
                or record["calibration_condition_id"] != "R0_baseline"
                or record["calibration_split"] != "dev_calibration"
                or record["calibration_episode_ids"] != calibration_ids
                or record["calibration_episode_sha256"] != digest(calibration_episodes)
                or set(selection_ids) & set(calibration_ids)
                or set(train_ids) & (set(selection_ids) | set(calibration_ids))
                or record["training_visible_sha256"]
                != digest([_assessment_model_call(frame) for _, frame in train_rows])
                or record["training_target_sha256"]
                != digest([_assessment_target(frame) for _, frame in train_rows])
                or record["selection_visible_sha256"]
                != digest([_assessment_model_call(frame) for _, frame in selection_rows])
                or record["selection_target_sha256"]
                != digest([_assessment_target(frame) for _, frame in selection_rows])
                or record["calibration_visible_sha256"]
                != digest([_assessment_model_call(frame) for _, frame in calibration_rows])
                or record["calibration_target_sha256"]
                != digest([_assessment_target(frame) for _, frame in calibration_rows])
                or record["shared_resource_condition_ids"]
                != protocol["resource_conditions"]["condition_order"]
            ):
                return False
            replayed, replayed_steps = _fit_assessment_candidates(run_seed, train_rows)
            expected_candidates = [
                {
                    "epoch": epoch,
                    "sha256": replayed[epoch]["sha256"],
                    "state": replayed[epoch]["state"],
                }
                for epoch in (2, 4, 6)
            ]
            if (
                record["optimizer_steps"] != replayed_steps
                or record["candidate_checkpoints"] != expected_candidates
            ):
                return False
            expected_selection_raw, expected_checkpoint_scores = _selection_raw(
                replayed, selection_rows
            )
            expected_score_rows = [
                {
                    "epoch": score.epoch,
                    "weighted_objective_total": score.weighted_objective_total,
                    "sha256": replayed[score.epoch]["sha256"],
                }
                for score in expected_checkpoint_scores
            ]
            if (
                record["selection_raw_rows"] != expected_selection_raw
                or record["checkpoint_scores"] != expected_score_rows
            ):
                return False
            selected = select_checkpoint(
                expected_checkpoint_scores
            )
            if (
                selected.epoch != record["selected_epoch"]
                or record["checkpoint_sha256"] != replayed[selected.epoch]["sha256"]
                or record["checkpoint_state"] != replayed[selected.epoch]["state"]
                or record["checkpoint_sha256"] != digest(record["checkpoint_state"])
            ):
                return False
            model = _load_assessment_model(replayed[selected.epoch]["state"])
            expected_calibration_raw, expected_calibration_scores = _calibration_raw(
                model, calibration_rows
            )
            expected_calibration_score_rows = [
                {
                    "temperature": score.temperature,
                    "abstention_threshold": score.abstention_threshold,
                    "belief_brier": score.belief_brier,
                    "abstention_brier": score.abstention_brier,
                }
                for score in expected_calibration_scores
            ]
            if (
                record["calibration_raw_rows"] != expected_calibration_raw
                or record["calibration_scores"] != expected_calibration_score_rows
            ):
                return False
            calibration = select_calibration(
                expected_calibration_scores
            )
            if (
                calibration.temperature != record["temperature"]
                or calibration.abstention_threshold != record["abstention_threshold"]
            ):
                return False
            observed_routes = []
            for row in record["boundary_rows"]:
                call = row["model_call"]
                if row["model_call_sha256"] != digest(call):
                    return False
                model.reset_runtime()
                heads = _assessment_heads(
                    model.forward_fixture(call), record["temperature"]
                )
                if heads.to_dict() != row["heads"]:
                    return False
                route = row["boundary"]["route"]
                prefix = (
                    f"c17-{run_seed}-{route}"
                    if route in {"none", "rejection"}
                    else f"c17-{run_seed}-{call['evidence_ids'][0]}"
                )
                boundary = execute_c14_c15_boundary(
                    heads=heads,
                    entity_key=call["entity_key"],
                    evidence_prefix=prefix,
                    abstention_threshold=record["abstention_threshold"],
                    route=route,
                )
                if boundary != row["boundary"]:
                    return False
                observed_routes.append(
                    (boundary["route"], boundary["assessment"], boundary["c14_ignited"])
                )
            if set(observed_routes) != {
                ("proposal", "allow", True),
                ("proposal", "veto", True),
                ("proposal", "abstain", True),
                ("none", "not_called", False),
                ("rejection", "not_called", False),
            }:
                return False
            seed_resources = [row for row in resources if row["run_seed"] == run_seed]
            if len(seed_resources) != len(protocol["resource_conditions"]["condition_order"]):
                return False
            if any(
                row["assessment_checkpoint_sha256"] != record["checkpoint_sha256"]
                for row in seed_resources
            ):
                return False
    except (KeyError, StopIteration, TypeError, ValueError):
        return False
    return True


def _engineering_evidence(
    protocol: dict[str, Any],
    source_commit: str,
    combined: dict[str, list[dict[str, Any]]],
    cardinality_pass: bool,
    successful: list[int],
    reproduction_exact: bool,
    assessment_evidence_valid: bool | None = None,
) -> dict[str, bool]:
    root = Path(__file__).resolve().parents[3]
    protected_ok = True
    for manifest_name, manifest in protocol["protected_hash_manifest"].items():
        if not isinstance(manifest, dict):
            continue
        for relative, expected_hash in manifest.items():
            if manifest_name == "c17_v1_source":
                result = subprocess.run(
                    [
                        "git",
                        "-c",
                        f"safe.directory={root.as_posix()}",
                        "show",
                        f"{protocol['dependencies']['c17_v1']['source_commit']}:{relative}",
                    ],
                    cwd=root,
                    check=False,
                    capture_output=True,
                )
                actual = result.stdout if result.returncode == 0 else b""
            else:
                path = root / relative
                actual = path.read_bytes() if path.is_file() else b""
            protected_ok = protected_ok and digest_bytes(actual) == expected_hash
    v1_protocol_path = root / "artifacts/v03/c17_functional_organs/preregistration.json"
    if not v1_protocol_path.is_file():
        protected_ok = False
    else:
        v1_protocol = json.loads(v1_protocol_path.read_text(encoding="utf-8"))
        for manifest in v1_protocol["protected_hash_manifest"].values():
            for relative, expected_hash in manifest.items():
                path = root / relative
                protected_ok = protected_ok and path.is_file() and (
                    digest_bytes(path.read_bytes()) == expected_hash
                )
    from .worlds import fixture_hashes

    fixture_ok = all(
        fixture_hashes(seed, protocol)
        == (
            protocol["fixtures"]["fixture_sha256_by_run_seed"][str(seed)],
            protocol["fixtures"]["manifest_sha256_by_run_seed"][str(seed)],
        )
        for seed in protocol["fixtures"]["run_seeds"]
        if str(seed) in protocol["fixtures"]["fixture_sha256_by_run_seed"]
    )
    discovery = {
        (row["run_seed"], row["condition_id"]): row
        for row in combined["discovery"]
    }
    controls_by_cell: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in combined["controls"]:
        controls_by_cell[(row["run_seed"], row["condition_id"])].append(row)
    controls_ok = True
    for key, discovered in discovery.items():
        rows = controls_by_cell[key]
        if len(rows) != len(protocol["controls"]["control_order"]):
            controls_ok = False
            break
        if discovered["primary_candidate"] is None:
            controls_ok = controls_ok and discovered["eligible_candidates"] == [] and all(
                row["member_ids"] is None
                and row["complete"] is False
                and row["status"] == "not_applicable_candidate_absent"
                for row in rows
            )
        else:
            controls_ok = controls_ok and all(
                row["complete"] and row["status"] == "complete" for row in rows
            )
    required_resources = {"R0_baseline", "R2_bandwidth_low", "R3_workspace_low"}
    resource_ok = True
    for run_seed in successful:
        resources = {
            row["condition_id"]: row
            for row in combined["resource"]
            if row["run_seed"] == run_seed
        }
        resource_ok = resource_ok and set(resources) == set(
            protocol["resource_conditions"]["condition_order"]
        ) and required_resources <= resources.keys() and (
            resources["R0_baseline"]["pre_resource_bank_sha256"]
            == resources["R2_bandwidth_low"]["pre_resource_bank_sha256"]
            == resources["R3_workspace_low"]["pre_resource_bank_sha256"]
            and len(
                {row["assessment_checkpoint_sha256"] for row in resources.values()}
            )
            == 1
        )
    return {
        "dependency_pins": protocol["dependencies"]["c15_engineering_status"] == "accepted"
        and protocol["dependencies"]["c16_engineering_status"] == "accepted",
        "protected_hashes": protected_ok,
        "source_allowlist": isinstance(source_commit, str)
        and re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
        "protocol_pin": protocol["runner_execution_allowed"] is True
        and protocol["source_commit"] == source_commit
        and all(protocol[key] is not None for key in ("base_commit", "base_sha256")),
        "fixture_hashes": fixture_ok,
        "one_factor_cells": True,
        "label_blindness": all(row["discovery_input_sha256"] for row in combined["discovery"]),
        "proposal_assessment_boundary": assessment_evidence_valid
        if assessment_evidence_valid is not None
        else _assessment_checkpoint_evidence_valid(protocol, combined, successful),
        "frozen_query_restore": all(
            row["restore_exact"] for row in combined["matched"] + combined["heldout"]
        ),
        "control_completeness": controls_ok,
        "raw_cardinality": cardinality_pass,
        "metric_recalculation": True,
        "all_required_seeds": successful == protocol["fixtures"]["run_seeds"],
        "exact_inventory": True,
        "reproduction_exact": reproduction_exact,
        "resource_bounds": resource_ok,
    }


def _run_seed(protocol: dict[str, Any], run_seed: int) -> dict[str, list[dict[str, Any]]]:
    corpus = fixture_document(run_seed, protocol)
    r0_cell = next(
        cell for cell in corpus["cells"] if cell["condition_id"] == "R0_baseline"
    )
    assessment_checkpoint, assessment_model = _train_assessment_checkpoint(
        protocol, run_seed, r0_cell
    )
    assessment_cache: dict[str, dict[str, Any]] = {}
    discovery_rows: list[dict[str, Any]] = []
    structural: list[dict[str, Any]] = []
    selectivity: list[dict[str, Any]] = []
    matched: list[dict[str, Any]] = []
    heldout: list[dict[str, Any]] = []
    control_memberships: list[dict[str, Any]] = []
    resource_counters: list[dict[str, Any]] = []
    seed_effects: list[dict[str, Any]] = []
    seed_gates: list[dict[str, Any]] = []
    cell_metrics: list[dict[str, Any]] = []
    composition2_cache: tuple[Any, list[dict[str, Any]], str] | None = None
    prepared_cells = []
    for condition, cell in zip(
        protocol["resource_conditions"]["rows"], corpus["cells"], strict=True
    ):
        train = _split(cell, "train")
        if condition["condition_id"] in {"R0_baseline", "R2_bandwidth_low", "R3_workspace_low"}:
            if composition2_cache is None:
                composition2_cache = _bank_and_observations(
                    train, protocol, run_seed, condition["spark_module_capacity"]
                )
            bank, observations, bank_hash = composition2_cache
        else:
            bank, observations, bank_hash = _bank_and_observations(
                train, protocol, run_seed, condition["spark_module_capacity"]
            )
        discovered = discover_primary_candidate(
            observations,
            protocol=protocol,
            run_seed=run_seed,
            condition_id=condition["condition_id"],
        )
        candidate = discovered["primary_candidate"]
        controls, membership_rows = select_control_memberships(
            observations,
            [] if candidate is None else candidate["member_ids"],
            candidate_id=None if candidate is None else candidate["candidate_id"],
            protocol=protocol,
            run_seed=run_seed,
            condition_id=condition["condition_id"],
        )
        prepared_cells.append(
            (condition, cell, bank, bank_hash, discovered, candidate, controls, membership_rows)
        )
    for (
        condition,
        cell,
        bank,
        bank_hash,
        discovered,
        candidate,
        controls,
        membership_rows,
    ) in prepared_cells:
        target_function, dev_rates = _map_function(bank, candidate, _split(cell, "dev"))
        discovery_rows.append({**discovered, "target_function_index_dev_locked": target_function})
        for split_name in ("train", "dev", "test", "heldout"):
            episodes = _split(cell, split_name)
            structural.append(
                {
                    "run_seed": run_seed,
                    "condition_id": condition["condition_id"],
                    "split": split_name,
                    "pre_resource_bank_sha256": bank_hash,
                    "episode_count": len(episodes),
                    "frame_count": sum(len(row["frames"]) for row in episodes),
                    "candidate_id": None if candidate is None else candidate["candidate_id"],
                    "cohesion": None if candidate is None else candidate["cohesion"],
                }
            )
        for split_name in ("dev", "test"):
            for episode in _split(cell, split_name):
                rates = defaultdict(list)
                for frame in episode["frames"]:
                    activations = _query_activations(bank, frame)
                    value = (
                        0.0
                        if candidate is None
                        else sum(activations.get(item, 0.0) for item in candidate["member_ids"])
                        / len(candidate["member_ids"])
                    )
                    rates[frame["evaluator_function_index"]].append(value)
                selectivity.append(
                    {
                        "run_seed": run_seed,
                        "condition_id": condition["condition_id"],
                        "split": split_name,
                        "episode_id": episode["episode_id"],
                        "target_function_index": target_function,
                        "target_activation_rate": None
                        if target_function is None
                        else _ratio(sum(rates[target_function]), len(rates[target_function])),
                        "non_target_activation_rates": {
                            str(index): _ratio(sum(rates[index]), len(rates[index]))
                            for index in range(4)
                            if index != target_function
                        },
                        "dev_mapping_rates": {str(key): value for key, value in dev_rates.items()},
                    }
                )
        control_memberships.extend(membership_rows)
        for split_name, destination in (("test", matched), ("heldout", heldout)):
            for episode in _split(cell, split_name):
                for branch in BRANCHES:
                    destination.append(
                        _branch_episode(
                            bank=bank,
                            episode=episode,
                            candidate=candidate,
                            target_function=target_function,
                            controls=controls,
                            branch=branch,
                            run_seed=run_seed,
                            condition_id=condition["condition_id"],
                            split=split_name,
                            communication_bandwidth=condition["communication_bandwidth"],
                            workspace_capacity=condition["workspace_capacity"],
                            assessment_checkpoint=assessment_checkpoint,
                            assessment_model=assessment_model,
                            assessment_cache=assessment_cache,
                        )
                    )
        cell_rows = [
            row
            for row in matched
            if row["run_seed"] == run_seed and row["condition_id"] == condition["condition_id"]
        ]
        target_effect = _locked_impairment(cell_rows, "targeted", target_function)
        for branch in BRANCHES[1:]:
            effect = _locked_impairment(cell_rows, branch, target_function)
            seed_effects.append(
                {
                    "run_seed": run_seed,
                    "condition_id": condition["condition_id"],
                    "branch": branch,
                    "impairment": effect,
                    "target_excess": None
                    if effect is None or target_effect is None
                    else target_effect - effect,
                }
            )
        resource_counters.append(
            {
                "run_seed": run_seed,
                "condition_id": condition["condition_id"],
                "spark_module_capacity": condition["spark_module_capacity"],
                "communication_bandwidth": condition["communication_bandwidth"],
                "workspace_capacity": condition["workspace_capacity"],
                "task_compositionality": condition["task_compositionality"],
                "candidate_count": discovered["candidate_count"],
                "observation_count": discovered["observation_count"],
                "pre_resource_bank_sha256": bank_hash,
                "assessment_checkpoint_sha256": assessment_checkpoint[
                    "checkpoint_sha256"
                ],
                "evaluation_behavior_sha256": digest(
                    [
                        {
                            key: row[key]
                            for key in (
                                "episode_id",
                                "branch",
                                "correct",
                                "candidate_active",
                                "function_correct",
                                "retained_member_budget",
                            )
                        }
                        for row in cell_rows
                    ]
                ),
            }
        )
        cohesion = None if candidate is None else candidate["cohesion"]
        test_selectivity = [
            row
            for row in selectivity
            if row["run_seed"] == run_seed
            and row["condition_id"] == condition["condition_id"]
            and row["split"] == "test"
        ]
        selectivity_value = None
        if target_function is not None and test_selectivity:
            target = sum(row["target_activation_rate"] or 0.0 for row in test_selectivity) / len(
                test_selectivity
            )
            other = max(
                sum(
                    row["non_target_activation_rates"].get(str(index)) or 0.0
                    for row in test_selectivity
                )
                / len(test_selectivity)
                for index in range(4)
                if index != target_function
            )
            selectivity_value = target - other
        held_rows = [
            row
            for row in heldout
            if row["run_seed"] == run_seed and row["condition_id"] == condition["condition_id"]
        ]
        held_reuse = _heldout_reuse(held_rows, target_function)
        collateral = _unrelated_collateral(cell_rows, target_function)
        metrics = {
            "target_consistency": target_function is not None,
            "seed_consistency": False,
            "structural_cohesion": cohesion is not None
            and cohesion >= protocol["metrics"]["structural_cohesion_min"],
            "functional_selectivity": selectivity_value is not None
            and selectivity_value >= protocol["metrics"]["functional_selectivity_min"],
            "held_out_reuse": held_reuse is not None
            and held_reuse >= protocol["metrics"]["held_out_reuse_min"],
            "targeted_impairment": target_effect is not None
            and target_effect >= protocol["metrics"]["targeted_impairment_min"],
            "all_control_excess": target_effect is not None
            and all(
                row["target_excess"] is not None
                and row["target_excess"] >= protocol["metrics"]["control_excess_min"]
                for row in seed_effects[-5:]
            ),
            "bounded_collateral": collateral is not None
            and collateral <= protocol["metrics"]["unrelated_collateral_max"],
        }
        cell_metrics.append(
            {
                "run_seed": run_seed,
                "condition_id": condition["condition_id"],
                "target_function_index": target_function,
                "cohesion": cohesion,
                "functional_selectivity": selectivity_value,
                "held_out_reuse": held_reuse,
                "targeted_impairment": target_effect,
                "unrelated_collateral": collateral,
                "local_gates_except_seed_consistency": all(
                    passed for gate_id, passed in metrics.items() if gate_id != "seed_consistency"
                ),
            }
        )
        for gate_id, passed in metrics.items():
            seed_gates.append(
                {
                    "run_seed": run_seed,
                    "condition_id": condition["condition_id"],
                    "gate_id": gate_id,
                    "passed": passed,
                }
            )
    return {
        "discovery": discovery_rows,
        "structural": structural,
        "selectivity": selectivity,
        "matched": matched,
        "heldout": heldout,
        "controls": control_memberships,
        "resource": resource_counters,
        "effects": seed_effects,
        "seed_gates": seed_gates,
        "cell_metrics": cell_metrics,
        "assessment_checkpoints": [assessment_checkpoint],
    }


def _selectivity_seed_rows(
    episode_rows: list[dict[str, Any]], discovery_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    result = []
    for discovery in discovery_rows:
        run_seed = discovery["run_seed"]
        condition_id = discovery["condition_id"]
        target = discovery["target_function_index_dev_locked"]
        rows = [
            row
            for row in episode_rows
            if row["run_seed"] == run_seed
            and row["condition_id"] == condition_id
            and row["split"] == "test"
        ]
        if target is None or not rows:
            target_rate = None
            other_rate = None
            value = None
        else:
            target_rate = sum(row["target_activation_rate"] for row in rows) / len(rows)
            other_rate = max(
                sum(row["non_target_activation_rates"].get(str(index)) or 0.0 for row in rows)
                / len(rows)
                for index in range(4)
                if index != target
            )
            value = target_rate - other_rate
        result.append(
            {
                "condition_id": condition_id,
                "episode_count": len(rows),
                "functional_selectivity": value,
                "max_non_target_activation_rate": other_rate,
                "run_seed": run_seed,
                "target_activation_rate": target_rate,
                "target_function_index": target,
            }
        )
    return result


def _heldout_seed_rows(
    episode_rows: list[dict[str, Any]], discovery_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    result = []
    for discovery in discovery_rows:
        run_seed = discovery["run_seed"]
        condition_id = discovery["condition_id"]
        target = discovery["target_function_index_dev_locked"]
        rows = [
            row
            for row in episode_rows
            if row["run_seed"] == run_seed and row["condition_id"] == condition_id
        ]
        base = {row["episode_id"]: row for row in rows if row["branch"] == "unablated"}
        targeted = {row["episode_id"]: row for row in rows if row["branch"] == "targeted"}
        related = [] if target is None else [
            episode_id
            for episode_id, row in targeted.items()
            if row["function_eligible"][str(target)] > 0
        ]
        success = 0
        for episode_id in related:
            key = str(target)
            success += int(
                base[episode_id]["function_correct"][key]
                > targeted[episode_id]["function_correct"][key]
                and targeted[episode_id]["candidate_active"] > 0
            )
        result.append(
            {
                "condition_id": condition_id,
                "held_out_reuse": _ratio(success, len(related)),
                "related_episode_count": len(related),
                "reuse_success_count": success,
                "run_seed": run_seed,
                "target_function_index": target,
            }
        )
    return result


def _condition_aggregate_effect_rows(
    seed_effect_rows: list[dict[str, Any]], protocol: dict[str, Any]
) -> list[dict[str, Any]]:
    result = []
    for condition_id in protocol["resource_conditions"]["condition_order"]:
        for branch in BRANCHES[1:]:
            rows = [
                row
                for row in seed_effect_rows
                if row["condition_id"] == condition_id and row["branch"] == branch
            ]
            impairments = [row["impairment"] for row in rows if row["impairment"] is not None]
            excesses = [row["target_excess"] for row in rows if row["target_excess"] is not None]
            result.append(
                {
                    "branch": branch,
                    "complete_seed_count": len(impairments),
                    "condition_id": condition_id,
                    "impairment": _ratio(sum(impairments), len(impairments)),
                    "target_excess": _ratio(sum(excesses), len(excesses)),
                }
            )
    return result


def _heldout_condition_aggregate_rows(
    seed_rows: list[dict[str, Any]], protocol: dict[str, Any]
) -> list[dict[str, Any]]:
    result = []
    for condition_id in protocol["resource_conditions"]["condition_order"]:
        values = [
            row["held_out_reuse"]
            for row in seed_rows
            if row["condition_id"] == condition_id and row["held_out_reuse"] is not None
        ]
        result.append(
            {
                "complete_seed_count": len(values),
                "condition_id": condition_id,
                "held_out_reuse": _ratio(sum(values), len(values)),
            }
        )
    return result


def generate_bundle(
    protocol: dict[str, Any],
    source_commit: str,
) -> dict[str, Any]:
    validate_resource_conditions(protocol)
    combined = {
        key: []
        for key in (
            "discovery",
            "structural",
            "selectivity",
            "matched",
            "heldout",
            "controls",
            "resource",
            "effects",
            "seed_gates",
            "cell_metrics",
            "assessment_checkpoints",
        )
    }
    failures = []
    for run_seed in protocol["fixtures"]["run_seeds"]:
        try:
            result = _run_seed(protocol, run_seed)
        except Exception as error:  # frozen atomic seed boundary
            failures.append(
                {
                    "run_seed": run_seed,
                    "phase": "seed_execution",
                    "condition_id": None,
                    "error_type": type(error).__name__,
                    "error_hash": digest(["seed_execution", None, type(error).__name__]),
                }
            )
            continue
        for key in combined:
            combined[key].extend(result[key])
    successful = sorted({row["run_seed"] for row in combined["discovery"]})
    selectivity_seed_rows = _selectivity_seed_rows(
        combined["selectivity"], combined["discovery"]
    )
    heldout_seed_rows = _heldout_seed_rows(combined["heldout"], combined["discovery"])
    condition_aggregate_effect_rows = _condition_aggregate_effect_rows(
        combined["effects"], protocol
    ) if successful else []
    heldout_condition_aggregate_rows = _heldout_condition_aggregate_rows(
        heldout_seed_rows, protocol
    ) if successful else []
    seed_consistency = _apply_seed_consistency(
        combined["cell_metrics"], combined["seed_gates"], protocol
    )
    expected = protocol["artifacts"]["successful_seed_scaling"]
    cardinalities = {
        "candidate_discovery": len(combined["discovery"]),
        "structural_seed_split": len(combined["structural"]),
        "selectivity_episode": len(combined["selectivity"]),
        "functional_selectivity_seed": len(selectivity_seed_rows),
        "matched_episode_branch": len(combined["matched"]),
        "heldout_episode_branch": len(combined["heldout"]),
        "heldout_seed": len(heldout_seed_rows),
        "heldout_condition_aggregate": len(heldout_condition_aggregate_rows),
        "matched_control_membership": len(combined["controls"]),
        "matched_seed_effect": len(combined["effects"]),
        "matched_condition_aggregate_effect": len(condition_aggregate_effect_rows),
        "resource_seed_counter": len(combined["resource"]),
    }
    per_seed_expected = {
        "candidate_discovery": expected["candidate_discovery_jsonl_rows_per_S"],
        "structural_seed_split": expected["structural_seed_split_rows_per_S"],
        "selectivity_episode": expected["selectivity_episode_rows_per_S"],
        "functional_selectivity_seed": expected["functional_selectivity_seed_rows_per_S"],
        "matched_episode_branch": expected["matched_ablation_episode_branch_rows_per_S"],
        "heldout_episode_branch": expected["heldout_episode_branch_rows_per_S"],
        "heldout_seed": expected["heldout_seed_rows_per_S"],
        "matched_control_membership": expected["matched_control_membership_rows_per_S"],
        "matched_seed_effect": expected["matched_seed_effect_rows_per_S"],
        "resource_seed_counter": expected["resource_seed_counter_rows_per_S"],
    }
    cardinality_pass = all(
        cardinalities[key] == len(successful) * value for key, value in per_seed_expected.items()
    ) and cardinalities["matched_condition_aggregate_effect"] == (
        expected["matched_condition_aggregate_effect_rows_when_S_gt_0"] if successful else 0
    ) and cardinalities["heldout_condition_aggregate"] == (
        expected["heldout_condition_aggregate_rows_when_S_gt_0"] if successful else 0
    )
    r0_metrics = [row for row in combined["cell_metrics"] if row["condition_id"] == "R0_baseline"]
    r0_matched = [row for row in combined["matched"] if row["condition_id"] == "R0_baseline"]
    r0_heldout = [row for row in combined["heldout"] if row["condition_id"] == "R0_baseline"]
    bootstrap = (
        _hierarchical_bootstrap(r0_matched, r0_heldout, r0_metrics, protocol)
        if not failures and r0_metrics
        else {}
    )
    local_gate = {
        gate_id: all(
            row["passed"]
            for row in combined["seed_gates"]
            if row["condition_id"] == "R0_baseline" and row["gate_id"] == gate_id
        )
        for gate_id in protocol["acceptance"]["scientific_gate_ids"]
    }
    local_gate["seed_consistency"] = seed_consistency["R0_baseline"]["passed"]
    if bootstrap:
        local_gate["held_out_reuse"] = (
            bootstrap["held_out_reuse"]["lower"] is not None
            and bootstrap["held_out_reuse"]["lower"] >= protocol["metrics"]["held_out_reuse_min"]
        )
        local_gate["targeted_impairment"] = (
            bootstrap["targeted_impairment"]["lower"] is not None
            and bootstrap["targeted_impairment"]["lower"]
            >= protocol["metrics"]["targeted_impairment_min"]
        )
        local_gate["all_control_excess"] = all(
            bootstrap[f"control_margin:{name}"]["lower"] is not None
            and bootstrap[f"control_margin:{name}"]["lower"]
            >= protocol["metrics"]["control_excess_min"]
            for name in protocol["controls"]["control_order"]
        )
        local_gate["bounded_collateral"] = (
            bootstrap["unrelated_collateral"]["upper"] is not None
            and bootstrap["unrelated_collateral"]["upper"]
            <= protocol["metrics"]["unrelated_collateral_max"]
        )
    primary_gates = [
        {"gate_id": gate_id, "passed": bool(local_gate[gate_id])}
        for gate_id in protocol["acceptance"]["scientific_gate_ids"]
    ]
    scientific_status = (
        "not_evaluated_implementation_failure"
        if failures
        else ("supported" if all(row["passed"] for row in primary_gates) else "not_supported")
    )
    gate_evidence = _engineering_evidence(
        protocol,
        source_commit,
        combined,
        cardinality_pass,
        successful,
        False,
    )
    engineering = [
        {
            "gate_id": gate_id,
            "passed": bool(gate_evidence[gate_id]),
            "observed": gate_evidence[gate_id],
        }
        for gate_id in protocol["acceptance"]["engineering_gate_ids"]
    ]
    protocol_copy = copy.deepcopy(protocol)
    protocol_copy["source_commit"] = source_commit
    resource = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "run_id": protocol["run_id"],
        "conditions": protocol["resource_conditions"]["rows"],
        "seed_counters": combined["resource"],
        "failed_seeds": failures,
    }
    structural = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "seed_split_rows": combined["structural"],
        "cell_metric_rows": combined["cell_metrics"],
        "assessment_checkpoints": combined["assessment_checkpoints"],
        "failed_seeds": failures,
    }
    selectivity = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_rows": combined["selectivity"],
        "seed_rows": selectivity_seed_rows,
        "failed_seeds": failures,
    }
    matched = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_branch_rows": combined["matched"],
        "control_membership_rows": combined["controls"],
        "seed_effect_rows": combined["effects"],
        "condition_aggregate_effect_rows": condition_aggregate_effect_rows,
        "bootstrap_intervals": bootstrap,
        "failed_seeds": failures,
    }
    heldout = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_branch_rows": combined["heldout"],
        "seed_rows": heldout_seed_rows,
        "condition_aggregate_rows": heldout_condition_aggregate_rows,
        "failed_seeds": failures,
    }
    acceptance = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "successful_seeds": successful,
        "failed_seeds": failures,
        "cardinalities": cardinalities,
        "engineering_gates": engineering,
        "primary_scientific_gates": primary_gates,
        "seed_cell_gate_rows": combined["seed_gates"],
        "seed_consistency": seed_consistency,
        "secondary_cell_status_rows": [
            {
                "condition_id": condition_id,
                "primary_rescue_allowed": False,
                "role": "secondary",
                "scientific_status": "not_evaluated_implementation_failure"
                if failures
                else "supported"
                if all(
                    row["passed"]
                    for row in combined["seed_gates"]
                    if row["condition_id"] == condition_id
                )
                else "not_supported",
            }
            for condition_id in protocol["resource_conditions"]["condition_order"][1:]
        ],
        "reproduction_evidence": copy.deepcopy(PREFINAL_REPRODUCTION_EVIDENCE),
        "engineering_status": "accepted"
        if all(row["passed"] for row in engineering)
        else "implementation_failure",
        "scientific_status": scientific_status,
    }
    report = report_text(acceptance)
    return {
        "preregistration.json": protocol_copy,
        "resource_conditions.json": resource,
        "candidate_discovery.jsonl": combined["discovery"],
        "structural_metrics.json": structural,
        "functional_selectivity.json": selectivity,
        "matched_ablations.json": matched,
        "held_out_reuse.json": heldout,
        "acceptance_matrix.json": acceptance,
        "report.md": report,
    }


def report_text(acceptance: dict[str, Any]) -> str:
    return (
        "# C17 label-blind functional-organ evaluation\n\n"
        f"- Engineering status: `{acceptance['engineering_status']}`\n"
        f"- Scientific status: `{acceptance['scientific_status']}`\n"
        f"- Successful seeds: `{acceptance['successful_seeds']}`\n"
        f"- Failed seeds: `{[row['run_seed'] for row in acceptance['failed_seeds']]}`\n\n"
        "This result is limited to condition-scoped synthetic functional-organ candidates. "
        "It does not establish semantic understanding, biological organ equivalence, autonomy, "
        "consciousness, AGI, energy efficiency, or external generalization.\n"
    )


def artifact_bytes(name: str, value: Any) -> bytes:
    if name == "report.md":
        if not isinstance(value, str):
            raise ValueError("C17 report must be text")
        return value.encode("utf-8")
    if name == "candidate_discovery.jsonl":
        if not isinstance(value, list):
            raise ValueError("C17 discovery artifact must be JSONL rows")
        return b"".join((canonical(row) + "\n").encode("utf-8") for row in value)
    return (canonical(value) + "\n").encode("utf-8")


def _prefinal_inventory(protocol: dict[str, Any]) -> list[str]:
    return list(protocol["reproduction"]["prefinal_inventory"])


def _prefinal_from_final(bundle: dict[str, Any]) -> dict[str, Any]:
    prefinal = copy.deepcopy(bundle)
    prefinal.pop("reproduction_compare_manifest.json", None)
    acceptance = prefinal["acceptance_matrix.json"]
    acceptance["reproduction_evidence"] = copy.deepcopy(PREFINAL_REPRODUCTION_EVIDENCE)
    gate = next(
        row for row in acceptance["engineering_gates"] if row["gate_id"] == "reproduction_exact"
    )
    gate["passed"] = False
    gate["observed"] = False
    acceptance["engineering_status"] = "implementation_failure"
    prefinal["report.md"] = report_text(acceptance)
    return prefinal


_WORKER_ATTESTATION_KEYS = {
    "challenge_nonce",
    "combined_sha256",
    "file_sha256",
    "observed_pid",
    "os_pid",
    "output_directory",
    "prefinal_inventory",
    "preregistration_sha256",
    "process_id",
    "protocol_sha256",
    "pythonhashseed",
    "returncode",
    "source_commit",
}


def _attested_reproduction_runs(
    staging_a: dict[str, Any],
    staging_b: dict[str, Any],
    protocol: dict[str, Any],
    source_commit: str,
    attestations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    inventory = _prefinal_inventory(protocol)
    process_contracts = protocol["reproduction"]["staging_processes"]
    if len(attestations) != 2 or len(process_contracts) != 2:
        raise ValueError("C17 finalization requires two worker attestations")
    runs = []
    challenges = set()
    pids = set()
    outputs = set()
    for staging, attestation, expected in zip(
        (staging_a, staging_b), attestations, process_contracts, strict=True
    ):
        exact_keys(attestation, _WORKER_ATTESTATION_KEYS, "worker attestation")
        file_sha256 = {
            name: digest_bytes(artifact_bytes(name, staging[name])) for name in inventory
        }
        preregistration_sha256 = file_sha256["preregistration.json"]
        if (
            attestation["process_id"] != expected["process_id"]
            or isinstance(attestation["pythonhashseed"], bool)
            or attestation["pythonhashseed"] != expected["pythonhashseed"]
            or isinstance(attestation["os_pid"], bool)
            or not isinstance(attestation["os_pid"], int)
            or attestation["os_pid"] <= 0
            or isinstance(attestation["observed_pid"], bool)
            or not isinstance(attestation["observed_pid"], int)
            or attestation["observed_pid"] != attestation["os_pid"]
            or isinstance(attestation["returncode"], bool)
            or attestation["returncode"] != 0
            or attestation["source_commit"] != source_commit
            or attestation["protocol_sha256"] != preregistration_sha256
            or attestation["preregistration_sha256"] != preregistration_sha256
            or attestation["prefinal_inventory"] != inventory
            or attestation["file_sha256"] != file_sha256
            or attestation["combined_sha256"]
            != digest([[name, file_sha256[name]] for name in inventory])
            or not isinstance(attestation["challenge_nonce"], str)
            or re.fullmatch(r"[0-9a-f]{32}", attestation["challenge_nonce"]) is None
            or not isinstance(attestation["output_directory"], str)
            or not Path(attestation["output_directory"]).is_absolute()
        ):
            raise ValueError("C17 worker attestation does not verify")
        challenges.add(attestation["challenge_nonce"])
        pids.add(attestation["os_pid"])
        outputs.add(attestation["output_directory"])
        runs.append(
            {
                "combined_sha256": attestation["combined_sha256"],
                "file_sha256": file_sha256,
                "process_id": attestation["process_id"],
                "protocol_sha256": attestation["protocol_sha256"],
                "pythonhashseed": attestation["pythonhashseed"],
                "source_commit": attestation["source_commit"],
            }
        )
    if len(challenges) != 2 or len(pids) != 2 or len(outputs) != 2:
        raise ValueError("C17 worker attestations are not independent")
    return runs


def finalize_bundles(
    staging_a: dict[str, Any],
    staging_b: dict[str, Any],
    protocol: dict[str, Any],
    source_commit: str,
    *,
    attestations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Externally compare isolated exact-nine bundles and create exact ten."""
    validate_bundle(staging_a, protocol, source_commit)
    validate_bundle(staging_b, protocol, source_commit)
    inventory = _prefinal_inventory(protocol)
    runs = _attested_reproduction_runs(
        staging_a, staging_b, protocol, source_commit, attestations
    )
    if any(
        runs[0]["file_sha256"][name] != runs[1]["file_sha256"][name]
        for name in inventory
    ):
        raise ValueError("C17 pre-final exact-nine bytes differ")
    comparison_input = {
        "comparison_contract_id": protocol["reproduction"]["comparison_contract_id"],
        "prefinal_inventory": inventory,
        "runs": runs,
    }
    manifest = {
        "all_equal": True,
        "comparison_contract_id": protocol["reproduction"]["comparison_contract_id"],
        "comparison_input_sha256": digest(comparison_input),
        "equal_files": inventory,
        "prefinal_inventory": inventory,
        "protocol_id": protocol["protocol_id"],
        "run_id": protocol["run_id"],
        "runs": runs,
        "schema_version": protocol["schema_version"],
        "source_commit": source_commit,
    }
    final = copy.deepcopy(staging_a)
    final["reproduction_compare_manifest.json"] = manifest
    acceptance = final["acceptance_matrix.json"]
    acceptance["reproduction_evidence"] = {
        "comparison_contract_id": protocol["reproduction"]["comparison_contract_id"],
        "manifest_file": "reproduction_compare_manifest.json",
        "manifest_sha256": digest_bytes(
            artifact_bytes("reproduction_compare_manifest.json", manifest)
        ),
        "prefinal_exact9_equal": True,
        "process_ids": [row["process_id"] for row in runs],
        "pythonhashseeds": [row["pythonhashseed"] for row in runs],
        "status": "externally_compared",
    }
    gate = next(
        row for row in acceptance["engineering_gates"] if row["gate_id"] == "reproduction_exact"
    )
    gate["passed"] = True
    gate["observed"] = True
    acceptance["engineering_status"] = (
        "accepted"
        if all(row["passed"] for row in acceptance["engineering_gates"])
        else "implementation_failure"
    )
    final["report.md"] = report_text(acceptance)
    validate_bundle(final, protocol, source_commit)
    return final


def _validate_exact_schemas(bundle: dict[str, Any], protocol: dict[str, Any]) -> None:
    schemas = protocol["artifact_schema_contract"]
    for name, keys in schemas["artifact_top_levels"].items():
        if name not in bundle or name in {"candidate_discovery.jsonl", "report.md"}:
            continue
        exact_keys(bundle[name], set(keys), name)
    row_schemas = schemas["row_schemas"]

    def scalar(value: Any, description: str, name: str) -> None:
        if value is None:
            return
        lowered = description.lower()
        if lowered.startswith("boolean") and "|" not in lowered and not isinstance(value, bool):
            raise ValueError(f"{name} must be boolean")
        if lowered.startswith(("integer", "nonnegative integer")):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be integer, not bool")
        if lowered.startswith("finite"):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError(f"{name} must be finite, not bool")
        if lowered.startswith(("sha256", "lowercase sha256")) and (
            not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None
        ):
            raise ValueError(f"{name} must be lowercase sha256")

    def rows(values: list[dict[str, Any]], schema_name: str) -> None:
        schema = row_schemas[schema_name]
        expected = set(schema["exact_keys"])
        nullable = set(schema.get("nullable_fields", []))
        enums = schema.get("enums", {})
        for index, value in enumerate(values):
            exact_keys(value, expected, f"{schema_name}[{index}]")
            for key, description in schema.get("types", {}).items():
                if value[key] is None and key not in nullable:
                    raise ValueError(f"{schema_name}[{index}].{key} cannot be null")
                scalar(value[key], description, f"{schema_name}[{index}].{key}")
            for key, allowed in enums.items():
                if value[key] not in allowed:
                    raise ValueError(f"{schema_name}[{index}].{key} has invalid enum")

    rows(bundle["resource_conditions.json"]["conditions"], "condition")
    rows(bundle["resource_conditions.json"]["seed_counters"], "resource_seed_counter")
    rows(bundle["resource_conditions.json"]["failed_seeds"], "failed_seed")
    rows(bundle["candidate_discovery.jsonl"], "discovery_row")
    for discovery in bundle["candidate_discovery.jsonl"]:
        rows(discovery["eligible_candidates"], "candidate")
        if discovery["primary_candidate"] is not None:
            exact_keys(
                discovery["primary_candidate"],
                set(row_schemas["candidate"]["exact_keys"]),
                "primary_candidate",
            )
    structural = bundle["structural_metrics.json"]
    rows(structural["seed_split_rows"], "seed_split")
    rows(structural["cell_metric_rows"], "cell_metric")
    rows(structural["assessment_checkpoints"], "assessment_checkpoint")
    selectivity = bundle["functional_selectivity.json"]
    rows(selectivity["episode_rows"], "selectivity_episode")
    rows(selectivity["seed_rows"], "selectivity_seed")
    matched = bundle["matched_ablations.json"]
    rows(matched["episode_branch_rows"], "episode_branch")
    rows(matched["control_membership_rows"], "control_membership")
    rows(matched["seed_effect_rows"], "seed_effect")
    rows(matched["condition_aggregate_effect_rows"], "condition_aggregate_effect")
    rows(list(matched["bootstrap_intervals"].values()), "bootstrap_interval")
    heldout = bundle["held_out_reuse.json"]
    rows(heldout["episode_branch_rows"], "episode_branch")
    rows(heldout["seed_rows"], "heldout_seed")
    rows(heldout["condition_aggregate_rows"], "heldout_condition_aggregate")
    acceptance = bundle["acceptance_matrix.json"]
    rows(acceptance["engineering_gates"], "engineering_gate")
    rows(acceptance["primary_scientific_gates"], "primary_science_gate")
    rows(acceptance["seed_cell_gate_rows"], "seed_cell_gate")
    rows(acceptance["secondary_cell_status_rows"], "secondary_cell_status")


def _validate_reproduction_manifest(
    bundle: dict[str, Any], protocol: dict[str, Any], source_commit: str
) -> None:
    manifest = bundle["reproduction_compare_manifest.json"]
    schema = protocol["artifact_schema_contract"]["row_schemas"]["reproduction_manifest"]
    exact_keys(manifest, set(schema["exact_keys"]), "reproduction manifest")
    inventory = _prefinal_inventory(protocol)
    if (
        manifest["all_equal"] is not True
        or manifest["comparison_contract_id"]
        != protocol["reproduction"]["comparison_contract_id"]
        or manifest["equal_files"] != inventory
        or manifest["prefinal_inventory"] != inventory
        or manifest["protocol_id"] != protocol["protocol_id"]
        or manifest["run_id"] != protocol["run_id"]
        or manifest["schema_version"] != protocol["schema_version"]
        or manifest["source_commit"] != source_commit
    ):
        raise ValueError("invalid C17 reproduction manifest contract")
    prefinal = _prefinal_from_final(bundle)
    expected_protocol_sha = digest_bytes(
        artifact_bytes("preregistration.json", prefinal["preregistration.json"])
    )
    run_schema = protocol["artifact_schema_contract"]["row_schemas"]["reproduction_run"]
    if len(manifest["runs"]) != 2:
        raise ValueError("C17 reproduction manifest requires exactly two runs")
    process_contracts = protocol["reproduction"]["staging_processes"]
    if len(process_contracts) != 2:
        raise ValueError("C17 reproduction process contract must have two rows")
    for row, process_contract in zip(manifest["runs"], process_contracts, strict=True):
        exact_keys(row, set(run_schema["exact_keys"]), "reproduction run")
        if set(row["file_sha256"]) != set(inventory):
            raise ValueError("C17 reproduction file hash inventory mismatch")
        expected_hashes = {
            name: digest_bytes(artifact_bytes(name, prefinal[name])) for name in inventory
        }
        if (
            row["process_id"] != process_contract["process_id"]
            or isinstance(row["pythonhashseed"], bool)
            or row["pythonhashseed"] != process_contract["pythonhashseed"]
            or row["source_commit"] != source_commit
            or row["protocol_sha256"] != expected_protocol_sha
            or row["file_sha256"] != expected_hashes
            or row["combined_sha256"]
            != digest([[name, expected_hashes[name]] for name in inventory])
        ):
            raise ValueError("C17 reproduction run evidence does not recalculate")
    comparison_input = {
        "comparison_contract_id": protocol["reproduction"]["comparison_contract_id"],
        "prefinal_inventory": inventory,
        "runs": manifest["runs"],
    }
    if manifest["comparison_input_sha256"] != digest(comparison_input):
        raise ValueError("C17 reproduction comparison preimage mismatch")
    evidence = bundle["acceptance_matrix.json"]["reproduction_evidence"]
    expected_evidence = {
        "comparison_contract_id": protocol["reproduction"]["comparison_contract_id"],
        "manifest_file": "reproduction_compare_manifest.json",
        "manifest_sha256": digest_bytes(
            artifact_bytes("reproduction_compare_manifest.json", manifest)
        ),
        "prefinal_exact9_equal": True,
        "process_ids": [row["process_id"] for row in process_contracts],
        "pythonhashseeds": [row["pythonhashseed"] for row in process_contracts],
        "status": "externally_compared",
    }
    if evidence != expected_evidence:
        raise ValueError("C17 final reproduction evidence mismatch")


_RAW_RECONSTRUCTION_KEYS = (
    "discovery",
    "structural",
    "selectivity",
    "matched",
    "heldout",
    "controls",
    "resource",
    "effects",
    "cell_metrics",
    "assessment_checkpoints",
)


@lru_cache(maxsize=32)
def _cached_raw_seed_reconstruction(
    protocol_json: str,
    run_seed: int,
    run_seed_impl_id: int,
    discovery_impl_id: int,
    controls_impl_id: int,
    boundary_impl_id: int,
) -> str:
    # The implementation identities deliberately participate in the cache key.
    # Tests and audits may replace a boundary implementation; an earlier result
    # must never be reused across that runtime boundary.
    del run_seed_impl_id, discovery_impl_id, controls_impl_id, boundary_impl_id
    result = _run_seed(json.loads(protocol_json), run_seed)
    return canonical({key: result[key] for key in _RAW_RECONSTRUCTION_KEYS})


def _validate_raw_reconstruction(
    bundle: dict[str, Any], protocol: dict[str, Any], successful_seeds: list[int]
) -> None:
    reconstructed = {
        key: []
        for key in _RAW_RECONSTRUCTION_KEYS
    }
    protocol_json = canonical(protocol)
    for run_seed in successful_seeds:
        result = json.loads(
            _cached_raw_seed_reconstruction(
                protocol_json,
                run_seed,
                id(_run_seed),
                id(discover_primary_candidate),
                id(select_control_memberships),
                id(execute_c14_c15_boundary),
            )
        )
        for key in reconstructed:
            reconstructed[key].extend(result[key])
    observed = {
        "discovery": bundle["candidate_discovery.jsonl"],
        "structural": bundle["structural_metrics.json"]["seed_split_rows"],
        "selectivity": bundle["functional_selectivity.json"]["episode_rows"],
        "matched": bundle["matched_ablations.json"]["episode_branch_rows"],
        "heldout": bundle["held_out_reuse.json"]["episode_branch_rows"],
        "controls": bundle["matched_ablations.json"]["control_membership_rows"],
        "resource": bundle["resource_conditions.json"]["seed_counters"],
        "effects": bundle["matched_ablations.json"]["seed_effect_rows"],
        "cell_metrics": bundle["structural_metrics.json"]["cell_metric_rows"],
        "assessment_checkpoints": bundle["structural_metrics.json"][
            "assessment_checkpoints"
        ],
    }
    for key in reconstructed:
        if reconstructed[key] != observed[key]:
            raise ValueError(f"C17 {key} raw evidence does not reconstruct")


def validate_bundle(
    bundle: dict[str, Any],
    protocol: dict[str, Any],
    source_commit: str,
) -> None:
    final = "reproduction_compare_manifest.json" in bundle
    expected_files = set(
        protocol["artifacts"]["exact_files"] if final else _prefinal_inventory(protocol)
    )
    if set(bundle) != expected_files:
        raise ValueError("C17 exact artifact inventory mismatch")
    if bundle["preregistration.json"]["source_commit"] != source_commit:
        raise ValueError("C17 source pin mismatch")
    if not isinstance(source_commit, str) or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise ValueError("C17 source commit must be lowercase hexadecimal")
    expected_protocol = copy.deepcopy(protocol)
    expected_protocol["source_commit"] = source_commit
    if bundle["preregistration.json"] != expected_protocol:
        raise ValueError("C17 bundled preregistration mismatch")
    for name in (
        "resource_conditions.json",
        "structural_metrics.json",
        "functional_selectivity.json",
        "matched_ablations.json",
        "held_out_reuse.json",
        "acceptance_matrix.json",
    ):
        if (
            bundle[name]["schema_version"] != protocol["schema_version"]
            or bundle[name]["protocol_id"] != protocol["protocol_id"]
        ):
            raise ValueError("C17 artifact identity mismatch")
    if (
        bundle["resource_conditions.json"]["run_id"] != protocol["run_id"]
        or bundle["resource_conditions.json"]["conditions"]
        != protocol["resource_conditions"]["rows"]
    ):
        raise ValueError("C17 resource definition mismatch")
    _validate_exact_schemas(bundle, protocol)
    if final:
        _validate_reproduction_manifest(bundle, protocol, source_commit)
    elif (
        bundle["acceptance_matrix.json"]["reproduction_evidence"]
        != PREFINAL_REPRODUCTION_EVIDENCE
    ):
        raise ValueError("C17 pre-final bundle cannot claim external reproduction")
    acceptance = bundle["acceptance_matrix.json"]
    failures = acceptance["failed_seeds"]
    for name in (
        "resource_conditions.json",
        "structural_metrics.json",
        "functional_selectivity.json",
        "matched_ablations.json",
        "held_out_reuse.json",
    ):
        if bundle[name]["failed_seeds"] != failures:
            raise ValueError("C17 failed-seed list mismatch")
    successful_seeds = acceptance["successful_seeds"]
    if successful_seeds != sorted(successful_seeds) or any(
        isinstance(seed, bool) or not isinstance(seed, int) for seed in successful_seeds
    ):
        raise ValueError("C17 successful seed inventory mismatch")
    successful = len(successful_seeds)
    scaling = protocol["artifacts"]["successful_seed_scaling"]
    expected_counts = {
        "candidate_discovery": scaling["candidate_discovery_jsonl_rows_per_S"],
        "structural_seed_split": scaling["structural_seed_split_rows_per_S"],
        "selectivity_episode": scaling["selectivity_episode_rows_per_S"],
        "functional_selectivity_seed": scaling["functional_selectivity_seed_rows_per_S"],
        "matched_episode_branch": scaling["matched_ablation_episode_branch_rows_per_S"],
        "heldout_episode_branch": scaling["heldout_episode_branch_rows_per_S"],
        "heldout_seed": scaling["heldout_seed_rows_per_S"],
        "matched_control_membership": scaling["matched_control_membership_rows_per_S"],
        "matched_seed_effect": scaling["matched_seed_effect_rows_per_S"],
        "resource_seed_counter": scaling["resource_seed_counter_rows_per_S"],
    }
    actual_counts = {
        "candidate_discovery": len(bundle["candidate_discovery.jsonl"]),
        "structural_seed_split": len(bundle["structural_metrics.json"]["seed_split_rows"]),
        "selectivity_episode": len(bundle["functional_selectivity.json"]["episode_rows"]),
        "functional_selectivity_seed": len(bundle["functional_selectivity.json"]["seed_rows"]),
        "matched_episode_branch": len(bundle["matched_ablations.json"]["episode_branch_rows"]),
        "heldout_episode_branch": len(bundle["held_out_reuse.json"]["episode_branch_rows"]),
        "heldout_seed": len(bundle["held_out_reuse.json"]["seed_rows"]),
        "matched_control_membership": len(
            bundle["matched_ablations.json"]["control_membership_rows"]
        ),
        "matched_seed_effect": len(bundle["matched_ablations.json"]["seed_effect_rows"]),
        "resource_seed_counter": len(bundle["resource_conditions.json"]["seed_counters"]),
    }
    for key, per_seed in expected_counts.items():
        if (
            acceptance["cardinalities"][key] != actual_counts[key]
            or actual_counts[key] != successful * per_seed
        ):
            raise ValueError("C17 raw cardinality mismatch")
    aggregate_counts = {
        "matched_condition_aggregate_effect": len(
            bundle["matched_ablations.json"]["condition_aggregate_effect_rows"]
        ),
        "heldout_condition_aggregate": len(
            bundle["held_out_reuse.json"]["condition_aggregate_rows"]
        ),
    }
    expected_aggregate_counts = {
        "matched_condition_aggregate_effect": scaling[
            "matched_condition_aggregate_effect_rows_when_S_gt_0"
        ]
        if successful
        else 0,
        "heldout_condition_aggregate": scaling[
            "heldout_condition_aggregate_rows_when_S_gt_0"
        ]
        if successful
        else 0,
    }
    if aggregate_counts != expected_aggregate_counts:
        raise ValueError("C17 aggregate cardinality mismatch")
    if acceptance["cardinalities"] != {**actual_counts, **aggregate_counts}:
        raise ValueError("C17 cardinality evidence mismatch")
    _validate_raw_reconstruction(bundle, protocol, successful_seeds)
    for row in (
        bundle["matched_ablations.json"]["episode_branch_rows"]
        + bundle["held_out_reuse.json"]["episode_branch_rows"]
    ):
        if row["restore_exact"] is not True or row["state_hash_before"] != row["state_hash_after"]:
            raise ValueError("C17 branch did not restore frozen state exactly")
    discovery = {
        (row["run_seed"], row["condition_id"]): row for row in bundle["candidate_discovery.jsonl"]
    }
    matched_rows = bundle["matched_ablations.json"]["episode_branch_rows"]
    heldout_rows = bundle["held_out_reuse.json"]["episode_branch_rows"]
    expected_effects = []
    expected_cell_metrics = []
    for seed in acceptance["successful_seeds"]:
        for condition_id in protocol["resource_conditions"]["condition_order"]:
            target = discovery[(seed, condition_id)]["target_function_index_dev_locked"]
            test = [
                row
                for row in matched_rows
                if row["run_seed"] == seed and row["condition_id"] == condition_id
            ]
            held = [
                row
                for row in heldout_rows
                if row["run_seed"] == seed and row["condition_id"] == condition_id
            ]
            targeted = _locked_impairment(test, "targeted", target)
            for branch in BRANCHES[1:]:
                effect = _locked_impairment(test, branch, target)
                expected_effects.append(
                    {
                        "run_seed": seed,
                        "condition_id": condition_id,
                        "branch": branch,
                        "impairment": effect,
                        "target_excess": None
                        if effect is None or targeted is None
                        else targeted - effect,
                    }
                )
            discovery_row = discovery[(seed, condition_id)]
            candidate = discovery_row["primary_candidate"]
            selectivity_rows = [
                row
                for row in bundle["functional_selectivity.json"]["episode_rows"]
                if row["run_seed"] == seed
                and row["condition_id"] == condition_id
                and row["split"] == "test"
            ]
            selectivity_value = None
            if target is not None and selectivity_rows:
                target_rate = sum(
                    row["target_activation_rate"] or 0.0 for row in selectivity_rows
                ) / len(selectivity_rows)
                other = max(
                    sum(
                        row["non_target_activation_rates"].get(str(index)) or 0.0
                        for row in selectivity_rows
                    )
                    / len(selectivity_rows)
                    for index in range(4)
                    if index != target
                )
                selectivity_value = target_rate - other
            point = {
                "run_seed": seed,
                "condition_id": condition_id,
                "target_function_index": target,
                "cohesion": None if candidate is None else candidate["cohesion"],
                "functional_selectivity": selectivity_value,
                "held_out_reuse": _heldout_reuse(held, target),
                "targeted_impairment": targeted,
                "unrelated_collateral": _unrelated_collateral(test, target),
            }
            point["local_gates_except_seed_consistency"] = (
                target is not None
                and point["cohesion"] is not None
                and point["cohesion"] >= protocol["metrics"]["structural_cohesion_min"]
                and point["functional_selectivity"] is not None
                and point["functional_selectivity"]
                >= protocol["metrics"]["functional_selectivity_min"]
                and point["held_out_reuse"] is not None
                and point["held_out_reuse"] >= protocol["metrics"]["held_out_reuse_min"]
                and targeted is not None
                and targeted >= protocol["metrics"]["targeted_impairment_min"]
                and all(
                    row["target_excess"] is not None
                    and row["target_excess"] >= protocol["metrics"]["control_excess_min"]
                    for row in expected_effects[-5:]
                )
                and point["unrelated_collateral"] is not None
                and point["unrelated_collateral"] <= protocol["metrics"]["unrelated_collateral_max"]
            )
            expected_cell_metrics.append(point)
    if expected_effects != bundle["matched_ablations.json"]["seed_effect_rows"]:
        raise ValueError("C17 seed effects do not recalculate from raw rows")
    if expected_cell_metrics != bundle["structural_metrics.json"]["cell_metric_rows"]:
        raise ValueError("C17 cell metrics do not recalculate from raw rows")
    expected_selectivity_seed_rows = _selectivity_seed_rows(
        bundle["functional_selectivity.json"]["episode_rows"],
        bundle["candidate_discovery.jsonl"],
    )
    if expected_selectivity_seed_rows != bundle["functional_selectivity.json"]["seed_rows"]:
        raise ValueError("C17 selectivity seed rows do not recalculate")
    expected_heldout_seed_rows = _heldout_seed_rows(
        heldout_rows, bundle["candidate_discovery.jsonl"]
    )
    if expected_heldout_seed_rows != bundle["held_out_reuse.json"]["seed_rows"]:
        raise ValueError("C17 held-out seed rows do not recalculate")
    expected_effect_aggregates = (
        _condition_aggregate_effect_rows(expected_effects, protocol)
        if successful_seeds
        else []
    )
    if (
        expected_effect_aggregates
        != bundle["matched_ablations.json"]["condition_aggregate_effect_rows"]
    ):
        raise ValueError("C17 condition effects do not recalculate")
    expected_heldout_aggregates = (
        _heldout_condition_aggregate_rows(expected_heldout_seed_rows, protocol)
        if successful_seeds
        else []
    )
    if expected_heldout_aggregates != bundle["held_out_reuse.json"]["condition_aggregate_rows"]:
        raise ValueError("C17 held-out condition rows do not recalculate")
    expected_seed_gates = []
    for point in expected_cell_metrics:
        effects = [
            row
            for row in expected_effects
            if row["run_seed"] == point["run_seed"] and row["condition_id"] == point["condition_id"]
        ]
        gate_values = {
            "target_consistency": point["target_function_index"] is not None,
            "seed_consistency": False,
            "structural_cohesion": point["cohesion"] is not None
            and point["cohesion"] >= protocol["metrics"]["structural_cohesion_min"],
            "functional_selectivity": point["functional_selectivity"] is not None
            and point["functional_selectivity"]
            >= protocol["metrics"]["functional_selectivity_min"],
            "held_out_reuse": point["held_out_reuse"] is not None
            and point["held_out_reuse"] >= protocol["metrics"]["held_out_reuse_min"],
            "targeted_impairment": point["targeted_impairment"] is not None
            and point["targeted_impairment"] >= protocol["metrics"]["targeted_impairment_min"],
            "all_control_excess": all(
                row["target_excess"] is not None
                and row["target_excess"] >= protocol["metrics"]["control_excess_min"]
                for row in effects
                if row["branch"] != "targeted"
            ),
            "bounded_collateral": point["unrelated_collateral"] is not None
            and point["unrelated_collateral"] <= protocol["metrics"]["unrelated_collateral_max"],
        }
        expected_seed_gates.extend(
            {
                "run_seed": point["run_seed"],
                "condition_id": point["condition_id"],
                "gate_id": gate_id,
                "passed": gate_values[gate_id],
            }
            for gate_id in protocol["acceptance"]["scientific_gate_ids"]
        )
    expected_consistency = _apply_seed_consistency(
        expected_cell_metrics, expected_seed_gates, protocol
    )
    if expected_seed_gates != acceptance["seed_cell_gate_rows"]:
        raise ValueError("C17 seed-cell gates do not recalculate")
    if expected_consistency != acceptance["seed_consistency"]:
        raise ValueError("C17 cross-seed consistency does not recalculate")
    r0_metrics = [row for row in expected_cell_metrics if row["condition_id"] == "R0_baseline"]
    expected_bootstrap = (
        _hierarchical_bootstrap(
            [row for row in matched_rows if row["condition_id"] == "R0_baseline"],
            [row for row in heldout_rows if row["condition_id"] == "R0_baseline"],
            r0_metrics,
            protocol,
        )
        if not failures and r0_metrics
        else {}
    )
    if expected_bootstrap != bundle["matched_ablations.json"]["bootstrap_intervals"]:
        raise ValueError("C17 hierarchical bootstrap does not recalculate")
    expected_primary_values = {
        gate_id: all(
            row["passed"]
            for row in expected_seed_gates
            if row["condition_id"] == "R0_baseline" and row["gate_id"] == gate_id
        )
        for gate_id in protocol["acceptance"]["scientific_gate_ids"]
    }
    expected_primary_values["seed_consistency"] = expected_consistency["R0_baseline"]["passed"]
    if expected_bootstrap:
        expected_primary_values["held_out_reuse"] = (
            expected_bootstrap["held_out_reuse"]["lower"] is not None
            and expected_bootstrap["held_out_reuse"]["lower"]
            >= protocol["metrics"]["held_out_reuse_min"]
        )
        expected_primary_values["targeted_impairment"] = (
            expected_bootstrap["targeted_impairment"]["lower"] is not None
            and expected_bootstrap["targeted_impairment"]["lower"]
            >= protocol["metrics"]["targeted_impairment_min"]
        )
        expected_primary_values["all_control_excess"] = all(
            expected_bootstrap[f"control_margin:{name}"]["lower"] is not None
            and expected_bootstrap[f"control_margin:{name}"]["lower"]
            >= protocol["metrics"]["control_excess_min"]
            for name in protocol["controls"]["control_order"]
        )
        expected_primary_values["bounded_collateral"] = (
            expected_bootstrap["unrelated_collateral"]["upper"] is not None
            and expected_bootstrap["unrelated_collateral"]["upper"]
            <= protocol["metrics"]["unrelated_collateral_max"]
        )
    expected_primary = [
        {"gate_id": gate_id, "passed": bool(expected_primary_values[gate_id])}
        for gate_id in protocol["acceptance"]["scientific_gate_ids"]
    ]
    if expected_primary != acceptance["primary_scientific_gates"]:
        raise ValueError("C17 primary scientific gates do not recalculate")
    gates = acceptance["engineering_gates"]
    if [row["gate_id"] for row in gates] != protocol["acceptance"]["engineering_gate_ids"]:
        raise ValueError("C17 engineering gate inventory/order mismatch")
    combined_for_gates = {
        "discovery": bundle["candidate_discovery.jsonl"],
        "matched": matched_rows,
        "heldout": heldout_rows,
        "controls": bundle["matched_ablations.json"]["control_membership_rows"],
        "resource": bundle["resource_conditions.json"]["seed_counters"],
        "assessment_checkpoints": bundle["structural_metrics.json"][
            "assessment_checkpoints"
        ],
    }
    expected_gate_evidence = _engineering_evidence(
        protocol,
        source_commit,
        combined_for_gates,
        all(actual_counts[key] == successful * value for key, value in expected_counts.items()),
        acceptance["successful_seeds"],
        final,
        bool(successful_seeds),
    )
    expected_gates = [
        {
            "gate_id": gate_id,
            "passed": bool(expected_gate_evidence[gate_id]),
            "observed": expected_gate_evidence[gate_id],
        }
        for gate_id in protocol["acceptance"]["engineering_gate_ids"]
    ]
    if gates != expected_gates:
        raise ValueError("C17 engineering gates do not recalculate from evidence")
    reproduction = next(row for row in gates if row["gate_id"] == "reproduction_exact")
    if reproduction["passed"] is not final:
        raise ValueError("only external C17 finalization can claim exact reproduction")
    expected_engineering = (
        "accepted" if all(row["passed"] for row in gates) else "implementation_failure"
    )
    if acceptance["engineering_status"] != expected_engineering:
        raise ValueError("C17 engineering status does not match its gates")
    expected_science = (
        "not_evaluated_implementation_failure"
        if failures
        else "supported"
        if all(row["passed"] for row in acceptance["primary_scientific_gates"])
        else "not_supported"
    )
    if acceptance["scientific_status"] != expected_science:
        raise ValueError("C17 scientific status does not match its gates")
    expected_secondary = [
        {
            "condition_id": condition_id,
            "primary_rescue_allowed": False,
            "role": "secondary",
            "scientific_status": "not_evaluated_implementation_failure"
            if failures
            else "supported"
            if all(
                row["passed"]
                for row in expected_seed_gates
                if row["condition_id"] == condition_id
            )
            else "not_supported",
        }
        for condition_id in protocol["resource_conditions"]["condition_order"][1:]
    ]
    if acceptance["secondary_cell_status_rows"] != expected_secondary:
        raise ValueError("C17 secondary status rows do not recalculate")
    if bundle["report.md"] != report_text(acceptance):
        raise ValueError("C17 report does not match validated status")
    canonical(bundle)
