# HUMAN-20260922-006 — Main stable baseline refresh

Human status: `OPEN`  
Created: `2026-09-22 JST`

### Intent

The human side wants `main` to be refreshed because its reader-facing version and status surfaces have fallen materially behind the stable substrate that already exists on `main`.

Current repository inspection shows that `main` already contains the v0.4 and v0.5 versioned runtime/specification/result surfaces, including `sparkbrain.v05`, `docs/THEORY_SPEC_v0.5.md`, and the v0.5 completion/result artifacts. However, major entrypoints such as `README.md`, `pyproject.toml`, `docs/START_HERE.md`, `docs/PROJECT_STATUS.md`, and `CHANGELOG.md` remain centered on `0.3.2.dev0` / v0.3-era framing.

This creates an undesirable state where the stable branch contains later stable research/runtime assets but presents itself to readers and tooling as if the project were still primarily v0.3.2.

The goal is **not** to make `main` chase the research frontier. The goal is to make `main` accurately represent the current stable shared substrate.

### Requested operating posture

1. Audit the current version semantics before changing metadata.
   - Distinguish package/release version, persisted schema version, research namespace version, theory-spec version, and historical evidence version.
   - Determine whether the package metadata should move from `0.3.2.dev0` to a v0.5-aligned development version or whether a different explicit versioning convention is safer.
   - Do not change a version number merely for cosmetic consistency if it would falsely imply compatibility or release status.

2. Refresh the stable reader-facing surfaces on `main` so they describe what is actually present and stable there.
   Review at minimum:
   - `README.md`
   - `pyproject.toml`
   - `docs/START_HERE.md`
   - `docs/PROJECT_STATUS.md`
   - `CHANGELOG.md`
   - repository structure / entrypoint documentation
   - references among v0.3, v0.4, and v0.5 theory/runtime documents

3. Make the relationship between versions explicit.
   A new reader looking only at `main` should be able to understand:
   - which runtimes are currently present and usable;
   - which version is the current stable baseline;
   - what v0.3, v0.4, and v0.5 each represent;
   - which scientific claims remain bounded/negative/reduced;
   - which parts are stable substrate versus active frontier research;
   - which historical schemas/artifacts remain compatibility targets.

4. Preserve the doctrine that `main` is stable shared substrate, not the latest scientific frontier.
   - Do not wholesale-merge active `research/*` branches merely to make `main` look current.
   - Do not move candidate-specific implementations, exploratory diagnostics, provisional discriminators, result-dependent mechanisms, or one-way evidence machinery into `main` unless their value is independent of the originating scientific result.

5. Re-audit post-v0.5 research for **main-promotion candidates**, but use a strict outcome-independence rule.
   A component is a promotion candidate only if it remains useful whether the originating hypothesis is positive, negative, reduced, or abandoned.
   Examples may include:
   - reusable generic runtime/tooling;
   - candidate-independent comparators;
   - generic provenance / reproducibility infrastructure;
   - stable diagnostic helpers;
   - architecture-neutral interfaces;
   - generic workflow-integrity or equivalence tooling;
   - reusable tests/fixtures.
   Candidate-specific scientific code, frozen thresholds, consumed identities, raw/scored evidence, and result-specific execution paths are excluded by default.

6. Prefer a small reviewed integration branch / PR rather than direct broad mutation of `main`.
   - Keep the refresh reviewable and separable from active science.
   - Require normal CI to be green before merge.
   - Do not merge a component that is currently known to be red, incomplete, or not promotion-ready merely because this directive exists.

### Scientific and evidence boundaries

This directive does **not** authorize rewriting scientific history or upgrading claim strength.

Preserve exactly:
- consumed one-way identities;
- immutable / evidence / preserve anchors;
- historical PASS / FAIL / INCONCLUSIVE / reduced interpretations;
- v0.3 / v0.4 / v0.5 negative boundaries;
- C19 / PD01 / NI01 / H5 and other formal evidence status;
- no-rerun / no-rescore constraints on consumed FORMAL identities.

A documentation/version refresh may summarize later evidence more accurately, but it must not retroactively convert historical research claims into stronger claims.

### Success condition

The directive is satisfied when `main`, viewed by itself, presents a coherent and current stable baseline:

> **main should be stable, but not stale.**

A reader should no longer infer that SparkBrain is still fundamentally at v0.3.2 when v0.4/v0.5 stable assets are already present, and the repository should clearly separate:
- stable baseline;
- historical versions;
- current bounded scientific status;
- active frontier research.

### Required independent review

This is a human-originated repository/product-direction directive, not scientific evidence.

Control Brain should classify it as `ACCEPT / MODIFY / DEFER / REJECT` and coordinate with Repository Steward and other appropriate workers.

If Control modifies or defers the request, it should identify the concrete compatibility, scientific-integrity, release-semantics, or repository-risk reason.

The directive should not be interpreted as authority for a wholesale research merge or automatic package-version bump without the version-semantics audit described above.
