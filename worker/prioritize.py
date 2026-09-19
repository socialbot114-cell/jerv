#!/usr/bin/env python3
"""JERV worker - rodada 1: prioriza achados via TypeSafe Jev (fan-out de Choice).
Um call, 5 perguntas Choice paralelas sobre o mesmo state; composicao no codigo.
Uso: set -a; . ~/.config/typesafe/.env; set +a; python3 /tmp/jerv_prioritize.py
"""
import json
import os
import sys
import urllib.request

API = "https://api.typesafe.ai/v1/systemone"
KEY = os.environ.get("TYPESAFE_API_KEY", "")
if not KEY:
    sys.exit("TYPESAFE_API_KEY ausente")

FINDINGS = [
    {"id": "qse-fluxo-terminal", "project": "quem sou eu ?", "auditor": "critica", "title": "Partida nao termina apos acerto sem guardas de estado", "why": "Palpite so muda para confirming; toque duplo pode duplicar vitoria; sem guards de fase terminal."},
    {"id": "qse-politica-palpite", "project": "quem sou eu ?", "auditor": "alta", "title": "Palpite usa so confidence>=0.68 sem margem", "why": "Primeiro e segundo empatados geram palpite errado; falta margem, razao e entropia."},
    {"id": "qse-indice-oob", "project": "quem sou eu ?", "auditor": "alta", "title": "chooseCandidateIndex sem validacao pode crashar", "why": "Indice fora de [0,count) acessa array fora dos limites."},
    {"id": "qse-soma-zero", "project": "quem sou eu ?", "auditor": "alta", "title": "Soma zero de escores nao recuperada", "why": "Scores zerados deixam bestGuess arbitrario e quebram logica de derrota."},
    {"id": "bf-lembretes-falsos", "project": "brasil feriados", "auditor": "critica", "title": "Lembretes falsos: nada agenda notificacao real", "why": "So persiste id no DataStore; sem WorkManager o Snackbar engana o usuario."},
    {"id": "bf-expira-2027", "project": "brasil feriados", "auditor": "critica", "title": "App expira em 31/12/2027 sem plano de atualizacao", "why": "Base so tem 2026/2027; em 2028 congela com lista vazia."},
    {"id": "bf-busca-mes", "project": "brasil feriados", "auditor": "alta", "title": "Busca por mes por extenso retorna zero", "why": "Filtro usa displayName SHORT; 'novembro' nunca da match."},
    {"id": "bf-favoritos-vazam", "project": "brasil feriados", "auditor": "alta", "title": "Favoritos vazam feriado do DF para outros UFs", "why": "ProfileScreen filtra lista global em vez de forLocation(ano,uf)."},
    {"id": "cat-keystore", "project": "CATECISMO + machado", "auditor": "critica", "title": "Keystore de release versionado no repo", "why": "Chave privada de assinatura commitada; exige revogacao e filter-repo."},
    {"id": "cat-segredos-apple", "project": "CATECISMO + machado", "auditor": "critica", "title": "Segredos Apple expostos no PROJECT_STATUS.md", "why": "TeamID, KeyID, Issuer, certificado e profile em claro."},
    {"id": "cat-doc-copia", "project": "CATECISMO", "auditor": "critica", "title": "PROJECT_STATUS.md e copia do Machado", "why": "Titulo, bundle e 30 obras descrevem o outro app; orienta release errado."},
    {"id": "cat-bundle-maiuscula", "project": "CATECISMO", "auditor": "alta", "title": "Bundle/applicationId com maiusculas", "why": "Viola reverse-DNS e quebra provisioning."},
    {"id": "cat-progresso-pagina", "project": "CATECISMO", "auditor": "alta", "title": "Progresso so ao concluir capitulo", "why": "Fechar no meio perde posicao; Machado salva por pagina."},
    {"id": "cb-browserrouter", "project": "city bikes premium", "auditor": "critica", "title": "BrowserRouter quebra reload na WebView Capacitor", "why": "Sem fallback, reload em /app da tela branca; usar HashRouter."},
    {"id": "cb-sem-cache", "project": "city bikes premium", "auditor": "critica", "title": "Nenhum cache offline para lista de redes", "why": "Sem persist; offline o mapa abre vazio."},
    {"id": "cb-context-memo", "project": "city bikes premium", "auditor": "alta", "title": "Context sem useMemo re-renderiza tudo", "why": "value recriado a cada pan de 600ms."},
    {"id": "cb-leaflet-leak", "project": "city bikes premium", "auditor": "alta", "title": "Leaflet com prototype global e mapRef em useState", "why": "Muta singleton e gera loop de renders."},
    {"id": "mus-catalogo-vazio", "project": "Musicas para Estudar", "auditor": "critica", "title": "Catalogo vazio crasha no arranque", "why": "catalog[3] sobre lista vazia; catalogo.json vazio e CATALOGO.json real nunca carregado."},
    {"id": "mus-resourceid", "project": "Musicas para Estudar", "auditor": "critica", "title": "resourceId() sempre lanca excecao", "why": "Funcao so da error(); toggle sempre crasha."},
    {"id": "mus-timer-rotacao", "project": "Musicas para Estudar", "auditor": "alta", "title": "Timer perde estado na rotacao e background", "why": "isRunning/deadline fora do SavedStateHandle; sem ForegroundService."},
    {"id": "rec-timer-silencioso", "project": "receitas airfreyr", "auditor": "alta", "title": "Timer silencioso sem notificacao", "why": "So funciona com app aberto; sem Alarm o usuario perde o ponto."},
    {"id": "vag-sem-fonte", "project": "vagas emprego brasilia", "auditor": "critica", "title": "Catalogo sem fonte, data ou URL de candidatura", "why": "Samples com Empresa local e tudo null; sem botao candidatar; impublicavel."},
    {"id": "rest-chips-mortos", "project": "restaurantes brasilia", "auditor": "critica", "title": "Chips da UI divergem do JSON; filtro morto", "why": "UI filtra por categorias inexistentes no JSON; retorna zero."},
    {"id": "vag-chave-titulo", "project": "vagas emprego brasilia", "auditor": "critica", "title": "Salvos usam title como chave; colisao garantida", "why": "Cargos repetidos colidem; Job sem id/slug."},
    {"id": "rest-openurl", "project": "restaurantes brasilia", "auditor": "alta", "title": "openUrl sem try/catch pode crashar", "why": "Sem handler de browser = crash direto."},
    {"id": "sw-licencas", "project": "swing brasilia", "auditor": "critica", "title": "Licencas de imagem pendentes; bloqueio App Store 5.2.3", "why": "7/8 imagens sem autor/licenca e hero sugestiva sem prova de direito."},
    {"id": "sw-agegate", "project": "swing brasilia", "auditor": "critica", "title": "Age gate burlavel por flag e 1-toque", "why": "SWING_SKIP_AGE=1 desliga barreira; sem data de nascimento."},
    {"id": "sw-whatsapp", "project": "swing brasilia", "auditor": "alta", "title": "WhatsApp comunidade igual ao de negocios", "why": "Mesmo invite mistura publicos; quebra moderacao."},
    {"id": "sw-nav-aninhada", "project": "swing brasilia", "auditor": "alta", "title": "NavigationStack aninhado quebra navegacao", "why": "Duplo header, back inconsistente, TabView fora de sincronia."},
]

options = {f["id"]: f"{f['project']} | {f['title']} | {f['why']}" for f in FINDINGS}

body = {
    "state": {
        "worker": "jerv-rodada-1",
        "goal": "Priorizar backlog de auditoria de 10 apps/jogos offline-first",
        "policy": "Crashes, dados errados e bloqueios de loja valem mais que cosmeticos.",
    },
    "model": "jev-latest",
    "questions": {
        "top_crash": {"type": "choice", "instructions": "Qual achado representa o MAIOR risco de crash ou perda de dados para o usuario?", "criteria": options},
        "top_security": {"type": "choice", "instructions": "Qual achado representa o MAIOR risco de seguranca, privacidade ou vazamento de segredos?", "criteria": options},
        "top_store_blocker": {"type": "choice", "instructions": "Qual achado tem MAIOR chance de causar rejeicao na App Store ou Play Store?", "criteria": options},
        "top_user_harm": {"type": "choice", "instructions": "Qual achado causa MAIOR dano ao usuario final (dado errado, funcao falsa, app inutil)?", "criteria": options},
        "top_quick_win": {"type": "choice", "instructions": "Qual achado e o QUICK WIN: alto impacto no usuario e correcao simples e localizada?", "criteria": options},
    },
}

req = urllib.request.Request(
    API,
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    out = json.load(resp)

with open("/tmp/jerv_jev_raw.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print("MODEL:", out.get("model"), "| USAGE:", json.dumps(out.get("usage")))
for qid, ans in out["answers"].items():
    print(f"--- {qid}: winner={ans.get('choice')} conf={ans.get('confidence')}")
    top3 = sorted(ans.get("probabilities", {}).items(), key=lambda kv: -kv[1])[:3]
    for fid, p in top3:
        print(f"    {p:.2f} {fid}")
