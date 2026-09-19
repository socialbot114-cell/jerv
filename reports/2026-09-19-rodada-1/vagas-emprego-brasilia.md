# Vagas Emprego Brasília — auditoria rodada 1

- **Stack:** Android nativo, Kotlin + Compose, DataStore
- **Conteúdo:** `JobCatalog` DF inicial (vagas de validação, sem fonte/link)
- **Testes:** `JobCatalogTest.kt`

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Catálogo sem fonte, data ou URL de candidatura — impublicável | conteúdo | crítica | `MainActivity.kt:77`, `PLAY_STORE_LISTING.md:25` |
| 2 | Vagas salvas usam `title` como chave — colisão garantida | bug | crítica | `MainActivity.kt:109` |
| 3 | Busca ignora descrição, tipo e salário | código | alta | `MainActivity.kt:161` |
| 4 | Categoria `Comercial` existe mas não tem chip (inacessível) | bug | alta | `MainActivity.kt:149,81` |
| 5 | Aba `Regiões` é placeholder estático; detalhe sem ação útil | fluxo | média | `MainActivity.kt:155,153` |

## Top 3 prioridades

1. **Vaga real ou nada** — `id/slug`, empresa, `sourceLabel/sourceUrl`, `expiresAt` e
   botão candidatar/ver fonte; remover mocks `Empresa local` antes da loja.
   (achados 1, 2)
2. **Busca e filtros completos** — incluir descrição/tipo/salário na busca, chip para
   todas as categorias existentes, `Regiões` com contagem e filtro por cidade.
   (achados 3, 4, 5)
3. **Validade dos dados** — expirar vagas vencidas, política de atualização do catálogo.
