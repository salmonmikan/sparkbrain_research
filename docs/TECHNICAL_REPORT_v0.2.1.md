# Event-routed persistent belief dynamics with evidence coalitions

## SparkBrain v0.2.1 release-candidate technical report

Status: evidence-bounded local research prototype. Public release is blocked until the repository owner selects a project license. C05 matched baselines, final C06 external execution, and C08 structural-plasticity results are not integrated in this candidate.

## 1. Problem and falsifiable hypotheses

SparkBrain asks whether explicit competing beliefs, evidence identity, coalition gates, residual loser state, and event routing improve stable but revisable inference. H1-H5 are tested as engineering or controlled-synthetic hypotheses. H6 emergent specialization remains unsupported. No biological, consciousness, AGI, novelty-proof, or energy claim follows.

## 2. Prior art and contribution boundary

Global-workspace systems, dynamic fields, recurrent independent mechanisms, adaptive resonance, HMMs, active inference, sparse event processing, argumentation, and spiking cognitive systems overlap strongly with the mechanisms. The candidate contribution is an inspectable integration and evaluation protocol, not a claim that its primitives are original. The bounded C09 audit and its unresolved search uncertainty are authoritative.

## 3. Formal model

The reference state contains Sparks, Connections, Coalitions, Workspace state, memory, queued Events, and control state. Events are ordered by time, priority, and sequence. Coalition score and ignition gates use evidence identity, source diversity, stability, contradiction, score, and competitor margin. No-ignition is valid. Full equations are in docs/THEORY_SPEC_v0.2.1.md.

## 4. Implementation and trace semantics

The dependency-free Python reference engine uses a deterministic priority queue and lazy decay. Pure inspection is separated from trace-recording snapshots. Checkpoints contain pending work and deterministic continuation state. Brain Lab runs only on loopback, exports explicit local bundles, rejects malformed or oversized imports, and does not use CDN assets or analytics.

## 5. Controlled worlds

C02 freezes six synthetic worlds and 37 declared conditions over 1,000 test seeds each. The full per-episode raw rows are locally reproducible but intentionally not committed because they are about 492 MiB. Committed manifests, aggregate values, intervals, failures, configs, and seeds preserve the experiment contract. MultiObjectWorld full coverage was zero and is retained.

## 6. Learned architecture

C04 adds an optional PyTorch learned encoder, bounded top-k router, persistent modules, selected-subgraph recurrent work, separate belief/action heads, coalition traces, and calibrated no-ignition. On 60 held-out controlled episodes it exceeded chance and a training-majority control, but the reduced smoke was below chance and the router retained dead and overloaded modules. This does not establish superiority or external generalization.

## 7. Matched baselines

The Phase-0 scalar controls and C02 ablations are present. The required matched GRU, Transformer, modular recurrent, and probabilistic comparison package from C05 is pending integration. Therefore CL-007 remains E0 and no result in this candidate supports a modern-baseline advantage.

## 8. External validation

C06 currently supplies only versioned acquisition/checksum/cache schemas and a generated development track. Belief-R remains test-only and its dataset card separately declares CC BY-SA 4.0; that declaration does not license generated Track B or SparkBrain source. External text is excluded from Git and release enumeration. Model execution is not an accepted result in this candidate.

## 9. Spiking equivalence

C07 provides a reduced snnTorch LIF sensory encoder while evidence graph, hypothesis, Coalition, ignition, and Workspace remain algorithmic. Nine frozen checks pass on one canonical scenario. A higher threshold produced no spikes and no predictions. This is E1 hybrid fixture evidence, not full spiking or biological equivalence.

## 10. Ablations and causal interventions

C02 records residual, hard-WTA, inhibition, source-diversity, contradiction, stability, margin, forced-prediction, dense-accounting, Workspace, homeostasis, and refractory conditions. Brain Lab branches preserve immutable parents. C08 emergent-organ interventions are pending and must not be inferred from C04 module activity.

## 11. Compute and resource accounting

Reference and learned paths separate active updates, edge/message evaluations, dense encoder/router work, estimated launches, tracked memory, and wall clock. These are software counters. No physical power measurement exists; Extension H is the only path for hardware-energy evidence.

## 12. Failures and threats to validity

The tasks are generated, weights and distributions can encode solutions, coverage changes metric interpretation, C04 uses a small held-out subset, C07 covers one scenario, C06 has no accepted model result, and C09 is a bounded audit. The generated negative appendix and evidence map enumerate exact run and artifact boundaries.

## 13. Reproducibility

After local dependency setup, run: python scripts/reproduce_release.py --offline --output artifacts/reproduced-release. The command checks frozen input hashes, runs CPU readiness, regenerates the bounded primary table and SVG, checks output hashes, and writes a machine manifest. It is a smoke subset, not the full evaluation. Full experiment commands remain in their phase reports and configs.

## Conclusion

The candidate establishes an inspectable local software substrate plus controlled synthetic observations. It does not establish a completed theory, general advantage, external replication, autonomous organs, biological fidelity, consciousness, AGI, novelty, or energy gains. Exact support and pending gates are machine-readable in artifacts/release/evidence_map.json.
