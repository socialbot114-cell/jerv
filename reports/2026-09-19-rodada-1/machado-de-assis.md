# Machado de Assis — auditoria rodada 1

- **Stack:** KMP + Android nativo + iOS SwiftUI + site (template mais completo)
- **Conteúdo:** 30 obras integrais (Wikisource CC BY-SA), gzip `.json.gzdata`, Room FTS4
- **Testes:** `CatalogTest`, `DatabaseTest` (Robolectric), `PreferencesTest`, `LibraryModelsTest`

> Atenção: valores de segredos NÃO são reproduzidos aqui — apenas a existência do problema.

## Achados (próprios + compartilhados com CATECISMO)

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Keystore de release versionado no repo **[Jev segurança 0.95]** | segurança | crítica | `machado-release.keystore` + `keystore.properties` |
| 2 | Segredos Apple expostos no `PROJECT_STATUS.md` | segurança | crítica | `PROJECT_STATUS.md:55-65` |
| 3 | `postCompileScripts` reescreve versão/ícone a cada build iOS | bug | alta | `iosApp/project.yml:52,65,77-78` |
| 4 | `shared/LibraryModels.kt` morto e divergente das plataformas | código | alta | `LibraryModels.kt:54-62` |
| 5 | Busca integral síncrona na MainActor trava a UI | performance | média | `LibraryViewModel.swift:193-207` |
| 6 | `SpeechReader` sem `didCancel` + import divergente do CATECISMO | bug | média | `SpeechReader.swift:1-2,102-113` |

## Top 3 prioridades

1. **Remover segredos do repo** — mesma ação do CATECISMO (keystore + valores Apple),
   pois compartilham o mesmo vazamento. (achados 1, 2)
2. **Build iOS reproduzível** — remover `PlistBuddy Set` do `postCompileScripts`;
   versão única no topo do `project.yml`. (achado 3)
3. **Busca em background** — mover decodificação dos 30 JSON para fila background com
   cancelamento por obra; unificar `SpeechReader`/`normalize` entre os dois apps.
   (achados 4, 5, 6)
