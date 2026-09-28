"""Composed causal-cut diagnostic for the noncanonical FLY-0 replacement ladder.

This module keeps the four matched replacement variants on one loop while
making local Observation and ascending LocalFeedback independently cuttable.
It is engineering-only Forge work and carries no scientific credit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256

from forge_prototypes.fly0_hierarchical_loop import (
    LocalFeedback,
    LoopSnapshot,
    Modulation,
    Observation,
    StepResult,
    WorldState,
)
from forge_prototypes.fly0_matched_replacement import (
    ActivityBasis,
    Variant,
    _build_bundle,
    _side,
    _topology_for,
    _zero,
)

_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)

_SEMANTIC_SURFACE_VERSION = "fly0-semantic-surface-v1"
_RANDOMIZATION_SEEDS: dict[Variant, int | None] = {
    "structured": None,
    "rewired": 2801,
    "random_sparse": 2802,
    "reactive": None,
}


def _semantic_surface_contract() -> dict[str, object]:
    """Describe the task-facing meaning that replacements must preserve."""

    return {
        "version": _SEMANTIC_SURFACE_VERSION,
        "channels": [
            {
                "channel_id": "sensory-left-signed-error",
                "direction": "sensory/input",
                "functional_role": "signed_error",
                "side": "left",
                "world_meaning": "target_is_left_of_position",
                "envelope_class": "bounded_observation_v1",
            },
            {
                "channel_id": "sensory-right-signed-error",
                "direction": "sensory/input",
                "functional_role": "signed_error",
                "side": "right",
                "world_meaning": "target_is_right_of_position",
                "envelope_class": "bounded_observation_v1",
            },
            {
                "channel_id": "motor-left-unit-step",
                "direction": "motor/output",
                "functional_role": "unit_step",
                "side": "left",
                "world_meaning": "position_decrements_by_one",
                "envelope_class": "bounded_action_v1",
            },
            {
                "channel_id": "motor-right-unit-step",
                "direction": "motor/output",
                "functional_role": "unit_step",
                "side": "right",
                "world_meaning": "position_increments_by_one",
                "envelope_class": "bounded_action_v1",
            },
        ],
        "world_scenario": "bounded-line-position-v1",
        "resource_envelope_class": "fly0-matched-envelope-v1",
    }


def _contract_fingerprint(contract: dict[str, object]) -> str:
    payload = json.dumps(
        contract, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(payload).hexdigest()


class ComposedCausalReplacementLoop:
    """Matched replacement loop with independent bottom-up causal cuts."""

    def __init__(
        self,
        initial_world: WorldState,
        *,
        variant: Variant,
        mask_observation: bool = False,
        mask_feedback: bool = False,
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
        topology = _topology_for(variant)
        self._topology_fingerprint = (
            topology.fingerprint() if topology is not None else None
        )
        self._randomization_seed = _RANDOMIZATION_SEEDS[variant]
        self._semantic_surface_contract = _semantic_surface_contract()
        self._semantic_surface_fingerprint = _contract_fingerprint(
            self._semantic_surface_contract
        )
        self._mask_observation = mask_observation
        self._mask_feedback = mask_feedback
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
    def topology_fingerprint(self) -> str | None:
        return self._topology_fingerprint

    @property
    def randomization_seed(self) -> int | None:
        return self._randomization_seed

    @property
    def semantic_surface_contract(self) -> dict[str, object]:
        return json.loads(json.dumps(self._semantic_surface_contract))

    @property
    def semantic_surface_fingerprint(self) -> str:
        return self._semantic_surface_fingerprint

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
            "schema_version": 2,
            "variant": self._variant,
            "module_ids": [item.module_id for item in self._controllers],
            "semantic_surface_contract": self._semantic_surface_contract,
            "semantic_surface_fingerprint": self._semantic_surface_fingerprint,
            "topology_fingerprint": self._topology_fingerprint,
            "randomization_seed": self._randomization_seed,
            "mask_observation": self._mask_observation,
            "mask_feedback": self._mask_feedback,
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
        if payload.get("schema_version") != 2:
            raise ValueError("checkpoint schema mismatch")
        if payload.get("variant") != self._variant:
            raise ValueError("checkpoint replacement variant mismatch")
        if payload.get("module_ids") != expected_ids:
            raise ValueError("checkpoint controller contract mismatch")
        if payload.get("semantic_surface_contract") != self._semantic_surface_contract:
            raise ValueError("checkpoint semantic-surface contract mismatch")
        if (
            payload.get("semantic_surface_fingerprint")
            != self._semantic_surface_fingerprint
        ):
            raise ValueError("checkpoint semantic-surface fingerprint mismatch")
        if payload.get("topology_fingerprint") != self._topology_fingerprint:
            raise ValueError("checkpoint topology fingerprint mismatch")
        if payload.get("randomization_seed") != self._randomization_seed:
            raise ValueError("checkpoint randomization-seed mismatch")
        if payload.get("mask_observation") != self._mask_observation:
            raise ValueError("checkpoint observation-mask contract mismatch")
        if payload.get("mask_feedback") != self._mask_feedback:
            raise ValueError("checkpoint feedback-mask contract mismatch")
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

    def _feedback_allows(self, desired: str) -> tuple[bool, str]:
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
        seen = (
            Observation(0, observation.sequence)
            if self._mask_observation
            else observation
        )
        try:
            proposals = tuple(
                item.propose(seen, modulation) for item in self._controllers
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
            feedback = tuple(item.feedback for item in proposals)
            if self._mask_feedback:
                feedback = tuple(
                    _zero(item.module_id, item.side) for item in feedback
                )
            after = LoopSnapshot(
                world=world,
                sequence=before.sequence + 1,
                feedback=feedback,
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
    loop: ComposedCausalReplacementLoop,
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
class CausalRow:
    variant: Variant
    activity_basis: ActivityBasis
    intact_trace: tuple[int, ...]
    intact_reached_target: bool
    intact_replay_exact: bool
    intact_rejection_reason: str | None
    observation_cut_trace: tuple[int, ...]
    observation_cut_reason: str | None
    feedback_cut_trace: tuple[int, ...]
    feedback_cut_reason: str | None

    @property
    def causal_probe_eligible(self) -> bool:
        return self.intact_reached_target

    @property
    def observation_cut_causal(self) -> bool:
        return (
            self.causal_probe_eligible
            and self.observation_cut_trace != self.intact_trace
        )

    @property
    def feedback_cut_causal(self) -> bool:
        return (
            self.causal_probe_eligible
            and self.feedback_cut_trace != self.intact_trace
        )


def _trace(initial: WorldState, results: tuple[StepResult, ...]) -> tuple[int, ...]:
    return (initial.position, *(item.after.world.position for item in results))


def _first_rejection(results: tuple[StepResult, ...]) -> str | None:
    return next((item.reason for item in results if not item.accepted), None)


def _capture_row(variant: Variant) -> CausalRow:
    initial = WorldState(position=2, target=-1)

    intact = ComposedCausalReplacementLoop(initial, variant=variant)
    checkpoint = intact.checkpoint()
    first = run_to_target(intact)
    first_tokens = tuple(item.after.token() for item in first)
    reached_target = intact.snapshot.world.position == intact.snapshot.world.target
    intact.restore(checkpoint)
    second = run_to_target(intact)

    observation_cut = ComposedCausalReplacementLoop(
        initial,
        variant=variant,
        mask_observation=True,
    )
    observation_results = run_to_target(observation_cut)

    feedback_cut = ComposedCausalReplacementLoop(
        initial,
        variant=variant,
        mask_feedback=True,
    )
    feedback_results = run_to_target(feedback_cut)

    return CausalRow(
        variant=variant,
        activity_basis=intact.activity_basis,
        intact_trace=_trace(initial, first),
        intact_reached_target=reached_target,
        intact_replay_exact=first_tokens
        == tuple(item.after.token() for item in second),
        intact_rejection_reason=_first_rejection(first),
        observation_cut_trace=_trace(initial, observation_results),
        observation_cut_reason=_first_rejection(observation_results),
        feedback_cut_trace=_trace(initial, feedback_results),
        feedback_cut_reason=_first_rejection(feedback_results),
    )


def build_composed_causal_report() -> dict[str, object]:
    rows = tuple(_capture_row(variant) for variant in _VARIANTS)
    functional = tuple(
        row.variant for row in rows if row.intact_reached_target
    )
    incapable = tuple(
        row.variant for row in rows if not row.intact_reached_target
    )
    composed_causal = tuple(
        row.variant
        for row in rows
        if row.observation_cut_causal and row.feedback_cut_causal
    )
    remaining: list[str] = []
    if "rewired" in incapable:
        remaining.append("REWIRED_BASELINE_FUNCTIONAL_CAPABILITY_ABSENT")
    if "random_sparse" in incapable:
        remaining.append("RANDOM_SPARSE_BASELINE_FUNCTIONAL_CAPABILITY_ABSENT")
    if len(composed_causal) != len(_VARIANTS):
        remaining.append(
            "FOUR_WAY_COMPOSED_CAUSAL_COMPARISON_BLOCKED_BY_BASELINE_CAPABILITY"
        )

    reference = ComposedCausalReplacementLoop(
        WorldState(position=0, target=0), variant="structured"
    )
    topology_fingerprints = {
        variant: ComposedCausalReplacementLoop(
            WorldState(position=0, target=0), variant=variant
        ).topology_fingerprint
        for variant in _VARIANTS
    }

    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "semantic_surface_contract": reference.semantic_surface_contract,
        "semantic_surface_fingerprint": reference.semantic_surface_fingerprint,
        "topology_fingerprints": topology_fingerprints,
        "rows": {row.variant: asdict(row) for row in rows},
        "functional_variants": functional,
        "baseline_incapable_variants": incapable,
        "composed_causal_variants": composed_causal,
        "replacement_ladder_functionally_matched": not incapable,
        "all_variants_replay_exact": all(row.intact_replay_exact for row in rows),
        "remaining_gap_codes": tuple(remaining),
        "claim_boundary": (
            "This is a bounded Forge engineering diagnostic. Baseline failure "
            "of a replacement prevents attributing a cut effect to that edge. "
            "It does not establish biological fidelity, topology necessity or "
            "superiority, compute or energy efficiency, composition "
            "contribution, novelty, external validity, scientific credit, or "
            "SB003 allocation."
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            build_composed_causal_report(),
            indent=2,
            sort_keys=True,
        )
    )
