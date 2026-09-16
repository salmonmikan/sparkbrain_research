# SparkBrain Research Orchestrator SUB — Latest

Run time: 2026-09-16 10:46 JST  
Worker role: `sub` / SECONDARY IMPLEMENTER

## MAIN frontier explicitly avoided

MAIN's A01 MD-002 P4 candidate-001 was not touched. During this SUB run, the newer MAIN report showed that candidate-001 had already crossed the one-way boundary and terminated as consumed development evidence with verdict `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`. SUB did not modify PR #137, the A01 research branch, P4 freeze/control/preserve refs, scorer, or any P4 follow-up design.

The Evidence Analyst handoff consumed for lane ownership was `ops/evidence-analyst-handoff@5f444a295d3ae32263923c3706ac2c6c6746533d`. Although its snapshot still described P4 as pre-STARTED, its reserved SUB lane remained scientifically independent of the later MAIN outcome.

## Selected independent SUB lane

Primary reserved lane: **RV01 canonical status and evidence-map consolidation**.

- reservation: `reserved_for_sub`
- independent of MAIN critical path: yes
- scientific execution allowed: no
- authoritative RV01 base rechecked: `research/rv01-endogenous-transition@98be60268845487ce51e76b8a7687552a5dbc51f`

Fresh evidence checks confirmed:

- R01-17 identity `rv01-r01-17-real-delay-causal-timing-v1` is consumed.
- frozen/STARTED source: `5ecb459b609b393ff837f57cc138f1eb44c1b255`
- raw preserve: `fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`
- scored preserve: `d4737d52ecbb2306d9f00f99366f0ad6424327be`
- preserved classification: `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`, development-only with no formal/held-out authority.
- ordinary local adaptive-delay plasticity remains the conservative simpler reduction.

## Implementation progress

Created distinct SUB docs branch:

- `research/rv01-status-evidence-consolidation-sub-20260916`

Added canonical status/evidence map:

- `docs/research/RV01_STATUS_EVIDENCE_MAP.md`
- commit `2d877a5af670c54d404d8782763129f497092f88`

The document consolidates the consumed result, exact source/STARTED/raw/scored evidence pointers, evidence digests, no-rerun/no-retune boundary, development-only authority, conservative reduction, relationship to R01-16, and the absence of a verified prospective successor. It does not create new science or reinterpret immutable evidence.

Opened reviewable docs-only PR:

- PR #140 — `RV01: consolidate current status and evidence map`
- base: `research/rv01-endogenous-transition`
- head: `research/rv01-status-evidence-consolidation-sub-20260916`
- exact head: `2d877a5af670c54d404d8782763129f497092f88`
- diff: one new documentation file, 117 additions

## Scientific / readiness result

No new experiment, workflow, STARTED boundary, scoring action, or one-way identity was executed by SUB. No new scientific measurement was produced.

The independent readiness/documentation completion target **was reached**: RV01 now has a reviewable canonical status/evidence-map package that makes the consumed development result and evidence boundaries explicit without opening successor science.

No immutable/frozen/formal evidence was modified. No consumed identity was rerun or retuned.

## Fallback / blockers

RV02 terminal-status/evidence-map consolidation remained available as the reserved fallback but was not needed because the primary RV01 lane completed successfully.

No blocker remains for this SUB completion target. PR review/merge may proceed independently and is not a dependency for MAIN.
