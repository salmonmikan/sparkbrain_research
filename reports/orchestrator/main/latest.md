# MAIN RELAY — Refractory comment-detector preflight repair checkpoint

Timestamp: `2026-09-20 07:16 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `7e7d425948a86d0eec306b1a75bfc07165d9afa1`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-REFRACTORY-CURRENT-ACCOUNTING-01`

## Lease / collision reconciliation

The inherited MAIN lease was a stale RELAY `RUNNING` lease from `06:49 JST`, not a fresh PRIMARY collision. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the active research branch remained on `ac5f4d5ef59bafaafe046130d21d3bed27a677a4` before this continuation. RELAY acquired MAIN lease `sparkbrain-main-relay-20260920T0712JST` before mutating the research branch.

Fresh Evidence Analyst authority `7e7d425948a86d0eec306b1a75bfc07165d9afa1` reviewed Architecture workflow `35471788666` and classified its failure as `PRE_START_COMMENT_DETECTOR_REPRESENTATION_BLOCKER`: lint/tests passed, both exact-head jobs failed only at `Verify prospective binding only`, the outcome-bearing Architecture job was skipped, and no diagnostic result was visible.

## Prospectively authorized repair

The contract binds the source comment as one continuous sentence, while the exact immutable source blob stores that sentence over two adjacent full-line `#` comments. The prior harness used raw substring matching, causing a deterministic representation false negative.

Under the Analyst contingency, RELAY modified only `analysis/architecture/refractory_current_accounting_cycle1_20260920.py` so full-line comment blocks are deterministically normalized by stripping comment markers/outer whitespace and joining adjacent comment lines. The existing bound contract sentence is then matched exactly against those normalized blocks.

Commit: `4589192d927e40cf7a05cf8a94207efb42ebbc65`.

The diff from `ac5f4d5ef59bafaafe046130d21d3bed27a677a4` is one harness file only (`+20/-1`). No production source, source binding, contract text, input family, comparator, currents/timestamps/probe, tolerance, observables, terminal mapping, TEST/formal surface, or SUB-owned object changed.

## Exact-head workflow state

Current exact research head: `4589192d927e40cf7a05cf8a94207efb42ebbc65`.

- ordinary CI `35472786733`: `in_progress` on the exact head.
- Refractory Architecture workflow `35472786687`: `in_progress` on the exact head.

The previous replacement Architecture workflow `35471788666` is `completed/failure` at preflight binding only; its Architecture outcome job was skipped and it produced no scientific terminal.

Under WAITING policy there is no other useful MAIN-critical action until the new exact-head workflows finish.

## Scientific / integrity status

New FORMAL scientific evidence: **none**.  
New PRE_FORMAL evidence: **none**.  
New valid Architecture terminal: **none yet**.  
Evidentiary status: **NON_EVIDENTIARY**.

No formal identity, STARTED/control authority, official TEST access, preserve/scoring/evidence mutation, consumed-identity retry, immutable evidence mutation, post-outcome repair, semantic redesign, or Utility request occurred.

Stop reason: **`PREFLIGHT_COMMENT_DETECTOR_REPAIRED_NEW_EXACT_HEAD_WORKFLOWS_IN_PROGRESS`**.

Final lease: **`WAITING_EXTERNAL`**. Next MAIN/Relay must re-fetch fresh Analyst authority, exact research head `4589192d927e40cf7a05cf8a94207efb42ebbc65`, ordinary CI `35472786733`, and Architecture workflow `35472786687`. If all unchanged prospective bindings pass and the workflow yields a valid artifact, verify exact head/source/contract/machine-fact/artifact/raw binding, apply the already-fixed terminal mapping exactly once, persist the NON_EVIDENTIARY result, and STOP for fresh Evidence Analyst review. Any other machine-fact failure or semantic/protocol gap STOPs; no cycle 2, PRE_FORMAL, FORMAL, semantic repair, or outcome-responsive redesign is authorized.
