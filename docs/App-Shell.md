# `AppShell` — cascarón de aplicación

> **Estado:** implementado en cts-theme (S1–S4 con la opción recomendada).
> E-Panel **omitido** por decisión del usuario: otra sesión tenía cambios sin
> commit en `Sidebar.tsx`, `Home.tsx` y `Login.tsx` (transición Login → Home).
> **Fuentes:** `cts-manager/frontend/src/layout/AppLayout.tsx` y
> `layout/Sidebar.tsx:420-440` (rama `production`, `7181d5d7`);
> `E-Panel/apps/web/src/pages/Home.tsx`, `Home.styles.ts`,
> `components/organisms/layout/Sidebar.tsx` y `Sidebar.styles.ts`.

Mismo patrón que [`LoginShell`](Login-Shell.md): el cascarón pone el marco, el
estilado y el comportamiento; cada aplicación llena los huecos. Es la versión
consolidada de `AppShell` + `NavRail` (superficie) + `FloatingActions`
(contenedor) + `ContentArea` de
[Instrucciones-Componentes.md](Instrucciones-Componentes.md). El contenido del
rail (zonas 2–5: cabecera, búsqueda, ítems, pie) sigue siendo del consumidor
hasta aprobar esos átomos.

---

## 1. Lo que hacen hoy las dos aplicaciones

| | cts-manager `AppLayout` | E-Panel `Home` |
|---|---|---|
| Marco | fila flex, `100dvh` | grilla 6×2, `100dvh`, solo `main` desplaza |
| Rail | Drawer 256 → **0** + franja de 24 px con botón de reapertura | Drawer 256 → **64** (iconos) |
| Responsivo | no | `temporary` (< md) · `overlay` (≥ md, vertical) · `push` (horizontal) |
| Barra superior | no («nunca AppBar persistente») | `AppBar` transparente: migas, fecha, modo, avatar |
| Flotante | `NotificationBell` | — |
| Contenido | `p: 3`, `overflow: auto` | sin padding, `overflow: auto` |
| Extra | — | una vista pide contraer el rail y espera `CLOSE_MS` antes de montar |

---

## 2. Anatomía

```
┌ rail (zona 1) ─┬──────────── columna (min-width: 0) ──────────────┐
│ [slot: rail]   │ [slot: header] (opcional)        [slot: floating]│
│ 256 ↔ 64 / 0   │──────────────────────────────────────────────────│
│ primary.main / │ main (zona 9) — desplaza — [children]            │
│ paper (oscuro) │                                                  │
└────────────────┴──────────────────────────────────────────────────┘
```

| Modo (`layout`) | Rail | Contenido |
|---|---|---|
| `push` | columna propia; abierto 256, cerrado 64 (`icons`) o 0 (`hidden`) | se reacomoda |
| `overlay` | reserva la franja cerrada; el panel abierto se superpone con velo | no se mueve |
| `temporary` | Drawer modal; nada reservado | ocupa todo; el lanzador va en el `header` |
| `auto` | `< md` → `temporary` · vertical → `overlay` · si no → `push` (E-Panel) | |

Con `collapsedRail="hidden"` y el rail cerrado (fuera de `temporary`), el
cascarón pinta la franja de reapertura de cts-manager (24 px + botón sticky) y
una franja gemela a la derecha.

---

## 3. API pública

```tsx
import { AppShell, useAppShell } from '@industriascts/cts-theme/views'

<AppShell
  rail={<MiRail />}               // contenido del rail (zonas 2–5)
  header={<MiBarra />}            // opcional (S1)
  floating={<Campana />}          // zona 6
  collapsedRail="icons"           // 'icons' (64) | 'hidden' (0 + reapertura)
  layout="auto"                   // 'auto' | 'push' | 'overlay' | 'temporary'
  content="padded"                // 'padded' (gutter 24) | 'bleed' (0)
  railOpen / defaultRailOpen / onRailOpenChange
>
  {vistas}
</AppShell>

// En cualquier slot o vista:
const { railOpen, setRailOpen, toggleRail, layout, collapsedRail, closeMs } = useAppShell()
```

- `defaultRailOpen` por defecto: abierto solo en `push` (donde no tapa nada).
- `closeMs`: lo que tarda en cerrarse el rail en el modo actual; una vista que
  pide contraerlo espera eso antes de montar su contenido.
- Raíz con `data-layout` y `data-rail="open|closed"` para estilos propios.

---

## 4. Valores

| Valor | Fuente | Destino |
|---|---|---|
| ancho 256 / 64 / 0 | Sidebar.tsx (ambas) | `layout.railWidth` / `railIconWidth` / `railCollapsedWidth` |
| fondo `#0065BB` / `#253662` | ambas | `primary.main` / `background.paper` |
| sombra `4px 0 20px rgba(0,0,0,0.2)` | ambas | `shadows.sidebar` |
| transición 0.25s | ambas (E-Panel: `cubic-bezier(0.2,0,0,1)`) | `motion.collapse` + `motion.easing` |
| velo del overlay `rgba(0,0,0,0.25)` | E-Panel Sidebar.styles.ts | `colors.scrim.rail` (nuevo) |
| franja de reapertura 24 · top 12 | AppLayout.tsx:29,34 | `layout.reopenStripWidth` / `layout.reopenTop` (nuevos) |
| hover del botón de reapertura | `#0078d4` / `#2e4275` (fuera de paleta, D13) | **propuesto:** `primary.dark` / `primary.main` |
| padding del contenido | AppLayout.tsx `p: 3` | `spacing.gutter` |
| acciones flotantes top/right 16 | NotificationBell.tsx:171-173 | `layout.floatingTop` / `floatingRight` |

---

## 5. Archivos

| Repo | Archivo | Cambio |
|---|---|---|
| cts-theme | `src/views/AppShell.tsx`, `AppShellContext.ts` | cascarón + contexto |
| cts-theme | `src/views/index.ts` | exporta `AppShell`, `useAppShell` y tipos |
| cts-theme | `src/tokens.ts`, `src/colors.ts` | `reopenStripWidth`, `reopenTop`, `scrim.rail` |
| cts-theme | `smoke/app-shell.tsx` | matriz MUI 6/7/9 |
| cts-theme | `playground/` | Login → entrar → AppShell de ejemplo → cerrar sesión; `#app` conserva la vista al recargar |
| E-Panel | `src/shell/AppShell.tsx`, `AppShellContext.ts` | copia; tokens en `shell/tokens.ts` |
| E-Panel | `pages/Home.tsx` | usa `AppShell` |
| E-Panel | `Sidebar.tsx` | conserva su contenido; el Drawer y lo responsivo pasan al cascarón |
| E-Panel | `TopBar` | va en `header`; en `temporary` el lanzador del rail va a su lado |

**Terminado cuando:** `typecheck:matrix`, `build`, E-Panel `tsc` + vitest
(`Sidebar.test.tsx` conserva sus aserciones, solo cambia el envoltorio de
render) y axe sin violaciones en claro y oscuro.

---

## 6. Decisiones

| # | Decisión | Elegido |
|---|---|---|
| S1 ✅ | Barra superior | slot `header` opcional. **Rompe la regla de la hoja «Estructura»** («nunca AppBar persistente»); cts-manager no lo usa |
| S2 ✅ | Responsivo | se adoptan los modos de E-Panel como comportamiento provisional; toca `Mobile.md` |
| S3 ✅ | cts-manager | solo fuente, no se modifica. E-Panel también quedó fuera en esta entrega |
| S4 ✅ | Nombre y ruta | `AppShell` desde `/views`, junto a `LoginShell` |
| S5 | Hover del botón de reapertura | propuesto `primary.dark` / `primary.main` en vez de los literales sueltos (D13) |
| R1 | Contraste de los tokens `rail.*` (axe sobre el playground) | ver §7 |

---

## 7. Resultado

Playground (`pnpm dev`): Login → «Ingresar» → `AppShell` de ejemplo; `#app`
conserva la vista al recargar; «Cerrar sesión» en el pie del rail vuelve al
login. Comprobado en Chromium (1440×900, 900×1200, 390×844): `push` con
contracción a iconos, modo `hidden` con botón de reapertura, `overlay` con
velo que cierra al hacer clic, `temporary` que cierra con Escape. Sin errores
de consola. `typecheck:matrix` y `build` en verde.

**axe — el cascarón no aporta violaciones.** Las que aparecen vienen de
tokens del sistema que el rail de ejemplo usa tal como están (R1):

| Token | Valor | Contraste | Para 4.5:1 |
|---|---|---|---|
| `rail.itemIdleColor` | blanco α .65 sobre `#0065BB` | 3.38 | α ≥ .83 |
| `rail.itemActiveBg` | blanco α .18 (texto blanco encima) | 4.13 | α ≤ .13 |
| `rail.descriptor` sobre `rail.footerBg` | blanco α .55 sobre `#00569f` | 3.35 | α ≥ .71 |
| `Button` outlined `primary.main` sobre `paper` oscuro | `#0065BB` / `#253662` | 2.01 | `primary.light` → 4.5 (D14) |

Mismos defectos que el `NavRail` real de cts-manager y E-Panel; se corrigen en
los tokens, no en el cascarón.
