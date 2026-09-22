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
