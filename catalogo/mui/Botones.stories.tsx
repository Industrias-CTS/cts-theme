import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button, IconButton, Stack, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material'
import AddRounded from '@mui/icons-material/AddRounded'
import DeleteOutlined from '@mui/icons-material/DeleteOutlined'
import SaveOutlined from '@mui/icons-material/SaveOutlined'
import { Page, Section } from '../ui'

/**
 * `Button` de MUI con el tema CTS: sin mayúsculas, peso 600, radio 8,
 * sombra azul en contained y borde 1.5 px en outlined. `size="small"` es el
 * tamaño habitual en tablas y barras de herramientas.
 */
const meta = {
  title: 'Componentes MUI/Botones',
  component: Button,
  tags: ['autodocs'],
  args: { children: 'Guardar cambios', variant: 'contained', color: 'primary', size: 'medium', disabled: false },
  argTypes: {
    variant: { control: 'inline-radio', options: ['contained', 'outlined', 'text'] },
    color: { control: 'select', options: ['primary', 'secondary', 'error', 'warning', 'success', 'info', 'inherit'] },
    size: { control: 'inline-radio', options: ['small', 'medium', 'large'] },
  },
} satisfies Meta<typeof Button>
export default meta
type Story = StoryObj<typeof meta>

/** Cambia variante, color y tamaño desde el panel de controles. */
export const Interactivo: Story = {}

export const Catalogo: Story = {
  name: 'Todas las variantes',
  parameters: { controls: { disable: true } },
  render: () => (
    <Page title="Botones" intro="Una acción principal por vista (contained primary). Secundarias en outlined; terciarias en text. Destructivas con color error.">
      {(['contained', 'outlined', 'text'] as const).map((variant) => (
        <Section key={variant} title={variant}>
          <Stack direction="row" spacing={1.5} useFlexGap sx={{ flexWrap: 'wrap', alignItems: 'center' }}>
            <Button variant={variant}>Primario</Button>
            <Button variant={variant} color="secondary">Secundario</Button>
            <Button variant={variant} color="error" startIcon={<DeleteOutlined />}>Eliminar</Button>
            <Button variant={variant} size="small">Pequeño</Button>
            <Button variant={variant} size="large">Grande</Button>
            <Button variant={variant} disabled>Deshabilitado</Button>
          </Stack>
        </Section>
      ))}
      <Section title="Con icono e icon button">
        <Stack direction="row" spacing={1.5} sx={{ alignItems: 'center' }}>
          <Button variant="contained" startIcon={<AddRounded />}>Nuevo proyecto</Button>
          <Button variant="outlined" startIcon={<SaveOutlined />}>Guardar</Button>
          <IconButton aria-label="Agregar"><AddRounded /></IconButton>
          <IconButton aria-label="Eliminar" color="error"><DeleteOutlined /></IconButton>
        </Stack>
      </Section>
      <Section title="Grupo de alternativas">
        <ToggleButtonGroup exclusive value="dia" size="small" aria-label="Periodo">
          <ToggleButton value="dia">Día</ToggleButton>
          <ToggleButton value="semana">Semana</ToggleButton>
          <ToggleButton value="mes">Mes</ToggleButton>
        </ToggleButtonGroup>
      </Section>
      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
        Elige «HMI oscuro» en la barra superior para ver los objetivos táctiles de 48 px.
      </Typography>
    </Page>
  ),
}
