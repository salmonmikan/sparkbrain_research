# V061 A01 MD-002 N3 source provenance audit

Date: 2026-09-12  
Status: **PRESERVED SOURCE RECOVERED / EXECUTION STILL DISABLED / EVIDENCE UNCHANGED**

## Scope

This is a read-only provenance audit of the already accepted narrow `N3-DEV-001` development record. It does not rerun N3, does not modify the retained N3 result, does not alter any frozen or preservation evidence, and does not authorize MD-002 execution.

The accepted record remains narrow: 36 cases / 72 arm rows under the preregistered local-competition adapter diagnostic. Full MD-002 and matched-resource equivalence remain `NOT_EVALUATED`.

## Preserved identity claims

`V061_A01_N3_DEV_001_EXECUTION_PIN.json` records:

```text
run_id        = N3-DEV-001
source_commit = 201ebd512cdee6365bd186e3ff0627ba784677cd
review_commit = 5cd8f43686801ceeafd87140f2daf21028c1c244
```

The same execution pin retains the source-manifest SHA-256 values used for that accepted run, including:

```text
src/sparkbrain/v061_a01/recurrent_adapter.py
  df1f3b8c3ab9bfb68c88d60af6bbfd0996c81d43511ff942698c1281f5cc8f76

src/sparkbrain/v061_a01/recurrent_development.py
  6c688a89e97fa6bc26922ea0611d30b764383382737026865dd15ccda9823539

docs/research/V061_A01_N3_DEV_001_PREREG.md
  46f7381d10b2e230668f2f5b1261e07244a03d58e415e7507c3356207443d1ba

scripts/run_a01_n3_development.py
  3a564a958c5accf9538dcd8fd812f65722369532e44ea82a9897697db10312c3
```

These retained hashes are evidence about the accepted run. This audit does not replace or rewrite them.

## Public-ref observation and preserved-bundle recovery

The repository's public GitHub commit endpoint does not resolve the recorded source commit directly:

```text
201ebd512cdee6365bd186e3ff0627ba784677cd
```

That observation alone is **not** a provenance failure. The repository already tracks an offline Git history bundle:

```text
artifacts/v061/a01/history/N3_DEV_001_history.bundle
```

Its adjacent metadata record binds:

```text
executed_source = 201ebd512cdee6365bd186e3ff0627ba784677cd
bundle_head     = 0efd8d6cc50b15882c40dc05d22cecba3033fea7
prerequisite    = c05abe90c9ef904aead27df5176d7385aa06fb64
bundle_bytes    = 111414
bundle_sha256   = f40f4a43749b310bcefc2f0efb7bbd3eeab1043b5472b9e5f7f3e85817779b75
```

Independent review of this audit fetched the tracked bundle, made the recorded source commit readable from the preserved history, and verified all 264 files against the execution pin with **zero SHA-256 mismatches**. The earlier interpretation that the source identity remained unresolved was therefore too strict: the commit lacks a public branch/ref, but its original source history is preserved in-repository and recoverable without rewriting Git history.

Accordingly, the original `N3-DEV-001` source identity is treated as recovered through the preserved bundle. No mutable branch is relabeled as the historical source and no reconstructed source is substituted for it.

## What may and may not be inferred

The following are now retained/reviewed facts:

- the execution pin records source commit `201ebd...` and its source-manifest SHA-256 values;
- the tracked history bundle metadata explicitly binds `executed_source = 201ebd...` and a bundle SHA-256;
- independent review recovered `201ebd...` from that bundle and reported zero SHA-256 mismatches across all 264 checked files;
- the N3 preregistration fixes the behavioral equations, seed `12001`, 36-case matrix, and development-only interpretation;
- the accepted independent result audit records a complete 36-case / 72-row narrow development result;
- full resource matching and full MD-002 remain unevaluated.

The following are **not** established merely by source recovery:

- that the current mutable `research/v061-a01-n3-adapter` copies are the historical source and may replace the bundle identity;
- that the accepted narrow N3 result establishes matched-resource equivalence;
- that the accepted N3 result authorizes full MD-002 execution;
- that incomplete P2/P3/P4/P5, matrix, budget, manifest, no-clobber, preservation, or authority requirements may be skipped.

## Fail-closed MD-002 rule after source recovery

The source-provenance blocker is closed, but MD-002 remains execution-disabled for the independent remaining prerequisites already recorded by the binding/status documents. Any future MD-002 source package must bind the recovered N3 source identity explicitly through the preserved bundle metadata and retained execution-pin manifest; it must not depend on a mutable branch silently standing in for `201ebd...`.

The next safe progression is therefore prospective MD-002 package completion: exact matrix/seeds/budgets/thresholds, matched-resource acceptance semantics, real P2/P3/P4/P5 completion, exact source manifest including the recovered N3 source identity, no-clobber one-shot runner, artifact/preservation schema, and final exact-head technical review.

## Governance status

The user's standing human-review-only waiver permits progression through literal reviewer-identity stops but is not needed to turn a missing public ref into evidence: source recovery is grounded in the tracked preserved bundle and its independent hash review. The waiver still grants no formal execution authority.

Accordingly:

```text
independent_human_review_required_as_a_stop = waived_by_user
n3_original_source_recovered                = true
n3_public_ref_present                       = false
accepted_n3_evidence_modified               = false
md002_execution_allowed                     = false
formal_execution_allowed                    = false
```

No N3 rerun, evidence rewrite, MD-002 capability execution, held-out execution, or formal execution is authorized by this audit.
