from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .engine import SparkBrain
from .validation import SCHEMA_VERSION, validate_trace_payload

HTML_TEMPLATE = r'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>SparkBrain Visualizer</title>
<style>
:root {
  color-scheme: dark;
  --bg: #0b1020;
  --panel: #131a2d;
  --panel2: #18213a;
  --text: #eef3ff;
  --muted: #9aa8c7;
  --line: #34415f;
  --hot: #ffd166;
  --ignite: #ff6b6b;
  --sensory: #5bc0eb;
  --hypothesis: #9b5de5;
  --memory: #00d084;
  --action: #ff9f1c;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); font: 14px/1.45 system-ui, sans-serif; }
header { padding: 18px 22px; border-bottom: 1px solid #26324d; display:flex; justify-content:space-between; gap:20px; align-items:center; }
h1 { margin:0; font-size:20px; }
small, .muted { color: var(--muted); }
main { display:grid; grid-template-columns:minmax(660px, 1fr) 360px; min-height:calc(100vh - 72px); }
#stageWrap { position:relative; overflow:auto; border-right:1px solid #26324d; }
#stage { min-width:900px; min-height:650px; width:100%; height:calc(100vh - 148px); }
.controls { height:76px; padding:12px 18px; border-top:1px solid #26324d; display:grid; grid-template-columns:auto auto 1fr auto; gap:12px; align-items:center; }
button { background:#26324d; color:var(--text); border:1px solid #3d4d71; border-radius:8px; padding:8px 13px; cursor:pointer; }
input[type=range] { width:100%; }
aside { padding:16px; overflow:auto; max-height:calc(100vh - 72px); }
.card { background:var(--panel); border:1px solid #26324d; border-radius:12px; padding:13px; margin-bottom:12px; }
.card h2 { font-size:14px; margin:0 0 8px; color:#cbd6ef; }
.big { font-size:26px; font-weight:750; letter-spacing:.02em; }
.badge { display:inline-block; border-radius:999px; padding:3px 8px; background:#25314f; margin:2px; }
table { width:100%; border-collapse:collapse; }
th, td { padding:6px 4px; text-align:left; border-bottom:1px solid #25314f; font-size:12px; }
.node-label { fill:#eaf0ff; font-size:11px; pointer-events:none; }
.organ-label { fill:#8fa0c4; font-size:14px; font-weight:650; }
.edge { stroke:var(--line); stroke-width:1; opacity:.20; }
.edge.inhibitory { stroke:#d06a7b; stroke-dasharray:4 4; }
.edge.active { opacity:.95; stroke-width:3; }
.node { stroke:#dce6ff; stroke-width:1; transition:.15s; }
.node.fired { stroke:var(--hot); stroke-width:5; }
.node.workspace { stroke:var(--ignite); stroke-width:6; }
.legend { display:flex; flex-wrap:wrap; gap:10px; }
.legend span::before { content:""; display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:5px; background:var(--c); }
@media (max-width:1100px) { main { grid-template-columns:1fr; } #stageWrap { border-right:0; } aside { max-height:none; } }
</style>
</head>
<body>
<header>
  <div><h1>SparkBrain Visualizer</h1><small>局所Spark → 競争 → Coalition → Ignition → Workspace</small></div>
  <div class="legend">
    <span style="--c:var(--sensory)">sensory</span>
    <span style="--c:var(--hypothesis)">hypothesis</span>
    <span style="--c:var(--memory)">memory</span>
    <span style="--c:var(--action)">action</span>
  </div>
</header>
<main>
  <section id="stageWrap">
    <svg id="stage" viewBox="0 0 1000 650" preserveAspectRatio="xMidYMid meet"></svg>
    <div class="controls">
      <button id="prev">◀</button>
      <button id="play">再生</button>
      <input id="slider" type="range" min="0" max="0" value="0" step="1" />
      <strong id="frameLabel">0 / 0</strong>
    </div>
  </section>
  <aside>
    <div class="card"><h2>入力イベント</h2><div id="event" class="big">—</div><div id="truth" class="muted"></div></div>
    <div class="card"><h2>現在の有効belief</h2><div id="prediction" class="big">NO IGNITION</div></div>
    <div class="card"><h2>Coalitions</h2><table><thead><tr><th>仮説</th><th>score</th><th>div.</th><th>stable</th></tr></thead><tbody id="coalitions"></tbody></table></div>
    <div class="card"><h2>Global Workspace</h2><div id="workspace" class="muted">empty</div></div>
    <div class="card"><h2>Engine stats</h2><div id="stats"></div></div>
    <div class="card"><h2>読み方</h2><div class="muted">円の大きさと透明度が活動値、黄色い輪が当該フレームでの発火、赤い輪がWorkspaceへ昇格した仮説を示す。破線は抑制性接続。</div></div>
  </aside>
</main>
<script>
const payload = __PAYLOAD__;
const svg = document.getElementById('stage');
const slider = document.getElementById('slider');
const frames = payload.frames;
slider.max = Math.max(0, frames.length - 1);

const organOrder = ['perception','hypothesis','memory','action','workspace'];
const xByOrgan = {perception:120, hypothesis:470, memory:720, action:900, workspace:820};
const colorByKind = {sensory:'#5bc0eb', feature:'#5bc0eb', hypothesis:'#9b5de5', memory:'#00d084', action:'#ff9f1c', goal:'#f4d35e', workspace:'#ff6b6b'};
const grouped = {};
for (const organ of organOrder) grouped[organ] = [];
for (const node of payload.graph.nodes) (grouped[node.organ] ||= []).push(node);

const positions = {};
for (const [organ, nodes] of Object.entries(grouped)) {
  nodes.sort((a,b) => a.label.localeCompare(b.label));
  const n = nodes.length;
  nodes.forEach((node, index) => {
    const y = n <= 1 ? 310 : 70 + index * (500 / Math.max(1,n-1));
    positions[node.id] = {x:xByOrgan[organ] || 500, y};
  });
}
function el(name, attrs={}) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', name);
  for (const [k,v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  return node;
}
for (const organ of organOrder) {
  if (!grouped[organ] || grouped[organ].length === 0) continue;
  const text = el('text',{x:(xByOrgan[organ]||500)-45,y:30,class:'organ-label'});
  text.textContent = organ.toUpperCase(); svg.appendChild(text);
}
const edgeEls = new Map();
payload.graph.edges.forEach((edge,index) => {
  const a=positions[edge.source], b=positions[edge.target]; if(!a||!b) return;
  const line=el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'edge'+(edge.weight<0?' inhibitory':'')});
  line.dataset.key=`${edge.source}|${edge.target}`; line.dataset.weight=edge.weight;
  svg.appendChild(line); edgeEls.set(line.dataset.key,line);
});
const nodeEls = new Map();
payload.graph.nodes.forEach(node => {
  const p=positions[node.id]; if(!p) return;
  const g=el('g');
  const circle=el('circle',{cx:p.x,cy:p.y,r:10,fill:colorByKind[node.kind]||'#aaa',class:'node'});
  const label=el('text',{x:p.x+15,y:p.y+4,class:'node-label'}); label.textContent=node.label;
  g.append(circle,label); svg.appendChild(g); nodeEls.set(node.id,circle);
});

let index=0, timer=null;
function render(i) {
  index=Math.max(0,Math.min(frames.length-1,i)); slider.value=index;
  const frame=frames[index];
  const byId=new Map(frame.sparks.map(s=>[s.id,s]));
  const fired=new Set(frame.fired);
  const workspaceIds=new Set(frame.workspace.map(w=>w.hypothesis_id));
  nodeEls.forEach((circle,id)=>{
    const s=byId.get(id); const a=s?Math.max(0,s.activation):0;
    circle.setAttribute('r', 8 + Math.min(18,a*11));
    circle.setAttribute('opacity', .22 + Math.min(.78,a));
    circle.classList.toggle('fired',fired.has(id));
    circle.classList.toggle('workspace',workspaceIds.has(id));
  });
  edgeEls.forEach(line=>line.classList.remove('active'));
  for(const [source,target] of frame.active_edges){ const line=edgeEls.get(`${source}|${target}`); if(line) line.classList.add('active'); }
  document.getElementById('event').textContent=frame.external_event;
  document.getElementById('truth').textContent=`t=${frame.time.toFixed(2)} / world truth=${frame.truth ?? '—'}`;
  document.getElementById('prediction').textContent=(frame.prediction||'NO IGNITION').toUpperCase();
  document.getElementById('frameLabel').textContent=`${index+1} / ${frames.length}`;
  const tbody=document.getElementById('coalitions'); tbody.innerHTML='';
  frame.coalitions.slice(0,6).forEach(c=>{
    const tr=document.createElement('tr'); tr.innerHTML=`<td>${c.label}</td><td>${c.score.toFixed(3)}</td><td>${c.diversity}</td><td>${c.stability}</td>`; tbody.appendChild(tr);
  });
  const ws=document.getElementById('workspace'); ws.innerHTML=frame.workspace.length?frame.workspace.map(w=>`<span class="badge">${w.label} ${w.score.toFixed(2)}</span>`).join(''):'empty';
  const stats=frame.stats; document.getElementById('stats').innerHTML=`events ${stats.events_processed}<br>spark updates ${stats.spark_updates}<br>edge evaluations ${stats.edge_evaluations}<br>fires ${stats.fires}<br>ignitions ${stats.ignitions}`;
}
slider.addEventListener('input',()=>render(Number(slider.value)));
document.getElementById('prev').onclick=()=>render(index-1);
document.getElementById('play').onclick=()=>{
  if(timer){clearInterval(timer);timer=null;document.getElementById('play').textContent='再生';return;}
  document.getElementById('play').textContent='停止';
  timer=setInterval(()=>{ if(index>=frames.length-1){clearInterval(timer);timer=null;document.getElementById('play').textContent='再生';return;} render(index+1); },850);
};
render(0);
</script>
</body>
</html>
'''


def _write_utf8_lf(path: Path, contents: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(contents)


def write_trace(brain: SparkBrain, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "graph": brain.export_graph(),
        "frames": [asdict(frame) for frame in brain.trace],
        "ignitions": [asdict(ignition) for ignition in brain.ignitions],
    }
    validate_trace_payload(payload)
    _write_utf8_lf(output, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return output


def write_visualizer(brain: SparkBrain, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "graph": brain.export_graph(),
        "frames": [asdict(frame) for frame in brain.trace],
        "ignitions": [asdict(ignition) for ignition in brain.ignitions],
    }
    validate_trace_payload(payload)
    html = HTML_TEMPLATE.replace(
        "__PAYLOAD__",
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
    )
    _write_utf8_lf(output, html)
    return output
