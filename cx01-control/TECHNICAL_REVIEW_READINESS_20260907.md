# CX01 Candidate-001 — Technical Review Readiness Audit

Status: **REVIEW BLOCKED / FORMAL CANDIDATE REJECTED PRE-START / SEAL PROHIBITED**

This audit is performed by the same assistant lineage that participated in CX01 source/package preparation. It is not the independent approval required by the protocol. During review-readiness inspection it found a scientific blocker that must be resolved before any independent seal can be issued.

## Audited identities

```text
freeze ref:       freeze/cx01-001
source SHA:       f2c5ead5afda7d731033d585511ea68dc066a162
control branch:   cx01-control/candidate-001
candidate:        cx01-candidate-001
seeds:            269810..269819
```

## Verdict by required question

| Question | Verdict | Evidence |
|---|---|---|
| 1. Exact source freeze identity | PASS with operational caveat | `freeze/cx01-001` still resolves to exact SHA `f2c5ead5...`. The ref is an unprotected branch and can technically be moved, but the manifest and formal workflow bind the exact SHA and fail closed on `GITHUB_SHA != source_sha`. |
| 2. Numeric seed-band separation | PASS | Candidate seeds are outside historical `100..109`, `1000..1009`, `2000..2009` and permanent CX01 non-formal `3000..5999`. Candidate validation rejects those exposed ranges. |
| 2b. Structural held-out independence of generated worlds | **FAIL — BLOCKER** | Frozen `build_world()` uses seed/generation primarily to permute anonymous token roles. HIGH_ORDER, TIMING, BRANCH, SELECTIVITY and LOOP keep the same lags, exposure counts, branch ratios and topology as development. CYCLE changes only the 2/3 exposure parity pattern, already present in development seeds. This does not satisfy CX01-09's preregistered requirement for `new topology/token permutations`, `new timing values`, and `new contingency schedules`. |
| 3. Candidate/grid/declaration/manifest hashes | PASS | Candidate spec and manifest hashes canonicalize correctly. Frozen-source structural validation PR #21 recomputed candidate grid, all 420 declarations, declaration bundle, privilege/schedule/scoring/schema hashes and complete manifest; CI passed and PR #21 was closed without merge. |
| 4. Privilege/schedule/scoring/schema frozen | PASS | Manifest binds comparator inventory plus privilege, schedule, scoring-policy, result-schema and resource-schema hashes. Independent recalculation of these semantic sub-hashes matches the manifest. |
| 5. Capability exposure remains unopened | PASS | Control directory contains neither `execution_seal.json` nor `STARTED.json`. GitHub Actions history since candidate preparation contains no `cx01-formal-one-way` workflow run. No formal result has been produced or inspected. |
| 6. May an independent seal be issued now? | **NO** | Scientific candidate-independence blocker exists, and no external independent approval exists. |

## Why the blocker is material

The frozen generator hard-codes the following development/formal structures for most families:

```text
HIGH_ORDER:  fixed lags 5/7/6, fixed exposure 5/5
TIMING:      fixed timing signatures 4/18 and 18/4, fixed exposure 5/5
BRANCH:      fixed counts 6/5/4 and fixed 5/5/5 lags
SELECTIVITY: fixed topology, fixed 5/7/5 lags, fixed exposure 5/5
LOOP:        fixed topology, fixed 5/5/8 lags, fixed exposure 5
CYCLE:       only 2/3 phase exposure parity varies with seed
```

For anonymous token-invariant comparators this means the formal candidate is largely a relabeling of already-observed development structures. A fresh numerical seed is therefore insufficient to establish the intended held-out generalization claim.

CX01-09 explicitly preregistered that the fresh candidate generator should create:

```text
fresh RNG salt
disjoint seeds
new topology/token permutations
new timing values
new contingency schedules
schema-only candidate declaration
```

Candidate-001 satisfies fresh identity/seed/token permutation, but not the required structural/timing/contingency novelty.

## Hash checks that still PASS

```text
candidate_spec_hash
aba791ade53feb89950ef0f0b673c68f9ef91b82b1ed9f0560ab9f2576e2fc30

candidate_grid_hash
6c81390a785deb0ea8fe30e35186361621dc31bb1e42fe09d7c63ab221575db7

declaration_bundle_hash
c77ff6cb90207d9ce02be328fff245926d1f40e196bb86f9b5eeb5d533404613

freeze_manifest_hash
e440dbb6fb6ba06e0196380d04c3c177f647a071a0a7c564fa2e817d6eebc915

privilege_inventory_hash
2a59a2cf34782bcbcf8fd135f2e378fef8dfb391215b25ba5ef8dfc8cd8f513a

schedule_policy_hash
b013e667a6f5fbc8910d11f13e19f7e200d790da17689caa672bd3e965452b6c

scoring_policy_hash
5cc3fe30c978f95e2ddbd0834eafd8963c37e0ccccb1dcc32915556577fcc76a

result_schema_hash
ecfa7bf1e1b9c9546879176bdb2891d6d4b0f984d146bba37566ab0b20c239dc

resource_schema_hash
b452efd1abbd37b581fc064783dfd9da021a1a2a897223fda8b5976e63a248bb
```

These hashes prove package integrity; they do not repair the scientific holdout defect.

## Current hard boundary

```text
package integrity                PASS
numeric seed separation          PASS
structural held-out validity     FAIL
scientific independent review    NOT COMPLETED
execution seal                   NOT ISSUED
persistent STARTED               NOT CREATED
formal capability                NOT OPENED
formal scorer                    NOT RUN
```

## Required correction path

Because formal capability has not started, this is a pre-start protocol correction, not a post-hoc repair.

1. Retire `cx01-candidate-001` / seeds `269810..269819` as exposed pre-start material.
2. Do not alter `freeze/cx01-001`; retain it as the rejected freeze/package record.
3. Create a new source revision whose formal world generation genuinely varies preregistered topology/timing/contingency parameters while preserving family identifiability and shared fairness semantics.
4. Freeze that new exact source SHA.
5. Select a new disjoint candidate seed band.
6. Generate a new outcome-blind package and submit that package to genuine independent review.

No seal or STARTED marker may be issued for candidate-001.
