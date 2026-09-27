# Forge prototype: observed-outcome revision loop

Status: FORGE_PROTOTYPE  
Source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001

## Question

Can the plural-scope revision bridge derive its routing error from the exposed
prediction pool and the later observed outcome, instead of accepting a
caller-computed prediction-error scalar?

## Prototype

The adapter calculates the bounded residual `1 - P(observed outcome)` from the
already exposed hypothesis pool, then passes that internally derived value to
the existing scope/revision bridge.

- the public mutation API has no `prediction_error` or scope/regime/episode ID;
- exposed outcomes can drive ordinary scope routing and revision;
- an outcome absent from the bounded exposed pool is reported as a no-write
  diagnostic, avoiding partial allocator mutation before revision rejection;
- invalid probability mass and duplicate hypotheses fail closed;
- bridge state still round-trips for deterministic checkpoint/replay.

## Ordinary reduction

`1 - P(y)` is a simple bounded residual over a categorical prediction. The
adapter is ordinary scoring and transactional API-boundary engineering, not a
new predictive-learning, uncertainty or memory mechanism.

## Diagnostic value

This removes one caller-controlled scalar from the retained Theory R6 loop and
tests whether the existing bridge can be driven by observable prediction/outcome
data alone. It also exposes a remaining limitation: top-k truncation prevents
safe revision of an outcome that was not in the exposed pool.

## Claim boundary

Passing tests establishes only bounded Forge component composition. The score
is not calibrated, is not a full proper-scoring-rule implementation, and no
continuous stream, comparator, resource match, interaction ablation or task
capability is tested. The prototype is not admitted to SB001 or RV02 and its
engineering usefulness does not establish scientific novelty.
