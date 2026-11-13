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
  /**
   * `text.disabled` — E-Panel `theme/colors.ts:258`. Más oscuro que el
   * equivalente de cts-manager (`#b5bcc6`, ~1.8:1) para que se lea (3.49:1
   * sobre blanco). Decisión G8 de Estandares-Globales.md.
   */
  textDisabled: '#808a99',
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
  /** borde de inputs — fieldset 1.5px (ctsTheme.ts `MuiOutlinedInput`) */
  inputBorder: 'rgba(74,144,226,0.25)',
  /** `text.disabled` — alfa 0.45 de cts-manager aplanado sobre el fondo (E-Panel `colors.ts:189`) */
  textDisabled: '#626e81',
} as const

/* ── Chrome — piezas de interfaz que no son texto ni superficie ─────────── *
 * Valores de `theme.components` de cts-manager (`ctsTheme.ts`), idénticos en
 * E-Panel (`theme/mui.ts`). Los lee `src/mui/components.ts`.                */
export const chrome = {
  scrollbarThumb:      '#c0c8d4',
  scrollbarThumbHover: '#a0aab8',
  scrollbarTrack:      '#f0f4f9',
  /** borde del input en hover — `primary.main` */
  inputBorderHover:    '#0065BB',
  /** globo del tooltip — `text.primary` */
  tooltip:             '#1a2236',
  /** cabecera de tabla — `primary.main` con texto blanco */
  tableHead:           '#0065BB',
  tableHeadDivider:    'rgba(255,255,255,0.12)',
  tableCellBorder:     '#dde3ec',
  /** hover de fila, sólido (pisa celdas sticky sin transparentar) */
  tableRowHover:       '#f7fafd',
  /**
   * Botón «Guardar» y confirmaciones positivas. `#00c875` no llega a 2.2:1
   * sobre blanco (E-Panel `colors.ts:268`).
   */
  save:                '#0a9d5a',
} as const

export const chromeDark = {
  scrollbarThumb:      '#3d4f6f',
  scrollbarThumbHover: '#4a6090',
  scrollbarTrack:      '#253662',
  inputBorderHover:    'rgba(41,171,226,0.5)',
  tooltip:             '#1e2d42',
  tableHead:           '#2d3c53',
  tableHeadDivider:    'rgba(74,144,226,0.12)',
  tableCellBorder:     'rgba(74,144,226,0.1)',
  tableRowHover:       '#2f435e',
  save:                '#22c55e',
} as const

/* ── Estados de interacción — `palette.action` (ctsTheme.ts) ─────────────── *
 * En claro solo se ajustan hover y selected; el resto queda en MUI.          */
export const action = {
  hover:    'rgba(0,101,187,0.05)',
  selected: 'rgba(0,101,187,0.1)',
} as const

export const actionDark = {
  active:             'rgba(255,255,255,0.6)',
  hover:              'rgba(74,144,226,0.08)',
  selected:           'rgba(74,144,226,0.16)',
  disabled:           'rgba(255,255,255,0.28)',
  disabledBackground: 'rgba(255,255,255,0.08)',
  focus:              'rgba(74,144,226,0.12)',
} as const

/* ── Superficie de marca — rail, barra superior, panel del login ─────────── *
 * Losa azul en claro y papel oscuro en oscuro. Su contenido usa `tokens.rail`
 * (blancos con alfa), no la paleta de texto. E-Panel `brandSurfaceBg`.      */
export const brandSurface = {
  light: '#0065BB',
  dark:  '#253662',
  /** texto pleno sobre la losa (cabecera de tabla, rail, panel de marca) */
  text:  '#ffffff',
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

/* ── Estados de proceso y de equipo ────────────────────────────────────── *
 * Vocabulario único para HMI, tableros, alarmas y símbolos (cts-hmi-symbols).
 * Antes había 7 verdes de «OK» entre apps (Estandares-Globales.md §1.4).
 * Cada estado apunta a un semántico o a un primitivo de marca; no hay hex
 * nuevos. Son colores de gráfico (≥ 3:1 contra el fondo), no de texto.     */
export const status = {
  /** en marcha · energizado · cerrado · aprobado · normal */
  ok:       semantic.success,
  /** en proceso · reconocido · bloqueado · advertencia */
  warning:  semantic.warning,
  /** falla · disparado · alarma activa · error */
  fault:    semantic.error,
  /** fuera de línea · inactivo · abierto · sin datos — 3.63:1 sobre `surface.soft` */
  offline:  palette.gray,
  info:     semantic.info,
  /** selección en lienzos y editores */
  selected: palette.blue,
} as const

export const statusDark = {
  ok:       semanticDark.success,
  warning:  semanticDark.warning,
  fault:    semanticDark.error,
  /** `palette.gray` no pasa 3:1 sobre el papel oscuro (2.94:1); este da 7.47:1 */
  offline:  palette.grayLight,
  info:     semanticDark.info,
  /** 4.72:1 sobre `surfaceDark.base` */
  selected: palette.blueLight,
} as const

export type StatusName = keyof typeof status

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

/* ── Autocompletado del login — AuthPage.tsx:66-67 ─────────────────────── *
 * Chrome pinta los campos autocompletados con su propio fondo; el login lo
 * reemplaza por estos. No son `text.primary`: se copian literales.          */
export const authAutofill = {
  light: { bg: '#e8f0fe', text: '#1a1a1a' },
  dark:  { bg: '#253662', text: '#ffffff' },
} as const

/* ── Velos — capas sobre el contenido ──────────────────────────────────── */
export const scrim = {
  /** velo bajo el rail en modo overlay — E-Panel Sidebar.styles.ts (overlayBackdropSx) */
  rail: 'rgba(0,0,0,0.25)',
} as const

export type Scrim = typeof scrim
export type Chrome = typeof chrome
export type ChromeDark = typeof chromeDark
export type Status = typeof status
export type Palette = typeof palette
export type Surface = typeof surface
export type SurfaceDark = typeof surfaceDark
export type Semantic = typeof semantic
export type Secondary = typeof secondary
export type AuthAutofill = typeof authAutofill
