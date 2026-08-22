# Artifact evaluation guide

## Candidate status

The non-license release package is reproducible, and C01-C10 evidence is integrated. Public readiness remains blocked by `LICENSE_NOT_SELECTED.md`. C05/C06 checkpoint evidence includes a dev-only encoder vocabulary hash and input-dimension validation; its external outcome is negative.

## Fast offline evaluation

1. Acquire/install the pinned environment while network access is allowed.
2. Disconnect or block network access.
3. Run python scripts/reproduce_release.py --offline --output <LOCAL_OUTPUT>.
4. Confirm run_manifest.json status is pass, offline_mode is true, and network_operations is empty.
5. Confirm primary_subset_is_full_evaluation is false.

## Evidence review

- artifacts/release/evidence_map.json maps claims to run IDs and files.
- artifacts/release/provenance.json maps generated products to raw/aggregate inputs.
- docs/NEGATIVE_RESULTS_APPENDIX.md indexes retained failures.
- artifacts/release/claim_audit.json records public-text checks and pending evidence.
- PACKAGE_MANIFEST.json records tracked-file hashes and classes.

## Full runs

The smoke command does not replace C02 37,000-episode generation, C04 training, C05/C06 execution, optional C07 execution, or C08 structural evaluation. Use the exact commands in each phase report/config and compare their immutable manifests.

## Acceptance interpretation

A passing smoke demonstrates local deterministic artifact regeneration from committed inputs. It is not independent scientific replication and does not raise an evidence grade.
