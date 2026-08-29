from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from sparkbrain.v06.foundation import ImmutableRuntimeTrace, digest


class AssemblyTrajectoryObserver:
    """Names repeated trajectories post hoc without entering runtime state."""

    def __init__(self, *, minimum_recurrence: int = 2) -> None:
        if minimum_recurrence < 2:
            raise ValueError("minimum_recurrence must be at least 2")
        self.minimum_recurrence = minimum_recurrence

    def observe(self, trace: ImmutableRuntimeTrace) -> Mapping[str, Any]:
        signatures: list[str] = []
        for frame in trace.frames:
            trajectory = frame.get("trajectory")
            if trajectory is not None:
                signatures.append(digest(trajectory)[:20])
        counts = Counter(signatures)
        observed = [
            {
                "observed_assembly_id": f"observed-{signature}",
                "recurrence": count,
                "trajectory_signature": signature,
            }
            for signature, count in sorted(counts.items())
            if count >= self.minimum_recurrence
        ]
        return {
            "observer": "assembly-trajectory-v06",
            "runtime_hash": trace.runtime_hash,
            "observed_assemblies": observed,
        }
