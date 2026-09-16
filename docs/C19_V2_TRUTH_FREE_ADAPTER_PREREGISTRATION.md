# C19-v2 truth-free symbolic adapter preregistration

## Scientific question

Can the integrated SparkBrain testbed accept Belief-R natural-language evidence through a deterministic, target-blind, source-index-preserving symbolic **surface** adapter without evaluator/test-target privilege, such that a fresh external-validation protocol becomes scientifically admissible?

This is a readiness-only prospective object. It does **not** authorize official Belief-R access or evaluation.

## Fresh identities

- protocol: `c19-external-v2`
- adapter contract: `c19-belief-r-truth-free-symbolic-adapter-v1`
- planned future official identity: `c19-external-v2-official-v1`
- input condition: `I2_truth_free_symbolic_surface`

The new condition name does not reuse the historical `I2_symbolic_oracle` contract. The new adapter must be autonomous and `oracle=false`.

## Historical boundary

The immutable C19-v1 blocked-readiness object remains authoritative at source `052413136229dcfa63f08cebe19585134f7cfb98`. Its official Belief-R cache/examples were not opened and its scientific status remains `not_evaluated`. C19-v2 does not mutate or reclassify it.

The versioned Belief-R specification/revision may be used as metadata pins only. During this readiness cycle the official cache may not be opened, verified, parsed, or inspected.

## Allowed adapter information

The adapter API is intentionally smaller than the existing Belief-R row/episode model. It may receive only:

1. a caller-owned record ID;
2. a non-negative source index;
3. a non-negative step index;
4. the backend-visible question text;
5. the three ordered backend-visible choice strings.

The adapter API does not accept benchmark `ground_truth`, update/no-update status, Target objects, evaluator labels, `modus`, relation type, agreement level, atomic index, dataset ID, cache bytes, or C06 official outputs. There is therefore no code path by which those fields can affect the mapping.

All autonomous comparison conditions must receive the same allowed visible envelope. I0 hashes that envelope, I1 encodes it compositionally, and the new condition gives the same envelope explicit surface roles/order. Scientific differences must come from representation, not additional data.

## Mapping contract

The adapter is a deterministic surface parser, not a semantic reasoner and not an Oracle.

- It recognizes only the versioned query marker `What necessarily had to follow`, already present in repository-owned Belief-R adapter logic and synthetic fixtures.
- Text before the first marker is treated as a premise surface prefix.
- Premises are segmented only by surface sentence boundaries after NFKC/casefold/whitespace normalization.
- No polarity, logical relation, entailment, answer correctness, update status, or ontology is inferred.
- Ordered choices remain ordered surface choices; the adapter never selects one.
- `source_index` and `step_index` are copied into the representation rather than reconstructed from content.
- Every emitted feature is a deterministic function of the allowed visible envelope.

The representation may encode role/index-qualified fingerprints and counts. A fingerprint is an identity transform over visible surface material, not a semantic label.

## Static falsifiers before official access

The exact proposal is rejected before official data access if any of these holds:

1. implementation requires evaluator truth, official labels/examples, benchmark-only semantic metadata, or C06 official outputs;
2. source ordering cannot be preserved deterministically without reading test behavior;
3. the new condition secretly invokes the historical symbolic Oracle or another evaluator-provided structure;
4. autonomous comparison conditions do not receive the same visible information boundary;
5. the implemented feature map is exactly equivalent to I0 or I1 on the registered synthetic distinction probes;
6. completing the package requires changing this scientific question, input boundary, condition/baseline matrix, metric boundary, or planned identity after binding.

If one of these falsifiers triggers, the v2 object is closed before official access. No replacement/v3 is designed in the same run.

## Prospective execution integrity plan

No one-way execution is allowed in the current handoff. A later official run, if independently admitted, must use a fresh STARTED/no-clobber claim for `c19-external-v2-official-v1`, verify exact source/protocol/package/input bindings, and preserve raw predictions before any scoring. Existing STARTED/raw/scored output under the planned identity would be fatal rather than overwritten or retried.

## Stop boundary for this readiness cycle

MAIN may implement the bound adapter, non-test synthetic fixtures, validation code, exact package manifests and semantics-preserving CI fixes. Once the exact package is reviewable and clean, MAIN must stop and return it to Evidence Analyst for a fresh ADMIT/REJECT. Official Belief-R cache/example access remains forbidden until that later decision.
