# MAIN canonical science report — candidate #35 Architecture R1

- schema_version: `2`
- generation: `MAIN-20260923T172900+0900-PRIMARY-CAND35-ARCHR1-R95-WAITING-CI`
- execution_mode: `PRIMARY`
- status: `WAITING_EXTERNAL`
- candidate: `CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING`
- layer: `ARCHITECTURE_STUDY`
- development phase: `OPEN_DEVELOPMENT`
- development revision: `ARCHITECTURE-R1-NONRESULT`
- cycle: `1`
- claim ceiling: `SYSTEM`
- preformal eligible/readiness: `false / NOT_READY`
- terminal state: `NONTERMINAL`
- system priority exception: `NO_COHERENT_MECHANISM_TARGET`, prospectively authorized by Evidence Analyst R95
- canonical branch/head: `research/main-cand35-queue-free-subthreshold-architecture-r95-cycle1@58d73aa7c0ad19d0a4e4f84bdbcaaf385e58f751`
- stable base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- CI: `35837060130`, in progress on the exact final head at disposition

## Analyst authority and scope

R95 explicitly allocates candidate #35 to MAIN as SYSTEM / Architecture Study / OPEN_DEVELOPMENT under the pre-recorded `NO_COHERENT_MECHANISM_TARGET` exception. The allowed work is non-result Architecture only: deterministic clone/reset, queue-cap enforcement, serializer, and synthetic validation. Candidate response-bearing execution remains STOP. Same-object SYSTEM-to-MECHANISM uplift is forbidden.

Candidate #34 is terminal-for-current-object after its preserved one-shot PRE_FORMAL development result and was not touched. H7 remains independently FORMAL-held. Fast Forge has no admitted or promoted object and explicitly excludes #35 canonical work. Utility remains PF-R1-specific and is not a dependency.

## Work performed

A fresh canonical research branch was created from the exact stable `main` head. No Forge branch or Forge observation was reused.

Added `src/sparkbrain/v05/subthreshold_architecture.py` with non-result Architecture helpers that:

- inspect serialized pending-arrival queue length without executing it;
- enforce a caller-supplied queue cap and fail closed when exceeded, with the candidate #35 queue-free anchor represented by cap zero;
- deep-clone an already queue-free brain without advancing source time or executing a cue, and verify source/clone state-hash identity;
- create a reset clone that changes only `potential` and `adaptation` for caller-supplied unit IDs while leaving candidate-unit choice, cue bytes, timing and response criteria undefined;
- serialize deterministic local physical state (`potential`, `adaptation`, threshold, refractory and update-time fields) for the ordinary local threshold/decay reduction panel;
- produce a canonical SHA-256 signature that explicitly marks candidate-response, PRE_FORMAL and FORMAL execution as disallowed.

Added `tests/test_v05_subthreshold_architecture.py` using synthetic fixtures only. The tests exercise exact queue-free cloning, queue-cap fail-closed behavior without advancing queued work, reset-diff scope, deterministic/order-independent serialization and explicit result-bearing-layer prohibitions. They do not execute the candidate #35 weak-cue response.

The first implementation-only CI exposed one line-length lint error. This was classified as `SCIENCE_INVARIANT_REPAIR` and repaired solely by wrapping the function signature; no hypothesis, cue, observable, reset meaning, queue semantics, comparator, threshold, falsifier, resource contract or success criterion changed.

## Observations / evidentiary status

No candidate response was generated or inspected. No scientific observation about whether queue-free subthreshold state changes a later weak-cue response was produced. All work in this run is `SYSTEM Architecture / NON_EVIDENTIARY` implementation and synthetic validation only. Confirmatory credit remains zero.

Architecture feasibility information obtained before external CI completion is limited to implementation construction: the main runtime exposes the required state/queue/checkpoint structures without requiring a result-bearing execution. Final implementation readiness remains contingent on exact-head CI success.

## Prior-result and hard-floor preservation

- candidate #34 D34-Q002 rerun/retune/rescore: `false`
- FORMAL identity created/consumed: `false`
- FORMAL STARTED: `false`
- protected/concealed FORMAL evaluation accessed: `false`
- official scoring: `false`
- result-bearing workflow dispatched: `false`
- scientific preserve/evidence/formal/sealed/freeze ref mutation: `false`
- consumed FORMAL identity rerun/retune/rescore: `false`
- prior scientific results rewritten: `false`
- Forge-derived code or observations reused: `false`

Stable `main` was independently re-fetched before mutation. Authoritative `evidence/*` remained the same five annotated tag objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remained empty. PR #148 and #149 remained open. Fast Forge and Utility were re-fetched for collision awareness and do not own #35.

## Stop reason / next canonical action

`WAITING_EXTERNAL` because generic CI `35837060130` is still running on exact head `58d73aa7c0ad19d0a4e4f84bdbcaaf385e58f751`.

On the next MAIN/Relay continuation, re-fetch the Evidence Analyst generation, exact research head and this CI run. If CI is green and R95 remains materially unchanged, close Architecture R1 implementation readiness and return the non-result construction to Evidence Analyst; do not execute a candidate response. If CI fails, repair only clearly science-invariant implementation defects on this object. Any change to scientific cue/reset/cap/observable meaning requires fresh Analyst authority before result-bearing work.
