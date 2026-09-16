# V061 A01 Family-C Generation-1 — Joint Return Address + Local Field Update

Status: **prospectively bound pre-START contract; NOT execution-admitted**  
Owner: MAIN research frontier  
Mechanism family: `joint-return-and-local-field-update`  
Generation: `1`  
Prospective identity: `a01-family-c-joint-return-local-field-gen1-v1`  
Analyst authority: `d295a61d37903f1b7c34fd793c6aa6a6e25c5cb6`

## 1. Scientific question

Can actual anonymous transient causal return provenance select which local/Field substructure receives external consequence while persistent Field-local state alone carries the resulting effect into later competition, with genuine plural-lineage discrimination and without reduction to equal-or-lower-resource explicit, recurrent, belief-state, or separable address-plus-Field nulls?

This Generation-1 object is prospectively specified after the Family-B pre-START closeout. It does not alter or reuse any consumed Family-A identity and does not rescue the rejected Family-B object.

## 2. Exact candidate organization

The candidate has two causally distinct stages.

### Update-time selector

At exact external pairing, the runtime supplies the **actual pending causal provenance capability** for the event that produced the return. The capability points to one anonymous local Field slot. It is not a semantic lineage label, task/evaluator key, answer key, caller-selected address, or global lookup key. The candidate does not search a table to choose a lineage.

At most two unresolved pending provenance capabilities may coexist in the bounded-plurality construction. The external pairing layer supplies the capability belonging to the actual event being resolved.

### Persistent carrier

Persistent Field state is a fixed-width credit vector:

```text
width = 4
decay = 0.5
credit in [-1, 1]^4
```

For an external signed consequence `sign in {-1,+1}` paired to actual pending slot `j`, the prospectively fixed update is:

```text
credit_prime[i] =
    decay * credit[i]
    + (1 - decay) * sign * indicator(i == j)
```

After that update, the transient provenance capability is discarded. It is not part of the post-update carrier.

Later local competition receives only:

```text
score(activity) = dot(credit, activity)
```

where `activity in [0,1]^4`. No transient address, semantic identifier, evaluator lookup, or global belief lookup is available to this later score.

## 3. Prospectively fixed discriminator identities

| role | ID | fixed requirement |
|---|---|---|
| lineage swap | `v061-a01-cgen1-lineage-swap-v1` | with pre-update Field fixed, changing the actual pending provenance before external pairing must change which local Field slot is updated |
| contradiction | `v061-a01-cgen1-contradiction-v1` | matched negative consequence must reverse/correct the selected local Field contribution |
| future competition | `v061-a01-cgen1-future-local-competition-v1` | after the selector expires, the updated Field alone must change later competition |
| bounded plurality | `v061-a01-cgen1-bounded-plurality-v1` | two anonymous pending causal provenances may coexist and be resolved according to the actual paired event without winner-only semantic selection |
| P3 selector/carrier cross | `v061-a01-cgen1-address-at-update-field-carrier-cross-v1` | address-at-update selects the update; post-update Field-only transplant transfers the later effect; address-only state after update is insufficient |
| explicit null | `v061-a01-cgen1-explicit-return-address-eligibility-null-v1` | explicit return-address/eligibility memory |
| recurrent null | `v061-a01-cgen1-resource-matched-recurrent-causal-trace-null-v1` | resource-matched recurrent causal trace |
| belief-state null | `v061-a01-cgen1-explicit-latent-cause-belief-null-v1` | explicit latent-cause/belief-state comparator |
| separable joint null | `v061-a01-cgen1-separable-address-plus-field-null-v1` | actual-address selector plus generic Field-credit update as separable components |
| negative stop | `v061-a01-cgen1-stop-no-selective-plurality-or-null-reduction-v1` | stop before rescue if selective plurality fails, forbidden privilege is required, or an equal/lower-resource null reproduces the complete dynamics |

## 4. Resource and privilege contract

The candidate may use only:

- the same actual pending event/provenance capability that exists at external pairing;
- four persistent Field credit scalars;
- at most two bounded pending provenance capabilities in the plurality construction;
- the signed external consequence;
- the later anonymous local activity vector.

Every registered null receives the same event stream and the same actual provenance capability at pairing. No null is disadvantaged by withholding the selector that the candidate receives. An equal-or-lower-state null with no greater lookup privilege is sufficient for reduction.

Forbidden privileges include semantic/typed lineage IDs, evaluator-selected addresses, correct-action/answer keys, task labels, global belief-table lookup, or any caller-selected historical lineage.

## 5. P3 selector-versus-carrier cross

The fixed causal cross is:

1. hold pre-update Field state constant;
2. change which actual pending provenance capability is paired to the return;
3. require the update to follow the actual capability;
4. expire the capability after update;
5. transplant only the updated Field state into a matched recipient;
6. require the later competition effect to transfer with Field alone;
7. require address-only state after update to be insufficient.

`expected_p3_carrier_loci = (field-state,)`.

## 6. Static-reduction gate

Before candidate implementation, MAIN must compare this exact bound object against all fixed nulls, including the separable address-plus-Field null. If an equal-or-lower-resource null reproduces the complete selector/update/carrier/competition dynamics, this exact Generation-1 object is rejected **before STARTED** and must not be implemented merely to reconfirm the reduction.

No null, resource constraint, scorer, success criterion, or mechanism rule may be weakened after this contract is bound.

## 7. Binding

`PreMechanismProposal.specification_hash()` for this exact proposal payload is:

```text
4b574b7053efb50b59a8d7536c94d02a7a25bdfc5b1d7f88575c7b6fc3e614ac
```

The additional Family-C extension binding covers the belief-state and separable-null IDs, selector source/lifetime, carrier locus, update/competition rules, width/decay/plurality bound, and resource rule:

```text
690a62df641d0577e3f7d760354763a6f0ec69e33eedfdacb37e92e7c654dbbc
```

Machine-readable constants live in:

```text
src/sparkbrain/evaluation/v061_family_c_premechanism.py
```

## 8. One-way prohibition

This handoff does not admit execution. MAIN must not create STARTED/control claims, dispatch one-way workflows, acquire or expose scientific outputs, score raw evidence, create freeze/evidence authority, or consume the identity. A terminal static reduction must return to the Evidence Analyst after canonical closeout.
