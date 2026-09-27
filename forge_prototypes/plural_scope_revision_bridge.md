# Forge prototype: plural-scope revision bridge

Status: FORGE_PROTOTYPE  
Source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001

## Question

Can internally generated plural scope hypotheses gate late-evidence revision so
that ambiguity never mutates scope or support state, while a separated existing
scope or a confirmed NEW_SCOPE can receive evidence?

## Prototype

The bridge composes the existing internal scope allocator, read-only plural
scope router, confirmation guard and managed late-evidence overlay.

- ambiguous routing returns without allocator or revision mutation;
- a selected existing scope must be independently re-confirmed by allocator
  mutation before evidence is applied;
- NEW_SCOPE may enter pending confirmation, but receives no evidence until the
  allocator actually creates it;
- disagreement between the read-only router and mutating allocator is rolled
  back before revision support changes;
- allocator and revision state round-trip together for deterministic replay.

The public API accepts observations, prediction error and late evidence. It does
not accept caller-provided scope, regime, episode or evaluator identities.

## Ordinary reduction

This is ordinary mixture/reject routing plus transactional validation and
rollback around cache-namespace mutation. It is not a calibrated posterior,
latent-cause learner, new memory mechanism or scientific result.

## Diagnostic value

The prototype closes one integration seam from Theory R6: plural scope
uncertainty can gate state mutation instead of being reported only as a
read-only diagnostic. It also exposes a real engineering conflict surface when
router thresholds favor NEW_SCOPE but allocator reuse rules favor an existing
scope.

## Claim boundary

Passing bounded tests supports only component composition in an isolated Forge
prototype. It does not establish task capability, calibrated uncertainty,
comparative advantage, composition contribution, SYSTEM_BUILD admission or
scientific novelty. It is not admitted to SB001 or RV02.
