# Scope allocator component-replacement probe

This NON_EVIDENTIARY/NONCANONICAL Forge probe replaces only the fixed-radius
nearest-centroid allocator in the scope-to-revision fixture with a standard
two-component Gaussian-mixture reference allocator.

The reference allocator receives observation vectors only. It does not receive
scope, regime, episode, label, truth or evaluator identity while fitting or
routing. Labels are applied only after routing through the unchanged
scope-specific revision overlay.

The comparator is deliberately limited. It fixes two components in advance and
fits the complete bounded stream before routing, so it has future-context and
model-cardinality advantages over the online fixed-radius allocator. It is a
component replacement diagnostic, not a fair system comparator.

The probe asks two narrow questions:

1. Does an established observation-only allocator resolve the prior
   within-reuse-radius collision?
2. Does it still fail closed when the observations are identical and therefore
   cannot identify the conflicting contexts?

A positive first result means the old failure was allocator-specific on this
fixture. It does not establish learned latent organization, general robustness,
composition contribution, comparative superiority or scientific novelty.
