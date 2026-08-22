# Causal Transformer baseline

- Context: maximum 64 observations; future positions are blocked by an upper-triangular
  attention mask.
- Architecture: one local Transformer encoder layer plus classifier, CPU path retained.
- Information/training/matching: identical to the recurrent cards.
- Limitation: compact one-layer/four-head integration configuration and short training;
  it is not presented as a definitive Transformer result.
