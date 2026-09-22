/**
 * Colores del Sistema de Diseño CTS.
 *
 * Valores **literales** de `cts-manager/frontend/src/theme/ctsTheme.ts`,
 * tal como los recoge la hoja «Colores» de `docs/demo/`.
 * No redondear ni aproximar.
 *
 * TODO
 * - Utilizar oklch
 * - Añadir un 'fallback' para convertir de oklch a hex para retrocompatibilidad
 */

/**
 * Colores primarios de la paleta de colores corporativos.
 */
export const palette = {
  blue:       '#0065BB',
  blueLight:  '#29ABE2',
  blueDark:   '#004696',
  /** @deprecated Declarado en el tema pero sin uso. La hoja «Colores» indica: no usar. */
  blueGrad1:  '#003B8E',
  gray:       '#7F7F7F',
  grayLight:  '#C9C9C9',
  grayDark:   '#5A5A5A',
} as const

/* ── Superficie — modo claro ───────────────────────────────────────────── */
export const surface = {
  /** `background.default` — fondo de aplicación */
  soft:        '#f0f4f9',
  /** `background.paper` — cards, menús, diálogos */
  paper:       '#ffffff',
  /** `text.primary` */
  navy:        '#1a2236',
  /** `text.secondary` — etiquetas, texto de apoyo */
  muted:       '#5a6a80',
  /** `divider` — hairline universal */
  border:      '#dde3ec',
  /** borde de inputs — fieldset 1.5px */
  inputBorder: '#d0d8e4',
} as const

/* ── Superficie — modo oscuro ──────────────────────────────────────────── *
 * Regla de la hoja «Modo oscuro»: el papel es MÁS CLARO que el fondo.       */
export const surfaceDark = {
  /** `background.default` */
  base:        '#2A3547',
  /** `background.paper` — más claro que el fondo, y color del rail en oscuro */
  paper:       '#253662',
  /** `text.primary` */
  text:        '#e8edf4',
  /** `text.secondary` */
  muted:       '#a6b4c8',
  /** `divider` */
  border:      'rgba(74,144,226,0.12)',
} as const

/* ── Semánticos ────────────────────────────────────────────────────────── */
export const semantic = {
  error:   '#e2445c',
  warning: '#fdab3d',
  success: '#00c875',
  info:    '#29ABE2',
} as const

export const semanticDark = {
  error:   '#ef4444',
  warning: '#f59e0b',
  success: '#22c55e',
  info:    '#06b6d4',
} as const

/* ── Secundario ────────────────────────────────────────────────────────── */
export const secondary = {
  main:  '#29ABE2',
  dark:  '#1a8ab8',
  light: '#6dcbee',
} as const

/* ── Paleta de datos ───────────────────────────────────────────────────── *
 * «Color funcional, no decorativo»: el chrome es azul + gris; estos 8 quedan
 * para datos del usuario (estados, grupos, gráficos). Orden significativo.   */
export const data8 = [
  '#0065BB',
  '#29ABE2',
  '#00c875',
  '#fdab3d',
  '#e2445c',
  '#a25ddc',
  '#ff642e',
  '#579bfc',
] as const

export type Data8 = typeof data8
export type DataColor = Data8[number]

/** Color de datos por índice, cíclico — para series de longitud arbitraria. */
export const dataColor = (index: number): DataColor =>
  data8[((index % data8.length) + data8.length) % data8.length] as DataColor

/**
 * Tinte de superficie para un color semántico o de datos.
 * La hoja «Controles» lo especifica como sufijo hex sobre el color pleno
 * (`color + '20'` / `+ '18'`), con el texto en el color pleno.
 */
export const tint = (hex: string, alpha: '20' | '18' = '20'): string => hex + alpha

export type Palette = typeof palette
export type Surface = typeof surface
export type SurfaceDark = typeof surfaceDark
export type Semantic = typeof semantic
export type Secondary = typeof secondary
