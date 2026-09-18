from __future__ import annotations

import random
from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable


@dataclass(frozen=True, slots=True)
class LineageEvent:
    """A synthetic/dev lineage event. It is never a formal observation row."""

    child: str
    parents: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class QueryResult:
    ancestor: str
    descendants: tuple[str, ...]
    visited_records: int


class ActualLineageIndex:
    """Reference semantics for actual append-only parent relations.

    This is deliberately small and dependency-free. A later formal adapter, if authorized,
    must bind these semantics to StructuralController identities/tombstones without changing
    the prospective contract.
    """

    def __init__(self) -> None:
        self.parents: dict[str, tuple[str, ...]] = {}
        self.children: dict[str, set[str]] = {}

    def apply(self, event: LineageEvent) -> None:
        if event.child in self.parents:
            raise ValueError(f"child already exists: {event.child}")
        if event.child in event.parents:
            raise ValueError("self-parent is forbidden")
        for parent in event.parents:
            if parent not in self.parents:
                raise ValueError(f"unknown parent: {parent}")
        self.parents[event.child] = event.parents
        self.children.setdefault(event.child, set())
        for parent in event.parents:
            self.children.setdefault(parent, set()).add(event.child)

    def add_root(self, logical_id: str) -> None:
        if logical_id in self.parents:
            raise ValueError(f"duplicate logical id: {logical_id}")
        self.parents[logical_id] = ()
        self.children.setdefault(logical_id, set())

    def descendants_of(self, ancestor: str, live_ids: Iterable[str]) -> QueryResult:
        if ancestor not in self.parents:
            raise KeyError(ancestor)
        live = set(live_ids)
        stack = [ancestor]
        seen: set[str] = set()
        visited = 0
        while stack:
            node = stack.pop()
            for child in sorted(self.children.get(node, ())):
                visited += 1
                if child in seen:
                    continue
                seen.add(child)
                stack.append(child)
        return QueryResult(ancestor, tuple(sorted(seen & live)), visited)


class ExplicitParentTable:
    """Independent ordinary explicit-state reduction.

    It consumes the same admitted event stream but stores transitive ancestors directly.
    It does not call ActualLineageIndex query logic.
    """

    def __init__(self) -> None:
        self.ancestors: dict[str, frozenset[str]] = {}

    def add_root(self, logical_id: str) -> None:
        if logical_id in self.ancestors:
            raise ValueError(f"duplicate logical id: {logical_id}")
        self.ancestors[logical_id] = frozenset()

    def apply(self, event: LineageEvent) -> None:
        if event.child in self.ancestors:
            raise ValueError(f"child already exists: {event.child}")
        inherited: set[str] = set()
        for parent in event.parents:
            if parent not in self.ancestors:
                raise ValueError(f"unknown parent: {parent}")
            inherited.add(parent)
            inherited.update(self.ancestors[parent])
        self.ancestors[event.child] = frozenset(inherited)

    def descendants_of(self, ancestor: str, live_ids: Iterable[str]) -> QueryResult:
        live = tuple(live_ids)
        descendants = tuple(
            sorted(node for node in live if ancestor in self.ancestors.get(node, ()))
        )
        return QueryResult(ancestor, descendants, len(live))


class RecentWindowState:
    """Bounded recent-event comparator with no access to older ancestry."""

    def __init__(self, max_events: int) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be positive")
        self.max_events = max_events
        self.events: list[LineageEvent] = []

    def apply(self, event: LineageEvent) -> None:
        self.events.append(event)
        if len(self.events) > self.max_events:
            del self.events[0]

    def descendants_of(self, ancestor: str, live_ids: Iterable[str]) -> QueryResult:
        parents = {event.child: event.parents for event in self.events}
        live = set(live_ids)
        found: set[str] = set()
        visits = 0
        changed = True
        while changed:
            changed = False
            for child, child_parents in parents.items():
                visits += 1
                if child in found:
                    continue
                direct = ancestor in child_parents
                inherited = any(parent in found for parent in child_parents)
                if direct or inherited:
                    found.add(child)
                    changed = True
        return QueryResult(ancestor, tuple(sorted(found & live)), visits)


def opaque_id(seed: int, ordinal: int) -> str:
    return sha256(f"lp01:{seed}:{ordinal}".encode()).hexdigest()[:20]


def generate_history(
    *, seed: int, live_nodes: int, history_events: int
) -> tuple[tuple[str, ...], tuple[LineageEvent, ...], tuple[str, ...]]:
    """Generate a deterministic dev-only acyclic history.

    IDs are opaque hashes and present live-node ordering is independent of ancestry labels.
    """

    if live_nodes < 8:
        raise ValueError("live_nodes must be at least 8")
    if history_events < live_nodes:
        raise ValueError("history_events must be >= live_nodes")
    rng = random.Random(seed)
    root_count = 6
    roots = tuple(opaque_id(seed, index) for index in range(root_count))
    known = list(roots)
    events: list[LineageEvent] = []
    for offset in range(history_events):
        child = opaque_id(seed, root_count + offset)
        parent_count = 2 if len(known) >= 2 and rng.random() < 0.4 else 1
        parents = tuple(sorted(rng.sample(known, parent_count)))
        event = LineageEvent(child, parents)
        events.append(event)
        known.append(child)
    live = tuple(sorted(known[-live_nodes:]))
    return roots, tuple(events), live


def destroy_provenance(
    roots: tuple[str, ...], events: tuple[LineageEvent, ...], *, seed: int
) -> tuple[LineageEvent, ...]:
    """Destroy ancestry while preserving event order and parent arity.

    Parent choices remain restricted to already-existing nodes, so acyclicity is preserved.
    This is a dev/reference transform only; a future formal preserver must freeze its exact
    implementation and digest before any identity is created.
    """

    known = list(roots)
    destroyed: list[LineageEvent] = []
    rng = random.Random(seed)
    for event in events:
        if not event.parents:
            replacement = ()
        elif len(known) == 1:
            replacement = (known[0],)
        else:
            candidates = known.copy()
            rng.shuffle(candidates)
            replacement_list: list[str] = []
            for original in event.parents:
                for candidate in candidates:
                    if candidate != original and candidate not in replacement_list:
                        replacement_list.append(candidate)
                        break
                else:
                    replacement_list.append(original)
            replacement = tuple(sorted(replacement_list))
        destroyed.append(LineageEvent(event.child, replacement))
        known.append(event.child)
    return tuple(destroyed)


def build_indexes(
    roots: tuple[str, ...], events: tuple[LineageEvent, ...], *, recent_window: int
) -> tuple[ActualLineageIndex, ExplicitParentTable, RecentWindowState]:
    actual = ActualLineageIndex()
    explicit = ExplicitParentTable()
    recent = RecentWindowState(recent_window)
    for root in roots:
        actual.add_root(root)
        explicit.add_root(root)
    for event in events:
        actual.apply(event)
        explicit.apply(event)
        recent.apply(event)
    return actual, explicit, recent


def construction_digest(
    roots: tuple[str, ...], events: tuple[LineageEvent, ...], live_ids: tuple[str, ...]
) -> str:
    payload = ["roots=" + ",".join(roots), "live=" + ",".join(live_ids)]
    payload.extend(f"{event.child}<-{','.join(event.parents)}" for event in events)
    return sha256("\n".join(payload).encode()).hexdigest()


def present_state_digest(*, seed: int, live_ids: tuple[str, ...], recent_token: str) -> str:
    """Opaque matched-present-state digest independent of ancestry relation."""

    payload = f"present:{seed}:{recent_token}:" + ",".join(sorted(live_ids))
    return sha256(payload.encode()).hexdigest()
