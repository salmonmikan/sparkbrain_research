"""Frozen, model-free C17 fixture construction."""

from __future__ import annotations

from typing import Any

from .contracts import digest, text_hash


def _uniform(text: str) -> float:
    return int(text_hash(text)[:13], 16) / float(2**52)


def _identity(kind: str, preimage: str) -> str:
    prefixes = {
        "sample": "sa-",
        "source": "src-",
        "group": "cg-",
        "entity": "en-",
        "hypothesis": "hy-",
        "action": "ac-",
    }
    return prefixes[kind] + text_hash(preimage)[:24]


def _frame(
    protocol: dict[str, Any],
    run_seed: int,
    split: str,
    compositionality: int,
    episode_index: int,
    episode_id: str,
    t: int,
) -> dict[str, Any]:
    function_index = episode_index % 4
    if compositionality == 2:
        composition = [function_index, (function_index + (2 if split == "heldout" else 1)) % 4]
    else:
        composition = [
            function_index,
            (function_index + 2) % 4 if split == "heldout" else (function_index + 1) % 4,
            (function_index + 3) % 4 if split == "heldout" else (function_index + 2) % 4,
        ]
    segment_length = 12 // compositionality
    function_index = composition[t // segment_length]
    local_step = t % segment_length
    target_bit = (run_seed + episode_index + function_index) % 2
    entity_index = (episode_index + local_step) % 2
    values = [0.0] * 12
    if function_index == 0:
        if local_step == 0:
            values[target_bit] = 1.0
        if local_step == segment_length - 1:
            values[10] = 0.4
    elif function_index == 1:
        values[2 + (target_bit ^ entity_index)] = 1.0
    elif function_index == 2:
        channel = 4 + (1 - target_bit if local_step == segment_length - 2 else target_bit)
        values[channel] = 1.0
    else:
        values[6 + ((target_bit + local_step) % 2)] = 1.0
    values[8 + entity_index] = max(values[8 + entity_index], 0.35)
    for j, value in enumerate(values):
        if value:
            key = (
                f"c17v2|amplitude|{run_seed}|{split}|composition{compositionality}|"
                f"{episode_index}|{t}|{j}"
            )
            values[j] = min(1.0, max(0.0, value + 0.02 * (2 * _uniform(key) - 1)))
    return {
        "t": t,
        "sample_id": _identity("sample", f"{episode_id}|frame|{t}"),
        "source_id": _identity("source", f"{episode_id}|sensor"),
        "correlation_group": _identity("group", f"{episode_id}|stream"),
        "base_values": values,
        "evaluator_function_index": function_index,
        "evaluator_entity_index": entity_index,
        "evaluator_target_bit": target_bit,
        "scoring": local_step == segment_length - 1,
        "entity_key": _identity("entity", f"{episode_id}|entity|{entity_index}"),
        "hypothesis_ids": [
            _identity("hypothesis", f"{episode_id}|hypothesis|{bit}") for bit in (0, 1)
        ],
        "action_ids": [_identity("action", f"{episode_id}|action|{bit}") for bit in (0, 1)],
    }


def fixture_document(
    run_seed: int,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    spec = protocol["fixtures"]
    allowed = spec["run_seeds"] + spec["reserved_test_seeds"]
    if isinstance(run_seed, bool) or not isinstance(run_seed, int) or run_seed not in allowed:
        raise ValueError("unregistered C17 run seed")
    rows = []
    for condition in protocol["resource_conditions"]["rows"]:
        compositionality = condition["task_compositionality"]
        splits = []
        for split in ("train", "dev", "test", "heldout"):
            episodes = []
            for episode_index in range(spec["episodes_per_split"][split]):
                episode_id = (
                    "ep-"
                    + text_hash(
                        f"c17v2|episode|{run_seed}|{split}|composition{compositionality}|{episode_index}"
                    )[:24]
                )
                episode_seed = (
                    spec["split_seed_bases"][split]
                    + 1000 * (run_seed - spec["run_seeds"][0])
                    + 100 * (compositionality - 2)
                    + episode_index
                )
                composition_start = episode_index % 4
                if compositionality == 2:
                    composition = [
                        composition_start,
                        (composition_start + (2 if split == "heldout" else 1)) % 4,
                    ]
                else:
                    composition = [
                        composition_start,
                        (composition_start + (2 if split == "heldout" else 1)) % 4,
                        (composition_start + (3 if split == "heldout" else 2)) % 4,
                    ]
                frames = [
                    _frame(
                        protocol,
                        run_seed,
                        split,
                        compositionality,
                        episode_index,
                        episode_id,
                        t,
                    )
                    for t in range(spec["frames_per_episode"])
                ]
                episodes.append(
                    {
                        "run_seed": run_seed,
                        "split": split,
                        "fixture_variant": f"composition{compositionality}",
                        "episode_index": episode_index,
                        "episode_seed": episode_seed,
                        "episode_id": episode_id,
                        "composition_indices": composition,
                        "frames": frames,
                    }
                )
            splits.append({"split": split, "episodes": episodes})
        rows.append({"condition_id": condition["condition_id"], "splits": splits})
    return {
        "schema_version": protocol["schema_version"],
        "protocol_id": protocol["protocol_id"],
        "run_seed": run_seed,
        "cells": rows,
    }


def fixture_manifest(run_seed: int, protocol: dict[str, Any]) -> dict[str, Any]:
    document = fixture_document(run_seed, protocol)
    return {
        "schema_version": document["schema_version"],
        "protocol_id": document["protocol_id"],
        "run_seed": run_seed,
        "cells": [
            {
                "condition_id": cell["condition_id"],
                "splits": [
                    {
                        "split": split["split"],
                        "episodes": [
                            {
                                **{key: value for key, value in episode.items() if key != "frames"},
                                "frame_count": len(episode["frames"]),
                            }
                            for episode in split["episodes"]
                        ],
                    }
                    for split in cell["splits"]
                ],
            }
            for cell in document["cells"]
        ],
    }


def fixture_hashes(run_seed: int, protocol: dict[str, Any]) -> tuple[str, str]:
    return digest(fixture_document(run_seed, protocol)), digest(
        fixture_manifest(run_seed, protocol)
    )
