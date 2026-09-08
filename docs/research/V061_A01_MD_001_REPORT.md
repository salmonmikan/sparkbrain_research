# V0.6.1 A01-MD-001 mechanism discrimination report

## Evidence status

A01-MD-001 is a fixed development diagnostic, not a replacement formal candidate and not a rescore of candidate-003.

| item | fixed value |
|---|---|
| executed source SHA | `e5882c060bf3029415d49c22d9130d59ecbadd00` |
| workflow run | `34234838728` |
| raw result SHA-256 | `361cc46b60ad9f09be7d71e69ecaabd82e9dada828dc64da46772c110e9f18f6` |
| internal result digest | `dbae940526222f72d3f5d1cb0d446db57addf578d4ec96e5df8641d4f357d7b4` |
| preservation commit | `febdc1dbea0b7f84b1625be51f44075d9fa5a8da` |
| threshold tuning | none |
| candidate-003 touched | no |
| forbidden runtime privilege | none detected |

The discriminator was executed after implementation was fixed. Subsequent interpretation does not alter its runtime, thresholds, or observations.

### Evidence-notation correction

The fixed raw artifact reports `155` serialized persistent-state bytes for both A01 and the N1 baseline. An earlier version of this report transcribed that value as `95`; the raw artifact, its SHA-256, and the internal result digest were not changed.

The raw fields `global_keyed_query_count=0` and `direct_keyed_target_query=false` mean that neither mechanism performs a global or direct world-target lookup. They do **not** mean that keyed access is absent: both mechanisms read and update an explicit local path-addressed support record. This report-only correction does not change any P1-P5 verdict and makes the explicit-memory reduction boundary more precise.

## Executive verdict

| required item | verdict |
|---|---|
| P1 causal-lineage discrimination | **SUPPORTED** |
| P2 world-to-local circulation | **SUPPORTED** |
| lineage selectivity | **SUPPORTED** |
| contradiction correction | **SUPPORTED** |
| absence/replay leakage | **not detected** |
| future shared-root competition change | **SUPPORTED** |
| actual persistent carrier locus | `L.local-transition.a01-causal-support` |
| transient routing locus | `R.transient-return-address` |
| anonymous sign-classification locus | `C.anonymous-consistency` |
| independent Field carrier | **not observed** |
| P3 state-locus separation | **SUPPORTED** |
| P4 bounded ambiguity | **SUPPORTED** |
| P5 dynamic/table-equivalence | **behaviorally-and-dynamically explicit-memory-equivalent** |
| value of continuing P3-P5 | high for reduction diagnosis; not evidence of Field emergence |
| reduction to explicit anonymous memory | **supported** |

## P1 — causal-lineage discrimination

All preregistered conditions were run against the A01 runtime rather than filled from evaluator labels.

| condition | observed effect | verdict |
|---|---|---|
| matched causal lineage | only the ancestry-recovered causal path gained positive support | pass |
| lineage swap | credit followed the swapped causal ancestry rather than the previously matched path | pass |
| external confirmation | causal-path support rose and its future proposal confidence increased | pass |
| external contradiction | causal-path contradiction count increased and the earlier competition advantage was removed | pass |
| external absence | no support differentiation and no positive commit | pass |
| internal replay only | rejected as non-external; no support differentiation and no positive commit | pass |
| matched noncausal lineage | no equal credit leakage | pass |

The clearest correction trace was:

```text
support score local:A->B: 0 -> +1 -> 0
competition B/C:           0.5/0.5 -> 0.6667/0.5 -> 0.5/0.5
                         confirmation           contradiction
```

Positive credit therefore requires an independently registered external observation with exact boundary parentage. Absence and internal replay do not create positive differentiation.

### Selectivity boundary

The runtime credits every `local_path_id` recovered from the causal proposal ancestry. It selects the causal provenance lineage and excludes unrelated matched lineages, but it does not solve finer causal attribution among multiple path segments inside the same ancestry. The supported claim is lineage-level selective return, not identification of one uniquely responsible edge inside a multi-edge lineage.

## P2 — world-to-local circulation

The base local temporal learned state was held equal across the two arms. Only the anonymous world relation was changed so that external evidence returned through lineage A in one arm and lineage B in the other.

| arm | selected path after evidence | future shared-root competition |
|---|---|---|
| world relation A | `local:A->B` | `B=0.6667`, `C=0.5000` |
| world relation B | `local:A->C` | `B=0.5000`, `C=0.6667` |

The base temporal state hash remained equal, the causal-support state hash changed, and the later competition winner changed. This is not a case where only final re-entry differs: the anonymous external relation changes persistent local support and then changes a later shared-root competition.

## P3 — state-locus cross-transplant

The state partition remained the declared four-locus partition:

- `L`: local transition state, including A01's path-local causal-support counters;
- `F`: Field state/provenance-origin input;
- `C`: anonymous consistency relation state;
- `R`: transient historical return address carried by live proposal ancestry.

No fifth undeclared persistent state was introduced for the transplant.

| isolated transplant | donor competition transferred? | interpretation |
|---|---:|---|
| `L` after learning | yes | persistent competition bias resides in local transition state |
| `F` after learning | no | Field state does not independently carry the learned A01 bias |
| `C` after learning | no | anonymous relation changes re-entry classification, not already learned competition |
| `R` during attribution episode | yes, by redirecting the update | R selects which existing L path receives evidence while live |
| persistent `R` after pairing | not applicable | R is consumed and is not persistent learned state |

The actual carrier is therefore:

```text
persistent carrier: L.a01-causal-support
transient router:   R.proposal ancestry / return address
sign classifier:    C.anonymous consistency
independent carrier: not F
```

This result supports the routing hypothesis in a limited sense: anonymous world evidence can return to the causal lineage. It does **not** support the stronger claim that Field dynamics themselves store or circulate the resulting credit.

## P4 — bounded ambiguity

Both lineages remain co-maximal before evidence. No early winner is forced. Later independent external evidence differentiates only the causal lineage; contradiction moves only the implicated lineage in the corrective direction; external absence and replay preserve the undifferentiated state.

The initial co-maximal cardinality is two in every P4 trial. Success therefore does not depend on forced early winner-take-all.

## P5 — dynamic and table equivalence

A01 was compared with the minimal N1 explicit local eligibility-memory baseline using all required challenges:

- matched causal lineage;
- lineage swap;
- external contradiction;
- external absence;
- internal replay only;
- bounded ambiguity;
- world-relation permutation;
- state-locus transplant;
- identifier permutation;
- physical trajectory substitution;
- unseen lineage combination.

The comparison covered endpoint behavior and the required dynamic/state signatures:

| dimension | A01 | minimal explicit N1 baseline |
|---|---|---|
| competition trace | matched | matched |
| ambiguity-cardinality trace | matched | matched |
| external observation to local effect latency | one subsequent proposal step | one subsequent proposal step |
| update locus | local transition path | local transition path |
| update count | matched | matched |
| persistent state units | 4 in peak compared episode | 4 |
| persistent serialized bytes | 155 | 155 |
| transient peak units | 6 | 6 |
| global/direct world-target lookup | none | none |
| local path-keyed support lookup | required | required |
| identifier permutation | equivalent | equivalent |
| physical trajectory substitution | equivalent when provenance resolves to the same path | equivalent |
| unseen lineage combination | equivalent path-local updates | equivalent |

The tested baseline was not larger and was not more lookup-privileged. No endpoint or temporal-state mismatch falsified it. The formal P5 classification is therefore:

> **behaviorally-and-dynamically-explicit-memory-equivalent**

A01 is not an explicit next-target transition predictor in the narrow sense: it does not store a direct world target prediction table. However, its effective mechanism reduces to an explicit path-addressed eligibility/support record fed by exact-parent provenance and anonymous confirmation/contradiction classification. It is therefore structurally close to a keyed eligibility table and typed consistency-memory mechanism.

## Scientific interpretation

The central hypothesis divides into two claims:

1. **Return claim:** anonymous external consequences can be routed back to the local causal lineage that produced them.
2. **Emergence claim:** the resulting credit is carried by an irreducible Field-organized dynamic rather than explicit anonymous memory.

A01-MD-001 supports the first claim and does not support the second. The mechanism successfully performs causal return, correction, non-leakage, and future competition change, but the persistent effect is fully carried by explicit path-local support state and is dynamically reproduced by the minimal explicit baseline.

P3-P5 were therefore worth running: they prevent P1/P2 success from being overstated. The correct development diagnosis is not “A01 failed to route credit,” but:

> A01 routes anonymous external evidence to the causal lineage successfully, while its persistent credit mechanism remains reducible to explicit local anonymous support memory rather than demonstrated Field emergence.

## Forward boundary

Do not tune A01-MD-001 or rerun candidate-003. A future mechanism should be a new hypothesis and candidate. To exceed this diagnosis it must falsify the explicit-memory reduction through dynamic/state differences, not merely reproduce the same endpoints under renamed state.
