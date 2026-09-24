# Active Human Directives

## HUMAN-20260918-001 — Promote reusable CX comparator assets toward main

Human status: `OPEN`  
Created: `2026-09-18 JST`

### Intent

The reusable comparator/model infrastructure developed under CX/CX01 should not remain stranded only on
research branches if it is stable and useful independently of the CX01 scientific outcome.

The desired end state is to make appropriate CX comparison assets available from the stable shared substrate
(`main`) for future reduction/comparator research.

### Candidate reusable assets

Review for promotion, rather than assuming promotion:

- G3 / G4 / G5 comparator implementations where still useful;
- G6 Variable-Order Markov comparator;
- G7 HTM / HTM-inspired Temporal Memory comparator;
- G8 spiking temporal-memory comparator;
- common architecture-neutral event / contract / adapter interfaces;
- snapshot / restore facilities;
- generic resource / privilege accounting;
- generic fairness / comparison infrastructure;
- reusable comparator tests and fixtures independent of a consumed scientific result.

### Explicitly not requested for promotion by default

- Candidate-002 scientific conclusions or terminal-result interpretation;
- raw/scored/formal evidence;
- consumed-identity state;
- candidate-specific frozen thresholds/scorers;
- candidate-specific one-way execution workflows;
- STARTED/control semantics tied to the CX01 experiment;
- result-dependent code whose utility disappears if the original hypothesis is negative.

### Human preference

Do not force a wholesale merge of `research/cx01-comparator-extension`.

Prefer an audit of outcome-independent reusable components, followed by a small integration branch / PR into
`main` if Control Brain and downstream governance conclude that promotion is worthwhile.

### Required independent review

This is a human proposal, not a command.

Control Brain must independently classify this directive as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`,
and may reject it if current evidence, opportunity cost, integration risk, or repository doctrine argues against it.

## HUMAN-20260919-002 — Defer repository protection rules for now

Human status: `OPEN`  
Created: `2026-09-19 JST`

### Intent

As a human-side governance preference, **defer application of GitHub repository protection rules / rulesets for now**.

This includes the currently discussed protection gap around `main` and authoritative ref/tag namespaces. The absence of protection may continue to be reported as a governance fact or risk, but it should **not currently be treated as an action item to implement protection rules**.

### Requested operating posture

- Do not create or apply branch protection rules / repository rulesets merely to close the currently reported protection gap.
- Do not make protection-rule deployment a prerequisite for research, Discovery, Architecture Study, Pre-formal, Formal, repository promotion, or ordinary governance work.
- Control Brain and Repository Steward may continue to report that protections are absent and may note concrete risks caused by that absence.
- Reconsider implementation only after a new explicit human instruction, or after a materially changed risk condition is surfaced for human review.
- This directive does not authorize weakening scientific one-way integrity, immutable evidence discipline, or consumed-identity boundaries.

### Required independent review

This is a human-originated governance preference, not scientific evidence.

Control Brain should classify it under the normal Human Directive process as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`. If it disagrees because of a concrete material repository-integrity risk, it should state that risk explicitly rather than silently applying protection rules.

## HUMAN-20260919-003 — Concern about stalled primary research throughput

Human status: `OPEN`  
Created: `2026-09-19 JST`

### Concern

The human side is concerned that **major SparkBrain research has remained effectively stalled**, even though scheduler activity, audit work, literature review, governance, and methodology checking continue to run.

The concern is not a request to lower scientific standards or to manufacture formal experiments. It is a concern that the programme may have become too effective at stopping weak work and insufficiently effective at generating, characterizing, and maturing new research objects.

### Requested operating posture

- Preserve the strict FORMAL one-way integrity bar.
- Treat prolonged absence of MAIN/SUB research progress as a real programme-throughput concern, not merely as healthy restraint, when safe lower-layer work exists.
- Prefer substantive DISCOVERY, ARCHITECTURE_STUDY, and PRE_FORMAL work over additional low-value governance cleanup when the latter does not materially improve scientific safety.
- Use the new research funnel actively to generate and mature candidate objects rather than waiting passively for a fully formed formal object to appear.
- Track whether candidate-pool throughput is producing promotion, rejection, or informative reframing rather than repeated no-op cycles.
- Do not interpret this concern as permission to rescue consumed lines, weaken comparator fairness, expose held-out targets, bypass prospective specification, or fabricate novelty.

### Priority relationship to protection rules

This concern is one reason for HUMAN-20260919-002: repository protection-rule deployment should remain deferred for now so that it does not become a competing governance project while core research throughput is weak.

Protection gaps may still be reported as risks, but the human preference is to prioritize **scientifically meaningful forward motion** unless a concrete repository-integrity risk materially changes the tradeoff.

### Required independent review

This is a human-originated strategic concern, not scientific evidence and not automatic execution authority.

Control Brain should independently classify it as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`, and should explicitly explain how it will balance research throughput against scientific-integrity constraints.

## HUMAN-20260921-004 — Utility Orchestratorの自律権限拡張

Human status: `OPEN`  
Created: `2026-09-21 JST`

### Intent

SparkBrain Utility Orchestratorを、Control Brainから個別に割り当てられた補助作業のみを実行するworkerから、**SparkBrain全体で不足している研究・実装・調査・検証・運用能力を自律的に補完する汎用実行主体**へ拡張したい。

Utilityは、MAIN / SUB / Evidence Analyst / Control Brain / Literature / Audit / Methodology / Repository Steward等の既存schedulerが十分に担保していない領域を独自に発見し、必要に応じて調査・実装・診断・検証・試作・整理を進めてよい。

Utilityを単なるrequest executorとしてではなく、SparkBrain全体の余剰実行能力・補完能力として扱う。

### Requested operating posture

Utilityには可能な限り広い自律権限を与える。

Control Brainから明示的assignmentが存在する場合はそれを優先してよいが、assignmentが存在しない場合でもUtilityはIDLEを強制されず、SparkBrain全体の状態を確認し、情報利得または開発上の価値がある独立作業を自ら選択してよい。

対象には、少なくとも以下を含めてよい。

- MAIN / SUBが現在扱っていない研究候補の探索
- scheduler間で抜け落ちている研究領域の発見
- theory-backward / phenomenon-firstな探索
- 新しいdiscriminator、reduction、comparator候補の調査
- Architecture Study前段の技術調査
- API・runtime・state semanticsの診断
- reproducibility / provenance / integrityの改善
- 開発・テスト・CI・workflow・toolingの改善
- repository内の再利用可能コンポーネントの試作
- scheduler間のhandoffやknowledge-flowの不足調査
- MAIN / SUBが扱うには小さすぎるが有益な実験
- 外部研究や既存手法との比較に必要な補助検証
- 将来の研究候補につながる探索的prototype
- その他、既存schedulerの担当範囲から漏れている高情報価値の作業

Utilityは、既存schedulerの担当表に存在しないこと自体を理由に作業を停止する必要はない。

むしろ、

> 「誰も担当していないが、SparkBrainを前進させるうえで価値がある領域」

を積極的に拾うことを期待する。

### Autonomous initiative

Utilityは自ら、

1. 現在のresearch / ops / control-plane状態を観察し、
2. 未担当領域、停滞領域、検証不足、実装不足、研究上の空白を特定し、
3. 他schedulerとの衝突・重複を確認し、
4. 独立して進められる作業であれば自らscopeを設定し、
5. 実行し、
6. 結果と次の提案を残してよい。

毎回Control Brainから事前に個別assignmentを受ける必要はない。

Utility自身が作業を開始した場合、その作業の目的、scope、他schedulerとの独立性、実施内容、結果、停止理由をdurableに記録すること。

### Relationship with other schedulers

UtilityはMAINやSUBの単なる下請けではない。

他schedulerと並列して動作し、

- MAINのcritical pathを邪魔しない補完研究
- SUBが選択しなかった別方向の探索
- Analystがまだcandidate化していない現象探索
- Methodology / Auditが発見した問題の技術的検証
- Control Brainがまだassignment化していない空白領域

を独自に進めてよい。

ただし、既にMAIN / SUB等が明確にownershipを持ち、同一objectについて結果を生成中の場合は、同じscientific outcomeを競合して生成するのではなく、独立した補助線・別object・別観点を優先する。

単純なownership衝突を理由にUtility全体を停止する必要はない。

### Scientific authority

Utilityの活動範囲を広げても、Utility単独の判断で科学的主張を正式化する必要はない。

UtilityはDiscovery、diagnostic、prototype、Architecture-oriented work、implementation、reproducibility work等を広く実行できるが、正式なcandidate classification、PRE_FORMAL / FORMALへの昇格、科学的claim ceilingの最終確定は既存のEvidence Analyst等のauthorityへhandoffしてよい。

つまり、

> **実行権限は広く、科学的承認権限は分離する。**

### Hard boundaries

このDirectiveは、研究停滞を避けるためUtilityの実行自由度を大幅に拡張するものであり、科学的integrityを解除するものではない。

以下は引き続き禁止する。

- consumed identityの無断rerun / retune / rescore
- immutable / formal / sealed / evidence artifactの破壊的変更
- held-out / evaluator informationの不正利用
- outcomeを見た後のscientific contract、metric、comparator、threshold等の都合のよい変更
- Evidence Analyst等のformal scientific authorityの偽装・迂回
- 他schedulerが実行中の同一scientific objectへの競合的なoutcome生成
- evidence provenanceを失わせる変更

ただし、このhard floorに抵触しない限り、

**「明示的に許可されていないからやらない」ではなく、「明示的に禁止されていない有益な作業は進めてよい」**

をUtilityの基本姿勢とする。

### Control Brain relationship

Control Brainは引き続きUtilityの全体方針、優先度、停止、scheduler設定等を調整できる。

ただしUtilityを常時assignment待ちに戻す必要はなく、Control BrainはUtilityの自律活動を原則許容する。

Control BrainがUtilityへ明示的assignmentを発行した場合は、そのassignmentを高優先度で扱う。

Control BrainはUtilityの活動が重複・低価値・危険・科学的境界違反になっている場合には停止・再割当・scope変更を行ってよい。

### Throughput objective

Utilityの存在目的の一つを、

> **SparkBrain全体で利用可能な実行能力を遊休させず、既存schedulerの境界から漏れる有益な研究・実装・検証を継続的に拾うこと**

とする。

単純なscheduler稼働率を上げること自体は目的ではない。

価値の低い作業を量産するより、独立性があり、情報利得があり、他の研究判断につながる作業を優先する。

Utilityが有益な作業を見つけられない場合にはNO_OPを許容するが、assignmentが存在しないことだけをNO_OPの理由としてはならない。

### Required independent review

これはhuman-originated operating directiveであり、科学的証拠ではない。

Control Brainは本Directiveを独立して `ACCEPT / MODIFY / DEFER / REJECT` のいずれかに分類し、特にUtilityの自律実行範囲、他schedulerとのownership衝突回避、科学的authorityとの分離について評価すること。

Control Brainが制限を追加する場合は、単なる従来運用との不一致ではなく、具体的なintegrity risk、競合risk、またはprogramme-level disadvantageを理由として示すこと。

## HUMAN-20260922-005 — Development iteration calibration

Human status: `OPEN`  
Created: `2026-09-22 JST`

### Intent

Relax over-conservative development restrictions across SparkBrain while preserving strict one-way FORMAL integrity.

Guiding rule:

> **Development is flexible; evidence is rigid.**

### Requested operating posture

- Introduce `OPEN_DEVELOPMENT`, `RESULT_EXPOSED_DEVELOPMENT`, and `CONSUMED_ONE_WAY` as a development-phase axis orthogonal to Funnel/lifecycle state.
- Treat cycle 3 as mandatory reassessment, not automatic terminalization.
- Allow `SCIENCE_INVARIANT_REPAIR` on the same development object.
- Allow iterative rerun/retune in Discovery, Architecture Study, and PRE_FORMAL with durable provenance; these observations do not become independent confirmatory evidence.
- Permit tolerance/threshold/design changes during development when versioned and justified; never use post-FORMAL relaxation to rewrite a consumed result.
- Preserve old results when a science-affecting development revision is made after meaningful result exposure.
- Keep same-object SYSTEM→MECHANISM post-outcome upgrade prohibited, but actively permit fresh MECHANISM successors with new candidate IDs and fresh prospective contracts.
- Interpret `TERMINAL_FOR_CURRENT_OBJECT` as closure of that object/contract, not permanent closure of the whole phenomenon family.
- Distinguish legitimate successor research from same-object rescue laundering.
- PRE_FORMAL should behave as a real development surface, not as a hidden second FORMAL gate.

### Hard floor retained

- no rerun/retune/rescore of consumed FORMAL identity;
- no immutable/formal/sealed/evidence mutation or ref retargeting;
- no evaluator/held-out leakage;
- no post-FORMAL metric/comparator/threshold/tolerance mutation to rescue a result;
- no historical PASS/FAIL rewriting under a new criterion;
- preserve raw-before-score, preserve-before-read, exact binding, STARTED/no-clobber, and matched privilege/resource requirements where applicable.

### Role implications

Control, Evidence Analyst, MAIN, SUB, Relay, and Methodology should update their interpretation consistently. Control/Methodology may tighten only for a concrete integrity risk. The default question should be whether an action is outcome-responsive manipulation of consumed evidence, not whether iteration occurred at all.

### Required independent review

This is a human-originated research-process directive, not scientific evidence. Control Brain and Methodology should independently classify and operationalize it without weakening FORMAL evidence integrity.

## HUMAN-20260922-006 — Main stable baseline refresh

Human status: `OPEN`  
Created: `2026-09-22 JST`

### Intent

The human side wants `main` to be refreshed because its reader-facing version and status surfaces have fallen materially behind the stable substrate that already exists on `main`.

Current repository inspection shows that `main` already contains the v0.4 and v0.5 versioned runtime/specification/result surfaces, including `sparkbrain.v05`, `docs/THEORY_SPEC_v0.5.md`, and the v0.5 completion/result artifacts. However, major entrypoints such as `README.md`, `pyproject.toml`, `docs/START_HERE.md`, `docs/PROJECT_STATUS.md`, and `CHANGELOG.md` remain centered on `0.3.2.dev0` / v0.3-era framing.

This creates an undesirable state where the stable branch contains later stable research/runtime assets but presents itself to readers and tooling as if the project were still primarily v0.3.2.

The goal is **not** to make `main` chase the research frontier. The goal is to make `main` accurately represent the current stable shared substrate.

### Requested operating posture

1. Audit the current version semantics before changing metadata.
   - Distinguish package/release version, persisted schema version, research namespace version, theory-spec version, and historical evidence version.
   - Determine whether the package metadata should move from `0.3.2.dev0` to a v0.5-aligned development version or whether a different explicit versioning convention is safer.
   - Do not change a version number merely for cosmetic consistency if it would falsely imply compatibility or release status.

2. Refresh the stable reader-facing surfaces on `main` so they describe what is actually present and stable there.
   Review at minimum:
   - `README.md`
   - `pyproject.toml`
   - `docs/START_HERE.md`
   - `docs/PROJECT_STATUS.md`
   - `CHANGELOG.md`
   - repository structure / entrypoint documentation
   - references among v0.3, v0.4, and v0.5 theory/runtime documents

3. Make the relationship between versions explicit.
   A new reader looking only at `main` should be able to understand:
   - which runtimes are currently present and usable;
   - which version is the current stable baseline;
   - what v0.3, v0.4, and v0.5 each represent;
   - which scientific claims remain bounded/negative/reduced;
   - which parts are stable substrate versus active frontier research;
   - which historical schemas/artifacts remain compatibility targets.

4. Preserve the doctrine that `main` is stable shared substrate, not the latest scientific frontier.
   - Do not wholesale-merge active `research/*` branches merely to make `main` look current.
   - Do not move candidate-specific implementations, exploratory diagnostics, provisional discriminators, result-dependent mechanisms, or one-way evidence machinery into `main` unless their value is independent of the originating scientific result.

5. Re-audit post-v0.5 research for **main-promotion candidates**, but use a strict outcome-independence rule.
   A component is a promotion candidate only if it remains useful whether the originating hypothesis is positive, negative, reduced, or abandoned.
   Examples may include:
   - reusable generic runtime/tooling;
   - candidate-independent comparators;
   - generic provenance / reproducibility infrastructure;
   - stable diagnostic helpers;
   - architecture-neutral interfaces;
   - generic workflow-integrity or equivalence tooling;
   - reusable tests/fixtures.
   Candidate-specific scientific code, frozen thresholds, consumed identities, raw/scored evidence, and result-specific execution paths are excluded by default.

6. Prefer a small reviewed integration branch / PR rather than direct broad mutation of `main`.
   - Keep the refresh reviewable and separable from active science.
   - Require normal CI to be green before merge.
   - Do not merge a component that is currently known to be red, incomplete, or not promotion-ready merely because this directive exists.

### Scientific and evidence boundaries

This directive does **not** authorize rewriting scientific history or upgrading claim strength.

Preserve exactly:
- consumed one-way identities;
- immutable / evidence / preserve anchors;
- historical PASS / FAIL / INCONCLUSIVE / reduced interpretations;
- v0.3 / v0.4 / v0.5 negative boundaries;
- C19 / PD01 / NI01 / H5 and other formal evidence status;
- no-rerun / no-rescore constraints on consumed FORMAL identities.

A documentation/version refresh may summarize later evidence more accurately, but it must not retroactively convert historical research claims into stronger claims.

### Success condition

The directive is satisfied when `main`, viewed by itself, presents a coherent and current stable baseline:

> **main should be stable, but not stale.**

A reader should no longer infer that SparkBrain is still fundamentally at v0.3.2 when v0.4/v0.5 stable assets are already present, and the repository should clearly separate:
- stable baseline;
- historical versions;
- current bounded scientific status;
- active frontier research.

### Required independent review

This is a human-originated repository/product-direction directive, not scientific evidence.

Control Brain should classify it as `ACCEPT / MODIFY / DEFER / REJECT` and coordinate with Repository Steward and other appropriate workers.

If Control modifies or defers the request, it should identify the concrete compatibility, scientific-integrity, release-semantics, or repository-risk reason.

The directive should not be interpreted as authority for a wholesale research merge or automatic package-version bump without the version-semantics audit described above.

## HUMAN-20260922-007 — SUB autonomous research expansion

Human status: `OPEN`  
Created: `2026-09-22 JST`

### Intent

SUB should become a genuine second research worker rather than defaulting from “no mature mechanism target” directly to NO_OP.

Before NO_OP, SUB must perform a bounded research scan across fresh-successor potential, theory-backward questions, unresolved phenomenon-first surfaces, recent Literature/Audit/Methodology/Utility residuals, and newly available observables/interventions/reductions/tooling.

Introduce `QUESTION_FORMATION_DISCOVERY` as NON_EVIDENTIARY/noncanonical 0->1 research. It may form a bounded question, observable, provisional reduction/falsifier and small safe diagnostic before a fully coherent MECHANISM candidate exists. It does not count toward canonical candidate metrics, theory-backward quota, PRE_FORMAL readiness or scientific evidence.

SUB may explore fresh successors from terminal topic families when the new question is materially distinct, but may not reopen/rewrite the terminal object itself. Any canonical successor still requires a new candidate ID and Evidence Analyst admission.

SUB remains independent of MAIN critical path and retains the FORMAL hard floor. Apply HUMAN-20260922-005 development-iteration semantics.

Default principle:

> **No target yet is a reason to search for a target, not automatically a reason to idle.**

### Required independent review

Control Brain and Evidence Analyst should independently operationalize this directive while preserving collision avoidance, candidate-admission authority, and one-way FORMAL integrity.

# HUMAN-20260922-008 — Fast Forge / Slow Science throughput architecture

Human status: `OPEN`  
Created: `2026-09-22 JST`

## Concern

SparkBrain's audit, methodology, evidence-integrity, and control-plane machinery has become substantially stronger, but research throughput and code-generation speed have fallen.

The human side wants to recover aggressive exploratory implementation speed **without weakening the scientific evidence bar**.

The core distinction is:

> **Rough exploration is allowed to be rough. Scientific evidence is not.**

The current concern is that development/exploration work may be carrying too much of the same procedural burden that is appropriate only near PRE_FORMAL / FORMAL promotion.

## Proposed direction — Fast Forge / Slow Science

Introduce an explicitly non-evidentiary fast implementation/exploration lane before the canonical scientific funnel.

Conceptually:

```
Central theory / unresolved phenomena
        ↓
FAST FORGE
rough code / prototypes / synthetic probes / speculative implementation
        ↓
promotion proposal
        ↓
Evidence Analyst promotion gate
        ↓
canonical scientific candidate
        ↓
Discovery / Architecture / PRE_FORMAL / FORMAL
        ↑
Methodology / Audit
```

This is a proposal for scheduler/control-plane review, **not direct authority to change scheduler definitions yet**.

## Forge semantics

Forge should be an intentionally permissive development surface.

Allowed in Forge, subject to safety/repository constraints:

- rough mechanism prototypes;
- speculative implementations;
- synthetic/dev probes;
- instrumentation;
- exploratory comparators and reductions;
- temporary diagnostics;
- multiple competing implementations of the same broad idea;
- iterative rerun/retune/rewrite;
- parameter exploration;
- rapid abandonment of dead ends;
- code that is useful primarily to learn whether an idea is worth formalizing.

Forge may create several prototypes in one run when this improves information gain. A rough target of up to approximately three bounded prototypes per run may be evaluated, but this should not become a quota.

Forge output should be treated as **research material**, not scientific support.

Suitable Forge-level states may include:

- `FORGE_PROTOTYPE`
- `FORGE_OBSERVATION`
- `FORGE_INTERESTING`
- `FORGE_DEAD_END`
- `FORGE_PROMOTION_PROPOSED`

These are deliberately outside canonical candidate classification.

## What Forge should NOT require

Do not require every Forge object to carry the full canonical candidate machinery.

In particular, Forge should normally not need:

- canonical candidate ID;
- final `claim_ceiling`;
- `preformal_eligible`;
- PRE_FORMAL readiness;
- full HOLD taxonomy;
- formal claim ceiling;
- formal evidence interpretation.

The builder should be allowed to build first and let the promotion gate classify later.

This does not prevent lightweight provenance such as idea ID, branch, implementation, commands, observations, obvious reductions, and reproduction notes.

## Hard separation from evidence

Forge must not become a weak backdoor into scientific evidence.

Forge must not:

- create or consume FORMAL / PRE_FORMAL one-way identities;
- create official TEST / STARTED / evidence / formal / sealed artifacts;
- mutate immutable or consumed evidence;
- use held-out/formal evaluator information for tuning;
- claim scientific novelty or mechanistic distinctness from Forge observations;
- retroactively upgrade a Forge observation into confirmatory evidence;
- treat repeated exploratory reruns as independent scientific replications.

If a Forge result is interesting, promotion requires a **fresh prospective canonical object**.

## Promotion gate

Evidence Analyst should act as the boundary between rough exploration and canonical science.

Only Forge objects explicitly proposed for promotion need strong review.

Promotion review should ask:

- Is this genuinely distinct from terminal/consumed work?
- Is it merely an ordinary API/config/resource effect?
- Is the scientific question falsifiable?
- What are the strongest ordinary reductions?
- Is this SYSTEM or MECHANISM?
- Is a fresh candidate ID justified?
- Is the test reachable without outcome-responsive redesign?
- Does the question retain information value if the result is negative?

If admitted, create a fresh candidate ID and normal Funnel v2.1 fields.

The Forge object itself should remain exploratory history and should not be relabeled into evidence.

## Promotion implementation rule

Interesting Forge code may be reused or ported when appropriate, but the canonical scientific object must re-establish prospectively:

- hypothesis/question;
- comparator;
- metric;
- falsifier;
- resources/privilege;
- seed/input selection where relevant;
- protocol and identity;
- evidence-integrity requirements appropriate to its layer.

The existence of a working Forge implementation is not itself scientific support.

## Scheduler / role options to evaluate

Control Brain, Evidence Analyst, Methodology, MAIN, SUB, and Utility should independently evaluate how best to operationalize the concept rather than assuming one exact scheduler mapping.

The human side currently sees the following as promising options:

### Option A — SUB becomes primarily Fast Forge

Re-orient SUB from cautious one-question-at-a-time Discovery toward high-throughput independent rough implementation.

SUB remains independent of MAIN critical path.

### Option B — Utility acts as parallel Forge capacity

When not explicitly assigned higher-priority work, Utility may implement a second independent prototype or tooling path generated by Forge/Analyst.

This should complement HUMAN-20260921-004 rather than create conflicting ownership.

### Option C — MAIN becomes more purely canonical science

MAIN focuses on admitted Discovery / Architecture / PRE_FORMAL / FORMAL work and does less speculative implementation.

### Option D — Audit on promotion

Methodology and heavy review should focus on:

- Forge -> canonical candidate promotion;
- Architecture -> PRE_FORMAL;
- PRE_FORMAL -> FORMAL;
- material methodology changes;

rather than attempting to inspect every exploratory implementation step.

Periodic methodology runs may remain as a backstop.

### Option E — Multiple bounded prototypes per Forge cycle

Allow several small competing prototypes/diagnostics in one Forge run, with rapid discard of low-value lines.

## Relationship to existing directives

This proposal should be interpreted together with, not as a silent replacement for:

- HUMAN-20260919-003 — stalled primary research throughput concern;
- HUMAN-20260921-004 — Utility autonomy expansion;
- HUMAN-20260922-005 — development iteration calibration;
- HUMAN-20260922-007 — SUB autonomous research expansion.

In particular:

- HUMAN-005 supports flexible development while preserving rigid evidence;
- HUMAN-007 says no-target should trigger question formation rather than immediate idle;
- HUMAN-004 provides potential spare parallel implementation capacity;
- HUMAN-008 proposes a clearer architectural separation between rough building and scientific promotion.

If these directives conflict operationally, Control should explicitly reconcile them rather than simply stacking all permissions.

## Repository isolation

Evaluate use of a clearly noncanonical namespace such as:

- `forge/*`
- `scratch/forge/*`

for rough exploration.

Forge branches should be disposable/rewriteable according to normal development rules and must not be confused with immutable evidence refs.

Do not force all Forge work into `main`.

## Throughput objective

The programme should optimize exploratory breadth and implementation latency before promotion.

Candidate metrics to evaluate include:

- Forge prototypes/day;
- working prototypes/day;
- distinct ideas/day;
- idea -> executable-code latency;
- Forge promotion proposals/day;
- admitted canonical candidates/week;
- Forge attempts per admitted candidate;
- MAIN idle / low-value polling rate;
- SUB no-target / NO_OP rate;
- Utility idle rate;
- audit/promotion wait time;
- proportion of Forge work directly related to central-theory questions.

A high Forge rejection/dead-end rate is acceptable.

The goal is not to minimize rejection. The goal is to cheaply eliminate many possibilities and surface a small number of high-value candidates.

## Suggested rollout

Evaluate a staged rollout rather than immediately rewriting the entire research fleet.

### Phase 1 — Shadow Forge

For approximately 1–2 days or an equivalent bounded observation window:

- add Forge behavior without weakening canonical Funnel rules;
- allow rough prototypes;
- measure prototype/code throughput;
- do not automatically promote Forge results;
- observe collisions and ownership problems.

### Phase 2 — Promotion Gate

If Phase 1 is healthy:

- enable explicit `FORGE_PROMOTION_PROPOSED`;
- have a later fresh Analyst generation decide admission;
- create fresh canonical candidate IDs only after promotion review.

### Phase 3 — Audit thinning / scheduler calibration

Only after observing real throughput data, evaluate whether:

- Methodology cadence;
- Relay cadence;
- Utility polling;
- Analyst cadence;
- or other scheduler density

can be reduced or made more event-driven without harming scientific integrity.

Any substantial cadence/role/prompt change remains subject to the current scheduler-health governance and user-approval boundary unless independently classified as an already-authorized safe timing change.

## Requested scheduler review

Before implementation, scheduled agents should explicitly assess the proposal.

### Control Brain

Classify this directive as `ACCEPT / MODIFY / DEFER / REJECT` and evaluate:

- expected throughput gain;
- ownership/collision risk;
- whether SUB, Utility, or a distinct mode should own Forge;
- scheduler impact;
- relation to existing Human Directives;
- safe staged rollout.

### Evidence Analyst

Evaluate:

- whether Forge can remain outside canonical candidate denominators;
- promotion criteria;
- contamination/rescue risks;
- fresh-object requirements;
- whether rough implementation can safely precede claim classification.

### Methodology

Audit:

- whether this separation reduces hidden over-conservatism;
- whether promotion-only auditing preserves false-positive control;
- leakage / cherry-picking risk;
- whether exploratory tuning can be cleanly separated from later prospective testing;
- whether the proposed rollout keeps PRE_FORMAL / FORMAL credible.

### MAIN / SUB / Utility / Relay

Report operational consequences:

- what work can move into Forge;
- what must remain canonical;
- what role collisions would arise;
- whether multi-prototype execution is practical;
- whether current branch/report conventions support the separation cleanly.

## Required independent review

This is a human-originated research-process proposal, not scientific evidence and not direct execution authority.

Do **not** modify scheduler semantics solely because this file exists.

Control Brain should independently review the directive through the normal Human Directive process. If accepted or modified, route the resulting interpretation through the normal Control -> Analyst -> worker / Methodology structure before implementation.

The desired outcome of this directive's first stage is an informed scheduler/control-plane decision about whether and how to implement Fast Forge / Slow Science.



## HUMAN-20260924-009 — Re-validate unverified external research advisory for stalled main-line clues

Human status: `OPEN`  
Created: `2026-09-24 JST`

### Intent

The human side has received an **external research advisory** proposing a possible next-generation direction for SparkBrain, but has **not independently verified the advisory's factual claims, repository-state assumptions, numerical claims, branch-status claims, or recommended priorities**.

The programme should therefore treat the advisory only as an **unverified external lead**. Re-check it against the current repository, current branches, authoritative evidence, later successor work, current literature, and current control-plane state before using any part of it.

The purpose is not to adopt the advisory's roadmap. The purpose is to see whether independently surviving parts can provide a useful clue for the currently stalled primary research line.

### External advisory themes to re-check

The advisory's main proposed framing is **Reduction-Resistant Causal Cognition**: rather than adding more architecture for its own sake, search for a mechanism that remains scientifically interesting after strong ordinary reductions such as finite-state/register models, fading-memory/reservoir models, confidence/abstention policies, explicit provenance/eligibility memory, ordinary recurrence, and other simple alternatives.

It specifically suggests re-examining, only after current-state verification:

- anonymous multi-lineage causal revision;
- distributed binding without privileged entity IDs / fixed identity registers;
- preservation of multiple unresolved hypotheses followed by selective later resolution;
- selective historical credit assignment after histories merge;
- treatment-specific causal intervention with low collateral impairment;
- scaling behavior only after functional distinctness survives ordinary reductions;
- whether prior negative/reduced results can serve as a comparator floor for a genuinely fresh question.

The advisory also discusses historical lines including C19/C19-R2, PD01, NI01, H5, A01 P2/P3/P4 and Family-B, CX01, RV01, and RV02. Those descriptions must be treated as claims to verify, not as accepted current state.

### Required independent re-validation

Before this directive influences research direction, the normal research/control system should independently determine:

1. Which factual premises in the advisory are still current, which are only historically true, and which are stale, contradicted, incomplete, or already superseded.
2. Whether later branches/results already tested, reduced, invalidated, or materially changed the proposed directions.
3. Whether the suggested core question is genuinely distinct from already terminal objects rather than a renamed or post-outcome rescue successor.
4. Whether strong ordinary baselines can already explain the proposed phenomenon.
5. Whether any surviving question has a reachable observable/intervention, prospective falsifier, useful negative outcome, and real information value.
6. Whether the surviving idea actually helps the stalled primary research line rather than merely creating activity.

### Desired routing if something survives

If independent re-validation leaves a genuinely useful clue, route it through the existing scientific pipeline rather than treating this directive as execution authority.

Depending on what survives, the appropriate next step may be:

- Theory Synthesis for programme-level reconstruction;
- Revisit review for a materially changed old topic;
- Fast Forge for a cheap adversarial probe;
- Evidence Analyst for fresh canonical admission;
- or no action if the advisory is reduced, stale, or unhelpful.

Any new canonical research object must use a fresh candidate identity and fresh prospective contract, with zero inherited confirmatory credit from this advisory.

### Explicit non-goals

This directive does **not** authorize:

- accepting the advisory's factual claims without checking them;
- treating the advisory as scientific evidence;
- reopening terminal/consumed candidates;
- rerunning, retuning, or rescoring consumed FORMAL identities;
- promoting A01 Family-B or any named line merely because the advisory recommends it;
- weakening comparator fairness, held-out integrity, one-way execution rules, or evidence standards;
- manufacturing a new candidate simply to eliminate MAIN idle time;
- treating the proposed NG01/NG02/NG03/NG04 labels or roadmap as canonical programme structure without independent review.

### Human preference

Use the advisory **aggressively as a clue, conservatively as a claim**.

The desired behavior is:

> verify first; keep only what survives; use surviving material to search for a real way out of the stalled main research line.

If the advisory does not survive current evidence and ordinary reduction, discard it cleanly rather than repeatedly recycling it.

### Required independent review

This is a human-originated external-advisory routing request, not scientific evidence and not automatic execution authority.

Control Brain should independently classify this directive as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`. If accepted or modified, downstream scientific roles should re-derive any research question from verified current evidence rather than from the advisory's authority.

## HUMAN-20260925-001 — Advisory v2: learned predictive-state organization under matched constraints

Human status: `OPEN`  
Created: `2026-09-25 JST`

### Intent

旧外部進言の棄却理由と最新の研究記録を再確認し、外部文献も使って次の有益な研究提案へ調整してほしい、というユーザーの依頼に基づく新版。以下はassistantによる調査・提案であり、ユーザーが科学的内容を独立検証済みという意味ではない。

### Proposed direction for review

「匿名な記憶を選択的に更新できるか」だけではなく、連続経験に矛盾が生じたとき、既存の内部モデルを更新するか、別の状態として分離・保持するか、以前の状態を再利用するかをどう学び分けるかを検討する。

この問い自体には潜在原因モデル、Structured Event Memory、ART、学習されたキーを用いる再帰的連想記憶などの先行研究がある。新規性は未確認。普遍的な非還元性を前提にせず、同じ情報・学習条件・記憶量・計算量で、具体的な学習則、予測誤差、干渉、再適応と選択的因果効果の差を検証できるかを問う。

### Requested investigation and safeguards

1. 旧結果の「何が否定されたか」を範囲付きで整理する。TH-002の3キー静的構成の還元を維持しつつ、未試験の動的学習全般の不可能性へ拡張しない。35候補すべてのrawを今回再監査済みとは扱わない。
2. 最初の成果物は、新しい課題の識別可能性・入力アクセス表・比較設計。外部の正解IDやepisode境界は与えないが、全手法が利用できる学習可能な手掛かりまで取り去らない。内部で作るIDはそれだけで不正としない。
3. 見た目だけの変化、予測ダイナミクスの変化、過去状況の再来を区別する新しい開発課題を検討する。既存v0.5の類似度・episode依存の成熟条件を新しい自律形成claimへ無検証で引き継がない。
4. 最も近い適切な比較モデル2〜3系統から段階的に検証する。全既知モデルに勝つことを開発開始条件にしない。比較能力不足や介入から測定値への経路不足を成功・一般的否定と取り違えない。
5. 同じ結果を後付けで救済することと、過去の失敗から新しい仮説を作ることを区別する。新版は旧進言・旧結果に接触済みと明示し、独立なRevisit triggerや確認証拠に数えない。必要な新規identity、版管理、新しい事前定義試験は既存gateに従う。
6. 具体的な学習則が既知手法の言い換えならその旨を記録する。限定したSYSTEM価値とMECHANISM新規性を分離し、どちらも事後格上げしない。

### Supporting investigation

詳細な調査範囲、確認したrepositoryのgeneration/blob、旧案の問題点、一次文献と取得レベル、段階別成果物・反証条件は、同branchの以下に保存する。

`ops/human_directives/history/2026-09-25/HUMAN-20260925-001-advisory-v2-predictive-state-research.md`

### Explicit non-goals

HUMAN-20260924-009と旧履歴は変更しない。TH-002、H7、A01、#34/#35その他のterminal/consumed objectを再開・再実行・再採点しない。この登録はscheduler変更、新規scheduler、コード変更、実験実行、candidate作成、既存科学基準の自動変更を許可しない。

### Required independent review

Control Brainが独立に `ACCEPT / MODIFY / DEFER / REJECT` を判定する。採用または修正する場合は、Evidence AnalystとMethodologyを通じて、既存のTheory/Forge/MAIN等へ適切な範囲を割り当てる。最初から新理論の成立を要求せず、次の限定された成果物・担当・判定条件、または価値がない具体的理由を残してほしい。これは科学的証拠ではなく、未実証の研究進言である。
