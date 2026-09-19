# EXPLORATORY / NON_EVIDENTIARY — Assembly prototype lock-in order sensitivity

Source semantics: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Question

Can v0.5 `TemporalAssemblyMemory` produce a different number of mature assemblies
from the exact same multiset of episode patterns solely because the episode order
changes?

This is a bounded Discovery probe. It uses no repository dataset, trained
checkpoint, preserved formal raw material, held-out TEST input, consumed identity,
or official scorer.

## Fixed synthetic construction

The default similarity threshold is fixed at `0.66` and maturation requires three
distinct episodes. Three pattern types are each presented exactly three times, with
all nine episode IDs distinct.

Pairwise similarities under the repository's exact `pattern_similarity` metric:

| pair | similarity |
| --- | ---: |
| A-B | `0.7250000000000001` |
| B-C | `0.7250000000000001` |
| A-C | `0.45` |

Thus B is above threshold to both endpoints, while A and C are below threshold to
each other. The experiment exhaustively enumerates all `1680` unique permutations
of the identical multiset `AAABBBCCC`.

## Observations

Exactly three final states occur:

| initial prototype path | episode counts | mature assemblies | orders |
| --- | --- | ---: | ---: |
| `A -> C` | `[6, 3]` | 2 | 560 |
| `B` | `[9]` | 1 | 560 |
| `C -> A` | `[6, 3]` | 2 | 560 |

Every order beginning with B collapses all nine observations into one mature
assembly. Every order beginning with A or C ends with two mature assemblies.
Therefore `560/1680` orders produce one mature assembly and `1120/1680` produce two.

The thresholded similarity graph over {A, B, C} is connected, so an
order-invariant connected-component reduction has one component. The split is not
forced by the metric alone.

## Reduction / interpretation

The effect is directly attributable to the current greedy frozen-prototype
contract. Once a candidate exists, accepted observations increment counts but do
not update its prototype. Consequently the first exemplar fixes the reference
geometry. B can bridge both A and C only when it is the prototype; when A or C is
first, the opposite endpoint must seed another candidate.

This is not scientific evidence and does not establish novelty. It is, however,
an architecture-level representation-order sensitivity that can change mature
assembly cardinality before downstream prediction/action learning.

- Evidentiary status: `NON_EVIDENTIARY`
- Recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`
- Candidate next research layer: `ARCHITECTURE_STUDY`
- What would reduce it: on a prospectively fixed DEV-only study, if matched
  episode-order permutations change assembly IDs/counts but not downstream
  prediction/action behavior beyond an order-invariant clustering comparator,
  treat the effect as representation bookkeeping only.
- Scientific choices still open: DEV input family, order-permutation family,
  assembly identity matching, functional metric/horizon, order-invariant
  comparator, and resource matching.
