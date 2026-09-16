# V061 A01 Family-C Generation-1 — Pre-START Static Reduction Decision

Classification: **REJECT_BEFORE_STARTED_STATIC_REDUCTION**  
Scientific execution: **NOT STARTED / NOT EXECUTED**  
Identity consumption: **NO**  
Identity: `a01-family-c-joint-return-local-field-gen1-v1`

## Exact bound object

Family-C branch:

```text
research/v061-a01-family-c-gen1-20260917
```

Proposal-binding commit:

```text
9cfddc6dc4d2beab090a9b38661a68dcec755ff7
```

Proposal specification SHA-256:

```text
4b574b7053efb50b59a8d7536c94d02a7a25bdfc5b1d7f88575c7b6fc3e614ac
```

Family-C extension binding SHA-256:

```text
690a62df641d0577e3f7d760354763a6f0ec69e33eedfdacb37e92e7c654dbbc
```

Analyst authority:

```text
d295a61d37903f1b7c34fd793c6aa6a6e25c5cb6
```

The proposal fixes the scientific question, selector source/lifetime, Field-only post-update carrier, update arithmetic, discriminator IDs, null IDs, resource/privilege matching, and negative stop rule before this reduction decision.

## Static reduction proof

The exact Gen1 candidate factorizes as:

```text
A = actual_pending_causal_provenance_capability
F' = U(F, A, signed_external_consequence)
expire(A)
later_output = C(F')
```

with fixed operators:

```text
U:
    F'[i] = 0.5 * F[i]
            + 0.5 * sign * indicator(i == selected_slot(A))

C:
    score(activity) = dot(F', activity)
```

The prospectively registered separable null
`v061-a01-cgen1-separable-address-plus-field-null-v1`
receives the same actual pending provenance capability at pairing and is defined by the same `A`, the same `U`, the same address expiration, and the same `C`.

It requires no additional persistent scalar state and no greater lookup privilege. It uses no semantic/typed lineage ID, evaluator-selected address, caller-selected lineage, or global belief lookup.

Therefore the candidate and the separable null have identical state transition and readout dynamics under the complete prospectively fixed discriminator set:

- **lineage swap:** both follow the same actual pending capability;
- **contradiction:** both apply the same signed local update;
- **future competition:** both expose the same post-update Field vector to the same dot-product readout;
- **bounded plurality:** both receive the same bounded set of actual pending causal capabilities and update the paired local Field slot;
- **P3 selector/carrier cross:** both use the transient address only at update, then transfer the later effect with Field state alone.

No deterministic implementation could distinguish the candidate from this equal-resource/equal-privilege separable null without changing the bound scientific object.

## Decision

The exact Family-C Generation-1 object is statically subsumed by a prospectively registered equal-resource null. Under the Evidence Analyst `PRE_START_STATIC_REDUCTION` contingency, the correct action is to reject before STARTED rather than implement or execute merely to reconfirm an algebraic equivalence.

This is an **admission/reduction decision**, not a scientific measurement.

No Family-C:

- STARTED/control ref;
- one-way workflow dispatch;
- acquisition;
- raw or scored evidence;
- preserve/freeze/formal/evidence authority;
- identity consumption

was created.

The fresh identity remains unused, but this exact object must not be executed, retuned, rebound, or rescued under the same identity.

Any non-separable Family-C redesign, Generation-2 object, changed update operator, changed null/resource accounting, or replacement identity requires a new Evidence Analyst cycle.
