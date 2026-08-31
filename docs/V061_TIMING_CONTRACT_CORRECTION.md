# v0.6.1 Timing Contract Correction

## Status

Candidate-002 is retired as a failed one-way confirmatory run. Its formal evidence must not be resumed, repaired in place, or scored as a complete matrix.

The correction branch introduces a new runtime distinction:

- `drain_scheduled_events(end_ms)` processes only events that actually occur at or before the observation bound and leaves the Field clock at the last processed event;
- `advance_silence(end_ms)` preserves the existing behavior of advancing the Field clock to the requested endpoint;
- `present_external()` continues to reject any external timestamp earlier than the current Field clock.

The anonymous boundary path uses `drain_scheduled_events()` before emitting world consequences. Other Primary evidence paths retain the original settle-to-horizon behavior.

## Reproduced failure class

The retired candidate-002 grid contains 50 worlds. Twenty-two satisfy:

```text
boundary_lag_ms < max(evaluation_lags_ms) + 5.0
```

Under the frozen candidate-002 ordering, these worlds could return an external consequence after the evaluator had already advanced the Field clock beyond the consequence timestamp.

The first formal failure occurred at:

```text
family:    heldout-sparse-permutation
seed:      1001
condition: primary
error:     external cue cannot move Field time backwards
```

## Regression contract

The correction is accepted only when all of the following hold:

1. scheduled-event draining stops at the last actual event rather than fabricating elapsed time;
2. ordinary silence advancement still reaches the requested endpoint;
3. backwards external timestamps are still rejected;
4. all 22 retired candidate-002 timing-risk worlds complete the boundary path without a time reversal;
5. the original seed-1001 Primary execution produces and validates all nine evidence-domain records.

These checks are compatibility and failure-regression tests only. Candidate-002 results are not eligible for confirmatory scoring.

## Next confirmatory attempt

A new attempt requires a fresh candidate generation with disjoint held-out seeds, a new world-generation identifier, a newly frozen source SHA, a new one-way marker, and a new formal artifact namespace. Candidate-003 must not reuse candidate-002 as confirmatory evidence.
