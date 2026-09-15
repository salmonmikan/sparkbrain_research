# SparkBrain Evidence Analyst — Latest Handoff

Analysis time: 2026-09-15 10:30 JST

## Evidence inspected

- `main` = `ba16bf10535141c2edb29bbe3439ba0a38e71179`
- A01 authoritative working frontier: `research/v061-a01-n3-adapter` = `97fb43cc76e878adcb9aad535b67c8b5cc1672ac`
- RV01 authoritative branch: `research/rv01-endogenous-transition` = `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- RV02 RD005 exact source branch: `research/rv02-rd005-source-binding-20260913` = `c60b7fd8d3889ee969f505d921e7d31c990871e6`
- CX01 candidate-002 prestart branch: `research/cx01-candidate-002-prestart` = `e8483968dfcb841982734630700cf1c8ed33de75`
- Open PRs at analysis time: none.
- R01-16 capability source freeze: `freeze/rv01-r01-16-capability-source-20260915` = `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- R01-16 capability preserve: `preserve/rv01-r01-16-capability-20260915` = `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- R01-16 canonical construction preserve: `preserve/rv01-r01-16-construction-census-34881254582` = `63cdf08edb438290e4a04f2fdb12d0cfdca0d6f8`
- R01-16 duplicate construction preserve: `preserve/rv01-r01-16-construction-census-34881331776` = `86679c9fd4560a441fca09f5bd61724ba40595da` (same consumed identity; never an independent replicate).
- RV02 RD005 D1 source freeze: `freeze/rv02-rd005-d1-source-20260913` = `c60b7fd8d3889ee969f505d921e7d31c990871e6`
- RV02 RD005 D1 exact preserve: `preserve/rv02-rd005-d1-96634541-20260914` = `d1fdd67ea197b879c52942c4a34e7d39a0a40698`
- CX01 candidate-002 source freeze: `freeze/cx01-candidate-002-source` = `b9ab9721f8a62b8a8d3bdf58b72dfb4b594c9fd6`
- CX01 candidate-002 exact formal preserve: `preserve/cx01-candidate-002-formal-34977997-20260911` = `6d45928827209cd763a2879494d85838df38b96f`
- A01 MD-001 preserve: `preserve/v061-a01-md-001` = `9aa6722004445bda6c5b95bd8858853d822da250`; exact launched source `e588abdbb7571e82c156b8e7b022fc2167be74af`.

This is the first durable Evidence Analyst handoff, so there is no prior analyst record to diff against. The newest scientific result in the repository is the R01-16 exposed-development capability run. No newer scientific execution was found after it. A provenance correction worth carrying forward: the exact RD005 D1 preserve is `preserve/rv02-rd005-d1-96634541-20260914`, not older shorthand/stale references used in some prior summaries.

## Scientific evidence vs readiness evidence

### A01 / MD-002

**Scientific baseline:** MD-001 is consumed and remains **UNRESOLVED / NOT_CLAIMABLE**. P1 passed. P2 numerically passed but was not claimable because the raw artifact/probe contract did not establish the required post-attribution shared-root competition. P3 only established the weaker native-control comparison; the intended stronger/third comparator was not validly bound. P4 was not run. P5 failed because provenance collapsed to binary evidence. No post-hoc repair of MD-001 is allowed.

**Current MD-002 readiness:** the current branch contains P2/P3/P4 construction work, but full MD-002 is not integrity-ready. The binding/status documents still leave exact component/runtime/package bindings incomplete. N3 remains genuinely unbound: the repository does not contain a qualifying old mature-library donor/control provenance chain for the required donor pair. That blocks a complete/formal MD-002 package, but it does **not** block a narrowly scoped, distinctly identified, development-only P2 capability measurement if that measurement is prospectively frozen before execution.

**Most valuable unresolved question:** does the P2 mechanism actually win/lose post-attribution competition for the same shared root, as opposed to merely showing forward architectural signals? The MD-002 supplemental already specifies the needed measurement family: occupied resource, post-attribution occupancy, missed-window, preemption-lost, and partition ownership at the earliest decisive cycle. The current `md002_p2_matrix_runner.py` validates/serializes a bound development matrix and explicitly leaves `capability_probe_scored=false`; it is not itself the missing shared-root execution probe.

Status: **UNRESOLVED; highest-value near-term measurement available.**

### RV01 / R01-16

**Scientific result:** the exposed-development capability identity `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af` is consumed. On 25 worlds / 100 eligible cells, the frozen classifier produced:
- Weight: **WEIGHT_SUPPORTED**, 100/100 support.
- Delay: **DELAY_MIXED**, 0 support / 54 negative / 46 discordant.
- Combined: **COMBINED_SUPPORTED**, 100/100 support.
- Held-out executions: 0; formal executions: 0; `formal_execution_allowed=false`.

Construction evidence showed weight contrasts at order-one scale while delay contrasts were exact-nonzero but extremely small. This scale separation is a useful mechanistic clue, but it must not be used to alter the consumed R01-16 classifier or thresholds.

**Integrity consequence:** no previously frozen downstream confirmatory identity was found. Any newly designed test informed by the Weight/Delay/Combined outcome must be labeled a **new exploratory/development successor**, not confirmatory. No `r01-17` prospective branch was found.

Status: **development evidence: Weight supported, Combined supported, Delay mixed; next successor must be distinct/exploratory.**

### RV02 / RD005

**Scientific/readiness result:** D1 is consumed. Exact preserve `preserve/rv02-rd005-d1-96634541-20260914` records a construction-only terminal failure: selected row is null, frozen decision matrix was not ready, blind reveal was not exercised, and scorer confirmed zero label access. Exact source was `c60b7fd8d3889ee969f505d921e7d31c990871e6`; construction identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; seed 92505; workflow run 34831458943.

The same identity must never be repaired/rerun. A distinct successor may diagnose why construction produced zero-ready while keeping blind identities sealed. No clear RD006 prospective successor branch was found.

Status: **terminal construction/readiness negative for D1; no blind scientific outcome revealed.**

### CX / CX01

**Scientific result:** candidate-002 is consumed and immutable **NEGATIVE**. Preserve `preserve/cx01-candidate-002-formal-34977997-20260911` records package SHA `2f18fe3b66eb61d29becf8251ce336e3ee20579fc39249492dd443458b127057`, 420 executions, 0 replay, and preregistered conditions C1–C7 all false. The strongest phi-space pattern was nonlocalized/high-overlap and did not satisfy metric support.

Never rerun or retune candidate-002. No candidate-003 prospective branch was found. Safe CX work is limited to diagnostics that do not reopen candidate-002, or a prospectively distinct new candidate.

Status: **NEGATIVE consumed formal identity; next candidate not yet near execution.**

## Consumed identities / no-rerun set relevant to current frontiers

- V061 A01 MD-001 — consumed; preserve `preserve/v061-a01-md-001`; do not repair/retest.
- RV01 R01-16 construction — `rv01-r01-16-development-7ed3a7532fc66ac8-87634d034204`; duplicate workflow 34881331776 is the same identity, not a replicate.
- RV01 R01-16 capability — `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`.
- RV02 RD005 D1 construction — `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`.
- CX01 candidate-002 formal — immutable negative; source/package/control/preserve refs above.
- Earlier R01/RV02/CX formal identities represented by freeze/preserve/control refs remain immutable even when not repeated in this short active-frontier list.

## Genuine blockers vs optional work

**Genuine:**
- A01 full MD-002 formal package: N3 provenance is still unbound; P3 stronger comparator, P4 replay recipe, P5 trial-level evidence, exact runtime/package/source sealing remain incomplete.
- A01 P2 measurement: actual post-attribution shared-root capability instrumentation must exist and be bound before execution; a serializer/forward-only architecture signal is insufficient.
- Any one-way run: distinct identity, remote collision/STARTED guard, exact source/runtime/package manifest, frozen scoring/thresholds, and no existing preserve/control claim.
- R01 successor: because R01-16 outcome is known, any newly designed successor is exploratory/development and must use new prospective identities/worlds; it cannot be presented as pre-outcome confirmation.
- RV02 successor: D1 is consumed; successor must be distinct and must not reveal blind labels during construction diagnostics.

**Optional / defer unless directly enabling measurement:**
- broad repository cleanup, stale branch deletion, documentation polish, generic registry refactors, or main integration not required for the next experiment.

## Ranked next actions

### 1. A01 MD-002 P2 post-attribution shared-root development probe — **Information: HIGH / Distance: NEAR–MODERATE**

Why #1: it directly attacks the key scientific weakness that made MD-001 P2 non-claimable, and the measurement contract was already described prospectively in the MD-002 supplemental. It can be kept development-only and scientifically separate from the still-blocked full MD-002 package/N3 work.

Minimum work: on a fresh prospective branch from the latest A01 head, implement/bind the real shared-root capability probe and its raw artifact path; freeze exact world/cloned-subepisode identities, arm semantics, reset/restore semantics, earliest-decisive-cycle observation window, resource instrumentation, budgets/thresholds, source/runtime/package manifest, and a distinct development identity. Add remote no-clobber/STARTED ownership before any one-way execution. Run tests/CI and substantive technical/semantic review; use the user-authorized human-review waiver only if literal human identity is the sole remaining gate.

### 2. A01 MD-002 P4 continuing-vs-reset lineage development discriminator — **Information: HIGH / Distance: MODERATE**

Why #2: MD-001 P4 was never executed, so this measures a genuinely unobserved discriminator rather than polishing an existing result. The old generated artifact is already bound, but the exact continuing-vs-reset replay recipe must be completed and frozen before execution. Treat it as its own development measurement unless/until the complete MD-002 formal package is prospectively sealed.

### 3. RV01 distinct exploratory delay-scale successor (R01-17 or equivalent new identity) — **Information: HIGH / Distance: MODERATE**

Why #3: R01-16 shows a sharp asymmetry (Weight supported, Delay mixed, Combined supported) and construction evidence suggests the delay perturbation is minute. A new prospective exploratory test can ask whether a scientifically meaningful delay perturbation changes the factorization behavior. It must use new worlds/seeds/identity and a newly frozen protocol. It must **not** be called confirmatory and must not retune/reuse R01-16.

Next outside top 3: RV02 distinct blinded construction diagnostic/successor to explain D1 zero-ready without reveal (**HIGH / MODERATE**). CX distinct next-candidate design is scientifically valid but currently farther from execution.

## GO / STOP criteria for recommendation #1

### GO only if all are true before output is observed

1. Re-fetch `research/v061-a01-n3-adapter` and confirm no newer prospective P2 branch/work supersedes this plan.
2. Bind exact P2 world source and cloned subepisodes; prove no collision with consumed/reserved identities.
3. Freeze the three P2 arm semantics exactly as the prospective MD-002 contract requires.
4. Freeze reset/restore semantics and the observation window.
5. Implement and bind **actual post-attribution shared-root competition instrumentation**: at minimum occupied resource, post-attribution occupancy, missed-window, preemption-lost, and partition ownership at the earliest decisive cycle. Forward architecture/state alone is not enough.
6. Freeze budgets, validity gates, thresholds/scoring before execution.
7. Create a distinct development identity and atomic remote STARTED/no-clobber claim; confirm no control/preserve ref already exists for it.
8. Freeze exact source/runtime/package manifest and pass relevant tests/CI.
9. Complete technical/semantic review; if the only remaining gate is literal independent-human identity, record `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE` / `HUMAN_REVIEW_WAIVED_BY_USER` rather than fabricating a reviewer.
10. Mark the run development-only: no held-out/formal scoring or opening.

### STOP if any are true

- The runner still only serializes precomputed/bound `world_data` or forward structure and does not execute the post-attribution shared-root competition.
- Reset/restore, resource ownership, observation timing, thresholds, or exact source/runtime/package are ambiguous at the one-way boundary.
- The proposed identity collides with any consumed/reserved identity or an existing STARTED/control/preserve ref.
- Remote head/diff moved after review; re-fetch and re-review before continuing.
- A newer worker has already implemented/executed the same prospective P2 identity.
- Any protocol/threshold choice is being changed in response to observed P2 output.

## Concurrency / staleness findings

- No open PRs were present at analysis time.
- No `ops/evidence-analyst-handoff` branch existed before this first handoff.
- No newer R01 successor, RV02 RD006, or CX candidate-003 prospective branch was found.
- Historical A01 P2/P3/P4 branches are behind `research/v061-a01-n3-adapter`; use current A01 head as the re-fetch starting point, not the older branch tips.
- Prior summaries that referenced an RD005 preserve without the construction-id suffix are stale; use `preserve/rv02-rd005-d1-96634541-20260914`.

## ORCHESTRATOR HANDOFF

Start with A01, not additional R01-16 post-processing. Re-fetch `research/v061-a01-n3-adapter` at `97fb43cc76e878adcb9aad535b67c8b5cc1672ac` (or its newer current tip) and verify no concurrent prospective P2 implementation already exists. Build the smallest scientifically real, development-only P2 shared-root capability probe that satisfies the already-written MD-002 contract; do not spend the run trying to solve N3 or full formal packaging unless that directly becomes necessary. Freeze identity/instrumentation/thresholds before any output, install atomic STARTED/no-clobber ownership, review/test, then execute exactly once only if all GO criteria above pass. If the P2 probe cannot be made integrity-ready in the run, pivot to the prospectively specified A01 P4 continuing-vs-reset discriminator rather than doing generic cleanup. Do not rerun R01-16, RD005 D1, CX01 candidate-002, or A01 MD-001.