# TH002-FORGE-001 — static addressability kill

- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- theory_id: `TH-002-ANONYMOUS-LINEAGE-ADDRESSABILITY`
- analyst_gate: `EVA-20260924T215808+0900-R126-TH002-THEORY-FORGE-TEST`
- probe_spec: `TH002-FORGE-001-STATIC-ADDRESSABILITY-KILL`
- status: `FORGE_DEAD_END`
- scientific_credit: `0`

## Prospectively fixed construction

Use exactly three anonymous lineages with content-derived physical signatures

- `k0=(1,1,1,-1)`
- `k1=(1,1,-1,1)`
- `k2=(1,-1,1,1)`

and scalar lineage states `v=(0.25,-0.50,0.75)`. The signatures are pairwise orthogonal with squared norm four. No semantic/entity identifier is supplied. Lineage order is not part of the carrier.

The merge carrier is fixed before evaluation as

`M = sum_i(v_i k_i / 4)`.

Delayed evidence supplies a physical/content signature `q=k_j`. Readout is `q dot M`. A requested scalar revision `delta=0.20` is applied as

`M' = M + delta q / 4`.

The checker must verify all six permutations of the three lineage orderings, all three delayed targets, and exact equivalence of decoded values before/after revision to an explicit three-register representation.

## Static observation

The checker passes permutation invariance of the merged carrier and target-selective revision. Because `k_i dot k_j = 4 delta_ij`, decoding gives exactly `v_j`, and the revision changes exactly one decoded scalar by `delta`.

That apparent anonymous selective revision is algebraically identical to ordinary addressable storage. The transform between carrier coordinates and `(v0,v1,v2)` is linear and invertible on the three-lineage subspace, and the delayed physical signature is the lookup key. An explicit finite register/provenance representation or associative key-value memory therefore reproduces every read/revision relation under matched information access. The construction also qualifies directly as separable address-plus-state.

## Disposition

`FORGE_DEAD_END` by the Analyst-owned immediate-kill criterion. No dynamic/performance experiment is authorized or needed. No parameter, architecture, resource, fixture, lineage count or scorer search is performed after observing the reduction. No promotion proposal or Utility request is created.

## Hard-floor / collision check

No PRE_FORMAL/FORMAL identity, STARTED state, official TEST/evidence/formal/sealed/freeze/preserve ref, terminal object, consumed result, protected held-out target, H7 path, Candidate #35 path, MAIN scorer/preserver/runtime/workflow or HUMAN-009 statement is used. MAIN currently has no canonical allocation; this branch is isolated `forge/*` development history and is not merged.
