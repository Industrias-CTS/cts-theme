import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'
import { Button, Dialog, DialogActions, DialogContent, Paper, Tab, Tabs, TextField } from '@mui/material'
import { DialogHeader } from '../../src/views'

/**
 * Cabecera estándar de diálogo: título, subtítulo, acciones y cierre. Va
 * dentro de `<Dialog>` en lugar de `<DialogTitle>`; pásale el mismo `titleId`
 * que al `aria-labelledby` del diálogo.
 */
const meta = {
  title: 'Componentes CTS/DialogHeader',
  component: DialogHeader,
  tags: ['autodocs'],
  args: { title: 'Nuevo proyecto', subtitle: 'Datos básicos del cliente y la obra', onClose: () => undefined, align: 'start' },
  argTypes: { onClose: { control: false }, left: { control: false }, actions: { control: false } },
  decorators: [
    (Story) => (
      <Paper elevation={1} sx={{ maxWidth: 560 }}>
        <Story />
      </Paper>
    ),
  ],
} satisfies Meta<typeof DialogHeader>
export default meta
type Story = StoryObj<typeof meta>

export const Basico: Story = { name: 'Básico' }

export const ConPestanas: Story = {
  name: 'Con pestañas',
  args: {
    align: 'center',
    subtitle: undefined,
    actions: (
      <Tabs value={0} aria-label="Secciones">
        <Tab label="General" />
        <Tab label="Eléctrico" />
      </Tabs>
    ),
  },
}

const EnDialogo = () => {
  const [open, setOpen] = useState(false)
  return (
    <>
      <Button variant="contained" onClick={() => setOpen(true)}>
        Abrir diálogo
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm" aria-labelledby="nuevo-proyecto">
        <DialogHeader titleId="nuevo-proyecto" title="Nuevo proyecto" subtitle="Datos básicos" onClose={() => setOpen(false)} />
        <DialogContent>
          <TextField label="Nombre" fullWidth sx={{ mt: 1 }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={() => setOpen(false)}>Crear</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}

export const DentroDeDialog: Story = {
  name: 'Dentro de un Dialog',
  decorators: [(Story) => <Story />],
  render: () => <EnDialogo />,
}
