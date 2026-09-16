# V061 A01 Family-C Generation-1 — Frozen Null Ladder

Status: **prospective pre-START null contract**

Identity under test:

```text
a01-family-c-joint-return-local-field-gen1-v1
```

All nulls receive the same external event stream and the same actual pending causal-provenance capability at exact pairing as the candidate. Reduction is valid when a null reproduces the complete prospectively claimed selector/update/carrier/competition dynamics with equal or lower persistent state and no greater lookup privilege.

## N1 — Explicit return-address / eligibility

ID:

```text
v061-a01-cgen1-explicit-return-address-eligibility-null-v1
```

An explicit bounded return-address/eligibility mechanism may retain the actual pending address and update local credit directly. Semantic/evaluator privilege is forbidden.

## N2 — Resource-matched recurrent causal trace

ID:

```text
v061-a01-cgen1-resource-matched-recurrent-causal-trace-null-v1
```

A bounded recurrent causal trace receives the same event/provenance inputs and may use no more persistent scalar state or lookup privilege than the candidate.

## N3 — Explicit latent-cause / belief state

ID:

```text
v061-a01-cgen1-explicit-latent-cause-belief-null-v1
```

A bounded explicit latent-cause/belief-state comparator is allowed only under matched event information and resource/lookup accounting.

## N4 — Separable address + Field

ID:

```text
v061-a01-cgen1-separable-address-plus-field-null-v1
```

This null intentionally tests whether the claimed “joint” organization is more than a separable composition:

```text
selector = actual pending causal-provenance capability
field_prime = generic_field_update(field, selector, signed_external_consequence)
discard selector
later_competition = field_only_score(field_prime, local_activity)
```

For the Generation-1 candidate contract, the matched N4 operator uses the same fixed rules:

```text
width = 4
decay = 0.5
field_prime[i] =
    decay * field[i]
    + (1 - decay) * sign * indicator(i == selected_slot)
later_score = dot(field_prime, activity)
```

N4 receives no semantic/typed identifier, no evaluator lookup, no caller-selected lineage, and no additional persistent state. It receives exactly the same actual transient provenance capability as the candidate at pairing.

## Static stop rule

If the exact bound candidate is expressible as N4 with the same selector, same Field update, same address lifetime, same later Field-only readout, and no resource/privilege advantage, all prospectively fixed discriminator dynamics are reproduced by an established separable organization. The correct disposition is then:

```text
REJECT_BEFORE_STARTED_STATIC_REDUCTION
```

No implementation or one-way run is required to reconfirm a complete algebraic equivalence.
