# Bounded G0 admission instrumentation: source-only remediation

Status: prospective software preparation. No new execution freeze, identity, approval,
native model import, constructor or research trajectory is created by this change.

## Motivation and preserved failure

The one-shot `assembly-m1-g0-v1-20261002` attempt is consumed. Its incomplete result,
original 199 files, exact source copies and independent data-only audit are preserved
by [PR193](https://github.com/salmonmikan/sparkbrain_research/pull/193) and the
[failure report](assembly_m1_g0_v1_failed_20261002.md). Exit 137 and absent terminal
records do not establish the causal resource trigger or furthest executed instruction.

Source inspection found repeated full permit/environment validation under an active
profiler, including a 15,221-file dependency census, and pathlib-based source-key work
on every Python/C profile event. These are concrete overhead hazards. This software
change does not retrospectively prove why that attempt terminated.

## Minimal boundary

Strict source, environment, approval and permit checks occur before profiler activation,
with bounded resource checks during lengthy scans. The resulting short-lived admitted
context is bound to the already consumed permit, exact root/freeze/approval and budget;
it is not independent execution authority. Its loader lifecycle is single-use and
thread-bound, with failure/exit invalidation. Runtime-admission transitions reject
finalizing budgets; terminal reserves are intended for cleanup and evidence only.

Immediately before native imports and after imports, explicit source/freeze/approval
integrity checks retain the trusted source-tree boundary without repeating the complete
dependency census inside every loader/constructor. The existing source-registry audit
remains an explicit post-import boundary. That historically pinned audit is a
coarser stage bracketed by budget checks; its individual reads and directory traversal
are not newly checkpointed, so arbitrary malformed trees have no new per-read bound. A final
unprofiled strict dependency check before a success verdict detects persistent
end-state drift under the normal soft budget. It does not replace the former timing
of a full post-import/pre-model census or detect transient mutations.
These checks do not claim atomic prevention
of concurrent file mutation; the dedicated, quiescent trusted-process assumptions
remain necessary. Any future execution must separately bind exact runtime/environment
bytes and reconsider those assumptions.

The code-key cache retains exact code-object identity and bounded references, not frames,
closures or instances under the existing trusted-process assumption. It caches only existing source-route classification. It does not
change native route admission or silently exempt new native calls, RNGs, locks or shell
allocations. Generated dataclass methods and other stdlib code retain their existing
classification; this is not a new arbitrary in-memory monkeypatch attestation system.

Budget checks are finite, nonrecursive and independent of output production where long
admission work requires them. No unrestricted profiler-event filesystem polling,
background timer, increased cap or zero-gap real-time guarantee is introduced.

## Historical and current-main reconciliation

This preparation starts from exact main
`f75f89f2734862dced6fc97bc23fd65a90089fb6`; all 1,290 baseline file blobs were independently
matched before edits. The later main merge
`5479f2bd8c2c0ee692f4757b50b231bc4db35d2b` (PR191) was explicitly reconciled by
matching its 21 changed file blobs. Those path-pilot documents, artifacts, scripts and
tests have no overlap with the four remediation files and change no runtime source.
Combined model-free validation covers both preparations without adopting the pilot
contract or granting it execution authority. The consumed run instead used historical source
`0a9a5123b1645fc462f95de8caddb8170b1020c5` from intentionally non-merging PR192, with
runtime rooted at `b9caed4797c9cd8217361b6e523864aabdd4cbcc`.

Current main contains the later `_MutableConcept` checkpoint registry compatibility
fix and its historical-fixture test support. It is not interchangeable with the old
frozen runtime. PR192's pointer/generation guard and native-rollback-equivalence
clarification also remain a separate historical branch delta. This preparation does
not retroactively rewrite those files, adopt a runtime for a future experiment, or
make an old freeze validate changed bytes. Historical source verification must keep
rejecting a mismatched current tree.

A future G0 or three-observation consumer must deliberately select and review the
complete source delta, including that pointer boundary and codec compatibility,
then receive a separate fresh prospective freeze and execution decision. The consumed
v1 identity is never reused, even if later preparation is successful.

## Validation scope

Required validation is synthetic/inert only: admitted-context lifecycle and cross-root
rejection; source/approval mutation; cache identity reuse/cap and unknown native routes;
long no-output scan reserve exhaustion; finalization poisoning; and scaling checks
that count expensive classification/census work rather than claim model speedup.
Independent review must cover admission-to-import drift, cache false negatives,
resource/birth accounting and terminal reserves. No native execution follows from
software tests, CI or source review alone.


## Completed source-only checks

- Independent review found no unresolved admission, cache, hook-cleanup or reserve-boundary
  issue in the exact four changed code/test files
- The six G0 suites passed 463 tests and 13 subtests
- After explicit PR191 reconciliation, all twelve G0/path-pilot suites passed 855 tests
  and 13 subtests with a native-import tripwire; full-tree Ruff passed
- Regression tests and independent adversarial probes covered warmed unknown lock/shell routes, code-identity
  mismatch, no-output soft-limit stopping, and callback failure at context-exit entry
- A two-thread observer-failure probe confirmed sticky failure, current/future hook
  detachment, zero admitted synthetic bodies, and cache cleanup
- The historical execution freeze still rejects changed current bytes; no historical
  freeze, runtime source, approval, ledger or consumed output was rewritten

The independent review covers the four remediation files; it does not independently
review the incoming PR191 pilot logic. The combined test run is reported separately.

These are software validation results, not a measured native model speedup or a cause
attribution for the incomplete run. The full local runtime suite was not run in this
source-only scope; ordinary CI remains a separate required software gate. Validation
metadata is in the [source-only validation record](../../artifacts/research/g0_admission_remediation_20261002/validation.json).
