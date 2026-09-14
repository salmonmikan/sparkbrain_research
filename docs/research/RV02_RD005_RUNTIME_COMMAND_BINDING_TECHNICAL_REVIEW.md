# RV02 RD005 D1 runtime/command binding technical review

Date: 2026-09-14  
Scope: prospective D1 construction-only integrity review  
Execution status: **D1 NOT STARTED; capability unopened; seed 92505 unconsumed**  
Human-review status: substantive automation review under `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`; no independent human identity is claimed.

## Purpose

The prior binding audit identified two remaining prospective integrity gaps after exact source-manifest preparation: the package plan did not fail-close on its canonical digest, and the exact D1 runtime/command contract was not bound before construction. The canonical package-plan preflight is now part of the authoritative construction path. This review covers the runtime/command layer only.

## Bound construction runtime

The D1 construction runtime is prospectively fixed to:

- Python implementation: `CPython`
- Python version: `3.11.15`

`rv02_rd005_execution_binding.py` encodes this contract and exposes a deterministic SHA-256 binding. `rv02_rd005_bound_construction.py` verifies the live interpreter before it reads the construction input or delegates to the output-producing construction runner. A runtime mismatch therefore fails before an output identity is consumed.

The version matches the previously used exact RD004 development runtime, but RD005 does not inherit RD004 scientific results or execution identity.

## Bound construction command

The only prospectively authorized D1 construction entrypoint is the module invocation template:

```text
python -m sparkbrain.research.rv02_rd005_bound_construction --input {construction_input_path} --repo-root {repo_root}
```

The argument vector, entrypoint module, runtime implementation, and runtime version are hashed together in `RD005_D1_EXECUTION_BINDING.binding_sha256`. The package plan includes that digest and marks the D1 construction wrapper, command contract, and Python runtime as bound. Capability remains explicitly unbound and closed.

The two placeholders are not free scientific parameters. Before execution, the control/seal record must bind them to one exact construction-input artifact and one exact frozen checkout root. The construction input itself must carry the exact frozen source manifest SHA, authoritative collision-registry SHA, and canonical package-plan SHA. No alternate command, runtime, input bytes, or source checkout is authorized by this review.

## Exact-byte handoff

The bound wrapper reads the construction input once, validates the canonical package-plan digest on those bytes, and passes the same in-memory bytes to `run_construction_from_bytes`. The output identity is derived from those same bytes. A regression test replaces the input path after preflight and verifies that construction still receives only the originally verified bytes. This closes the preflight-to-consumption TOCTOU gap identified during review of the earlier stacked change.

## Scientific boundary

This binding authorizes no execution by itself. It does not:

- create D1 output;
- run a learner or probe;
- open capability output;
- score a scientific outcome;
- grant held-out or formal authority;
- permit retry of a consumed D1 identity.

## Remaining gates before D1

D1 remains blocked until all of the following are complete against the final settled source head:

1. this runtime/command binding is reviewed, CI-green, and merged;
2. an exact SHA-256 source manifest is generated for the final source head;
3. the authoritative retained collision registry and canonical package-plan digest are reverified against that manifest;
4. the exact construction-input artifact and its digest are created prospectively without consuming D1;
5. a durable technical/semantic review record confirms the final source/package/input identities;
6. a non-moving exact-source freeze ref is created and verified;
7. the execution seal/control record binds the concrete input path/digest, frozen source SHA/ref, runtime binding digest, command contract, and fresh/no-clobber output identity.

Only after those gates pass may D1 construction cross its one-way boundary exactly once under the 2026-09-13 global execution authorization. Capability must remain unopened until D1 raw evidence is preserved and independently reviewed.

## Decision

**RUNTIME/COMMAND BINDING IS SUITABLE FOR PROSPECTIVE REVIEW. D1 REMAINS BLOCKED PENDING FINAL SOURCE MANIFEST, CONCRETE INPUT BINDING, FINAL REVIEW, SOURCE FREEZE, AND EXECUTION SEAL.**
