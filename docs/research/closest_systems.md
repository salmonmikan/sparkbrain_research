# C09 Closest Systems and Claim Boundaries

**Status:** initial counterexample set, reviewed 2026-08-23.
**Scope:** this file identifies the strongest known precedents for SparkBrain's current design language. It does not claim the set is exhaustive or that a complete duplicate has been found.

## Bottom line

SparkBrain must not present any of the following as a new mechanism by itself:

- coalitions competing for a global workspace and then broadcasting;
- ignition, competition, recurrent persistence, or inhibition;
- mismatch/reset, prediction-error processing, or nonmonotonic update;
- selective modular activation or event-driven local graph recomputation;
- spiking cognitive architectures or rate-to-spiking implementation work;
- belief-revision evaluation on sequential evidence.

The current defensible research question is narrower: whether an implementation that **keeps explicit competing belief objects, evidence identities, residual-loser recovery measures, a no-ignition state, and audited event-routed execution together** has a measurable and reproducible benefit under preregistered tasks. That benefit is unverified.

## Strongest architectural precedents

### LIDA / Global Workspace implementations — PA-001

Baars and Franklin describe a distributed codelet architecture in which coalitions compete for a capacity-limited global workspace and a selected coalition is broadcast. This is the closest cognitive-architecture precedent for SparkBrain's coalition-to-workspace narrative.

**Boundary:** SparkBrain's `Coalition`, `Ignition`, and `Workspace` terminology must be described as an explicit engineering instantiation and measurement target, not as a new architectural principle.

### Shared Global Workspace — PA-007

Goyal et al. implement specialized neural modules that compete to write to and read from a shared, bandwidth-limited workspace.

**Boundary:** learned modular competition plus a shared workspace is already a modern ML architecture. Any later C04/C05 result must compare against this family or avoid a broad modular-workspace novelty claim.

### Global neuronal workspace and spiking broadcast — PA-002 / PA-003

Dehaene, Kerszberg, and Changeux formalize global-workspace ignition; Shanahan implements broadcast and competition in a spiking network.

**Boundary:** ignition and a local spiking backend are inherited research programs. C07 can contribute only a predeclared behavioral-equivalence or failure analysis for SparkBrain's own contracts.

## Strongest dynamics precedents

### Dynamic Field Theory — PA-004

DFT provides persistent activity peaks, excitation, inhibition, competition, and working-memory capacity effects.

**Boundary:** residual activity and soft competition cannot be introduced as original dynamics. G3 remains a testable evaluation emphasis: residual-loser retention must improve recovery under controlled ablation or it is not a supported design advantage.

### Adaptive Resonance Theory — PA-005

ART has top-down expectation, vigilance, mismatch/reset, and adaptive search in a sequential setting.

**Boundary:** no-ignition must be formally contrasted with ART's mismatch/reset and category search. A no-ignition state is not novel merely because the implementation labels it differently.

### Predictive coding — PA-010

Predictive-coding formulations already use recurrent inference and prediction-error signals.

**Boundary:** the project may use error signals, but cannot claim prediction-error activation as its own theoretical primitive.

## Strongest computation and representation precedents

### RIMs, temporal graph networks, and AEGNN — PA-006 / PA-008 / PA-009

RIMs establish selective recurrent-module updates. TGN provides persistent state over timestamped graph events. AEGNN is especially important because it explicitly restricts recomputation to nodes affected by an event.

**Boundary:** the C04/C05 execution-sparsity claim requires counters that prove which Spark updates and edge evaluations did not occur, plus a comparison to a dense-equivalent path. Activity masks and activity ratios alone are insufficient.

### Assembly Calculus and Spaun — PA-011 / PA-012

Assembly Calculus gives local assembly operations with plasticity and inhibition; Spaun demonstrates a large functional spiking cognitive architecture.

**Boundary:** C07/C08 must not claim first functional spiking cognition, biological equivalence, or first assembly-based organization. Structural-plasticity results require causal intervention and held-out reuse tests.

### Abstract argumentation and Belief-R — PA-013 / PA-014

Dung's framework is a strong formal precedent for nonmonotonic support/attack reasoning. Belief-R is a benchmark precedent for the update-versus-retain trade-off under sequential premises.

**Boundary:** evidence provenance, contradiction, and revision need formal comparison to argumentation semantics; C06 must treat Belief-R as an established external benchmark rather than a novel task.

### Workspace-like language-model representations — PA-015

The 2026 Transformer Circuits report presents causal evidence for workspace-like representations in language models. It is a first-party research report and is not treated here as peer reviewed.

**Boundary:** no public document may assert that Transformers or LLMs lack workspace-like organization. SparkBrain's potential distinction is explicit inspectable state and event-routed execution, neither of which is yet a demonstrated performance advantage.

## Claim-by-claim novelty verdicts

| SparkBrain candidate | Current verdict | Strongest counterexample(s) | Required evidence before stronger framing |
|---|---|---|---|
| Persistent competing belief objects | partial overlap | LIDA, ART, temporal graph memory | formal comparison and controlled held-out revision tests |
| Evidence-bearing coalition | partial overlap; high risk | LIDA coalitions; Dung argument graphs | define independence, provenance, and contradiction semantics against those systems |
| Residual loser recovery | plausible evaluation emphasis; unverified | DFT persistence; ART search/reset | ablation with confidence intervals across controlled worlds |
| No-ignition as a computational state | partial overlap | ART reset/search; abstention and belief-revision evaluation | formal semantics and calibration/abstention comparison |
| True execution sparsity | partial overlap; strong precedent | RIMs; AEGNN | audited no-touch counters and dense-equivalence tests |
| Unified inspectability | engineering-integration value | traceable cognitive architectures and causal-analysis work | do not frame as standalone scientific novelty |
| Rate-to-spiking transition | known research program | Shanahan; Spaun | predeclared equivalence/failure suite |

## Citation map

The full bibliographic and implementation-status record is in `literature_matrix.csv`; exact query history and the required second-pass search plan are in `search_log.md`.
