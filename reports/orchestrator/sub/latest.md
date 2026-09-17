# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-17T22:47:36+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `9f88fba973f54bc6608d183aacfaccd7952a229f`

Formal `sub_lane` and `sub_fallback` remain null. MAIN owns C19-R1 end-to-end on `research/c19-r1-revision-authority-reduction-20260917@c23736b63e6100bcdc38e7f11d94c782eb6273dc`; exact-head ordinary CI `35221764016` and pre-START `35221764005` are green, but current Analyst authority still forbids R1 STARTED/execution pending fresh authorization. Fresh reconciliation found no `control/c19-r1*` STARTED ref. SUB did not touch R1, C19-v4, consumed C19 identities, official Belief-R inputs/outputs, preservation, scoring, control authority, or successor design.

## Exploratory target

Selected exactly one independent NON_EVIDENTIARY target: **H6 workspace broadcast communication-accounting sensitivity**. New branch: `research/exploratory-sub-h6-workspace-accounting-20260917@3904596cdb6377fc460435bf1b8a6dcdadff4fab`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Implemented:
- `scripts/exploratory_h6_workspace_accounting.py`
- `tests/test_exploratory_h6_workspace_accounting.py`
- `artifacts/exploratory_h6_workspace_accounting/README.md`

The fixed toy has 31 potential consumer modules, a direct-router budget of four recipients, fan-out `1/2/4/8/16`, and direct-router destination-knowledge probabilities `0.25/0.50/0.75/1.00`. Direct delivery is computed exactly from the binomial expectation; no formal data or tuning is used. Workspace recall is defined as 1.0 in the toy, while two deliberately different communication-cost contracts are compared: `shared_slot` charges one publication once, whereas `recipient_charged` charges the publication plus exposure to all 31 consumers.

Across 20 fixed scenarios, `shared_slot` makes workspace efficiency strictly better than direct routing in 19/20 scenarios and tied in 1/20. Under `recipient_charged`, direct routing is strictly more efficient in 20/20 scenarios. With perfect destination knowledge, the direct router reaches recall `1.0` for fan-out 1/2/4 and then saturates its four-recipient budget at `0.5` for fan-out 8 and `0.25` for fan-out 16. At fan-out 8 and knowledge 0.25, direct expected recall is about `0.303` while workspace recall is `1.0`, yet the efficiency ordering still flips solely with the accounting rule.

Initial exact-head CI `35228743996` failed at lint before tests. SUB changed formatting only in its own exploratory script (`3904596c...`), with no toy-semantic change. Replacement exact-head CI `35229064353` completed **success**.

## Integrity / Analyst handoff

`evidentiary_status: NON_EVIDENTIARY`. This does not show that workspace broadcast is scientifically better or worse, and it does not upgrade H6. It shows that a future H6 efficiency result can be accounting-driven unless publication/read/exposure cost, direct-router knowledge/overhead, message budgets and matched coordination quality are frozen prospectively.

Candidate future formal question: under a prospectively fixed communication-cost contract and matched coordination quality, does a capacity-limited workspace retain a coordination/communication advantage over direct routed communication, a shared recurrent-state reduction and other matched alternatives across a predeclared module/fan-out regime?

Before formalization, a fresh object must define task/coordination semantics, router-knowledge and routing-overhead assumptions, fan-out/read/exposure accounting, comparator definitions, message/capacity budgets, quality matching, module/fan-out regime, uncertainty/seeds/runtime, tuning budget, success/failure criteria and fresh protocol/package/runtime/identity/integrity gates. None of the exploratory numbers should be copied automatically into a formal protocol.

Promotion recommendation: `CONTINUE_EXPLORING` only after Evidence Analyst classification; do not automatically continue or formalize this H6 theme next run.

No formal scientific result, formal identity consumption, STARTED/control authority, one-way workflow, official input access, scoring, preserve/freeze/formal/evidence ref, PR or merge was created. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.

Completion target reached: one bounded independent H6 accounting-sensitivity diagnostic with green final exact-head CI.
