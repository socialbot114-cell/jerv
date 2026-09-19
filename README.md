# JERV — Worker de auditoria dos apps

Repositório de conhecimento do pipeline de criação de apps: auditorias de código,
design e fluxo, backlog priorizado e histórico de melhorias.

**Regra dura: nenhum segredo aqui.** Sem `.p8`, `.jks`, `.keystore`, `keystore.properties`,
API keys ou tokens. Achados de segurança citam o problema, nunca o valor.

## Estrutura

```text
jerv/
  README.md            este arquivo
  worker/
    prioritize.py      worker sob demanda: prioriza achados via TypeSafe Jev
  reports/
    YYYY-MM-DD-rodada-N/
      README.md        resumo executivo da rodada
      <projeto>.md     1 arquivo por projeto com analise e problemas
```

## Como rodar (sob demanda)

```sh
set -a; . ~/.config/typesafe/.env; set +a
python3 worker/prioritize.py
```

O worker usa 1 chamada Jev (`jev-latest`, endpoint `/v1/systemone`) com 5 perguntas
`Choice` em paralelo (`top_crash`, `top_security`, `top_store_blocker`,
`top_user_harm`, `top_quick_win`) e compõe o ranking no código.
Confiança baixa (< 0.6) vai para revisão humana — ver skill `typesafe-ai`.

## Rodadas

- `reports/2026-09-19-rodada-1/` — primeira auditoria: 10 projetos, 100+ achados.
