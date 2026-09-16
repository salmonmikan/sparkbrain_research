# V061 A01 Family-B Generation-1 — Distributed Field Trace

Status: **prospective readiness contract; NOT execution-admitted**  
Owner: MAIN research frontier  
Mechanism family: `distributed-field-trace`  
Generation: `1`  
Prospective identity: `a01-family-b-distributed-field-trace-gen1-v1`

## 1. Prospectivity boundary

This Generation-1 package is created after the terminal Family-A P4 result. It is **not** represented as a pre-P4 fully specified candidate. Its admissible scientific boundary is inherited only from pre-P4 Family-B material in `V061_D8_SPARKBRAIN_MECHANISTIC_THEORY_REVISION.md`, `V061_PREMECHANISM_ADMISSION_AND_NEGATIVE_COMPLETION.md`, and `V061_CROSS_LINE_EVIDENCE_FIREWALL_AND_PREMECHANISM_MATRIX.md`. The earliest repository revision that introduced the H-B `Field-distributed consequence trace` family used here is `525ecd9e205b2657a4ed207ae2b6cef0bae4bffc`; that revision is a family-level prior only, not a frozen Generation-1 protocol bundle.

- an interaction may leave a **decaying distributed Field trace**;
- later local competition may be biased through that trace;
- no direct transition/path table is required by the candidate mechanism;
- P1 must show causal selectivity under matched resources;
- P2 must show world-to-local competition circulation;
- P3 must support a valid **F-only** transfer of the learned functional effect;
- P4 must support bounded plurality and later causal differentiation;
- P5 must survive matched explicit-memory, recurrent causal-trace, and explicit latent-cause/belief-state reductions.

No threshold, carrier rule, scorer rule, or stopping rule in this contract is chosen from the observed Family-A P4 residuals. The Family-A outcome is used only to mark Family A terminal and to motivate moving to the already-registered Family-B family.

## 2. Candidate mechanism rule

The minimal Generation-1 carrier is a fixed-width local Field state with two component-wise vectors:

- `eligibility[i]`: a decaying local footprint left by local Field activity;
- `credit[i]`: a signed, leaky local consequence trace updated only when an external world return overlaps an eligible footprint.

The candidate stores **no lineage identifier, semantic label, task label, evaluator lookup key, transition/path identifier, global belief table, or evidence ID**. It exposes no API that accepts a selected lineage. The scientific carrier receives only a fixed-width anonymous boundary vector plus a signed physical consequence (`+1` or `-1`).

Repeated delivery of one external evidence identity must not create repeated credit. An acquisition-side `ExternalEvidenceLedger` therefore consumes opaque evidence IDs exactly once before an update is accepted. This ledger is **not** part of the candidate Field carrier, is not exported by the P3 F-only transfer, cannot affect competition scores, and cannot select a lineage; it exists only to enforce the repository-wide duplicate-evidence invariant. Its consumed-ID state is deterministic checkpoint state: callers must persist `export_consumed_ids()` and restore it with `from_consumed_ids()` across restart/checkpoint boundaries before accepting further returns. Recreating an empty ledger after prior consumption is not a valid acquisition boundary.

Local update rules are fixed prospectively:

1. Local Field activity `a`, with each component in `[0, 1]`, advances one local step as `e' = decay * e + a` and `c' = decay * c`.
2. Internal replay alone does not create or strengthen consequence credit.
3. A deduplicated external return vector `r`, with each component in `[0, 1]`, and sign `s ∈ {-1,+1}` updates credit as `c' = decay * c + (1 - decay) * s * (e ⊙ r)`.
4. Later local competition for activity vector `q ∈ [0, 1]^width` receives only the local score `dot(c, q)` from this carrier.
5. Export/import of the candidate carrier for P3 is exactly the Field carrier `(eligibility, credit, decay)`; the acquisition-side evidence ledger and any hidden N/P/global state are excluded.
6. The fixed input range and leaky updates imply a resource bound `B = 1 / (1 - decay)` for each eligibility component and the absolute value of each credit component. State outside this bound is invalid and fails closed.

The fixed default readiness configuration is:

- width: `4` components;
- decay: `0.5`;
- local/boundary/competition components: `[0, 1]`;
- score: unnormalized local dot product;
- credit update gain: exactly `(1 - decay)`;
- per-component eligibility/credit resource bound: `1 / (1 - decay)`;
- no clipping, softmax, learned threshold, normalization, or post-outcome parameter tuning.

These defaults are construction/readiness constants, not biological constants.

## 3. Prospectively fixed discriminator identities

The following IDs are part of the Generation-1 proposal binding and must not be changed after output exposure:

| role | ID | fixed interpretation |
|---|---|---|
| lineage swap | `v061-a01-bgen1-lineage-swap-v1` | swap anonymous physical footprints while preserving matched resources; effect must follow the actual Field footprint rather than a semantic/declared lineage |
| contradiction | `v061-a01-bgen1-contradiction-v1` | matched negative world return must reverse/correct the local credit contribution |
| future competition | `v061-a01-bgen1-future-local-competition-v1` | learned consequence must alter a later local competition score without global/evaluator lookup |
| bounded ambiguity | `v061-a01-bgen1-bounded-plurality-v1` | two coexisting anonymous Field footprints may remain represented without winner-only collapse; later anonymous world return must differentiate them locally |
| P3 F-only transfer | `v061-a01-bgen1-field-only-functional-transfer-v1` | exporting/importing only the Field carrier must transfer the learned functional competition effect |
| explicit-memory null | `v061-a01-bgen1-explicit-eligibility-return-address-null-v1` | matched explicit eligibility/return-address memory |
| recurrent null | `v061-a01-bgen1-resource-matched-recurrent-causal-trace-null-v1` | matched recurrent/reservoir causal-trace baseline |
| belief-state null | `v061-a01-bgen1-explicit-latent-cause-belief-null-v1` | explicit latent-cause/belief-state baseline |
| negative stop | `v061-a01-bgen1-stop-f-only-failure-or-null-reduction-v1` | stop if valid F-only transfer fails, forbidden privilege is required, or matched nulls fully reproduce the claimed residual |

## 4. Scientific falsifiers

Generation-1 must be stopped rather than rescued if any of the following is observed under a prospectively frozen execution package:

1. **F-only transfer failure:** the learned functional effect does not transfer with the Field carrier alone.
2. **Privilege failure:** selective behavior requires lineage IDs, semantic/task labels, evaluator lookup, caller-selected lineage, or global belief lookup.
3. **Circulation failure:** external consequence does not reach later local competition through allowed local state.
4. **Plurality failure:** bounded coexisting footprints cannot later be causally differentiated without privileged addressing.
5. **Null reduction:** the claimed residual is reproduced by the matched explicit eligibility/return-address null, recurrent causal-trace null, or explicit latent-cause/belief-state null with equal or lower privilege/resources.
6. **Identity/binding failure:** proposal/source/protocol/package/input identity cannot be verified exactly before STARTED.
7. **Bound/dedup failure:** the candidate requires unbounded eligibility/credit, repeated delivery of one evidence ID increases causal credit, or duplicate-consumption state cannot survive the acquisition lifecycle.

No observed failure may be repaired under the same consumed identity.

## 5. Construction/readiness tests allowed before execution admission

The following are deterministic implementation tests, not scientific measurements and do not consume the one-way identity:

- component-wise lineage-swap construction follows anonymous physical footprint;
- external return is necessary for credit creation/strengthening;
- repeated delivery of one evidence ID is rejected by the acquisition boundary, including after checkpoint/export and ledger restoration;
- contradiction changes the sign of the local consequence contribution;
- F-only carrier serialization/export/import preserves the deterministic competition score;
- two disjoint coexisting footprints can be represented and anonymous boundary return can address them only through vector overlap;
- eligibility and credit decay on later local steps and remain inside the fixed resource bound;
- malformed public fixture values (including fractional/boolean/string width, fractional signs, and stringified vector values), dimensional mismatch, non-finite values, out-of-range activity, invalid consequence sign, or invalid decay fail closed;
- proposal hash, exact source key set/source blobs, contract bytes, input bytes, discriminator IDs, null IDs, and privilege declarations verify exactly.

Passing these tests means **ready for Evidence Analyst review**, not ready for one-way execution.

## 6. Explicit prohibitions

Before a later Evidence Analyst handoff explicitly admits execution, MAIN must not:

- create STARTED/control consumption for this identity;
- dispatch acquisition/scoring workflows;
- expose one-way outputs;
- claim Family-B scientific support from readiness tests;
- tune this contract against Family-A P4 outcomes or any future Generation-1 scientific result.

SUB must not work on this branch, identity, verifier, CI, review, binding, or any other critical-path fix.

## 7. Binding fields

The code-side `PreMechanismProposal.protocol_bundle_source_sha` binds the **post-P4 Generation-1 protocol-contract source** commit `7af99d6c3bbbf946f90fc01d9bc7cc7661de2006`; it is not claimed to be a pre-P4 protocol bundle. The package separately binds `pre_p4_family_source_sha` to `525ecd9e205b2657a4ed207ae2b6cef0bae4bffc`, the pre-P4 revision that introduced H-B as a conceptual family. That earlier revision establishes only the admissible family-level prior and does not retroactively fix Generation-1 discriminator IDs, dynamics, thresholds, scorer rules, or stopping rules.

Because this post-P4 readiness contract did not exist at the pre-P4 family source, the readiness package binds the exact bytes of this document using both its Git blob SHA and SHA-256. The package binding also fixes the complete required source-path key set, each source Git blob, the readiness input bytes, the additional belief-state null ID, and an exact implementation-head SHA. `implementation_head_sha` denotes the last commit containing all mechanism, harness, tests, status/decision documentation, and provenance clarifications before the package-binding metadata itself is finalized; the binding-finalization commit may only change the binding artifact and its binding-verification test.

The final readiness package must record:

- prospective identity;
- pre-P4 Family-B family-source SHA;
- post-P4 Generation-1 protocol-contract source SHA;
- mechanism rule spec path (this file);
- exact mechanism-contract Git blob and SHA-256;
- null-ladder spec path (`docs/V061_A01_NULL_LADDER.md` plus the explicit IDs above);
- canonical proposal SHA-256 from `PreMechanismProposal.bind()`;
- belief-state null ID;
- complete required source-path key set and exact source Git blobs;
- exact readiness input blob/SHA-256;
- exact implementation head reviewed by CI/review.

The branch remains mutable research state. It is not an immutable freeze/seal/evidence anchor, and no new freeze tag/ref is created during readiness-only work.
