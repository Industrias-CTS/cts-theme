import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button, Typography } from '@mui/material'
import InboxOutlined from '@mui/icons-material/InboxOutlined'
import { QueryState } from '../../src/views'

/**
 * Estados de una consulta: **cargando**, **error** con reintento y **vacío**
 * con acción. Si no aplica ninguno, pinta `children`. Úsalo en toda lista,
 * tabla o panel que dependa de datos remotos.
 */
const meta = {
  title: 'Componentes CTS/QueryState',
  component: QueryState,
  tags: ['autodocs'],
  args: {
    loading: false,
    error: null,
    isEmpty: false,
    emptyTitle: 'Sin proyectos todavía',
    emptyDescription: 'Crea el primero para empezar a diseñar tableros.',
    emptyIcon: <InboxOutlined />,
    emptyAction: <Button variant="contained">Crear proyecto</Button>,
    onRetry: () => undefined,
    children: <Typography>Contenido cargado: aquí iría la tabla.</Typography>,
  },
  argTypes: {
    emptyIcon: { control: false },
    emptyAction: { control: false },
    children: { control: false },
    onRetry: { control: false },
  },
} satisfies Meta<typeof QueryState>
export default meta
type Story = StoryObj<typeof meta>

export const Contenido: Story = {}
export const Cargando: Story = { args: { loading: true } }
export const ConError: Story = { name: 'Error', args: { error: 'No se pudo cargar la lista de proyectos.' } }
export const Vacio: Story = { name: 'Vacío', args: { isEmpty: true } }
