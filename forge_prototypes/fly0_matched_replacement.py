"""Matched replacement-ladder diagnostic for the noncanonical FLY-0 track.

The diagnostic puts structured, rewired, random-sparse, and ordinary reactive
controllers behind the same observation/feedback gate and explicit logical
feedback-delay envelope. It is engineering-only Forge work.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Literal

from forge_prototypes.fly0_hierarchical_loop import (
    ActionProposal,
    Fly0LocalController,
    LocalController,
    LocalFeedback,
    LoopSnapshot,
    Modulation,
    Observation,
    ReactiveLocalController,
    Side,
    StepResult,
    WorldState,
)
from forge_prototypes.fly0_topology_probe import (
    Topology,
    build_degree_preserving_rewire,
    build_random_sparse,
    build_structured_topology,
)

Variant = Literal["structured", "rewired", "random_sparse", "reactive"]
ActivityBasis = Literal["topology_trace_events", "reactive_activation_events"]

_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def _side(error: int) -> Side | None:
    if error < 0:
        return "left"
    if error > 0:
        return "right"
    return None


def _zero(module_id: str, side: Side) -> LocalFeedback:
    return LocalFeedback(module_id, side, 0, 0, 0, None)


@dataclass(frozen=True)
class ObservationAwareController:
    """Apply the same local observation check to every replacement variant."""

    inner: LocalController

    @property
    def module_id(self) -> str:
        return self.inner.module_id

    @property
    def side(self) -> Side:
        return self.inner.side

    def propose(
        self,
        observation: Observation,
        modulation: Modulation,
    ) -> ActionProposal:
        if (
            modulation.desired_side == self.side
            and _side(observation.signed_error) != self.side
        ):
            return ActionProposal(
                self.module_id,
                0,
                False,
                _zero(self.module_id, self.side),
            )
        return self.inner.propose(observation, modulation)


@dataclass(frozen=True)
class ControllerBundle:
    controllers: tuple[ObservationAwareController, ...]
    activity_basis: ActivityBasis
    topology_resource_signature: dict[str, object] | None


def _topology_for(variant: Variant) -> Topology | None:
    if variant == "reactive":
        return None
    structured = build_structured_topology()
    if variant == "structured":
        return structured
    if variant == "rewired":
        return build_degree_preserving_rewire(structured)
    return build_random_sparse(structured)


def _build_bundle(variant: Variant) -> ControllerBundle:
    topology = _topology_for(variant)
    if topology is None:
        controllers = (
            ObservationAwareController(
                ReactiveLocalController("reactive-left", "left")
            ),
            ObservationAwareController(
                ReactiveLocalController("reactive-right", "right")
            ),
        )
        return ControllerBundle(
            controllers=controllers,
            activity_basis="reactive_activation_events",
            topology_resource_signature=None,
        )

    controllers = (
        ObservationAwareController(
            Fly0LocalController(f"{variant}-left", "left", topology)
        ),
        ObservationAwareController(
            Fly0LocalController(f"{variant}-right", "right", topology)
        ),
    )
    return ControllerBundle(
        controllers=controllers,
        activity_basis="topology_trace_events",
        topology_resource_signature=topology.resource_signature(),
    )


class MatchedEnvelopeLoop:
    """Closed loop with a common gate, budget, and logical delay contract."""

    def __init__(
        self,
        initial_world: WorldState,
        *,
        variant: Variant,
        feedback_delay_steps: int = 1,
        max_feedback_delay_steps: int = 1,
        event_budget: int = 4096,
    ) -> None:
        if feedback_delay_steps < 1:
            raise ValueError("feedback_delay_steps must be positive")
        if max_feedback_delay_steps < 1:
            raise ValueError("max_feedback_delay_steps must be positive")
        if event_budget < 1:
            raise ValueError("event_budget must be positive")
        bundle = _build_bundle(variant)
        self._variant = variant
        self._controllers = bundle.controllers
        self._activity_basis = bundle.activity_basis
        self._topology_resource_signature = bundle.topology_resource_signature
        self._feedback_delay_steps = feedback_delay_steps
        self._max_feedback_delay_steps = max_feedback_delay_steps
        self._event_budget = event_budget
        self._snapshot = LoopSnapshot(initial_world, 0)

    @property
    def snapshot(self) -> LoopSnapshot:
        return self._snapshot

    @property
    def variant(self) -> Variant:
        return self._variant

    @property
    def activity_basis(self) -> ActivityBasis:
        return self._activity_basis

    @property
    def topology_resource_signature(self) -> dict[str, object] | None:
        return self._topology_resource_signature

    @property
    def feedback_delay_steps(self) -> int:
        return self._feedback_delay_steps

    @property
    def max_feedback_delay_steps(self) -> int:
        return self._max_feedback_delay_steps

    @property
    def event_budget(self) -> int:
        return self._event_budget

    def checkpoint(self) -> str:
        payload = {
            "schema_version": 1,
            "variant": self._variant,
            "module_ids": [item.module_id for item in self._controllers],
            "feedback_delay_steps": self._feedback_delay_steps,
            "max_feedback_delay_steps": self._max_feedback_delay_steps,
            "event_budget": self._event_budget,
            "snapshot": asdict(self._snapshot),
            "token": self._snapshot.token(),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        expected_ids = [item.module_id for item in self._controllers]
        if payload.get("schema_version") != 1:
            raise ValueError("checkpoint schema mismatch")
        if payload.get("variant") != self._variant:
            raise ValueError("checkpoint replacement variant mismatch")
        if payload.get("module_ids") != expected_ids:
            raise ValueError("checkpoint controller contract mismatch")
        if payload.get("feedback_delay_steps") != self._feedback_delay_steps:
            raise ValueError("checkpoint feedback-delay contract mismatch")
        if (
            payload.get("max_feedback_delay_steps")
            != self._max_feedback_delay_steps
        ):
            raise ValueError("checkpoint feedback-delay budget mismatch")
        if payload.get("event_budget") != self._event_budget:
            raise ValueError("checkpoint event-budget mismatch")
        raw = payload["snapshot"]
        restored = LoopSnapshot(
            world=WorldState(**raw["world"]),
            sequence=raw["sequence"],
            feedback=tuple(LocalFeedback(**item) for item in raw["feedback"]),
        )
        if restored.token() != payload.get("token"):
            raise ValueError("checkpoint token mismatch")
        self._snapshot = restored

    def _feedback_allows(self, desired: Side) -> tuple[bool, str]:
        if self._snapshot.sequence == 0:
            return True, "INITIAL_STEP"
        if self._feedback_delay_steps > self._max_feedback_delay_steps:
            return False, "feedback delay exceeds matched budget"
        matching = tuple(
            item for item in self._snapshot.feedback if item.side == desired
        )
        if len(matching) != 1:
            return False, "ascending feedback insufficient for modulation"
        item = matching[0]
        if (
            item.matched_motor_events < 1
            or item.matched_motor_events <= item.opposite_motor_events
        ):
            return False, "ascending feedback insufficient for modulation"
        return True, "FEEDBACK_ACCEPTED"

    def step(self) -> StepResult:
        before = self._snapshot
        error = before.world.target - before.world.position
        desired = _side(error)
        if desired is not None:
            allowed, reason = self._feedback_allows(desired)
            if not allowed:
                return StepResult(
                    False,
                    reason,
                    before,
                    before,
                    Modulation(None),
                    (),
                )

        modulation = Modulation(desired)
        observation = Observation(error, before.sequence)
        try:
            proposals = tuple(
                item.propose(observation, modulation)
                for item in self._controllers
            )
            if any(
                item.feedback.fired_events > self._event_budget
                for item in proposals
            ):
                raise RuntimeError("local event budget exceeded")
            active = tuple(item for item in proposals if item.active)
            if desired is None:
                if active:
                    raise RuntimeError("local module acted without modulation")
                action = 0
            elif len(active) != 1:
                raise RuntimeError("action arbitration requires one active module")
            else:
                action = active[0].action
            world = WorldState(
                position=max(
                    -4,
                    min(4, before.world.position + action),
                ),
                target=before.world.target,
                step=before.world.step + 1,
            )
            after = LoopSnapshot(
                world=world,
                sequence=before.sequence + 1,
                feedback=tuple(item.feedback for item in proposals),
            )
            self._snapshot = after
            return StepResult(
                True,
                "COMMITTED",
                before,
                after,
                modulation,
                proposals,
            )
        except (RuntimeError, ValueError) as exc:
            return StepResult(
                False,
                str(exc),
                before,
                before,
                modulation,
                locals().get("proposals", ()),
            )


def run_to_target(
    loop: MatchedEnvelopeLoop,
    *,
    max_steps: int = 4,
) -> tuple[StepResult, ...]:
    if not 1 <= max_steps <= 8:
        raise ValueError("max_steps must be in [1, 8]")
    results: list[StepResult] = []
    for _ in range(max_steps):
        if loop.snapshot.world.position == loop.snapshot.world.target:
            break
        result = loop.step()
        results.append(result)
        if not result.accepted:
            break
    return tuple(results)


@dataclass(frozen=True)
class VariantRow:
    variant: Variant
    activity_basis: ActivityBasis
    accepted_steps: int
    rejected_steps: int
    final_position: int
    reached_target: bool
    position_trace: tuple[int, ...]
    controller_calls: int
    active_proposals: int
    fired_events: int
    feedback_delay_steps: int
    max_feedback_delay_steps: int
    event_budget_per_controller_call: int
    replay_exact: bool
    topology_resource_signature: dict[str, object] | None


@dataclass(frozen=True)
class ReplacementLadderReport:
    status: str
    rows: tuple[VariantRow, ...]
    replacement_ladder_complete: bool
    configured_envelope_matched: bool
    feedback_delay_envelope_matched: bool
    topology_resource_envelope_matched: bool
    activity_instrumentation_commensurate_across_all: bool
    strict_activity_resource_match: bool
    remaining_gap_codes: tuple[str, ...]
    claim_boundary: str

    def summary(self) -> dict[str, object]:
        return {
            "status": self.status,
            "rows": {
                row.variant: asdict(row)
                for row in self.rows
            },
            "comparability": {
                "replacement_ladder_complete": self.replacement_ladder_complete,
                "configured_envelope_matched": self.configured_envelope_matched,
                "feedback_delay_envelope_matched": (
                    self.feedback_delay_envelope_matched
                ),
                "topology_resource_envelope_matched": (
                    self.topology_resource_envelope_matched
                ),
                "activity_instrumentation_commensurate_across_all": (
                    self.activity_instrumentation_commensurate_across_all
                ),
                "strict_activity_resource_match": (
                    self.strict_activity_resource_match
                ),
                "remaining_gap_codes": list(self.remaining_gap_codes),
            },
            "claim_boundary": self.claim_boundary,
        }


def _capture_row(variant: Variant) -> VariantRow:
    initial = WorldState(position=2, target=-1)
    loop = MatchedEnvelopeLoop(initial, variant=variant)
    checkpoint = loop.checkpoint()
    first = run_to_target(loop)
    first_tokens = tuple(item.after.token() for item in first)
    final = loop.snapshot

    loop.restore(checkpoint)
    second = run_to_target(loop)
    proposals = tuple(
        proposal
        for result in first
        for proposal in result.proposals
    )
    active = tuple(item for item in proposals if item.active)
    rejected = tuple(item for item in first if not item.accepted)
    return VariantRow(
        variant=variant,
        activity_basis=loop.activity_basis,
        accepted_steps=sum(item.accepted for item in first),
        rejected_steps=len(rejected),
        final_position=final.world.position,
        reached_target=final.world.position == final.world.target,
        position_trace=(
            initial.position,
            *(item.after.world.position for item in first),
        ),
        controller_calls=len(proposals),
        active_proposals=len(active),
        fired_events=sum(
            item.feedback.fired_events
            for item in proposals
        ),
        feedback_delay_steps=loop.feedback_delay_steps,
        max_feedback_delay_steps=loop.max_feedback_delay_steps,
        event_budget_per_controller_call=loop.event_budget,
        replay_exact=(
            first_tokens
            == tuple(item.after.token() for item in second)
        ),
        topology_resource_signature=loop.topology_resource_signature,
    )


def build_replacement_ladder_report() -> ReplacementLadderReport:
    rows = tuple(_capture_row(variant) for variant in _VARIANTS)
    by_variant = {row.variant: row for row in rows}

    configured_signatures = {
        (
            row.feedback_delay_steps,
            row.max_feedback_delay_steps,
            row.event_budget_per_controller_call,
        )
        for row in rows
    }
    topology_signatures = {
        json.dumps(
            row.topology_resource_signature,
            sort_keys=True,
        )
        for row in rows
        if row.topology_resource_signature is not None
    }
    activity_bases = {row.activity_basis for row in rows}

    ladder_complete = set(by_variant) == set(_VARIANTS)
    configured_matched = len(configured_signatures) == 1
    delay_matched = len(
        {
            (
                row.feedback_delay_steps,
                row.max_feedback_delay_steps,
            )
            for row in rows
        }
    ) == 1
    topology_matched = len(topology_signatures) == 1
    activity_commensurate = len(activity_bases) == 1
    strict_activity_match = (
        activity_commensurate
        and len({row.fired_events for row in rows}) == 1
    )

    remaining: list[str] = []
    if not activity_commensurate:
        remaining.append(
            "REACTIVE_INTERNAL_ACTIVITY_BASIS_NOT_COMMENSURATE"
        )
    if not strict_activity_match:
        remaining.append("STRICT_INTERNAL_ACTIVITY_RESOURCE_MATCH_OPEN")
    if not configured_matched:
        remaining.append("CONFIGURED_ENVELOPE_MISMATCH")
    if not delay_matched:
        remaining.append("FEEDBACK_DELAY_ENVELOPE_MISMATCH")
    if not topology_matched:
        remaining.append("TOPOLOGY_RESOURCE_ENVELOPE_MISMATCH")
    if not ladder_complete:
        remaining.append("REPLACEMENT_LADDER_INCOMPLETE")

    return ReplacementLadderReport(
        status="NON_EVIDENTIARY_NONCANONICAL_FORGE",
        rows=rows,
        replacement_ladder_complete=ladder_complete,
        configured_envelope_matched=configured_matched,
        feedback_delay_envelope_matched=delay_matched,
        topology_resource_envelope_matched=topology_matched,
        activity_instrumentation_commensurate_across_all=activity_commensurate,
        strict_activity_resource_match=strict_activity_match,
        remaining_gap_codes=tuple(remaining),
        claim_boundary=(
            "This closes only the engineering replacement-ladder and logical "
            "delay-envelope gaps. Reactive internal activity remains on a "
            "different measurement basis, so no strict compute, energy, "
            "efficiency, topology-superiority, biological-fidelity, "
            "composition, novelty, or scientific claim is supported."
        ),
    )


if __name__ == "__main__":
    print(
        json.dumps(
            build_replacement_ladder_report().summary(),
            indent=2,
            sort_keys=True,
        )
    )
