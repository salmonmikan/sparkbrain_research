# H6 Workspace Accounting Sensitivity Probe

> **EXPLORATORY / NON_EVIDENTIARY**
>
> This artifact is hypothesis-generation material only. It is not a formal SparkBrain result, does not satisfy any H6 gate, and must not be promoted to evidence without a fresh prospective object.

## Question

Can an apparent coordination/efficiency advantage for a capacity-limited workspace broadcast be created or removed purely by how global fan-out is charged, relative to a direct router with imperfect destination knowledge?

This is deliberately separate from the active C19-R1 MAIN frontier and uses no formal, held-out, sealed, or official data.

## Fixed synthetic setup

- 31 potential consumer modules plus one sender/workspace publication operation.
- Direct-router send budget: at most 4 recipients per message.
- Relevant-consumer fan-out: 1, 2, 4, 8, 16.
- Independent destination-knowledge probability: 0.25, 0.50, 0.75, 1.00.
- Direct-router expected delivery is computed exactly from the binomial distribution; no Monte Carlo sampling or tuning is used.
- Workspace recall is defined as 1.0 in this toy because all potential consumers can inspect a published item.

Two communication-accounting contracts are intentionally compared:

1. `shared_slot`: one workspace publication is charged once regardless of readership.
2. `recipient_charged`: one publication plus exposure to all 31 potential consumers is charged.

The accounting alternatives are the object of the diagnostic. Neither is asserted to be the correct physical cost model.

## Observation

Across the 20 fixed fan-out/knowledge scenarios:

- under `shared_slot` accounting, workspace efficiency is strictly above direct routing in 19/20 scenarios and ties in 1/20;
- under `recipient_charged` accounting, direct routing is strictly more efficient in 20/20 scenarios;
- at perfect destination knowledge, direct routing reaches recall 1.0 for fan-out 1/2/4, then saturates its fixed budget at recall 0.5 for fan-out 8 and 0.25 for fan-out 16;
- for fan-out 8 and destination knowledge 0.25, direct expected recall is about 0.303, while workspace recall is 1.0; nevertheless the efficiency ordering still flips solely with the fan-out charging rule.

## Interpretation

This toy does **not** show that workspace broadcast is good or bad. It shows that H6 can become accounting-sensitive before any learning or task effect is considered. A future formal H6 object should prospectively fix at least:

- whether one global publication is charged once or per exposed/reading consumer;
- direct-router destination knowledge and routing overhead;
- communication/message budget matching;
- whether unread workspace exposure is charged;
- coordination-success/quality matching before comparing communication cost.

Without those choices frozen in advance, a broadcast-efficiency result can be manufactured by the accounting contract itself.

## Candidate formal question

Under a prospectively fixed communication-cost contract and matched coordination quality, does a capacity-limited workspace retain a coordination/communication advantage over direct routed communication, a shared recurrent-state reduction, and other matched alternatives across a predeclared module/fan-out regime?

## Promotion recommendation

`CONTINUE_EXPLORING` only. A formal object would still require fresh task semantics, routing-knowledge assumptions, cost accounting, comparator definitions, budgets, quality criteria, uncertainty treatment, seeds/runtime, success/failure criteria, and a new formal identity/package. None of the exploratory numerical values above should be copied automatically into a formal protocol.
