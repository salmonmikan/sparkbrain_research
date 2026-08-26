"""C17 experiment assembly and raw-to-derived validation.

Discovery is label blind. Evaluator-only fields are joined only after each bank,
candidate, development mapping, and train-only control membership are frozen.
"""

from __future__ import annotations

import copy
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from .contracts import canonical, digest, validate_resource_conditions
from .discovery import discover_primary_candidate, select_controls
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
) -> dict[str, Any]:
    members = [] if candidate is None else candidate["member_ids"]
    ablated = members if branch == "targeted" else (controls.get(branch) or [])
    eligible = correct = active = related = disrupted = 0
    collateral_wrong = 0
    before = digest({"bank": bank.state(), "episode_id": episode["episode_id"]})
    for frame in episode["frames"]:
        if not frame["scoring"]:
            continue
        eligible += 1
        function_index = frame["evaluator_function_index"]
        activations = _query_activations(bank, frame)
        candidate_active = (
            bool(members)
            and sum(activations.get(item, 0.0) for item in members) / len(members) >= 0.5
        )
        if candidate_active:
            active += 1
        is_related = target_function is not None and function_index == target_function
        if is_related:
            related += 1
        ablation_active = bool(ablated) and any(
            activations.get(item, 0.0) >= 0.5 for item in ablated
        )
        wrong = ablation_active and candidate_active and is_related
        if wrong:
            disrupted += 1
        if ablation_active and not is_related and branch == "targeted":
            collateral_wrong += 1
        correct += int(not wrong)
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
        "collateral_wrong": collateral_wrong,
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
                        )
                    )
        cell_rows = [
            row
            for row in matched
            if row["run_seed"] == run_seed and row["condition_id"] == condition["condition_id"]
        ]
        target_effect = _impairment(cell_rows, "targeted")
        for branch in BRANCHES[1:]:
            effect = _impairment(cell_rows, branch)
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
        held_reuse = _ratio(
            sum(row["disrupted"] for row in held_rows if row["branch"] == "targeted"),
            sum(row["eligible"] for row in held_rows if row["branch"] == "targeted"),
        )
        collateral = _ratio(
            sum(row["collateral_wrong"] for row in cell_rows if row["branch"] == "targeted"),
            sum(row["eligible"] for row in cell_rows if row["branch"] == "targeted"),
        )
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
    expected = protocol["artifacts"]["successful_seed_scaling"]
    engineering = [
        {"gate_id": gate_id, "passed": not failures, "observed": None}
        for gate_id in protocol["acceptance"]["engineering_gate_ids"]
    ]
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
    for row in engineering:
        if row["gate_id"] in {"raw_cardinality", "exact_inventory", "all_required_seeds"}:
            row["passed"] = (
                not failures
                and cardinality_pass
                and successful == protocol["fixtures"]["run_seeds"]
            )
            row["observed"] = cardinalities
    primary_gates = []
    for gate_id in protocol["acceptance"]["scientific_gate_ids"]:
        values = [
            row["passed"]
            for row in combined["seed_gates"]
            if row["condition_id"] == "R0_baseline" and row["gate_id"] == gate_id
        ]
        if gate_id == "seed_consistency":
            passed = sum(values) >= protocol["metrics"]["seed_consistency_min"]
        else:
            passed = bool(values) and all(values)
        primary_gates.append({"gate_id": gate_id, "passed": passed})
    scientific_status = (
        "not_evaluated_implementation_failure"
        if failures
        else ("supported" if all(row["passed"] for row in primary_gates) else "not_supported")
    )
    intervals = []
    for branch in BRANCHES[1:]:
        values = [
            row["impairment"]
            for row in combined["effects"]
            if row["condition_id"] == "R0_baseline"
            and row["branch"] == branch
            and row["impairment"] is not None
        ]
        intervals.append(
            {
                "branch": branch,
                "interval": _bootstrap(values, protocol)
                if not failures
                else _bootstrap([], protocol),
            }
        )
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
        "bootstrap_intervals": intervals,
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
    if canonical(bundle).find("NaN") >= 0:
        raise ValueError("C17 bundle contains nonfinite values")
