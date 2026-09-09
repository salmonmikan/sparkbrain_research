# N3-DEV-001 development result — 2026-09-09

Status: COMPLETE at the bounded descriptive development scope. The one authorized
execution produced 72 arm rows for all 36 cases, without a failed arm. All 36
paired admissible input hashes agree. All 36 absence/replay arm rows leave learned
state unchanged. No MD-001 or MD-002 outcome runner was executed.

## Source and execution

Source: `201ebd512cdee6365bd186e3ff0627ba784677cd`.
Independent source review: `5cd8f43686801ceeafd87140f2daf21028c1c244`.
Execution authorization: `e471e13` (full identity in Git history).
Protocol, complete 264-file source manifest, complete checkpoint cuts, observed
outputs and timing/allocation measurements are in the exact-four bundle.
The fixed recurrent weights were seeded; two readout weights actually learn from
anonymous signed external evidence. Current hidden state affects inference.
No model, hyperparameter or fixture was selected from these outcomes.

```bash
PYTHONPATH=src python scripts/run_a01_n3_development.py \
  --authorization docs/research/V061_A01_N3_DEV_001_EXECUTION_PIN.json \
  --output artifacts/v061/a01/N3_DEV_001
```

This command was executed once. The output directory must be new. Reproduction
requires the recorded source tree and authorization; timings/allocation peaks
are machine-dependent and are not asserted byte-reproducible.

## Observations

Confidence outputs are equal in 18/36 paired cases: all absence and replay
cases. They differ in all 18 confirmation/contradiction cases. This difference
is descriptive, not a performance win for A01 or a failure of generic recurrence.

For first-path confirmation, A01 confidence is 0.6666667 at delays 0,1,4;
N3 is respectively 0.6224593, 0.6194985, 0.5110399. Under contradiction the
corresponding A01 confidence is 0.3333333 and N3 is 0.3775407, 0.3805015, 0.4889601.
Thus this fixed learned recurrent readout shows an elapsed-delay effect.

Merged ancestry is not automatically selective evidence. At delay4 merged
confirmation N3 gives 0.5815312 and 0.5508413, despite the same eligible sign
for both paths. A01 gives equal 0.6666667 values. The asymmetric recurrent
substrate can introduce unequal confidence under indistinguishable ancestry;
this is retained as an ambiguity-preservation limitation, not useful causal
separation or proof that P4 passed. No endpoint was corrected or discarded.

## Resources and limitations

| Observed representation | A01 | N3 |
|---|---:|---:|
| Incremental mechanism JSON bytes across final rows | 2–155 | 465–514 |
| Whole adapter-runtime checkpoint JSON bytes across all cuts | 3630–5171 | 4068–5520 |
| Fixed / learned / retained-hidden scalar capacity | 0 / up to4 / 0 | 2 / 2 / 2 |
| Maximum whole-arm traced Python allocations, bytes | 109543 | 121329 |

Mechanism JSON scope differs by its real constituent fields; whole-runtime
checkpoint bytes include each arm's base local temporal state, C, provenance
ledger, bridge records, config and model state. Normalized payload bytes are
also retained per cut. These are explicit representation/accounting results,
not RAM or energy superiority. No actual Field simulation is included.
Actual N3 update/edge/index-search counters are retained; complete router/query
lookup counts, resident duplicates and exact transient occupancy are unavailable.
Resource matching and full MD-002 therefore remain NOT_EVALUATED. Shared causal
routing means this diagnostic cannot distinguish the routing mechanism itself.
Repaired P2 world interventions, third-runtime P3 transplants, full P4 continuation
and complete matched P5 remain future prerequisites. No Field emergence or
claim-grade promotion follows.

## Validation

Ten focused pytest tests pass (seven independently authored adapter tests and
three actual shared-bridge tests). They cover genuine recurrence, recurrence-off
intervention, live-state readout, ID renaming, exact restore, nonmutation,
unknown/duplicate input rejection, extra-supervision rejection, external-only
learning, fallback, no-prior and replay exclusion. Ruff across the checked-out tree (all src/tests/scripts) and
local readiness pass. Full pytest stopped during collection with 21 missing
optional-dependency errors (including FastAPI, torch, jsonschema); it did not
execute the existing outcome suites and is not reported as a full-suite pass.
No protected legacy artifact or MD-001 evidence was rewritten.

## Exact artifact hashes

- `protocol.json`: `d9c95e52063a77806a723fa537f8354fc6d2d175b1f2fac36f27edd3e166c6b2`
- `raw_rows.jsonl`: `cd9b0565c16963319eab2f8a011b970f628cf1638154f1689ee85ffb0e53f5b1`
- `source_manifest.json`: `dba6bbfab6b2da96d2a6713238991eb151aea078fc994528c9bc85903a847214`
- `summary.json`: `69d8945be1c569e096c67a1721314baebfeaba8965aae2e55488ce0e7c04731f`

Independent raw-only acceptance also passed all 72 rows and the exact-four
inventory; see V061_A01_N3_DEV_001_INDEPENDENT_RESULT_AUDIT.md. No outcome rerun
was used for this check. The Git worktree excludes unrelated legacy artifacts
through sparse checkout; full-repository artifact validation is not asserted.
