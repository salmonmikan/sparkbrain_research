# SparkBrain Methodology Calibration Audit — R92

- schema_version: 2
- generation_id: `METHCAL-20260923T232021+0900-R92-5C91E7A4`
- produced_at: `2026-09-23T23:20:21+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T221827+0900-R91-7E31B4A2`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The material change since R91 is methodological, not scientific. Evidence Analyst R100 is now the canonical gate and has prospectively authorized exactly one bounded result-bearing Candidate 35 `ARCHITECTURE_STUDY` development batch, conditional on exact R100 authority repin, unchanged scientific-source binding, fixed five-arm order, exact runtime/component/input/serializer/preservation binding, and a NON_RESULT preflight. Candidate 35 remains `SYSTEM`, `OPEN_DEVELOPMENT`, and `preformal_eligible=false`; no candidate response has yet been generated after R100, and no PRE_FORMAL or FORMAL credit follows from the authorization.

This is calibrated development iteration rather than evidence manipulation if and only if the result is interpreted at the SYSTEM/architecture claim ceiling. R100 explicitly requires raw exclusive-create preservation before any response is returned/read/interpreted, exhausts authority after the first complete five-arm result exposure, and prohibits automatic rerun/retune/tolerance/comparator/observable changes. A negative or ordinary-reduction outcome remains valid information gain. The prior R91 concern that a caller-supplied `response_execution_allowed` flag could become de facto authority is materially addressed because R100 now requires exact fresh Analyst authority independently of that flag.

The important split is claim-type, not whether a development response may exist. A bounded SYSTEM development response is acceptable in `OPEN_DEVELOPMENT`; it must not be laundered into MECHANISM support, PRE_FORMAL readiness, or confirmatory evidence. R100 correctly states that any later mechanistic/on-manifold discriminator must be a separately prospectively defined revision or fresh successor, and the literature-based concern motivating that discriminator is recorded before the current result is exposed. This lowers rescue-laundering risk, but any later successor still needs a fresh candidate ID, independently stated residual, and fresh reduction/comparator/falsifier contract.

H7 remains unchanged on a nonterminal FORMAL integrity/capability HOLD. Stable main and authoritative evidence refs are unchanged; no H7 identity, STARTED/control ref, preserve ref, protected-evaluation access, score, or new scientific result exists. The hard one-way FORMAL floor remains intact.

A funnel-observability issue remains: R100 reports persisted PRE_FORMAL eligible/READY fields as `1/1` while simultaneously reporting H7 as non-executable on FORMAL integrity HOLD and fresh executable FORMAL authority as zero. The semantics are explicitly correct in prose, but dashboards/state consumers can still misread persisted READY as current executable readiness. Prospectively, stored readiness should be visibly separated from effective current executability/HOLD status.

## Inputs and authority reconstruction

### Prior methodology history

R91 was read first. It classified Candidate 35's cycle-3 NON_RESULT preservation/provenance completion as calibrated, kept Candidate 35 SYSTEM/OPEN/not-PRE_FORMAL, required fresh exact Analyst authority before any result-bearing use, and warned that the caller execution flag was not authority. R92 does not rewrite R91; it evaluates the new R100 authority prospectively.

### Human directive

`HUMAN-20260922-005` is consumed strictly as a process directive with zero scientific evidentiary weight. Its orthogonal development-phase semantics and cycle-3 reassessment rule remain the calibration target.

### Designated Control history

Latest designated Control is `CTRL-20260923T225500+0900-R44-C8F41D72`, state commit `3c46617fba123704297d880a748c305c16a7dd01`. R44 independently re-fetched repository/control-plane state, kept H7 on integrity-capability HOLD, recognized Candidate 35's preservation closure as NON_RESULT/science-invariant, and kept Candidate 35 response STOP pending fresh Analyst authority. Control is mailbox/governance context, not scientific source of truth.

### Designated Analyst history

Latest canonical gate is Evidence Analyst R100, state commit `a32494246245a559ad4e1f8543a1f252b03ef2e7`, with the decision history introduced at commit `2c939418abbdcfe3faba30bd2d95a2be9766909b`. R100 prospectively authorizes one bounded Candidate 35 architecture response only after exact authority/runtime/preservation closure and retains H7 FORMAL STOP.

### Independently re-fetched authoritative repository/evidence

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative `evidence/*` annotated tags: exactly 5, unchanged
- `formal/*`: 0
- `sealed/*`: 0
- `freeze/*`: 0
- H7 `control/h7*`: none independently observed
- Candidate 35 scientific source: `8ea6581544c642ad74f1a95955ab2c5f795afccc`
- Candidate 35 implementation head: `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c`
- Candidate 35 commits after the R100 decision point: none observed at audit time
- therefore no post-R100 candidate response implementation/result exposure is independently observed in this generation

## Development iteration calibration

### Candidate 35

Candidate 35 remains `SYSTEM / OPEN_DEVELOPMENT / ARCHITECTURE_STUDY`, not PRE_FORMAL eligible. R100's result-bearing authority is a legitimate additional development cycle because the scientific object and frozen fields are already stated, the batch is bounded to one fixed-order five-arm run, raw preservation must occur before return/interpretation, and authority is exhausted immediately after first complete result exposure. This is consistent with the rule that cycle 3 is reassessment rather than a hard cap.

The current authorization is not a hidden second FORMAL gate. Candidate 35 is not required to have already won a comparator/reduction/falsifier test before development response. Conversely, the development batch cannot create confirmatory credit. After exposure, the object must transition to `RESULT_EXPOSED_DEVELOPMENT`; same-object science-invariant repair remains permissible, while science-affecting changes require an explicit versioned development revision or fresh successor preserving the first result.

R100's literature-based interpretation ceiling is methodology-positive. It prospectively states that coordinate-wise potential/adaptation nulls may be off-manifold and therefore a positive intervention effect would show surgical sensitivity, not automatically a naturally reachable memory carrier. This prevents a SYSTEM result from silently inflating into a MECHANISM claim. Any later on-manifold causal-abstraction question must be separately prospectively contracted and must not inherit confirmatory credit from this development batch.

The R91 implementation/scientific revision observability concern remains. R100 conceptually separates unchanged scientific source from implementation head, which is an improvement, but durable state should continue to expose these as orthogonal revision axes rather than relying on prose/Git reconstruction.

### H7

H7 remains `MECHANISM / RESULT_EXPOSED_DEVELOPMENT / NONTERMINAL_HOLD`. The protected-sidecar capability blocker remains operational/integrity-only, not scientific evidence against H7. Allowed work remains science-invariant provisioning/authority plumbing plus NON_RESULT readiness. Green readiness must still STOP and return to a later fresh Analyst before any FORMAL identity materialization or START.

The fresh `CONSUMED_ONE_WAY` transition remains unobserved. Therefore exact source/protocol/package/runtime/input/scorer/preserver binding, target-blind prediction, raw-before-score, preserve-before-target-side read, and one-way identity consumption remain prospective requirements rather than fully demonstrated end-to-end in a fresh live case.

### Candidate 34 and successor semantics

Candidate 34 remains `RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT`, zero confirmatory credit. No same-object rescue is authorized. The current object is closed, not the topic. A future successor remains legitimate only with a new candidate ID, an independently motivated mechanistic residual/question, fresh reduction/comparator/falsifier contract, and fresh development state. R100's prospective literature note for Candidate 35 is a useful example of how independent motivation can be recorded before outcome exposure rather than manufactured afterward.

## Gate-by-gate classifications

| Material gate | Classification | Calibration finding |
|---|---|---|
| Hard integrity floor | KEEP | No new FORMAL identity, START, protected evaluation, score, evidence mutation, or historical rewrite observed. |
| Orthogonal development-phase axis | KEEP | #35 remains OPEN, H7 remains RESULT_EXPOSED, consumed one-way remains separate. |
| Fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live case | INSUFFICIENT_EVIDENCE | Fresh one-way FORMAL consumption remains unobserved. |
| Cycle-3 mandatory reassessment | KEEP | R100 reassesses #35 and allows one specifically bounded informative batch rather than terminalizing on count. |
| Cycle-3 automatic terminal cap | RELAX | It must not be a hard cap. |
| #35 one bounded result-bearing SYSTEM development batch | SPLIT_BY_CLAIM_TYPE | KEEP for SYSTEM architecture information; TIGHTEN against MECHANISM/PRE_FORMAL/confirmatory inference. |
| #35 exact fresh Analyst authority before result | KEEP | R100 directly supplies prospective authority, with exact repin required before execution. |
| Caller result-enable flag as authority | TIGHTEN | The boolean remains insufficient without the exact R100 binding/preflight. |
| #35 fixed-order one-shot batch | KEEP | Bounds adaptive choice after partial outcomes. |
| #35 preserve-before-return/read | KEEP | Prospective requirement is strong; live result-bearing execution remains unobserved. |
| Partial-batch outcome-responsive redesign | TIGHTEN | R100 explicitly prohibits redesign from partial outcome knowledge. |
| #35 post-exposure transition to RESULT_EXPOSED | KEEP | Explicitly required after the first complete batch. |
| #35 post-exposure automatic rerun/retune | TIGHTEN | Explicitly prohibited. |
| #35 scientific vs implementation revision observability | CLARIFY | R100 improves the distinction, but durable orthogonal fields remain preferable. |
| #35 SYSTEM claim ceiling | KEEP | No SYSTEM→MECHANISM inflation is authorized. |
| #35 PRE_FORMAL eligibility / READY | KEEP | Architecture response authority does not make it PRE_FORMAL or READY. |
| H7 integrity HOLD | KEEP | Capability blocker remains non-scientific and nonterminal. |
| H7 science-invariant remediation | KEEP | Sidecar/authority/runtime plumbing may be repaired without changing R5 science. |
| H7 green readiness as FORMAL GO | TIGHTEN | Must STOP for a later fresh Analyst before identity creation/START. |
| Same-identity rerun/retune/rescore after START | TIGHTEN | Remains forbidden. |
| RESULT_EXPOSED invariant repair | KEEP | Allowed with durable provenance. |
| RESULT_EXPOSED science-affecting change | KEEP | Requires explicit versioned revision or fresh successor preserving prior result. |
| Development observations as independent confirmation | TIGHTEN | #35 batch remains zero confirmatory credit. |
| PRE_FORMAL as real development | KEEP | Iteration remains allowed without turning repeated observations into independent evidence. |
| Hidden second FORMAL gate | KEEP | No requirement to pre-win the science before READY is observed. |
| Current-object terminal semantics | KEEP | #34 current-object closure is not topic death. |
| Immediate rescue successor manufacture | TIGHTEN | Still forbidden. |
| Fresh independently motivated successor | KEEP | Legitimate in principle with fresh prospective contracts. |
| Live fresh SYSTEM→MECHANISM successor case | INSUFFICIENT_EVIDENCE | No clean live case yet. |
| Persisted READY vs effective executable readiness | CLARIFY | R100 shows READY 1/1 while H7 is HOLD and executable FORMAL authority is 0; consumers need an explicit effective-status dimension. |
| Mechanism-first priority | KEEP | H7 remains preferred when executable; #35 is a bounded SYSTEM exception while H7 is blocked. |
| SYSTEM-priority exception scope | SPLIT_BY_CLAIM_TYPE | Result-bearing SYSTEM development is acceptable only for the prospectively bounded SYSTEM question, never as a MECHANISM substitute. |
| Theory-backward quality floor | KEEP | No weakening or forced mechanism target observed. |
| Protected/adaptive-evaluation validity | TIGHTEN | No leakage observed, but successful H7 protected handoff/one-way consumption remains unobserved. |
| Classification completeness | KEEP | R100 reports 35/35 classified. |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Mostly yes for OPEN and RESULT_EXPOSED. R100 now supplies a clean prospective transition rule for #35 after first result exposure. Fresh `CONSUMED_ONE_WAY` remains unobserved.
2. **Is cycle-3 review being mistaken for a hard terminal cap?** No. #35 is allowed one additional bounded batch because it has prospectively stated information gain and fixed stopping rules.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in R100: authority/runtime/package/preservation closure may be repaired; any change to frozen scientific fields must stop for a versioned revision/fresh successor decision.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** Yes prospectively for the new #35 batch: one batch only, zero confirmatory credit, no automatic rerun/retune. No new result has yet been observed.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Observed historical cases remain preserved; #35's prospective rule requires preserved raw before interpretation and versioning/fresh successor for science-affecting post-exposure change. The live #35 transition is not yet observed.
6. **Is FORMAL one-way integrity unchanged?** Yes. Main/evidence refs are unchanged; H7 has no identity/START/protected evaluation/score/new evidence.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** Neither is demonstrated. #35 remains SYSTEM; R100 prospectively records an independent literature-based on-manifold concern without manufacturing an immediate successor. A future successor must still satisfy fresh-ID/contract requirements.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes. #35 remains below PRE_FORMAL despite receiving bounded architecture-response authority; development success/failure cannot become confirmation.
9. **Are terminal semantics and candidate-supply controls calibrated?** Mostly. #34 is terminal only for its current object; executable MECHANISM supply remains zero. One bounded SYSTEM development batch is a defensible throughput exception, but repeated SYSTEM result work merely because MECHANISM supply is zero would become over-permissive.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes, conditionally. H7 is blocked by a concrete protected-sidecar capability and fresh authorization sequence, not by an impossible evidence threshold. No criterion relaxation is required.

## Risk assessment

### False-positive risk

`LOW_TO_MODERATE_WATCH`. R100 substantially reduces the prior flag-as-authority risk by requiring exact authority repin and a fixed batch. The remaining risk is interpretive: a positive off-manifold null intervention could be overread as a naturally reachable MECHANISM. R100's explicit SYSTEM ceiling and prospective literature interpretation guard should be kept.

### False-negative / throughput risk

`LOW_TO_MODERATE_WATCH`. Executable MECHANISM supply is still zero while H7 is capability-held. The bounded #35 batch provides legitimate development information, but the programme must continue independent MECHANISM discovery and avoid normalizing SYSTEM result-bearing work as a substitute for mechanism supply.

### Moving-goalpost / rescue risk

`LOW_WATCH`. #35 scientific fields are frozen before the authorized batch; partial results cannot authorize redesign; first complete exposure exhausts authority. Risk would rise if the later literature-motivated on-manifold question were instantiated only after seeing the #35 outcome without preserving the already-recorded independent motivation and fresh contract.

### Over-terminalization risk

`LOW_TO_MODERATE_WATCH`. Cycle 3 is explicitly not a hard cap and #34 is current-object terminal only. Main residual risk remains candidate-supply scarcity, not observed topic death.

## Claim-type findings

- Candidate 35 remains SYSTEM. The authorized development batch can test the frozen SYSTEM architecture question only.
- Candidate 35 must not become MECHANISM, PRE_FORMAL-ready, or confirmatory merely because the batch has a positive result.
- H7 remains MECHANISM on nonterminal integrity HOLD, not scientific FAIL.
- Candidate 34 remains terminal for its current result-exposed object only.
- No same-object post-outcome SYSTEM→MECHANISM uplift is observed.
- No fresh successor is yet admitted; the pre-outcome R39 literature concern may serve as independent motivation only if a future successor receives a fresh ID and prospective contract.

## Mechanism-supply health

`ZERO_EXECUTABLE_MECHANISM_WITH_ONE_BOUNDED_SYSTEM_DEVELOPMENT_RESPONSE_PROSPECTIVELY_AUTHORIZED`.

This is acceptable as a temporary throughput condition because the #35 action is one-shot, prospectively bounded, zero-credit, and claim-scoped. It becomes a calibration problem if further SYSTEM result-bearing cycles are granted mainly to keep activity high, if H7 capability remediation stalls without independent mechanism discovery, or if #35's result is used to bypass a fresh MECHANISM contract.

## Funnel observability

Canonical R100 reports:

- canonical candidates: 35
- MECHANISM: 14
- SYSTEM: 21
- ACTIVE: 0
- QUEUED: 1
- HOLD: 1
- TERMINAL_FOR_CURRENT_OBJECT: 33
- OPEN_DEVELOPMENT: 3
- RESULT_EXPOSED_DEVELOPMENT: 32
- canonical CONSUMED_ONE_WAY: 0
- persisted PRE_FORMAL eligible / READY: 1 / 1
- viable executable MECHANISM: 0
- fresh executable FORMAL authority: 0
- official consumed scientific identities: 7, unchanged
- new identity consumed in R100: 0
- SYSTEM-over-MECHANISM priority exception: 1
- classification completeness: 35/35

The main observability clarification is that persisted READY must not be mistaken for current executable readiness when a stronger HOLD dimension is active. Prospectively expose `effective_executable_ready` (or equivalent) separately from persisted scientific readiness/history.

## PRE_FORMAL calibration

`CALIBRATED_WITH_OBSERVABILITY_WATCH`.

PRE_FORMAL remains development-only and repeated development observations retain zero independent confirmatory credit. Candidate 35 demonstrates that informative development may occur even before PRE_FORMAL eligibility; that is acceptable because the architecture batch is explicitly non-evidentiary. H7's persisted readiness field coexisting with an integrity HOLD should be made clearer in state/reporting, but it is not itself a hidden second FORMAL gate.

## Pass reachability

`REALISTIC_WITHOUT_STANDARD_RELAXATION_BUT_CAPABILITY_CONDITIONED`.

H7 has a concrete, repairable non-scientific blocker. The correct path remains: science-invariant protected-sidecar/authority repair → green NON_RESULT readiness → STOP → later fresh Analyst re-fetch → one untouched FORMAL identity if reauthorized. No threshold/comparator/scorer/evidence relaxation is needed.

## Prospective recommendations

1. Execute no #35 response unless the implementation is repinned to exact R100 authority and the fixed five-arm NON_RESULT preflight proves scientific fields/order/bindings unchanged.
2. If the #35 batch executes, preserve each raw artifact before any return/read/comparison, stop after the first complete batch, transition the object to RESULT_EXPOSED_DEVELOPMENT, and do not automatically rerun/retune.
3. Treat any #35 positive effect as SYSTEM-level surgical sensitivity only. Do not infer MECHANISM or PRE_FORMAL success from it.
4. If a later on-manifold/mechanistic question is pursued, preserve the pre-outcome R39 motivation and require a fresh candidate ID plus fresh reduction/comparator/falsifier contract; do not rescue the current object.
5. Continue to separate scientific development revision from implementation/instrumentation revision in durable state.
6. Make persisted readiness and effective executable readiness/HOLD visibly distinct in funnel reporting.
7. Keep H7 repair non-result and science-invariant; a green readiness run must still stop for a later fresh Analyst before identity materialization/START.
8. Continue independent MECHANISM discovery while H7 is blocked; do not use repeated SYSTEM result work to normalize zero mechanism supply.

## Utility request

No Utility request created. R100 already supplies a bounded live calibration case (#35 one-shot development response) and H7 has a specific live remediation boundary. An additional methodology request would add little information and could collide with active work.

## Hard-floor confirmation

`CONFIRMED_DO_NOT_RELAX`.

No consumed FORMAL identity was rerun, retuned, or rescored. No frozen historical PASS/FAIL was rewritten. Stable main and evidence refs are unchanged. No H7 identity/START/protected-evaluation access/scoring/new evidence was observed. #35 has not yet produced a post-R100 result, and its prospective authority remains development-only with zero confirmatory credit.

## Confidence

- prior methodology reconstruction: HIGH
- R100 authority reconstruction: HIGH
- stable main/evidence nonmutation: HIGH
- #35 no post-R100 branch commit/result at audit point: HIGH for branch state, MODERATE for all possible external runtime surfaces
- #35 one-shot SYSTEM development calibration: MODERATE_TO_HIGH
- H7 unchanged integrity HOLD: HIGH
- fresh end-to-end CONSUMED_ONE_WAY calibration: MODERATE / insufficient live evidence
- fresh SYSTEM→MECHANISM successor calibration: MODERATE / insufficient live evidence

## Questions for Control / Analyst

1. After the #35 batch, will the development phase be changed to RESULT_EXPOSED before any further scientific decision, with the one-shot authority explicitly exhausted?
2. Will #35's fixed SYSTEM interpretation ceiling survive a positive intervention result without opportunistic MECHANISM uplift?
3. If an on-manifold successor is later proposed, will the already-recorded pre-outcome R39 motivation be paired with a genuinely fresh candidate ID and prospective contract rather than an outcome-contingent rescue?
4. Can funnel state expose persisted READY separately from effective executable readiness while H7 is on integrity HOLD?
5. Will H7 capability repair remain separated from identity creation/START and require a later fresh Analyst after green NON_RESULT readiness?
