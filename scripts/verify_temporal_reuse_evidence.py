"""Verify published bytes, descriptive arithmetic and gates without importing a model."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

SEEDS = ("910071", "910072")
ARMS = ("Q", "H", "R", "S", "F")
CONDITIONS = ("return", "interleaved")


def check(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare(calculated: Any, reported: Any, label: str) -> None:
    if isinstance(calculated, float):
        check(
            type(reported) in (int, float)
            and math.isclose(calculated, reported, rel_tol=0, abs_tol=1e-12),
            label,
        )
    else:
        # JSON booleans must not be accepted as numerically equal 0/1 (or vice versa).
        check(type(reported) is type(calculated) and calculated == reported, label)


def validate_predictions(raw: list[dict[str, Any]], label: str) -> None:
    for row in raw:
        check(
            type(row["p1"]) in (int, float)
            and math.isfinite(row["p1"])
            and 0 <= row["p1"] <= 1
            and type(row["outcome"]) is int
            and row["outcome"] in (0, 1)
            and (row["native"] is None or (type(row["native"]) is int and row["native"] in (0, 1))),
            label + "/prediction domain",
        )


def causal_metrics(raw: list[dict[str, Any]], arm: str, label: str) -> dict[str, Any]:
    validate_predictions(raw, label)
    states = ("sham", "targeted", "matched", "observer") if arm in ("S", "F") else ("sham",)
    required = {
        (pair, cue, state, removed)
        for pair in range(8)
        for cue in (0, 1)
        for state, removed in [(state, False) for state in states] + [("sham", True)]
    }
    for row in raw:
        check(
            type(row["pair"]) is int
            and type(row["cue"]) is int
            and row["cue"] == row["outcome"]
            and type(row["removed"]) is bool,
            label + "/fork key domain",
        )
    grouped = {(r["pair"], r["cue"], r["intervention"], r["removed"]): r for r in raw}
    check(len(raw) == len(grouped) and set(grouped) == required, label + "/fork inventory")

    def equal(left: dict[str, Any], right: dict[str, Any], fields: tuple[str, ...]) -> bool:
        return all(left[field] == right[field] for field in fields)

    output_fields = ("p1", "native", "operational_sha256")
    calculated: dict[str, Any] = {
        "cue_directions": sum(
            grouped[(i, 1, "sham", False)]["p1"] > grouped[(i, 0, "sham", False)]["p1"]
            for i in range(8)
        ),
        "removed_equal": all(
            equal(
                grouped[(i, 0, "sham", True)],
                grouped[(i, 1, "sham", True)],
                ("input_sha256", *output_fields),
            )
            for i in range(8)
        ),
        # The recorded observer branch is a duplicate sham, not a renderer test.
        "observer_equal": all(
            equal(
                grouped[(i, cue, "sham", False)],
                grouped[(i, cue, "observer", False)],
                output_fields,
            )
            for i in range(8)
            for cue in (0, 1)
        )
        if arm in ("S", "F")
        else None,
    }
    if arm in ("S", "F"):
        impairment = {}
        for cue in (0, 1):
            for state in ("targeted", "matched"):
                changes = [
                    (grouped[(i, cue, state, False)]["p1"] - cue) ** 2
                    - (grouped[(i, cue, "sham", False)]["p1"] - cue) ** 2
                    for i in range(8)
                ]
                impairment[f"{cue}_{state}"] = sum(changes) / 8
                if cue == 1 and state == "targeted":
                    calculated["absolute_B_collateral"] = sum(abs(x) for x in changes) / 8
        calculated["impairment"] = impairment
        calculated["targeted_minus_matched_A"] = impairment["0_targeted"] - impairment["0_matched"]
    return calculated


def decision_gates(arms: dict[str, Any], causal: dict[str, Any]) -> dict[str, bool]:
    """Rebuild the frozen runner's gates from recalculated inputs only."""
    # This summarizes fork equalities, not independent execution/isolation certification.
    guards = all(
        causal[arm]["removed_equal"] and causal[arm]["observer_equal"] is not False for arm in ARMS
    )
    s, c = arms["S"], causal["S"]
    gate = (
        all(
            s[key]["brier"] <= arms[arm][key]["brier"] - 0.02
            for key in CONDITIONS
            for arm in ("H", "R")
        )
        and 1 - s["return"]["first_p1"] >= 0.75
        and c["targeted_minus_matched_A"] >= 0.05
        and c["absolute_B_collateral"] <= 0.02
        and c["cue_directions"] >= 6
        and c["removed_equal"]
        and c["observer_equal"]
        and guards
    )
    return {"all_control_guards_passed": guards, "integration_proposal_gate": gate}


def verify(directory: Path, extract: Path | None = None) -> dict[str, Any]:
    transport = json.loads((directory / "transport_manifest.json").read_text())
    chunks = []
    for part in transport["parts"]:
        check(PurePosixPath(part["path"]).name == part["path"], "unsafe transport path")
        encoded = (directory / part["path"]).read_bytes()
        check(sha(encoded) == part["encoded_sha256"], "encoded part mismatch")
        data = base64.b64decode(b"".join(encoded.split()), validate=True)
        check(len(data) == part["bytes"] and sha(data) == part["sha256"], "decoded part mismatch")
        chunks.append(data)
    archive = b"".join(chunks)
    check(len(archive) == transport["archive_bytes"], "archive length mismatch")
    check(sha(archive) == transport["archive_sha256"], "archive hash mismatch")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
        members = bundle.getmembers()
        names = [row.name for row in members]
        check(len(names) == len(set(names)) == transport["archive_files"], "archive inventory")
        for row in members:
            path = PurePosixPath(row.name)
            check(
                row.isfile() and not path.is_absolute() and ".." not in path.parts,
                "unsafe archive member",
            )

        def read(name: str) -> bytes:
            stream = bundle.extractfile(name)
            check(stream is not None, f"missing {name}")
            return stream.read()

        def document(name: str) -> Any:
            return json.loads(read(name))

        def rows(name: str) -> list[dict[str, Any]]:
            return [json.loads(line) for line in read(name).splitlines()]

        manifest = document("ARCHIVE_MANIFEST.json")
        check(set(manifest["files"]) | {"ARCHIVE_MANIFEST.json"} == set(names), "archive coverage")
        for name, expected in manifest["files"].items():
            raw = read(name)
            check(len(raw) == expected["bytes"] and sha(raw) == expected["sha256"], name)
        inner = document("run/manifest.json")
        check(inner["complete"], "run inventory incomplete")
        for name, expected in inner["files"].items():
            check(sha(read("run/" + name)) == expected, "run manifest: " + name)
        report = document("run/report.json")
        check(report["status"] == "completed", "run not completed")
        check(transport["raw_run_exit_code_observed"] == 0, "nonzero recorded process exit")
        count, forks = 0, 0
        gates = {}
        check(set(report["seeds"]) == set(SEEDS), "seed inventory")
        for seed, result in report["seeds"].items():
            check(set(result["arms"]) == set(ARMS), f"{seed}/arm inventory")
            check(set(result["causal"]) == set(ARMS), f"{seed}/causal arm inventory")
            calculated_arms: dict[str, Any] = {}
            calculated_causal = {}
            for arm, conditions in result["arms"].items():
                check(set(conditions) == set(CONDITIONS), f"{seed}/{arm}/condition inventory")
                calculated_arms[arm] = {}
                for condition, expected in conditions.items():
                    raw = rows(f"run/{seed}-{arm}-{condition}/raw.jsonl")
                    check(len(raw) == 32, f"{seed}/{arm}/{condition}/suffix inventory")
                    validate_predictions(raw, f"{seed}/{arm}/{condition}")
                    count += len(raw)
                    losses = [(r["p1"] - r["outcome"]) ** 2 for r in raw]
                    calculated = {
                        "n": len(raw),
                        "brier": sum(losses) / len(raw),
                        "coverage": sum(r["native"] is not None for r in raw) / len(raw),
                        "accuracy_all": sum(r["native"] == r["outcome"] for r in raw) / len(raw),
                        "first_p1": raw[0]["p1"],
                        "first_loss": losses[0],
                        "first_four_brier": sum(losses[:4]) / 4,
                    }
                    for key, value in calculated.items():
                        compare(value, expected[key], f"{seed}/{arm}/{key}")
                    calculated_arms[arm][condition] = calculated
                raw = rows(f"run/{seed}-{arm}-forks/raw.jsonl")
                forks += len(raw)
                calculated_causal[arm] = causal_metrics(raw, arm, f"{seed}/{arm}")
                expected = result["causal"][arm]
                for key, value in calculated_causal[arm].items():
                    if key == "impairment":
                        check(
                            set(expected[key]) == set(value), f"{seed}/{arm}/impairment inventory"
                        )
                        for name, impairment in value.items():
                            compare(impairment, expected[key][name], f"{seed}/{arm}/{key}/{name}")
                    else:
                        compare(value, expected[key], f"{seed}/{arm}/{key}")
            recalculated = decision_gates(calculated_arms, calculated_causal)
            for key, value in recalculated.items():
                compare(value, result[key], f"{seed}/{key}")
            gates[seed] = recalculated["integration_proposal_gate"]
        both_seeds = all(gates[seed] for seed in SEEDS)
        compare(
            both_seeds,
            report["integration_proposal_gate_both_seeds"],
            "integration_proposal_gate_both_seeds",
        )
        check(count == 640 and forks == 512, "measured row inventory")
        if extract is not None:
            extract.mkdir(parents=True, exist_ok=False)
            for row in members:
                target = extract.joinpath(*PurePosixPath(row.name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(read(row.name))
    return {
        "status": "verified",
        "archive_files": len(names),
        "run_manifest_files": len(inner["files"]),
        "measured_suffix_rows": count,
        "causal_fork_rows": forks,
        "integration_proposal_gates": gates,
        "integration_proposal_gate_both_seeds": both_seeds,
        "archive_sha256": sha(archive),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory", type=Path, default=Path("artifacts/research/temporal_reuse_loop_20261001")
    )
    parser.add_argument("--extract", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.directory, args.extract), indent=2))


if __name__ == "__main__":
    main()
