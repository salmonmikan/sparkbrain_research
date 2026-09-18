# MAIN Orchestrator — NI01 execution authority bound; final CI pending

Timestamp: `2026-09-18 16:30 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `d3626617c3b054afd726e468682aaa02d613bca0`

## Frontier

The PRIMARY frontier remains **NI01 / H4 — native No-Ignition selective prediction**. FAST PATH remained valid; FULL RECONCILIATION was not triggered.

The prospectively reviewed scientific object remains frozen at `research/ni01-no-ignition-selective-prediction-spec-20260918@2664951b65dd18883d3d80862e80b86ac66cf24f`. Under the Analyst's conditional one-way authority, MAIN added only science-invariant execution/admission scaffolding and fast-forwarded the same research branch to final execution head `dbfe7469dbbbc1adbb00789ab382de892a1b3563`.

The exact diff from the reviewed scientific head is one commit and six added administrative/execution files only: NI01 execution authority, execution-authority checker, official runner, raw preserver, dedicated formal pre-START workflow, and one-way workflow. No frozen world, seed, candidate, comparator, scorer, loss, coverage guard, PASS/FAIL/INCONCLUSIVE threshold, bootstrap, runtime/device, join key, raw-before-score order, or other scientific contract file changed.

## Critical-path progress

The execution package is explicitly bound to Analyst `d3626617c3b054afd726e468682aaa02d613bca0`, scientific contract blob `3dc90b08f85e0e7c459e0c17e86ab338901fd4c6`, NI01 scorer blob `d3b3565a08277e6a94ef9be1e5bd13e86265f8f2`, official runner blob `d1602b22bacec1b4e8d2166bd0c184382e632d7e`, and preserver blob `390816f9d69604adc0ce3fbf21be93dd916256fd`.

The official runner keeps DEV threshold selection target-free, projects TEST raw without truth / target / `decision_justified` / target-derived scenario labels, requires the registered 46,080-step cardinality and unique `(world, seed, step_index)` keys, preserves raw before target materialization, then performs the registered deterministic scoring/bootstrap only after independent preserved-byte verification. The one-way workflow is no-retry and triggers only from the planned STARTED control namespace.

## Final-head gates

On exact execution head `dbfe7469dbbbc1adbb00789ab382de892a1b3563`:

- `NI01 formal pre-START` run `35319571793`: `completed/success`;
- `NI01 preformal contract` compatibility run `35319571868`: `completed/success`;
- ordinary `ci` run `35319571743`: `in_progress` at checkpoint.

Because ordinary CI is the only remaining external gate and no useful local critical-path work remains, STARTED has **not** been created. Identity `ni01-no-ignition-selective-prediction-official-v1` remains unSTARTED/unconsumed. No official TEST raw, preserve ref, TEST target materialization, scoring, or evidence tag has been produced, so there is **no new scientific information**.

## Handoff

Lease is `WAITING_EXTERNAL`. Relay continuation is expected. The next MAIN/Relay action is to collect ordinary CI `35319571743`. If it is green, re-fetch the Analyst authority, exact research head, identity/consumed state, and exact control/preserve/evidence namespaces immediately before mutation. If all remain clean, create STARTED exactly once from exact package head `dbfe7469dbbbc1adbb00789ab382de892a1b3563` and allow exactly one registered NI01 one-way workflow. If CI fails mechanically, only a science-invariant repair is allowed and all final-head gates reset. Any semantic/scientific change requires STOP and fresh Analyst review before mutation.
