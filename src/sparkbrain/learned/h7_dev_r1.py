from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Final

import torch
from torch import Tensor, nn

from .config import LearnedConfig
from .model import SparseRoutingModel, StepOutput

CONTRACT_ID: Final = "H7-DEV-R1-ARCH-CONTRACT-V1"
INTERVENTION_ID: Final = "TOP1_SELECTED_LOCAL_NODE_CUT_V1"
FROZEN_WORLDS: Final = (
    "switchworld",
    "contradiction_world",
    "goal_conflict_world",
    "multi_object_world",
)
FIT_SEEDS: Final = range(7_601_000, 7_601_048)
CALIBRATION_SEEDS: Final = range(7_602_000, 7_602_012)
DISCRIMINATOR_SEEDS: Final = range(7_603_000, 7_603_024)
STEPS_PER_EPISODE: Final = 24
CUT_TOKEN: Final = "CUT"
START_TOKEN: Final = "START"


class ContractConformanceError(RuntimeError):
    """Raised when implementation inputs drift from the frozen contract."""


class ComparatorSpecificationGap(RuntimeError):
    """Raised where R60/R61 do not fix a science-affecting comparator choice."""


@dataclass(frozen=True, slots=True)
class FrozenEpisodeSpec:
    split: str
    seed: int
    world_id: str
    steps: int = STEPS_PER_EPISODE


@dataclass(frozen=True, slots=True)
class PairedStepResult:
    baseline: StepOutput
    cut: StepOutput
    selected: tuple[int, ...]
    target_module: int
    baseline_post_state: Tensor
    cut_post_state: Tensor


@dataclass(frozen=True, slots=True)
class FiniteStateResolvedRow:
    """A row whose previous-prediction state was resolved outside this table core."""

    previous_prediction: str
    route_token: int | str
    label: str


@dataclass(frozen=True, slots=True)
class ImplementationBlocker:
    comparator_id: str
    field: str
    reason: str


def frozen_split_specs(split: str) -> tuple[FrozenEpisodeSpec, ...]:
    seed_ranges = {
        "fit": FIT_SEEDS,
        "calibration": CALIBRATION_SEEDS,
        "discriminator": DISCRIMINATOR_SEEDS,
    }
    try:
        seeds = seed_ranges[split]
    except KeyError as exc:
        raise ValueError(f"unknown H7 DEV-R1 split: {split!r}") from exc
    return tuple(
        FrozenEpisodeSpec(split, seed, FROZEN_WORLDS[index % len(FROZEN_WORLDS)])
        for index, seed in enumerate(seeds)
    )


def assert_discriminator_access_allowed(*, result_bearing_authority: bool) -> None:
    if not result_bearing_authority:
        raise PermissionError(
            "H7 DEV-R1 discriminator access is forbidden during implementation-only cycle 2"
        )


def assert_frozen_contract(contract: dict) -> None:
    created = contract["created_under"]
    surface = contract["development_surface_frozen_for_future_authorized_execution"]
    native = contract["native_development_model"]
    measurement = contract["measurement_contract_for_future_authorized_run"]
    panel = contract["ordinary_reduction_panel"]["comparators"]

    expected = {
        "contract_id": CONTRACT_ID,
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "development_revision": "H7-DEV-R1-CLAIM-SCOPED-CAUSAL-CONTRACT",
        "research_layer": "ARCHITECTURE_STUDY",
        "claim_ceiling": "MECHANISM",
        "preformal_eligible": True,
        "preformal_readiness": "NOT_READY",
        "terminal_state": "ACTIVE",
        "queue_state": "ACTIVE",
        "worlds": list(FROZEN_WORLDS),
        "steps_per_episode": STEPS_PER_EPISODE,
        "fit_seed_range_inclusive": [FIT_SEEDS.start, FIT_SEEDS.stop - 1],
        "calibration_seed_range_inclusive": [
            CALIBRATION_SEEDS.start,
            CALIBRATION_SEEDS.stop - 1,
        ],
        "discriminator_seed_range_inclusive": [
            DISCRIMINATOR_SEEDS.start,
            DISCRIMINATOR_SEEDS.stop - 1,
        ],
        "native_seed": 7601,
        "native_epochs": 4,
        "native_learning_rate": 0.012,
        "native_device": "cpu",
        "event_dim": 24,
        "hidden_dim": 24,
        "module_count": 12,
        "active_k": 4,
        "numerical_no_change_tolerance": 1e-7,
        "comparator_ids": [
            "ORDINARY_DENSE_RECURRENT_V1",
            "FINITE_STATE_ROUTE_HISTORY_V1",
            "ELIGIBILITY_ROUTE_LEDGER_V1",
        ],
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
        "worlds": surface["worlds"],
        "steps_per_episode": surface["steps_per_episode"],
        "fit_seed_range_inclusive": surface["fit_seed_range_inclusive"],
        "calibration_seed_range_inclusive": surface["calibration_seed_range_inclusive"],
        "discriminator_seed_range_inclusive": surface["discriminator_seed_range_inclusive"],
        "native_seed": native["fresh_training_seed"],
        "native_epochs": native["epochs"],
        "native_learning_rate": native["learning_rate"],
        "native_device": native["device"],
        "event_dim": native["event_dim"],
        "hidden_dim": native["hidden_dim"],
        "module_count": native["module_count"],
        "active_k": native["active_k"],
        "numerical_no_change_tolerance": measurement["numerical_no_change_tolerance"],
        "comparator_ids": [row["id"] for row in panel],
    }
    if observed != expected:
        raise ContractConformanceError(
            f"H7 DEV-R1 frozen contract mismatch: expected={expected!r}, observed={observed!r}"
        )


def load_and_assert_frozen_contract(path: str | Path) -> dict:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    assert_frozen_contract(contract)
    return contract


def native_development_config() -> LearnedConfig:
    return replace(
        LearnedConfig(),
        seed=7601,
        epochs=4,
        learning_rate=0.012,
        event_dim=24,
        hidden_dim=24,
        module_count=12,
        active_k=4,
        steps=24,
        device="cpu",
        condition="full",
    )


def dense_recurrent_comparator_config() -> LearnedConfig:
    return replace(
        native_development_config(),
        seed=7602,
        condition="dense_recurrent",
    )


def _paired_arm(
    model: SparseRoutingModel,
    *,
    encoded: Tensor,
    router_probabilities: Tensor,
    selected: Tensor,
    pre_state: Tensor,
    pre_probabilities: Tensor,
    condition: str,
    cut: bool,
) -> tuple[StepOutput, Tensor]:
    k = selected.numel()
    previous = pre_state.index_select(0, selected).clone()
    local_edges = model.edge_weights.index_select(0, selected).index_select(1, selected).clone()
    if cut:
        previous[0] = 0
        local_edges[0, :] = 0
        local_edges[:, 0] = 0

    normalizer = max(1, k - 1)
    messages = torch.tanh(local_edges) @ previous / normalizer
    event_state = torch.tanh(model.event_to_state(encoded)).expand(k, -1)
    updated = model.update(event_state + messages, previous)
    if condition != "no_persistent_state":
        updated = model.config.persistence * updated + (1 - model.config.persistence) * previous
    if cut:
        updated = updated.clone()
        updated[0] = 0

    new_state = pre_state.clone().index_copy(0, selected, updated)
    if condition == "no_persistent_state":
        new_state = torch.zeros_like(new_state)

    pooled = updated.mean(dim=0)
    logits = model.belief_head(pooled)
    if condition != "no_residual":
        logits = logits + model.config.residual_scale * model.residual_head(encoded)
    probabilities = torch.softmax(logits, dim=-1)
    action_logits = model.action_head(pooled)

    support = probabilities.max()
    diversity = router_probabilities.gather(0, selected).sum() / k
    stability = 1.0 - torch.abs(probabilities - pre_probabilities).mean()
    contradiction = 1.0 - torch.dot(probabilities, pre_probabilities)
    components = torch.stack((support, diversity, stability, -contradiction))
    if condition == "detached_coalition" or not model.config.coalition_end_to_end:
        components = components.detach()
    coalition_score = (
        support
        if condition == "no_coalition_score"
        else model.coalition_head(components).squeeze()
    )
    edge_pairs = torch.cartesian_prod(selected, selected)
    output = StepOutput(
        logits,
        action_logits,
        probabilities,
        router_probabilities,
        selected,
        edge_pairs,
        support,
        diversity,
        stability,
        contradiction,
        coalition_score,
    )
    return output, new_state


def paired_top1_selected_local_node_cut(
    model: SparseRoutingModel,
    *,
    evidence: str,
    source: str,
    channel: str,
    strength: float,
    delay: float,
    condition: str | None = None,
) -> PairedStepResult:
    """Execute one frozen baseline/cut pair and commit only the baseline runtime state."""

    condition = condition or model.config.condition
    if condition == "random_router":
        raise ContractConformanceError(
            "TOP1_SELECTED_LOCAL_NODE_CUT_V1 requires deterministic unperturbed selection"
        )

    pre_state = model.module_state.clone()
    pre_probabilities = model.previous_probabilities.clone()
    encoded = model.encoder(evidence, source, channel, strength, delay)
    router_logits = model.router(encoded)
    router_probabilities = torch.softmax(router_logits, dim=-1)
    k = model.config.module_count if condition == "dense_recurrent" else model.config.active_k
    selected = torch.topk(router_logits, k=k, sorted=True).indices

    baseline, baseline_state = _paired_arm(
        model,
        encoded=encoded,
        router_probabilities=router_probabilities,
        selected=selected,
        pre_state=pre_state,
        pre_probabilities=pre_probabilities,
        condition=condition,
        cut=False,
    )
    cut, cut_state = _paired_arm(
        model,
        encoded=encoded,
        router_probabilities=router_probabilities,
        selected=selected,
        pre_state=pre_state,
        pre_probabilities=pre_probabilities,
        condition=condition,
        cut=True,
    )
    if not torch.equal(baseline.selected, cut.selected):
        raise ContractConformanceError("baseline/cut selected IDs diverged")

    model.module_state = baseline_state
    model.previous_probabilities = baseline.probabilities
    selected_ids = tuple(int(index) for index in selected.detach().cpu().tolist())
    return PairedStepResult(
        baseline=baseline,
        cut=cut,
        selected=selected_ids,
        target_module=selected_ids[0],
        baseline_post_state=baseline_state,
        cut_post_state=cut_state,
    )


class FiniteStateRouteHistoryComparator:
    """Exact table core; fitting closure stays blocked until Analyst fixes its semantics."""

    def __init__(self, labels: Sequence[str]) -> None:
        self.labels = tuple(sorted(labels))
        self._counts: dict[tuple[str, int | str], Counter[str]] = {}

    def fit_resolved_rows(self, rows: Iterable[FiniteStateResolvedRow]) -> None:
        for row in rows:
            key = (row.previous_prediction, row.route_token)
            self._counts.setdefault(key, Counter())[row.label] += 1

    def predict_resolved(self, previous_prediction: str, route_token: int | str) -> str:
        key = (previous_prediction, route_token)
        counts = self._counts.get(key)
        if not counts:
            raise ComparatorSpecificationGap(
                "FINITE_STATE_ROUTE_HISTORY_V1 unseen-state fallback is not fixed by the contract"
            )
        maximum = max(counts.values())
        return min(label for label in self.labels if counts[label] == maximum)


class EligibilityRouteLedgerComparator(nn.Module):
    """Frozen ledger/head structure without an invented training or encoder-provenance policy."""

    def __init__(self, *, module_count: int = 12, event_dim: int = 24, labels: int = 3) -> None:
        super().__init__()
        self.module_count = module_count
        self.event_dim = event_dim
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(7603)
            self.head = nn.Linear(module_count + event_dim, labels)

    def initial_ledger(self, *, device: torch.device | None = None) -> Tensor:
        return torch.zeros(self.module_count, device=device)

    def advance_ledger(self, ledger: Tensor, selected: Tensor, *, cut: bool) -> Tensor:
        updated = 0.90 * ledger.clone()
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


def implementation_blockers() -> tuple[ImplementationBlocker, ...]:
    return (
        ImplementationBlocker(
            comparator_id="FINITE_STATE_ROUTE_HISTORY_V1",
            field="fit_state_closure_and_unseen_state_policy",
            reason=(
                "The frozen table key uses previous predicted label, but the contract does not fix "
                "how previous predictions are produced while fitting paired baseline/cut counts or "
                "how unseen state keys predict. Choosing either would change comparator semantics."
            ),
        ),
        ImplementationBlocker(
            comparator_id="ELIGIBILITY_ROUTE_LEDGER_V1",
            field="event_encoder_provenance_training_and_calibration_protocol",
            reason=(
                "The frozen comparator fixes ledger decay, head shape, seed/epochs/lr and "
                "split use, but not which frozen event encoder supplies the 24-d encoding, the "
                "optimizer/loss/update ordering for the head, or what calibration operation means. "
                "Choosing these after R60 would change comparator semantics."
            ),
        ),
    )
