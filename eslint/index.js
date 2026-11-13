/**
 * Preset de ESLint (flat config, ESLint 9) del Sistema de Diseño CTS.
 *
 * Convierte en errores las reglas de docs/Filosofia.md:
 *   - sin colores literales (hex, rgb, rgba, hsl) fuera de los archivos de tema
 *   - sin `Grid` de MUI ni imports profundos de `@mui/material`
 *   - sin `extendTheme` / `CssVarsProvider`
 *   - sin props legados de MUI (`PaperProps`, `InputProps`, `componentsProps`…):
 *     se usa `slotProps` (decisión G6)
 *   - sin `zIndex` global escrito a mano (> 10): `theme.zIndex` o `theme.cts.zIndex`
 *   - sin pesos 500 ni 800 (decisión G5)
 *
 * Uso en `eslint.config.js` de una app, después de su config de TypeScript:
 *
 * ```js
 * import tseslint from 'typescript-eslint'
 * import { ctsLint } from '@industriascts/cts-theme/eslint'
 *
 * export default tseslint.config(
 *   ...tseslint.configs.recommended,
 *   ...ctsLint({
 *     // carpetas con colores de dominio (lienzos, 3D, reportes, símbolos)
 *     domain: ['src/features/editor/**', 'src/three/**'],
 *     // 'warn' mientras se migra; 'error' cuando el conteo llegue a cero
 *     level: 'warn',
 *   }),
 * )
 * ```
 *
 * `no-restricted-syntax` y `no-restricted-imports` se reemplazan (no se
 * fusionan) si otra config los declara después. Para sumar reglas propias,
 * usa `ctsSyntaxRestrictions` y `ctsImportRestrictions` y declara una sola.
 */

const SOURCE_FILES = ['**/*.{js,jsx,ts,tsx,mjs,cjs,mts,cts}']

/** Archivos donde los valores literales SÍ se permiten. */
export const themeFiles = [
  '**/colors.{ts,js}',
  '**/tokens.{ts,js}',
  '**/theme/**',
  '**/*.test.{ts,tsx,js,jsx}',
  '**/*.spec.{ts,tsx,js,jsx}',
]

const COLOR_LITERAL = '/^(#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})|(?:rgba?|hsla?)\\(.*\\))$/'
const COLOR_IN_TEMPLATE = '/(?:^|[\\s:(,])(?:#[0-9a-fA-F]{3,8}\\b|(?:rgba?|hsla?)\\()/'

const LEGACY_PROPS = [
  'componentsProps',
  'PaperProps',
  'InputProps',
  'inputProps',
  'InputLabelProps',
  'SelectProps',
  'FormHelperTextProps',
  'MenuProps',
  'MenuListProps',
  'ModalProps',
  'BackdropProps',
  'TransitionProps',
  'TransitionComponent',
  'PopperProps',
  'primaryTypographyProps',
  'secondaryTypographyProps',
]

/** Selectores de `no-restricted-syntax` del sistema. */
export const ctsSyntaxRestrictions = [
  {
    selector: `Literal[value=${COLOR_LITERAL}]`,
    message:
      'Color literal. Usa un rol del tema (`palette.*`, `theme.cts.*`) o un primitivo de `@industriascts/cts-theme/colors`.',
  },
  {
    selector: `TemplateElement[value.raw=${COLOR_IN_TEMPLATE}]`,
    message: 'Color literal dentro de un template. Usa un rol del tema o una variable `--cts-*`.',
  },
  {
    selector: `JSXAttribute[name.name=/^(${LEGACY_PROPS.join('|')})$/]`,
    message: 'Prop legado de MUI (eliminado o deprecado en 7/9). Usa `slots` / `slotProps`.',
  },
  {
    selector: "Property[key.name='zIndex'] > Literal[value>10]",
    message: 'zIndex global a mano. Usa `theme.zIndex.*` o `theme.cts.zIndex.*`; los números sueltos solo de 1 a 10.',
  },
  {
    selector: "Property[key.name='fontWeight'] > Literal[value=/^(500|800)$/]",
    message: 'Peso no cargado en el sistema: 500 → 600, 800 → 700.',
  },
  {
    selector: "Property[key.name='fontWeight'] > Literal[value=500]",
    message: 'Peso no cargado en el sistema: 500 → 600.',
  },
  {
    selector: "Property[key.name='fontWeight'] > Literal[value=800]",
    message: 'Peso no cargado en el sistema: 800 → 700.',
  },
]

/** Opciones de `no-restricted-imports` del sistema. */
export const ctsImportRestrictions = {
  paths: [
    {
      name: '@mui/material',
      importNames: ['Grid', 'Grid2', 'GridLegacy', 'Unstable_Grid2', 'extendTheme', 'CssVarsProvider'],
      message: '`Grid` cambió en cada major (Grid2 → Grid → GridLegacy eliminado). Usa `Stack`, `Box` con flex o CSS grid.',
    },
    {
      name: '@mui/material/styles',
      importNames: ['extendTheme', 'CssVarsProvider', 'experimental_extendTheme', 'Experimental_CssVarsProvider'],
      message: 'API de variables CSS de MUI movida entre majors. Lee de `theme.cts` o de `--cts-*`.',
    },
  ],
  patterns: [
    {
      group: ['@mui/material/Grid', '@mui/material/Grid2', '@mui/material/GridLegacy', '@mui/material/Unstable_Grid2'],
      message: 'Sin `Grid` de MUI. Usa `Stack`, `Box` con flex o CSS grid.',
    },
    {
      group: ['@mui/material/*/*'],
      message: 'Import profundo de segundo nivel (eliminado en MUI 7). Importa desde `@mui/material`.',
    },
  ],
}

/**
 * Config lista para usar.
 *
 * @param {object} [options]
 * @param {string[]} [options.domain] globs de carpetas con colores de dominio, exentas de la regla de color
 * @param {'error' | 'warn'} [options.level] severidad; por defecto `'error'`
 * @returns {import('eslint').Linter.Config[]}
 */
export function ctsLint({ domain = [], level = 'error' } = {}) {
  const noColor = ctsSyntaxRestrictions.filter((r) => !r.selector.includes('Literal[value=/^(#') && !r.selector.startsWith('TemplateElement'))
  return [
    {
      name: 'cts-theme/rules',
      files: SOURCE_FILES,
      rules: {
        'no-restricted-syntax': [level, ...ctsSyntaxRestrictions],
        'no-restricted-imports': [level, ctsImportRestrictions],
      },
    },
    {
      name: 'cts-theme/theme-and-domain-files',
      files: [...themeFiles, ...domain],
      rules: {
        'no-restricted-syntax': [level, ...noColor],
      },
    },
  ]
}

export default ctsLint()
