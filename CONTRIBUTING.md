# Contributing to SparkBrain Research v0.2.1

Read `AGENTS.md` and `docs/LOCAL_EXECUTION_POLICY.md` before making changes. Contributions are evaluated on scientific traceability, software quality, and whether the core remains runnable on one local machine.

## Change types

- theory changes require equations/invariants, plain-language mapping, code mapping, and falsification tests;
- engine changes require deterministic tests and trace compatibility notes;
- experiment changes require split/seed/manifest documentation and local data paths;
- visual changes must remain faithful to recorded state and avoid mandatory remote assets;
- claim changes require a `CLAIMS_REGISTER.md` evidence-grade review;
- learned/spiking changes require a CPU-runnable reduced configuration;
- dedicated-hardware work belongs to Extension H and must be isolated from core acceptance criteria.

## Pull request checklist

- [ ] scoped task or issue referenced
- [ ] `python scripts/local_readiness_check.py` passes
- [ ] tests added and passing
- [ ] ruff passes
- [ ] generated artifacts reproduced locally
- [ ] raw results/configs retained in explicit local paths
- [ ] status and results ledger updated
- [ ] negative findings included
- [ ] no unsupported research claim
- [ ] no mandatory cloud/API/SaaS runtime dependency
- [ ] static or localhost UI remains offline-capable
- [ ] dependency and license impact documented
- [ ] formal theory, beginner guide, and glossary remain consistent where terminology changed

Do not bundle theory changes, UI redesign, and benchmark retuning into one pull request.
