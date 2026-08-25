from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import subprocess
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

from sparkbrain.v03_seed import EvidenceLedger, EvidenceRecord, V03ReferenceLoop
from sparkbrain.v03_seed.coalition import C14_BOUNDED_MODE, CoalitionGate
from sparkbrain.v03_seed.evidence import derive_evidence_id

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "artifacts" / "v03" / "c14_coalition_gate" / "protocol.json"
EXPECTED_FILES = {
    "causal_evidence_removal.jsonl",
    "fixed_logit_interventions.jsonl",
    "gate_ablation_metrics.json",
    "no_ignition_reasons.json",
    "protocol.json",
    "report.md",
}
SOURCE_PATHS = (
    "src/sparkbrain/v03_seed/contracts.py",
    "src/sparkbrain/v03_seed/coalition.py",
    "src/sparkbrain/v03_seed/loop.py",
    "scripts/run_c14_coalition_gate.py",
)


class _NoopInterpreter:
    def interpret(self, spark: object) -> tuple[()]:
        return ()


class _TracingCoalitionGate(CoalitionGate):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list[str] = []

    def evaluate(self, *args: object, mode: str, **kwargs: object) -> object:
        self.calls.append(mode)
        return super().evaluate(*args, mode=mode, **kwargs)


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_json(path: Path, value: object) -> None:
    path.write_text(_canonical(value) + "\n", encoding="utf-8", newline="\n")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(_canonical(row) + "\n")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def fixed_logit_payload(protocol: dict[str, Any]) -> dict[str, object]:
    frozen = protocol["frozen_logits"]
    return {
        "labels": list(frozen["labels"]),
        "logits": list(frozen["actual_logits"]),
        "probabilities": list(frozen["probabilities"]),
        "schema_version": frozen["schema_version"],
    }


def build_fixture_document(protocol: dict[str, Any], seed: int) -> dict[str, object]:
    freeze = protocol["final_pre_execution_freeze"]
    generator = freeze["fixture_generator"]
    cases: list[dict[str, object]] = []
    for case_index, case_id in enumerate(generator["case_order"]):
        case = json.loads(_canonical(freeze["case_specs"][case_id]))
        case["case_id"] = case_id
        case["case_index"] = case_index
        case["id_prefix"] = generator["id_prefix"].format(
            seed=seed,
            case_index=case_index,
            case_id=case_id,
        )
        cases.append(case)
    return {
        "cases": cases,
        "document_id_prefix": generator["document_id_prefix"].format(seed=seed),
        "schema_version": "0.3",
        "seed": seed,
        "templates": dict(generator["id_templates"]),
    }


def fixture_sha256(protocol: dict[str, Any], seed: int) -> str:
    return _sha256_bytes(_canonical(build_fixture_document(protocol, seed)).encode())


def _preflight(
    *, root: Path, protocol_path: Path, source_commit: str
) -> tuple[dict[str, Any], bytes, dict[str, str], dict[str, str]]:
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes.decode("utf-8"))
    dependencies = protocol["dependencies"]
    if dependencies.get("runner_execution_allowed") is not True:
        raise RuntimeError("C14 runner execution is disabled until the source-pin amendment")
    if dependencies.get("c14_source_pin") != source_commit:
        raise RuntimeError("C14 source commit does not match the preregistered pin")

    for name in ("c12_merge", "c13_merge", "c13_source_contract"):
        commit = str(dependencies[name])
        _git(root, "cat-file", "-e", f"{commit}^{{commit}}")
    _git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    _git(root, "merge-base", "--is-ancestor", dependencies["c12_merge"], "HEAD")
    _git(root, "merge-base", "--is-ancestor", dependencies["c13_merge"], "HEAD")
    changed = _git(root, "diff", "--name-only", source_commit, "--", *SOURCE_PATHS)
    if changed:
        raise RuntimeError("C14 source differs from the preregistered source commit")
    learned_changed = _git(
        root,
        "diff",
        "--name-only",
        dependencies["c13_merge"],
        source_commit,
        "--",
        "src/sparkbrain/learned",
    )
    if learned_changed:
        raise RuntimeError("C14 must not change the v0.2 learned backend")

    frozen = protocol["frozen_logits"]
    fixed_hash = _sha256_bytes(_canonical(fixed_logit_payload(protocol)).encode())
    if fixed_hash != frozen["sha256"]:
        raise RuntimeError("C14 fixed-logit hash mismatch")
    generator = protocol["final_pre_execution_freeze"]["fixture_generator"]
    fixture_hashes: dict[str, str] = {}
    for seed in protocol["seeds"]:
        actual = fixture_sha256(protocol, int(seed))
        expected = generator["full_fixture_sha256_by_seed"][str(seed)]
        if actual != expected:
            raise RuntimeError(f"C14 full fixture hash mismatch for seed {seed}")
        fixture_hashes[str(seed)] = actual

    protected_path = (
        root / "artifacts" / "v03" / "c11_input_diagnosis" / "frozen_baseline_hashes.json"
    )
    protected_manifest = json.loads(protected_path.read_text(encoding="utf-8"))
    protected = dict(protected_manifest["protected_files"])
    if len(protected) != 5:
        raise RuntimeError("C14 protected baseline must contain exactly five files")
    for relative, expected in protected.items():
        path = root / relative
        if not path.is_file() or _sha256_file(path) != expected:
            raise RuntimeError(f"protected baseline hash changed: {relative}")
    return protocol, protocol_bytes, fixture_hashes, protected


def _record_for_role(
    *, protocol: dict[str, Any], seed: int, case_id: str, role_spec: dict[str, Any]
) -> tuple[EvidenceRecord, str, str]:
    generator = protocol["final_pre_execution_freeze"]["fixture_generator"]
    case_index = generator["case_order"].index(case_id)
    prefix = generator["id_prefix"].format(
        seed=seed,
        case_index=case_index,
        case_id=case_id,
    )
    role = str(role_spec["role"])
    sample_id = generator["sample_id"].format(id_prefix=prefix, role=role)
    spark_id = generator["spark_id"].format(id_prefix=prefix, role=role)
    spark_evidence_id = generator["spark_evidence_id"].format(id_prefix=prefix, role=role)
    evidence_id = derive_evidence_id(
        spark_evidence_id=spark_evidence_id,
        hypothesis_id=str(role_spec["hypothesis_id"]),
        polarity=str(role_spec["polarity"]),
    )
    record = EvidenceRecord(
        evidence_id=evidence_id,
        source_id=str(role_spec["source_id"]),
        entity_key=str(protocol["final_pre_execution_freeze"]["case_specs"][case_id]["entity_key"]),
        hypothesis_id=str(role_spec["hypothesis_id"]),
        time=float(role_spec["evidence_time"]),
        polarity=str(role_spec["polarity"]),
        strength=float(role_spec["strength"]),
        correlation_group=str(role_spec["correlation_group"]),
        parent_evidence_ids=(),
        parent_spark_ids=(spark_id,),
        metadata=dict(role_spec["metadata"]),
    )
    return record, sample_id, spark_id


def _build_loop(
    *,
    protocol: dict[str, Any],
    seed: int,
    case_id: str,
    stage: str,
    roles_override: tuple[str, ...] | None = None,
    apply_redeliveries: bool = True,
) -> tuple[V03ReferenceLoop, dict[str, EvidenceRecord]]:
    spec = protocol["final_pre_execution_freeze"]["case_specs"][case_id]
    selected = (
        set(roles_override)
        if roles_override is not None
        else {str(row["role"]) for row in spec["records"]}
    )
    ledger = EvidenceLedger()
    records: dict[str, EvidenceRecord] = {}
    for role_spec in spec["records"]:
        role = str(role_spec["role"])
        if role not in selected:
            continue
        record, sample_id, spark_id = _record_for_role(
            protocol=protocol,
            seed=seed,
            case_id=case_id,
            role_spec=role_spec,
        )
        ledger.register_sample(sample_id)
        ledger.register_spark(spark_id, (sample_id,))
        ledger.add(record)
        if apply_redeliveries and int(role_spec.get("delivery_count", 1)) == 2:
            ledger.add(record, delivered_at=record.time)
        records[role] = record

    stage_spec = spec["stages"][stage]
    active_roles = set(stage_spec["active_roles"])
    for role, record in records.items():
        if role not in active_roles:
            ledger.deactivate(record.evidence_id, at_time=float(spec["now"]))
    deactivated = stage_spec.get("deactivated_role")
    if deactivated is not None and ledger.is_active(records[deactivated].evidence_id):
        ledger.deactivate(records[deactivated].evidence_id, at_time=float(spec["now"]))
    restored = stage_spec.get("restored_role")
    if restored is not None:
        record = records[restored]
        ledger.deactivate(record.evidence_id, at_time=float(spec["now"]))
        ledger.restore(record.evidence_id, at_time=float(spec["now"]))
    return (
        V03ReferenceLoop(_NoopInterpreter(), ledger=ledger, coalition_gate=_TracingCoalitionGate()),
        records,
    )


def _belief_snapshot(loop: V03ReferenceLoop, entity_key: str) -> dict[str, object]:
    states = [
        {
            "activation": row.activation,
            "cited_evidence_ids": sorted(set(row.cited_evidence_ids)),
            "entity_key": row.object_key or "__global__",
            "hypothesis_id": row.belief_key,
            "ignition_count": row.ignition_count,
            "last_score": row.last_score,
            "last_update_time": row.last_update_time,
        }
        for row in loop.belief_field.ranked(entity_key)
    ]
    states.sort(key=lambda row: (str(row["entity_key"]), str(row["hypothesis_id"])))
    return {"states": states, "winner": loop.belief_field.winner(entity_key)}


def _candidate_terms(decision: object) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in decision.coalitions:
        rows.append(
            {
                "activation": item.normalized_activation,
                "contradiction": item.normalized_contradiction,
                "contradiction_evidence_ids": list(item.contradiction_ids),
                "effective_support": item.normalized_support,
                "entity_key": item.object_key or "__global__",
                "evidence_count": item.evidence_count,
                "group_diversity": item.normalized_group_diversity,
                "hypothesis_id": item.belief_key,
                "independent_group_count": item.independent_group_count,
                "raw_activation": item.activation,
                "raw_effective_contradiction": item.effective_contradiction,
                "raw_effective_support": item.effective_support,
                "raw_redundancy": item.redundancy,
                "recency": item.normalized_recency,
                "redundancy": item.normalized_redundancy,
                "score": item.score,
                "source_count": item.source_count,
                "source_diversity": item.normalized_source_diversity,
                "stability": item.stability,
                "support_evidence_ids": list(item.support_ids),
                "support_evidence_times": list(item.support_times),
                "temporal_stability": item.normalized_stability,
                "weighted_activation": item.weighted_activation,
                "weighted_contradiction": item.weighted_contradiction,
                "weighted_group_diversity": item.weighted_group_diversity,
                "weighted_recency": item.weighted_recency,
                "weighted_redundancy": item.weighted_redundancy,
                "weighted_source_diversity": item.weighted_source_diversity,
                "weighted_support": item.weighted_support,
                "weighted_temporal_stability": item.weighted_stability,
            }
        )
    rows.sort(key=lambda row: (str(row["entity_key"]), str(row["hypothesis_id"])))
    return rows


def _decision_row(decision: object) -> dict[str, object]:
    runner_up = (
        decision.coalitions[1].score
        if len(decision.coalitions) > 1
        else decision.score - decision.margin
    )
    citations = (
        sorted(set(decision.coalitions[0].support_ids))
        if decision.ignited and decision.coalitions
        else []
    )
    return {
        "citations": citations,
        "ignited": decision.ignited,
        "margin": decision.margin,
        "reason": decision.reason,
        "runner_up_score": runner_up,
        "score": decision.score,
        "winner_entity": decision.object_key if decision.ignited else None,
        "winner_hypothesis": decision.belief_key if decision.ignited else None,
    }


def _mode(condition_id: str) -> str:
    return C14_BOUNDED_MODE if condition_id == "G1_evidence_coalition" else condition_id


def _execute_replay(
    *,
    protocol: dict[str, Any],
    seed: int,
    case_id: str,
    stage: str,
    condition_id: str,
    roles_override: tuple[str, ...] | None = None,
    apply_redeliveries: bool = True,
) -> tuple[list[dict[str, object]], V03ReferenceLoop, dict[str, EvidenceRecord]]:
    spec = protocol["final_pre_execution_freeze"]["case_specs"][case_id]
    loop, records = _build_loop(
        protocol=protocol,
        seed=seed,
        case_id=case_id,
        stage=stage,
        roles_override=roles_override,
        apply_redeliveries=apply_redeliveries,
    )
    observations: list[dict[str, object]] = []
    for evaluation_index in (1, 2):
        before = _belief_snapshot(loop, str(spec["entity_key"]))
        decision = loop.settle(
            now=float(spec["now"]),
            object_key=str(spec["entity_key"]),
            activation_overrides=dict(spec["activation_overrides"]),
            gate_mode=_mode(condition_id),
        )
        observations.append(
            {
                "belief_after": _belief_snapshot(loop, str(spec["entity_key"])),
                "belief_before": before,
                "candidate_terms": (
                    _candidate_terms(decision) if condition_id == "G1_evidence_coalition" else []
                ),
                "decision": _decision_row(decision),
                "evaluation_index": evaluation_index,
                "ledger_active_state_hash": loop.ledger.active_state_hash(),
            }
        )
        calls = loop.coalition_gate.calls
        if condition_id == "G1_evidence_coalition":
            if calls != [C14_BOUNDED_MODE] * evaluation_index:
                raise RuntimeError("C14 settle did not consume the bounded Coalition gate")
        elif calls:
            raise RuntimeError("probability control unexpectedly consumed Coalition terms")
    return observations, loop, records


def _comparator(
    *,
    protocol: dict[str, Any],
    seed: int,
    case_id: str,
    roles: tuple[str, ...],
) -> dict[str, object]:
    observations, _, _ = _execute_replay(
        protocol=protocol,
        seed=seed,
        case_id=case_id,
        stage="main",
        condition_id="G1_evidence_coalition",
        roles_override=roles,
        apply_redeliveries=False,
    )
    final = observations[1]
    return {
        "belief_after": final["belief_after"],
        "belief_before": final["belief_before"],
        "candidate_terms": final["candidate_terms"],
        "decision": final["decision"],
    }


def _decision_diff(left: dict[str, object], right: dict[str, object]) -> bool:
    return any(left[key] != right[key] for key in ("ignited", "winner_hypothesis", "reason"))


def _primary_rows(rows: list[dict[str, object]], condition: str) -> list[dict[str, object]]:
    return [row for row in rows if row["condition_id"] == condition and row["primary"]]


def _metric_rows(
    rows: list[dict[str, object]], protocol: dict[str, Any]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    conditions = protocol["conditions"]
    metrics = protocol["reported_metrics"]
    no_ignition = set(
        protocol["final_pre_execution_freeze"]["primary_metrics"]["expected_no_ignition_cases"]
    )
    by_key = {
        (str(row["condition_id"]), int(row["seed"]), str(row["case_id"])): row
        for row in rows
        if row["primary"]
    }

    def calculate(
        condition: str, selected: list[dict[str, object]]
    ) -> dict[str, tuple[float, float, int]]:
        ignited = [row for row in selected if row["decision"]["ignited"]]
        covered_correct = sum(
            row["decision"]["winner_hypothesis"] == row["expected_winner"] for row in ignited
        )
        negatives = [row for row in selected if row["case_id"] in no_ignition]
        scores = [float(row["decision"]["score"]) for row in selected]
        if condition == "G1_evidence_coalition":
            independent = [
                float(row["decision"]["score"])
                - float(row["comparators"]["primary_support_only"]["decision"]["score"])
                for row in selected
                if row["case_id"] == "independent_multi_source_support"
            ]
            contradiction = [
                float(row["decision"]["score"])
                - float(row["comparators"]["independent_support_baseline"]["decision"]["score"])
                for row in selected
                if row["case_id"] == "strong_contradiction"
            ]
        else:
            count = len({int(row["seed"]) for row in selected})
            independent = [0.0] * count
            contradiction = [0.0] * count
        seed_set = sorted({int(row["seed"]) for row in selected})
        g1_g0 = [
            int(
                _decision_diff(
                    by_key[("G1_evidence_coalition", seed, case)],
                    by_key[("G0_probability_margin", seed, case)],
                )
            )
            for seed in seed_set
            for case in protocol["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
        ]
        g1_no = [
            int(
                _decision_diff(
                    by_key[("G1_evidence_coalition", seed, case)],
                    by_key[("G1_no_coalition_ablation", seed, case)],
                )
            )
            for seed in seed_set
            for case in protocol["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
        ]
        return {
            "coverage": (len(ignited) / len(selected), float(len(ignited)), len(selected)),
            "covered_accuracy": (
                covered_correct / len(ignited) if ignited else 0.0,
                float(covered_correct),
                len(ignited),
            ),
            "false_ignition_rate": (
                sum(row["decision"]["ignited"] for row in negatives) / len(negatives),
                float(sum(row["decision"]["ignited"] for row in negatives)),
                len(negatives),
            ),
            "mean_top_coalition_score": (mean(scores), sum(scores), len(scores)),
            "mean_score_delta_from_independent_support": (
                mean(independent),
                sum(independent),
                len(independent),
            ),
            "mean_score_delta_from_contradiction": (
                mean(contradiction),
                sum(contradiction),
                len(contradiction),
            ),
            "g1_vs_g0_decision_difference_rate": (mean(g1_g0), float(sum(g1_g0)), len(g1_g0)),
            "g1_vs_no_coalition_decision_difference_rate": (
                mean(g1_no),
                float(sum(g1_no)),
                len(g1_no),
            ),
        }

    aggregate: list[dict[str, object]] = []
    seed_rows: list[dict[str, object]] = []
    for condition in conditions:
        values = calculate(condition, _primary_rows(rows, condition))
        for metric in metrics:
            value, numerator, denominator = values[metric]
            aggregate.append(
                {
                    "condition_id": condition,
                    "denominator": denominator,
                    "metric": metric,
                    "numerator": numerator,
                    "value": value,
                }
            )
        for seed in protocol["seeds"]:
            selected = [
                row for row in _primary_rows(rows, condition) if int(row["seed"]) == int(seed)
            ]
            values = calculate(condition, selected)
            for metric in metrics:
                value, numerator, denominator = values[metric]
                seed_rows.append(
                    {
                        "condition_id": condition,
                        "denominator": denominator,
                        "metric": metric,
                        "numerator": numerator,
                        "seed": int(seed),
                        "value": value,
                    }
                )
    return aggregate, seed_rows


def _percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    fraction = position - low
    return ordered[low] + fraction * (ordered[high] - ordered[low])


def _paired_statistics(
    rows: list[dict[str, object]], protocol: dict[str, Any]
) -> list[dict[str, object]]:
    primary = [row for row in rows if row["primary"]]
    by_key = {
        (str(row["condition_id"]), int(row["seed"]), str(row["case_id"])): row for row in primary
    }
    vectors = {
        "contradiction_score_delta": [
            float(
                by_key[("G1_evidence_coalition", int(seed), "strong_contradiction")]["decision"][
                    "score"
                ]
            )
            - float(
                by_key[("G1_evidence_coalition", int(seed), "strong_contradiction")]["comparators"][
                    "independent_support_baseline"
                ]["decision"]["score"]
            )
            for seed in protocol["seeds"]
        ],
        "g1_vs_g0_decision_difference": [
            float(
                _decision_diff(
                    by_key[("G1_evidence_coalition", int(seed), case)],
                    by_key[("G0_probability_margin", int(seed), case)],
                )
            )
            for seed in protocol["seeds"]
            for case in protocol["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
        ],
        "g1_vs_no_coalition_decision_difference": [
            float(
                _decision_diff(
                    by_key[("G1_evidence_coalition", int(seed), case)],
                    by_key[("G1_no_coalition_ablation", int(seed), case)],
                )
            )
            for seed in protocol["seeds"]
            for case in protocol["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
        ],
        "independent_support_score_delta": [
            float(
                by_key[("G1_evidence_coalition", int(seed), "independent_multi_source_support")][
                    "decision"
                ]["score"]
            )
            - float(
                by_key[("G1_evidence_coalition", int(seed), "independent_multi_source_support")][
                    "comparators"
                ]["primary_support_only"]["decision"]["score"]
            )
            for seed in protocol["seeds"]
        ],
    }
    rng = random.Random(int(protocol["statistics"]["bootstrap_seed"]))
    output: list[dict[str, object]] = []
    for effect_id in protocol["final_pre_execution_freeze"]["primary_metrics"][
        "bootstrap_effects_in_order"
    ]:
        vector = vectors[effect_id]
        estimates = [
            mean(vector[rng.randrange(len(vector))] for _ in vector)
            for _ in range(int(protocol["statistics"]["bootstrap_resamples"]))
        ]
        output.append(
            {
                "bootstrap_resamples": int(protocol["statistics"]["bootstrap_resamples"]),
                "bootstrap_seed": int(protocol["statistics"]["bootstrap_seed"]),
                "ci_high": _percentile(estimates, 0.975),
                "ci_low": _percentile(estimates, 0.025),
                "confidence_interval": float(protocol["statistics"]["confidence_interval"]),
                "effect_id": effect_id,
                "n": len(vector),
                "pairing_unit": protocol["statistics"]["pairing_unit"],
                "point_estimate": mean(vector),
            }
        )
    return output


def _run_evaluation(
    *,
    protocol: dict[str, Any],
    fixture_hashes: dict[str, str],
    fixed_hash: str,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    raw: list[dict[str, object]] = []
    removal: list[dict[str, object]] = []
    freeze = protocol["final_pre_execution_freeze"]
    case_order = freeze["fixture_generator"]["case_order"]
    for condition in protocol["conditions"]:
        for seed in protocol["seeds"]:
            for case_index, case_id in enumerate(case_order):
                spec = freeze["case_specs"][case_id]
                stages = (
                    ["main"]
                    if case_id != "necessary_evidence_remove_restore"
                    else ["baseline", "removed", "restored"]
                )
                stage_observations: dict[str, list[dict[str, object]]] = {}
                stage_records: dict[str, dict[str, EvidenceRecord]] = {}
                for stage in stages:
                    observations, _, records = _execute_replay(
                        protocol=protocol,
                        seed=int(seed),
                        case_id=case_id,
                        stage=stage,
                        condition_id=condition,
                    )
                    stage_observations[stage] = observations
                    stage_records[stage] = records
                    for observation in observations:
                        primary = (
                            stage == spec["primary_stage"]
                            and observation["evaluation_index"] == spec["primary_evaluation"]
                        )
                        comparators: dict[str, object | None] = {
                            "independent_support_baseline": None,
                            "primary_support_only": None,
                        }
                        if primary and condition == "G1_evidence_coalition":
                            if case_id in {
                                "independent_multi_source_support",
                                "same_id_exact_duplicate",
                                "correlated_distinct_copy",
                            }:
                                comparators["primary_support_only"] = _comparator(
                                    protocol=protocol,
                                    seed=int(seed),
                                    case_id=case_id,
                                    roles=("primary_support",),
                                )
                            if case_id == "strong_contradiction":
                                comparators["independent_support_baseline"] = _comparator(
                                    protocol=protocol,
                                    seed=int(seed),
                                    case_id=case_id,
                                    roles=("primary_support", "secondary_independent_support"),
                                )
                        expected = spec["expected_g1"]
                        if condition != "G1_evidence_coalition":
                            expected = {
                                "ignited": True,
                                "reason": "ignited",
                                "winner": "hypothesis-alpha",
                            }
                        raw.append(
                            {
                                "belief_after": observation["belief_after"],
                                "belief_before": observation["belief_before"],
                                "candidate_terms": observation["candidate_terms"],
                                "case_id": case_id,
                                "case_index": case_index,
                                "comparators": comparators,
                                "condition_id": condition,
                                "decision": observation["decision"],
                                "entity_key": spec["entity_key"],
                                "evaluation_index": observation["evaluation_index"],
                                "evidence_ids": sorted(
                                    record.evidence_id for record in records.values()
                                ),
                                "expected_ignited": expected["ignited"],
                                "expected_reason": expected["reason"],
                                "expected_winner": expected["winner"],
                                "fixed_logit_sha256": fixed_hash,
                                "fixture_sha256": fixture_hashes[str(seed)],
                                "ledger_active_state_hash": observation["ledger_active_state_hash"],
                                "now": spec["now"],
                                "primary": primary,
                                "schema_version": "0.3",
                                "seed": int(seed),
                                "stage": stage,
                            }
                        )
                if case_id == "necessary_evidence_remove_restore":
                    baseline = stage_observations["baseline"][1]
                    removed = stage_observations["removed"][1]
                    restored = stage_observations["restored"][1]
                    record = stage_records["baseline"]["secondary_independent_support"]
                    g1 = condition == "G1_evidence_coalition"
                    removal.append(
                        {
                            "baseline_active_state_hash": baseline["ledger_active_state_hash"],
                            "baseline_decision": baseline["decision"],
                            "baseline_terms": baseline["candidate_terms"][0] if g1 else None,
                            "case_id": case_id,
                            "condition_id": condition,
                            "fixed_logit_sha256": fixed_hash,
                            "fixture_sha256": fixture_hashes[str(seed)],
                            "immutable_evidence": record.to_canonical_json(),
                            "removed_active_state_hash": removed["ledger_active_state_hash"],
                            "removed_decision": removed["decision"],
                            "removed_terms": removed["candidate_terms"][0] if g1 else None,
                            "restore_belief_exact": baseline["belief_after"]
                            == restored["belief_after"],
                            "restore_decision_exact": baseline["decision"] == restored["decision"],
                            "restore_state_exact": baseline["ledger_active_state_hash"]
                            == restored["ledger_active_state_hash"],
                            "restore_terms_exact": baseline["candidate_terms"]
                            == restored["candidate_terms"],
                            "restored_active_state_hash": restored["ledger_active_state_hash"],
                            "restored_decision": restored["decision"],
                            "restored_terms": restored["candidate_terms"][0] if g1 else None,
                            "schema_version": "0.3",
                            "seed": int(seed),
                        }
                    )
    return raw, removal


def _engineering_gates(
    rows: list[dict[str, object]], removal: list[dict[str, object]], protocol: dict[str, Any]
) -> list[dict[str, object]]:
    thresholds = protocol["engineering_gates"]
    g1 = _primary_rows(rows, "G1_evidence_coalition")
    independent = [row for row in g1 if row["case_id"] == "independent_multi_source_support"]
    duplicate = [row for row in g1 if row["case_id"] == "same_id_exact_duplicate"]
    correlated = [row for row in g1 if row["case_id"] == "correlated_distinct_copy"]
    contradiction = [row for row in g1 if row["case_id"] == "strong_contradiction"]
    by_key = {
        (str(row["condition_id"]), int(row["seed"]), str(row["case_id"])): row
        for row in rows
        if row["primary"]
    }
    case_order = protocol["final_pre_execution_freeze"]["fixture_generator"]["case_order"]
    g1_g0 = mean(
        _decision_diff(
            by_key[("G1_evidence_coalition", int(seed), case)],
            by_key[("G0_probability_margin", int(seed), case)],
        )
        for seed in protocol["seeds"]
        for case in case_order
    )
    g1_no = mean(
        _decision_diff(
            by_key[("G1_evidence_coalition", int(seed), case)],
            by_key[("G1_no_coalition_ablation", int(seed), case)],
        )
        for seed in protocol["seeds"]
        for case in case_order
    )
    reason_set = sorted({str(row["decision"]["reason"]) for row in g1})
    fixed_ok = all(row["fixed_logit_sha256"] == protocol["frozen_logits"]["sha256"] for row in rows)
    observations: dict[str, tuple[object, str]] = {
        "fixed_logit_integrity_rate_min": (float(fixed_ok), ">="),
        "independent_support_ignition_rate_min": (
            mean(row["decision"]["ignited"] for row in independent),
            ">=",
        ),
        "independent_support_score_delta_min": (
            mean(
                float(row["decision"]["score"])
                - float(row["comparators"]["primary_support_only"]["decision"]["score"])
                for row in independent
            ),
            ">=",
        ),
        "same_id_score_and_decision_delta_max": (
            max(
                max(
                    abs(
                        float(row["decision"]["score"])
                        - float(row["comparators"]["primary_support_only"]["decision"]["score"])
                    ),
                    float(
                        _decision_diff(
                            row["decision"], row["comparators"]["primary_support_only"]["decision"]
                        )
                    ),
                )
                for row in duplicate
            ),
            "<=",
        ),
        "correlated_copy_independent_group_delta_max": (
            max(
                int(row["candidate_terms"][0]["independent_group_count"])
                - int(
                    row["comparators"]["primary_support_only"]["candidate_terms"][0][
                        "independent_group_count"
                    ]
                )
                for row in correlated
            ),
            "<=",
        ),
        "contradiction_score_delta_max": (
            max(
                float(row["decision"]["score"])
                - float(row["comparators"]["independent_support_baseline"]["decision"]["score"])
                for row in contradiction
            ),
            "<=",
        ),
        "removal_reversal_rate_min": (
            mean(
                not row["removed_decision"]["ignited"] and row["baseline_decision"]["ignited"]
                for row in removal
                if row["condition_id"] == "G1_evidence_coalition"
            ),
            ">=",
        ),
        "restore_exact_rate_min": (
            mean(
                row["restore_state_exact"]
                and row["restore_terms_exact"]
                and row["restore_decision_exact"]
                and row["restore_belief_exact"]
                for row in removal
                if row["condition_id"] == "G1_evidence_coalition"
            ),
            ">=",
        ),
        "g1_vs_g0_decision_difference_rate_min": (g1_g0, ">="),
        "g1_vs_no_coalition_decision_difference_rate_min": (g1_no, ">="),
        "required_reason_coverage": (reason_set, "coverage"),
        "call_graph_requires_coalition_score_consumption": (True, "call_graph"),
    }
    output: list[dict[str, object]] = []
    for gate_id, threshold in thresholds.items():
        observed, comparison = observations[gate_id]
        if comparison == ">=":
            passed = float(observed) >= float(threshold)
        elif comparison == "<=":
            passed = float(observed) <= float(threshold)
        elif comparison == "coverage":
            passed = set(observed) == set(threshold)
        else:
            passed = bool(observed) is bool(threshold)
        output.append(
            {
                "comparison": comparison,
                "gate_id": gate_id,
                "observed": observed,
                "passed": passed,
                "threshold": threshold,
            }
        )
    return output


def _generate(
    *,
    root: Path,
    output: Path,
    protocol: dict[str, Any],
    protocol_bytes: bytes,
    source_commit: str,
    fixture_hashes: dict[str, str],
    protected: dict[str, str],
) -> dict[str, object]:
    fixed_hash = protocol["frozen_logits"]["sha256"]
    raw, removal = _run_evaluation(
        protocol=protocol,
        fixture_hashes=fixture_hashes,
        fixed_hash=fixed_hash,
    )
    if len(raw) != 360 or len(removal) != 15:
        raise RuntimeError("C14 raw artifact cardinality mismatch")
    aggregate, seed_rows = _metric_rows(raw, protocol)
    paired = _paired_statistics(raw, protocol)
    gates = _engineering_gates(raw, removal, protocol)
    failed = [
        {
            "reasons": sorted(row["gate_id"] for row in gates if not row["passed"]),
            "seed": int(seed),
        }
        for seed in protocol["seeds"]
        if any(not row["passed"] for row in gates)
    ]
    g1_primary = _primary_rows(raw, "G1_evidence_coalition")
    required = list(protocol["engineering_gates"]["required_reason_coverage"])
    counts = {reason: 0 for reason in required}
    references: list[dict[str, object]] = []
    for row in g1_primary:
        reason = str(row["decision"]["reason"])
        counts[reason] += 1
        references.append(
            {
                "case_id": row["case_id"],
                "case_index": row["case_index"],
                "condition_id": row["condition_id"],
                "evaluation_index": row["evaluation_index"],
                "reason": reason,
                "seed": row["seed"],
                "stage": row["stage"],
            }
        )
    reasons = {
        "coverage_passed": set(counts) == {reason for reason, count in counts.items() if count},
        "observed_reason_counts": counts,
        "protocol_id": protocol["protocol_id"],
        "raw_references": references,
        "required_reasons": required,
        "run_id": protocol["run_id"],
        "schema_version": "0.3",
    }
    manifest = {
        "dependency_hashes": {
            key: protocol["dependencies"][key]
            for key in ("c12_merge", "c13_merge", "c13_source_contract")
        },
        "failed_seeds": failed,
        "fixed_logit_hash": fixed_hash,
        "fixture_hashes": fixture_hashes,
        "protected_hashes": protected,
        "protocol_hash": _sha256_bytes(protocol_bytes),
        "raw_row_counts": {
            "causal_evidence_removal_jsonl": len(removal),
            "fixed_logit_interventions_jsonl": len(raw),
        },
        "source_commit": source_commit,
    }
    metrics = {
        "aggregate_metrics": aggregate,
        "engineering_gates": gates,
        "failed_seeds": failed,
        "manifest": manifest,
        "paired_statistics": paired,
        "protocol_id": protocol["protocol_id"],
        "run_id": protocol["run_id"],
        "schema_version": "0.3",
        "seed_level_rows": seed_rows,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "protocol.json").write_bytes(protocol_bytes)
    _write_jsonl(output / "fixed_logit_interventions.jsonl", raw)
    _write_json(output / "gate_ablation_metrics.json", metrics)
    _write_jsonl(output / "causal_evidence_removal.jsonl", removal)
    _write_json(output / "no_ignition_reasons.json", reasons)
    passed = all(row["passed"] for row in gates)
    report = f"""# C14 Coalition-driven Ignition

Protocol: `{protocol["protocol_id"]}`  
Run: `{protocol["run_id"]}`  
Source commit: `{source_commit}`  
Engineering acceptance: `{"pass" if passed else "fail"}`

This local CPU synthetic intervention run tests whether the bounded attributable-evidence
Coalition score is consumed by the isolated v0.3 reference loop while frozen logits remain
unchanged. It does not establish external accuracy, semantic understanding, biological fidelity,
or energy efficiency. The accepted C06/C08 negative findings, v0.2 package/schema, claim grades,
release metadata, and protected hashes remain unchanged.
"""
    (output / "report.md").write_text(report, encoding="utf-8", newline="\n")
    return {"acceptance_passed": passed, "failed_seeds": failed}


def run(*, root: Path, protocol_path: Path, output: Path, source_commit: str) -> dict[str, object]:
    protocol, protocol_bytes, fixture_hashes, protected = _preflight(
        root=root,
        protocol_path=protocol_path,
        source_commit=source_commit,
    )
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("output directory must be new or empty")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    try:
        result = _generate(
            root=root,
            output=staging,
            protocol=protocol,
            protocol_bytes=protocol_bytes,
            source_commit=source_commit,
            fixture_hashes=fixture_hashes,
            protected=protected,
        )
        if {path.name for path in staging.iterdir()} != EXPECTED_FILES:
            raise RuntimeError("C14 staging output is incomplete or contains extra files")
        if output.exists():
            output.rmdir()
        staging.replace(output)
        return result
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the frozen C14 Coalition evaluation")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    result = run(
        root=args.root.resolve(),
        protocol_path=args.protocol.resolve(),
        output=args.output.resolve(),
        source_commit=args.source_commit,
    )
    print(_canonical(result))
    return 0 if result["acceptance_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
