# CATECISMO — auditoria rodada 1

- **Stack:** KMP (Kotlin 2.0.21) + Android + iOS SwiftUI + site (fork do Machado)
- **Conteúdo:** 8 guias autorais (Credo, sacramentos etc.), leitura paginada, busca, TTS
- **Testes:** `LibraryModelsTest.kt` (KMP jvmTest)

> Atenção: valores de segredos NÃO são reproduzidos aqui — apenas a existência do problema.

## Achados (próprios + compartilhados com Machado)

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Keystore de release versionado no repo **[Jev segurança 0.95]** | segurança | crítica | `machado-release.keystore` + `keystore.properties` |
| 2 | Segredos Apple expostos no `PROJECT_STATUS.md` | segurança | crítica | `PROJECT_STATUS.md:55-65` |
| 3 | `PROJECT_STATUS.md` é cópia do Machado (bundle, 30 obras) | conteúdo | crítica | `PROJECT_STATUS.md:1,19,115` |
| 4 | Bundle/applicationId com maiúsculas | bug | alta | `app/build.gradle:12`, `iosApp/project.yml:3,9` |
| 5 | Progresso só ao "Concluir capítulo", sem retomar página | fluxo | alta | `LibraryViewModel.swift:44-47` |
| 6 | `addQuote` permite duplicatas | bug | alta | `LibraryViewModel.swift:52` |
| 7 | `shared/LibraryModels.kt` morto e divergente das plataformas | código | alta | `LibraryModels.kt:54-62` |
| 8 | Busca iOS superficial e sem debounce | fluxo | média | `ContentView.swift:155-158` |
| 9 | Leitor sem paginação/tema/fonte/TTS avançado (fork regrediu) | design | média | `ContentView.swift:302-350` |
| 10 | `SpeechReader` sem `didCancel`; interrupção trava `isSpeaking` | bug | média | `SpeechReader.swift:102-113` |
| 11 | `project.yml` lista 8 JSON um-a-um; validador só checa `len==8` | código | média | `iosApp/project.yml:32-48` |
| 12 | `tools/*.py` ainda machadianos (30 obras, OUT errado) | conteúdo | baixa | `tools/fetch_machado.py:201` |

## Top 3 prioridades

1. **Remover segredos do repo** — `git filter-repo` no keystore, apagar valores Apple do
   `PROJECT_STATUS.md`, rotacionar chave de assinatura. (achados 1, 2)
2. **Corrigir identidade do app** — bundle minúsculo, `PROJECT_STATUS.md` próprio com os
   8 guias, scripts adaptados ao Catecismo. (achados 3, 4, 12)
3. **Paridade com o Machado** — progresso por página, dedup de citações, busca com
   `folding` + debounce, leitor com tema/fonte/TTS. (achados 5, 6, 8, 9)
