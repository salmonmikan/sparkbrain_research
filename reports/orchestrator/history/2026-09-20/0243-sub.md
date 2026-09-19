# SparkBrain Research Orchestrator SUB — 2026-09-20 02:43 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `7dd9d9d4d02febe2547a4cc547b31891a0bc285f`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_PENDING_FRESH_OBJECT`
- SUB lane consumed: `V05_TOPOLOGY_DIMENSION_BINDING_DISCOVERY_CYCLE1`
- fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- selected target: `V05_TOPOLOGY_DIMENSION_BINDING_DISCOVERY_CYCLE1`
- candidate_pool_id: `CAND-V05-TOPOLOGY-CONFIG-BINDING-01`
- exploration cycle: `1/3`, Analyst-bounded to stop after this cycle
- evidentiary status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## MAIN frontier avoided / integrity

Fresh stable `main` is `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN is explicitly holding with no active execution object, and its latest report states that this candidate is SUB-owned. SUB did not continue Temporal batching, Top-k, H7, the rejected stride-11 aliasing candidate, any MAIN blocker/successor, or any consumed/formal/TEST/scoring/preserve/evidence surface. No MAIN branch or production source was modified.

The seven consumed identities in Analyst `do_not_touch` were not accessed or rerun. No STARTED/control authority, freeze/formal/evidence ref, preserve result, official score, or TEST access was created. Open PRs were observed read-only only. Utility request created: none.

## Discovery question / implementation

Created the clearly non-authoritative branch `research/exploratory-sub-v05-topology-config-binding-20260920` from exact stable main. The prospective question was bound before the diagnostic in commit `78918eeee62a5b91e5149d39704d8f59a3ca5d85`; the exploratory pytest was added in `a35fec4407fd376ca7aa7bcc16653fc688be510c`; the complete Analyst handoff/result was recorded in exact research head `ddd80443dd670698397683b95742428045c74932`.

Question: do public/configured `V05BrainConfig.width`, `height`, and `receptor_rows` actually bind the integrated v0.5 topology, or are they accepted/persisted dimension-like fields whose runtime geometry is bypassed by explicit `layered_reservoir_topology(seed=...)` injection?

Fixed bounded check: instantiate development-only configs `(8,8,1)` and `(12,10,2)` with identical topology seed `41`; record declared v0.5 values, nested v0.4 values, actual field unit/receptor/reservoir counts and identities, and connection count. No repository dataset, trained checkpoint, formal raw, confirmatory/held-out TEST input, scorer, or consumed identity was used. No production source was changed.

The exact branch diff from stable main contains only the prospective Discovery note, one exploratory test, and the result/handoff note.

## Observations

`V05BrainConfig` publicly exposes `width`, `height`, and `receptor_rows`, and `configs/v05_reference.json` persists the same fields. `IntegratedV05Brain` copies those values into nested `V04BrainConfig`, but simultaneously supplies `IntegratedV04Brain` an explicit `layered_reservoir_topology(seed=...)` without forwarding those dimensions. `IntegratedV04Brain` therefore uses the supplied topology instead of constructing its config-sized grid.

The alternate `(width=12,height=10,receptor_rows=2)` configuration is accepted and retained in both the v0.5 and nested v0.4 configs, yet under the same topology seed its actual integrated topology is unchanged from `(8,8,1)`: `64` total units = `16` receptors + `48` reservoir units, with identical unit IDs, receptor IDs, and connection count.

Repository search found no current v0.5 test or integrated callsite that binds those three fields into `layered_reservoir_topology`, and no current documentation was found that explicitly declares them intentional metadata-only/no-op compatibility fields. Current reference/evaluation paths use the fixed topology defaults.

This does not constitute a new scientific mechanism and does not revive the rejected stride-11 fanout aliasing candidate. It is an Architecture/API configuration-semantics mismatch: accepted dimension-like configuration can disagree with actual runtime geometry.

Exact-head ordinary CI `35458809766` completed `success` for head `ddd80443dd670698397683b95742428045c74932`; the workflow passed its Python 3.11/3.13 matrix, including lint, local readiness, tests, and bundle validation. CI has no evidentiary role.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, specifically an API-correctness/geometry-contract study rather than scientific functional testing. A fresh prospective object should decide whether `width/height` parameterize reservoir dimensions or total field dimensions (or should be removed/deprecated), whether `receptor_rows` maps to layered receptor geometry or should be rejected, and what checkpoint/backward-compatibility semantics apply.

Reduce to `REJECT/NO_ACTION` if a current supported contract is identified that explicitly defines v0.5 geometry as fixed and these exported dimension fields as intentionally non-operative compatibility metadata. Otherwise a future Architecture object should prospectively test supported non-default configuration/checkpoint round trips against actual topology metadata. It must not use resonant stride-11 behavior as a rescue signal.

Candidate next research layer: `ARCHITECTURE_STUDY` / API correctness, only after fresh Analyst promotion. Scientific/semantic choices still open: geometry meaning of `width/height`, mapping or rejection semantics for `receptor_rows`, checkpoint/backward compatibility, and whether validation should reject unsupported non-default geometry rather than silently accept it.

Utility request: none. Consumed identities: none. New formal results: zero. Blocker: fresh Evidence Analyst classification and prospective Architecture/API contract only. SUB stops here; no cycle 2 is authorized.

Completion target: `ACHIEVED_ONE_ANALYST_AUTHORIZED_BOUNDED_CONFIG_BINDING_DISCOVERY_CYCLE_AND_RETURNED_API_CORRECTNESS_PROMOTION_CANDIDATE`.
