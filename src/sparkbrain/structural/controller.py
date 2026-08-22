from __future__ import annotations

import heapq
import random
from typing import Any

import torch

from .config import StructuralConfig
from .contracts import StructuralEvent, StructuralIdentity, StructuralStats
from .model import StructuralSparseModel

EVENT_PRIORITY = {
    "edge_prune": 10,
    "module_prune": 20,
    "merge": 30,
    "create": 40,
    "duplicate": 50,
    "split": 60,
    "edge_grow": 70,
}


def _restore_tuple(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_restore_tuple(item) for item in value)
    return value


class StructuralController:
    def __init__(self, config: StructuralConfig, model: StructuralSparseModel) -> None:
        self.config = config
        self.model = model
        self.random = random.Random(config.seed)
        self.sequence = 0
        self.identity_counter = config.source_modules
        self.pending: list[StructuralEvent] = []
        self.history: list[StructuralEvent] = []
        self.tombstones: list[StructuralIdentity] = []
        self.events_applied = 0
        self.events_rejected = 0
        self.homeostatic_updates = 0
        self.remaining_budget = config.max_events_total
        self.identities: dict[int, StructuralIdentity] = {
            slot: StructuralIdentity(f"source:{slot}", slot, 1, "active", None)
            for slot in range(config.source_modules)
        }

    def _new_identity(
        self, slot: int, *, event: StructuralEvent, parents: tuple[str, ...]
    ) -> None:
        old = self.identities.get(slot)
        version = (old.version + 1) if old else 1
        if old is not None:
            old.status = "tombstone"
            old.tombstone_reason = "slot_reused"
            self.tombstones.append(old)
        logical_id = f"struct:{self.config.seed}:{self.identity_counter}"
        self.identity_counter += 1
        self.identities[slot] = StructuralIdentity(
            logical_id, slot, version, "active", event.sequence, parents
        )

    def queue_event(
        self,
        *,
        boundary: int,
        kind: str,
        source_slot: int | None = None,
        target_slot: int | None = None,
        score: float = 0.0,
        reason: str = "",
    ) -> StructuralEvent:
        if kind not in EVENT_PRIORITY:
            raise ValueError(f"Unknown structural event: {kind}")
        event = StructuralEvent(
            boundary,
            EVENT_PRIORITY[kind],
            self.sequence,
            kind,
            source_slot,
            target_slot,
            score,
            reason,
        )
        self.sequence += 1
        heapq.heappush(self.pending, event)
        return event

    def discover(self, stats: StructuralStats, *, next_boundary: int) -> list[StructuralEvent]:
        """Queue candidates from unlabeled dynamics statistics only."""
        stats.validate(self.config.max_modules)
        self.apply_homeostasis(stats)
        active = torch.where(self.model.active_module_mask)[0].tolist()
        inactive = torch.where(~self.model.active_module_mask)[0].tolist()
        total = sum(stats.routing_load[index] for index in active) or 1.0
        mean_load = total / len(active)
        candidates: list[tuple[float, str, int | None, int | None, str]] = []
        if inactive:
            overloaded = max(active, key=lambda item: stats.routing_load[item])
            ratio = stats.routing_load[overloaded] / max(mean_load, 1e-9)
            if ratio >= self.config.load_high:
                candidates.append(
                    (ratio, "duplicate", overloaded, inactive[0], "routing_load_high")
                )
        if len(active) > self.config.min_live_modules:
            underused = min(active, key=lambda item: stats.routing_load[item])
            ratio = stats.routing_load[underused] / max(mean_load, 1e-9)
            if ratio <= self.config.load_low:
                candidates.append((1 - ratio, "module_prune", underused, None, "load_low"))
        best_grow: tuple[float, int, int] | None = None
        best_prune: tuple[float, int, int] | None = None
        for source in active:
            for target in active:
                credit = stats.edge_credit[source][target]
                if (
                    not self.model.active_edge_mask[source, target]
                    and credit >= self.config.grow_credit
                ):
                    if best_grow is None or credit > best_grow[0]:
                        best_grow = (credit, source, target)
                if (
                    self.model.active_edge_mask[source, target]
                    and credit <= self.config.prune_credit
                ):
                    if best_prune is None or credit < best_prune[0]:
                        best_prune = (credit, source, target)
        if best_grow:
            candidates.append(
                (best_grow[0], "edge_grow", best_grow[1], best_grow[2], "edge_credit_high")
            )
        if best_prune:
            candidates.append(
                (1 - best_prune[0], "edge_prune", best_prune[1], best_prune[2], "edge_credit_low")
            )
        candidates.sort(key=lambda row: (-row[0], EVENT_PRIORITY[row[1]], row[2] or -1))
        return [
            self.queue_event(
                boundary=next_boundary,
                kind=kind,
                source_slot=source,
                target_slot=target,
                score=score,
                reason=reason,
            )
            for score, kind, source, target, reason in candidates[
                : self.config.max_events_per_boundary
            ]
        ]

    def apply_homeostasis(self, stats: StructuralStats) -> None:
        stats.validate(self.config.max_modules)
        active = torch.where(self.model.active_module_mask)[0].tolist()
        mean_load = sum(stats.routing_load[index] for index in active) / max(1, len(active))
        if mean_load <= 0:
            return
        with torch.no_grad():
            for slot in active:
                deviation = stats.routing_load[slot] / mean_load - 1.0
                self.model.router.bias[slot].sub_(self.config.homeostasis_rate * deviation)
        self.homeostatic_updates += 1

    def apply_boundary(self, boundary: int) -> list[StructuralEvent]:
        applied: list[StructuralEvent] = []
        boundary_count = 0
        deferred: list[StructuralEvent] = []
        while self.pending:
            event = heapq.heappop(self.pending)
            if event.boundary > boundary:
                deferred.append(event)
                continue
            if boundary_count >= self.config.max_events_per_boundary:
                self._reject(event, "boundary_budget")
            elif self.remaining_budget <= 0:
                self._reject(event, "run_budget")
            elif event.kind not in self.config.enabled_events:
                self._reject(event, "event_disabled")
            elif self._apply(event):
                event.status = "applied"
                self.events_applied += 1
                self.remaining_budget -= 1
                boundary_count += 1
                self.history.append(event)
                applied.append(event)
            else:
                self._reject(event, event.rejection or "invariant")
        for event in deferred:
            heapq.heappush(self.pending, event)
        return applied

    def _reject(self, event: StructuralEvent, reason: str) -> None:
        event.status = "rejected"
        event.rejection = reason
        self.events_rejected += 1
        self.history.append(event)

    def _empty_slot(self) -> int | None:
        rows = torch.where(~self.model.active_module_mask)[0].tolist()
        return rows[0] if rows else None

    def _apply(self, event: StructuralEvent) -> bool:
        source, target = event.source_slot, event.target_slot
        active = self.model.active_module_mask
        edges = self.model.active_edge_mask
        if event.kind in {"create", "duplicate", "split"}:
            target = target if target is not None else self._empty_slot()
            if target is None or bool(active[target]):
                event.rejection = "module_capacity"
                return False
            parents: tuple[str, ...] = ()
            with torch.no_grad():
                if event.kind in {"duplicate", "split"}:
                    if source is None or not bool(active[source]):
                        event.rejection = "inactive_source"
                        return False
                    parents = (self.identities[source].logical_id,)
                    self.model.router.weight[target].copy_(self.model.router.weight[source])
                    self.model.router.bias[target].copy_(self.model.router.bias[source])
                    self.model.edge_weights[target].copy_(self.model.edge_weights[source])
                    self.model.edge_weights[:, target].copy_(self.model.edge_weights[:, source])
                    if event.kind == "split":
                        noise = torch.tensor(
                            [
                                self.random.uniform(-0.01, 0.01)
                                for _ in self.model.router.weight[target]
                            ],
                            dtype=self.model.router.weight.dtype,
                        )
                        self.model.router.weight[target].add_(noise)
                active[target] = True
                edges[target, target] = True
            self._new_identity(target, event=event, parents=parents)
            return True
        if event.kind == "merge":
            if source is None or target is None or source == target:
                event.rejection = "merge_operands"
                return False
            if not bool(active[source]) or not bool(active[target]):
                event.rejection = "inactive_operand"
                return False
            if int(active.sum()) <= self.config.min_live_modules:
                event.rejection = "minimum_modules"
                return False
            parents = (self.identities[source].logical_id, self.identities[target].logical_id)
            with torch.no_grad():
                self.model.router.weight[source].copy_(
                    (self.model.router.weight[source] + self.model.router.weight[target]) / 2
                )
                active[target] = False
                edges[target, :] = False
                edges[:, target] = False
            old = self.identities[target]
            old.status = "tombstone"
            old.tombstone_reason = "merged"
            self.tombstones.append(old)
            self.identities.pop(target)
            self.identities[source].version += 1
            self.identities[source].parents = parents
            return True
        if event.kind == "module_prune":
            if source is None or not bool(active[source]):
                event.rejection = "inactive_source"
                return False
            if int(active.sum()) <= self.config.min_live_modules:
                event.rejection = "minimum_modules"
                return False
            active[source] = False
            edges[source, :] = False
            edges[:, source] = False
            old = self.identities.pop(source)
            old.status = "tombstone"
            old.tombstone_reason = "pruned"
            self.tombstones.append(old)
            return True
        if event.kind == "edge_grow":
            if (
                source is None
                or target is None
                or not bool(active[source])
                or not bool(active[target])
            ):
                event.rejection = "inactive_endpoint"
                return False
            if int(edges.sum()) >= self.config.max_active_edges:
                event.rejection = "edge_capacity"
                return False
            edges[source, target] = True
            return True
        if event.kind == "edge_prune":
            if source is None or target is None or not bool(edges[source, target]):
                event.rejection = "inactive_edge"
                return False
            if int(edges[:, target].sum()) <= self.config.min_in_degree:
                event.rejection = "minimum_in_degree"
                return False
            edges[source, target] = False
            return True
        event.rejection = "unsupported"
        return False

    def candidate_group(self, stats: StructuralStats, *, size: int = 2) -> tuple[int, ...]:
        """Return a label-free high-credit lineage/interaction candidate."""
        stats.validate(self.config.max_modules)
        active = torch.where(self.model.active_module_mask)[0].tolist()
        scored = sorted(
            active,
            key=lambda slot: (
                -stats.routing_load[slot],
                -sum(stats.coactivation[slot]),
                slot,
            ),
        )
        return tuple(scored[: min(size, len(scored))])

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "sequence": self.sequence,
            "identity_counter": self.identity_counter,
            "pending": [event.to_dict() for event in sorted(self.pending)],
            "history": [event.to_dict() for event in self.history],
            "identities": {str(slot): row.to_dict() for slot, row in self.identities.items()},
            "tombstones": [row.to_dict() for row in self.tombstones],
            "events_applied": self.events_applied,
            "events_rejected": self.events_rejected,
            "homeostatic_updates": self.homeostatic_updates,
            "remaining_budget": self.remaining_budget,
            "rng_state": self.random.getstate(),
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        restored_config = StructuralConfig.from_dict(state.get("config", {}))
        if restored_config != self.config:
            raise ValueError("Structural controller config mismatch")
        self.sequence = int(state["sequence"])
        self.identity_counter = int(state["identity_counter"])
        self.pending = [StructuralEvent(**row) for row in state["pending"]]
        heapq.heapify(self.pending)
        sequences = [event.sequence for event in self.pending]
        if len(sequences) != len(set(sequences)):
            raise ValueError("Pending structural event sequences must be unique")
        if sequences and self.sequence <= max(sequences):
            raise ValueError("Next structural sequence must exceed pending events")
        self.history = [StructuralEvent(**row) for row in state["history"]]
        self.identities = {
            int(slot): StructuralIdentity(
                **{**row, "parents": tuple(row.get("parents", ()))}
            )
            for slot, row in state["identities"].items()
        }
        self.tombstones = [
            StructuralIdentity(**{**row, "parents": tuple(row.get("parents", ()))})
            for row in state["tombstones"]
        ]
        self.events_applied = int(state["events_applied"])
        self.events_rejected = int(state["events_rejected"])
        self.homeostatic_updates = int(state.get("homeostatic_updates", 0))
        self.remaining_budget = int(state["remaining_budget"])
        self.random.setstate(_restore_tuple(state["rng_state"]))
