# CX01 candidate-002 pre-start technical review — 2026-09-11

## Disposition

**INDEPENDENT PACKAGE-LEVEL TECHNICAL REVIEW: PASS**

**EXECUTION AUTHORITY: NOT GRANTED**

This review is outcome-blind and does not execute comparator capability, inspect a formal result, issue an execution seal, create `STARTED`, or score candidate-002. It reviews the already preserved pre-start package on `prepare/cx01-candidate-002` and leaves that package unchanged.

The next boundary remains explicit user authorization for the named candidate `cx01-candidate-002`. Until that authorization exists, one-way formal execution is prohibited.

## Reviewed immutable identities

- candidate: `cx01-candidate-002`
- candidate seeds: `370110..370119`
- protocol: `cx01-comparator-protocol-2`
- authoritative frozen source SHA: `e8483968ce43076b4c3fd04c76e62106e2031769`
- pre-start package commit: `c104be281285d52a732d5366fe36209d5688d973`
- freeze manifest file SHA-256: `3d2297790529610fd85516565e797c5443d7fec1eba5b5542ef75000becb198e`
- canonical freeze-manifest hash: `18f88a6285b23fef920ee8f040787ffc3543348268b3cd5316f6fb1cf7f0ee6a`
- candidate specification hash: `5b51b5ac53a66b0ca79939c9eff976b53c75477ba38fd77547e2bd3858d095c8`
- candidate grid hash: `0c6849a823c4befcd5a3071a4755dbcadcdb88ec8fc072da0713415adc12e3ce`
- declaration bundle hash: `ca21263f60d6e1c2d78f64ed1d628fde123f48355af3eb3a519b037a3068e537`

The branch `freeze/cx01-002-source` is a convenience pointer, not the authority for identity. It is not protected against branch movement. Any later seal, `STARTED` transition, or formal runner must compare the current checked-out Git commit directly with the exact source SHA above and refuse execution on any mismatch. A branch name alone is never sufficient.

The canonical manifest hash above is the SHA-256 of the manifest state serialized with sorted keys and compact JSON separators, matching `FreezeManifest.manifest_hash()` semantics. It is recorded before any formal outcome exists so a later seal can be checked against a fixed reviewed value rather than reconstructed after outcomes exist.

## Independent reconstruction

The review branch contains a read-only independent workflow that checks out the exact frozen source SHA rather than the review branch's source tree. Successful run `34554376533` performed all of the following without opening formal capability:

1. verified the rejected candidate-001 freeze still resolves to its recorded immutable commit and that its preserved package commit exists;
2. checked out exact candidate-002 source `e8483968ce43076b4c3fd04c76e62106e2031769`;
3. ran CX01 Ruff checks and the complete `tests/cx01` suite on that exact source;
4. revalidated that candidate-001's generation/seed band remains rejected and candidate-002 remains a valid fresh formal candidate;
5. rechecked candidate-001 → candidate-002 execution/scoring contract continuity, treating protocol v1 → v2 as the explicit registered revision rather than hiding it as an unchanged field;
6. independently regenerated candidate-002's complete outcome-blind package from the exact frozen source;
7. byte-compared every regenerated package file against the preserved package commit `c104be281285d52a732d5366fe36209d5688d973`;
8. confirmed the reconstructed inventory contains no `execution_seal.json`, `STARTED`, or `results.jsonl`;
9. applied a source-only guard against direct result/execution material in the candidate/formal-revision generator source.

All nine stages completed successfully. The first review-run attempt had one false-positive source scan because the string `capability_result_present` is an intentional fail-closed outcome-blind schema field. The scan was narrowed to actual execution/result material and the complete independent review then passed; no candidate, frozen package, scoring rule, world grid, or source SHA was altered by that correction.

## Package completeness and no-start boundary

The preserved package inventory contains exactly the expected outcome-blind material:

- `OUTCOME_BLIND`
- `candidate.json`
- `declarations.jsonl`
- `freeze_manifest.json`
- `package_checksums.json`
- `package_status.json`
- `structural_novelty_audit.json`
- `world_grid.json`

No `execution_seal.json`, `STARTED`, or `results.jsonl` is present in the preserved package.

The recorded package status is internally consistent with pre-start use:

- 60 worlds;
- 420 unscored declarations;
- `candidate_consumed=false`;
- `formal_capability_executed=false`;
- `formal_score_present=false`;
- `execution_seal_status=NOT_ISSUED`;
- `formal_status=NOT_STARTED`;
- `independent_review_status=PENDING` in the immutable generated provenance.

The `PENDING` value belongs to the immutable package-generation record and is not rewritten after review. This append-only review is the later independent review record; changing generated provenance would destroy rather than improve provenance fidelity.

## Contract continuity review

Candidate-002 intentionally advances the protocol identifier from candidate-001 protocol v1 to protocol v2. That revision is explicitly recorded rather than hidden as an unchanged field.

The independent reconstruction verified that the execution/scoring contract inherited from candidate-001 is unchanged for:

- development grid hash;
- comparator inventory;
- privilege inventory;
- schedule policy;
- scoring policy;
- result schema;
- resource schema;
- execution command;
- artifact root.

No outcome-dependent contract change is visible in the preserved package, and no formal outcome existed during this review.

## Structural holdout review

The packaged structural audit reports:

- 60 / 60 worlds passing canonical structural review;
- 10 unique full structures in each of the six formal families;
- zero development full-structure overlap in every family;
- component structural audit `passed=true` with no recorded violations;
- formal generator revision `cx01-formal-structural-revision-v4`;
- family-identifiability pass counts of 10 / 10 for every family.

Some component axes are intentionally non-applicable to particular families and may therefore overlap development on that non-applicable axis. The packaged policy marks those axes as `novelty_required=false`; this is not treated as hidden full-structure reuse. Full structures remain novel under the registered audit.

## Checksum and byte-identity review

The package checksum manifest binds the seven payload files (excluding the checksum file itself), including:

- `declarations.jsonl`: 420 records, 119680 bytes;
- `world_grid.json`: 60 records, 93919 bytes;
- `structural_novelty_audit.json`: 36350 bytes;
- `freeze_manifest.json`: 1406 bytes;
- `package_status.json`: 820 bytes.

The independent workflow went beyond metadata inspection: it regenerated all eight package files from exact frozen source and byte-compared each regenerated file with the preserved package commit. The complete comparison passed.

## Review limitations

This is a package/control-plane review, not a capability review. It cannot know whether any comparator will pass or fail the frozen formal scoring rule because no candidate capability output has been opened.

The source-only tuning scan is a defensive static guard, not a proof that no conceivable semantic dependence exists anywhere in repository history. The stronger protection is procedural and cryptographic: candidate-002's source SHA, candidate specification, world grid, declaration bundle, execution/scoring contract, and byte-identical pre-start package were all fixed before formal execution and independently reconstructed before any formal result exists.

This review also does not act as the user's single-use execution authorization. The automation/reviewer must not infer authorization from older blanket permissions or from this PASS disposition.

## Seal-ready handoff

No package-level blocker was found that requires modifying candidate-002 or its frozen execution/scoring contract before a seal can be considered.

If and only if the user explicitly authorizes **`cx01-candidate-002` formal execution**, the next one-way transition may bind an execution seal to:

```text
candidate:      cx01-candidate-002
source SHA:     e8483968ce43076b4c3fd04c76e62106e2031769
manifest hash:  18f88a6285b23fef920ee8f040787ffc3543348268b3cd5316f6fb1cf7f0ee6a
```

The approval digest and reviewer/authority identity must be derived from that later explicit candidate-specific approval, not invented in advance. After a valid seal, execution must remain one-way and exactly once: verify exact source SHA, create the persistent start state, execute the frozen command against the frozen source/candidate, preserve raw evidence before scoring, lock it, and apply only the frozen scoring procedure.

Until that explicit authorization is received, the correct state is **seal-ready / NOT_STARTED**.
