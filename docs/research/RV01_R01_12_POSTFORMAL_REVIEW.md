# RV01 R01-12D / R01-12F post-formal review

## Evidence boundary

- R01-12F is consumed, fixed, and not rerunnable.
- This review changes no architecture, threshold, comparator, candidate, or raw result.
- R01-12D contains final summaries only.
- R01-12F contains intermediate Field probe traces, but the reservoir raw contains final probes only.
- Consequently, phase-by-phase Field/reservoir superiority is not identifiable from the fixed evidence.

## Evidence binding

| evidence | source | raw SHA-256 | cardinality |
|---|---|---|---:|
| R01-12D | `b163117512daca23b613c8a109a544833af7d360` | `8abc7fc462ed18cc7a57aa24365c9118d0e94579ec32f8b53d3bb1da368d8c67` | 15 worlds / 60 final route probes |
| R01-12F | `83d2c77d8ae3878727d2ed4e9e78bc169ce064b8` | `e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4` | 50 worlds / 200 final route probes |

## Aggregate comparison

| phase | architecture | ordered retention | exact-route rate | contamination / route | first-hop coverage |
|---|---|---:|---:|---:|---:|
| R01-12D | Field | 1.0000 | 0.4000 | 3.6000 | 1.0000 |
| R01-12D | reservoir | 0.9000 | 0.4000 | 2.9500 | 0.9500 |
| R01-12F | Field | 1.0000 | 0.4000 | 3.6000 | 1.0000 |
| R01-12F | reservoir | 0.9017 | 0.4000 | 2.9450 | 0.9500 |

The exact-route rate is **0.4000 for both architectures in both phases**. Field's higher ordered retention therefore does not establish cleaner route selection. Field has a retention/coverage advantage, but it pays for that breadth with more off-route activation.

## Family comparison

| family | phase | Field retention | reservoir retention | Field exact | reservoir exact | Field contamination/route | reservoir contamination/route |
|---|---|---:|---:|---:|---:|---:|---:|
| disjoint-routes | R01-12D | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| disjoint-routes | R01-12F | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| shared-cue-branches | R01-12D | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 6.0000 | 6.0000 |
| shared-cue-branches | R01-12F | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 6.0000 | 6.0000 |
| shared-prefix-branches | R01-12D | 1.0000 | 0.7778 | 0.0000 | 0.0000 | 4.0000 | 3.3333 |
| shared-prefix-branches | R01-12F | 1.0000 | 0.7778 | 0.0000 | 0.0000 | 4.0000 | 3.3333 |
| edge-reversal | R01-12D | 1.0000 | 0.8889 | 0.3333 | 0.3333 | 2.0000 | 1.3333 |
| edge-reversal | R01-12F | 1.0000 | 0.9000 | 0.3333 | 0.3333 | 2.0000 | 1.3000 |
| dense-route-load | R01-12D | 1.0000 | 0.8750 | 0.5000 | 0.5000 | 4.5000 | 3.3750 |
| dense-route-load | R01-12F | 1.0000 | 0.8750 | 0.5000 | 0.5000 | 4.5000 | 3.3750 |

### Family interpretation

- **Disjoint routes:** no Field-specific advantage. Both architectures retain and recover every route without contamination.
- **Shared cue:** both retain all ordered continuations, both fail exact branch recovery, and both contaminate equally. Retention alone is clearly insufficient for selection.
- **Shared prefix:** Field retains all continuations while reservoir retention is lower, but exact recovery remains zero and Field contamination is higher.
- **Edge reversal:** Field retains more under opposing interference, but exact recovery is unchanged and contamination is higher.
- **Dense load:** Field has better first-hop coverage and retention, but no exact-route advantage and substantially more contamination.

## Replicated and non-replicated signatures

The following signatures reproduced from R01-12D to R01-12F:

1. Field ordered retention remains 1.0000.
2. Reservoir ordered retention remains approximately 0.90.
3. Exact-route recovery remains exactly equal overall and within every family.
4. Field contamination remains higher overall and in the same families.
5. Field is never lower in mean retention at the world level, but it is tied in all disjoint and shared-cue worlds.
6. The family-level direction of retention, precision, contamination, and first-hop coverage is unchanged.

The exact numerical values that did not reproduce identically are limited to small reservoir shifts in edge-reversal and the aggregate induced by them: reservoir aggregate retention changes from 0.9000 to 0.9017, and edge-reversal contamination/route changes from 1.3333 to 1.3000. These do not change the qualitative signature.

## Formal Field phase diagnosis

The fixed R01-12F Field raw allows Field-internal phase analysis. It does **not** permit an intermediate-phase comparison with reservoir.

### Learned-position profile

| family | route position at probe time | ordered retention | exact-route rate | contamination / route | first-hop coverage |
|---|---|---:|---:|---:|---:|
| disjoint-routes | current | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| disjoint-routes | prior | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| shared-cue-branches | current | 1.0000 | 0.3333 | 3.0000 | 0.6667 |
| shared-cue-branches | prior | 1.0000 | 0.0000 | 5.0000 | 0.8889 |
| shared-cue-branches | future/untrained | 0.0000 | 0.0000 | 4.0000 | 0.4444 |
| shared-prefix-branches | current | 1.0000 | 0.3333 | 2.0000 | 1.0000 |
| shared-prefix-branches | prior | 1.0000 | 0.0000 | 3.3333 | 1.0000 |
| shared-prefix-branches | future/untrained | 0.3333 | 0.0000 | 2.6667 | 1.0000 |
| edge-reversal | current | 1.0000 | 0.6667 | 1.0000 | 1.0000 |
| edge-reversal | prior | 1.0000 | 0.4667 | 1.6000 | 1.0000 |
| dense-route-load | current | 1.0000 | 0.6250 | 2.2500 | 0.8125 |
| dense-route-load | prior | 1.0000 | 0.5393 | 3.3214 | 0.8991 |
| dense-route-load | future/untrained | 0.0000 | 0.0000 | 1.8536 | 0.1545 |

The decisive phase signature is not forgetting: previously trained routes retain ordered sequence at 1.0000. The failure is selection. In shared-cue and shared-prefix worlds, prior routes remain retained while exact recovery falls to zero and contamination grows. Shared-prefix also shows activation of not-yet-trained routes, including first-hop coverage of 1.0000. That is difficult to describe as precise memory and is compatible with uncontrolled spreading activation.

Dense-load phase progression reinforces the same distinction. As trained-route coverage rises from 0.1250 to 1.0000, contamination/route rises from 0.6750 to 4.5000, while exact recovery finishes at only 0.5000. The broadening is real, but it is not equivalent to route precision.

## Hypothesis verdicts

### A. Field is simply a stronger memory substrate

**Not supported as a claim of general selective-memory superiority.**

A narrow statement is supported: Field is a stronger substrate for retaining ordered continuations under interference. But if memory quality includes exact route recovery and exclusion of irrelevant routes, Field is not stronger on the fixed evidence.

### B. Field is stronger in continuation/coverage but lower in precision

**Best-supported interpretation.**

This hypothesis explains all major signatures simultaneously: higher ordered retention, higher dense first-hop coverage, unchanged exact-route recovery, and higher contamination.

### C. The difference is merely over-activation / contamination

**Partially supported and not resolved.**

Over-activation is a viable explanation because retention and contamination rise together, and some untrained branches activate before exposure. However, the fixed experiment does not measure whether the broadened candidate set later provides useful recoverable options. It therefore cannot distinguish useful plural candidate maintenance from uncontrolled spread.

## A01 connection

A coherent functional decomposition remains possible:

```text
RV01 Field
  retains a broad set of continuation candidates
        ↓
A01 external-evidence mechanism
  selects, weakens, or corrects candidates later
```

This is an interpretation, not a jointly tested result. R01-12F was not used to tune A01. Moreover, A01-MD-001 identifies its persistent carrier as explicit local causal-support state, not as a demonstrated Field-internal carrier. RV01 therefore supplies candidate breadth; current A01 supplies an explicit selector.

## Next experiment boundary

R01-12F remains closed. A follow-on must be a new RV hypothesis and a new candidate that independently measures:

- useful candidate-set coverage after delayed evidence,
- post-evidence selection precision,
- off-route activity mass and spatial spread,
- whether broad early activation predicts later correct recoverability,
- whether the same benefit survives a resource-matched non-Field substrate with matched activity mass.

The purpose would be to discriminate useful plural retention from uncontrolled spreading activation, not to repair or reopen R01-12F.

## One-sentence conclusion

> RV01のFieldはresource-matched reservoirより干渉下の順序付きcontinuationと一部のfirst-hop候補を多く保持するが、exact routeをより正確には回復できず、より大きなcontaminationを伴うため、現時点では選択的記憶ではなく広い候補保持substrateとして解釈するのが妥当である。
