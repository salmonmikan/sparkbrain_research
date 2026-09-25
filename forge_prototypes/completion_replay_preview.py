from __future__ import annotations

from dataclasses import dataclass

from forge_prototypes.assembly_completion import AssemblyCompletionProbe, CompletionProposal
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v05.assemblies import TemporalAssemblyMemory
from sparkbrain.v05.contracts import ActivityPattern


@dataclass(frozen=True, slots=True)
class CompletionReplayPreviewConfig:
    horizon_ms: float = 4.0
    trigger_epsilon: float = 1e-6
    max_trigger_units: int = 8

    def __post_init__(self) -> None:
        if self.horizon_ms <= 0.0:
            raise ValueError("horizon_ms must be positive")
        if self.trigger_epsilon <= 0.0:
            raise ValueError("trigger_epsilon must be positive")
        if self.max_trigger_units <= 0:
            raise ValueError("max_trigger_units must be positive")


@dataclass(frozen=True, slots=True)
class CompletionReplayPreviewResult:
    route: str
    assembly_id: str | None
    completion: CompletionProposal
    trigger_unit_ids: tuple[int, ...]
    baseline_spike_unit_ids: tuple[int, ...]
    replay_spike_unit_ids: tuple[int, ...]
    recovered_missing_unit_ids: tuple[int, ...]
    spillover_unit_ids: tuple[int, ...]
    missing_recovery_fraction: float
    prototype_recovery_fraction: float
    live_state_unchanged: bool
    reason: str


class CompletionReplayPreview:
    """Forge-only counterfactual completion replay on a cloned field.

    The live field is never mutated. Only the observed cue units are triggered;
    missing Assembly units must be recruited by the cloned field's existing
    recurrent connections.
    """

    def __init__(
        self,
        memory: TemporalAssemblyMemory,
        completion: AssemblyCompletionProbe | None = None,
        config: CompletionReplayPreviewConfig | None = None,
    ) -> None:
        self.memory = memory
        self.completion = completion or AssemblyCompletionProbe(memory)
        self.config = config or CompletionReplayPreviewConfig()

    def preview(
        self,
        field: TemporalExcitableField,
        cue: ActivityPattern,
    ) -> CompletionReplayPreviewResult:
        live_before = field.state_hash()
        proposal = self.completion.propose(cue)
        if proposal.abstained or proposal.assembly_id is None:
            return self._abstain(proposal, proposal.reason)

        candidate = self.memory.candidates.get(proposal.assembly_id)
        if candidate is None:
            return self._abstain(proposal, "candidate_disappeared")

        prototype_unit_ids = tuple(dict.fromkeys(candidate.prototype.ordered_units))
        trigger_unit_ids = tuple(dict.fromkeys(cue.ordered_units))
        known_ids = set(field.units)
        if not set(prototype_unit_ids).issubset(known_ids):
            return self._abstain(proposal, "prototype_unit_missing_from_field")
        if not set(trigger_unit_ids).issubset(known_ids):
            return self._abstain(proposal, "cue_unit_missing_from_field")
        if set(prototype_unit_ids) & set(field.receptor_ids):
            return self._abstain(proposal, "prototype_contains_receptor")
        if len(trigger_unit_ids) > self.config.max_trigger_units:
            return self._abstain(proposal, "too_many_trigger_units")

        now = field.current_time_ms
        if any(
            field.units[unit_id].refractory_until_ms > now
            for unit_id in trigger_unit_ids
        ):
            return self._abstain(proposal, "trigger_unit_refractory")

        baseline = TemporalExcitableField.from_state_dict(field.state_dict())
        replay = TemporalExcitableField.from_state_dict(field.state_dict())
        end_ms = now + self.config.horizon_ms

        baseline_spikes = baseline.run_until(end_ms)

        for unit_id in trigger_unit_ids:
            unit = replay.units[unit_id]
            current = (
                replay.dynamic_threshold(unit)
                + abs(unit.potential)
                + self.config.trigger_epsilon
            )
            replay.schedule_arrival(
                SynapticArrival(
                    time_ms=now,
                    target_id=unit_id,
                    current=current,
                    source_id=None,
                    pulse_id=f"forge-replay:{proposal.assembly_id}:{unit_id}",
                )
            )
        replay_spikes = replay.run_until(end_ms)

        baseline_ids = tuple(sorted({row.unit_id for row in baseline_spikes}))
        replay_ids = tuple(sorted({row.unit_id for row in replay_spikes}))
        net_replay_ids = set(replay_ids) - set(baseline_ids)
        missing_ids = set(proposal.missing_unit_ids)
        prototype_ids = set(prototype_unit_ids)

        recovered_missing = tuple(sorted(missing_ids & net_replay_ids))
        spillover = tuple(sorted(net_replay_ids - prototype_ids))
        missing_fraction = len(recovered_missing) / max(1, len(missing_ids))
        prototype_fraction = len(prototype_ids & net_replay_ids) / max(
            1,
            len(prototype_ids),
        )

        return CompletionReplayPreviewResult(
            route="counterfactual_replay",
            assembly_id=proposal.assembly_id,
            completion=proposal,
            trigger_unit_ids=trigger_unit_ids,
            baseline_spike_unit_ids=baseline_ids,
            replay_spike_unit_ids=replay_ids,
            recovered_missing_unit_ids=recovered_missing,
            spillover_unit_ids=spillover,
            missing_recovery_fraction=missing_fraction,
            prototype_recovery_fraction=prototype_fraction,
            live_state_unchanged=field.state_hash() == live_before,
            reason=(
                "missing_units_recruited"
                if recovered_missing
                else "no_missing_units_recruited"
            ),
        )

    @staticmethod
    def _abstain(
        proposal: CompletionProposal,
        reason: str,
    ) -> CompletionReplayPreviewResult:
        return CompletionReplayPreviewResult(
            route="abstain",
            assembly_id=proposal.assembly_id,
            completion=proposal,
            trigger_unit_ids=(),
            baseline_spike_unit_ids=(),
            replay_spike_unit_ids=(),
            recovered_missing_unit_ids=(),
            spillover_unit_ids=(),
            missing_recovery_fraction=0.0,
            prototype_recovery_fraction=0.0,
            live_state_unchanged=True,
            reason=reason,
        )
