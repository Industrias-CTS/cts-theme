/**
 * Prueba de humo de tipos para `AppShell` — NO se publica (vive fuera de `src`).
 *
 * Verifica, contra MUI 6 · 7 · 9, que el cascarón compila con sus slots, con
 * el modo no controlado y con el canal `useAppShell`. Ver `docs/App-Shell.md` §5.
 */
import type { JSX } from 'react'
import { Button, ThemeProvider, Typography } from '@mui/material'
import { createCtsTheme } from '../src/index'
import { AppShell, useAppShell } from '../src/views'

const dark = createCtsTheme('dark')

/** Slot del rail: lee el estado y lo cambia sin recibir props. */
const RailProbe = (): JSX.Element => {
  const { railOpen, toggleRail, closeMs } = useAppShell()
  return (
    <Button onClick={toggleRail}>
      {railOpen ? `cerrar ${closeMs}` : `abrir ${closeMs}`}
    </Button>
  )
}

export const AppShellProbe = (): JSX.Element => (
  <ThemeProvider theme={dark}>
    <AppShell
      rail={<RailProbe />}
      header={<Typography>CABECERA</Typography>}
      floating={<Button variant="contained">ACCIÓN</Button>}
      collapsedRail="hidden"
      layout="push"
      content="bleed"
      onRailOpenChange={() => {}}
    >
      <Typography>Contenido</Typography>
    </AppShell>
  </ThemeProvider>
)
