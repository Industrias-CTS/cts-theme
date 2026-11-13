import type { JSX } from 'react'
import { Box, Button, Paper, Typography } from '@mui/material'
import type { RailCollapse } from '../src/views'
import { useAppShell } from '../src/views'

export interface MockContentProps {
  collapse: RailCollapse
  onCollapseChange: (collapse: RailCollapse) => void
}

const STATS = [
  { label: 'Proyectos', value: 12 },
  { label: 'Tableros', value: 48 },
  { label: 'Pendientes', value: 7 },
] as const

const FILLER_ROWS = Array.from({ length: 30 }, (_, i) => `Fila de ejemplo ${i + 1}`)

/** Contenido de ejemplo de la vista Inicio, dentro de `AppShell`. */
export function MockContent({ collapse, onCollapseChange }: MockContentProps): JSX.Element {
  const { layout, railOpen } = useAppShell()

  return (
    <>
      <Typography
        variant="h4"
        component="h1"
        sx={(t) => ({ fontWeight: t.cts.fontWeight.bold, mb: 0.5 })}
      >
        Inicio
      </Typography>
      <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
        Vista de ejemplo dentro de AppShell.
      </Typography>

      <Box
        sx={(t) => ({
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, minmax(0, 1fr))' },
          gap: `${t.cts.spacing.cardGapMin}px`,
          mb: 3,
        })}
      >
        {STATS.map(({ label, value }) => (
          <Paper
            key={label}
            variant="outlined"
            sx={(t) => ({ p: 2.5, borderRadius: `${t.cts.radii.card}px` })}
          >
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {label}
            </Typography>
            <Typography
              variant="h4"
              component="p"
              sx={(t) => ({ fontWeight: t.cts.fontWeight.bold, m: 0 })}
            >
              {value}
            </Typography>
          </Paper>
        ))}
      </Box>

      <Paper
        variant="outlined"
        sx={(t) => ({ p: 2.5, mb: 3, borderRadius: `${t.cts.radii.card}px` })}
      >
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
          Modo del rail al cerrar
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1.5, mb: 2 }}>
          <Button
            variant={collapse === 'icons' ? 'contained' : 'outlined'}
            aria-pressed={collapse === 'icons'}
            onClick={() => onCollapseChange('icons')}
          >
            Rail con iconos
          </Button>
          <Button
            variant={collapse === 'hidden' ? 'contained' : 'outlined'}
            aria-pressed={collapse === 'hidden'}
            onClick={() => onCollapseChange('hidden')}
          >
            Rail oculto
          </Button>
        </Box>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          Layout: {layout} · Rail: {railOpen ? 'abierto' : 'cerrado'}
        </Typography>
      </Paper>

      <Paper variant="outlined" sx={(t) => ({ borderRadius: `${t.cts.radii.card}px`, overflow: 'hidden' })}>
        {FILLER_ROWS.map((row) => (
          <Box
            key={row}
            sx={(t) => ({
              height: t.cts.density.tableRow,
              px: 2,
              display: 'flex',
              alignItems: 'center',
              fontSize: t.cts.fontSize.dense,
              borderBottom: `${t.cts.borders.hairline}px solid`,
              borderColor: 'divider',
              '&:last-of-type': { borderBottom: 0 },
            })}
          >
            {row}
          </Box>
        ))}
      </Paper>
    </>
  )
}
