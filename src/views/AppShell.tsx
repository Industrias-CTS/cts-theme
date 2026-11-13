/**
 * `AppShell` — cascarón de aplicación con rail de navegación.
 *
 * Porta el marco de `AppLayout.tsx` de cts-manager (rail a 0 con franja de
 * reapertura, líneas 25-50) y los modos responsivos de E-Panel
 * (`Sidebar.tsx` `useSidebarLayout`, `Sidebar.styles.ts` `drawerSx`). Los
 * huecos (rail, header, flotantes, vistas) son slots: cada aplicación pone su
 * contenido. Ver `docs/App-Shell.md`.
 *
 * Colores y medidas siempre en `sx`, leídos de `theme.cts` y de los roles de
 * `theme.palette`. Colores del rail en `sx`, nunca con el prop `color` de
 * `Typography`: MUI 9 lo tipa como `textSecondary` y descarta `'text.secondary'`.
 */
import type { JSX, ReactNode } from 'react'
import { useCallback, useMemo, useState } from 'react'
import { Backdrop, Box, Drawer, IconButton, SvgIcon, useMediaQuery, useTheme } from '@mui/material'
import type { Theme } from '@mui/material'
import { scrim } from '../colors'
import '../mui/augmentation'
import { AppShellContext } from './AppShellContext'
import type { AppShellContextValue, RailCollapse, ShellLayout } from './AppShellContext'

export interface AppShellProps {
  /** Contenido del rail (zonas 2–5). */
  rail: ReactNode
  /** Barra superior opcional (S1). */
  header?: ReactNode
  /** Acciones flotantes (zona 6). */
  floating?: ReactNode
  /** Vistas (zona 9). */
  children: ReactNode
  /** Qué queda del rail cerrado. Por defecto `'icons'`. */
  collapsedRail?: RailCollapse
  /** Modo del rail. `'auto'` resuelve por viewport. Por defecto `'auto'`. */
  layout?: 'auto' | ShellLayout
  /** `'padded'` aplica el gutter de página; `'bleed'` no deja margen. Por defecto `'padded'`. */
  content?: 'padded' | 'bleed'
  /** Estado controlado del rail. */
  railOpen?: boolean
  /** Estado inicial no controlado. Por defecto, abierto solo en `push`. */
  defaultRailOpen?: boolean
  onRailOpenChange?: (open: boolean) => void
  /** `aria-label` de la `<nav>` del rail. Por defecto `'Navegación principal'`. */
  railLabel?: string
  /** `aria-label` del botón de reapertura. Por defecto `'Mostrar menú'`. */
  reopenLabel?: string
}

/** Un slot cuenta como presente salvo que sea vacío, nulo o booleano. */
const present = (node: ReactNode): boolean =>
  node !== undefined && node !== null && node !== false && node !== ''

/**
 * Modo automático: `< md` → `temporary`; vertical → `overlay`; si no → `push`.
 * E-Panel `Sidebar.tsx` `useSidebarLayout` (líneas 19-31).
 */
const autoLayout = (isNarrow: boolean, isPortrait: boolean): ShellLayout => {
  if (isNarrow) return 'temporary'
  if (isPortrait) return 'overlay'
  return 'push'
}

/**
 * Superficie del rail: losa de `primary.main` en claro y `background.paper` en
 * oscuro. `open` decide la sombra. E-Panel `Sidebar.styles.ts` `paperBaseSx`.
 * `as const` para que las claves sean literales al pasarlas a `sx`.
 */
const railSurfaceSx = (t: Theme, open: boolean) =>
  ({
    bgcolor: t.palette.mode === 'dark' ? 'background.paper' : 'primary.main',
    color: 'primary.contrastText',
    border: 'none',
    boxShadow: open ? t.cts.shadows.sidebar : 'none',
    display: 'flex',
    flexDirection: 'column',
    overflowX: 'hidden',
    boxSizing: 'border-box',
  }) as const

/** Chevron derecho de `@mui/icons-material/ChevronRight`, dibujado a mano (no hay dependencia de iconos). */
const ChevronPath = (): JSX.Element => (
  <SvgIcon fontSize="small">
    <path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
  </SvgIcon>
)

export const AppShell = ({
  rail,
  header,
  floating,
  children,
  collapsedRail = 'icons',
  layout = 'auto',
  content = 'padded',
  railOpen: railOpenProp,
  defaultRailOpen,
  onRailOpenChange,
  railLabel = 'Navegación principal',
  reopenLabel = 'Mostrar menú',
}: AppShellProps): JSX.Element => {
  const theme = useTheme()
  // Ambas consultas se llaman siempre, aunque `layout` no sea `auto`: el orden de hooks no cambia.
  const isNarrow = useMediaQuery(theme.breakpoints.down('md'), { noSsr: true })
  const isPortrait = useMediaQuery('(orientation: portrait)', { noSsr: true })
  const resolvedLayout: ShellLayout = layout === 'auto' ? autoLayout(isNarrow, isPortrait) : layout

  // Controlado / no controlado, igual que `LoginShell`. El valor inicial se
  // fija una sola vez: en `push` no tapa nada, así que arranca abierto.
  const [internalOpen, setInternalOpen] = useState<boolean>(
    () => defaultRailOpen ?? (resolvedLayout === 'push'),
  )
  const isControlled = railOpenProp !== undefined
  const railOpen = railOpenProp ?? internalOpen

  const setRailOpen = useCallback(
    (open: boolean) => {
      if (!isControlled) setInternalOpen(open)
      onRailOpenChange?.(open)
    },
    [isControlled, onRailOpenChange],
  )

  const toggleRail = useCallback(() => setRailOpen(!railOpen), [railOpen, setRailOpen])

  // Tiempo de cierre del modo actual. `temporary` usa la duración de MUI del
  // Drawer; el resto, la transición del propio rail (0.25s → 250).
  const closeMs =
    resolvedLayout === 'temporary'
      ? theme.transitions.duration.leavingScreen
      : parseFloat(theme.cts.motion.collapse) * 1000

  const contextValue = useMemo<AppShellContextValue>(
    () => ({ railOpen, setRailOpen, toggleRail, layout: resolvedLayout, collapsedRail, closeMs }),
    [railOpen, setRailOpen, toggleRail, resolvedLayout, collapsedRail, closeMs],
  )

  const collapsedWidth =
    collapsedRail === 'icons' ? theme.cts.layout.railIconWidth : theme.cts.layout.railCollapsedWidth
  const transition = `width ${theme.cts.motion.collapse} ${theme.cts.motion.easing}`
  const panelTransition = `${transition}, box-shadow ${theme.cts.motion.collapse} ${theme.cts.motion.easing}`
  const showReopen = collapsedRail === 'hidden' && !railOpen && resolvedLayout !== 'temporary'

  // Rail según el modo. `temporary` es un Drawer modal y no reserva nada en la fila.
  const railNode =
    resolvedLayout === 'temporary' ? (
      <Drawer
        variant="temporary"
        open={railOpen}
        onClose={() => setRailOpen(false)}
        sx={(t) => ({
          '& .MuiDrawer-paper': { width: t.cts.layout.railWidth, ...railSurfaceSx(t, true) },
        })}
      >
        <Box
          component="nav"
          aria-label={railLabel}
          sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}
        >
          {rail}
        </Box>
      </Drawer>
    ) : resolvedLayout === 'overlay' ? (
      // AppLayout-like: la franja colapsada reserva su columna; el panel se superpone.
      <>
        <Box
          sx={(t) => ({
            flexShrink: 0,
            width: collapsedWidth,
            position: 'relative',
            zIndex: t.zIndex.drawer,
          })}
        >
          <Box
            component="nav"
            aria-label={railLabel}
            sx={(t) => ({
              position: 'absolute',
              top: 0,
              bottom: 0,
              left: 0,
              width: railOpen ? t.cts.layout.railWidth : collapsedWidth,
              transition: panelTransition,
              ...railSurfaceSx(t, railOpen),
            })}
          >
            {rail}
          </Box>
        </Box>
        <Backdrop
          open={railOpen}
          onClick={() => setRailOpen(false)}
          sx={(t) => ({ zIndex: t.zIndex.drawer - 1, bgcolor: scrim.rail })}
        />
      </>
    ) : (
      // push: columna propia; al ensancharse empuja el contenido.
      <Box
        component="nav"
        aria-label={railLabel}
        sx={(t) => ({
          flexShrink: 0,
          height: '100%',
          width: railOpen ? t.cts.layout.railWidth : collapsedWidth,
          transition,
          ...railSurfaceSx(t, railOpen),
        })}
      >
        {rail}
      </Box>
    )

  // Franja de reapertura (AppLayout.tsx:27-40) y su gemela a la derecha (AppLayout.tsx:50).
  const reopenButton = (
    <Box sx={(t) => ({ width: t.cts.layout.reopenStripWidth, flexShrink: 0, position: 'relative' })}>
      <IconButton
        size="small"
        aria-label={reopenLabel}
        onClick={() => setRailOpen(true)}
        sx={(t) => ({
          position: 'sticky',
          top: t.cts.layout.reopenTop,
          ml: 1.5,
          mt: 1.5,
          bgcolor: t.palette.mode === 'dark' ? 'background.paper' : 'primary.main',
          color: 'primary.contrastText',
          boxShadow: t.cts.shadows.elevation1,
          //? S5 (propuesta, D13): `primary.dark` / `primary.main` en lugar de los literales sueltos de AppLayout.tsx:39.
          '&:hover': {
            bgcolor: t.palette.mode === 'dark' ? 'primary.main' : 'primary.dark',
          },
        })}
      >
        <ChevronPath />
      </IconButton>
    </Box>
  )

  return (
    <AppShellContext.Provider value={contextValue}>
      <Box
        data-layout={resolvedLayout}
        data-rail={railOpen ? 'open' : 'closed'}
        sx={{
          display: 'flex',
          height: '100dvh',
          overflow: 'hidden',
          bgcolor: 'background.default',
        }}
      >
        {railNode}
        {showReopen && reopenButton}

        {/* Columna de contenido: header opcional arriba, `main` desplazable debajo. */}
        <Box
          sx={{
            flex: 1,
            minWidth: 0,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          }}
        >
          {present(header) && <Box sx={{ flexShrink: 0 }}>{header}</Box>}
          <Box
            component="main"
            sx={(t) => ({
              flex: 1,
              minHeight: 0,
              overflow: 'auto',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              p: content === 'padded' ? `${t.cts.spacing.gutter}px` : 0,
            })}
          >
            {children}
          </Box>
        </Box>

        {showReopen && <Box sx={(t) => ({ width: t.cts.layout.reopenStripWidth, flexShrink: 0 })} />}

        {present(floating) && (
          <Box
            sx={(t) => ({
              position: 'fixed',
              top: t.cts.layout.floatingTop,
              right: t.cts.layout.floatingRight,
              zIndex: t.zIndex.speedDial,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            })}
          >
            {floating}
          </Box>
        )}
      </Box>
    </AppShellContext.Provider>
  )
}
