# RV02 Field Scale / Interference Geometry Study Plan

Status: **PLANNING ONLY — NO IMPLEMENTATION AUTHORIZED**

Branch: `research/rv02-field-scale-study-plan`

Base line: `research/rv01-endogenous-transition`

This document defines a new RV-series experiment. It does not reopen, repair, rerun, or rescore R01-12F. The R01-12F formal candidate remains consumed and immutable.

---

## 1. Motivation

RV01 produced a repeatable pattern in which the Field retained ordered continuation and first-hop coverage at least as well as the resource-matched reservoir, while exact-route recovery did not improve and contamination was higher.

That evidence is compatible with several qualitatively different mechanisms:

1. the Field is genuinely using distributed state space to preserve multiple candidate continuations, but the current Field is too small and trajectories collide;
2. the Field advantage is mainly uncontrolled diffusion / over-activation, in which case a larger Field should not improve route precision;
3. additional Field capacity exists but the current dynamics do not exploit it, so scaling produces little change;
4. larger state space improves representation only when input/evidence scale also grows, rather than for the same external experience.

RV02 is designed to discriminate among these explanations rather than to demonstrate that a larger Field is better.

---

## 2. Primary research question

> When the amount and structure of external evidence are held fixed, does increasing Field capacity reduce internal trajectory interference and improve route separability, or does it mainly increase the amount of uncontrolled activity?

A secondary question is:

> Are any scaling effects specific to Field dynamics, or are they reproduced by a resource-matched reservoir given the same increase in computational resources?

---

## 3. Scope

Primary scale points:

- `1x`
- `3x`
- `10x`

The study must compare, at every scale:

- Field
- resource-matched reservoir

The `1x` condition is a new RV02 development/formal condition, not a rerun designation for R01-12F. RV01 artifacts may be used as historical evidence but not as the RV02 formal candidate.

Primary scaling mode:

### Evidence-preserving scale

Increase internal Field/reservoir capacity while holding the external world, number of observations, route exposures, probe schedule, and evidence budget fixed.

This is the main experiment because it asks whether a larger internal state space uses the same experience more effectively.

Optional secondary scaling mode, only after the primary protocol is frozen:

### Density-preserving input scale

Scale input ports/evidence with internal capacity to test whether larger systems exploit proportionally richer external input.

This secondary mode must be a separately declared analysis and must not replace a negative primary result.

---

## 4. Scale definition

The default scale variable is the number of Field computational units.

For a scale factor `s`:

- Field unit count: `N_s = s * N_1`
- reservoir unit count: resource-matched to the corresponding Field condition
- average local out-degree: fixed within a declared tolerance
- average local in-degree: fixed within a declared tolerance
- connection density therefore decreases approximately as `1/N` when size grows
- learning/update opportunity budget per unit must not silently increase
- world exposure count must remain fixed in the primary experiment

The experiment must not hold connection density constant, because doing so would make edge count grow approximately quadratically and would confound Field size with connectivity explosion.

Resource matching must account for at least:

- computational units
- persistent trainable/adaptive state
- connection count
- update operations
- execution steps
- external observations
- probe count

If exact equality is impossible, the matching rule and residual mismatch must be declared before formal execution.

---

## 5. Hypotheses

### H1 — finite-capacity trajectory crowding

The RV01 contamination/precision trade-off is caused in substantial part by insufficient internal state space.

Expected scaling signature:

- ordered retention: stable or higher
- first-hop coverage: stable or higher
- normalized contamination: lower
- route-to-route overlap: lower
- exact-route recovery: higher
- activation remains bounded rather than simply filling the larger Field

A strong H1 signature would be especially interesting if the Field improves more than the resource-matched reservoir.

### H2 — intrinsic diffusion / over-activation

The Field's apparent retention advantage is primarily produced by activity spreading broadly rather than by useful trajectory separation.

Expected signature:

- raw contamination: increases with scale
- normalized contamination: flat or increases
- active-unit fraction: flat or increases
- exact-route recovery: approximately unchanged
- retention remains high
- route overlap does not improve enough to produce precision gains

### H3 — scalable distributed candidate substrate

The Field uses additional state space to retain more mutually separable candidate continuations.

Expected signature:

- candidate coverage increases or remains saturated
- route-to-route overlap decreases
- unseen-combination interference decreases
- normalized contamination decreases
- exact-route recovery and/or later selective continuation improves
- active-unit fraction does not approach global saturation

This is stronger than H1 because it predicts useful exploitation of increased state space rather than merely relief from a small-system bottleneck.

### H4 — inactive excess capacity

The current dynamics do not recruit additional Field capacity.

Expected signature:

- most behavioral metrics remain approximately unchanged
- unique occupied-unit fraction decreases with scale
- absolute occupied-unit count changes little relative to total capacity
- trajectory overlap remains similar
- resource use increases without a corresponding behavioral or geometric change

### H5 — generic capacity effect

Both Field and reservoir improve similarly when scaled.

This would show that capacity matters but would not support a Field-specific scaling mechanism.

---

## 6. Experimental matrix

Minimum matrix:

| Architecture | Scale | External evidence | Connectivity policy |
|---|---:|---|---|
| Field | 1x | fixed | fixed average degree |
| Field | 3x | fixed | fixed average degree |
| Field | 10x | fixed | fixed average degree |
| Reservoir | 1x | fixed | resource matched |
| Reservoir | 3x | fixed | resource matched |
| Reservoir | 10x | fixed | resource matched |

The same world families should be represented at all scale points.

Scale must not change:

- world semantics/structure
- route count
- exposure schedule
- probe schedule
- scoring definition
- threshold definitions used to declare success

Any unavoidable architecture-dependent runtime parameter must be declared as a scale-normalization rule before development experiments begin.

---

## 7. World families

RV02 should inherit the interference questions established by RV01, while using a new RV02 candidate namespace and fresh world seeds.

At minimum include worlds corresponding to:

- disjoint routes
- shared cue
- shared prefix
- opposing/reversal interference
- dense-load interference

A scale-specific addition is recommended:

### Capacity-pressure family

Construct a family in which the number of simultaneously relevant candidate routes increases while exposure budget remains bounded.

Purpose:

- distinguish useful multi-candidate preservation from simple global activation;
- measure whether additional internal capacity actually increases separability;
- avoid relying only on saturated retention metrics.

This family must be defined before formal outcomes are observed and must not be tuned to favor the Field.

---

## 8. Primary behavioral metrics

Retain RV01-compatible metrics:

1. ordered retention
2. exact-route recovery
3. contamination
4. first-hop coverage
5. family-level performance

Do not use ordered retention alone as evidence of superiority.

Exact-route recovery remains a required precision metric.

---

## 9. Scale-specific internal geometry metrics

The following should be captured for Field and, where meaningfully definable, for the reservoir:

1. active unit count
2. active unit fraction
3. unique occupied unit count
4. unique occupied unit fraction
5. cascade size
6. cascade duration
7. spatial/topological cascade extent
8. route-to-route active-state overlap
9. trajectory overlap over time
10. activation entropy or an equivalent preregistered diversity statistic
11. state reuse frequency
12. route-specific state exclusivity

The implementation must define these operationally before formal execution.

---

## 10. Contamination normalization

Raw contamination alone is insufficient for a scale study.

At minimum report:

- raw contamination per route
- contamination per active unit
- contamination per total internal unit
- contamination relative to recovered route length
- contamination relative to total candidate activity

This prevents a larger system from being penalized merely because it contains more units, while also preventing normalization from hiding a genuine explosion in raw off-route activity.

Both raw and normalized values must always be reported together.

---

## 11. Scaling signatures

The study should emphasize curves, not only pairwise 1x-vs-10x comparisons.

For each primary metric, report:

- 1x value
- 3x value
- 10x value
- monotonicity/non-monotonicity
- architecture-by-scale interaction

A single favorable 10x endpoint is insufficient.

Important derived signatures include:

### Precision-retention frontier

Plot/measure the relation between:

- ordered retention
- exact-route recovery
- contamination

A meaningful Field scaling result would improve the frontier, not merely move toward more activity and more retention.

### Capacity utilization curve

Track:

- total units
- unique occupied units
- active fraction
- route-exclusive units

This distinguishes unused extra capacity from useful distributed recruitment.

### Interference-separation curve

Track route overlap as Field size increases.

H1/H3 predict decreasing overlap. H2 predicts little useful reduction or increasing spread.

---

## 12. Primary decision criteria

The protocol should not define a single "Field wins" threshold at planning time.

Instead the primary conclusion must classify the observed scaling signature.

### SUPPORT H1/H3 direction

Require a conjunction such as:

- retention does not materially degrade;
- normalized contamination decreases with scale;
- route overlap decreases;
- exact-route recovery or another preregistered precision measure improves;
- improvement is not fully reproduced by the resource-matched reservoir.

Exact numerical tolerances must be frozen only after development calibration and before formal execution.

### SUPPORT H2 direction

Evidence includes:

- contamination scales with or faster than capacity;
- normalized contamination fails to decline;
- exact-route recovery remains flat;
- active fraction remains globally high;
- route overlap fails to improve.

### SUPPORT H4 direction

Evidence includes:

- increased capacity is weakly utilized;
- geometric metrics remain nearly unchanged;
- behavioral metrics remain nearly unchanged;
- utilization fraction falls strongly with size.

### GENERIC CAPACITY EFFECT

If Field and reservoir show similar scaling improvements after resource matching, classify the result as generic capacity scaling rather than Field-specific evidence.

---

## 13. Development phase

Development may be used to validate:

- scale construction
- resource accounting
- numerical stability
- metric definitions
- runtime feasibility
- world-family validity
- statistical power assumptions

Development may not be used to repeatedly modify the Field until the desired H1/H3 signature appears.

Before formal freeze, record all architecture-affecting changes and the reason for each change.

No formal candidate may be generated until the scale protocol, scoring definitions, resource matching, and metric schemas are frozen.

---

## 14. Formal held-out phase

RV02 formal evaluation must use:

- a new RV02 candidate ID
- fresh disjoint seeds
- fresh held-out worlds
- a new formal freeze
- one-way execution
- immutable raw-result preservation

R01-12F must not be rerun, repaired, or reused as an RV02 formal candidate.

After `STARTED`:

- no rerun
- no repair
- no threshold tuning
- no scale-point replacement
- no world replacement
- no resource-matching adjustment
- no architecture-specific tuning

Failure or crash after `STARTED` consumes the candidate unless the preregistered execution policy explicitly classifies the failure as infrastructure-only without exposing capability outcomes.

---

## 15. Statistical structure

The formal design should be paired by world wherever possible:

- the same held-out world is evaluated at 1x, 3x, 10x;
- both Field and reservoir see equivalent evidence;
- comparisons are made within world before aggregation.

Primary analyses should include:

- architecture effect
- scale effect
- architecture × scale interaction
- family × scale interaction

Avoid claiming a scaling law from only three points. The 1x/3x/10x series is a scale-response study, not evidence of an asymptotic power law.

---

## 16. Resource accounting

For every run record at least:

- unit count
- connection count
- persistent state bytes
- transient peak state bytes
- update count
- total computational steps
- external observation count
- wall-clock time as a secondary engineering metric

Behavioral conclusions must not use wall-clock speed as a substitute for resource matching.

Resource-matched reservoir construction must be audited independently from capability results.

---

## 17. Ablations and secondary analyses

These are allowed only if preregistered before formal execution or performed as new post-formal development studies.

Potential secondary studies:

1. evidence-preserving vs input-density-preserving scaling
2. fixed-degree vs alternative connectivity scaling
3. scale-specific homeostatic activity normalization
4. route count / capacity pressure sweeps
5. local Field geometry variations

None should be introduced after formal outcomes merely to rescue a negative primary result.

---

## 18. Relationship to A01

RV02 must remain independent of A01 mechanism tuning.

RV02 may answer whether a larger Field:

- retains more simultaneous candidate continuations;
- separates candidate trajectories better;
- lowers normalized contamination;
- creates a more useful substrate for later selective credit.

It must not use A01 results to tune Field parameters.

A later, separately declared experiment may test whether an already-frozen A01 mechanism can select among candidate lineages produced by different Field scales.

That later study is not part of RV02 primary scope.

---

## 19. Failure interpretations

A negative result is scientifically useful and must be preserved.

Examples:

### Larger Field, same precision, more contamination

Interpret as evidence against finite-capacity crowding as the main RV01 limitation and in favor of intrinsic diffusion/over-activation.

### Larger Field, same everything

Interpret as evidence that current dynamics do not exploit extra capacity.

### Larger Field and reservoir both improve similarly

Interpret as generic capacity scaling, not Field-specific organization.

### Retention improves but exact-route stays flat

Do not call this Field superiority. Classify it as stronger broad retention without improved precision.

### Exact-route improves only after changing thresholds or activity normalization post hoc

Primary RV02 result remains unsupported; the modified architecture belongs to a new candidate.

---

## 20. Required final report

The eventual RV02 report must include at least:

- exact scale definitions
- Field/reservoir resource accounting
- development/formal separation
- formal candidate identity and source SHA
- 1x/3x/10x results
- ordered retention curves
- exact-route recovery curves
- raw contamination curves
- normalized contamination curves
- first-hop coverage curves
- active-unit fraction curves
- trajectory-overlap curves
- capacity-utilization curves
- family-specific trends
- architecture × scale interaction
- whether extra Field capacity is actually recruited
- whether precision improves or only activity increases
- whether any scaling gain is Field-specific or generic
- implications for A01 as a later selector, without tuning A01

The final conclusion should be expressible in the form:

> Increasing Field capacity [does / does not] convert the RV01 broad-retention phenotype into better-separated and more precise continuation state, and the observed change [is / is not] specific to Field dynamics relative to a resource-matched reservoir.

---

## 21. Explicit prohibitions

During RV02 implementation and formal evaluation, do not:

- rerun R01-12F
- modify R01-12F artifacts
- reuse the consumed R01-12F candidate
- weaken the reservoir to create a Field advantage
- increase connection density accidentally while claiming only size scaling
- increase the evidence budget in the primary evidence-preserving study
- tune thresholds separately by scale after viewing formal outcomes
- change world difficulty by scale
- select only favorable metrics
- treat ordered retention alone as success
- omit raw contamination when reporting normalized contamination
- omit normalized contamination when reporting raw contamination
- call three scale points a proven scaling law
- tune A01 from RV02 outcomes
- perform architecture repair after formal `STARTED`

---

## 22. Implementation gate

No implementation is authorized by this document.

Before implementation begins, the study should receive an explicit go-ahead on at least:

1. `1x / 3x / 10x` as the primary scale points;
2. fixed-average-degree scaling as the primary connectivity policy;
3. evidence-preserving scaling as the primary study;
4. resource-matched reservoir at every scale;
5. the required geometry/normalization metrics;
6. whether Capacity-pressure is included in the initial development worlds;
7. the intended runtime/resource ceiling for 10x.

Until then this branch is planning-only.
