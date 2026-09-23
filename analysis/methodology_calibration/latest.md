# SparkBrain Methodology Calibration Audit — R91

- schema_version: 2
- generation_id: `METHCAL-20260923T221827+0900-R91-7E31B4A2`
- produced_at: `2026-09-23T22:18:27+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T212015+0900-R90-C2A74E19`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The material change since R90 is methodological, not scientific. Candidate 35 completed the bounded NON_RESULT preservation/provenance work that Analyst R99 had prospectively allowed under the temporary SYSTEM-priority exception. The authoritative research branch advanced from scientific source head `8ea6581544c642ad74f1a95955ab2c5f795afccc` to implementation head `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c` by adding only a preservation wrapper and tests; a direct compare shows no modification to the underlying candidate35 architecture/scientific source. The final follow-up commit changed import ordering only. Generic CI run `35863266802` passed and produced no workflow artifact.

The new wrapper prospectively binds the R99 Analyst generation/commit, scientific source head/blob, serializer, schema, exclusive-create/no-clobber preservation mode, and explicit STOP fields. Its NON_RESULT preflight checks that candidate response, PRE_FORMAL, and FORMAL authority are false and does not create a raw response. Tests exercise fail-closed behavior before output creation or source-state mutation. This is a well-calibrated completion of the cycle-3 reassessment work: cycle 3 was not treated as a hard terminal cap, but the additional work stayed within the prospectively stated information gain and generated no scientific response.

There is one observability/calibration issue to clarify prospectively. The preservation wrapper imports and reuses the existing scientific `DEVELOPMENT_REVISION` even though it is a new implementation/provenance layer. That is not scientific revision laundering because the scientific source is unchanged and the Git provenance is durable, but it conflates scientific-contract revision with non-scientific implementation/instrumentation revision. Future state should represent those axes separately (for example, scientific development revision plus implementation/instrumentation revision or append-only cycle event) so additional development work is visible without falsely implying scientific retuning.

A second guard remains important: the wrapper contains a future result-bearing function that can be enabled by passing `response_execution_allowed=True`. Current authority remains STOP and no result was produced. Before any future result-bearing use, authorization must be bound to a fresh exact Analyst decision and exact source/protocol/runtime state; a caller-supplied boolean must not by itself be treated as scientific authority.

H7 is unchanged from R90. Analyst R99 remains canonical; H7 remains on nonterminal `FORMAL_INTEGRITY_CAPABILITY` hold after the protected-sidecar readiness failure. No newer H7 controller branch exists, no H7 control/preserve refs exist, no H7 identity was consumed, and no protected evaluation/result/scoring occurred. Stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five `evidence/*` annotated tags remain; `formal/*`, `sealed/*`, and `freeze/*` remain absent.

## Inputs and authority reconstruction

### Prior methodology history

R90 was read first. It classified H7's failed protected-sidecar readiness as a methodology-positive fail-closed boundary test and prospectively allowed Candidate 35 only a bounded NON_RESULT preservation/provenance cycle while executable MECHANISM supply was zero. R91 does not rewrite R90; it records completion of that bounded Candidate 35 work.

### Human directive

`HUMAN-20260922-005` is consumed as a human process directive only, with zero scientific evidentiary weight. Its development-axis and iteration semantics remain the calibration target.

### Designated Control history

Latest designated Control remains `CTRL-20260923T155900+0900-R43-A91C4E6B`, commit `1592c3b52a8a545aa2503fd4618c0a761921ef1e`. It is mailbox/control history, not scientific source of truth.

### Designated Analyst history

Latest canonical gate remains `EVA-20260923T210010+0900-R99-6F2B8C14`, commit `59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`. No newer canonical Analyst generation exists at this audit point. Therefore Candidate 35's implementation completion does not itself advance READY, PRE_FORMAL eligibility, claim ceiling, or lifecycle.

### Independently re-fetched authoritative repository/evidence

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- evidence tags: exactly 5, unchanged
- formal tags: 0
- sealed tags: 0
- freeze tags: 0
- H7 `control/h7*`: none
- H7 `preserve/h7*`: none
- H7 scientific source remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- H7 controller remains `research/main-h7-r5-oneway-controller-r98@f21dc7521af7413adcc46a2561271e0b8852f371`
- Candidate 35 scientific source remains `8ea6581544c642ad74f1a95955ab2c5f795afccc`
- Candidate 35 implementation head is now `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c`
- compare `8ea6581...` → `5bc64fb...`: only `candidate35_preservation.py` and its tests were added; underlying architecture source was not modified
- Candidate 35 CI run `35863266802`: success
- Candidate 35 CI artifacts: none

## Development iteration calibration

### Candidate 35

Phase remains `OPEN_DEVELOPMENT`, claim ceiling remains `SYSTEM`, and it remains not PRE_FORMAL eligible. The cycle-3 reassessment did not terminalize the candidate merely because the count reached three. Instead, Analyst R99 allowed a bounded additional implementation task with distinct prospective information gain: demonstrate preserve-before-read/provenance binding without executing the candidate response.

That work is now complete. The wrapper binds provenance and provides an exclusive-create raw preservation path for a future authorized response, while the current contract and preflight keep response execution, PRE_FORMAL execution, and FORMAL action disabled. Tests verify that unauthorized invocation fails before output creation and before source state mutation. The final implementation repair was import ordering only. This is `SCIENCE_INVARIANT_REPAIR` / non-scientific instrumentation work, not a scientific retune.

The main calibration weakness is representational rather than scientific: the new preservation layer reuses the existing scientific development revision label. Git commits and exact source-head binding preserve provenance, so this is not laundering. Still, scientific revision and implementation/instrumentation revision should be orthogonal fields so additional cycles and repairs remain observable without implying a science-affecting change.

The future result-bearing helper accepts an explicit enable flag. Current STOP authority is intact, but a future workflow must prove fresh exact Analyst authority independently; setting the flag is not itself sufficient authority.

### H7

H7 remains `RESULT_EXPOSED_DEVELOPMENT`, nonterminal on `FORMAL_INTEGRITY_CAPABILITY` hold. No sidecar remediation, new readiness run, fresh FORMAL authority, identity creation/consumption, protected evaluation access, result, or scoring has appeared since R90. The allowed next move remains science-invariant capability repair + exact current Analyst repin + NON_RESULT readiness, then STOP for a later fresh Analyst decision.

### Candidate 34 / historical development cases

No historical rewrite is performed. Candidate 34 remains `RESULT_EXPOSED_DEVELOPMENT`, `TERMINAL_FOR_CURRENT_OBJECT`, zero confirmatory credit. Its execution-source metadata ambiguity still requires append-only clarification only; no rerun or raw mutation.

## Gate-by-gate classifications

| Material gate | Classification | Calibration finding |
|---|---|---|
| Hard integrity floor | KEEP | No FORMAL identity consumption, protected-eval access, evidence mutation, or historical rewrite occurred. |
| Orthogonal development-phase axis | KEEP | Candidate 35 stays OPEN; H7 stays RESULT_EXPOSED; neither is laundered into CONSUMED_ONE_WAY. |
| Fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live case | INSUFFICIENT_EVIDENCE | Fresh one-way FORMAL consumption remains unobserved. |
| Candidate 35 cycle-3 mandatory reassessment | KEEP | Reassessment led to bounded distinct NON_RESULT information gain rather than forced terminalization. |
| Cycle 3 automatic terminal cap | RELAX | Remains explicitly not a hard cap. |
| Candidate 35 additional bounded development work | KEEP | Preservation/provenance wrapper completed without candidate response. |
| Candidate 35 preservation wrapper science classification | KEEP | Scientific architecture source is unchanged; wrapper/tests are science-invariant instrumentation. |
| Candidate 35 scientific vs implementation revision observability | CLARIFY | Reusing one `DEVELOPMENT_REVISION` obscures a useful orthogonal implementation/instrumentation revision axis. |
| Candidate 35 response under temporary SYSTEM exception | TIGHTEN | Response remains STOP until a fresh exact Analyst authority explicitly permits a result-bearing development action. |
| Caller-supplied result-enable flag as authority | TIGHTEN | A runtime boolean must never substitute for exact prospective authority/binding. |
| Candidate 35 SYSTEM claim ceiling | KEEP | No SYSTEM→MECHANISM inflation occurred. |
| Candidate 35 PRE_FORMAL eligibility / READY | KEEP | CI/preservation success does not create scientific readiness or success. |
| Temporary SYSTEM priority exception | KEEP | Still calibrated as bounded NON_RESULT throughput work while H7 is integrity-blocked. |
| H7 NON_RESULT readiness fail-closed | KEEP | Prior sidecar failure remains a valid preidentity integrity stop. |
| H7 identity creation during remediation | TIGHTEN | Still prohibited. |
| H7 green readiness as automatic FORMAL GO | TIGHTEN | Still requires STOP and later fresh Analyst. |
| Same-identity rerun/retune/rescore after START | TIGHTEN | Remains forbidden. |
| RESULT_EXPOSED same-object invariant repair | KEEP | Science-invariant repair remains permitted with provenance. |
| RESULT_EXPOSED science-affecting change | KEEP | Requires explicit versioned development revision or fresh successor preserving prior result. |
| Development observations as independent confirmation | TIGHTEN | No development/CI observation receives confirmatory credit. |
| PRE_FORMAL as real development | KEEP | Real iteration remains allowed before FORMAL without becoming confirmation. |
| Hidden second FORMAL gate | KEEP | No precondition that a candidate must already win its scientific test before READY. |
| Current-object terminal semantics | KEEP | Candidate 34 closure remains current-object only. |
| Immediate rescue successor manufacture | TIGHTEN | Same-family outcome-driven rescue remains disallowed. |
| Fresh independently motivated MECHANISM successor | KEEP | Legitimate in principle with fresh identity/contract/state. |
| Live fresh SYSTEM→MECHANISM successor case | INSUFFICIENT_EVIDENCE | Still no clean live case. |
| Raw-before-score as mere file order | CLARIFY | Formal validity still requires target-blind generation and preserve-before-target-side read, not only serialization order. |
| Global target-blind raw generation | TIGHTEN | Must still be demonstrated in protected result-bearing paths. |
| Preserve-before-target-side read/scoring | TIGHTEN | H7 protected path remains unexercised end-to-end. |
| Exact source/protocol/package/runtime/input/scorer/preserver binding | TIGHTEN | Strong prospectively, but fresh one-way FORMAL consumption remains unobserved. |
| Classification completeness | KEEP | Canonical R99 remains 35/35 classified. |
| Mechanism-first priority | KEEP | H7 remains preferred when executable; Candidate 35 exception remains non-result only. |
| Theory-backward quality floor | KEEP | No weakening observed. |
| Protected/adaptive-evaluation validity | TIGHTEN | No leakage observed, but successful protected handoff remains unobserved. |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Mostly for OPEN and RESULT_EXPOSED. Candidate 35 provides another clean OPEN non-result iteration example; a fresh CONSUMED_ONE_WAY transition remains unobserved.
2. **Is cycle-3 review being mistaken for a hard terminal cap?** No. Candidate 35 completed prospectively bounded preservation/provenance work after cycle-3 reassessment without result generation.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in the observed Candidate 35 update: preservation instrumentation, tests, and import-order repair changed no scientific architecture source. H7's allowed sidecar remediation also remains invariant-only.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** No laundering is observed. However, implementation/instrumentation revision should be represented separately from the scientific `DEVELOPMENT_REVISION` for clearer provenance.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Yes in observed cases; nothing in this generation mutates prior H7/Candidate 34/PF-R1 results.
6. **Is FORMAL one-way integrity unchanged?** Yes. No new identity, START, H7 control/preserve ref, protected evaluation, score, or evidence ref appeared.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** No manufacture observed; Candidate 35 remains SYSTEM. A clean fresh-successor live case remains unobserved, so suppression remains a watch item rather than a finding.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes. Candidate 35 CI/preservation success does not make it PRE_FORMAL eligible or READY and receives no scientific credit.
9. **Are terminal semantics and candidate-supply controls calibrated?** Mostly. Temporary SYSTEM non-result work maintained throughput without claim inflation, but executable MECHANISM supply remains zero while H7 is capability-blocked.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes, conditionally. H7 remains blocked on a concrete integrity capability, not on an impossible evidence criterion; no standard relaxation is needed.

## Risk assessment

### False-positive risk

`LOW_TO_MODERATE_WATCH`. Candidate 35's preservation helper now contains a future result-bearing path guarded by a caller-supplied boolean. No response has run, and current R99 authority is STOP. Before future result-bearing use, authority must be independently bound to a fresh exact Analyst decision and exact source state; a boolean flag alone must not become authorization. H7 retains the separate risk of coupling sidecar remediation/green readiness directly to START.

### False-negative / throughput risk

`LOW_TO_MODERATE_WATCH`. Candidate 35 shows that non-result work can continue without claim inflation while executable MECHANISM supply is zero. That is healthy, but prolonged zero supply remains a throughput risk and should not normalize SYSTEM-only activity or suppress independent MECHANISM discovery.

### Moving-goalpost / rescue risk

`LOW_WATCH`. Candidate 35's scientific source is unchanged across the preservation implementation. H7 R5 remains unchanged. Risk would rise if either object's scientific metric/comparator/threshold/intervention/resource contract/hypothesis/falsifier/success criteria were changed in response to results or operational failures without explicit versioning.

### Over-terminalization risk

`LOW_TO_MODERATE_WATCH`. Cycle 3 was correctly not treated as a hard cap, and Candidate 34 remains terminal only for its current object. Main residual risk is prolonged mechanism-supply scarcity rather than demonstrated successor suppression.

## Claim-type findings

- Candidate 35 remains SYSTEM / OPEN_DEVELOPMENT / nonterminal; preservation completion does not uplift its claim type.
- H7 remains MECHANISM / RESULT_EXPOSED_DEVELOPMENT / nonterminal integrity hold; it is not a scientific FAIL.
- Candidate 34 remains terminal for current object only, development-only, zero confirmatory credit.
- No same-object SYSTEM→MECHANISM post-outcome uplift is observed.
- No manufactured rescue successor is observed.
- A legitimate fresh SYSTEM→MECHANISM successor live case remains insufficiently observed.

## Mechanism-supply health

`TRANSIENT_ZERO_EXECUTABLE_MECHANISM_ON_INTEGRITY_CAPABILITY_HOLD_WITH_COMPLETED_BOUNDED_SYSTEM_NONRESULT_PRESERVATION_WORK`.

This is not yet candidate starvation. Candidate 35's exception produced infrastructure/provenance information only and did not generate a response. It becomes a calibration problem if H7 remains capability-blocked, no independent MECHANISM discovery appears, and SYSTEM exceptions begin expanding into result-bearing work merely to maintain activity.

## Funnel observability

Canonical R99 remains the latest authority, so scientific funnel counts are unchanged:

- canonical candidates: 35
- MECHANISM: 14
- SYSTEM: 21
- active: 0
- queued: 1
- nonterminal hold: 1
- terminal for current object: 33
- OPEN_DEVELOPMENT: 3
- RESULT_EXPOSED_DEVELOPMENT: 32
- CONSUMED_ONE_WAY canonical current objects: 0
- preformal eligible current nonterminal: 1
- preformal ready current nonterminal: 1
- viable executable MECHANISM: 0
- fresh executable FORMAL authority: 0
- official consumed identities: 7
- new identity consumed this generation: 0
- SYSTEM-over-MECHANISM exception: 1, bounded to Candidate 35 NON_RESULT work
- classification completeness: 35/35

Operationally, Candidate 35's bounded preservation implementation is now complete at `5bc64f...`, but this is not a canonical funnel transition until a fresh Analyst generation says so.

## PRE_FORMAL calibration

No hidden second FORMAL gate is observed. Candidate 35 remains not PRE_FORMAL eligible despite successful CI and preservation instrumentation. Its new wrapper creates no scientific result in preflight and tests fail closed under current STOP authority. Repeated development implementation observations remain nonconfirmatory. READY remains an informativeness/well-definition gate, not a retrospective success gate.

## Pass reachability

`REALISTIC_BUT_CAPABILITY_CONDITIONED_WITHOUT_STANDARD_RELAXATION`.

H7 remains blocked on protected-sidecar capability. The route remains: provision only the already-required capability, repin exact current Analyst, run NON_RESULT readiness only, stop, obtain later fresh Analyst authority, then at most one fresh untouched FORMAL identity under unchanged R5 with exact binding and preserve-before-read. Candidate 35's completed preservation wrapper neither helps nor weakens H7's evidence standard.

## Prospective recommendations

1. Keep Candidate 35 response STOP until a fresh Analyst generation explicitly authorizes a result-bearing development action; CI/preservation completion must not auto-advance it.
2. Separate scientific `development_revision` from implementation/instrumentation revision (or an append-only implementation-cycle event) so non-scientific iterative work is durably visible without implying scientific retuning.
3. If Candidate 35 later becomes result-bearing, bind authorization to exact fresh Analyst/source/protocol/runtime state; do not treat `response_execution_allowed=True` as sufficient authority by itself.
4. Preserve the Candidate 35 wrapper's exclusive-create/no-clobber behavior and retain development-only/zero-confirmatory-credit labeling for any future development response.
5. For H7, provision only the already-required protected-sidecar capability, repin to the then-current exact Analyst commit, rerun NON_RESULT readiness only, then stop for a later fresh Analyst decision.
6. Keep FORMAL START irreversible: after START, no same-identity rerun/retune/rescore or science-affecting repair.
7. Continue independent MECHANISM discovery so the H7 capability hold does not normalize zero executable mechanism supply.
8. Keep Candidate 34 provenance correction append-only; no rerun, raw mutation, or retroactive reinterpretation.

## Utility request

No new Utility request. Candidate 35's bounded preservation work is complete, and H7's blocker is already specifically identified. A new methodology-generated Utility proposal would not materially test calibration and could collide with live remediation.

## Hard-floor confirmation

`CONFIRMED_DO_NOT_RELAX`.

No consumed FORMAL identity was rerun/retuned/rescored; no scientific identity was consumed; no protected evaluation or target-side result was read; no evidence ref was mutated; no scientific PR was merged by this auditor; no scheduler was changed; no historical PASS/FAIL was rewritten.

## Confidence

- stable main / evidence-ref nonmutation: `HIGH`
- Candidate 35 scientific-source nonmutation across preservation implementation: `HIGH`
- Candidate 35 no response / no PRE_FORMAL / no FORMAL action in the observed CI path: `HIGH`
- Candidate 35 preservation-wrapper classification as science-invariant instrumentation: `HIGH`
- Candidate 35 implementation-revision observability concern: `MODERATE_TO_HIGH`
- H7 unchanged integrity-hold status: `HIGH`
- full OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live semantics: `MODERATE`, because final fresh FORMAL transition remains unobserved
- global protected/adaptive-evaluation validity: `MODERATE`
- fresh SYSTEM→MECHANISM successor calibration: `LOW_TO_MODERATE`, insufficient live evidence

## Questions for Control / Analyst

1. Will Candidate 35's scientific development revision remain distinct from future implementation/instrumentation revision so additional non-scientific cycles are visible without implying retuning?
2. Before any Candidate 35 result-bearing action, will exact fresh Analyst authority be bound independently of the caller-supplied execution flag?
3. Will successful Candidate 35 preservation/CI remain nonconfirmatory and not auto-promote PRE_FORMAL eligibility or READY?
4. Will H7 protected-sidecar remediation remain operationally separate from FORMAL identity creation/START and require a later fresh Analyst after green readiness?
5. If executable MECHANISM supply stays at zero, will independent discovery continue without inflating SYSTEM claims or manufacturing rescue successors?