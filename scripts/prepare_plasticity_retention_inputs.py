#!/usr/bin/env python3
"""Prepare immutable JSON inputs for an unallocated retention study; no model imports."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import random
import subprocess
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/plasticity_retention_bounded_v1.json"
DEFAULT = ROOT / "artifacts/research/plasticity_retention_preparation_20261001"
ARCHIVE_SHA = "2dfbe4f3afb8b046c1b465dcb52461daa027f72939dd85cf7dfad15670947082"
WRAPPER_SHA = "28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae"
CONDITIONS = ("return", "stationary", "novel")
MATRIX = {
    "return": (32, ("C", "L", "G", "Fw"), ("H", "R")),
    "stationary": (16, ("C", "L"), ()),
    "novel": (32, ("C", "L", "Fw"), ("H", "R")),
}


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encoded(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def rng(key: str) -> random.Random:
    return random.Random(int(hashlib.sha256(key.encode()).hexdigest(), 16))


def validate_protocol(p: dict[str, Any]) -> None:
    require(
        p["execution_authorized"] is False and p["execution_runner_present"] is False,
        "preparation cannot authorize execution",
    )
    require(
        p["fixtures"]
        == [
            {"prefix_seed": 910071, "suffix_seed": 910075},
            {"prefix_seed": 910072, "suffix_seed": 910076},
        ],
        "fixture identity",
    )
    require(p["public_prefix_source"]["archive_sha256"] == ARCHIVE_SHA, "archive pin")
    require(p["public_prefix_source"]["wrapper_sha256"] == WRAPPER_SHA, "wrapper pin")
    for name, (rows, arms, memory) in MATRIX.items():
        value = p["conditions"][name]
        require(
            (value["rows"], tuple(value["v05_arms"]), tuple(value["memory_arms"]))
            == (rows, arms, memory),
            "matrix identity",
        )
    require(type(p["schema_version"]) is int and p["schema_version"] == 1, "schema identity")
    expected_arms = {
        "C": {"enable_weight_learning": True, "eligibility_decay": 0.9, "learning_rate": 0.001},
        "L": {"enable_weight_learning": True, "eligibility_decay": 0.0, "learning_rate": 0.001},
        "G": {"enable_weight_learning": True, "eligibility_decay": 0.9, "learning_rate": 0.0001},
        "Fw": {"enable_weight_learning": False, "eligibility_decay": 0.9, "learning_rate": 0.001},
    }
    require(encoded(p["arms"]) == encoded(expected_arms), "exact intervention profile")
    for name, (orders, outcomes) in {
        "return": (["AFC"], [0]),
        "stationary": (["CFA"], [1]),
        "novel": (["ACF", "CAF"], [0, 1]),
    }.items():
        require(
            p["conditions"][name]["cue_orders"] == orders
            and p["conditions"][name]["outcomes"] == outcomes,
            "fixed cue/target mapping",
        )
    require(
        p["conditions"]["novel"]["balanced_blocks"]
        == [
            {"start": 0, "rows": 16, "counts": {"0": 8, "1": 8}},
            {"start": 16, "rows": 16, "counts": {"0": 8, "1": 8}},
        ],
        "exact balanced novel blocks",
    )
    spec = p["input_contract"]
    require(spec["model_keys"] == ["occurrence_id", "start_ms", "pulses"], "model information")
    require(
        spec["cue_offsets_ms"] == [8, 13, 15]
        and spec["query_offset_ms"] == 40
        and spec["prediction_offset_ms"] == 72
        and spec["receipt_offset_ms"] == 80
        and spec["first_cycle"] == 64
        and spec["cycle_ms"] == 200,
        "input timing",
    )
    require(
        spec["distractor_channels"] == "HIJKLM"
        and spec["distractor_count"] == 2
        and spec["distractor_time_range_ms"] == [0, 36]
        and spec["cue_jitter_range_ms"] == [-0.35, 0.35],
        "fixed input noise",
    )
    require(p["arms"]["L"]["eligibility_decay"] == 0.0, "L must remove apply carry")
    require(p["arms"]["L"]["enable_weight_learning"] is True, "L must retain learning")
    require(p["common_v05"]["enable_delay_learning"] is False, "fixed-delay boundary")
    b = p["budget"]
    require(
        (b["total_pairs"], b["v05_pairs"], b["memory_pairs"], b["new_prefix_pairs"])
        == (768, 512, 256, 0),
        "pair budget",
    )
    r = p["resources"]
    require(
        r["ordinary_output_bytes"] + r["reserved_failure_metadata_bytes"]
        == r["output_total_bytes"],
        "failure reserve is within total",
    )
    require(
        26 * r["max_worker_terminal_metadata_bytes"] + r["max_driver_terminal_metadata_bytes"]
        <= r["reserved_failure_metadata_bytes"],
        "failure reserve exceeds total",
    )


def pulse(at: float, channel: str, magnitude: float, fixed: dict[str, Any]) -> dict[str, Any]:
    return {
        "time_ms": float(at),
        "channel": channel,
        "magnitude": float(magnitude),
        **json.loads(json.dumps(fixed)),
    }


def make_inputs(p: dict[str, Any]) -> dict[str, Any]:
    validate_protocol(p)
    spec = p["input_contract"]
    streams = {}
    for fixture in p["fixtures"]:
        seed = fixture["suffix_seed"]
        for condition in CONDITIONS:
            kind = p["conditions"][condition]
            targets = []
            if condition == "novel":
                for block in range(2):
                    rows = [0] * 8 + [1] * 8
                    rng(f"retention-v1|{seed}|novel-order|{block}").shuffle(rows)
                    targets.extend(rows)
            else:
                targets = kind["outcomes"] * kind["rows"]
            rows = []
            for index, target in enumerate(targets):
                randomizer = rng(f"retention-v1|{seed}|{condition}|{index}")
                cycle = spec["first_cycle"] + index
                start = float(cycle * spec["cycle_ms"])
                pulses = []
                for _ in range(spec["distractor_count"]):
                    channel = spec["distractor_channels"][randomizer.randrange(6)]
                    at = randomizer.uniform(*spec["distractor_time_range_ms"])
                    pulses.append(
                        pulse(
                            start + at,
                            channel,
                            spec["distractor_magnitude"],
                            spec["pulse_fixed_fields"],
                        )
                    )
                jitter = [randomizer.uniform(*spec["cue_jitter_range_ms"]) for _ in range(3)]
                order = kind["cue_orders"][target if condition == "novel" else 0]
                for channel, offset, variation in zip(
                    order, spec["cue_offsets_ms"], jitter, strict=True
                ):
                    pulses.append(
                        pulse(
                            start + offset + variation,
                            channel,
                            spec["cue_magnitude"],
                            spec["pulse_fixed_fields"],
                        )
                    )
                pulses.append(
                    pulse(
                        start + spec["query_offset_ms"],
                        spec["query_channel"],
                        spec["query_magnitude"],
                        spec["pulse_fixed_fields"],
                    )
                )
                rows.append(
                    {
                        "occurrence_id": f"occ-{cycle:06d}",
                        "start_ms": start,
                        "pulses": sorted(pulses, key=lambda v: (v["time_ms"], v["channel"])),
                        "outcome": target,
                        "receipt_time_ms": start + spec["receipt_offset_ms"],
                    }
                )
            streams[f"{seed}-{condition}"] = rows
    return {
        "schema_version": 1,
        "classification": "FROZEN_INPUTS_NOT_MODEL_RESULTS",
        "streams": streams,
    }


def archive_prefixes(p: dict[str, Any]) -> dict[str, Any]:
    directory = ROOT / p["public_prefix_source"]["transport_directory"]
    manifest = json.loads((directory / "transport_manifest.json").read_bytes())
    chunks = []
    for index, part in enumerate(manifest["parts"]):
        require(part["path"] == f"evidence.part{index:03d}.b64", "transport order")
        raw = (directory / part["path"]).read_bytes()
        require(sha(raw) == part["encoded_sha256"], "encoded transport digest")
        decoded = base64.b64decode(b"".join(raw.split()), validate=True)
        require(sha(decoded) == part["sha256"], "decoded transport digest")
        chunks.append(decoded)
    payload = b"".join(chunks)
    require(
        sha(payload) == ARCHIVE_SHA and len(payload) == manifest["archive_bytes"], "archive pin"
    )
    records = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        members = {}
        for member in archive:
            path = PurePosixPath(member.name)
            require(
                member.isfile()
                and not path.is_absolute()
                and ".." not in path.parts
                and member.name not in members,
                "unsafe archive member",
            )
            members[member.name] = member
        for fixture in p["fixtures"]:
            seed = fixture["prefix_seed"]
            for arm in ("S", "H", "R"):
                parent = f"run/{seed}-{arm}-prefix/"
                paths = [parent + "checkpoint/wrapper.json", parent + "result.json"]
                if arm == "S":
                    paths.append(parent + "checkpoint/brain.json")
                raw_files = {}
                for path in paths:
                    stream = archive.extractfile(members[path])
                    require(stream is not None, "missing retained prefix file")
                    raw_files[path] = stream.read()
                wrapper = json.loads(raw_files[paths[0]])
                result = json.loads(raw_files[paths[1]])
                require(
                    wrapper["arm"] == arm
                    and wrapper["pending"] is None
                    and len(wrapper["receipts"]) == 64,
                    "wrapper prefix boundary",
                )
                require(
                    result["status"] == "completed" and result["eligibility"]["eligible"] is True,
                    "recorded prefix eligibility",
                )
                if arm == "S":
                    fact = result["eligibility"]
                    require(
                        fact["next_start_ms"] == 12800
                        and fact["queue_length"] == 0
                        and fact["pending_cascade_spikes"] == 0
                        and fact["noncanonical_outgoing_sources"] == [],
                        "quiet prefix facts",
                    )
                    require(
                        all(t < 12800 - fact["burst_window_ms"] for t in fact["burst_times"])
                        and fact["max_emitted_key_ms"] < 12800,
                        "expired omitted caches",
                    )
                    require(
                        json.loads(raw_files[paths[2]])["payload"]["episode_index"] == 64,
                        "brain prefix episode count",
                    )
                records[f"{seed}-{arm}"] = {
                    "files_sha256": {name: sha(raw) for name, raw in raw_files.items()},
                    "checkpoint_members": [name for name in paths if "/checkpoint/" in name],
                    "recorded_eligibility": result["eligibility"],
                    "wrapper_receipts": 64,
                    "wrapper_pending": None,
                }
    return {
        "archive_sha256": ARCHIVE_SHA,
        "prefixes": records,
        "scope": "Published restricted native-restore fixtures; no new load/ownership proof",
    }


def make_jobs(
    p: dict[str, Any], inputs: dict[str, Any], prefixes: dict[str, Any]
) -> dict[str, Any]:
    rows = []
    for fixture in p["fixtures"]:
        for condition in CONDITIONS:
            kind = p["conditions"][condition]
            stream = f"{fixture['suffix_seed']}-{condition}"
            for arm in kind["v05_arms"] + kind["memory_arms"]:
                v05 = arm in p["arms"]
                prefix = f"{fixture['prefix_seed']}-{'S' if v05 else arm}"
                rows.append(
                    {
                        "job_id": f"{stream}-{arm}",
                        "arm": arm,
                        "family": "v05" if v05 else "ordinary_memory",
                        "condition": condition,
                        "stream": stream,
                        "input_sha256": sha(encoded(inputs["streams"][stream])),
                        "prefix": prefix,
                        "prefix_source_sha256": sha(encoded(prefixes["prefixes"][prefix])),
                        "pairs": kind["rows"],
                        "cpu_seconds": p["resources"][
                            "v05_worker_cpu_seconds" if v05 else "memory_worker_cpu_seconds"
                        ],
                        "wall_seconds": p["resources"][
                            "v05_worker_wall_seconds" if v05 else "memory_worker_wall_seconds"
                        ],
                    }
                )
    require(len(rows) == 26 and sum(row["pairs"] for row in rows) == 768, "job budget")
    return {"schema_version": 1, "execution_authorized": False, "jobs": rows}


def source_files(commit: str) -> dict[str, str]:
    require(len(commit) == 40 and all(c in "0123456789abcdef" for c in commit), "exact source SHA")

    def git(*args: str) -> bytes:
        return subprocess.check_output(["git", *args], cwd=ROOT)

    names = git("ls-tree", "-r", "--name-only", commit, "src/sparkbrain", "schemas")
    return {name: sha(git("show", f"{commit}:{name}")) for name in names.decode().splitlines()}


def build() -> dict[str, bytes]:
    raw_protocol = PROTOCOL.read_bytes()
    p = json.loads(raw_protocol)
    validate_protocol(p)
    wrapper = ROOT / p["public_prefix_source"]["wrapper_source"]
    require(sha(wrapper.read_bytes()) == WRAPPER_SHA, "published wrapper changed")
    inputs = make_inputs(p)
    prefixes = archive_prefixes(p)
    jobs = make_jobs(p, inputs, prefixes)
    files = {
        "inputs.json": encoded(inputs),
        "prefix_sources.json": encoded(prefixes),
        "jobs.json": encoded(jobs),
    }
    files["preparation_manifest.json"] = encoded(
        {
            "schema_version": 1,
            "status": "SOURCE_INPUT_PREPARATION_ONLY",
            "model_imported": False,
            "model_import_statement_basis": (
                "Source architecture and runtime-import tripwire tests; "
                "this manifest flag is not a self-proving or universal runtime attestation"
            ),
            "model_calls": 0,
            "execution_authorized": False,
            "execution_runner_present": False,
            "execution_dependency_freeze_complete": False,
            "protocol_sha256": sha(raw_protocol),
            "preparer_sha256": sha(Path(__file__).read_bytes()),
            "wrapper_sha256": WRAPPER_SHA,
            "runtime_source_commit": p["runtime_source_commit"],
            "runtime_and_schema_sha256": source_files(p["runtime_source_commit"]),
            "files_sha256": {name: sha(raw) for name, raw in files.items()},
            "ceiling": p["budget"],
            "implementation_boundary": (
                "No enforcement or execution implementation; "
                "a separately reviewed runner freeze is required"
            ),
        }
    )
    return files


def write_new(output: Path, files: dict[str, bytes]) -> None:
    require(not output.exists() and not output.is_symlink(), "output must be absent; no clobber")
    output = output.resolve()
    old = (ROOT / "artifacts/research/temporal_reuse_loop_20261001").resolve()
    require(
        not output.is_relative_to(old) and not old.is_relative_to(output), "input/output overlap"
    )
    require(not output.exists(), "resolved output already exists")
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in files.items():
        with (output / name).open("xb") as stream:
            stream.write(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT)
    parser.add_argument("--check", action="store_true", help="read-only exact regeneration check")
    args = parser.parse_args()
    files = build()
    if args.check:
        require({p.name for p in args.output.iterdir()} == set(files), "output inventory mismatch")
        for name, raw in files.items():
            path = args.output / name
            require(
                path.is_file() and not path.is_symlink() and path.read_bytes() == raw,
                f"prepared bytes mismatch: {name}",
            )
    else:
        write_new(args.output, files)
    print(
        json.dumps(
            {
                "status": "verified_preparation" if args.check else "prepared",
                "files": {name: sha(raw) for name, raw in files.items()},
                "future_pairs_ceiling": 768,
                "model_calls": 0,
                "execution_authorized": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
