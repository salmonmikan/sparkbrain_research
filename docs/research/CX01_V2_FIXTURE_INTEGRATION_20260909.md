# CX01 protocol-v2 reserved-fixture integration

Status: **ENGINEERING TESTED; FORMAL NOT AUTHORIZED**.

Base: `0687c8db3efb8180c8599d32235751b93f3c1f77`.
This additive integration preserves the accepted protocol-v2 source and six-file
package contract. It does not merge the divergent component or prestart source.

## Reconciliation decisions

| Item | Decision |
| --- | --- |
| Accepted candidate validation, deterministic seed selection, freeze bindings | Preserve byte-for-byte |
| Accepted world generators, original auditors, raw audit hash preimages | Preserve byte-for-byte |
| Consumer envelope correction at `1f13cc9aa49ab90d1bb3e2baed89a71b0ae87635` | Not applied: accepted parent has no erroneous top-level passed guard |
| Component source `10490ee302d3e6c540a5acc886d530250745143e` | Integration deferred; divergent generator/auditor contract requires separate review |
| Prestart source `24baf69324696c945b9be2b68917c1ee2467d9ee` | Not imported; retain parent protocol-v2 rejection and source-bound selection |
| Divergent package verifier | Replace its intended engineering check with a new fixture-only canonical reconstruction verifier; no divergent payload schema imported |
| Rejected freeze | Runbook and accepted status document both identify `freeze/cx01-001` as `f2c5ead5afda7d731033d585511ea68dc066a162`; retain untouched |
| Divergent workflow constant `97d47af0b98ce4e34918aeed63b8e9d975e37838` | Workflow not imported; historical cause of mismatch remains unresolved, no freeze moved |

The integration adds `verify_prepared.py`, which requires independently supplied
expected fixture identity and metadata, reconstructs the existing prepare output
in a temporary directory, and compares every canonical payload byte. It refuses
formal purpose before reconstruction. Candidate validation additionally restricts
fixture namespaces and seeds to the existing reserved band. It accepts exactly
the six runbook files and rejects missing/extra entries, symlinks, directories,
modified declarations, audits, seed metadata, and manifest bindings.

No package-supplied checksum or `passed` field supplies authority. Returning raw
SHA-256 values is an engineering comparison result, not formal review, an
execution seal, or source-checkout attestation. The caller must establish the
expected source revision independently; a package cannot choose both sides of
the comparison. The package must be quiescent during verification.

## Reserved prepare-to-verify evidence

An actual end-to-end prepare and verification completed for:

```text
generation_id: cx01-fixture-integration-20260909
purpose: structure-fixture
seeds: 5000..5009
source_git_sha: 0687c8db3efb8180c8599d32235751b93f3c1f77
builder: engineering-fixture-builder
execution_command: reserved-fixture-no-capability
artifact_root: reserved-fixture-unused
```

The source SHA describes the unchanged accepted preparation implementation used
to produce this engineering fixture, not a new formal freeze. The package has
60 worlds and 420 declarations, all unscored with capability/result flags false.
No comparator was instantiated and no formal seed selector executed.

| Payload | Raw SHA-256 |
| --- | --- |
| candidate.json | `8a2d0014d46ed0fe1ec9908ba550c534ce84d52a5a585fb8d5e52a88dc9cafbc` |
| declarations.jsonl | `9e692d52d59bcafcb358a20f1638cd794a1ab86ed5476463d0a7241aeb070b1d` |
| formal_identifiability_audit.json | `97621fdd551e777b7b0a27f377dcb5b243a8ef32d8e632b6e443ab2af7e59b22` |
| formal_seed_selection.json | `e8a4570885d23305a52f1863a4fc1fbdc6020c38af15768b561e4cd59f56801d` |
| formal_structure_audit.json | `027712979dfb3fc6bd100ba609a2acc6f1976df6cd970419832b296717ae8079` |
| freeze_manifest.json | `2b7ec2a9483ee1e27516b9aaa8dca18fb211c5ab30e99f9caa4c1ba55824d99e` |

The unchanged development grid recomputes to
`d93b362ce672fffd233973b8f27521f9d6a5fbdf4f3d4cba9369495635a33c9f`.

## Validation and limitations

```bash
PYTHONPATH=src python -m unittest discover -s tests/cx01 -p test_verify_prepared.py -v
```

Six standard-library tests cover the full reserved roundtrip, mutation of every
payload, empty/false audits, missing declarations, exact inventory, symlinks and
non-file rejection, externally expected source/metadata mismatch, and refusal
of formal-purpose input before reconstruction. The denial test constructs only
an in-memory specification; no formal world or formal package is generated.

Validation uses Python 3.12 in a source snapshot; full repository readiness,
full suite, Ruff, Python 3.11.16/3.13, and 210-cell development execution are not
claimed. The exact-source qualification gates in the runbook remain outstanding.
No existing source file, workflow, stored evidence, freeze, control branch, or
scientific claim is changed. No new formal candidate, held-out run, seal,
STARTED marker, or main merge was performed.

Component integration and historical freeze-constant provenance are still
unresolved. This result closes only the reserved protocol-v2 package engineering
comparison step; it does not certify complete CX01 integration or formal readiness.

## Independent engineering acceptance

The coordinating root agent independently read the verifier and candidate
contract and reran all six tests: PASS, 17.508 seconds. It accepted the narrow
reserved-fixture scope. This assistant-lineage review is engineering acceptance
only and cannot satisfy the genuinely independent formal review requirement.
The companion JSON retains all six raw fixture payloads, their byte hashes, and
the new verifier/test source hashes for reproducibility.
