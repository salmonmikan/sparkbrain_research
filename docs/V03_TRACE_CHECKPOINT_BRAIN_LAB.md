# v0.3 trace, checkpoint and Brain Lab boundary

## C18 contract

`sparkbrain.v03_integration` is an additive, read-only integration namespace.
It accepts explicit v0.3 state from the perception/evidence/Coalition path and
does not mutate the accepted v0.2 engine, trace reader, `/api` surface, or
existing Brain Lab. New payloads identify schema `0.3`; a v0.2 payload is not
treated as a v0.3 payload.

Trace events record accepted/suppressed sensory events and salience terms,
evidence IDs, Coalition components, no-ignition, workspace broadcast, concept
candidates, checkpoints, and explicit intervention branches. A cited evidence
ID must already exist in stored evidence. The inspector consumes snapshots and
does not advance a counter or reconstruct hidden state.

## Replay and intervention

A checkpoint retains config, exact state, branch lineage and the trace hash
chain. Replay verifies the chain and terminal state hash, then restores only
the stored checkpoint state. It does not infer evidence from UI data.

Forks retain the parent checkpoint ID and record an intervention event. The
official C18 smoke case removes one cited evidence ID on a child branch, then
records no-ignition because the independent-source condition is no longer met.

## Artifact and claim boundary

The exact official/reproduction artifacts are under
`artifacts/v03/c18_brain_lab/{official,reproduction}`. The static export is
local and has no CDN, remote API or hosted assets. This validates deterministic
observability/replay plumbing only. It does not support semantic understanding,
functional-organ formation, biological equivalence, energy efficiency or an
external-performance claim.
