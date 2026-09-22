/**
 * Tokens del Sistema de Diseño CTS.
 *
 * Todos los valores son **literales** copiados de las hojas del sistema
 * (`docs/demo/build.py`), que a su vez los copia de
 * `cts-manager/frontend/src/theme/ctsTheme.ts` y sus componentes.
 *
 * Regla de oro: no redondear ni aproximar. Los tamaños fraccionales
 * (9.5, 10.5, 12.5, 13.5, 15.5 px) son intencionales.
 *
 * Fuente por grupo:
 *   radii · borders · shadows · density · motion  → hoja «Forma y espacio»
 *   rail                                          → hoja «Navegación»
 *   layout                                        → hoja «Estructura»
 *   fontSize · fontWeight · letterSpacing         → hoja «Tipografía»
 */

/* ── Radios — por nivel de elevación (hoja «Forma y espacio») ───────────── */
export const radii = {
  /** chips, menu-item, tooltip */
  chip: 6,
  /** botones, inputs, list-item, nav-item */
  control: 8,
  /** menús, tablas (base) — `shape.borderRadius` del tema */
  base: 10,
  /** cards, paper */
  card: 12,
  /** diálogos */
  dialog: 14,
  /** diálogos destacados (`borderRadius: 3` en MUI spacing) */
  dialogFeature: 30,
  /** píldoras y badges */
  pill: 99,
} as const

/* ── Bordes — «los bordes estructuran, no las sombras» ──────────────────── */
export const borders = {
  /** hairline universal — divisores, cards, tablas */
  hairline: 1,
  /** énfasis: fieldset de inputs, botones outlined, cards seleccionables */
  emphasis: 1.5,
  /** subrayado de tabs, avatar del rail */
  accent: 2,
  /** nav activo (borde izq.), indicadores de drop, acento de tipo de columna */
  indicator: 3,
  /** riel de color de grupo / tablero */
  groupRail: 4,
} as const

/* ── Sombras — azuladas en claro, reservadas a capas flotantes ──────────── */
export const shadows = {
  /** las cards son planas: borde, sin sombra */
  card: 'none',
  elevation1: '0 1px 4px rgba(0,0,0,0.06)',
  buttonContained: '0 2px 8px rgba(0,101,187,0.3)',
  buttonContainedHover: '0 4px 12px rgba(0,101,187,0.4)',
  buttonSecondary: '0 2px 8px rgba(41,171,226,0.3)',
  menu: '0 8px 24px rgba(0,101,187,0.15)',
  dialog: '0 24px 64px rgba(0,101,187,0.18)',
  sidebar: '4px 0 20px rgba(0,0,0,0.2)',
  tooltipRich: '0 6px 20px rgba(0,101,187,0.12)',
  /** círculos de acción flotante (zona 6) — misma que elevación 1 */
  floatingAction: '0 1px 4px rgba(0,0,0,0.06)',
} as const

/* ── Densidad — «densidad de hoja de cálculo» (alturas en px) ───────────── */
export const density = {
  tableRow: 38,
  gridRow: 40,
  groupHeader: 44,
  groupSummary: 36,
  /** TextField / botón dentro de la toolbar de vista (zona 8) */
  toolbarControl: 32,
  navItem: 34,
  workspaceSelector: 42,
  railSearch: 34,
  chip: 24,
  chipCount: 20,
  chipBadge: 18,
  inlineEdit: 26,
  /** círculo de acción flotante (zona 6) */
  floatingAction: 38,
  /** avatar del footer del rail (zona 5) */
  avatar: 32,
  /** logo de la cabecera del rail (zona 2) */
  railLogo: 34,
} as const

/* ── Animación ─────────────────────────────────────────────────────────── */
export const motion = {
  /** micro: opacidad de botones ocultos, swatches */
  micro: '0.12s',
  /** nav, list-items, menú (background), hovers de fila */
  nav: '0.15s',
  /** botones (all), focus ring de inputs */
  control: '0.2s',
  /** colapso del sidebar, cambio de tema */
  collapse: '0.25s',
  /** ease global */
  easing: 'cubic-bezier(0.32, 0.72, 0, 1)',
} as const

/* ── Espaciado ─────────────────────────────────────────────────────────── */
export const spacing = {
  /** base MUI; medios pasos 2/4/6px permitidos */
  base: 8,
  /** gutter de página (`p: 3`) */
  gutter: 24,
  cardGapMin: 16,
  cardGapMax: 24,
} as const

/* ── Layout — shell de aplicación, zonas 1-10 (hoja «Estructura») ───────── */
export const layout = {
  /** zona 1 · rail de navegación, ancho fijo */
  railWidth: 256,
  /** zona 1 · colapsado a 0 con FAB de reapertura */
  railCollapsedWidth: 0,
  /** zona 1 · alternativa de colapso declarada en la hoja: solo iconos */
  railIconWidth: 64,
  /** zona 6 · acciones flotantes, `position: fixed` */
  floatingTop: 16,
  floatingRight: 16,
  /** zona 7 · separación bajo la cabecera de vista */
  viewHeaderMarginBottom: 24,
  /** zona 7 · separación entre migas y título */
  breadcrumbMarginBottom: 8,
  /** zona 8 · ancho del campo de búsqueda de la toolbar */
  toolbarSearchWidth: 200,
  toolbarSelectMinWidth: 135,
  toolbarSelectMaxWidth: 185,
  /** zona 10 · panel lateral */
  panelMinWidth: 300,
  panelMaxWidth: 360,
} as const

/* ── Rail — colores propios del riel azul (hoja «Navegación») ───────────── *
 * El rail es una losa de color sólido: su contenido NO usa la paleta de
 * texto del tema, sino blancos con alfa sobre el azul.                      */
export const rail = {
  itemActiveBg: 'rgba(255,255,255,0.18)',
  itemActiveBorder: 'rgba(255,255,255,0.9)',
  itemHoverBg: 'rgba(255,255,255,0.1)',
  itemIdleColor: 'rgba(255,255,255,0.65)',
  itemActiveColor: '#ffffff',
  divider: 'rgba(255,255,255,0.1)',
  searchBg: 'rgba(255,255,255,0.08)',
  searchBorder: 'rgba(255,255,255,0.15)',
  searchPlaceholder: 'rgba(255,255,255,0.4)',
  sectionTitle: 'rgba(255,255,255,0.45)',
  descriptor: 'rgba(255,255,255,0.55)',
  footerBg: 'rgba(0,0,0,0.15)',
  avatarBg: 'rgba(255,255,255,0.2)',
  avatarBorder: 'rgba(255,255,255,0.35)',
  logoutHoverBg: 'rgba(255,100,100,0.2)',
  logoutHoverColor: 'rgba(255,180,180,1)',
} as const

/* ── Tipografía (hoja «Tipografía») ─────────────────────────────────────── */
export const fontFamily =
  "'Titillium Web', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

export const fontWeight = {
  light: 300,
  regular: 400,
  semibold: 600,
  bold: 700,
  /** wordmark del rail */
  black: 900,
} as const

/** Tamaños fraccionales intencionales — no redondear. */
export const fontSize = {
  /** descriptor del producto en la cabecera del rail (zona 2) */
  descriptor: 9.5,
  /** título de sección del sidebar (zona 4) */
  sectionTitle: 10,
  /** rol del usuario (zona 5) */
  userRole: 10.5,
  /** cabecera de tabla · eyebrow · overline */
  overline: 11,
  caption: 12,
  /** nombre del usuario (zona 5) · búsqueda del rail */
  userName: 12.5,
  /** fila de datos · body2 · migas de pan */
  dense: 13,
  /** etiqueta de nav (zona 4) */
  navLabel: 13.5,
  /** body1 */
  body: 15,
  /** wordmark del rail (zona 2) */
  wordmark: 17,
} as const

export const letterSpacing = {
  /** título de sección del sidebar */
  sectionTitle: '0.1em',
  /** cabecera de tabla */
  tableHeader: '0.06em',
  /** overline */
  overline: '0.08em',
  /** eyebrow / micro-etiqueta */
  eyebrow: '0.32em',
  /** wordmark del rail */
  wordmark: '2px',
} as const

/* ── Breakpoints ────────────────────────────────────────────────────────── *
 * PROVISIONAL. El Sistema de Diseño CTS no define móvil todavía; estos son
 * los valores por defecto de MUI, incluidos para que los componentes tengan
 * un eje sobre el que crecer. Ver MOBILE-TBD.md antes de usarlos como norma. */
export const breakpoints = {
  xs: 0,
  sm: 600,
  md: 900,
  lg: 1200,
  xl: 1536,
} as const

/** Ancho de referencia de las hojas del sistema (artboards). */
export const artboardWidth = 1440

export type Radii = typeof radii
export type Borders = typeof borders
export type Shadows = typeof shadows
export type Density = typeof density
export type Motion = typeof motion
export type Spacing = typeof spacing
export type Layout = typeof layout
export type Rail = typeof rail
export type FontSize = typeof fontSize
export type FontWeight = typeof fontWeight
export type LetterSpacing = typeof letterSpacing
export type Breakpoints = typeof breakpoints

/** Bolsa única de tokens; se inyecta en el tema MUI como `theme.cts`. */
export const tokens = {
  radii,
  borders,
  shadows,
  density,
  motion,
  spacing,
  layout,
  rail,
  fontFamily,
  fontWeight,
  fontSize,
  letterSpacing,
  breakpoints,
  artboardWidth,
} as const

export type CtsTokens = typeof tokens
