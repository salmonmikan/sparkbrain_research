# Fast Forge — FLY-0 matched replacement and delay envelope

- generation_id: `FORGE-20260928T143500+0900-FLY0-MATCHED-REPLACEMENT-A`
- forge_id: `FORGE-FLY0-MATCHED-REPLACEMENT-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0

## Authority and collision

Human Directive index is unchanged at active-index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
Durable Analyst authority remains R167 and allocates Forge to non-evidentiary
bottom-up verification/comparator gaps while MAIN owns only M1-002. MAIN R174
still owns `BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS`; Relay remains
unallocated. This isolated Forge branch does not collide with MAIN.

## Prototype

Branch: `forge/20260928-fly0-matched-replacement-a`
Exact verified prototype head: `26c740b302b5c6eb2549eca4033a3e79618931a8`
Exact prototype tree: `f513f42e9a49a2cc7b3c04c6447ae0c41f5b1913`
Parent durable Forge handoff: `c637e0c348c5eaca5be64d8555366ad785b3733c`

Added:
- `forge_prototypes/fly0_matched_replacement.py`
- `tests/test_forge_fly0_matched_replacement.py`

A separate markdown design-note publication was attempted five times and was
refused before GitHub on all five attempts, so that optional file was not
created. The module docstring, tests, and this durable handoff preserve the
implemented contract without bypassing that exhausted mutation purpose.

CI run `36382942094` completed successfully on Python 3.11 and 3.13.

## Bounded engineering observations

The new harness places four replacement variants behind one common bounded
observation/action/gating envelope:
1. structured FLY-0 topology;
2. degree-preserving rewired topology;
3. random sparse topology;
4. ordinary reactive replacement.

All four share the same configured event-budget ceiling and one-logical-step
feedback-delay envelope. The three topology variants retain the same topology
resource signature already established by the topology probe.

The exact-head tests establish:
- the ladder contains all four variants under the same configured envelope;
- structured and ordinary reactive variants both reach the target with trace
  `2 -> 1 -> 0 -> -1`;
- a delay of two logical steps against a one-step maximum allows the first
  action, then fails closed before any second world transition;
- structured/reactive checkpoint replay is exact;
- checkpoint restore rejects replacement-variant mismatch;
- replacement variant, event budget, feedback delay and delay budget are bound
  into checkpoint semantics.

This closes the missing ordinary-replacement and explicit logical-delay
engineering surfaces at the Forge level. It does not establish that every
resource dimension is commensurate.

## Remaining comparator gap

Internal activity remains deliberately non-commensurate across the full ladder:
the topology variants expose `topology_trace_events`, while the ordinary
reactive replacement exposes `reactive_activation_events`.

Therefore:
- interface/configured exposure is matched;
- logical feedback-delay envelope is matched;
- topology resource envelope is matched among structured/rewired/random;
- strict internal activity/resource matching remains OPEN.

Unlike activity counters are not converted into compute, energy, efficiency or
fairness claims.

## Ordinary reduction

The ordinary reactive replacement still solves the bounded movement task under
the same observation/gate/delay envelope. This is a stronger reduction target,
not evidence that fly-like structure is necessary or superior.

## Claim boundary

NON_EVIDENTIARY / NONCANONICAL. No SB003 allocation. No topology superiority,
biological fidelity, energy efficiency, whole-system superiority, composition
contribution, novelty, external validity or scientific credit is established.
No A01, RV02, H9, C07, M1-002, FORMAL, immutable, sealed or evidence object was
modified.

## P0 observation

The GitHub mutation-recurrence incident remains OPEN. This run observed:
- prototype source publication: first attempt succeeded;
- focused test publication: four pre-GitHub refusals, fifth attempt succeeded;
- optional markdown design-note publication: five pre-GitHub refusals and no
  file creation.

This supports the existing intermittent/path-dependent mutation-refusal
classification for the tested paths only. It does not establish an internal
root cause or repository-wide outage.
