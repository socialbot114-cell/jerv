# Quem Sou Eu? — plano design FAANG (rodada 2)

Meta: sair do MVP `DesignSystem.swift:1-205` (CTA 52px, sombra 0.08/18, radius 22)
para o spec `quem_sou_eu_design_spec_mockups.md` (933 linhas, 15 PNGs 941×1672).

## Diff spec × código (o que está feio)

| Área | Código atual | Spec | Gap |
|---|---|---|---|
| Paleta | violet ~`#6320F0`, canvas grouped | `#21104F` fundo, `#6C22E8` CTA, `#B8FF35` | hex diverge; falta roxo profundo |
| CTA | 52px Capsule, sem sombra colorida | 90–110px, radius 30, círculo lime + seta, sombra roxa + inset | metade da altura, sem dominância |
| BottomNav | `ultraThinMaterial` + divider | pill flutuante, ativo lime + label escuro | totalmente divergente |
| Resultado | card genérico, `+20 moedas` texto | pill CONFIRMADO + 3 mini-cards + banner mascote + confetes | gap de gamificação mais crítico |
| Home | 2 chips, mascote em card | trio pastel (sequência/moedas/pontos) + speech bubble + 3 cards | falta celebração e progresso |
| Tipo | só SF system | Nunito/Fredoka/Baloo 800–900, 36–52px | sem fonte custom |
| Mascote | 1 estado + float | 6 estados (curioso/comemorando/…) | sem variação por tela |
| Splash | inexistente | `backgroud 1 tela.png`: blobs + onda lime | sem branding de entrada |

## Ordem de implementação

1. **Tokens exatos** — trocar `Palette` pelos hex de `design-tokens.json`, radius
   28/30/32, sombras com inset; 1 arquivo, impacto global. (quick win)
2. **CTA hero 90px** — novo `PrimaryHeroButtonStyle` com círculo lime + seta;
   manter o atual como secundário.
3. **BottomNav flutuante** — pill lime no ativo, blur leve, sem divider.
4. **Resultado gamificado** — pill CONFIRMADO + `RewardCard` ×3 + banner lilás.
5. **Home completa** — trio pastel + `SpeechBubble` + 3 cards secundários.
6. **Mascote e splash** — 6 estados + splash dedicada (precisa de ilustrador para
   os estados; PNGs atuais são AI-generated, ok como ref, não final).

## Sinais Jev

Nenhum gap deste app venceu; `qse-palette` foi 2º–3º em 3 perguntas. Leitura: a
fundação da Airfryer bloqueia mais; aqui o caminho é incremental por componente.
