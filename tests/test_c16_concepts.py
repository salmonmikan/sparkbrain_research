"""Reserved synthetic C16 tests; official seeds are used for pure hashes only."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import numpy as np
import pytest

from sparkbrain.v03_concepts.bank import ConceptBank, build_controls, cosine
from sparkbrain.v03_concepts.learning import encode, fit_encoder, fit_readout, normalize, predict
from sparkbrain.v03_concepts.worlds import (
    canonical,
    digest,
    fixture,
    protocol_document,
    sensory_episode,
    split_manifest,
    text_hash,
    variant_values,
)


@pytest.fixture
def protocol():
    return protocol_document()


def _x(*coordinates):
    result = [0.0] * 12
    for index in coordinates:
        result[index] = 1.0
    return result


def _bank(protocol, representation="online_prototype", **kwargs):
    return ConceptBank(protocol, 99016, representation, "canonical", **kwargs)


def _exemplar(index, x):
    return {
        "observation_id": f"reserved-{index:04}",
        "global_frame_index": index,
        "feature_ids": [f"local_numeric:ch{j:02}" for j, value in enumerate(x) if value],
        "emitted_vector": x,
        "representation": normalize(x),
    }


def test_official_fixture_hashes_are_pure_and_exact(protocol):
    for seed in protocol["seeds"]["run_seeds"]:
        for split in ("train", "dev", "test"):
            document = fixture(seed, split, protocol)
            manifest = split_manifest(seed, split, protocol)
            assert (
                digest(document)
                == protocol["seeds"]["full_fixture_sha256_by_run_seed_and_split"][str(seed)][split]
            )
            assert (
                digest(manifest)
                == protocol["seeds"]["manifest_sha256_by_run_seed_and_split"][str(seed)][split]
            )
            assert len(document["episodes"]) == (32 if split == "train" else 16)
            assert all(len(row["frames"]) == 9 for row in document["episodes"])


def test_reserved_fixture_names_do_not_leak_into_sensory(protocol):
    episode = fixture(99016, "train", protocol)["episodes"][0]
    renamed = copy.deepcopy(episode)
    renamed["world"] = "evaluator-only-rename"
    for frame in renamed["frames"]:
        frame["context"] = 999
        frame["phase"] = 777
    first = sensory_episode(episode, "base", protocol)
    second = sensory_episode(renamed, "base", protocol)
    for left, right in zip(first, second, strict=True):
        assert {k: v for k, v in left.items() if k != "context"} == {
            k: v for k, v in right.items() if k != "context"
        }
        assert len(left["sensory_trace"]) == 12
        assert sum(left["emitted_mask"]) <= 8
        assert left["sensory_work"]["channels_inspected"] == 12
        assert left["sensory_work"]["sparks_emitted"] == len(left["perceptual_spark_ids"])
        assert left["parent_sample_ids"] in ([], [left["sample_id"]])
        for index, accepted in enumerate(left["emitted_mask"]):
            assert left["emitted_vector"][index] == (
                left["input_values"][index] if accepted else 0.0
            )


def test_sensory_future_suffix_and_episode_reset(protocol):
    episode = fixture(99016, "train", protocol)["episodes"][0]
    changed = copy.deepcopy(episode)
    changed["frames"][6]["base_values"] = _x(8, 9)
    first = sensory_episode(episode, "base", protocol)
    assert first[:6] == sensory_episode(changed, "base", protocol)[:6]
    assert first == sensory_episode(episode, "base", protocol)
    quiet = copy.deepcopy(episode)
    for frame in quiet["frames"]:
        frame["base_values"] = _x()
    assert all(row["emitted_vector"] == _x() for row in sensory_episode(quiet, "base", protocol))


def test_variants_preserve_base_and_order_and_targets(protocol):
    episode = fixture(99016, "test", protocol)["episodes"][0]
    before = canonical(episode)
    for frame in episode["frames"]:
        assert variant_values(frame, "base") == variant_values(frame, "order_shuffle")
        perturbed = variant_values(frame, "amplitude_perturbation")
        assert all(0 <= value <= 1 for value in perturbed)
        assert all(perturbed[j] == 0 for j, value in enumerate(frame["base_values"]) if value == 0)
        distracted = variant_values(frame, "irrelevant_distractor")
        changed = [j for j in range(12) if distracted[j] != frame["base_values"][j]]
        assert len(changed) == 1 and changed[0] in (9, 10, 11)
    assert canonical(episode) == before


@pytest.mark.parametrize("representation", ["cc0_assembly", "online_prototype"])
def test_identity_exact_noop_changed_content_and_registry_bound(protocol, representation):
    bank = _bank(protocol, representation)
    bank.observe(_x(0, 1), "ob-unique")
    before = bank.hash()
    duplicate = bank.observe(_x(0, 1), "ob-unique")
    assert duplicate["no_match_reason"] == "duplicate_ignored"
    assert duplicate["winner_id"] is None and duplicate["events"] == []
    assert bank.hash() == before
    with pytest.raises(ValueError, match="changed vector"):
        bank.observe(_x(2, 3), "ob-unique")
    assert bank.hash() == before
    for i in range(287):
        bank.observe(_x(), f"quiet-{i}")
    before = bank.hash()
    with pytest.raises(ValueError, match="registry exhausted"):
        bank.observe(_x(), "overflow")
    assert bank.hash() == before and len(bank.state()["seen_observations"]) == 288


@pytest.mark.parametrize(
    "bad",
    [
        [True] + [0.0] * 11,
        [float("nan")] * 12,
        [float("inf")] * 12,
        [-0.1] * 12,
        [1.1] * 12,
        [0.0] * 11,
        ["0"] * 12,
    ],
)
def test_invalid_vectors_rejected_before_mutation(protocol, bad):
    bank = _bank(protocol)
    before = bank.hash()
    with pytest.raises(ValueError):
        bank.observe(bad, "identity")
    assert bank.hash() == before


@pytest.mark.parametrize("bad", [None, True, 3, "", "  "])
def test_invalid_identity_rejected_before_mutation(protocol, bad):
    bank = _bank(protocol)
    before = bank.hash()
    with pytest.raises(ValueError):
        bank.observe(_x(1), bad)
    assert bank.hash() == before


def test_prototype_update_usage_ema_and_retained_window(protocol):
    bank = _bank(protocol)
    first = bank.observe(_x(0, 1), "first")
    key = first["winner_id"]
    x = _x(0, 1)
    x[2] = 0.2
    bank.observe(x, "second")
    candidate = bank.state()["live_candidates"][0]
    assert candidate["usage"] == 0.05
    assert candidate["prototype"] == normalize(
        0.9 * np.asarray(normalize(_x(0, 1))) + 0.1 * np.asarray(normalize(x))
    )
    assert candidate["member_feature_ids"] == [f"local_numeric:ch{j:02}" for j in (0, 1, 2)]
    for i in range(40):
        assert bank.observe(_x(0, 1), f"later-{i}")["winner_id"] == key
    candidate = bank.state()["live_candidates"][0]
    assert len(candidate["retained_exemplars"]) == 32
    assert candidate["retained_exemplars"][0]["global_frame_index"] == 10
    assert "local_numeric:ch02" not in candidate["member_feature_ids"]


def test_inactivity_delete_and_awaken_boundaries(protocol):
    bank = _bank(protocol)
    key = bank.observe(_x(0), "first")["winner_id"]
    for i in range(1, 16):
        bank.observe(_x(), f"idle-{i}")
    row = bank.observe(_x(0), "at16")
    assert row["winner_id"] == key
    assert [event["operation"] for event in row["events"]] == ["dormant", "awaken", "update"]
    for i in range(17, 48):
        bank.observe(_x(), f"idle-{i}")
    row = bank.observe(_x(0), "at48")
    assert row["winner_id"] != key
    assert [event["operation"] for event in row["events"]] == ["delete", "birth"]
    assert bank.state()["retired_candidates"][0]["candidate_id"] == key


def test_top1_tie_slot_freeze_and_exclusion_are_state_neutral(protocol):
    bank = _bank(protocol)
    x = _x(0, 1)
    for i in range(2):
        bank._birth(normalize(x), [_exemplar(i, x)], i)
    bank.freeze()
    before = bank.hash()
    slots = bank.slot_candidate_ids
    assert len(slots) == 8 and slots[:2] == sorted(slots[:2]) and slots[2:] == [None] * 6
    assert bank.query(x)["winner_id"] == slots[0]
    assert bank.query(x, exclude_id=slots[0])["winner_id"] == slots[1]
    assert bank.query(x)["winner_id"] == slots[0]
    slots[0] = "external-mutation"
    state = bank.state()
    state["live_candidates"][0]["usage"] = 99
    assert bank.hash() == before
    with pytest.raises(ValueError, match="cannot observe"):
        bank.observe(x, "frozen")


def test_capacity_birth_budget_and_quiet_no_force(protocol):
    bank = _bank(protocol)
    assert bank.observe(_x(), "quiet")["winner_id"] is None
    for i in range(8):
        assert bank.observe(_x(i), f"birth-{i}")["winner_id"] is not None
    row = bank.observe(_x(8), "capacity")
    assert row["winner_id"] is None and row["no_match_reason"] == "capacity"
    assert len(bank.state()["live_candidates"]) == 8
    budget = _bank(protocol)
    budget._births = 32
    row = budget.observe(_x(0), "budget")
    assert row["no_match_reason"] == "birth_budget" and budget._births == 32


def test_split_exact_children_pivot_tie_and_atomic_budget(protocol):
    bank = _bank(protocol)
    rows = [_exemplar(i, _x(0) if i < 4 else _x(1)) for i in range(8)]
    parent = bank._birth(normalize(_x(0, 1)), rows, 0, usage=0.4)
    events = []
    operated = bank._split(set(bank._live), 8, events)
    assert operated == {parent["candidate_id"]}
    assert len(bank._live) == 2 and len(bank._retired) == 1
    assert [row["operation"] for row in events] == ["split", "split"]
    assert all(row["candidate_count_after"] == 2 for row in events)
    assert all(row["usage"] == 0.2 and row["first_seen"] == 8 for row in bank._live.values())
    assert [row["prototype"] for row in bank._live.values()] == [normalize(_x(0)), normalize(_x(1))]
    assert all(row["parent_ids"] == [parent["candidate_id"]] for row in bank._live.values())
    rejected = _bank(protocol)
    rejected._birth(normalize(_x(0, 1)), rows, 0, usage=0.4)
    rejected._births = 31
    before, events = rejected.hash(), []
    rejected._split(set(rejected._live), 8, events)
    assert rejected.hash() == before and events[0]["reason"] == "birth_budget"


def test_merge_complete_link_before_window_truncation_and_atomic_budget(protocol):
    bank = _bank(protocol)
    common, outlier = _x(0), _x(1)
    left_rows = [_exemplar(0, outlier)] + [_exemplar(i, common) for i in range(1, 32)]
    right_rows = [_exemplar(i, common) for i in range(32, 64)]
    bank._birth(normalize(common), left_rows, 0)
    bank._birth(normalize(common), right_rows, 32)
    before, events = bank.hash(), []
    bank._merge(set(bank._live), set(), 64, events)
    assert bank.hash() == before and events[0]["reason"] == "complete_link"
    assert cosine(normalize(common), normalize(outlier)) < 0.8
    valid = _bank(protocol)
    valid._birth(normalize(common), [_exemplar(i, common) for i in range(32)], 0, usage=0.7)
    valid._birth(normalize(common), right_rows, 32, usage=0.6)
    before_ids = sorted(valid._live)
    events = []
    valid._merge(set(valid._live), set(), 64, events)
    child = next(iter(valid._live.values()))
    assert child["usage"] == 1.0 and child["parent_ids"] == before_ids
    assert [r["global_frame_index"] for r in child["retained_exemplars"]] == list(range(32, 64))
    assert len(valid._retired) == 2 and events[0]["births_consumed"] == 1


def test_observation_winner_is_not_transferred_on_same_frame_merge(protocol):
    bank = _bank(protocol)
    x = _x(0)
    for i in range(2):
        bank._birth(normalize(x), [_exemplar(i, x)], 0)
    expected = min(bank._live)
    result = bank.observe(x, "current")
    assert result["winner_id"] == expected and expected in bank._retired
    assert result["events"][-1]["operation"] == "merge"
    assert result["winner_id"] != result["events"][-1]["candidate_id"]


def test_immutable_cc0_adapter_and_supported_noops(protocol):
    bank = _bank(protocol, "cc0_assembly")
    for i in range(3):
        row = bank.observe(_x(0, 1), f"cc0-{i}")
    assert row["winner_id"] is not None
    for i in range(40):
        row = bank.observe(_x(), f"cc0-quiet-{i}")
        assert not {event["operation"] for event in row["events"]}.intersection(
            {"merge", "split", "dormant", "delete"}
        )
    assert len(bank.state()["live_candidates"]) == 1
    assert bank.state()["cc0_source_state"]["feature_counts"]["local_numeric:ch00"] == 3
    path = Path(__file__).resolve().parents[1] / "src/sparkbrain/v03_seed/concepts.py"
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest()
        == protocol["source_control"]["protected_hash_manifest"][
            "src/sparkbrain/v03_seed/concepts.py"
        ]
    )


def test_controls_exact_rank_count_usage_and_no_label_reading(protocol):
    primary = _bank(protocol)
    frames = [
        {"episode_id": f"opaque-{i // 9}", "emitted_vector": _x(i % 3), "sample_id": f"sample-{i}"}
        for i in range(288)
    ]
    for frame in frames:
        primary.observe(frame["emitted_vector"], frame["sample_id"])
    primary.freeze()
    banks, construction = build_controls(primary, frames)
    renamed = [{**frame, "world": "evaluator-irrelevant", "target": [99] * 12} for frame in frames]
    _, same = build_controls(primary, renamed)
    assert construction == same
    assert set(construction) == set(protocol["schemas"]["control_construction"])
    inventory = construction["pattern_inventory"]
    for item in inventory:
        assert set(item) == set(protocol["schemas"]["pattern_inventory_item"])
        assert item["frame_count"] == 96 and item["distinct_episode_count"] == 32
    for row in construction["reference_banks"]:
        bank = banks[row["bank_kind"]]
        assert row["reference_count"] == row["primary_count"] == 3 and row["shortfall"] == 0
        assert bank.state()["accepted_observation_count"] == 0
        assert bank.state()["seen_observations"] == []
        assert row["bank_hash"] == bank.hash()
        assert all(candidate["grade"] is None for candidate in row["references"])
        with pytest.raises(ValueError, match="cannot observe"):
            bank.observe(_x(0), "control-no-mutation")
    frequency = construction["reference_banks"][1]
    assert frequency["selection_order_pattern_ids"] == sorted(r["pattern_id"] for r in inventory)
    random = construction["reference_banks"][0]
    assert random["selection_order_pattern_ids"] == sorted(
        [r["pattern_id"] for r in inventory],
        key=lambda pid: (text_hash(f"c16|random|99016|online_prototype|canonical|{pid}"), pid),
    )


def test_control_shortfall_never_fabricates_patterns(protocol):
    bank = _bank(protocol)
    bank.observe(_x(0), "one")
    bank.observe(_x(1), "two")
    bank.freeze()
    frames = [{"episode_id": f"opaque-{i // 9}", "emitted_vector": _x(0)} for i in range(288)]
    _, row = build_controls(bank, frames)
    assert all(
        item["reference_count"] == 1 and item["shortfall"] == 1 for item in row["reference_banks"]
    )


def test_control_mean_preserves_zero_direction_frames_and_boundary(protocol, monkeypatch):
    bank = _bank(protocol)
    bank.observe(_x(0), "one")
    bank.freeze()
    frames = [{"episode_id": f"opaque-{i // 9}", "emitted_vector": _x(0)} for i in range(288)]
    # Two near-cancelling unit directions and286 absent directions share the same mask.
    # Their full-group mean norm falls below1e-12; dropping absent rows would exceed it.
    epsilon = 1e-10
    counter = iter(
        [normalize([1.0, epsilon] + [0.0] * 10), normalize([-1.0, epsilon] + [0.0] * 10)]
        + [None] * 286
    )
    monkeypatch.setattr(bank, "_representation", lambda x: next(counter))
    _, construction = build_controls(bank, frames)
    assert construction["pattern_inventory"][0]["mean_representation"] is None
    assert construction["pattern_inventory"][0]["eligible"] is False
    assert all(row["shortfall"] == 1 for row in construction["reference_banks"])


def test_tied_linear_encoder_deterministic_48_parameters_twenty_steps(protocol):
    vectors = [_x(i % 3, i % 3 + 3) for i in range(288)]
    checkpoint = fit_encoder(vectors, 99016)
    assert checkpoint == fit_encoder(vectors, 99016)
    assert set(checkpoint) == set(protocol["schemas"]["checkpoint_record"])
    assert checkpoint["parameter_count"] == 48 and checkpoint["optimizer_steps"] == 20
    assert len(checkpoint["epoch_losses"]) == 20 and set(checkpoint["weights"]) == {"W"}
    assert checkpoint["training_input_hash"] == digest(vectors)
    assert checkpoint["checkpoint_hash"] == digest(
        {k: v for k, v in checkpoint.items() if k != "checkpoint_hash"}
    )
    assert len(encode(vectors[0], checkpoint)) == 4
    assert encode(_x(), checkpoint) is None
    assert encode(_x()) is None
    bank = _bank(protocol, "learned_local_prototype", encoder=checkpoint)
    assert len(bank.observe(vectors[0], "latent")["representation_vector"]) == 4
    assert len(normalize(_x(0))) == 12


def test_ridge_exact_closed_form_intercept_only_and_clip():
    queries = [{"slot_index": None}] * 256
    targets = [[0.25] * 12] * 256
    coefficients = fit_readout(queries, targets)
    assert coefficients == [[0.25] * 12] + [[0.0] * 12] * 8
    raw, clipped = predict(coefficients, None)
    assert raw == clipped == [0.25] * 12
    queries = [{"slot_index": i % 2} for i in range(256)]
    targets = [_x(i % 2) for i in range(256)]
    coefficients = np.asarray(fit_readout(queries, targets))
    phi = np.zeros((256, 9))
    phi[:, 0] = 1
    for i in range(256):
        phi[i, 1 + i % 2] = 1
    expected = np.linalg.solve(
        phi.T @ phi + np.diag([0.0] + [0.1] * 8), phi.T @ np.asarray(targets)
    )
    assert np.array_equal(coefficients, expected)
    extreme = [[2.0] * 12] + [[0.0] * 12] * 8
    assert predict(extreme, None) == ([2.0] * 12, [1.0] * 12)
    with pytest.raises(ValueError, match="exactly256"):
        fit_readout([], [])


def test_bank_exact_nested_schema_and_lineage_parent_order(protocol):
    bank = _bank(protocol)
    for i in range(4):
        result = bank.observe(_x(i % 2), f"schema-{i}")
        for event in result["events"]:
            assert set(event) == set(protocol["schemas"]["lineage_event"])
    state = bank.state()
    assert set(state) == set(protocol["schemas"]["bank_final_state"])
    assert set(state["bank"]) == set(protocol["schemas"]["bank_identity"])
    for candidate in bank.candidates():
        assert set(candidate) == set(protocol["schemas"]["candidate_state"])
        for row in candidate["retained_exemplars"]:
            assert set(row) == set(protocol["schemas"]["exemplar_state"])
    assert canonical(state) == canonical(copy.deepcopy(state))


def test_perceptual_registry_hash_commits_sample_and_spark_registration(protocol):
    from sparkbrain.v03_seed.evidence import EvidenceLedger

    episode = fixture(99016, "train", protocol)["episodes"][0]
    frames = sensory_episode(episode, "base", protocol)
    ledger = EvidenceLedger()
    hashes = []
    for frame in frames:
        ledger.register_sample(frame["sample_id"])
        for spark_id in frame["perceptual_spark_ids"]:
            ledger.register_spark(spark_id, (frame["sample_id"],))
        expected = hashlib.sha256(ledger.serialize_state().encode("utf-8")).hexdigest()
        assert frame["lineage_registry_hash"] == expected
        hashes.append(expected)
    assert len(set(hashes)) == 9


def _grade_case(protocol, seed=99016, *, count=8, recurrence=3, shortfall=0):
    # Numerical grader fixtures only; no model/sensory execution or official data.
    cid = f"candidate-{seed}"
    state = {
        "candidate_id": cid,
        "birth_ordinal": 0,
        "status": "active",
        "parent_ids": [],
        "member_feature_ids": [],
        "retained_exemplars": [],
    }
    bank = {
        "bank": dict(
            run_seed=seed,
            representation="online_prototype",
            bank_kind="primary",
            discovery_order="canonical",
        ),
        "final_state": {"live_candidates": [state], "retired_candidates": []},
        "candidates": [],
    }
    lineage = []
    for i in range(recurrence):
        eid = "ep-" + text_hash(f"c16|episode|{seed}|train|recurrence|{i}")[:24]
        lineage.append(
            dict(
                row_kind="episode",
                run_seed=seed,
                representation="online_prototype",
                discovery_order="canonical",
                world="recurrence",
                episode_id=eid,
                frames=[dict(winner_id=cid, frame_index=0)],
            )
        )
    lineage.append(
        dict(
            row_kind="control",
            run_seed=seed,
            representation="online_prototype",
            discovery_order="canonical",
            reference_banks=[{"shortfall": shortfall}, {"shortfall": 0}],
        )
    )
    utility = []
    for variant in ("base", "amplitude_perturbation", "irrelevant_distractor"):
        for kind, error in (("primary", 1.2), ("matched_random", 1.44), ("frequency_topk", 1.56)):
            for episode_index in range(2):
                steps = [
                    dict(
                        t=t,
                        winner_id=cid if 4 * episode_index + t < count else "other",
                        context=t % 2,
                        squared_error_sum=error,
                    )
                    for t in range(4)
                ]
                utility.append(
                    dict(
                        run_seed=seed,
                        split="test",
                        variant=variant,
                        cell=f"online_prototype/{kind}",
                        episode_id=f"test-{episode_index}",
                        steps=steps,
                    )
                )
    causal = []
    for world in protocol["world_generator"]["world_order"]:
        causal.append(
            dict(
                run_seed=seed,
                representation="online_prototype",
                candidate_id=cid,
                world=world,
                target_world="recurrence",
                comparator_id="comparator",
                restore_exact=True,
                baseline=dict(mse=0.1, squared_error_sum=9.6, denominator=96),
                targeted_suppression=dict(
                    mse=0.16 if world == "recurrence" else 0.11,
                    squared_error_sum=15.36 if world == "recurrence" else 10.56,
                    denominator=96,
                ),
                matched_random_suppression=dict(mse=0.12, squared_error_sum=11.52, denominator=96),
            )
        )
    return [bank], lineage, utility, causal


def _grade(protocol, **kwargs):
    from sparkbrain.v03_concepts.evaluation import candidate_metrics

    data = _grade_case(protocol, **kwargs)
    return candidate_metrics(*data, protocol, [])[0]["candidates"][0]


def test_grade_requires_independent_recurrence_and_exact_active_subset(protocol):
    assert _grade(protocol, recurrence=2)["grade"] is None
    assert _grade(protocol, count=7)["grade"] == "CC1"
    result = _grade(protocol)
    assert result["grade"] == "CC2"
    assert result["active_test_step_count"] == 8
    assert result["random_gain"] == pytest.approx(0.02)
    assert result["cc3_local_pass"] is True
    assert result["replication_seed_count"] == 1


def test_incomplete_controls_preserve_cc1_but_forbid_cc2_and_cc3(protocol):
    result = _grade(protocol, shortfall=1)
    assert result["grade"] == "CC1"
    assert result["qualification"] == "control_matching_incomplete"
    assert result["cc3_local_pass"] is False
    assert result["random_gain"] > 0.01


def test_cc3_requires_three_distinct_seed_effects_not_candidate_alignment(protocol):
    from sparkbrain.v03_concepts.evaluation import candidate_metrics

    merged = [[], [], [], []]
    # Third ID is an in-memory numerical replication fixture, not a runtime seed.
    for seed in (99016, 99017, 99018):
        for target, source in zip(merged, _grade_case(protocol, seed), strict=True):
            target.extend(source)
    result = candidate_metrics(*merged, protocol, [])
    assert {r["candidates"][0]["grade"] for r in result} == {"CC3"}
    assert {r["candidates"][0]["replication_seed_count"] for r in result} == {3}
    failed = candidate_metrics(*merged, protocol, [{"run_seed": 99999}])
    assert {r["candidates"][0]["grade"] for r in failed} == {"CC0"}


@pytest.mark.parametrize("change", ["no_comparator", "no_restore", "collateral", "random_equal"])
def test_cc3_causal_gates_cannot_be_replaced_by_cohesion(protocol, change):
    from sparkbrain.v03_concepts.evaluation import candidate_metrics

    data = _grade_case(protocol)
    for row in data[3]:
        if change == "no_comparator":
            row["comparator_id"] = None
        elif change == "no_restore":
            row["restore_exact"] = False
        elif change == "collateral" and row["world"] != "recurrence":
            row["targeted_suppression"]["squared_error_sum"] = 96 * 0.2
        elif change == "random_equal":
            row["matched_random_suppression"] = copy.deepcopy(row["targeted_suppression"])
    assert not candidate_metrics(*data, protocol, [])[0]["candidates"][0]["cc3_local_pass"]


def test_null_jaccard_and_retired_child_do_not_inherit_grade(protocol):
    from sparkbrain.v03_concepts.evaluation import _jaccard, candidate_metrics

    assert _jaccard(set(), set()) is None
    data = _grade_case(protocol)
    parent = data[0][0]["final_state"]["live_candidates"].pop()
    parent["status"] = "retired"
    data[0][0]["final_state"]["retired_candidates"] = [parent]
    child = {
        **copy.deepcopy(parent),
        "candidate_id": "child",
        "birth_ordinal": 1,
        "parent_ids": [parent["candidate_id"]],
        "status": "active",
    }
    data[0][0]["final_state"]["live_candidates"] = [child]
    rows = candidate_metrics(*data, protocol, [])[0]["candidates"]
    assert rows[0]["grade"] == "CC0"
    assert rows[1]["grade"] is None
    assert rows[1]["train_episode_count"] == 0


def test_train_only_comparator_usage_tolerance_and_zero_usage_world(protocol):
    from sparkbrain.v03_concepts.evaluation import select_interventions

    rows = [dict(winner_id="a", world="recurrence")] * 8
    rows += [dict(winner_id="b", world="bridge_overmerge")] * 6
    rows += [dict(winner_id="c", world="decoy_reversal")] * 3
    choices = select_interventions(
        rows,
        ["a", "b", "c", "d"],
        run_seed=99016,
        representation="online_prototype",
        protocol=protocol,
    )
    assert choices["a"]["comparator_id"] == "b"
    assert choices["d"]["target_world"] is None
    assert choices["d"]["comparator_id"] is None


def _comparison_rows(protocol):
    rows = []
    for split in ("dev", "test"):
        for cell in protocol["scope"]["cell_order"]:
            for variant in protocol["scope"]["evaluation_variants"]:
                for wi, world in enumerate(protocol["world_generator"]["world_order"]):
                    for i in range(4):
                        total = float(wi + i + 1) + (0 if cell.endswith("/primary") else 2)
                        rows.append(
                            dict(
                                run_seed=99016,
                                split=split,
                                cell=cell,
                                variant=variant,
                                world=world,
                                episode_id=f"{world}-{i}",
                                squared_error_sum=total,
                                denominator=96,
                            )
                        )
    return rows


def test_bootstrap_is_paired_and_partial_intervals_are_not_imputed(protocol):
    from sparkbrain.v03_concepts.evaluation import control_comparisons, utility_summaries

    rows = _comparison_rows(protocol)
    seed, aggregate = control_comparisons(rows, protocol, [], resamples=40)
    assert len(seed) == len(aggregate) == 48
    for row in aggregate:
        interval = row["interval"]
        assert interval["defined_resamples"] == 40 and interval["undefined_resamples"] == 0
        assert interval["effect"] == pytest.approx(2 / 96)
        assert interval["lower"] == pytest.approx(2 / 96)
        assert interval["upper"] == pytest.approx(2 / 96)
    _, partial = control_comparisons(rows, protocol, [{"run_seed": 99017}], resamples=40)
    for row in partial:
        assert all(
            row["interval"][key] is None
            for key in ("effect", "lower", "upper", "defined_resamples", "undefined_resamples")
        )
    summaries, aggregates = utility_summaries(rows, protocol)
    assert len(summaries) == len(aggregates) == 72
    assert all(row["denominator"] == 16 * 96 for row in summaries)


@pytest.fixture(scope="module")
def reserved_complete_bundle():
    from sparkbrain.v03_concepts.evaluation import generate_bundle

    p = protocol_document()
    p["seeds"]["run_seeds"] = [99016]
    bundle = generate_bundle(p, "a" * 40)
    assert bundle["candidate_metrics.json"]["failed_seeds"] == []
    return p, bundle


def test_reserved_full_bundle_raw_replay_and_derived_recalculation(reserved_complete_bundle):
    from sparkbrain.v03_concepts.evaluation import validate_bundle

    p, bundle = reserved_complete_bundle
    validate_bundle(bundle, p, "a" * 40)
    assert len(bundle["candidate_lineage.jsonl"]) == 198
    assert len(bundle["causal_interventions.jsonl"]) == 384


@pytest.mark.parametrize("field", ["unknown", "hash", "nonfinite"])
def test_actual_bundle_rejects_nested_unknown_hash_and_nonfinite(reserved_complete_bundle, field):
    from sparkbrain.v03_concepts.evaluation import validate_bundle

    p, original = reserved_complete_bundle
    bundle = copy.deepcopy(original)
    row = bundle["candidate_metrics.json"]["bank_rows"][0]
    if field == "unknown":
        row["final_state"]["unregistered"] = True
    elif field == "hash":
        row["final_state_hash"] = "0" * 64
    else:
        row["readout_coefficients"][0][0] = float("nan")
    with pytest.raises(ValueError):
        validate_bundle(bundle, p, "a" * 40)


def test_mutating_actual_bank_encoder_cannot_claim_exact_restore(protocol, monkeypatch):
    from sparkbrain.v03_concepts.evaluation import _causal_rows

    episode = fixture(99016, "test", protocol)["episodes"][0]
    frames = sensory_episode(episode, "base", protocol)
    checkpoint = {"weights": {"W": [[0.0] * 12 for _ in range(4)]}}
    bank = _bank(protocol, "learned_local_prototype", encoder=checkpoint)
    cid = bank._birth([1.0, 0.0, 0.0, 0.0], [], 0)["candidate_id"]
    bank.freeze()
    before = digest(bank.encoder)
    query = bank.query

    def mutate_unused_weight(x, exclude_id=None):
        # This coordinate is zero: unchanged predictions cannot conceal a mutated AE.
        bank.encoder["weights"]["W"][0][11] += .0001
        return query(x, exclude_id)

    monkeypatch.setattr(bank, "query", mutate_unused_weight)
    selection = {cid: {"target_world": "recurrence", "comparator_id": None,
                       "train_candidate_usage": 0, "train_comparator_usage": None}}
    with pytest.raises(ValueError, match="mutated bank or representation"):
        _causal_rows(bank, [[0.0] * 12 for _ in range(9)], episode, frames,
                     selection, before, protocol, "a" * 40)
    assert digest(bank.encoder) != before


@pytest.mark.parametrize("split", ["dev", "test"])
def test_heldout_sensory_preparation_failure_resets_phase(protocol, monkeypatch, split):
    from sparkbrain.v03_concepts import evaluation, learning, worlds

    # Exercise the actual outer _run_seed/generate_bundle flow with no model execution.
    # Empty synthetic cells bypass discovery; the preceding phase remains representation_fit.
    p = copy.deepcopy(protocol)
    p["seeds"]["run_seeds"] = [99016, 99017]
    p["scope"]["primary_representations"] = []
    p["scope"]["cell_order"] = []

    def fail_preparation(episode, variant, protocol):
        if episode["split"] == split:
            raise RuntimeError("reserved preparation failure")
        return []

    monkeypatch.setattr(worlds, "sensory_episode", fail_preparation)
    monkeypatch.setattr(learning, "fit_encoder", lambda *args: {"stub": "reserved only"})
    bundle = evaluation.generate_bundle(p, "a" * 40)
    failures = bundle["candidate_metrics.json"]["failed_seeds"]
    assert [row["run_seed"] for row in failures] == [99016, 99017]
    for row in failures:
        assert row["phase"] == f"{split}_evaluation"
        assert row["representation"] is row["discovery_order"] is row["bank_kind"] is None
        assert row["error_type"] == "RuntimeError"
        assert row["error_hash"] == digest(
            [f"{split}_evaluation", None, None, None, "RuntimeError"])
    assert bundle["candidate_lineage.jsonl"] == []
    assert bundle["candidate_metrics.json"]["representation_checkpoints"] == []
    assert bundle["held_out_utility.json"]["episode_rows"] == []


@pytest.mark.parametrize("field,value", [
    ("representation", "not-a-representation"), ("discovery_order", True),
    ("bank_kind", {"unknown": "nested-key"}), ("error_type", ""),
    ("error_type", 3), ("run_seed", True),
])
def test_failed_seed_exact_types_and_enums_reject_even_rehashed(
    protocol, monkeypatch, field, value,
):
    from sparkbrain.v03_concepts import evaluation

    p = copy.deepcopy(protocol)
    p["seeds"]["run_seeds"] = [99016, 99017]

    def fail_without_execution(*args):
        raise RuntimeError("reserved stub, no fixture/model execution")

    monkeypatch.setattr(evaluation, "_run_seed", fail_without_execution)
    bundle = evaluation.generate_bundle(p, "a" * 40)
    failure = bundle["candidate_metrics.json"]["failed_seeds"][0]
    failure[field] = value
    failure["error_hash"] = digest([failure[key] for key in (
        "phase", "representation", "discovery_order", "bank_kind", "error_type")])
    bundle["report.md"] = evaluation.report_text(bundle, p, "a" * 40)
    with pytest.raises(ValueError, match="C16 failure"):
        evaluation.validate_bundle(bundle, p, "a" * 40)


def _raw_bundle(bundle):
    return {
        "lineage": bundle["candidate_lineage.jsonl"],
        "banks": list(bundle["candidate_metrics.json"]["bank_rows"]),
        "checkpoints": bundle["candidate_metrics.json"]["representation_checkpoints"],
        "utility": bundle["held_out_utility.json"]["episode_rows"],
        "causal": bundle["causal_interventions.jsonl"],
        "control_banks": list(bundle["matched_controls.json"]["control_bank_rows"]),
    }


@pytest.mark.parametrize("field,expected", [
    ("retired_count", "retired count"), ("dormant_count", "dormant count"),
    ("peak_live_count", "peak count"), ("unsupported_operations", "unsupported operations"),
    ("representation_hash", "representation commitment"),
])
def test_raw_replay_rejects_derived_and_representation_self_claim(
    reserved_complete_bundle, field, expected,
):
    from sparkbrain.v03_concepts.evaluation import _validate_raw

    p, bundle = reserved_complete_bundle
    data = _raw_bundle(bundle)
    row = copy.deepcopy(data["banks"][0])
    data["banks"][0] = row
    if field == "unsupported_operations":
        row[field] = ["invented-capability"]
    elif field == "representation_hash":
        row[field] = "0" * 64
    else:
        row[field] += 1
    with pytest.raises(ValueError, match=expected):
        _validate_raw(data, p, "a" * 40)


def test_raw_control_identity_inventory_rejects_duplicate_replacing_missing(
    reserved_complete_bundle,
):
    from sparkbrain.v03_concepts.evaluation import _validate_raw

    p, bundle = reserved_complete_bundle
    data = _raw_bundle(bundle)
    data["control_banks"][1] = copy.deepcopy(data["control_banks"][0])
    # Cardinality and every individual reference row remain valid; only identity coverage fails.
    assert len(data["control_banks"]) == 12
    with pytest.raises(ValueError, match="matched-control identity set"):
        _validate_raw(data, p, "a" * 40)


def test_all_deletions_precede_any_dormancy_regardless_of_candidate_id(protocol):
    bank = _bank(protocol)
    bank._birth(normalize(_x(0)), [_exemplar(0, _x(0))], 0)
    bank._birth(normalize(_x(1)), [_exemplar(1, _x(1))], 0)
    dormant, deleted = sorted(bank._live)
    bank._live[dormant]["last_seen"] = 16
    bank._live[deleted]["last_seen"] = 0
    bank._seen = {f"prior-{i}": digest(_x()) for i in range(32)}
    row = bank.observe(_x(), "at32")
    assert [event["operation"] for event in row["events"]] == ["delete", "dormant"]
    assert [event["candidate_id"] for event in row["events"]] == [deleted, dormant]


def test_rejected_split_leaves_parent_untouched_and_eligible_for_merge(protocol):
    bank = _bank(protocol)
    left = [.6, .8] + [0.0] * 10
    right = [.7, .714] + [0.0] * 10
    assert cosine(normalize(left), normalize(right)) >= .8
    for offset in (0, 8):
        rows = [_exemplar(i, left if i % 8 < 4 else right) for i in range(offset, offset + 8)]
        bank._birth(normalize(_x(0)), rows, offset)
    # One lifetime birth remains: split needs two, merge needs one.
    bank._births = 31
    original = set(bank._live)
    before, events = bank.hash(), []
    operated = bank._split(original, 16, events)
    assert bank.hash() == before and operated == set()
    assert events[0]["operation"] == "split_rejected"
    assert events[0]["reason"] == "birth_budget"
    bank._merge(original, operated, 16, events)
    assert [event["operation"] for event in events] == ["split_rejected", "merge"]
    assert len(bank._live) == 1 and bank._births == 32
    assert next(iter(bank._live.values()))["parent_ids"] == sorted(original)
