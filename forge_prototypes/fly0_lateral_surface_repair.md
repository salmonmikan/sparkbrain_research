# FLY-0 lateral-surface repair diagnosis

Status: NON_EVIDENTIARY / NONCANONICAL Forge diagnostic.

The current rewired and random-sparse controls preserve role-pair counts, signs,
delays, and (for the rewired control) node degrees, but they do not preserve the
declared left/right sensorimotor interface. Their randomization can connect a
left input surface to right-local/right-motor nodes and vice versa.

That explains the current composed-loop failure: the local controller asks for a
left action, while the comparator topology produces roughly balanced or
opposite-side motor events, so arbitration fails before world progress.

A bounded repair is to preserve source and target lateral surface in addition to
the existing role-pair/resource constraints:
- degree-preserving rewiring: swap targets only inside
  (source role, target role, source side, target side) strata;
- random sparse: sample source and target from the same role+side surfaces as
  each template edge.

A deterministic local reconstruction with the existing seeds preserved the
128-unit / 512-edge resource signature and exact node-degree sequence for the
rewired control. Both repaired controls produced matched-side motor activity
with zero opposite-side motor events for left and right probes, making them
eligible for the four-way composed causal test.

This is a repair hypothesis and local engineering reconstruction only. The
repository exact head has not been changed or CI-verified because all five
authorized publication attempts for the source-repair purpose were refused
before GitHub mutation. No topology superiority, biological fidelity,
efficiency, scientific novelty, scientific credit, or SB003 allocation follows.
