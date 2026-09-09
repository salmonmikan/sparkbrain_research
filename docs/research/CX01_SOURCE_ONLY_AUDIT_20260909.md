# CX01 source-only audit — 2026-09-09

Disposition: **RETURN_SOURCE_ONLY**. This is an assistant source/CI review,
not independent formal approval, an execution seal, or permission to start.

## Exact observed revisions

| Branch | Observed SHA |
| --- | --- |
| research/cx01-comparator-extension | 0687c8db3efb8180c8599d32235751b93f3c1f77 |
| research/cx01-component-structural-audit | 10490ee302d3e6c540a5acc886d530250745143e |
| research/cx01-candidate-002-prestart | 24baf69324696c945b9be2b68917c1ee2467d9ee |
| freeze/cx01-001 | f2c5ead5afda7d731033d585511ea68dc066a162 |
| cx01-control/candidate-001 | e1a1d9c1435de8aaf875aa40b5e62a7f40de9732 |

The observations below refer to these revisions, not future branch state.
No formal comparator was executed, seed set selected, package regenerated,
seal issued, STARTED marker created, saved evidence modified, or branch merged.

## Observed blockers

### 1. Rejected-freeze guard mismatch

The candidate-002 workflow at 24baf693 requires rejected freeze commit
97d47af0b98ce4e34918aeed63b8e9d975e37838, while the observed freeze ref is
f2c5ead5afda7d731033d585511ea68dc066a162. Workflow run 34242645854,
job 102116470303, fails with `Rejected candidate-001 freeze moved; refusing
to continue`. Package generation, upload, source-freeze and package-preservation
steps are skipped. No complete candidate-002 package was available from this run.

Do not move the preserved freeze to satisfy the guard. Establish the intended
freeze/source/package identities from retained history before correcting a
source-only workflow constant. Current ref mismatch alone does not establish
whether a historical freeze moved or the constant was originally incorrect.

### 2. Incompatible audit return shapes

Both component and prestart prepare.py check `row.get("passed")` for all three
auditors. `audit_formal_grid_structure` and `audit_formal_grid_identifiability`
raise on failure but return successful reports without a top-level `passed`.
Thus successful reports are rejected as false by the packaging guard.

Component CI run 34237156743 confirms preparation failures. It also contains
five formal-scoring fixture failures at the CYCLE global-majority identifiability
gate; these require separate fixture/source investigation without weakening the
scientific gate.

### 3. Automated normalization did not apply

Run 34237156822, job 102097714629, failed with `expected audit block was not
found`; commit/push was skipped. The workflow's multiline replacement literal
does not match source indentation. The observed branch still contains the
original bug. This moving-branch self-modification workflow should not be used
as evidence of a completed correction.

The proposed wrapper assigning passed=true after a successful auditor call
does not swallow current auditor exceptions, but this alone is insufficient
verification. Prefer an explicit common return contract with adversarial tests.

### 4. Divergent source lines omit accepted parent protections

Parent 0687c8db contains source-SHA-bound formal seed selection and explicit
seed-selection/structure/identifiability audit freeze bindings. The component
and prestart source trees do not include formal_seed_selection.py. The reviewed
component FreezeManifest omits those new audit/selection fields. The reviewed
prestart CandidateSpec.validate does not reject protocol-v1 state.

Do not integrate by replacing the parent's files wholesale with the divergent
branch files. Preserve parent protocol-v2 protections and review component
additions against them individually. The fixed proposed candidate-002 seed band
must not silently supersede the source-bound selection policy.

### 5. Package verification is not a complete semantic audit

The divergent verify_outcome_blind_bundle implementation does not reconstruct
packaged worlds, declarations or audits from the exact source and compare them.
It trusts saved audit passed flags, and all() on an empty audit mapping is true.
It verifies listed checksums but does not require every payload to be listed.
Its forbidden set contains STARTED but not the runbook's STARTED.json.

A future source-only verifier should require an exact allowed file set, reject
symlinks and non-file payloads, ensure full checksum coverage, enforce exact
schema/status/cardinality, and compare reconstructed worlds/declarations/audits
and their freeze bindings. Tests should include updated-checksum tampering,
missing checksum entries, empty/false audit reports and STARTED.json injection.

## CI evidence boundaries

| Revision / run | Observation |
| --- | --- |
| 10490ee3 / 34237156743 | ordinary CI failed |
| 10490ee3 / 34237156822 | normalization failed; no commit |
| 24baf693 / 34242645938 | ordinary CI succeeded |
| 24baf693 / 34242645854 | prestart failed before packaging |
| 0687c8db / 34237735107 and 34237727623 | ordinary CI succeeded |
| 0687c8db / 34237735120 and 34237727660 | development workflow succeeded |

These are inspected CI records, not local validation performed by this review.
Success at the parent revision is not evidence that a future integrated source
passes. Ordinary CI success at prestart is not package-preparation success.

## Next authorized source-only task

Start from 0687c8db3efb8180c8599d32235751b93f3c1f77 on a new branch.
First preserve protocol-v2 seed/freeze protections, then introduce a separately
reviewable complete package verifier and consistent audit report contracts.
Test only reserved non-formal fixtures. Do not tune candidate-002 worlds, alter
its seeds, regenerate its package or reuse exposed candidates without a new
explicit governance decision. Preserve candidate-001 evidence unchanged.

The runbook explicitly excludes the freeze builder, model author and this
assistant as substitutes for genuine independent review. This audit cannot
supply that approval. After source completion and exact-source local/CI
validation, obtain independent review before any formal seal or STARTED.

This disposition is not REJECT_PRESTART: missing source/package evidence does
not establish a scientific rejection of candidate-002. It also does not certify
the candidate as fresh, eligible or available for reuse.

## Source links

- https://github.com/salmonmikan/sparkbrain_research/actions/runs/34242645854
- https://github.com/salmonmikan/sparkbrain_research/actions/runs/34237156743
- https://github.com/salmonmikan/sparkbrain_research/actions/runs/34237156822
- https://github.com/salmonmikan/sparkbrain_research/blob/10490ee302d3e6c540a5acc886d530250745143e/src/sparkbrain/comparison/cx01/prepare.py
- https://github.com/salmonmikan/sparkbrain_research/blob/24baf69324696c945b9be2b68917c1ee2467d9ee/.github/workflows/cx01-candidate-002-prestart.yml
- https://github.com/salmonmikan/sparkbrain_research/blob/0687c8db3efb8180c8599d32235751b93f3c1f77/docs/CX01_FORMAL_RUNBOOK.md
