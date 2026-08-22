from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..tasks import Episode, generate_episode


def load_split_manifest(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "0.2" or not value.get("frozen"):
        raise ValueError("C05 requires a frozen C02 split manifest")
    return value


def episodes_from_manifest(
    manifest: dict[str, object], *, worlds: list[str], steps: int, limit: int | None = None
) -> list[Episode]:
    count = int(manifest["episode_count"])
    if limit is not None:
        count = min(count, limit)
    start = int(manifest["seed_start"])
    split = str(manifest["split"])
    return [
        generate_episode(world, seed=start + index, split=split, steps=steps)
        for world in worlds
        for index in range(count)
    ]


def episode_manifest_hash(episodes: list[Episode]) -> str:
    payload = [episode.canonical_json() for episode in episodes]
    return hashlib.sha256("\n".join(payload).encode("utf-8")).hexdigest()


def split_dev_episodes(episodes: list[Episode]) -> tuple[list[Episode], list[Episode]]:
    ordered = sorted(episodes, key=lambda episode: episode.episode_id)
    train = ordered[::2]
    selection = ordered[1::2]
    if not train or not selection:
        raise ValueError("At least two dev episodes are required")
    return train, selection
