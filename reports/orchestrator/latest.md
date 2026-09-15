# SparkBrain Research Orchestrator run report — 2026-09-15 18:44 JST

## Control-plane input

- Evidence Analyst handoff: `ops/evidence-analyst-handoff` at `6f2c5a54d1d6ae4e4d03731f039f727478a74e6c`.
- Status: **followed, then partially superseded by newer repository evidence**. The analyst ranked A01 P4 first, with an explicit STOP if no complete pre-P2 executable scoring/replay/decision contract could be recovered, and RV01 as the pivot.
- Previous orchestrator report read: `ops/orchestrator-run-report` at `c13ae95c289ec27ca2601c3aed7541261c055bfc` (18:21 JST). It already contained a newly derived RV01 R01-16 post-hoc interaction diagnostic and PR #133, so this run reconciled that work rather than duplicating it.

## Authoritative refs / evidence re-fetched

- `main`: `ba16bf10535141c2edb29bbe3439ba0a38e71179`.
- A01 authoritative `research/v061-a01-n3-adapter`: `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d` (re-fetched during this run; no concurrent movement observed).
- RV01 authoritative `research/rv01-endogenous-transition`: `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`.
- RV02 authoritative/source-binding remains `research/rv02-rd005-source-binding-20260913`: `c60b7fd8d3889ee969f505d921e7d31c990871e6`.
- Relevant immutable refs were inventoried again. Current freeze refs include A01 P2 candidate-002 source, CX01 candidate-001/002 source/package, RV01 R01-15/R01-16 sources, and RV02 RD003/RD004/RD005 sources. Current preserve refs include A01 P2 candidate-002, CX01 candidate-002 formal evidence, RV01 R01-14/15/16 evidence, RV02 RD002/3/4/5 evidence, and A01 MD-001. Current STARTED/control refs include A01 P2 candidate-002, CX01 candidate-002, RV01 R01-16 capability, and RV02 RD005 D1.

## Active research lines

### A01 MD-002

P2 candidate-002 is consumed and remains no-rerun/no-retune. Development result remains `SUPPORTED_SELECTIVE_CIRCULATION`; no held-out/formal claim is made.

The analyst-recommended P4 route was rechecked against historical P4 construction. The historical P4 fixture is execution-disabled and the trace binding intentionally does not score or open an execution gate. No complete pre-P2 executable P4 scoring/replay/decision contract was recovered. Therefore the old-confirmatory P4 path remains STOP. Any P4 designed now must be a distinct prospective exploratory/development identity unless stronger pre-P2 evidence is later recovered.

### RV01 R01-16

The previous orchestrator worker had already derived and documented a new post-hoc diagnostic from immutable, already-consumed capability evidence. This run re-fetched and independently checked the current PR/document rather than recomputing or rerunning R01-16.

Bound evidence in the current diagnostic:
- authoritative RV01 source `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- capability identity `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`
- preserve ref `preserve/rv01-r01-16-capability-20260915`
- preserve commit `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- raw artifact SHA-256 `e3b6e8c7ed6db423919c4360a5291ac207544566beb4656954be344cb253f335`
- capability suite hash / immutable result provenance `b1b4d555d30630d1051482563696981261619143099216ab893bbea481d69392d`
- source/package manifest SHA-256 `bc36c7da23f4d6b8fa1ee7d4d8c7bacdfd5970818482e146a188837247332582`
- retained-history registry SHA-256 `232f4fb23b74662d10adca2990e1b030bbb1c74e45fb67f607982738570795bd`

Verified contrast counts over 100 eligible development cells:
- `F0_vs_FW_different`: 100/100
- `FD_vs_FWD_different`: 100/100
- `F0_vs_FD_different`: 46/100
- `FW_vs_FWD_different`: 0/100
- `F0_vs_FWD_different`: 100/100

The frozen aggregate classifications remain Weight=`WEIGHT_SUPPORTED` 100/100, Delay=`DELAY_MIXED` (0 support / 54 negative / 46 discordant), Combined=`COMBINED_SUPPORTED` 100/100.

The sharpened post-hoc interpretation is **asymmetric, weight-conditioned expression of the learned-delay contribution at the measured behavioral endpoint**: delay reset changes the signature in 46/100 cells while learned weight is retained, but in 0/100 cells after weight reset; weight remains consequential 100/100 under either delay state. This does not establish direct biophysical gating/causation and remains exposed-development/post-hoc evidence.

Important reconciliation: an earlier shorthand framing this as different delay-scale buckets is not authoritative. The current bound diagnostic is a 2x2 weight/delay interaction (`F0`, `FW`, `FD`, `FWD`), and successor design should reflect that interaction rather than merely increasing delay magnitude.

### RV02 RD005

D1 identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a` remains consumed with terminal `D1_ZERO_READY_STOP` / zero-ready construction-readiness result. Blind result remains unopened. No repair or rerun was attempted.

### CX/CX01

Candidate-002 remains immutable formal NEGATIVE (420 executions, replay 0, C1-C7 false) and consumed. No rerun, retune, or mutation of source/package/control/preserve evidence occurred.

## PR #133 reconciliation and advancement

Open PR #133: `RV01 R01-16: record delay interaction diagnostic`.
- base: `research/rv01-endogenous-transition` at `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- head: `review/rv01-r01-16-delay-interaction-diagnostic-20260915`
- exact current head: `78790d08b1da9c7efcb397203ca77cce34a7a487`
- mergeable: true
- changed files: one diagnostic document
- current-head CI jobs observed green in the re-fetch sequence
- Codex review completed on exact head and found a new P1 governance blocker: the newly derived negative/null diagnostic must be entered in canonical `docs/RESULTS_LEDGER.md`.

This run did **not** merge PR #133 because the canonical ledger entry is a real durable-provenance blocker, not optional polish. The available direct GitHub file writer requires complete-file replacement for the large ledger, so this run avoided an unsafe manual whole-file rewrite. Instead it used the repository's existing Codex remediation path and posted `@codex address that feedback` (issue comment id `5678073446`) so the review worker can append the ledger entry safely on the PR branch. At the last exact-head re-fetch during this run the PR head had not yet moved, so no stale merge attempt was made.

If Codex advances the head, the next orchestrator must re-fetch the new exact head, inspect the ledger patch and diagnostic diff, re-run/confirm required checks/review, and only then merge using that exact reviewed head SHA. The current `78790d08...` must not be merged while the P1 finding is unresolved.

## Executions / one-way boundaries

- New scientific workflow or experiment launched by this run: **0**.
- New one-way identity consumed by this run: **0**.
- New freeze refs: **0**.
- New preserve refs: **0**.
- New STARTED/control refs: **0**.
- Frozen/preserved/formal evidence modified: **0**.
- Human-review gate override used: **0**.

Consumed identities remain no-rerun/no-retune: A01 MD-001, A01 MD-002 P2 candidate-002, RV01 R01-16 construction and capability, RV02 RD005 D1, CX01 candidate-002, plus all other explicitly consumed/frozen identities represented by immutable control/preserve refs.

## Repository hygiene / main

- Obsolete PRs closed: **0**.
- Exact-head merges: **0**.
- Main integration: **0**.
- Branch deletion: **0**.
- Historical A01 P4 fixture/trace-binding branches remain evidence-bearing/archival and superseded as an immediately executable old-confirmatory path; leave intact.
- Older RV01 R01-12/13/14/15 and RV02 RD001-004 construction/review branches are historical/evidence-bearing unless separately proven obsolete; no deletion or force movement was attempted.

## Genuine blockers

1. PR #133 requires the canonical `docs/RESULTS_LEDGER.md` entry before merge. Codex remediation has been requested; exact head must be re-reviewed after any movement.
2. A01 P4 lacks a verified complete pre-P2 executable scoring/replay/decision contract; any new P4 must be prospective exploratory/development.
3. RV01's next causal discriminator requires a fresh identity/world/seed set and prospectively fixed endpoints. Based on the new interaction diagnostic, the high-information successor should keep the existing route/behavior endpoint and add an orthogonal timing/trajectory-sensitive endpoint to distinguish weight-conditioned delay expression, latent timing/decision-boundary convergence, and route-level interaction.
4. RV02 D1 is consumed; only a distinct blind-preserving successor is valid.

## Next-ready actions

1. **Finish PR #133 provenance record and exact-head merge if clean — NEAR, required correctness work.** Re-fetch after the Codex remediation request; if a new head adds the canonical ledger entry and exact-head CI/review are green, inspect and merge only that exact head. This is minimal work needed to make the new RV01 diagnostic durable on the active research line.
2. **RV01 distinct interaction successor — HIGH information / MODERATE distance.** Prospectively preregister fresh worlds/seeds/identity and both route/behavior plus timing/trajectory endpoints; do not rerun R01-16.
3. **A01 P4 distinct exploratory/development candidate — HIGH / MODERATE** if no complete pre-P2 contract emerges; never retroactively label a post-P2 scorer confirmatory.
4. **RV02 blind-preserving zero-ready successor — HIGH / MODERATE** after the nearer RV01/A01 frontier.

## Run result

**This run itself did not generate a new experiment measurement or consume a new identity.** It reconciled scientifically meaningful RV01 information generated by the immediately preceding worker, corrected the successor interpretation to the authoritative weight-by-delay interaction, verified that PR #133 is not yet merge-safe due to a canonical-ledger P1, and advanced that blocker through the repository's Codex remediation path without risking a stale merge or unsafe whole-file rewrite.
