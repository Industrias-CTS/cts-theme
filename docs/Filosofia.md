# Filosofía y reglas del Sistema de Diseño CTS

Estas reglas valen para **todas** las aplicaciones de Industrias CTS:
cts-manager (W-Flow), E-Panel, t-monitor y las que vengan. Las que se pueden
comprobar automáticamente las comprueba el preset de ESLint
(`@industriascts/cts-theme/eslint`, ver [Nueva-App.md](Nueva-App.md)). Las
marcadas **[lint]** fallan en CI.

## Principios

1. **Los componentes se usan tal como vienen de la librería**, sin cambiarles
   el estilo. El aspecto de botones, inputs, tablas, diálogos, menús, chips y
   tooltips lo pone el tema (`src/mui/components.ts`), no cada pantalla.
2. **Los valores primitivos viven en un solo lugar.** Los colores están en
   `src/colors.ts` y las medidas en `src/tokens.ts`. Una app puede
   sobrescribirlos de forma global (su tema) o local (un `ThemeProvider`
   anidado), pero nunca escribirlos sueltos.
3. **Los componentes con estilo propio usan roles, no colores.** Se escribe
   `text.secondary`, `theme.cts.rail.itemActiveBg` o `status.fault`, nunca
   `#5a6a80`.
4. **Los compuestos dejan huecos.** `LoginShell`, `AppShell`, `QueryState` y
   `DialogHeader` ponen estructura, estilo y comportamiento. Cada app llena los
   huecos (logo, formulario, rail, acciones) con sus propios componentes.
5. **Se copia lo que ya funciona en producción.** Los valores salen literales
   de las apps (regla de oro del [README](../README.md#regla-de-oro)) y cada
   cambio cita su archivo fuente.
6. **Los componentes propios de una app no deben superar en número a los
   importados del sistema.** Si un patrón se repite en dos apps, se propone
   como compuesto aquí.

## Reglas

### Color
| Regla | |
|---|---|
| Sin hex, `rgb()`, `rgba()` ni `hsl()` literales fuera de `colors.ts`, `tokens.ts` y la carpeta `theme/` de la app | **[lint]** |
| Los estados de equipo y de proceso usan `status.*` / `statusDark.*` (`ok`, `warning`, `fault`, `offline`, `info`, `selected`) o `--cts-status-*` | |
| `data8` es solo para datos del usuario (series, grupos, etiquetas), nunca para chrome | |
| El chrome es azul + grises; los semánticos son solo para significado (error, éxito…) | |
| Colores de dominio (lienzos, 3D, símbolos eléctricos, reportes) se declaran en carpetas exentas con `domain` en el preset, no línea por línea | |

### Tipografía
| Regla | |
|---|---|
| Titillium Web en toda la interfaz, títulos incluidos | |
| Conthrax (`brandFontFamily`) solo en marca: wordmark, logo de texto, panel del login, barras de marca | |
| Pesos: 300, 400, 600 y 700; 900 solo para el wordmark. Sin 500 ni 800 | **[lint]** |
| Tamaños: variantes de `Typography` (`body1` 15, `body2` 13, `caption` 12, `overline` 11…) o `theme.cts.fontSize`. Sin tamaños nuevos a mano | |

### Capas, forma y movimiento
| Regla | |
|---|---|
| `zIndex` mayor que 10 solo desde `theme.zIndex` o `theme.cts.zIndex` | **[lint]** |
| Radios desde `theme.cts.radii`; `shape.borderRadius` es 10 | |
| Una sola curva: `theme.cts.motion.easing`; duraciones de `theme.cts.motion` | |

### Formato e idioma
| Regla | |
|---|---|
| UI en español; `<html lang="es">` | |
| Fechas, horas, números, moneda y porcentajes con `@industriascts/cts-theme/format` (`es-CO`). Sin `toLocaleString` suelto | |

### Funciones de MUI prohibidas

| Prohibido | Motivo | |
|---|---|---|
| `Grid` / `Grid2` / `GridLegacy` | renombrado en 7 (`Grid2` → `Grid`); `GridLegacy` eliminado en 9. Usar `Stack`, `Box` con flex o CSS grid | **[lint]** |
| Props legados: `componentsProps`, `PaperProps`, `InputProps`, `inputProps`, `InputLabelProps`, `SelectProps`, `MenuProps`, `TransitionProps`, `TransitionComponent`, `primaryTypographyProps`… | deprecados en 7 y eliminados en 9. Usar `slots` / `slotProps` | **[lint]** |
| imports profundos de 2.º nivel (`@mui/material/Button/Button`) | eliminados en 7. Importar desde la raíz | **[lint]** |
| `extendTheme` · `CssVarsProvider` · `theme.vars` | movidos o fusionados entre majors. Leer de `theme.cts` o de `--cts-*` | **[lint]** (imports) |
| Claves compuestas de `styleOverrides` (`containedPrimary`, `sizeSmall`…) | eliminadas en 9. Usar `variants` | |

`slotProps` **sí se permite** en las apps (decisión G6 de
[Estandares-Globales.md](Estandares-Globales.md)): es la API de MUI 7 y 9.
Lo que se mantiene es que los componentes **de cts-theme** exponen props
propias explícitas y no reenvían slots de MUI.

## Ejemplo de compuesto

```tsx
import { LoginShell } from '@industriascts/cts-theme/views'

export const AppLogin = (): React.JSX.Element => (
  <LoginShell logo={<MiLogo />} brandName="E-PANEL" tagline="Diseño de tableros">
    <MiFormulario />
  </LoginShell>
)
```
