#!/usr/bin/env python3
"""JERV worker - rodada 2 design: prioriza gaps visuais via TypeSafe Jev.
Um call, 5 perguntas Choice em paralelo; composicao no codigo.
Uso: set -a; . ~/.config/typesafe/.env; set +a; python3 /tmp/jerv_design_r2.py
"""
import json
import os
import sys
import urllib.request

API = "https://api.typesafe.ai/v1/systemone"
KEY = os.environ.get("TYPESAFE_API_KEY", "")
if not KEY:
    sys.exit("TYPESAFE_API_KEY ausente")

GAPS = [
    {"id": "qse-palette", "app": "quem sou eu ?", "title": "Hex do codigo diverge do spec; falta roxo profundo #21104F", "why": "Codigo usa violet ~#6320F0 e canvas grouped; mockups exigem fundo #21104F e CTA #6C22E8."},
    {"id": "qse-cta", "app": "quem sou eu ?", "title": "CTA 52px Capsule vs spec 90-110px com circulo lime e seta", "why": "Botao atual e metade da altura e perde dominancia hero; sem sombra colorida nem inset highlight."},
    {"id": "qse-bottomnav", "app": "quem sou eu ?", "title": "BottomNav material generica vs floating pill lime", "why": "ultraThinMaterial + divider; spec pede peca flutuante com ativo lime e label escuro."},
    {"id": "qse-result", "app": "quem sou eu ?", "title": "ResultCard generico vs tela gamificada", "why": "Faltam pill CONFIRMADO, 3 mini-cards de recompensa, banner mascote e confetes."},
    {"id": "qse-home", "app": "quem sou eu ?", "title": "Home sem chips de moedas/pontos, speech bubble e cards secundarios", "why": "So 2 stat chips; spec pede trio pastel + balao 'Grandes personagens...' + 3 cards lilas/amarelo/rosa."},
    {"id": "qse-type", "app": "quem sou eu ?", "title": "Sem fonte rounded custom; so SF system", "why": "Spec pede Nunito/Fredoka/Baloo 800-900; titulos 36-52px nao existem no codigo."},
    {"id": "qse-mascot", "app": "quem sou eu ?", "title": "Mascote com 1 estado vs 6 estados do spec", "why": "So mascot_princess estatica com float; faltam curioso/comemorando/investigando/pensando/confiante/surpreso."},
    {"id": "qse-splash", "app": "quem sou eu ?", "title": "Sem splash dedicada fiel ao backgroud 1 tela.png", "why": "Onboarding generico; falta branding roxo profundo + blobs + onda lime."},
    {"id": "rec-tokens", "app": "receitas airfryer", "title": "Cores hardcoded; PaleOrange quase igual a Cream; radius 14-32 aleatorios", "why": "7 cores soltas no MainActivity, delta 5% entre tons claros, 6 radius sem escala, sem elevation."},
    {"id": "rec-hero", "app": "receitas airfryer", "title": "Cards brancos flat sem sombra nem hero premium", "why": "CardDefaults sem elevation; mockup vovo pede calor rustico com profundidade e ouro."},
    {"id": "rec-cover14", "app": "receitas airfryer", "title": "14/30 receitas sem imageKey caem em Canvas procedural", "why": "Doces novos renderizam placeholder; quebra Hero/Detail/Row."},
    {"id": "rec-cta", "app": "receitas airfryer", "title": "Botoes 52-56px sem hierarquia premium nem dark card", "why": "COMEÇAR A COZINHAR e primario ok mas sem escala; modo cozinhar usa card Ink bom, resto nao acompanha."},
    {"id": "rec-type", "app": "receitas airfryer", "title": "Tipografia manual sem escala modular", "why": "sp soltos 9-58, headline misturado com Bold/Black ad-hoc; sem display serif para marca vovo."},
    {"id": "rec-brand", "app": "receitas airfryer", "title": "Marca dividida: mockup vovo rustico vs codigo laranja flat", "why": "Kit reffffs define madeira/ambar/serif dourada; codigo nao reflete nenhuma das duas direcoes com intencao."},
]

options = {g["id"]: f"{g['app']} | {g['title']} | {g['why']}" for g in GAPS}

body = {
    "state": {
        "worker": "jerv-rodada-2-design",
        "goal": "Transformar design atual em padrao FAANG nativo; piloto: quem sou eu (iOS) e receitas airfryer (Android)",
        "policy": "Telashot de loja e primeira impressao valem mais; tokens antes de telas; marca vovo = rustico premium, nao roxo/lima.",
    },
    "model": "jev-latest",
    "questions": {
        "top_visual_crack": {"type": "choice", "instructions": "Qual gap grita mais 'nao-FAANG' no primeiro olhar?", "criteria": options},
        "top_ux_friction": {"type": "choice", "instructions": "Qual gap mais atrapalha hierarquia, leitura ou acao do usuario?", "criteria": options},
        "top_brand_inconsistency": {"type": "choice", "instructions": "Qual gap representa a maior inconsistencia de marca entre mockup/spec e codigo?", "criteria": options},
        "top_store_appeal": {"type": "choice", "instructions": "Qual gap, se corrigido, mais aumenta conversao em screenshots e primeira sessao na loja?", "criteria": options},
        "top_quick_design_win": {"type": "choice", "instructions": "Qual gap e o quick win visual: alto impacto e correcao localizada em tokens/componente?", "criteria": options},
    },
}

req = urllib.request.Request(
    API,
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    out = json.load(resp)

with open("/tmp/jerv_design_r2_raw.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print("MODEL:", out.get("model"), "| USAGE:", json.dumps(out.get("usage")))
for qid, ans in out["answers"].items():
    print(f"--- {qid}: winner={ans.get('choice')} conf={ans.get('confidence')}")
    for fid, p in sorted(ans.get("probabilities", {}).items(), key=lambda kv: -kv[1])[:3]:
        print(f"    {p:.2f} {fid}")
