# C06 External Validation Foundation Plan

## Gate and scope

- Base commit: `c96635a8577ac5e5f371df67ef4f0e4d0b5fffb4` from a clean integration tree.
- Branch/worktree: `codex/c06-external-validation` / `C:\55_personal\sikou\sparkbrain-c06`.
- Implement only the model-independent foundation that can precede C04/C05 integration.
- Do not clone, import, copy, or execute the upstream Belief-R GitHub code.
- Do not add model glue or produce performance claims while the C04/C05 gate is closed.

## Implementation sequence

1. Extend the C02 Episode contract with recursive evaluator-field leakage detection and a
   train split needed only for locally generated Track B data.
2. Add a pinned official Belief-R dataset specification and a verify-only-by-default local
   cache adapter with size, SHA-256, CSV header, and sequential-pair validation.
3. Map official test pairs to C02 Observation/Target episodes while keeping answers in the
   evaluator-owned Target only.
4. Add a seeded symbolic non-monotonic generator, an independent forward-chaining oracle,
   and template-family train/dev/test group splits.
5. Add target-blind order, delay, duplicate-restatement, correlated-source, and irrelevant
   distractor transforms.
6. Add model-independent metrics, error categories, and evidence remove/replace
   intervention primitives.
7. Document licensing, cache boundaries, offline operation, test-only restrictions, and the
   explicit C04/C05 model-evaluation gate.
8. Run focused tests, full tests, Ruff, local readiness, and pinned-cache verification.

## Acceptance evidence

| Contract | Evidence |
| --- | --- |
| Official immutable source | full HF revision, real file SHA-256/size, exact header/count config |
| No silent network | verify-only default and network-block unit tests |
| Atomic non-overwrite cache | verified temporary file plus exclusive hard-link publication test |
| No dataset redistribution | `data/external/` and `.cache/external/` ignored; no official rows in fixtures |
| Test-only discipline | adapter rejects non-test filename/split and exposes no train/dev partition |
| Sequential pair integrity | every `time_t1` resolves to exactly one `time_t`; pinned pair/update counts |
| Target isolation | evaluator-only Target plus recursive nested metadata leakage test |
| Track B generalization | seeded oracle episodes and disjoint template-family group split tests |
| Track C blindness | transform API accepts observations only and returns evaluator mapping |
| C04/C05 dependency | explicit failing gate until both integrations are available |

## Excluded work

- Learned encoders, learned routing, neural baselines, prompt tuning, and model execution.
- Training or tuning on Belief-R.
- Splitting Belief-R into development subsets.
- Redistribution of Belief-R text or reuse of the unlicensed upstream GitHub code.
- External performance results or claim-grade changes.
