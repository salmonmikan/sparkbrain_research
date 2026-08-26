"""Frozen C16 pure fixtures and the C12/C13 perceptual boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":"))


def digest(value: object) -> str:
    return text_hash(canonical(value))


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _uniform(value: str) -> float:
    return int(text_hash(value)[:13], 16) / float(2**52)


def protocol_document() -> dict:
    path = Path(__file__).resolve().parents[3] / "artifacts/v03/c16_proto_concepts/protocol.json"
    return json.loads(path.read_text(encoding="utf-8"))


def fixture(run_seed: int, split: str, protocol: dict | None = None) -> dict:
    p = protocol_document() if protocol is None else protocol
    if isinstance(run_seed, bool) or not isinstance(run_seed, int):
        raise ValueError("run_seed must be an integer")
    if run_seed not in p["seeds"]["run_seeds"] + p["seeds"]["reserved_test_seeds"]:
        raise ValueError("unregistered run_seed")
    world_spec = p["world_generator"]
    if split not in world_spec["episodes_per_world"]:
        raise ValueError("unregistered split")
    episodes = []
    for wi, world in enumerate(world_spec["world_order"]):
        for i in range(world_spec["episodes_per_world"][split]):
            prefix = f"c16|episode|{run_seed}|{split}|{world}|{i}"
            episode_id = "ep-" + text_hash(prefix)[:24]
            row = {
                "run_seed": run_seed, "split": split, "world": world,
                "episode_index": i,
                "episode_seed": p["seeds"]["split_seed_bases"][split]
                + 1000 * (run_seed - 3601) + 100 * wi + i,
                "episode_id": episode_id,
            }
            frames = []
            for t in range(world_spec["frames_per_episode"]):
                phase = (i + (run_seed - 3601) + t) % 3
                context = (phase + 2) % 3 if split == "test" else (phase + i % 2) % 3
                foreground = world_spec["base_foreground"][world][phase]
                values = [0.0] * 12
                for j in foreground:
                    values[j] = 1.0
                values[6 + context] = 0.25
                if world == "frequency_distractor":
                    values[9] = 1.0
                elif world == "decoy_reversal":
                    values[9 + ((phase + 1) % 3 if split == "test" else phase)] = 0.75
                for j, value in enumerate(values):
                    if value:
                        key = f"c16|amplitude|{run_seed}|{split}|{world}|{i}|{t}|{j}"
                        values[j] = min(1.0, max(0.0, value + .02 * (2 * _uniform(key) - 1)))
                frames.append({
                    "t": t, "sample_id": "sa-" + text_hash(f"{episode_id}|frame|{t}")[:24],
                    "source_id": "src-" + text_hash(episode_id + "|sensor")[:24],
                    "correlation_group": "cg-" + text_hash(episode_id + "|stream")[:24],
                    "base_values": values, "foreground_indices": list(foreground),
                    "phase": phase, "context": context,
                })
            episodes.append({**row, "frames": frames})
    return {"schema_version": "0.3", "run_seed": run_seed, "split": split,
            "episodes": episodes}


def split_manifest(run_seed: int, split: str, protocol: dict | None = None) -> list[dict]:
    return [{key: value for key, value in row.items() if key != "frames"}
            for row in fixture(run_seed, split, protocol)["episodes"]]


def variant_values(frame: dict, variant: str) -> list[float]:
    values = list(frame["base_values"])
    sample_id = frame["sample_id"]
    if variant == "amplitude_perturbation":
        for j, value in enumerate(values):
            if value:
                noise = .02 * (2 * _uniform(f"c16|perturb|{sample_id}|{j}") - 1)
                values[j] = min(1.0, max(0.0, value + noise))
    elif variant == "irrelevant_distractor":
        eligible = [j for j in (9, 10, 11) if values[j] == 0]
        chosen = min(eligible, key=lambda j: text_hash(f"c16|distractor|{sample_id}|{j}"))
        values[chosen] = .2
    elif variant not in ("base", "order_shuffle"):
        raise ValueError("unregistered variant")
    return values


def sensory_episode(episode: dict, variant: str, protocol: dict) -> list[dict]:
    # Import runtime only here: pure official fixture hashes never execute sensory code.
    from sparkbrain.v03_seed.contracts import SensorySample
    from sparkbrain.v03_seed.evidence import EvidenceLedger
    from sparkbrain.v03_seed.sensory_field import AdaptiveSensoryField, SensoryFieldConfig

    field = AdaptiveSensoryField(SensoryFieldConfig(**protocol["scope"]["sensory_config"]))
    ledger = EvidenceLedger()
    channels = protocol["world_generator"]["channels"]
    modality = protocol["world_generator"]["modality"]
    feature_index = {f"{modality}:{name}": j for j, name in enumerate(channels)}
    result = []
    for frame in episode["frames"]:
        values = variant_values(frame, variant)
        sample = SensorySample(
            sample_id=frame["sample_id"], time=frame["t"], source_id=frame["source_id"],
            modality=modality, values=dict(zip(channels, values, strict=True)),
            correlation_group=frame["correlation_group"], entity_hint=None,
            metadata={}, omitted_channels=(),
        )
        observation = field.observe_with_trace(sample, goal_bias=None, ablations=None, bypass=False)
        ledger.register_sample(sample.sample_id)
        emitted, mask, parents = [0.0] * 12, [False] * 12, set()
        for spark in sorted(observation.sparks, key=lambda row: row.spark_id):
            lineage = tuple(sorted(spark.parents))
            if lineage != (sample.sample_id,):
                raise ValueError("unexpected perceptual lineage")
            ledger.register_spark(spark.spark_id, lineage)
            parents.update(lineage)
            index = feature_index[spark.feature_id]
            emitted[index] = min(1.0, max(0.0, float(spark.activation)))
            mask[index] = True
        result.append({
            "episode_id": episode["episode_id"], "frame_index": frame["t"],
            "sample_id": sample.sample_id, "input_values": values,
            "emitted_vector": emitted, "emitted_mask": mask,
            "perceptual_spark_ids": sorted(s.spark_id for s in observation.sparks),
            "parent_sample_ids": sorted(parents),
            "lineage_registry_hash": text_hash(ledger.serialize_state()),
            "sensory_trace": [r.as_dict() for r in sorted(
                observation.channel_trace, key=lambda row: row.feature_id)],
            "sensory_work": observation.work_delta.as_dict(),
            "sensory_state_hash_before": observation.state_hash_before,
            "sensory_state_hash_after": observation.state_hash_after, "context": frame["context"],
        })
    return result
