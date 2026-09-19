# Swing Brasília — auditoria rodada 1

- **Stack:** iOS 17, Swift 5, SwiftUI, XcodeGen (`br.com.swingbrasilia.fun`), iPhone-only
- **Conteúdo:** `venues.json` com 25 locais, busca/filtros offline, sem rede/conta
- **Testes:** `VenueCatalogTests.swift`, `AgeGateStoreTests.swift`

> Atenção: nenhum link, invite ou identificador foi reproduzido aqui.

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Licenças de imagem pendentes — bloqueio App Store 5.2.3 **[Jev 0.79]** | conteúdo | crítica | `docs/content/image-credits.json:4` |
| 2 | Age gate burlável por flag + confirmação 1-toque sem fricção | segurança | crítica | `RootView.swift:29`, `AgeGateView.swift:40` |
| 3 | WhatsApp comunidade == negócios (mesmo invite) | segurança | alta | `Data/AppConfig.swift:8` |
| 4 | `NavigationStack` aninhado — navegação quebrada | fluxo | alta | `HomeView.swift:53`, `DirectoryView.swift:14` |
| 5 | Fonte pública falsa (`google.com/search`) + coordenada precisa vs rótulo aproximado | conteúdo | alta | `venues.json:20`, `VenueDetailView.swift:120` |
| 6 | `loadBundled()` falha silenciosa — catálogo vazio sem erro | bug | alta | `VenueCatalog.swift:64` |
| 7 | Dupla confirmação de idade desconectada (`RulesView` ignora `AgeGateStore`) | fluxo | alta | `RulesView.swift:6,90` |
| 8 | `fullScreenCover` com `set: {_ in}` noop | código | média | `RootView.swift:35` |
| 9 | Selo patrocinado sem checar `isSponsored` (risco 5.2.5/FTC) | bug | média | `VenueDetailView.swift:54` |
| 10 | Hero 560pt fixo + `safeAreaPadding(96)` mágico + galeria repetida | design | média | `HomeView.swift:39` |
| 11 | Busca limitada + `count(for:)` recalcula 5x por render | performance | média | `VenueCatalog.swift:42`, `DirectoryView.swift:113` |
| 12 | `DEVELOPMENT_TEAM` hardcoded + versão manual | código | baixa | `iosApp/project.yml:9` |

## Top 3 prioridades

1. **Aprovação na loja** — regularizar autor/licença das 7 imagens (hero sugestiva
   primeiro), remover backdoor `SWING_SKIP_AGE`, exigir data de nascimento + 2º passo
   e re-checagem no age gate. Sem isso, rejeição quase certa. (achados 1, 2)
2. **Dados e moderação** — invites separados (comunidade vs negócios), fontes reais por
   local (nunca `google.com/search`), coerência entre coordenada e rótulo de
   privacidade, unificar aceite das regras no `AgeGateStore`. (achados 3, 5, 7)
3. **Navegação e robustez** — um `NavigationStack` por aba, erro/log em `loadBundled`,
   badge patrocinado só com `isSponsored==true`, hero responsivo. (achados 4, 6, 9, 10)
