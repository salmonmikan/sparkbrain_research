# SparkBrain Methodology Calibration Audit — 2026-09-22 15:21 JST

schema_version: `2`  
generation_id: `METHCAL-20260922T152143+0900-R60-B7E4C219`  
produced_at: `2026-09-22T15:21:43+09:00`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260922T132125+0900-R59-F4C7A21D`

## Result

`MATERIAL_CALIBRATION_UPDATE`

Overall classification remains **`MIXED_CALIBRATION`**.

Prior Methodology R59 was read first. Stable repository/evidence were then independently refreshed before current designated Control/Analyst history; only afterward was the current MAIN mailbox consulted. Stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` is still exactly five tag objects; tag-form `formal/*=0`, `sealed/*=0`, `freeze/*=0`. `ops/*` was treated only as control/history/mailbox material, not scientific source of truth.

The material update is the **first canonical READY -> PRE_FORMAL transition under HUMAN-20260922-005**. Evidence Analyst R64 completed H7 DEV-R2 implementation/conformance without scientific outcome exposure in that cycle and prospectively promoted candidate 7 to `PRE_FORMAL`, `preformal_eligible=true`, `preformal_readiness.status=READY` under versioned revision `H7-PF-R1-FROZEN-PANEL-DEVELOPMENT-EVALUATION`. R64 explicitly states that READY is justified because the next test is well-defined and informative **without requiring H7 already to defeat its reductions or survive its falsifier**. This is the strongest live evidence so far that READY is development readiness rather than a hidden second FORMAL gate.

The transition also validates the cycle policy. H7 was not terminalized at cycle 3: the cycle-3 reassessment versioned the underspecified comparator protocol into DEV-R2, DEV-R2 then completed implementation/conformance, and R64 advanced the same MECHANISM object to a fixed cycle-4 PRE_FORMAL development evaluation. `cycle3_as_automatic_terminal_cap` therefore remains `RELAX`; `cycle3_mandatory_reassessment_with_prospective_information_gain=KEEP`.

A second important positive signal is that versioning does **not** erase exposure state. H7 remains `RESULT_EXPOSED_DEVELOPMENT` while moving from DEV-R2 to PF-R1. This is calibrated: same-object versioning does not reset the lineage to `OPEN_DEVELOPMENT` and thereby launder prior exposure. R64 requires any science-affecting redesign after meaningful result exposure to use explicit versioning or a fresh successor while preserving the prior result unchanged.

The first PRE_FORMAL run is not yet an observed result. At audit cutoff the MAIN mailbox had only acquired the R64 H7 PF-R1 cycle-4 lease; no completed result report was available. Accordingly, actual iterative PRE_FORMAL rerun/retune behavior, non-independent evidence accounting across repeated result-bearing PRE_FORMAL observations, and the first science-affecting revision **after** a meaningful PF result all remain `INSUFFICIENT_EVIDENCE`. Lease acquisition must not be treated as result exposure.

## Gate classifications

- hard FORMAL integrity floor: `KEEP`
- development-phase axis on active path: `KEEP`
- full end-to-end development rollout: `INSUFFICIENT_EVIDENCE`
- result-exposure phase persistence across same-object versioning: **`KEEP`**
- same-object `SCIENCE_INVARIANT_REPAIR`: `KEEP`
- science-affecting change -> versioned revision/fresh successor preserving prior results: `KEEP`
- post-meaningful-result science-affecting revision live case: `INSUFFICIENT_EVIDENCE`
- cycle 3 as automatic terminal cap: **`RELAX`**
- cycle 3 mandatory reassessment: `KEEP`
- first READY -> PRE_FORMAL development semantics: **`KEEP`**
- READY = well-defined/informative next test, not prior success: **`KEEP`**
- `preformal_eligible` distinct from READY: `KEEP`
- PRE_FORMAL as real development surface: `KEEP`
- PRE_FORMAL allocation without prior comparator/reduction/falsifier victory: **`KEEP`**
- live iterative PRE_FORMAL execution: `INSUFFICIENT_EVIDENCE`
- repeated PRE_FORMAL observations not independent confirmatory evidence: `KEEP`
- current-object `claim_ceiling`: `KEEP`
- same-object SYSTEM -> MECHANISM uplift ban: `KEEP`
- fresh SYSTEM -> MECHANISM successor admission: `INSUFFICIENT_EVIDENCE`
- `TERMINAL_FOR_CURRENT_OBJECT` closes current object, not topic: `KEEP`
- terminal-topic fresh-successor question formation: **`KEEP`**
- classification-completeness gating: `KEEP`
- MAIN MECHANISM priority / prospective SYSTEM exception: `KEEP`
- theory-backward quality floor / `NO_COHERENT_MECHANISM_TARGET`: `KEEP`
- comparator-equivalence verifier independence: `TIGHTEN`
- raw-before-score / preserve-before-read execution plumbing: `TIGHTEN`
- protected/adaptive-evaluation validity and exposure observability: `TIGHTEN`

`HIDDEN_SECOND_FORMAL_GATE=false`.

## Development-iteration calibration

HUMAN-20260922-005 is being implemented consistently through the READY allocation path. Control R33 had already made the development phase orthogonal to Funnel/lifecycle; R64 preserves that separation at PRE_FORMAL. H7 is simultaneously `MECHANISM / PRE_FORMAL / ACTIVE / eligible / READY` and `RESULT_EXPOSED_DEVELOPMENT`.

R64's PF-R1 authority is explicitly fixed-endpoint and nonconfirmatory. It permits only the already-fixed fit/calibration/discriminator sequence and endpoints, then requires STOP for fresh Analyst review. New comparator, intervention, metric, seed/split, threshold/tolerance, resource/privilege, claim, falsifier or success-rule choices require explicit versioned reassessment; mechanical lint/import/build/path/serialization/logging/hash fixes remain science-invariant. This is calibrated against rescue tuning while still allowing real development.

The strongest remaining test is the first completed PF-R1 result. If a meaningful result is exposed and a science-affecting change follows, the programme must preserve the exact prior raw/result/contract, keep the lineage `RESULT_EXPOSED_DEVELOPMENT`, version before any new execution, and keep all repeated PRE_FORMAL observations nonconfirmatory.

## Terminal / successor calibration

Canonical candidate 32 remains terminal and is not reopened. R64 nevertheless retains a noncanonical question-formation seed asking whether a **fresh future SYSTEM successor** could close the raw->digest/provenance boundary. It explicitly gives the proposed successor a SYSTEM ceiling, keeps PRE_FORMAL eligibility false, and requires later fresh Analyst admission. This is useful evidence that `TERMINAL_FOR_CURRENT_OBJECT` is not being treated as automatic topic death while same-object rescue laundering remains blocked. A genuine fresh SYSTEM -> MECHANISM successor admission is still unobserved.

The previous `NO_COHERENT_MECHANISM_TARGET` episode remains closed at canonical liveness count 23 for the active H7 revision and is not evidence that mechanisms do not exist.

## Funnel / risks

Canonical population remains **32 = MECHANISM 13 / SYSTEM 19**, classification completeness **32/32**. Lifecycle is `ACTIVE=1 / TERMINAL_FOR_CURRENT_OBJECT=31`. Architecture active/queued is now `0/0`; PRE_FORMAL has `eligible=1`, `READY=1`, and one prospectively allocated active MECHANISM. Fresh FORMAL authority remains `0`. Development phases remain `OPEN_DEVELOPMENT=2 / RESULT_EXPOSED_DEVELOPMENT=30 / canonical CONSUMED_ONE_WAY=0`, with seven official consumed scientific identities tracked separately and immutable.

Mechanism supply health improves to **`RECOVERING_BUT_THIN_SINGLE_READY_MECHANISM_WITH_QUALITY_FLOOR_INTACT`**. False-positive risk remains **`LOW_TO_MODERATE_WATCH`**. False-negative/opportunity-cost risk is **`MODERATE_WATCH_IMPROVING`**. Moving-goalpost/rescue risk is **`LOW_TO_MODERATE_WATCH`**. Over-terminalization risk is **`MODERATE_WATCH_IMPROVING`**.

## PASS reachability

PASS is realistically reachable without weakening evidence standards. This run gives the first live evidence that an object can move through versioned development into READY/PRE_FORMAL without already having won its scientific test. PF-R1 remains nonconfirmatory development. Clean confirmation still requires a fresh `CONSUMED_ONE_WAY` FORMAL identity with a prospective frozen protocol, raw-before-score, preserve-before-read, exact source/protocol/package/runtime/input binding, immutable evidence, and a valid protected/adaptive-evaluation regime.

## Prospective recommendations

At the first completed PF-R1 result, persist exact development-result refs, revision/contract/runtime/input binding, exposure state and `NONCONFIRMATORY` status before any redesign. If a science-affecting change is then proposed, preserve the prior raw/result/contract and version or create a fresh successor **before** any new run; do not reset the same lineage from `RESULT_EXPOSED_DEVELOPMENT` to `OPEN_DEVELOPMENT`. Keep PRE_FORMAL run count separate from confirmatory-evidence count, which remains zero until a fresh one-way FORMAL identity. Continue allowing terminal SYSTEM topics to generate fresh successor questions, but require a new candidate ID and fresh reduction/comparator/falsifier contract.

No Utility request was created; the live H7 PF-R1 rollout is the higher-information calibration path. Hard floor remains **`CONFIRMED / DO NOT RELAX`**.

Questions for Control/Analyst to resolve through future observable state: whether the first completed PF-R1 result is durably linked before any redesign; whether repeated PRE_FORMAL attempts remain one nonconfirmatory lineage; and whether any future successor from a terminal SYSTEM family receives a new candidate ID and fresh scientific contract.

Confidence is **`HIGH`** for development calibration through READY/PRE_FORMAL allocation and **`MEDIUM_LOW`** for completed iterative PRE_FORMAL/post-result revision behavior because those cases have not yet occurred.
