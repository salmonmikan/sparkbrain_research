# SparkBrain Methodology Calibration Audit — R69

- schema_version: `2`
- generation_id: `METHCAL-20260923T002000+0900-R69-7D2B4C91`
- produced_at: `2026-09-23T00:20:00+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`
- material_change: `true`
- material_change_reason: `H7_R3_FAILS_CLOSED_ON_LITERAL_PACKAGE_BINDING;_R81_VERSIONS_R4_AND_REVEALS_NEED_TO_SEPARATE_CLAIM_CAPABLE_SCIENTIFIC_RUNTIME_LOCK_FROM_BROAD_DEV_TOOLING_ENVIRONMENT`

## Input generations and authoritative refs

- Prior methodology: `METHCAL-20260922T232000+0900-R68-9C4E7A31`, `ops/methodology-calibration-audit@0ffa61f19ce874bfb55dc25c9918ae293528e6dd`.
- Human process directive: `HUMAN-20260922-005` (process directive, not scientific evidence).
- Control: `CTRL-20260922T235000+0900-R37-7A3E9C51`, `ops/control-brain-handoff@23676a55c9473d1cfd22d982ffffd5d2ba18b557`.
- Evidence Analyst: `EVA-20260923T001221+0900-R81-4885D9DE`, `ops/evidence-analyst-handoff@725aff8a8a5f4105d85cc1893036ef4c48f893c4`.
- Independent Audit prior: `AUD-20260922T223000+0900-R7-H7-RAWGATE-6C8F21D4@d1e2ffe278a8af40b0b61250aeba8dbd8da8cbd1`.
- Stable scientific source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` remains exactly five refs; tag-form `formal/*`, `sealed/*`, `freeze/*` remain empty.
- Current H7 R3 research ref: `research/main-h7-formal-r3-unexposed-eval-runtime-r76-cycle9@f0780f2f91779a8bd1a1d09eb535921d0d48f7d4`.
- R4: prospectively authorized by R81, not yet materialized as a research branch at audit time.

`ops/*` is mailbox/history/authority context only. Repository refs, exact source files, workflow state, artifact bytes and evidence namespaces were independently re-fetched.

## Material finding

H7 R3 now provides a useful calibration case for the boundary between rigorous exact runtime binding and over-conservative environment overbinding. The exact non-result-bearing R3 preidentity workflow at `f0780f2...` passes package installation, R3 tests and lint, then fails closed in `Build non-result R3 integrity closure`. The uploaded runtime observation differs from the frozen runtime binding only in `pip_freeze_sha256` (and therefore the aggregate runtime-observation hash); Python, OS, runner image, Torch version/build/git/distribution hash, CPU contract, thread settings and deterministic-algorithm flag match.

The failed run observed `pip_freeze_sha256=b4c2c84a...`; the frozen binding expected `25b4a1c5...`. The R3 builder hashes literal `python -m pip freeze --all` output, but the workflow installs broad extras `.[dev,learned,spiking]`. `pyproject.toml` shows the `dev` extra includes pytest, ruff, jsonschema, FastAPI, uvicorn and httpx in addition to the scientific learned/spiking packages. The former successful freeze manifest bytes were not persisted, only their digest. Therefore a same-object silent rebind cannot prove exact package equivalence, and R81 correctly fails closed and versions a prospective R4 resource/package contract rather than normalizing or retrying until a desired hash appears.

The calibration implication is two-sided. Exact package/runtime binding remains a hard requirement for claim-capable execution, but the *scientific identity surface* should bind the exact packages/artifacts that can affect the protected runner/scorer/preserver/resource semantics. Development/lint tooling should be logged and reproducible for engineering provenance, but should not automatically become scientific identity solely because the preidentity workflow happens to install it. Binding the entire mutable `pip freeze --all` development environment as a scientific contract creates avoidable false-negative churn without increasing scientific protection. R81's R4 instruction to persist exact lock bytes, bind third-party distributions/artifact hashes prospectively, separate repository source identity, and keep development/lint tooling outside the protected scientific runtime unless explicitly required is well calibrated.

This is also a positive HUMAN-005 case. H7 is already `RESULT_EXPOSED_DEVELOPMENT`; when exact resource binding could no longer be proven, the programme did not silently repair R3. R81 explicitly versions `H7-FORMAL-R4-REPRODUCIBLE-RUNTIME-PACKAGE-LOCK-AND-PREIDENTITY-REVALIDATION`, preserves R3 unchanged, and keeps fresh FORMAL authority at zero. Cycle 10 has prospectively stated information gain: close a reproducible scientific-resource contract before any one-way identity.

## Gate-by-gate classification

| Material gate | Classification | Finding |
|---|---|---|
| hard FORMAL integrity floor | `KEEP` | No fresh identity/result; historical evidence refs unchanged. |
| orthogonal development-phase axis | `KEEP` | H7 remains RESULT_EXPOSED development; R4 is prospective preidentity only. |
| full OPEN→RESULT_EXPOSED→CONSUMED_ONE_WAY live path | `INSUFFICIENT_EVIDENCE` | Fresh post-directive consumed FORMAL still unobserved. |
| OPEN bounded development iteration | `KEEP` | Iteration remains allowed before one-way consumption. |
| RESULT_EXPOSED same-object invariant repair | `KEEP` | Mechanical repair after a fixed R4 lock may remain same-object. |
| post-result science-affecting change → version/fresh successor | `KEEP` | R81 versions package/resource contract change to R4 rather than rebinding R3. |
| H7 R3 silent package hash rebind/normalization | `KEEP` | Correctly forbidden. |
| R4 versioned scientific-runtime resource closure | `KEEP` | Prospectively bounded to package/runtime binding only. |
| digest-only package binding without exact manifest/lock bytes | `TIGHTEN` | Digest is insufficient when later exact-equivalence must be audited. |
| repeated mutable resolver attempts until a matching hash appears | `TIGHTEN` | Must not be used as a repair strategy. |
| claim-capable scientific runtime/package exact binding | `KEEP` | Exact lock/artifact hashes remain required before one-way identity. |
| whole dev/lint environment as scientific identity | `SPLIT_BY_CLAIM_TYPE` | Claim-capable packages/resources are hard-bound; unrelated dev tooling is engineering provenance, not automatically scientific identity. |
| repository source identity via editable-project freeze entry | `CLARIFY` | Source commit/blob must be bound separately from third-party package lock. |
| cycle 3 as automatic terminal cap | `RELAX` | H7 cycle 10 is allowed because new information gain remains. |
| cycle 3 as mandatory reassessment | `KEEP` | Current continuation is prospectively justified. |
| raw-before-score as file/write ordering only | `CLARIFY` | R68 finding unchanged. |
| literal target-blind prediction raw | `TIGHTEN` | R3 implementation closure remains required. |
| scorer-side recomputation after immutable preserve | `TIGHTEN` | Remains required. |
| target-sidecar independence | `TIGHTEN` | Remains required. |
| preserve-before-read / immutable FORMAL evidence path | `TIGHTEN` | Remains required. |
| concealed/unexposed evaluation surface | `TIGHTEN` | R2 remains quarantined; R3/R4 must retain concealed post-binding surface. |
| repeated development observations ≠ independent evidence | `KEEP` | Non-result preidentity reruns have zero evidentiary credit. |
| repeated result-bearing PRE_FORMAL rerun/retune live case | `INSUFFICIENT_EVIDENCE` | Still not adequately stress-tested. |
| durable RESULT_EXPOSED development bytes | `TIGHTEN` | PF-R1 exact-byte preservation remains outstanding. |
| PRE_FORMAL as real development surface | `KEEP` | Development tuning remains permitted without confirmatory credit. |
| preformal_eligible distinct from READY | `KEEP` | Distinction remains live. |
| READY = informative next test, not prior victory | `KEEP` | `HIDDEN_SECOND_FORMAL_GATE=false`. |
| current-object claim ceiling | `KEEP` | Object-specific ceiling remains enforced. |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` | No laundering observed. |
| fresh terminal SYSTEM successor discipline | `KEEP` | Candidate 33 remains SYSTEM-only and current-object terminal. |
| fresh SYSTEM→MECHANISM successor admission | `INSUFFICIENT_EVIDENCE` | Genuine live case still absent. |
| TERMINAL_FOR_CURRENT_OBJECT scope | `KEEP` | Topic death is not implied. |
| classification-completeness gating | `KEEP` | R81 retains 33/33 classified. |
| MAIN MECHANISM priority | `KEEP` | H7 remains the sole viable canonical MECHANISM lane. |
| prospective SYSTEM priority exception | `KEEP` | No comparable-MECHANISM override observed. |
| genuine SYSTEM-over-MECHANISM exception | `INSUFFICIENT_EVIDENCE` | Still unobserved. |
| theory-backward quality floor / no-target liveness | `KEEP` | No candidate manufacture to maintain activity. |
| protected/adaptive-evaluation validity | `TIGHTEN` | Prior R67/R68 exposure/raw findings remain unresolved preidentity gates. |

## Mandatory questions

1. Development-phase semantics are consistent through R4 authorization, but not yet proven through a fresh `CONSUMED_ONE_WAY` result.
2. Cycle 3 is not a hard terminal cap. H7 has reached cycle 10 only through explicit reassessments with new information gain.
3. Repair classification is currently calibrated: inability to prove equivalence of a scientific package/resource binding is treated as science-affecting and versioned; purely mechanical closure after a fixed lock remains invariant.
4. No rerun/retune/tolerance laundering into independent evidence is observed. Non-result preidentity workflow attempts are not evidence. R81 additionally forbids repeated package resolution until a preferred hash appears.
5. RESULT_EXPOSED lineage is preserved: R3 remains unchanged and R4 is additive. PF-R1 exact raw/summary byte durability remains the open preservation gap.
6. FORMAL one-way integrity is unchanged. Main/evidence refs are unchanged, tag-form formal/sealed/freeze remain empty, and H7 has no FORMAL identity/STARTED/result.
7. No genuine fresh SYSTEM→MECHANISM successor exists yet. Candidate 33 remains a legitimate SYSTEM successor without uplift.
8. PRE_FORMAL remains development, not hidden FORMAL. READY is development readiness only.
9. Terminal semantics remain calibrated, but mechanism supply remains thin: one active H7 lineage, 32 current-object terminals.
10. PASS remains realistically reachable without lowering standards. R4 should make the protected scientific runtime reproducible by construction rather than by matching an opaque digest from a mutable broad development environment.

## Risks and calibration

False-positive risk remains `MODERATE_WATCH`, driven mainly by the unresolved concealed-evaluation and semantic raw-preservation gates discovered in R67/R68. The new package mismatch itself is a fail-closed preidentity defect, not evidence contamination.

False-negative/opportunity-cost risk remains `MODERATE_WATCH`, with a newly concrete sub-risk: overbinding unrelated dev/lint packages into the scientific identity can cause spurious version churn and unnecessary blockage. R81's R4 split reduces this risk without weakening exact scientific runtime binding.

Moving-goalpost/rescue risk is `LOW_TO_MODERATE_WATCH_IMPROVING`: R3 is preserved, R4 is explicit and prospective, and resolver/hash shopping is forbidden. Over-terminalization remains `LOW_TO_MODERATE_WATCH_IMPROVING`.

## Funnel / mechanism supply / claim-type findings

R81 canonical state remains `33 = MECHANISM 13 / SYSTEM 20`, classification completeness `33/33`, lifecycle `ACTIVE=1 / NONTERMINAL_HOLD=0 / TERMINAL_FOR_CURRENT_OBJECT=32`, development phases `OPEN_DEVELOPMENT=2 / RESULT_EXPOSED_DEVELOPMENT=31 / canonical CONSUMED_ONE_WAY=0`, PRE_FORMAL eligible/READY `1/1`, fresh FORMAL authority `0`, with `7` historical official consumed identities in a separate one-way lineage.

Candidate 7/H7 remains `MECHANISM / FORMALIZE / READY(development-only) / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`; R4 is authorized preidentity-only and not yet materialized at audit time. Candidate 33 remains `SYSTEM / RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED` with no semantic-equivalence or MECHANISM claim. Mechanism supply remains `ONE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_THIN`.

## Prospective recommendations

Keep R3 unchanged. Materialize R4 only as a new versioned development revision. Persist the exact scientific-runtime lock/manifest bytes themselves, plus artifact hashes, before relying on their digest. Bind repository source separately by exact commit/blob. Define an explicit protected-runtime allowlist for claim-capable packages/resources; keep pytest/ruff/web tooling or other development-only packages out of the scientific identity unless they can affect the protected execution. Record development-tool versions separately for engineering reproducibility.

Run one non-result-bearing reproducibility validation against that prospectively fixed R4 lock. If it passes, STOP and return to a fresh Analyst before evaluation commitment or identity. If scientific package/resource/privilege scope must change after the lock is frozen, version again; do not silently edit R4. Preserve all R3 target-blind raw, target-sidecar, post-preserve scorer, concealed-evaluation, no-clobber and collision gates unchanged.

Complete the existing PF-R1 exact-byte preservation request without rerunning or reconstructing PF-R1.

## Utility request

No new Utility request. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains outstanding and its request branch has not advanced.

## Hard-floor confirmation, confidence, and questions for Control/Analyst

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence is `HIGH` that the R3 failure is a package-freeze binding mismatch with the rest of the recorded runtime fields matching, `HIGH` that one-way integrity remains unconsumed, `HIGH` that explicit R4 versioning is calibrated, and `MEDIUM_HIGH` on the exact future R4 scientific-runtime allowlist because it is not yet materialized. Fresh consumed-FORMAL end-to-end and fresh SYSTEM→MECHANISM successor remain `UNOBSERVED`.

Questions for future Control/Analyst state: whether R4's protected scientific package allowlist is explicit and excludes irrelevant development tooling; whether exact lock/manifest bytes and artifact hashes are durably persisted; whether repository source is bound independently from package metadata; whether the same frozen lock reproduces exactly without resolver shopping; whether all R68 target-blind/preserve gates remain unchanged; whether PF-R1 exact bytes are durably preserved; and whether any future SYSTEM→MECHANISM successor fixes an independently motivated residual plus fresh reduction/comparator/falsifier contract before admission.
