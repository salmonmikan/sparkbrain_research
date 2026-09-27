# SparkBrain Fast Forge — plural scope posterior router

- schema_version: `2`
- generation_id: `FORGE-20260927T095427+0900-PLURAL-SCOPE-POSTERIOR-CI-CLEAN`
- produced_at: `2026-09-27T09:54:27+09:00`
- forge_id: `FORGE-PLURAL-SCOPE-POSTERIOR-A`
- source_design_id: `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-plural-scope-posterior-a`
- exact_prototype_head: `f5e0968f5292a392c984fbe2efb011a23a49f86f`
- ci_run: `36283779602`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: `0`
- new_scientific_result: `false`

## Question / why now

Theory R6 leaves an integration seam between internally allocated scopes and the plural-hypothesis/reject path: when several existing scopes are plausible, can a bounded component retain several alternatives and abstain instead of collapsing immediately to one scope, without accepting caller-supplied regime/episode/scope identity?

This is independent of MAIN's current RV02-RD006 D0 line. MAIN R155 has a durable D0-inconclusive development result awaiting Analyst reconciliation; this Forge prototype neither reads its result artifacts nor changes that line.

## Prototype

Added:

- `forge_prototypes/plural_scope_posterior.py`
- `forge_prototypes/plural_scope_posterior.md`
- `tests/test_forge_plural_scope_posterior.py`

The router reads only:
- internal scope centroids already held by the Forge allocator;
- the current admissible observation vector;
- prediction error.

It ranks existing internally minted scope tokens together with a synthetic `NEW_SCOPE` alternative, retains bounded top-k alternatives, and selects only when preconfigured mass and winner-margin thresholds pass. Routing is read-only: ranking `NEW_SCOPE` does not mutate or allocate a scope.

## Diagnostics / observations

Bounded tests verify:

1. the public route API contains no scope/episode/regime/entity/target/truth/evaluator input;
2. two equally supported existing scopes remain represented and the router abstains;
3. a clear return observation selects the prior internally minted scope;
4. a large mismatch can rank `NEW_SCOPE` without mutating allocator state;
5. at least three bounded alternatives can be retained;
6. route output is deterministic across allocator checkpoint/restore.

Exact-head GitHub CI `36283779602` succeeded on Python 3.11 and 3.13, including lint, local readiness, full tests and bundle validation.

## Ordinary reduction

The prototype reduces to normalized radial/RBF-like scoring over stored prototypes plus an explicit reject option. The `NEW_SCOPE` score is a fixed heuristic function of prediction error.

It is not a calibrated Bayesian posterior, latent-cause inference result, new context-discovery mechanism, new memory mechanism or new learning rule.

## Engineering usefulness

The component supplies a missing integration function: scope ambiguity can remain explicit rather than being destroyed by hard nearest-scope assignment. It also cleanly separates "a new scope is plausible" from "allocate a new scope", which allows a future build to keep mutation authority behind a separate prospective policy.

## Scientific claim boundary / limitations

- fixed temperature, error scaling, mass and margin thresholds are not learned or calibrated;
- masses are heuristic normalized scores, not validated posterior probabilities;
- no matched HMM/BOCPD/mixture comparator was run;
- no system-level update/separate/reuse task was run;
- no composition contribution or comparative advantage was established;
- the prototype does not establish true latent-cause identity;
- no candidate/build/FORMAL identity is created;
- usefulness does not establish scientific novelty.

## MAIN collision check

PASS. MAIN owns RV02-RD006 and awaits Analyst reconciliation after R155 D0 inconclusive. E0/E1/ES, scaling and reservoir comparisons remain outside Forge. SB001 is already integrated and was not modified. No terminal/consumed/frozen scientific object or authoritative science/evidence ref was touched.

## Inputs / refs

- main: `cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- Analyst: `EVA-20260927T070206+0900-R144-RD006-BRANCH-LIT45-FORGE-HANDOFF-RECONCILED`
- Control: `CTRL-20260927T065000+0900-R88-P0-FORGE-HANDOFF-RECONCILED`
- MAIN: `MAIN-20260927T092301+0900-PRIMARY-R155-RD006-D0-INCONCLUSIVE`
- Theory current: `THEORY-20260927T094100+0900-R7-NO-PROPOSAL-LIFECYCLE-RECONCILIATION-5A7C9E31`
- source integration design: `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001` from Theory R6
- Literature: R45
- Audit: R10
- Methodology: R126
- Utility: `UTILITY-20260927T052236+0900-P0-DURABILITY-WINDOW-RECON`
- source Forge branch: `forge/20260927-internal-scope-confirmation-guard-a@0b3f8a5e074b346ef18b10ddf3c0893ba6996043`

## Metrics this run

- scientific novelty probes: 0
- scientific kills: 0
- scientific survivors: 0
- integration prototypes: 1
- integration prototypes useful: 1
- integration prototypes exact-head CI green: 1

## P0 observation

Prototype branch creation, object publication, non-force ref update and exact-file readback succeeded on the first publication attempt. This proves only this Forge path succeeded in this run; it does not close INC-GITHUB-PERSISTENCE-20260925-001 or prove a repository-wide/root-cause resolution.

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

A later Analyst may choose to include this as a noncanonical engineering input in a fresh SYSTEM_BUILD. It carries zero scientific credit.
