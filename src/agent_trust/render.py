from __future__ import annotations

import html
import json
from pathlib import Path

from .core import calculate_score


def render_profile(profile_path: Path, output_path: Path) -> None:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    result = calculate_score(profile)
    esc = lambda value: html.escape(str(value))
    tools = "".join(f"<li><strong>{esc(x.get('name'))}</strong><span>{esc(x.get('access', 'unspecified'))}</span></li>" for x in profile["tools"])
    scores = "".join(f"<tr><td>{esc(k.replace('_',' ').title())}</td><td>{esc(v)}</td></tr>" for k, v in profile["assurance"]["scores"].items())
    gates = "".join(f"<tr><td>{esc(k.replace('_',' ').title())}</td><td class='{esc(v.lower())}'>{esc(v)}</td></tr>" for k, v in profile["assurance"]["mandatory_gates"].items())
    document = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(profile['name'])} AI Agent Security Trust Center</title><meta name='description' content='Verifiable AI agent security, MCP security, authorization, governance and compliance profile for {esc(profile['name'])}.'><style>{CSS}</style></head><body><main><header><p class='eyebrow'>AI AGENT SECURITY TRUST CENTER</p><h1>{esc(profile['name'])}</h1><p class='purpose'>{esc(profile['purpose'])}</p><div class='status {result['effective_status'].lower()}'>{esc(result['effective_status'])}</div></header><section class='facts'><div><span>Agent ID</span>{esc(profile['agent_id'])}</div><div><span>Version</span>{esc(profile['version'])}</div><div><span>Owner</span>{esc(profile['owner']['name'])}</div><div><span>Autonomy</span>L{esc(profile['autonomy_level'])}</div><div><span>Assurance score</span>{esc(result['score'])}/100</div><div><span>Valid until</span>{esc(profile['assurance'].get('valid_until','Not declared'))}</div></section><section><h2>Authorized tools</h2><ul>{tools or '<li>No tools declared</li>'}</ul></section><section class='grid'><div><h2>Assurance dimensions</h2><table>{scores}</table></div><div><h2>Mandatory gates</h2><table>{gates}</table></div></section><section><h2>Known limitations</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in profile.get('limitations',[])) or '<li>No limitations declared</li>'}</ul></section><footer>Generated from a machine-readable assurance profile. Verify the evidence bundle and signature before relying on this page.</footer></main></body></html>"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")


CSS = """
:root{font-family:Inter,ui-sans-serif,system-ui;color:#dfe7f2;background:#07111f}body{margin:0;background:radial-gradient(circle at top right,#17335d 0,#07111f 38%);min-height:100vh}main{max-width:1080px;margin:auto;padding:64px 24px}header{border-bottom:1px solid #38506c;padding-bottom:34px;position:relative}.eyebrow{color:#63e6be;font-size:13px;font-weight:800;letter-spacing:.16em}h1{font-size:clamp(42px,7vw,78px);line-height:1;margin:18px 0}.purpose{font-size:20px;color:#aebed1;max-width:760px;line-height:1.5}.status{display:inline-block;margin-top:12px;padding:10px 16px;border:1px solid;border-radius:999px;font-weight:800}.verified,.pass{color:#63e6be}.review_required,.not_tested{color:#ffd43b}.restricted,.fail,.expired{color:#ff8787}.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#38506c;margin:38px 0;border:1px solid #38506c}.facts div{background:#0b192b;padding:22px;font-size:18px}.facts span{display:block;color:#8ea2ba;text-transform:uppercase;font-size:11px;letter-spacing:.1em;margin-bottom:9px}section{margin:48px 0}h2{font-size:24px}ul{padding:0;list-style:none}li{display:flex;justify-content:space-between;border-bottom:1px solid #243b55;padding:14px 0;color:#cad6e4}li span{color:#8ea2ba}.grid{display:grid;grid-template-columns:1fr 1fr;gap:50px}table{width:100%;border-collapse:collapse}td{padding:12px 4px;border-bottom:1px solid #243b55}td:last-child{text-align:right;font-weight:800}footer{border-top:1px solid #38506c;padding-top:24px;color:#71869f;font-size:13px}@media(max-width:700px){.facts,.grid{grid-template-columns:1fr}}
"""
