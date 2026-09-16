# C19-v2 Executable Harness Readiness

Status: **pre-START harness scaffold; official execution remains forbidden**.

This package adds the executable state-machine boundary required by the Evidence Analyst handoff
without opening or verifying the official Belief-R cache. It preserves the scientific semantics
frozen at `90c936a7abca7eba0dac1f977753503551e73368`.

## What is now executable on synthetic/dev fixtures

- exact 55-row inventory traversal using the frozen protocol inventory;
- strict admission gating with a separate synthetic-only admission scope;
- network-off and no official fit/tune/select runtime assertions;
- exact five-family baseline executor registry coverage;
- target-blind raw-record validation;
- no-clobber raw JSONL writing;
- deterministic raw reconstruction and SHA-256 verification;
- immutable preservation-receipt validation;
- hard raw-before-score ordering.

The harness never locates, downloads, verifies, or opens Belief-R. Official examples are injected
by a caller only after a future execution admission and STARTED authority.

## Remaining pre-START blocker

The repository still does not freeze the **scientific execution implementation bindings** needed
to make the 55 rows meaningful:

1. there is no exact executable mapping from the three C19 input tracks plus G0/G1/E0 conditions
   to a frozen C19 model/runner implementation;
2. the five baseline family names are frozen, and reusable neural factories exist, but the exact
   family-to-factory/hyperparameter/checkpoint mapping required by the registered resource rules
   is not frozen.

The harness intentionally does not invent those mappings. Doing so would define scientific
execution semantics beyond the `90c936...` protocol anchor. This is therefore a
`PRE_START_HARNESS_INCOMPLETE` readiness result, not an execution failure and not a consumed
identity.

Official access, STARTED/control creation, workflow dispatch, one-way acquisition, preservation,
scoring, and identity consumption remain prohibited.
