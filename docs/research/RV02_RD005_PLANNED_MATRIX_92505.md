# RV02 RD005 fresh construction-matrix plan

Date: 2026-09-12  
Status: **OUTCOME-BLIND CONSTRUCTION PLAN / D1 NOT YET EXECUTED / NO CAPABILITY**

## Fixed identity

```text
protocol: rv02-rd005-gate-reachable-hidden-eligibility-v1
construction plan: rv02-rd005-planned-matrix-92505-v1
fresh ScaleStudyConfig seed: 92505
scales: 1, 3, 10
family templates: inherited six RV02 development families
planned cells before construction: 6 families × 3 scales = 18
return lag from discovery clock: +1.0 ms
formal execution allowed: false
held-out capability allowed: false
```

Seed `92505` is fixed prospectively here, before any RD005 D1 construction result or capability result is opened. It is distinct from the consumed RD003/RD004 development identity (`92001`). The existing family templates and exposure counts are inherited, but the route permutation, world IDs, topology fill and evidence hashes must be regenerated from this fresh seed.

No alternative seed may replace `92505` under this plan identity after D1 is observed. If the construction gate fails, the failure is retained and any redesign requires a new plan/protocol identity.

## Purpose

RD004 retained hidden eligibility but produced no admissible hidden-return commit opportunities. RD005 must demonstrate prospectively that its E1 hidden source can physically reach at least one return gate before any route/capability output is measured.

The merged construction kernel already fixes the admissible gate predicates:

- same immutable eligibility-event and external-return-event budget for E1 and ES;
- ES differs only by a non-identity bijection over the observed hidden-source inventory;
- lag in the inherited inclusive `[0.5, 6.5] ms` window;
- physical edge exists from assigned source to return target;
- edge is plastic;
- initial weight is non-negative;
- return generation is outcome-blind.

This document fixes how the fresh matrix will produce that budget without looking at task outcome.

## Construction-only discovery pass

For each of the 18 planned cells, run only the ordinary pre-capability Field dynamics needed to expose a prospective hidden eligibility batch. Do **not** instantiate an RD005 hidden learner, apply a hidden-return update, run a probe, compute route correctness, or score capability.

The cell is constructed from the fresh `ScaleStudyConfig(seed=92505)`, the inherited topology builder, boundary gain, and inherited external training schedule shape. External event IDs must use the new RD005 plan namespace rather than reusing a consumed RD003/RD004 event identity.

At each ordinary external schedule clock `T`, before injecting the ordinary event at `T`:

1. advance the ordinary Field only to `T`;
2. inspect the hidden spikes emitted since the previous ordinary external clock;
3. for each hidden source, retain only spikes for which a proposed return at `T + 1.0 ms` gives an inherited-valid lag in `[0.5, 6.5] ms`;
4. require that the hidden source has at least one physical outgoing edge to a visible RV02 port whose edge is plastic and whose construction-start weight is non-negative;
5. for a source with more than one eligible spike in this interval, select the latest spike deterministically, breaking an exact tie by the retained spike/event identity;
6. select the smallest numeric eligible visible target for that source.

The algorithm must stop at the **first** external clock `T` for which at least two distinct hidden sources satisfy all conditions. It may not skip an earlier qualifying clock in search of a more favorable source set.

The discovery pass stops for that cell immediately after this first qualifying batch is frozen. Later hidden activity is not inspected for gate selection.

## Shared E1 / ES event budget

At the first qualifying clock for a cell, create exactly one prospective eligibility event and one prospective return event for each selected hidden source.

For every selected source:

```text
eligibility time = retained hidden-spike time
return time      = T + 1.0 ms
return target    = smallest eligible visible-port target fixed above
outcome_blind    = true
```

All selected returns occur before the next ordinary 5 ms-spaced event within a route segment. The future execution layer must schedule the fixed return events before advancing past their timestamp; scheduling a return into the past is an integrity failure.

E1 uses the identity source assignment. ES uses a deterministic one-position rotation of the sorted selected hidden-source IDs:

```text
s[0] -> s[1]
s[1] -> s[2]
...
s[n-1] -> s[0]
```

Because a qualifying batch requires at least two distinct sources, this is a non-identity bijection by construction. No outcome, future update, route score, or later probe behavior may influence the permutation.

## Cell construction status

Each original 18-cell identity receives exactly one immutable construction status:

- `D1_READY`: the first qualifying batch exists and the merged `RD005GateConstruction.assert_development_matrix_reachable()` passes for E1;
- `D1_UNREACHABLE`: no qualifying batch exists under the complete fixed ordinary training schedule;
- `CONSTRUCTION_INTEGRITY_FAILURE`: an invariant, timestamp, topology, edge-snapshot, event-identity, or certificate check fails.

A `D1_UNREACHABLE` cell is a retained negative construction result. It is not retried with another clock, target rule, lag, seed, gain, route mapping, or topology under this plan identity.

A `CONSTRUCTION_INTEGRITY_FAILURE` blocks the entire matrix until repaired prospectively under a reviewed source revision; the failed artifact remains preserved.

## Capability-cell selection rule fixed before D1

If and only if there is no construction-integrity failure and at least one `D1_READY` cell, the future RD005 exposed-development capability matrix is **exactly the complete ordered set of all `D1_READY` cells**. Selection is therefore based only on preregistered physical gate availability, before capability output exists.

`D1_UNREACHABLE` cells remain in the construction artifact and are not silently dropped or replaced. If zero cells are `D1_READY`, RD005 stops under this plan identity and no capability runner may be opened.

## Required retained construction artifact

Before any future capability runner exists, retain one canonical artifact containing:

- plan/protocol IDs and source SHA;
- fresh seed and full 18-cell ordered identity list;
- regenerated world/evidence/topology hashes;
- exact ordinary external schedule hash for every cell;
- construction-start connection rows/hash;
- all hidden spikes inspected at each clock up to and including the first qualifying clock, or through schedule exhaustion for an unreachable cell;
- selected eligibility events and return events;
- deterministic ES permutation;
- E1 and ES gate certificates;
- per-cell `D1_READY` / `D1_UNREACHABLE` / integrity-failure status;
- complete ordered list of future capability cells derived by the fixed rule above;
- whole-artifact SHA-256.

The artifact must contain no route correctness, task reward, capability score, pass/fail endpoint, or held-out evidence.

## No-change boundary after D1 artifact

Once the construction artifact is retained and reviewed, its seed, worlds, selected clocks, eligibility events, return events, target identities, ES mapping, certificate rules, and capability-cell list are immutable for this RD005 development identity.

A later runner may consume the artifact; it may not rediscover gates online or substitute a newly favorable gate.

## Human-review governance

A literal independent-human identity is not manufactured by automation. If the construction package later reaches a gate blocked **only** by a human-review identity requirement, the standing user instruction permits an explicit `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER` governance record after substantive technical/semantic review. That waiver does not authorize any one-way formal/held-out execution.

## Next safe implementation step

Implement the construction-only discovery/artifact builder and tests on a separate research branch. Unit tests must cover at least:

- first-qualifying-clock selection;
- latest-eligible-spike selection per source;
- smallest eligible visible-target selection;
- inclusive lag boundaries;
- two-source minimum and non-identity ES rotation;
- no task/capability fields in the artifact;
- retained unreachable cells;
- whole-matrix stop on integrity failure;
- deterministic capability-cell derivation;
- fail-closed D1 when zero cells are ready.

No probe runner, route scorer, formal/held-out path, or execution authority should be added in that implementation PR.