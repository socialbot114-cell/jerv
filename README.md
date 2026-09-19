# JERV — App Factory e Worker de auditoria

Repositório de conhecimento e automação do pipeline de criação de apps:
auditorias de código, design e fluxo, backlog priorizado, templates SwiftUI,
validação de release e workflows reutilizáveis.

**Regra dura: nenhum segredo aqui.** Sem `.p8`, `.jks`, `.keystore`, `keystore.properties`,
API keys ou tokens. Achados de segurança citam o problema, nunca o valor.

## Estrutura

```text
jerv/
  README.md            este arquivo
  worker/
    prioritize.py      worker sob demanda: prioriza achados via TypeSafe Jev
  jerv_cli.py           CLI determinística de validação, auditoria e scaffolding
  templates/            templates de novos apps
  workflows/            workflows reutilizáveis do GitHub Actions
  xcode-cloud/          scripts para gerar projetos no Xcode Cloud
  blueprints/           contratos iniciais dos apps Brasília
  reports/
    YYYY-MM-DD-rodada-N/
      README.md        resumo executivo da rodada
      <projeto>.md     1 arquivo por projeto com analise e problemas
```

## Como rodar a fábrica

```bash
python3 jerv_cli.py validate path/to/app.yml
python3 jerv_cli.py audit path/to/app.yml
python3 jerv_cli.py release-check path/to/app.yml
python3 jerv_cli.py init path/to/new-app --manifest blueprints/restaurantes-ios/app.yml
```

`validate` verifica a estrutura, o bundle, o catálogo, o Privacy Manifest e
arquivos que parecem segredos. `release-check` também exige que todos os
registros estejam marcados como `data_status: verified`.

## Worker Jev (sob demanda)

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
