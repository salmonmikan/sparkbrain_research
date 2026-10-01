"""Verify published bytes and descriptive arithmetic without importing a model."""

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


def check(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
        for seed, result in report["seeds"].items():
            for arm, conditions in result["arms"].items():
                for condition, expected in conditions.items():
                    raw = rows(f"run/{seed}-{arm}-{condition}/raw.jsonl")
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
                        check(
                            math.isclose(value, expected[key], abs_tol=1e-12), f"{seed}/{arm}/{key}"
                        )
                raw = rows(f"run/{seed}-{arm}-forks/raw.jsonl")
                forks += len(raw)
                if arm in ("S", "F"):
                    by_key = {
                        (r["pair"], r["cue"], r["intervention"], r["removed"]): r for r in raw
                    }
                    expected = result["causal"][arm]
                    for cue in (0, 1):
                        for intervention in ("targeted", "matched"):
                            changes = [
                                (by_key[(i, cue, intervention, False)]["p1"] - cue) ** 2
                                - (by_key[(i, cue, "sham", False)]["p1"] - cue) ** 2
                                for i in range(8)
                            ]
                            check(
                                math.isclose(
                                    sum(changes) / 8,
                                    expected["impairment"][f"{cue}_{intervention}"],
                                    abs_tol=1e-12,
                                ),
                                "causal arithmetic",
                            )
                            if cue == 1 and intervention == "targeted":
                                check(
                                    math.isclose(
                                        sum(abs(x) for x in changes) / 8,
                                        expected["absolute_B_collateral"],
                                        abs_tol=1e-12,
                                    ),
                                    "absolute collateral",
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
