# RV02-RD006 v3 structural-temporal role preflight contract

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Revision: `v3-structural-temporal-role-preflight`

Phase: `OPEN_DEVELOPMENT`

Claim ceiling: `SYSTEM`

Evidence Analyst authority: `EVA-20260927T135700+0900-R149-RD006-V3-STATIC-PREFLIGHT`

Parent static audit: `cdb985e16dda2b38f7a0713e51992fa16f128ad5`

## Scope

This revision is a prospective construction and static preflight only. It may
create a deterministic role/schedule topology and verify static invariants. It
must not instantiate or run a Field, execute an OFF/ON arm, cell or matrix,
score capability, use held-out data, or inspect v1/v2 spike identities and
per-row outcomes as construction inputs.

The v1 and v2 outcomes remain preserved and closed as
`D0_INCONCLUSIVE_BOUNDED_EXPLOSION`, with zero confirmatory credit. RD005
remains `CONSUMED_ONE_WAY` and is not reopened.

## Precommitted construction rule

Rule: `STATIC_PORT_HIDDEN_RETURN_CLOCK_V1`.

For each of the six fixed families:

1. Reconstruct the baseline topology from the fixed seed and family routes.
2. Reconstruct the unchanged declared 5.5 ms schedule.
3. Sort consecutive within-route schedule transitions by route, episode,
   position, predecessor role, return role and event ID.
4. Select the first transition whose predecessor port already has at least two
   outgoing edges to static hidden roles and whose nominal hidden time
   (`predecessor clock + fixed 5.0 ms delay`) is 0.5–6.5 ms before the declared
   return clock.
5. Order those hidden roles by a digest of only the rule ID, fixed seed,
   family, predecessor role, return role and hidden role. Select the first two.
6. Preserve every port-source/route edge. For the selected hidden roles, add a
   hidden-to-return edge while preserving every hidden ring edge. Fill the
   remaining hidden-source slots deterministically from baseline targets, then
   numeric targets, to retain exact out-degree 8.

No observed spike, ready-cell result, artifact row, capability result, or
bounded-stop outcome is accepted as a construction input.

## Static acceptance

Every family must satisfy all of the following:

- at least one declared return clock has two distinct static hidden-source
  paths under the precommitted rule;
- each source has a predecessor-port-to-hidden edge and hidden-to-return edge;
- the nominal hidden-to-return-clock lag is within the fixed 0.5–6.5 ms window;
- 48 units, 384 directed edges, exact per-source out-degree 8 and mean
  out-degree 8.0;
- all existing port-source/route edges and all hidden ring edges are preserved;
- no self edge;
- deterministic serialization and replay;
- dynamic entrypoints fail closed.

Static failure closes this construction proposal without dynamics. Static
success proves construction reachability only. It does not prove that hidden
roles fire, that a visible return occurs, that learning happens, or that any
capability improves.

## Stop boundary

After publishing the source, tests, contract and static report, stop for fresh
Evidence Analyst reconciliation. A v3 matrix, E0/E1/ES, scale expansion,
reservoir comparison, learner-boundary change and capability scoring remain
unauthorized.
