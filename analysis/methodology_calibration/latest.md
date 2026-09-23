# SparkBrain Methodology Calibration Audit — R79

- schema_version: `2`
- generation_id: `METHCAL-20260923T111832+0900-R79-5B7C21D4`
- produced_at: `2026-09-23T11:18:32+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes_generation_id: `METHCAL-20260923T101704+0900-R78-2B6F91C4`
- material_change: `true`
- audit_result: `MATERIAL_CALIBRATION_UPDATE`
- overall_classification: `MIXED_CALIBRATION`

## Executive decision

A material calibration update is present and the hard integrity floor remains unchanged.

Fresh Evidence Analyst R92 retracts candidate #34's R91 PRE_FORMAL READY transition before any response-bearing execution. Independent Audit R8 found a causal-opportunity defect in the frozen R1 intervention plan: under the authoritative current implementation, the direct target edge `2→3` has a `2.0 ms` delay, while the fixed source pattern directly cues unit 2 at `0.0 ms` and unit 3 at `1.0 ms`. With threshold `1.0` and `3.0 ms` refractory duration, unit 3 spikes from the direct cue at `1.0 ms` and is refractory through approximately `4.0 ms`; transmission from unit 2 arrives at `2.0 ms`. Therefore the target weight-null arm is structurally distinct but lacks ordinary pre-outcome causal opportunity to alter unit-3 spiking under the frozen plan. Executing R1 would risk a low-information null/equivalence observation caused by the intervention timing rather than route non-identifiability.

The defect was detected before any candidate response execution, scoring, scientific evidence creation, FORMAL identity, or evaluation consumption. R1's scientific contract and exact prebinding remain preserved as NON_RESULT provenance. R92 returns candidate #34 to `MECHANISM / PRE_FORMAL / OPEN_DEVELOPMENT / NOT_READY`, explicitly forbids R1 response execution, and authorizes only a prospectively versioned same-candidate `CAND34-PREF-R2-CAUSAL-OPPORTUNITY-REVISION` that must establish pre-outcome causal opportunity before any response-bearing development run.

This is a strong positive case for HUMAN-20260922-005 development semantics. The required R2 change is science-affecting, but it occurs in `OPEN_DEVELOPMENT` before meaningful result exposure. The programme does not need a fresh candidate merely because the development contract requires revision; a same-question, explicitly versioned R2 is calibrated if R1 remains immutable provenance and the change is prospective. A fresh successor becomes necessary when the scientific question is genuinely distinct or when post-result changes would otherwise rescue an exposed object.

A new methodology guard is required prospectively: structural intervention distinctness, hash distinctness, and successful prebinding do not establish scientific informativeness. Before response-bearing PRE_FORMAL execution, intervention plans must demonstrate a causal-opportunity path from the manipulated variable to the measured outcome within the fixed source pattern/window and model dynamics. For candidate #34 R2 this should include, at minimum, source/cue timing, edge-delivery timing, downstream threshold/refractory state, the actual transmitted state variable used by the outcome, and the same opportunity check for matched controls.

The stale literature-summary phrase describing a `2 ms` timestep is not authoritative for current execution. Independent repository re-fetch confirms current `V05BrainConfig.dt_ms=0.25`, and the current refractory implementation sets `refractory_until = now_ms + refractory_ms`. Current source/protocol bindings supersede stale narrative prose; the stale prose must not be used to justify or reinterpret the frozen R1 timing.

H7 remains unchanged at R5 PREIDENTITY COMPLETE but NON_EVIDENTIARY and held at the FORMAL provenance gate. The PF-R1 artifact is still present and unexpired, but durable NON_EVIDENTIARY preservation remains blocked by missing matching schema-v2 Utility machine authority. No rerun/reconstruction/rescore is justified or permitted.

Independent repository/evidence re-fetch confirms stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, authoritative `evidence/*` remains exactly five tag objects, and tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No fresh FORMAL identity consumption is observed.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase orthogonal axis | `KEEP` |
| fresh OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY end-to-end | `INSUFFICIENT_EVIDENCE` |
| OPEN development may make explicit prospective science-affecting pre-result revisions | `KEEP` |
| candidate #34 READY revocation after pre-result informativeness defect | `KEEP` |
| preserve superseded R1 contract/prebind as NON_RESULT provenance | `KEEP` |
| same-candidate versioning before meaningful result exposure when question is unchanged | `KEEP` |
| requiring a fresh candidate for every pre-result OPEN scientific revision | `CLARIFY` |
| candidate #34 response execution under causally inert R1 target arm | `TIGHTEN` |
| causal-opportunity/informativeness proof before response-bearing PRE_FORMAL | `TIGHTEN` |
| structural/hash distinctness treated as causal opportunity | `CLARIFY` |
| authoritative current source/protocol timing over stale literature prose | `KEEP` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 as mandatory information-gain reassessment | `KEEP` |
| additional development cycle with prospectively stated distinct information gain | `KEEP` |
| development rerun/retune results counted as independent confirmation | `TIGHTEN` |
| repeated result-bearing PRE_FORMAL live stress case | `INSUFFICIENT_EVIDENCE` |
| PRE_FORMAL as genuine development | `KEEP` |
| preformal_eligible distinct from READY | `KEEP` |
| READY = next test well-defined/informative, not prior success | `KEEP` |
| HIDDEN_SECOND_FORMAL_GATE | `KEEP` — false |
| H7 R5 PREIDENTITY COMPLETE distinct from FORMAL authority/evidence | `KEEP` |
| PF-R1 exact-byte preservation requirement | `KEEP` |
| PF-R1 preservation execution state | `TIGHTEN` |
| Utility default-deny without schema-v2 machine authority | `KEEP` |
| duplicate request/rerun to bypass PF-R1 authority gap | `TIGHTEN` |
| raw-before-score as file ordering only | `CLARIFY` |
| literal target-blind prediction raw | `TIGHTEN` |
| immutable preserve before target-side scoring | `TIGHTEN` |
| post-preserve scorer recomputation | `TIGHTEN` |
| target-sidecar independence | `TIGHTEN` |
| fresh concealed evaluation surface | `TIGHTEN` |
| final exact source/runner/scorer/preserver/runtime/input binding | `TIGHTEN` |
| current-object claim ceiling | `KEEP` |
| same-object post-outcome SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh successor distinctness/non-rescue | `KEEP` |
| fresh SYSTEM→MECHANISM successor specifically | `INSUFFICIENT_EVIDENCE` |
| TERMINAL_FOR_CURRENT_OBJECT closes only the current object | `KEEP` |
| classification completeness | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| SYSTEM work that does not displace a viable MECHANISM lane | `KEEP` |
| genuine SYSTEM-over-comparable-MECHANISM MAIN exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor | `KEEP` |
| NO_COHERENT_MECHANISM_TARGET liveness semantics | `KEEP` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Are development-phase semantics implemented consistently end-to-end?** They are consistent through the newly observed pre-result revision boundary. Candidate #34 is a strong positive case: an informativeness defect was found after non-result prebinding, READY was revoked, R1 was preserved, and a science-affecting R2 revision was authorized without claiming evidence. A fresh post-HUMAN-005 `CONSUMED_ONE_WAY` completion remains unobserved.
2. **Is cycle 3 being mistaken for a hard terminal cap?** No. R91 used cycle 3 as reassessment; R92 then found a distinct pre-result information defect and permits cycle 4 only to establish causal opportunity prospectively. This is calibrated additional development, not rescue tuning.
3. **Are SCIENCE_INVARIANT_REPAIR and SCIENCE_AFFECTING_CHANGE distinguished correctly?** Yes in this case. The R2 intervention/timing repair is science-affecting, but because no meaningful result was exposed it may be an explicit same-candidate OPEN development revision. R1 remains immutable provenance. After result exposure, the same kind of change would require a new version/fresh successor under RESULT_EXPOSED rules.
4. **Are development rerun/retune/tolerance revisions logged without being laundered into independent evidence?** No laundering is observed. R1 prebinding and CI are NON_RESULT; no candidate response exists. The programme still lacks a live repeated result-bearing PRE_FORMAL series that stress-tests correlated/non-independent accounting.
5. **Does RESULT_EXPOSED development preserve prior results when revised?** Yes in the H7 R4→R5 lineage. Programme-wide durability remains incomplete because PF-R1 existing bytes are not yet durably preserved under valid machine authority. Candidate #34 is not yet RESULT_EXPOSED.
6. **Is FORMAL one-way integrity unchanged?** Yes. Stable main/evidence refs are unchanged, no formal/sealed/freeze tags exist, and no new identity/result consumption is observed.
7. **Are legitimate fresh SYSTEM→MECHANISM successors being suppressed or manufactured?** No manufacture is observed. A specifically fresh MECHANISM successor originating from a terminal SYSTEM object remains unobserved.
8. **Is PRE_FORMAL behaving as development rather than hidden FORMAL?** Yes, strongly. #34 READY can be revoked before result exposure because the next test is not informative; the programme revises the development test instead of pretending technical prebinding is scientific success. No prior comparator/falsifier victory is required.
9. **Are terminal semantics and candidate-supply controls calibrated?** Yes/improving. There are two MECHANISM lineages (H7 held, #34 open revision) plus SYSTEM discovery backup without forced claim inflation.
10. **Is PASS realistically reachable without weakening evidence standards?** Yes. H7 remains `REALISTIC_NEAR_TERM_CONDITIONAL`; #34 can regain development readiness after R2 demonstrates causal opportunity. No evidence standard needs weakening.

## Risk calibration

False-positive risk is `MODERATE_WATCH`: a structurally distinct but causally inert intervention could produce a misleading null/equivalence result if response execution were allowed without a causal-opportunity gate. Technical binding success must not be mistaken for intervention informativeness.

False-negative/opportunity-cost risk is `LOW_TO_MODERATE_WATCH_IMPROVING`: the defect was detected before output exposure, READY was revoked without terminalizing the topic, and a same-candidate prospective revision is allowed instead of forcing unnecessary successor fragmentation.

Moving-goalpost/rescue risk is `LOW_WATCH_IMPROVING`: no outcome was observed before the R2 change, so the revision is not outcome-responsive rescue. R1 remains frozen NON_RESULT provenance and the R2 delta must be prospective.

Over-terminalization risk is `LOW_WATCH_IMPROVING`: #34 is revised rather than killed, while the scientific question/claim ceiling remains stable.

## Development-iteration calibration

Candidate #34 now supplies the clearest live example of why iteration itself is not a defect. Architecture R2 and PRE_FORMAL R1 prebinding were technically coherent, but static causal analysis showed the target intervention lacked opportunity to affect the chosen outcome under the fixed dynamics. Because this was discovered before any meaningful response, `OPEN_DEVELOPMENT` should permit a science-affecting R2 revision with explicit provenance.

The calibrated R2 boundary is narrow: modify only what is necessary to ensure the target and matched controls have pre-outcome causal opportunity under the same fixed source pattern/common measurement window, document the exact scientific delta prospectively, prove the opportunity statically against current authoritative source dynamics, freeze R2, run only NON_RESULT validators/CI, and STOP for fresh Analyst review before any response-bearing execution.

Structural byte/hash distinctness is an engineering integrity check, not a scientific opportunity check. The new prospective methodology guard should explicitly trace timing/state reachability from source cue/spike through the manipulated edge to the measured downstream variable before candidate response execution.

## Funnel observability / mechanism supply

Fresh R92 canonical population remains `35 = 14 MECHANISM / 21 SYSTEM`. Lifecycle remains `TERMINAL_FOR_CURRENT_OBJECT 32` with one held MECHANISM lineage and queued/open development lanes; development phases remain `OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`. PRE_FORMAL eligible remains `2`, while READY drops from `2` to `1` because candidate #34 is correctly returned to NOT_READY. Fresh FORMAL authority remains `0`, historical official consumed identities remain `7`, and classification completeness remains `35/35`.

Mechanism-supply health is `TWO_MECHANISM_LINEAGES_H7_FORMAL_HOLD_CAND34_OPEN_REVISION_WITH_SYSTEM_DISCOVERY_BACKUP_QUALITY_FLOOR_INTACT`.

## Preformal calibration / pass reachability

`HIDDEN_SECOND_FORMAL_GATE=false`. Candidate #34 demonstrates that READY is reversible before meaningful exposure when the proposed development test is discovered to be uninformative. That is development calibration, not terminal failure and not evidence invalidation.

Repeated PRE_FORMAL observations, when eventually used, remain one correlated development sequence rather than independent confirmation. No repeated result-bearing live stress case has yet been observed.

H7 PASS reachability remains `REALISTIC_NEAR_TERM_CONDITIONAL`: preserve existing PF-R1 bytes under valid machine authority without rerun/reconstruction/rescore, require a later fresh Analyst re-fetch of unchanged exact R5, and retain prediction-only raw → immutable preserve → target-side scoring, concealed evaluation, collision/no-clobber, and exact binding gates.

## Utility request

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the only request. Utility default-deny remains correct until matching schema-v2 machine authority exists. The existing PF-R1 artifact is recoverable and must not be rerun, reconstructed, regenerated, or rescored.

## Prospective recommendations

- Do not execute candidate #34 R1 responses. Preserve the frozen R1 contract and exact prebinding unchanged as NON_RESULT provenance.
- Create an explicit same-candidate R2 development revision limited to causal opportunity. For target and controls, statically demonstrate cue/source timing, edge delivery, downstream threshold/refractory state, and the actual state variable capable of influencing the measured outcome before the outcome window closes.
- Treat structural/hash distinctness as necessary engineering provenance but insufficient scientific informativeness.
- Freeze R2 prospectively, validate it only with NON_RESULT checks, then STOP for fresh Analyst review before any response-bearing PRE_FORMAL run.
- If R2 would need to alter the scientific question, outcome, comparator/reduction meaning, decision criterion, or resource/privilege contract beyond the documented opportunity repair, explicitly reassess/version that broader change; do not smuggle it in as implementation repair.
- Keep H7 development stopped; resolve PF-R1 preservation using existing bytes only under valid machine authority, then require fresh Analyst one-way review.

## Hard-floor confirmation / confidence

`CONFIRMED_DO_NOT_RELAX`.

Confidence: FORMAL non-consumption `HIGH`; candidate #34 R1 NON_RESULT prebinding `HIGH`; R1 causal-opportunity defect under authoritative current source timing/refractory dynamics `HIGH`; READY revocation and same-candidate pre-result R2 revision calibration `HIGH`; PF-R1 artifact recoverability/authority blocker `HIGH`; fresh consumed-FORMAL end-to-end `UNOBSERVED`; repeated result-bearing PRE_FORMAL non-independence live stress case `UNOBSERVED`; fresh specifically SYSTEM→MECHANISM successor `UNOBSERVED`.

## Questions for Control / Analyst

- Will candidate #34 R2 explicitly prove pre-outcome causal opportunity for target and matched controls before any response-bearing execution?
- Will R1 contract/prebinding remain immutable NON_RESULT provenance rather than being rewritten or reinterpreted after the defect?
- Will R2 stay a same-candidate explicit development revision only while the underlying scientific question remains unchanged and no meaningful result has yet been exposed?
- Will R2 freeze and STOP for fresh Analyst review before any candidate response, scoring, or evidence creation?
- Can the existing PF-R1 preservation request receive matching schema-v2 machine authority without duplicate request or artifact rerun/reconstruction?

## Authoritative refs used

- prior Methodology: `METHCAL-20260923T101704+0900-R78-2B6F91C4@14f0f1a009a5f288e1463782c638db679b4f3f76`
- Human directive: `HUMAN-20260922-005` (process directive, not scientific evidence)
- Control: `CTRL-R40@f25d48598584bffc5ca736c6ac52c50a94688d89`
- Evidence Analyst: `EVIDENCE-ANALYST-R92@a05ab3f655a23eabd84c910ba337d64a948c168a`
- Independent Audit: `R8@6755579f5f21b19ca90788c948d8126529b648c6`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative evidence tags: 5 unchanged
- tag-form `formal/*`: empty
- tag-form `sealed/*`: empty
- tag-form `freeze/*`: empty
- H7 R5 exact head: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- candidate #34 frozen R1 execution contract base: `research/main-cand34-assembly-route-architecture-r90-cycle2@a6455a3929b86ad25fd106ea93a03604192fc3be`
- candidate #34 R1 prebinding: `research/main-cand34-assembly-route-preformal-r91-cycle3@2de73b9d0f21a2e8f07b43ca517b5247e6a7dfd0`
- candidate #34 prebind workflow: `35808210818` success
- PF-R1 existing artifact: workflow `35695286240`, artifact `10680620448`, digest `sha256:db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d`, unexpired
