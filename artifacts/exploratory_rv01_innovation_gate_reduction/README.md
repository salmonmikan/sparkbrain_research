# EXPLORATORY / NON_EVIDENTIARY — final RV01 scalar-filter reduction

Evidence Analyst authority:
`ops/evidence-analyst-handoff@719b9e74063e5e10f6226fd49f1835036ed75e5b`.

This is the **single final bounded stronger ordinary scalar-filter probe** authorized after the
previous clipped-EWMA sensitivity result. It is synthetic-only and cannot count as scientific
evidence, satisfy a gate, support an RV01 claim, or authorize formal execution.

## Question

Does the RV01-motivated residual-deadzone delay learner retain a stable mechanism-specific
advantage over a stronger ordinary scalar adaptive filter when information access, persistent
state, and DEV-selected control count are matched?

The new generic comparator is an **innovation-gated EWMA**:

- one persistent scalar delay estimate;
- two DEV-selected controls: `alpha` and a symmetric innovation threshold;
- update only when `abs(observation - estimate) >= threshold`;
- comparator family and parameter grid fixed before TEST;
- no TEST-driven comparator selection, parameter sweep, or retuning.

The RV01-motivated comparator remains the same residual-deadzone scalar learner used in the
previous bounded probe, also with one persistent scalar and two DEV-selected controls.

## Fixed synthetic contract

The world is unchanged from the preceding probe: latent delays `1/3/5 ms`, 128 sequences per
seed, 64 steps, stay probability `0.94`, Gaussian noise sigma `0.55 ms`, and signed `3.0 ms`
outliers. DEV uses five seeds at outlier probability `0.06`. TEST uses five disjoint seeds at
fixed outlier probabilities `0/0.03/0.06/0.12/0.20`.

The fixed toy utility remains:

`-mae - 0.20*false_adjustment_rate - 0.03*switch_latency + 0.15*return_recovery_2step`

DEV selected:

- residual-deadzone: `eta=0.8`, `deadzone=0.35 ms`;
- innovation-gated EWMA: `alpha=0.65`, `gate_threshold=0.75 ms`.

Those parameters were frozen before the disjoint TEST sweep was opened.

## Observation

`generic - deadzone` TEST utility is:

- `-0.031840` at 0% outliers;
- `-0.021394` at 3%;
- `-0.014399` at 6%;
- `+0.001513` at 12%;
- `+0.021803` at 20%.

The residual-deadzone learner wins the three lower-corruption regimes, while the stronger
ordinary filter wins the 12% and 20% regimes. Relative to the previous clipped-EWMA reduction,
the ordinary scalar comparator now crosses over earlier, but it still does not dominate the
low/mid-corruption regimes.

The useful conclusion is therefore only **reduction pressure**: the apparent advantage remains
materially regime-dependent and is not a stable SparkBrain/RV01-specific discriminator in this
toy. Conversely, this one generic filter does not fully reduce the toy across all regimes.

## Integrity / hard stop

- `evidentiary_status: NON_EVIDENTIARY`
- no formal identity, STARTED/control authority, official/sealed input, formal score, preserve,
  freeze, formal, or evidence ref is created;
- consumed/frozen RV01 identities and results are not rerun, rescored, repaired, or
  reinterpreted;
- MAIN C19-R2 work is untouched;
- this exhausts the Analyst-authorized one-final-probe allowance.

`promotion_recommendation: REJECT` applies to **this exploratory candidate as a direct
formalization basis**, not to RV01 as a formal scientific hypothesis.

Do not continue this RV01 exploratory ladder without a new Evidence Analyst classification.
Any future formal question must be a fresh prospective object with a new protocol, package,
bindings, and identity.

## Candidate future formal question

Under prospectively matched information access, persistent state, parameter/training/tuning
budget, and compute/resource budget, does an RV01-specific learned-delay mechanism provide a
stable held-out timing/recovery advantage over strong generic robust adaptive filters across
predeclared process/noise regimes?

Before any such formalization, new scientific choices are required for the task/world family,
delay-change process, observation/noise contract, exact mechanism and comparator family,
resource matching, calibration/tuning budget, primary metrics/Pareto criteria, held-out
regimes/seeds, runtime/determinism, statistical/preservation contract, and fresh
protocol/package/bindings/identity.
