# Artifact evaluation guide

## Candidate status

The non-license release preparation passes in both repository mode and standalone no-`.git`
archive mode. This establishes deterministic reproduction of the bounded primary smoke subset,
not the full C02-C08 evaluation or independent scientific replication. C01-C10 evidence is
integrated. Public readiness remains blocked by the owner project-license decision represented by
`LICENSE_NOT_SELECTED.md`. C05/C06 checkpoint evidence includes a dev-only encoder vocabulary
hash and input-dimension validation; its external outcome remains negative. C08 causal
specialization also remains negative, and CL-007/CL-008 remain E0.

## Fast offline evaluation

1. Acquire/install the pinned environment while network access is allowed.
2. Disconnect or block network access.
3. Run python scripts/reproduce_release.py --offline --output <LOCAL_OUTPUT>.
4. Confirm run_manifest.json status is pass, offline_mode is true, and network_operations is empty.
5. Confirm primary_subset_is_full_evaluation is false.
6. Run python scripts/validate_release.py --preparation-only and confirm preparation_status is
   pass while public status is blocked only by the owner license decision.

## Evidence review

- artifacts/release/evidence_map.json maps claims to run IDs and files.
- artifacts/release/provenance.json maps generated products to raw/aggregate inputs.
- docs/NEGATIVE_RESULTS_APPENDIX.md indexes retained failures.
- artifacts/release/claim_audit.json records public-text checks and pending evidence.
- PACKAGE_MANIFEST.json records tracked-file hashes and classes.
- Archive mode verifies fixed release metadata and PACKAGE_MANIFEST.json without Git.
- A private review ZIP uses REVIEW_BUNDLE_MANIFEST.json as its exact content authority and an
  adjacent SHA-256 sidecar; it is not validated as a public release archive.

## Full runs

The smoke command does not replace C02 37,000-episode generation, C04 training, C05/C06 execution, optional C07 execution, or C08 structural evaluation. Use the exact commands in each phase report/config and compare their immutable manifests.

## Acceptance interpretation

A passing smoke demonstrates local deterministic artifact regeneration from committed inputs. It is not independent scientific replication and does not raise an evidence grade.
