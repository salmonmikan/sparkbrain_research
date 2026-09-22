# SparkBrain Methodology Calibration Audit — R68

- schema_version: `2`
- generation_id: `METHCAL-20260922T232000+0900-R68-9C4E7A31`
- produced_at: `2026-09-22T23:20:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- material_change_reason: `INDEPENDENT_AUDIT_R7_EXPOSES_TARGET_DERIVED_CORRECTNESS_BEFORE_IMMUTABLE_RAW_PRESERVATION;_R80_FAILS_CLOSED_PREIDENTITY_AND_REQUIRES_LITERAL_PREDICTION_RAW_GATE`

## Input generations and authoritative refs

- Prior methodology: `METHCAL-20260922T223100+0900-R67-E5A19C42`, branch `ops/methodology-calibration-audit@3bad5b3113a7645b1d6c30cb2b105548ea691f14`.
- Human process directive: `HUMAN-20260922-005` (process directive, not scientific evidence).
- Control: `CTRL-20260922T214728+0900-R36-C8F31D72`, `ops/control-brain-handoff@ba1c10f3e45d15fa72ce15170ad213b48a980f8e`.
- Evidence Analyst: `EVA-20260922T230224+0900-R80-6B8F31C4`, `ops/evidence-analyst-handoff@88f72d4e55d30e561143df94e06ce10c91972104`.
- Independent Audit: `AUD-20260922T223000+0900-R7-H7-RAWGATE-6C8F21D4`, `ops/external-research-audit-handoff@d1e2ffe278a8af40b0b61250aeba8dbd8da8cbd1`.
- Stable scientific source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` remains exactly five refs; tag-form `formal/*`, `sealed/*`, `freeze/*` remain empty.
- Active H7 R3 preidentity development ref: `research/main-h7-formal-r3-unexposed-eval-runtime-r76-cycle9@325e93c62c1f79baa107b677a3dc881dc6f47ace`.
- R2 quarantined development history: `research/main-h7-formal-r2-input-split-r75-cycle8@a7a3c82416af5bd3c8bf3340cc9276f161ddb0d0`.

`ops/*` is treated only as mailbox/history/authority context. Scientific facts below were independently reconstructed from stable `main`, exact research refs, exact source files, and current evidence namespaces.

## Material finding

The new material calibration finding is stricter than the prior R67 holdout-secrecy finding. H7 R1/R2 achieved byte-ordering in which a `raw` artifact is closed before the later scorer runs, but the object called `TargetBlindRawCollector` is not semantically target-blind. The R2 result runner derives `baseline_correct` and `cut_correct` by comparing model/comparator outputs with `belief_truth` before the raw collector is closed. The later scorer then consumes those target-relative correctness bits. Therefore the preserved object is decision-blind, but it is already target-derived and score-sufficient.

This matters because a post-preserve scorer cannot independently recompute or audit whether correctness was derived faithfully from the underlying predictions and protected targets. `raw-before-score` must therefore mean both: (1) immutable preservation occurs before the scorer reads the raw artifact, and (2) the preserved raw is prediction/output/intervention data plus opaque identity metadata, not correctness/effect/decision fields already derived using protected target material.

Independent Audit R7 discovered this before any H7 FORMAL identity, STARTED marker, protected evaluation, official scoring, scientific preserve, or evidence ref existed. Evidence Analyst R80 then failed closed: fresh FORMAL authority remains zero; R3 may only implement the already-fixed `target_blind_raw=true`, `raw_before_score=true`, and `preserve_before_read=true` intent using a literal prediction-raw allowlist, target-sidecar independence tests, and scorer-side recomputation after immutable preservation. No R2 in-place repair is authorized.

This is not a reason to relax development. The R3 contract already fixed literal target-blind raw as part of the intended one-way integrity design. Implementing prediction-only raw faithfully is therefore `SCIENCE_INVARIANT_REPAIR` so long as metric/scorer mathematics, bootstrap/decision semantics, target definition, seed/exclusion policy, comparator, intervention, thresholds/tolerances, resource contract, claim, falsifier, sample size, or world distribution do not change. If any such field must change, STOP and version a science-affecting revision prospectively.

## Gate-by-gate classification

| Material gate | Classification | Finding |
|---|---|---|
| hard FORMAL integrity floor | `KEEP` | No fresh identity consumed; historical evidence untouched. |
| orthogonal development-phase axis | `KEEP` | R3 remains `RESULT_EXPOSED_DEVELOPMENT`, fresh FORMAL remains unconsumed. |
| full OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live path | `INSUFFICIENT_EVIDENCE` | No fresh post-directive H7 FORMAL identity/result exists yet. |
| OPEN bounded development iteration | `KEEP` | Development remains allowed with provenance. |
| RESULT_EXPOSED same-object invariant repair | `KEEP` | Faithful implementation of already-fixed R3 raw intent may be repaired same-object. |
| post-result science-affecting change | `KEEP` | Must remain explicit version/fresh successor; no in-place R2 rewrite. |
| cycle 3 as automatic terminal cap | `RELAX` | H7 has progressed beyond cycle 3 on prospectively stated information gain. |
| cycle 3 as mandatory reassessment | `KEEP` | Current behavior remains calibrated. |
| raw-before-score as file/write ordering only | `CLARIFY` | Byte ordering alone is insufficient. |
| literal target-blind prediction raw | `TIGHTEN` | No target/truth/correctness/effect/decision fields before immutable preserve. |
| scorer-side recomputation from preserved raw + protected target sidecar | `TIGHTEN` | Required for independent auditability. |
| target-sidecar independence/data-flow test | `TIGHTEN` | Changing target sidecar must not alter prediction-raw bytes for fixed observations. |
| preserve-before-read / immutable evidence path | `TIGHTEN` | Must apply to prediction raw before scorer or claim-capable process gets protected target material. |
| concealed/unexposed evaluation surface | `TIGHTEN` | R2 stays quarantined; R3 concealed post-binding surface remains required. |
| exact source/protocol/package/runtime/input/evaluator binding | `TIGHTEN` | Must be complete before one-way authority. |
| repeated development observations ≠ independent evidence | `KEEP` | PF-R1 remains one nonconfirmatory observation; confirmatory count stays zero. |
| repeated result-bearing PRE_FORMAL rerun/retune live case | `INSUFFICIENT_EVIDENCE` | Still not sufficiently stress-tested. |
| durable RESULT_EXPOSED development bytes | `TIGHTEN` | PF-R1 exact-byte preservation remains outstanding; no rerun/rescore substitute. |
| PRE_FORMAL as real development surface | `KEEP` | Iteration is permitted without confirmatory credit. |
| preformal_eligible distinct from READY | `KEEP` | Distinction remains live. |
| READY = informative next test, not prior victory | `KEEP` | `HIDDEN_SECOND_FORMAL_GATE=false`. |
| current-object claim ceiling | `KEEP` | Claim ceilings remain object-specific. |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` | No laundering observed. |
| fresh terminal SYSTEM successor discipline | `KEEP` | Candidate 33 remains SYSTEM-only. |
| fresh SYSTEM→MECHANISM successor admission | `INSUFFICIENT_EVIDENCE` | No genuine live case yet. |
| TERMINAL_FOR_CURRENT_OBJECT scope | `KEEP` | Candidate 33 may close its bounded SYSTEM object without topic death. |
| classification-completeness gating | `KEEP` | R80 reports 33/33 classified. |
| MAIN MECHANISM priority | `KEEP` | H7 remains MAIN scientific priority. |
| prospective SYSTEM priority exception | `KEEP` | No comparable-MECHANISM override observed. |
| genuine SYSTEM-over-MECHANISM exception | `INSUFFICIENT_EVIDENCE` | Still unobserved. |
| theory-backward quality floor / no-target liveness | `KEEP` | No-target remains non-evidentiary and no candidate is manufactured to fill activity. |
| protected/adaptive-evaluation validity | `TIGHTEN` | Protection requires both information-level non-exposure and semantically raw pre-score preservation. |

## Mandatory questions

1. Development-phase semantics are consistent through R3 preidentity closure, but not yet proven end-to-end through a fresh `CONSUMED_ONE_WAY` result.
2. Cycle 3 is not being treated as a hard terminal cap. H7 continues only where an explicit information-gain question remains.
3. Repair classification is currently calibrated: literal prediction-raw implementation is invariant only because R3 already fixes target-blind raw as scientific intent; any metric/target/comparator/threshold/resource/claim change remains science-affecting and must version.
4. No development rerun/retune/tolerance laundering into independent evidence is observed. The repeated result-bearing PRE_FORMAL stress case remains insufficiently observed.
5. RESULT_EXPOSED lineage is preserved semantically across R1/R2/R3. PF-R1 exact raw/summary byte durability remains an open provenance gap, so preservation is not yet fully satisfactory.
6. FORMAL one-way integrity is unchanged: stable main/evidence refs are unchanged, fresh authority is zero, and no H7 identity/STARTED/result has been consumed.
7. No fresh SYSTEM→MECHANISM successor has yet been demonstrated. Candidate 33 is a legitimate fresh SYSTEM successor and remains SYSTEM; no rescue uplift is observed.
8. PRE_FORMAL behaves as development, not hidden FORMAL. READY does not require prior comparator/reduction/falsifier victory.
9. Terminal/supply controls are mostly calibrated. R80 canonicalizes candidate 33 current object terminal without MECHANISM uplift or automatic successor manufacture. Mechanism supply remains thin.
10. PASS remains realistically reachable without weakening standards, but only after R3 closes literal prediction-raw preservation, post-preserve scorer recomputation, concealed fresh evaluation identity, exact bindings, no-clobber/collision gates, and PF-R1 durable development provenance.

## Risks and calibration

False-positive risk is `MODERATE_WATCH`. The main risk is not merely public/reconstructible R2 targets; it is that target-derived correctness bits could be mistaken for target-blind raw and thereby hide evaluator/scorer coupling before immutable preservation. If consumed, that would make a positive result less independently auditable.

False-negative/opportunity-cost risk remains `MODERATE_WATCH`: the quality floor is intact, but viable MECHANISM supply is effectively one H7 lineage. Over-terminalization is `LOW_TO_MODERATE_WATCH_IMPROVING`; candidate 33 closes only its bounded SYSTEM architecture question and does not kill the topic family. Moving-goalpost/rescue risk is `LOW_TO_MODERATE_WATCH`: R2 is quarantined, R3 is explicit and prospective, and no in-place post-result scientific rewrite is authorized.

## Funnel / mechanism supply / claim-type findings

R80 canonical state is `33 = MECHANISM 13 / SYSTEM 20`, classification completeness `33/33`, lifecycle `ACTIVE=1 / NONTERMINAL_HOLD=0 / TERMINAL_FOR_CURRENT_OBJECT=32`, development phases `OPEN_DEVELOPMENT=2 / RESULT_EXPOSED_DEVELOPMENT=31 / canonical CONSUMED_ONE_WAY=0`, with `7` historical official consumed scientific identities in a separate one-way lineage. PRE_FORMAL is eligible/READY `1/1`; fresh FORMAL authority is `0`.

Candidate 7/H7 remains `MECHANISM / FORMALIZE / READY / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`. Candidate 33 is `SYSTEM / RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`; its completed bounded auditability/reachability question does not support semantic equivalence or MECHANISM uplift. SYSTEM-terminal successor accounting remains one realized fresh SYSTEM successor, zero fresh MECHANISM successors. Mechanism supply is therefore `ONE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_THIN`.

## Prospective recommendations

Keep R1/R2/PF-R1 historical development artifacts unchanged. Keep R2 quarantined. On R3, implement a positive allowlist whose pre-preserve artifact contains only model/comparator predictions or output distributions, intervention metadata, and opaque row identifiers needed for deterministic joins; exclude target/truth/correctness/effect/decision fields. Immutable-preserve those exact bytes first. Only a separate fixed scorer may then receive the protected target mapping and recompute correctness/effect/decision from preserved raw. Add a target-sidecar independence test and fail closed if scorer semantics or any scientific field would need to change.

Do not create evaluation commitment, FORMAL identity, STARTED marker, protected evaluation, official scoring, or scientific evidence until a fresh Analyst reviews green preidentity closure and separately authorizes one-way consumption. Complete the existing PF-R1 exact-byte preservation request without rerunning PF-R1. Candidate 33 should remain closed only for its current SYSTEM object, with no automatic successor creation.

## Utility request

No new Utility request. The existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the relevant bounded request and is not observed completed.

## Hard-floor confirmation, confidence, and questions for Control/Analyst

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence is `HIGH` for the R1/R2 target-derived-raw finding, current fail-closed preidentity state, and unchanged one-way evidence refs; `MEDIUM_HIGH` for R3 closure classification because implementation is not yet complete; `UNOBSERVED` for a fresh post-directive consumed-FORMAL end-to-end case and a genuine fresh SYSTEM→MECHANISM successor.

Questions to be resolved by future Control/Analyst state, without changing criteria here: whether R3's final raw allowlist excludes all target-derived fields; whether immutable preserve is provably upstream of any target access/scorer process; whether target-sidecar independence is tested; whether exact runner/scorer/preserver/runtime/package/input/evaluator bindings are frozen before commitment/identity; whether PF-R1 exact bytes are durably preserved; and whether any future SYSTEM→MECHANISM successor fixes an independently motivated residual plus fresh reduction/comparator/falsifier contract before admission.
