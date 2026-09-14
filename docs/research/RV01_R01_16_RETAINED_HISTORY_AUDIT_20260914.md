# RV01 R01-16 retained-history completeness audit

Date: 2026-09-14  
Status: **PARTIAL AUTHORITATIVE RECONSTRUCTION; R01-16 EXECUTION REMAINS FAIL-CLOSED**

## Purpose

This audit records the currently retained RV01 evidence that must feed the R01-16 collision registry. It is intentionally conservative: no registry is marked `authoritative_complete=true` until every consumed or reserved seed/world identity can be reconstructed from durable evidence without guessing.

## Authoritative branch inspected

- branch: `research/rv01-endogenous-transition`
- exact inspected commit: `466053e8e50b05366f24d0c516dc911bec1b20a8`

## Retained evidence roots present

The inspected commit contains the retained RV01 roots:

- `artifacts/research/rv01/r01_12_postformal/`
- `artifacts/research/rv01/r01_12d/`
- `artifacts/research/rv01/r01_12f/`
- `artifacts/research/rv01/r01_13/`
- `artifacts/research/rv01/r01_14/`

These roots are evidence inputs to collision-history reconstruction; they are not disposable staging outputs.

## R01-12D development evidence

`r01_12d/development_result_manifest.json` durably binds:

- execution source `b163117512daca23b613c8a109a544833af7d360`
- 15 development worlds over five families
- comparator `seed_offset=12001`
- exact world-grid and suite hashes
- held-out capability remained closed

The manifest explicitly lists 15 development world IDs and semantic/specification hashes. These world identities are therefore known retained collision material. The compact manifest does **not** by itself provide a complete consumed/reserved seed ledger suitable for R01-16.

## R01-12F formal evidence

`r01_12f/formal_result_manifest.json` records candidate `rv01-r01-12-interference-heldout-v1` as `formal-held-out-executed-fixed` with execution policy `one-way-no-rerun`:

- workflow run `33953949771`
- frozen source `83d2c77d8ae3878727d2ed4e9e78bc169ce064b8`
- seal commit `003cc0c390d53ab3a09420b4ad61fc7bb5e9a059`
- held-out capability executed: true
- 50 held-out worlds

This formal identity is consumed and must be represented in retained collision history. It must never be rerun merely to recover bookkeeping.

## R01-13 development evidence

`r01_13/development_result_manifest.json` records:

- protocol `rv01-r01-13-activity-matched-discrimination-v1`
- source `241669c92a0fd93b1f98ffe5e5dcaf8fd97c4de2`
- status `development-fixed-heldout-closed`
- 25 worlds / 100 probes
- held-out capability remained closed
- retained raw result at `artifacts/research/rv01/r01_13/development_result.json`

The compact manifest does not expose a complete seed/world collision ledger. The raw result is retained and is an admissible source for deterministic reconstruction, but completeness must be demonstrated rather than inferred from `world_count` alone.

## R01-14 development evidence

`r01_14/development_result_manifest.json` records:

- protocol `rv01-r01-14-traversal-dynamics-v1`
- source `d0c828dda9faf1ff0d455adf02be4e9ef65030fb`
- status `development-fixed-heldout-closed`
- 25 worlds / 100 probes
- held-out capability remained closed
- retained raw result at `artifacts/research/rv01/r01_14/development_result.json`
- the historical normalized discovery AUC v1 is explicitly invalid due to an unregistered denominator

Again, the compact manifest binds the retained experiment but is insufficient by itself to assert the complete consumed/reserved seed ledger.

## R01-16 fail-closed requirement

`R0116CollisionRegistry` correctly requires all of the following before it can be accepted:

- schema `rv01-r01-16-collision-registry-v1`
- authority `repository-retained-seed-history`
- `authoritative_complete=true`
- exact lowercase SHA-256 registry identity
- sorted/unique consumed and reserved seeds/world IDs
- provenance entries bound by artifact identifiers and SHA-256
- zero overlap with every prospective R01-16 seed/world identity

The current retained manifests establish multiple mandatory evidence sources but do not yet justify setting `authoritative_complete=true` without deterministic extraction from the retained raw/provenance artifacts and any later R01-15 retained evidence.

## Decision

R01-16 remains **NOT EXECUTION-READY**. Do not freeze or execute a registry assembled only from the compact manifests above, and do not mark completeness by hand.

The next safe step is to implement a deterministic retained-history builder/verifier that reads the preserved RV01 evidence roots (including later R01-15 evidence), emits the complete consumed/reserved seed/world registry with per-source provenance hashes, and fails closed when an expected evidence class cannot expose its identities. Only after that builder independently proves completeness should the proposed fresh R01-16 identities be bound to exact source/runtime/package manifests and proceed toward freeze/seal.
