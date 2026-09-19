# EXPLORATORY / NON_EVIDENTIARY — Homeostasis window-partition invariance

Source semantics: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Question

Does the v0.5 `HomeostaticController` preserve its final threshold when the same
physical synthetic spike train is presented through different observation-window
partitions?

This is a bounded Discovery probe only. It uses no repository dataset, trained
checkpoint, preserved formal raw material, held-out TEST input, consumed identity,
or official scorer.

## Fixed synthetic input

- 4 units, each starting at base threshold `1.0`.
- 1000 ms physical horizon.
- 40 spikes total, exactly one every 25 ms, rotating uniformly across the 4 units
  (10 spikes/unit).
- Observation windows: 10, 20, 25, 50, 100, and 200 ms.
- Stable v0.5 defaults: target `0.35 spikes/window`, learning rate `0.004`,
  rate EMA decay `0.88`.

Only the partition passed to `observe()` changes; the physical spike train does not.

## Observations

| window ms | calls | empty calls | final mean threshold | mean final rate EMA |
|---:|---:|---:|---:|---:|
| 10 | 100 | 60 | 0.896693683795 | 0.112715325178 |
| 20 | 50 | 10 | 0.963794522552 | 0.211550367529 |
| 25 | 40 | 0 | 0.976710783904 | 0.248496003261 |
| 50 | 20 | 0 | 0.998470920973 | 0.461218603181 |
| 100 | 10 | 0 | 1.004836028630 | 0.721499023991 |
| 200 | 5 | 0 | 1.005293605786 | 0.944536166400 |

Final mean threshold spans `0.108599921991` across the fixed partition grid:
`0.896693683795` at 10 ms versus `1.005293605786` at 200 ms.

## Reduction / interpretation

The effect is directly explained by existing controller semantics:
`target_spikes_per_window` is a count target per `observe()` call and `rate_decay`
is also applied once per call. Neither is normalized by physical elapsed duration.
Changing the observation partition therefore changes both the number of target
subtractions and the effective physical-time EMA decay, even though the physical
spike train is identical.

This is a useful protocol/engineering constraint but not a distinct scientific
phenomenon under the current question.

- Evidentiary status: `NON_EVIDENTIARY`
- Recommendation: `REJECT`
- Candidate next research layer: `NONE_SCIENTIFICALLY`
- What would require a fresh object: a prospectively specified duration-normalized
  homeostasis contract or a question about functional consequences after resource-
  and physical-time matching. It must not be treated as a rescue cycle.
