# V06 — Field-Embedded Endogenous Dynamics

## Goal

Implement and test SparkBrain v0.6 without introducing an explicit Assembly state into the primary
runtime. Start from the accepted v0.5 baseline and follow `docs/V06_MASTER_PLAN.md` and
`docs/V06_RUNTIME_INVARIANTS.md`.

## Current accepted slice

- V06-00 protocol foundation;
- V06-01 provenance and anti-self-confirmation;
- V06-02 Assembly-free runtime and observer boundary;
- V06-03 canonical G0 queue-drain diagnostic.

## Next task

Implement V06-04: G1 local temporal expectation traces.

## G1 requirements

- learn only local source-target timing relations;
- do not use Assembly IDs, motif IDs, answer labels, or a global sequence state;
- emit `EndogenousPulseProposal` values with target, time, confidence, local path, validity, depth,
  and energy cost;
- create eligibility at prediction time but commit no positive update;
- commit positive learning only after a registered external event confirms the path;
- expose frozen, shuffled-time, and random-transition controls;
- keep the observer outside the runtime dependency graph;
- keep a deterministic CPU reference path.

## Required focused tests

1. repeated local lag creates a proposal;
2. reversed or shuffled lag does not receive the same confidence;
3. no Assembly field appears in state or checkpoint;
4. endogenous-only activity does not increase confidence;
5. matching external input commits bounded learning;
6. unrelated external input cannot commit learning;
7. expiry removes eligibility without positive update;
8. observer ON/OFF produces identical runtime state;
9. proposal depth, energy, and lifetime bounds fail closed;
10. checkpoint continuation is deterministic.

## Stop conditions

Stop and mark the task blocked if:

- a generic RNN or explicit Assembly memory is needed in the primary G1 path;
- an endogenous event is counted as an observation;
- the future target is read from evaluator metadata;
- observer output is fed back into runtime;
- forward and retrospective completion cannot be timestamped separately.

## Completion report

Report changed files, exact commands, test results, provenance audit, observer equality hash,
scientific boundary, negative results, and the next recommended task.
