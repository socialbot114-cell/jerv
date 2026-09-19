# Receitas Airfryer — plano design FAANG (rodada 2)

Referência: `reffffs/receitas da vovo kit/start receitas vovo.png` — cena quente
rústica: airfryer preta hero, placa de madeira "Receitas Airfryer da Vovó", serif
dourada, tomate/manjerico/luz âmbar. Direção: **rústico premium**, não laranja flat.

## Diff mockup × código (o que está feio)

| Área | Código atual (`MainActivity.kt`) | Direção vovó |
|---|---|---|
| Tokens | 7 cores soltas (`Orange 0xFFF26A21`…), `PaleOrange` ≈ `Cream` (delta 5%), radius 14–32 aleatórios, sem elevation | paleta `design-tokens.json`: ember/amber/gold/cream/crust + radius 26/20/18 + elevation 2/4/6 |
| Cards | brancos flat, `CardDefaults` sem sombra | sombra quente + borda sutil; hero com foto real |
| Capas | 14/30 sem `imageKey` caem em `Canvas` procedural | cobertura total (foto ou ilustração quente, nunca placeholder frio) |
| CTA | 52–56px laranja, hierarquia fraca | primário ember 56px + card Ink no modo cozinhar (já bom em `:333`) como padrão |
| Tipo | sp soltos 9–58, Black/Bold ad-hoc | display serif (marca vovó) + corpo sans + eyebrow tracked |
| Marca | laranja flat genérico | madeira/âmbar/serif dourada, noite quente |

## Ordem de implementação

1. **Tokens** — `ReceitasTheme` com a paleta/radius/elevation/tipo do JSON; remover
   `PaleOrange` redundante. **[Jev quick win 0.79]**
2. **Decisão de marca (humano)** — confirmar rústico vovó vs laranja atual antes de
   polir telas. **[Jev brand 0.68]**
3. **Hero + capas** — `HeroRecipeCard` com sombra/elevation, `imageKey` nas 14
   restantes; grid adaptativo no tablet.
4. **Modo cozinhar como padrão** — estender o dark card `:333` (temperatura ouro 34sp,
   timer 58sp) para detalhe e resultado.
5. **Display serif** — importar serif para títulos de marca; manter sans no corpo.

## Sinais Jev

`rec-tokens` venceu visual (0.31, conf baixa), fricção (0.63) e quick win (0.81);
`rec-brand` venceu marca (0.71) e loja (0.34, conf baixa). Revisão humana pendente:
qual tela pesa mais em screenshot.
