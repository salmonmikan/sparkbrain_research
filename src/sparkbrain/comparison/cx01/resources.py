from __future__ import annotations

import math
import time
import tracemalloc
from dataclasses import asdict, dataclass
from typing import Any, Callable, TypeVar

from .contract import ComparatorKind, ComparatorProtocol
from .privilege import privilege_profile

_T = TypeVar("_T")


@dataclass(frozen=True, slots=True)
class ResourceRecord:
    kind: ComparatorKind
    wall_clock_ns: int
    process_cpu_ns: int
    peak_traced_memory_bytes: int
    parameter_count: int
    state_entry_count: int
    observed_external_events: int
    generated_internal_events: int
    privileges: tuple[str, ...]
    decision_use: str = "descriptive-only"

    def validate(self) -> None:
        numeric = (
            self.wall_clock_ns,
            self.process_cpu_ns,
            self.peak_traced_memory_bytes,
            self.parameter_count,
            self.state_entry_count,
            self.observed_external_events,
            self.generated_internal_events,
        )
        if any(value < 0 or not math.isfinite(float(value)) for value in numeric):
            raise ValueError("resource values must be finite and non-negative")
        if self.decision_use != "descriptive-only":
            raise ValueError("CX01 resource use must remain descriptive-only")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["kind"] = self.kind.value
        value["privileges"] = list(self.privileges)
        return value


def measure_model_call(
    model: ComparatorProtocol,
    call: Callable[[], _T],
) -> tuple[_T, ResourceRecord]:
    """Measure one evaluator-bounded operation without affecting pass/fail."""

    tracemalloc.start()
    wall_start = time.perf_counter_ns()
    cpu_start = time.process_time_ns()
    try:
        result = call()
        process_cpu_ns = time.process_time_ns() - cpu_start
        wall_clock_ns = time.perf_counter_ns() - wall_start
        _, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    profile = privilege_profile(model.kind)
    record = ResourceRecord(
        kind=model.kind,
        wall_clock_ns=wall_clock_ns,
        process_cpu_ns=process_cpu_ns,
        peak_traced_memory_bytes=peak_memory,
        parameter_count=model.parameter_count,
        state_entry_count=model.state_entry_count,
        observed_external_events=model.observed_external_events,
        generated_internal_events=model.generated_internal_events,
        privileges=tuple(row.value for row in profile.privileges),
    )
    record.validate()
    return result, record
