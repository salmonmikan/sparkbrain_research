# CX01 candidate-002 user execution authorization

Date: 2026-09-12
Candidate: `cx01-candidate-002`
Governance state: **USER_AUTHORIZED_FOR_EXACTLY_ONCE_FORMAL_EXECUTION / NOT_STARTED**

## Authorization

The user explicitly authorized the CX/CX01 research line to proceed through an experiment boundary when the experiment is prospectively fixed, technically ready, and execution approval is the only remaining blocker. This line-scoped authorization was given on 2026-09-12 and applies to this already frozen, execution-seal-ready candidate.

For `cx01-candidate-002`, the previously recorded seal-ready identities remain authoritative:

- source freeze: `freeze/cx01-002-source` -> `e8483968ce43076b4c3fd04c76e62106e2031769`
- package freeze: `freeze/cx01-002-package` -> `c104be281285d52a732d5366fe36209d5688d973`
- candidate specification SHA-256: `5b51b5ac53a66b0ca79939c9eff976b53c75477ba38fd77547e2bd3858d095c8`
- semantic disposition: `PASS`
- governance disposition for the human-review-only condition: `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE`

This authorization permits the next control-plane operation to issue the candidate-specific execution seal, create the durable precommitted `STARTED` state required by the frozen workflow contract, and invoke the one-way formal workflow exactly once, provided all identities are revalidated immediately before consumption and no new scientific or integrity blocker is discovered.

## Integrity constraints

This authorization does not permit:

- moving or rewriting either freeze ref;
- regenerating or replacing the frozen package;
- changing the candidate, protocol, scoring policy, world grid, or execution contract after outcomes are observed;
- rerunning the candidate after `STARTED` or after any retained formal run for the same candidate/source identity;
- silently repairing a consumed or partially executed candidate;
- describing this automation as an independent human reviewer.

The candidate remains **NOT_STARTED** at the time this record is committed. The authorization itself does not issue a seal and does not consume the candidate.

## Execution-mechanism note

The frozen formal workflow `.github/workflows/cx01-formal-one-way.yml` is `workflow_dispatch`-only and requires a separately precommitted sealed control branch. The current automation connector does not expose a workflow-dispatch mutation. Therefore, this record preserves the authorization without prematurely creating `STARTED`: the control package must not be consumed unless the same run can also dispatch the bound formal workflow. If dispatch capability becomes available, revalidate the frozen refs and retained Actions history immediately before issuing the seal/STARTED state and executing exactly once.
