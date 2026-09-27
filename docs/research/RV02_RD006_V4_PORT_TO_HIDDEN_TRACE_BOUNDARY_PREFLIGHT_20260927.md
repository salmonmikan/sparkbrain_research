# RV02-RD006 v4 PORT-to-hidden trace-boundary synthetic preflight

## Disposition

Status: `PASS`

Development phase: `OPEN_DEVELOPMENT`

Evidentiary status: `DEVELOPMENT_IMPLEMENTATION_ZERO_CONFIRMATORY_CREDIT`

Scientific credit: 0

## Implemented boundary

The ordinary external learner now has a versioned v4 implementation that can
apply an actual external PORT pulse trace to an actual hidden spike through an
already-existing, plastic, non-negative PORT-to-hidden edge. Existing
PORT-to-PORT behavior delegates unchanged to the prior learner.

No hidden trace is created. Hidden-to-PORT, hidden-to-hidden, absent, negative,
non-plastic, and new-edge updates remain forbidden.

## Synthetic verification

- The positive microfixture injected an external pulse into PORT 0.
- The Field emitted PORT 0 at 0.0 ms and hidden unit 36 at 5.5 ms.
- Exactly one existing `PORT_TO_HIDDEN` edge, 0→36, received the ordinary
  causal update.
- Checkpoint restore reproduced the same hidden spike, update, and final Field
  state.
- Existing PORT-to-PORT updates and final Field state matched the parent
  ordinary learner exactly.
- Every negative microfixture produced zero updates and no connection mutation.
- Fixed-window endpoints 0.5 ms and 6.5 ms are inclusive.
- The committed report reproduces deterministically and verifies its digest.

## Integrity boundary

This run executed only synthetic contract dynamics. It did not execute any of
the six RD006 families, an OFF/ON matrix, E0/E1/ES, a scale or reservoir
comparison, capability scoring, or held-out access.

The v3 topology, schedule, seed, resources, thresholds, weights, delays, gain,
stimulus, and ceilings are unchanged. The exact single invariant diff is the
ordinary learner's PORT-to-hidden trace boundary.

## Interpretation

The v4 learner boundary is implementable, serializable, replayable, and
fail-closed at the authorized synthetic-preflight surface. This is engineering
readiness, not evidence that the two-source dynamic gate will open or that any
capability improves.

Next action: stop for fresh Evidence Analyst reconciliation.
