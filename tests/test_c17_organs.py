from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from sparkbrain.release import release_mode
from sparkbrain.v03_organs.contracts import (
    canonical,
    digest,
    protocol_document,
    validate_resource_conditions,
)
from sparkbrain.v03_organs.discovery import (
    assess_proposal,
    discover_primary_candidate,
    select_control_memberships,
    select_controls,
)
from sparkbrain.v03_organs.worlds import fixture_document, fixture_hashes, fixture_manifest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def protocol():
    return protocol_document()


def _independent_fixture(run_seed: int, p: dict) -> dict:
    """Second stdlib-only construction; intentionally does not import C17 worlds."""

    def sha(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def ids(prefix: str, text: str) -> str:
        return prefix + sha(text)[:24]

    cells = []
    for cell_spec in p["resource_conditions"]["rows"]:
        condition_id, comp = cell_spec["condition_id"], cell_spec["task_compositionality"]
        splits = []
        for split_spec in p["fixtures"]["generation_contract"]["split_order"]:
            split, count, base = (
                split_spec["split"],
                split_spec["episode_count"],
                split_spec["split_seed_base"],
            )
            episodes = []
            for episode_index in range(count):
                f = episode_index % 4
                if comp == 2:
                    composition = [f, (f + (2 if split == "heldout" else 1)) % 4]
                else:
                    composition = [
                        f,
                        (f + (2 if split == "heldout" else 1)) % 4,
                        (f + (3 if split == "heldout" else 2)) % 4,
                    ]
                variant = f"composition{comp}"
                episode_id = ids(
                    "ep-", f"c17v2|episode|{run_seed}|{split}|{variant}|{episode_index}"
                )
                frames = []
                segment = 12 // comp
                for t in range(12):
                    local = t % segment
                    function = composition[t // segment]
                    bit = (run_seed + episode_index + function) % 2
                    entity = (episode_index + local) % 2
                    values = [0.0] * 12
                    if function == 0:
                        if local == 0:
                            values[bit] = 1.0
                        if local == segment - 1:
                            values[10] = 0.4
                    elif function == 1:
                        values[2 + (bit ^ entity)] = 1.0
                    elif function == 2:
                        observed = 1 - bit if local == segment - 2 else bit
                        values[4 + observed] = 1.0
                    else:
                        values[6 + ((bit + local) % 2)] = 1.0
                    values[8 + entity] = max(values[8 + entity], 0.35)
                    for j, value in enumerate(values):
                        if value:
                            preimage = (
                                f"c17v2|amplitude|{run_seed}|{split}|{variant}|"
                                f"{episode_index}|{t}|{j}"
                            )
                            uniform = int(sha(preimage)[:13], 16) / float(2**52)
                            values[j] = min(1.0, max(0.0, value + 0.02 * (2 * uniform - 1)))
                    frames.append(
                        {
                            "t": t,
                            "sample_id": ids("sa-", f"{episode_id}|frame|{t}"),
                            "source_id": ids("src-", f"{episode_id}|sensor"),
                            "correlation_group": ids("cg-", f"{episode_id}|stream"),
                            "base_values": values,
                            "evaluator_function_index": function,
                            "evaluator_entity_index": entity,
                            "evaluator_target_bit": bit,
                            "scoring": local == segment - 1,
                            "entity_key": ids("en-", f"{episode_id}|entity|{entity}"),
                            "hypothesis_ids": [
                                ids("hy-", f"{episode_id}|hypothesis|{b}") for b in (0, 1)
                            ],
                            "action_ids": [ids("ac-", f"{episode_id}|action|{b}") for b in (0, 1)],
                        }
                    )
                episodes.append(
                    {
                        "run_seed": run_seed,
                        "split": split,
                        "fixture_variant": variant,
                        "episode_index": episode_index,
                        "episode_seed": base
                        + 1000 * (run_seed - 4801)
                        + 100 * (comp - 2)
                        + episode_index,
                        "episode_id": episode_id,
                        "composition_indices": composition,
                        "frames": frames,
                    }
                )
            splits.append({"split": split, "episodes": episodes})
        cells.append({"condition_id": condition_id, "splits": splits})
    return {
        "schema_version": "0.3",
        "protocol_id": p["protocol_id"],
        "run_seed": run_seed,
        "cells": cells,
    }


def test_two_independent_pure_fixture_implementations_match_all_frozen_hashes(protocol):
    for seed in protocol["fixtures"]["run_seeds"]:
        first = fixture_document(seed, protocol)
        second = _independent_fixture(seed, protocol)
        assert canonical(first) == canonical(second)
        assert digest(first) == protocol["fixtures"]["fixture_sha256_by_run_seed"][str(seed)]
        assert (
            digest(fixture_manifest(seed, protocol))
            == protocol["fixtures"]["manifest_sha256_by_run_seed"][str(seed)]
        )
        assert fixture_hashes(seed, protocol) == (
            digest(second),
            digest(fixture_manifest(seed, protocol)),
        )


def test_fixture_schema_identity_and_cell_repetition(protocol):
    corpus = fixture_document(9901801, protocol)
    assert len(corpus["cells"]) == 5
    first = corpus["cells"][0]["splits"][0]["episodes"][0]
    assert set(first) == {
        "run_seed",
        "split",
        "fixture_variant",
        "episode_index",
        "episode_seed",
        "episode_id",
        "composition_indices",
        "frames",
    }
    assert set(first["frames"][0]) == set(
        protocol["fixtures"]["generation_contract"]["object_schemas"]["frame"]["exact_keys"]
    )
    for index in (1, 2, 3):
        repeated = corpus["cells"][index]["splits"][0]["episodes"][0]
        assert canonical(first) == canonical(repeated)
    assert corpus["cells"][4]["splits"][0]["episodes"][0]["fixture_variant"] == "composition3"


def test_resource_one_factor_validator_fails_closed(protocol):
    assert len(validate_resource_conditions(protocol)) == 5
    broken = copy.deepcopy(protocol)
    broken["resource_conditions"]["rows"][1]["workspace_capacity"] = 1
    with pytest.raises(ValueError, match="exactly one"):
        validate_resource_conditions(broken)


def _observations() -> list[dict]:
    rows = []
    for episode in range(12):
        for time in range(2):
            for candidate in ("a", "b", "c", "d", "e", "f"):
                rows.append(
                    {
                        "opaque_candidate_id": candidate,
                        "activation": 1.0,
                        "message_source_id": candidate,
                        "message_target_id": "b" if candidate == "a" else "a",
                        "message_weight": 1.0 if candidate in {"a", "b"} else 0.1,
                        "opaque_episode_id": f"opaque-{episode}",
                        "time": time,
                    }
                )
    return rows


def test_discovery_is_exact_schema_label_blind_deterministic_and_has_absence(protocol):
    rows = _observations()
    first = discover_primary_candidate(
        rows, protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )
    assert first == discover_primary_candidate(
        copy.deepcopy(rows), protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )
    assert {"a", "b"}.issubset(first["primary_candidate"]["member_ids"])
    leaked = copy.deepcopy(rows)
    leaked[0]["function"] = "renamed-label"
    with pytest.raises(ValueError, match="exact label-blind"):
        discover_primary_candidate(
            leaked, protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
        )
    absent = discover_primary_candidate(
        rows[:2], protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )
    assert absent["primary_candidate"] is None and absent["eligible_candidates"] == []


def test_all_five_controls_are_train_only_deterministic_and_exclude_target(protocol):
    controls = select_controls(
        _observations(), ["a", "b"], protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )
    assert list(controls) == protocol["controls"]["control_order"]
    assert all(
        value is not None and not {"a", "b"}.intersection(value) for value in controls.values()
    )
    assert controls == select_controls(
        _observations(), ["a", "b"], protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )


def test_control_type_sizes_and_selection_preimage_hashes(protocol):
    selections, memberships = select_control_memberships(
        _observations(),
        ["a", "b"],
        candidate_id="candidate",
        protocol=protocol,
        run_seed=9901801,
        condition_id="R0_baseline",
    )
    requested = 1 + int(
        hashlib.sha256(b"c17v2|control|9901801|R0_baseline").hexdigest()[:8], 16
    ) % 4
    assert len(selections["random_unmatched"]) == min(requested, 4)
    assert all(
        len(selections[name]) == 2 for name in protocol["controls"]["control_order"][1:]
    )
    assert [row["control_type"] for row in memberships] == protocol["controls"]["control_order"]
    assert all(
        row["status"] == "complete" and row["selection_input_sha256"]
        for row in memberships
    )


def test_c14_proposal_bytes_are_invariant_and_c15_cannot_create_one():
    proposal = {"coalition_id": "opaque", "members": ["a", "b"], "score": 0.75}
    before = canonical(proposal)
    for outcome in ("allow", "veto", "abstain"):
        result = assess_proposal(proposal, outcome)
        assert canonical(proposal) == before
        assert result["proposal_sha256"] == digest(proposal)
    assert assess_proposal(None, "allow")["assessment"] == "not_called"


def test_actual_c14_proposal_and_c15_v4_assessment_only_boundary(reserved_bundle):
    _, bundle = reserved_bundle
    checkpoint = bundle["structural_metrics.json"]["assessment_checkpoints"][0]
    rows = checkpoint["boundary_rows"]
    assert {(row["boundary"]["route"], row["boundary"]["assessment"]) for row in rows} == {
        ("proposal", "allow"),
        ("proposal", "veto"),
        ("proposal", "abstain"),
        ("none", "not_called"),
        ("rejection", "not_called"),
    }
    proposal_rows = [row["boundary"] for row in rows if row["boundary"]["route"] == "proposal"]
    assert all(row["c14_ignited"] for row in proposal_rows)
    assert all(row["replacement_possible"] is False for row in proposal_rows)


@pytest.fixture(scope="module")
def reserved_bundle(protocol):
    from sparkbrain.v03_organs.evaluation import generate_bundle, validate_bundle

    value = copy.deepcopy(protocol)
    value["fixtures"]["run_seeds"] = [9901801]
    value["statistics"]["bootstrap_resamples"] = 30
    bundle = generate_bundle(value, "a" * 40)
    validate_bundle(bundle, value, "a" * 40)
    return value, bundle


def test_reserved_bundle_exact_cardinality_restore_and_negative_science(reserved_bundle):
    _, bundle = reserved_bundle
    acceptance = bundle["acceptance_matrix.json"]
    assert acceptance["engineering_status"] == "implementation_failure"
    reproduction = next(
        row for row in acceptance["engineering_gates"] if row["gate_id"] == "reproduction_exact"
    )
    assert reproduction["passed"] is False
    assert acceptance["scientific_status"] in {"supported", "not_supported"}
    assert acceptance["cardinalities"] == {
        "candidate_discovery": 5,
        "structural_seed_split": 20,
        "selectivity_episode": 120,
        "functional_selectivity_seed": 5,
        "matched_episode_branch": 420,
        "heldout_episode_branch": 420,
        "heldout_seed": 5,
        "heldout_condition_aggregate": 5,
        "matched_control_membership": 25,
        "matched_seed_effect": 30,
        "matched_condition_aggregate_effect": 30,
        "resource_seed_counter": 5,
    }
    all_rows = (
        bundle["matched_ablations.json"]["episode_branch_rows"]
        + bundle["held_out_reuse.json"]["episode_branch_rows"]
    )
    assert all(
        row["restore_exact"] and row["state_hash_before"] == row["state_hash_after"]
        for row in all_rows
    )


def test_bundle_validator_recalculates_inventory_and_cardinality(reserved_bundle):
    from sparkbrain.v03_organs.evaluation import validate_bundle

    protocol, original = reserved_bundle
    broken = copy.deepcopy(original)
    broken["candidate_discovery.jsonl"].pop()
    broken["acceptance_matrix.json"]["cardinalities"]["candidate_discovery"] -= 1
    with pytest.raises(ValueError, match="cardinality"):
        validate_bundle(broken, protocol, "a" * 40)


def test_validator_rejects_control_preimage_and_dynamic_count_tamper(reserved_bundle):
    from sparkbrain.v03_organs.evaluation import validate_bundle

    protocol, original = reserved_bundle
    broken = copy.deepcopy(original)
    broken["matched_ablations.json"]["control_membership_rows"][0][
        "selection_input_sha256"
    ] = "0" * 64
    with pytest.raises(ValueError, match="controls"):
        validate_bundle(broken, protocol, "a" * 40)
    broken = copy.deepcopy(original)
    broken["candidate_discovery.jsonl"][0]["control_feasible_candidate_count"] += 1
    with pytest.raises(ValueError, match="discovery"):
        validate_bundle(broken, protocol, "a" * 40)
    broken = copy.deepcopy(original)
    broken["candidate_discovery.jsonl"][0]["candidate_count"] = True
    with pytest.raises(ValueError, match="integer, not bool"):
        validate_bundle(broken, protocol, "a" * 40)


def test_external_exact_nine_compare_is_only_reproduction_authority(reserved_bundle):
    from sparkbrain.v03_organs.evaluation import finalize_bundles, generate_bundle, validate_bundle

    protocol, prefinal = reserved_bundle
    with pytest.raises(TypeError):
        generate_bundle(protocol, "a" * 40, reproduction_exact=True)
    final = finalize_bundles(prefinal, copy.deepcopy(prefinal), protocol, "a" * 40)
    validate_bundle(final, protocol, "a" * 40)
    assert set(final) == set(protocol["artifacts"]["exact_files"])
    reproduction = next(
        row
        for row in final["acceptance_matrix.json"]["engineering_gates"]
        if row["gate_id"] == "reproduction_exact"
    )
    assert reproduction == {
        "gate_id": "reproduction_exact",
        "observed": True,
        "passed": True,
    }
    broken = copy.deepcopy(final)
    broken["reproduction_compare_manifest.json"]["runs"][0]["file_sha256"][
        "report.md"
    ] = "0" * 64
    with pytest.raises(ValueError, match="reproduction"):
        validate_bundle(broken, protocol, "a" * 40)


def test_resource_interventions_share_bank_but_change_evaluation(reserved_bundle):
    _, bundle = reserved_bundle
    rows = {row["condition_id"]: row for row in bundle["resource_conditions.json"]["seed_counters"]}
    assert len({row["assessment_checkpoint_sha256"] for row in rows.values()}) == 1
    assert (
        rows["R0_baseline"]["pre_resource_bank_sha256"]
        == rows["R2_bandwidth_low"]["pre_resource_bank_sha256"]
        == rows["R3_workspace_low"]["pre_resource_bank_sha256"]
    )
    assert (
        rows["R0_baseline"]["evaluation_behavior_sha256"]
        != rows["R2_bandwidth_low"]["evaluation_behavior_sha256"]
    )
    assert (
        rows["R0_baseline"]["evaluation_behavior_sha256"]
        != rows["R3_workspace_low"]["evaluation_behavior_sha256"]
    )


def test_checkpoint_uses_disjoint_r0_train_dev_and_is_artifact_verifiable(reserved_bundle):
    _, bundle = reserved_bundle
    checkpoint = bundle["structural_metrics.json"]["assessment_checkpoints"][0]
    assert (
        checkpoint["training_condition_id"]
        == checkpoint["selection_condition_id"]
        == "R0_baseline"
    )
    assert checkpoint["training_split"] == "train"
    assert checkpoint["selection_split"] == "dev_selection"
    assert checkpoint["calibration_split"] == "dev_calibration"
    assert checkpoint["dev_partition_rule"] == "episode_index_even_selection_odd_calibration"
    selection = set(checkpoint["selection_episode_ids"])
    calibration = set(checkpoint["calibration_episode_ids"])
    assert not selection & calibration
    assert not set(checkpoint["training_episode_ids"]) & (selection | calibration)
    assert len(checkpoint["candidate_checkpoints"]) == 3
    assert {row["epoch"] for row in checkpoint["candidate_checkpoints"]} == {2, 4, 6}
    assert all(
        row["state"] and len(row["sha256"]) == 64
        for row in checkpoint["candidate_checkpoints"]
    )
    assert checkpoint["selected_epoch"] in {2, 4, 6}
    assert checkpoint["selection_raw_rows"]
    assert checkpoint["calibration_raw_rows"]
    assert len(checkpoint["calibration_scores"]) == 9


@pytest.mark.parametrize(
    "tamper",
    [
        "candidate_state",
        "selection_raw",
        "checkpoint_score",
        "calibration_raw",
        "calibration_score",
        "partition_hash",
    ],
)
def test_checkpoint_validator_rejects_micro_tamper(reserved_bundle, tamper):
    from sparkbrain.v03_organs.evaluation import validate_bundle

    protocol, original = reserved_bundle
    broken = copy.deepcopy(original)
    checkpoint = broken["structural_metrics.json"]["assessment_checkpoints"][0]
    if tamper == "candidate_state":
        checkpoint["candidate_checkpoints"][0]["state"]["abstention_head.bias"][0] += 1e-7
    elif tamper == "selection_raw":
        checkpoint["selection_raw_rows"][0]["weighted_objective_total"] += 1e-12
    elif tamper == "checkpoint_score":
        checkpoint["checkpoint_scores"][0]["weighted_objective_total"] += 1e-12
    elif tamper == "calibration_raw":
        checkpoint["calibration_raw_rows"][0]["belief_squared_error"] += 1e-12
    elif tamper == "calibration_score":
        checkpoint["calibration_scores"][0]["belief_brier"] += 1e-12
    else:
        checkpoint["selection_episode_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="raw evidence"):
        validate_bundle(broken, protocol, "a" * 40)


@pytest.mark.skipif(
    release_mode(ROOT) == "archive",
    reason="C17 v1 source-commit hash pins require the retained stage checkout",
)
def test_candidate_absence_is_engineering_success_and_scientific_negative(
    protocol, monkeypatch
):
    from sparkbrain.v03_organs import evaluation

    original = evaluation.discover_primary_candidate

    def absent(*args, **kwargs):
        row = original(*args, **kwargs)
        return {
            **row,
            "absence_reason": "no_activity_eligible_candidate",
            "activity_eligible_candidate_count": 0,
            "control_feasible_candidate_count": 0,
            "infeasible_control_pool_candidate_count": 0,
            "primary_candidate": None,
            "eligible_candidates": [],
        }

    monkeypatch.setattr(evaluation, "discover_primary_candidate", absent)
    value = copy.deepcopy(protocol)
    value["fixtures"]["run_seeds"] = [9901801]
    value["statistics"]["bootstrap_resamples"] = 5
    value["runner_execution_allowed"] = True
    value["base_commit"] = "b" * 40
    value["base_sha256"] = "c" * 64
    value["source_commit"] = "a" * 40
    prefinal = evaluation.generate_bundle(value, "a" * 40)
    bundle = evaluation.finalize_bundles(
        prefinal, copy.deepcopy(prefinal), value, "a" * 40
    )
    acceptance = bundle["acceptance_matrix.json"]
    assert acceptance["engineering_status"] == "accepted", [
        row for row in acceptance["engineering_gates"] if not row["passed"]
    ]
    assert acceptance["scientific_status"] == "not_supported"
    assert acceptance["failed_seeds"] == []
    assert all(row["primary_candidate"] is None for row in bundle["candidate_discovery.jsonl"])
    assert all(
        row["member_ids"] is None and row["complete"] is False
        for row in bundle["matched_ablations.json"]["control_membership_rows"]
    )


def test_cross_seed_consistency_counts_same_locked_function(protocol):
    from sparkbrain.v03_organs.evaluation import _apply_seed_consistency

    cells = [
        {
            "run_seed": seed,
            "condition_id": "R0_baseline",
            "target_function_index": function,
            "local_gates_except_seed_consistency": True,
        }
        for seed, function in ((1, 2), (2, 2), (3, 2), (4, 1), (5, 1))
    ]
    gates = [
        {
            "run_seed": row["run_seed"],
            "condition_id": "R0_baseline",
            "gate_id": "seed_consistency",
            "passed": False,
        }
        for row in cells
    ]
    value = copy.deepcopy(protocol)
    value["resource_conditions"]["condition_order"] = ["R0_baseline"]
    result = _apply_seed_consistency(cells, gates, value)
    assert result["R0_baseline"]["function_index"] == 2
    assert result["R0_baseline"]["qualifying_seed_count"] == 3
    assert [row["passed"] for row in gates] == [True, True, True, False, False]


def test_hierarchical_bootstrap_inventory_and_registered_bounds(reserved_bundle):
    protocol, bundle = reserved_bundle
    intervals = bundle["matched_ablations.json"]["bootstrap_intervals"]
    assert set(intervals) == {
        "held_out_reuse",
        "targeted_impairment",
        *(f"control_margin:{name}" for name in protocol["controls"]["control_order"]),
        "unrelated_collateral",
    }
    assert all(row["resamples"] == 30 for row in intervals.values())
    assert all(
        row["bootstrap_seed"] == protocol["statistics"]["bootstrap_seed"]
        for row in intervals.values()
    )


def test_discovery_final_tie_break_is_single_member_list_hash(protocol):
    import itertools

    rows = _observations()
    for row in rows:
        row["message_source_id"] = None
        row["message_target_id"] = None
        row["message_weight"] = 0.0
    result = discover_primary_candidate(
        rows, protocol=protocol, run_seed=9901801, condition_id="R0_baseline"
    )
    pairs = list(itertools.combinations(sorted("abcdef"), 2))
    expected = min(
        pairs,
        key=lambda members: hashlib.sha256(canonical(list(members)).encode()).hexdigest(),
    )
    assert result["primary_candidate"]["member_ids"] == list(expected)


@pytest.mark.parametrize(
    "tamper,match",
    [
        ("metric", "effects"),
        ("bootstrap", "bootstrap"),
        ("science_gate", "scientific gates"),
        ("engineering_gate", "engineering gates"),
        ("checkpoint", "raw evidence"),
    ],
)
def test_validator_rejects_metric_and_gate_tamper(reserved_bundle, tamper, match):
    from sparkbrain.v03_organs.evaluation import validate_bundle

    protocol, original = reserved_bundle
    broken = copy.deepcopy(original)
    if tamper == "metric":
        broken["matched_ablations.json"]["seed_effect_rows"][0]["impairment"] = 1.0
    elif tamper == "bootstrap":
        broken["matched_ablations.json"]["bootstrap_intervals"]["held_out_reuse"]["effect"] = 1.0
    elif tamper == "science_gate":
        broken["acceptance_matrix.json"]["primary_scientific_gates"][0]["passed"] ^= True
    else:
        if tamper == "engineering_gate":
            broken["acceptance_matrix.json"]["engineering_gates"][0]["passed"] ^= True
        else:
            broken["structural_metrics.json"]["assessment_checkpoints"][0][
                "checkpoint_sha256"
            ] = "0" * 64
    with pytest.raises(ValueError, match=match):
        validate_bundle(broken, protocol, "a" * 40)
