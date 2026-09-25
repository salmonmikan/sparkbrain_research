from __future__ import annotations

from dataclasses import dataclass

from forge_prototypes.assembly_completion import AssemblyCompletionProbe, CompletionProposal
from sparkbrain.v05.action import AssemblyActionPolicy
from sparkbrain.v05.assemblies import TemporalAssemblyMemory
from sparkbrain.v05.contracts import ActivityPattern, AssemblyActivation


@dataclass(frozen=True, slots=True)
class CompletionActionPreviewConfig:
    min_action_margin: float = 0.05

    def __post_init__(self) -> None:
        if not 0.0 <= self.min_action_margin <= 1.0:
            raise ValueError("min_action_margin must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class CompletionActionPreviewResult:
    route: str
    assembly_id: str | None
    action: str | None
    confidence: float
    completion: CompletionProposal | None
    action_margin: float
    reason: str


class CompletionActionPreview:
    """Forge-only read-only action preview for native or completed Assembly cues."""

    def __init__(
        self,
        memory: TemporalAssemblyMemory,
        policy: AssemblyActionPolicy,
        completion: AssemblyCompletionProbe | None = None,
        config: CompletionActionPreviewConfig | None = None,
    ) -> None:
        self.memory = memory
        self.policy = policy
        self.completion = completion or AssemblyCompletionProbe(memory)
        self.config = config or CompletionActionPreviewConfig()

    def preview(self, cue: ActivityPattern) -> CompletionActionPreviewResult:
        native = self.memory.observe(
            cue,
            time_ms=cue.end_ms,
            episode_id="forge-readonly-action-preview",
            learn=False,
        )
        if native is not None and native.mature and not native.suppressed:
            return self._preview_activation(
                native,
                route="native",
                completion=None,
                route_confidence=native.similarity,
            )

        proposal = self.completion.propose(cue)
        if proposal.abstained or proposal.assembly_id is None:
            return CompletionActionPreviewResult(
                route="abstain",
                assembly_id=None,
                action=None,
                confidence=0.0,
                completion=proposal,
                action_margin=0.0,
                reason=proposal.reason,
            )

        candidate = self.memory.candidates.get(proposal.assembly_id)
        if candidate is None:
            return self._abstain(proposal, "candidate_disappeared")

        mature = candidate.episode_count >= self.memory.config.mature_episodes
        suppressed = candidate.assembly_id in self.memory.suppressed
        if not mature or suppressed:
            return self._abstain(proposal, "candidate_not_available")

        virtual_activation = AssemblyActivation(
            assembly_id=candidate.assembly_id,
            pattern_id=cue.pattern_id,
            time_ms=cue.end_ms,
            similarity=proposal.similarity,
            occurrences=candidate.occurrences,
            episode_count=candidate.episode_count,
            mature=True,
            unit_ids=candidate.prototype.unit_ids,
            suppressed=False,
        )
        return self._preview_activation(
            virtual_activation,
            route="completion",
            completion=proposal,
            route_confidence=proposal.similarity,
        )

    def _preview_activation(
        self,
        activation: AssemblyActivation,
        *,
        route: str,
        completion: CompletionProposal | None,
        route_confidence: float,
    ) -> CompletionActionPreviewResult:
        table = self.policy.scores.get(activation.assembly_id)
        if not table:
            return CompletionActionPreviewResult(
                route="abstain",
                assembly_id=activation.assembly_id,
                action=None,
                confidence=0.0,
                completion=completion,
                action_margin=0.0,
                reason="no_action_history",
            )

        actions = self.policy.config.actions
        if any(action not in table for action in actions):
            return CompletionActionPreviewResult(
                route="abstain",
                assembly_id=activation.assembly_id,
                action=None,
                confidence=0.0,
                completion=completion,
                action_margin=0.0,
                reason="incomplete_action_table",
            )

        ranked = sorted(actions, key=lambda action: (-table[action], actions.index(action)))
        best = ranked[0]
        second_value = table[ranked[1]] if len(ranked) > 1 else 0.0
        margin = table[best] - second_value
        if margin < self.config.min_action_margin:
            return CompletionActionPreviewResult(
                route="abstain",
                assembly_id=activation.assembly_id,
                action=None,
                confidence=0.0,
                completion=completion,
                action_margin=margin,
                reason="ambiguous_action",
            )

        policy_confidence = max(0.0, min(1.0, 0.5 + margin))
        confidence = min(max(0.0, min(1.0, route_confidence)), policy_confidence)
        return CompletionActionPreviewResult(
            route=route,
            assembly_id=activation.assembly_id,
            action=best,
            confidence=confidence,
            completion=completion,
            action_margin=margin,
            reason=f"{route}_action_preview",
        )

    @staticmethod
    def _abstain(
        proposal: CompletionProposal,
        reason: str,
    ) -> CompletionActionPreviewResult:
        return CompletionActionPreviewResult(
            route="abstain",
            assembly_id=proposal.assembly_id,
            action=None,
            confidence=0.0,
            completion=proposal,
            action_margin=0.0,
            reason=reason,
        )
