import { useEffect, useMemo, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { CssBaseline, IconButton, ThemeProvider } from '@mui/material'
import DarkModeOutlined from '@mui/icons-material/DarkModeOutlined'
import LightModeOutlined from '@mui/icons-material/LightModeOutlined'
import { createCtsTheme } from '../src/index'
import { AppShell, LoginShell } from '../src/views'
import type { LoginStatus, RailCollapse } from '../src/views'
import { MockContent } from './MockContent'
import { MockFloating } from './MockFloating'
import { MockHeader } from './MockHeader'
import { MockLogo } from './MockLogo'
import { MockLoginForm } from './MockLoginForm'
import { MockRail } from './MockRail'

type Mode = 'light' | 'dark'
type View = 'login' | 'app'

/** Pausa tras el éxito para que se vea la alerta de sesión iniciada. */
const MOCK_SUCCESS_DELAY_MS = 600
/** Hash que conserva la vista de app al recargar la página. */
const APP_HASH = 'app'

const initialMode = (): Mode =>
  window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'

const initialView = (): View => (window.location.hash === `#${APP_HASH}` ? 'app' : 'login')

function Playground() {
  const [mode, setMode] = useState<Mode>(initialMode)
  const [view, setView] = useState<View>(initialView)
  const [collapse, setCollapse] = useState<RailCollapse>('icons')
  const timerRef = useRef<number | undefined>(undefined)
  const theme = useMemo(() => createCtsTheme(mode), [mode])
  const isDark = mode === 'dark'

  useEffect(() => () => window.clearTimeout(timerRef.current), [])

  const enter = () => {
    setView('app')
    window.location.hash = APP_HASH
  }

  const logout = () => {
    setView('login')
    window.history.replaceState(null, '', window.location.pathname)
  }

  const onLoginStatus = (status: LoginStatus) => {
    if (status !== 'success') return
    window.clearTimeout(timerRef.current)
    timerRef.current = window.setTimeout(enter, MOCK_SUCCESS_DELAY_MS)
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {view === 'login' ? (
        <>
          <IconButton
            aria-label={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
            onClick={() => setMode(isDark ? 'light' : 'dark')}
            sx={(t) => ({
              position: 'fixed',
              top: t.cts.layout.floatingTop,
              right: t.cts.layout.floatingRight,
            })}
          >
            {isDark ? <LightModeOutlined /> : <DarkModeOutlined />}
          </IconButton>
          <LoginShell
            logo={<MockLogo />}
            brandName="Mock-App"
            tagline="Gestión de ejemplo"
            legend="Somos más, somos CTS."
            title="Bienvenido"
            subtitle="Ingresa tus credenciales para continuar"
            footer={`© ${new Date().getFullYear()} Industrias CTS · Mock-App`}
            onStatusChange={onLoginStatus}
          >
            <MockLoginForm />
          </LoginShell>
        </>
      ) : (
        <AppShell
          rail={<MockRail onLogout={logout} />}
          header={<MockHeader />}
          floating={
            <MockFloating
              mode={mode}
              onToggleMode={() => setMode(isDark ? 'light' : 'dark')}
            />
          }
          collapsedRail={collapse}
          layout="auto"
        >
          <MockContent collapse={collapse} onCollapseChange={setCollapse} />
        </AppShell>
      )}
    </ThemeProvider>
  )
}

createRoot(document.getElementById('root')!).render(<Playground />)
