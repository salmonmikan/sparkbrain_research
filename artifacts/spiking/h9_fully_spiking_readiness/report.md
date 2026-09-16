# H9 / C07 fully-spiking boundary readiness audit

Status: `PRE_START_UNDERSPECIFIED`  
Execution allowed: **false**  
Evidence Analyst authority: `25eae547ccd9bb22edc2010e698a8dd2ecd33dcc`  
Source base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Purpose

This package is a source-only readiness/prospectivity audit for the independent H9/C07
secondary line. It does not execute a new C07 experiment, consume an identity, retune the
historical hybrid backend, or modify C19.

H9 is already canonical: a spiking substrate may preserve theory-level behavior. C07 also
already names a `hybrid vs fully spiking boundary comparison`. The historical C07 object is
useful evidence, but it is explicitly hybrid rather than fully spiking.

## Existing evidence and boundary

The historical C07 comparison used a snnTorch LIF **sensory encoder** in front of the
unchanged rate/algorithmic C01 engine. Its signed evidence graph, hypothesis state,
Coalition scoring, ignition, broadcast, and Workspace were not implemented as spike-domain
dynamics. The historical object passed all 9 frozen behavioral checks on the canonical
SwitchWorld scenario.

A retained negative is also informative: `spike_threshold=1.1` with unit currents produced
no sensory spikes and no predictions. That negative is preserved as historical evidence and
must not be tuned away or reused as a fresh one-way object.

The repository's existing H9/C07 doctrine does prospectively support continued use of the
canonical CAT→TOY→CAT scenario, shared C01 task-facing protocol, local/offline CPU
reproduction, the existing behavioral invariants, common trace schema, separate activity
and wall-clock reporting, and the prohibition on energy-efficiency claims.

## Why a fresh fully-spiking experiment is not ready

The source audit found no registered fully-spiking backend and no unique pre-existing
contract that determines the following choices:

1. **Operational fully-spiking boundary.** C07 allows Coalition and Workspace to remain
   algorithmic in the first hybrid backend, but never defines which components must become
   spike-mediated for a successor to count as fully spiking.
2. **Non-sensory neuron/synapse dynamics.** No exact recurrent neuron, synapse/filter,
   inhibitory, refractory, or integration equations are frozen for hypothesis state,
   Coalition, ignition, broadcast, or Workspace.
3. **Representation/decoder mapping.** There is no registered spike-domain mapping for
   evidence identity, residual belief state, Coalition score, ignition, or Workspace that
   avoids silently delegating those semantics to the rate engine.
4. **Parameter and tuning budget.** Historical LIF parameters belong to the hybrid object.
   No successor rule defines what is fixed, what may be tuned, on which data, or under what
   budget.
5. **Primary comparator and claim.** H9 describes rate-vs-spiking invariance, while C07 also
   names hybrid-vs-fully-spiking comparison. The primary contrast and allowed claim are not
   uniquely fixed.
6. **Tolerance authority.** The historical tolerances were frozen for the hybrid object.
   The repository does not say whether every one is the acceptance rule for a fully-spiking
   successor or merely an inherited diagnostic.
7. **Training/plasticity regime.** Fixed-weight, surrogate-gradient, and local-plastic
   routes are not prospectively disambiguated.
8. **Exact runtime/randomness contract.** Historical versions are recorded, but a new exact
   Python/PyTorch/snnTorch runtime, seeds, determinism settings, and noise policy are not
   frozen.

Choosing any of these now would design new science. SUB therefore stops before creating a
fresh scientific identity or executable successor protocol.

## Readiness assets established

`readiness.json` pins the exact current source blobs that define H9, C07 doctrine, the
historical hybrid backend, canonical scenario, comparison runner/tests, dependency record,
and historical result. It also records the existing hybrid-vs-fully-spiking boundary and
the scientific choices that remain unresolved.

`scripts/verify_h9_fully_spiking_readiness.py` is a fail-closed source-only verifier. It
checks the pinned Git blobs, confirms the package remains non-executable, verifies the
historical hybrid boundary markers, and requires every unresolved scientific choice to
remain explicit. It does not import snnTorch, run SwitchWorld, or produce scientific output.

## Handoff to the next Analyst cycle

A fresh H9 successor can be protocolized only after the Analyst prospectively fixes the
fully-spiking operational boundary, neural dynamics/representation mapping, comparator and
claim, tolerance authority, parameter/tuning budget, runtime/randomness contract, and a
distinct protocol/one-way identity.

Until then:

- do not rerun or retune historical C07;
- do not treat the 9/9 hybrid result as evidence for a fully-spiking system;
- do not use the threshold-1.1 negative as a calibration target;
- do not cross STARTED;
- do not make energy claims;
- do not touch C19 from this branch.
