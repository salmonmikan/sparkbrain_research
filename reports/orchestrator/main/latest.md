# MAIN Orchestrator — RELAY checkpoint

Timestamp: `2026-09-18 01:49 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `42836802e78abd26d19c5b8a789411f2b03d0ea1`

## MAIN frontier

C19-R1 representation-matched stateless revision-authority reduction remains the PRIMARY frontier under fresh execution authorization for exactly one one-way run.

## Relay continuation

Relay consumed the prior `WAITING_EXTERNAL` handoff. Exact package `7197ab0f9683616858859446ae9eed7b75707f25` remained current, and Analyst authority remained `42836802...`.

The two final admission gates both completed successfully on the exact same package SHA:
- ordinary CI `35246655185` — **success**;
- dedicated R1 pre-START `35246655189` — **success**.

Fresh checks also found no prior R1 STARTED branch, no R1 preserve branch and no R1 evidence tag.

## STARTED / one-way boundary

Relay created exactly one fresh control ref:

`control/c19-r1-revision-authority-started-20260918@62e4f03a2b276fa00627c6c198fa4cd3b8d8c2f2`

The STARTED marker is bound to:
- exact package `7197ab0f9683616858859446ae9eed7b75707f25`;
- Analyst authority `42836802e78abd26d19c5b8a789411f2b03d0ea1`;
- protocol `c19-r1-revision-authority-protocol-v1`;
- identity `c19-r1-revision-authority-official-v1`;
- target-free `atomic_idx` source-map digest `cb3ca63703bdab4107e896884908817680dd4fe4b5eebc32b6219075f0187bbb`.

R1 identity is therefore now **consumed / no retry**.

The STARTED push triggered the prospectively authorized one-way workflow:

`35248878958` — currently **in progress**.

A normal CI run on the STARTED commit (`35248878746`) is also in progress, but no second one-way execution is permitted regardless of its outcome.

## Science / integrity

New scientific information: **none yet**. No terminal R1 result, preserve ref or evidence tag has been observed at this checkpoint.

No scientific contract, preregistration, controller rule, representation, resource contract, metric, inferential rule or prior immutable C19-v4 evidence was changed.

## Stop / relay boundary

Lease is `WAITING_EXTERNAL`. Waiting for workflow `35248878958` is the only remaining valid action.

Next MAIN/Relay must collect **that same one-way run only**:
- if successful, verify raw preservation/refetch/digest ordering before target materialization/scoring, then verify the terminal evidence/tag and persist the fixed classification;
- if it fails after STARTED, preserve/verify diagnostics, keep R1 consumed with no retry, and STOP.

No automatic R2 or outcome-responsive redesign is authorized.
