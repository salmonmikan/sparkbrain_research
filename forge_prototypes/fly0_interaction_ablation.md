# FLY-0 interaction-ablation matrix

Status: NON_EVIDENTIARY / NONCANONICAL Fast Forge diagnostic

This diagnostic closes one open FLY-0 engineering question by asking which
interface edges are actually causal for bounded world progress in the current
hierarchical prototype. It does not turn the prototype into a scientific
experiment and does not allocate SB003.

## Matrix

The same structured FLY-0 controller and deterministic line world are run under
five conditions:

1. intact;
2. local observation payload masked before it reaches the local controller;
3. ascending feedback payload zeroed while preserving the controller action;
4. descending modulation removed;
5. local action output forced to zero while preserving proposal activity.

The matrix is about the current implementation boundary rather than topology
quality. It complements the separate resource-normalization diagnostic.

## Expected engineering interpretation

The current local controller derives its direction from descending modulation
and does not consume the local `Observation` payload. The high-level loop
derives the next modulation from world error and stores local feedback for
inspection, but does not feed that payload back into the next decision.

Therefore the bounded prototype should show:

- masking the local observation payload preserves the world trajectory;
- masking the ascending feedback payload preserves the world trajectory;
- removing descending modulation prevents progress and fails closed at action
  arbitration;
- zeroing local action prevents progress even though bounded steps can commit.

If these checks pass, the useful result is a negative engineering localization:
the current prototype has a causal top-down modulation -> local action path, but
its nominal bottom-up observation/feedback surfaces are not yet causally
integrated into the next control decision.

That identifies a concrete future integration gap without claiming that a
fly-like topology is necessary or superior.

## Run

```bash
python -m pytest -q tests/test_forge_fly0_interaction_ablation.py
python -m ruff check forge_prototypes/fly0_interaction_ablation.py \
  tests/test_forge_fly0_interaction_ablation.py
python -m forge_prototypes.fly0_interaction_ablation
```

## Claim boundary

The matrix is NON_EVIDENTIARY/NONCANONICAL. It supports only a bounded
engineering statement about which payloads the current implementation consumes
causally. It does not establish topology superiority, biological fidelity,
composition contribution, external validity, energy efficiency, novelty, or
SYSTEM_BUILD admission. It does not modify A01, RV02, H9, C07, M1, canonical
science, or any consumed/frozen identity.
