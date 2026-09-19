# Brasil Feriados — auditoria rodada 1

- **Stack:** Android nativo, Kotlin + Jetpack Compose (BOM 2025.02.00), minSdk 26
- **Base:** `HolidayData.kt` + `HolidayCalendar` (2026/2027), galeria offline em `drawable-nodpi`
- **Testes:** `HolidayCalendarTest.kt` (JUnit)

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Lembretes falsos: nada agenda notificação real | bug | crítica | `MainActivity.kt:411`, `UserPreferences.kt:46-47` |
| 2 | App expira em 31/12/2027 sem plano de atualização | conteúdo | crítica | `MainActivity.kt:161`, `HolidayData.kt:33-36` |
| 3 | Busca por mês por extenso retorna zero | bug | alta | `MainActivity.kt:362,524` |
| 4 | Favoritos vazam feriado do DF para outros UFs e misturam anos | bug | alta | `MainActivity.kt:426,491-495` |
| 5 | Imagem hero duplicada 100% sobreposta (decode/memória 2x) | performance | alta | `MainActivity.kt:216-217,509-510` |
| 6 | Grade do calendário não é clicável | fluxo | alta | `MainActivity.kt:301-321` |
| 7 | Diálogo de localidade impede SC/RS/PR apesar do app suportar | fluxo | alta | `MainActivity.kt:469-470` vs `:191` |
| 8 | Rotação perde navegação e volta para home | código | média | `MainActivity.kt:133-136` |
| 9 | Detalhe hardcodifica "2 dias de férias" divergindo do Planejador | fluxo | média | `MainActivity.kt:384,406` |
| 10 | `bridgePlan` cobra férias em meio-expediente e na virada do ano | bug | média | `HolidayData.kt:80-87` |
| 11 | Semana começa na segunda, contra padrão BR | design | média | `MainActivity.kt:303,305` |
| 12 | Release sem assinatura garantida + backup expõe DataStore | segurança | baixa | `app/build.gradle:17-32` |

## Top 3 prioridades

1. **Lembretes reais ou remover o botão** — implementar `WorkManager` + canal de
   notificação + permissão `POST_NOTIFICATIONS`, ou trocar o Snackbar por "em breve".
   Hoje a função mente para o usuário. (achado 1)
2. **Base rolante de feriados** — gerar 2028+ (ou cálculo de feriados móveis) e remover
   o `coerceIn(2026,2027)`; sem isso o app morre em 01/01/2028. (achado 2)
3. **Busca e favoritos por UF/ano** — normalizar mês por extenso, filtrar favoritos com
   `forLocation(ano,uf)` e exibir o ano no card. (achados 3, 4)
