from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

P4CreditScope = Literal[
    "all-resolved-paths",
    "partial-resolved-paths",
    "no-credit",
]

_CREDITING_STATUSES = {"exact-match", "exact-contradiction"}


@dataclass(frozen=True, slots=True)
class P4MergedLineageCreditProbe:
    """Development-only observation of how merged ancestry receives A01 credit.

    This is deliberately not a P4 scorer and cannot mark P4 pass/fail. P4 is
    downstream of P3 in the MD-002 development plan, so this probe only records
    the current bridge's credit scope for a genuinely merged boundary event.
    """

    boundary_event_id: str
    source_proposal_ids: tuple[str, ...]
    credited_path_ids: tuple[str, ...]
    status: str
    path_reliability_before: tuple[tuple[str, float], ...]
    path_reliability_after: tuple[tuple[str, float], ...]
    changed_path_ids: tuple[str, ...]
    credit_scope: P4CreditScope
    development_only: bool = True
    formal_p4_result: None = None

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _pending_state(bridge: Any) -> dict[str, Any]:
    return dict(bridge.consistency.state_dict().get("pending", {}))


def _require_registered_boundary_payload(bridge: Any, boundary: Any) -> None:
    """Fail closed unless the supplied boundary is exactly the pending event."""

    registered = _pending_state(bridge).get(boundary.event_id)
    if registered is None:
        raise ValueError("P4 merged-lineage boundary must be registered and pending")
    if registered.get("event") != boundary.state_dict():
        raise ValueError("P4 merged-lineage boundary must match registered pending boundary")


def _require_selected_exact_parent(bridge: Any, boundary: Any, external: Any) -> None:
    """Require an unambiguous exact parent before consistency can mutate state."""

    pending = _pending_state(bridge)
    valid_exact: list[str] = []
    for event_id in dict.fromkeys(external.parent_event_ids):
        row = pending.get(event_id)
        if row is None:
            continue
        event = row["event"]
        lag_ms = external.time_ms - float(event["time_ms"])
        if (
            0 <= lag_ms <= bridge.consistency.config.maximum_pair_lag_ms
            and external.time_ms <= float(row["valid_until_ms"])
        ):
            valid_exact.append(event_id)

    if valid_exact != [boundary.event_id]:
        raise ValueError(
            "P4 merged-lineage credit probe requires one unambiguous selected exact parent"
        )


def _require_unused_external_evidence(bridge: Any, external: Any) -> None:
    """Prevent one external pulse from becoming multiple credit observations."""

    if any(
        row.external_event_id == external.event_id
        for row in bridge.consistency.resolutions
    ):
        raise ValueError("P4 merged-lineage external evidence must not be reused")


def _validate_causal_ancestry(bridge: Any, proposal_ids: tuple[str, ...]) -> None:
    """Resolve ancestry and local paths fully before any pending state is consumed."""

    pending = list(proposal_ids)
    visited: set[str] = set()
    paths: set[str] = set()
    while pending:
        proposal_id = pending.pop()
        if proposal_id in visited:
            continue
        visited.add(proposal_id)
        proposal = bridge.ledger.proposals.get(proposal_id)
        if proposal is None:
            raise ValueError(f"P4 merged-lineage boundary references unknown proposal: {proposal_id}")
        paths.update(proposal.local_path_ids)
        pending.extend(proposal.parent_proposal_ids)

    if not paths:
        raise ValueError("P4 merged-lineage ancestry must resolve to local causal paths")

    learned = bridge.expectation.learned_state_dict()
    known_paths = {
        f"local:{source}->{target}"
        for source, table in learned.get("transitions", {}).items()
        for target in table
    }
    unknown_paths = paths - known_paths
    if unknown_paths:
        raise ValueError(
            f"P4 merged-lineage ancestry references unknown local paths: {sorted(unknown_paths)}"
        )


def probe_merged_lineage_credit(
    bridge: Any,
    *,
    boundary: Any,
    external: Any,
) -> P4MergedLineageCreditProbe:
    """Apply one already-admissible external event and record merged credit scope.

    The caller remains responsible for registering the boundary with the shared
    consistency model and the external event with the shared provenance ledger.
    The probe refuses singleton ancestry so it cannot be mistaken for P4 data.
    It also requires an exact, unambiguous parent relation: fallback or competing
    temporal pairing is not evidence about lineage-specific causal credit.
    """

    source_proposal_ids = tuple(dict.fromkeys(boundary.source_proposal_ids))
    if len(source_proposal_ids) < 2:
        raise ValueError("P4 merged-lineage credit probe requires plural source ancestry")
    if len(source_proposal_ids) != len(boundary.source_proposal_ids):
        raise ValueError("P4 merged-lineage source proposal IDs must be unique")
    if boundary.event_id not in external.parent_event_ids:
        raise ValueError("P4 merged-lineage credit probe requires exact-parent evidence")
    _require_registered_boundary_payload(bridge, boundary)
    _require_selected_exact_parent(bridge, boundary, external)
    _require_unused_external_evidence(bridge, external)
    _validate_causal_ancestry(bridge, source_proposal_ids)

    resolution = bridge.observe_external(boundary, external)
    before = dict(resolution.path_reliability_before)
    after = dict(resolution.path_reliability_after)
    credited_path_ids = resolution.path_ids
    changed_path_ids = tuple(
        path_id
        for path_id in credited_path_ids
        if before.get(path_id) != after.get(path_id)
    )
    status = resolution.status.value

    if not credited_path_ids or status not in _CREDITING_STATUSES:
        credit_scope: P4CreditScope = "no-credit"
    elif set(changed_path_ids) == set(credited_path_ids):
        credit_scope = "all-resolved-paths"
    else:
        credit_scope = "partial-resolved-paths"

    return P4MergedLineageCreditProbe(
        boundary_event_id=boundary.event_id,
        source_proposal_ids=source_proposal_ids,
        credited_path_ids=credited_path_ids,
        status=status,
        path_reliability_before=resolution.path_reliability_before,
        path_reliability_after=resolution.path_reliability_after,
        changed_path_ids=changed_path_ids,
        credit_scope=credit_scope,
    )
