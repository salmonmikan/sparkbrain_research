# v0.6.1 Pre-Mechanism Admission and Negative-Completion Rule

## Purpose

This protocol prevents two symmetric errors after candidate-003:

1. implementing a new mechanism merely because it might improve the failed score;
2. terminating the stronger Field-organized causal-credit hypothesis before the registered
   mechanism families and null models have been tested.

It is diagnostic governance only. It does not reopen candidate-003, alter Primary, or authorize a
fresh formal capability execution.

## Pre-mechanism admission

A proposed mechanism is implementation-ready only if all of the following are declared before its
capability outcome is observed:

```text
causal-lineage swap test
external-confirmation-only positive update
contradiction / reversal correction
future local-competition effect
bounded ambiguity behavior
no forbidden typed / semantic / evaluator privilege
expected P3 carrier locus or loci
smallest explicit-memory null
strong generic recurrent null
negative stopping observation
```

Missing any item fails closed. In particular, naming a Field variable, adding decay, or making an ID
anonymous does not satisfy the contract.

The machine evaluator is:

```text
src/sparkbrain/evaluation/v061_premechanism_admission.py
```

and its tests are:

```text
tests/v06/test_premechanism_admission.py
```

## Immutable proposal specification binding

The checklist above is not accepted as a set of free-floating booleans. An admitted proposal must
also identify the concrete discriminator and null specifications it commits to:

```text
lineage-swap protocol ID
contradiction protocol ID
future-competition protocol ID
bounded-ambiguity protocol ID
P3 cross-transplant protocol ID
explicit-memory null ID
recurrent/reservoir null ID
negative stopping-observation ID
```

Together with the mechanism family, declaration flags, forbidden-privilege declaration, and expected
P3 carrier loci, these fields form a canonical JSON proposal specification. The evaluator computes a
SHA-256 digest over that specification.

Admission requires the proposal's stored binding hash to match the recomputed digest exactly:

```text
bound proposal specification
    -> implementation / diagnostic execution

changed protocol, null, carrier expectation, or declaration
    -> hash mismatch
    -> proposal-specification-binding-invalid
    -> register a new proposal generation instead
```

This does not prove scientific adequacy. It prevents a proposal from silently changing its
falsifiers or null models after results are visible.

Every later `CandidateDisposition` used by the negative-completion evaluator also carries a valid
proposal-specification SHA-256, so terminal accounting remains tied to a preregistered proposal
identity rather than an unbound candidate label.

## Registered mechanism families

Negative completion cannot be declared by testing only one favored mechanism. The current stronger
hypothesis programme must cover all three registered non-privileged candidate families:

```text
1. transient-return-address
2. distributed-field-trace
3. joint-return-and-local-field-update
```

These families correspond to the main unresolved causal-carrier possibilities after D5-D11 and
P1-P5. They are not assumed to work.

The explicit anonymous transition-memory and generic recurrent/reservoir cases remain adversarial
nulls rather than evidence for the stronger Field-organized claim.

## Candidate disposition

For negative-completion accounting, every implemented candidate receives a fail-closed disposition:

```text
proposal specification hash
mechanism family
non-privileged
P1 passed
P2 passed
P3 passed
P4 passed
P5 assessed
P5 reduced to explicit memory
```

A candidate is a P1-P4 survivor only if it is non-privileged and passes all four causal
discriminators. A typed, semantic, evaluator-keyed, or otherwise privileged mechanism does not count
as a survivor even if it performs well.

P5 reduction cannot be recorded before P5 has actually been assessed. An invalid or missing proposal
SHA-256 also fails closed before terminal accounting.

## Stop rule

The stronger claim of emergent Field-organized anonymous causal credit may be terminated only when:

```text
candidate programme explicitly complete
AND
all registered mechanism families completed
AND
all candidate dispositions are bound to registered proposal specifications
AND
(
    no non-privileged candidate survives P1-P4
    OR
    every P1-P4 survivor has completed strengthened P5
    AND every survivor reduces to established-minimal explicit anonymous memory
)
```

If the programme is incomplete, the evaluator returns:

```text
programme-incomplete
```

If one or more required mechanism families remain uncovered:

```text
mechanism-family-coverage-incomplete
```

If a P1-P4 survivor still lacks P5:

```text
p5-incomplete-for-survivors
```

If at least one fully assessed survivor is not reduced by the tested established-minimal explicit
baseline ladder:

```text
stronger-field-claim-remains-open
```

This last state does not prove emergence. It only means the preregistered negative-completion
condition has not been met.

## Valid negative completions

Two terminal classifications are currently permitted:

```text
negative-completion-no-p1-p4-survivor

negative-completion-all-survivors-explicit-memory-reducible
```

The first says none of the registered non-privileged mechanism families produced a causal-credit
carrier that survived the discriminators.

The second says causal behavior survived P1-P4 but the surviving mechanisms were fully reproducible
by established-minimal explicit anonymous memory under the strengthened endpoint, temporal,
state-locus, state-size, and lookup-privilege P5 contract.

Neither conclusion says SparkBrain as a whole is impossible. Both terminate only the stronger claim
that anonymous causal credit requires or demonstrates emergent Field organization under the current
premises.

## Evidence firewall

The stop rule consumes only prospective mechanism dispositions created under this protocol. It does
not reinterpret the candidate-003 formal matrix, and it does not pool RV01 or CX01 results into the
v0.6.1 formal record.

RV01 and CX01 continue to influence only adversarial null-model design and protocol quality through
the cross-line evidence firewall.
