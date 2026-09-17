"""Target-free atomic_idx source-map binding for prospective C19-R2 inference."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.belief_r import BeliefRPair
from sparkbrain.v03_external_validation.c19_r2_protocol import EXPECTED_PAIRS

SOURCE_MAP_SCHEMA_VERSION = "1"
SOURCE_MAP_CLUSTER_KEY = "atomic_idx"
SourceMapEntry = dict[str, object]


def validate_atomic_idx_source_map(
    entries: Sequence[Mapping[str, Any]],
) -> tuple[SourceMapEntry, ...]:
    if len(entries) != EXPECTED_PAIRS:
        raise ValueError("R2 atomic_idx source map must contain exactly 1744 pairs")
    normalized: dict[int, SourceMapEntry] = {}
    for value in entries:
        if set(value) != {"pair_index", "atomic_idx"}:
            raise ValueError("R2 atomic_idx source-map fields drift")
        pair_index = value["pair_index"]
        if isinstance(pair_index, bool) or not isinstance(pair_index, int) or pair_index < 0:
            raise ValueError("R2 source-map pair_index must be a non-negative integer")
        atomic_idx = value["atomic_idx"]
        if not isinstance(atomic_idx, str) or not atomic_idx.strip():
            raise ValueError("R2 source-map atomic_idx must be a non-empty string")
        if pair_index in normalized:
            raise ValueError("duplicate R2 source-map pair assignment")
        normalized[pair_index] = {"pair_index": pair_index, "atomic_idx": atomic_idx}
    if set(normalized) != set(range(EXPECTED_PAIRS)):
        raise ValueError("R2 atomic_idx source map is not total")
    return tuple(normalized[index] for index in range(EXPECTED_PAIRS))


def _artifact_bytes(entries: Sequence[Mapping[str, Any]]) -> bytes:
    normalized = validate_atomic_idx_source_map(entries)
    payload = {
        "schema_version": SOURCE_MAP_SCHEMA_VERSION,
        "cluster_key": SOURCE_MAP_CLUSTER_KEY,
        "pair_assignment": "exactly_once",
        "target_fields_materialized": False,
        "entries": [dict(entry) for entry in normalized],
    }
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def build_atomic_idx_source_map(pairs: Sequence[BeliefRPair]) -> tuple[SourceMapEntry, ...]:
    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError("R2 atomic_idx source map requires exactly 1744 pairs")
    entries = []
    for pair_index, pair in enumerate(pairs):
        before = pair.time_t.atomic_idx
        after = pair.time_t1.atomic_idx
        if not before.strip() or before != after:
            raise ValueError("R2 pair must bind to one non-empty atomic_idx cluster")
        entries.append({"pair_index": pair_index, "atomic_idx": before})
    return validate_atomic_idx_source_map(entries)


def atomic_idx_source_map_sha256(entries: Sequence[Mapping[str, Any]]) -> str:
    return hashlib.sha256(_artifact_bytes(entries)).hexdigest()


def atomic_idx_clusters(
    entries: Sequence[Mapping[str, Any]],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    normalized = validate_atomic_idx_source_map(entries)
    clusters: dict[str, list[int]] = {}
    for entry in normalized:
        atomic_idx = str(entry["atomic_idx"])
        clusters.setdefault(atomic_idx, []).append(int(entry["pair_index"]))
    if not clusters:
        raise ValueError("R2 atomic_idx source map has no clusters")
    return tuple((key, tuple(indices)) for key, indices in clusters.items())


def write_atomic_idx_source_map_no_clobber(
    path: Path,
    pairs: Sequence[BeliefRPair],
) -> tuple[tuple[SourceMapEntry, ...], str]:
    entries = build_atomic_idx_source_map(pairs)
    payload = _artifact_bytes(entries)
    digest = hashlib.sha256(payload).hexdigest()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)
    return entries, digest


def read_atomic_idx_source_map(
    path: Path,
    *,
    expected_sha256: str,
) -> tuple[SourceMapEntry, ...]:
    payload = path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError("R2 atomic_idx source-map digest mismatch")
    value = json.loads(payload.decode("utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("R2 atomic_idx source-map artifact must be a mapping")
    if value.get("schema_version") != SOURCE_MAP_SCHEMA_VERSION:
        raise ValueError("R2 atomic_idx source-map schema drift")
    if value.get("cluster_key") != SOURCE_MAP_CLUSTER_KEY:
        raise ValueError("R2 atomic_idx source-map cluster key drift")
    if value.get("pair_assignment") != "exactly_once":
        raise ValueError("R2 atomic_idx source-map assignment contract drift")
    if value.get("target_fields_materialized") is not False:
        raise ValueError("R2 atomic_idx source map must remain target-free")
    entries = value.get("entries")
    if not isinstance(entries, list) or not all(isinstance(entry, Mapping) for entry in entries):
        raise ValueError("R2 atomic_idx source-map entries missing")
    normalized = validate_atomic_idx_source_map(entries)
    if _artifact_bytes(normalized) != payload:
        raise ValueError("R2 atomic_idx source-map artifact is not canonical")
    return normalized


__all__ = [
    "SOURCE_MAP_CLUSTER_KEY",
    "SOURCE_MAP_SCHEMA_VERSION",
    "atomic_idx_clusters",
    "atomic_idx_source_map_sha256",
    "build_atomic_idx_source_map",
    "read_atomic_idx_source_map",
    "validate_atomic_idx_source_map",
    "write_atomic_idx_source_map_no_clobber",
]
