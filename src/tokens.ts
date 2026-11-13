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
  /** ctsTheme.ts `MuiButton.containedSecondary:hover` */
  buttonSecondaryHover: '0 4px 12px rgba(41,171,226,0.4)',
  /**
   * `Paper` con `elevation={1}` — ctsTheme.ts `MuiPaper.elevation1`. Pisa a
   * `elevation1` (que sigue siendo `theme.shadows[1]`). Decisión G11.
   */
  paper: '0 2px 8px rgba(0,0,0,0.07)',
  /** anillo de foco de inputs — ctsTheme.ts `MuiOutlinedInput .Mui-focused` */
  focusRing: '0 0 0 3px rgba(0,101,187,0.15)',
  /** notificación (snackbar) — cts-manager `GlobalSnackbar.tsx` */
  toast: '0 4px 20px rgba(0,0,0,0.25)',
} as const

/** Sombras en modo oscuro: negras y más densas. Mismas claves que `shadows`. */
export const shadowsDark = {
  elevation1: '0 1px 4px rgba(0,0,0,0.4)',
  paper: '0 2px 8px rgba(0,0,0,0.4)',
  menu: '0 8px 24px rgba(0,0,0,0.5)',
  dialog: '0 24px 64px rgba(0,0,0,0.7)',
} as const

/**
 * Escala `theme.shadows` 1-5; del 6 al 24 se repite `top`.
 * ctsTheme.ts `shadows` (idéntica en E-Panel `theme/mui.ts:75-83`).
 */
export const elevation = {
  light: [
    '0 1px 4px rgba(0,0,0,0.06)',
    '0 2px 8px rgba(0,0,0,0.08)',
    '0 4px 16px rgba(0,0,0,0.1)',
    '0 8px 24px rgba(0,0,0,0.12)',
    '0 12px 32px rgba(0,0,0,0.14)',
  ],
  lightTop: '0 16px 40px rgba(0,0,0,0.16)',
  dark: [
    '0 1px 4px rgba(0,0,0,0.4)',
    '0 2px 8px rgba(0,0,0,0.45)',
    '0 4px 16px rgba(0,0,0,0.5)',
    '0 8px 24px rgba(0,0,0,0.55)',
    '0 12px 32px rgba(0,0,0,0.6)',
  ],
  darkTop: '0 16px 40px rgba(0,0,0,0.65)',
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
  /**
   * Curva única. Reemplaza `ease`, `cubic-bezier(0.16,1,0.3,1)` (cts-manager)
   * y `cubic-bezier(0.2,0,0,1)` (E-Panel). Estandares-Globales.md §2.3.
   */
  easing: 'cubic-bezier(0.32, 0.72, 0, 1)',
} as const

/* ── Notificaciones — cts-manager `GlobalSnackbar.tsx` ──────────────────── */
export const notify = {
  /** aviso normal, en ms */
  autoHide: 4000,
  /** aviso con acción (p. ej. «Deshacer»): más tiempo para reaccionar */
  autoHideWithAction: 7000,
  /** ancho máximo desde `sm` */
  maxWidth: 560,
} as const

/* ── Capas (z-index) ───────────────────────────────────────────────────── *
 * Toda capa global sale de aquí o de `theme.zIndex`; los números sueltos
 * solo valen para apilar dentro de un componente (1-10). Se alinea con los
 * valores por defecto de MUI (appBar 1100, drawer 1200, modal 1300,
 * snackbar 1400, tooltip 1500). Antes: 1000-2100 dispersos en cada app.     */
export const zIndex = {
  /** apilado local dentro de un componente: 1 a `localMax` */
  localMax: 10,
  /** encabezados y columnas sticky */
  sticky: 3,
  /** acciones flotantes (zona 6) — `theme.zIndex.fab` */
  floating: 1050,
  /** barra superior o inferior de la app — `theme.zIndex.appBar` */
  bar: 1100,
  /** rail de navegación — `theme.zIndex.drawer` */
  rail: 1200,
  /** diálogos y velos — `theme.zIndex.modal` */
  modal: 1300,
  /** teclado virtual (HMI): encima de diálogos con campos, debajo de avisos */
  keyboard: 1350,
  /** notificaciones — `theme.zIndex.snackbar` */
  toast: 1400,
  /** tooltips — `theme.zIndex.tooltip` */
  tooltip: 1500,
  /** recorridos guiados: lo único por encima de todo */
  tour: 1600,
} as const

/* ── Perfil táctil (HMI / kiosco) ──────────────────────────────────────── *
 * t-monitor `VirtualKeyboard.tsx:51-54` (teclas 48-64) y WCAG 2.5.5.       */
export const touch = {
  /** objetivo táctil mínimo en el perfil `hmi` */
  minTarget: 48,
  keyMin: 48,
  keyMax: 64,
  /** fila de tabla en el perfil `hmi` */
  tableRow: 48,
} as const

/* ── Espaciado ─────────────────────────────────────────────────────────── */
export const spacing = {
  /** base MUI; medios pasos 2/4/6px permitidos */
  base: 8,
  /** gutter de página (`p: 3`) */
  gutter: 24,
  /** gutter de página bajo `sm` (`p: 1.5`) — cts-manager `AppLayout.tsx:54` */
  gutterCompact: 12,
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
  /** AppLayout.tsx:29 (cts-manager) · franja del botón de reapertura con el rail oculto */
  reopenStripWidth: 24,
  /** AppLayout.tsx:34 (cts-manager) · `top` sticky del botón de reapertura */
  reopenTop: 12,
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
  /** drawer derecho de detalle — cts-manager (440 / 720), `xs: '100%'` */
  sidePanelWidth: 440,
  sidePanelWideWidth: 720,
  /** columna de formulario dentro de una página */
  formMaxWidth: 560,
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
/** Familia de toda la interfaz, títulos incluidos. */
export const fontFamily =
  "'Titillium Web', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

/**
 * Familia de marca: solo wordmark, logo de texto, panel del login y barras
 * de marca. Nunca en títulos de contenido ni en texto corrido. Decisión G3.
 * Cada app aloja sus archivos (`Conthrax-*.woff2`); ver docs/Nueva-App.md.
 */
export const brandFontFamily = "'Conthrax', 'Titillium Web', sans-serif"

/**
 * Pesos permitidos. 500 y 800 NO existen en el sistema (no se cargan): un
 * 500 se escribe 600 y un 800 se escribe 700. Decisión G5.
 */
export const fontWeight = {
  light: 300,
  regular: 400,
  semibold: 600,
  bold: 700,
  /** solo wordmark (rail, login); con Titillium requiere cargar el 900 */
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
  /** ítem de menú */
  menuItem: 14,
  /** body1 */
  body: 15,
  /** título de diálogo */
  dialogTitle: 16,
  /** wordmark del rail (zona 2) */
  wordmark: 17,
} as const

export const letterSpacing = {
  /** título de sección del sidebar */
  sectionTitle: '0.1em',
  /**
   * cabecera de tabla — ctsTheme.ts `MuiTableCell.head`. Sin mayúsculas: el
   * nombre de la columna se muestra tal como se escribió (reporte del
   * 8-sep-2026 en ctsTheme.ts:221-228). Antes `0.06em`. Decisión G11.
   */
  tableHeader: '0.01em',
  /** botones y caption */
  control: '0.01em',
  /** overline */
  overline: '0.08em',
  /** eyebrow / micro-etiqueta */
  eyebrow: '0.32em',
  /** wordmark del rail */
  wordmark: '2px',
} as const

/* ── Login — pantalla de acceso (AuthPage.tsx de cts-manager) ───────────── */
export const login = {
  /** AuthPage.tsx:75 — `flex: 0 0 45%` del panel de marca */
  brandPanelBasis: '45%',
  /** AuthPage.tsx:140 — columna del formulario */
  formMaxWidth: 420,
  /** AuthPage.tsx:92-94 — wordmark de la marca */
  wordmarkSize: 42,
  wordmarkTracking: 4,
  /** AuthPage.tsx:102 — descriptor bajo el wordmark */
  taglineSize: 13,
  /**
   * Decisión L4 (2026-11-06): AuthPage usa 0.7 → 3.69:1 sobre `#0065BB`,
   * bajo el 4.5:1 de WCAG AA. Blanco a 0.83 es el mínimo que pasa sobre
   * `#0065BB`; 0.85 → 4.70:1 en claro y 8.99:1 sobre `#253662` en oscuro.
   */
  taglineOpacity: 0.85,
  taglineTracking: 1,
  /** AuthPage.tsx:123 — leyenda del panel de marca */
  legendSize: 12,
  /** Decisión L4: AuthPage usa 0.45 → 2.37:1. Mismo valor que el tagline. */
  legendOpacity: 0.85,
} as const

/* ── Breakpoints ────────────────────────────────────────────────────────── *
 * Los de MUI por defecto: las tres apps auditadas los usan sin cambios.
 * `< md` → rail temporal; `< sm` → teléfono (gutter compacto). Lo que falta
 * definir para móvil está en Mobile.md.                                     */
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
export type Login = typeof login
export type Breakpoints = typeof breakpoints
export type ShadowsDark = typeof shadowsDark
export type Elevation = typeof elevation
export type Notify = typeof notify
export type ZIndex = typeof zIndex
export type Touch = typeof touch

/** Bolsa única de tokens; se inyecta en el tema MUI como `theme.cts`. */
export const tokens = {
  radii,
  borders,
  shadows,
  shadowsDark,
  elevation,
  density,
  motion,
  notify,
  zIndex,
  touch,
  spacing,
  layout,
  rail,
  fontFamily,
  brandFontFamily,
  fontWeight,
  fontSize,
  letterSpacing,
  login,
  breakpoints,
  artboardWidth,
} as const

export type CtsTokens = typeof tokens
