import { palette as P } from '../colors'
import { type PaletteMode } from '@mui/material'

/**
 * 'Helper' para creación de paleta disponible para componentes de MUI
 *
 */
export const palette = (mode: PaletteMode) => {

	const isDark = mode === 'dark'

	return {
      mode,
      primary:    { main: P.blue, dark: P.blueDark, light: P.blueLight, contrastText: '#fff' },
      secondary:  { main: P.blueLight, dark: '#1a8ab8', light: '#6dcbee', contrastText: '#fff' },
      background: isDark
        ? { default: '#2A3547', paper: '#253662' }
        : { default: '#f0f4f9', paper: '#ffffff' },
      text: isDark
        ? { primary: '#e8edf4', secondary: '#a6b4c8' }
        : { primary: '#1a2236', secondary: '#5a6a80' },
      divider:    isDark ? 'rgba(74,144,226,0.12)' : '#dde3ec',
      error:   { main: isDark ? '#ef4444' : '#e2445c' },
      warning: { main: isDark ? '#f59e0b' : '#fdab3d' },
      success: { main: isDark ? '#22c55e' : '#00c875' },
      info:    { main: isDark ? '#06b6d4' : P.blueLight },
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
 *
 * TODO
 * 	- Conversión de oklch a rgba a hex
 */
