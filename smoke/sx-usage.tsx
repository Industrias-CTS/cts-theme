/**
 * Prueba de humo de tipos — NO se publica (vive fuera de `src`).
 *
 * Verifica, contra MUI 6 · 7 · 9, que la decisión de escribir el sistema con
 * el prop `sx` se sostiene: que `theme.cts` está visible dentro de un `sx` y
 * que los tokens tienen los tipos que los componentes de zona van a usar.
 *
 * Si esto compila en los tres majors, el rango `^6 || ^7 || ^9` de
 * `peerDependencies` está respaldado por una comprobación, no por una
 * suposición.
 *
 * Reglas que este archivo respeta a propósito (ver INSTRUCCIONES-COMPONENTES.md):
 *   - nada de `Grid`   → renombrado en 7, `GridLegacy` eliminado en 9
 *   - nada de `slotProps`/`componentsProps` → consolidados en 7
 *   - nada de imports profundos de segundo nivel → eliminados en 7
 *   - nada de `extendTheme`/`CssVarsProvider`/`theme.vars`
 */
import { Box, Stack, ThemeProvider } from '@mui/material'
import { createCtsTheme, dataColor, tint, semantic } from '../src/index'

const light = createCtsTheme('light')
const dark = createCtsTheme('dark')

/** Zona 1 — el rail leyendo ancho, sombra y colapso desde `theme.cts`. */
export const RailProbe = () => (
  <Box
    component="aside"
    sx={(t) => ({
      width: t.cts.layout.railWidth,
      background: t.palette.primary.main,
      boxShadow: t.cts.shadows.sidebar,
      transition: `width ${t.cts.motion.collapse} ${t.cts.motion.easing}`,
      overflow: 'hidden',
    })}
  />
)

/** Zona 4 — estados exactos del ítem de navegación. */
export const NavItemProbe = ({ active }: { active: boolean }) => (
  <Box
    sx={(t) => ({
      height: t.cts.density.navItem,
      margin: `0 12px 2px 12px`,
      padding: '0 12px',
      borderRadius: `${t.cts.radii.control}px`,
      fontSize: t.cts.fontSize.navLabel,
      fontWeight: t.cts.fontWeight.semibold,
      borderLeft: `${t.cts.borders.indicator}px solid ${
        active ? t.cts.rail.itemActiveBorder : 'transparent'
      }`,
      background: active ? t.cts.rail.itemActiveBg : 'transparent',
      color: active ? t.cts.rail.itemActiveColor : t.cts.rail.itemIdleColor,
      transition: `background ${t.cts.motion.nav} ${t.cts.motion.easing}`,
      '&:hover': { background: t.cts.rail.itemHoverBg },
    })}
  />
)

/** Zona 9 — gutter de página y radio de card. */
export const ContentProbe = () => (
  <Stack
    sx={(t) => ({
      padding: `${t.cts.spacing.gutter}px`,
      gap: `${t.cts.spacing.cardGapMin}px`,
      borderRadius: `${t.cts.radii.card}px`,
      boxShadow: t.cts.shadows.card,
      border: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
    })}
  />
)

/** Micro-tipografía: los tamaños fraccionales sobreviven al tipado. */
export const EyebrowProbe = () => (
  <Box
    sx={(t) => ({
      fontSize: t.cts.fontSize.overline,
      fontWeight: t.cts.fontWeight.bold,
      letterSpacing: t.cts.letterSpacing.eyebrow,
      textTransform: 'uppercase',
      color: t.palette.primary.main,
    })}
  />
)

/** Paleta de datos y tintes, fuera del tema. */
export const DataProbe = () => (
  <Box sx={{ color: dataColor(11), background: tint(semantic.success, '20') }} />
)

export const App = () => (
  <ThemeProvider theme={light}>
    <RailProbe />
    <NavItemProbe active />
    <ContentProbe />
    <EyebrowProbe />
    <DataProbe />
    <ThemeProvider theme={dark}>
      <RailProbe />
    </ThemeProvider>
  </ThemeProvider>
)
