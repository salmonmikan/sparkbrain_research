# Forge prototype: plural scope posterior router

Status: FORGE_PROTOTYPE  
Source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001

## Question

Can the existing internally allocated scope namespace expose several plausible
scope alternatives and abstain under ambiguity without receiving a caller
supplied regime/episode/scope identity?

## Prototype

The router reads only the allocator's internal centroids plus the current
admissible observation and prediction error. It ranks existing internal scope
tokens together with a synthetic NEW_SCOPE option, retains a bounded top-k, and
selects only when both mass and winner-margin thresholds pass.

Routing is read-only: NEW_SCOPE being ranked does not itself allocate or mutate
a scope.

## Ordinary reduction

This is normalized radial scoring plus a reject option. It is ordinary mixture /
nearest-prototype engineering, not a calibrated Bayesian posterior and not a
new context-discovery, memory, or learning mechanism.

## Diagnostic value

The prototype tests a missing integration seam from Theory R6:

- preserve multiple plausible scopes rather than collapsing immediately to top-1;
- expose ambiguity explicitly;
- permit deterministic replay from the same allocator state;
- keep scope identity internally generated;
- separate "NEW_SCOPE is plausible" from actually mutating the allocator.

## Claim boundary

Success only supports bounded component function in a rough Forge prototype.
It does not establish true latent-cause identification, calibration, comparative
advantage, composition contribution, SYSTEM_BUILD readiness, or scientific
novelty. It is not admitted to SB001 or RV02.
