# SparkBrain Theory Synthesis — R8 NO_PROPOSAL / Forge seam reconciliation

- schema_version: `2`
- generation_id: `THEORY-20260927T133111+0900-R8-NO-PROPOSAL-FORGE-SEAM-RECONCILIATION-8D3F6A27`
- produced_at: `2026-09-27T13:31:11+09:00`
- producer_run_id: `external-theory-auto-THEORY-20260927T133111+0900-R8-NO-PROPOSAL-FORGE-SEAM-RECONCILIATION-8D3F6A27`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `THEORY-20260927T094100+0900-R7-NO-PROPOSAL-LIFECYCLE-RECONCILIATION-5A7C9E31`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- schedule_slot: `13:30 JST`
- genuinely_new_information: `true`
- theory_status: `NO_PROPOSAL`
- revisit_status: `NO_REVISIT_PROPOSAL`
- new_sparkbrain_scientific_result: `false`

## Primary disposition

No new scientific theory or integration-design proposal is created.

Retain the existing noncanonical integration design
`ID-SB-LATENT-SCOPE-PLURAL-REVISION-001` from Theory R6. The new Forge
artifacts materially reduce implementation uncertainty around that design, but
they do not change its target capability, component classes, state loop,
scientific boundary or alternative established architectures enough to justify
a second primary proposal.

## New inputs reconciled

### Plural-scope revision bridge

Forge generation
`FORGE-20260927T104030+0900-PLURAL-SCOPE-REVISION-BRIDGE-CI-CLEAN`
connects internally generated plural-scope routing to late-evidence revision.

Its bounded tests show:

- ambiguity abstains without allocator or revision mutation;
- a NEW_SCOPE can remain pending and receives no evidence before confirmation;
- an existing scope must be re-confirmed by the allocator before revision;
- router/allocator disagreement rolls back before support-state mutation;
- allocator and revision state replay together after checkpoint restoration;
- no caller-provided scope, regime or episode identity is accepted.

This closes an R6 integration seam. It reduces to ordinary mixture/reject routing
plus transactional validation and rollback. It is not a latent-cause learner,
calibrated posterior, new memory mechanism or scientific result.

### Observed-outcome and top-k coverage boundary

The subsequent Forge chain removes caller-supplied prediction error for exposed
outcomes and adds a coverage-aware guard for an observed outcome omitted by the
top-k prediction pool.

For an omitted value, the guard preserves only:

`P(observed) in [0, tail_mass]`

and therefore:

`prediction_error in [exposed_mass, 1]`.

Routing is inspected at both interval endpoints on checkpoint-isolated state. If
the routing decision depends on the unknown tail allocation, the result is
abstention/no-write. Even endpoint-stable omitted outcomes remain diagnostic
only and do not allocate a scope or revise support.

This is useful integration hygiene, but it reduces to interval/imprecise
probability handling, monotone endpoint robustness and transactional
checkpoint isolation. It is not open-set learning, calibrated uncertainty or a
new predictive principle.

### Current canonical boundary

Evidence Analyst R148 keeps canonical science at 35/35 terminal, with zero
active or scientifically queued objects. RD006 v2 is closed as
`RESULT_EXPOSED_DEVELOPMENT / D0_INCONCLUSIVE_BOUNDED_EXPLOSION` with zero
scientific credit. MAIN is limited to a read-only preserved static
topology/return-edge coverage audit and an optional prospective v3 contract
proposal. No new dynamics, E0/E1/ES, scale/reservoir work or topology mutation
is authorized.

SB001 remains `INTEGRATED_COMPLETE / NON_EVIDENTIARY_BUILD` with scientific
credit zero. The R6 design remains only an optional future, separately bound
SYSTEM_BUILD input.

## Retained R6 component map

| Function | Current direct/Forge component | Established reduction/reference | Status |
|---|---|---|---|
| persistent predictive state | SB001 runtime substrate | PSR / belief-state families | existing non-evidentiary build substrate |
| internal scope inference | internal scope allocator | latent-cause, mixture, HMM/BOCPD allocators | Forge-bounded only |
| plural hypotheses | plural-scope router / top-k pool | mixture/beam/MHT-style hypothesis maintenance | Forge-bounded only |
| mutation gating | plural-scope revision bridge | reject option + transaction/rollback | Forge-bounded only |
| observed evidence binding | observed-outcome adapter | categorical residual `1-P(y)` | Forge-bounded only |
| omitted-outcome handling | coverage-aware outcome guard | interval/imprecise probability | Forge-bounded diagnostic only |
| late selective revision | managed revision overlay | Bayesian/log-linear reweighting; delta/gated-delta/Kalman/HRR-VSA comparators | Forge-bounded only |
| scope retirement | close/tombstone lifecycle | ordinary session/cache lifecycle | optional engineering input |
| replay/inspection | checkpoint and deterministic replay | ordinary state serialization | bounded engineering support |

No component receives scientific credit from this mapping.

## Sharpened future SYSTEM_BUILD acceptance surface

If Evidence Analyst later creates a fresh SYSTEM_BUILD allocation from R6, the
smallest coherent slice should require all of the following prospectively:

1. only observations, prediction outputs and later observed outcomes enter the
   public loop; no caller-supplied true scope/regime/episode identity;
2. no caller-supplied prediction-error scalar where it can be derived from the
   exposed predictive distribution;
3. exact handling for exposed outcomes and interval-bounded handling for
   omitted top-k outcomes;
4. ambiguity, tail-sensitive routing, allocator disagreement and unconfirmed
   NEW_SCOPE all produce complete no-write behavior, including no lazy cache
   creation;
5. update, separate, reuse and close/tombstone paths are inspectable and
   checkpoint/replay deterministic;
6. cue-rich controls succeed while non-identifiable controls abstain;
7. the fixed test stream separates appearance-only change, predictive-dynamics
   change and return of an earlier regime;
8. current-head CI and acceptance tests pass; review remains advisory rather
   than a mandatory SYSTEM_BUILD gate.

The first comparator set should remain small:

- the current SB001 nearest-context/error heuristic;
- one established latent-cause or finite-mixture allocator;
- one HMM/BOCPD-style regime allocator.

Component-replacement tests and connection ablations must remain separate.
Replacing the allocator tests component necessity/substitutability. Cutting the
scope-to-revision gate or bypassing abstention tests interaction contribution.
Neither establishes scientific novelty by itself.

## Why no new proposal

The new artifacts instantiate already-described R6 interfaces and guards.
They do not expose a reduction-resistant phenomenon, a new prediction, a new
falsifier or a new target capability. Creating another proposal would duplicate
R6 and blur the distinction between design maturation and theory generation.

A green Forge prototype establishes only bounded component composition. It does
not establish end-to-end task capability, comparative support, composition
contribution, scientific novelty or SYSTEM_BUILD admission.

## Revisit and integrity disposition

- No Revisit trigger fires.
- RD005 remains consumed and is not reopened.
- RD006 v2 remains closed at its current development ceiling.
- H7 remains historical `INCONCLUSIVE / CONSUMED_ONE_WAY`.
- TH-002 remains killed.
- Candidate #34, Candidate #35, A01 and C19 receive no new trigger.
- No experiment, result-bearing workflow, candidate, build allocation, merge,
  scheduler change, scientific result mutation or immutable-ref movement is
  performed.

## Inputs and refs inspected

- `main@cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- active Human Directive stream including `HUMAN-20260927-002`
- Evidence Analyst
  `EVA-20260927T130000+0900-R148-RD006-V2-RECONCILIATION`
- Literature
  `LIT-20260927T062709+0900-R45-RV02-RD006-REACHABILITY-91C4A8E2`
- Audit
  `AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91`
- prior Theory
  `THEORY-20260927T094100+0900-R7-NO-PROPOSAL-LIFECYCLE-RECONCILIATION-5A7C9E31`
- Forge plural-scope bridge handoff
  `77814d0c2ea97a7c350f443809bc3f23f294c3ce`
- Forge coverage-aware outcome handoff
  `751b4d72185e87ea88521aa93bf780048ccac4ae`

## Run close

Exactly one internal role was performed:
`THEORY_SYNTHESIS_ARCHITECT`.

New noncanonical engineering information was reconciled, but no primary Theory
proposal was warranted. The retained R6 design is more implementation-ready;
its scientific status is unchanged.

New SparkBrain scientific result: no.
