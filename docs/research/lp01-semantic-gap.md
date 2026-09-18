# LP01 actual-lineage causal-credit prospective review

Status: **`NO_HIGH_VALUE_OBJECT`** for the currently allocated claim.

Evidence Analyst authority: `57464c4ad6881c27371be5305512656c6ae315d3`.

This is a pre-formal source/semantics review only. No formal identity exists, no STARTED marker exists, no official TEST input was accessed, and no formal scoring, preservation, or evidence was produced.

## Question reviewed

Can the current SparkBrain architecture support a clean prospective test that actual historical lineage/provenance carries causal credit for later competition or decision behavior after present observable state, recent input, information privilege, and lineage-bookkeeping resources are matched?

## Native source finding

On current `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, lineage is persisted and inspectable metadata, but it is not a causal input to the online decision or reward paths that LP01 would need to test:

- `StructuralSparseModel.forward_step` reads the current encoded event, active masks, selected module state, active selected edges, learned parameters, and previous probabilities. It does not read logical identity, parents, lineage, or tombstones.
- `StructuralBrainBackend.run` calls `forward_step`; `_consume_structural` updates routing/coactivation/edge-credit statistics from current selected modules and confidence changes. Neither path reads lineage metadata.
- `StructuralBrainBackend.apply_reward_eligibility` modifies active-edge credit only; it does not propagate reward through ancestry.
- `StructuralController.discover` uses current routing load and edge credit; `candidate_group` ranks current routing load/coactivation. Neither uses stored ancestry.
- Logical IDs/parents/tombstones are consumed for structural mutation bookkeeping, checkpoint serialization, inspection, and post-hoc structural analysis.

Therefore, with all current numeric state, masks, pending work, budgets, recent input, and RNG state held fixed, changing only lineage metadata cannot change the next ordinary forward decision through the current implementation.

## Why the proposed candidate is not a clean residual test

A draft LP01 candidate can be invented by adding a new delayed-credit adapter that explicitly queries stored ancestry. That would indeed make historical lineage causally active. But the same ancestry relation is already a finite explicit data structure encoded by parent tuples and the append-only structural event history.

Under matched information privilege, an ordinary explicit-state comparator can reconstruct the same parent relation losslessly from the same event stream and execute the same ancestry query/credit propagation. The dev-only reference implementation on this branch intentionally uses two independent representations (`ActualLineageIndex` and `ExplicitParentTable`) to make that reduction testable without touching formal inputs.

Any prospective advantage for the lineage-branded candidate would therefore have to come from at least one of the following asymmetries:

1. candidate receives ancestry/history that the explicit comparator is denied;
2. comparator receives a tighter state/compute budget than the candidate;
3. candidate is granted a specialized ancestry operation while the comparator is forbidden an equivalent ordinary explicit operation;
4. the claim is changed to training efficiency, storage efficiency, inductive bias, or engineering convenience rather than lineage-specific causal credit.

The first three violate the allocated matched-privilege/resource causal question. The fourth is a different scientific claim and would require a fresh independent allocation; it must not be manufactured here as an LP01 rescue.

## Dev-only construction check

The branch contains a NON_EVIDENTIARY synthetic construction that checks only semantics and testability:

- opaque logical IDs prevent lexical ancestry leakage;
- present-state digests are independent of ancestry assignment;
- an independent explicit parent table must exactly reproduce actual-lineage descendant queries;
- a provenance-destroyed control preserves event order and parent arity while altering ancestry;
- a bounded recent-event state can forget older ancestry.

These diagnostics are not evidence for or against a formal scientific effect. Their purpose is to demonstrate that the proposed lineage information is finitely and losslessly representable by an ordinary explicit-state surrogate when information privilege is matched.

## Decision

**`NO_HIGH_VALUE_OBJECT`** for `LP01_ACTUAL_LINEAGE_CAUSAL_CREDIT_PROSPECTIVE_SPECIFICATION` under the present allocation.

Reason: the current architecture has no native lineage-to-decision causal path, and adding one prospectively does not isolate a new lineage-specific computational principle because the exact admitted lineage relation is reducible to an ordinary explicit parent-state representation under matched privilege. A positive result would require an asymmetric comparator or a materially different claim.

This closes LP01 at the prospective-specification boundary only. It does not alter any immutable evidence, consumed identity, or prior terminal result. A future Evidence Analyst may allocate a distinct question if new architecture or external theory supplies a non-privileged discriminator that is not definitionally reducible to explicit state.
