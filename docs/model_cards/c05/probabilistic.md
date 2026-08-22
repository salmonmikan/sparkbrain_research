# Probabilistic baselines

## Privileged Bayes

Uses declared evidence weights and a fixed stay/switch prior. It is a privileged diagnostic,
not an information-matched learned competitor.

## Laplace HMM

Transition and emission probabilities use only the training half of C02 dev episodes with
Laplace smoothing. Filtering is causal, resets per episode, and maps unseen evidence to
`UNK`. Both systems have zero trainable parameters and report state updates/state bytes.
