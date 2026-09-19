from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology

CONTRACT_PATH = Path(
    "analysis/architecture/refractory_current_accounting_cycle1_contract_20260920.json"
)
TOLERANCE = 1e-12


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def verify_bindings(contract: dict[str, Any]) -> dict[str, bool]:
    main = contract["source_binding"]["main"]
    checks: dict[str, bool] = {}
    for path, expected in contract["source_binding"].items():
        if path == "main":
            continue
        actual = git("rev-parse", f"{main}:{path}")
        checks[path] = actual == expected
    return checks


def bound_text(contract: dict[str, Any], path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{contract['source_binding']['main']}:{path}"],
        text=True,
    )


def function_node(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise ValueError(f"missing function: {name}")


def named_assignment(node: ast.AST, target: str) -> ast.Assign | None:
    for item in ast.walk(node):
        if not isinstance(item, ast.Assign):
            continue
        if any(isinstance(row, ast.Name) and row.id == target for row in item.targets):
            return item
    return None


def machine_facts(contract: dict[str, Any]) -> dict[str, bool]:
    source = bound_text(contract, "src/sparkbrain/v04/field.py")
    tree = ast.parse(source)
    deliver = function_node(tree, "_deliver_group")
    schedule = function_node(tree, "schedule_arrival")
    run_until = function_node(tree, "run_until")

    positive_assign = named_assignment(deliver, "positive")
    negative_assign = named_assignment(deliver, "negative")
    net_assign = named_assignment(deliver, "net_current")
    net_is_subtraction = bool(
        net_assign is not None
        and isinstance(net_assign.value, ast.BinOp)
        and isinstance(net_assign.value.op, ast.Sub)
        and isinstance(net_assign.value.left, ast.Name)
        and net_assign.value.left.id == "positive"
        and isinstance(net_assign.value.right, ast.Name)
        and net_assign.value.right.id == "negative"
    )

    refractory_min_net = False
    for item in ast.walk(deliver):
        if not isinstance(item, ast.AugAssign) or not isinstance(item.op, ast.Add):
            continue
        target = item.target
        value = item.value
        if not (
            isinstance(target, ast.Attribute)
            and target.attr == "potential"
            and isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "min"
            and len(value.args) == 2
        ):
            continue
        names = {row.id for row in ast.walk(value) if isinstance(row, ast.Name)}
        if "net_current" in names:
            refractory_min_net = True

    schedule_current_sign_checks = any(
        isinstance(item, ast.Compare)
        and any(
            isinstance(row, ast.Attribute) and row.attr == "current"
            for row in ast.walk(item)
        )
        for item in ast.walk(schedule)
    )
    deliver_text = ast.unparse(deliver)
    run_until_text = ast.unparse(run_until)
    same_time_grouping = (
        "by_target.setdefault(row.target_id, []).append(row)" in deliver_text
        and "self._queue[0][0] == time_ms" in run_until_text
        and "group.append(arrival)" in run_until_text
    )
    positive_aggregation = positive_assign is not None and "row.current" in ast.unparse(
        positive_assign
    )
    negative_aggregation = negative_assign is not None and "row.current" in ast.unparse(
        negative_assign
    )
    source_comment = contract["supported_contract_scope"]["bound_source_comment"]

    return {
        "deliver_group_groups_same_time_arrivals_by_target": same_time_grouping,
        "positive_current_is_summed_separately": positive_aggregation,
        "negative_current_is_summed_separately": negative_aggregation,
        "net_current_is_positive_minus_negative": net_is_subtraction,
        "refractory_branch_applies_min_zero_net_current": refractory_min_net,
        "schedule_arrival_accepts_signed_current_without_sign_rejection": not schedule_current_sign_checks,
        "bound_positive_drive_ignored_comment_present": source_comment in source,
    }


def field_config(contract: dict[str, Any]) -> ExcitableFieldConfig:
    row = contract["input_family"]["field_config"]
    return ExcitableFieldConfig(
        membrane_tau_ms=float(row["membrane_tau_ms"]),
        adaptation_tau_ms=float(row["adaptation_tau_ms"]),
        refractory_ms=float(row["refractory_ms"]),
        reset_potential=float(row["reset_potential"]),
        adaptation_increment=float(row["adaptation_increment"]),
        receptor_fanout=1,
    )


def production_arm(
    contract: dict[str, Any],
    condition_name: str,
    arm_name: str,
) -> dict[str, Any]:
    family = contract["input_family"]
    unit_row = family["unit"]
    condition = family[condition_name]
    unit = UnitState(
        unit_id=int(unit_row["unit_id"]),
        x=float(unit_row["x"]),
        y=float(unit_row["y"]),
        potential=float(unit_row["initial_potential"]),
        base_threshold=float(unit_row["base_threshold"]),
        adaptation=float(unit_row["adaptation"]),
        refractory_until_ms=float(condition["refractory_until_ms"]),
        last_update_ms=float(unit_row["last_update_ms"]),
    )
    topology = explicit_topology((unit,), (), receptor_ids=())
    field = TemporalExcitableField(topology, field_config(contract))
    treatment_time = float(condition["treatment_time_ms"])
    currents = [float(value) for value in condition["arms"][arm_name]]
    for index, current in enumerate(currents):
        field.schedule_arrival(
            SynapticArrival(
                time_ms=treatment_time,
                target_id=unit.unit_id,
                current=current,
                source_id=None,
                pulse_id=f"{condition_name}-{arm_name}-treatment-{index}",
            )
        )
    treatment_spikes = field.run_until(treatment_time)
    potential_after_treatment = field.units[unit.unit_id].potential
    probe_time = float(condition["probe_time_ms"])
    field.schedule_arrival(
        SynapticArrival(
            time_ms=probe_time,
            target_id=unit.unit_id,
            current=float(condition["probe_current"]),
            source_id=None,
            pulse_id=f"{condition_name}-{arm_name}-probe",
        )
    )
    probe_spikes = field.run_until(probe_time)
    return {
        "potential_after_treatment": potential_after_treatment,
        "treatment_spike_count": len(treatment_spikes),
        "post_refractory_probe_spike_count": len(probe_spikes),
        "final_potential": field.units[unit.unit_id].potential,
    }


def shadow_arm(
    contract: dict[str, Any],
    condition_name: str,
    arm_name: str,
) -> dict[str, Any]:
    family = contract["input_family"]
    unit = family["unit"]
    condition = family[condition_name]
    config = family["field_config"]
    potential = float(unit["initial_potential"])
    base_threshold = float(unit["base_threshold"])
    adaptation = float(unit["adaptation"])
    last_update = float(unit["last_update_ms"])
    refractory_until = float(condition["refractory_until_ms"])
    membrane_tau = float(config["membrane_tau_ms"])
    adaptation_tau = float(config["adaptation_tau_ms"])
    refractory_ms = float(config["refractory_ms"])
    reset_potential = float(config["reset_potential"])
    adaptation_increment = float(config["adaptation_increment"])

    def decay(time_ms: float) -> None:
        nonlocal potential, adaptation, last_update
        elapsed = time_ms - last_update
        potential *= math.exp(-elapsed / membrane_tau)
        adaptation *= math.exp(-elapsed / adaptation_tau)
        last_update = time_ms

    treatment_time = float(condition["treatment_time_ms"])
    decay(treatment_time)
    currents = [float(value) for value in condition["arms"][arm_name]]
    positive = sum(max(0.0, value) for value in currents)
    negative = sum(max(0.0, -value) for value in currents)
    treatment_spikes = 0
    if treatment_time < refractory_until:
        potential -= negative
    else:
        potential += positive - negative
        threshold = base_threshold + max(0.0, adaptation)
        if potential + 1e-12 >= threshold:
            treatment_spikes = 1
            potential = reset_potential
            adaptation += adaptation_increment
            refractory_until = treatment_time + refractory_ms
    potential_after_treatment = potential

    probe_time = float(condition["probe_time_ms"])
    decay(probe_time)
    probe_current = float(condition["probe_current"])
    probe_spikes = 0
    if probe_time < refractory_until:
        potential += min(0.0, probe_current)
    else:
        potential += probe_current
        threshold = base_threshold + max(0.0, adaptation)
        if potential + 1e-12 >= threshold:
            probe_spikes = 1
            potential = reset_potential
            adaptation += adaptation_increment
            refractory_until = probe_time + refractory_ms
    return {
        "potential_after_treatment": potential_after_treatment,
        "treatment_spike_count": treatment_spikes,
        "post_refractory_probe_spike_count": probe_spikes,
        "final_potential": potential,
    }


def run_condition(contract: dict[str, Any], condition_name: str) -> dict[str, Any]:
    arms = contract["input_family"][condition_name]["arms"]
    return {
        arm_name: {
            "production": production_arm(contract, condition_name, arm_name),
            "positive_ignore_shadow": shadow_arm(contract, condition_name, arm_name),
        }
        for arm_name in arms
    }


def nearly_equal(left: float, right: float) -> bool:
    return abs(left - right) <= TOLERANCE


def pair_matches(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        nearly_equal(
            float(left["potential_after_treatment"]),
            float(right["potential_after_treatment"]),
        )
        and left["treatment_spike_count"] == right["treatment_spike_count"]
        and left["post_refractory_probe_spike_count"]
        == right["post_refractory_probe_spike_count"]
    )


def map_outcome(
    contract: dict[str, Any],
    bindings_ok: bool,
    facts: dict[str, bool],
    refractory: dict[str, Any],
    outside: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    required = contract["machine_fact_binding"]["required_production_facts"]
    fact_key_map = {
        "deliver_group_groups_same_time_arrivals_by_target": "deliver_group_groups_same_time_arrivals_by_target",
        "positive_current_is_summed_separately": "positive_current_is_summed_separately",
        "negative_current_is_summed_separately": "negative_current_is_summed_separately",
        "net_current_is_positive_minus_negative": "net_current_is_positive_minus_negative",
        "refractory_branch_applies_min_zero_net_current": "refractory_branch_applies_min_zero_net_current",
        "schedule_arrival_accepts_signed SynapticArrival.current without sign rejection": "schedule_arrival_accepts_signed_current_without_sign_rejection",
    }
    machine_facts_ok = all(facts[fact_key_map[name]] for name in required)
    outside_match = all(
        pair_matches(row["production"], row["positive_ignore_shadow"])
        for row in outside.values()
    )
    refractory_simple_controls_match = all(
        pair_matches(
            refractory[name]["production"],
            refractory[name]["positive_ignore_shadow"],
        )
        for name in ("inhibition_only", "excitation_only")
    )
    treatment_spikes_zero = all(
        row[arm][side]["treatment_spike_count"] == 0
        for row in (refractory,)
        for arm in row
        for side in ("production", "positive_ignore_shadow")
    )
    balanced = refractory["balanced_same_time"]
    state_effect = not nearly_equal(
        float(balanced["production"]["potential_after_treatment"]),
        float(balanced["positive_ignore_shadow"]["potential_after_treatment"]),
    )
    functional_effect = (
        balanced["production"]["post_refractory_probe_spike_count"]
        != balanced["positive_ignore_shadow"]["post_refractory_probe_spike_count"]
    )
    supported_mixed_sign = (
        facts["deliver_group_groups_same_time_arrivals_by_target"]
        and facts["positive_current_is_summed_separately"]
        and facts["negative_current_is_summed_separately"]
        and facts["schedule_arrival_accepts_signed_current_without_sign_rejection"]
    )
    explicit_hits = contract["supported_contract_scope"][
        "explicit_refractory_netting_contract_hits"
    ]
    decision = {
        "source_bindings_ok": bindings_ok,
        "machine_facts_ok": machine_facts_ok,
        "outside_refractory_control_match": outside_match,
        "refractory_simple_controls_match": refractory_simple_controls_match,
        "refractory_treatment_spikes_zero": treatment_spikes_zero,
        "supported_mixed_sign_runtime_condition": supported_mixed_sign,
        "explicit_netting_contract_match": bool(explicit_hits),
        "state_effect": state_effect,
        "functional_effect": functional_effect,
    }
    if not (
        bindings_ok
        and machine_facts_ok
        and outside_match
        and refractory_simple_controls_match
        and treatment_spikes_zero
    ):
        return "INVALID_DIAGNOSTIC", decision
    if explicit_hits:
        return "EXPLICIT_NETTING_CONTRACT_MATCHES_PRODUCTION", decision
    if not supported_mixed_sign:
        return "NO_SUPPORTED_MIXED_SIGN_RUNTIME_CONDITION", decision
    if state_effect and functional_effect:
        return "FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT", decision
    if state_effect and not functional_effect:
        return "STATE_ONLY_REFRACTORY_ACCOUNTING_EFFECT", decision
    if not state_effect and not functional_effect:
        return "NO_SEMANTIC_DIFFERENCE_UNDER_FIXED_PROBE", decision
    return "MIXED_OR_AMBIGUOUS_REFRACTORY_CONTRACT", decision


def preflight(contract: dict[str, Any]) -> dict[str, Any]:
    bindings = verify_bindings(contract)
    facts = machine_facts(contract)
    family = contract["input_family"]
    expected_arms = {"inhibition_only", "balanced_same_time", "excitation_only"}
    family_ok = (
        set(family["refractory_condition"]["arms"]) == expected_arms
        and set(family["outside_refractory_control"]["arms"]) == expected_arms
        and family["refractory_condition"]["arms"]
        == family["outside_refractory_control"]["arms"]
        and float(family["refractory_condition"]["treatment_time_ms"])
        == float(family["outside_refractory_control"]["treatment_time_ms"])
        and float(family["refractory_condition"]["probe_time_ms"])
        == float(family["outside_refractory_control"]["probe_time_ms"])
        and float(family["refractory_condition"]["probe_current"])
        == float(family["outside_refractory_control"]["probe_current"])
    )
    ancestry = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            contract["source_binding"]["main"],
            "HEAD",
        ],
        check=False,
    ).returncode == 0
    return {
        "source_blob_verification": bindings,
        "all_source_bindings_ok": all(bindings.values()),
        "machine_facts": facts,
        "machine_facts_ok": all(facts.values()),
        "matched_family_materialized": family_ok,
        "git_head": git("rev-parse", "HEAD"),
        "main_is_ancestor": ancestry,
    }


def write_raw_then_summary(
    output_dir: Path,
    raw: dict[str, Any],
) -> tuple[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "raw.json"
    with raw_path.open("w", encoding="utf-8") as handle:
        handle.write(canonical(raw) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    reloaded = json.loads(raw_path.read_text(encoding="utf-8"))
    if canonical(reloaded) != canonical(raw):
        raise RuntimeError("raw artifact round-trip mismatch")
    raw_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    return raw_sha, raw_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    contract = load_contract()
    pre = preflight(contract)
    valid_preflight = (
        pre["all_source_bindings_ok"]
        and pre["machine_facts_ok"]
        and pre["matched_family_materialized"]
        and pre["main_is_ancestor"]
    )
    if not valid_preflight:
        raise SystemExit(f"preflight failed: {canonical(pre)}")
    if args.preflight_only:
        print(canonical(pre))
        return
    if args.output_dir is None:
        raise SystemExit("--output-dir is required unless --preflight-only is used")

    refractory = run_condition(contract, "refractory_condition")
    outside = run_condition(contract, "outside_refractory_control")
    outcome, decision_facts = map_outcome(
        contract,
        pre["all_source_bindings_ok"],
        pre["machine_facts"],
        refractory,
        outside,
    )
    input_digest = sha256_text(canonical(contract["input_family"]))
    contract_sha = hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest()
    raw = {
        "analyst_authority": contract["analyst_authority"],
        "candidate_id": contract["candidate_id"],
        "lane": contract["lane"],
        "research_layer": contract["research_layer"],
        "evidentiary_status": contract["evidentiary_status"],
        "source_binding": contract["source_binding"],
        "source_blob_verification": pre["source_blob_verification"],
        "machine_facts": pre["machine_facts"],
        "input_family_digest": input_digest,
        "comparator": contract["comparator"],
        "observables": contract["observables"],
        "refractory_results": refractory,
        "outside_refractory_control": outside,
        "decision_facts": decision_facts,
        "mapped_outcome": outcome,
        "git_head": pre["git_head"],
        "contract_sha256": contract_sha,
        "workflow_run_id": int(os.environ.get("GITHUB_RUN_ID", "0")),
        "stop_required": True,
    }
    raw_sha, _ = write_raw_then_summary(args.output_dir, raw)
    summary = {
        key: raw[key]
        for key in (
            "analyst_authority",
            "candidate_id",
            "lane",
            "research_layer",
            "evidentiary_status",
            "source_binding",
            "source_blob_verification",
            "machine_facts",
            "input_family_digest",
            "comparator",
            "observables",
            "refractory_results",
            "outside_refractory_control",
            "decision_facts",
            "mapped_outcome",
            "git_head",
            "contract_sha256",
            "workflow_run_id",
            "stop_required",
        )
    }
    summary["raw_sha256"] = raw_sha
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(canonical(summary) + "\n", encoding="utf-8")
    print(
        canonical(
            {
                "mapped_outcome": outcome,
                "raw_sha256": raw_sha,
                "stop_required": True,
            }
        )
    )


if __name__ == "__main__":
    main()
