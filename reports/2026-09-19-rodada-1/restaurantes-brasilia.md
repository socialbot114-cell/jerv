# Restaurantes Brasília — auditoria rodada 1

- **Stack:** Android nativo, Kotlin + Compose, DataStore
- **Conteúdo:** catálogo local DF (`restaurantes.json`, ~240 bairros via `normalizeNeighborhood`)
- **Testes:** `RestaurantCatalogTest.kt`

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Chips da UI divergem do JSON — filtro morto após load | bug | crítica | `RestaurantCatalog.kt:21`, `MainActivity.kt:174,193` |
| 2 | Favoritos usam `name` instável + `slug=name` com espaços/acentos | código | alta | `MainActivity.kt:93` |
| 3 | Filtro de região fixo ignora bairros do JSON (não filtráveis) | fluxo | alta | `MainActivity.kt:178`, `RestaurantCatalog.kt:59` |
| 4 | `openUrl` sem `try/catch` pode crashar sem browser | bug | alta | `MainActivity.kt:281` |
| 5 | `getIdentifier()` por card a cada recomposição (jank com 240 itens) | performance | média | `MainActivity.kt:218,238` |
| 6 | `query` e filtros compartilhados entre Home/Explore; volta perde contexto | fluxo | média | `MainActivity.kt:133` |
| 7 | Samples com `price="Consultar"`, sem rating/horas/contato | conteúdo | média | `MainActivity.kt:108`, `RestaurantCatalog.kt:75` |
| 8 | Favorito só muda `tint`; voltar `‹` sem acessibilidade/área mínima | design | média | `MainActivity.kt:222` |
| 9 | Docs desatualizados (`versionCode 1`) + `EmptyScreen` morto | código | baixa | `RELEASE_CHECKLIST.md:7`, `MainActivity.kt:251` |

## Top 3 prioridades

1. **Filtros que funcionam** — gerar chips/regiões a partir do JSON (fonte única) e
   chave estável `slug` para favoritos. Hoje o filtro principal retorna zero.
   (achados 1, 2, 3)
2. **Robustez de links e lista** — `try/catch` em `openUrl`, memoizar `getIdentifier`
   com `remember(slug)`, estados separados por aba. (achados 4, 5, 6)
3. **Conteúdo confiável pré-loja** — preço/horário/contato reais, rating quando houver,
   ícone `Filled` no favorito e voltar acessível. (achados 7, 8)
