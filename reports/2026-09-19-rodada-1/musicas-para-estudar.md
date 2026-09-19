# Músicas para Estudar — auditoria rodada 1

- **Stack:** Android nativo, Kotlin + Compose + Media3/ExoPlayer, DataStore
- **Conteúdo:** `musicas/CATALOGO.json` (17 MP3 locais) + 36 capas WebP; timer 25/50/90
- **Testes:** `FocusSessionViewModelTest.kt`

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Catálogo vazio crasha no arranque **[Jev crash/quick-win]** | bug | crítica | `MainActivity.kt:156,247`, `assets/catalogo.json:1-4` |
| 2 | `resourceId()` sempre lança exceção **[Jev crash 0.56]** | bug | crítica | `MainActivity.kt:212`, `:196-205` |
| 3 | `HomeScreen` usa `first{}` sobre catálogo vazio/categorias divergentes | bug | crítica | `MainActivity.kt:383-390` |
| 4 | Timer perde estado na rotação/background | fluxo | alta | `MainActivity.kt:114-127` |
| 5 | Botão Foco dessincroniza áudio e sessão | fluxo | alta | `MainActivity.kt:548-555` |
| 6 | `LazyColumn` aninhada sem peso quebra rolagem/busca | bug | alta | `MainActivity.kt:575-589` |
| 7 | Estatísticas contam duplicado e minuto impreciso | código | média | `MainActivity.kt:275-283` |
| 8 | `MediaController` sem `try/catch`/release do `Future` | código | média | `MainActivity.kt:182-194,210` |

## Top 3 prioridades

1. **App precisa abrir** — carregar `CATALOGO.json` real no `assets/catalogo.json`,
   implementar `resourceId()` de verdade, trocar `first{}` por `firstOrNull` e alinhar
   categorias do código com as do JSON. Três crashes de arranque. (achados 1, 2, 3)
2. **Timer confiável** — estado no `SavedStateHandle` + `ForegroundService`/alarme para
   background; separar toggle de áudio e de sessão com fonte única de verdade.
   (achados 4, 5)
3. **Player robusto** — `try/catch` no `Future`, `release()` no ciclo de vida,
   `weight(1f)` na lista da biblioteca, estatísticas idempotentes. (achados 6, 7, 8)
