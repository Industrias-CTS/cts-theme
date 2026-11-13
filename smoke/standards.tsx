/**
 * Prueba de humo de tipos de los estándares globales — NO se publica.
 *
 * Comprueba contra MUI 6 · 7 · 9 el perfil `hmi`, los roles de estado, las
 * capas, el formato `es-CO`, las variables CSS y los compuestos comunes.
 */
import { Box, Button, Dialog, DialogContent, ThemeProvider } from '@mui/material'
import {
  createCtsTheme,
  cssVariables,
  formatCurrency,
  formatDate,
  status,
  statusDark,
  themeOptions,
} from '../src/index'
import type { StatusName } from '../src/index'
import { DialogHeader, NotificationHost, QueryState, useNotify } from '../src/views'

const hmi = createCtsTheme('dark', { profile: 'hmi' })
const app = createCtsTheme()
export const options = themeOptions('light', { profile: 'app' })

/** Indicador de estado de equipo leyendo el rol, nunca un hex. */
export const StatusDot = ({ state, dark }: { state: StatusName; dark?: boolean }) => (
  <Box
    sx={(t) => ({
      width: t.cts.touch.minTarget / 4,
      height: t.cts.touch.minTarget / 4,
      borderRadius: `${t.cts.radii.pill}px`,
      bgcolor: (dark ? statusDark : status)[state],
      zIndex: t.cts.zIndex.sticky,
    })}
  />
)

const SaveButton = () => {
  const { notify } = useNotify()
  return (
    <Button
      variant="contained"
      onClick={() =>
        notify(`Guardado el ${formatDate(new Date())} · ${formatCurrency(1500000)}`, {
          action: { label: 'Deshacer', onClick: () => undefined },
        })
      }
    >
      Guardar
    </Button>
  )
}

export const Screen = ({ open, onClose }: { open: boolean; onClose: () => void }) => (
  <ThemeProvider theme={hmi}>
    <NotificationHost>
      <QueryState loading={false} isEmpty emptyTitle="Sin equipos" emptyAction={<SaveButton />}>
        <StatusDot state="fault" dark />
      </QueryState>
      <Dialog open={open} onClose={onClose} aria-labelledby="dlg-titulo">
        <DialogHeader titleId="dlg-titulo" title="Equipo" subtitle="Detalle" onClose={onClose} />
        <DialogContent />
      </Dialog>
    </NotificationHost>
  </ThemeProvider>
)

export const vars: Record<string, string> = cssVariables('dark')
export const themes = [hmi, app]
