# RV01 R01-15 implementation audit

Status: **SOURCE AUDIT PASS / DEVELOPMENT EXECUTION NOT YET STARTED**

## Bound identities

- Protocol: `rv01-r01-15-post-spike-suppression-v1`
- Active preregistration merge: `b28e79005438de66fde07eee89e8f1fcc1c5cc6d`
- Audited implementation head: `f8cdd7ea3baf4c8f9b22994ccf02b44bde1bb2cc`
- Implementation branch: `research/rv01-r01-15-post-spike-suppression-impl`
- Exact-head push CI: Actions run `34592700837`, success on the repository CI matrix.

This audit is outcome-blind with respect to the R01-15 development grid: no registered development seed has been executed by the audited implementation and no held-out seed is opened.

## Contract audit

The implementation satisfies the preregistered isolation contract:

1. Every intervention arm restores from the same serialized pre-probe Field state and verifies semantic equality with the supplied checkpoint before the first probe spike.
2. `PostSpikeSuppressionField._deliver_group` delegates to the ordinary Field runtime first. The registered spike and its ordinary outgoing queue/connection consequences therefore exist before any R01-15 edit is applied.
3. `adaptation_zero` edits only the spiking unit's `adaptation` field to `0.0` after the spike.
4. `refractory_zero` edits only the spiking unit's `refractory_until_ms` to the emitted spike time after the spike.
5. `both_zero` is exactly the conjunction of those two registered edits; it adds no third intervention.
6. The implementation changes no topology, connection weight/delay, cue route, base threshold, queue item or training state.
7. Every edit is retained with mode, unit ID, spike time, field, before value and after value.
8. The module contains no development-grid generator, scorer, held-out path or formal execution entrypoint.

## Test audit

The exact audited head includes tests that verify:

- byte-semantic pre-probe restoration equality across F0/FA/FR/FAR;
- ordinary queue and connection state equality after the first spike across arms;
- FA/FR/FAR field isolation;
- exact intervention-record scope;
- a later-arrival isolation check in which refractory neutralization changes response while the later input remains above the still-adapted threshold.

Two deterministic CI repairs made before the successful exact-head run were non-scientific:

- raising the synthetic later-arrival test current from `0.6` to `0.7` so the FR arm actually isolates refractory state rather than remaining below the adapted threshold;
- importing `SynapticArrival` from its actual `sparkbrain.v04.contracts` module.

Neither repair changes the registered R01-15 development seeds, world salt, runtime constants, intervention values, horizon, comparator, endpoints or held-out namespace.

## Audit verdict

**PASS for implementation isolation.** The exact head `f8cdd7ea3baf4c8f9b22994ccf02b44bde1bb2cc` is suitable to merge into the active RV01 research line once its PR CI is green and the head remains unchanged.

This audit does **not** authorize any held-out execution. After merge, the next permitted scientific step under the preregistration is construction and review of a fixed five-seed exposed-development runner using seeds `141500..141504`, followed by one development execution under the frozen protocol inputs. Reserved held-out seeds `141600..141609` remain capability-sealed.
