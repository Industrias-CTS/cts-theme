# Reporte de Estilado y Consumo de cts-theme en Proyectos MUI

Este documento tiene dos partes:

1. **Estilado con MUI:** los métodos que MUI ofrece para dar estilo a un
   componente, y cómo se aplican los tokens de CTS en cada uno.
2. **Inyección de cts-theme en un proyecto MUI:** todas las formas en que el
   paquete puede entrar a un proyecto que ya usa MUI.

Reglas que siguen todos los ejemplos (ver `INSTRUCCIONES-COMPONENTES.md`):

- Ningún valor literal (`34`, `#0065BB`, `0.15s`) si existe un token.
- Importar desde la raíz de MUI (`@mui/material`, `@mui/material/styles`).
- Sin `Grid`, `slotProps`, `componentsProps`, `extendTheme`, `CssVarsProvider` ni `theme.vars`.

---

## Parte 1. Estilado con MUI

### 1.1 `sx` con objeto literal

```tsx
import { Box } from '@mui/material'

export const Panel = (): React.JSX.Element => (
  <Box
    sx={(t) => ({
      padding: `${t.cts.spacing.gutter}px`,
      borderRadius: `${t.cts.radii.card}px`,
      background: t.palette.background.paper,
      border: `1px solid ${t.palette.divider}`,
    })}
  >
    Contenido
  </Box>
)
```

Si el objeto no necesita el tema (por ejemplo, solo `display: 'flex'`), puede
ir sin función. Cualquier valor del sistema pasa por `t.cts.*`.

### 1.2 `sx` como función `(theme) => ...`

Es la forma para leer `theme.cts` y `theme.palette`. Es la que usa todo el
sistema.

```tsx
import { Box } from '@mui/material'

export const NavItemFrame = ({ active }: { active: boolean }): React.JSX.Element => (
  <Box
    sx={(t) => ({
      height: t.cts.density.navItem,
      background: active ? t.cts.rail.itemActiveBg : 'transparent',
      color: active ? t.cts.rail.itemActiveColor : t.cts.rail.itemIdleColor,
      transition: `background ${t.cts.motion.nav} ${t.cts.motion.easing}`,
    })}
  />
)
```

### 1.3 `sx` con pseudo-clases y selectores anidados

```tsx
import { Box } from '@mui/material'

export const Row = (): React.JSX.Element => (
  <Box
    sx={(t) => ({
      '&:hover': { background: t.palette.action.hover },
      '&:focus-visible': { outline: `2px solid ${t.palette.primary.main}` },
      '& .MuiTypography-root': { fontWeight: t.cts.fontWeight.semibold },
      '& + &': { borderTop: `1px solid ${t.palette.divider}` },
    })}
  />
)
```

### 1.4 `sx` como array (condicionales)

MUI aplica los elementos en orden. Un `false` se ignora.

```tsx
import { Box } from '@mui/material'

export const Chip = ({ selected }: { selected: boolean }): React.JSX.Element => (
  <Box
    sx={[
      (t) => ({ height: t.cts.density.toolbarControl }),
      selected && ((t) => ({ background: t.palette.action.selected })),
    ]}
  />
)
```

### 1.5 `styled()` con `shouldForwardProp`

Crea un componente con estilos fijos. `shouldForwardProp` evita que una prop
propia llegue al DOM.

```tsx
import { Box } from '@mui/material'
import { styled } from '@mui/material/styles'

export const Tile = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'accent',
})<{ accent?: boolean }>(({ theme, accent }) => ({
  borderRadius: `${theme.cts.radii.card}px`,
  boxShadow: theme.cts.shadows.card,
  background: theme.palette.background.paper,
  borderLeft: accent
    ? `${theme.cts.borders.indicator}px solid ${theme.palette.primary.main}`
    : 'none',
}))
```

### 1.6 `styled()` con `variants`

Los vaops.
riantes se declaran como datos y MUI los aplica según las pr
```tsx
import { Button } from '@mui/material'
import { styled } from '@mui/material/styles'

export const StatusButton = styled(Button)(({ theme }) => ({
  height: `${theme.cts.density.toolbarControl}px`,
  fontSize: `${theme.cts.fontSize.dense}px`,
  variants: [
    {
      props: { tone: 'danger' },
      style: { background: theme.palette.error.main, color: theme.palette.error.contrastText },
    },
  ],
}))

// Uso: <StatusButton tone="danger" />
// Requiere augmentar `ButtonProps` con `tone` para que TypeScript lo acepte.
```

### 1.7 Prop `component` (polimorfismo)

Cambia la etiqueta HTML o el componente raíz sin perder estilos.

```tsx
import { Box } from '@mui/material'

export const SidebarRoot = (): React.JSX.Element => (
  <Box component="aside" sx={(t) => ({ width: t.cts.layout.railWidth })} />
)
```

En un router, `component={Link}` con `to` o `href` funciona igual (es la vía
prevista para `NavItem`).

### 1.8 `className` (vía de escape)

Para integrar estilos externos (CSS de otra librería, clases de un
framework). Los estilos MUI de `sx` tienen prioridad sobre las clases
externas en el mismo elemento, salvo que se use mayor especificidad.

```tsx
import { Box } from '@mui/material'
import './legacy.css'

export const Legacy = (): React.JSX.Element => <Box className="legacy-block" />
```

### 1.9 Prop `style` (inline) — evitar

Se permite solo para valores calculados en tiempo de ejecución que no pueden
expresarse en `sx` (por ejemplo, una posición medida en píxeles). Los valores
fijos del sistema van en `sx`. Un estilo inline no respeta media queries,
pseudo-clases ni el tema.

```tsx
import { Box } from '@mui/material'

export const Marker = ({ x }: { x: number }): React.JSX.Element => (
  <Box sx={{ position: 'absolute' }} style={{ left: x }} />
)
```

### 1.10 `theme.components` / `styleOverrides`

Define el estilo por defecto de cada componente MUI. **cts-theme ya lo trae**:
`createCtsTheme` incluye los overrides de `src/mui/components.ts` (Button,
OutlinedInput, Paper, Card, Table*, Dialog, Tooltip, Chip, Alert,
ListItemButton, LinearProgress, Menu, MenuItem, Drawer, Divider y
CssBaseline), copiados de cts-manager y comprobados contra MUI 6, 7 y 9.

Una app solo agrega lo propio y, para variantes por props, usa `variants`
(las claves compuestas como `containedPrimary` no existen en MUI 9):

```tsx
import { createTheme } from '@mui/material/styles'
import { themeOptions } from '@industriascts/cts-theme'

export const theme = createTheme(themeOptions('light'), {
  components: {
    MuiToggleButton: {
      styleOverrides: {
        root: ({ theme }) => ({ borderRadius: `${theme.cts.radii.control}px` }),
      },
    },
  },
})
```

### 1.11 `useTheme()` para valores en JavaScript

Cuando un valor se necesita en lógica (cálculo, prop de un tercero), no en
CSS.

```tsx
import { useTheme } from '@mui/material/styles'
import { useMediaQuery } from '@mui/material'

export const Gutter = (): number => {
  const theme = useTheme()
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'))
  return isDesktop ? theme.cts.spacing.gutter : theme.cts.spacing.gutter / 2
}
```

Nota: bajo `sm` el gutter es `theme.cts.spacing.gutterCompact` (12); ver `Mobile.md`. Este
ejemplo muestra la forma, no un valor aprobado.

### 1.12 `alpha()` para tintes

MUI ofrece `alpha(color, valor)`. Para los tintes de estado del sistema
(`color + '20'`), usar `tint()` de cts-theme (ver 2.15), no `alpha()`.

```tsx
import { alpha } from '@mui/material/styles'
import { Box } from '@mui/material'

export const Hover = (): React.JSX.Element => (
  <Box sx={(t) => ({ '&:hover': { background: alpha(t.palette.primary.main, 0.08) } })} />
)
```

### 1.13 `GlobalStyles` y `CssBaseline`

`CssBaseline` normaliza el navegador y pinta el fondo con
`palette.background.default`. `GlobalStyles` agrega reglas globales.

```tsx
import { CssBaseline, GlobalStyles } from '@mui/material'

export const Globals = (): React.JSX.Element => (
  <>
    <CssBaseline />
    <GlobalStyles
      styles={(t) => ({
        '*::placeholder': { color: t.cts.rail.searchPlaceholder },
      })}
    />
  </>
)
```

### 1.14 Métodos prohibidos o fuera de uso

| Método | Motivo |
|---|---|
| `Grid` de MUI | Renombrado en 7 (`Grid2` → `Grid`); `GridLegacy` eliminado en 9. Usar flex/grid CSS. |
| `slotProps` / `componentsProps` | Consolidados en 7. Exponer props propias explícitas. |
| Imports profundos (`@mui/material/Button/Button`) | Eliminados en 7. Importar desde la raíz. |
| `extendTheme` · `CssVarsProvider` · `theme.vars` | Movidos o fusionados entre majors. Leer de `theme.cts`. |

---

## Parte 2. Inyectar cts-theme en un proyecto MUI

Cada vía responde a una necesidad distinta. La más común es **2.4 + 2.12**:
un `ThemeProvider` con `createCtsTheme` y `sx` leyendo `theme.cts`.

### 2.1 Instalación del paquete

El paquete es `private` (`UNLICENSED`) y no se publica en npm. Las formas de
instalarlo son las de 2.2 a 2.6.

Antes de instalar desde una ruta local o de git, hay que compilar: `main`,
`types` y `exports` apuntan a `dist/`, y `dist/` está en `.gitignore`.

```bash
# En cts-theme
pnpm build
```

### 2.2 Ruta local con `file:`

Copia el paquete compilado en `node_modules`. Hay que volver a instalar
cada vez que cambie cts-theme.

```bash
# En el proyecto consumidor
pnpm add file:../cts-theme
```

```json
// package.json del consumidor
{
  "dependencies": {
    "@industriascts/cts-theme": "file:../cts-theme"
  }
}
```

### 2.3 Ruta local con `link:` (desarrollo)

Enlaza la carpeta. Los cambios en `dist/` se ven sin reinstalar (solo hay que
recompilar cts-theme).

```bash
pnpm add link:../cts-theme
```

### 2.4 Tarball

Para distribuir una versión fija sin repositorio compartido.

```bash
# En cts-theme
pnpm build && pnpm pack          # genera industriascts-cts-theme-0.1.0.tgz

# En el proyecto consumidor
pnpm add ../cts-theme/industriascts-cts-theme-0.1.0.tgz
```

### 2.5 Dependencia de git

Requiere que `dist/` llegue al repositorio o que el consumidor compile. Hoy
`package.json` no tiene script `prepare`, así que una dependencia de git sin
`dist/` no funciona.

```bash
pnpm add git+ssh://git@github.com/<org>/cts-theme.git#v0.1.0
```

### 2.6 Workspace de monorepo

Si cts-theme vive en el mismo monorepo que la aplicación.

```json
{
  "dependencies": {
    "@industriascts/cts-theme": "workspace:*"
  }
}
```

### 2.7 Entrada barrel: `@industriascts/cts-theme`

Trae todo: tokens, colores, `createCtsTheme`, `themeOptions`, `typography`, y
la augmentation de `theme.cts`.

```tsx
import { createCtsTheme, dataColor, tint, palette } from '@industriascts/cts-theme'
```

En el barrel, `palette` es la paleta de **marca** (hexes). La fábrica de paleta
MUI se reexporta como `muiPalette`.

### 2.8 Subrutas: `/colors`, `/tokens`, `/mui`

Importar solo lo necesario. Útil para no cargar MUI en código que no lo usa
(por ejemplo, un script de build o un servicio sin React).

```tsx
import { palette, surface, semantic, data8 } from '@industriascts/cts-theme/colors'
import { radii, density, motion, layout } from '@industriascts/cts-theme/tokens'
import { createCtsTheme, themeOptions, typography } from '@industriascts/cts-theme/mui'
```

Aquí `palette` de `/mui` es la **fábrica** (`palette(mode)`), no la de marca de
`/colors`. Es la colisión que el barrel evita con `muiPalette`.

### 2.9 Tema completo: `createCtsTheme` + `ThemeProvider`

La vía principal. Un solo `ThemeProvider` en la raíz de la aplicación.

```tsx
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const theme = createCtsTheme('light')

export const Root = ({ children }: { children: React.ReactNode }): React.JSX.Element => (
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
)
```

`createCtsTheme` devuelve un tema de MUI completo, con `theme.cts` ya expuesto.
Crear el tema una sola vez, fuera del componente.

### 2.10 `ThemeProvider` + `CssBaseline`

Igual que 2.9, con el reset de MUI y el fondo `palette.background.default`.

```tsx
import { CssBaseline } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const theme = createCtsTheme('light')

export const Root = ({ children }: { children: React.ReactNode }): React.JSX.Element => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    {children}
  </ThemeProvider>
)
```

### 2.11 Modo oscuro: dos temas y conmutador

Se crean los dos temas y se elige cuál pasar al `ThemeProvider`. El estado
vive en la aplicación, no en cts-theme (no hay estado global en la librería).

```tsx
import { useMemo, useState } from 'react'
import { CssBaseline } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const themes = {
  light: createCtsTheme('light'),
  dark: createCtsTheme('dark'),
}

export const App = ({ children }: { children: React.ReactNode }): React.JSX.Element => {
  const [mode, setMode] = useState<'light' | 'dark'>('light')
  const theme = useMemo(() => themes[mode], [mode])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <button onClick={() => setMode((m) => (m === 'light' ? 'dark' : 'light'))}>
        Cambiar tema
      </button>
      {children}
    </ThemeProvider>
  )
}
```

### 2.12 Modo según preferencia del sistema

Elige el modo inicial con `prefers-color-scheme`. Si el usuario puede
cambiarlo, combinar con 2.11.

```tsx
import { useMediaQuery } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const light = createCtsTheme('light')
const dark = createCtsTheme('dark')

export const App = ({ children }: { children: React.ReactNode }): React.JSX.Element => {
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
  return <ThemeProvider theme={prefersDark ? dark : light}>{children}</ThemeProvider>
}
```

### 2.13 Tema anidado: una zona con otro modo

Un `ThemeProvider` interior **reemplaza** el tema de afuera; no lo fusiona. Si
la zona interior usa `createCtsTheme`, trae su propio `cts`, así que no hace
falta nada más.

```tsx
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'
import { Box } from '@mui/material'

const dark = createCtsTheme('dark')

export const DarkPanel = ({ children }: { children: React.ReactNode }): React.JSX.Element => (
  <ThemeProvider theme={dark}>
    <Box sx={(t) => ({ background: t.palette.background.default, color: t.palette.text.primary })}>
      {children}
    </Box>
  </ThemeProvider>
)
```

Si el tema interior debe **heredar** del exterior y solo cambiar algo, usar la
forma función de `ThemeProvider`: `theme={(outer) => ({ ...outer, ... })}`.

### 2.14 Extender el tema CTS: `createTheme(themeOptions(mode), overrides)`

Para un proyecto que necesita ajustar el tema sin tocar cts-theme. `themeOptions`
trae la paleta, la tipografía, el radio base, el espaciado, los breakpoints y
`cts`. `createTheme` acepta varios argumentos y los fusiona en profundidad.

```tsx
import { createTheme } from '@mui/material/styles'
import { themeOptions } from '@industriascts/cts-theme/mui'

export const theme = createTheme(themeOptions('light'), {
  palette: {
    secondary: { main: '#2E7D32' },
  },
})
```

Atención: el valor `#2E7D32` es un literal del consumidor. Un cambio de
marca debe hacerse en cts-theme (`src/colors.ts`), no en cada proyecto. Este
ejemplo muestra la técnica para un ajuste local y transitorio.

### 2.15 Consumir `theme.cts` dentro de `sx`

Funciona en cualquier componente que esté bajo un `ThemeProvider` con un tema
CTS. Es la forma prevista para todo el sistema (ver 1.2).

```tsx
import { Box } from '@mui/material'

export const Badge = (): React.JSX.Element => (
  <Box
    sx={(t) => ({
      minWidth: t.cts.density.chipBadge,
      height: t.cts.density.chipBadge,
      borderRadius: `${t.cts.radii.pill}px`,
      background: t.palette.error.main,
      color: t.palette.error.contrastText,
    })}
  />
)
```

> Claves usadas: `density.chipBadge` (18) y `radii.pill` (99) existen en
> `src/tokens.ts`. El color de texto sale de la paleta MUI, sin literales.

Si el tipo `theme.cts` no aparece en el autocompletado, la augmentation no se
cargó. Importar cualquier entrada de cts-theme (por ejemplo, `createCtsTheme`
del barrel) en el punto de entrada del proyecto.

### 2.16 Consumir `theme.cts` dentro de `styled()`

Igual que 2.15, con la misma garantía de tipos.

```tsx
import { Box } from '@mui/material'
import { styled } from '@mui/material/styles'

export const Card = styled(Box)(({ theme }) => ({
  padding: `${theme.cts.spacing.gutter}px`,
  borderRadius: `${theme.cts.radii.card}px`,
  boxShadow: theme.cts.shadows.card,
}))
```

### 2.17 Tokens directos, sin `ThemeProvider`

Para código fuera de React o un estilo que no pasa por MUI: importar el objeto
`tokens` y leerlo como constante. No hay `theme.cts` ni cambio de modo.

```tsx
import { tokens } from '@industriascts/cts-theme/tokens'
import { Box } from '@mui/material'

export const FixedRail = (): React.JSX.Element => (
  <Box sx={{ width: tokens.layout.railWidth, boxShadow: tokens.shadows.sidebar }} />
)
```

Usar esto solo cuando el componente no está bajo `ThemeProvider`. Dentro de una
app MUI, `sx` con `theme.cts` (2.15) es la vía correcta.

### 2.18 Solo colores, sin MUI

Para estilos fuera de MUI (un script de exportación, un informe, un gráfico
externo). Cero dependencia de MUI.

```ts
import { palette, surface, semantic, dataColor, tint } from '@industriascts/cts-theme/colors'

const seriesColor = dataColor(2)        // '#00c875' (índice módulo 8)
const chipBg = tint(semantic.error)     // hex + '20'
const pageBg = surface.soft
const brand = palette.blue
```

`tint()` devuelve `color + '20'` (o `'18'`), es decir, un hex de 8 dígitos. No
funciona con colores `rgb()` ni con variables CSS.

### 2.19 Solo la paleta MUI, dentro de un tema propio

Cuando el proyecto ya tiene su tema y solo quiere la paleta CTS. No trae
`cts` ni tipografía.

```tsx
import { createTheme } from '@mui/material/styles'
import { palette as muiPalette } from '@industriascts/cts-theme/mui'

export const theme = createTheme({
  palette: muiPalette('dark'),
})
```

Sin `cts`, `theme.cts` no existe. Si el proyecto necesita los tokens, usar 2.14.

### 2.20 Tipos para props y helpers

Para tipar props o funciones que reciben valores del sistema, sin copiar
los tipos.

```tsx
import type { CtsTokens, DataColor, Palette } from '@industriascts/cts-theme'

export type ChartPalette = readonly DataColor[]

export const fixedTokens = (t: CtsTokens): number => t.layout.railWidth
```

### 2.21 Pruebas unitarias con un wrapper

Un wrapper de pruebas envuelve el componente con el tema CTS. Vale para
Vitest, Jest o cualquier runner que use React.

```tsx
import { render } from '@testing-library/react'
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'
import { Panel } from './Panel'

const theme = createCtsTheme('light')

const renderWithCts = (ui: React.ReactElement) =>
  render(<ThemeProvider theme={theme}>{ui}</ThemeProvider>)

it('renderiza el panel', () => {
  renderWithCts(<Panel />)
})
```

### 2.22 Storybook: decorador global

Un decorador global aplica el tema a todas las historias. Es la misma
técnica que 2.9, con la forma de Storybook.

```tsx
// .storybook/preview.tsx (ejemplo)
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const theme = createCtsTheme('light')

export const decorators = [
  (Story: React.ComponentType) => (
    <ThemeProvider theme={theme}>
      <Story />
    </ThemeProvider>
  ),
]
```

---

## Parte 3. Resumen de vías de inyección

| # | Vía | Import | Cuándo |
|---|---|---|---|
| 2.2 | `file:` | — | Ruta local, compilada |
| 2.3 | `link:` | — | Desarrollo con recompilación |
| 2.4 | Tarball | — | Versión fija compartida |
| 2.5 | Git | — | Requiere `dist/` en el repo |
| 2.6 | Workspace | — | Monorepo |
| 2.7 | Barrel | `@industriascts/cts-theme` | Uso general |
| 2.8 | Subrutas | `/colors` `/tokens` `/mui` | Importar solo lo necesario |
| 2.9 | Tema completo | `createCtsTheme` | **Vía principal** |
| 2.10 | + `CssBaseline` | `createCtsTheme` | Reset de MUI |
| 2.11 | Dos temas + conmutador | `createCtsTheme` | Modo oscuro manual |
| 2.12 | Modo del sistema | `createCtsTheme` | Modo oscuro automático |
| 2.13 | Tema anidado | `createCtsTheme` | Zona con otro modo |
| 2.14 | Extender | `themeOptions` | Ajuste local del tema |
| 2.15 | `theme.cts` en `sx` | — | Estilado de componentes |
| 2.16 | `theme.cts` en `styled()` | — | Componentes reutilizables |
| 2.17 | Tokens directos | `tokens` | Fuera de `ThemeProvider` |
| 2.18 | Solo colores | `/colors` | Sin MUI |
| 2.19 | Solo paleta MUI | `muiPalette` / `palette` (`/mui`) | Tema propio |
| 2.20 | Tipos | tipos del barrel | Props y helpers tipados |
| 2.21 | Pruebas | `createCtsTheme` | Wrapper de tests |
| 2.22 | Storybook | `createCtsTheme` | Decorador global |

### Vías que no existen o están prohibidas

| Vía | Estado |
|---|---|
| Export de variables CSS (`--cts-*`) | No existe. Los tokens viven en JS. |
| `CssVarsProvider` / `extendTheme` / `theme.vars` | Prohibido (ver 1.14). |
| Preset de Tailwind | No existe. |
| Copiar valores a mano en cada proyecto | Prohibido por la regla de oro: los valores se importan, no se re-declaran. |
| Paquete en npm público | No existe. El paquete es `private`. |

## Compatibilidad MUI 6 · 7 · 9

`peerDependencies` declara `^6 || ^7 || ^9`. Los ejemplos usan solo imports
estables en los tres majors:

- `ThemeProvider`, `createTheme`, `styled`, `useTheme`, `alpha` desde
  `@mui/material/styles`.
- `Box`, `CssBaseline`, `GlobalStyles`, `useMediaQuery` desde `@mui/material`.

**No verificado en este documento.** La compatibilidad se declara en
`package.json` y se comprueba con `pnpm typecheck:matrix` sobre `smoke/`,
no sobre estos fragmentos.


## Parte 4. Consumo


Utilizamos `ThemeProvider` como proveedor del tema global.

```tsx
import { useMemo, useState } from 'react'
import { CssBaseline } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import { createCtsTheme } from '@industriascts/cts-theme'

const themes = {
  light: createCtsTheme('light'),
  dark: createCtsTheme('dark'),
}

export const App = ({ children }: { children: React.ReactNode }): React.JSX.Element => {
  const [mode, setMode] = useState<'light' | 'dark'>('light')
  const theme = useMemo(() => themes[mode], [mode])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <button onClick={() => setMode((m) => (m === 'light' ? 'dark' : 'light'))}>
        Cambiar tema
      </button>
      {children}
    </ThemeProvider>
  )
}
```

_El usuario conecta los estados para cambiar de temas_


Para los distintos layouts, átomos, moléculas y componentes, la mayoría, vienen listos para importarse.