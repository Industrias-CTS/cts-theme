import type { Meta, StoryObj } from '@storybook/react-vite'
import type { ReactNode } from 'react'
import { Box, Chip, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, useTheme } from '@mui/material'
import { formatDate, formatNumber, status, statusDark } from '../../src/index'
import type { StatusName } from '../../src/index'
import { Page } from '../ui'

const meta = { title: 'Componentes MUI/Tablas' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const FILAS: { id: string; equipo: string; estado: StatusName; etiqueta: string; carga: number; fecha: string }[] = [
  { id: 'TAB-001', equipo: 'Tablero general', estado: 'ok', etiqueta: 'En marcha', carga: 1234.5, fecha: '2026-11-02' },
  { id: 'TAB-002', equipo: 'Tablero de iluminación', estado: 'warning', etiqueta: 'Mantenimiento', carga: 310, fecha: '2026-10-28' },
  { id: 'TAB-003', equipo: 'CCM bombas', estado: 'fault', etiqueta: 'Falla', carga: 0, fecha: '2026-11-12' },
  { id: 'TAB-004', equipo: 'Tablero de respaldo', estado: 'offline', etiqueta: 'Fuera de línea', carga: 0, fecha: '2026-09-15' },
]

const Celda = ({ children, align }: { children: ReactNode; align?: 'right' }) => (
  <TableCell align={align}>
    <Box sx={{ px: 1.5 }}>{children}</Box>
  </TableCell>
)

const Ejemplo = () => {
  const t = useTheme()
  const st = t.palette.mode === 'dark' ? statusDark : status
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Código</TableCell>
            <TableCell>Equipo</TableCell>
            <TableCell>Estado</TableCell>
            <TableCell align="right">Carga (kW)</TableCell>
            <TableCell>Última revisión</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {FILAS.map((f) => (
            <TableRow key={f.id}>
              <Celda>{f.id}</Celda>
              <Celda>{f.equipo}</Celda>
              <Celda>
                <Chip
                  size="small"
                  label={f.etiqueta}
                  variant="outlined"
                  sx={{ borderColor: st[f.estado], color: 'text.primary' }}
                  icon={<Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: st[f.estado], ml: '8px !important' }} />}
                />
              </Celda>
              <Celda align="right">{formatNumber(f.carga, { decimals: 1 })}</Celda>
              <Celda>{formatDate(f.fecha)}</Celda>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export const Tabla: Story = {
  render: () => (
    <Page
      title="Tablas"
      intro="Cabecera azul (gris azulado en oscuro) sin mayúsculas: el nombre de la columna se ve tal como se escribió. Filas de 38 px (48 en HMI), hover sólido para no transparentar columnas sticky."
    >
      <Ejemplo />
    </Page>
  ),
}
