# SparkBrain Methodology Calibration Audit — R90

- schema_version: 2
- generation_id: `METHCAL-20260923T212015+0900-R90-C2A74E19`
- produced_at: `2026-09-23T21:20:15+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T202015+0900-R89-4A7D91C2`
- material_change: true
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

The material change since R89 is not a scientific result. H7's prospective one-way FORMAL path was exercised only through a NON_RESULT preidentity/readiness workflow. The readiness workflow independently reached the final protected-sidecar capability gate after exact authority, untouched namespace, exact H7 source, locked runtime, fixed-blob, and R5 preidentity checks, then failed closed because the required protected-sidecar handoff capability was absent. The diagnostic explicitly reported no protected evaluation access, no scientific result, and no scoring. No H7 control/preserve ref was created and no FORMAL identity was consumed.

This is a methodology-positive failure mode: it demonstrates that the programme can revoke an operational GO before identity consumption when an integrity capability is missing. Analyst R99 correctly superseded the R97/R98 prospective FORMAL GO, put H7 on a nonterminal `FORMAL_INTEGRITY_CAPABILITY` hold, and classified remediation as science-invariant. The scientific H7 R5 contract remains unchanged.

The permitted H7 remediation is narrowly calibrated: provision the already-required protected sidecar capability, repin controller authority to the then-current Analyst exact commit, and rerun NON_RESULT readiness only. Identity creation/START in the same remediation run remains prohibited. A green readiness run must stop and be followed by a later fresh Analyst generation before any fresh FORMAL identity may be created or consumed.

Candidate 35 remains SYSTEM / OPEN_DEVELOPMENT. With H7 temporarily non-executable, R99 activates a bounded SYSTEM-priority exception only for NON_RESULT preserve-before-read/provenance-wrapper work around the unchanged contract. Candidate response remains STOP. This is a calibrated throughput valve, not a mechanism uplift and not evidence generation.

The global hard integrity floor remains unchanged. Stable main is still `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five `evidence/*` annotated tags remain; `formal/*`, `sealed/*`, and `freeze/*` are absent; no current `control/h7*` or `preserve/h7*` refs exist.

## Inputs and authority reconstruction

### Prior methodology history

R89 was read first. It had correctly classified H7 as prospectively eligible for exactly one fresh untouched one-way FORMAL identity, but explicitly noted that actual fresh consumption had not yet been observed. R90 does not rewrite R89; it records the newer readiness evidence prospectively.

### Human directive

`HUMAN-20260922-005` is consumed as a human process directive only, with zero scientific evidentiary weight. Its development-axis and iteration semantics remain the calibration target.

### Designated Control history

Latest designated Control remains `CTRL-20260923T155900+0900-R43-A91C4E6B`. It is historical/control-plane context, not scientific source of truth, and predates the new H7 readiness failure.

### Designated Analyst history

Latest canonical gate is `EVA-20260923T210010+0900-R99-6F2B8C14`, branch commit `59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`. R99 directly incorporates readiness run `35857110884` and supersedes the prior executable H7 FORMAL GO.

### Independently re-fetched authoritative repository/evidence

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- H7 scientific source: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- H7 controller: `research/main-h7-r5-oneway-controller-r98@f21dc7521af7413adcc46a2561271e0b8852f371`
- controller diff is path plumbing only: it supplies the checked-out scientific workspace path to the existing preflight script
- readiness run: `35857110884`, conclusion `failure`
- exact preidentity diagnostic completed before failure and reported `protected_evaluation_accessed=false`, `scientific_result=null`, `scoring_performed=false`
- failure boundary: missing required `H7_R5_SIDECAR_PASSPHRASE`; FORMAL was refused to arm
- `control/h7*`: none
- `preserve/h7*`: none
- evidence tags: 5 unchanged
- formal tags: 0
- sealed tags: 0
- freeze tags: 0

## Development iteration calibration

### H7

Phase remains `RESULT_EXPOSED_DEVELOPMENT`; it has not crossed into `CONSUMED_ONE_WAY`. The new controller/readiness work is correctly treated as integrity plumbing, not a new scientific revision. The missing protected sidecar capability and Analyst-SHA repin are `SCIENCE_INVARIANT_REPAIR` so long as they do not alter source, protocol, metric/scorer meaning, comparator, threshold/tolerance, seed/exclusion policy, intervention, input, resource/privilege scientific contract, hypothesis, falsifier, success criteria, or preserver semantics.

The important calibration improvement is that prior prospective authority did not survive a failed integrity check. R99 revoked executable authority before identity creation. That is the correct direction: authority is conditional on current exact binding and capability, not a license to push through a failed prestart gate.

A remaining false-positive risk is coupling remediation and START. The sidecar secret/capability may be provisioned, but the remediation run must remain NON_RESULT and must not create/consume an identity. A later fresh Analyst review is necessary after green readiness.

### Candidate 35

Phase remains `OPEN_DEVELOPMENT`, claim ceiling remains `SYSTEM`, and it is not PRE_FORMAL eligible. Cycle 3 continues to behave as mandatory reassessment rather than an automatic terminal cap. The next bounded cycle has prospective information gain: demonstrate preserve-before-read/provenance-wrapper closure without exposing the candidate response. This is a legitimate additional development cycle.

The temporary SYSTEM priority exception is acceptable only because executable MECHANISM supply is currently zero for an integrity-capability reason, and because the permitted work is NON_RESULT. It must not become an excuse to generate a response, infer support, or uplift the claim ceiling.

### Candidate 34 / historical development cases

No historical rewrite is performed. Candidate 34 remains `RESULT_EXPOSED_DEVELOPMENT`, `TERMINAL_FOR_CURRENT_OBJECT`, zero confirmatory credit. Its earlier execution-source metadata ambiguity still requires append-only clarification only; no raw mutation or rerun. It remains an example of correct preservation of development results, not independent confirmation.

## Gate-by-gate classifications

| Material gate | Classification | Calibration finding |
|---|---|---|
| Hard integrity floor | KEEP | No identity consumption, protected-eval access, scoring, evidence mutation, or historical rewrite occurred. |
| Orthogonal development-phase axis | KEEP | OPEN and RESULT_EXPOSED remain distinct from consumed one-way evidence. |
| Fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end live case | INSUFFICIENT_EVIDENCE | Fresh H7 FORMAL consumption is still unobserved. |
| H7 NON_RESULT readiness gate | KEEP | It failed before identity creation on a required protected-sidecar capability. |
| H7 exact source/runtime/preidentity binding | KEEP | Exact scientific source, fixed blobs, locked runtime, and preidentity checks all passed before the sidecar gate. |
| H7 protected evaluation isolation during readiness | KEEP | Diagnostic reports no protected evaluation access, result, or scoring. |
| H7 missing-sidecar remediation classification | KEEP | Provisioning an already-required sidecar capability is science-invariant if science remains unchanged. |
| H7 fresh Analyst SHA repin | KEEP | Authority must bind to the then-current Analyst exact commit before readiness rerun. |
| H7 identity creation in remediation run | TIGHTEN | Explicitly prohibit creation/consumption during capability repair/readiness. |
| Green readiness as automatic FORMAL authorization | TIGHTEN | Green readiness must STOP; later fresh Analyst authorization is required. |
| Same-identity rerun/retune/rescore after START | TIGHTEN | Remains forbidden. |
| Science-affecting repair after START | TIGHTEN | Remains forbidden absent prospectively frozen adaptivity. |
| RESULT_EXPOSED same-object invariant repair | KEEP | H7 controller/capability plumbing fits this class. |
| RESULT_EXPOSED science-affecting change | KEEP | Must be explicit versioned development revision or fresh successor preserving prior result. |
| Development observations as independent confirmation | TIGHTEN | PF-R1 and other development observations retain zero confirmatory credit. |
| PRE_FORMAL as real development | KEEP | Iteration is allowed before FORMAL; outcome-responsive laundering is not. |
| PRE_FORMAL eligible vs READY | KEEP | Distinction remains intact. |
| READY means informative next test | KEEP | H7 readiness is not scientific success; CAND35 green implementation is not READY. |
| Hidden second FORMAL gate | KEEP | No requirement that development must already win comparator/reduction/falsifier before READY was introduced. |
| Cycle 3 automatic terminal cap | RELAX | Explicitly not a hard cap. |
| Cycle 3 mandatory reassessment | KEEP | CAND35 provides a live compliant case. |
| Additional cycle with prospectively stated information gain | KEEP | CAND35 NON_RESULT preservation wrapper is bounded and distinct. |
| Current-object terminal semantics | KEEP | CAND34 closure does not imply topic death. |
| Immediate rescue successor manufacture | TIGHTEN | No same-family outcome-driven rescue should be generated. |
| Fresh independently motivated MECHANISM successor | KEEP | Legitimate in principle with new ID/question/reduction/comparator/falsifier/state. |
| Live SYSTEM→fresh MECHANISM successor calibration | INSUFFICIENT_EVIDENCE | No clean new live case yet. |
| CAND35 SYSTEM claim ceiling | KEEP | No mechanism inflation observed. |
| Temporary SYSTEM priority exception with zero executable MECHANISM | KEEP | Calibrated only for bounded NON_RESULT work. |
| CAND35 response while exception is active | TIGHTEN | Response remains STOP pending fresh Analyst. |
| Candidate 34 execution-source provenance | TIGHTEN | Append-only clarification still needed; no rerun/raw rewrite. |
| Raw-before-score as mere file order | CLARIFY | Must mean target-blind prediction/raw generation, not just filenames or serialization sequence. |
| Global literal target-blind prediction raw | TIGHTEN | Still must be demonstrated in each protected path. |
| Preserve-before-target-side read/scoring | TIGHTEN | H7 sidecar path has not yet been exercised end-to-end. |
| Target-sidecar independence | TIGHTEN | Missing capability shows the boundary is active, but successful protected handoff remains unobserved. |
| Exact source/protocol/package/runtime/input/scorer/preserver binding | TIGHTEN | H7 prospective path is strong, but actual one-way consumption remains to be observed. |
| Classification completeness | KEEP | Analyst R99 reports 35/35 classified. |
| Mechanism-first priority | KEEP | H7 remains first when executable; CAND35 exception is temporary and non-result. |
| Theory-backward quality floor | KEEP | No weakening observed. |
| Protected/adaptive-evaluation validity | TIGHTEN | No leakage observed, but the protected sidecar handoff is not yet operationally demonstrated. |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** Partly. OPEN and RESULT_EXPOSED semantics are functioning well; fresh `CONSUMED_ONE_WAY` transition remains unobserved. H7 readiness stopping before identity creation is a positive boundary test.
2. **Is cycle-3 review being mistaken for a hard terminal cap?** No. CAND35 is allowed a bounded extra NON_RESULT cycle for a stated preservation/provenance information gain.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in the current H7 case. Path plumbing, protected-sidecar capability provisioning, and authority-SHA repin are invariant; scientific fields remain prohibited.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** No laundering observed. Development evidence remains zero-confirmatory-credit; no new tolerance/scientific retune is being smuggled through H7 remediation.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Yes in observed cases. H7 remediation does not replace prior development results; CAND34/PF-R1 remain preserved.
6. **Is FORMAL one-way integrity unchanged?** Yes. No new identity is consumed, no H7 START/control/preserve ref exists, no protected evaluation is accessed, and evidence refs remain unchanged.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** No manufacturing is observed; CAND35 remains SYSTEM. A clean fresh-successor live case is still unobserved, so suppression risk remains a watch item.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes. Development/architecture checks and PF-R1 are not counted as confirmation; H7 readiness is an integrity gate, not a positive scientific result.
9. **Are terminal semantics and candidate-supply controls calibrated?** Mostly. Current executable MECHANISM supply is temporarily zero, but a bounded SYSTEM NON_RESULT exception provides forward motion without claim inflation. Prolonged zero-supply normalization would be a false-negative/throughput risk.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes, conditionally. The current blocker is an integrity capability (protected sidecar), not an evidentiary criterion. PASS remains reachable if the capability is provisioned and the later one-way path satisfies all exact bindings without relaxing standards.

## Risk assessment

### False-positive risk

`LOW_TO_MODERATE_WATCH`. The most important near-term hazard is accidentally treating sidecar provisioning or a green readiness check as authorization to create/start a FORMAL identity. The current R99 requirement for a later fresh Analyst is the correct guard. A second hazard is allowing the controller's Analyst authority pin to go stale; it must be re-pinned to the current exact Analyst commit before the next readiness attempt.

### False-negative / throughput risk

`LOW_TO_MODERATE_WATCH`. Viable executable MECHANISM supply has fallen from 1 to 0 due to an integrity-capability hold, not scientific exhaustion. The bounded CAND35 SYSTEM exception is a reasonable throughput response. The programme should continue independent MECHANISM discovery rather than normalize zero supply or inflate SYSTEM objects.

### Moving-goalpost / rescue risk

`LOW_WATCH`. H7 scientific R5 remains unchanged; remediation is plumbing/capability only. Risk would rise immediately if metric/scorer meaning, comparator, threshold/tolerance, intervention, input, hypothesis, falsifier, success criterion, or resource/privilege scientific contract changed in response to the failed readiness run.

### Over-terminalization risk

`LOW_TO_MODERATE_WATCH`. CAND34 is correctly terminal only for its current object. The main current risk is indirect: zero executable MECHANISM supply could become normalized and suppress fresh successor/discovery work. No such suppression is yet proven.

## Claim-type findings

- H7 remains MECHANISM ceiling, RESULT_EXPOSED development, nonterminal integrity hold; it is not a scientific FAIL.
- CAND35 remains SYSTEM ceiling; temporary priority does not change its claim type.
- CAND34 remains terminal for current object only and development-only; it is not retroactively rescored.
- No same-object SYSTEM→MECHANISM post-outcome uplift is observed.
- A legitimate fresh SYSTEM→MECHANISM successor live case remains insufficiently observed.

## Mechanism-supply health

`TRANSIENT_ZERO_EXECUTABLE_MECHANISM_ON_INTEGRITY_CAPABILITY_HOLD_WITH_BOUNDED_SYSTEM_NONRESULT_EXCEPTION`.

This is not yet candidate starvation, because H7 remains nonterminal and its blocker is specific and non-scientific. It becomes a calibration problem if the sidecar capability remains unresolved while no fresh MECHANISM discovery is supplied, or if CAND35 begins to receive response-bearing work solely to create activity.

## Funnel observability

Latest canonical Analyst R99 reports:

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
- SYSTEM-over-MECHANISM exception: 1, bounded to CAND35 NON_RESULT work
- classification completeness: 35/35

## PRE_FORMAL calibration

No hidden second FORMAL gate is observed. H7's earlier development results remain nonconfirmatory. CAND35 architecture/CI success does not make it PRE_FORMAL eligible or READY. Repeated PRE_FORMAL observations remain development observations, not independent confirmation. READY remains an informativeness/well-definition gate rather than an already-successful gate.

## Pass reachability

`REALISTIC_BUT_CAPABILITY_CONDITIONED_WITHOUT_STANDARD_RELAXATION`.

The H7 path is currently not executable because the required protected-sidecar handoff capability is absent. This is a real operational/integrity prerequisite and should not be bypassed. If provisioned, the programme must rerun NON_RESULT readiness, stop, obtain a later fresh Analyst generation, then use exactly one fresh untouched identity under the unchanged R5 contract. No criterion relaxation is needed.

## Prospective recommendations

1. Provision only the already-required protected-sidecar capability through the authorized control plane; do not expose its value and do not modify H7 scientific fields.
2. Repin the H7 controller to the then-current exact Analyst commit before rerunning readiness.
3. Rerun NON_RESULT readiness only. Even if green, do not create or consume a FORMAL identity in that run.
4. Require a later fresh Analyst generation after green readiness to re-fetch exact source/protocol/package/runtime/input/scorer/preserver/namespace state and explicitly authorize at most one untouched identity.
5. Preserve the START boundary as irreversible: once crossed, move to `CONSUMED_ONE_WAY`; no same-identity rerun/retune/rescore or science-affecting repair.
6. Keep CAND35's temporary SYSTEM exception strictly NON_RESULT and preserve-before-read/provenance-only. Candidate response stays STOP pending fresh Analyst.
7. Continue independent MECHANISM supply/discovery so H7's temporary integrity hold does not normalize zero executable mechanism supply.
8. Keep CAND34 provenance correction append-only; no rerun, raw mutation, or retroactive scientific reinterpretation under changed criteria.

## Utility request

No new Utility request. The current H7 blocker is already specifically identified as protected-sidecar/control-plane capability plus fresh authority repin. A methodology-generated Utility proposal would add no calibration information and could collide with live remediation.

## Hard-floor confirmation

`CONFIRMED_DO_NOT_RELAX`.

No consumed FORMAL identity was rerun/retuned/rescored; no scientific identity was consumed; no protected evaluation or target-side result was read; no evidence ref was mutated; no scientific PR was merged by this auditor; no scheduler was changed; no historical PASS/FAIL was rewritten.

## Confidence

- stable main / evidence-ref nonmutation: `HIGH`
- H7 exact source/controller/readiness status: `HIGH`
- H7 no result / no score / no protected-eval access / no identity consumption: `HIGH`
- H7 repair classification: `HIGH`
- CAND35 temporary SYSTEM exception calibration: `MODERATE_TO_HIGH`
- full OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live semantics: `MODERATE`, because final fresh FORMAL transition remains unobserved
- global protected/adaptive-evaluation validity: `MODERATE`
- fresh SYSTEM→MECHANISM successor calibration: `LOW_TO_MODERATE`, insufficient live evidence

## Questions for Control / Analyst

1. Will protected-sidecar capability provisioning be kept operationally separate from FORMAL identity creation/START?
2. Will the controller be pinned to the then-current Analyst exact SHA before the next readiness run?
3. Will a green readiness run stop and require a later fresh Analyst decision rather than auto-start FORMAL?
4. Will CAND35's temporary SYSTEM exception remain strictly NON_RESULT with candidate response STOP?
5. If executable MECHANISM supply stays at zero, will independent discovery continue without inflating SYSTEM claims or manufacturing rescue successors?
6. At the eventual H7 START boundary, will identity consumption, exact binding, target-blind raw generation, preservation-before-read, and irreversible `CONSUMED_ONE_WAY` semantics be enforced atomically/prospectively?
