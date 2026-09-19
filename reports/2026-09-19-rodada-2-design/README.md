# Rodada 2 (design, piloto) — 19/09/2026

Piloto FAANG em 2 apps: **quem sou eu ?** (iOS SwiftUI) e **receitas airfreyr**
(Android Compose). Método: diff spec/mockup × código + 1 chamada Jev (`jev-1.13.0`,
5 `Choice` em paralelo, 4849 in / 767 out). Nenhum código de app foi alterado.

## Veredito Jev

| Pergunta | Vencedor | Confiança |
|---|---|---|
| Maior grito não-FAANG | `rec-tokens` | 0.25 — fraca, revisar |
| Maior fricção UX | `rec-tokens` | 0.59 — moderada |
| Maior inconsistência de marca | `rec-brand` | 0.68 — sólida |
| Mais apelo de loja | `rec-brand` | 0.30 — fraca, revisar |
| Melhor quick win | `rec-tokens` | 0.79 — forte |

## Leitura composta (código + Jev)

1. **Fundação da Airfryer primeiro** — tokens quebrados (`rec-tokens` venceu 3/5) são
   pré-requisito de qualquer tela bonita. Quick win forte (0.79).
2. **Decidir a marca da Airfryer** — mockup vovó (madeira/âmbar/serif dourada) vs
   código laranja flat. Sem essa decisão, todo polimento é chute.
3. **Depois, heróis do Quem Sou Eu** — CTA 90px, bottom nav flutuante lime, resultado
   gamificado; paleta exata do spec já está mapeada em `design-tokens.json`.
4. Revisão humana pendente: qual tela pesa mais em screenshot (`store_appeal` conf 0.30).

## Arquivos

- `quem-sou-eu-design.md` — diff spec × código + plano de componentes
- `receitas-airfryer-design.md` — direção vovó rústica + plano de tokens/telas
- `design-tokens.json` — tokens canônicos dos 2 apps (sem segredos)
