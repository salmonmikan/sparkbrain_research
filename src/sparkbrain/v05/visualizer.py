from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def _seed_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, phase in (("development_results", "development"), ("confirmatory_results", "confirmatory")):
        for row in payload.get(key, []):
            item = dict(row)
            item["protocol_phase"] = phase
            rows.append(item)
    return rows


def build_v05_html(payload: dict[str, Any], *, title: str = "SparkBrain v0.5") -> str:
    display_payload = dict(payload)
    display_payload["seed_results"] = _seed_rows(payload)
    data = json.dumps(display_payload, ensure_ascii=False, separators=(",", ":"))
    safe_title = html.escape(title)
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{safe_title}</title><style>
body{{margin:0;background:#0d1117;color:#e6edf3;font-family:system-ui,sans-serif}}header{{padding:18px;border-bottom:1px solid #30363d}}
main{{display:grid;grid-template-columns:1fr 390px;gap:16px;padding:16px}}canvas{{width:100%;height:680px;background:#010409;border:1px solid #30363d}}
.panel{{background:#161b22;border:1px solid #30363d;padding:12px}}pre{{white-space:pre-wrap;max-height:620px;overflow:auto}}select{{margin:8px}}
.badge{{display:inline-block;padding:3px 8px;border:1px solid #30363d;border-radius:999px;margin-right:6px}}
</style></head><body><header><h1>{safe_title}</h1><p>Anonymous temporal Assembly candidates; no semantic concept claim.</p><div id=\"gates\"></div></header>
<main><canvas id=\"chart\" width=\"1100\" height=\"680\"></canvas><aside class=\"panel\"><select id=\"seed\"></select><pre id=\"details\"></pre></aside></main>
<script>const data={data};const rows=data.seed_results||[];const sel=document.getElementById('seed');const canvas=document.getElementById('chart');const ctx=canvas.getContext('2d');const details=document.getElementById('details');const gates=document.getElementById('gates');
Object.entries(data.gates||{{}}).forEach(([k,v])=>{{const b=document.createElement('span');b.className='badge';b.textContent=k+': '+(v?'PASS':'FAIL');gates.appendChild(b)}});
for(const row of rows){{const o=document.createElement('option');o.value=row.protocol_phase+':'+row.seed;o.textContent=row.protocol_phase+' seed '+row.seed;sel.appendChild(o)}}
function draw(){{const row=rows.find(x=>x.protocol_phase+':'+x.seed===sel.value)||rows[0];ctx.clearRect(0,0,canvas.width,canvas.height);if(!row)return;const conditions=Object.entries(row.conditions||{{}});const metrics=['prediction_accuracy','action_accuracy','assembly_activation_rate','assembly_purity'];const colors=['#58a6ff','#3fb950','#d2a8ff','#f2cc60'];conditions.forEach(([name,value],i)=>{{metrics.forEach((m,j)=>{{const v=value.summary[m]||0;ctx.fillStyle=colors[j];ctx.fillRect(70+i*165+j*25,610-v*500,20,v*500)}});ctx.fillStyle='#e6edf3';ctx.fillText(name,60+i*165,645)}});details.textContent=JSON.stringify(row,null,2)}}sel.onchange=draw;draw();</script></body></html>"""


def write_v05_html(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_v05_html(payload), encoding="utf-8")
