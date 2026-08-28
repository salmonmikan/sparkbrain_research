# v0.4 scientific basis and claim boundaries

## Purpose

v0.4 borrows experimentally or computationally established motifs, but their combination does not prove that SparkBrain is biologically faithful or intelligent.

## Primary sources used as design precedents

1. Lichtsteiner, Posch, and Delbruck, **A 128 x 128 120 dB 15 us Latency Asynchronous Temporal Contrast Vision Sensor**, IEEE JSSC 43(2), 2008. DOI: `10.1109/JSSC.2007.914337`.
   - Precedent: a digital sensor can emit asynchronous local change events rather than full frames.
   - Does not prove: SparkBrain's transduction matches retinal computation.

2. Maass, Natschläger, and Markram, **Real-time computing without stable states**, Neural Computation 14(11), 2002. DOI: `10.1162/089976602760407955`.
   - Precedent: time-varying input can perturb recurrent circuits whose transient state is computationally useful.
   - Does not prove: the v0.4 field has liquid-state separation or approximation guarantees.

3. Beggs and Plenz, **Neuronal Avalanches in Neocortical Circuits**, Journal of Neuroscience 23(35), 2003. DOI: `10.1523/JNEUROSCI.23-35-11167.2003`.
   - Precedent: cortical activity has been analyzed as cascades/avalanches with nontrivial size distributions.
   - Does not prove: the brain is universally critical, or that v0.4 should be tuned to a power law.

4. Izhikevich, **Polychronization: Computation with Spikes**, Neural Computation 18(2), 2006. DOI: `10.1162/089976606775093882`.
   - Precedent: conduction delays and spike timing can support reproducible time-locked but non-synchronous patterns.
   - Does not prove: a recurring v0.4 cascade is a memory or concept.

5. Timing-dependent synaptic plasticity literature.
   - Precedent: update direction may depend on relative pre/post spike timing.
   - v0.4 uses a bounded engineering rule and does not claim a faithful biological STDP model.

## Claims permitted for the reference implementation

When tests pass, the project may say:

- a local CPU simulation can convert digital changes into timestamped pulses;
- delayed recurrent propagation can distinguish temporal order;
- aligned weak arrivals can trigger a target when dispersed arrivals do not;
- adaptation can change repeated responsiveness;
- a learned temporal interval can produce an omission prediction-error pulse;
- recurrent cascade signatures can be measured and visualized;
- state can be checkpointed with integrity verification.

## Claims not permitted

- human-like perception;
- semantic understanding;
- spontaneous concept or organ formation;
- consciousness or AGI;
- biological equivalence;
- critical-brain confirmation;
- lower physical energy use;
- superiority to Transformers, RNNs, SNNs, or neuromorphic hardware;
- generalization beyond the tested synthetic conditions.
