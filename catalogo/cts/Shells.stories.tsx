import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'
import { useTheme } from '@mui/material'
import { AppShell, LoginShell } from '../../src/views'
import type { RailCollapse } from '../../src/views'
import { MockContent } from '../../playground/MockContent'
import { MockFloating } from '../../playground/MockFloating'
import { MockHeader } from '../../playground/MockHeader'
import { MockLoginForm } from '../../playground/MockLoginForm'
import { MockLogo } from '../../playground/MockLogo'
import { MockRail } from '../../playground/MockRail'

/**
 * Los dos cascarones de pantalla completa. El contenido (rail, cabecera,
 * formulario, logo) son mocks del playground; cada app pone los suyos.
 * Ver docs/App-Shell.md y docs/Login-Shell.md.
 */
const meta = {
  title: 'Componentes CTS/Shells',
  parameters: { layout: 'fullscreen' },
} satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const App = () => {
  const [collapse, setCollapse] = useState<RailCollapse>('icons')
  const mode = useTheme().palette.mode
  return (
    <AppShell
      rail={<MockRail onLogout={() => undefined} />}
      header={<MockHeader />}
      floating={<MockFloating mode={mode} onToggleMode={() => undefined} />}
      collapsedRail={collapse}
    >
      <MockContent collapse={collapse} onCollapseChange={setCollapse} />
    </AppShell>
  )
}

export const AppShell_: Story = { name: 'AppShell', render: () => <App /> }

export const LoginShell_: Story = {
  name: 'LoginShell',
  render: () => (
    <LoginShell
      logo={<MockLogo />}
      brandName="Mock-App"
      tagline="Gestión de ejemplo"
      legend="Somos más, somos CTS."
      title="Bienvenido"
      subtitle="Ingresa tus credenciales para continuar"
      footer="© Industrias CTS · Mock-App"
    >
      <MockLoginForm />
    </LoginShell>
  ),
}
