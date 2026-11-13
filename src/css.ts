/**
 * Variables CSS del Sistema de Diseño CTS.
 *
 * Para lo que no usa MUI: `hmi-configurator`, `cts-hmi-symbols`, reportes
 * impresos, lienzos (maxgraph, three.js) y páginas estáticas. Mismos valores
 * que el tema MUI, leídos de `./colors` y `./tokens`.
 *
 * Se publica ya generada como `@industriascts/cts-theme/css`
 * (`dist/cts-theme.css`). El modo oscuro se activa con
 * `<html data-theme="dark">` o, si no hay atributo, con la preferencia del
 * sistema. `data-theme="light"` fuerza claro. Es el mismo contrato que ya
 * usan t-monitor y cts-hmi-symbols.
 */
import type { PaletteMode } from '@mui/material'
import {
  brandSurface,
  chrome,
  chromeDark,
  data8,
  palette as P,
  secondary,
  semantic,
  semanticDark,
  status,
  statusDark,
  surface,
  surfaceDark,
} from './colors'
import { brandFontFamily, fontFamily, motion, radii, shadows, shadowsDark, spacing, touch, zIndex, layout } from './tokens'

/** Prefijo de todas las variables. */
export const CSS_PREFIX = '--cts-'

const kebab = (s: string) => s.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)

/** Variables que cambian entre claro y oscuro. */
const modeVars = (mode: PaletteMode): Record<string, string> => {
  const isDark = mode === 'dark'
  const sem = isDark ? semanticDark : semantic
  const st = isDark ? statusDark : status
  const ch = isDark ? chromeDark : chrome
  return {
    bg: isDark ? surfaceDark.base : surface.soft,
    paper: isDark ? surfaceDark.paper : surface.paper,
    text: isDark ? surfaceDark.text : surface.navy,
    'text-muted': isDark ? surfaceDark.muted : surface.muted,
    'text-disabled': isDark ? surfaceDark.textDisabled : surface.textDisabled,
    divider: isDark ? surfaceDark.border : surface.border,
    'input-border': isDark ? surfaceDark.inputBorder : surface.inputBorder,
    'input-border-hover': ch.inputBorderHover,
    'brand-surface': isDark ? brandSurface.dark : brandSurface.light,
    tooltip: ch.tooltip,
    'table-head': ch.tableHead,
    'table-row-hover': ch.tableRowHover,
    save: ch.save,
    ...Object.fromEntries(Object.entries(sem).map(([k, v]) => [k, v])),
    ...Object.fromEntries(Object.entries(st).map(([k, v]) => [`status-${k}`, v])),
    'shadow-menu': isDark ? shadowsDark.menu : shadows.menu,
    'shadow-dialog': isDark ? shadowsDark.dialog : shadows.dialog,
    'shadow-paper': isDark ? shadowsDark.paper : shadows.paper,
  }
}

/** Variables iguales en los dos modos. */
const sharedVars = (): Record<string, string> => ({
  primary: P.blue,
  'primary-dark': P.blueDark,
  'primary-light': P.blueLight,
  secondary: secondary.main,
  'secondary-dark': secondary.dark,
  'on-brand': brandSurface.text,
  gray: P.gray,
  'gray-light': P.grayLight,
  'gray-dark': P.grayDark,
  ...Object.fromEntries(data8.map((c, i) => [`data-${i + 1}`, c])),
  font: fontFamily,
  'font-brand': brandFontFamily,
  ...Object.fromEntries(Object.entries(radii).map(([k, v]) => [`radius-${kebab(k)}`, `${v}px`])),
  'shadow-button': shadows.buttonContained,
  'focus-ring': shadows.focusRing,
  easing: motion.easing,
  ...Object.fromEntries(
    (['micro', 'nav', 'control', 'collapse'] as const).map((k) => [`duration-${k}`, motion[k]]),
  ),
  spacing: `${spacing.base}px`,
  gutter: `${spacing.gutter}px`,
  'rail-width': `${layout.railWidth}px`,
  'rail-icon-width': `${layout.railIconWidth}px`,
  'touch-target': `${touch.minTarget}px`,
  ...Object.fromEntries(
    Object.entries(zIndex)
      .filter(([k]) => k !== 'localMax')
      .map(([k, v]) => [`z-${kebab(k)}`, String(v)]),
  ),
})

/** Todas las variables de un modo, con prefijo: `{ '--cts-primary': '#0065BB', … }`. */
export const cssVariables = (mode: PaletteMode = 'light'): Record<string, string> =>
  Object.fromEntries(
    Object.entries({ ...sharedVars(), ...modeVars(mode) }).map(([k, v]) => [`${CSS_PREFIX}${k}`, v]),
  )

const block = (selector: string, vars: Record<string, string>, indent = '') =>
  `${indent}${selector} {\n${Object.entries(vars)
    .map(([k, v]) => `${indent}  ${k}: ${v};`)
    .join('\n')}\n${indent}}`

/**
 * Hoja de estilos completa: claro en `:root`, oscuro por atributo y por
 * preferencia del sistema. Es lo que se publica en `dist/cts-theme.css`.
 */
export const cssText = (): string => {
  const prefixed = (mode: PaletteMode) =>
    Object.fromEntries(Object.entries(modeVars(mode)).map(([k, v]) => [`${CSS_PREFIX}${k}`, v]))
  const shared = Object.fromEntries(Object.entries(sharedVars()).map(([k, v]) => [`${CSS_PREFIX}${k}`, v]))
  return [
    '/* @industriascts/cts-theme — variables CSS. Archivo generado desde src/css.ts: no editar. */',
    block(':root', { ...shared, ...prefixed('light'), 'color-scheme': 'light' }),
    block(':root[data-theme="dark"]', { ...prefixed('dark'), 'color-scheme': 'dark' }),
    `@media (prefers-color-scheme: dark) {\n${block(':root:not([data-theme])', { ...prefixed('dark'), 'color-scheme': 'dark' }, '  ')}\n}`,
    '',
  ].join('\n\n')
}
