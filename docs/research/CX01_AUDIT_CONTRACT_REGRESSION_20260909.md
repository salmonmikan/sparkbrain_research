# Executable CX01 audit-contract regression

Status: **BLOCKER_REPRODUCED / RETURN_SOURCE_ONLY**.

The diagnostic at `scripts/cx01_audit_contract_regression.py` was executed on
2026-09-09 with exact source files from
`10490ee302d3e6c540a5acc886d530250745143e`. It checks all six file SHA-256 values
before executing source. The JSON companion records those hashes and output.

It constructs only the already-reserved `cx01-fixture-prepare-001` worlds with
seeds 5000 through 5009, 60 worlds total. All three actual structural auditors
return successfully. The original preparation function's audit assignment and
following guard are extracted as AST and executed unchanged; that guard then
raises `candidate structural audits must pass before packaging` because
canonical_structure and family_identifiability lack a top-level passed key.

This is a real executable reproduction of the audit-return mismatch, not a
full package run or scientific capability result. No comparator is imported,
no formal seed selection occurs, and no candidate package, manifest, seal or
STARTED is written. No source fixes or independent formal approval are claimed.

## Reproduce offline

Obtain the six pinned files from the above Git revision into one local folder,
or use a separate checkout of that revision, then run:

```bash
python scripts/cx01_audit_contract_regression.py --source /path/to/observed-checkout/src/sparkbrain/comparison/cx01
```

The exit code is 0 only if all assertions reproduce the expected blocker.
The diagnostic hashes reject other source revisions rather than silently
labelling them as the observed source. It prints JSON to stdout; shell output
redirection may be used by a human running the reproducer to retain a log.

The program uses the standard library only. Byte-compilation also passed.
This bounded execution is not full local readiness, full pytest, or acceptance
of an integrated CX01 correction. The original source-only audit and its
independence/freeze/protocol-drift blockers still apply.
