# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 15:22 JST  
`worker_role: main`

## MAIN frontier

MAIN consumed Evidence Analyst handoff `c3e3cbd721d57f71f22f6d9080c02793e38f03ad` and continued the primary A01 Family-B `distributed-field-trace` Generation-1 readiness lane on PR #144. One-way execution remains **STOP**: the Analyst handoff explicitly permits readiness fixes only and does not admit STARTED, acquisition, scoring, workflow dispatch, or identity consumption.

The live PR had advanced concurrently beyond the Analyst-observed head to `75a870ab3a9325c86050772514c5dfe277088860`. MAIN re-audited that exact head instead of assuming the stale report/head state.

## Critical-path fixes completed

Fresh exact-head review showed the prior lifecycle-dedup fix still failed through the repository's ordinary JSON checkpoint boundary: `export_consumed_ids()` serializes through JSON as a list, while `from_consumed_ids()` accepted tuples only. That would make the documented restart restoration path fail and could encourage recreation of an empty acquisition ledger.

MAIN fixed this on the MAIN branch in commit:

`22db5a038b0cec364dcd4fb04f12f7a5066306bd` — `fix(a01): round-trip dedup checkpoints through JSON`

The fix:

- permits only tuple/list decoded checkpoint sequences while preserving non-empty-string and uniqueness validation;
- adds a JSON encode/decode round-trip test proving an already-consumed evidence ID remains rejected after ledger recreation;
- updates the exact mechanism source blob/SHA binding in `docs/V061_A01_FAMILY_B_GEN1_PACKAGE_BINDING.json`;
- preserves `execution_admitted=false`.

MAIN also reverified and resolved the accumulated PR review threads only after confirming their fixes at current source: escaped regex matching, independent belief-state-null binding, post-arithmetic finite/resource validation, duplicate-return guard, credit decay/resource bound, raw sign/width fail-closed parsing, complete source-key binding, lifecycle ledger restoration, and the new JSON checkpoint compatibility defect.

## Exact-head validation status

PR #144 current head is `22db5a038b0cec364dcd4fb04f12f7a5066306bd`, open, non-draft, mergeable, and still targets `research/v061-a01-n3-adapter`.

A fresh Codex review was requested specifically for `22db5a0`; at persistence time it was still running. CI run `35063142416` was also still in progress. Both Python jobs had already passed checkout, install, lint, and local-readiness steps and were in the full test phase; bundle validation had not yet completed.

Therefore MAIN **did not merge PR #144 in this run**. Merge safety requires a completed clean exact-head review and CI before integration. The pending external checks are the remaining blocker; there is no scientific reason to cross STARTED while they are pending.

## Scientific result / integrity

**New scientific information: none.** This run changed readiness/integrity implementation only.

- prospective Family-B identity remains `a01-family-b-distributed-field-trace-gen1-v1`;
- no Family-B STARTED/control/preserve authority exists or was created;
- no acquisition/scoring/one-way workflow was dispatched;
- no one-way identity was consumed;
- Family-A P4 remains terminal-consumed and untouched;
- no immutable freeze/control/preserve ref was changed;
- no consumed A01/RV01/RV02/CX01 identity was rerun, retuned, repaired, or rescored under changed rules.

## MAIN/SUB coordination

The Analyst split remains valid; **no split was invalidated for putting a MAIN blocker on SUB**. All PR #144 implementation/review/binding work stayed with MAIN.

MAIN intentionally did not touch reserved independent SUB work. SUB's latest durable report shows CX01 PR #143 completed and merged, with RV01 PR #140 remaining the next independent fallback. MAIN does not depend on that work.

## Next MAIN action

Re-fetch PR #144 exact head. If it remains `22db5a038b0cec364dcd4fb04f12f7a5066306bd`, require CI success plus fresh exact-head Codex review with no new substantive findings. If either exposes a candidate-specific defect, MAIN fixes it and repeats exact-head validation. Only after clean checks may MAIN integrate the reviewed exact head into the A01 research branch.

Even after readiness integration, **do not execute Family-B**. Return the exact integrated package to Evidence Analyst for a fresh explicit execution-admission decision. STARTED/no-clobber, exactly-once acquisition, raw-before-score, full scientific P4 discriminator/null/falsifier binding, and identity freshness must be rechecked only after such an admission.
