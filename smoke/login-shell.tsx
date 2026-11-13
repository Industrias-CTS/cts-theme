/**
 * Prueba de humo de tipos para `LoginShell` — NO se publica (vive fuera de `src`).
 *
 * Verifica, contra MUI 6 · 7 · 9, que el cascarón compila con sus slots, con
 * el modo controlado y con el canal `useLoginShell`. Ver `smoke/sx-usage.tsx`
 * y `docs/Login-Shell.md` §4.
 */
import type { JSX } from 'react'
import { Button, ThemeProvider, Typography } from '@mui/material'
import { createCtsTheme } from '../src/index'
import { LoginShell, useLoginShell } from '../src/views'

const dark = createCtsTheme('dark')

/** Slot del formulario: cambia el estado sin recibir props. */
const SubmitProbe = (): JSX.Element => {
  const { status, setStatus } = useLoginShell()
  return (
    <Button variant="contained" onClick={() => setStatus('submitting')}>
      {status}
    </Button>
  )
}

export const LoginShellProbe = (): JSX.Element => (
  <ThemeProvider theme={dark}>
    <LoginShell
      logo={<Typography>LOGO</Typography>}
      brandName="W-Flow"
      tagline="Gestión de flujos de trabajo"
      legend="Somos más, somos CTS."
      title="Bienvenido"
      subtitle="Ingresa tus credenciales para continuar"
      footer="© Industrias CTS · W-Flow"
      status="error"
      onStatusChange={() => {}}
    >
      <SubmitProbe />
    </LoginShell>
  </ThemeProvider>
)
