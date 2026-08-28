from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AttributionMetrics:
    attribution_coverage: float
    active_citation_validity: float | None
    causal_attribution_fidelity: float | None
    cited_count: int
    eligible_count: int
    citation_count: int
    active_citation_count: int
    causal_evaluated_count: int
    causal_valid_count: int


@dataclass(frozen=True)
class RevisionMetrics:
    transition_proposal_precision: float | None
    transition_proposal_recall: float | None
    accepted_revision_precision: float | None
    accepted_revision_recall: float | None


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _plain_bool(value: Any, *, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
    return value


def _ids(record: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = record.get(key, ())
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{key} must be a list or tuple")
    result = tuple(value)
    if any(not isinstance(item, str) or not item for item in result):
        raise ValueError(f"{key} must contain non-empty strings")
    if len(set(result)) != len(result):
        raise ValueError(f"{key} must not contain duplicates")
    return result


def attribution_metrics(
    records: Sequence[Mapping[str, Any]],
    *,
    eligible_count: int | None = None,
) -> AttributionMetrics:
    eligible = len(records) if eligible_count is None else eligible_count
    if isinstance(eligible, bool) or not isinstance(eligible, int) or eligible < len(records):
        raise ValueError("eligible_count must be an integer at least as large as records")
    cited_decisions = 0
    citation_count = 0
    active_citation_count = 0
    causal_evaluated_count = 0
    causal_valid_count = 0
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ValueError(f"records[{index}] must be a mapping")
        citations = _ids(record, "citation_ids")
        active = _ids(record, "active_citation_ids")
        if not set(active).issubset(citations):
            raise ValueError("active_citation_ids must be a subset of citation_ids")
        causal_evaluated = _plain_bool(
            record.get("causal_evaluated", False),
            name="causal_evaluated",
        )
        changed = _plain_bool(
            record.get("decision_changed_after_removal", False),
            name="decision_changed_after_removal",
        )
        if changed and not causal_evaluated:
            raise ValueError("decision_changed_after_removal requires causal_evaluated")
        if causal_evaluated and not citations:
            raise ValueError("causal evaluation requires at least one citation")
        cited_decisions += bool(citations)
        citation_count += len(citations)
        active_citation_count += len(active)
        causal_evaluated_count += causal_evaluated
        causal_valid_count += changed
    return AttributionMetrics(
        attribution_coverage=(cited_decisions / eligible) if eligible else 0.0,
        active_citation_validity=_ratio(active_citation_count, citation_count),
        causal_attribution_fidelity=_ratio(causal_valid_count, causal_evaluated_count),
        cited_count=cited_decisions,
        eligible_count=eligible,
        citation_count=citation_count,
        active_citation_count=active_citation_count,
        causal_evaluated_count=causal_evaluated_count,
        causal_valid_count=causal_valid_count,
    )


def revision_metrics(transitions: Sequence[Mapping[str, Any]]) -> RevisionMetrics:
    normalized: list[tuple[bool, bool, bool]] = []
    for index, transition in enumerate(transitions):
        if not isinstance(transition, Mapping):
            raise ValueError(f"transitions[{index}] must be a mapping")
        expected = _plain_bool(
            transition.get("expected_revision", False),
            name="expected_revision",
        )
        accepted = _plain_bool(transition.get("accepted", False), name="accepted")
        proposal = transition.get("proposal")
        observed = transition.get("transition")
        if proposal is not None and proposal not in {"maintain", "revise"}:
            raise ValueError("proposal must be maintain or revise")
        if observed is not None and observed not in {
            "insufficient_information",
            "maintain",
            "recover",
            "revise",
        }:
            raise ValueError("transition has an unsupported value")
        if proposal is None and observed is None:
            raise ValueError("proposal or transition is required")
        proposed = proposal == "revise" if proposal is not None else observed == "revise"
        if proposal is not None and observed is not None and proposed != (observed == "revise"):
            raise ValueError("proposal and transition disagree")
        if accepted and not proposed:
            raise ValueError("accepted revision requires a revise proposal")
        normalized.append((expected, proposed, accepted))
    expected_positive = [row for row in normalized if row[0]]
    proposed_positive = [row for row in normalized if row[1]]
    accepted_positive = [row for row in normalized if row[2]]
    proposed_tp = sum(row[0] for row in proposed_positive)
    accepted_tp = sum(row[0] for row in accepted_positive)
    return RevisionMetrics(
        transition_proposal_precision=_ratio(proposed_tp, len(proposed_positive)),
        transition_proposal_recall=_ratio(proposed_tp, len(expected_positive)),
        accepted_revision_precision=_ratio(accepted_tp, len(accepted_positive)),
        accepted_revision_recall=_ratio(accepted_tp, len(expected_positive)),
    )


def action_mismatch_rate(expected: Iterable[Any], observed: Iterable[Any]) -> float:
    expected_rows = list(expected)
    observed_rows = list(observed)
    if len(expected_rows) != len(observed_rows):
        raise ValueError("expected and observed must have the same length")
    if not expected_rows:
        return 0.0
    return sum(a != b for a, b in zip(expected_rows, observed_rows, strict=True)) / len(
        expected_rows
    )
