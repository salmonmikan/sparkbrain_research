# V061 A01 MD-002 N3 source provenance audit

Date: 2026-09-12  
Status: **AUDIT FINDING / EXECUTION DISABLED / EVIDENCE UNCHANGED**

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

## Negative provenance finding

During this audit, the repository's public GitHub commit endpoint could not resolve the recorded source commit:

```text
201ebd512cdee6365bd186e3ff0627ba784677cd
```

A direct commit lookup returned `No commit found for SHA`, and a contents lookup using that SHA as a ref likewise returned no commit/ref. Therefore this audit cannot truthfully declare that the original N3 source commit is currently reachable from the public repository history.

This is a provenance/reproducibility gap, not evidence that the retained N3 result is invalid. The accepted result and its source-manifest hashes remain preserved. It does mean that MD-002 must not treat `201ebd...` as a presently verified fetchable source anchor.

## What may and may not be inferred

The following remain legitimate retained facts:

- the execution pin records the source SHA and source-manifest SHA-256 values above;
- the N3 preregistration fixes the behavioral equations, seed `12001`, 36-case matrix, and development-only interpretation;
- the accepted independent result audit records a complete 36-case / 72-row narrow development result;
- full resource matching and full MD-002 remain unevaluated.

The following are **not** established by this audit:

- that the current branch version of `recurrent_adapter.py` or `recurrent_development.py` is byte-identical to the accepted source;
- that the missing `201ebd...` commit can be reconstructed merely from its SHA string;
- that an existing mutable branch may be relabeled as the historical source commit;
- that a reconstructed source, even if hash-matched, retroactively restores the original Git commit ancestry;
- that the accepted N3 result authorizes any new MD-002 execution.

## Fail-closed MD-002 rule

The MD-002 binding remains execution-disabled until exact N3 source identity is resolved prospectively and reviewably. The allowed recovery paths are:

1. **Original-source recovery:** the exact `201ebd...` commit becomes resolvable/reachable without rewriting or force-moving preserved history, and its relevant files are revalidated against the retained execution-pin SHA-256 manifest; or
2. **Prospective reconstruction:** exact file contents are independently reconstructed and verified byte-for-byte against the retained source-manifest SHA-256 values, then frozen under a **new prospective MD-002 source identity**. Such a source must explicitly state that it is a reconstruction verified against the retained `N3-DEV-001` manifest; it must not claim to be the original Git commit or inherit the original commit ancestry by assertion.

Any prospective reconstruction must keep the accepted N3 result immutable and must not use result inspection to tune equations, hyperparameters, matrix identity, or source content. If any required manifest hash cannot be matched, source identity remains unresolved.

## Governance status

The user's standing human-review-only waiver does not cure this provenance gap: it permits progression through human-review-only governance stops, but it does not convert an unresolved source identity into verified evidence and it grants no formal execution authority.

Accordingly:

```text
independent_human_review_required_as_a_stop = waived_by_user
source_identity_verified                    = false
accepted_n3_evidence_modified               = false
md002_execution_allowed                     = false
formal_execution_allowed                    = false
```

The next safe action is source reconstruction/verification or original-source recovery, followed by a separate immutable prospective source binding. No MD-002 capability execution should occur before that step is complete.
