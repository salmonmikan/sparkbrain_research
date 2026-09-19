# Receptor post-adaptation polarity inversion — Discovery cycle 1

**EXPLORATORY / NON_EVIDENTIARY**

Source semantics: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Question

Can a positive probe after sustained same-sign positive stimulation be emitted
with negative polarity by the v0.5 multi-timescale receptor, and if so does the
effect require any mechanism beyond the explicit receptor direction rule?

## Protocol

A fresh `MultiTimescaleReceptorBank` was used for each synthetic cell. Each cell
received 20 positive training pulses of magnitude `1.0`, followed by one positive
probe. Training ITI was `2/5/10/20/40 ms`; the post-train gap was
`0/2/5/10/20/40/80/160 ms`; probe magnitude was
`0.02/0.05/0.1/0.2/0.4/0.8/1.0`. Prediction error was fixed to zero.

This is a 280-cell synthetic sweep. No repository dataset, trained checkpoint,
formal raw material, held-out TEST input, official scorer, or consumed identity
was used.

## Observation

- `191/280` cells emitted **negative polarity despite a positive probe**.
- `89/280` emitted positive polarity; none failed the emission threshold.
- The analytic rule `sign(probe + derivative)` predicted the emitted direction
  in `280/280` cells.
- Inversion occurred through an `80 ms` gap for every tested training ITI and
  disappeared by `160 ms` in this grid.
- Example: ITI `10 ms`, gap `20 ms`, positive probe `1.0` produced derivative
  `-1.0817059176`; `probe + derivative = -0.0817059176`, so the emitted polarity
  was negative.
- Example: ITI `5 ms`, gap `80 ms`, positive probe `0.1` produced derivative
  `-0.1282277256`, so the emitted polarity was also negative.

## Reduction

The effect is exactly reduced by the current implementation:

`direction = sign(signed_input + (fast_trace - medium_trace))`.

The current probe adds the same signed increment to fast and medium traces, so
their difference is inherited from the pre-probe adaptation history. After a
dense positive train, the fast trace can decay below the slower medium trace,
making the derivative sufficiently negative to flip the output sign.

This is therefore ordinary multi-timescale temporal-contrast coding under the
current receptor contract, not an unexplained memory/adaptation phenomenon.

## Handoff

- exploration cycle: `1/3`
- evidentiary status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- candidate next research layer: `NONE_SCIENTIFICALLY`
- stop reason: exact implementation reduction after one bounded cycle

Engineering/protocol note: downstream work must not assume emitted receptor
polarity always preserves raw stimulus polarity after adaptation history. A
different polarity rule or explicit sign-preservation contract would be a fresh
future object, not a rescue cycle for this Discovery candidate.
