# RV02-RD001 recruitment diagnosis — development only

Date: 2026-09-09. The owner authorized parallel implementation and experiments through
acceptance. This is a new diagnosis of the retained RV02 feasibility substrate, not a
formal candidate, a repair of the previous 36 cells, or a new capability claim.

## Frozen pre-outcome choices

Keep all RV02 v1 world fixtures, seed 92001, 48/144/480 units, degree eight, fixed 36 ports,
training observations, external-only physical learner, threshold 0.5, initial weight 0.05,
initial delay 5ms, cue current 1.0 and recurrent state unchanged. The already exposed
development worlds are reused deliberately for mechanism diagnosis, not fresh generalization.
The baseline learning algorithm and the prior source/results remain byte-identical.

Train one new diagnostic Field per family/scale (18 cells). Freeze four probe conditions:

1. Natural route cue, horizon 40ms after cue, ordinary topology/weights.
2. Identical natural cue, horizon 160ms. No additional evidence or altered dynamics.
3. Identical natural cue, 40ms, visible-to-hidden and hidden-to-visible boundary weights
   set to zero AFTER training. Preserve hidden-to-hidden edges, all units and all edge
   slots; this explicit causal ablation is not baseline tuning.
4. Separate engineering-only positive control: inject current 1.0 directly into the
   smallest hidden unit at t=100ms on a fresh trained-state clone, horizon 40ms. Do not
   add that injection to learning/evidence or score it as natural recruitment.

Apply 1–3 to every route, and condition 4 once per cell. Exactly 252 probes are expected:
78 natural + 78 extended + 78 ablated + 18 positive controls. No reservoir comparison.

## Observation contract

At EVERY event timestamp and target, record number of synaptic arrivals, summed positive
and negative currents, decayed pre-integration potential, refractory state, effective
pre-reset potential, dynamic threshold, actual spike and post-event potential. Derive
decayed state by a pure arithmetic projection only (no runtime decay call). Report
stored final potential with last-update timestamp separately from pure projected final
potential at the final clock. The inherited delivery method is called
exactly once; observer records never re-enter learning or dynamics.

Independently run an unobserved clone with the same intervention and require identical
spike bytes and complete Field state hash. Before/after connection hashes must be equal
inside a probe. The ablation hash is recorded separately from the baseline hash.

Report per-hidden-unit arrivals/current/max potential-to-threshold ratio and spikes.
Count all arrivals separately from positive-current arrivals: zero-weight ablation still
schedules zero-current arrivals. Compare both visible spikes and full visible final UnitState
hash/rows, since equal spikes do not imply equal subthreshold or provenance state.
Silent hidden units have zero arrivals and null maximum ratio, not invented measurements.
Preserve raw event rows and generated spikes. Compare natural 40/160ms visible traces;
record queue-drained versus live-horizon endings. A drained queue cannot restart merely
because a later horizon was specified.

Record actual Field-learning trace keys and every returned edge update during training.
Report hidden external trace/eligibility count and changed hidden edges. Endogenous
observations are not permitted to create positive learning. No learning repair is allowed.

## Acceptance and interpretation

Engineering acceptance requires all 18 cells, 252 probes, observer equivalence, positive
control activation, fixed topology/evidence, probe nonlearning, source binding and raw
integrity. Failure is retained and cannot be replaced by a favorable rerun.

Arrival without spiking means subthreshold influence, NOT unused/inert state. No hidden
arrivals plus a passing direct control localizes failure to recruitment rather than unit
execution. Extended horizon only distinguishes temporal truncation if queues remain alive.
Unchanged behavior under hidden-boundary ablation is evidence of no observed contribution
in these diagnostics, not a proof against all possible Field mechanisms.

## Resource and persistence boundary

CPU/local only. At most 60s and 1GiB per cell; at most 600s total. Native arrival/spike
guards stay bounded at 4096 arrivals/512 spikes per probe; exceeding them makes the cell
incomplete. Fresh output directory, source Git SHA and source hashes, closed raw atomic
publication, manifest/summary integrity verification, no formal or held-out mode.
Source and tests must be committed and independently reviewed before execution.
