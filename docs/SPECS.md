# Specifications and Rationale

Decisiones de diseño del paquete `@industriascts/cts-theme` y por qué se
tomaron. Los **valores** viven en `docs/demo/` (las nueve hojas del sistema);
aquí se documenta cómo se traducen a código.

## Current State of the Art

Construida y verificada la **base de tokens**. Todavía no hay componentes.

| Módulo | Qué aporta |
|---|---|
| `src/tokens.ts` | radios · bordes · sombras · densidad · animación · espaciado · layout (zonas 1–10) · rail · tipografía · breakpoints |
| `src/colors.ts` | marca · superficie claro/oscuro · semánticos · paleta de datos (8) · `dataColor()` · `tint()` |
| `src/mui/theme.ts` | `createCtsTheme(mode)` — paleta, tipografía, `shape.borderRadius: 10`, `spacing: 8` |
| `src/mui/augmentation.ts` | expone los tokens como `theme.cts` dentro de cualquier `sx` |

**Deuda consciente:** `themeOptions` no lleva `components`. Los overrides de
botones, inputs, chips, tabs, menús, diálogos y tablas (hojas «Controles» y
«Tablas y listas») son una decisión aparte, porque los nombres de slot y los
`defaultProps` sí cambian entre majors de MUI — a diferencia de todo lo de
arriba.

Los 13 componentes de layout están especificados, no escritos:
[INSTRUCCIONES-COMPONENTES.md](INSTRUCCIONES-COMPONENTES.md).

```tsx
// App.tsx
import { ThemeProvider, CssBaseline } from '@mui/material'
import { createCtsTheme } from '@industriascts/cts-theme'

const theme = createCtsTheme('light')   // o 'dark'

export const App = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <Vista />
  </ThemeProvider>
)

// Cualquier `sx` lee los tokens del tema — sin importar nada más:
const Fila = () => (
  <Box sx={(t) => ({
    height: t.cts.density.tableRow,                 // 38
    fontSize: t.cts.fontSize.dense,                 // 13
    borderBottom: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
    transition: `background ${t.cts.motion.nav} ${t.cts.motion.easing}`,
  })} />
)
```

### Por qué `sx` y no `styled()`

Lo fija la hoja «Portada»: *React + MUI · createTheme + sx*. `styled()` daría
algo mejor de rendimiento, pero divergiría de la guía que el resto del grupo
lee. `augmentation.ts` es lo que hace que la decisión se sostenga: sin
`theme.cts`, cada `sx` tendría que importar los tokens por separado y el tema
quedaría decorativo.

## Compatibility

`peerDependencies: "@mui/material": "^6 || ^7 || ^9"` — **comprobado, no
supuesto**. `pnpm typecheck:matrix` compila `src/` y `smoke/` contra los tres
majors instalados en paralelo vía alias de pnpm:

| Major | Versión probada | Estado |
|---|---|---|
| 6 | 6.5.0 | verde |
| 7 | 7.3.11 | verde |
| 9 | 9.4.0 | verde |

No existe MUI 8: npm publica 5, 6, 7 y 9.

`smoke/sx-usage.tsx` no es decorativo — ejerce `theme.cts` dentro de `sx` en
casos reales de las zonas 1, 4 y 9. Es lo que convierte el rango de peers en
una comprobación.

### Cómo se mantiene verde

Lo que rompe entre majors, y por tanto está prohibido en este paquete:

| Prohibido | Motivo |
|---|---|
| `Grid` | renombrado en 7 (`Grid2`→`Grid`); `GridLegacy` eliminado en 9 |
| `componentsProps` / `slotProps` | consolidados en 7 |
| imports profundos de 2.º nivel | eliminados en 7 |
| `extendTheme` · `CssVarsProvider` · `theme.vars` | movidos/fusionados entre majors |

No cuesta nada: un shell de flex nunca necesitó `Grid`.

La matriz discrimina de verdad — verificado con centinelas que solo existen en
un major: `Grid2` resuelve únicamente bajo 6, `GridLegacy` únicamente bajo 7.

### Trampa de empaquetado: TS2742

Con pnpm, un componente exportado sin tipo de retorno anotado rompe la emisión
de `.d.ts`:

```
error TS2742: The inferred type of 'X' cannot be named without a reference to
'.pnpm/@mui+types@9.4.0_.../node_modules/@mui/types'
```

Detectado en este repo. **Anotar el retorno de todo componente exportado**, o
`pnpm build` falla aunque `pnpm typecheck` pase.

### Móvil

Sin definir en el sistema: las nueve hojas miden 1440 px. El paquete no
inventa valores; deja los ejes abiertos (`variant`, `density`, `open`) para que
la ratificación sea un cambio de valor y no de firma.
Nueve conflictos abiertos en [MOBILE-TBD.md](MOBILE-TBD.md).
