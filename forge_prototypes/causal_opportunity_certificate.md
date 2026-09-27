# Causal opportunity certificate — Forge prototype

Status: `FORGE_PROTOTYPE`  
Evidence: `NON_EVIDENTIARY / NONCANONICAL`  
Scientific credit: `0`

## Target capability

Before interpreting a null intervention, check whether a complete recorded event
surface contains at least one time-respecting path from post-intervention activity
of a treated actor to a declared readout.

The prototype returns one of:

- `CERTIFIED`: a deterministic shortest witness path exists;
- `NO_TREATED_ACTIVITY`: no state-bearing treated event was recorded;
- `NO_PATH_TO_READOUT`: treated activity exists but is disconnected from readout;
- `INCOMPLETE_TRACE`: the caller admits that the relevant trace surface is incomplete;
- `INVALID_TRACE`: IDs, readouts, or event ordering are inconsistent.

## Why now

Independent Audit R10 identified a general treatment/readout support risk: an
intervention may modify one population while the declared response is produced
only by directly cued, untreated units.  The diagnostic here is generic synthetic
tooling.  It does not rerun, repair, reinterpret, or reopen Candidate #35.

## Ordinary reduction

The implementation is deterministic directed-graph reachability with a temporal
ordering check and fail-closed input validation.  No new learning, memory, causal
inference, or cognitive mechanism is required.

## Claim boundary

A path certificate establishes only **causal opportunity on the supplied trace**.
It does not establish:

- that the intervention changed any event on the path;
- incremental or counterfactual causal contribution;
- absence of hidden untraced paths;
- readout sensitivity or lack of ceiling effects;
- capability, composition contribution, comparative superiority, or novelty.

An absent path is informative only when `trace_complete=True` is justified by an
independent trace contract.  Even a certified path still requires an appropriate
counterfactual or intervention comparison before causal effect can be claimed.

## Collision boundary

The prototype is isolated from `BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT` and does
not implement online scope routing, route-local revision, checkpoint/replay, or
any RD006 dynamics.  It reads only caller-supplied synthetic event graphs.
