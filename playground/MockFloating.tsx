import type { JSX } from 'react'
import { Box, IconButton } from '@mui/material'
import type { Theme } from '@mui/material'
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined'
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined'
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined'

export interface MockFloatingProps {
  mode: 'light' | 'dark'
  onToggleMode: () => void
}

/** Acciones flotantes de ejemplo (slot `floating` de `AppShell`). */
export function MockFloating({ mode, onToggleMode }: MockFloatingProps): JSX.Element {
  const isDark = mode === 'dark'

  const circleSx = (t: Theme) => ({
    width: t.cts.density.floatingAction,
    height: t.cts.density.floatingAction,
    bgcolor: 'background.paper',
    color: 'text.primary',
    border: `${t.cts.borders.hairline}px solid`,
    borderColor: 'divider',
    boxShadow: t.cts.shadows.floatingAction,
    borderRadius: '50%',
  })

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <IconButton
        aria-label={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
        onClick={onToggleMode}
        sx={circleSx}
      >
        {isDark ? <LightModeOutlinedIcon /> : <DarkModeOutlinedIcon />}
      </IconButton>
      <IconButton aria-label="Notificaciones" sx={circleSx}>
        <NotificationsNoneOutlinedIcon />
      </IconButton>
    </Box>
  )
}
