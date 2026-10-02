#!/usr/bin/env python3
"""Model-free literal preparation and input reduction, not a pilot execution runner.

Only immutable PR182 JSON members are read. No model, checkpoint, producer, M1,
random generator, or historical runner is imported or invoked. The returned
literals are prospective inputs, never observations of successful execution.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import io
import json
import math
import re
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/research/assembly_m1_path_v1_20261002"
SOURCE = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
ARCHIVE_SHA256 = "2dfbe4f3afb8b046c1b465dcb52461daa027f72939dd85cf7dfad15670947082"
SOURCE_MEMBERS = {
    "run/inputs-910071-prefix.json": (
        "e464364135a1f42e4cc0527f6e6fc5a08b5784d169f6202b4aa138e93d6c5661"
    ),
    "run/inputs-910071-pairs.json": (
        "b9c673bb08ad4e2401667a0ced819dadc6a4a9fab5708b0c82df6122d53d30b3"
    ),
}
CHANNELS = tuple("ACFHIJKLMQ")
FEATURE_WIDTH = 7
WINDOW_MS = 40.0
DECISION_OFFSET_MS = 72.0
OUTCOME_OFFSET_MS = 100.0
OBSERVATION_KEYS = frozenset({"occurrence_id", "start_ms", "pulses"})
PULSE_KEYS = frozenset(
    {
        "channel",
        "location",
        "magnitude",
        "metadata",
        "novelty",
        "polarity",
        "prediction_error",
        "source_id",
        "time_ms",
    }
)


class InputContractError(ValueError):
    """A malformed/causally invalid observation or explicit raw-domain rejection."""

    def __init__(self, status: str, message: str) -> None:
        self.status = status
        super().__init__(f"{status}: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def encoded(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _finite(value: Any, name: str) -> float:
    if type(value) not in (int, float):
        raise InputContractError("malformed_input", f"{name} must be a non-boolean number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise InputContractError("malformed_input", f"{name} must be finite") from exc
    if not math.isfinite(result):
        raise InputContractError("malformed_input", f"{name} must be finite")
    return result


def _exact_keys(value: Any, keys: frozenset[str], name: str) -> None:
    if type(value) is not dict or set(value) != keys:
        raise InputContractError("malformed_input", f"{name} has unexpected fields")


def validate_observation(observation: dict[str, Any]) -> None:
    """Check every pulse before any reduction or future component advance.

    A/C zero magnitude and negative polarity are valid literal pulse syntax but
    outside the raw encoder's domain. Negative cue magnitude is also reported as
    out_of_domain; it never reaches a producer. Malformed/future pulses anywhere
    in the list take priority over such domain rejection.
    """
    _exact_keys(observation, OBSERVATION_KEYS, "observation")
    identity = observation["occurrence_id"]
    if type(identity) is not str or re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", identity) is None:
        raise InputContractError("malformed_input", "invalid opaque occurrence_id")
    start = _finite(observation["start_ms"], "start_ms")
    cutoff = start + WINDOW_MS
    if start < 0 or not math.isfinite(cutoff) or cutoff <= start:
        raise InputContractError("malformed_input", "invalid finite nonnegative window")
    pulses = observation["pulses"]
    if type(pulses) is not list:
        raise InputContractError("malformed_input", "pulses must be a list")
    invalid_cue = False
    for index, pulse in enumerate(pulses):
        _exact_keys(pulse, PULSE_KEYS, f"pulse[{index}]")
        channel = pulse["channel"]
        if type(channel) is not str or channel not in CHANNELS:
            raise InputContractError("malformed_input", "unknown channel")
        at = _finite(pulse["time_ms"], "pulse time_ms")
        if at < start or at > cutoff:
            raise InputContractError("causal_input_violation", "pulse outside inclusive window")
        magnitude = _finite(pulse["magnitude"], "pulse magnitude")
        polarity = pulse["polarity"]
        if type(polarity) is not int or polarity not in (-1, 1):
            raise InputContractError("malformed_input", "polarity must be integer -1 or +1")
        if (
            pulse["source_id"] != "probe-input"
            or type(pulse["source_id"]) is not str
            or type(pulse["metadata"]) is not dict
            or pulse["metadata"]
            or pulse["location"] is not None
        ):
            raise InputContractError("malformed_input", "pulse provenance/metadata contract")
        if (
            _finite(pulse["novelty"], "novelty") != 0.0
            or _finite(pulse["prediction_error"], "prediction_error") != 0.0
        ):
            raise InputContractError("malformed_input", "pulse modulation contract")
        if channel in ("A", "C"):
            invalid_cue |= magnitude <= 0.0 or polarity != 1
        elif magnitude < 0.0 or polarity != 1:
            raise InputContractError("malformed_input", "non-cue pulse magnitude/polarity")
    if invalid_cue:
        raise InputContractError("out_of_domain", "A/C requires positive magnitude and polarity +1")


def encode_raw_order(observation: dict[str, Any]) -> dict[str, Any]:
    """Fixed seven slots from strict A/C time order, with no tolerance or labels."""
    try:
        validate_observation(observation)
    except InputContractError as exc:
        if exc.status == "out_of_domain":
            return {"status": "out_of_domain", "vector": None}
        raise
    a = [pulse for pulse in observation["pulses"] if pulse["channel"] == "A"]
    c = [pulse for pulse in observation["pulses"] if pulse["channel"] == "C"]
    if len(a) != 1 or len(c) != 1:
        return {"status": "out_of_domain", "vector": None}
    if a[0]["time_ms"] == c[0]["time_ms"]:
        return {"status": "ambiguous_order", "vector": None}
    vector = [0.0] * FEATURE_WIDTH
    vector[0 if a[0]["time_ms"] < c[0]["time_ms"] else 1] = 1.0
    return {"status": "accepted", "vector": vector}


def raster(observation: dict[str, Any]) -> list[float]:
    """Retain PR182's 10 by 41 floor/ceil interpolation and mass normalization."""
    validate_observation(observation)
    values = [0.0] * (41 * len(CHANNELS))
    for pulse in observation["pulses"]:
        relative = pulse["time_ms"] - observation["start_ms"]
        at = CHANNELS.index(pulse["channel"]) * 41
        lower = math.floor(relative)
        fraction = relative - lower
        values[at + lower] += pulse["magnitude"] * (1 - fraction)
        if fraction:
            values[at + lower + 1] += pulse["magnitude"] * fraction
    # Fix binary64 addition order; Python 3.12 changed builtin sum's float algorithm.
    # This audit raster never supplies the seven-coordinate raw M1 representation.
    total = 0.0
    for value in values:
        total += value
    if not math.isfinite(total) or total <= 0:
        raise InputContractError("malformed_input", "raster requires finite positive mass")
    return [value / total for value in values]


def _features(values: Any, inlet: str) -> list[float]:
    if type(values) not in (list, tuple) or len(values) != FEATURE_WIDTH:
        raise InputContractError("malformed_input", f"{inlet} requires exactly seven coordinates")
    result = [_finite(value, inlet) for value in values]
    if any(value < 0.0 or value > 1.0 for value in result):
        raise InputContractError("malformed_input", f"{inlet} coordinates must be in [0,1]")
    return result


def adapt(
    observation: dict[str, Any],
    predictive_features: list[float] | tuple[float, ...],
    routing_features: list[float] | tuple[float, ...],
) -> dict[str, Any]:
    """Make a detached primitive M1 wire payload; this never creates or calls M1."""
    validate_observation(observation)
    predictive = _features(predictive_features, "predictive")
    routing = _features(routing_features, "routing")
    return {
        "event_id": observation["occurrence_id"],
        "time": (observation["start_ms"] + DECISION_OFFSET_MS) / 1000.0,
        "sensory_values": {
            "signal": 0.0,
            **{f"temporal_{index:03d}": value for index, value in enumerate(predictive)},
        },
        "routing_features": [0.0, *routing],
    }


def read_source_literals() -> dict[str, Any]:
    """Hash-check transport and selected literal members without extracting files."""
    manifest = json.loads((SOURCE / "transport_manifest.json").read_bytes())
    require(manifest["archive_sha256"] == ARCHIVE_SHA256, "PR182 archive pin changed")
    chunks = []
    for index, part in enumerate(manifest["parts"]):
        require(part["path"] == f"evidence.part{index:03d}.b64", "transport order")
        raw = (SOURCE / part["path"]).read_bytes()
        require(sha(raw) == part["encoded_sha256"], "encoded transport digest")
        decoded = base64.b64decode(b"".join(raw.split()), validate=True)
        require(
            sha(decoded) == part["sha256"] and len(decoded) == part["bytes"],
            "decoded transport digest/size",
        )
        chunks.append(decoded)
    payload = b"".join(chunks)
    require(
        sha(payload) == ARCHIVE_SHA256 and len(payload) == manifest["archive_bytes"],
        "PR182 archive digest/size",
    )
    result = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        seen = set()
        for member in archive:
            path = PurePosixPath(member.name)
            require(
                member.isfile()
                and not path.is_absolute()
                and ".." not in path.parts
                and member.name not in seen,
                "unsafe or duplicate archive member",
            )
            seen.add(member.name)
            if member.name in SOURCE_MEMBERS:
                stream = archive.extractfile(member)
                require(stream is not None, "missing literal member")
                raw = stream.read()
                require(sha(raw) == SOURCE_MEMBERS[member.name], "PR182 literal member pin")
                result[member.name] = json.loads(raw)
    require(set(result) == set(SOURCE_MEMBERS), "literal member inventory")
    return result


def _literal(source: dict[str, Any], cycle: int, start: float) -> dict[str, Any]:
    shift = start - source["start_ms"]
    pulses = copy.deepcopy(source["pulses"])
    if shift != 0.0:
        for pulse in pulses:
            pulse["time_ms"] += shift
    return {"occurrence_id": f"m1-path-20261002-{cycle:06d}", "start_ms": start, "pulses": pulses}


def make_inputs(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Use all first-seed prefix literals and exactly the first paired query fixture."""
    prefix = source["run/inputs-910071-prefix.json"]
    pair = source["run/inputs-910071-pairs.json"][0]
    require(len(prefix) == 64 and len(pair) == 2, "one 64-window prefix and one pair")
    rows = [_literal(row, index, row["start_ms"]) for index, row in enumerate(prefix)]
    for cue, cycle, start in (
        (0, 64, 12800.0),
        (1, 65, 13000.0),
        (0, 66, 13200.0),
        (1, 66, 13200.0),
    ):
        rows.append(_literal(pair[cue], cycle, start))
    require(len(rows) == 68, "producer window inventory")
    for row in rows:
        require(len(row["pulses"]) == 6, "six raw pulses per literal window")
        require(encode_raw_order(row)["status"] == "accepted", "literal raw-order domain")
    return rows


def make_evaluator(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep targets, signed teaching feedback, audit labels and rasters outside inputs."""
    teaching = []
    for index, label, outcome in ((64, "A", 0.8), (65, "B", -0.8)):
        row = rows[index]
        teaching.append(
            {
                "input_index": index,
                "audit_label": label,
                "event_id": row["occurrence_id"],
                "outcome": outcome,
                "decision_time_ms": row["start_ms"] + DECISION_OFFSET_MS,
                "delivery_time_ms": row["start_ms"] + OUTCOME_OFFSET_MS,
                "receipt_ids": {
                    arm: f"m1-path-20261002-{arm}-receipt-{index:06d}" for arm in ("S", "R")
                },
            }
        )
    queries = []
    for index, label, action, outcome in ((66, "A", "act_alpha", 0.8), (67, "B", "act_beta", -0.8)):
        row = rows[index]
        queries.append(
            {
                "input_index": index,
                "audit_label": label,
                "target_action": action,
                "signed_outcome_target": outcome,
                "event_id": row["occurrence_id"],
                "decision_time_ms": row["start_ms"] + DECISION_OFFSET_MS,
                "beforestate": "same_post_teaching_owner_independent_candidate",
                "feedback_allowed": False,
            }
        )
    return {
        "schema_version": 1,
        "classification": "SOURCE_ONLY_UNEXECUTED_NONCANONICAL_NON_EVIDENTIARY",
        "execution_authorized": False,
        "scientific_credit": 0,
        "source": {
            "prefix_seed": 910071,
            "pair_index": 0,
            "selection": "first_declared",
            "archive_sha256": ARCHIVE_SHA256,
            "member_sha256": SOURCE_MEMBERS,
        },
        "producer_windows": 68,
        "acquisition_input_indices": list(range(64)),
        "time_origin_ms": 0.0,
        "input_cutoff_offset_ms": WINDOW_MS,
        "decision_offset_ms": DECISION_OFFSET_MS,
        "current_input": {"sensory_values": {"signal": 0.0}, "routing_features": [0.0]},
        "teaching": teaching,
        "queries": queries,
        "controls": {
            "producer_advances": 0,
            "feedback_allowed": False,
            "inlets": [["A", "B"], ["B", "A"], ["A", "A"]],
            "observation_binding_from_input_index": 66,
            "sham_copies_complete_factual_A_observation": True,
        },
        "raw_order": {
            "width": FEATURE_WIDTH,
            "slot_0": "strict_t_A_less_than_t_C",
            "slot_1": "strict_t_C_less_than_t_A",
            "unused_tail": [2, 3, 4, 5, 6],
            "tie_policy": "ambiguous_order",
            "epsilon": None,
        },
        "raster_retention": {
            "channel_order": list(CHANNELS),
            "bins_per_channel": 41,
            "construction": "floor_ceil_linear_interpolation_then_total_mass_normalization",
            "mass_sum": "left_to_right_binary64_across_410_slots",
            "input_rows": [
                {
                    "input_index": index,
                    "observation_sha256": sha(canonical(row)),
                    "values": raster(row),
                }
                for index, row in enumerate(rows)
            ],
        },
    }


def teaching_schedule(evaluator: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Project only the frozen teaching receipts; no query target enters a driver.

    Only ``teaching`` is read. The caller should retain the complete evaluator
    separately from both model observations and this truth-minimized schedule.
    """
    rows = evaluator["teaching"]
    require(type(rows) is list and len(rows) == 2, "exact two teaching rows")
    schedule: dict[str, list[dict[str, Any]]] = {"S": [], "R": []}
    for offset, (cycle, label, outcome) in enumerate(((64, "A", 0.8), (65, "B", -0.8))):
        expected = {
            "input_index": cycle,
            "audit_label": label,
            "event_id": f"m1-path-20261002-{cycle:06d}",
            "outcome": outcome,
            "decision_time_ms": float(cycle * 200) + DECISION_OFFSET_MS,
            "delivery_time_ms": float(cycle * 200) + OUTCOME_OFFSET_MS,
            "receipt_ids": {
                arm: f"m1-path-20261002-{arm}-receipt-{cycle:06d}" for arm in ("S", "R")
            },
        }
        require(canonical(rows[offset]) == canonical(expected), "frozen teaching row changed")
        for arm in schedule:
            schedule[arm].append(
                {
                    "receipt_id": expected["receipt_ids"][arm],
                    "event_id": expected["event_id"],
                    "outcome": expected["outcome"],
                    "delivery_ms": expected["delivery_time_ms"],
                }
            )
    return schedule


def build() -> dict[str, bytes]:
    """Return deterministic prepared bytes only; never write or import a model."""
    rows = make_inputs(read_source_literals())
    return {
        "inputs.jsonl": b"".join(canonical(row) + b"\n" for row in rows),
        "evaluator.json": encoded(make_evaluator(rows)),
    }


def check(output: Path, files: dict[str, bytes]) -> None:
    """Read-only exact artifact check, tolerant of other pilot preparation files."""
    for name, raw in files.items():
        path = output / name
        require(
            path.is_file() and not path.is_symlink() and path.read_bytes() == raw,
            f"prepared bytes mismatch: {name}",
        )


def write_new(output: Path, files: dict[str, bytes]) -> None:
    """Write only our two new files, never clobber or modify historical artifacts."""
    resolved = output.resolve()
    old = SOURCE.resolve()
    require(
        not output.is_symlink()
        and not resolved.is_relative_to(old)
        and not old.is_relative_to(resolved),
        "input/output overlap or symlink",
    )
    require(set(files) == {"inputs.jsonl", "evaluator.json"}, "prepared file inventory")
    require(
        all(not (output / name).exists() and not (output / name).is_symlink() for name in files),
        "output files must be absent; no clobber",
    )
    output.mkdir(parents=True, exist_ok=True)
    for name, raw in files.items():
        with (output / name).open("xb") as stream:
            stream.write(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--check", action="store_true", help="read-only exact byte check")
    operation.add_argument(
        "--write-new", action="store_true", help="prepare new files, no overwrite"
    )
    args = parser.parse_args()
    files = build()
    if args.check:
        check(args.output, files)
    else:
        write_new(args.output, files)
    print(
        json.dumps(
            {
                "status": "verified_preparation" if args.check else "prepared",
                "files_sha256": {name: sha(raw) for name, raw in files.items()},
                "producer_windows": 68,
                "model_calls": 0,
                "execution_authorized": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
