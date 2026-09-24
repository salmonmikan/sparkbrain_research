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

The merge carrier is fixed before evaluation as `M = sum_i(v_i k_i / 4)`. Delayed evidence supplies a physical/content signature `q=k_j`. Readout is `q dot M`. A requested scalar revision `delta=0.20` is applied as `M' = M + delta q / 4`.

The ordinary comparator receives exactly the same physical/content query and stores the same `(key,value)` bindings in an associative key-value table. The checker must verify all six lineage orderings, all three delayed queries, and exact equality of every decoded value before and after revision. No comparator receives an evaluator-only target index.

## Static observation

The checker passes permutation invariance of the merged carrier, target-selective revision, and matched-access key-value equivalence. Because `k_i dot k_j = 4 delta_ij`, decoding gives exactly `v_j`, and the revision changes exactly one decoded scalar by `delta`.

That apparent anonymous selective revision is algebraically ordinary addressable storage. The delayed physical signature is the lookup key; an associative key-value memory given the same content cue reproduces every read/revision relation. On the three-lineage subspace the carrier is also a linear encoding of three finite scalar registers, so it additionally qualifies as a separable address-plus-state representation. No reduction-resistant residue remains.

## Disposition

`FORGE_DEAD_END` by the Analyst-owned immediate-kill criterion. No dynamic/performance experiment is authorized or needed. No parameter, architecture, resource, fixture, lineage count or scorer search is performed after observing the reduction. No promotion proposal or Utility request is created.

## Hard-floor / collision check

No PRE_FORMAL/FORMAL identity, STARTED state, official TEST/evidence/formal/sealed/freeze/preserve ref, terminal object, consumed result, protected held-out target, H7 path, Candidate #35 path, MAIN scorer/preserver/runtime/workflow or HUMAN-009 statement is used. MAIN currently has no canonical allocation; this branch is isolated `forge/*` development history and is not merged.
