"""Common runtime-work accounting for the noncanonical FLY-0 ladder.

This probe adds one implementation-level measurement basis across replacement
variants without pretending that topology trace events and reactive activations
are the same quantity. The counter is an engineering diagnostic only.
"""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from types import FrameType
from typing import Literal

from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_matched_replacement import (
    MatchedEnvelopeLoop,
    Variant,
    run_to_target,
)

WorkBasis = Literal["cpython_opcode_events_forge_path"]

_RUNTIME_DIR = Path(__file__).resolve().parent
_ALLOWED_RUNTIME_PATHS = frozenset(
    (_RUNTIME_DIR / name).resolve()
    for name in (
        "fly0_hierarchical_loop.py",
        "fly0_matched_replacement.py",
        "fly0_topology_probe.py",
    )
)


def _runtime_path_eligible(filename: str) -> bool:
    """Match only exact resolved Forge runtime source paths."""
    try:
        return Path(filename).resolve() in _ALLOWED_RUNTIME_PATHS
    except (OSError, RuntimeError):
        return False


def _runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    """Bind the measurement identity to the measured source bytes."""
    return tuple(
        (path.name, sha256(path.read_bytes()).hexdigest())
        for path in sorted(_ALLOWED_RUNTIME_PATHS)
    )


def _runtime_fingerprint() -> str:
    payload = {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "cache_tag": sys.implementation.cache_tag,
        "source_sha256": dict(_runtime_source_manifest()),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


class _OpcodeCounter:
    """Count CPython opcode events only inside the selected Forge runtime path."""

    def __init__(self) -> None:
        self.count = 0

    @staticmethod
    def _eligible(frame: FrameType) -> bool:
        return _runtime_path_eligible(frame.f_code.co_filename)

    def trace(
        self,
        frame: FrameType,
        event: str,
        arg: object,
    ) -> object:
        del arg
        eligible = self._eligible(frame)
        if event == "call":
            if not eligible:
                return None
            frame.f_trace_lines = False
            frame.f_trace_opcodes = True
            return self.trace
        if event == "opcode" and eligible:
            self.count += 1
        return self.trace


@dataclass(frozen=True)
class CommonWorkRow:
    variant: Variant
    runtime_fingerprint: str
    work_basis: WorkBasis
    opcode_events: int
    replay_opcode_events: int
    work_count_replay_exact: bool
    committed_world_transitions: int
    opcode_events_per_transition: float
    raw_activity_basis: str
    raw_fired_events: int
    raw_fired_events_per_transition: float
    position_trace: tuple[int, ...]
    reached_target: bool
    state_replay_exact: bool

    def __post_init__(self) -> None:
        if self.opcode_events < 1 or self.replay_opcode_events < 1:
            raise ValueError("opcode work counters must be positive")
        if self.committed_world_transitions < 1:
            raise ValueError("at least one committed transition is required")
        if self.raw_fired_events < 0:
            raise ValueError("raw activity must be non-negative")


@dataclass(frozen=True)
class CommonWorkReport:
    status: str
    rows: tuple[CommonWorkRow, ...]
    common_work_measurement_available: bool
    common_work_instrumentation_commensurate: bool
    common_work_count_replay_deterministic: bool
    raw_activity_instrumentation_commensurate: bool
    actual_common_work_exposure_equal: bool
    remaining_gap_codes: tuple[str, ...]
    claim_boundary: str

    def summary(self) -> dict[str, object]:
        return {
            "status": self.status,
            "rows": {row.variant: asdict(row) for row in self.rows},
            "comparability": {
                "common_work_measurement_available": (
                    self.common_work_measurement_available
                ),
                "common_work_instrumentation_commensurate": (
                    self.common_work_instrumentation_commensurate
                ),
                "common_work_count_replay_deterministic": (
                    self.common_work_count_replay_deterministic
                ),
                "raw_activity_instrumentation_commensurate": (
                    self.raw_activity_instrumentation_commensurate
                ),
                "actual_common_work_exposure_equal": (
                    self.actual_common_work_exposure_equal
                ),
                "remaining_gap_codes": list(self.remaining_gap_codes),
            },
            "claim_boundary": self.claim_boundary,
        }


def _counted_run(
    loop: MatchedEnvelopeLoop,
) -> tuple[tuple[object, ...], int]:
    counter = _OpcodeCounter()
    previous_trace = sys.gettrace()
    sys.settrace(counter.trace)
    try:
        results = run_to_target(loop)
    finally:
        sys.settrace(previous_trace)
    return results, counter.count


def _capture_row(variant: Variant) -> CommonWorkRow:
    initial = WorldState(position=2, target=-1)
    loop = MatchedEnvelopeLoop(initial, variant=variant)
    checkpoint = loop.checkpoint()

    first, first_count = _counted_run(loop)
    first_tokens = tuple(result.after.token() for result in first)
    final = loop.snapshot
    accepted = tuple(result for result in first if result.accepted)
    proposals = tuple(
        proposal
        for result in accepted
        for proposal in result.proposals
    )

    loop.restore(checkpoint)
    replay, replay_count = _counted_run(loop)
    replay_tokens = tuple(result.after.token() for result in replay)

    transitions = len(accepted)
    raw_fired = sum(item.feedback.fired_events for item in proposals)
    return CommonWorkRow(
        variant=variant,
        runtime_fingerprint=_runtime_fingerprint(),
        work_basis="cpython_opcode_events_forge_path",
        opcode_events=first_count,
        replay_opcode_events=replay_count,
        work_count_replay_exact=first_count == replay_count,
        committed_world_transitions=transitions,
        opcode_events_per_transition=first_count / transitions,
        raw_activity_basis=loop.activity_basis,
        raw_fired_events=raw_fired,
        raw_fired_events_per_transition=raw_fired / transitions,
        position_trace=(
            initial.position,
            *(result.after.world.position for result in first),
        ),
        reached_target=final.world.position == final.world.target,
        state_replay_exact=first_tokens == replay_tokens,
    )


def build_common_work_report() -> CommonWorkReport:
    rows = tuple(
        _capture_row(variant)
        for variant in (
            "structured",
            "rewired",
            "random_sparse",
            "reactive",
        )
    )
    work_bases = {row.work_basis for row in rows}
    runtimes = {row.runtime_fingerprint for row in rows}
    raw_bases = {row.raw_activity_basis for row in rows}

    common_basis = len(work_bases) == 1 and len(runtimes) == 1
    deterministic = all(row.work_count_replay_exact for row in rows)
    raw_commensurate = len(raw_bases) == 1
    equal_actual_work = (
        common_basis
        and len({row.opcode_events for row in rows}) == 1
    )

    remaining: list[str] = []
    if not common_basis:
        remaining.append("COMMON_WORK_BASIS_UNAVAILABLE")
    if not deterministic:
        remaining.append("COMMON_WORK_COUNTER_NOT_REPLAY_DETERMINISTIC")
    if not raw_commensurate:
        remaining.append("RAW_ACTIVITY_SEMANTICS_DISTINCT")
    if not equal_actual_work:
        remaining.append("ACTUAL_COMMON_WORK_EXPOSURE_NOT_EQUAL")

    return CommonWorkReport(
        status="NON_EVIDENTIARY_NONCANONICAL_FORGE",
        rows=rows,
        common_work_measurement_available=common_basis and deterministic,
        common_work_instrumentation_commensurate=common_basis,
        common_work_count_replay_deterministic=deterministic,
        raw_activity_instrumentation_commensurate=raw_commensurate,
        actual_common_work_exposure_equal=equal_actual_work,
        remaining_gap_codes=tuple(remaining),
        claim_boundary=(
            "CPython opcode events provide one implementation-level work basis "
            "only within one interpreter/cache-tag and exact source manifest. "
            "Frame eligibility is restricted to exact resolved Forge runtime "
            "paths. The counter does not measure energy, biological activity, "
            "algorithmic efficiency, or scientific superiority. Raw topology/"
            "reactive activity semantics remain separately labeled, and unequal "
            "measured work is reported rather than normalized away."
        ),
    )


if __name__ == "__main__":
    print(
        json.dumps(
            build_common_work_report().summary(),
            indent=2,
            sort_keys=True,
        )
    )
