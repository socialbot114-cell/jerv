# City Bikes Premium — auditoria rodada 1

- **Stack:** React 19 + TypeScript 5.9 + Vite 5.4 + Capacitor 7.6.8 (Web + Android + iOS)
- **Dados:** api.citybik.es, Open-Meteo, USGS, Open Charge Map, Overpass, OSRM (tudo remoto)
- **Testes:** `navigation.test.ts` (vitest) — sem suite de componentes/fluxo

## Achados

| # | Título | Cat. | Sev. | Local |
|---|---|---|---|---|
| 1 | `BrowserRouter` quebra deep-link/reload na WebView Capacitor | fluxo | crítica | `src/App.tsx:31` |
| 2 | Nenhum cache offline/fallback para lista de redes | bug | crítica | `src/api/citybikes.ts:28`, `CityBikesContext.tsx:84` |
| 3 | Context `Provider value` sem `useMemo` re-renderiza tudo | performance | alta | `CityBikesContext.tsx:204` |
| 4 | Leaflet: `prototype` global + `mapRef` em `useState` (loop renders) | performance | alta | `MapComponent.tsx:29,75` |
| 5 | `TileLayer` OSM sem cache, retry ou tile de erro offline | bug | alta | `MapComponent.tsx:344` |
| 6 | `SplashScreen.hide()` no import, antes do React pronto | fluxo | alta | `src/main.tsx:21` |
| 7 | `requestLocation()` trava após `granted`, impede re-centralizar | fluxo | alta | `CityBikesContext.tsx:180` |
| 8 | Precipitação sempre `0`, dado horário ignorado | bug | média | `src/api/smartCity.ts:65` |
| 9 | OpenChargeMap sem `X-API-Key` (401/429); chave no front vazaria | código | média | `src/api/smartCity.ts:132` |
| 10 | Overpass via `GET` com query concatenada (414/CORS), POIs ignorados | performance | média | `src/api/smartCity.ts:176` |
| 11 | `VITE_SWETRIX_PID` real commitado no exemplo + `origin` ao Google | segurança | média | `.env.example:1`, `navigation.ts:3` |
| 12 | Overlays `z-index` cobrem o mapa no mobile 320px; busca bloqueada no load | design | média | `MapComponent.tsx:125`, `NetworkSearch.tsx:50,69` |

## Top 3 prioridades

1. **Roteador + splash + offline primeiro** — `HashRouter`, `hide()` após mapa pronto,
   persistir última lista de redes (React Query persist + `localStorage`) e tiles com
   fallback. Sem isso o app abre vazio/tela branca no caso mais comum (rua, sem rede).
   (achados 1, 2, 5, 6)
2. **Performance do mapa** — `useMemo` no context, `useRef` + `mergeOptions` no Leaflet,
   Overpass via `POST`, busca completa de POIs. (achados 3, 4, 10)
3. **Dados e chaves** — precipitação real, proxy/backend para OpenChargeMap (nunca chave
   no front), rotacionar o PID vazado, consentimento de localização explícito.
   (achados 8, 9, 11)
