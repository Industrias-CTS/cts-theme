import type { PaletteMode, ThemeOptions } from '@mui/material'
import { createTheme } from '@mui/material/styles'
import { palette as P, surface, surfaceDark, semantic, semanticDark, secondary } from '../colors'
import { tokens, radii, fontFamily, fontWeight, fontSize, letterSpacing, spacing, breakpoints } from '../tokens'

import './augmentation'

/**
 * 'Helper' para creación de paleta disponible para componentes de MUI
 *
 * Fuente: hojas «Colores» y «Modo oscuro».
 */
export const palette = (mode: PaletteMode) => {

	const isDark = mode === 'dark'

	return {
      mode,
      primary:    { main: P.blue, dark: P.blueDark, light: P.blueLight, contrastText: '#fff' },
      secondary:  { main: secondary.main, dark: secondary.dark, light: secondary.light, contrastText: '#fff' },
      background: isDark
        ? { default: surfaceDark.base, paper: surfaceDark.paper }
        : { default: surface.soft, paper: surface.paper },
      text: isDark
        ? { primary: surfaceDark.text, secondary: surfaceDark.muted }
        : { primary: surface.navy, secondary: surface.muted },
      divider:    isDark ? surfaceDark.border : surface.border,
      error:   { main: isDark ? semanticDark.error   : semantic.error },
      warning: { main: isDark ? semanticDark.warning : semantic.warning },
      success: { main: isDark ? semanticDark.success : semantic.success },
      info:    { main: isDark ? semanticDark.info    : semantic.info },
      ...(isDark ? {
        action: {
          active:            'rgba(255,255,255,0.6)',
          hover:             'rgba(74,144,226,0.08)',
          selected:          'rgba(74,144,226,0.16)',
          disabled:          'rgba(255,255,255,0.28)',
          disabledBackground:'rgba(255,255,255,0.08)',
          focus:             'rgba(74,144,226,0.12)',
        },
      } : {
        action: {
          hover:    'rgba(0,101,187,0.05)',
          selected: 'rgba(0,101,187,0.1)',
        },
      }),
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
  button: { fontWeight: fontWeight.semibold, letterSpacing: '0.01em', textTransform: 'none' as const },
  caption: { fontSize: fontSize.caption, letterSpacing: '0.01em' },
  overline: {
    fontSize: fontSize.overline,
    fontWeight: fontWeight.semibold,
    letterSpacing: letterSpacing.overline,
    textTransform: 'uppercase' as const,
  },
}

/**
 * Opciones base del tema CTS, sin `components`.
 *
 * Los overrides de `components` (botones, inputs, chips, tabs, menús,
 * diálogos, tablas — hojas «Controles» y «Tablas y listas») NO están aquí
 * a propósito: los nombres de slot y los `defaultProps` cambian entre MUI 6,
 * 7 y 9, así que son una decisión aparte. Ver INSTRUCCIONES-COMPONENTES.md.
 */
export const themeOptions = (mode: PaletteMode): ThemeOptions => ({
  palette: palette(mode),
  typography,
  shape: { borderRadius: radii.base },
  spacing: spacing.base,
  breakpoints: { values: { ...breakpoints } },
  cts: tokens,
})

/**
 * Tema CTS listo para `<ThemeProvider theme={...}>`.
 *
 * Deja `theme.cts` disponible dentro de cualquier `sx`.
 */
export const createCtsTheme = (mode: PaletteMode = 'light') =>
  createTheme(themeOptions(mode))

/**
 *
 * TODO
 * 	- Conversión de oklch a rgba a hex
 */
