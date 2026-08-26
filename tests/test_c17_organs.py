from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from sparkbrain.v03_organs.contracts import (
    canonical,
    digest,
    protocol_document,
    validate_resource_conditions,
)
from sparkbrain.v03_organs.discovery import (
    assess_proposal,
    discover_primary_candidate,
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
    for cell_spec in p["fixtures"]["generation_contract"]["constants_and_array_order"][
        "cell_order"
    ]:
        condition_id, comp = cell_spec["condition_id"], cell_spec["compositionality"]
        splits = []
        for split_spec in p["fixtures"]["generation_contract"]["constants_and_array_order"][
            "split_order"
        ]:
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
                episode_id = ids("ep-", f"c17|episode|{run_seed}|{split}|{variant}|{episode_index}")
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
                                f"c17|amplitude|{run_seed}|{split}|{variant}|"
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
                        + 1000 * (run_seed - 4701)
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
    corpus = fixture_document(9901701, protocol)
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
        rows, protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
    )
    assert first == discover_primary_candidate(
        copy.deepcopy(rows), protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
    )
    assert {"a", "b"}.issubset(first["primary_candidate"]["member_ids"])
    leaked = copy.deepcopy(rows)
    leaked[0]["function"] = "renamed-label"
    with pytest.raises(ValueError, match="exact label-blind"):
        discover_primary_candidate(
            leaked, protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
        )
    absent = discover_primary_candidate(
        rows[:2], protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
    )
    assert absent["primary_candidate"] is None and absent["eligible_candidates"] == []


def test_all_five_controls_are_train_only_deterministic_and_exclude_target(protocol):
    controls = select_controls(
        _observations(), ["a", "b"], protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
    )
    assert list(controls) == protocol["controls"]["control_order"]
    assert all(
        value is not None and not {"a", "b"}.intersection(value) for value in controls.values()
    )
    assert controls == select_controls(
        _observations(), ["a", "b"], protocol=protocol, run_seed=9901701, condition_id="R0_baseline"
    )


def test_c14_proposal_bytes_are_invariant_and_c15_cannot_create_one():
    proposal = {"coalition_id": "opaque", "members": ["a", "b"], "score": 0.75}
    before = canonical(proposal)
    for outcome in ("allow", "veto", "abstain"):
        result = assess_proposal(proposal, outcome)
        assert canonical(proposal) == before
        assert result["proposal_sha256"] == digest(proposal)
    assert assess_proposal(None, "allow")["assessment"] == "not_called"


@pytest.fixture(scope="module")
def reserved_bundle(protocol):
    from sparkbrain.v03_organs.evaluation import generate_bundle, validate_bundle

    value = copy.deepcopy(protocol)
    value["fixtures"]["run_seeds"] = [9901701]
    value["statistics"]["bootstrap_resamples"] = 30
    bundle = generate_bundle(value, "a" * 40)
    validate_bundle(bundle, value, "a" * 40)
    return value, bundle


def test_reserved_bundle_exact_cardinality_restore_and_negative_science(reserved_bundle):
    _, bundle = reserved_bundle
    acceptance = bundle["acceptance_matrix.json"]
    assert acceptance["engineering_status"] == "accepted"
    assert acceptance["scientific_status"] in {"supported", "not_supported"}
    assert acceptance["cardinalities"] == {
        "candidate_discovery": 5,
        "structural_seed_split": 20,
        "selectivity_episode": 120,
        "matched_episode_branch": 420,
        "heldout_episode_branch": 420,
        "matched_control_membership": 25,
        "matched_seed_effect": 30,
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
