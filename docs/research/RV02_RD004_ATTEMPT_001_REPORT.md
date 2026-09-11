# RV02 RD004 development attempt 001 report

Date: 2026-09-11  
Status: **PRESERVED DEVELOPMENT DIAGNOSIS / NOT FORMAL / NOT HELD-OUT**

## Execution identity

- Protocol: `rv02-rd004-relative-probe-clock-v1`
- Frozen source: `freeze/rv02-rd004-development-source`
- Exact source SHA: `75268dd804f0ef113869be172adf575ac22523a0`
- One-shot execution branch: `ops/rv02-rd004-development-execution-20260911`
- GitHub Actions run: `34592080367`
- Python: `3.11.15`
- Workflow conclusion: `success`
- Formal execution allowed: `false`
- Held-out capability executed: `false`
- Same-source rerun allowed: `false`

The source ref was frozen before execution. The workflow verified that the pushed execution SHA exactly matched the frozen ref, ran the fixed exposed-development matrix, independently verified the produced bundle, and uploaded the raw evidence. No formal or held-out capability was opened.

## Matrix result

The fixed 18-cell matrix was attempted exactly once. Fifteen cells completed. The three `opposing-reversal` cells (scales 1, 3, 10) ended as `incomplete_native_guard_training`, as the preregistration explicitly required rather than raising native limits. No cell failed during washout, probe execution, integrity verification, or other execution.

| family | scale | status | E1 eligibility events | ES eligibility events | E0/E1/ES visible probe behavior identical | natural vs hidden-boundary-cut behavior changed |
|---|---:|---|---:|---:|---|---|
| disjoint-routes | 1 | `complete` | 0 | 0 | yes | no |
| disjoint-routes | 3 | `complete` | 0 | 0 | yes | no |
| disjoint-routes | 10 | `complete` | 0 | 0 | yes | no |
| shared-cue | 1 | `complete` | 4 | 4 | yes | no |
| shared-cue | 3 | `complete` | 0 | 0 | yes | no |
| shared-cue | 10 | `complete` | 0 | 0 | yes | no |
| shared-prefix | 1 | `complete` | 0 | 0 | yes | no |
| shared-prefix | 3 | `complete` | 0 | 0 | yes | no |
| shared-prefix | 10 | `complete` | 0 | 0 | yes | no |
| opposing-reversal | 1 | `incomplete_native_guard_training` | - | - | - | - |
| opposing-reversal | 3 | `incomplete_native_guard_training` | - | - | - | - |
| opposing-reversal | 10 | `incomplete_native_guard_training` | - | - | - | - |
| dense-load | 1 | `complete` | 28 | 28 | yes | no |
| dense-load | 3 | `complete` | 16 | 16 | yes | no |
| dense-load | 10 | `complete` | 0 | 0 | yes | no |
| capacity-pressure | 1 | `complete` | 28 | 28 | yes | no |
| capacity-pressure | 3 | `complete` | 20 | 20 | yes | no |
| capacity-pressure | 10 | `complete` | 8 | 8 | yes | no |

## Development interpretation under the preregistered readout

Among all 15 complete family/scale cells, the visible continuation metrics were identical across E0 (disabled), E1 (causal hidden assignment), and ES (matched shuffled assignment) for every registered probe. The paired hidden-boundary cut also did not change the registered visible continuation behavior in any complete probe.

Some complete cells did contain matched E1/ES hidden eligibility activity (for example `shared-cue` scale 1, `dense-load` scales 1 and 3, and all three `capacity-pressure` scales), but that activity did not produce an E1-specific visible improvement and the retained causal hidden-return update lists were empty. Cells without hidden eligibility likewise provide no positive selective-organization evidence.

Therefore the preregistered conjunction for a useful selective-organization signal is **not satisfied in any complete RD004 cell**. In particular, E1 does not improve exact-route recovery or contamination relative to both E0 and ES, and the boundary cut does not remove an E1-specific improvement. Under the preregistered rule, causal hidden assignment is not supported by this exposed-development diagnostic.

This is a negative development result, not a global RV02 capability claim: the `opposing-reversal` family is incomplete at every scale, and the preregistration prohibits averaging around required per-probe criteria or converting native-guard incompleteness into behavioral scores.

## Preserved evidence identifiers

- Actions artifact: `rv02-rd004-development-34592080367` (artifact id `10196093854`)
- Artifact archive digest: `sha256:1b583bd25587944f96b98d580c99d4215547859df28730e64e454072122a57f0`
- `raw_cells.jsonl.gz`: `2c553868031848d7d24a9e39ce0f508de99e2b8ea5dfcf3fffe70d7b6215588c`
- raw JSONL temporary stream: `29634cbb981daa84d3221f0e96f64268b0e23ce5a247000c4b62da49c65a52fc`
- `manifest.json`: `8f7502606a19110ad2443a0d72190357e7badf337e28095a2f7f81fe0d2b8f6c`
- `summary.json`: `d101dc668726f9d35c09eace9057e17f9ec5e6ce212136a1a813769f499daae1`

The full raw compressed evidence remains the immutable output of run `34592080367`; this report copies only compact metadata and derived matrix accounting into Git history. The raw source identity must not be rerun or tuned under RD004 after this result.
