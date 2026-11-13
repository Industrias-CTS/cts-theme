/**
 * Overrides de componentes MUI del Sistema de Diseño CTS.
 *
 * Copia literal de `theme.components` de cts-manager
 * (`frontend/src/theme/ctsTheme.ts`, rama `production` `50010f9`), que E-Panel
 * repite casi idéntico en `apps/web/src/theme/mui.ts`. Aquí ya no hay ningún
 * hex: todo sale de `../colors` y `../tokens`.
 *
 * Compatibilidad: solo se usan `styleOverrides` con claves de slot que
 * existen igual en MUI 6, 7 y 9, y un único `defaultProps.slotProps`
 * (Tooltip), que los tres aceptan. Lo comprueba `pnpm typecheck:matrix`.
 *
 * Perfil `hmi` (t-monitor y pantallas táctiles): objetivos de 48 px, filas
 * de tabla de 48, sin selección de texto ni resaltado al tocar. Ver
 * docs/Mobile.md § «Perfil HMI».
 */
import type { PaletteMode, ThemeOptions } from '@mui/material'
import { brandSurface, chrome, chromeDark, palette as P, secondary, surface, surfaceDark } from '../colors'
import { borders, fontSize, fontWeight, letterSpacing, motion, radii, shadows, shadowsDark, touch } from '../tokens'

/** `app`: escritorio y web (por defecto). `hmi`: pantallas táctiles y kioscos. */
export type CtsProfile = 'app' | 'hmi'

const px = (n: number) => `${n}px`
const rem = (n: number) => `${n / 16}rem`

export const components = (
  mode: PaletteMode,
  profile: CtsProfile = 'app',
): NonNullable<ThemeOptions['components']> => {
  const isDark = mode === 'dark'
  const isHmi = profile === 'hmi'
  const C = isDark ? chromeDark : chrome
  const divider = isDark ? surfaceDark.border : surface.border
  const flat = isDark ? { backgroundImage: 'none' } : {}
  const hairline = (color: string) => `${borders.hairline}px solid ${color}`
  const touchTarget = isHmi ? { minHeight: touch.minTarget } : {}

  return {
    MuiCssBaseline: {
      styleOverrides: {
        '*': {
          scrollbarWidth: 'thin',
          scrollbarColor: `${C.scrollbarThumb} ${C.scrollbarTrack}`,
        },
        body: {
          transition: `background-color ${motion.collapse} ease, color ${motion.collapse} ease`,
          // La página nunca se desplaza de lado; `clip` y no `hidden` para no
          // crear contenedor de scroll y conservar los sticky (ctsTheme.ts).
          overflowX: 'clip',
          ...(isHmi
            ? {
                userSelect: 'none',
                touchAction: 'manipulation',
                WebkitTapHighlightColor: 'transparent',
              }
            : {}),
        },
        '*::-webkit-scrollbar': { width: 6, height: 6 },
        '*::-webkit-scrollbar-track': { background: C.scrollbarTrack, borderRadius: 3 },
        '*::-webkit-scrollbar-thumb': {
          background: C.scrollbarThumb,
          borderRadius: 3,
          '&:hover': { background: C.scrollbarThumbHover },
        },
        // Un campo editable sigue siendo seleccionable en el perfil HMI.
        ...(isHmi ? { 'input, textarea, [contenteditable="true"]': { userSelect: 'text' } } : {}),
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: fontWeight.semibold,
          borderRadius: radii.control,
          transition: `all ${motion.control}`,
          ...touchTarget,
          // `variants` y no `containedPrimary`/`sizeSmall`: MUI 9 eliminó las
          // claves compuestas; `variants` existe igual en 6, 7 y 9.
          variants: [
            {
              props: { variant: 'contained', color: 'primary' },
              style: {
                backgroundColor: P.blue,
                boxShadow: shadows.buttonContained,
                '&:hover': { backgroundColor: P.blueDark, boxShadow: shadows.buttonContainedHover },
              },
            },
            {
              props: { variant: 'contained', color: 'secondary' },
              style: {
                backgroundColor: secondary.main,
                boxShadow: shadows.buttonSecondary,
                '&:hover': { backgroundColor: secondary.dark, boxShadow: shadows.buttonSecondaryHover },
              },
            },
            {
              props: { variant: 'outlined' },
              style: {
                borderWidth: px(borders.emphasis),
                '&:hover': { borderWidth: px(borders.emphasis) },
              },
            },
            {
              props: { size: 'small' },
              style: { fontSize: rem(fontSize.dense), padding: '4px 12px' },
            },
          ],
        },
      },
    },

    MuiIconButton: {
      styleOverrides: {
        root: isHmi ? { minWidth: touch.minTarget, minHeight: touch.minTarget } : {},
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: flat,
        rounded: { borderRadius: radii.card },
        elevation1: { boxShadow: isDark ? shadowsDark.paper : shadows.paper },
      },
    },

    // Sin hover global: lo agrega cada pantalla si lo necesita (ctsTheme.ts).
    MuiCard: {
      styleOverrides: { root: { ...flat, borderRadius: radii.card } },
    },

    MuiTextField: { defaultProps: { variant: 'outlined' } },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: radii.control,
          transition: `box-shadow ${motion.control}`,
          '&.Mui-focused': { boxShadow: shadows.focusRing },
          '& fieldset': {
            borderColor: isDark ? surfaceDark.inputBorder : surface.inputBorder,
            borderWidth: px(borders.emphasis),
          },
          '&:hover fieldset': { borderColor: C.inputBorderHover },
          ...touchTarget,
        },
      },
    },

    MuiDrawer: {
      styleOverrides: {
        paper: isDark ? { backgroundImage: 'none', backgroundColor: brandSurface.dark } : {},
      },
    },

    MuiTableCell: {
      styleOverrides: {
        head: {
          backgroundColor: C.tableHead,
          color: brandSurface.text,
          fontWeight: fontWeight.semibold,
          fontSize: rem(fontSize.overline),
          // El nombre de la columna se muestra tal como se escribió.
          textTransform: 'none',
          letterSpacing: letterSpacing.tableHeader,
          padding: '9px 12px',
          whiteSpace: 'nowrap',
          borderRight: hairline(C.tableHeadDivider),
        },
        body: {
          padding: 0,
          fontSize: rem(fontSize.dense),
          height: isHmi ? touch.tableRow : 38,
          borderRight: hairline(C.tableCellBorder),
          borderBottom: hairline(C.tableCellBorder),
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        // Sólido para que las celdas sticky no transparenten al hacer hover.
        root: { '&:hover td': { backgroundColor: C.tableRowHover } },
      },
    },
    MuiTableContainer: {
      styleOverrides: { root: { borderRadius: radii.base, border: hairline(divider) } },
    },

    MuiDialog: {
      styleOverrides: {
        paper: {
          ...flat,
          borderRadius: radii.dialog,
          boxShadow: isDark ? shadowsDark.dialog : shadows.dialog,
        },
      },
    },
    MuiDialogTitle: {
      styleOverrides: {
        root: { fontWeight: fontWeight.bold, fontSize: rem(fontSize.dialogTitle), paddingBottom: 8 },
      },
    },

    MuiTooltip: {
      // `strategy: 'fixed'` evita que un globo pegado al borde derecho ensanche
      // el documento y haga vibrar el layout (ctsTheme.ts `MuiTooltip`).
      defaultProps: {
        arrow: true,
        slotProps: { popper: { popperOptions: { strategy: 'fixed' } } },
      },
      styleOverrides: {
        tooltip: {
          backgroundColor: C.tooltip,
          fontSize: rem(fontSize.caption),
          fontWeight: fontWeight.semibold,
          borderRadius: radii.chip,
          padding: '5px 10px',
        },
        arrow: { color: C.tooltip },
      },
    },

    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: fontWeight.semibold,
          fontSize: rem(fontSize.caption),
          height: 24,
          borderRadius: radii.chip,
        },
      },
    },

    MuiAlert: {
      styleOverrides: { root: { borderRadius: radii.control, fontWeight: fontWeight.semibold } },
    },

    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: radii.control,
          margin: '1px 8px',
          padding: '7px 12px',
          transition: `all ${motion.nav}`,
          ...touchTarget,
        },
      },
    },

    MuiLinearProgress: {
      styleOverrides: {
        root: { borderRadius: 4, height: 3 },
        bar: { backgroundColor: P.blue },
      },
    },

    MuiDivider: {
      styleOverrides: { root: { borderColor: divider } },
    },

    MuiMenu: {
      styleOverrides: {
        paper: {
          borderRadius: radii.base,
          boxShadow: isDark ? shadowsDark.menu : shadows.menu,
          border: hairline(isDark ? chromeDark.tableCellBorder : surface.border),
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          borderRadius: radii.chip,
          margin: '2px 6px',
          padding: '7px 10px',
          fontSize: rem(fontSize.menuItem),
          transition: `background ${motion.nav}`,
          ...touchTarget,
        },
      },
    },
  }
}
