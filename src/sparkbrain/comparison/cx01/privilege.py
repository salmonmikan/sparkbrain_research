from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .contract import ComparatorKind


class ComparatorPrivilege(StrEnum):
    EXPLICIT_EPISODE_BOUNDARY = "explicit-episode-boundary"
    HIGH_ORDER_CONTEXT = "high-order-context"
    PRECISE_TIMESTAMPS = "precise-timestamps"
    FIXED_TOKEN_SDR = "fixed-token-sdr"
    PREDICTIVE_STATE_READOUT = "predictive-state-readout"
    GLOBAL_REPLAY_MODE_SWITCH = "global-replay-mode-switch"
    EXTERNAL_READOUT = "external-readout"
    EXPLICIT_ASSEMBLY_STATE = "explicit-assembly-state"
    TYPED_FUNCTIONAL_HEADS = "typed-functional-heads"
    SCALAR_REWARD = "scalar-reward"


@dataclass(frozen=True, slots=True)
class PrivilegeProfile:
    kind: ComparatorKind
    privileges: tuple[ComparatorPrivilege, ...]
    generated_events_may_train: bool
    evaluator_context_id_visible: bool
    correct_target_visible: bool

    def validate(self) -> None:
        if len(set(self.privileges)) != len(self.privileges):
            raise ValueError("privileges must be unique")
        if self.generated_events_may_train:
            raise ValueError("CX01 comparators must not self-train on generated events")
        if self.evaluator_context_id_visible:
            raise ValueError("CX01 comparators cannot receive evaluator context IDs")
        if self.correct_target_visible:
            raise ValueError("CX01 comparators cannot receive evaluator targets")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["kind"] = self.kind.value
        value["privileges"] = [row.value for row in self.privileges]
        return value


def privilege_profile(kind: ComparatorKind) -> PrivilegeProfile:
    mapping = {
        ComparatorKind.G3_FIRST_ORDER: (),
        ComparatorKind.G4_ASSEMBLY: (
            ComparatorPrivilege.EXPLICIT_ASSEMBLY_STATE,
        ),
        ComparatorKind.G5_TYPED: (
            ComparatorPrivilege.TYPED_FUNCTIONAL_HEADS,
            ComparatorPrivilege.SCALAR_REWARD,
        ),
        ComparatorKind.G6_VARIABLE_ORDER: (
            ComparatorPrivilege.EXPLICIT_EPISODE_BOUNDARY,
            ComparatorPrivilege.HIGH_ORDER_CONTEXT,
        ),
        ComparatorKind.G7_HTM_TEMPORAL_MEMORY: (
            ComparatorPrivilege.EXPLICIT_EPISODE_BOUNDARY,
            ComparatorPrivilege.HIGH_ORDER_CONTEXT,
            ComparatorPrivilege.FIXED_TOKEN_SDR,
            ComparatorPrivilege.PREDICTIVE_STATE_READOUT,
        ),
        ComparatorKind.G8_PREDICTION: (
            ComparatorPrivilege.EXPLICIT_EPISODE_BOUNDARY,
            ComparatorPrivilege.HIGH_ORDER_CONTEXT,
            ComparatorPrivilege.PRECISE_TIMESTAMPS,
            ComparatorPrivilege.PREDICTIVE_STATE_READOUT,
        ),
        ComparatorKind.G8_REPLAY: (
            ComparatorPrivilege.EXPLICIT_EPISODE_BOUNDARY,
            ComparatorPrivilege.HIGH_ORDER_CONTEXT,
            ComparatorPrivilege.PRECISE_TIMESTAMPS,
            ComparatorPrivilege.GLOBAL_REPLAY_MODE_SWITCH,
        ),
    }
    profile = PrivilegeProfile(
        kind=kind,
        privileges=mapping[kind],
        generated_events_may_train=False,
        evaluator_context_id_visible=False,
        correct_target_visible=False,
    )
    profile.validate()
    return profile
