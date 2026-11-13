import { useState } from 'react'
import type { JSX } from 'react'
import { Avatar, Box, IconButton, Typography } from '@mui/material'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined'
import FolderOutlinedIcon from '@mui/icons-material/FolderOutlined'
import BarChartOutlinedIcon from '@mui/icons-material/BarChartOutlined'
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined'
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined'
import { useAppShell } from '../src/views'

type NavIcon = typeof HomeOutlinedIcon

interface NavEntry {
  id: string
  label: string
  Icon: NavIcon
}

const NAV_ITEMS: readonly NavEntry[] = [
  { id: 'inicio', label: 'Inicio', Icon: HomeOutlinedIcon },
  { id: 'proyectos', label: 'Proyectos', Icon: FolderOutlinedIcon },
  { id: 'reportes', label: 'Reportes', Icon: BarChartOutlinedIcon },
  { id: 'ajustes', label: 'Ajustes', Icon: SettingsOutlinedIcon },
]

export interface MockRailProps {
  onLogout: () => void
}

/**
 * Contenido de ejemplo del rail de `AppShell` (zonas 2–5: cabecera, ítems, pie).
 * Todo el color sale de `theme.cts.rail`: el rail es una losa azul o navy con
 * texto blanco, no usa la paleta de texto del tema.
 */
export function MockRail({ onLogout }: MockRailProps): JSX.Element {
  const { railOpen, setRailOpen, toggleRail, layout } = useAppShell()
  const [activeId, setActiveId] = useState<string>(NAV_ITEMS[0]?.id ?? '')

  const onCollapseClick = () => {
    // En `temporary` el rail es un Drawer modal: el botón lo cierra.
    if (layout === 'temporary') setRailOpen(false)
    else toggleRail()
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', minHeight: 0 }}>
      {/* Cabecera: logo + wordmark + botón de colapso. En columna cuando el rail
          está cerrado (64 px de ancho) para que quepan los tres elementos. */}
      <Box
        sx={(t) => ({
          display: 'flex',
          flexDirection: railOpen ? 'row' : 'column',
          alignItems: 'center',
          justifyContent: railOpen ? 'space-between' : 'center',
          gap: 1,
          px: 2,
          py: 2,
          borderBottom: `${t.cts.borders.hairline}px solid ${t.cts.rail.divider}`,
        })}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, minWidth: 0 }}>
          <Box
            aria-hidden="true"
            sx={(t) => ({
              width: t.cts.density.railLogo,
              height: t.cts.density.railLogo,
              borderRadius: `${t.cts.radii.control}px`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              bgcolor: t.cts.rail.itemActiveBg,
              color: t.cts.rail.itemActiveColor,
              fontWeight: t.cts.fontWeight.black,
              fontSize: t.cts.fontSize.wordmark,
            })}
          >
            M
          </Box>
          {railOpen && (
            <Typography
              component="span"
              sx={(t) => ({
                color: t.cts.rail.itemActiveColor,
                fontSize: t.cts.fontSize.wordmark,
                fontWeight: t.cts.fontWeight.black,
                letterSpacing: t.cts.letterSpacing.wordmark,
                lineHeight: 1,
                whiteSpace: 'nowrap',
              })}
            >
              Mock-App
            </Typography>
          )}
        </Box>

        <IconButton
          size="small"
          aria-label={railOpen ? 'Contraer menú' : 'Expandir menú'}
          onClick={onCollapseClick}
          sx={(t) => ({
            color: t.cts.rail.itemIdleColor,
            '&:hover': { bgcolor: t.cts.rail.itemHoverBg, color: t.cts.rail.itemActiveColor },
          })}
        >
          {railOpen ? <ChevronLeftIcon /> : <ChevronRightIcon />}
        </IconButton>
      </Box>

      {/* Ítems de navegación. Con el rail cerrado solo quedan los iconos, centrados. */}
      <Box
        component="nav"
        aria-label="Principal"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 0.5,
          p: railOpen ? 1.5 : 1,
          flex: 1,
          minHeight: 0,
          overflowY: 'auto',
        }}
      >
        {NAV_ITEMS.map(({ id, label, Icon }) => {
          const active = id === activeId
          return (
            <Box
              key={id}
              component="button"
              type="button"
              aria-label={label}
              aria-current={active ? 'page' : undefined}
              onClick={() => setActiveId(id)}
              sx={(t) => ({
                m: 0,
                p: 0,
                border: 0,
                boxSizing: 'border-box',
                display: 'flex',
                textAlign: 'left',
                alignItems: 'center',
                justifyContent: railOpen ? 'flex-start' : 'center',
                gap: 1.5,
                width: '100%',
                height: t.cts.density.navItem,
                px: railOpen ? 1.5 : 0,
                cursor: 'pointer',
                borderRadius: `${t.cts.radii.control}px`,
                borderLeft: `${t.cts.borders.indicator}px solid ${
                  active ? t.cts.rail.itemActiveBorder : 'transparent'
                }`,
                fontFamily: 'inherit',
                fontSize: t.cts.fontSize.navLabel,
                color: active ? t.cts.rail.itemActiveColor : t.cts.rail.itemIdleColor,
                background: active ? t.cts.rail.itemActiveBg : 'transparent',
                transition: `background ${t.cts.motion.nav} ${t.cts.motion.easing}, color ${t.cts.motion.nav} ${t.cts.motion.easing}`,
                '&:hover': {
                  background: active ? t.cts.rail.itemActiveBg : t.cts.rail.itemHoverBg,
                  color: t.cts.rail.itemActiveColor,
                },
                '&:focus-visible': {
                  outline: `${t.cts.borders.emphasis}px solid ${t.cts.rail.itemActiveBorder}`,
                  outlineOffset: -2,
                },
              })}
            >
              <Icon sx={{ fontSize: 20, flexShrink: 0 }} />
              {railOpen && (
                <Box component="span" sx={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {label}
                </Box>
              )}
            </Box>
          )
        })}
      </Box>

      {/* Pie: usuario y cierre de sesión. */}
      <Box
        sx={(t) => ({
          display: 'flex',
          flexDirection: railOpen ? 'row' : 'column',
          alignItems: 'center',
          justifyContent: railOpen ? 'space-between' : 'center',
          gap: 1,
          p: 2,
          bgcolor: t.cts.rail.footerBg,
          borderTop: `${t.cts.borders.hairline}px solid ${t.cts.rail.divider}`,
        })}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, minWidth: 0 }}>
          <Avatar
            sx={(t) => ({
              width: t.cts.density.avatar,
              height: t.cts.density.avatar,
              fontSize: t.cts.fontSize.caption,
              fontWeight: t.cts.fontWeight.semibold,
              bgcolor: t.cts.rail.avatarBg,
              color: t.cts.rail.itemActiveColor,
              border: `${t.cts.borders.accent}px solid ${t.cts.rail.avatarBorder}`,
            })}
          >
            MU
          </Avatar>
          {railOpen && (
            <Box sx={{ minWidth: 0 }}>
              <Typography
                component="div"
                sx={(t) => ({
                  color: t.cts.rail.itemActiveColor,
                  fontSize: t.cts.fontSize.userName,
                  fontWeight: t.cts.fontWeight.semibold,
                  whiteSpace: 'nowrap',
                })}
              >
                Mock User
              </Typography>
              <Typography
                component="div"
                sx={(t) => ({
                  color: t.cts.rail.descriptor,
                  fontSize: t.cts.fontSize.userRole,
                  whiteSpace: 'nowrap',
                })}
              >
                Diseño
              </Typography>
            </Box>
          )}
        </Box>

        <IconButton
          size="small"
          aria-label="Cerrar sesión"
          onClick={onLogout}
          sx={(t) => ({
            color: t.cts.rail.itemIdleColor,
            '&:hover': {
              bgcolor: t.cts.rail.logoutHoverBg,
              color: t.cts.rail.logoutHoverColor,
            },
          })}
        >
          <LogoutOutlinedIcon fontSize="small" />
        </IconButton>
      </Box>
    </Box>
  )
}
