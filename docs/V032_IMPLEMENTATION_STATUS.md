# SparkBrain v0.3.2 development implementation status

## Boundary

The checked-in package is `0.3.2.dev0`. The accepted `sparkbrain.v03` API, persisted schema `0.2`,
C18 additive schema `0.3`, protected scientific artifacts, and v0.3.1 release evidence remain
unchanged. This development commit does not create a public or re-signed release candidate.

## Integrated corrective APIs

- `sparkbrain.v032.attribution_metrics` counts cited decisions, citation IDs, active citation IDs,
  and causal-removal decisions separately and fails closed on inconsistent inputs.
- `revision_metrics` separates proposed and accepted revision behavior.
- `action_mismatch_rate` rejects unequal sequence lengths instead of truncating with `zip`.
- `disable_loser_residual_only` supports the actual C15 `RevisionBeliefField`; it rejects the
  generic `PersistentBeliefField`, whose current rule cannot provide a pure loser-only ablation.
- `IntegratedV032Brain` preserves the v0.3 keyword arguments and exposes the actual sensory
  channel trace without class-global monkeypatching.
- `DirectCheckpointManager` saves the default integrated runtime without history replay, uses an
  exact class registry, binds the envelope hash, writes with atomic no-clobber publication, and
  verifies restored state. It is for trusted local files, not hostile input.
- `RelationAwareLocalInterpreter` is a truth-free, uncalibrated local diagnostic scaffold. It is
  not evidence of semantic understanding and is not the accepted C19 adapter.
- release groups use a native no-replace directory rename on Linux, macOS, and Windows. A failed
  post-publish validation directory is retained for audit rather than deleted by path.

## Intake corrections

The supplied ChatGPT ZIP was treated as implementation input, not as an authoritative release.
Its outer checksum was valid, but its embedded source/package manifests described the v0.3.1 base
and did not cover the overlay. The supplied focused tests passed, while its Engineering test tier
failed and its overall status was `ok: false`.

The following transport-only files and manifest-bypassing wrapper were intentionally not merged:

- `PRIVATE_REVIEW_NOTICE.txt`
- `REVIEW_BUNDLE_MANIFEST.json`
- `SOURCE_MANIFEST.json`
- `CHATGPT_DEVELOPMENT_BUILD.md`
- the replacement `scripts/run_tests.py` and `scripts/run_tests_core.py`

The current test-tier wrapper remains authoritative. New manifests must be generated from a clean
integrated commit; stale delivery manifests are never used as release evidence.

## Verification and repository transport

Fast and Engineering remain the normal development gates. v0.3.2 runtime and direct-checkpoint
tests are marked Integration; native publication tests are marked Slow + Reproduction; metric and
input-semantics contracts remain Fast. The current collection has 892 tests (Fast 469,
Engineering 502, Scientific 156, Release 892).

Three protected scientific artifacts exceed GitHub's ordinary object-size guidance or hard limit.
Their exact paths are tracked with Git LFS so their checked-out bytes and scientific hashes remain
unchanged. Only local `main` commits above `origin/main` are migrated; unrelated worktree branches
are not moved or rewritten.

## Scientific status

No scientific claim grade changes. External generalization, autonomous semantic formation,
functional concept formation, functional organ formation, and residual superiority remain
unsupported or unevaluated. C19 remains blocked.
