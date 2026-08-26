"""Label-blind C17 group discovery and deterministic train-only controls."""

from __future__ import annotations

import itertools
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from .contracts import canonical, digest, require_finite_number, text_hash

OBSERVATION_KEYS = {
    "opaque_candidate_id",
    "activation",
    "message_source_id",
    "message_target_id",
    "message_weight",
    "opaque_episode_id",
    "time",
}


def validate_observation(row: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(row, dict) or set(row) != OBSERVATION_KEYS:
        raise ValueError("discovery observation must have the exact label-blind schema")
    for key in ("opaque_candidate_id", "opaque_episode_id"):
        if not isinstance(row[key], str) or not row[key]:
            raise ValueError(f"{key} must be a nonblank opaque string")
    for key in ("message_source_id", "message_target_id"):
        if row[key] is not None and (not isinstance(row[key], str) or not row[key]):
            raise ValueError(f"{key} must be null or a nonblank opaque string")
    activation = require_finite_number(row["activation"], "activation")
    weight = require_finite_number(row["message_weight"], "message_weight")
    if not 0.0 <= activation <= 1.0 or weight < 0.0:
        raise ValueError("activation/weight outside registered bounds")
    if isinstance(row["time"], bool) or not isinstance(row["time"], int) or row["time"] < 0:
        raise ValueError("time must be a nonnegative integer")
    return dict(row)


def _candidate_id(
    protocol_id: str, run_seed: int, condition_id: str, members: Iterable[str]
) -> str:
    ordered = sorted(members)
    return "oc-" + text_hash(f"{protocol_id}|{run_seed}|{condition_id}|" + canonical(ordered))[:24]


def discover_primary_candidate(
    observations: list[dict[str, Any]],
    *,
    protocol: dict[str, Any],
    run_seed: int,
    condition_id: str,
) -> dict[str, Any]:
    rows = [validate_observation(row) for row in observations]
    candidate_ids = sorted({row["opaque_candidate_id"] for row in rows})
    active_episodes: dict[str, set[str]] = defaultdict(set)
    active_steps: dict[str, int] = defaultdict(int)
    activation_mass: dict[str, float] = defaultdict(float)
    edge_weight: dict[tuple[str, str], float] = defaultdict(float)
    for row in rows:
        cid = row["opaque_candidate_id"]
        if row["activation"] > 0.0:
            active_episodes[cid].add(row["opaque_episode_id"])
            active_steps[cid] += 1
            activation_mass[cid] += row["activation"]
        source, target = row["message_source_id"], row["message_target_id"]
        if source is not None and target is not None:
            edge_weight[(source, target)] += row["message_weight"]
    minimum_member = protocol["discovery"]["eligibility"][
        "minimum_active_distinct_train_episodes_per_member"
    ]
    minimum_group = protocol["discovery"]["eligibility"]["minimum_group_train_episode_coverage"]
    eligible: list[dict[str, Any]] = []
    for size in protocol["discovery"]["candidate_subset_sizes"]:
        for members_tuple in itertools.combinations(candidate_ids, size):
            members = set(members_tuple)
            if any(len(active_episodes[member]) < minimum_member for member in members):
                continue
            group_episodes = set().union(*(active_episodes[member] for member in members))
            if len(group_episodes) < minimum_group:
                continue
            within = sum(
                value
                for (source, target), value in edge_weight.items()
                if source in members and target in members
            )
            boundary = sum(
                value
                for (source, target), value in edge_weight.items()
                if (source in members) != (target in members)
            )
            denominator = within + boundary
            cohesion = None if denominator == 0 else within / denominator
            eligible.append(
                {
                    "candidate_id": _candidate_id(
                        protocol["protocol_id"], run_seed, condition_id, members
                    ),
                    "member_ids": sorted(members),
                    "member_count": len(members),
                    "within_weight": within,
                    "boundary_weight": boundary,
                    "cohesion": cohesion,
                    "train_episode_coverage": len(group_episodes),
                    "member_active_episode_counts": {
                        member: len(active_episodes[member]) for member in sorted(members)
                    },
                }
            )
    eligible.sort(
        key=lambda row: (
            -(row["cohesion"] if row["cohesion"] is not None else -1.0),
            -row["within_weight"],
            row["member_count"],
            text_hash(canonical(row["member_ids"])),
        )
    )
    primary = eligible[0] if eligible else None
    return {
        "run_seed": run_seed,
        "condition_id": condition_id,
        "primary_candidate": primary,
        "eligible_candidates": eligible,
        "candidate_count": len(candidate_ids),
        "observation_count": len(rows),
        "discovery_input_sha256": digest(rows),
    }


def select_controls(
    observations: list[dict[str, Any]],
    target_members: list[str],
    *,
    protocol: dict[str, Any],
    run_seed: int,
    condition_id: str,
) -> dict[str, list[str] | None]:
    rows = [validate_observation(row) for row in observations]
    all_ids = sorted({row["opaque_candidate_id"] for row in rows})
    target = set(target_members)
    pool = [candidate for candidate in all_ids if candidate not in target]
    if not target or not pool:
        return {name: None for name in protocol["controls"]["control_order"]}
    active_steps: dict[str, int] = defaultdict(int)
    mass: dict[str, float] = defaultdict(float)
    degree: dict[str, float] = defaultdict(float)
    for row in rows:
        cid = row["opaque_candidate_id"]
        if row["activation"] > 0:
            active_steps[cid] += 1
            mass[cid] += row["activation"]
        source, endpoint = row["message_source_id"], row["message_target_id"]
        if source is not None and endpoint is not None:
            degree[source] += row["message_weight"]
            degree[endpoint] += row["message_weight"]
    size = len(target)
    exact = list(itertools.combinations(pool, size))

    def choose(metric: dict[str, float], target_value: float) -> list[str] | None:
        if not exact:
            return None
        return list(
            min(
                exact,
                key=lambda subset: (
                    abs(sum(metric[item] for item in subset) - target_value),
                    text_hash(digest(sorted(subset))),
                ),
            )
        )

    random_size = 1 + int(text_hash(f"c17|control|{run_seed}|{condition_id}")[:8], 16) % 4
    random_options = list(itertools.combinations(pool, min(random_size, len(pool))))
    random_subset = list(min(random_options, key=lambda subset: text_hash(digest(sorted(subset)))))
    return {
        "random_unmatched": random_subset,
        "size_matched": choose(defaultdict(float), 0.0),
        "degree_matched": choose(degree, sum(degree[item] for item in target)),
        "load_matched": choose(mass, sum(mass[item] for item in target)),
        "activity_matched": choose(active_steps, sum(active_steps[item] for item in target)),
    }


def assess_proposal(proposal: dict[str, Any] | None, outcome: str) -> dict[str, Any]:
    if outcome not in {"allow", "veto", "abstain"}:
        raise ValueError("unregistered C15 assessment outcome")
    if proposal is None:
        return {"proposal": None, "proposal_sha256": None, "assessment": "not_called"}
    before = digest(proposal)
    retained = dict(proposal) if outcome == "allow" else None
    if digest(proposal) != before:
        raise ValueError("assessment mutated the C14 proposal")
    return {"proposal": retained, "proposal_sha256": before, "assessment": outcome}


def execute_c14_c15_boundary(
    *, proposal_belief: str, outcome: str, alternate_proposal: object | None = None
) -> dict[str, Any]:
    """Run the accepted C14 proposal through C15 v4's assessment-only veto.

    C17 cannot pass an alternate proposal into this boundary. C15 receives one
    already-created C14 ``IgnitionDecision`` and can return either those exact
    proposal bytes or a no-Ignition veto; it has no proposal factory/replacement
    input or output.
    """
    if alternate_proposal is not None:
        raise ValueError("alternate proposals are unrepresentable at the C15 boundary")
    if outcome not in {"allow", "veto", "abstain"}:
        raise ValueError("unregistered C15 assessment outcome")
    from types import MappingProxyType

    from sparkbrain.v03_seed.coalition import decide_c14
    from sparkbrain.v03_seed.contracts import CoalitionState
    from sparkbrain.v03_seed.revision import (
        RevisionBeliefSnapshot,
        RevisionController,
        RevisionHeadOutput,
    )

    coalition = CoalitionState(
        belief_key=proposal_belief,
        object_key="c17-opaque-entity",
        score=0.8,
        activation=1.0,
        effective_support=2.0,
        effective_contradiction=0.0,
        redundancy=0.0,
        source_count=2,
        independent_group_count=2,
        evidence_count=2,
        stability=2,
        support_ids=("c17-opaque-support-a", "c17-opaque-support-b"),
        contradiction_ids=(),
        normalized_recency=1.0,
    )
    proposal = decide_c14((coalition,))
    if not proposal.ignited:
        raise ValueError("registered C14 proposal construction failed")
    proposal_body = {
        "belief_key": proposal.belief_key,
        "object_key": proposal.object_key,
        "score": proposal.score,
        "margin": proposal.margin,
        "reason": proposal.reason,
        "coalitions": [
            {name: getattr(row, name) for name in row.__dataclass_fields__}
            for row in proposal.coalitions
        ],
    }
    before = digest(proposal_body)
    heads = RevisionHeadOutput(
        belief_probabilities=MappingProxyType({"alpha": 0.05, "beta": 0.9, "gamma": 0.05}),
        maintain_probability=1.0,
        update_probability=1.0 if outcome == "allow" else 0.0,
        recovery_probability=1.0 if outcome == "allow" else 0.0,
        abstention_probability=1.0 if outcome == "abstain" else 0.0,
    )
    state = RevisionBeliefSnapshot(
        activations=MappingProxyType({"alpha": 1.0, "beta": 0.0, "gamma": 0.0}),
        citations=(),
        entity_key="c17-opaque-entity",
        history=("alpha",),
        state_hash="0" * 64,
        winner="alpha",
    )
    assessed = RevisionController()._apply_veto(proposal, heads, state)
    if digest(proposal_body) != before:
        raise ValueError("C15 assessment mutated the C14 proposal")
    if assessed.ignited and assessed != proposal:
        raise ValueError("C15 replaced the C14 proposal")
    return {
        "c14_proposal_sha256": before,
        "c14_ignited": proposal.ignited,
        "assessment": outcome,
        "assessment_allowed": assessed == proposal,
        "assessment_reason": assessed.reason,
        "output_proposal_sha256": before if assessed == proposal else None,
        "replacement_possible": False,
    }
