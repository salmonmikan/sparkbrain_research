from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v06_boundary_probe import run_canonical_boundary_suite
from sparkbrain.evaluation.v06_chain_probe import run_canonical_chain_suite
from sparkbrain.evaluation.v06_revision_probe import run_canonical_revision_suite
from sparkbrain.evaluation.v06_state_probe import run_canonical_state_probe
from sparkbrain.v06.foundation import digest

FROZEN_V06_CODE_SHA = "1c89324958ffb3619878a6e0791aaf3c7a14c5da"
FROZEN_V06_CI_RUN_ID = 33342374956

# Git blob IDs from the post-3600 formal v0.6.1 code tree. RV01 is allowed to
# import this baseline, but it must not silently rewrite these mechanisms while
# using them as its comparison condition.
FROZEN_RUNTIME_BLOBS: dict[str, str] = {
    "src/sparkbrain/v06/boundary.py": "f0683e9bcfad9b54d8d7cdbfc9798bf55100cd9c",
    "src/sparkbrain/v06/consistency.py": "2752b3efc2bd17b35376dbae107cea817041896e",
    "src/sparkbrain/v06/endogenous_chain.py": "10a487cd7f62ba1f6ef651c8f15be1a08d9d8e1c",
    "src/sparkbrain/v06/forward.py": "77051083d52add239e1624e276de7b50fe40737f",
    "src/sparkbrain/v06/foundation.py": "35f9cf7065bd22449375cd315d3047bd0b3e9691",
    "src/sparkbrain/v06/g0.py": "02378aad2c4d87af1a9cb441c4b45d2c3e0fe6e7",
    "src/sparkbrain/v06/local_expectation.py": "caeb0b7ccc07ce9fdf26f56b25b11ba59fbc8594",
    "src/sparkbrain/v06/local_transition.py": "df3ed3b349d6745d165f2e772898783dc472d5f3",
    "src/sparkbrain/v06/reality.py": "4f43d6be7427cb15afaedcbb449d63dfa3b25291",
    "src/sparkbrain/v06/reinjection.py": "4df023a7ea0df53e3e8f4f6bbb44789d904a3cac",
    "src/sparkbrain/v06/relation_reentry.py": "0feff95f11809caec51c89eab1308c09f6b6f59b",
    "src/sparkbrain/v06/taxonomy.py": "2be0ffe1a8af4022be30d6af3313be9c0f9c8888",
    "src/sparkbrain/v06/world_boundary.py": "9b62fb46326ad94081e3d6994e935d0362d3e131",
    "src/sparkbrain/evaluation/v06_boundary_probe.py": (
        "9099a81a3426fe0d0f833b72cde529e5141c1861"
    ),
    "src/sparkbrain/evaluation/v06_chain_probe.py": (
        "4fdb681fd3c8635eb858ef26c032cc1a4159314c"
    ),
    "src/sparkbrain/evaluation/v06_revision_probe.py": (
        "448350c9d37480908a492189f72c9e1070af2dd8"
    ),
    "src/sparkbrain/evaluation/v06_state_probe.py": (
        "d86ded31e8361e49e1f68bf76d534f34432fe120"
    ),
}


@dataclass(frozen=True, slots=True)
class RuntimeFingerprintRow:
    path: str
    expected_git_blob_sha: str
    observed_git_blob_sha: str | None
    matched: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RuntimeFingerprintReport:
    frozen_code_sha: str
    rows: tuple[RuntimeFingerprintRow, ...]

    @property
    def complete(self) -> bool:
        return len(self.rows) == len(FROZEN_RUNTIME_BLOBS) and all(
            row.matched for row in self.rows
        )

    @property
    def mismatch_paths(self) -> tuple[str, ...]:
        return tuple(row.path for row in self.rows if not row.matched)

    def state_dict(self) -> dict[str, Any]:
        return {
            "complete": self.complete,
            "frozen_code_sha": self.frozen_code_sha,
            "mismatch_paths": list(self.mismatch_paths),
            "rows": [row.state_dict() for row in self.rows],
        }


@dataclass(frozen=True, slots=True)
class FrozenBaselineReport:
    frozen_code_sha: str
    frozen_ci_run_id: int
    fingerprints: RuntimeFingerprintReport
    canonical_summary: dict[str, Any]
    canonical_summary_hash: str
    state_candidate: bool
    chain_candidate: bool
    boundary_candidate: bool
    revision_candidate: bool

    @property
    def reproduced(self) -> bool:
        return self.fingerprints.complete and all(
            (
                self.state_candidate,
                self.chain_candidate,
                self.boundary_candidate,
                self.revision_candidate,
            )
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "boundary_candidate": self.boundary_candidate,
            "canonical_summary": self.canonical_summary,
            "canonical_summary_hash": self.canonical_summary_hash,
            "chain_candidate": self.chain_candidate,
            "fingerprints": self.fingerprints.state_dict(),
            "frozen_ci_run_id": self.frozen_ci_run_id,
            "frozen_code_sha": self.frozen_code_sha,
            "reproduced": self.reproduced,
            "revision_candidate": self.revision_candidate,
            "state_candidate": self.state_candidate,
        }


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


def verify_frozen_runtime_fingerprints(
    repository_root: Path | None = None,
) -> RuntimeFingerprintReport:
    root = repository_root or _repository_root()
    rows: list[RuntimeFingerprintRow] = []
    for relative_path, expected in sorted(FROZEN_RUNTIME_BLOBS.items()):
        path = root / relative_path
        observed = git_blob_sha(path.read_bytes()) if path.is_file() else None
        rows.append(
            RuntimeFingerprintRow(
                path=relative_path,
                expected_git_blob_sha=expected,
                observed_git_blob_sha=observed,
                matched=observed == expected,
            )
        )
    return RuntimeFingerprintReport(
        frozen_code_sha=FROZEN_V06_CODE_SHA,
        rows=tuple(rows),
    )


def _event_targets(events: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
    return tuple(str(row["target"]) for row in events)


def run_frozen_v06_baseline() -> FrozenBaselineReport:
    """Reproduce the canonical post-3600 v0.6.1 evidence without modifying it."""

    state = run_canonical_state_probe()
    chain = run_canonical_chain_suite()
    boundary = run_canonical_boundary_suite()
    revision = run_canonical_revision_suite()
    summary = {
        "boundary": {
            "internal_only_link_count": (
                boundary.assessment.internal_only_link_count
            ),
            "matched_random_main_boundary_count": (
                boundary.matched_random_port_suppression.main_boundary_count
            ),
            "sham_main_boundary_count": boundary.sham.main_boundary_count,
            "sham_main_external_count": boundary.sham.main_external_count,
            "targeted_main_boundary_count": (
                boundary.targeted_port_suppression.main_boundary_count
            ),
        },
        "chain": {
            "matched_random_main_units": (
                chain.matched_random_expansion.main_units
            ),
            "root_reinjection_suppressed_units": (
                chain.root_reinjection_suppressed.main_units
            ),
            "selective_effect": chain.assessment.selective_effect,
            "sham_main_units": chain.sham.main_units,
            "targeted_main_units": chain.targeted_expansion.main_units,
        },
        "revision": {
            "acquired_old_reliability": (
                revision.revision.acquisition.old_reliability
            ),
            "reacquisition_crossing_episode": (
                revision.assessment.reacquisition_crossing_episode
            ),
            "returned_new_reliability": (
                revision.revision.return_to_old.new_reliability
            ),
            "returned_old_reliability": (
                revision.revision.return_to_old.old_reliability
            ),
            "reversal_crossing_episode": (
                revision.assessment.reversal_crossing_episode
            ),
            "reversed_new_reliability": (
                revision.revision.reversal.new_reliability
            ),
            "reversed_old_reliability": (
                revision.revision.reversal.old_reliability
            ),
        },
        "state": {
            "alternate_targets": _event_targets(
                state.alternate_history.endogenous_events
            ),
            "no_history_event_count": state.no_history_event_count,
            "reference_targets": _event_targets(state.reference.endogenous_events),
            "replay_targets": _event_targets(
                state.reference_replay.endogenous_events
            ),
        },
    }
    fingerprints = verify_frozen_runtime_fingerprints()
    return FrozenBaselineReport(
        frozen_code_sha=FROZEN_V06_CODE_SHA,
        frozen_ci_run_id=FROZEN_V06_CI_RUN_ID,
        fingerprints=fingerprints,
        canonical_summary=summary,
        canonical_summary_hash=digest(summary),
        state_candidate=state.engineering_candidate,
        chain_candidate=chain.assessment.engineering_candidate,
        boundary_candidate=boundary.assessment.engineering_candidate,
        revision_candidate=revision.assessment.engineering_candidate,
    )
