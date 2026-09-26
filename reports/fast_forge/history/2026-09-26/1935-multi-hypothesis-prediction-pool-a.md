# Fast Forge history — multi-hypothesis prediction pool A

generation_id: FORGE-20260926T193511+0900-MULTI-HYPOTHESIS-PREDICTION-POOL-A
produced_at: 2026-09-26T19:35:11+09:00
forge_id: FORGE-MULTI-HYPOTHESIS-PREDICTION-POOL-A
status: FORGE_INTERESTING
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

## Why now

Canonical science is empty and MAIN is occupied only with reviewed integration of BUILD-SB-001. Analyst R137 forbids feature mixing into that build. The current programme-level integration objective still needs plural hypotheses and an abstain/act boundary, while stable v0.5 stores per-Assembly future-event counts but exposes only one top prediction.

## Probe

Implemented a Forge-only read-only view over `AssemblyPredictor.counts` that returns deterministic top-k hypotheses and abstains unless minimum observation, confidence, and margin requirements pass. No learning state is mutated.

## Diagnostic disposition

- 5/5 counts: alternatives retained, abstain.
- 8/2 counts: top event selected at confidence 0.8 / margin 0.6.
- one observation: abstain for insufficient support.
- immature/suppressed/no activation: abstain.

## Reduction

Killed immediately as a novelty idea: ordinary categorical histogram, explicit beam/top-k bookkeeping, and a standard reject option explain the behavior completely.

## Build value

Survives only as an engineering primitive and may be considered later as SYSTEM_BUILD_INPUT. It exposes plural alternatives and an explicit abstention boundary without altering stable predictor learning.

## Collision / integrity

main: d16403414fc7abebd23075fc401240971b8eb91d
Analyst: R137
MAIN/Relay: R146
BUILD-SB-001 head: e9b93456a0c37e2d1393463c167912e0e3968817
PR #152: open/unmerged at selection time
existing Forge completion work: untouched
consumed identities and immutable/formal/sealed/evidence/preserve/control refs: untouched

No scientific result is created.
