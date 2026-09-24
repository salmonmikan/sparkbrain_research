from __future__ import annotations

from dataclasses import dataclass

from sparkbrain.v05.assemblies import TemporalAssemblyMemory, pattern_similarity
from sparkbrain.v05.contracts import ActivityPattern


@dataclass(frozen=True, slots=True)
class CompletionConfig:
    similarity_threshold: float = 0.55
    min_margin: float = 0.08
    require_mature: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be in [0, 1]")
        if not 0.0 <= self.min_margin <= 1.0:
            raise ValueError("min_margin must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class CompletionProposal:
    assembly_id: str | None
    prototype_pattern_id: str | None
    similarity: float
    margin: float
    observed_unit_ids: tuple[int, ...]
    missing_positions: tuple[int, ...]
    missing_unit_ids: tuple[int, ...]
    abstained: bool
    reason: str


def _subsequence_positions(
    observed: tuple[int, ...],
    prototype: tuple[int, ...],
) -> tuple[int, ...] | None:
    positions: list[int] = []
    start = 0
    for unit_id in observed:
        for index in range(start, len(prototype)):
            if prototype[index] == unit_id:
                positions.append(index)
                start = index + 1
                break
        else:
            return None
    return tuple(positions)


class AssemblyCompletionProbe:
    """Forge-only read-only completion proposal over mature v0.5 Assemblies."""

    def __init__(
        self,
        memory: TemporalAssemblyMemory,
        config: CompletionConfig | None = None,
    ) -> None:
        self.memory = memory
        self.config = config or CompletionConfig()

    def propose(self, cue: ActivityPattern) -> CompletionProposal:
        rows = []
        for candidate in self.memory.candidates.values():
            if candidate.assembly_id in self.memory.suppressed:
                continue
            mature = candidate.episode_count >= self.memory.config.mature_episodes
            if self.config.require_mature and not mature:
                continue
            positions = _subsequence_positions(
                cue.ordered_units,
                candidate.prototype.ordered_units,
            )
            if positions is None:
                continue
            rows.append(
                (
                    pattern_similarity(candidate.prototype, cue),
                    candidate,
                    positions,
                )
            )

        if not rows:
            return self._abstain(cue, reason="no_compatible_candidate")

        rows.sort(key=lambda row: (-row[0], row[1].assembly_id))
        best_score, best_candidate, best_positions = rows[0]
        second_score = rows[1][0] if len(rows) > 1 else 0.0
        margin = best_score - second_score

        if best_score < self.config.similarity_threshold:
            return self._abstain(
                cue,
                reason="below_completion_threshold",
                similarity=best_score,
                margin=margin,
            )

        if len(rows) > 1 and margin < self.config.min_margin:
            return self._abstain(
                cue,
                reason="ambiguous_candidate",
                similarity=best_score,
                margin=margin,
            )

        selected = set(best_positions)
        missing_positions = tuple(
            index
            for index in range(len(best_candidate.prototype.ordered_units))
            if index not in selected
        )
        if not missing_positions:
            return self._abstain(
                cue,
                reason="already_complete",
                similarity=best_score,
                margin=margin,
            )

        return CompletionProposal(
            assembly_id=best_candidate.assembly_id,
            prototype_pattern_id=best_candidate.prototype.pattern_id,
            similarity=best_score,
            margin=margin,
            observed_unit_ids=cue.unit_ids,
            missing_positions=missing_positions,
            missing_unit_ids=tuple(
                best_candidate.prototype.ordered_units[index]
                for index in missing_positions
            ),
            abstained=False,
            reason="completion_proposed",
        )

    @staticmethod
    def _abstain(
        cue: ActivityPattern,
        *,
        reason: str,
        similarity: float = 0.0,
        margin: float = 0.0,
    ) -> CompletionProposal:
        return CompletionProposal(
            assembly_id=None,
            prototype_pattern_id=None,
            similarity=similarity,
            margin=margin,
            observed_unit_ids=cue.unit_ids,
            missing_positions=(),
            missing_unit_ids=(),
            abstained=True,
            reason=reason,
        )
