# A01-MD-002 prospective binding status — 2026-09-11

Status: **DRAFT_CONSTRUCTION_BOUND_EXECUTION_DISABLED_BY_TECHNICAL_GATES**

This is an append-only prospective status note. It does not execute A01-MD-002, rerun or rescore A01-MD-001, or modify any preserved evidence. The user's line-scoped A01 execution authorization dated 2026-09-12 is recorded separately in `docs/research/V061_A01_MD002_EXECUTION_AUTHORIZATION_20260912.md`; that authorization removes the need for another user approval once an exact MD-002 identity is technically seal-ready, but it does not waive any technical or scientific-integrity prerequisite.

## What changed since the supplemental draft

The supplemental draft was intentionally marked `DRAFT_N3_UNBOUND` because no genuine compatible recurrent N3 family had yet been bound. That specific family-existence blocker has now narrowed.

`N3-DEV-001` has an accepted narrow development record for a live-state recurrent causal learner. Its independent read-only audit accepted 36 preregistered cases / 72 arm rows, shared-bridge input handling, recurrent clock/write behavior, fixed artifact identities, and inspectable accounting boundaries. The same audit explicitly leaves resource matching and full MD-002 `NOT_EVALUATED`.

Therefore MD-002 must **not** treat N3 as scientifically matched or use N3-DEV-001 outcomes as a full P5 result. The accepted fact is only that a genuine recurrent family implementation now exists and can be prospectively bound into a later MD-002 matrix.

## Construction contracts now present

The MD-002 construction branch adds fail-closed prospective contracts for four previously blocking areas:

1. **P2 world-only intervention** — pre-evidence local, Field, consistency and return-address state must remain matched. Only the anonymous external world-relation mapping may differ before the same admissible external evidence is applied.
2. **P3 actual R transplant** — baseline and donor must begin with matching L/F/C and genuinely different R; the third arm must carry donor R on the baseline L/F/C state, have a distinct retained runtime trace, and measure the required post-attribution L update. The semantic snapshots and outputs must be present in that retained trace so relabeling a donor record cannot satisfy the contract.
3. **P4 plural ancestry** — merged ancestry and active lineages must be contained in a retained runtime trace, must contain genuine plurality, and later state must retain at least one lineage from the merged BoundaryEvent source ancestry. A separately supplied lineage tuple or digest is insufficient.
4. **P5 comparator evidence** — A01, N1 and N3 must receive byte-identical admissible anonymous evidence; resource matching and full MD-002 cannot be predeclared as evaluated.

Dynamic/resource counters are parsed from retained runtime counter-trace records and checked against the trace digest; declarative counter rows or a caller-controlled `measured=true` flag are not accepted as measurement provenance.

The construction contract now also requires a retained `md002-external-observation` marker and measures external-effect latency from that observation step rather than from the first counter sample. The runtime trace must contain exactly one non-negative observation marker inside the sampled interval, and a measured external effect is rejected if it precedes the observation. This is measurement hardening only; it does not execute capability or provide an MD-002 result.

`MD002ExecutionGate` contains no caller-controlled review/authority booleans. In this construction branch both immutable authority-artifact digest pins are deliberately unset, so execution is impossible even if a caller supplies fabricated approval payloads. A later separately reviewed source revision must pin the exact SHA-256 identities of an independent technical-review JSON artifact and a distinct gate-compatible execution-authority JSON artifact. The execution-authority JSON must be created only after the exact MD-002 source/protocol identity is fixed, must bind that exact identity, and must cite the existing 2026-09-12 user-authorization record as provenance; the Markdown authorization record itself is provenance and is not directly consumable by `MD002ExecutionGate`.

These are construction invariants, not capability evidence.

## Gates still open before any MD-002 execution

The following remain unresolved and execution-blocking:

- bind the exact N3 configuration/source identity to be used in MD-002 without selecting it from MD-002 outcomes;
- bind matched-resource accounting and acceptance semantics across A01/N1/N3; N3-DEV-001 explicitly did not establish resource equivalence;
- implement and independently validate the actual P2 world fixture/reset/restore execution path;
- implement full runtime snapshot, R partition, round-trip validation and real third-arm execution for P3;
- implement continuing merged-ancestry runtime generation and measurement for P4;
- implement an independently emitted retained instrumentation stream for dynamic/resource counters and verify it from raw artifacts;
- bind the complete P1-P5 matrix, arm applicability, seeds, budgets, thresholds, expected control directions and exclusions;
- bind source SHA, protocol digest, source manifest, unique output paths and a source-identity-checked runner;
- bind raw artifact schema and preservation procedure before scoring can be opened;
- complete independent technical review of the final executable package;
- pin the immutable technical-review JSON artifact digest in a separately reviewed source revision;
- after the exact source/protocol identity is frozen, generate a gate-compatible `execution-authority` JSON record that binds that exact identity and cites `docs/research/V061_A01_MD002_EXECUTION_AUTHORIZATION_20260912.md` as the user-authorization provenance, then pin the JSON artifact digest in the final separately reviewed source revision.

The user's explicit A01 line-scoped execution authorization dated 2026-09-12 is sufficient user authority for a future exact MD-002 identity once all of the technical, review, freeze, and seal prerequisites above pass. The later gate-compatible JSON artifact is an identity-binding/seal representation of that already-granted authority, not a request for new user approval. Do not request another user approval solely because the experiment reaches the execution boundary. This authorization does not permit changing the protocol after outcomes, reusing a consumed identity, or bypassing any scientific-integrity gate.

## Current scientific boundary

A01-MD-001 remains immutable and retains its reviewed limitations. N3-DEV-001 remains an accepted narrow development artifact, not a matched comparator result. A01-MD-002 has no capability result.

The safe next step is to continue implementing the still-prospective fixture/snapshot/instrumentation layers under the execution-disabled technical boundary. Any future capability runner must remain fail-closed until the complete matrix, source identity, instrumentation provenance, independent review, freeze/seal conditions, and immutable digest bindings for the technical-review artifact and gate-compatible execution-authority artifact are fixed and verified.
