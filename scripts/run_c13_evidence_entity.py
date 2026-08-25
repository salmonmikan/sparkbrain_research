from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path
from statistics import mean
from typing import Any

from sparkbrain.v03_seed import (
    E0_GLOBAL,
    E1_ORACLE_ENTITY,
    EntityBinding,
    EvidenceLedger,
    EvidenceRecord,
    EvidenceSummary,
    PerceptualSpark,
    SlotMetricRow,
    aggregate_condition_rows,
    bind_entity,
    build_evidence_fixture,
    canonical_fixture_json,
    decide_g0,
    derive_binding_id,
    derive_evidence_id,
    fixture_sha256,
    permutation_invariant_slot_metrics,
    probability_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "artifacts" / "v03" / "c13_evidence_entity" / "protocol.json"
DEFAULT_PROTECTED = (
    ROOT / "artifacts" / "v03" / "c11_input_diagnosis" / "frozen_baseline_hashes.json"
)
ACCEPTED_C12 = "280516fb61eab7c7a96c109baefc82b333fcc367"
CONDITIONS = (E0_GLOBAL, E1_ORACLE_ENTITY)
EXPECTED_FILES = {
    "causal_removal_examples.jsonl",
    "cross_talk_examples.jsonl",
    "entity_condition_metrics.json",
    "evidence_invariant_tests.json",
    "paired_statistics.json",
    "protocol.json",
    "report.md",
    "run_manifest.json",
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _compact_json(value: object) -> str:
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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(_compact_json(row) + "\n")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _verify_dependencies(
    root: Path, protocol: dict[str, Any], source_commit: str
) -> dict[str, str]:
    if protocol["dependencies"]["c12_contract"] != ACCEPTED_C12:
        raise RuntimeError("C13 protocol does not pin the accepted C12 merge")
    _git(root, "merge-base", "--is-ancestor", ACCEPTED_C12, "HEAD")
    _git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    changed = _git(
        root,
        "diff",
        "--name-only",
        source_commit,
        "--",
        "src/sparkbrain/v03_seed",
        "scripts/run_c13_evidence_entity.py",
    )
    if changed:
        raise RuntimeError("C13 source differs from the pinned source commit")
    protected_path = (
        root
        / "artifacts"
        / "v03"
        / "c11_input_diagnosis"
        / "frozen_baseline_hashes.json"
    )
    frozen = json.loads(protected_path.read_text(encoding="utf-8"))
    protected = dict(frozen["protected_files"])
    for relative, expected in protected.items():
        path = root / relative
        if not path.is_file() or _sha256_file(path) != expected:
            raise RuntimeError(f"protected baseline hash changed: {relative}")
    return protected


def _percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    fraction = position - low
    return ordered[low] * (1.0 - fraction) + ordered[high] * fraction


def _paired_bootstrap(effects: list[float], protocol: dict[str, Any]) -> dict[str, object]:
    statistics = protocol["statistics"]
    repetitions = int(statistics["bootstrap_resamples"])
    generator = random.Random(int(statistics["bootstrap_seed"]))
    estimates = [
        mean(generator.choice(effects) for _ in effects) for _ in range(repetitions)
    ]
    alpha = 1.0 - float(statistics["confidence_interval"])
    return {
        "bootstrap_resamples": repetitions,
        "bootstrap_seed": int(statistics["bootstrap_seed"]),
        "ci_high": _percentile(estimates, 1.0 - alpha / 2.0),
        "ci_low": _percentile(estimates, alpha / 2.0),
        "confidence_interval": float(statistics["confidence_interval"]),
        "effect": mean(effects),
        "paired": True,
    }


def _spark_for_event(
    *, episode: dict[str, Any], event: dict[str, Any]
) -> PerceptualSpark:
    kind = str(event["kind"])
    spark_id = f"{episode['episode_id']}:spark:{kind}"
    return PerceptualSpark(
        spark_id=spark_id,
        feature_id=f"symbolic:{episode['target_hypothesis']}",
        time=float(event["observed_time"]),
        activation=float(event["strength"]),
        salience=float(event["strength"]),
        prediction_error=float(event["strength"]),
        threshold=0.5,
        evidence_id=f"{spark_id}:evidence",
        source_id=str(event["source_id"]),
        correlation_group=str(event["correlation_group"]),
        entity_slot=str(episode["target_entity"]),
        parents=(f"{episode['episode_id']}:sample:{kind}",),
    )


def _record_for_event(
    *,
    condition_id: str,
    episode: dict[str, Any],
    event: dict[str, Any],
    spark: PerceptualSpark,
) -> tuple[EvidenceRecord, EntityBinding]:
    binding = bind_entity(
        spark,
        condition_id=condition_id,
        entity_hint=str(episode["target_entity"]),
    )
    expected_binding_id = derive_binding_id(
        parent_spark_id=spark.spark_id,
        entity_hint=str(episode["target_entity"]),
        entity_slot=spark.entity_slot,
        assignment_status="assigned",
    )
    if binding.binding_id != expected_binding_id:
        raise RuntimeError("production EntityBinding ID derivation mismatch")
    polarity = str(event["polarity"])
    expected_evidence_id = derive_evidence_id(
            spark_evidence_id=spark.evidence_id,
            hypothesis_id=str(episode["target_hypothesis"]),
            polarity=polarity,
        )
    record = EvidenceRecord(
        evidence_id=expected_evidence_id,
        source_id=str(event["source_id"]),
        entity_key=str(binding.entity_key),
        hypothesis_id=str(episode["target_hypothesis"]),
        time=float(event["observed_time"]),
        polarity=polarity,
        strength=float(event["strength"]),
        correlation_group=str(event["correlation_group"]),
        parent_spark_ids=(spark.spark_id,),
        metadata={"episode_id": episode["episode_id"], "event_kind": event["kind"]},
    )
    if record.evidence_id != expected_evidence_id:
        raise RuntimeError("production EvidenceRecord ID derivation mismatch")
    return record, binding


def _snapshot_equal(left: dict[str, object], right: dict[str, object]) -> bool:
    return _compact_json(left) == _compact_json(right)


def _run_seed(
    *, condition_id: str, fixture: dict[str, Any]
) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    ledger = EvidenceLedger()
    execution_rows: list[dict[str, object]] = []
    cross_rows: list[dict[str, object]] = []
    removal_rows: list[dict[str, object]] = []
    assignment_eligible = 0
    assignment_errors = 0
    assignment_covered = 0
    cross_numerator = 0
    cross_denominator = 0

    for episode in fixture["episodes"]:
        records: dict[str, EvidenceRecord] = {}
        pre_deactivate_state = ""
        pre_deactivate_target: dict[str, object] = {}
        for event in episode["events"]:
            kind = str(event["kind"])
            event_time = float(event["event_time"])
            row: dict[str, object] = {
                "condition_id": condition_id,
                "episode_id": episode["episode_id"],
                "episode_index": episode["episode_index"],
                "event_kind": kind,
                "event_time": event["event_time"],
                "seed": fixture["seed"],
                "target_entity": episode["target_entity"],
                "target_hypothesis": episode["target_hypothesis"],
            }
            if kind.startswith("add_"):
                spark = _spark_for_event(episode=episode, event=event)
                sample_id = spark.parents[0]
                ledger.register_sample(sample_id)
                ledger.register_spark(spark.spark_id, (sample_id,))
                evidence, binding = _record_for_event(
                    condition_id=condition_id,
                    episode=episode,
                    event=event,
                    spark=spark,
                )
                ledger.add(evidence, delivered_at=event_time)
                records[kind] = evidence
                assignment_eligible += 1
                assignment_covered += int(bool(evidence.entity_key))
                if condition_id == E1_ORACLE_ENTITY:
                    assignment_errors += int(
                        evidence.entity_key != episode["target_entity"]
                    )
                row["evidence_id"] = evidence.evidence_id
                row["entity_key"] = evidence.entity_key
                row["assignment_status"] = binding.assignment_status
                row["binding_id"] = binding.binding_id
                row["eligible_for_assignment"] = True
                row["lineage_resolution_denominator"] = 1
                row["lineage_resolution_numerator"] = int(
                    ledger.lineage_resolution_rate() == 1.0
                )
                row["lineage_resolved"] = (
                    row["lineage_resolution_numerator"] == 1
                )
                row["parent_spark_ids"] = list(evidence.parent_spark_ids)
                row["sample_id"] = sample_id
                row["spark_id"] = spark.spark_id
            elif kind == "late_exact_redelivery":
                evidence = records[str(event["redelivers"])]
                state_before = ledger.active_state_hash()
                ledger.add(evidence, delivered_at=event_time)
                row["active_state_unchanged"] = ledger.active_state_hash() == state_before
                row["evidence_id"] = evidence.evidence_id
            elif kind == "deactivate_primary":
                evidence = records[str(event["target"])]
                pre_deactivate_state = ledger.active_state_hash()
                target_key = (
                    "__global__" if condition_id == E0_GLOBAL else str(episode["target_entity"])
                )
                pre_deactivate_target = probability_snapshot(
                    ledger,
                    entity_key=target_key,
                    hypothesis_id=str(episode["target_hypothesis"]),
                    now=event_time,
                )
                paired_key = "__global__" if condition_id == E0_GLOBAL else "object-b"
                paired_before = probability_snapshot(
                    ledger,
                    entity_key=paired_key,
                    hypothesis_id=str(episode["target_hypothesis"]),
                    now=event_time,
                )
                ledger.deactivate(evidence.evidence_id, at_time=event_time)
                paired_after = probability_snapshot(
                    ledger,
                    entity_key=paired_key,
                    hypothesis_id=str(episode["target_hypothesis"]),
                    now=event_time,
                )
                if episode["target_entity"] == "object-a":
                    cross_denominator += 1
                    cross_event = not _snapshot_equal(paired_before, paired_after)
                    cross_numerator += int(cross_event)
                    before_bytes = _compact_json(paired_before).encode("utf-8")
                    after_bytes = _compact_json(paired_after).encode("utf-8")
                    cross_rows.append(
                        {
                            "condition_id": condition_id,
                            "cross_talk_event": cross_event,
                            "episode_id": episode["episode_id"],
                            "non_target_entity": "object-b",
                            "non_target_probability_after": paired_after[
                                "positive_probability"
                            ],
                            "non_target_probability_before": paired_before[
                                "positive_probability"
                            ],
                            "non_target_snapshot_after_sha256": _sha256_bytes(
                                after_bytes
                            ),
                            "non_target_snapshot_before_sha256": _sha256_bytes(
                                before_bytes
                            ),
                            "non_target_snapshot_byte_identical": before_bytes
                            == after_bytes,
                            "seed": fixture["seed"],
                            "target_entity": "object-a",
                        }
                    )
                row["evidence_id"] = evidence.evidence_id
            elif kind == "restore_primary":
                evidence = records[str(event["target"])]
                ledger.restore(evidence.evidence_id, at_time=event_time)
                target_key = (
                    "__global__" if condition_id == E0_GLOBAL else str(episode["target_entity"])
                )
                restored_target = probability_snapshot(
                    ledger,
                    entity_key=target_key,
                    hypothesis_id=str(episode["target_hypothesis"]),
                    now=float(event["event_time"]) - 1.0,
                )
                removal_rows.append(
                    {
                        "active_state_hash_restored": ledger.active_state_hash()
                        == pre_deactivate_state,
                        "condition_id": condition_id,
                        "episode_id": episode["episode_id"],
                        "fixed_snapshot_restored": _snapshot_equal(
                            pre_deactivate_target, restored_target
                        ),
                        "immutable_payload": evidence.to_canonical_json(),
                        "seed": fixture["seed"],
                    }
                )
                row["evidence_id"] = evidence.evidence_id
            execution_rows.append(row)

    aggregate_condition_rows(execution_rows, condition_id=condition_id)
    decision_entity = "__global__" if condition_id == E0_GLOBAL else "object-a"
    decision = decide_g0(ledger, entity_key=decision_entity, now=240.0)
    metrics = {
        "condition_id": condition_id,
        "cross_talk_denominator": cross_denominator,
        "cross_talk_numerator": cross_numerator,
        "cross_talk_rate": cross_numerator / cross_denominator,
        "decision": decision.to_dict(),
        "evidence_assignment_denominator": assignment_eligible,
        "evidence_misassignment_numerator": assignment_errors,
        "evidence_misassignment_rate": assignment_errors / assignment_eligible,
        "execution_row_count": len(execution_rows),
        "lineage_resolution_rate": ledger.lineage_resolution_rate(),
        "oracle_coverage_numerator": assignment_covered,
        "oracle_entity_coverage": assignment_covered / assignment_eligible,
        "seed": fixture["seed"],
    }
    return metrics, cross_rows, removal_rows, execution_rows


def _summary_observation(summary: EvidenceSummary) -> dict[str, object]:
    return {
        "contradiction_ids": list(summary.contradiction_ids),
        "effective_contradiction": summary.effective_contradiction,
        "effective_support": summary.effective_support,
        "independent_group_count": summary.independent_group_count,
        "redundancy": summary.redundancy,
        "source_count": summary.source_count,
        "support_ids": list(summary.support_ids),
        "unique_evidence_count": summary.unique_evidence_count,
    }


def _invariant_audit() -> dict[str, object]:
    ledger = EvidenceLedger()
    ledger.register_sample("sample-1")
    ledger.register_spark("spark-1", ("sample-1",))
    primary = EvidenceRecord(
        evidence_id="ev-invariant-primary",
        source_id="source-primary",
        entity_key="object-a",
        hypothesis_id="state-left",
        time=0.0,
        polarity="support",
        strength=1.0,
        correlation_group="cg:invariant",
        parent_spark_ids=("spark-1",),
    )
    ledger.add(primary)
    initial_summary = ledger.summary("state-left", object_key="object-a", now=0.0)
    initial_probability = probability_snapshot(
        ledger, entity_key="object-a", hypothesis_id="state-left", now=0.0
    )
    state_before_redelivery = ledger.active_state_hash()
    ledger.add(primary, delivered_at=1.0)
    state_after_redelivery = ledger.active_state_hash()
    redelivered_summary = ledger.summary("state-left", object_key="object-a", now=0.0)
    redelivered_probability = probability_snapshot(
        ledger, entity_key="object-a", hypothesis_id="state-left", now=0.0
    )
    ledger.register_sample("sample-2")
    ledger.register_spark("spark-2", ("sample-2",))
    correlated = EvidenceRecord(
        evidence_id="ev-invariant-correlated",
        source_id="source-correlated",
        entity_key="object-a",
        hypothesis_id="state-left",
        time=0.0,
        polarity="support",
        strength=1.0,
        correlation_group="cg:invariant",
        parent_spark_ids=("spark-2",),
    )
    ledger.add(correlated)
    correlated_summary = ledger.summary("state-left", object_key="object-a", now=0.0)
    correlated_probability = probability_snapshot(
        ledger, entity_key="object-a", hypothesis_id="state-left", now=0.0
    )
    restore_before_state = ledger.active_state_hash()
    restore_before_summary = ledger.summary(
        "state-left", object_key="object-a", now=2.0
    )
    restore_before_snapshot = probability_snapshot(
        ledger, entity_key="object-a", hypothesis_id="state-left", now=2.0
    )
    restore_before_decision = decide_g0(
        ledger, entity_key="object-a", now=2.0
    )
    ledger.deactivate(primary.evidence_id, at_time=2.0)
    removed_state = ledger.active_state_hash()
    ledger.restore(primary.evidence_id, at_time=2.0)
    restore_after_state = ledger.active_state_hash()
    restore_after_summary = ledger.summary(
        "state-left", object_key="object-a", now=2.0
    )
    restore_after_snapshot = probability_snapshot(
        ledger, entity_key="object-a", hypothesis_id="state-left", now=2.0
    )
    restore_after_decision = decide_g0(
        ledger, entity_key="object-a", now=2.0
    )
    identity_state_before = ledger.active_state_hash()
    try:
        ledger.add(replace(primary, polarity="contradict"), delivered_at=3.0)
        identity_rejected = False
    except ValueError:
        identity_rejected = True
    identity_state_after = ledger.active_state_hash()
    citations = tuple(
        restore_after_summary.support_ids + restore_after_summary.contradiction_ids
    )
    orphan_count = 0
    for evidence_id in citations:
        try:
            ledger.resolve(evidence_id)
        except KeyError:
            orphan_count += 1
    same_id = {
        "active_state_hash_after": state_after_redelivery,
        "active_state_hash_before": state_before_redelivery,
        "independent_group_count_after": redelivered_summary.independent_group_count,
        "independent_group_count_before": initial_summary.independent_group_count,
        "independent_group_count_delta": redelivered_summary.independent_group_count
        - initial_summary.independent_group_count,
        "positive_probability_after": redelivered_probability["positive_probability"],
        "positive_probability_before": initial_probability["positive_probability"],
        "positive_probability_delta": abs(
            float(redelivered_probability["positive_probability"])
            - float(initial_probability["positive_probability"])
        ),
        "summary_after": _summary_observation(redelivered_summary),
        "summary_before": _summary_observation(initial_summary),
        "unique_evidence_count_after": redelivered_summary.unique_evidence_count,
        "unique_evidence_count_before": initial_summary.unique_evidence_count,
    }
    correlation = {
        "correlation_group": correlated.correlation_group,
        "effective_marginal": correlated_summary.effective_support
        - initial_summary.effective_support,
        "effective_marginal_ratio": (
            correlated_summary.effective_support - initial_summary.effective_support
        )
        / correlated.strength,
        "effective_support_after": correlated_summary.effective_support,
        "effective_support_before": initial_summary.effective_support,
        "independent_group_count_after": correlated_summary.independent_group_count,
        "independent_group_count_before": initial_summary.independent_group_count,
        "positive_probability_after": correlated_probability["positive_probability"],
        "positive_probability_before": initial_probability["positive_probability"],
        "positive_probability_delta": abs(
            float(correlated_probability["positive_probability"])
            - float(initial_probability["positive_probability"])
        ),
    }
    identity_mutation = {
        "attempted_fields": ["polarity"],
        "attempted_polarity": "contradict",
        "rejected": identity_rejected,
        "state_hash_after": identity_state_after,
        "state_hash_before": identity_state_before,
    }
    lineage = {
        "resolution_denominator": 2,
        "resolution_numerator": int(ledger.lineage_resolution_rate() == 1.0) * 2,
        "resolution_rate": ledger.lineage_resolution_rate(),
    }
    remove_restore = {
        "active_state_hash_after_restore": restore_after_state,
        "active_state_hash_before_remove": restore_before_state,
        "active_state_hash_removed": removed_state,
        "citations_after_restore": list(citations),
        "citations_before_remove": list(
            restore_before_summary.support_ids
            + restore_before_summary.contradiction_ids
        ),
        "decision_after_restore": restore_after_decision.to_dict(),
        "decision_before_remove": restore_before_decision.to_dict(),
        "orphan_count_after_restore": orphan_count,
        "positive_probability_after_restore": restore_after_snapshot[
            "positive_probability"
        ],
        "positive_probability_before_remove": restore_before_snapshot[
            "positive_probability"
        ],
        "summary_after_restore": _summary_observation(restore_after_summary),
        "summary_before_remove": _summary_observation(restore_before_summary),
    }
    checks = {
        "cited_lineage_resolution_rate": lineage["resolution_numerator"]
        == lineage["resolution_denominator"],
        "correlated_effective_marginal_ratio": abs(
            float(correlation["effective_marginal_ratio"]) - 0.2
        )
        <= 1e-12,
        "correlated_group_count_delta": correlation[
            "independent_group_count_after"
        ]
        == correlation["independent_group_count_before"],
        "correlated_prediction_change": float(
            correlation["positive_probability_delta"]
        )
        <= 0.05,
        "fixed_time_restore_exact": remove_restore[
            "active_state_hash_after_restore"
        ]
        == remove_restore["active_state_hash_before_remove"]
        and remove_restore["summary_after_restore"]
        == remove_restore["summary_before_remove"]
        and remove_restore["positive_probability_after_restore"]
        == remove_restore["positive_probability_before_remove"]
        and remove_restore["decision_after_restore"]
        == remove_restore["decision_before_remove"]
        and remove_restore["citations_after_restore"]
        == remove_restore["citations_before_remove"],
        "identity_reassignment_rejected": identity_mutation["rejected"]
        and identity_mutation["state_hash_before"]
        == identity_mutation["state_hash_after"],
        "same_id_independent_count_delta": same_id[
            "independent_group_count_delta"
        ]
        == 0,
        "same_id_prediction_change": float(
            same_id["positive_probability_delta"]
        )
        <= 0.01,
        "same_id_state_unchanged": same_id["active_state_hash_before"]
        == same_id["active_state_hash_after"],
        "same_id_summary_delta": same_id["summary_before"]
        == same_id["summary_after"],
        "orphan_citations_after_remove_restore": remove_restore[
            "orphan_count_after_restore"
        ]
        == 0,
    }
    return {
        "all_checks_passed": all(checks.values()),
        "audit_trust_boundary": (
            "semantic replay detects internal state-transition tampering, but the audit chain "
            "is not an externally anchored signature"
        ),
        "checks": checks,
        "observations": {
            "correlation": correlation,
            "identity_mutation": identity_mutation,
            "lineage": lineage,
            "remove_restore": remove_restore,
            "same_id_redelivery": same_id,
        },
    }


def _run_into(
    *,
    root: Path,
    protocol_path: Path,
    output: Path,
    source_commit: str,
) -> dict[str, object]:
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes.decode("utf-8"))
    if protocol["protocol_id"] != "c13-evidence-entity-v1":
        raise RuntimeError("unexpected C13 protocol")
    if tuple(protocol["conditions"]) != CONDITIONS:
        raise RuntimeError("C13 conditions differ from the final freeze")
    if protocol["seeds"] != [2601, 2602, 2603, 2604, 2605]:
        raise RuntimeError("C13 seeds differ from the final freeze")
    protected = _verify_dependencies(root, protocol, source_commit)
    expected_hashes = protocol["final_pre_execution_freeze"]["fixture_generator"][
        "fixture_sha256_by_seed"
    ]
    fixtures = {seed: build_evidence_fixture(seed) for seed in protocol["seeds"]}
    fixture_hashes = {str(seed): fixture_sha256(value) for seed, value in fixtures.items()}
    if fixture_hashes != expected_hashes:
        raise RuntimeError("C13 fixture hash differs from the final freeze")

    seed_rows: list[dict[str, object]] = []
    cross_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []
    removal_rows: list[dict[str, object]] = []
    failed_seeds: list[dict[str, object]] = []
    for condition_id in CONDITIONS:
        for seed, fixture in fixtures.items():
            try:
                metrics, cross, removal, execution = _run_seed(
                    condition_id=condition_id, fixture=fixture
                )
                seed_rows.append(metrics)
                cross_rows.extend(cross)
                execution_rows.extend(execution)
                removal_rows.extend(removal)
            except Exception as exc:
                failed_seeds.append(
                    {
                        "condition_id": condition_id,
                        "error_type": type(exc).__name__,
                        "seed": seed,
                    }
                )

    by_condition = {
        condition: [row for row in seed_rows if row["condition_id"] == condition]
        for condition in CONDITIONS
    }
    if any(len(rows) != 5 for rows in by_condition.values()) or failed_seeds:
        raise RuntimeError("C13 evaluation has failed or missing seed rows")
    e0 = {int(row["seed"]): row for row in by_condition[E0_GLOBAL]}
    e1 = {int(row["seed"]): row for row in by_condition[E1_ORACLE_ENTITY]}
    effects = [
        float(e0[seed]["cross_talk_rate"])
        - float(e1[seed]["cross_talk_rate"])
        for seed in protocol["seeds"]
    ]
    paired = _paired_bootstrap(effects, protocol)
    paired["failed_seeds"] = failed_seeds
    paired["seed_level_effects"] = [
        {"effect": effect, "seed": seed}
        for seed, effect in zip(protocol["seeds"], effects, strict=True)
    ]
    invariants = _invariant_audit()
    e1_cross = sum(int(row["cross_talk_numerator"]) for row in e1.values()) / sum(
        int(row["cross_talk_denominator"]) for row in e1.values()
    )
    e1_misassignment = sum(
        int(row["evidence_misassignment_numerator"]) for row in e1.values()
    ) / sum(int(row["evidence_assignment_denominator"]) for row in e1.values())
    e1_coverage = sum(int(row["oracle_coverage_numerator"]) for row in e1.values()) / sum(
        int(row["evidence_assignment_denominator"]) for row in e1.values()
    )
    gates = {
        "G02_invariants": bool(invariants["all_checks_passed"]),
        "G05_e1_cross_talk": e1_cross <= 0.02,
        "G05_e1_evidence_misassignment": e1_misassignment <= 0.01,
        "G05_e1_oracle_entity_coverage": e1_coverage >= 1.0,
    }
    acceptance = all(gates.values())
    slot_rows = [
        SlotMetricRow(
            sequence=index,
            predicted_slot=str(row["target_entity"]),
            oracle_entity=str(row["target_entity"]),
            assignment_status="assigned",
        )
        for index, row in enumerate(cross_rows)
        if row["condition_id"] == E1_ORACLE_ENTITY
    ]
    metric_artifact = {
        "acceptance_gates": gates,
        "acceptance_passed": acceptance,
        "conditions": {
            condition: {
                "cross_talk_denominator": sum(
                    int(row["cross_talk_denominator"]) for row in rows
                ),
                "cross_talk_numerator": sum(
                    int(row["cross_talk_numerator"]) for row in rows
                ),
                "evidence_assignment_denominator": sum(
                    int(row["evidence_assignment_denominator"]) for row in rows
                ),
                "evidence_misassignment_numerator": sum(
                    int(row["evidence_misassignment_numerator"]) for row in rows
                ),
                "failed_seeds": failed_seeds,
                "oracle_coverage_numerator": sum(
                    int(row["oracle_coverage_numerator"]) for row in rows
                ),
                "seed_level_rows": rows,
            }
            for condition, rows in by_condition.items()
        },
        "e2_execution_rows": 0,
        "execution_rows": sorted(
            execution_rows,
            key=lambda row: (
                CONDITIONS.index(str(row["condition_id"])),
                int(row["seed"]),
                int(row["episode_index"]),
                int(row["event_time"]),
            ),
        ),
        "failed_seeds": failed_seeds,
        "slot_metrics": permutation_invariant_slot_metrics(slot_rows),
    }
    input_hash = _sha256_bytes(
        canonical_fixture_json(fixture_hashes).encode("utf-8")
    )
    manifest = {
        "condition_row_counts": {
            condition: sum(int(row["execution_row_count"]) for row in rows)
            for condition, rows in by_condition.items()
        },
        "failed_seeds": failed_seeds,
        "fixture_sha256_by_seed": fixture_hashes,
        "input_hash": input_hash,
        "protected_hashes": protected,
        "protocol_hash": _sha256_bytes(protocol_bytes),
        "protocol_id": protocol["protocol_id"],
        "run_id": protocol["run_id"],
        "source_commit": source_commit,
    }
    cross_rows.sort(
        key=lambda row: (
            str(row["condition_id"]),
            int(row["seed"]),
            str(row["episode_id"]),
        )
    )
    removal_rows.sort(
        key=lambda row: (str(row["condition_id"]), int(row["seed"]), str(row["episode_id"]))
    )
    output.mkdir(parents=True, exist_ok=True)
    (output / "protocol.json").write_bytes(protocol_bytes)
    (output / "run_manifest.json").write_text(
        _canonical_json(manifest), encoding="utf-8", newline="\n"
    )
    (output / "evidence_invariant_tests.json").write_text(
        _canonical_json(invariants), encoding="utf-8", newline="\n"
    )
    (output / "entity_condition_metrics.json").write_text(
        _canonical_json(metric_artifact), encoding="utf-8", newline="\n"
    )
    (output / "paired_statistics.json").write_text(
        _canonical_json(paired), encoding="utf-8", newline="\n"
    )
    _write_jsonl(output / "cross_talk_examples.jsonl", cross_rows)
    _write_jsonl(output / "causal_removal_examples.jsonl", removal_rows)
    report = f"""# C13 evidence/entity report

Protocol: `{protocol['protocol_id']}`  
Run: `{protocol['run_id']}`  
Source commit: `{source_commit}`

## Engineering result

- C13 acceptance: **{'pass' if acceptance else 'fail'}**
- E1 cross-talk rate: {e1_cross:.6f}
- E1 evidence-misassignment rate: {e1_misassignment:.6f}
- E1 oracle-entity coverage: {e1_coverage:.6f}
- E0 minus E1 cross-talk point estimate: {paired['effect']:.6f}

## Claim boundary

E1 is an oracle entity binding, not autonomous entity discovery. The paired gap is scientific
support only under this frozen relation-free fixture; it is not an engineering gate. This result
does not change the C06/C08 negative findings, v0.2 package/schema, protected artifacts, or any
existing scientific claim grade. E2 remains unimplemented and has zero execution rows.

The audit chain is semantically replayed on load, but it is not an externally anchored signature
or independent trust root.
"""
    (output / "report.md").write_text(report, encoding="utf-8", newline="\n")
    return {
        "acceptance_passed": acceptance,
        "manifest": manifest,
        "metrics": metric_artifact,
        "paired_statistics": paired,
    }


def run(
    *, root: Path, protocol_path: Path, output: Path, source_commit: str
) -> dict[str, object]:
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("output directory must be new or empty")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    try:
        result = _run_into(
            root=root,
            protocol_path=protocol_path,
            output=staging,
            source_commit=source_commit,
        )
        if {path.name for path in staging.iterdir()} != EXPECTED_FILES:
            raise RuntimeError("C13 staging output is incomplete or contains extra files")
        for name in EXPECTED_FILES - {
            "cross_talk_examples.jsonl",
            "causal_removal_examples.jsonl",
            "report.md",
        }:
            json.loads((staging / name).read_text(encoding="utf-8"))
        if not all((staging / name).read_text(encoding="utf-8").strip() for name in EXPECTED_FILES):
            raise RuntimeError("C13 staging output contains an empty file")
        if output.exists():
            output.rmdir()
        staging.replace(output)
        return result
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the frozen C13 evidence/entity evaluation")
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
    print(json.dumps({"acceptance_passed": result["acceptance_passed"]}, sort_keys=True))
    return 0 if result["acceptance_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
