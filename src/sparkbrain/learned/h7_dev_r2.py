from __future__ import annotations

import copy
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from .h7_dev_r1 import (
    CALIBRATION_SEEDS,
    CUT_TOKEN,
    DISCRIMINATOR_SEEDS,
    FIT_SEEDS,
    FROZEN_WORLDS,
    START_TOKEN,
    STEPS_PER_EPISODE,
    ContractConformanceError,
)
from .model import EventEncoder

CONTRACT_ID: Final = "H7-DEV-R2-ARCH-CONTRACT-V1"
DEVELOPMENT_REVISION: Final = "H7-DEV-R2-COMPARATOR-PROTOCOL-CLOSURE"
FINITE_STATE_ID: Final = "FINITE_STATE_ROUTE_HISTORY_V2"
ELIGIBILITY_LEDGER_ID: Final = "ELIGIBILITY_ROUTE_LEDGER_V2"
ENCODER_PROVENANCE: Final = "FITTED_NATIVE_DEV_R2_FROZEN_COPY"
IDENTITY_CALIBRATION: Final = "IDENTITY_NO_TUNABLE_CALIBRATION"
HEAD_SEED: Final = 7603
HEAD_EPOCHS: Final = 4
HEAD_LR: Final = 0.012
LEDGER_DECAY: Final = 0.90
GRAD_CLIP_NORM: Final = 2.0


@dataclass(frozen=True, slots=True)
class FiniteStatePairPrediction:
    baseline: str
    cut: str
    previous_route: int | str
    current_unperturbed_route: int


@dataclass(frozen=True, slots=True)
class LedgerFitStep:
    evidence: str
    source: str
    channel: str
    strength: float
    delay: float
    selected: tuple[int, ...]
    label_index: int


@dataclass(frozen=True, slots=True)
class LedgerPairLogits:
    baseline_logits: Tensor
    cut_logits: Tensor
    baseline_ledger: Tensor
    cut_ledger: Tensor


@dataclass(frozen=True, slots=True)
class InterventionConformanceSnapshot:
    baseline_selected: tuple[int, ...]
    cut_selected: tuple[int, ...]
    baseline_output: Tensor
    cut_output: Tensor
    baseline_input_digest: str
    cut_input_digest: str
    baseline_parameter_digest: str
    cut_parameter_digest: str
    baseline_rng_digest: str
    cut_rng_digest: str
    cut_state_carried_forward: bool


def assert_dev_r2_contract(contract: dict) -> None:
    created = contract["created_under"]
    inherited = contract["inherited_scientific_fields"]
    panel = contract["ordinary_reduction_panel"]["comparators"]
    intervention = contract["intervention"]

    expected = {
        "contract_id": CONTRACT_ID,
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "development_revision": DEVELOPMENT_REVISION,
        "research_layer": "ARCHITECTURE_STUDY",
        "claim_ceiling": "MECHANISM",
        "preformal_eligible": True,
        "preformal_readiness": "NOT_READY",
        "terminal_state": "ACTIVE",
        "queue_state": "ACTIVE",
        "worlds": list(FROZEN_WORLDS),
        "steps": STEPS_PER_EPISODE,
        "fit": [FIT_SEEDS.start, FIT_SEEDS.stop - 1],
        "calibration": [CALIBRATION_SEEDS.start, CALIBRATION_SEEDS.stop - 1],
        "discriminator": [DISCRIMINATOR_SEEDS.start, DISCRIMINATOR_SEEDS.stop - 1],
        "comparators": [
            "ORDINARY_DENSE_RECURRENT_V1",
            FINITE_STATE_ID,
            ELIGIBILITY_LEDGER_ID,
        ],
        "intervention_id": "TOP1_SELECTED_LOCAL_NODE_CUT_V1",
        "cut_discarded": True,
    }
    observed = {
        "contract_id": contract["contract_id"],
        "development_phase": created["development_phase"],
        "development_revision": created["development_revision"],
        "research_layer": created["research_layer"],
        "claim_ceiling": created["claim_ceiling"],
        "preformal_eligible": created["preformal_eligible"],
        "preformal_readiness": created["preformal_readiness"],
        "terminal_state": created["terminal_state"],
        "queue_state": created["queue_state"],
        "worlds": inherited["worlds"],
        "steps": inherited["steps_per_episode"],
        "fit": inherited["fit_seed_range_inclusive"],
        "calibration": inherited["calibration_seed_range_inclusive"],
        "discriminator": inherited["discriminator_seed_range_inclusive"],
        "comparators": [row["id"] for row in panel],
        "intervention_id": intervention["id"],
        "cut_discarded": intervention["one_step_discarded"],
    }
    if observed != expected:
        raise ContractConformanceError(
            f"H7 DEV-R2 contract mismatch: expected={expected!r}, observed={observed!r}"
        )


def load_and_assert_dev_r2_contract(path: str | Path) -> dict:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    assert_dev_r2_contract(contract)
    return contract


class FiniteStateRouteHistoryV2:
    """Prospectively fixed route-history comparator from Analyst R62/R63."""

    def __init__(self, labels: Sequence[str]) -> None:
        self.labels = tuple(sorted(labels))
        if not self.labels:
            raise ValueError("FINITE_STATE_ROUTE_HISTORY_V2 requires at least one label")
        self._counts: dict[tuple[int | str, int | str], Counter[str]] = {}
        self._global_counts: Counter[str] = Counter()
        self._previous_unperturbed_route: int | str = START_TOKEN

    def reset_episode(self) -> None:
        self._previous_unperturbed_route = START_TOKEN

    @property
    def previous_unperturbed_route(self) -> int | str:
        return self._previous_unperturbed_route

    def fit_step(self, *, unperturbed_rank1_route: int, label: str) -> None:
        if label not in self.labels:
            raise ValueError(f"unknown label: {label!r}")
        previous = self._previous_unperturbed_route
        for current in (unperturbed_rank1_route, CUT_TOKEN):
            key = (previous, current)
            self._counts.setdefault(key, Counter())[label] += 1
        self._global_counts[label] += 1
        self._previous_unperturbed_route = unperturbed_rank1_route

    def _majority(self, counts: Counter[str]) -> str:
        if not counts:
            raise ContractConformanceError(
                "FINITE_STATE_ROUTE_HISTORY_V2 requires fit-split counts before prediction"
            )
        maximum = max(counts.values())
        return min(label for label in self.labels if counts[label] == maximum)

    def _predict_key(self, key: tuple[int | str, int | str]) -> str:
        counts = self._counts.get(key)
        if counts:
            return self._majority(counts)
        return self._majority(self._global_counts)

    def predict_pair(self, *, unperturbed_rank1_route: int) -> FiniteStatePairPrediction:
        previous = self._previous_unperturbed_route
        baseline = self._predict_key((previous, unperturbed_rank1_route))
        cut = self._predict_key((previous, CUT_TOKEN))
        self._previous_unperturbed_route = unperturbed_rank1_route
        return FiniteStatePairPrediction(
            baseline=baseline,
            cut=cut,
            previous_route=previous,
            current_unperturbed_route=unperturbed_rank1_route,
        )


class EligibilityRouteLedgerV2(nn.Module):
    """Exact DEV-R2 structural/training implementation; cycle-3 tests never invoke fit()."""

    def __init__(
        self,
        native_event_encoder: EventEncoder,
        *,
        encoder_provenance: str,
        module_count: int = 12,
        event_dim: int = 24,
        labels: int = 3,
    ) -> None:
        super().__init__()
        if encoder_provenance != ENCODER_PROVENANCE:
            raise ContractConformanceError(
                f"ELIGIBILITY_ROUTE_LEDGER_V2 requires {ENCODER_PROVENANCE!r} provenance"
            )
        self.module_count = module_count
        self.event_dim = event_dim
        self.encoder_provenance = encoder_provenance
        self.event_encoder = copy.deepcopy(native_event_encoder).eval()
        for parameter in self.event_encoder.parameters():
            parameter.requires_grad_(False)
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(HEAD_SEED)
            self.head = nn.Linear(module_count + event_dim, labels)

    @property
    def calibration_operation(self) -> str:
        return IDENTITY_CALIBRATION

    def initial_ledger(self, *, device: torch.device | None = None) -> Tensor:
        return torch.zeros(self.module_count, device=device)

    def encode_event(
        self,
        *,
        evidence: str,
        source: str,
        channel: str,
        strength: float,
        delay: float,
    ) -> Tensor:
        with torch.no_grad():
            encoded = self.event_encoder(evidence, source, channel, strength, delay)
        return encoded.detach()

    def advance_ledger(self, ledger: Tensor, selected: Tensor, *, cut: bool) -> Tensor:
        updated = LEDGER_DECAY * ledger.clone()
        active = selected[1:] if cut else selected
        updated.index_add_(0, active, torch.ones_like(active, dtype=updated.dtype))
        if cut:
            updated[selected[0]] = 0
        return updated

    def logits(self, ledger: Tensor, event_encoding: Tensor) -> Tensor:
        if event_encoding.numel() != self.event_dim:
            raise ContractConformanceError(
                f"event encoding must have {self.event_dim} values, got {event_encoding.numel()}"
            )
        return self.head(torch.cat((ledger, event_encoding)))

    def paired_logits(
        self,
        ledger: Tensor,
        selected: Tensor,
        event_encoding: Tensor,
    ) -> LedgerPairLogits:
        baseline_ledger = self.advance_ledger(ledger, selected, cut=False)
        cut_ledger = self.advance_ledger(ledger, selected, cut=True)
        return LedgerPairLogits(
            baseline_logits=self.logits(baseline_ledger, event_encoding),
            cut_logits=self.logits(cut_ledger, event_encoding),
            baseline_ledger=baseline_ledger,
            cut_ledger=cut_ledger,
        )

    def fit(self, episodes: Sequence[Sequence[LedgerFitStep]]) -> None:
        """Implement the frozen fit protocol. Not authorized to execute in cycle 3."""

        optimizer = torch.optim.Adam(self.head.parameters(), lr=HEAD_LR, weight_decay=0.0)
        for epoch in range(HEAD_EPOCHS):
            generator = torch.Generator(device="cpu")
            generator.manual_seed(HEAD_SEED + epoch)
            order = torch.randperm(len(episodes), generator=generator).tolist()
            for episode_index in order:
                episode = episodes[episode_index]
                if not episode:
                    raise ContractConformanceError("ledger fit episode must not be empty")
                ledger = self.initial_ledger(device=self.head.weight.device)
                optimizer.zero_grad()
                losses: list[Tensor] = []
                for step in episode:
                    selected = torch.tensor(
                        step.selected,
                        dtype=torch.long,
                        device=self.head.weight.device,
                    )
                    ledger = self.advance_ledger(ledger, selected, cut=False)
                    encoded = self.encode_event(
                        evidence=step.evidence,
                        source=step.source,
                        channel=step.channel,
                        strength=step.strength,
                        delay=step.delay,
                    ).to(self.head.weight.device)
                    logits = self.logits(ledger, encoded)
                    target = torch.tensor(
                        [step.label_index],
                        dtype=torch.long,
                        device=logits.device,
                    )
                    losses.append(F.cross_entropy(logits.unsqueeze(0), target))
                torch.stack(losses).mean().backward()
                torch.nn.utils.clip_grad_norm_(self.head.parameters(), GRAD_CLIP_NORM)
                optimizer.step()


def assert_intervention_well_posed(snapshot: InterventionConformanceSnapshot) -> None:
    if snapshot.baseline_selected != snapshot.cut_selected:
        raise ContractConformanceError("INVALID_INTERVENTION: selected route IDs differ")
    if snapshot.baseline_output.shape != snapshot.cut_output.shape:
        raise ContractConformanceError("INVALID_INTERVENTION: output shape differs")
    if snapshot.baseline_output.dtype != snapshot.cut_output.dtype:
        raise ContractConformanceError("INVALID_INTERVENTION: output dtype differs")
    if not torch.isfinite(snapshot.baseline_output).all() or not torch.isfinite(
        snapshot.cut_output
    ).all():
        raise ContractConformanceError("INVALID_INTERVENTION: output is non-finite")
    if snapshot.baseline_input_digest != snapshot.cut_input_digest:
        raise ContractConformanceError("INVALID_INTERVENTION: non-target input changed")
    if snapshot.baseline_parameter_digest != snapshot.cut_parameter_digest:
        raise ContractConformanceError("INVALID_INTERVENTION: parameters changed")
    if snapshot.baseline_rng_digest != snapshot.cut_rng_digest:
        raise ContractConformanceError("INVALID_INTERVENTION: RNG state changed")
    if snapshot.cut_state_carried_forward:
        raise ContractConformanceError("INVALID_INTERVENTION: cut state carried forward")


def assert_cycle3_non_result_bearing_authority(
    *,
    training: bool = False,
    calibration: bool = False,
    discriminator: bool = False,
    scientific_metric: bool = False,
) -> None:
    requested = {
        "training": training,
        "calibration": calibration,
        "discriminator": discriminator,
        "scientific_metric": scientific_metric,
    }
    forbidden = [name for name, enabled in requested.items() if enabled]
    if forbidden:
        raise PermissionError(
            "H7 DEV-R2 cycle3 implementation-only authority forbids: " + ", ".join(forbidden)
        )
