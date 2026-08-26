"""Frozen C16 experiment assembly and raw-to-derived evaluation.

Evaluator labels live here, never in the vector-only discovery bank.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from typing import Any


def canonical(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _ratio(numerator: float, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _loss(prediction: list[float], target: list[float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(prediction, target, strict=True))


def _effect(control: float | None, primary: float | None) -> float | None:
    return None if control is None or primary is None else control - primary


def _pooled(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = sum(row["squared_error_sum"] for row in rows)
    denominator = sum(row["denominator"] for row in rows)
    return {
        "episode_count": len(rows),
        "step_count": denominator // 12,
        "squared_error_sum": total,
        "denominator": denominator,
        "mse": _ratio(total, denominator),
    }


def utility_summaries(rows: list[dict], protocol: dict) -> tuple[list[dict], list[dict]]:
    """Pool exact raw sums; do not average already-rounded seed means."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        groups[(row["split"], row["cell"], row["run_seed"], row["variant"])].append(row)
    seeds = sorted({row["run_seed"] for row in rows})
    summaries, aggregates = [], []
    for split, cell in itertools.product(("dev", "test"), protocol["scope"]["cell_order"]):
        for seed in seeds:
            for variant in protocol["scope"]["evaluation_variants"]:
                selected = groups[(split, cell, seed, variant)]
                item = {
                    "split": split,
                    "cell": cell,
                    "variant": variant,
                    "run_seed": seed,
                    **_pooled(selected),
                }
                item["world_metrics"] = [
                    {"world": world, **_pooled([r for r in selected if r["world"] == world])}
                    for world in protocol["world_generator"]["world_order"]
                ]
                summaries.append(item)
        for variant in protocol["scope"]["evaluation_variants"]:
            selected = [r for seed in seeds for r in groups[(split, cell, seed, variant)]]
            if not selected:
                continue
            item = {"split": split, "cell": cell, "variant": variant, **_pooled(selected)}
            item["world_metrics"] = [
                {"world": world, **_pooled([r for r in selected if r["world"] == world])}
                for world in protocol["world_generator"]["world_order"]
            ]
            aggregates.append(item)
    return summaries, aggregates


def _percentile(values: list[float], p: float) -> float:
    position = (len(values) - 1) * p
    lower, upper = math.floor(position), math.ceil(position)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def control_comparisons(
    rows: list[dict], protocol: dict, failed_seeds: list[dict], *, resamples: int = 10000
) -> tuple[list[dict], list[dict]]:
    """Paired seed/world/episode bootstrap with one uninterrupted RNG stream."""
    lookup = {
        (r["run_seed"], r["split"], r["cell"], r["variant"], r["episode_id"]): r for r in rows
    }
    seeds = sorted({r["run_seed"] for r in rows})
    rng = random.Random(protocol["seeds"]["bootstrap_seed"])
    per_seed, aggregates = [], []
    for representation, control_kind, split, variant in itertools.product(
        protocol["scope"]["primary_representations"],
        ("matched_random", "frequency_topk"),
        ("dev", "test"),
        protocol["scope"]["evaluation_variants"],
    ):
        paired: dict[int, dict[str, list[tuple[dict, dict]]]] = {}
        common = {
            "representation": representation,
            "control_kind": control_kind,
            "split": split,
            "variant": variant,
        }
        selected_summaries = []
        for seed in seeds:
            paired[seed] = {}
            all_pairs = []
            for world in protocol["world_generator"]["world_order"]:
                primary = sorted(
                    [
                        r
                        for r in rows
                        if r["run_seed"] == seed
                        and r["split"] == split
                        and r["variant"] == variant
                        and r["cell"] == f"{representation}/primary"
                        and r["world"] == world
                    ],
                    key=lambda r: r["episode_id"],
                )
                pairs = [
                    (
                        p,
                        lookup[
                            (
                                seed,
                                split,
                                f"{representation}/{control_kind}",
                                variant,
                                p["episode_id"],
                            )
                        ],
                    )
                    for p in primary
                ]
                for p, c in pairs:
                    if p["denominator"] != c["denominator"]:
                        raise ValueError("unpaired C16 denominator")
                paired[seed][world] = pairs
                all_pairs.extend(pairs)
            p_sum = sum(p["squared_error_sum"] for p, _ in all_pairs)
            c_sum = sum(c["squared_error_sum"] for _, c in all_pairs)
            denominator = sum(p["denominator"] for p, _ in all_pairs)
            p_mse, c_mse = _ratio(p_sum, denominator), _ratio(c_sum, denominator)
            item = {
                "run_seed": seed,
                **common,
                "primary_squared_error_sum": p_sum,
                "control_squared_error_sum": c_sum,
                "denominator": denominator,
                "primary_mse": p_mse,
                "control_mse": c_mse,
                "effect": _effect(c_mse, p_mse),
            }
            per_seed.append(item)
            selected_summaries.append(item)
        if not seeds:
            continue
        p_sum = sum(r["primary_squared_error_sum"] for r in selected_summaries)
        c_sum = sum(r["control_squared_error_sum"] for r in selected_summaries)
        denominator = sum(r["denominator"] for r in selected_summaries)
        p_mse, c_mse = _ratio(p_sum, denominator), _ratio(c_sum, denominator)
        point = _effect(c_mse, p_mse)
        interval = {
            "effect": None if failed_seeds else point,
            "lower": None,
            "upper": None,
            "resamples": resamples,
            "bootstrap_seed": protocol["seeds"]["bootstrap_seed"],
            "defined_resamples": None,
            "undefined_resamples": None,
        }
        if not failed_seeds:
            values, undefined = [], 0
            for _ in range(resamples):
                p_total = c_total = 0.0
                count = 0
                for seed in rng.choices(seeds, k=len(seeds)):
                    for world in protocol["world_generator"]["world_order"]:
                        pairs = paired[seed][world]
                        for p, c in rng.choices(pairs, k=len(pairs)):
                            p_total += p["squared_error_sum"]
                            c_total += c["squared_error_sum"]
                            count += p["denominator"]
                value = _effect(_ratio(c_total, count), _ratio(p_total, count))
                if value is None:
                    undefined += 1
                else:
                    values.append(value)
            interval["defined_resamples"], interval["undefined_resamples"] = len(values), undefined
            if point is not None and not undefined:
                values.sort()
                interval["lower"] = _percentile(values, 0.025)
                interval["upper"] = _percentile(values, 0.975)
        aggregates.append(
            {
                **common,
                "primary_squared_error_sum": p_sum,
                "control_squared_error_sum": c_sum,
                "denominator": denominator,
                "primary_mse": p_mse,
                "control_mse": c_mse,
                "effect": point,
                "interval": interval,
            }
        )
    return per_seed, aggregates


def _jaccard(left: set[tuple], right: set[tuple]) -> float | None:
    union = left | right
    return len(left & right) / len(union) if union else None


def select_interventions(
    train_rows: list[dict],
    slot_ids: list[str],
    *,
    run_seed: int,
    representation: str,
    protocol: dict,
) -> dict[str, dict]:
    """Freeze target-world and comparator from train, without held-out effects."""
    usage = Counter(r["winner_id"] for r in train_rows if r["winner_id"] is not None)
    world_order = protocol["world_generator"]["world_order"]
    result = {}
    for candidate in slot_ids:
        counts = Counter(r["world"] for r in train_rows if r["winner_id"] == candidate)
        target = (
            min(world_order, key=lambda w: (-counts[w], world_order.index(w))) if counts else None
        )
        eligible = [
            other
            for other in slot_ids
            if other != candidate
            and abs(usage[other] - usage[candidate]) <= max(2, 0.25 * usage[candidate])
        ]

        def ranking(other: str, candidate_id: str = candidate) -> tuple[str, str]:
            text = f"c16|suppression-control|{run_seed}|{representation}|{candidate_id}|{other}"
            return hashlib.sha256(text.encode()).hexdigest(), other

        comparator = min(eligible, key=ranking) if eligible else None
        result[candidate] = {
            "target_world": target,
            "comparator_id": comparator,
            "train_candidate_usage": usage[candidate],
            "train_comparator_usage": usage[comparator] if comparator else None,
        }
    return result


def candidate_metrics(
    bank_rows: list[dict],
    lineage: list[dict],
    utility: list[dict],
    causal: list[dict],
    protocol: dict,
    failed_seeds: list[dict],
) -> list[dict]:
    """Grades use actual discovery winners, never retrospective child attribution."""
    result = copy.deepcopy(bank_rows)
    test_index = {
        (r["run_seed"], r["cell"], r["variant"], r["episode_id"], s["t"]): s
        for r in utility
        if r["split"] == "test"
        for s in r["steps"]
    }
    replication: dict[tuple[str, str], set[int]] = defaultdict(set)
    pending = []
    for bank_row in result:
        bank = bank_row["bank"]
        seed, representation, kind, order = (
            bank[k] for k in ("run_seed", "representation", "bank_kind", "discovery_order")
        )
        records = (
            bank_row["final_state"]["live_candidates"]
            + bank_row["final_state"]["retired_candidates"]
        )
        discovery = [
            r
            for r in lineage
            if r["row_kind"] == "episode"
            and r["run_seed"] == seed
            and r["representation"] == representation
            and r["discovery_order"] == order
        ]
        controls = [
            r
            for r in lineage
            if r["row_kind"] == "control"
            and r["run_seed"] == seed
            and r["representation"] == representation
            and r["discovery_order"] == order
        ]
        incomplete = any(c["shortfall"] for r in controls for c in r["reference_banks"])
        candidates = []
        for state in sorted(records, key=lambda r: r["birth_ordinal"]):
            cid = state["candidate_id"]
            item = {key: None for key in protocol["schemas"]["candidate_metric"]}
            item.update(
                {
                    "candidate_id": cid,
                    "birth_ordinal": state["birth_ordinal"],
                    "status": state["status"],
                    "parent_ids": state["parent_ids"],
                    "member_feature_ids": state["member_feature_ids"],
                    "retained_observation_ids": [
                        e["observation_id"] for e in state["retained_exemplars"]
                    ],
                    "cc3_local_pass": False,
                    "replication_seed_count": 0,
                }
            )
            if kind != "primary":
                item["qualification"] = "reference_control_not_discovered"
                candidates.append(item)
                continue
            episodes, contexts = set(), set()
            for row in discovery:
                for frame in row["frames"]:
                    if frame["winner_id"] == cid:
                        episodes.add(row["episode_id"])
                        # Context is reconstructed from the fixture, not bank state.
                        contexts.add(
                            _context(
                                seed,
                                row["world"],
                                row["episode_id"],
                                frame["frame_index"],
                                protocol,
                            )
                        )
            item.update(
                train_episode_count=len(episodes),
                train_context_count=len(contexts),
                qualification="insufficient_independent_recurrence",
            )
            if len(episodes) >= 3 and len(contexts) >= 2:
                item.update(grade="CC0", qualification="recurring_assembly")
            if state["status"] == "retired" or order != "canonical":
                item["qualification"] = (
                    "retired_before_held_out"
                    if state["status"] == "retired"
                    else "order_control_not_perturbation_evaluated"
                )
                candidates.append(item)
                continue
            active = {}
            for variant in ("base", "amplitude_perturbation", "irrelevant_distractor"):
                active[variant] = {
                    (eid, t)
                    for (s, cell, v, eid, t), step in test_index.items()
                    if s == seed
                    and cell == f"{representation}/primary"
                    and v == variant
                    and step["winner_id"] == cid
                }
            base = active["base"]
            base_steps = [
                test_index[(seed, f"{representation}/primary", "base", eid, t)]
                for eid, t in sorted(base)
            ]
            item.update(
                test_episode_count=len({eid for eid, _ in base}),
                test_context_count=len({s["context"] for s in base_steps}),
                active_test_step_count=len(base),
                perturbation_jaccard=_jaccard(base, active["amplitude_perturbation"]),
                distractor_jaccard=_jaccard(base, active["irrelevant_distractor"]),
            )
            if (
                item["grade"] == "CC0"
                and item["test_episode_count"] >= 2
                and item["test_context_count"] >= 2
                and all(
                    item[k] is not None and item[k] >= 0.8
                    for k in ("perturbation_jaccard", "distractor_jaccard")
                )
            ):
                item.update(grade="CC1", qualification="stable_candidate")
            denominator = 12 * len(base)
            item["primary_active_mse"] = _ratio(
                sum(s["squared_error_sum"] for s in base_steps), denominator
            )
            for control, prefix in (("matched_random", "random"), ("frequency_topk", "frequency")):
                steps = [
                    test_index[(seed, f"{representation}/{control}", "base", eid, t)]
                    for eid, t in sorted(base)
                ]
                mse = _ratio(sum(s["squared_error_sum"] for s in steps), denominator)
                item[f"{prefix}_active_mse"] = mse
                item[f"{prefix}_gain"] = _effect(mse, item["primary_active_mse"])
            if (
                item["grade"] == "CC1"
                and not incomplete
                and len(base) >= 8
                and all(
                    item[k] is not None and item[k] >= 0.01
                    for k in ("random_gain", "frequency_gain")
                )
            ):
                item.update(grade="CC2", qualification="held_out_candidate")
            interventions = [
                r
                for r in causal
                if r["run_seed"] == seed
                and r["representation"] == representation
                and r["candidate_id"] == cid
            ]
            if interventions:
                item["train_target_world"] = interventions[0]["target_world"]
                item["comparator_id"] = interventions[0]["comparator_id"]
                target = [r for r in interventions if r["world"] == item["train_target_world"]]
                other = [r for r in interventions if r["world"] != item["train_target_world"]]
                for key, selected, branch in (
                    ("target_impairment", target, "targeted_suppression"),
                    ("random_impairment", target, "matched_random_suppression"),
                    ("collateral", other, "targeted_suppression"),
                ):
                    valid = selected and all(r[branch]["mse"] is not None for r in selected)
                    if valid:
                        den = sum(r[branch]["denominator"] for r in selected)
                        branch_mse = _ratio(
                            sum(r[branch]["squared_error_sum"] for r in selected), den
                        )
                        baseline_mse = _ratio(
                            sum(r["baseline"]["squared_error_sum"] for r in selected), den
                        )
                        item[key] = _effect(branch_mse, baseline_mse)
                item["target_minus_random"] = _effect(
                    item["target_impairment"], item["random_impairment"]
                )
                local = (
                    item["grade"] == "CC2"
                    and item["comparator_id"] is not None
                    and item["target_impairment"] is not None
                    and item["target_impairment"] >= 0.05
                    and item["target_minus_random"] is not None
                    and item["target_minus_random"] >= 0.03
                    and item["collateral"] is not None
                    and item["collateral"] <= 0.02
                    and all(r["restore_exact"] for r in interventions)
                )
                item["cc3_local_pass"] = bool(local)
                if local:
                    replication[(representation, item["train_target_world"])].add(seed)
                pending.append((representation, item))
            if incomplete and item["grade"] is not None:
                item["qualification"] = "control_matching_incomplete"
            candidates.append(item)
        bank_row["candidates"] = candidates
    for representation, item in pending:
        count = len(replication[(representation, item["train_target_world"])])
        item["replication_seed_count"] = count
        if item["cc3_local_pass"] and count >= 3:
            item.update(grade="CC3", qualification="causal_candidate")
    if failed_seeds:
        for row in result:
            for item in row["candidates"]:
                if item["grade"] in ("CC1", "CC2", "CC3"):
                    item["grade"] = "CC0"
                if row["bank"]["bank_kind"] == "primary":
                    item["qualification"] = "not_evaluated_implementation_failure"
    return result


def _context(seed: int, world: str, episode_id: str, t: int, protocol: dict) -> int:
    for i in range(protocol["world_generator"]["episodes_per_world"]["train"]):
        text = f"c16|episode|{seed}|train|{world}|{i}"
        if "ep-" + hashlib.sha256(text.encode()).hexdigest()[:24] == episode_id:
            return ((i + seed - 3601 + t) % 3 + i % 2) % 3
    raise ValueError("discovery episode is not in the frozen train fixture")


def _common(protocol: dict, source_commit: str) -> dict:
    return {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
    }


def _predict_steps(
    bank: Any,
    coefficients: list,
    frames: list[dict],
    episode: dict,
    *,
    exclude_id: str | None = None,
    substitute: tuple[str, str] | None = None,
) -> list[dict]:
    from .learning import predict

    before = bank.hash()
    encoder_before = _bank_representation_hash(bank)
    rows = []
    for t, frame in enumerate(frames[:8]):
        query = bank.query(frame["emitted_vector"], exclude_id=exclude_id)
        if substitute and query["winner_id"] == substitute[0]:
            query = {
                **query,
                "winner_id": substitute[1],
                "slot_index": bank.slot_candidate_ids.index(substitute[1]),
            }
        raw, prediction = predict(coefficients, query["slot_index"])
        target = episode["frames"][t + 1]["base_values"]
        row = {
            "t": t,
            "sample_id": frame["sample_id"],
            **{
                k: frame[k]
                for k in (
                    "input_values",
                    "emitted_vector",
                    "emitted_mask",
                    "perceptual_spark_ids",
                    "parent_sample_ids",
                    "lineage_registry_hash",
                    "context",
                )
            },
            "sensory_state_hash": frame["sensory_state_hash_after"],
            **query,
            "target": target,
            "raw_prediction": raw,
            "prediction": prediction,
            "squared_error_sum": _loss(prediction, target),
            "denominator": 12,
        }
        rows.append(row)
    if bank.hash() != before or _bank_representation_hash(bank) != encoder_before:
        raise ValueError("C16 inference mutated bank or representation state")
    return rows


def _bank_representation_hash(bank: Any) -> str:
    if bank.encoder is None:
        return digest(bank.protocol["representations"][bank.identity["representation"]])
    payload = {k: v for k, v in bank.encoder.items() if k != "checkpoint_hash"}
    return digest(payload)


def _branch(steps: list[dict] | None, status: str) -> dict:
    if steps is None:
        return {
            "status": status,
            "winner_ids": None,
            "raw_predictions": None,
            "predictions": None,
            "squared_error_sum": None,
            "denominator": None,
            "mse": None,
        }
    total = sum(s["squared_error_sum"] for s in steps)
    denominator = sum(s["denominator"] for s in steps)
    return {
        "status": status,
        "winner_ids": [s["winner_id"] for s in steps],
        "raw_predictions": [s["raw_prediction"] for s in steps],
        "predictions": [s["prediction"] for s in steps],
        "squared_error_sum": total,
        "denominator": denominator,
        "mse": _ratio(total, denominator),
    }


def _causal_rows(
    bank: Any,
    coefficients: list,
    episode: dict,
    frames: list[dict],
    selection: dict,
    representation_hash: str,
    protocol: dict,
    source_commit: str,
) -> list[dict]:
    rows = []
    baseline = _predict_steps(bank, coefficients, frames, episode)
    bank_hash, readout_hash = bank.hash(), digest(coefficients)
    actual_representation_hash = _bank_representation_hash(bank)
    if actual_representation_hash != representation_hash:
        raise ValueError("C16 representation commitment mismatch")
    for slot, cid in enumerate(bank.slot_candidate_ids):
        row = {
            **_common(protocol, source_commit),
            **{k: bank.state()["bank"][k] for k in ("run_seed", "representation")},
            "episode_id": episode["episode_id"],
            "world": episode["world"],
            "slot_index": slot,
            "candidate_id": cid,
            "status": "evaluated" if cid else "not_instantiated",
            "target_world": None,
            "comparator_id": None,
            "train_candidate_usage": None,
            "train_comparator_usage": None,
            "bank_hash_before": bank_hash,
            "bank_hash_after": bank_hash,
            "bank_hash_restored": bank_hash,
            "representation_hash_before": actual_representation_hash,
            "representation_hash_after": actual_representation_hash,
            "readout_hash_before": readout_hash,
            "readout_hash_after": readout_hash,
            "baseline_prediction_hash": None,
            "restored_prediction_hash": None,
            "restore_exact": None,
        }
        if cid is None:
            for name in (
                "baseline",
                "targeted_suppression",
                "matched_random_suppression",
                "substitution",
            ):
                row[name] = _branch(None, "not_instantiated")
        else:
            row.update(selection[cid])
            comparator = selection[cid]["comparator_id"]
            targeted = _predict_steps(bank, coefficients, frames, episode, exclude_id=cid)
            matched = (
                _predict_steps(bank, coefficients, frames, episode, exclude_id=comparator)
                if comparator
                else None
            )
            substituted = (
                _predict_steps(bank, coefficients, frames, episode, substitute=(cid, comparator))
                if comparator
                else None
            )
            restored = _predict_steps(bank, coefficients, frames, episode)
            row.update(
                baseline=_branch(baseline, "evaluated"),
                targeted_suppression=_branch(targeted, "evaluated"),
                matched_random_suppression=_branch(
                    matched, "evaluated" if comparator else "no_comparator"
                ),
                substitution=_branch(substituted, "evaluated" if comparator else "no_comparator"),
                baseline_prediction_hash=digest(baseline),
                restored_prediction_hash=digest(restored),
                bank_hash_after=bank.hash(),
                bank_hash_restored=bank.hash(),
                representation_hash_after=_bank_representation_hash(bank),
                readout_hash_after=digest(coefficients),
            )
            row["restore_exact"] = (
                row["baseline_prediction_hash"] == row["restored_prediction_hash"]
                and bank.hash() == bank_hash
                and _bank_representation_hash(bank) == actual_representation_hash
                and digest(coefficients) == readout_hash
            )
            if not row["restore_exact"]:
                raise ValueError("C16 intervention restore mismatch")
        rows.append(row)
    return rows


def _run_seed(protocol: dict, source_commit: str, seed: int, location: dict) -> dict:
    from .bank import ConceptBank, build_controls
    from .learning import fit_encoder, fit_readout
    from .worlds import fixture, sensory_episode

    def phase(
        name: str,
        representation: str | None = None,
        order: str | None = None,
        kind: str | None = None,
    ) -> None:
        location.update(
            phase=name, representation=representation, discovery_order=order, bank_kind=kind
        )

    phase("fixture")
    fixtures = {split: fixture(seed, split, protocol) for split in ("train", "dev", "test")}
    phase("sensory")
    train = fixtures["train"]["episodes"]
    sensory = {e["episode_id"]: sensory_episode(e, "base", protocol) for e in train}
    train_frames = [frame for e in train for frame in sensory[e["episode_id"]]]
    phase("representation_fit", "learned_local_prototype")
    checkpoint = fit_encoder([f["emitted_vector"] for f in train_frames], seed)
    checkpoint_before = canonical(checkpoint)
    output: dict[str, Any] = {
        "lineage": [],
        "banks": [],
        "checkpoints": [checkpoint],
        "utility": [],
        "causal": [],
        "control_banks": [],
    }
    runtime = {}
    for representation in protocol["scope"]["primary_representations"]:
        encoder = checkpoint if representation == "learned_local_prototype" else None
        representation_hash = (
            checkpoint["checkpoint_hash"]
            if encoder
            else digest(protocol["representations"][representation])
        )
        for order in protocol["scope"]["discovery_orders"]:
            phase("discovery", representation, order, "primary")
            primary = ConceptBank(protocol, seed, representation, order, encoder=encoder)
            episodes = list(train)
            if order == "episode_shuffle":
                episodes.sort(
                    key=lambda e: (
                        hashlib.sha256(
                            f"c16|shuffle|{seed}|{e['episode_id']}".encode()
                        ).hexdigest(),
                        e["episode_id"],
                    )
                )
            peak = 0
            for execution_index, episode in enumerate(episodes):
                before = primary.hash()
                frames = []
                for frame in sensory[episode["episode_id"]]:
                    observation_id = (
                        "ob-" + hashlib.sha256(frame["sample_id"].encode()).hexdigest()[:24]
                    )
                    observed = primary.observe(frame["emitted_vector"], observation_id)
                    row = {
                        key: frame[key]
                        for key in (
                            "frame_index",
                            "sample_id",
                            "input_values",
                            "emitted_vector",
                            "emitted_mask",
                            "perceptual_spark_ids",
                            "parent_sample_ids",
                            "lineage_registry_hash",
                            "sensory_state_hash_before",
                            "sensory_state_hash_after",
                            "sensory_trace",
                            "sensory_work",
                        )
                    }
                    row.update(
                        {
                            key: observed[key]
                            for key in (
                                "global_frame_index",
                                "representation_vector",
                                "winner_id",
                                "match_score",
                                "events",
                                "bank_hash_before",
                                "bank_hash_after",
                            )
                        }
                    )
                    frames.append(row)
                    peak = max(peak, len(primary.state()["live_candidates"]))
                output["lineage"].append(
                    {
                        **_common(protocol, source_commit),
                        "row_kind": "episode",
                        "run_seed": seed,
                        "representation": representation,
                        "discovery_order": order,
                        "execution_episode_index": execution_index,
                        "episode_id": episode["episode_id"],
                        "world": episode["world"],
                        "frames": frames,
                        "bank_hash_before": before,
                        "bank_hash_after": primary.hash(),
                    }
                )
            primary.freeze()
            phase("control_build", representation, order)
            controls, construction = build_controls(primary, train_frames)
            construction = {
                **construction,
                **_common(protocol, source_commit),
                "row_kind": "control",
            }
            output["lineage"].append(construction)
            for kind, bank in {"primary": primary, **controls}.items():
                phase("readout_fit", representation, order, kind)
                before = bank.hash()
                queries, targets, raw_queries = [], [], []
                for episode in train:
                    for t, frame in enumerate(sensory[episode["episode_id"]][:8]):
                        query = bank.query(frame["emitted_vector"])
                        queries.append(query)
                        targets.append(episode["frames"][t + 1]["base_values"])
                        raw_queries.append(
                            {
                                "episode_id": episode["episode_id"],
                                "world": episode["world"],
                                "t": t,
                                "sample_id": frame["sample_id"],
                                "context": frame["context"],
                                **query,
                            }
                        )
                coefficients = fit_readout(queries, targets)
                if bank.hash() != before:
                    raise ValueError("C16 readout fitting mutated bank")
                phase("train_evaluator_selection", representation, order, kind)
                slots = [cid for cid in bank.slot_candidate_ids if cid is not None]
                usage = dict(
                    sorted((cid, sum(q["winner_id"] == cid for q in queries)) for cid in slots)
                )
                selection = select_interventions(
                    raw_queries,
                    slots,
                    run_seed=seed,
                    representation=representation,
                    protocol=protocol,
                )
                state = bank.state()
                unsupported = (
                    ["update", "merge", "split", "dormancy", "deletion"]
                    if kind != "primary"
                    else ["merge", "split", "dormancy", "deletion", "homeostasis"]
                    if representation == "cc0_assembly"
                    else []
                )
                record = {
                    "bank": state["bank"],
                    "final_state": state,
                    "final_state_hash": bank.hash(),
                    "slot_candidate_ids": list(bank.slot_candidate_ids),
                    "unsupported_operations": unsupported,
                    "birth_count": state["birth_counter"],
                    "retired_count": len(state["retired_candidates"]),
                    "dormant_count": sum(
                        c["status"] == "dormant" for c in state["live_candidates"]
                    ),
                    "peak_live_count": peak if kind == "primary" else len(slots),
                    "train_query_rows": raw_queries,
                    "train_usage_counts": usage,
                    "candidates": [],
                    "readout_coefficients": coefficients,
                    "readout_hash": digest(coefficients),
                    "representation_hash": representation_hash,
                }
                output["banks"].append(record)
                runtime[(representation, kind, order)] = (
                    bank,
                    coefficients,
                    selection,
                    representation_hash,
                )
                if kind != "primary":
                    reference = next(
                        r for r in construction["reference_banks"] if r["bank_kind"] == kind
                    )
                    output["control_banks"].append(
                        {
                            "bank": state["bank"],
                            "primary_bank_hash": primary.hash(),
                            "control_bank_hash": bank.hash(),
                            "primary_count": reference["primary_count"],
                            "reference_count": reference["reference_count"],
                            "slot_budget": 8,
                            "member_sizes": [
                                len(c["member_feature_ids"]) for c in state["live_candidates"]
                            ],
                            "train_usage_counts": usage,
                            "shortfall": reference["shortfall"],
                            "selection_pattern_ids": reference["selection_order_pattern_ids"],
                        }
                    )
    for split in ("dev", "test"):
        for episode in fixtures[split]["episodes"]:
            phase(f"{split}_evaluation")
            cached = {
                variant: sensory_episode(episode, variant, protocol)
                for variant in ("base", "amplitude_perturbation", "irrelevant_distractor")
            }
            cached["order_shuffle"] = cached["base"]
            for cell in protocol["scope"]["cell_order"]:
                representation, kind = cell.split("/")
                for variant in protocol["scope"]["evaluation_variants"]:
                    order = protocol["scope"]["variant_to_bank_order"][variant]
                    phase(f"{split}_evaluation", representation, order, kind)
                    bank, coefficients, selection, representation_hash = runtime[
                        (representation, kind, order)
                    ]
                    steps = _predict_steps(bank, coefficients, cached[variant], episode)
                    total = sum(s["squared_error_sum"] for s in steps)
                    denominator = sum(s["denominator"] for s in steps)
                    output["utility"].append(
                        {
                            "run_seed": seed,
                            "split": split,
                            "world": episode["world"],
                            "episode_id": episode["episode_id"],
                            "cell": cell,
                            "variant": variant,
                            "bank_order": order,
                            "bank_hash": bank.hash(),
                            "representation_hash": representation_hash,
                            "readout_hash": digest(coefficients),
                            "steps": steps,
                            "squared_error_sum": total,
                            "denominator": denominator,
                            "mse": _ratio(total, denominator),
                        }
                    )
                if split == "test" and kind == "primary":
                    phase("causal_evaluation", representation, "canonical", kind)
                    bank, coefficients, selection, representation_hash = runtime[
                        (representation, kind, "canonical")
                    ]
                    output["causal"].extend(
                        _causal_rows(
                            bank,
                            coefficients,
                            episode,
                            cached["base"],
                            selection,
                            representation_hash,
                            protocol,
                            source_commit,
                        )
                    )
    phase("seed_validation")
    if canonical(checkpoint) != checkpoint_before:
        raise ValueError("C16 evaluation mutated the learned representation")
    if any(
        _bank_representation_hash(bank) != representation_hash
        for bank, _, _, representation_hash in runtime.values()
    ):
        raise ValueError("C16 bank-local representation mutated")
    return output


def failure_examples(
    bank_rows: list[dict],
    lineage: list[dict],
    utility: list[dict],
    protocol: dict,
    source_commit: str,
) -> list[dict]:
    rows = []
    lookup = {
        (r["run_seed"], r["cell"], r["episode_id"]): r
        for r in utility
        if r["split"] == "test" and r["variant"] == "base"
    }
    for bank in bank_rows:
        identity = bank["bank"]
        if identity["bank_kind"] != "primary" or identity["discovery_order"] != "canonical":
            continue
        seed, representation = identity["run_seed"], identity["representation"]
        training = [
            r
            for r in lineage
            if r["row_kind"] == "episode"
            and r["run_seed"] == seed
            and r["representation"] == representation
            and r["discovery_order"] == "canonical"
        ]
        counts, pair_counts = Counter(), Counter()
        for episode in training:
            for frame in episode["frames"]:
                features = [
                    f"local_numeric:ch{i:02d}"
                    for i, x in enumerate(frame["emitted_vector"])
                    if x != 0
                ]
                counts.update(features)
                pair_counts.update(itertools.combinations(features, 2))
        for world in protocol["world_generator"]["world_order"]:
            options = []
            for (s, cell, eid), primary in lookup.items():
                if s != seed or cell != f"{representation}/primary" or primary["world"] != world:
                    continue
                random_row = lookup[(seed, f"{representation}/matched_random", eid)]
                frequency_row = lookup[(seed, f"{representation}/frequency_topk", eid)]
                regret = primary["mse"] - min(random_row["mse"], frequency_row["mse"])
                options.append((regret, eid, primary, random_row, frequency_row))
            regret, eid, primary, random_row, frequency_row = min(
                options, key=lambda x: (-x[0], x[1])
            )
            winner_counts = Counter(
                s["winner_id"] for s in primary["steps"] if s["winner_id"] is not None
            )
            active_ids = sorted(winner_counts)
            states = (
                bank["final_state"]["live_candidates"] + bank["final_state"]["retired_candidates"]
            )
            transitive, similarities = [], []
            for state in states:
                if state["candidate_id"] not in active_ids:
                    continue
                for a, b in itertools.combinations(sorted(state["member_feature_ids"]), 2):
                    if not pair_counts[(a, b)]:
                        transitive.append(
                            {
                                "candidate_id": state["candidate_id"],
                                "left_feature_id": a,
                                "right_feature_id": b,
                                "joint_frame_count": 0,
                                "left_frame_count": counts[a],
                                "right_frame_count": counts[b],
                            }
                        )
                vectors = [
                    e["representation"]
                    for e in state["retained_exemplars"]
                    if e["representation"] is not None
                ]
                for a, b in itertools.combinations(vectors, 2):
                    norm = math.sqrt(sum(x * x for x in a) * sum(x * x for x in b))
                    if norm > 1e-12:
                        similarities.append(
                            max(
                                -1.0, min(1.0, sum(x * y for x, y in zip(a, b, strict=True)) / norm)
                            )
                        )
            reasons = []
            if not similarities:
                reasons.append("fewer_than_two_nonzero_retained_exemplars")
            if not winner_counts:
                reasons.append("no_matched_steps")
            rows.append(
                {
                    **_common(protocol, source_commit),
                    "run_seed": seed,
                    "representation": representation,
                    "world": world,
                    "episode_id": eid,
                    "classification": "utility_regret" if regret > 0 else "no_failure_observed",
                    "primary_mse": primary["mse"],
                    "random_mse": random_row["mse"],
                    "frequency_mse": frequency_row["mse"],
                    "regret": regret,
                    "candidate_ids": active_ids,
                    "transitive_overmerge_pairs": sorted(
                        transitive,
                        key=lambda r: (
                            r["candidate_id"],
                            r["left_feature_id"],
                            r["right_feature_id"],
                        ),
                    ),
                    "minimum_retained_pair_cosine": min(similarities) if similarities else None,
                    "peak_live_count": bank["peak_live_count"],
                    "birth_budget_exhausted": bank["birth_count"]
                    >= protocol["formation"]["maximum_births_per_primary_bank"],
                    "winner_share_max": max(winner_counts.values()) / sum(winner_counts.values())
                    if winner_counts
                    else None,
                    "null_metric_reasons": reasons,
                }
            )
    return rows


def _sort_raw(data: dict, protocol: dict) -> None:
    reps = protocol["scope"]["primary_representations"]
    orders = protocol["scope"]["discovery_orders"]
    kinds = protocol["scope"]["bank_kinds"]
    variants = protocol["scope"]["evaluation_variants"]
    data["lineage"].sort(
        key=lambda r: (
            r["run_seed"],
            reps.index(r["representation"]),
            orders.index(r["discovery_order"]),
            r["row_kind"] != "episode",
            r.get("execution_episode_index", 0),
        )
    )
    data["banks"].sort(
        key=lambda r: (
            r["bank"]["run_seed"],
            reps.index(r["bank"]["representation"]),
            kinds.index(r["bank"]["bank_kind"]),
            orders.index(r["bank"]["discovery_order"]),
        )
    )
    data["utility"].sort(
        key=lambda r: (
            ("dev", "test").index(r["split"]),
            protocol["scope"]["cell_order"].index(r["cell"]),
            r["run_seed"],
            r["episode_id"],
            variants.index(r["variant"]),
        )
    )
    data["causal"].sort(
        key=lambda r: (
            r["run_seed"],
            reps.index(r["representation"]),
            r["episode_id"],
            r["slot_index"],
        )
    )
    data["control_banks"].sort(
        key=lambda r: (
            r["bank"]["run_seed"],
            reps.index(r["bank"]["representation"]),
            kinds.index(r["bank"]["bank_kind"]),
            orders.index(r["bank"]["discovery_order"]),
        )
    )


def _stage_status(banks: list[dict], protocol: dict, failures: list[dict]) -> dict:
    seeds = sorted({b["bank"]["run_seed"] for b in banks})
    eligible = [
        c
        for b in banks
        if b["bank"]["bank_kind"] == "primary" and b["bank"]["discovery_order"] == "canonical"
        for c in b["candidates"]
    ]
    grades = ["CC0", "CC1", "CC2", "CC3"]
    result = {}
    for index, grade in enumerate(grades):
        count = sum(c["grade"] in grades[index:] for c in eligible)
        result[grade] = {
            "status": "not_evaluated_implementation_failure"
            if failures
            else "supported"
            if count
            else "not_supported",
            "qualified_candidate_count": None if failures else count,
            "required_run_seeds": len(protocol["seeds"]["run_seeds"]),
            "successful_run_seeds": len(seeds),
        }
    return result


def _engineering(data: dict, failures: list[dict], protocol: dict) -> list[dict]:
    # Source integrity is checked by the mandatory runner preflight. The remaining
    # assertions are reconstructed from raw evidence before this function is used.
    parents = [f for r in data["lineage"] if r["row_kind"] == "episode" for f in r["frames"]]
    resolved = sum(
        all(p == f["sample_id"] for p in f["parent_sample_ids"])
        and (not f["perceptual_spark_ids"] or f["parent_sample_ids"] == [f["sample_id"]])
        for f in parents
    )
    rate = resolved / len(parents) if parents else None
    live = [r for r in data["causal"] if r["candidate_id"] is not None]
    observed = {
        "protected_and_source_integrity": True,
        "no_target_leakage": bool(data["banks"]),
        "bounded_identity_and_lifecycle": bool(data["banks"])
        and all(
            len(b["final_state"]["live_candidates"]) <= 8
            and b["birth_count"] <= 32
            and b["final_state"]["accepted_observation_count"] <= 288
            for b in data["banks"]
        ),
        "lineage_parent_resolution": rate,
        "frozen_inference_and_exact_restore": bool(data["banks"])
        and all(r["restore_exact"] for r in live),
        "matched_budgets": bool(data["banks"])
        and all(len(b["slot_candidate_ids"]) == 8 for b in data["banks"]),
        "raw_cardinality_and_recalculation": True,
        "all_required_seeds_complete": not failures,
    }
    gates = []
    for name in protocol["schemas"]["engineering_gate_order"]:
        required = 1.0 if name == "lineage_parent_resolution" else True
        gates.append(
            {
                "gate_id": name,
                "observed": observed[name],
                "required": required,
                "passed": observed[name] == required,
            }
        )
    return gates


def report_text(bundle: dict, protocol: dict, source_commit: str) -> str:
    metrics = bundle["candidate_metrics.json"]
    failures = metrics["failed_seeds"]
    status = (
        "implementation_failure"
        if failures
        else "pass"
        if all(g["passed"] for g in metrics["engineering_gates"])
        else "fail"
    )
    lines = [
        "# C16 bounded proto-concept formation",
        "",
        f"Protocol: `{protocol['protocol_id']}`",
        f"Run: `{protocol['run_id']}`",
        f"Source commit: `{source_commit}`",
        "",
        "## Engineering",
        "",
        f"Status: `{status}`",
        f"Failed seeds: `{canonical(failures)}`",
        "",
        "## Scientific stages",
        "",
    ]
    for grade, result in metrics["scientific_stage_status"].items():
        lines.append(
            f"- {grade}: {result['status']}; "
            f"qualified candidates={result['qualified_candidate_count']}"
        )
    lines += [
        "",
        "## Scope and counterexamples",
        "",
        "Five run seeds, three representations, matched controls, canonical/shuffled",
        "discovery and four held-out variants. All exact raw denominators, absent slots, control",
        "shortfalls and worst-episode audits are retained. Negative findings are not hidden.",
        "Only next-channel MSE is assessed. Grades describe unlabeled synthetic candidates, not",
        "human semantic concepts, autonomous understanding, biological equivalence,",
        "organs, or energy efficiency.",
        "Bootstrap intervals are descriptive and do not establish familywise significance.",
        "",
        "## Reproduction",
        "",
        "Use the recorded stage execution checkout and a different PYTHONHASHSEED.",
        "Require all eight artifact files to be byte-identical. Later main source changes",
        "are not silently accepted by the source guard.",
        "",
    ]
    return "\n".join(lines)


def generate_bundle(protocol: dict, source_commit: str) -> dict:
    data: dict[str, list] = {
        k: [] for k in ("lineage", "banks", "checkpoints", "utility", "causal", "control_banks")
    }
    failures = []
    for seed in protocol["seeds"]["run_seeds"]:
        location = {
            "phase": "fixture",
            "representation": None,
            "discovery_order": None,
            "bank_kind": None,
        }
        try:
            buffered = _run_seed(protocol, source_commit, seed, location)
            _validate_counts(buffered, 1)
            _validate_raw(buffered, protocol, source_commit)
        except Exception as error:
            error_type = type(error).__name__
            failures.append(
                {
                    "run_seed": seed,
                    **location,
                    "error_type": error_type,
                    "error_hash": digest(
                        [
                            location["phase"],
                            location["representation"],
                            location["discovery_order"],
                            location["bank_kind"],
                            error_type,
                        ]
                    ),
                }
            )
            continue
        for key in data:
            data[key].extend(buffered[key])
    _sort_raw(data, protocol)
    common = {**_common(protocol, source_commit), "failed_seeds": failures}
    summaries, aggregates = utility_summaries(data["utility"], protocol)
    comparisons, aggregate_comparisons = control_comparisons(data["utility"], protocol, failures)
    data["banks"] = candidate_metrics(
        data["banks"], data["lineage"], data["utility"], data["causal"], protocol, failures
    )
    examples = failure_examples(
        data["banks"], data["lineage"], data["utility"], protocol, source_commit
    )
    bundle = {
        "protocol.json": copy.deepcopy(protocol),
        "candidate_lineage.jsonl": data["lineage"],
        "candidate_metrics.json": {
            **common,
            "bank_rows": data["banks"],
            "representation_checkpoints": data["checkpoints"],
            "scientific_stage_status": _stage_status(data["banks"], protocol, failures),
            "engineering_gates": _engineering(data, failures, protocol),
        },
        "held_out_utility.json": {
            **common,
            "episode_rows": data["utility"],
            "seed_summaries": summaries,
            "aggregate_rows": aggregates,
        },
        "causal_interventions.jsonl": data["causal"],
        "matched_controls.json": {
            **common,
            "control_bank_rows": data["control_banks"],
            "seed_comparisons": comparisons,
            "aggregate_comparisons": aggregate_comparisons,
        },
        "failure_examples.jsonl": examples,
    }
    bundle["report.md"] = report_text(bundle, protocol, source_commit)
    return bundle


def _validate_counts(data: dict, successes: int) -> None:
    expected = {
        "lineage": 198,
        "banks": 18,
        "checkpoints": 1,
        "utility": 1152,
        "causal": 384,
        "control_banks": 12,
    }
    for name, per_seed in expected.items():
        if len(data[name]) != per_seed * successes:
            raise ValueError(f"C16 {name} cardinality mismatch")


def _keys(value: object, names: list[str] | tuple[str, ...], label: str) -> None:
    if not isinstance(value, dict) or set(value) != set(names):
        raise ValueError(f"C16 {label} exact keys mismatch")


def _finite_tree(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("C16 nonfinite artifact number")
    if isinstance(value, dict):
        for child in value.values():
            _finite_tree(child)
    if isinstance(value, list):
        for child in value:
            _finite_tree(child)


def _same(actual: object, expected: object, label: str) -> None:
    if canonical(actual) != canonical(expected):
        raise ValueError(f"C16 {label} reconstruction mismatch")


def validate_bundle(bundle: dict, protocol: dict, source_commit: str) -> None:
    """Validate exact schemas and independently reconstruct reported summaries."""
    _keys(bundle, protocol["artifacts"]["exact_files"], "bundle")
    _finite_tree(bundle)
    _same(bundle["protocol.json"], protocol, "protocol")
    schemas = protocol["schemas"]
    metrics, utility, controls = (
        bundle[n]
        for n in ("candidate_metrics.json", "held_out_utility.json", "matched_controls.json")
    )
    for value, schema in (
        (metrics, "candidate_metrics_top_level"),
        (utility, "utility_top_level"),
        (controls, "matched_top_level"),
    ):
        _keys(value, schemas[schema], schema)
        for key, expected in _common(protocol, source_commit).items():
            _same(value[key], expected, key)
    failures = metrics["failed_seeds"]
    for other in (utility, controls):
        _same(other["failed_seeds"], failures, "common failures")
    failed_ids = []
    for row in failures:
        _keys(row, protocol["failure_and_resource_contract"]["failed_seed_fields"], "failed seed")
        if row["phase"] not in protocol["failure_and_resource_contract"]["phase_order"]:
            raise ValueError("C16 failure phase")
        if (
            isinstance(row["run_seed"], bool)
            or not isinstance(row["run_seed"], int)
            or row["run_seed"] not in protocol["seeds"]["run_seeds"]
        ):
            raise ValueError("C16 failure seed")
        for key, allowed in (
            ("representation", protocol["scope"]["primary_representations"]),
            ("discovery_order", protocol["scope"]["discovery_orders"]),
            ("bank_kind", protocol["scope"]["bank_kinds"]),
        ):
            if row[key] is not None and row[key] not in allowed:
                raise ValueError(f"C16 failure {key}")
        if not isinstance(row["error_type"], str) or not row["error_type"].strip():
            raise ValueError("C16 failure error_type")
        failed_ids.append(row["run_seed"])
        _same(
            row["error_hash"],
            digest(
                [
                    row[k]
                    for k in (
                        "phase",
                        "representation",
                        "discovery_order",
                        "bank_kind",
                        "error_type",
                    )
                ]
            ),
            "failure hash",
        )
    if failed_ids != sorted(set(failed_ids)) or not set(failed_ids) <= set(
        protocol["seeds"]["run_seeds"]
    ):
        raise ValueError("C16 failed seed identity")
    successful = sorted(set(protocol["seeds"]["run_seeds"]) - set(failed_ids))
    data = {
        "lineage": bundle["candidate_lineage.jsonl"],
        "banks": metrics["bank_rows"],
        "checkpoints": metrics["representation_checkpoints"],
        "utility": utility["episode_rows"],
        "causal": bundle["causal_interventions.jsonl"],
        "control_banks": controls["control_bank_rows"],
    }
    _validate_counts(data, len(successful))
    sorted_data = copy.deepcopy(data)
    _sort_raw(sorted_data, protocol)
    _same(data, sorted_data, "raw ordering")
    for key in ("lineage", "utility", "causal", "checkpoints"):
        if sorted({r["run_seed"] for r in data[key]}) != successful:
            raise ValueError("C16 incomplete or leaked run seed")
    _validate_raw(data, protocol, source_commit)
    expected_banks = candidate_metrics(
        data["banks"], data["lineage"], data["utility"], data["causal"], protocol, failures
    )
    _same(data["banks"], expected_banks, "candidate grades")
    summaries, aggregates = utility_summaries(data["utility"], protocol)
    _same(utility["seed_summaries"], summaries, "seed utility")
    _same(utility["aggregate_rows"], aggregates, "pooled utility")
    comparisons, aggregate_comparisons = control_comparisons(data["utility"], protocol, failures)
    _same(controls["seed_comparisons"], comparisons, "seed controls")
    _same(controls["aggregate_comparisons"], aggregate_comparisons, "bootstrap controls")
    _same(
        bundle["failure_examples.jsonl"],
        failure_examples(data["banks"], data["lineage"], data["utility"], protocol, source_commit),
        "counterexamples",
    )
    _same(
        metrics["scientific_stage_status"],
        _stage_status(data["banks"], protocol, failures),
        "stage status",
    )
    _same(metrics["engineering_gates"], _engineering(data, failures, protocol), "engineering")
    _same(bundle["report.md"], report_text(bundle, protocol, source_commit), "report")


def _validate_raw(data: dict, protocol: dict, source_commit: str) -> None:
    from .bank import ConceptBank, build_controls
    from .learning import fit_readout, predict
    from .worlds import fixture, sensory_episode

    schemas = protocol["schemas"]
    checkpoints = {c["run_seed"]: c for c in data["checkpoints"]}
    fixtures, frames_cache = {}, {}
    for seed, checkpoint in checkpoints.items():
        _keys(checkpoint, schemas["checkpoint_record"], "checkpoint")
        _same(
            checkpoint["checkpoint_hash"],
            digest({k: v for k, v in checkpoint.items() if k != "checkpoint_hash"}),
            "checkpoint hash",
        )
        if (
            checkpoint["parameter_count"] != 48
            or checkpoint["optimizer_steps"] != 20
            or len(checkpoint["epoch_losses"]) != 20
        ):
            raise ValueError("C16 encoder training budget")
        _keys(checkpoint["weights"], ["W"], "encoder weights")
        if len(checkpoint["weights"]["W"]) != 4 or any(
            len(r) != 12 for r in checkpoint["weights"]["W"]
        ):
            raise ValueError("C16 encoder shape")
        for split in ("train", "dev", "test"):
            for episode in fixture(seed, split, protocol)["episodes"]:
                fixtures[(seed, split, episode["episode_id"])] = episode

    def sensory(seed: int, split: str, episode_id: str, variant: str) -> list[dict]:
        variant = "base" if variant == "order_shuffle" else variant
        key = seed, split, episode_id, variant
        if key not in frames_cache:
            frames_cache[key] = sensory_episode(
                fixtures[(seed, split, episode_id)], variant, protocol
            )
        return frames_cache[key]

    identities = set()
    banks_by_identity, runtime = {}, {}
    for row in data["banks"]:
        _keys(row, schemas["bank_metric_row"], "bank metric")
        _keys(row["bank"], schemas["bank_identity"], "bank identity")
        bank = row["bank"]
        key = tuple(bank[k] for k in ("run_seed", "representation", "bank_kind", "discovery_order"))
        if key in identities:
            raise ValueError("C16 duplicate bank")
        identities.add(key)
        banks_by_identity[key] = row
        state = row["final_state"]
        _keys(state, schemas["bank_final_state"], "bank state")
        _same(state["bank"], bank, "state identity")
        _same(row["final_state_hash"], digest(state), "bank hash")
        _same(row["readout_hash"], digest(row["readout_coefficients"]), "readout hash")
        if len(row["slot_candidate_ids"]) != 8 or len(row["train_query_rows"]) != 256:
            raise ValueError("C16 slot/train-query budget")
        if (
            state["accepted_observation_count"] != len(state["seen_observations"])
            or len(state["seen_observations"]) > 288
        ):
            raise ValueError("C16 identity bound")
        seen_ids = []
        for observation in state["seen_observations"]:
            _keys(observation, schemas["seen_observation"], "seen observation")
            seen_ids.append(observation["observation_id"])
        if seen_ids != sorted(set(seen_ids)):
            raise ValueError("C16 duplicate/unsorted observation registry")
        candidates = state["live_candidates"] + state["retired_candidates"]
        if (
            len(candidates) != row["birth_count"]
            or row["birth_count"] > 32
            or len(state["live_candidates"]) > 8
        ):
            raise ValueError("C16 candidate bounds")
        births = {}
        for candidate in sorted(candidates, key=lambda c: c["birth_ordinal"]):
            _keys(candidate, schemas["candidate_state"], "candidate state")
            cid = candidate["candidate_id"]
            if cid in births or candidate["birth_ordinal"] != len(births):
                raise ValueError("C16 birth identity/order")
            if any(parent not in births for parent in candidate["parent_ids"]):
                raise ValueError("C16 noncausal candidate ancestry")
            births[cid] = candidate["birth_ordinal"]
            if len(candidate["retained_exemplars"]) > 32:
                raise ValueError("C16 retained exemplar bound")
            for exemplar in candidate["retained_exemplars"]:
                _keys(exemplar, schemas["exemplar_state"], "exemplar")
        for metric in row["candidates"]:
            _keys(metric, schemas["candidate_metric"], "candidate metric")
            if metric["grade"] not in protocol["grading"]["grade_values"]:
                raise ValueError("C16 candidate grade")
            if metric["qualification"] not in protocol["grading"]["qualification_values"]:
                raise ValueError("C16 candidate qualification")
        for query in row["train_query_rows"]:
            _keys(query, schemas["train_query_row"], "train query")
        if state["cc0_source_state"] is not None:
            source = state["cc0_source_state"]
            _keys(source, ["feature_counts", "pair_counts", "concepts", "id_mapping"], "CC0 source")
            for pair in source["pair_counts"]:
                _keys(pair, ["left_feature_id", "right_feature_id", "count"], "CC0 pair")
            for concept in source["concepts"]:
                _keys(
                    concept,
                    [
                        "source_candidate_id",
                        "members",
                        "strength",
                        "observations",
                        "reuse_count",
                        "first_seen",
                        "last_seen",
                    ],
                    "CC0 source concept",
                )
            for mapping in source["id_mapping"]:
                _keys(mapping, ["source_candidate_id", "candidate_id"], "CC0 mapping")

    # Replay formation from actual emitted vectors with stored train-only encoder
    # weights, not labels or next-step targets. This also audits every lifecycle event.
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    construction_rows = {}
    for row in data["lineage"]:
        schema = "lineage_episode" if row["row_kind"] == "episode" else "control_construction"
        _keys(row, schemas[schema], schema)
        for key, value in _common(protocol, source_commit).items():
            _same(row[key], value, "lineage common")
        identity = row["run_seed"], row["representation"], row["discovery_order"]
        if row["row_kind"] == "control":
            if identity in construction_rows:
                raise ValueError("C16 duplicate control construction")
            construction_rows[identity] = row
            for pattern in row["pattern_inventory"]:
                _keys(pattern, schemas["pattern_inventory_item"], "pattern")
            for reference in row["reference_banks"]:
                _keys(reference, schemas["reference_bank_construction"], "reference bank")
                for candidate in reference["references"]:
                    _keys(candidate, schemas["reference_record"], "reference")
            continue
        if row["row_kind"] != "episode" or len(row["frames"]) != 9:
            raise ValueError("C16 lineage row/frame count")
        grouped[identity].append(row)
    for (seed, representation, order), episodes in grouped.items():
        encoder = checkpoints[seed] if representation == "learned_local_prototype" else None
        primary = ConceptBank(protocol, seed, representation, order, encoder=encoder)
        peak_live = 0
        train_document = fixture(seed, "train", protocol)["episodes"]
        train_frames = [
            f for e in train_document for f in sensory(seed, "train", e["episode_id"], "base")
        ]
        _same(
            checkpoints[seed]["training_input_hash"],
            digest([f["emitted_vector"] for f in train_frames]),
            "train-only encoder inputs",
        )
        expected_episodes = list(train_document)
        if order == "episode_shuffle":
            expected_episodes.sort(
                key=lambda e: (
                    hashlib.sha256(f"c16|shuffle|{seed}|{e['episode_id']}".encode()).hexdigest(),
                    e["episode_id"],
                )
            )
        _same(
            [r["episode_id"] for r in episodes],
            [e["episode_id"] for e in expected_episodes],
            "discovery order",
        )
        for index, episode in enumerate(episodes):
            if episode["execution_episode_index"] != index:
                raise ValueError("C16 execution episode index")
            _same(episode["bank_hash_before"], primary.hash(), "episode before")
            actual_frames = sensory(seed, "train", episode["episode_id"], "base")
            for t, frame in enumerate(episode["frames"]):
                _keys(frame, schemas["lineage_frame"], "lineage frame")
                actual = actual_frames[t]
                for key in (
                    "frame_index",
                    "sample_id",
                    "input_values",
                    "emitted_vector",
                    "emitted_mask",
                    "perceptual_spark_ids",
                    "parent_sample_ids",
                    "lineage_registry_hash",
                    "sensory_state_hash_before",
                    "sensory_state_hash_after",
                    "sensory_trace",
                    "sensory_work",
                ):
                    _same(frame[key], actual[key], "sensory provenance")
                observed = primary.observe(
                    frame["emitted_vector"],
                    "ob-" + hashlib.sha256(frame["sample_id"].encode()).hexdigest()[:24],
                )
                peak_live = max(peak_live, len(primary.state()["live_candidates"]))
                for key in (
                    "global_frame_index",
                    "representation_vector",
                    "winner_id",
                    "match_score",
                    "events",
                    "bank_hash_before",
                    "bank_hash_after",
                ):
                    _same(frame[key], observed[key], "discovery replay")
                for event in frame["events"]:
                    _keys(event, schemas["lineage_event"], "lineage event")
            _same(episode["bank_hash_after"], primary.hash(), "episode after")
        primary.freeze()
        references, constructed = build_controls(primary, train_frames)
        constructed = {**constructed, **_common(protocol, source_commit), "row_kind": "control"}
        _same(construction_rows[(seed, representation, order)], constructed, "train-only controls")
        for kind, bank in {"primary": primary, **references}.items():
            key = seed, representation, kind, order
            record = banks_by_identity[key]
            _same(record["final_state"], bank.state(), "final formation state")
            _same(record["slot_candidate_ids"], bank.slot_candidate_ids, "final slots")
            state = bank.state()
            _same(record["retired_count"], len(state["retired_candidates"]), "retired count")
            _same(
                record["dormant_count"],
                sum(c["status"] == "dormant" for c in state["live_candidates"]),
                "dormant count",
            )
            _same(
                record["peak_live_count"],
                peak_live if kind == "primary" else len(state["live_candidates"]),
                "peak count",
            )
            unsupported = (
                ["update", "merge", "split", "dormancy", "deletion"]
                if kind != "primary"
                else ["merge", "split", "dormancy", "deletion", "homeostasis"]
                if representation == "cc0_assembly"
                else []
            )
            _same(record["unsupported_operations"], unsupported, "unsupported operations")
            representation_hash = (
                checkpoints[seed]["checkpoint_hash"]
                if encoder
                else digest(protocol["representations"][representation])
            )
            _same(record["representation_hash"], representation_hash, "representation commitment")
            queries, targets = [], []
            for episode in train_document:
                for t, frame in enumerate(
                    sensory(seed, "train", episode["episode_id"], "base")[:8]
                ):
                    queries.append(
                        {
                            "episode_id": episode["episode_id"],
                            "world": episode["world"],
                            "t": t,
                            "sample_id": frame["sample_id"],
                            "context": frame["context"],
                            **bank.query(frame["emitted_vector"]),
                        }
                    )
                    targets.append(episode["frames"][t + 1]["base_values"])
            _same(record["train_query_rows"], queries, "frozen train query")
            coefficients = fit_readout(queries, targets)
            _same(record["readout_coefficients"], coefficients, "train-only ridge")
            slots = [cid for cid in bank.slot_candidate_ids if cid is not None]
            usage = dict(
                sorted((cid, sum(q["winner_id"] == cid for q in queries)) for cid in slots)
            )
            _same(record["train_usage_counts"], usage, "train usage")
            selection = select_interventions(
                queries, slots, run_seed=seed, representation=representation, protocol=protocol
            )
            runtime[key] = bank, coefficients, selection, record["representation_hash"]
    seen_utility = set()
    for row in data["utility"]:
        _keys(row, schemas["utility_episode"], "utility episode")
        seed, split, eid, variant = (row[k] for k in ("run_seed", "split", "episode_id", "variant"))
        identity = seed, split, eid, variant, row["cell"]
        if identity in seen_utility:
            raise ValueError("C16 duplicate utility row")
        seen_utility.add(identity)
        representation, kind = row["cell"].split("/")
        order = protocol["scope"]["variant_to_bank_order"][variant]
        bank, coefficients, _, representation_hash = runtime[(seed, representation, kind, order)]
        episode = fixtures[(seed, split, eid)]
        _same(row["world"], episode["world"], "utility world")
        _same(row["bank_order"], order, "variant bank order")
        _same(row["bank_hash"], bank.hash(), "utility bank hash")
        _same(row["readout_hash"], digest(coefficients), "utility readout hash")
        _same(row["representation_hash"], representation_hash, "utility representation hash")
        steps = _predict_steps(bank, coefficients, sensory(seed, split, eid, variant), episode)
        _same(row["steps"], steps, "held-out predictions")
        for step in row["steps"]:
            _keys(step, schemas["utility_step"], "utility step")
            raw, prediction = predict(coefficients, step["slot_index"])
            _same(step["raw_prediction"], raw, "raw prediction")
            _same(step["prediction"], prediction, "clipped prediction")
        total = sum(s["squared_error_sum"] for s in steps)
        _same(row["squared_error_sum"], total, "episode error")
        _same(row["denominator"], 96, "episode denominator")
        _same(row["mse"], total / 96, "episode MSE")
    expected_causal = []
    for (seed, _representation, kind, order), (
        bank,
        coefficients,
        selection,
        representation_hash,
    ) in runtime.items():
        if kind != "primary" or order != "canonical":
            continue
        for (s, split, eid), episode in fixtures.items():
            if s == seed and split == "test":
                expected_causal.extend(
                    _causal_rows(
                        bank,
                        coefficients,
                        episode,
                        sensory(seed, "test", eid, "base"),
                        selection,
                        representation_hash,
                        protocol,
                        source_commit,
                    )
                )
    expected_causal.sort(
        key=lambda r: (
            r["run_seed"],
            protocol["scope"]["primary_representations"].index(r["representation"]),
            r["episode_id"],
            r["slot_index"],
        )
    )
    actual_causal = sorted(
        data["causal"],
        key=lambda r: (
            r["run_seed"],
            protocol["scope"]["primary_representations"].index(r["representation"]),
            r["episode_id"],
            r["slot_index"],
        ),
    )
    _same(actual_causal, expected_causal, "causal intervention replay")
    for row in data["causal"]:
        _keys(row, schemas["causal_episode_slot"], "causal slot")
        for branch in (
            "baseline",
            "targeted_suppression",
            "matched_random_suppression",
            "substitution",
        ):
            _keys(row[branch], schemas["intervention_branch"], "intervention branch")
    for row in data["control_banks"]:
        _keys(row, schemas["control_bank_metric"], "matched control bank")
        key = tuple(
            row["bank"][k] for k in ("run_seed", "representation", "bank_kind", "discovery_order")
        )
        record = banks_by_identity[key]
        primary = banks_by_identity[(key[0], key[1], "primary", key[3])]
        reference = next(
            r
            for r in construction_rows[(key[0], key[1], key[3])]["reference_banks"]
            if r["bank_kind"] == key[2]
        )
        expected = {
            "bank": record["bank"],
            "primary_bank_hash": primary["final_state_hash"],
            "control_bank_hash": record["final_state_hash"],
            "primary_count": reference["primary_count"],
            "reference_count": reference["reference_count"],
            "slot_budget": 8,
            "member_sizes": [
                len(c["member_feature_ids"]) for c in record["final_state"]["live_candidates"]
            ],
            "train_usage_counts": record["train_usage_counts"],
            "shortfall": reference["shortfall"],
            "selection_pattern_ids": reference["selection_order_pattern_ids"],
        }
        _same(row, expected, "matched control bank")
    expected_control_identities = {
        (seed, representation, kind, order)
        for seed in checkpoints
        for representation in protocol["scope"]["primary_representations"]
        for kind in ("matched_random", "frequency_topk")
        for order in protocol["scope"]["discovery_orders"]
    }
    actual_control_identities = {
        tuple(
            row["bank"][key]
            for key in ("run_seed", "representation", "bank_kind", "discovery_order")
        )
        for row in data["control_banks"]
    }
    if actual_control_identities != expected_control_identities or len(
        actual_control_identities
    ) != len(data["control_banks"]):
        raise ValueError("C16 matched-control identity set")
