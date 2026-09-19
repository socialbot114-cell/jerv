# Receitas Airfryer — auditoria rodada 1

- **Stack:** Android nativo, Kotlin + Compose, DataStore, offline-first
- **Conteúdo:** 30 receitas (11 doces), guia de 15 alimentos, ranking de despensa
- **Testes:** `RecipeCatalogTest.kt`

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Timer de cozinhar silencioso, sem notificação/alarme | fluxo | alta | `MainActivity.kt:326-327,356`, `UserPreferences.kt:81-91` |
| 2 | Progresso da etapa perdido ao avançar (`clearTimer` antes de `stepIndex++`) | fluxo | alta | `MainActivity.kt:318,341` |
| 3 | `BackHandler` manda Detalhe sempre para Home (perde origem) | fluxo | média | `MainActivity.kt:143-145` |
| 4 | 14/30 receitas sem `imageKey` caem em placeholder genérico | design | média | `RecipeCatalog.kt:197-215`, `MainActivity.kt:396-409` |
| 5 | Filtros dietéticos perdem rascunho na rotação | código | média | `MainActivity.kt:234,238` |
| 6 | `activeStep` persistido como `String` (`toIntOrNull()?:0`) | código | média | `UserPreferences.kt:40,55,83` |

## Top 3 prioridades

1. **Timer que avisa de verdade** — `AlarmManager` + notificação com som; sem isso o
   usuário queima a receita com o app em background. (achado 1)
2. **Passo a passo persistente** — salvar `activeStep` (como `int`) antes de limpar o
   timer; voltar à origem em vez de Home. (achados 2, 3, 6)
3. **Cobertura visual total** — `imageKey` para as 14 receitas restantes (doces novos);
   `rememberSaveable` nos filtros. (achados 4, 5)
