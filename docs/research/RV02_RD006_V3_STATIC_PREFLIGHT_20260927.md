# RV02-RD006 v3 static preflight

## Authority and boundary

- Evidence Analyst: `EVA-20260927T135700+0900-R149-RD006-V3-STATIC-PREFLIGHT`
- Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`
- Revision: `v3-structural-temporal-role-preflight`
- Phase: `OPEN_DEVELOPMENT`
- Claim ceiling: `SYSTEM`
- Evidentiary status: `DEVELOPMENT_CONSTRUCTION_ZERO_CONFIRMATORY_CREDIT`

This preflight uses only the fixed seed, family, sorted static roles, declared
5.5 ms schedule, fixed 5.0 ms connection delay and fixed 0.5–6.5 ms lag
window. It does not read v1/v2 result artifacts or observed spike identities,
and it does not instantiate or execute Field dynamics.

## Result

`STATIC_PREFLIGHT_PASS`

All six families have at least one declared return clock with two distinct
static hidden-source paths under `STATIC_PORT_HIDDEN_RETURN_CLOCK_V1`. In each
case the nominal hidden time is 0.5 ms before the declared return clock.

The construction preserves:

- 48 units;
- 384 directed edges;
- exact per-source and mean out-degree 8;
- every existing port-source/route edge;
- every hidden ring edge;
- deterministic serialization and replay.

The complete machine-readable family rows, exact edge changes, path roles,
clock IDs, invariant checks and report digest are in:

`artifacts/rv02_rd006/external_learning_reachability_a_v3_structural_temporal_role_preflight/static_preflight.json`

## Interpretation

This is construction reachability, not dynamic or capability evidence. The
preflight does not show that either hidden source fires, produces visible
return, learns, or improves performance. Scientific credit remains zero.

No v3 matrix, E0/E1/ES, scale expansion, reservoir comparison or capability
scoring was performed or authorized. Fresh Evidence Analyst reconciliation is
required before any result-bearing execution.

## Reproduction

```bash
PYTHONPATH=src python scripts/build_rv02_rd006_v3_static_preflight.py \
  --output artifacts/rv02_rd006/external_learning_reachability_a_v3_structural_temporal_role_preflight/static_preflight.json
python -m pytest -q tests/test_rv02_rd006_v3_static_preflight.py
python -m ruff check \
  src/sparkbrain/research/rv02_rd006_external_learning_reachability_v3.py \
  scripts/build_rv02_rd006_v3_static_preflight.py \
  tests/test_rv02_rd006_v3_static_preflight.py
```
