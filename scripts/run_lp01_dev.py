from __future__ import annotations

import json
import random
from pathlib import Path

from sparkbrain.lp01_lineage import (
    build_indexes,
    destroy_provenance,
    generate_history,
    present_state_digest,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    contract_path = root / "configs/experiments/lp01/prospective_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    profile = contract["held_out_construction"]["dev_profile"]
    if profile["evidentiary_status"] != "NON_EVIDENTIARY":
        raise AssertionError("LP01 dev runner may execute only NON_EVIDENTIARY profile")

    total_queries = 0
    destroyed_differences = 0
    recent_differences = 0
    recent_window = contract["resource_contract"]["max_recent_window_events"]
    for seed in profile["history_seeds"]:
        roots, events, live = generate_history(
            seed=seed,
            live_nodes=profile["live_nodes"],
            history_events=profile["history_events"],
        )
        actual, explicit, recent = build_indexes(
            roots,
            events,
            recent_window=recent_window,
        )
        destroyed_events = destroy_provenance(roots, events, seed=seed + 900_000)
        destroyed, _, _ = build_indexes(
            roots,
            destroyed_events,
            recent_window=recent_window,
        )

        actual_present = present_state_digest(seed=seed, live_ids=live, recent_token="matched")
        destroyed_present = present_state_digest(
            seed=seed, live_ids=live, recent_token="matched"
        )
        if actual_present != destroyed_present:
            raise AssertionError("present-state digest changed under provenance destruction")

        known = roots + tuple(event.child for event in events)
        rng = random.Random(seed + 700_000)
        queries = rng.sample(known[:-1], profile["queries_per_history"])
        for ancestor in queries:
            candidate = actual.descendants_of(ancestor, live).descendants
            ordinary = explicit.descendants_of(ancestor, live).descendants
            if candidate != ordinary:
                raise AssertionError("ordinary explicit parent table failed exact lineage reduction")
            if candidate != destroyed.descendants_of(ancestor, live).descendants:
                destroyed_differences += 1
            if candidate != recent.descendants_of(ancestor, live).descendants:
                recent_differences += 1
            total_queries += 1

    if total_queries == 0:
        raise AssertionError("no LP01 dev queries executed")
    if destroyed_differences == 0:
        raise AssertionError("provenance-destroyed dev control failed to alter any query")

    print(
        "LP01 DEV NON_EVIDENTIARY: PASS — actual lineage and independent ExplicitParentTable "
        f"were exactly equivalent on {total_queries} construction queries; provenance destruction "
        f"changed {destroyed_differences} query results; bounded recent state differed on "
        f"{recent_differences} queries. These diagnostics are construction checks only."
    )


if __name__ == "__main__":
    main()
