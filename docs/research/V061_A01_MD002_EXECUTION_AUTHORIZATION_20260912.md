# A01 MD-002 user execution authorization — 2026-09-12

Status: **USER_AUTHORIZED_WHEN_TECHNICALLY_READY / EXECUTION_DISABLED_AT_CURRENT_SOURCE**

## Authorization

The user explicitly authorized the A01 research line to proceed through an experiment boundary when the experiment is prospectively fixed, technically ready, and execution approval is the only remaining blocker. This authorization was given on 2026-09-12 and applies to A01 MD-002 once its exact experiment identity and executable package satisfy the preregistered integrity gates.

This durable record supersedes only the prior governance assumption that another user execution-approval request must always be obtained. It does **not** supersede or waive any technical/scientific-integrity prerequisite.

When a specific A01 MD-002 development or formal/confirmatory experiment reaches a state where all of the following are fixed and validated, the user authorization may be used as the candidate/diagnostic-specific execution authority for that exact identity:

- exact experiment/candidate identity and prospective matrix;
- exact source SHA and source manifest;
- bound protocol/scoring/acceptance rules and exclusions;
- complete P1-P5 applicability/condition identity required for that experiment;
- required A01/N1/N3 source/configuration identities and resource-accounting semantics;
- raw artifact schema, preservation/no-clobber procedure, and independent verifier;
- technical/semantic review, with any literal human-identity-only condition transparently handled under the standing user-authorized review-gate override;
- execution seal or equivalent immutable authority binding required by the runtime gate.

Immediately before consumption, all bound identities must be revalidated. An experiment may then be executed exactly once under the fixed contract, with raw evidence preserved before scoring.

## Current MD-002 boundary

At the source revision from which this authorization record is branched, MD-002 is **not execution-ready**. The existing binding status and P4 technical review retain genuine unresolved engineering/scientific prerequisites, including full P2/P3/P4 executable construction, N3 resource matching, complete matrix/budget/threshold binding, exact source/runtime runner binding, raw preservation/verifier integration, and final executable-package review.

Therefore this record does not set either immutable execution-authority digest pin in `MD002ExecutionGate`, does not create `STARTED`, does not issue an execution seal, and does not execute capability.

## Scientific-integrity constraints

The authorization never permits:

- rerunning or rescoring A01 MD-001;
- modifying `preserve/*`, `freeze/*`, formal evidence, or another immutable anchor;
- tuning the same MD-002 identity after inspecting its result;
- replacing or silently repairing a consumed candidate/diagnostic identity;
- using the authorization to bypass a technical or scientific-integrity blocker;
- fabricating an independent human reviewer identity.

Each distinct execution identity remains one-shot. Once an identity is consumed or fails after crossing its no-change/STARTED boundary, it remains consumed.

## Required record at execution

Any future A01 execution that relies on this authorization must durably record that it proceeded under the user's explicit A01 line-scoped execution authorization dated **2026-09-12**, together with the exact consumed experiment identity, source SHA, authority/seal identity, and execution/run identity.
