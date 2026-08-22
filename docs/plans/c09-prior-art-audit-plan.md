# C09 Prior-Art Audit Second-Pass Plan

## Objective

Complete a reproducible second-pass prior-art audit that challenges every current SparkBrain contribution candidate with the strongest retrieved precedent. Completion is falsifiable: the literature matrix must cover every required search family, retain dated queries and access states, include implementation/license evidence where available, and drive machine-checked claim-boundary outputs without treating non-retrieval as novelty.

## Current behavior

- Commit `94be973` contains a 15-record initial counterexample matrix and updates to the source, gap-analysis, and claims documents.
- `docs/research/search_log.md` explicitly leaves backward/forward citation chaining, additional databases, and official repository/license checks for a required second pass.
- Several required families are incomplete: active inference, attractor persistence, blackboard architectures beyond LIDA, probabilistic/neural competing-hypothesis systems, and neuromorphic dynamic-field/workspace implementations.
- Nearly all `code_license` fields are `not checked`; PA-015 uses provisional author metadata.
- There is no executable validator proving that contribution verdicts and closest-system conclusions remain derivable from the matrix.

## Theory contract

- This task changes claim boundaries and literature evidence, not SparkBrain dynamics equations.
- Preserve the distinction between known components, partial overlap, near duplicate, evaluation precedent, unverified integration candidate, and supported contribution.
- Do not infer novelty from an empty search result, inaccessible paper, missing code, or absence of an end-to-end duplicate.
- Spiking, workspace, coalition, persistent activity, structural plasticity, event-local graph recomputation, and belief revision all have known precedents; any remaining claim must be narrower and experimentally falsifiable.

## Implementation slices

1. Expand the dated search log with exact second-pass queries, source/index, retrieval state, and chaining relationships.
2. Add primary papers for the missing families and stronger counterexamples discovered by backward/forward chaining.
3. Verify official repositories and repository license files for selected reproducible precedents; retain `not found` or `not checked` explicitly where evidence is unavailable.
4. Correct PA-015 author/status metadata from its first-party page.
5. Add a claim-by-claim adversarial pass mapping each SparkBrain contribution candidate to its strongest retrieved counterexample and required disambiguating experiment.
6. Add a lightweight validator that checks matrix schema, unique IDs, required family coverage, primary URLs, explicit publication/access/license states, claim coverage, and consistency of generated verdict tables.
7. Regenerate the derived closest-systems verdict table from the matrix and update project-level source/claim/gap documents.

## Data and evaluation

- Data is bibliographic metadata in `docs/research/literature_matrix.csv`; no model training or human-subject data is involved.
- Retrieval date is 2026-08-23 in Asia/Tokyo.
- Each row records source family, primary URL/identifier, publication status, access state, exact overlap/non-overlap, challenged claims, verdict, and code/license state.
- The validator is deterministic and network-free. Web access is used only during research; the completed audit remains locally inspectable and validatable offline.

## Risk register

- **Scientific confound:** cherry-picking distant precedents. Mitigation: strongest-counterexample framing and citation chaining from near matches.
- **Coverage risk:** a search family is represented only by a survey. Mitigation: primary papers or official proceedings are required for matrix rows.
- **Status risk:** preprints and first-party reports are mislabeled as peer reviewed. Mitigation: explicit `publication_status` and validator-enforced non-empty status.
- **License risk:** repository existence is mistaken for reusable code. Mitigation: license URL and SPDX/name are recorded only from official repository evidence.
- **Attribution risk:** a prior paper's non-overlap is asserted more strongly than reviewed evidence supports. Mitigation: narrow wording and explicit uncertainty notes.
- **Local/offline risk:** validation depends on live URLs. Mitigation: validator checks retained metadata only and performs no network access.

## Acceptance criteria

- Every proposed contribution has at least one strongest competing precedent.
- Every source-backed claim has a primary citation.
- Search dates and strings are retained.
- Preprints and peer-reviewed work are labeled.
- No “does not exist” conclusion is made from absence in search.
- Near-duplicate architectures trigger reframing rather than concealment.
- Initial conclusions can be regenerated from the matrix.
- Second-pass citation chaining, missing-family coverage, official code/license notes, PA-015 author verification, and adversarial claim review are recorded.

## Validation commands

```powershell
.venv\Scripts\python.exe scripts\validate_prior_art_audit.py
.venv\Scripts\python.exe -m pytest -q tests\test_prior_art_audit.py
.venv\Scripts\python.exe scripts\local_readiness_check.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe scripts\validate_bundle.py
```

## Documentation updates

- `docs/research/literature_matrix.csv`
- `docs/research/search_log.md`
- `docs/research/closest_systems.md`
- `docs/research/claim_challenge_report.md`
- `docs/PRIOR_ART_GAP_ANALYSIS.md`
- `docs/SOURCES.md`
- `docs/CLAIMS_REGISTER.md`
- `docs/PROJECT_STATUS.md`

## Local execution contract

- Research retrieval uses web access during this task, but repository validation is CPU-only and offline.
- No remote API, cloud database, hosted tracker, or remote storage becomes a runtime dependency.
- All audit evidence and derived outputs remain under explicit repository paths.
- No credentials, environment files, cookies, sessions, or restricted full-text sources are accessed.

## Rollback boundary

- All changes stay on `codex/c09-prior-art-audit` in `C:\55_personal\sikou\sparkbrain-c09`.
- Revert the single scoped C09 commit to remove the second pass; no shared-main files or generated experiment results are modified.
- Existing first-pass rows remain traceable; corrections are explained in the search log rather than silently deleting prior conclusions.

## Plan updates

- 2026-08-23: initial second-pass plan created before C09 implementation edits.
- 2026-08-23: completed the bounded minimum-full audit with 23 matrix records, six covered family groups, backward/forward chains, four official repository/license checks, exact PA-015 authors, and a matrix-consistency validator. Authenticated citation-index exports and complete forward-citation enumeration remain unavailable and are recorded as uncertainty rather than evidence of novelty.
