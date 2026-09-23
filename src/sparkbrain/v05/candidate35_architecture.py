from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.v04.contracts import SignalPulse, canonical_json

from .brain import IntegratedV05Brain, V05BrainConfig
from .subthreshold_architecture import (
    SubthresholdArchitectureUnreachable,
    clone_at_queue_free_anchor,
    pending_arrival_count,
    snapshot_subthreshold_units,
)

Candidate35Arm = Literal[
    "SHAM_STATE",
    "POTENTIAL_NULL",
    "ADAPTATION_NULL",
    "JOINT_SUBTHRESHOLD_NULL",
    "DELAYED_SHAM_32MS",
]

CANDIDATE_ID = "CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING"
DEVELOPMENT_REVISION = (
    "ARCHITECTURE-R2-EXACT-CANDIDATE-SURFACE-AND-EXECUTOR-BINDING-NONRESULT"
)
PRIME_SOURCE_ID = "cand35-prime"
PRIME_EPISODE_ID = "cand35-prime-episode"
CUE_SOURCE_ID = "cand35-cue"
NORMAL_SETTLE_MS = 32.0
ANCHOR_INCREMENT_MS = 32.0
ANCHOR_MAX_ADDITIONAL_BOUNDARIES = 8
ANCHOR_MAX_ADDITIONAL_MS = 256.0
CUE_OFFSET_MS = 4.0
DELAYED_SHAM_OFFSET_MS = 32.0
MEASUREMENT_WINDOW_MS = 32.0
MEMBRANE_TAU_MS = 18.0
ADAPTATION_TAU_MS = 90.0

ARMS: tuple[Candidate35Arm, ...] = (
    "SHAM_STATE",
    "POTENTIAL_NULL",
    "ADAPTATION_NULL",
    "JOINT_SUBTHRESHOLD_NULL",
    "DELAYED_SHAM_32MS",
)


class Candidate35ResponseNotAuthorized(RuntimeError):
    """Raised before any candidate response when response authority is absent."""


@dataclass(frozen=True, slots=True)
class Candidate35Preflight:
    contract_json: str
    contract_sha256: str
    binding_json: str
    binding_sha256: str
    cue_route_targets: tuple[int, ...]
    candidate_response_executed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Candidate35ResponseRecord:
    arm: Candidate35Arm
    anchor_time_ms: float
    cue_time_ms: float
    treatment_state_hash: str
    causal_response_json: str
    causal_response_sha256: str
    reduction_ledger_json: str
    reduction_ledger_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def candidate35_prime_pulses() -> tuple[SignalPulse, ...]:
    """Return the prospectively frozen no-learning v0.5 prime inputs."""
    return (
        SignalPulse(
            time_ms=0.0,
            channel="A",
            magnitude=1.18,
            polarity=1,
            novelty=0.25,
            prediction_error=0.0,
            source_id=PRIME_SOURCE_ID,
        ),
        SignalPulse(
            time_ms=5.0,
            channel="F",
            magnitude=1.18,
            polarity=1,
            novelty=0.25,
            prediction_error=0.0,
            source_id=PRIME_SOURCE_ID,
        ),
        SignalPulse(
            time_ms=7.0,
            channel="C",
            magnitude=1.18,
            polarity=1,
            novelty=0.25,
            prediction_error=0.0,
            source_id=PRIME_SOURCE_ID,
        ),
    )


def candidate35_cue(*, anchor_time_ms: float, delayed_sham: bool = False) -> SignalPulse:
    offset = CUE_OFFSET_MS + (DELAYED_SHAM_OFFSET_MS if delayed_sham else 0.0)
    return SignalPulse(
        time_ms=float(anchor_time_ms) + offset,
        channel="A",
        magnitude=0.85,
        polarity=1,
        novelty=0.0,
        prediction_error=0.0,
        source_id=CUE_SOURCE_ID,
    )


def candidate35_frozen_contract() -> dict[str, Any]:
    """Machine-readable R2 binding of the unchanged Discovery R1 contract."""
    return {
        "candidate_id": CANDIDATE_ID,
        "claim_ceiling": "SYSTEM",
        "development_revision": DEVELOPMENT_REVISION,
        "prime": {
            "episode_id": PRIME_EPISODE_ID,
            "source_id": PRIME_SOURCE_ID,
            "pulses": [pulse.as_dict() for pulse in candidate35_prime_pulses()],
            "learn_assembly": False,
            "learn_field": False,
            "explore_action": False,
            "normal_settle_ms": NORMAL_SETTLE_MS,
        },
        "anchor": {
            "require_queue_empty": True,
            "increment_ms": ANCHOR_INCREMENT_MS,
            "max_additional_boundaries": ANCHOR_MAX_ADDITIONAL_BOUNDARIES,
            "max_additional_ms": ANCHOR_MAX_ADDITIONAL_MS,
            "cap_extension_allowed": False,
        },
        "reset_scope": "ALL_NON_RECEPTOR_UNITS",
        "arms": list(ARMS),
        "cue": {
            "channel": "A",
            "offset_ms": CUE_OFFSET_MS,
            "delayed_sham_offset_ms": CUE_OFFSET_MS + DELAYED_SHAM_OFFSET_MS,
            "magnitude": 0.85,
            "polarity": 1,
            "novelty": 0.0,
            "prediction_error": 0.0,
            "source_id": CUE_SOURCE_ID,
        },
        "measurement_window_ms": MEASUREMENT_WINDOW_MS,
        "response_signature": (
            "ordered spike/cascade/ignition rows plus cue routing targets and exact "
            "processed-event counts; canonical JSON hash"
        ),
        "treatment_state_hash_role": "INTEGRITY_ONLY_NOT_CAUSAL_FALSIFIER",
        "ordinary_reductions": [
            "exact_sham_clone",
            "factorial_potential_adaptation_joint_null",
            "delayed_sham_natural_decay",
            (
                "local_dynamic_threshold_margin_ledger_with_18ms_potential_"
                "and_90ms_adaptation_decay"
            ),
            "hard_queue_empty_requirement",
            "identical_topology_weights_higher_state_and_no_learning",
        ],
        "decay_constants_ms": {
            "potential": MEMBRANE_TAU_MS,
            "adaptation": ADAPTATION_TAU_MS,
        },
        "causal_falsifier": (
            "complete causal-response signature identical across SHAM_STATE/POTENTIAL_NULL/"
            "ADAPTATION_NULL/JOINT_SUBTHRESHOLD_NULL"
        ),
        "same_object_system_to_mechanism_uplift_allowed": False,
        "candidate_response_execution_allowed": False,
        "preformal_execution_allowed": False,
        "formal_action_allowed": False,
    }


def _component_binding() -> dict[str, str]:
    return {
        "brain_type": "sparkbrain.v05.brain.IntegratedV05Brain",
        "prime_executor": "IntegratedV05Brain.process_episode",
        "anchor_advance": "IntegratedV04Brain.advance",
        "queue_counter": "sparkbrain.v05.subthreshold_architecture.pending_arrival_count",
        "anchor_clone": "sparkbrain.v05.subthreshold_architecture.clone_at_queue_free_anchor",
        "cue_executor": "IntegratedV04Brain.ingest_pulses",
        "cue_router": "TemporalExcitableField.route_pulse",
        "response_source": (
            "sparkbrain.v05.candidate35_architecture.execute_candidate35_response"
        ),
        "serializer": "sparkbrain.v04.contracts.canonical_json",
    }


def build_candidate35_brain() -> IntegratedV05Brain:
    """Construct the exact fresh v0.5 source surface without executing the prime."""
    return IntegratedV05Brain(
        V05BrainConfig(
            topology_seed=41,
            settle_ms=NORMAL_SETTLE_MS,
            enable_weight_learning=False,
            enable_delay_learning=False,
            enable_reward_modulation=False,
        )
    )


def all_non_receptor_unit_ids(brain: IntegratedV05Brain) -> tuple[int, ...]:
    receptor_ids = set(brain.base.field.receptor_ids)
    return tuple(
        unit_id
        for unit_id in sorted(brain.base.field.units)
        if unit_id not in receptor_ids
    )


def build_candidate35_anchor() -> tuple[IntegratedV05Brain, float]:
    """Bind the frozen prime/settle path and bounded queue-empty anchor.

    R2 never calls this function. A later fresh Analyst must authorize candidate execution first.
    """
    brain = build_candidate35_brain()
    brain.process_episode(
        candidate35_prime_pulses(),
        learn_assembly=False,
        learn_field=False,
        episode_id=PRIME_EPISODE_ID,
        explore_action=False,
    )
    if pending_arrival_count(brain) == 0:
        clone, anchor = clone_at_queue_free_anchor(brain)
        return clone, anchor.current_time_ms

    for _ in range(ANCHOR_MAX_ADDITIONAL_BOUNDARIES):
        brain.base.advance(brain.current_time_ms + ANCHOR_INCREMENT_MS)
        if pending_arrival_count(brain) == 0:
            clone, anchor = clone_at_queue_free_anchor(brain)
            return clone, anchor.current_time_ms

    raise SubthresholdArchitectureUnreachable(
        "candidate #35 queue-empty anchor was not reached within the fixed 256 ms cap"
    )


def _clone_with_arm_treatment(
    anchor_brain: IntegratedV05Brain,
    arm: Candidate35Arm,
) -> IntegratedV05Brain:
    clone, _ = clone_at_queue_free_anchor(anchor_brain)
    unit_ids = all_non_receptor_unit_ids(clone)
    if not unit_ids:
        raise SubthresholdArchitectureUnreachable("candidate #35 has no non-receptor units")
    if arm in {"POTENTIAL_NULL", "JOINT_SUBTHRESHOLD_NULL"}:
        for unit_id in unit_ids:
            clone.base.field.units[unit_id].potential = 0.0
    if arm in {"ADAPTATION_NULL", "JOINT_SUBTHRESHOLD_NULL"}:
        for unit_id in unit_ids:
            clone.base.field.units[unit_id].adaptation = 0.0
    if pending_arrival_count(clone) != 0:
        raise SubthresholdArchitectureUnreachable("arm preparation created pending work")
    return clone


def _reduction_ledger(
    anchor_brain: IntegratedV05Brain,
    treatment_brain: IntegratedV05Brain,
) -> str:
    unit_ids = all_non_receptor_unit_ids(anchor_brain)
    payload = {
        "anchor": [
            row.as_dict() for row in snapshot_subthreshold_units(anchor_brain, unit_ids)
        ],
        "treatment": [
            row.as_dict()
            for row in snapshot_subthreshold_units(treatment_brain, unit_ids)
        ],
        "membrane_tau_ms": MEMBRANE_TAU_MS,
        "adaptation_tau_ms": ADAPTATION_TAU_MS,
        "reduction_role": "ORDINARY_LOCAL_THRESHOLD_AND_DECAY_LEDGER",
    }
    return canonical_json(payload)


def execute_candidate35_response(
    anchor_brain: IntegratedV05Brain,
    *,
    anchor_time_ms: float,
    arm: Candidate35Arm,
    response_execution_allowed: bool = False,
) -> Candidate35ResponseRecord:
    """Exact candidate response executor, hard-gated off during Architecture R2."""
    if response_execution_allowed is not True:
        raise Candidate35ResponseNotAuthorized(
            "candidate #35 response remains STOP under Architecture R2 authority"
        )
    if arm not in ARMS:
        raise ValueError(f"unknown candidate #35 arm: {arm}")
    if pending_arrival_count(anchor_brain) != 0:
        raise SubthresholdArchitectureUnreachable(
            "candidate #35 response requires queue-empty anchor"
        )
    if abs(float(anchor_brain.current_time_ms) - float(anchor_time_ms)) > 1e-12:
        raise SubthresholdArchitectureUnreachable(
            "candidate #35 anchor time does not match brain time"
        )

    treatment = _clone_with_arm_treatment(anchor_brain, arm)
    ledger_json = _reduction_ledger(anchor_brain, treatment)
    treatment_state_hash = treatment.state_hash()
    delayed = arm == "DELAYED_SHAM_32MS"
    if delayed:
        treatment.base.advance(anchor_time_ms + DELAYED_SHAM_OFFSET_MS)
        if pending_arrival_count(treatment) != 0:
            raise SubthresholdArchitectureUnreachable(
                "delayed sham natural-decay interval did not remain queue empty"
            )
    cue = candidate35_cue(anchor_time_ms=anchor_time_ms, delayed_sham=delayed)
    cue_targets = treatment.base.field.route_pulse(cue)
    result = treatment.base.ingest_pulses((cue,), settle_ms=MEASUREMENT_WINDOW_MS)
    response_payload = {
        "arm": arm,
        "spikes": [row.as_dict() for row in result.spikes],
        "cascades": [row.as_dict() for row in result.cascades],
        "ignitions": [row.as_dict() for row in result.ignitions],
        "cue_routing_targets": list(cue_targets),
        "processed_event_counts": {
            "arrivals": int(treatment.base.field.last_run_arrivals),
            "spikes": int(treatment.base.field.last_run_spikes),
        },
    }
    response_json = canonical_json(response_payload)
    return Candidate35ResponseRecord(
        arm=arm,
        anchor_time_ms=float(anchor_time_ms),
        cue_time_ms=float(cue.time_ms),
        treatment_state_hash=treatment_state_hash,
        causal_response_json=response_json,
        causal_response_sha256=_sha256_text(response_json),
        reduction_ledger_json=ledger_json,
        reduction_ledger_sha256=_sha256_text(ledger_json),
    )


def candidate35_nonresult_preflight() -> Candidate35Preflight:
    """Validate exact R2 bindings without prime, treatment, cue, or response execution."""
    contract_json = canonical_json(candidate35_frozen_contract())
    binding_json = canonical_json(_component_binding())
    brain = build_candidate35_brain()

    field_config = brain.base.field.config
    if float(field_config.membrane_tau_ms) != MEMBRANE_TAU_MS:
        raise AssertionError("candidate #35 membrane decay constant drifted")
    if float(field_config.adaptation_tau_ms) != ADAPTATION_TAU_MS:
        raise AssertionError("candidate #35 adaptation decay constant drifted")
    if float(brain.config.settle_ms) != NORMAL_SETTLE_MS:
        raise AssertionError("candidate #35 normal settle drifted")
    if brain.config.enable_weight_learning or brain.config.enable_delay_learning:
        raise AssertionError("candidate #35 source surface must disable field learning")
    if brain.config.enable_reward_modulation:
        raise AssertionError("candidate #35 source surface must disable reward modulation")
    if pending_arrival_count(brain) != 0:
        raise AssertionError("candidate #35 fresh source must start queue empty")

    probe_cue = candidate35_cue(anchor_time_ms=0.0)
    cue_targets = brain.base.field.route_pulse(probe_cue)
    if not cue_targets:
        raise AssertionError("candidate #35 cue route is empty")
    if brain.current_time_ms != 0.0 or pending_arrival_count(brain) != 0:
        raise AssertionError("NON_RESULT cue routing preflight mutated the source surface")

    return Candidate35Preflight(
        contract_json=contract_json,
        contract_sha256=_sha256_text(contract_json),
        binding_json=binding_json,
        binding_sha256=_sha256_text(binding_json),
        cue_route_targets=tuple(cue_targets),
    )
