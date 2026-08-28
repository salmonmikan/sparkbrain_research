from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def build_trace_html(trace: list[dict[str, Any]], *, title: str = "SparkBrain v0.4") -> str:
    payload = json.dumps(trace, ensure_ascii=False, separators=(",", ":"))
    safe_title = html.escape(title)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{safe_title}</title>
<style>
:root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; }}
body {{ margin: 0; background: #0d1117; color: #e6edf3; }}
header {{ padding: 16px 20px; border-bottom: 1px solid #30363d; }}
main {{ display:grid; grid-template-columns: 1fr 320px; gap:16px; padding:16px; }}
canvas {{ width:100%; height:640px; background:#010409; border:1px solid #30363d; }}
.panel {{ border:1px solid #30363d; padding:12px; background:#161b22; }}
button,input {{ margin:4px; }}
pre {{ white-space:pre-wrap; overflow:auto; max-height:520px; }}
.legend span {{ display:inline-block; margin-right:12px; }}
</style>
</head>
<body>
<header><h1>{safe_title}</h1><div class=\"legend\">
<span>● spike</span><span>◆ ignition</span><span>vertical axis: unit ID</span>
</div></header>
<main>
<section><canvas id=\"raster\" width=\"1100\" height=\"640\"></canvas></section>
<aside class=\"panel\">
<label>Step <input id=\"step\" type=\"range\" min=\"0\" value=\"0\"></label>
<button id=\"play\">Play</button><button id=\"pause\">Pause</button>
<pre id=\"details\"></pre>
</aside>
</main>
<script>
const trace={payload};
const canvas=document.getElementById('raster');
const ctx=canvas.getContext('2d');
const slider=document.getElementById('step');
const details=document.getElementById('details');
slider.max=Math.max(0,trace.length-1);
let timer=null;
function draw(index){{
  const row=trace[index]?.result||{{}};
  const spikes=row.spikes||[];
  const ignitions=row.ignitions||[];
  const maxUnit=Math.max(1,...spikes.map(x=>x.unit_id));
  const start=row.start_ms||0, end=Math.max(start+1,row.end_ms||start+1);
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#8b949e'; ctx.font='14px monospace';
  ctx.fillText(`time ${{start.toFixed?.(1)??start}} → ${{end.toFixed?.(1)??end}} ms`,18,22);
  for(const s of spikes){{
    const x=40+(s.time_ms-start)/(end-start)*(canvas.width-70);
    const y=42+s.unit_id/maxUnit*(canvas.height-70);
    const radius=2.2+Math.min(4,s.prediction_error*3+s.novelty*2);
    ctx.beginPath(); ctx.arc(x,y,radius,0,Math.PI*2);
    ctx.fillStyle=s.prediction_error>0.5?'#ff7b72':'#58a6ff'; ctx.fill();
  }}
  for(const ig of ignitions){{
    const x=40+(ig.time_ms-start)/(end-start)*(canvas.width-70);
    ctx.strokeStyle='#d2a8ff'; ctx.lineWidth=2; ctx.beginPath();
    ctx.moveTo(x,35); ctx.lineTo(x,canvas.height-20); ctx.stroke();
  }}
  details.textContent=JSON.stringify(row,null,2);
}}
slider.addEventListener('input',()=>draw(Number(slider.value)));
document.getElementById('play').onclick=()=>{{
  clearInterval(timer);
  timer=setInterval(()=>{{
    slider.value=(Number(slider.value)+1)%Math.max(1,trace.length);
    draw(Number(slider.value));
  }},700);
}};
document.getElementById('pause').onclick=()=>clearInterval(timer);
draw(0);
</script>
</body></html>"""


def write_trace_html(
    path: str | Path,
    trace: list[dict[str, Any]],
    *,
    title: str = "SparkBrain v0.4",
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_trace_html(trace, title=title), encoding="utf-8")
