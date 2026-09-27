# HUMAN-20260928-002 — Fly-inspired Sensorimotor Integration Track

Human status: `OPEN`  
Created: `2026-09-28 JST`  
Priority: `HIGH / PARALLEL SYSTEM INTEGRATION TRACK`

## Intent

SparkBrainへ、ショウジョウバエ等の昆虫神経系から着想した **fly-like sensorimotor track** を導入する方向を検討・開発する。

目的は「ハエ脳をそのまま再現した」と主張することではない。局所的・疎・再帰的・event-drivenな感覚運動回路、興奮/抑制、delay、fast local loop、上位状態からのdescending modulationといった構造原理を、SparkBrainの継続的な外界相互作用へ接続できるかを検証する。

本trackは、既存A01 / RV02等のmechanism-discrimination objectへ直接ねじ込むのではなく、まず非証拠的なForge / SYSTEM_BUILD integration lineとして扱うことを希望する。

## Current placement request

現時点の推奨配置は以下とする。

`Fast Forge bounded prototype`
→ `Evidence Analyst review/allocation`
→ `SYSTEM_BUILD fly-like sensorimotor pilot`
→ 必要な場合のみ `fresh prospective scientific successor`

SYSTEM_BUILDへ昇格する場合のbuild IDは、例として

`BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT`

を候補とする。ただし、番号・名称・正確な統合順序は、現在のbuild ledger、collision、priorityを再確認したEvidence Analyst / Control Brainが変更してよい。

このtrackの導入自体を、既存科学候補のreopen、科学的claim upgrade、Fly connectomeの生物学的忠実性証明として扱わない。

## Stage FLY-0 — bounded Forge topology probe

最初からFlyWire全脳・全CNS規模をcanonical runtimeへ投入しない。

まず、現在のSparkBrainで安全に比較できる縮約fly-like topologyを小規模に構成する。規模は事前にboundedとし、数百〜約1000 unit程度を一つの目安としてよいが、これは固定の科学条件ではなく、計算資源と比較公平性に応じてprospectiveに決める。

最低限の構造要素として以下を検討する。

- event-like sensory input;
- sparse recurrent connectivity;
- excitatory / inhibitory interaction;
- propagation delay;
- local fast sensorimotor loops;
- bounded motor output;
- high-level descending modulation interface;
- inspectable internal activity / trace.

初期比較は、可能な限り少なくとも以下を同一resource envelopeで比較する。

1. fly-like structured topology;
2. degree-preserving rewired topology;
3. random sparse topology.

比較時は、unit数、edge数、input/output surface、可能な範囲のactivity/resource budget、delay budget等を一致または明示的に整合する。

特にdegree-preserving rewiringを入れ、単なる疎性、hub数、edge density等だけで差を説明できないかを切り分ける。

Forgeで得られた結果は `NON_EVIDENTIARY / NONCANONICAL` とし、科学的confirmatory creditを与えない。

## Stage SB003 — closed-loop SYSTEM_BUILD integration

FLY-0がengineering componentとして有用で、現行SYSTEM_BUILD critical pathと整合する場合、fly-like sensorimotor componentを独立したSYSTEM_BUILDとして統合することを検討する。

目標は概ね以下のloopを閉じること。

`WORLD`
→ `event/sensory input`
→ `fly-like local sensorimotor organ`
→ `SparkBrain persistent state / prediction / scope / revision`
→ `high-level modulation`
→ `fly-like local action generation`
→ `ACTION`
→ `WORLD changes`
→ next observation.

SparkBrain上位系は、可能な限りmicro-controlを直接担当せず、`approach / avoid / track / explore / ignore` 等に相当する高位状態・goal・modulationを下位sensorimotor componentへ与える方向を優先する。

低遅延な姿勢・追跡・回避・局所補償のような制御は、fly-like component側で局所的に閉じる設計を検討する。

SB001 predictive-state revision、SB002 causal-scope revision等の既存SYSTEM_BUILDとの接続は、必要なinterfaceだけを使用し、不必要に既存buildの内部を改変しない。

SYSTEM_BUILD acceptanceには少なくとも以下を検討する。

- deterministic bounded synthetic world;
- closed-loop action→world→observation continuity;
- checkpoint / restore / replay;
- trace / internal-state observability;
- failure時のbounded rollback / fail-closed behavior;
- component provenance;
- interaction / connection ablation;
- matched replacement variant where feasible.

この段階も `NON_EVIDENTIARY_BUILD` とし、統合成功からtopology superiority、biological fidelity、novelty、whole-system superiorityを自動的に主張しない。

## Relationship to H9 / C07 fully-spiking line

現時点のH9 / C07 fully-spiking readiness lineは別管理とする。

既存C07はhistorical hybrid objectであり、sensory encoding以外の主要state / evidence / Coalition / ignition / Workspace等を全面的なspike-domain dynamicsとして実装したcanonical fully-spiking backendではない。

したがって、本Directiveを理由としてH9の未確定事項を勝手に埋めたり、historical C07をfully-spiking evidenceへ読み替えたり、旧条件をretune / rerunしてはならない。

fly-like sensorimotor componentは、最初は縮約されたintegration primitiveとして扱い、SparkBrain全体のfully-spiking化とは分離する。

## Whole FlyWire / connectome use

実FlyWire等の大規模connectomeそのものを利用する研究は将来候補として保持するが、初期SB003の必須条件にはしない。

大規模connectome利用へ進む前に、少なくとも以下を再評価する。

- current spiking/runtime substrateのcapacity;
- fully-spiking operational boundary;
- neuron/synapse model;
- representation/decoder mapping;
- resource/tuning budget;
- exact comparator;
- licensing/provenance/data handling;
- whether a reduced motif provides the same engineering value.

大規模connectomeは、縮約motifで得られる情報以上の明確なinformation gainが見込める場合に優先する。

## Build-to-science promotion rule

ForgeまたはSYSTEM_BUILDで、fly-like topologyに由来する可能性のある興味深い差・現象が観測されても、その観測をそのままscientific evidenceへ昇格させない。

科学的問いへ進む場合は、fresh candidateとして、

- new candidate identity;
- prospective protocol;
- matched comparators;
- degree-preserving / random reductions;
- falsifier;
- frozen metrics / thresholds / resources;
- held-out / one-way integrity where applicable;

を新たに定義する。

BUILD / Forge observationからconfirmatory creditを継承しない。

## Relationship to HUMAN-20260928-001

本Directiveは `HUMAN-20260928-001 — Accelerated Integrated SparkBrain Completion` と整合させる。

Integrated Prototype Milestone 1のcritical pathを不必要に遅らせない。

当面、fly-like trackがMilestone 1へ必須でない場合は、Fast Forge等のparallel trackとして先行してよい。既存統合が完成した後にsensorimotor embodimentを追加する方がtotal latencyを下げる場合は、その順序を優先してよい。

逆に、Evidence Analystが「閉ループaction/world interactionがMilestone 1または直後のintegration milestoneに直接必要」と判断した場合は、SYSTEM_BUILD critical pathへ早期昇格してよい。

## Non-goals / scientific hard floor

本Directiveは以下を許可しない。

- 「ハエ脳を再現した」「生物学的等価」とする未証明claim;
- BUILD結果のscientific evidence化;
- A01 / RV02 / H9その他terminal/consumed objectの偽装reopen;
- consumed FORMAL identityのrerun / retune / rescore;
- immutable / frozen / sealed / formal / evidence artifactの改変;
- held-out / evaluator leakage;
- outcomeを見た後のscientific contract変更;
- energy-efficiency claimをactivity countやwall-clockだけから導くこと.

## Requested Control / Analyst handling

Control Brainは本Directiveを `ACCEPT / MODIFY / DEFER / REJECT` で独立評価する。

採用または修正する場合、Evidence Analystは少なくとも以下を判断する。

1. Fast ForgeへFLY-0縮約topology probeを割り当てるか;
2. existing MAIN / SYSTEM_BUILDとcollisionしないか;
3. `BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT`相当のSYSTEM_BUILDをいつ割り当てるか;
4. HUMAN-20260928-001のremaining integration graphへどこで接続するか;
5. H9 / C07とはどのinterfaceだけ共有し、何を分離するか;
6. later scienceへ昇格する場合のfresh prospective discriminatorは何か.

Methodology / Literature / Auditは必要な比較公平性、prior-art、claim boundaryを支援してよいが、NON_EVIDENTIARY Forge / SYSTEM_BUILDの通常engineeringを、具体的integrity issueなしに形式的理由だけで停止させない方向を評価する。

本Directiveはscientific evidenceではなく、SparkBrainへembodied / sensorimotor loopを追加するためのhuman-originated integration/research intentである。
