# Security and privacy review

## Local execution boundary

The reference engine uses no remote API, telemetry, hosted storage, or mandatory network client. Brain Lab rejects non-loopback host configuration, bundles its static assets, confines exports to its configured artifact root, applies a 25 MiB import limit, and validates nested bundle structure before run creation.

## External data

Belief-R and any other third-party text are acquired only during explicit setup into data/external or .cache/external. Both are excluded from Git and release manifests. Checksums and pinned revisions authenticate expected inputs; they do not make untrusted text safe. External text is never embedded into report or release artifacts by the C10 generator.

## Checkpoints and deserialization

Reference checkpoints are validated JSON. Learned PyTorch checkpoints load on CPU with weights_only=True and must match the declared schema/backend before model construction. A C05 checkpoint is not release evidence until its input dimension is bound to a hashed, dev-only encoder vocabulary/feature manifest and restored predictions are verified. Do not bypass this boundary for unknown checkpoints. Package installation and archive extraction remain supply-chain boundaries.

## Data handling

Brain Lab exports may contain user-injected evidence text and traces. They stay in explicit local paths. The project does not provide automatic deletion, encryption, access control, or multi-user isolation; operators own local retention and filesystem permissions.

## Release controls

Manifest enumeration excludes external caches and symlinks. Archive construction refuses while the project license is unselected and verifies all manifest hashes first. No credential, environment file, browser session, or secret belongs in a release artifact.
