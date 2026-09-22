/**
 * cts-theme — Sistema de Diseño CTS para JavaScript/TypeScript.
 *
 * Fuente de verdad de los valores: `docs/demo/` en este repo,
 * que los copia literalmente de `cts-manager/frontend/src/theme/ctsTheme.ts`.
 */
export * from './colors'
export * from './tokens'

/**
 * `palette` existe con dos sentidos: los hexes de marca en `./colors` y la
 * fábrica de paleta MUI en `./mui/theme`. En el barrel gana el de marca; la
 * fábrica se reexporta como `muiPalette`. Sin ambigüedad se pueden importar
 * las dos por su ruta: `@industriascts/cts-theme/colors` y `/mui`.
 */
export {
  palette as muiPalette,
  typography,
  themeOptions,
  createCtsTheme,
} from './mui/theme'

import './mui/augmentation'
