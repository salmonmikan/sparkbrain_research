# C11 input-bottleneck diagnosis

- Protocol: `c11-input-bottleneck-v2`
- Conclusion: **implicated**
- Engineering status: complete
- Official Belief-R test used: no
- Oracle leakage audit: pass
- Seeds: 1729, 1730, 1731, 1732, 1733
- Paired interval method: diagnostic-pair block bootstrap
- Strongest counterexample: I1_local_compositional / high_overlap_negation / similarity 0.737984

## Interpretation

- Oracle accuracy gap over I0: 0.500000
- I1 similar-pair surface retention delta over I0: 0.559798
- Oracle leakage audit: pass
- I1 accuracy did not improve over I0; a rough-input solution is unsupported

The result localizes an input-representation bottleneck under this synthetic
diagnostic. It does not establish semantic understanding or external
generalization,
concept or organ formation, biological fidelity, or cognitive-core validity.
