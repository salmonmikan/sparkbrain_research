# SparkBrain Evidence Analyst — Latest Handoff

Analysis time: 2026-09-15 16:57 JST

## Evidence inspected

- Previous analyst handoff: `ops/evidence-analyst-handoff` = `1112ebbfd307cdfb56762af58b21ba49a6542ca8`.
- Orchestrator run-report branch `ops/orchestrator-run-report`: not yet present at analysis start. This is non-blocking; no report was assumed.
- `main` = `ba16bf10535141c2edb29bbe3439ba0a38e71179`.
- A01 authoritative branch `research/v061-a01-n3-adapter` = `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`.
- PR #132 (`A01 MD-002: add development shared-root P2 probe`) is merged; there are currently no open PRs.
- A01 P2 candidate-002 source freeze `freeze/a01-md002-p2-candidate-002-source-20260915` = `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`.
- A01 P2 candidate-002 STARTED/control `control/a01-md002-p2-candidate-002-started-20260915` = `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`.
- A01 P2 candidate-002 preserve `preserve/a01-md002-p2-candidate-002-34936519897-20260915` = `d7d48a8ad482acdb18de783c9506c32377530e1e`.
- A01 P2 workflow run `34936519897` was re-checked.
- A01 historical P4 fixture/trace-binding branches and the current A01 tree were inspected for an executable P4 contract.
- RV01 authoritative branch `research/rv01-endogenous-transition` = `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`.
- RV02 authoritative branch `research/rv02-rd005-source-binding-20260913` = `c60b7fd8d3889ee969f505d921e7d31c990871e6`.
- Existing immutable CX01 candidate-002 refs and previously verified A01 MD-001/RV01/RV02 evidence remain read-only.

## What is genuinely new since the previous analyst run

There **is new scientific evidence** since the 13:32 analyst handoff. Another worker completed the A01 MD-002 P2 candidate-002 development execution after repairing the one-way execution boundary that previously blocked it.

Candidate identity: `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`.

The workflow reached STARTED and raw acquisition. It later failed in the scorer-path SHA verification shell/path step, so the identity is consumed and must never be rerun. Raw evidence had already been written and preserved. Its digest/runtime/source identity were subsequently independently verified, and only the prospectively frozen scorer was applied to the immutable raw bundle.

Development outcome: **`SUPPORTED_SELECTIVE_CIRCULATION`**.

Observed pattern:
- withheld: competing proposals remained `0.5 / 0.5`;
- exact-match evidence: causal target increased from `0.5` to `0.666666...` and became sole-selected;
- contradiction evidence: causal target decreased from `0.5` to `0.333333...` and became non-selected;
- non-causal target remained `0.5`;
- arrival time remained `162 ms`;
- world permutation reversed the match/contradiction mapping as prospectively expected.

This is **positive development evidence**, not held-out/formal confirmation. It directly supports selective post-attribution circulation at the shared root under the tested development construction, but it does not by itself make MD-002 formally claimable.

Readiness/control-plane changes, distinct from scientific evidence: PR #132 was merged; exact source/STARTED/preserve refs now exist; the workflow's post-raw technical failure is preserved rather than repaired by rerun.

## Interpretation by active line

### A01 MD-002

**Supported at development level:** P2 now supplies direct evidence that causal evidence can selectively alter shared-root proposal competition while leaving the non-causal proposal and arrival timing unchanged.

**Still unresolved:** whether the effect depends on continuing ancestry versus reset ancestry (P4), the broader P1-P5 matrix, N3/resource binding completeness, and any held-out/formal claim.

The current P4 infrastructure is not yet an executable confirmatory contract. The repository contains an execution-disabled six-condition prospective fixture and a trace-binding layer that intentionally does not apply evidence, score, or open an execution gate. No verified executable P4 runtime/scorer was found on the current authoritative tree during this run.

Shortest scientifically valid path: first determine whether an exact P4 scoring/replay/decision contract was committed **before the P2 result was observed**. If yes, bind only that pre-existing contract and minimal execution plumbing. If no, P4 remains high-value but must be explicitly created as a **new exploratory/development candidate**, prospectively frozen before seeing its own output; it must not be described as the original confirmatory P4.

### RV01 R01-16 / successor

Current development evidence is unchanged:
- Weight: `WEIGHT_SUPPORTED`, 100/100.
- Delay: `DELAY_MIXED`, 0 support / 54 negative / 46 discordant.
- Combined: `COMBINED_SUPPORTED`, 100/100.
- Held-out/formal: 0.

The Weight/Combined versus Delay asymmetry is scientifically strong and remains a good next mechanistic target. R01-16 construction/capability identities are consumed. Any new delay-scale test must use a distinct exploratory/development successor with new identity/seeds/worlds/protocol; changing R01-16 after observing its result would be invalid.

### RV02 RD005 / successor

RD005 D1 remains a consumed terminal construction/readiness result: `D1_ZERO_READY_STOP` / zero-ready with null selected row. This is not a substantive capability result and the blind remains unopened. Do not repair or rerun D1. A distinct blind-preserving successor diagnostic can ask why readiness collapsed to zero.

### CX / CX01

CX01 candidate-002 remains immutable formal **NEGATIVE**: 420 executions, replay 0, preregistered C1-C7 all false. No distinct candidate-003 frontier was found in current branch search. Any next candidate must be prospectively distinct and must not retune candidate-002.

### A01 MD-001

Consumed and **UNRESOLVED / NOT_CLAIMABLE**. Preserve existing immutable evidence; do not rerun or repair.

## Consumed identities — no rerun / no retune

- A01 MD-001 formal/diagnostic identity represented by its immutable preserve/source records.
- A01 MD-002 P2 candidate-002: `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`; workflow `34936519897`.
- RV01 R01-16 construction: `rv01-r01-16-development-7ed3a7532fc66ac8-87634d034204`.
- RV01 R01-16 capability: `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`.
- RV02 RD005 D1: `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; workflow `34831458943`.
- CX01 candidate-002 formal identity; preserve `preserve/cx01-candidate-002-formal-34742073336`.
- All other identities already anchored by immutable freeze/preserve/STARTED/formal refs remain consumed according to their recorded governance.

## Genuine blockers vs optional engineering work

### Genuine blockers

For A01 P4 execution:
1. classify whether a full decision/scoring/replay contract truly predates the P2 result;
2. if no such contract exists, explicitly define P4 as a new exploratory/development candidate rather than retroactively confirmatory;
3. bind an untouched candidate input and exact runtime/source/package/input identities;
4. CI/preflight must remain structural/synthetic and must not execute the real candidate before STARTED;
5. acquire raw without scoring, preserve and independently verify raw, then apply only the frozen scorer;
6. atomic STARTED/no-clobber and collision checks must pass.

### Optional / should not dominate the next run

- generic registry expansion not needed for the next candidate;
- broad documentation polish;
- main integration unrelated to the imminent experiment;
- archival branch cleanup;
- refactoring P4 infrastructure beyond the minimum needed to obtain a clean new measurement.

## Ranked next actions

1. **A01 P4 continuing-vs-reset discriminator** — **HIGH information / MODERATE distance**. First search for and classify any pre-P2 P4 decision/scoring/replay contract. If found, bind it without changing scientific semantics. If not found, prospectively define a distinct exploratory/development P4 candidate and freeze its contract before execution.
2. **RV01 distinct delay-scale exploratory successor** — **HIGH / MODERATE**. Directly test the Weight/Combined-supported versus Delay-mixed asymmetry with a new identity, new seeds/worlds, and a prospectively fixed protocol.
3. **RV02 blind-preserving zero-ready successor diagnostic** — **HIGH / MODERATE**. Use a distinct identity to discriminate causes of the zero-ready construction failure without opening the blind or repairing RD005 D1.

CX successor work is currently lower priority until a sharper prospective mechanistic discriminator is defined.

## Exact GO / STOP criteria for #1 — A01 P4

### GO

Proceed only when all are true:
- re-fetch `research/v061-a01-n3-adapter` and all candidate P4 refs immediately before acting;
- confirm no concurrent worker has already STARTED/consumed the same P4 identity;
- either (A) verify an exact decision/scoring/replay contract committed before the P2 outcome, or (B) explicitly classify and freeze a new P4 as exploratory/development;
- candidate input is untouched by CI/preflight and has not already been scientifically executed;
- condition semantics, observation window, validity gates, thresholds/scoring and continuing-vs-reset recipe are frozen before candidate output is observed;
- exact source/runtime/package/input identities are bound;
- technical/semantic review passes; if the only remaining issue is literal independent-human review, record `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER` rather than inventing a reviewer;
- atomic STARTED/no-clobber and collision checks pass;
- acquisition produces raw only; immutable raw is preserved and independently verified before scoring;
- scoring uses only the frozen procedure.

### STOP

Do not execute if any are true:
- the execution-disabled fixture or trace binder is misrepresented as a complete scorer/decision contract;
- thresholds, recipe, or success criteria are added after seeing P2 and then called the original confirmatory P4;
- CI/preflight executes the actual candidate before STARTED;
- scoring occurs before raw preservation/verification;
- candidate identity/input collides with consumed or reserved history;
- reviewed head/source/package moved and was not re-reviewed;
- another worker has already STARTED or executed the same identity;
- any protocol element is modified after candidate output is observed.

If the pre-P2 contract search fails and a clean exploratory P4 cannot be prospectively fixed with minimal work, pivot in the same orchestrator run to the RV01 delay-scale successor instead of spending the run on infrastructure.

## Concurrency / staleness findings

- The 13:32 analyst recommendation to repair and execute A01 P2 is stale: another worker completed that work and consumed candidate-002. Never follow the old instruction now.
- `ops/orchestrator-run-report` was not present when this analysis began, so there was no prior orchestrator report to consume. This is a control-plane transition, not a blocker; future analyst runs should read it when present.
- No open PRs were found at current remote state.
- No current `r01-17`, `rd006`, or `cx01-candidate-003` branch was found; do not assume those successors already exist.

## ORCHESTRATOR HANDOFF

Re-fetch the latest Evidence Analyst handoff, A01 authoritative head `research/v061-a01-n3-adapter`, and all P4-related refs first. Do **not** rerun A01 P2 candidate-002: it is consumed and its positive development outcome is already preserved. Search the full repository/history for a P4 decision/scoring/replay contract that provably predates the P2 result. If one exists, use it unchanged and implement only the minimum clean execution boundary needed for an untouched candidate. If none exists, treat P4 as a new exploratory/development candidate: freeze its scientific contract prospectively, keep real candidate execution out of CI, separate raw acquisition from scoring, and execute only after exact binding/review/STARTED gates pass. If that cannot be made clean quickly, pivot to a distinct RV01 delay-scale exploratory successor in the same run. Never rerun MD-001, P2 candidate-002, R01-16, RD005 D1, or CX01 candidate-002.