# Quem Sou Eu? Adivinha — auditoria rodada 1

- **Stack:** iOS 17, Swift 5, SwiftUI, XcodeGen (`br.com.quemsoueu.adivinha`, v1.2.1 build 8)
- **Núcleo:** `iosApp/Sources/GameEngine/GameEngine.swift` (probabilístico offline) +
  `iosApp/Sources/Views/GameViews.swift` (máquina de estados)
- **Base:** `knowledge.json` com 76 personalidades + 56 perguntas, 100% offline
- **Testes:** `GameEngineTests.swift`, `ProgressStoreTests.swift`

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | Partida não termina após acerto sem guardas de estado | fluxo | crítica | `GameViews.swift:250-295` |
| 2 | Palpite usa só `confidence>=0.68`, sem margem entre candidatos | código | alta | `GameEngine.swift:18-19`, `GameViews.swift:255` |
| 3 | `chooseCandidateIndex` sem validação pode crashar (OOB) | bug | alta | `GameEngine.swift:27-28` |
| 4 | Soma zero de escores não recuperada; `bestGuess` arbitrário | bug | alta | `GameEngine.swift:40-48` |
| 5 | Ausente tratado como `0.5` penaliza 33% sem dado real | código | alta | `GameEngine.swift:37,80-86` |
| 6 | Cobertura sobre massa libera pergunta com 20% de contagem | código | alta | `GameEngine.swift:60-77` |
| 7 | Pergunta obsoleta permanece em `confirming` (VoiceOver + save) | fluxo | média | `GameViews.swift:212-221,307-317` |
| 8 | Salvamento sem versão/expiração; base v2 invalida v1 | fluxo | média | `ProgressModels.swift:18-25` |
| 9 | Rejeição sem `Set` nem limite (`maxRejected`) | código | média | `GameViews.swift:286-296` |
| 10 | Base 100% binária `0/1`; pares diferem em 1 atributo | conteúdo | média | `knowledge.json` |
| 11 | Atributos hierárquicos (`born_before_*`) tratados como independentes | código | média | `GameEngine.swift`, `validate_content.py` |
| 12 | Limite 14 força decisão com confiança baixa em categorias esparsas | fluxo | média | `GameViews.swift:149` |

## Top 3 prioridades

1. **Máquina de estados terminal** — estado `loading`, guardas `canRespond/canConfirm`,
   `isTransitioning` + debounce, `question=nil` ao palpitar, `rejectedIDs` como `Set`
   com `maxRejected=4`. (achados 1, 7, 9)
2. **Política de palpite composta** — extrair `GuessPolicy` pura: `confidence≥0.78`,
   `margin≥0.22`, `ratio≥3.0`, `effectiveCandidates≤3.5` (calibrar no simulador).
   Expor `secondBest/margin/ratio/entropy`. (achado 2)
3. **Invariantes numéricos** — `guard` no índice aleatório, normalização robusta com
   redistribuição sobre não-rejeitados, ausente com verossimilhança uniforme.
   (achados 3, 4, 5)

## Sinais Jev

Nenhum achado deste projeto venceu as 5 perguntas; `qse-indice-oob` ficou em 3º em
risco de crash (0.10). Prioridade vem do auditor + plano `docs/PLANO_MELHORIAS_MOTOR_OFFLINE.md`.
