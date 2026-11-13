import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'
import { Box, Button, Stack } from '@mui/material'
import { motion, notify, zIndex } from '../../src/index'
import { Code, Page, RefTable, Section } from '../ui'

const meta = { title: 'Fundamentos/Capas y movimiento' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const Animacion = () => {
  const [abierto, setAbierto] = useState(true)
  return (
    <Stack spacing={2}>
      <Box>
        <Button variant="outlined" onClick={() => setAbierto((a) => !a)}>
          {abierto ? 'Colapsar' : 'Expandir'}
        </Button>
      </Box>
      {(['micro', 'nav', 'control', 'collapse'] as const).map((k) => (
        <Stack key={k} direction="row" spacing={2} sx={{ alignItems: 'center' }}>
          <Box sx={{ width: 140 }}>
            <Code>{`motion.${k} · ${motion[k]}`}</Code>
          </Box>
          <Box
            sx={(t) => ({
              height: 16,
              width: abierto ? 320 : 40,
              bgcolor: 'primary.main',
              borderRadius: `${t.cts.radii.pill}px`,
              transition: `width ${motion[k]} ${t.cts.motion.easing}`,
            })}
          />
        </Stack>
      ))}
    </Stack>
  )
}

export const Capas: Story = {
  render: () => (
    <Page title="Capas y movimiento" intro="Toda capa global sale de theme.cts.zIndex o theme.zIndex. Los números sueltos solo valen de 1 a 10, dentro de un componente.">
      <Section title="Capas · zIndex">
        <RefTable
          head={['Token', 'Valor', 'Uso']}
          rows={[
            ['sticky', zIndex.sticky, 'encabezados y columnas sticky'],
            ['floating', zIndex.floating, 'acciones flotantes'],
            ['bar', zIndex.bar, 'barra superior o inferior'],
            ['rail', zIndex.rail, 'rail de navegación'],
            ['modal', zIndex.modal, 'diálogos y velos'],
            ['keyboard', zIndex.keyboard, 'teclado virtual (HMI)'],
            ['toast', zIndex.toast, 'avisos'],
            ['tooltip', zIndex.tooltip, 'tooltips'],
            ['tour', zIndex.tour, 'recorridos guiados'],
          ].map(([k, v, u]) => [<Code>{`zIndex.${k}`}</Code>, v, u])}
        />
      </Section>
      <Section title="Movimiento" note={`Una sola curva: ${motion.easing}. Pulsa el botón para comparar duraciones.`}>
        <Animacion />
      </Section>
      <Section title="Avisos · notify">
        <RefTable head={['Token', 'Valor']} rows={Object.entries(notify).map(([k, v]) => [<Code>{`notify.${k}`}</Code>, v])} />
      </Section>
    </Page>
  ),
}
