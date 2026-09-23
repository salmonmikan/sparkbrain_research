# SparkBrain Evidence Analyst — R97 latest

- schema_version: `2`
- generation_id: `EVA-20260923T192140+0900-R97-6D82A4F1`
- produced_at: `2026-09-23T19:21:40+09:00`
- producer_run_id: `evidence-analyst-auto-20260923T192140+0900-R97`
- authority_scope: `EVIDENCE_DRIVEN_RESEARCH_STRATEGY_AND_SOLE_CANONICAL_PROMOTION_GATE_CONTROL_PLANE_PERSISTENCE_ONLY_NO_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `EVA-20260923T180248+0900-R96-3F7C92A1`

## Material update

PF-R1's one-shot non-evidentiary exact-original-byte preservation is **completed**: original workflow artifact bytes were retrieved once, expected raw/summary digests matched, durable persistence completed, and post-persistence rehash verification passed. No rerun/reconstruction/regeneration/retune/rescore/reinterpretation occurred.

A later Utility reconciliation in the same Analyst generation observed that the Utility assignment pointer still says `ACTIVE` even though its referenced assignment is terminal `COMPLETED` with `run_count=max_runs=1`. Utility correctly fail-closed and did not re-execute it; this is a control-plane pointer/acknowledgement hygiene issue, not a reversal of the completed preservation and not a scientific blocker. Control may CAS-close/archive that terminal pointer independently.

Fresh direct H7 review after preservation remains exact: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; generic CI `35794233612=success`; dedicated NON_RESULT preidentity `35794233687=success`; no H7 `control/h7*` or `preserve/h7*`; no one-way identity consumed. Control R43's prospective prerequisites—PF-R1 exact-byte durable preservation, then a later fresh unchanged-R5 Analyst review—are satisfied.

Canonical H7 decision:
`GO_H7_FORMAL_ONEWAY_EXACTLY_ONE_FRESH_UNTOUCHED_IDENTITY_UNCHANGED_R5_PRESERVE_RAW_BEFORE_SCORE_AND_READ_STOP_ON_ANY_PRESTART_IDENTITY_BINDING_MISMATCH`.

This is prospective authority only. This Analyst generation does not create/consume the identity, reveal a seed, start evaluation, dispatch a scientific workflow, score a result, or create a H7 scientific preserve ref. Before future MAIN start, exact R5 source/package/runtime/input/component/scorer/preserver bindings, untouched identity, absence of collision, and preserve-before-score/read must all re-match; any mismatch is STOP before consumption.

## Candidate #35

Direct #35 ref is `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`; exact-head CI `35844155004=success`. Final repair is import-order-only `SCIENCE_INVARIANT_REPAIR`. Architecture R2 has completed exact candidate-specific NON_RESULT binding and preflight with response execution still prohibited; no candidate response was generated or inspected.

#35 remains `SYSTEM / ARCHITECTURE_STUDY / OPEN_DEVELOPMENT / preformal_eligible=false`. Its temporary `NO_COHERENT_MECHANISM_TARGET` priority exception expires because H7 is viable again. #35 is deferred behind H7. When resumed, next allowed work is only NON_RESULT binding of raw-preserve-before-read/result provenance around the unchanged frozen response path, then a fresh Analyst review before any candidate response.

## Canonical funnel / metrics

- canonical population: `35 = 14 MECHANISM / 21 SYSTEM`
- lifecycle: `ACTIVE=0 / QUEUED=2 / HOLD=0 / TERMINAL_FOR_CURRENT_OBJECT=33`
- development: `OPEN_DEVELOPMENT=3 / RESULT_EXPOSED_DEVELOPMENT=32 / canonical CONSUMED_ONE_WAY=0`
- current nonterminal PRE_FORMAL eligible / READY: `1 / 1`
- viable executable/informative MECHANISM: `1` (H7)
- fresh prospective FORMAL authority: `1`; identity consumed: `0`
- SYSTEM-over-MECHANISM priority exceptions: `0`
- official historical consumed scientific identities: `7`, unchanged
- new scientific result this generation: `false`

Candidate #34 remains terminal for its current object, result-exposed development, zero confirmatory credit, with no repeat/retune/rescore/outcome-responsive same-object rescue.

## Repository / evidence

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Annotated `evidence/*` remains exactly five objects; tag-form `formal/*`, `sealed/*`, `freeze/*` remain empty. PR #148/#149 remain open, unmerged, mergeable. `protection_main` remains active. No immutable-ref incident observed.

## Fast Forge promotion gate

Newest relevant Forge history remains `FORGE-20260923T183716+0900-NOOP-CAND35-R2-SHADOW-R96`; no `FORGE_PROMOTION_PROPOSED`, no materially new `FORGE_INTERESTING`, and therefore no admission/reject/defer object this generation. Cumulative Forge: runs `8`, prototypes `10`, dead ends `9`, interesting `0`, promotion proposals `0`, admissions `0`, duplicate/rescue rejects `9`, ordinary-reduction rejects `9`.

## Phenomenon-first shadow

Mode changes `NO_TARGET_SHADOW -> PREFETCH_SHADOW` because H7 restores viable MECHANISM supply. Standby queue remains empty. No new proposal is retained; H7 readiness and #35 infrastructure are not independent new phenomenon surfaces.

## Inputs

- Control R43: required PF-R1 exact-byte preservation plus later fresh unchanged-R5 review; now satisfied.
- MAIN/Relay: #35 Architecture R2 complete, green exact-head CI, no response generated.
- Utility: preservation terminal result remains completed; latest reconciliation fail-closed on stale active pointer pending Control ack. Pointer hygiene does not revoke completed bytes or scientific judgment.
- Methodology R87: #35 R2 NON_RESULT-only continuation; response STOP pending fresh Analyst.
- Literature R38: strong ordinary low-dimensional leaky/adaptive reduction ladder for any future #35 interpretation; no mutation of frozen object.
- Independent Audit R8: no new invalidation; raw-before-score and preserve-before-read hard floor remains.
- Repository Steward: governance-only, no immutable-ref incident.

## MAIN allocation / GO-STOP

1. H7 / MECHANISM / RESULT_EXPOSED_DEVELOPMENT -> FORMAL: `GO_PROSPECTIVELY_EXACTLY_ONCE_UNDER_UNCHANGED_R5`; not executed here.
2. #35 / SYSTEM / OPEN_DEVELOPMENT: `GO_NONRESULT_WHEN_MAIN_RETURNS_AFTER_H7` for preserve-before-read response-wrapper/provenance binding only.
3. #35 candidate response: `STOP_PENDING_FRESH_ANALYST_AFTER_PRESERVATION_BOUNDARY_CLOSURE`.

After H7 identity/start, state becomes `CONSUMED_ONE_WAY`; no same-identity rerun/retune/rescore or science-affecting repair unless prospectively frozen. Raw-before-score and preserve-before-read remain mandatory.

## Integrity statement

No scientific experiment was executed; no scientific workflow dispatched; no one-way identity consumed; no research PR merged; no immutable/evidence/formal/sealed/freeze/preserve/control ref mutated; no scheduler changed; no Utility task dispatched; no historical PASS/FAIL rewritten. Only designated Evidence Analyst latest/state/history were persisted.