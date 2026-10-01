# Prospective v0.5 paired-input coverage fixture

2026-10-01 UTC. **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**; scientific credit **0**.
Diagnostic identity: `v05-paired-coverage-20261001`.

## Question and boundary

Can one source-derived, predeclared two-pulse input produce an actual mature internal
assembly in the unchanged v0.5 producer, so a later ownership test can exercise acquired
state? This protocol characterizes that prerequisite only. It neither runs ownership
transactions nor connects the producer to M1.

[PR176](https://github.com/salmonmikan/sparkbrain_research/pull/176) remains
[coverage-blocked](v05_owned_state_results_20261001.md): its single Q episodes produced
receptor activity without internal patterns, and P5/P6 were not executed. The current
fixture is a separate prospective development object with new episode IDs. It will not
rerun, retune, replace or reinterpret the earlier probe. Successful coverage here would
not retroactively clear its untested ownership cases.

## Source-derived input, not a parameter search

At source `a5b231db84fb7017b5df5e7653739c65bb4175bb`:

- Receptor-to-reservoir edges start at current/weight 0.47, with delays 1.0, 2.6 and
  4.2 ms. Internal thresholds start at 0.76
  ([topology.py](../../src/sparkbrain/v05/topology.py), lines 29–67)
- Membrane decay uses tau 18 ms. Two arrivals along the same unchanged edge, with no
  intervening reset or competing input, yield `0.47 * (1 + exp(-gap / 18))`: about
  0.84635 at 4 ms and 0.52093 at 40 ms
  ([field.py](../../src/sparkbrain/v04/field.py), lines 25–37 and 106–122)
- Receptor refractory duration is 3 ms. The source supports a second receptor spike
  after 4 ms; synaptic propagation sends `edge.weight`, independent of receptor spike
  magnitude. Increasing input amplitude alone therefore does not increase that current
  ([field.py](../../src/sparkbrain/v04/field.py), lines 219–266)
- Patterns exclude receptor IDs. Candidate matching requires similarity at least 0.66;
  maturity requires three distinct episode IDs. Three calls alone do not promise a
  mature candidate ([assemblies.py](../../src/sparkbrain/v05/assemblies.py), lines
  120–169 and 230–280)

This first-hop calculation motivates the fixed input. It does not predict the complete
recurrent response, candidate partition, third-episode maturity or any behavioral benefit.
Actual emitted polarity and receptor routes will be retained rather than assumed.

## Frozen finite plan

The complete [machine-readable protocol](../../artifacts/research/v05_paired_coverage_20261001/protocol.json)
contains all 15 pulse records, nine distinct episode IDs, constructor configurations,
call flags, arm order, 27 source-file hashes, resource limits and decision rules. Its
SHA-256 is `09edae7add4210121b699583b935c8ba5b0dd2b382fa8d9d848d6ac0ce6bff25`.

Each arm starts from one fresh state graph, using the same topology seed 920041. These
are not independent statistical replicates. In fixed order:

| Arm | Episode 1 pulse times | Episode 2 | Episode 3 | Role |
|---|---|---|---|---|
| single | 8 | 208 | 408 | Single-pulse characterization control |
| paired_4ms | 8, 12 | 208, 212 | 408, 412 | Only eligible target fixture |
| spaced_40ms | 8, 48 | 208, 248 | 408, 448 | Equal-pulse-count spaced control |

Times are milliseconds. Every raw pulse is positive channel Q, magnitude 1.2, null
location, zero supplied novelty/prediction error and empty metadata. Each row is one
`process_episode` call containing all pulses for that episode. Separate calls for the
4-ms pair would be invalid because the first call settles for 32 ms.

The complete top-level PR176 configuration is retained. The v0.5 prediction, action and reward
modulation switches are disabled; assembly, receptor bank, weight/delay learning and homeostasis
remain enabled. `learn_assembly=True`, `learn_field=True`, `explore_action=False` and
empty call metadata are fixed. No external threshold, configuration or state overrides
are allowed. Endogenous thresholds and edges are allowed to change through their existing
runtime rules and must be recorded. The underlying v0.4 ActionAssociator diagnostic
remains active in its existing ingestion path; no outcome feedback is delivered.

The nested constructor configuration projection is also frozen, including inactive base
plasticity and action defaults. The actual layered topology has 16 receptors plus an
8-by-6 reservoir; top-level width/height fields do not replace this explicit topology.

## Gates and interpretation

After the first episode of every arm, no candidate/activation may be mature, and
`pending_activation` must be null. Multiple patterns within one episode are not independent
episode evidence. An invariant failure stops the diagnostic immediately.

After exactly the third paired-target episode, require all of:

1. A non-null, mature and unsuppressed actual pending activation
2. Its assembly ID resolves to an existing candidate containing exactly all three target
   episode IDs
3. That candidate's prototype is the identical object in retained `result.patterns`, with
   result/pattern indices saved
4. The pending activation is the identical object in retained `result.assembly_activations`,
   with result/activation indices saved

Target absence is `coverage_blocked`. No extra episodes, changed gaps, new seeds, threshold
changes or control-arm substitution are permitted. The control arms are still completed
within the fixed plan unless an exception, resource limit or invariant failure requires
an early stop.

Control characterization is separate from target coverage. The source-derived expectation
is zero internal patterns/candidates/activations in every single/spaced episode. If a control
surprises, preserve its full result and label the expected timing-specific contrast
unsupported. A valid paired target remains a covered state fixture, but that does not
establish a membrane-only causal explanation. A successful control never replaces a failed
target. No significance test, aggregate performance metric or hypothesis promotion is planned.

## Raw preservation and bounded execution

This document authorizes no execution by itself. Before any model import/construction,
publish a separate exact runner/source freeze and obtain independent pre-execution review.
The runner must use a fresh no-clobber output directory and verify source/config/input
bindings before proceeding. There is one bounded execution, with no retry or reproduction.

Maximum use: **3 fresh brains, 9 process attempts and 15 raw pulses**, at most two pulses
per call. No native loads, whole-brain copies, outcome deliveries or ownership operations.
CPU limit 60 seconds, wall limit 120 seconds, address space 512 MiB and output limit
32 MiB. A small reserved finalization allowance must be included inside those limits.
Hard process termination can prevent finalization and must not be reported as complete.
Network denial must be described at its actual enforcement layer, without an OS-isolation
claim unless that is separately implemented and verified.

Preserve before interpreting each call:

- Exact raw inputs and call flags; complete returned result or exception
- Spikes, cascades, internal patterns, similarities, all candidate/prototype/activation
  values and episode-ID sets; first-episode and endpoint gate inputs
- Actual emitted receptor traces/routes, source topology, initial/per-call thresholds and
  connections, native value views, and identity-index witnesses for retained aliases
- Exact source/config hashes, Python/platform versions, measured resources, actual counts,
  terminal status, raw-file hashes and a manifest

Native value views are incomplete ownership snapshots, as PR176 demonstrated. They are
retained for inspection, not claimed as a complete resumable fixture. Do not use a matching
native hash as a substitute for the actual object-identity witnesses. Save partial raw data
on failure; a resource or inspection failure cannot be silently turned into a target miss.

## Known limits and next decision

State persists between episodes. Lazy membrane/adaptation decay, receptor slow/gain traces,
endogenous plasticity and homeostasis all remain active. Homeostasis counts calls rather
than normalizing by duration; single/paired/spaced calls end at 40/44/80 ms in the first
episode. Gap-dependent receptor normalization means the spaced control is not an isolated
intervention on membrane summation. Cascade gaps greater than 6 ms can split patterns;
sequence/timing changes can split candidates. The single control deliberately has fewer
pulses than either pair arm.

If acquired target coverage is absent, retain the block and stop. If present, propose a
separate prospective ownership test with its own finite budget and source freeze. That
later test must verify complete-state rollback/commit and detached output ownership for
its actual acquired producer; this characterization provides none of those conclusions.
The interface in [PR174's design](assembly_m1_interface_design_20261001.md), causal controls,
and real producer-to-M1 contribution remain separate prerequisites.

## Source review and coordination

Independent source-only review supported the exact 4-ms/40-ms inputs without changing
seed, magnitude, thresholds or episode count. It required one-call pulse pairs, explicit
endogenous learning, non-statistical arm language, actual maturity/alias gates, and separate
control interpretation. No model was imported, constructed or run for that review.

Main/AGENTS and active directives were freshly checked. Directive index ref
`ops/human-directives` was at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. This dedicated cloud-only development work
supports the integration prerequisite and does not take ownership of canonical M1 work,
PR173 causal triage, formal identities, shared scheduler state or scientific acceptance.
