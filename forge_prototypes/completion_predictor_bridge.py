from __future__ import annotations

from dataclasses import dataclass

from forge_prototypes.assembly_completion import AssemblyCompletionProbe, CompletionProposal
from sparkbrain.v05.assemblies import TemporalAssemblyMemory
from sparkbrain.v05.contracts import ActivityPattern, AssemblyActivation, PredictionDecision
from sparkbrain.v05.prediction import AssemblyPredictor


@dataclass(frozen=True, slots=True)
class CompletionPredictionResult:
    route: str
    assembly_id: str | None
    prediction: PredictionDecision
    completion: CompletionProposal | None
    reason: str


class CompletionPredictorBridge:
    """Forge-only read-only fallback from partial Assembly cues to prediction."""

    def __init__(
        self,
        memory: TemporalAssemblyMemory,
        predictor: AssemblyPredictor,
        completion: AssemblyCompletionProbe | None = None,
    ) -> None:
        self.memory = memory
        self.predictor = predictor
        self.completion = completion or AssemblyCompletionProbe(memory)

    def predict(self, cue: ActivityPattern) -> CompletionPredictionResult:
        native = self.memory.observe(
            cue,
            time_ms=cue.end_ms,
            episode_id="forge-readonly-probe",
            learn=False,
        )
        if native is not None and native.mature and not native.suppressed:
            return CompletionPredictionResult(
                route="native",
                assembly_id=native.assembly_id,
                prediction=self.predictor.predict(native),
                completion=None,
                reason="native_match",
            )

        proposal = self.completion.propose(cue)
        if proposal.abstained or proposal.assembly_id is None:
            return CompletionPredictionResult(
                route="abstain",
                assembly_id=None,
                prediction=PredictionDecision(None, None, 0.0),
                completion=proposal,
                reason=proposal.reason,
            )

        candidate = self.memory.candidates.get(proposal.assembly_id)
        if candidate is None:
            return CompletionPredictionResult(
                route="abstain",
                assembly_id=None,
                prediction=PredictionDecision(None, None, 0.0),
                completion=proposal,
                reason="candidate_disappeared",
            )

        mature = candidate.episode_count >= self.memory.config.mature_episodes
        suppressed = candidate.assembly_id in self.memory.suppressed
        if not mature or suppressed:
            return CompletionPredictionResult(
                route="abstain",
                assembly_id=None,
                prediction=PredictionDecision(None, None, 0.0),
                completion=proposal,
                reason="candidate_not_available",
            )

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
        prediction = self.predictor.predict(virtual_activation)
        reason = (
            "completion_prediction"
            if prediction.value is not None
            else "completion_match_without_predictive_history"
        )
        return CompletionPredictionResult(
            route="completion",
            assembly_id=candidate.assembly_id,
            prediction=prediction,
            completion=proposal,
            reason=reason,
        )
