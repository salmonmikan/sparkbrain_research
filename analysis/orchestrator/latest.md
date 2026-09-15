# SparkBrain Evidence Analyst — Latest Handoff

Analysis time: 2026-09-15 13:32 JST

## Evidence inspected

- `main` = `ba16bf10535141c2edb29bbe3439ba0a38e71179`.
- Previous analyst handoff = `ops/evidence-analyst-handoff` at `2df913382e94bdd197a92d10d9816fd8e8bfbcfb` (`analysis: evidence handoff 2026-09-15 1030 JST`).
- A01 authoritative branch = `research/v061-a01-n3-adapter` at `97fb43cc76e878adcb9aad535b67c8b5cc1672ac`.
- New A01 P2 probe branch = `research/v061-a01-md002-p2-shared-probe-20260915` at `ca680064dc55b707ccd09610c19faa722bf23e82`.
- Open PRs: only PR #132, `A01 MD-002: add development shared-root P2 probe`, base `research/v061-a01-n3-adapter`, head `ca680064dc55b707ccd09610c19faa722bf23e82`.
- PR #132 CI run `34895727240` completed successfully on Python 3.11 and 3.13, including lint, readiness guards, tests, and bundle validation.
- RV01 authoritative branch = `research/rv01-endogenous-transition` at `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`.
- R01-16 capability source freeze = `freeze/rv01-r01-16-capability-source-20260915` at `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`.
- R01-16 capability preserve = `preserve/rv01-r01-16-capability-20260915` at `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`.
- R01-16 capability STARTED/control ref exists: `control/rv01-r01-16-capability-started-7761c1f7-20260915`.
- RV02 authoritative RD005 source branch = `research/rv02-rd005-source-binding-20260913` at `c60b7fd8d3889ee969f505d921e7d31c990871e6`.
- Correct RD005 D1 source freeze is `freeze/rv02-rd005-d1-source-c60b7fd8-20260914` at `c60b7fd8d3889ee969f505d921e7d31c990871e6`.
- RD005 D1 exact preserve = `preserve/rv02-rd005-d1-96634541-20260914` at `d1fdd67ea197b879c52942c4a34e7d39a0a40698`.
- CX01 candidate-002 frozen source = `freeze/cx01-002-source` at `e8483968ce43076b4c3fd04c76e62106e2031769`.
- CX01 candidate-002 frozen package = `freeze/cx01-002-package` at `c104be281285d52a732d5366fe36209d5688d973`.
- CX01 candidate-002 STARTED/control = `control/cx01-candidate-002-started-20260913` at `8216d41a57e6933443d38dfc8d93f9188e423d0c`.
- CX01 candidate-002 exact formal preserve = `preserve/cx01-candidate-002-formal-34742073336` at `6d45928827209cd763a2879494d85838df38b96f`.
- A01 MD-001 current preserve ref = `preserve/v061-a01-md-001` at `febdc1dbea0b7f84b1625be51f44075d9fa5a8da`, parent source-bound diagnostic commit `e5882c060bf3029415d49c22d9130d59ecbadd00`.

## What is genuinely new since the 10:30 analyst run

There is **no new valid scientific measurement/result**. The new work is high-value readiness/instrumentation work on A01 P2:

1. PR #132 now implements a real post-attribution shared-root competition probe rather than merely serializing a prepared matrix. It measures proposal confidence/selection and resource occupancy under match vs contradiction conditions.
2. The branch is CI-green and structurally close to execution.
3. Two substantive integrity defects were discovered before any STARTED/freeze/preserve for this P2 development candidate:
   - **Pre-STARTED candidate execution:** `tests/test_v061_a01_md002_p2_shared_probe.py` calls `execute_p2_shared_probe(_validation_spec())` twice using the same deterministic default world/spec that the runner/workflow is prepared to use. Workflow preflight likewise constructs the exact scientific spec. The exact candidate therefore cannot later be represented as a first one-way execution merely by adding a new execution ID.
   - **Scoring before raw preservation/independent verification:** `execute_p2_shared_probe()` scores each raw observation in memory and returns scored artifacts. This conflicts with the existing A01 authorization contract requiring raw output preservation, independent verification against the seal, and only then preregistered scoring.

CI success is readiness evidence, not scientific evidence. The current PR #132 default fixture/spec is best treated as **development validation input already exercised by CI**, not as a clean prospective one-way scientific candidate.

### Provenance/ref corrections carried forward

The previous analyst handoff contained stale/non-canonical ref names. Current remote re-verification establishes:

- RD005 D1 source freeze: `freeze/rv02-rd005-d1-source-c60b7fd8-20260914`, not the older shorthand `freeze/rv02-rd005-d1-source-20260913`.
- CX01 candidate-002 canonical freeze refs are `freeze/cx01-002-source` and `freeze/cx01-002-package`; its formal preserve is `preserve/cx01-candidate-002-formal-34742073336`.
- `preserve/v061-a01-md-001` currently points to `febdc1dbea0b7f84b1625be51f44075d9fa5a8da`; do not reuse the stale SHA recorded in the 10:30 handoff.

These are control-plane/provenance corrections, not new scientific results.

## Scientific evidence vs readiness evidence

### A01 / MD-002

**Scientific baseline:** MD-001 remains consumed and **UNRESOLVED / NOT_CLAIMABLE**. P1 passed. P2 numerically passed but did not establish the required post-attribution shared-root competition. P3 established only the weaker native-control comparison. P4 was never run. P5 provenance was insufficient. No post-hoc repair of MD-001 is allowed.

**New readiness evidence:** PR #132 implements the scientifically relevant P2 competition path and is CI-green. This materially shortens distance to a useful measurement.

**Current scientific-integrity status:** **STOP for execution on the current exact fixture/workflow.** The exact validation candidate has already been executed inside CI/test code before STARTED, and raw observations are scored before immutable preservation/independent verification. Neither issue can be cured by relabeling the same deterministic fixture with a fresh ID.

**Shortest valid path:** retain the already-fixed scientific measurement/scoring contract, but separate synthetic structural validation from the actual prospective candidate and split acquisition from scoring. Use a distinct prospectively bound world/input not executed by CI, atomically claim STARTED before execution, produce raw-only evidence, preserve it, independently verify it, then score under the already-fixed contract.

Status: **UNRESOLVED scientifically; execution is near after two integrity-boundary fixes.**

### RV01 / R01-16 and successor

No new R01 scientific evidence was found. R01-16 exposed-development capability remains consumed:

- Weight: **WEIGHT_SUPPORTED**, 100/100 support.
- Delay: **DELAY_MIXED**, 0 support / 54 negative / 46 discordant.
- Combined: **COMBINED_SUPPORTED**, 100/100 support.
- Held-out executions: 0; formal executions: 0.

The result was known before any successor protocol was frozen. Therefore any newly designed delay-scale or factorization test is a **new exploratory/development successor**, never a confirmatory continuation of R01-16. The scale asymmetry remains scientifically interesting, but R01-16 itself must not be rerun or retuned.

Status: **development evidence supports Weight and Combined; Delay mixed; successor must be distinct/exploratory.**

### RV02 / RD005 and successor

No new RD005 scientific evidence was found. D1 is consumed and terminal at construction/readiness: selected row null / zero-ready; blind reveal was not exercised and label access remained zero. Exact source is `c60b7fd8d3889ee969f505d921e7d31c990871e6`; construction identity remains `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; exact preserve is `preserve/rv02-rd005-d1-96634541-20260914`.

Status: **terminal construction/readiness negative for D1, with no blinded scientific outcome revealed.** A successor must use a distinct prospective identity and keep labels sealed during diagnosis/construction.

### CX / CX01

No new CX scientific evidence was found. Candidate-002 remains consumed and immutable **NEGATIVE**: 420 executions, 0 replay, C1-C7 false. Canonical source/package/control/preserve refs were re-verified above. No rerun or same-candidate retuning is allowed.

Status: **NEGATIVE consumed formal identity; next candidate remains farther from execution than A01 P2/P4 or an RV01 exploratory successor.**

## Consumed identities / no-rerun set relevant to active work

- V061 A01 MD-001 — consumed; preserve `preserve/v061-a01-md-001`.
- RV01 R01-16 construction — `rv01-r01-16-development-7ed3a7532fc66ac8-87634d034204`; duplicate workflow `34881331776` is the same consumed identity, not an independent replicate.
- RV01 R01-16 capability — `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`.
- RV02 RD005 D1 construction — `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`.
- CX01 candidate-002 formal — consumed; frozen source/package and STARTED/preserve refs above.

The PR #132 validation fixture is **not recorded as a consumed formal identity**, but it has already been computationally exercised by CI. Do not promote/relabel that same exact deterministic fixture as a pristine one-way experimental identity.

## Genuine blockers vs optional engineering work

**Genuine blockers for the highest-value next result:**

- P2 preflight/tests must not execute the actual prospective candidate before STARTED.
- The prospective P2 candidate must use a distinct, pre-specified input/world identity not already evaluated by CI/tests.
- P2 raw acquisition must be separated from scoring: raw-only artifact -> durable preservation -> independent integrity verification -> frozen scoring.
- Exact source/runtime/package/input identity and score contract must be bound before the one-way boundary.
- Atomic remote STARTED/no-clobber ownership and collision checks must happen before candidate execution.

**Optional/defer:** N3 completion, full MD-002 formal packaging, broad registry work, generic refactors, documentation polish, stale branch cleanup, and main integration, unless one directly blocks the P2 acquisition boundary above.

## Ranked next actions

### 1. Repair the PR #132 execution boundary, then run a **distinct prospective A01 MD-002 P2 shared-root development probe** — Information: **HIGH** / Distance: **NEAR**

Why #1: the instrumentation now targets exactly the missing MD-001 discriminator. Most code exists and CI is green. The remaining work is narrowly integrity-related, not broad infrastructure.

Minimum work:

1. Keep the scientific arm semantics, observation variables, budgets, thresholds, and score contract fixed unless a pre-outcome correctness bug independently requires a documented protocol revision.
2. Change tests/preflight so they validate structure with a clearly synthetic/dummy fixture or structural-only checks and never execute the real prospective candidate.
3. Bind a new prospective world/input identity that has not been executed by CI or any prior run. Do not simply rename seed 106617/current validation spec.
4. Split runner/workflow into raw acquisition and later scoring. Acquisition writes raw trial observations without score-derived fields; preserve/lock raw evidence and independently verify source/seal/raw hashes before invoking scorer.
5. Re-review, rerun CI, freeze exact source/runtime/package/input, atomically claim a distinct STARTED/no-clobber identity, then execute exactly once as development-only.

### 2. If #1 cannot be made clean without reusing observed input or altering the scientific contract, pivot to **A01 MD-002 P4 continuing-vs-reset lineage development discriminator** — Information: **HIGH** / Distance: **MODERATE**

P4 was never run in MD-001 and therefore remains a genuinely unobserved discriminator. Complete and freeze the exact continuing-vs-reset replay recipe and use a fresh development identity. Do not let P2 infrastructure repair consume multiple runs if P4 can reach a clean measurement first.

### 3. RV01 **distinct exploratory delay-scale successor** (R01-17 or equivalent) — Information: **HIGH** / Distance: **MODERATE**

R01-16’s Weight/Delay asymmetry suggests a direct mechanistic question about whether a scientifically meaningful delay perturbation changes factorization behavior. Use new seeds/worlds/identity and a new prospective protocol. Because R01-16 outcomes are already known, label this exploratory/development, not confirmatory.

Next outside top 3: a distinct blinded RV02 successor/diagnostic explaining RD005 D1 zero-ready while keeping labels sealed (**HIGH / MODERATE**). CX next-candidate design remains valid but farther from execution.

## GO / STOP criteria for recommendation #1

### Current status: **STOP** until the execution boundary is repaired

### GO only if all are true before candidate output is produced

1. Re-fetch PR #132, `research/v061-a01-md002-p2-shared-probe-20260915`, and `research/v061-a01-n3-adapter`; re-review if any head moved.
2. The actual prospective candidate input/world is distinct from the current validation fixture and has never been executed by tests, preflight, CI, or prior experiments.
3. Tests/preflight cannot call the real prospective candidate; they are synthetic/structural-only.
4. Arm semantics, reset/restore, observation window, resource instrumentation, budgets, validity gates, thresholds, and scoring are fixed before output.
5. Raw acquisition is score-free and produces a complete raw artifact first.
6. Raw artifact is durably preserved and independently verified against exact source/runtime/package/input/seal before scorer access.
7. A distinct execution identity is collision-checked and atomically claimed via STARTED/no-clobber before candidate execution; no existing control/preserve claim exists.
8. Exact source/runtime/package/input manifests are frozen and CI/review are green.
9. If literal independent-human identity is the only remaining gate, record `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE` / `HUMAN_REVIEW_WAIVED_BY_USER`; never fabricate a reviewer.
10. The run remains development-only; do not open held-out/formal scoring.

### STOP if any are true

- The real candidate is executed by unit tests, preflight, CI, or another worker before STARTED.
- The proposed candidate differs only by an ID label while reusing the already-exercised deterministic validation fixture/input.
- Scoring occurs before raw artifact preservation and independent verification.
- Proceeding requires changing thresholds/arm semantics/observation rules in response to candidate output.
- Exact source/runtime/package/input or reset/restore semantics are ambiguous.
- Head/diff moves after review without re-fetch/re-review.
- The candidate collides with a consumed/reserved/STARTED/control/preserve identity.
- A newer worker has already executed the same prospective identity.

If the STOP state cannot be cleared with narrow integrity fixes, pivot to P4 rather than broad cleanup.

## Concurrency / staleness findings

- The handoff branch had not moved since the 10:30 analyst commit when this analysis was completed.
- PR #132 is the only PR updated since the previous analyst handoff and is the only current open PR.
- A01 authoritative base `97fb43...`, RV01 `02b3d8...`, RV02 `c60b7f...`, and `main` `ba16bf...` did not move relative to the 10:30 handoff; the new concurrent work is isolated on the P2 probe branch/PR.
- No P2 freeze/control/preserve branch matching the new P2 probe exists yet; therefore no new A01 P2 one-way identity has been legitimately consumed.
- Several ref names in the 10:30 analyst record were stale/non-canonical; corrected refs are listed above and must be used by future orchestration.

## ORCHESTRATOR HANDOFF

Start with PR #132 and **do not execute its current exact validation fixture**. Re-fetch head `ca680064dc55b707ccd09610c19faa722bf23e82` (or newer) and the A01 base. Fix only the two real execution-boundary defects: (1) make CI/preflight structural or synthetic so the real prospective candidate is never executed before STARTED, and bind a distinct pre-specified candidate input; (2) split raw acquisition from scoring so raw evidence is preserved and independently verified before scorer access. Keep the scientific measurement/scoring contract outcome-blind and unchanged. Once the updated head is reviewed/green, freeze exact source/runtime/package/input, atomically claim STARTED, execute the distinct P2 development identity exactly once, preserve/verify raw evidence, then score. If a clean distinct P2 candidate cannot be established without relabeling the already-exercised fixture or changing the contract, stop and pivot in the same run to the prospectively clean A01 P4 continuing-vs-reset discriminator. Do not rerun MD-001, R01-16, RD005 D1, or CX01 candidate-002.