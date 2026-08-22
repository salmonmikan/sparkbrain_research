# Event-routed persistent belief dynamics with evidence coalitions

## SparkBrain v0.2.1 release-candidate technical report

Status: evidence-bounded local research prototype. C01-C10 implementation and non-license reproducibility preparation are integrated. Public release remains blocked until the repository owner selects a project license.

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

The Phase-0 scalar controls, C02 ablations, and ten C05 baseline families are integrated. In the reduced five-seed acceptance run, architecture-body parameters were within ±2% and an optimizer-work proxy within ±5%, but quality matching and scientific compute matching failed. Learned accuracy varied sharply by seed. CL-007 remains E0; the run validates the harness, not a modern-baseline advantage.

## 8. External validation

C06 pins Belief-R revision `3719f5804c63318037465fecf298a7fd78d99121` and evaluates all 1,744 official pairs zero-shot with network access blocked. The official test cannot be used for fit, calibration, selection, or splitting. Spark BU/BM/BREU were 0.0391/0.0896/0.0643 with final coverage 0.2271, below direct and uniform-chance BREU 0.25. Representations, parameters, and compute were unmatched; duplicate and irrelevant interventions exposed substantial sensitivity. This is a negative external result and CL-007 remains E0. External text remains excluded from Git and release enumeration.

## 9. Spiking equivalence

C07 provides a reduced snnTorch LIF sensory encoder while evidence graph, hypothesis, Coalition, ignition, and Workspace remain algorithmic. Nine frozen checks pass on one canonical scenario. A higher threshold produced no spikes and no predictions. This is E1 hybrid fixture evidence, not full spiking or biological equivalence.

## 10. Ablations and causal interventions

C02 records residual, hard-WTA, inhibition, source-diversity, contradiction, stability, margin, forced-prediction, dense-accounting, Workspace, homeostasis, and refractory conditions. Brain Lab branches preserve immutable parents. C08 implemented bounded structural mechanisms, but targeted, random, and degree-matched ablations all produced zero impairment; decisiveness, fertility, and specificity failed. CL-008 remains E0 and no emergent-organ claim is permitted.

## 11. Compute and resource accounting

Reference and learned paths separate active updates, edge/message evaluations, dense encoder/router work, estimated launches, tracked memory, and wall clock. These are software counters. No physical power measurement exists; Extension H is the only path for hardware-energy evidence.

## 12. Failures and threats to validity

The controlled tasks are generated, weights and distributions can encode solutions, coverage changes metric interpretation, C04 uses a small held-out subset, C05 matching failed, C06 representations are unmatched and performed below direct/chance, C07 covers one scenario, C08 specialization gates failed, and C09 is a bounded audit. The generated negative appendix and evidence map enumerate exact run and artifact boundaries.

## 13. Reproducibility

After local dependency setup, run: python scripts/reproduce_release.py --offline --output artifacts/reproduced-release. The command checks frozen input hashes, runs CPU readiness, regenerates the bounded primary table and SVG, checks output hashes, and writes a machine manifest. It is a smoke subset, not the full evaluation. Full experiment commands remain in their phase reports and configs.

## Conclusion

The candidate establishes an inspectable local software substrate, controlled synthetic observations, and a negative offline external evaluation. It does not establish a completed theory, general advantage, successful external generalization, autonomous organs, biological fidelity, consciousness, AGI, novelty, or energy gains. Exact support and evidence boundaries are machine-readable in artifacts/release/evidence_map.json.
