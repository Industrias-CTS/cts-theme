# Cómo usar cts-theme en una app

Guía para apps nuevas y para migrar las existentes (cts-manager, E-Panel,
t-monitor). Las reglas que se aplican están en [Filosofia.md](Filosofia.md);
el porqué de cada valor, en [Estandares-Globales.md](Estandares-Globales.md).

## 1. Requisitos

| | Versión |
|---|---|
| React | 18 o 19 |
| MUI (`@mui/material`) | 6, 7 o 9. **MUI 5 no está soportado** |
| ESLint (opcional, para el preset) | 9, flat config |

## 2. Instalar

El paquete es privado de la organización. Mientras no se publique en un
registro, se instala desde Git:

```bash
pnpm add github:Industrias-CTS/cts-theme#main
```

## 3. Tema

```tsx
import { CssBaseline, ThemeProvider } from '@mui/material'
import { createCtsTheme } from '@industriascts/cts-theme'
import { NotificationHost } from '@industriascts/cts-theme/views'

export function Root() {
  const mode = useModo() // 'light' | 'dark', guardado por la app
  const theme = useMemo(() => createCtsTheme(mode), [mode])
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NotificationHost>
        <App />
      </NotificationHost>
    </ThemeProvider>
  )
}
```

- `createCtsTheme` trae paleta, tipografía, sombras y **todos los overrides
  de componentes**. No hace falta repetir `theme.components` en la app.
- Crear el tema dentro de `useMemo`, no en cada render (t-monitor lo
  reconstruye en cada render hoy).
- Para extenderlo con algo propio de la app:

  ```ts
  import { createTheme } from '@mui/material/styles'
  import { themeOptions } from '@industriascts/cts-theme'

  export const theme = (mode) => createTheme(themeOptions(mode), { /* solo lo propio */ })
  ```

### Perfil HMI (pantallas táctiles, kioscos, Raspberry Pi)

```ts
createCtsTheme('dark', { profile: 'hmi' })
```

Objetivos táctiles de 48 px, filas de tabla de 48, sin selección de texto ni
resaltado al tocar. Ver [Mobile.md](Mobile.md#perfil-hmi).

## 4. Fuentes

El paquete no incluye archivos de fuente. Cada app carga:

- **Titillium Web** 300, 400, 600 y 700 (y 900 si muestra el wordmark). Puede
  ser `@fontsource/titillium-web` o archivos propios en `public/fonts`.
- **Conthrax** solo si la app muestra marca con ella (login, wordmark). Los
  archivos están en E-Panel (`apps/web/src/theme/fonts.css`) y en t-monitor
  (`hmi-configurator/public/fonts`).

Sin pesos 500 ni 800: no se cargan y el lint los rechaza.

## 5. Valores en `sx`

```tsx
<Box
  sx={(t) => ({
    p: 3,                                   // espaciado: múltiplos de 8
    borderRadius: `${t.cts.radii.card}px`,
    boxShadow: t.cts.shadows.menu,
    zIndex: t.cts.zIndex.floating,
    transition: `width ${t.cts.motion.collapse} ${t.cts.motion.easing}`,
    color: 'text.secondary',                // roles del tema como cadena
  })}
/>
```

Colores de estado de equipos:

```tsx
import { status, statusDark } from '@industriascts/cts-theme'

const color = (t: Theme, s: StatusName) => (t.palette.mode === 'dark' ? statusDark : status)[s]
```

## 6. Sin MUI: variables CSS

Para apps sin MUI (`hmi-configurator`), lienzos, símbolos o reportes:

```ts
import '@industriascts/cts-theme/css'
```

```css
.panel   { background: var(--cts-paper); border-radius: var(--cts-radius-card); }
.alarma  { color: var(--cts-status-fault); }
```

Modo oscuro con `<html data-theme="dark">`; sin atributo sigue la preferencia
del sistema. Lista completa: `cssVariables('light')` o
`dist/cts-theme.css`.

## 7. Componentes comunes

| Componente | Para qué |
|---|---|
| `AppShell` | marco de la app con rail (256 · 64 · 0), barra superior opcional y acciones flotantes |
| `LoginShell` | pantalla de acceso con panel de marca y hueco para el formulario |
| `QueryState` | carga, error con «Reintentar» y estado vacío de una consulta |
| `DialogHeader` | cabecera de diálogo con título, subtítulo, acciones y cierre |
| `NotificationHost` + `useNotify()` | avisos globales abajo a la derecha (4 s, 7 s con acción, persistentes con avance) |

Todos se importan de `@industriascts/cts-theme/views`.

## 8. Formato

```ts
import { formatDate, formatDateTime, formatNumber, formatCurrency, formatUnit } from '@industriascts/cts-theme/format'

formatDate(fecha)                 // 13 de nov de 2026
formatDate(fecha, { style: 'short' }) // 13/11/2026
formatDateTime(fecha)             // 13 de nov de 2026, 14:05
formatNumber(1234567.891)         // 1.234.567,89
formatCurrency(1234567)           // $ 1.234.567
formatUnit(230.44, 'V')           // 230,4 V
```

Fechas vacías o inválidas devuelven `—`. Una cadena `YYYY-MM-DD` se lee como
fecha local.

## 9. Lint

```js
// eslint.config.js
import tseslint from 'typescript-eslint'
import { ctsLint } from '@industriascts/cts-theme/eslint'

export default tseslint.config(
  ...tseslint.configs.recommended,
  ...ctsLint({
    domain: ['src/features/editor/**'], // colores de dominio permitidos
    level: 'warn',                      // 'error' cuando la app ya cumpla
  }),
)
```

En apps existentes se empieza con `level: 'warn'` y se sube a `'error'` cuando
el conteo de avisos fuera de las carpetas de dominio llegue a cero.

## 10. Checklist de una app nueva

- [ ] React 18/19 y MUI 7 o 9
- [ ] `createCtsTheme` + `CssBaseline` + `NotificationHost` en la raíz
- [ ] Titillium Web cargada (300/400/600/700)
- [ ] `AppShell` y `LoginShell` para el marco y el acceso
- [ ] `<html lang="es">`
- [ ] Preset de ESLint en `error`
- [ ] Fechas y números con `format`
- [ ] Sin `theme/` propio salvo extensiones de dominio
