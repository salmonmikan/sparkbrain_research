from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from sparkbrain.v04.contracts import CascadeEvent, SpikeEvent
from sparkbrain.v05.assemblies import (
    AssemblyConfig,
    TemporalAssemblyMemory,
    pattern_from_spikes,
    patterns_from_step,
)
from sparkbrain.v05.prediction import AssemblyPredictor

CONTRACT_PATH = Path(
    "analysis/architecture/"
    "assembly_crosscascade_fallback_segmentation_cycle1_contract_20260920.json"
)


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


def spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=1.0,
        x=0.0,
        y=0.0,
        source_pulse_ids=("synthetic-development",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def cascade(row: dict[str, Any]) -> CascadeEvent:
    ordered = tuple(int(value) for value in row["ordered_units"])
    return CascadeEvent(
        cascade_id=str(row["cascade_id"]),
        start_ms=float(row["start_ms"]),
        end_ms=float(row["end_ms"]),
        spike_count=len(ordered),
        unit_ids=tuple(int(value) for value in row["unit_ids"]),
        ordered_units=ordered,
        spatial_spread=0.0,
        novelty=0.0,
        prediction_error=0.0,
        recurrence=0.0,
        signature=f"synthetic-{row['cascade_id']}",
    )


def materialize_family(
    contract: dict[str, Any],
) -> tuple[tuple[SpikeEvent, ...], dict[str, tuple[CascadeEvent, ...]]]:
    family = contract["input_family"]
    spikes = tuple(
        spike(float(row["time_ms"]), int(row["unit_id"])) for row in family["spikes"]
    )
    variants = {
        name: tuple(cascade(row) for row in rows)
        for name, rows in family["segmentation_variants"].items()
    }
    return spikes, variants


def shadow_boundary_preserving(
    cascades: tuple[CascadeEvent, ...],
    spikes: tuple[SpikeEvent, ...],
    *,
    temporal_bin_ms: float,
    excluded_unit_ids: tuple[int, ...],
    source_kind: str,
) -> tuple[Any, ...]:
    excluded = set(excluded_unit_ids)
    spike_rows = tuple(row for row in spikes if row.unit_id not in excluded)
    patterns = []
    for item in cascades:
        rows = [
            row
            for row in spike_rows
            if item.start_ms - 1e-9 <= row.time_ms <= item.end_ms + 1e-9
            and row.unit_id in item.unit_ids
        ]
        pattern = pattern_from_spikes(
            rows,
            source_cascade_id=item.cascade_id,
            temporal_bin_ms=temporal_bin_ms,
            source_kind=source_kind,
        )
        if pattern is not None:
            patterns.append(pattern)
    return tuple(patterns)


def current_extractor(
    cascades: tuple[CascadeEvent, ...],
    spikes: tuple[SpikeEvent, ...],
    *,
    temporal_bin_ms: float,
    excluded_unit_ids: tuple[int, ...],
    source_kind: str,
) -> tuple[Any, ...]:
    return patterns_from_step(
        cascades,
        spikes,
        temporal_bin_ms=temporal_bin_ms,
        excluded_unit_ids=excluded_unit_ids,
        source_kind=source_kind,
    )


def strongest(activations: list[Any]) -> Any | None:
    usable = [row for row in activations if row.mature and not row.suppressed]
    return max(
        usable,
        key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
        default=None,
    )


def run_arm(
    extractor: Callable[..., tuple[Any, ...]],
    cascades: tuple[CascadeEvent, ...],
    spikes: tuple[SpikeEvent, ...],
    contract: dict[str, Any],
) -> dict[str, Any]:
    family = contract["input_family"]
    kwargs = {
        "temporal_bin_ms": float(family["temporal_bin_ms"]),
        "excluded_unit_ids": tuple(int(value) for value in family["excluded_unit_ids"]),
        "source_kind": str(family["source_kind"]),
    }
    memory = TemporalAssemblyMemory(AssemblyConfig())
    predictor = AssemblyPredictor()
    target = contract["assembly_binding"]["predictor_training_target"]
    training_episodes = int(contract["assembly_binding"]["training_episodes"])
    last_patterns: tuple[Any, ...] = ()
    last_activation = None
    for index in range(1, training_episodes + 1):
        last_patterns = extractor(cascades, spikes, **kwargs)
        activations = []
        for pattern in last_patterns:
            activation = memory.observe(
                pattern,
                time_ms=pattern.end_ms,
                episode_id=f"train-{index}",
                learn=True,
            )
            if activation is not None:
                activations.append(activation)
        last_activation = strongest(activations)
        predictor.observe(last_activation, target)

    probe_patterns = extractor(cascades, spikes, **kwargs)
    probe_activations = []
    for pattern in probe_patterns:
        activation = memory.observe(
            pattern,
            time_ms=pattern.end_ms,
            episode_id="probe-4",
            learn=False,
        )
        if activation is not None:
            probe_activations.append(activation)
    probe_activation = strongest(probe_activations)
    prediction = predictor.predict(probe_activation)
    mature_present = any(
        candidate.episode_count >= memory.config.mature_episodes
        for candidate in memory.candidates.values()
    )
    return {
        "patterns": [
            {
                "ordered_units": list(pattern.ordered_units),
                "source_cascade_id": pattern.source_cascade_id,
                "spike_count": pattern.spike_count,
            }
            for pattern in probe_patterns
        ],
        "pattern_count": len(probe_patterns),
        "candidate_count": len(memory.candidates),
        "mature_activation_present": mature_present,
        "probe_prediction_value": prediction.value,
        "training_mature_activation_present": last_activation is not None,
    }


def same_joined_control(left: dict[str, Any], right: dict[str, Any]) -> bool:
    keys = (
        "patterns",
        "candidate_count",
        "mature_activation_present",
        "probe_prediction_value",
    )
    return all(left[key] == right[key] for key in keys)


def representation_diff(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["pattern_count"] != right["pattern_count"]
        or left["patterns"] != right["patterns"]
    )


def assembly_diff(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["candidate_count"] != right["candidate_count"]
        or left["mature_activation_present"] != right["mature_activation_present"]
    )


def map_outcome(
    contract: dict[str, Any],
    joined_current: dict[str, Any],
    joined_shadow: dict[str, Any],
    split_current: dict[str, Any],
    split_shadow: dict[str, Any],
    bindings_ok: bool,
) -> tuple[str, dict[str, bool]]:
    joined_ok = same_joined_control(joined_current, joined_shadow)
    rep_effect = representation_diff(split_current, split_shadow)
    asm_effect = assembly_diff(split_current, split_shadow)
    functional_effect = (
        split_current["probe_prediction_value"]
        != split_shadow["probe_prediction_value"]
    )
    facts = {
        "source_bindings_ok": bindings_ok,
        "joined_control_match": joined_ok,
        "representation_effect": rep_effect,
        "assembly_effect": asm_effect,
        "functional_effect": functional_effect,
    }
    if not bindings_ok or not joined_ok:
        return "INVALID_DIAGNOSTIC", facts
    explicit_hits = contract["supported_contract_scope"][
        "explicit_episode_global_crosscascade_contract_hits"
    ]
    if explicit_hits:
        return "EXPLICIT_EPISODE_GLOBAL_FALLBACK_CONTRACT", facts
    if (
        not rep_effect
        and split_current["pattern_count"] == 0
        and split_shadow["pattern_count"] == 0
    ):
        return "NO_SUPPORTED_RUNTIME_CONDITION", facts
    if rep_effect and asm_effect and functional_effect:
        return "FUNCTIONAL_CROSSCASCADE_SEGMENTATION_EFFECT", facts
    if (rep_effect or asm_effect) and not functional_effect:
        return "REPRESENTATION_ONLY_CROSSCASCADE_EFFECT", facts
    return "MIXED_OR_AMBIGUOUS_SEGMENTATION_CONTRACT", facts


def preflight(contract: dict[str, Any]) -> dict[str, Any]:
    checks = verify_bindings(contract)
    spikes, variants = materialize_family(contract)
    matched = set(variants) == {"split_sparse", "joined_control"} and len(spikes) == 4
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
        "source_blob_verification": checks,
        "all_source_bindings_ok": all(checks.values()),
        "matched_family_materialized": matched,
        "git_head": git("rev-parse", "HEAD"),
        "main_is_ancestor": ancestry,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    contract = load_contract()
    pre = preflight(contract)
    valid_preflight = (
        pre["all_source_bindings_ok"]
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

    spikes, variants = materialize_family(contract)
    joined_current = run_arm(
        current_extractor,
        variants["joined_control"],
        spikes,
        contract,
    )
    joined_shadow = run_arm(
        shadow_boundary_preserving,
        variants["joined_control"],
        spikes,
        contract,
    )
    split_current = run_arm(
        current_extractor,
        variants["split_sparse"],
        spikes,
        contract,
    )
    split_shadow = run_arm(
        shadow_boundary_preserving,
        variants["split_sparse"],
        spikes,
        contract,
    )
    outcome, decision_facts = map_outcome(
        contract,
        joined_current,
        joined_shadow,
        split_current,
        split_shadow,
        pre["all_source_bindings_ok"],
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
        "input_family_digest": input_digest,
        "comparator": contract["extractor_arms"],
        "observables": contract["observables"],
        "joined_control": {
            "episode_global_fallback": joined_current,
            "boundary_preserving_shadow": joined_shadow,
        },
        "split_sparse": {
            "episode_global_fallback": split_current,
            "boundary_preserving_shadow": split_shadow,
        },
        "decision_facts": decision_facts,
        "mapped_outcome": outcome,
        "git_head": pre["git_head"],
        "contract_sha256": contract_sha,
        "workflow_run_id": int(os.environ.get("GITHUB_RUN_ID", "0")),
        "stop_required": True,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.output_dir / "raw.json"
    raw_path.write_text(canonical(raw) + "\n", encoding="utf-8")
    raw_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
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
            "input_family_digest",
            "comparator",
            "observables",
            "joined_control",
            "split_sparse",
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
