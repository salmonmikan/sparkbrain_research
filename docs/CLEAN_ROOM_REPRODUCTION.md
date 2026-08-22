# Clean-room CPU reproduction

## Setup boundary

Python/package acquisition may use the network. The tested candidate snapshot is requirements-release.lock; provenance and platform limitations are recorded separately. External dataset acquisition is separate and not needed by the primary smoke subset.

## Offline command

python scripts/reproduce_release.py --offline --output <EMPTY_LOCAL_DIRECTORY>

The command uses only repository files, verifies input hashes, runs local readiness, writes two generated products plus run_manifest.json, and records no network operations. The output path must be explicit and should be outside the tracked release tree for independent evaluation.

## Expected result

The result is status pass and exact output hashes matching artifacts/release/primary_subset.json. Timing and platform fields are descriptive and are not hash-frozen.

## Full versus smoke

The frozen primary subset is deliberately small. It is not the full C02 suite, C04 training, matched C05 baselines, external C06 evaluation, C07 multi-world study, or C08 exploration.
