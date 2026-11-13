import type { JSX } from 'react'
import { Box, IconButton } from '@mui/material'
import MenuOutlinedIcon from '@mui/icons-material/MenuOutlined'
import { useAppShell } from '../src/views'

/**
 * Cabecera de ejemplo (slot `header` de `AppShell`). En `temporary` el rail es
 * un Drawer que no ocupa sitio, así que el lanzador vive aquí.
 */
export function MockHeader(): JSX.Element {
  const { layout, setRailOpen } = useAppShell()

  return (
    <Box
      sx={(t) => ({
        height: t.cts.density.groupHeader,
        px: 3,
        display: 'flex',
        alignItems: 'center',
        gap: 1,
      })}
    >
      {layout === 'temporary' && (
        <IconButton
          size="small"
          aria-label="Abrir menú"
          onClick={() => setRailOpen(true)}
        >
          <MenuOutlinedIcon />
        </IconButton>
      )}

      <Box
        component="nav"
        aria-label="Migas de pan"
        sx={(t) => ({
          display: 'flex',
          alignItems: 'center',
          gap: 1,
          fontSize: t.cts.fontSize.dense,
          minWidth: 0,
          whiteSpace: 'nowrap',
        })}
      >
        <Box component="span" sx={{ color: 'text.secondary' }}>
          Mock-App
        </Box>
        <Box component="span" aria-hidden="true" sx={{ color: 'text.secondary' }}>
          /
        </Box>
        <Box component="span" aria-current="page" sx={{ color: 'text.primary' }}>
          Inicio
        </Box>
      </Box>
    </Box>
  )
}
