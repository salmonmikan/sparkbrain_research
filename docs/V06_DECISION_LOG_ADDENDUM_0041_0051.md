# SparkBrain v0.6 Decision Log Addendum
## Decisions D-V06-0041 through D-V06-0051

This addendum continues `docs/V06_DECISION_LOG.md` after D-V06-0040.

## D-V06-0041 — Repeated-episode causal provenance uses current arrivals

The retained v0.4 `source_pulse_ids` field accumulates unit history and is not sufficient to identify
the current Spark's causal roots. The v0.6 chain adapter peeks pulse IDs arriving at the current event
time and attributes proposal roots only from those arrivals.

## D-V06-0042 — Outbound ports are anonymous execution boundaries

A terminal Field Spark may emit through an anonymous structural port. The port is not tagged as an
action, policy, output class, correct response, or goal.

## D-V06-0043 — World links are physical mappings outside the Field

The world adapter maps an anonymous outbound port to later raw external events. The Field receives no
correct-port signal, reward, utility, outcome class, or semantic interpretation of that mapping.

## D-V06-0044 — Boundary recurrence does not stabilize a relation

An outbound boundary event creates only a pending structural exposure. It cannot create or strengthen
a positive anonymous port-to-external link without a later registered external event.

## D-V06-0045 — External consistency updates anonymous structural tuples

The consistency substrate may update `(port, external target, polarity, lag, magnitude ratio,
reliability)` after external pairing. It may not store a functional relation type or meaning value.

## D-V06-0046 — Boundary intervention is causal and stage-matched

Targeted suppression of `port:7` preserves the internal terminal Spark but removes the corresponding
raw external stream. Suppression of the equally active disjoint `port:9` does not damage the target
stream.

## D-V06-0047 — Observer taxonomy permutations cannot alter Primary state

Renaming or permuting post-hoc descriptions of anonymous ports may change observer artifacts only.
The Primary runtime state hash must remain unchanged.

## D-V06-0048 — V06-10 is partial Level 3 only

V06-10 demonstrates external stabilization and selective boundary/world effect in one canonical
engineering world. It is not completed Level 3 until anonymous relation revision and held-out
controls are demonstrated.

## D-V06-0049 — Revision changes external consistency, not port identity

V06-11 keeps the internal chain and `port:7` fixed while the world changes its raw external target.
This tests revision of anonymous relation state rather than replacement of the outbound unit or port.

## D-V06-0050 — Old anonymous relation history is retained during reversal

Reversal increases inconsistency for the old link and consistency for the new link. The old link is
not erased. If the original contingency returns, its previous evidence can be extended and it can
again become dominant.

## D-V06-0051 — V06-11 is a single-world Level-3 engineering candidate

The canonical relation stabilizes, reverses, and reacquires under raw external contingencies while a
stable control avoids unnecessary link proliferation. This completes the shape of Level 3 in one
engineering construction. It is not confirmatory Level 3 because held-out worlds/seeds, adaptive use
of revised state, and persistence-locus analysis remain unresolved.
