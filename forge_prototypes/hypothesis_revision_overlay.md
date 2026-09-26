# FAST FORGE integration prototype — late-evidence hypothesis overlay

- worker_role: FAST_FORGE
- forge_id: FORGE-LATE-EVIDENCE-HYPOTHESIS-OVERLAY-A
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- prototype_kind: INTEGRATION
- target_capability: plural hypotheses -> later evidence -> selective reweighting -> abstain/select
- scientific_novelty_claim: none
- recommended_handoff: SYSTEM_BUILD_INPUT

## Question

Can the existing Forge multi-hypothesis prediction pool accept later evidence without mutating the stable v0.5 predictor, while preserving alternatives, explicit abstention and replayable state?

## Composition

This prototype layers an append-only evidence overlay on top of the prior Forge prediction pool.

1. Stable v0.5 AssemblyPredictor remains read-only.
2. The prior Forge pool exposes a bounded set of hypotheses and base probabilities.
3. Later evidence contributes bounded signed support only to an already-exposed hypothesis.
4. Support is combined with base log-probability using an ordinary multiplicative-weights/log-linear update.
5. The same confidence/margin style gate decides select versus abstain.
6. Overlay events can be serialized and replayed without changing predictor counts.

Unknown labels fail closed, and late evidence is not allowed to rescue a base pool rejected for insufficient observations.

## Development diagnostics

Synthetic checks cover:
- a 5:5 retained tie becoming selectable after one bounded evidence update;
- balanced later evidence restoring abstention rather than overwriting the earlier event;
- JSON save/replay equivalence;
- no mutation of AssemblyPredictor state;
- insufficient-data pools remaining abstained;
- unknown evidence labels failing closed.

## Strongest ordinary reduction

This is ordinary Bayesian/log-linear reweighting, multiplicative weights, or a categorical evidence accumulator over an explicit hypothesis set. It is not a new selective-revision mechanism.

The current Literature R44 reduction makes this boundary especially important: selective low-collateral revision is already ordinary associative-memory territory when an admissible cue works as a key.

## Engineering usefulness

The seam may be useful in a future SYSTEM_BUILD after SB001 integration because it provides an inspectable path:

prediction histogram -> plural hypotheses -> later evidence -> selective reweight -> abstain/select

without editing the underlying predictor or claiming emergent memory. It also gives a clean component-replacement surface: the overlay can later be swapped for a standard Bayesian/state-space updater while preserving the surrounding interfaces.

## Scientific claim boundary

FORGE-only and zero-credit. This does not establish novelty, causal contribution, superiority, emergent memory, or a scientific successor. It does not reopen TH-002, Candidate #35, H7 or any terminal object, and it is not mixed into BUILD-SB-001.

## MAIN collision

PASS_NO_COLLISION. MAIN R147 is WAITING_EXTERNAL on PR #152 exact-head review. This prototype uses only the prior Forge branch and stable public APIs; it does not touch the SYSTEM_BUILD branch, PR, workflow, scorer, preserve path or scientific identity.

hard_floor_actions: NONE
