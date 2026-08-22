# C09 — Systematic Prior-Art and Novelty Boundary Audit

## Goal

Turn the initial gap analysis into a traceable, reproducible literature matrix that identifies the strongest precedent for every proposed contribution and prevents unsupported novelty claims.

## Local-only contract

- Required outputs must run on one general-purpose local computer.
- Keep a CPU-runnable reference or reduced configuration. Local GPU use is optional.
- Do not introduce a mandatory cloud service, remote model API, hosted database, remote queue, or SaaS login.
- Runtime data, checkpoints, traces, and reports stay in explicit local paths.
- After dependencies/data are installed, the task's primary smoke/reproduction path must run offline.
- Dedicated neuromorphic hardware belongs to Extension H and is not an acceptance requirement.
- Run `python scripts/local_readiness_check.py` before completion.

## Independence

May start immediately and run continuously. Prefer a separate documentation branch/worktree to avoid code conflicts.

## Search families

At minimum cover:

- Global Workspace Theory / Global Neuronal Workspace / LIDA;
- Dynamic Field Theory and neural fields;
- Recurrent Independent Mechanisms and shared workspaces;
- Adaptive Resonance Theory and resonance/reset systems;
- predictive coding / active inference relevant to competing hypotheses;
- attractor networks and hypothesis persistence;
- blackboard/cognitive architectures and codelets;
- cell assemblies / Assembly Calculus;
- spiking global workspace and semantic spiking cognition;
- event-driven sparse graph/neural execution;
- belief revision, non-monotonic neural reasoning, explicit belief states;
- neural theorem/probabilistic state models with competing hypotheses;
- neuromorphic dynamic fields and workspace implementations;
- workspace-like internal organization in Transformers/LLMs.

## Method

1. Define dated search strings and databases.
2. Prefer primary papers and official implementation docs.
3. Record title, authors, year, venue/status, URL/DOI, code, license, benchmark, mechanism, exact overlap, exact non-overlap, and confidence.
4. Use backward and forward citation chaining for the strongest matches.
5. Search terminology variants rather than only “Spark” or “Coalition.”
6. Distinguish:
   - not retrieved;
   - retrieved but inaccessible;
   - reviewed and not matching;
   - partial overlap;
   - near duplicate;
   - invalidates contribution claim.
7. Have a second pass challenge each proposed novelty claim with the strongest counterexample.

## Outputs

- `docs/research/literature_matrix.csv`
- `docs/research/search_log.md`
- `docs/research/closest_systems.md`
- updated `PRIOR_ART_GAP_ANALYSIS.md`
- updated `SOURCES.md`
- claim-by-claim novelty verdicts in `CLAIMS_REGISTER.md`
- implementation/license notes for reproducible precedents

## Acceptance criteria

- every proposed contribution has at least one strongest competing precedent;
- every source-backed claim has a primary citation;
- search dates and strings are retained;
- preprints and peer-reviewed work are labeled;
- no “does not exist” conclusion is made from absence in search;
- near-duplicate architectures trigger reframing rather than concealment;
- initial conclusions can be regenerated from the matrix.

## Non-goals

- proving universal novelty;
- relying on blogs/search snippets as decisive evidence;
- citation count as a quality proxy;
- changing code solely to manufacture a superficial naming difference.
