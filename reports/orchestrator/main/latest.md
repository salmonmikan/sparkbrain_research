# MAIN Orchestrator — NI01 STARTED; fixed one-way execution in progress

Timestamp: `2026-09-18 16:47 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Latest designated Evidence Analyst handoff: `34ad5e0fa1a31cff7b8faebe845cf1d5442a602b` (mailbox tip `f75328c6e32f324287ece53901dd332d764eeef9`)  
Frozen NI01 execution authority carried by the package/STARTED marker: `d3626617c3b054afd726e468682aaa02d613bca0`

## Collision / authority reconciliation

RELAY resumed only from PRIMARY's explicit `WAITING_EXTERNAL` checkpoint. Immediately before mutation, the current `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the exact NI01 execution branch remained `research/ni01-no-ignition-selective-prediction-spec-20260918@dbfe7469dbbbc1adbb00789ab382de892a1b3563`; ordinary CI `35319571743` and dedicated formal pre-START `35319571793` were both `completed/success` on that same exact head. The latest Analyst handoff continued to authorize exactly one unchanged NI01 chain, with any semantic/scientific change forbidden.

Fresh namespace checks immediately before STARTED found no NI01 control ref, no NI01 preserve ref, and no NI01 evidence tag. SUB was `no_op` and explicitly avoiding NI01 MAIN-critical work. No fresh PRIMARY `RUNNING` lease on the same object was observed; RELAY claimed the MAIN lease before crossing the formal boundary.

## STARTED boundary crossed exactly once

Using the prospectively fixed `control_ref` from `configs/experiments/ni01/execution_authority.json`, RELAY created:

- control branch `control/ni01-no-ignition-selective-prediction-started-v1-20260918` from exact package head `dbfe7469dbbbc1adbb00789ab382de892a1b3563`;
- `artifacts/v03/ni01/official_v1/STARTED.json` with protocol `ni01-no-ignition-selective-prediction-protocol-v1`, identity `ni01-no-ignition-selective-prediction-official-v1`, frozen Analyst authority `d3626617c3b054afd726e468682aaa02d613bca0`, exact package commit `dbfe7469dbbbc1adbb00789ab382de892a1b3563`, and `no_retry: true`;
- STARTED commit `d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d`.

The NI01 identity is therefore **consumed from STARTED onward**. It must not be retried, repaired after consumption, retuned, or silently replaced.

## One-way workflow

The STARTED push triggered the registered workflow `NI01 no-ignition selective prediction one-way`, run **`35321054429`**, on exact STARTED head `d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d`. At checkpoint it is `in_progress`, attempt `1`.

Observed job state at checkpoint:

- checkout STARTED control ref: success;
- STARTED marker / no-clobber validation: success;
- checkout exact authority package: success;
- frozen Python setup: in progress;
- authority re-proof, target-free DEV threshold derivation, target-blind TEST raw acquisition, preserve, independent refetch/digest/cardinality, TEST target materialization, scoring/bootstrap, and terminal evidence: not yet executed.

Therefore **no new scientific information exists yet**. At this checkpoint there has been no official TEST raw acquisition, preserve ref, scoring result, or terminal evidence tag.

## Handoff

Lease is `WAITING_EXTERNAL`. The next MAIN/RELAY cycle should collect only workflow `35321054429` and reconcile its terminal effects. If successful, independently verify the preserve ref, preserved digests/cardinality/join bindings, evidence tag and result classification before marking `COMPLETED`. If the post-START workflow fails or evidence is invalid, the identity remains consumed and MAIN must stop terminally without retry, salvage, retuning, or automatic successor.
