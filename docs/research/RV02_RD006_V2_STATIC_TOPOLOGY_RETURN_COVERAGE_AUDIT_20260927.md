# RV02 RD006 v2 preserved static-topology return-coverage audit

## Authority and identity

- Evidence Analyst authority: `EVA-20260927T130000+0900-R148-RD006-V2-RECONCILIATION`
- Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`
- Development phase: `RESULT_EXPOSED_DEVELOPMENT`
- Preserved result head: `d2462ebc52e3bf1e6a50334ee6b8d7cf437b416a`
- Exact execution source: `7896433af675b77b1f442e9efaf268d16564c564`
- Preserved artifact SHA-256: `5898fdcb75b10747fb88f8a19329f2d063422bb5012e80683c2c413cbbfb76d6`
- Preserved artifact file SHA-256: `7ce4ffa4366f60290b26ead6edd31f9a2083f0822949c7c11815aefe8df5c468`

This audit used the preserved v2 bytes and deterministic static construction only. It did not run a Field arm, cell or matrix; mutate topology; score capability; use held-out data; infer the 16 clocks hidden by the bounded stop; or execute a v3 revision.

## Current static return coverage

Across the six family-specific topologies there are 88 scheduled return-unit roles. They are family-local counts, not 88 distinct physical unit IDs in one topology.

| Family | Return roles | 0 hidden incoming | 1 hidden incoming | 2+ hidden incoming | ON clocks with 2+ time-aligned hidden sources |
| --- | ---: | ---: | ---: | ---: | ---: |
| disjoint-routes | 12 | 2 | 3 | 7 | 0 |
| shared-cue | 10 | 2 | 1 | 7 | 0 |
| shared-prefix | 8 | 1 | 1 | 6 | 0 |
| opposing-reversal | 10 | 1 | 2 | 7 | 4 |
| dense-load | 29 | 3 | 13 | 13 | 0 |
| capacity-pressure | 19 | 3 | 9 | 7 | 8 |
| **Total** | **88** | **12** | **29** | **47** | **12** |

The preserved ON-arm timing contains 400 inspected clocks and 16 unobserved clocks behind the unchanged opposing-reversal ceiling. Fifty-one inspected clocks have at least one hidden source in the fixed 0.5–6.5 ms window and 12 have at least two. With the actual v2 edges, seven clocks have one structurally eligible source and zero have two.

## Outcome-independent role rule feasibility

The audit evaluated a static proposal, `BALANCED_HIDDEN_RETURN_INDEGREE_2_V1`. It orders the 12 hidden units from only the fixed seed, family and unit roles, then assigns two balanced hidden-source roles to each sorted scheduled return unit. It never accepts observed spike identities as input.

For every family, a topology satisfying that rule can be constructed while preserving:

- 48 units;
- 384 total directed edges;
- exact mean out-degree 8.0 and per-source out-degree 8;
- all existing port-source and route edges;
- the hidden ring edge for every hidden source.

The largest family needs at most five assigned return roles per hidden source, leaving capacity under the fixed degree budget. Therefore the rule is **structurally feasible under the same unit count and edge budget**.

This is not evidence that it is sufficient. When the deterministic, outcome-independent plan is crossed with preserved v2 timing, 19 clocks have one eligible source and zero have two. Fresh dynamics could change after rewiring, so preserved timing neither proves nor disproves a fresh revision. It only shows that static coverage feasibility is not itself a gate-opening result.

## Disposition

- v2 remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION` and its contract remains closed.
- Scientific credit remains zero.
- The failure surface is separated into static coverage deficits, temporal alignment, and the bounded/unobserved region.
- E0/E1/ES, scale expansion, reservoir comparison, learner-boundary changes and any new result-bearing matrix remain unauthorized.

An optional prospective v3 contract can require the role-level construction rule before any dynamics, preserve the same resource budget and forbid observed-spike-driven edge selection. This is a proposal only. Evidence Analyst must issue fresh authority before implementation or execution.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_rv02_rd006_v2_static_topology_return_coverage.py \
  --artifact artifacts/rv02_rd006/external_learning_reachability_a_v2_lag_alignment/attempt-001/artifact.json.gz \
  --output artifacts/rv02_rd006/external_learning_reachability_a_v2_lag_alignment/audits/preserved_static_topology_return_coverage_audit_v2.json.gz
python -m pytest -q tests/test_rv02_rd006_v2_static_topology_return_coverage.py
```
