# Estándares globales — auditoría y decisiones

> **Estado:** decisiones G1–G12 **tomadas** e implementadas en cts-theme
> (2026-11-13). Falta la adopción en cada app (§4).
> Reglas resultantes: [Filosofia.md](Filosofia.md). Guía de uso:
> [Nueva-App.md](Nueva-App.md).
> **Apps auditadas (solo lectura):**
>
> | App | Carpeta | Versión | Stack |
> |---|---|---|---|
> | cts-manager (W-Flow) | `frontend` | rama `production` `50010f9` | React 19 · MUI 7.3.9 |
> | E-Panel | `apps/web` | `main` `14c34615` | React 19 · MUI 6.4 |
> | t-monitor | `frontend` | `baf19d1` | React 18 · MUI 7.3 |
> | t-monitor | `config-generator` | `baf19d1` | React 18 · MUI 5.15 |
> | t-monitor | `hmi-configurator` | `baf19d1` | React 18 · sin MUI, CSS propio |
> | E-Panel y t-monitor | `packages/cts-hmi-symbols` | — | compartido |
>
> Los conteos salen de `grep` sobre `.ts/.tsx/.css` y excluyen tests. Los
> valores son literales, como pide la [regla de oro](../README.md#regla-de-oro).

## Resumen

1. **Ninguna app consume cts-theme todavía.** Cada una tiene su propio tema.
2. **cts-manager y E-Panel ya comparten el estándar.** Su paleta es idéntica a
   `src/colors.ts`, y sus `theme.components` son casi iguales entre sí.
   Duplican unas 200 líneas de overrides que cts-theme todavía no ofrece. Es
   la ganancia más grande y la más barata.
3. **t-monitor tiene su propio estándar.** Usa grises *slate* de Tailwind, un
   secundario gris, radio 8 y un fondo claro distinto. `hmi-configurator` tiene
   un tercer sistema en variables CSS.
4. **No existe un estándar de colores de estado.** El verde de «OK» tiene 7
   valores entre las apps, y las alarmas y los símbolos HMI tienen colores
   propios.
5. **La deuda está en los valores sueltos, no en el tema.** Hay más de 4.000
   colores literales y unos 3.500 `fontSize` numéricos en total. Ninguna app
   tiene una regla de lint que lo impida.

---

## 1. Comparación

### 1.1 Paleta

| Rol | cts-theme | cts-manager | E-Panel | t-monitor `frontend` | `config-generator` | `hmi-configurator` |
|---|---|---|---|---|---|---|
| primary | `#0065BB` | = | = | = | = | `--cts-blue #0065bb` |
| primary.dark | `#004696` | = | = | **`#004EA3`** | **`#004EA3`** | **`#004d9e`** |
| primary.light | `#29ABE2` | = | = | **`#3B82F6`** | **`#3B82F6`** | **`#89aedc`** |
| secondary | `#29ABE2` | = | = | **`#64748b`** (slate) | **`#64748b`** | — |
| bg claro | `#f0f4f9` | = | = | **`#FAFBFC`** | ≈ frontend | **`#f4f7fb`** |
| bg oscuro | `#2A3547` / `#253662` | = | = | = | = | **`#0c1420` / `#111b2b`** |
| texto claro | `#1a2236` / `#5a6a80` | = | = | **`#374151` / `#64748b`** | ≈ frontend | **`#1a1a1a` / `#646464`** |
| texto oscuro | `#e8edf4` / `#a6b4c8` | = | = | **`#ffffff` / `#94a3b8`** | ≈ frontend | — |
| success claro | `#00c875` | = | = | **`#10b981`** | = frontend | **`#16a34a`** |

En negrita: valores que difieren de cts-theme. E-Panel guarda además una paleta
paralela en `theme/colors.ts` (`useColors()`, 1.139 lecturas frente a 29 del
tema MUI). Ahí define `textDisabled`, `save`, `topBar`, `dataBoard` y otros
roles que cts-theme no tiene.

### 1.2 Tipografía y forma

| | cts-theme | cts-manager | E-Panel | t-monitor `frontend` | `config-generator` | `hmi-configurator` |
|---|---|---|---|---|---|---|
| Cuerpo | Titillium Web | = | = | Titillium, Arial | **Inter** (no se carga) | Titillium |
| Títulos h1–h6 | sin familia | sin familia | **Conthrax 700** | **Conthrax 700/600** | — | Conthrax |
| body1 / body2 | 15 / 13 | = | = | **14 / 12** | — | 14 |
| Pesos cargados | 300–700 | 300–700, pero usa **500, 800 y 900** | 300–700 | **solo 400 + Conthrax Bold** | ninguno | 300–700 |
| `borderRadius` | 10 | 10 | 10 | **8** | **8** | **6 / 10** |
| Card | sin sombra | sin sombra | sin sombra | **`0 0 10px 2px rgba(10,10,10,0.1) !important`** | sombra propia | — |

### 1.3 Shell y layout

| | cts-theme `AppShell` | cts-manager | E-Panel | t-monitor `frontend` | `config-generator` | `hmi-configurator` |
|---|---|---|---|---|---|---|
| Rail abierto | 256 | 256 | 256 | **250** | **260** | **220** |
| Rail cerrado | 0 / 64 | 0 | 64 | **80** | temporary | fijo |
| Barra superior | opcional | no | AppBar transparente 4rem | **barra inferior** 9.2vh | AppBar | header 52 |
| Padding de página | 24 | `p: 3` (12 en móvil) | `{xs:2, md:3}` | margen 2rem + 24 | — | 28 |
| Easing | `cubic-bezier(0.32,0.72,0,1)` | `ease`, `(0.16,1,0.3,1)` | `(0.2,0,0,1)` | `0.3s ease` | — | — |

### 1.4 Colores de estado

| Significado | cts-manager / E-Panel | t-monitor `frontend` | `cts-hmi-symbols` | `hmi-configurator` | E-Panel (fuera del tema) |
|---|---|---|---|---|---|
| OK / en marcha | `#00c875` | `#4caf50` | `#16A34A` | `#16a34a`, `#2e7d32` | `#0a9d5a` (guardar), `#4ade80`, `#16a34a` |
| Advertencia | `#fdab3d` | `#ff9800`, `#FFA500` | `#F59E0B` (bloqueado), `#FF9800` (disparado) | `#f57c00` | `#f59e0b`, `#d97706` |
| Falla / error | `#e2445c` | `#f44336`, `#d18282` | `#DC2626` | `#dc2626` | `#DC2626` |
| Fuera de línea / inactivo | — | `#8F8F8F` | `#9CA3AF`, `#64748B` | — | `#93a8c9`, `#64748b` |
| Selección | — | — | `#2563EB` | `#1976d2` | `#2563eb` |

La paleta `data8` de cts-theme no se usa en E-Panel. `useManufacturerForm.ts`
tiene su propia paleta de 8 colores.

### 1.5 Métodos de estilado y valores sueltos

| | cts-manager | E-Panel | t-monitor `frontend` | `config-generator` | `hmi-configurator` |
|---|---|---|---|---|---|
| `sx` | 6.758 | 1.676 | 508 | 249 | 0 |
| Archivos `*.styles.ts` | 0 | 133 | 0 | 0 | — |
| `styled()` | 0 | 0 | 18 | 0 | — |
| `style={{}}` inline | 175 | 17 | 24 | 0 | 338 |
| Hex literales | 1.288 | 453 (168 de dominio) | 310 | 85 | 48 |
| `fontSize` literales | 2.847 | 454 | 135 | 25 | 76 |
| Ternarios `isDark ?` | 171 | (vía `C.*`) | — | — | — |
| `zIndex` | 1–10 y 1100–2100 sueltos | 1400–1600 sueltos | 1000–1400 sueltos | 1 | 2 |

### 1.6 Funciones de MUI prohibidas en [Filosofia.md](Filosofia.md)

| | cts-manager | E-Panel | t-monitor `frontend` | `config-generator` |
|---|---|---|---|---|
| `Grid` | 0 | 2 (`Grid2 as Grid`) | 3 | **141 (v1, `item xs`)** |
| `slotProps` | 123 (también en el tema) | 91 | 2 | 0 |
| Props legados (`PaperProps`, `InputProps`, …) | ≈ 200 | ≈ 15 | 27 | 13 |
| `componentsProps` | 3 | 0 | 0 | 0 |
| Imports profundos | 0 | 0 | 0 | 0 |
| `extendTheme` / `theme.vars` | 0 | 0 | 0 | 0 |

`config-generator` usa MUI 5, que cts-theme no soporta (`^6 || ^7 || ^9`).

### 1.7 Convenciones

| | cts-manager | E-Panel | t-monitor |
|---|---|---|---|
| ESLint | flat config, sin reglas de estilo | `apps/web` **sin config** (tiene script `lint`) | solo `frontend`; config-generator y hmi-configurator **sin config** |
| Prettier | no | `singleQuote` | sí, con husky |
| Commits | — | `CONTRIBUTING.md` | commitlint conventional |
| Estructura | por feature (`features/*`, `ui/`) | atómica | atómica en `frontend`; plana en las otras |
| Idioma de la UI | español | español | español (`<html lang="en">`) |
| Fechas y números | `es-CO`, dayjs `es` | `es-ES`, `es-CO` y sin locale mezclados | dayjs |
| Notificaciones | snackbar global abajo a la derecha, 4000/7000 ms | toasts propios 6000 ms | diálogo modal (alarmas); snackbar 4000 ms (config-generator) |
| Vacío / carga / error | `EmptyState` (sin uso), Skeleton, `BrandLoader` | `QueryState` | `LoadingSpinner`, `ErrorMessage` |
| Accesibilidad (`aria-*` + `role`) | 236 | 440 | 5 / 1 / 2 |

---

## 2. Qué agrega cts-theme

En orden de impacto. Todo pasa `pnpm check` (tipos contra MUI 6, 7 y 9,
lint con el propio preset y build).

| § | Implementado en |
|---|---|
| 2.1 | `src/mui/components.ts`; `createCtsTheme` lo incluye |
| 2.2 | `status` / `statusDark` en `src/colors.ts` |
| 2.3 | `zIndex`, `notify`, `elevation`, `shadowsDark` y `motion.easing` en `src/tokens.ts` |
| 2.4 | `src/css.ts` → `dist/cts-theme.css` (`@industriascts/cts-theme/css`) |
| 2.5 | `createCtsTheme(mode, { profile: 'hmi' })`, `tokens.touch` |
| 2.6 | `src/format.ts` (`@industriascts/cts-theme/format`) |
| 2.7 | `QueryState`, `DialogHeader`, `NotificationHost` + `useNotify` en `src/views/` |
| 2.8 | `eslint/index.js` (`@industriascts/cts-theme/eslint`) |

Diferencias deliberadas frente a la copia literal de cts-manager:
- `Tooltip` y `Alert` usan peso 600 en lugar de 500 (G5).
- `containedPrimary`, `containedSecondary`, `outlined` y `sizeSmall` se
  escriben como `variants` de `MuiButton.root`, porque MUI 9 eliminó esas
  claves. El resultado visual es el mismo.

### 2.1 Overrides de componentes (`src/mui/components.ts`)
Es el paso 2 de [Atomos.md](Atomos.md). cts-manager y E-Panel coincidían en
Button, OutlinedInput, Paper, Card, TableCell, TableRow, Dialog, Tooltip, Chip,
Alert, ListItemButton, LinearProgress, Menu, MenuItem, Drawer y CssBaseline.
Con esto, ninguna app vuelve a copiar esas 200 líneas. Los átomos con
micro-estados de Atomos.md (D1–D23 pendientes) se construyen encima.

### 2.2 Roles de estado (`src/status.ts`)
Es un vocabulario único para estados de proceso y de equipo. Cada estado apunta
a un rol semántico existente, no a un hex nuevo:

| Rol | Uso | Claro | Oscuro |
|---|---|---|---|
| `status.ok` | en marcha, energizado, cerrado, aprobado | `semantic.success` | `semanticDark.success` |
| `status.warning` | en proceso, reconocido, bloqueado | `semantic.warning` | `semanticDark.warning` |
| `status.fault` | falla, disparado, alarma activa | `semantic.error` | `semanticDark.error` |
| `status.offline` | fuera de línea, inactivo, abierto | `palette.gray` `#7F7F7F` | `palette.grayLight` `#C9C9C9` |
| `status.info` | informativo | `semantic.info` | `semanticDark.info` |
| `status.selected` | selección en lienzos | `palette.blue` | `palette.blueLight` |

En oscuro, `#7F7F7F` da 2.94:1 sobre el papel, debajo del 3:1 que piden los
gráficos. Por eso se usa `#C9C9C9` (7.47:1). En claro, `ok` (2.00:1),
`warning` (1.72:1) e `info` (2.37:1) tampoco llegan a 3:1 sobre el fondo:
son los semánticos de producción y no se cambian aquí. Por eso un estado
siempre va con etiqueta o icono.

`cts-hmi-symbols` lo usan E-Panel y t-monitor, así que se alinea en un solo
lugar. Consume estos roles como variables `--cts-status-*` (ver 2.4).

### 2.3 Escalas que hoy no existen
- **`zIndex`**: capas con nombre (`sticky`, `floating`, `rail`, `overlay`,
  `keyboard`, `toast`, `tour`) sobre las de MUI, en lugar de 1000/1400/2000/2100
  sueltos.
- **Tipografía**: un juego cerrado de tamaños. Hoy cts-manager usa 13 tamaños
  numéricos distintos entre 10 y 18 (incluidos 10.5, 11.5, 12.5 y 13.5). Se
  mapean a variantes de `Typography` y a `fontSize` de `tokens.ts`.
- **Movimiento**: un solo `easing` y tres duraciones. Hoy conviven cuatro
  curvas.
- **Duraciones de notificación**: 4000 ms normal y 7000 ms con acción, como
  hace cts-manager.

### 2.4 Variables CSS (`@industriascts/cts-theme/css`)
Una hoja `cts-theme.css` generada desde `colors.ts` y `tokens.ts`, con
`:root` y `[data-theme="dark"]`. La necesitan `hmi-configurator` (no usa MUI),
`cts-hmi-symbols` y los reportes impresos de E-Panel. Ya existe el patrón:
`hmi-configurator` usa `--cts-blue` y t-monitor pone `<html data-theme>`.

### 2.5 Perfil HMI / kiosco (`createCtsTheme(mode, { profile: 'hmi' })`)
Lo que t-monitor ya hace, convertido en estándar:
- Oscuro por defecto.
- Objetivos táctiles de 48 px como mínimo (el teclado virtual usa 48–64).
- `touch-action: manipulation` y sin `user-select`.
- Sin `backdrop-filter` ni sombras pesadas, por rendimiento en Raspberry Pi.
- Ningún estado que dependa solo del hover.

Se documenta en [Mobile.md](Mobile.md) junto con lo móvil.

### 2.6 Formato (`@industriascts/cts-theme/format`)
`formatDate`, `formatDateTime`, `formatNumber` y `formatCurrency` con locale
`es-CO` fijo. Reemplaza las llamadas sueltas a `toLocaleString` y los locales
mezclados.

### 2.7 Componentes compuestos comunes
Con el mismo patrón de slots que `LoginShell` y `AppShell`:
- `QueryState`, que unifica vacío, carga y error. Toma como base el de E-Panel;
  el `EmptyState` de cts-manager no tiene uso.
- `NotificationHost`, un snackbar global con store, como el de cts-manager.
- `DialogHeader`, con título, cierre y acciones, como el de E-Panel.

### 2.8 Preset de ESLint (`@industriascts/cts-theme/eslint`)
Convierte las reglas de [Filosofia.md](Filosofia.md) en errores de CI:

| Regla | Implementación |
|---|---|
| Sin hex ni rgba literales fuera de `colors.ts` | `no-restricted-syntax` sobre `Literal[value=/^#[0-9a-f]{3,8}$/i]` y `/^rgba?\(/` |
| Sin `Grid` | `no-restricted-imports` |
| Sin props legados (`PaperProps`, `InputProps`, `componentsProps`, …) | `no-restricted-syntax` sobre `JSXAttribute` |
| Sin imports profundos de `@mui/material` | `no-restricted-imports` con patrón |
| Sin `zIndex` numérico mayor que 10 | `no-restricted-syntax` |

Los colores de dominio (lienzos maxgraph, three.js, reportes) se eximen con
`overrides` por carpeta, no línea por línea.

---

## 3. Decisiones (tomadas el 2026-11-13)

Se adoptó la recomendación en todas.

| # | Decisión | Opciones | Adoptada |
|---|---|---|---|
| **G1** | ¿t-monitor adopta la paleta de cts-manager? Cambia secundario, grises, fondo claro y texto, y se nota en pantalla. | (a) sí, completa · (b) solo marca y semánticos; los grises *slate* quedan como perfil HMI | **(a)**, en una entrega propia validada en pantalla real |
| **G2** | Valor de `status.offline` y `status.selected` | (a) `palette.gray` `#7F7F7F` y `palette.blue` · (b) primitivos nuevos | **(a)**: ya son primitivos de marca |
| **G3** | Conthrax en títulos | (a) estándar global h1–h6 · (b) solo marca (logo, login, wordmark) · (c) cada app decide | **(b)**. cts-manager no la usa, y E-Panel ya la limita a marca y títulos (`mui.ts:56`) |
| **G4** | `body1`: 15 (cts-manager y E-Panel) o 14 (t-monitor) | (a) 15 global · (b) 15 y 14 en el perfil HMI | **(a)**: en HMI la distancia de lectura pide más, no menos |
| **G5** | Pesos 500, 800 y 900, usados en cts-manager pero no cargados | (a) cargarlos · (b) mapearlos a 600/700 | **(b)**. Coincide con D22 de [Atomos.md](Atomos.md) |
| **G6** | Prohibición de `slotProps` | (a) mantenerla · (b) permitir `slotProps` en apps y prohibir los props legados | **(b)**. `slotProps` es la API de MUI 7/9, ya hay 216 usos, y los legados son los que se eliminan. La regla de no reenviar slots sigue aplicando a los componentes de cts-theme |
| **G7** | Rail cerrado: 0 (cts-manager), 64 (E-Panel) u 80 (t-monitor) | `AppShell` ya acepta `collapsedRail` | **64** con iconos (`collapsedRail='icons'`), **0** sin ellos; el 80 de t-monitor desaparece |
| **G8** | Paleta paralela `useColors()` de E-Panel | (a) migrar sus roles a cts-theme · (b) dejarla como roles de dominio de E-Panel | **(a)** para roles de interfaz (`textDisabled`, `save`, `topBar`, `onBrand`); **(b)** para `editor` y `dataBoard` |
| **G9** | `config-generator` en MUI 5 con 141 `Grid` | (a) migrar a MUI 7 antes de adoptar · (b) dejarlo fuera | **(a)**, pero al final del plan |
| **G10** | `hmi-configurator` sin MUI | (a) adoptar MUI · (b) solo variables CSS | **(b)**: aplicación pequeña y apuntada al hardware |
| **G11** | Deriva de cts-theme frente a cts-manager: `tableHeader` `0.06em` vs `0.01em`, `elevation1` del Paper `0 2px 8px …0.07`, `easing` | Seguir a cts-manager | **Seguir a cts-manager.** El `0.01em` tiene motivo documentado en `ctsTheme.ts:221-228`. Amplía D15 |
| **G12** | Locale único | `es-CO` | **`es-CO`**, y `<html lang="es">` en todas |

---

## 4. Plan de adopción

Cada app se migra en su propia rama, sin rediseñar lo que funciona en
producción (regla 00 de `cts-manager/CLAUDE.md`).

| Orden | App | Esfuerzo | Qué cambia |
|---|---|---|---|
| 1 | **cts-theme** | medio | 2.1–2.8 y la resolución de G1–G12 |
| 2 | **cts-manager** | bajo | `ctsTheme.ts` pasa a importar `createCtsTheme`; el resto queda igual. Los literales se migran por lotes, primero los colores de marca: `#0065BB` aparece 131 veces |
| 3 | **E-Panel** | bajo–medio | `theme/mui.ts` importa de cts-theme; `colors.ts` se reduce a roles de dominio (G8); `Sidebar` pasa a `AppShell` |
| 4 | **cts-hmi-symbols** | bajo | Fallbacks de sus `*.styles.ts` hacia `status.*` (2.2 y 2.4) |
| 5 | **t-monitor `frontend`** | medio | Paleta (G1), radio 10, perfil HMI, sombra de Card sin `!important` |
| 6 | **`hmi-configurator`** | bajo | Cambia sus variables por `cts-theme.css` |
| 7 | **`config-generator`** | alto | MUI 5 → 7, quitar `Grid`, cargar fuentes |

En todas las apps: agregar el preset de ESLint (2.8) primero como **warning**.
Pasa a **error** cuando el conteo de literales de la app baje a cero fuera de
las carpetas de dominio. Pasos de adopción: [Nueva-App.md](Nueva-App.md).

---

## 5. Fuera de alcance

Fuera de esta auditoría:
- Otros repos de la organización, como M-System, M-Client, hmi-builder y
  G-Cron.
- Backends.
- Contenido de los lienzos de dominio: maxgraph, three.js y reportes en `pt`.
  Se citan solo para eximirlos del lint.
