# Contributing to SparkBrain Research

Read `AGENTS.md` before making changes. Contributions are evaluated on scientific traceability as well as software quality.

## Change types

- theory changes require equations/invariants, code mapping, and falsification tests;
- engine changes require deterministic tests and trace compatibility notes;
- experiment changes require split/seed/manifest documentation;
- visual changes must remain faithful to recorded state;
- claim changes require a `CLAIMS_REGISTER.md` evidence-grade review.

## Pull request checklist

- [ ] scoped task or issue referenced
- [ ] tests added and passing
- [ ] ruff passes
- [ ] generated artifacts reproduced
- [ ] raw results/configs retained
- [ ] status and results ledger updated
- [ ] negative findings included
- [ ] no unsupported research claim
- [ ] dependency and license impact documented

Do not bundle theory changes, UI redesign, and benchmark retuning into one pull request.
