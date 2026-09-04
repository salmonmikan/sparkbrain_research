# v0.6.1 P5 Addendum — Dynamic and State-Structural Equivalence

## 1. Why the original P5 endpoint comparison is insufficient

The original P5 protocol correctly requires 11 interventions and rejects the inference:

```text
one explicit table fails
    therefore
emergent Field organization is proven
```

However, endpoint equivalence alone is still too weak. Two mechanisms can produce the same final
winner and boundary output while differing in the causal process that generates them.

Cross-line development makes that distinction important without changing candidate-003 evidence:

- RV01 R01-12D shows a mixed Field-versus-resource-matched-reservoir trade-off: ordered retention,
  exact-route recovery, and contamination are not interchangeable measurements of one capability;
- CX01 pre-formal review shows that train/eval state mutation and episode-finalization boundaries can
  change what a comparator is actually doing even when a high-level task contract appears unchanged.

Therefore P5 must compare causal dynamics and state structure as well as endpoints.

## 2. Strengthened comparison surface

For every one of the original 11 P5 challenges, candidate and explicit baseline now record:

```text
future competition endpoint
boundary endpoint
positive commit delta
competition trace over time
ambiguity-cardinality trace
latency from external observation to local effect
state-update locus or loci
state-update count
global indexed-lookup count delta
```

At the mechanism-run level they also record:

```text
persistent state units
persistent serialized bytes
peak transient state units
global keyed-query count
direct keyed-target-query requirement
forbidden privilege
explicit-predictor status
minimality evidence
P1-P4 contract status
```

No tolerance or success threshold is introduced. Equivalence is exact over the declared discrete
signatures.

## 3. Reduction rule

A candidate is classified as reducible to explicit anonymous memory only when all of the following
hold:

1. candidate and baseline cover every required P5 challenge;
2. candidate has already passed the P1-P4 contracts;
3. all endpoint signatures match;
4. all temporal/state-update signatures match;
5. the explicit baseline's minimality has been established rather than merely claimed;
6. baseline persistent and transient state is no larger than the candidate;
7. the baseline does not require more global keyed lookup or a direct target query absent from the
   candidate;
8. neither reduction depends on forbidden semantic/typed privilege.

Then and only then the classification is:

```text
behaviorally-and-dynamically-explicit-memory-equivalent
```

This is a negative classification for the stronger emergent-Field claim, not a statement that the
architecture is useless.

## 4. Matching endpoint, different dynamics

The following is explicitly non-equivalent:

```text
same final competition winner
same boundary output
but
external evidence affects the candidate after a different causal latency
or
state updates occur at different loci
or
ambiguity collapses through a different temporal trajectory
```

Classification:

```text
matching-endpoints-different-dynamics
```

This does not prove emergence. It says only that the tested explicit baseline has not reproduced the
candidate's full causal process.

## 5. Global lookup is a structural distinction

A central table that reproduces all outputs is not automatically a structural reduction of a local
candidate when the table requires global indexed queries or direct target lookup that the candidate
does not use.

Such a case is classified:

```text
matching-explicit-baseline-structurally-non-equivalent
```

The correct next action is to search for a smaller/local explicit baseline, not to declare the
candidate emergent.

## 6. Minimality is evidence, not a label

An explicit comparator is not the "smallest equivalent table" merely because its implementation
says so. Minimality must be established by the comparison programme.

A matching baseline without that evidence receives:

```text
matching-baseline-minimality-not-established
```

This closes an important loophole in which a deliberately oversized or globally privileged table
could be used either to overclaim reduction or to create an easy-to-defeat strawman.

## 7. Relation to RV01 and CX01

RV01 and CX01 remain behind the evidence firewall. Their outcomes do not enter the v0.6.1 formal
scorer.

They influence P5 only at the level of null-model design:

```text
RV01
    -> generic recurrent/reservoir dynamics must be taken seriously as a resource-matched null

CX01
    -> variable-order/context/temporal-memory predictors must be taken seriously as explicit nulls
    -> strict train/eval state boundaries are part of comparator validity
```

Historical CX01 development totals are not used as corrected freeze-ready evidence because the
pre-formal review requires the full matrix to be rerun after train/eval-boundary corrections.

## 8. Negative-completion implication

The stronger SparkBrain claim reaches a defensible negative completion if every admissible candidate
that passes P1-P4 is also reproducible by an established-minimal explicit predictor under both:

```text
endpoint behavior
and
causal dynamics / state structure
```

Alternatively, if no non-privileged candidate survives P1-P4, the stronger claim also terminates.

Failure of one table, one reservoir, or one comparator class is not sufficient positive evidence.
The null ladder must remain adversarial.

## 9. Implementation

```text
src/sparkbrain/evaluation/v061_p5_dynamics_equivalence_protocol.py
tests/v06/test_p5_dynamics_equivalence_protocol.py
```

The addendum is evaluator-only. It does not implement a learning mechanism, modify Primary, reopen
candidate-003, tune thresholds, or import RV01/CX01 results into the frozen v0.6.1 conclusion.
