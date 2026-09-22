# Instrucciones — componentes de layout (zonas 1–10)

Especificación de implementación de los 13 componentes de estructura. Los
valores son **literales** de `docs/demo/build.py` (funciones `v_*`);
la regla de oro sigue vigente: **no redondear ni aproximar**.

La base ya está construida y verificada: `src/tokens.ts`, `src/colors.ts`,
`src/mui/theme.ts` + `augmentation.ts`. Ningún componente debe re-declarar un
valor que ya esté en `tokens.ts`.

---

## 0. Reglas del piso

### Estilado: `sx`, leyendo del tema

Decidido así por la hoja «Portada» (*createTheme + sx*). `theme.cts` expone
todos los tokens dentro de cualquier `sx` gracias a `src/mui/augmentation.ts`:

```tsx
<Box sx={(t) => ({
  height: t.cts.density.navItem,              // 34
  borderRadius: `${t.cts.radii.control}px`,   // 8
  transition: `background ${t.cts.motion.nav} ${t.cts.motion.easing}`,
})} />
```

Nunca escribir `34`, `#0065BB` ni `0.15s` a mano en un componente. Si un valor
falta en `tokens.ts`, se añade allí citando la hoja de la que sale.

### Compatibilidad MUI 6 · 7 · 9 — lista de prohibiciones

`peerDependencies` declara `^6 || ^7 || ^9`, y `pnpm typecheck:matrix` lo
comprueba de verdad contra 6.5.0, 7.3.11 y 9.4.0. Para que siga verde:

| Prohibido | Motivo |
|---|---|
| `Grid` de MUI | renombrado en 7 (`Grid2`→`Grid`); `GridLegacy` eliminado en 9. Usar flex/grid CSS: un shell de flex nunca lo necesitó. |
| `componentsProps` / `slotProps` | consolidados en 7. Exponer props propias explícitas, no reenviar slots. |
| imports profundos de 2.º nivel (`@mui/material/Button/Button`) | eliminados en 7. Importar desde la raíz. |
| `extendTheme` · `CssVarsProvider` · `theme.vars` | movidos/fusionados entre majors. Leer de `theme.cts`, no de `theme.vars`. |

Componentes MUI sí permitidos (verificados presentes en los tres):
`Box`, `Stack`, `Typography`, `Avatar`, `Chip`, `IconButton`, `Paper`,
`Divider`, `Drawer`, `useMediaQuery`, `styled`, `useTheme`, `alpha`.

### Gotcha de empaquetado: TS2742

Con pnpm, un componente exportado **sin tipo de retorno anotado** puede romper
la emisión de `.d.ts`:

```
error TS2742: The inferred type of 'X' cannot be named without a reference to
'.pnpm/@mui+types@.../node_modules/@mui/types'
```

Detectado ya en este repo. **Anotar siempre el retorno** de cada componente
exportado (`): React.JSX.Element`), o el `build` fallará aunque el
`typecheck` pase.

### Móvil

Cada componente marcado abajo lleva su eje móvil ya en la firma, pero **solo
renderiza el valor de escritorio ratificado**. No inventar valores móviles:
ver `MOBILE-TBD.md` y sus 9 conflictos abiertos.

### Convenciones comunes

- Todos aceptan `sx` y `className` (vía de escape).
- Todos aceptan `children` salvo indicación.
- Nombres de archivo en `src/layout/`, un componente por archivo.
- Sin estado global: `NavRail` usa contexto propio, nada de Redux/zustand.

---

## 1. `AppShell` — contenedor del shell

`src/layout/AppShell.tsx` · hoja «Estructura»

Raíz de toda vista CTS. Fila flex: rail a la izquierda, contenido a la derecha.

| Prop | Tipo | Defecto | Nota |
|---|---|---|---|
| `rail` | `ReactNode` | — | zona 1 |
| `children` | `ReactNode` | — | zonas 6–10 |

```
display: flex
height: 100dvh            (no 100vh: 100dvh evita el salto de la barra móvil)
overflow: hidden
background: palette.background.default   // #f0f4f9 / #2A3547
```

La columna de contenido es `flex-grow: 1; min-width: 0; display: flex;
flex-direction: column; overflow: hidden`. **`min-width: 0` es obligatorio**:
sin él, una tabla ancha en la zona 9 empuja el shell y rompe el rail.

> **Regla de la hoja:** *nunca AppBar persistente*. El rail y las acciones
> flotantes son todo el chrome. `AppShell` no tiene ranura superior.

---

## 2. `NavRail` — zona 1

`src/layout/NavRail.tsx` · hoja «Navegación»

| Prop | Tipo | Defecto | Nota |
|---|---|---|---|
| `variant` | `'permanent' \| 'collapsed' \| 'temporary'` | `'permanent'` | **eje móvil** — hoy solo implementar `permanent` y `collapsed` |
| `open` | `boolean` | — | controlado |
| `defaultOpen` | `boolean` | `true` | no controlado |
| `onOpenChange` | `(open: boolean) => void` | — | |

```
width: cts.layout.railWidth           // 256  (colapsado: 0)
background: palette.primary.main      // #0065BB claro · #253662 oscuro
color: #ffffff
boxShadow: cts.shadows.sidebar        // 4px 0 20px rgba(0,0,0,0.2)
border: none                          // la sombra sustituye al borde
display: flex; flex-direction: column
overflow: hidden
flex-shrink: 0
transition: width 0.25s cubic-bezier(0.32, 0.72, 0, 1)
```

> **Cuidado con la hoja «Navegación»:** ahí el rail se dibuja con
> `border-radius: 12px` porque es un espécimen aislado sobre fondo claro. En el
> shell real (hoja «Estructura») va a sangre contra el borde izquierdo:
> **sin radio**.

El texto interior **no** usa `palette.text.*`: usa los blancos con alfa de
`cts.rail.*`, porque vive sobre la losa azul.

Exportar también `NavRailProvider` / `useNavRail()` para que el FAB de
reapertura (zona 6) pueda abrir el rail sin *prop drilling*.

---

## 3. `NavRailHeader` — zona 2

`src/layout/NavRailHeader.tsx`

| Prop | Tipo | Nota |
|---|---|---|
| `logo` | `ReactNode` | `<img>` de 34 px |
| `wordmark` | `string` | p. ej. `"W-FLOW"` |
| `descriptor` | `string` | p. ej. `"Gestión de flujos"` |

```
display: flex; align-items: center; gap: 12px
padding: 24px 24px 16px 24px
borderBottom: 1px solid cts.rail.divider      // rgba(255,255,255,0.1)

logo       → width: cts.density.railLogo      // 34, height auto
wordmark   → 17px / 900 / letterSpacing 2px / #fff / line-height 1.1
descriptor → 9.5px / cts.rail.descriptor      // rgba(255,255,255,0.55)
```

El 900 del wordmark es el único uso de Black en el sistema.

---

## 4. `NavRailSearch` — zona 3

`src/layout/NavRailSearch.tsx`

| Prop | Tipo | Defecto | Nota |
|---|---|---|---|
| `variant` | `'search' \| 'workspace'` | `'search'` | 34 px vs 42 px |
| `placeholder` | `string` | `'Buscar…'` | |
| `value` / `onChange` | | | controlado |

```
contenedor → padding: 12px 16px 6px 16px
campo      → height: 34  (workspace: 42)
             background: cts.rail.searchBg        // rgba(255,255,255,0.08)
             border: 1px solid cts.rail.searchBorder  // rgba(255,255,255,0.15)
             borderRadius: cts.radii.base         // 10 — no 8
             padding: 0 10px
             fontSize: 12.5
             color: #fff
             ::placeholder → cts.rail.searchPlaceholder  // rgba(255,255,255,0.4)
```

Radio 10, no 8: es la excepción a «inputs = 8» de la hoja «Controles», porque
aquí el campo vive en el rail. Opcional según la app.

---

## 5. `NavSection` — zona 4

`src/layout/NavSection.tsx`

| Prop | Tipo |
|---|---|
| `title` | `string` |
| `children` | `NavItem[]` |

```
título → padding: 10px 20px 4px 20px
         fontSize: cts.fontSize.sectionTitle     // 10
         fontWeight: 700
         textTransform: uppercase
         letterSpacing: cts.letterSpacing.sectionTitle   // 0.1em
         color: cts.rail.sectionTitle            // rgba(255,255,255,0.45)
```

Separador entre secciones: `height 1px · background cts.rail.divider ·
margin 10px 16px`.

---

## 6. `NavItem` — zona 4

`src/layout/NavItem.tsx` · **el componente con los estados más exactos del sistema**

| Prop | Tipo | Nota |
|---|---|---|
| `icon` | `ReactNode` | 18×18 |
| `label` | `string` | |
| `active` | `boolean` | |
| `href` / `onClick` | | polimórfico: `component` prop para el Link del router |

```
display: flex; align-items: center; gap: 10px
height: 34 · margin: 0 12px 2px 12px · padding: 0 12px
borderRadius: 8 · fontSize: 13.5 · fontWeight: 600
transition: background 0.15s cubic-bezier(0.32, 0.72, 0, 1)

activo   → background: rgba(255,255,255,0.18)
           borderLeft: 3px solid rgba(255,255,255,0.9)
           color: #ffffff
hover    → background: rgba(255,255,255,0.1)
           borderLeft: 3px solid transparent
           color: #ffffff
inactivo → background: transparent
           borderLeft: 3px solid transparent
           color: rgba(255,255,255,0.65)
```

**El `borderLeft` de 3px existe siempre**, transparente cuando no está activo.
Si se añade solo en activo, el texto salta 3 px al seleccionar.

---

## 7. `NavRailFooter` — zona 5

`src/layout/NavRailFooter.tsx`

| Prop | Tipo |
|---|---|
| `name` / `role` | `string` |
| `avatar` | `ReactNode \| string` (iniciales) |
| `onLogout` | `() => void` |

```
display: flex; align-items: center; gap: 12px
padding: 12px 16px
marginTop: auto                        // anclado abajo (la hoja dibuja 8px)
borderTop: 1px solid cts.rail.divider
background: cts.rail.footerBg          // rgba(0,0,0,0.15)

avatar → 32×32 · borderRadius 50%
         background: cts.rail.avatarBg       // rgba(255,255,255,0.2)
         border: 2px solid cts.rail.avatarBorder  // rgba(255,255,255,0.35)
         fontSize 11 / 700
nombre → 12.5 / 700 / #fff · line-height 1.3
rol    → 10.5 / opacity 0.5
logout hover → background cts.rail.logoutHoverBg   // rgba(255,100,100,0.2)
               color      cts.rail.logoutHoverColor // rgba(255,180,180,1)
```

`marginTop: auto`, no posición fija: el rail ya es una columna flex.

---

## 8. `FloatingActions` — zona 6

`src/layout/FloatingActions.tsx`

Envuelve cada hijo en un círculo de papel. Sustituye a la barra superior.

```
contenedor → position: fixed; top: 16; right: 16
             display: flex; gap: 8px; align-items: center
             zIndex: por encima del contenido, por debajo de modales

círculo    → 38×38 · borderRadius 50%
             background: palette.background.paper
             border: 1px solid palette.divider
             boxShadow: cts.shadows.floatingAction   // 0 1px 4px rgba(0,0,0,0.06)

badge      → position absolute · top -4 · right -4
             minWidth 16 · height 16 · borderRadius 8
             background: palette.error.main · color #fff · 10px / 700
```

Contenido típico: campana de notificaciones + conmutador de tema + perfil.
**Conflicto móvil 3** (`MOBILE-TBD.md`): choca con el FAB de reapertura del
rail y con `safe-area-inset`. No resolver aquí por cuenta propia.

---

## 9. `Breadcrumbs` — zona 7

`src/layout/Breadcrumbs.tsx`

No usar el `Breadcrumbs` de MUI: sus separadores y tipografía no coinciden.

```
display: flex; align-items: center; gap: 6px
fontSize: 13 · marginBottom: 8

enlaces → fontWeight 500 · color palette.text.secondary
          hover → textDecoration: underline
último  → fontWeight 700 · color palette.text.primary · sin enlace
separador → "/" · color palette.text.secondary
```

Va **dentro del contenido**, sobre el título — nunca en una barra propia.

---

## 10. `ViewHeader` — zona 7

`src/layout/ViewHeader.tsx`

| Prop | Tipo | Nota |
|---|---|---|
| `title` | `string` | |
| `breadcrumbs` | `ReactNode` | el componente 9 |
| `count` | `number` | chip de conteo |
| `actions` | `ReactNode` | a la derecha |

```
breadcrumbs (mb 8)
fila → display: flex; align-items: center; justify-content: space-between
       título → variant h5 · fontWeight 700
       chip de conteo → height 20 · radius 6 · tinte del color + '20'
borderBottom: 1px solid palette.divider
marginBottom: cts.layout.viewHeaderMarginBottom   // 24
```

---

## 11. `ViewToolbar` — zona 8

`src/layout/ViewToolbar.tsx`

| Prop | Tipo |
|---|---|
| `search` / `filters` / `actions` | `ReactNode` |

```
display: flex; align-items: center; gap: 8px
todos los controles → height: cts.density.toolbarControl   // 32
búsqueda → width: 200
selects  → minWidth 135 · maxWidth 185
CTA      → variant contained, empujado a la derecha (marginLeft: auto)
fontSize: 13
```

> **Regla de la hoja:** *un solo CTA primario por vista*, y vive aquí. Si una
> vista necesita dos acciones sólidas, una de las dos está mal.

**Conflicto móvil 4**: a 360 px no cabe. Sin resolver.

---

## 12. `ContentArea` — zona 9

`src/layout/ContentArea.tsx`

| Prop | Tipo | Defecto | Nota |
|---|---|---|---|
| `variant` | `'padded' \| 'bleed'` | `'padded'` | `bleed` = editor de lienzo |

```
flex-grow: 1 · min-height: 0 · overflow: auto
padded → padding: cts.spacing.gutter     // 24  (p: 3)
bleed  → padding: 0                      // variante C, lienzo a sangre
```

`min-height: 0` es obligatorio por lo mismo que `min-width: 0` en `AppShell`.

Separación entre cards dentro: 16–24 px (`cts.spacing.cardGapMin/Max`).

---

## 13. `SidePanel` — zona 10

`src/layout/SidePanel.tsx`

| Prop | Tipo | Defecto | Nota |
|---|---|---|---|
| `width` | `number` | `320` | rango ratificado 300–360 |
| `side` | `'left' \| 'right'` | `'right'` | izquierda = catálogo (variante C) |
| `variant` | `'inline' \| 'overlay'` | `'inline'` | **eje móvil** — hoy solo `inline` |

```
width: clamp(cts.layout.panelMinWidth, width, cts.layout.panelMaxWidth)
flex-shrink: 0 · overflow: auto
background: palette.background.paper
borderLeft: 1px solid palette.divider      // borderRight si side='left'
```

> **Regla de la hoja:** el rail (1) nunca duplica contenido del panel (10).

---

## Orden de implementación

1. `AppShell` + `ContentArea` — el esqueleto, comprobable al instante.
2. `NavRail` + contexto, luego 3 → 4 → 5 → 6 → 7 (de fuera adentro).
3. `Breadcrumbs` → `ViewHeader` → `ViewToolbar`.
4. `SidePanel`.
5. `FloatingActions` al final: depende del contexto del rail.

## Definición de terminado

- [ ] `pnpm typecheck:matrix` verde en 6 · 7 · 9
- [ ] `pnpm build` emite `.d.ts` sin TS2742
- [ ] Ningún literal numérico ni hex fuera de `tokens.ts` / `colors.ts`
- [ ] Cada componente exportado con tipo de retorno anotado
- [ ] `smoke/` ampliado con el componente nuevo
- [ ] Comparación visual contra su artboard:
      `google-chrome --headless=new --window-size=1440,1600 --screenshot=/tmp/x.png docs/demo/artboards/Estructura.dc.html`
- [ ] Si se tocó un eje móvil, `MOBILE-TBD.md` actualizado
