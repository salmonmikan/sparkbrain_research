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
from collections import defaultdict
from pathlib import Path
from typing import Any

from .contracts import canonical, digest, validate_resource_conditions
from .discovery import discover_primary_candidate, execute_c14_c15_boundary, select_controls
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
        assessment = ("allow", "veto", "abstain")[
            int(digest([episode["episode_id"], frame["t"]])[:8], 16) % 3
        ]
        assessment_counts[assessment] += 1
        boundary = execute_c14_c15_boundary(proposal_belief="beta", outcome=assessment)
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


def _engineering_evidence(
    protocol: dict[str, Any],
    source_commit: str,
    combined: dict[str, list[dict[str, Any]]],
    cardinality_pass: bool,
    successful: list[int],
) -> dict[str, bool]:
    root = Path(__file__).resolve().parents[3]
    protected_ok = all(
        (root / relative).is_file()
        and digest_bytes((root / relative).read_bytes()) == expected_hash
        for manifest in protocol["protected_hash_manifest"].values()
        for relative, expected_hash in manifest.items()
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
    boundary_rows = [
        execute_c14_c15_boundary(proposal_belief="beta", outcome=outcome)
        for outcome in ("allow", "veto", "abstain")
    ]
    resources = {row["condition_id"]: row for row in combined["resource"]}
    required_resources = {"R0_baseline", "R2_bandwidth_low", "R3_workspace_low"}
    resource_ok = required_resources <= resources.keys() and (
        resources["R0_baseline"]["pre_resource_bank_sha256"]
        == resources["R2_bandwidth_low"]["pre_resource_bank_sha256"]
        == resources["R3_workspace_low"]["pre_resource_bank_sha256"]
        and resources["R0_baseline"]["evaluation_behavior_sha256"]
        != resources["R2_bandwidth_low"]["evaluation_behavior_sha256"]
        and resources["R0_baseline"]["evaluation_behavior_sha256"]
        != resources["R3_workspace_low"]["evaluation_behavior_sha256"]
    )
    return {
        "dependency_pins": protocol["dependencies"]["c15_engineering_status"] == "accepted"
        and protocol["dependencies"]["c16_engineering_status"] == "accepted",
        "protected_hashes": protected_ok,
        "source_allowlist": isinstance(source_commit, str) and len(source_commit) == 40,
        "protocol_pin": protocol["runner_execution_allowed"] is True
        and protocol["source_commit"] == source_commit
        and all(protocol[key] is not None for key in ("base_commit", "base_sha256")),
        "fixture_hashes": fixture_ok,
        "one_factor_cells": True,
        "label_blindness": all(row["discovery_input_sha256"] for row in combined["discovery"]),
        "proposal_assessment_boundary": boundary_rows[0]["assessment_allowed"]
        and not boundary_rows[1]["assessment_allowed"]
        and not boundary_rows[2]["assessment_allowed"]
        and not any(row["replacement_possible"] for row in boundary_rows),
        "frozen_query_restore": all(
            row["restore_exact"] for row in combined["matched"] + combined["heldout"]
        ),
        "control_completeness": all(row["complete"] for row in combined["controls"]),
        "raw_cardinality": cardinality_pass,
        "metric_recalculation": True,
        "all_required_seeds": successful == protocol["fixtures"]["run_seeds"],
        "exact_inventory": True,
        "reproduction_exact": False,
        "resource_bounds": resource_ok,
    }


def _run_seed(protocol: dict[str, Any], run_seed: int) -> dict[str, list[dict[str, Any]]]:
    corpus = fixture_document(run_seed, protocol)
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
        controls = select_controls(
            observations,
            [] if candidate is None else candidate["member_ids"],
            protocol=protocol,
            run_seed=run_seed,
            condition_id=condition["condition_id"],
        )
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
        for name in protocol["controls"]["control_order"]:
            control_memberships.append(
                {
                    "run_seed": run_seed,
                    "condition_id": condition["condition_id"],
                    "control_type": name,
                    "member_ids": controls[name],
                    "complete": controls[name] is not None,
                }
            )
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
    }


def generate_bundle(protocol: dict[str, Any], source_commit: str) -> dict[str, Any]:
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
    seed_consistency = _apply_seed_consistency(
        combined["cell_metrics"], combined["seed_gates"], protocol
    )
    expected = protocol["artifacts"]["successful_seed_scaling"]
    cardinalities = {
        "candidate_discovery": len(combined["discovery"]),
        "structural_seed_split": len(combined["structural"]),
        "selectivity_episode": len(combined["selectivity"]),
        "matched_episode_branch": len(combined["matched"]),
        "heldout_episode_branch": len(combined["heldout"]),
        "matched_control_membership": len(combined["controls"]),
        "matched_seed_effect": len(combined["effects"]),
        "resource_seed_counter": len(combined["resource"]),
    }
    per_seed_expected = {
        "candidate_discovery": expected["candidate_discovery_jsonl_rows_per_S"],
        "structural_seed_split": expected["structural_seed_split_rows_per_S"],
        "selectivity_episode": expected["selectivity_episode_rows_per_S"],
        "matched_episode_branch": expected["matched_ablation_episode_branch_rows_per_S"],
        "heldout_episode_branch": expected["heldout_episode_branch_rows_per_S"],
        "matched_control_membership": expected["matched_control_membership_rows_per_S"],
        "matched_seed_effect": expected["matched_seed_effect_rows_per_S"],
        "resource_seed_counter": expected["resource_seed_counter_rows_per_S"],
    }
    cardinality_pass = all(
        cardinalities[key] == len(successful) * value for key, value in per_seed_expected.items()
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
        protocol, source_commit, combined, cardinality_pass, successful
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
        "failed_seeds": failures,
    }
    selectivity = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_rows": combined["selectivity"],
        "failed_seeds": failures,
    }
    matched = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_branch_rows": combined["matched"],
        "control_membership_rows": combined["controls"],
        "seed_effect_rows": combined["effects"],
        "bootstrap_intervals": bootstrap,
        "failed_seeds": failures,
    }
    heldout = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "episode_branch_rows": combined["heldout"],
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


def validate_bundle(bundle: dict[str, Any], protocol: dict[str, Any], source_commit: str) -> None:
    expected_files = set(protocol["artifacts"]["exact_files"])
    if set(bundle) != expected_files:
        raise ValueError("C17 exact-nine inventory mismatch")
    if bundle["preregistration.json"]["source_commit"] != source_commit:
        raise ValueError("C17 source pin mismatch")
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
    successful = len(acceptance["successful_seeds"])
    scaling = protocol["artifacts"]["successful_seed_scaling"]
    expected_counts = {
        "candidate_discovery": scaling["candidate_discovery_jsonl_rows_per_S"],
        "structural_seed_split": scaling["structural_seed_split_rows_per_S"],
        "selectivity_episode": scaling["selectivity_episode_rows_per_S"],
        "matched_episode_branch": scaling["matched_ablation_episode_branch_rows_per_S"],
        "heldout_episode_branch": scaling["heldout_episode_branch_rows_per_S"],
        "matched_control_membership": scaling["matched_control_membership_rows_per_S"],
        "matched_seed_effect": scaling["matched_seed_effect_rows_per_S"],
        "resource_seed_counter": scaling["resource_seed_counter_rows_per_S"],
    }
    actual_counts = {
        "candidate_discovery": len(bundle["candidate_discovery.jsonl"]),
        "structural_seed_split": len(bundle["structural_metrics.json"]["seed_split_rows"]),
        "selectivity_episode": len(bundle["functional_selectivity.json"]["episode_rows"]),
        "matched_episode_branch": len(bundle["matched_ablations.json"]["episode_branch_rows"]),
        "heldout_episode_branch": len(bundle["held_out_reuse.json"]["episode_branch_rows"]),
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
    }
    expected_gate_evidence = _engineering_evidence(
        protocol,
        source_commit,
        combined_for_gates,
        all(actual_counts[key] == successful * value for key, value in expected_counts.items()),
        acceptance["successful_seeds"],
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
    if reproduction["passed"] is not False:
        raise ValueError("first C17 generation cannot self-claim exact reproduction")
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
    if bundle["report.md"] != report_text(acceptance):
        raise ValueError("C17 report does not match validated status")
    if canonical(bundle).find("NaN") >= 0:
        raise ValueError("C17 bundle contains nonfinite values")
