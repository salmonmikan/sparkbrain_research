# PD0.1 long-history / fading-memory — pre-formal package

Status: `PREFORMAL_REVIEW_ONLY`

Evidence Analyst authority: `b009f497e65cddf1dd93cd4edc50f874c159ccd7`
Base substrate: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
Formal identity: **UNRESERVED**
Official data/target access: **FORBIDDEN**
STARTED / one-way execution: **FORBIDDEN**

## Purpose

Prepare exactly one deterministic fading-memory comparator family for the next external-validation
axis without consuming or adapting to any official outcome. This package is intentionally reviewable
but scientifically incomplete: values that the Evidence Analyst has not yet authorized remain
explicitly unresolved rather than being guessed by MAIN.

## Fixed pre-formal implementation shape

The candidate implementation is the non-trainable exponential-memory transition
`state_t = decay * state_(t-1) + observation_t`, reset to zero at every history boundary. There is no
fit/tune/select loop, no learned recurrent component, and no cross-history state. The implementation
accepts target-free numeric observations supplied by a later authorized protocol; it does not define
the official representation or task/world subset itself.

History ordering support is deterministic but parameterized by an explicitly supplied unique stable
order field. The formal order field is not selected here. Target-free inventory tooling counts
histories and observations before any scorer or target materialization exists.

Synthetic/dev tests may instantiate a decay solely to exercise implementation mechanics. Such a
value is NON_SCIENTIFIC and must never be promoted into the formal protocol by inference from this
branch.

## Still blocked on fresh prospective Evidence Analyst authorization

The following are deliberately `UNRESOLVED_BY_ANALYST` and must be fixed prospectively before any
formal identity or execution package is created:

- exact task/world subset and official input universe;
- deterministic official history construction and order field;
- exact lag grid / long-history points;
- formal comparator configuration, including decay and any representation binding;
- numeric scoring metrics and effect contrast;
- no-effect, inconclusive, and success criteria / thresholds or equivalence rule;
- formal contender count;
- resource/cost budget;
- runtime and package-version pinning;
- exact raw cardinality/inventory implied by the authorized universe.

## Integrity boundaries

1. No formal identity, STARTED/control ref, preserve ref, evidence ref, or official workflow is
   created by this package.
2. No official data, labels, answers, targets, or outcomes may be read during pre-formal readiness.
3. A future formal protocol must preserve raw-before-score and preserve-before-targets ordering.
4. A future scorability/target-independence gate must be frozen before official access.
5. Any observation that would motivate changing candidate shape, scientific metrics, thresholds,
   runtime, resource contract, or identity returns to the Evidence Analyst rather than being repaired
   post hoc by MAIN.
6. Terminal C19-R2 evidence is immutable and is not used to tune this candidate.

## Review exit

This branch is ready for Analyst review when its deterministic primitive, synthetic/dev tests,
pre-formal fail-closed checker, and exact-head CI/pre-formal check are green. At that point MAIN must
stop. Formalization requires a newer Analyst handoff resolving the blocked scientific fields above.
