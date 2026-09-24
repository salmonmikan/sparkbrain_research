# FAST FORGE: read-only Assembly completion design probe

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
status: FORGE_INTERESTING
prototype_kind: INTEGRATION
recommended_handoff: SYSTEM_BUILD_INPUT
new_scientific_result: false

## Target capability

Bounded read-only integration seam independent of MAIN's active BUILD-SB-001 critical path:

`partial internal ActivityPattern -> mature Assembly lookup -> completion proposal OR abstain`

The adapter does not relax Assembly formation, mutate TemporalAssemblyMemory, inject spikes, create an Assembly, or claim autonomous regeneration.

## Bounded design

The executable Forge adapter:
- inspects only mature, unsuppressed Assembly candidates;
- requires the observed ordered units to be an ordered subsequence of a stored prototype;
- scores with stable v0.5 pattern_similarity;
- keeps the stable formation threshold 0.66 unchanged and uses a completion-only development threshold 0.55;
- requires a best-vs-second margin of 0.08;
- abstains on no compatible candidate, low similarity, ambiguity, or already-complete input;
- returns only an inspectable proposal with assembly id, similarity, margin, missing positions and missing units.

The completion-only threshold and margin are Forge development diagnostics, not canonical defaults or scientific parameters.

## Static diagnostic

For prototype (1,2,3,4)/(0,1,2,3) and partial cue (1,3)/(0,2), the exact stable formula gives:
- edit similarity 0.50
- Jaccard 0.50
- timing similarity 1.00
- total 0.6000000000000001

This is below stable formation threshold 0.66 but above completion-only 0.55. Missing positions are (1,3), units (2,4).

A competing prototype (1,5,3,6)/(0,1,2,3) gives the same 0.6000000000000001 for the same cue, so the 0.08 margin guard abstains at margin 0.0.

A 3-of-4 cue (1,2,3)/(0,1,2) scores 0.80 and already clears stable 0.66, so the separate completion path mainly targets weaker partial cues.

## Strongest ordinary reduction

Nearest-prototype associative pattern completion / content-addressable memory with rejection/abstention. Stable v0.5 already provides the similarity machinery. No new regeneration principle is identified.

## Engineering usefulness

Potentially useful as a future SYSTEM_BUILD input because it separates Assembly formation/learning from read-only partial-cue completion while making ambiguity explicit.

Usefulness does not establish scientific novelty.

## Scientific claim boundary

This prototype does not establish autonomous Assembly regeneration, de-novo internal-state completion, causal contribution to downstream behavior, superiority over associative memory, a new candidate, or any canonical scientific result.

A feedback/re-injection experiment would be a distinct Forge object requiring a fresh collision and claim-boundary review.

## MAIN collision check

PASS_NO_COLLISION. BUILD-SB-001 source/acceptance/protected integration, H7, Candidate #34/#35, RVT35, TH-002, protected evaluators/held-out targets, and scientific refs are untouched.

## Utility

No Utility request.

hard_floor_actions: NONE
