# SparkBrain Theory Specification v0.6 — Development Foundation

Status: **V06-00–V06-02 implemented; generative dynamics not yet established**  
Target namespace: `sparkbrain.v06`  
Baseline: `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`

## 1. Central hypothesis

The primary runtime must not require an explicit Assembly state. v0.6 tests whether persistent
Field state can later generate forward endogenous Sparks, accept external correction, and retain
experience without treating internal predictions as observations.

```text
external signal
      ↓
persistent Field state
      ↓
G0/G1/G2 endogenous transition
      ↓
internal pulse proposal
      ↓
normal-rule Field reinjection
      ↓
external confirmation or contradiction
```

Assembly analysis is outside this runtime path:

```text
immutable runtime trace
      ↓
post-hoc Assembly / trajectory observer
```

## 2. Runtime state

The development state is:

\[
B_t=(F_t,Q_t^{ext},Q_t^{endo},Z_t,T_t,H_t,R_t,C_t)
\]

- `F`: current excitable-Field state;
- `Q_ext`: external event queue;
- `Q_endo`: endogenous proposal queue;
- `Z`: persistent local traces;
- `T`: local transition state;
- `H`: homeostatic and adaptation state;
- `R`: generation budgets;
- `C`: reality-matching state.

No Assembly ID, prototype, or membership belongs to `B_t`.

## 3. Provenance

Every runtime pulse has exactly one origin:

- `external`;
- `endogenous-unconfirmed`;
- `endogenous-confirmed`;
- `endogenous-contradicted`;
- `endogenous-expired`.

Only `external` counts as an observation. A prediction that causes a Field spike remains a
prediction.

## 4. Two-phase learning

An endogenous path may create a temporary eligibility record, but it cannot commit a positive
update. Positive learning is committed only after a registered external event confirms that same
path. Contradiction and expiry cannot increase confidence.

This rejects the loop:

```text
predict C → internally fire C → count C as observed → increase confidence
```

## 5. Observer non-interference

For identical initial state, seed, and external input:

\[
Runtime(Observer=ON)=Runtime(Observer=OFF)
\]

Field trace, queues, predictions, actions, learning updates, RNG state, and state hashes must be
identical. Only observer artifacts may differ.

## 6. Forward completion

For an external sequence `A → B → [C omitted] → D`, primary forward completion requires:

\[
t(C_{endo}) < t(D_{external})
\]

Inferring C after D arrives is retrospective reconstruction and is scored separately.

## 7. Current implemented contracts

- external/endogenous event provenance;
- endogenous proposals and chains;
- two-phase eligibility;
- external-confirmation gate;
- Assembly-free runtime-state validation;
- immutable observer trace;
- observer ON/OFF equality helper;
- fail-closed development checkpoint integrity.

## 8. Current non-claims

This foundation does not establish G0/G1/G2 continuation, forward missing-middle completion,
reality correction, prediction/action utility, a memory locus, semantic meaning, concepts, organs,
consciousness, AGI, or biological equivalence.

`docs/V06_RUNTIME_INVARIANTS.md` is normative for implementation safety. The full program is
specified by the final v0.6 master plan retained with the project handoff.
