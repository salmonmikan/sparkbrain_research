# SparkBrain Methodology Calibration Audit — R102

- schema_version: 2
- generation_id: `METHCAL-20260924T091717+0900-R102-8D31C7A4`
- produced_at: `2026-09-24T09:17:17+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260924T081857+0900-R101-4C7A2D91`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE_PROVENANCE_METADATA_EXACTNESS`
- overall_classification: `WELL_CALIBRATED`

## Executive decision

R101 was read first. Current repository/evidence refs were then re-fetched independently, followed by designated Analyst/Control history and current MAIN/Theory/Revisit/Forge handoffs. The scientific programme remains `WELL_CALIBRATED`: the hard FORMAL floor is intact, no terminal current object was reopened, no Revisit trigger appeared, and no development/Forge/Theory observation acquired independent confirmatory credit.

A new, bounded provenance-observability defect appears in MAIN R110. MAIN binds Analyst authority to the correct exact commit `7bc866c6d4dd1d723156345d056fadb027a85c1c`, but persists a non-existent/mismatched Analyst generation label `EVA-20260924T085933+0900-R110-H7-OPBLOCK-EXT-MISALIGNED-NOOP`. The authoritative Analyst `latest.md`, `state.json`, and history entry at that commit identify the generation as `EVA-20260924T085900+0900-R110-CONVERGED-NOOP`. Because the exact Analyst commit is correct, the decision semantics are aligned, no FORMAL identity/START exists, and no result/evidence was produced, this is a science-invariant provenance/logging defect rather than a scientific-integrity breach. It should be corrected prospectively; historical R110 records should not be rewritten.

The authoritative scientific surface otherwise remains unchanged: stable `main` is `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` remains exactly five tags; H7 `control/h7*`, `preserve/h7*`, and `launch/h7-r5-*` namespaces remain empty. H7 science remains `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; controller remains `042d00375278d551dbf643ad866a4c883852804d`. No H7 identity, START, protected result, preserve ref, score, PASS/FAIL, or evidence ref exists.

Analyst R110 is a converged no-op and keeps H7 scientifically `READY/QUEUED`, `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`, with `executor_trigger_capable=false` and `effectively_executable=false`. Control R51 likewise reports no science change. MAIN R110 remains `WAITING_EXTERNAL` before identity/START and performs only read-only freshness/capability reconciliation. Fast Forge R20 remains a no-op with no Theory/Revisit/fresh independent target selected.

TH-001 remains rejected only for the current proposal after the contract-faithful Q0-vs-QI discriminator was reduced by ordinary residual adaptation/threshold plus fixed edge/delay. It remains noncanonical and zero-credit; no positive-search retuning is authorized. Literature R41 remains prospective guardrail input only.

Revisit remains unchanged: 34/34 terminal objects classified; 1 `CLOSED_STRONG`, 19 `DORMANT_REVISITABLE`, 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION`, 0 `REVISIT_TRIGGERED`; no `REVISIT_FORGE_TEST`, no `REVISIT_CANONICALIZE`, no fresh successor, no old-ID reopening, no historical outcome rewrite.

## Input generations and authoritative refs

Prior methodology: R101 (`METHCAL-20260924T081857+0900-R101-4C7A2D91`) at methodology branch head `cbba92a23462ff20fde24db60205ebfdb2bac250`, classified `WELL_CALIBRATED`.

Human directive: `HUMAN-20260922-005` remains process-only, not scientific evidence.

Canonical gate: Analyst R110 (`EVA-20260924T085900+0900-R110-CONVERGED-NOOP`) at `7bc866c6d4dd1d723156345d056fadb027a85c1c`; material change false.

Control: R51 (`CTRL-20260924T091000+0900-R51-6D2A8F41`) at `b938a9f7356267dceadbe14d60ca4481cbe37d38`; control-plane mailbox/history only.

MAIN: `MAIN-20260924T091500+0900-PRIMARY-H7-R110-LAUNCH-CAPABILITY-WAITING-EXTERNAL` at `409416500bbdc080409e74259fde461202cbcdfe`; non-result prestart operational capability observation.

Fast Forge: `FORGE-20260924T083726+0900-NOOP-R109-R101-CONVERGED` at exact persisted commit `6ecce79f76b54b61b873a6e2a385b3f84055099c`; zero-credit and no selected work.

External Literature/Theory/Revisit mailbox: `1b91b18460e552df36cbdc3ef050e38ffd72342a`, unchanged. TH-001 R1 remains current Theory proposal and remains rejected for the current proposal only.

Independent repository reconstruction: stable main `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five annotated `evidence/*` tags; H7 control/preserve/launch namespaces empty. Repository rulesets currently expose one active branch-target ruleset for main and no observed tag-target ruleset; no evidence-ref mutation is observed in this audit.

## Development iteration calibration

Current development-phase semantics remain consistent. H7 stays `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`; MAIN R110 performs no science-affecting change. Candidate #34 and #35 remain terminal for their current objects; neither returns to ACTIVE. Candidate #34 remains MECHANISM-ceiling/CLOSED_STRONG; Candidate #35 remains SYSTEM-ceiling/DEFERRED_INDEPENDENT_REIDENTIFICATION with zero confirmatory credit and same-object rerun/retune/rescore stopped.

Cycle 3 remains mandatory reassessment, not automatic terminalization. No new hard-cap behavior is observed.

Science-invariant versus science-affecting separation remains substantively correct. The newly observed MAIN R110 Analyst-generation label mismatch is itself a `SCIENCE_INVARIANT_REPAIR` class issue: metadata/provenance plumbing is inconsistent while scientific meaning and exact commit binding are unchanged.

Development, Theory, Forge and Revisit observations remain outside independent confirmatory evidence credit.

## PRE_FORMAL / FORMAL calibration

PRE_FORMAL remains genuine development. H7 can be scientifically READY/QUEUED while operationally non-triggerable; READY does not imply prior success or immediate executability. No hidden second FORMAL gate is observed.

FORMAL one-way integrity remains unchanged. No H7 identity, START, protected-evaluation access, raw result, score, preserve ref, PASS/FAIL or evidence ref exists. Exact science/controller refs are unchanged. The required prospective sequence remains: provision only the missing authorized one-shot trigger capability, then obtain a fresh Analyst exact-binding revalidation, then at most one FORMAL start.

The MAIN R110 provenance-label mismatch must not be silently rewritten in historical records. Before any future identity/START, the fresh MAIN/Relay consumer should verify both the exact Analyst commit and the generation identifier parsed from the authoritative Analyst artifact at that commit. A disagreement should fail closed before identity creation and be repaired prospectively as metadata plumbing.

The live fresh one-way FORMAL transition remains unobserved, so its live execution gate remains `INSUFFICIENT_EVIDENCE`. PASS remains scientifically reachable without weakening evidence standards; it is operationally blocked.

## Theory / Forge calibration

Theory/canonical separation remains calibrated. TH-001 and Forge observations remain zero-credit/noncanonical. The current TH-001 proposal remains rejected after its prospective discriminator hit the ordinary-state reduction condition. No same-proposal positive-search retuning is warranted.

Fast Forge R20 consumed current Analyst R109 and Methodology R101 before selection and correctly selected `NO_OP`. No fresh Theory, Revisit or independent target was created. Forge did not touch H7 or terminal Candidate #34/#35 rescue surfaces.

## Revisit / resurrection calibration

The Revisit axis remains orthogonal to terminal state. All 34 terminal current objects remain terminal. Bootstrap remains complete and conservative, with no systematic CLOSED_STRONG default and no aggressive resurrection.

There is still no live independent Revisit trigger. Consequently end-to-end trigger sensitivity, `REVISIT_FORGE_TEST` new-trigger-only behavior and `REVISIT_CANONICALIZE` remain untested rather than failed.

No valuable old line is concretely observed being missed, and no weak old line is being revived by renaming or immediate-successor rescue. Current false-negative and zombie risks remain low, with moderate uncertainty on the first live Revisit path.

## Funnel / claim type / candidate supply / pass reachability

Canonical population remains 35 = 14 MECHANISM / 21 SYSTEM; 34 terminal, H7 sole nonterminal. H7 is scientifically queued but operationally triggerable/effectively executable counts remain zero. Mechanism supply remains fragile, but there is no concrete legitimate successor or candidate-specific Revisit trigger being suppressed, and no candidate is manufactured to fill the queue.

Claim ceilings remain enforced; no same-object post-outcome SYSTEM-to-MECHANISM uplift is observed.

PASS remains scientifically reachable without weakening evidence standards once the authorized trigger primitive exists and a fresh exact-binding revalidation succeeds.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity: `KEEP`
- Terminal current object never reactivated: `KEEP`
- Cycle-3 mandatory reassessment: `KEEP`
- Cycle-3 automatic hard cap: `RELAX`
- Science-invariant vs science-affecting separation: `KEEP`
- Development observations as independent evidence: `KEEP`
- PRE_FORMAL as genuine development: `KEEP`
- Hidden second FORMAL gate: `KEEP`
- Scientific readiness / queue orthogonal to executor capability: `KEEP`
- Effective executability requires verified trigger capability: `KEEP`
- Scientific FORMAL authority exact binding: `KEEP`
- Consumer input generation-id / exact-commit metadata consistency: `TIGHTEN`
- Fresh FORMAL one-way transition: `INSUFFICIENT_EVIDENCE`
- Revisit axis orthogonal to terminal state: `KEEP`
- Revisit bootstrap coverage: `KEEP`
- Revisit bootstrap conservatism: `KEEP`
- Revisit historical specificity / trigger provenance: `CLARIFY`
- Revisit independent-trigger detection end-to-end: `INSUFFICIENT_EVIDENCE`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit fresh-candidate / zero inherited credit: `KEEP`
- REVISIT_FORGE_TEST new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- REVISIT_CANONICALIZE full gate: `INSUFFICIENT_EVIDENCE`
- Theory/canonical separation: `KEEP`
- Theory Forge zero-credit bounded surface: `KEEP`
- Theory rejection after contract-faithful ordinary reduction: `KEEP`
- Forge methodology freshness before selection: `KEEP`
- Fast Forge/canonical separation: `KEEP`
- Claim ceiling enforcement: `KEEP`
- Mechanism-supply health: `CLARIFY`
- PASS reachability without weaker standards: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? **Yes on current canonical objects.**
2. Cycle 3 mistaken for a hard cap? **No.**
3. Science-invariant vs science-affecting changes distinguished? **Yes; the new R110 issue is provenance/logging only and is science-invariant.**
4. Development observations kept out of independent evidence credit? **Yes.**
5. FORMAL one-way integrity unchanged? **Yes.** No H7 identity/START/protected result/evidence exists.
6. Legitimate fresh SYSTEM-to-MECHANISM successors suppressed or manufactured? **No current concrete example.**
7. PRE_FORMAL genuine development? **Yes.** READY remains distinct from success and executor capability.
8. Terminal semantics calibrated? **Yes.** All 34 terminal IDs remain terminal.
9. Revisit catches genuinely changed conditions? **Not demonstrated live; no current candidate-specific independent trigger is missed.**
10. Revisit avoids rescue laundering and zombie inflation? **Yes in current observations.**
11. REVISIT_FORGE_TEST tests new trigger rather than old failure? **Insufficient evidence; no live case exists.**
12. Bootstrap complete and conservative? **Yes**, with candidate-specific closure provenance required before live trigger.
13. PASS realistically reachable without weaker standards? **Yes scientifically; operationally blocked pending authorized trigger capability and fresh revalidation.**

## Risks

False-positive rescue laundering / zombie inflation: `LOW_CURRENT_MODERATE_FUTURE_TRIGGER_WATCH`.

False-negative forgotten valuable lines: `LOW_CURRENT_MODERATE_UNTESTED_REVISIT_PATH`.

Moving-goalpost / rescue: `LOW_CURRENT`.

Over-terminalization: `LOW_CURRENT_NO_CONCRETE_MISSED_TRIGGER_OR_SUCCESSOR`.

FORMAL integrity: `LOW_CURRENT_FAIL_CLOSED_BEFORE_IDENTITY`.

Provenance observability: `LOW_CURRENT_BOUNDED_METADATA_MISMATCH`; exact Analyst commit is correct, generation label is not. Risk becomes material only if a future consumer trusts the label independently of the exact commit/artifact.

Mechanism supply: `FRAGILE_ONE_SCIENTIFICALLY_QUEUED_ZERO_OPERATIONALLY_TRIGGERABLE`.

## Prospective recommendations

1. Keep H7 R5 science/controller/runtime/input/scorer/preserver bindings and one-way rules unchanged.
2. Keep scientific `READY/QUEUED` separate from executor triggerability/effective executability.
3. Prospectively repair MAIN/Relay input-generation metadata plumbing so the persisted Analyst generation ID is read from the exact Analyst artifact at the exact bound commit; do not rewrite MAIN R110 history.
4. Before any future identity/START, require exact Analyst commit + artifact generation-ID consistency as part of fresh provenance revalidation; mismatch must stop before identity creation.
5. Keep the current TH-001 proposal rejected/zero-credit and do not retune it for a positive.
6. Keep all terminal IDs terminal; require independent candidate-specific Revisit triggers, with any Revisit Forge probe testing only the new trigger.
7. Do not weaken claim ceilings or evidence standards to compensate for fragile mechanism supply.

Utility request: none. The observed issue is a straightforward science-invariant provenance-plumbing correction and does not require a new methodology experiment.

## Hard-floor confirmation

No consumed FORMAL identity was rerun, retuned or rescored; no terminal current object was reactivated; no frozen protocol or historical PASS/FAIL was rewritten; no evaluator/held-out leakage is observed; no silent post-FORMAL repair occurred; no H7 identity/START exists; no scientific/evidence ref was mutated by this audit.

Confidence: `HIGH` for the current provenance mismatch, development/terminal/H7 prestart calibration, and current Theory/Forge disposition; `MODERATE` for live Revisit behavior because no actual `REVISIT_FORGE_TEST` or `REVISIT_CANONICALIZE` has occurred.

Questions for Control/Analyst: no blocking scientific question. Prospectively require consumers to persist the exact generation ID read from the exact Analyst commit they bind, and stop before identity/START if the pair does not match. At the first real Revisit trigger, record the candidate-specific historical closure premise changed by the independent trigger before any Forge referral.