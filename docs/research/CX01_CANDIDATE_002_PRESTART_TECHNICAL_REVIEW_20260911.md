# CX01 candidate-002 pre-start technical review — 2026-09-11

## Disposition

**PRESTART DISPOSITION: `RETURN_SOURCE_ONLY`**

**AUTOMATED PACKAGE/CONTROL-PLANE CHECKS: PASS**

**INDEPENDENT HUMAN REVIEW: NOT YET RECORDED**

**EXECUTION AUTHORITY: NOT GRANTED**

`RETURN_SOURCE_ONLY` is deliberate. The package has passed the available outcome-blind technical checks, but repository policy requires a genuine independent reviewer other than the freeze builder and explicitly does not permit this assistant or its automated workflow to substitute for that reviewer. Therefore this record is not an `APPROVE_PRESTART` disposition, is not an execution seal, and must not be used to claim seal readiness.

No comparator capability is executed, no formal result is inspected, no execution seal is issued, no `STARTED` state is created, and no scoring occurs.

## Immutable candidate/package identities

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

The `freeze/cx01-002-source` branch is only a convenience pointer. Any later review, seal or formal runner must bind directly to the exact source SHA above.

## Automated exact-source checks completed

The read-only review workflow checks out the exact frozen source rather than executing from the review branch. It verifies, without opening formal capability:

1. candidate-001 rejected freeze identity and preserved package commit;
2. exact candidate-002 frozen source identity;
3. Ruff and the complete `tests/cx01` suite on that exact source;
4. permanent rejection of candidate-001 generation/seed band and formal validity of candidate-002;
5. candidate-001 → candidate-002 execution/scoring contract continuity, with the explicit protocol v1 → v2 revision recorded separately;
6. independent regeneration of the complete candidate-002 outcome-blind package;
7. byte identity of every regenerated package file against the preserved package commit;
8. absence of `execution_seal.json`, `STARTED`, and `results.jsonl`;
9. a complete-file-set machine scan over the candidate generator source for direct result/execution material.

The generator source set scanned by the workflow is:

- `candidate.py`
- `formal_revision.py`
- `formal_worlds.py`
- `structural_components.py`
- `development.py`
- `prepare.py`

The workflow records SHA-256 identities for that source set. This machine scan is a fail-closed guard only. It does **not** claim that a literal-string scan can prove absence of comparator-specific or success-directed semantic tuning.

## Package boundary

The preserved outcome-blind package contains exactly:

- `OUTCOME_BLIND`
- `candidate.json`
- `declarations.jsonl`
- `freeze_manifest.json`
- `package_checksums.json`
- `package_status.json`
- `structural_novelty_audit.json`
- `world_grid.json`

It contains 60 worlds and 420 unscored declarations. The immutable generated status remains `candidate_consumed=false`, `formal_capability_executed=false`, `formal_score_present=false`, `execution_seal_status=NOT_ISSUED`, `formal_status=NOT_STARTED`, and `independent_review_status=PENDING`.

The generated `PENDING` provenance is intentionally not rewritten after later review activity.

## Execution/scoring contract continuity

Candidate-002 intentionally changes the protocol identifier from candidate-001 v1 to v2. The automated reconstruction verifies that these inherited execution/scoring fields remain unchanged:

- development grid hash;
- comparator inventory;
- privilege inventory;
- schedule policy;
- scoring policy;
- result schema;
- resource schema;
- execution command;
- artifact root.

No formal outcome existed during these checks.

## Remaining independent-review requirement

Before this candidate can receive `APPROVE_PRESTART`, a genuine independent reviewer must durably record the review required by the CX01 runbook, including semantic inspection of the complete candidate/world generator for comparator-specific or success-directed tuning. The reviewer must be independent of the freeze builder; this assistant and its automation do not satisfy that role.

That human review must either record `APPROVE_PRESTART`, `REJECT_PRESTART`, or `RETURN_SOURCE_ONLY` and bind the disposition to the exact candidate/source/package identities above.

## Formal boundary

There are now **two** distinct unresolved gates, in order:

1. independent human pre-start review and durable disposition for `cx01-candidate-002`;
2. if and only if that review records `APPROVE_PRESTART`, explicit candidate-specific user authorization for one-way formal execution.

Until both gates are satisfied, the correct state remains:

```text
candidate:                    cx01-candidate-002
package:                      frozen outcome-blind
formal capability executed:  false
execution seal:              NOT ISSUED
formal status:               NOT_STARTED
pre-start disposition:       RETURN_SOURCE_ONLY
```

No past blanket approval is authority for this candidate.
