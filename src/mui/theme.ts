import type { PaletteMode, ThemeOptions } from '@mui/material'
import { createTheme } from '@mui/material/styles'
import type { Shadows } from '@mui/material/styles'
import { palette as P, surface, surfaceDark, semantic, semanticDark, secondary, brandSurface, action, actionDark } from '../colors'
import { tokens, radii, elevation, fontFamily, fontWeight, fontSize, letterSpacing, spacing, breakpoints } from '../tokens'
import { components } from './components'
import type { CtsProfile } from './components'

import './augmentation'

export type { CtsProfile }

export interface CtsThemeOptions {
  /** `'app'` (por defecto) o `'hmi'` para pantallas táctiles. Ver docs/Mobile.md. */
  profile?: CtsProfile
}

/**
 * 'Helper' para creación de paleta disponible para componentes de MUI
 *
 * Fuente: hojas «Colores» y «Modo oscuro».
 */
export const palette = (mode: PaletteMode) => {

	const isDark = mode === 'dark'

	return {
      mode,
      primary:    { main: P.blue, dark: P.blueDark, light: P.blueLight, contrastText: brandSurface.text },
      secondary:  { main: secondary.main, dark: secondary.dark, light: secondary.light, contrastText: brandSurface.text },
      background: isDark
        ? { default: surfaceDark.base, paper: surfaceDark.paper }
        : { default: surface.soft, paper: surface.paper },
      text: isDark
        ? { primary: surfaceDark.text, secondary: surfaceDark.muted, disabled: surfaceDark.textDisabled }
        : { primary: surface.navy, secondary: surface.muted, disabled: surface.textDisabled },
      divider:    isDark ? surfaceDark.border : surface.border,
      error:   { main: isDark ? semanticDark.error   : semantic.error },
      warning: { main: isDark ? semanticDark.warning : semantic.warning },
      success: { main: isDark ? semanticDark.success : semantic.success },
      info:    { main: isDark ? semanticDark.info    : semantic.info },
      action: isDark ? { ...actionDark } : { ...action },
	}}

/**
 * Tipografía del tema — hoja «Tipografía».
 *
 * h1–h5 conservan los tamaños por defecto de MUI y solo cambian peso y
 * tracking; el resto lleva los valores literales del sistema.
 */
export const typography = {
  fontFamily,
  fontWeightLight:    fontWeight.light,
  fontWeightRegular:  fontWeight.regular,
  fontWeightMedium:   fontWeight.semibold,
  fontWeightBold:     fontWeight.bold,
  h1: { fontWeight: fontWeight.bold, letterSpacing: '-0.5px' },
  h2: { fontWeight: fontWeight.bold, letterSpacing: '-0.25px' },
  h3: { fontWeight: fontWeight.bold },
  h4: { fontWeight: fontWeight.bold },
  h5: { fontWeight: fontWeight.bold },
  h6: { fontWeight: fontWeight.semibold },
  subtitle1: { fontSize: '1rem', lineHeight: 1.4, fontWeight: fontWeight.semibold },
  subtitle2: { fontSize: fontSize.dense, fontWeight: fontWeight.semibold },
  body1: { fontSize: fontSize.body, lineHeight: 1.6, fontWeight: fontWeight.regular },
  body2: { fontSize: fontSize.dense, lineHeight: 1.5, fontWeight: fontWeight.regular },
  button: { fontWeight: fontWeight.semibold, letterSpacing: letterSpacing.control, textTransform: 'none' as const },
  caption: { fontSize: fontSize.caption, letterSpacing: letterSpacing.control },
  overline: {
    fontSize: fontSize.overline,
    fontWeight: fontWeight.semibold,
    letterSpacing: letterSpacing.overline,
    textTransform: 'uppercase' as const,
  },
}

/**
 * Escala `theme.shadows` de 25 entradas: `none`, cinco niveles y el nivel
 * superior repetido. ctsTheme.ts `shadows`.
 */
export const shadowScale = (mode: PaletteMode): Shadows => {
  const isDark = mode === 'dark'
  const steps = isDark ? elevation.dark : elevation.light
  const top = isDark ? elevation.darkTop : elevation.lightTop
  return ['none', ...steps, ...Array<string>(19).fill(top)] as Shadows
}

/**
 * Opciones completas del tema CTS: paleta, tipografía, forma, sombras,
 * overrides de componentes (`./components`) y tokens en `theme.cts`.
 *
 * Para extenderlo en una app: `createTheme(themeOptions(mode), propias)`.
 */
export const themeOptions = (mode: PaletteMode, options: CtsThemeOptions = {}): ThemeOptions => ({
  palette: palette(mode),
  typography,
  shape: { borderRadius: radii.base },
  spacing: spacing.base,
  breakpoints: { values: { ...breakpoints } },
  shadows: shadowScale(mode),
  components: components(mode, options.profile),
  cts: tokens,
})

/**
 * Tema CTS listo para `<ThemeProvider theme={...}>`.
 *
 * Deja `theme.cts` disponible dentro de cualquier `sx`. El perfil `hmi` se
 * usa en modo oscuro por defecto: `createCtsTheme('dark', { profile: 'hmi' })`.
 */
export const createCtsTheme = (mode: PaletteMode = 'light', options: CtsThemeOptions = {}) =>
  createTheme(themeOptions(mode, options))
