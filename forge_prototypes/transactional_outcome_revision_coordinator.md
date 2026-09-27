# Forge prototype: transactional observed-outcome revision coordinator

Status: FORGE_PROTOTYPE  
Source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001

## Question

Can one observed-outcome step update scope allocation and late-evidence support
atomically, so a validation failure or no-write routing result never leaves a
partial allocator/cache mutation?

## Why now

The coverage-aware outcome guard closes the top-k omission seam, but its exposed
outcome path delegates directly to the plural-scope revision bridge. The bridge
routes and allocates before the revision overlay validates evidence strength.
An invalid strength therefore raises as intended while leaving a newly created
scope behind. That partial state is ordinary transaction-boundary debt.

## Prototype

`TransactionalOutcomeRevisionCoordinator` evaluates each step on a restored
checkpoint copy. It replaces live state only after the complete step returns an
intentional mutation action:

- `applied_created`;
- `applied_existing`;
- `pending` confirmation state.

Ambiguous routing, router/allocator conflict, omitted outcomes and exceptions
preserve the exact prior checkpoint. Successful state is restored through the
public serialization contract before becoming live, avoiding speculative object
aliasing.

The public API accepts only prediction-pool state, an observation vector, the
later observed value and evidence strength. It accepts no scope, regime,
episode, evaluator identity, prediction-error scalar or tail assignment.

## Ordinary reduction

This is copy-on-write transaction/checkpoint isolation around stateful
components. It is not a new revision rule, uncertainty model, memory mechanism
or scientific result.

## Claim boundary

Passing bounded tests supports only atomic component composition in an isolated
Forge prototype. It does not establish end-to-end task capability, comparative
advantage, composition contribution, SYSTEM_BUILD admission or scientific
novelty. It is not admitted to SB001 or RV02.
