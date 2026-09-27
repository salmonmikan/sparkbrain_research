# Causal online scope-router probe

This NON_EVIDENTIARY/NONCANONICAL Forge probe removes the complete-stream
look-ahead used by the earlier batch two-component GMM reference. It uses a
bounded streaming two-centroid router: a component is born only from the
current observation and prior state, centroids update by an online mean, and
ambiguous or out-of-support observations are rejected without mutation.

The router receives observation vectors only. Labels are applied afterward to
the unchanged scope-local revision overlay. Scope, regime, episode, truth and
evaluator identities are absent from the routing API.

The probe asks whether the earlier close A/B synthetic fixture remains
separable under three arrival orders without future context, while preserving
no-write rejection at the midpoint, outside learned support, and when identical
observations carry conflicting labels.

This is ordinary streaming clustering with fixed K=2, a fixed birth threshold,
nearest-centroid routing and margin rejection. A positive result removes one
engineering limitation of the batch reference on these fixtures only. It does
not provide a matched comparison, automatic component-count selection,
drift handling, learned representations, general robustness, composition
contribution or scientific novelty.
