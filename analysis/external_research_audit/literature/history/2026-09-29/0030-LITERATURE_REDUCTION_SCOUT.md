# External Literature Reduction Scout — bilateral semantic surfaces and matched fly-control nulls

- schema_version: `2`
- generation_id: `LIT-20260929T003503+0900-R48-BILATERAL-SEMANTIC-NULLS-BANC`
- produced_at: `2026-09-29T00:35:03+09:00`
- role: `LITERATURE_REDUCTION_SCOUT`
- status: `NON_EVIDENTIARY / NONCANONICAL`
- genuinely_new_information: `true`
- new_scientific_result: `false`

Directive index is unchanged at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d / 1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Durable Control is R116; durable Analyst is R168. SB003 remains unallocated. M1-002 is not blocked by this literature work.

This run targeted the FLY-0 comparator defect identified by Methodology R145 / Forge: rewired and random-sparse controls can destroy left/right sensorimotor meaning while the structured fixture preserves it.

## Findings

1. **Bates et al., Nature 2026 — distributed brain-and-cord control**
   - DOI: https://doi.org/10.1038/s41586-026-10735-w
   - Classes: `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.
   - Adult-fly BANC reports same-body-part sensory→effector local feedback loops linked by ascending/descending behaviour-centric modules, with learning/navigation regions acting in a supervisory role.
   - Design use: local sensorimotor loops plus selective long-range supervision.
   - Limit: does not validate SparkBrain's reduced topology or biological fidelity.

2. **Rayshubskiy et al., eLife 2025 + Braun et al., Nature 2024 — bilateral/population steering control**
   - DOI: https://doi.org/10.7554/eLife.102230.1
   - DOI: https://doi.org/10.1038/s41586-024-07523-9
   - Classes: `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.
   - Right-minus-left descending activity predicts steering; bilateral see-saw recruitment and distributed behaviour-specific DN populations carry functional motor meaning.
   - Design use: preserve declared left/right motor semantics when topology is randomized.
   - Limit: does not require every internal edge to stay ipsilateral and does not establish fly-like topology superiority.

3. **Pedigo et al., eLife 2023 — bilateral network comparisons depend on the null definition**
   - DOI: https://doi.org/10.7554/eLife.83739
   - Classes: `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.
   - Symmetry conclusions change with density adjustment, cell-type grouping, edge definition and the selected network model.
   - Design use: declare semantic partitions before randomization and use nested nulls rather than calling one rewiring universally matched.
   - Limit: connectome symmetry is not controller equivalence.

4. **Hao et al., Network Neuroscience 2025 — degree preservation alone is not a generally sufficient neural-network null**
   - DOI: https://doi.org/10.1162/netn_a_00428
   - Classes: `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.
   - Across fly/mouse/human connectomes, degree-only and spatial-only models each miss structure that combined constraints recover.
   - Design use: match variables that confound the claim under test.
   - Limit: spatial/contact matching is not a default gate for ordinary NON_EVIDENTIARY engineering.

## Handoff

The literature materially supports the prospective FLY-0 repair: for the **primary functional comparator**, preserve the task-relevant semantic surface—at minimum `source role + target role + source side + target side`—alongside the declared resource/degree/sign/delay constraints that actually apply, then randomize topology.

Retain the old degree/role-only rewiring as a **coarse diagnostic null**, not the sole functionally matched comparator. For any later topology-specific scientific claim, use a prospective nested reduction ladder and add stronger spatial/contact constraints only if the claim requires them.

This does not repair Forge code, allocate SB003, stop M1, reopen prior science, or establish biological fidelity, topology superiority, efficiency, novelty, composition contribution, or scientific credit.
