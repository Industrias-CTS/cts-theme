import type { Meta, StoryObj } from '@storybook/react-vite'
import { useEffect, useRef } from 'react'
import { Button, Stack } from '@mui/material'
import { useNotify } from '../../src/views'
import { Code, Page, Section } from '../ui'

const meta = { title: 'Componentes CTS/Notificaciones' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const Botones = () => {
  const { notify, dismiss } = useNotify()
  const timer = useRef<number | undefined>(undefined)
  useEffect(() => () => window.clearInterval(timer.current), [])

  const largo = () => {
    window.clearInterval(timer.current)
    let p = 0
    notify('Eliminando 1.240 elementos…', { severity: 'info', persistent: true, progress: p })
    timer.current = window.setInterval(() => {
      p += 10
      if (p > 100) {
        window.clearInterval(timer.current)
        notify('Se eliminaron 1.240 elementos')
        return
      }
      notify('Eliminando 1.240 elementos…', { severity: 'info', persistent: true, progress: p })
    }, 400)
  }

  return (
    <Stack direction="row" spacing={1.5} useFlexGap sx={{ flexWrap: 'wrap' }}>
      <Button variant="contained" onClick={() => notify('Proyecto guardado')}>Éxito</Button>
      <Button variant="outlined" color="error" onClick={() => notify('No se pudo guardar el proyecto', { severity: 'error' })}>Error</Button>
      <Button variant="outlined" color="warning" onClick={() => notify('Hay cambios sin publicar', { severity: 'warning' })}>Advertencia</Button>
      <Button
        variant="outlined"
        onClick={() => notify('Tablero movido a «Archivados»', { action: { label: 'Deshacer', onClick: () => notify('Movimiento deshecho', { severity: 'info' }) } })}
      >
        Con acción
      </Button>
      <Button variant="outlined" onClick={largo}>Persistente con avance</Button>
      <Button onClick={dismiss}>Cerrar aviso</Button>
    </Stack>
  )
}

export const Avisos: Story = {
  render: () => (
    <Page
      title="Notificaciones"
      intro="Un solo aviso a la vez, abajo a la derecha. 4 s; 7 s si tiene acción; los persistentes no se cierran solos y pueden mostrar avance."
    >
      <Section title="Pruébalo">
        <Botones />
      </Section>
      <Section title="Uso">
        <Stack spacing={0.5}>
          <Code>{'<NotificationHost> una vez en la raíz de la app'}</Code>
          <Code>{"const { notify } = useNotify()"}</Code>
          <Code>{"notify('Proyecto guardado')"}</Code>
          <Code>{"notify('No se pudo guardar', { severity: 'error' })"}</Code>
          <Code>{"notify('Tablero movido', { action: { label: 'Deshacer', onClick } })"}</Code>
        </Stack>
      </Section>
    </Page>
  ),
}
