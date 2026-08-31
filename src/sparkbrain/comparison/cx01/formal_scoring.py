from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .candidate import CX01_COMPARATOR_INVENTORY, CandidateSpec
from .contract import ComparatorKind
from .formal import _run_id
from .freeze import FreezeManifest
from .privilege import privilege_profile
from .raw_store import FormalRawStore
from .worlds import CX01Family


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


@dataclass(frozen=True, slots=True)
class FormalScoringPolicy:
    minimum_family_pass_fraction: float = 0.80
    require_all_families: bool = True
    require_training_transcript_match: bool = True
    require_privilege_match: bool = True

    def validate(self) -> None:
        if not 0.0 < self.minimum_family_pass_fraction <= 1.0:
            raise ValueError("minimum family pass fraction must be in (0, 1]")
        if not self.require_all_families:
            raise ValueError("CX01 formal scoring must remain non-compensatory across families")
        if not self.require_training_transcript_match:
            raise ValueError("CX01 formal scoring requires training transcript equality")
        if not self.require_privilege_match:
            raise ValueError("CX01 formal scoring requires exact privilege disclosure")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ComparatorFormalDecision:
    kind: ComparatorKind
    family_pass_fractions: tuple[tuple[CX01Family, float], ...]
    minimum_family_fraction: float
    supported: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            "family_pass_fractions": {
                family.value: fraction for family, fraction in self.family_pass_fractions
            },
            "kind": self.kind.value,
            "minimum_family_fraction": self.minimum_family_fraction,
            "supported": self.supported,
        }


@dataclass(frozen=True, slots=True)
class FormalAnalysis:
    run_id: str
    raw_aggregate_hash: str
    execution_count: int
    policy: FormalScoringPolicy
    decisions: tuple[ComparatorFormalDecision, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "decisions": [row.state_dict() for row in self.decisions],
            "execution_count": self.execution_count,
            "policy": self.policy.state_dict(),
            "raw_aggregate_hash": self.raw_aggregate_hash,
            "run_id": self.run_id,
        }


def _validate_rows(
    rows: tuple[dict[str, Any], ...],
    *,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    policy: FormalScoringPolicy,
) -> None:
    expected_count = len(candidate.seeds) * len(CX01Family) * len(CX01_COMPARATOR_INVENTORY)
    if len(rows) != expected_count:
        raise RuntimeError("formal analysis received an incomplete raw matrix")

    candidate_hash = candidate.specification_hash()
    manifest_hash = manifest.manifest_hash()
    seen_ids: set[str] = set()
    seen_keys: set[tuple[str, int, str]] = set()
    transcript_by_world: dict[tuple[str, int], set[str]] = {}

    for index, row in enumerate(rows):
        if int(row.get("formal_index", -1)) != index:
            raise RuntimeError("formal raw execution indices are not contiguous")
        execution_id = str(row.get("execution_id", ""))
        if len(execution_id) != 64 or execution_id in seen_ids:
            raise RuntimeError("formal raw execution IDs must be unique SHA-256 values")
        seen_ids.add(execution_id)
        if row.get("candidate_spec_hash") != candidate_hash:
            raise RuntimeError("formal row candidate hash mismatch")
        if row.get("manifest_hash") != manifest_hash:
            raise RuntimeError("formal row manifest hash mismatch")

        family = CX01Family(str(row["family"]))
        kind = ComparatorKind(str(row["kind"]))
        seed = int(row["seed"])
        if seed not in candidate.seeds:
            raise RuntimeError("formal row contains an undeclared seed")
        key = (family.value, seed, kind.value)
        if key in seen_keys:
            raise RuntimeError("formal raw matrix contains a duplicate architecture/world cell")
        seen_keys.add(key)

        transcript_hash = str(row.get("training_transcript_hash", ""))
        if len(transcript_hash) != 64:
            raise RuntimeError("formal row training transcript hash is invalid")
        transcript_by_world.setdefault((family.value, seed), set()).add(transcript_hash)

        decision = row.get("decision")
        if not isinstance(decision, dict) or decision.get("family") != family.value:
            raise RuntimeError("formal row decision family mismatch")
        if not isinstance(decision.get("passed"), bool):
            raise RuntimeError("formal row decision must contain a Boolean pass value")

        if policy.require_privilege_match:
            resource = row.get("resource")
            if not isinstance(resource, dict):
                raise RuntimeError("formal row is missing resource metadata")
            observed_privileges = tuple(str(value) for value in resource.get("privileges", ()))
            expected_privileges = tuple(
                value.value for value in privilege_profile(kind).privileges
            )
            if observed_privileges != expected_privileges:
                raise RuntimeError("formal row privilege inventory mismatch")

    expected_keys = {
        (family.value, seed, kind.value)
        for family in CX01Family
        for seed in candidate.seeds
        for kind in CX01_COMPARATOR_INVENTORY
    }
    if seen_keys != expected_keys:
        raise RuntimeError("formal raw matrix coverage does not match frozen inventory")
    if policy.require_training_transcript_match and any(
        len(values) != 1 for values in transcript_by_world.values()
    ):
        raise RuntimeError("comparators did not consume identical training transcripts")


def score_finalized_candidate(
    *,
    artifact_root: Path,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    policy: FormalScoringPolicy | None = None,
) -> FormalAnalysis:
    candidate.require_formal()
    manifest.validate()
    decision_policy = policy or FormalScoringPolicy()
    decision_policy.validate()
    if candidate.specification_hash() != manifest.candidate_spec_hash:
        raise RuntimeError("analysis candidate does not match frozen manifest")
    if str(artifact_root) != manifest.artifact_root:
        raise RuntimeError("analysis artifact root does not match frozen manifest")

    run_id = _run_id(manifest, candidate)
    expected_count = len(candidate.seeds) * len(CX01Family) * len(CX01_COMPARATOR_INVENTORY)
    store = FormalRawStore(artifact_root, run_id)
    rows = store.read_finalized(expected_count)
    _validate_rows(
        rows,
        candidate=candidate,
        manifest=manifest,
        policy=decision_policy,
    )

    completion = json.loads((store.root / "RAW_COMPLETE.json").read_text(encoding="utf-8"))
    decisions: list[ComparatorFormalDecision] = []
    for kind in CX01_COMPARATOR_INVENTORY:
        family_fractions: list[tuple[CX01Family, float]] = []
        for family in CX01Family:
            selected = [
                row
                for row in rows
                if row["kind"] == kind.value and row["family"] == family.value
            ]
            fraction = sum(bool(row["decision"]["passed"]) for row in selected) / len(selected)
            family_fractions.append((family, fraction))
        minimum = min(fraction for _, fraction in family_fractions)
        supported = all(
            fraction >= decision_policy.minimum_family_pass_fraction
            for _, fraction in family_fractions
        )
        decisions.append(
            ComparatorFormalDecision(
                kind=kind,
                family_pass_fractions=tuple(family_fractions),
                minimum_family_fraction=minimum,
                supported=supported,
            )
        )

    return FormalAnalysis(
        run_id=run_id,
        raw_aggregate_hash=str(completion["aggregate_hash"]),
        execution_count=expected_count,
        policy=decision_policy,
        decisions=tuple(decisions),
    )


def write_analysis_atomic(artifact_root: Path, analysis: FormalAnalysis) -> Path:
    target = artifact_root / f"{analysis.run_id}.ANALYSIS"
    temporary = artifact_root / f".{analysis.run_id}.ANALYSIS.tmp"
    if target.exists() or temporary.exists():
        raise FileExistsError("formal analysis identity already exists")
    temporary.mkdir(parents=False)
    try:
        analysis_bytes = _canonical_bytes(analysis.state_dict()) + b"\n"
        (temporary / "analysis.json").write_bytes(analysis_bytes)
        checksums = {"analysis.json": hashlib.sha256(analysis_bytes).hexdigest()}
        (temporary / "checksums.json").write_bytes(_canonical_bytes(checksums) + b"\n")
        (temporary / "COMPLETE").write_text("complete\n", encoding="utf-8")
        for path in temporary.iterdir():
            if path.is_file():
                path.chmod(0o444)
        os.replace(temporary, target)
        target.chmod(0o555)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return target


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    args = parser.parse_args()
    candidate = CandidateSpec.from_state_dict(_read_json(args.candidate))
    manifest = FreezeManifest.from_state_dict(_read_json(args.manifest))
    analysis = score_finalized_candidate(
        artifact_root=args.artifact_root,
        candidate=candidate,
        manifest=manifest,
    )
    print(write_analysis_atomic(args.artifact_root, analysis))


if __name__ == "__main__":
    main()
