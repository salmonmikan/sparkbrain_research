# FLY-0 hierarchical sensorimotor loop

Status: NON_EVIDENTIARY / NONCANONICAL Fast Forge prototype

This probe implements one bounded slice of
`ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`. It tests whether two
replaceable local modules can sit behind an explicit descending-modulation
surface, return ascending runtime feedback, arbitrate one bounded action and
commit an action-to-world transition atomically.

It does not allocate SB003, modify the integrated M1 implementation, reproduce
a fly brain, or provide scientific evidence.

## Prototype boundary

The synthetic world is a bounded line with one current position and target.
The event adapter exposes only signed current error and sequence. A trivial
reference supervisor maps the sign to `left`, `right` or abstention. Two
local modules receive that descending modulation:

- the existing structured FLY-0 topology wrapped behind a local-controller
  interface;
- an ordinary reactive reference controller using the same interface.

The loop commits only when exactly one local module is active. Module conflict,
unmodulated action, resource overflow or invalid state leaves the complete
world/feedback/sequence snapshot unchanged.

Ascending feedback contains module identity, side, event count, matched and
opposite motor counts, and first motor time. It intentionally contains no world
target or evaluator field.

## Bounded observation

Both controller implementations move the world from position 2 to target -1
in three accepted steps and reproduce identical same-history checkpoint tokens
after restore/replay.

Their resource exposures are deliberately not declared matched:

- wrapped structured FLY-0: 300 fired events per active step;
- reactive reference: 1 counted event per active step.

The shared interface and closed-loop function therefore survive a simple
replacement, but the result is not a fair performance comparison. The resource
mismatch is an explicit diagnostic, not evidence for or against either
controller.

## Verified guards

- exact checkpoint/restore/replay for the same history;
- complete no-write rollback on two active modules;
- complete no-write rollback on local event-budget overflow;
- controller-contract rejection during restore;
- bounded two-module action arbitration;
- feedback-surface check for target/oracle leakage;
- deterministic summary for structured and reactive replacements.

## Run

```bash
python -m pytest -q tests/test_forge_fly0_hierarchical_loop.py
python -m ruff check forge_prototypes/fly0_hierarchical_loop.py \
  tests/test_forge_fly0_hierarchical_loop.py
python -m forge_prototypes.fly0_hierarchical_loop
```

## Claim boundary

This prototype supports only the engineering claim that a small explicit
hierarchical interface can close a deterministic loop and fail closed under
the tested faults. It does not establish topology superiority, biological
fidelity, composition contribution, external validity, energy efficiency or
scientific novelty. FLY-0 and this extension remain Forge-only until Evidence
Analyst separately admits any SYSTEM_BUILD.
