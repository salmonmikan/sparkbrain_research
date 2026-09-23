# SparkBrain Methodology Calibration Audit — R93

- schema_version: 2
- generation_id: `METHCAL-20260924T002000+0900-R93-B71C4A9E`
- produced_at: `2026-09-24T00:20:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T232021+0900-R92-5C91E7A4`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The material update is a strong live validation of the development-iteration model for Candidate 35, paired with one material semantic regression in H7.

Candidate 35 completed exactly the one prospectively authorized fixed-order SYSTEM/ARCHITECTURE development batch under R100. Direct repository inspection verifies exact R100 authority freshness checks, exact frozen implementation/scientific-source binding, one-time raw-ref exclusion, fixed five-arm execution, exclusive-create raw serialization before response return, and a raw branch containing the preflight, all five arm records, and the batch-complete marker. The completion record carries zero confirmatory credit, no PRE_FORMAL or FORMAL action, and explicit authority exhaustion. MAIN then stopped and waited for a fresh Analyst. R101 subsequently moved the same object to `RESULT_EXPOSED_DEVELOPMENT`, `TERMINAL_FOR_CURRENT_OBJECT`, exhausted the one-shot authority, and prohibited same-object rerun/retune/rescore or SYSTEM->MECHANISM uplift. This is a clean live OPEN_DEVELOPMENT -> result exposure -> RESULT_EXPOSED_DEVELOPMENT transition and demonstrates that cycle 3 is a reassessment point rather than an automatic terminal cap.

The hard FORMAL floor remains unchanged. Stable main is unchanged, the authoritative evidence tag set remains five, `formal/*`, `sealed/*`, `freeze/*`, and `immutable/*` remain empty, and no fresh H7 identity/START/protected evaluation/score/evidence mutation is observed.

However, R101 canonically labels H7 `OPEN_DEVELOPMENT`, whereas R100 and R92 both had the same H7 object at `RESULT_EXPOSED_DEVELOPMENT` after the previously exposed/preserved development observation. No fresh H7 candidate ID, versioned science-affecting development revision, or fresh successor contract accompanies this regression. The allowed actions remain safely restricted to science-invariant capability/authority plumbing plus NON_RESULT readiness, so there is no immediate scientific-integrity breach; nevertheless the phase label is materially too permissive because OPEN_DEVELOPMENT semantics permit operations that a same-object RESULT_EXPOSED object must not regain. Development phase must be monotone for a given object once meaningful result exposure occurs, unless a genuinely fresh versioned object/revision is explicitly instantiated while preserving the prior result.

Mechanism supply also remains weak: 34/35 current objects are terminal, H7 is the sole nonterminal object on capability HOLD, there is no executable MECHANISM and no queued canonical candidate. R101 correctly does not manufacture a Candidate 35 successor from the observed result, but its `NO_TARGET_SHADOW` should not normalize current-object terminalization into topic death. The pre-outcome, independently recorded reachable-state/on-manifold residual should receive an explicit prospective disposition: either it meets the theory-backward quality floor and becomes a fresh candidate with a new ID/contract, or it is recorded as `NO_COHERENT_MECHANISM_TARGET` with a reason. No successor should inherit confirmatory credit from Candidate 35.

## Inputs and authority reconstruction

### Prior methodology history

R92 was read first from the designated methodology history. R92 classified the R100 Candidate 35 one-batch authorization as calibrated only at the SYSTEM development claim ceiling, required raw-before-read and first-result authority exhaustion, kept H7 at `RESULT_EXPOSED_DEVELOPMENT` on FORMAL integrity/capability HOLD, and retained the distinction between persisted READY and effective executable readiness. R93 does not rescore or rewrite R92; it evaluates the new live execution and R101 state prospectively.

### Human directive

`HUMAN-20260922-005` is consumed strictly as a human process directive with zero scientific evidentiary weight. Its orthogonal development-phase axis, cycle-3 reassessment rule, repair taxonomy, and prospective-only successor semantics remain the calibration target.

### Designated Control and Analyst history

Latest designated Control remains R44 at commit `3c46617fba123704297d880a748c305c16a7dd01`. It predates the Candidate 35 result and is treated only as control history/mailbox context.

Latest canonical Analyst is R101 (`EVA-20260924T000324+0900-R101-CAND35-POSTEXPOSURE`) on `ops/evidence-analyst-handoff`, with current branch head `e50e0a91e25f2457d0b7152900a48cbdc5006485`. R101's current state blob is `5a609f807921846e0110f6e7865d04fc511ecff1`. A transient incorrect main SHA in the first R101 persistence was corrected contemporaneously on the Analyst branch; the corrected current report matches independently fetched main and has no scientific effect.

### Independently re-fetched authoritative repository/evidence

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative `evidence/*` annotated tags: exactly 5, unchanged
- `formal/*`: 0
- `sealed/*`: 0
- `freeze/*`: 0
- `immutable/*`: 0
- Candidate 35 live branch: `62db3b437ffc26b931bbe5b9e78ca814bddbeb81`
- Candidate 35 frozen scientific source: `8ea6581544c642ad74f1a95955ab2c5f795afccc`
- Candidate 35 bound implementation: `b5f312683d50ed3a086348b62770fc8923c78046`
- Candidate 35 result workflow run: `35877765051`, success
- Candidate 35 exclusive raw preservation ref: `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`
- Candidate 35 batch completion: `complete_batch=true`, `confirmatory_credit=0`, PRE_FORMAL/FORMAL/scoring false, authority exhausted
- H7 controller: `f21dc7521af7413adcc46a2561271e0b8852f371`, unchanged
- H7 latest readiness remains a pre-identity failure at the protected-sidecar capability gate; no fresh H7 FORMAL identity, START, protected evaluation, score, or evidence ref was observed

## Development iteration calibration

### Candidate 35 — live OPEN -> RESULT_EXPOSED transition

Candidate 35 is the strongest current positive example of the intended development semantics. R100 prospectively fixed the five-arm order and scientific source before any response. The launch workflow verified exact Analyst authority, exact implementation/source bytes, runtime/package bindings, current ownership, and absence of the raw ref. It then executed exactly one batch, wrote each raw arm record with exclusive-create semantics before returning the response object, created a one-time raw branch, and exhausted authority after the complete batch.

The post-exposure relay did not reinterpret its own authority as permission to continue. It stopped and required a fresh Analyst. R101 then canonically changed the object to `RESULT_EXPOSED_DEVELOPMENT`, terminalized only the current synthetic-null contract, assigned zero confirmatory credit, and prohibited same-object rerun/retune/rescore. No hidden second FORMAL gate was imposed: Candidate 35 was allowed to learn from a real development response without first proving the hypothesis, while remaining below PRE_FORMAL and FORMAL.

The batch therefore supports KEEP for bounded development iteration and for cycle-3 reassessment. It also supports TIGHTEN against any attempt to treat repeated development observations as independent confirmation.

One observability issue remains. The result-bearing raw records and R101 state still carry a development revision label ending in `NONRESULT`. This does not launder the result—the evidentiary status, batch marker, raw hashes, and post-exposure state are explicit—but it conflates scientific revision, implementation/preservation revision, and observation-batch identity. Prospectively these should be orthogonal durable fields. Existing raw records must not be renamed or rewritten.

### H7 — material phase monotonicity regression

H7 is the principal negative calibration finding in R93. R100 directly recorded the current H7 object as `RESULT_EXPOSED_DEVELOPMENT`; R92 methodology preserved that interpretation. R101 now records the same H7 object as `OPEN_DEVELOPMENT` while preserving the same MECHANISM claim ceiling, PRE_FORMAL readiness, integrity HOLD, controller/science refs, and no fresh candidate ID or science-affecting development revision.

That reversion is inconsistent with the development-phase contract. Once meaningful development results have been exposed on an object, the same object must not regain OPEN_DEVELOPMENT permissions. It may receive SCIENCE_INVARIANT_REPAIR, or a science-affecting change may proceed only under an explicit versioned development revision/fresh successor that preserves the prior result and prospectively fixes the new contract.

Immediate rescue risk is bounded because R101 still says H7 FORMAL STOP and permits only science-invariant protected-sidecar/authority plumbing plus NON_RESULT readiness. Nonetheless, the canonical label itself must be corrected prospectively because downstream automation could otherwise infer broader OPEN permissions. Historical R100/R101 records must remain unchanged.

### Repair classification

Candidate 35's launch-workflow syntax repair is correctly SCIENCE_INVARIANT_REPAIR: the workflow proves that the only launch-commit difference from the bound implementation head is the workflow file, then checks out the exact implementation and exact scientific-source blob before response execution. The fixed science did not change.

H7 capability/authority plumbing remains SCIENCE_INVARIANT_REPAIR so long as it does not alter R5 metric/scorer meaning, scientific threshold/tolerance, comparator, seed/exclusion policy, intervention, resource/privilege contract, hypothesis, falsifier, or success criteria. Green NON_RESULT readiness still must not automatically authorize FORMAL.

### Cycle-3 policy

Cycle 3 is not being used as an automatic terminal cap. Candidate 35 received one additional bounded cycle because the prospectively stated question had information value regardless of outcome. It was terminalized only after that current question was answered, not because a numeric cycle limit was reached. This is calibrated.

### Terminal and successor semantics

Candidate 35 is terminal for the current synthetic coordinate-null object only. The result does not justify same-object SYSTEM->MECHANISM uplift. A reachable-state/matched-natural-history successor can be legitimate only with a new candidate ID, independently motivated residual, fresh development state, and fresh reduction/comparator/falsifier contract, and must receive zero inherited confirmatory credit from the current batch.

The programme is not currently manufacturing such a successor. The remaining concern is the opposite: with zero executable mechanisms and an empty shadow/queue, the already pre-outcome-motivated residual should receive an explicit quality-floor disposition rather than disappear under generic `NO_TARGET_SHADOW`. This is a throughput/false-negative calibration issue, not a license to create a successor automatically.

## Gate-by-gate classifications

| Material gate | Classification | Calibration finding |
|---|---|---|
| Hard integrity floor | KEEP | No consumed FORMAL rerun/rescore, new H7 identity/START, evidence mutation, or historical rewrite observed. |
| Orthogonal development-phase axis | TIGHTEN | Candidate 35 is correct, but H7 regressed from RESULT_EXPOSED to OPEN on the same object without fresh-version semantics. |
| Candidate 35 live OPEN -> RESULT_EXPOSED transition | KEEP | One bounded batch, raw-before-return, fresh Analyst review, authority exhaustion, no automatic continuation. |
| Fresh RESULT_EXPOSED -> CONSUMED_ONE_WAY live trace | INSUFFICIENT_EVIDENCE | A fresh one-way FORMAL consumption remains unobserved. |
| Cycle-3 mandatory reassessment | KEEP | Candidate 35 continued only for a prospectively stated informative question. |
| Cycle-3 automatic terminal cap | RELAX | Count alone must never terminalize an informative development object. |
| Candidate 35 one bounded SYSTEM development batch | KEEP | Correctly scoped as SYSTEM development only, not confirmation. |
| Candidate 35 raw-before-return/read preservation | KEEP | Direct code/workflow/raw-ref evidence demonstrates the intended ordering. |
| Candidate 35 one-shot authority exhaustion | KEEP | Batch-complete marker and post-exposure state exhaust authority. |
| Candidate 35 same-object rerun/retune/rescore | TIGHTEN | Must remain STOP after exposure. |
| Candidate 35 SYSTEM claim ceiling | KEEP | No MECHANISM uplift or PRE_FORMAL credit occurred. |
| Candidate 35 current-object terminalization | KEEP | The frozen current question was answered; terminalization is not cycle-count based. |
| Candidate 35 science/implementation/observation revision observability | CLARIFY | `NONRESULT` revision naming survives into result-bearing records; use orthogonal durable axes prospectively. |
| H7 phase monotonicity after prior result exposure | TIGHTEN | Same object should remain RESULT_EXPOSED unless a fresh versioned object/revision is explicitly created. |
| H7 science-invariant remediation only | KEEP | Capability/authority plumbing and NON_RESULT readiness remain appropriately scoped. |
| H7 green readiness as automatic FORMAL GO | TIGHTEN | A fresh Analyst generation is still required before any one-way identity/start. |
| Development observations as independent confirmation | TIGHTEN | Candidate 35 remains zero-credit; repeated PRE_FORMAL/development observations must not accumulate confirmatory weight. |
| PRE_FORMAL as real development | KEEP | Development may produce informative results without becoming FORMAL. |
| Hidden second FORMAL gate | KEEP | Candidate 35 was not required to have already won before development response. |
| Persisted READY vs effective executable readiness | CLARIFY | H7 remains persisted READY but effectively non-executable on HOLD. |
| Current-object terminal semantics | KEEP | #34/#35 current-object terminalization does not imply topic death. |
| Same-object post-outcome SYSTEM -> MECHANISM uplift | TIGHTEN | Remains prohibited. |
| Fresh independently motivated SYSTEM -> MECHANISM successor | KEEP | Legitimate only with a new ID and fresh prospective contract. |
| No-target shadow vs pre-outcome residual disposition | CLARIFY | Explicitly adjudicate the recorded reachable-state residual or state NO_COHERENT_MECHANISM_TARGET with reason. |
| Mechanism-supply health | CLARIFY | Zero executable MECHANISM and empty queue/shadow is acceptable briefly but must not become normalized without explicit residual review. |
| Theory-backward quality floor | KEEP | No forced mechanism target is required; explicit NO_COHERENT_MECHANISM_TARGET is valid when justified. |
| Protected/adaptive-evaluation validity | TIGHTEN | No leakage observed, but a fresh successful one-way FORMAL protected handoff remains unobserved. |
| Classification completeness | KEEP | R101 reports all 35 canonical candidates classified. |
| PASS reachability | KEEP | H7 has a concrete capability/authorization blocker, not an impossible evidence threshold. |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Not fully. Candidate 35 now demonstrates a clean live OPEN -> RESULT_EXPOSED transition, but H7's canonical phase regressed from RESULT_EXPOSED in R100/R92 to OPEN in R101 without fresh-object semantics. That must be tightened prospectively.
2. **Is cycle-3 review being mistaken for a hard terminal cap?** No. Candidate 35 continued for one bounded informative batch and closed only after the prospective question was answered.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Mostly yes. Candidate 35 workflow/authority plumbing and H7 sidecar plumbing are correctly invariant; the H7 phase regression and `NONRESULT` revision naming create semantic observability ambiguity that must be clarified.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** Candidate 35 yes: exactly one batch, zero confirmatory credit, unique raw ref, authority exhausted, no automatic rerun. H7 has no rerun authorized, but the OPEN label could create future permissive ambiguity.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Candidate 35 does. H7's earlier result remains preserved, but its phase label must not revert to OPEN on the same object. Any future science-affecting H7 revision needs explicit versioning/fresh-object semantics while preserving the prior result.
6. **Is FORMAL one-way integrity unchanged?** Yes. Stable main/evidence refs remain unchanged; no new H7 identity, START, protected evaluation, score, or evidence ref is observed.
7. **Are legitimate fresh SYSTEM->MECHANISM successors being suppressed or manufactured?** No manufactured successor is observed. Suppression is not proven, but the pre-outcome Candidate 35 residual should receive an explicit quality-floor disposition so `NO_TARGET_SHADOW` does not silently become topic death.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes for Candidate 35: it remained below PRE_FORMAL and zero-credit despite a real informative development response. H7 READY remains distinct from effective executability.
9. **Are terminal semantics and candidate-supply controls calibrated?** Current-object terminalization is calibrated; candidate supply is not yet healthy. Zero executable MECHANISM plus an empty queue/shadow warrants explicit residual adjudication rather than automatic rescue or indefinite no-target normalization.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes. H7 remains blocked by a concrete protected-sidecar capability plus fresh-Analyst authorization sequence. No criterion relaxation is needed; development-phase labeling should be corrected before automated permissions depend on it.

## Risk assessment

### False-positive risk

`MODERATE_WATCH`. Candidate 35 itself is well bounded, but H7's canonical reversion to OPEN_DEVELOPMENT could allow a downstream consumer to infer rerun/retune permissions that are invalid for a result-exposed same object. Current explicit HOLD/STOP language prevents an immediate violation.

### False-negative / throughput risk

`MODERATE_WATCH`. There is no executable MECHANISM, no queued canonical candidate, and 34/35 current objects are terminal. The programme should neither manufacture a successor nor allow a previously recorded independent residual to disappear without a theory-backward disposition.

### Moving-goalpost / rescue risk

`LOW_WATCH` for Candidate 35: the scientific fields were frozen, the one-shot batch was exact-bound, raw was preserved first, and authority is exhausted. `MODERATE_SEMANTIC_WATCH` for H7 until phase monotonicity is restored prospectively.

### Over-terminalization risk

`MODERATE_WATCH`. #34/#35 current-object closures are individually justified, but the queue/shadow is empty despite a prospectively recorded residual that may or may not support a fresh successor. The correct response is explicit residual adjudication, not automatic reopening.

## Claim-type findings

- Candidate 35 remains SYSTEM. Its batch is informative only for the frozen SYSTEM architecture question and carries zero confirmatory credit.
- Candidate 35 must not be upgraded on the same object to MECHANISM or PRE_FORMAL based on this result.
- H7 remains MECHANISM at PRE_FORMAL with persisted READY but effective FORMAL STOP on integrity/capability HOLD.
- H7's phase should remain RESULT_EXPOSED on the same object; OPEN is not appropriate absent a fresh versioned object/revision.
- Candidate 34 remains terminal for its current object only.
- A fresh Candidate 35 topic successor is legitimate only if independently motivated and prospectively contracted; the current batch cannot supply confirmatory credit to it.

## Mechanism-supply health

`ZERO_EXECUTABLE_MECHANISM_EMPTY_CANONICAL_QUEUE_WITH_ONE_EXPLICIT_PREOUTCOME_RESIDUAL_REQUIRING_DISPOSITION`.

This is acceptable as a short-lived state, not as a default equilibrium. H7 capability remediation should continue only as science-invariant preparation. Separately, the recorded Candidate 35 reachable-state/on-manifold residual should either pass the theory-backward quality floor into a fresh candidate or receive an explicit `NO_COHERENT_MECHANISM_TARGET` disposition. No rescue successor should be forced merely to create activity.

## Funnel observability

R101 reports 35 total candidates, 34 `TERMINAL_FOR_CURRENT_OBJECT`, one nonterminal H7 HOLD, zero queued objects, zero executable MECHANISM, persisted READY=1 but effective executable=0, OPEN_DEVELOPMENT=2, and RESULT_EXPOSED_DEVELOPMENT=33. The READY/effective split is still necessary and should be explicit to all state consumers.

The H7 phase regression shows that the development-phase dimension itself needs a monotonicity invariant in durable state: same candidate/object identity may transition OPEN -> RESULT_EXPOSED -> CONSUMED_ONE_WAY, but must not transition RESULT_EXPOSED -> OPEN unless a new versioned object/revision is explicitly instantiated and linked to preserved prior results.

## PRE_FORMAL calibration

PRE_FORMAL remains development-only. Candidate 35 demonstrates that meaningful development results can be obtained below PRE_FORMAL without treating them as independent confirmation or requiring a prior win. H7 demonstrates why persisted `READY` must mean only that a prospective next test is scientifically well-defined; integrity/capability HOLD can still make effective execution unavailable.

No hidden second FORMAL gate is observed. Repeated development observations must continue to carry zero independent confirmatory multiplicity.

## Pass reachability

PASS remains realistically reachable without weakening evidence standards. H7's blocker is a concrete protected-sidecar capability/authority problem. The required route remains: science-invariant capability repair -> NON_RESULT readiness -> STOP -> fresh Analyst exact re-fetch/authorization -> fresh one-way FORMAL identity/START only if still valid. A fresh successful one-way case remains unobserved, so the final protected-evaluation path is still an evidence gap rather than a reason to weaken standards.

## Prospective recommendations

1. In the next canonical Analyst generation, restore development-phase monotonicity for H7. If it is the same object, keep `RESULT_EXPOSED_DEVELOPMENT`. If a genuinely fresh development revision/object is intended, create explicit versioned semantics that preserve PF-R1 and prospectively fix the new contract. Do not edit historical R100/R101 records.
2. Keep Candidate 35's current object terminal and prohibit same-object rescue. Evaluate the already pre-outcome-recorded reachable-state/on-manifold residual through the normal theory-backward quality floor. Admit only a fresh candidate with a new ID/contract, or record `NO_COHERENT_MECHANISM_TARGET` with the reason.
3. Prospectively separate `scientific_revision`, `implementation_revision`, and `observation_batch_id/result_exposure_id`. Do not rename or mutate existing Candidate 35 raw artifacts.
4. Preserve the persisted READY vs effective executable split as an explicit machine-readable invariant; HOLD must dominate execution permissions.
5. Keep H7 FORMAL STOP after green NON_RESULT readiness until a later fresh Analyst independently re-fetches all exact bindings and explicitly authorizes one-way start.

## Utility request

`NONE`. No bounded Utility proposal is required for this audit. The material issues are canonical state semantics and candidate-supply adjudication, not a missing utility measurement.

## Hard-floor confirmation

No consumed FORMAL identity was rerun, retuned, rescored, or silently repaired. No historical PASS/FAIL was rewritten. No evidence tag was mutated. Candidate 35 is development-only and zero-credit; its raw response was preserved under exact prospective bindings before return/interpretation. H7 has no fresh identity/START/protected evaluation/score. The hard integrity floor remains intact.

## Confidence

`HIGH` on Candidate 35 execution/preservation semantics and FORMAL non-consumption because they were independently verified from the live research branch, exact workflow/runner/preservation code, raw branch, batch-complete marker, direct tag refs, and post-exposure Analyst state.

`HIGH` on the H7 phase-regression finding because R100 directly records `RESULT_EXPOSED_DEVELOPMENT` for the same H7 object while R101 directly records `OPEN_DEVELOPMENT` without a fresh candidate ID or science-affecting revision contract.

`MODERATE` on the candidate-supply diagnosis because the queue/shadow is directly empty, but whether the pre-outcome residual is coherent enough for a fresh successor is appropriately a future Analyst/theory-backward judgment rather than this methodology audit's scientific decision.

## Questions for Control / Analyst

- Was R101's H7 `OPEN_DEVELOPMENT` label intentional? If the object is unchanged, the next generation should restore `RESULT_EXPOSED_DEVELOPMENT`; if a fresh versioned object was intended, where is the explicit revision/successor contract preserving PF-R1?
- Will the Candidate 35 pre-outcome reachable-state/on-manifold residual receive an explicit theory-backward disposition rather than remaining implicit under `NO_TARGET_SHADOW`?
- Can durable state enforce a monotonic development-phase transition invariant and keep scientific revision, implementation revision, and result-batch identity as separate fields?
