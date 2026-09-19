# Rodada 1 — 19/09/2026

Primeira auditoria do worker JERV: 10 projetos em `/home/richard/Documentos/play store`.
Método: leitura estática dos fontes + 1 chamada Jev (`jev-1.13.0`) com 5 perguntas
`Choice` em paralelo para priorização. Nenhum código foi alterado nesta rodada.

## Veredito Jev (1 call, 5 perguntas, 29 achados como opções)

| Pergunta | Vencedor | Confiança |
|---|---|---|
| Maior risco de crash/perda de dados | `mus-resourceid` (Musicas) | 0.54 — moderada |
| Maior risco de segurança/privacidade | `cat-keystore` (CATECISMO+Machado) | 0.94 — forte |
| Maior bloqueio de loja | `sw-licencas` (Swing) | 0.78 — forte |
| Maior dano ao usuário | `mus-catalogo-vazio` (Musicas) | 0.30 — fraca, revisar |
| Melhor quick win | `mus-catalogo-vazio` (Musicas) | 0.19 — fraca, revisar |

Custo da chamada: 7820 tokens in / 1782 out.

## Top 5 prioridades compostas (Jev × severidade do auditor)

1. **Keystore de release versionado** (CATECISMO + Machado) — Jev 0.95. Revogar,
   remover do git com `filter-repo`, mover para CI secrets.
2. **Licenças de imagem pendentes** (Swing) — Jev 0.79. Bloqueio App Store 5.2.3
   quase certo; regularizar 7 imagens antes de submeter.
3. **Catálogo vazio crasha no arranque** (Musicas) — crash imediato; carregar
   `CATALOGO.json` real em vez de `emptyList`.
4. **`resourceId()` sempre lança** (Musicas) — `toggle()` crasha em qualquer troca.
5. **Segredos Apple em PROJECT_STATUS.md** (CATECISMO + Machado) — remover valores,
   manter só referências.

## Arquivos por projeto

- `quem-sou-eu.md` — iOS SwiftUI, motor de adivinhação offline
- `brasil-feriados.md` — Android Kotlin/Compose
- `catecismo.md` — KMP (Android + iOS + site)
- `machado-de-assis.md` — KMP (Android + iOS + site)
- `city-bikes-premium.md` — React 19 + TS + Capacitor
- `musicas-para-estudar.md` — Android Kotlin/Compose + Media3
- `receitas-airfryer.md` — Android Kotlin/Compose
- `restaurantes-brasilia.md` — Android Kotlin/Compose
- `vagas-emprego-brasilia.md` — Android Kotlin/Compose
- `swing-brasilia.md` — iOS SwiftUI, guia 18+ offline

Fora do escopo (pastas vazias/placeholder): `menos delivery`, `Oficinas Brasília`,
`tem glutem ?`, `xadrez cor sim cor não`, `reffffs` (só referências visuais).
