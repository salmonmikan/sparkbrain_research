# Scope-revision boundary stress probe

This Forge-only probe reuses the continuous scope-to-revision interaction
ablation with three fixed synthetic cases:

- moderately overlapping clusters with small within-cluster jitter and an
  ambiguous midpoint query;
- contradictory outcomes whose observations remain inside the allocator's
  fixed reuse radius;
- two separable clusters with one conflicting label in the A cluster.

The probe records both the connected and connection-cut arms, their commit
counts, internally generated opaque scope tokens, query outputs and abstentions.
It accepts no caller scope, regime, episode, truth or evaluator identity.

This is a deterministic boundary diagnostic, not a benchmark. The expected
result is deliberately mixed: the connected fixture can retain context-specific
majorities when routing remains separable, but it must abstain when the fixed
router cannot distinguish observations inside its reuse radius. That failure is
part of the result and prevents interpreting the component as general latent
cause discovery.

The behavior reduces to ordinary nearest-centroid allocation, a reject option,
and per-key evidence accumulation. It does not establish calibrated robustness,
system superiority, general composition contribution or scientific novelty.
