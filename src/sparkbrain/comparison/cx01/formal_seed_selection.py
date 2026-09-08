from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from .candidate import CandidatePurpose, CandidateSpec, build_candidate_grid

FORMAL_SEED_SELECTION_POLICY = "cx01-formal-seed-selection-v1"


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_source_sha(source_git_sha: str) -> None:
    if len(source_git_sha) != 40 or any(
        char not in "0123456789abcdef" for char in source_git_sha.lower()
    ):
        raise ValueError("formal seed selection requires an exact 40-character Git SHA")


@dataclass(frozen=True, slots=True)
class FormalSeedSelection:
    source_git_sha: str
    generation_id: str
    seeds: tuple[int, ...]
    attempt_index: int
    policy_version: str = FORMAL_SEED_SELECTION_POLICY

    def validate(self) -> None:
        _validate_source_sha(self.source_git_sha)
        if self.policy_version != FORMAL_SEED_SELECTION_POLICY:
            raise ValueError("unexpected formal seed selection policy")
        if self.attempt_index < 0:
            raise ValueError("formal seed selection attempt index must be non-negative")
        CandidateSpec(
            generation_id=self.generation_id,
            seeds=self.seeds,
            purpose=CandidatePurpose.FORMAL,
        ).validate()

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["seeds"] = list(self.seeds)
        return value

    def selection_hash(self) -> str:
        return _digest(self.state_dict())


def _initial_block_start(source_git_sha: str, generation_id: str) -> int:
    material = {
        "generation_id": generation_id,
        "policy": FORMAL_SEED_SELECTION_POLICY,
        "source_git_sha": source_git_sha.lower(),
    }
    # Keep formal seeds in a high namespace far from all historical/development
    # ranges. CandidateSpec remains the normative overlap guard.
    return 1_000_000 + (int(_digest(material)[:12], 16) % 90_000_000) // 10 * 10


def select_outcome_blind_formal_seeds(
    *,
    source_git_sha: str,
    generation_id: str,
    count: int = 10,
    maximum_attempts: int = 1000,
) -> FormalSeedSelection:
    """Choose the first deterministic block passing structural pre-capability gates.

    Candidate models are never instantiated. A block may be skipped only when
    candidate validation, structural-heldout audit, or analytical
    identifiability audit fails. No comparator outcome or resource measurement
    is available to this procedure.
    """

    _validate_source_sha(source_git_sha)
    if count < 10:
        raise ValueError("formal seed selection requires at least ten seeds")
    if maximum_attempts < 1:
        raise ValueError("maximum_attempts must be positive")

    start = _initial_block_start(source_git_sha, generation_id)
    stride = count
    for attempt in range(maximum_attempts):
        block_start = start + attempt * stride
        seeds = tuple(range(block_start, block_start + count))
        spec = CandidateSpec(
            generation_id=generation_id,
            seeds=seeds,
            purpose=CandidatePurpose.FORMAL,
        )
        try:
            # This path builds structure and audits only. It cannot instantiate
            # a comparator because candidate.py has no comparator-model import.
            build_candidate_grid(spec)
        except (RuntimeError, ValueError):
            continue
        selection = FormalSeedSelection(
            source_git_sha=source_git_sha.lower(),
            generation_id=generation_id,
            seeds=seeds,
            attempt_index=attempt,
        )
        selection.validate()
        return selection

    raise RuntimeError("no structurally eligible formal seed block found within safety bound")
