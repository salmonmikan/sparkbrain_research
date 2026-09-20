# Prospective comparator-feasibility contract

Candidate: `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01`  
Layer: `ARCHITECTURE_STUDY`  
Claim ceiling: `MECHANISM`  
Evidence status: `NON_EVIDENTIARY`  
Analyst authority: `EVA-20260921T065846+0900-R29-7B2C91E4@de3de2fcf0f21aa33ebfe417d210df1e96889a90`  
Source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Authorized question

Can the Assembly-member causal-selectivity successor be given an outcome-independent, exact **aggregate activity-load + structural topology-load** nonmember comparator contract on the fixed v0.5 development surface, while also fixing sham/random controls and target-selection privilege before any suppression outcome is observed?

This cycle is comparator-feasibility and contract definition only. It MUST NOT call `suppress_units`, `suppress_assembly`, or execute any intervention outcome.

## Fixed development surface

The only admissible surfaces are the source-defined development seeds, in fixed order: `501`, then `502`. Each surface uses:

- `train_brain(seed, count=24)`;
- the first fresh `MOTIF_X` development probe at `index=24`;
- probe start time `trained.current_time_ms + 100.0`;
- `learn_assembly=false`, `learn_field=false`, `explore_action=false`;
- expected baseline prediction `outcome-0`.

No held-out/confirmatory seed is used. No alternate seed, probe, threshold, training count, or retry may be introduced after feasibility is observed.

## Target selection

For each fixed seed:

1. From training rows, rank mature Assembly IDs by descending `motif_x - motif_y` count, then ascending Assembly ID.
2. Require a positive-delta Assembly and a baseline probe whose strongest mature activation is that Assembly with prediction `outcome-0`.
3. Target the **entire selected prototype unit set**, sorted by unit ID. Prototype cardinality must be between 1 and 4 inclusive; otherwise that seed is invalid for this bounded contract.

No target unit is selected or dropped using an intervention result.

## Eligible comparator pool

Eligible comparator units are internal-reservoir units that are not receptor units and are not members of the selected target prototype. Comparator sets have exactly the same cardinality as the target set.

Comparator choice may use only the baseline probe and pre-intervention structural graph. It may not use a suppression/intervention outcome, prediction under suppression, Assembly activation under suppression, or any post-intervention metric.

## Exact aggregate load signature

For a unit set, the exact activity/topology load signature is the following integer tuple:

1. total baseline-probe spike count across the set;
2. number of excitatory units;
3. total incoming edge count;
4. total outgoing edge count;
5. total incoming edges whose source is a receptor;
6. total distinct internal-reservoir units reachable in one or two directed outgoing hops, summed per selected unit;
7. total distinct internal-reservoir units able to reach each selected unit in one or two directed incoming hops, summed per selected unit.

All graph quantities are computed from the already-constructed field graph before any intervention. Edge weights, prediction outcomes, and post-intervention dynamics are not part of comparator selection.

An exact matched-load comparator is feasible iff at least one eligible same-cardinality nonmember set has a signature exactly equal to the target set signature. The primary exact comparator is the lexicographically smallest exact set. This is a set-level load match; per-unit one-to-one activity identity is not required.

## Sham and random controls

These future control definitions are fixed now, but are **not executed in this cycle**:

- sham: identical probe path with no suppressed units;
- generic random lesion: a deterministic same-cardinality draw from the eligible comparator pool using `random.Random(7919 + seed)`, sorted after sampling; if that draw equals the primary exact comparator, advance through the same deterministic shuffle to the first distinct same-cardinality set.

The random lesion is a generic lesion-load control; the primary exact comparator is the activity/topology-load control. Neither may be changed after intervention outcomes are opened.

## Seed selection and feasibility terminal

The future successor surface, if feasible, is the **first seed in fixed order `(501, 502)`** satisfying the exact comparator contract. This selection rule is fixed before this feasibility program runs.

Prospective feasibility terminals:

- `MATCHED_LOAD_COMPARATOR_CONTRACT_FEASIBLE`: at least one fixed development seed has an exact comparator; report the first feasible seed, target set, exact comparator, random set, and pre-intervention signatures, then STOP for fresh Analyst review. Do not run suppression.
- `EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`: both fixed development seeds are valid baseline surfaces but neither has an exact comparator; STOP under the Analyst contingency for fresh canonicalization.
- `SUPPORTED_REACHABILITY_OR_API_CONTRACT_INVALID`: a fixed surface cannot satisfy the baseline/target/API contract in a way that prevents the fixed feasibility decision; STOP for fresh classification.

`COMPARATOR_DEFINITION_REQUIRES_OUTCOME_KNOWLEDGE` is invalid by construction: this program never observes an intervention outcome.

## Readiness boundary

`preformal_eligible=true` means only that this fresh MECHANISM object is in-principle eligible. Current readiness remains `NOT_READY`. A feasible comparator does not constitute scientific success, does not imply likely PASS, and does not authorize PRE_FORMAL. Fresh Evidence Analyst review is required before any outcome-bearing continuation.
