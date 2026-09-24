# FAST FORGE: delayed action credit routing

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
prototype_kind: INTEGRATION
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT

## Target capability

Allow delayed scalar feedback to reach more than the single most recently pending
v0.5 assembly/action pair, without modifying stable v0.5 source.

## Prototype

`EligibilityActionCreditRouter` wraps the stable `AssemblyActionPolicy` and keeps a
decaying trace keyed by `(assembly_id, action)`. A delayed reward updates every
surviving trace.

This is an ordinary eligibility-trace mechanism. It is not a scientific novelty
claim and does not infer causal responsibility.

## Synthetic diagnostic

For two consecutive actions A then B, decay=0.8 and learning_rate=0.3:

- delayed reward +1 gives A += 0.24 and B += 0.30;
- the stable last-pending-only policy gives A += 0.00 and B += 0.30.

A negative-reward diagnostic with decay=0.5 gives A -= 0.15 and B -= 0.30.

The second result is also the main limitation: a generic eligibility trace spreads
credit over recent actions and can therefore assign feedback to intervening actions
that were not causally responsible.

## Build value

Useful as a bounded action-credit primitive when feedback arrives after multiple
steps. The simpler established explanation is ordinary eligibility traces / TD-style
credit assignment. Stable v0.5 already uses eligibility at field-plasticity level;
this prototype only extends the same engineering idea to action-score credit.

## Claim boundary

Usefulness does not establish scientific novelty, native responsibility, causal
credit discovery, or superiority over established RL credit-assignment methods.
No protected target, evaluator label, consumed scientific identity, or MAIN
SYSTEM_BUILD branch was touched.
