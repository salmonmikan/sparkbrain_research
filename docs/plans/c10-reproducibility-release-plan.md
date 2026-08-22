# C10 reproducibility and release plan

## Scope and dependency gate

C10 packages the accepted C01-C09 results; it does not manufacture new positive claims. The
release candidate may be assembled before C04-C08 finish, but the final manifest, report,
claim audit, archive, tag, and clean-room result are generated only from their integrated
commits. C08 is exploratory and may remain a documented negative result.

The repository currently contains `LICENSE_NOT_SELECTED.md`. Until the owner selects a
project license, the validator must report the release as blocked and no public release tag or
archive may be described as redistributable. Third-party package and dataset licenses remain
separate from this project-license decision.

## Implementation

1. Add deterministic release-manifest tooling that enumerates tracked release files, excludes
   the self-referential manifest and local/external caches, and records path, byte size, SHA-256,
   Git revision, platform, artifact class, and generated timestamp supplied by the caller.
2. Add a release validator for required artifacts, immutable experiment manifests, raw-to-
   table/figure provenance, claim-to-run links, license state, third-party notices, privacy and
   security review, SBOM, archive checksum, negative-results appendix, and offline smoke entry.
3. Add a single CPU smoke reproduction command. It runs readiness and validation, reproduces a
   bounded primary table/figure subset from committed raw inputs, checks exact hashes or frozen
   numerical tolerances, and writes a machine-readable run manifest to an explicit output path.
4. Pin supported environments with reproducible lock or constraint files and document the
   tested Windows/Linux Python matrix. Optional learned, lab, and spiking stacks stay outside the
   dependency-free reference core.
5. Build the technical report, system/model cards, artifact-evaluation guide, third-party
   notices, security/privacy review, SBOM, negative-result appendix, and release checklist from
   accepted evidence. Every conclusion must resolve to `CLAIMS_REGISTER.md` and exact run IDs.
6. Generate the final package manifest and archive only after all selected results and report
   source are frozen. Verify the archive in a new local environment with networking blocked
   after setup/data acquisition.

## Verification

- Unit tests cover stable enumeration, hash mismatch, untracked/external-data rejection,
  missing evidence links, license-blocked state, and offline command construction.
- `python scripts/local_readiness_check.py`, the complete test suite, Ruff, prior-art validator,
  bundle validator, and release validator pass from the integrated tree.
- A clean-room CPU smoke run reproduces the selected table/figure subset within documented
  tolerance and emits a manifest containing source revision, input hashes, command, versions,
  duration, and output hashes.
- The final release remains blocked unless a project license has actually been selected; no
  inferred license or silent replacement of `LICENSE_NOT_SELECTED.md` is permitted.
