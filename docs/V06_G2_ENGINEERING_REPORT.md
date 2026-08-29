# SparkBrain v0.6 G2 Engineering Report

## Scope

V06-05 implements sparse local transition adaptation on top of the accepted G1 local temporal
expectation component. It does not implement Field reinjection or claim forward completion.

## Data flow

```text
external-to-external G1 statistics
        ↓
G1 local proposal
        ↓
G2 path-specific calibration
        ↓
ProvenanceLedger proposal + chain
        ↓
uncommitted LearningEligibility
        ↓
matching external event
        ↓
positive commit and local-path update
```

## Learning boundary

Proposal generation alone changes only pending/provenance state. It does not create a learned path
adaptation and does not increase confidence. Positive path changes occur only after the ledger has
recorded a matching external event and committed the associated eligibility record.

Contradictory external input may lower the path reliability posterior. It cannot commit a positive
update. Full contradiction cancellation and stale-chain cleanup remain V06-07 work.

## Adapted quantities

Each observed local path retains only:

- external confirmation count;
- external contradiction count;
- bounded confidence calibration;
- exponentially updated timing correction;
- exponentially updated magnitude correction.

No Assembly state, motif label, global sequence ID, correct action, or semantic target is stored.

## Tests

Focused tests cover:

- proposal/chain/eligibility registration;
- no adaptation on proposal generation;
- external-confirmation-only positive commit;
- endogenous-event rejection;
- contradiction without positive commit;
- timing and magnitude correction;
- directional sparse path separation;
- deterministic resolved-state round trip;
- pending budget fail-closed behavior;
- expiration without adaptation;
- pending restore requiring matching provenance state.

Local result before push: `11 passed`.

## Claim boundary

This result supports only the existence of an Assembly-free, externally confirmed local transition
adaptation mechanism. It does not support an internal model, missing-middle completion, semantic
prediction, or functional utility.
