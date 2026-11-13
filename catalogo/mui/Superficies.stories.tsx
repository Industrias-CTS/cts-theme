import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'
import {
  Alert,
  Avatar,
  Badge,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  LinearProgress,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  MenuList,
  Paper,
  Skeleton,
  Stack,
  Tab,
  Tabs,
  Tooltip,
  Typography,
} from '@mui/material'
import ContentCopy from '@mui/icons-material/ContentCopy'
import DeleteOutlined from '@mui/icons-material/DeleteOutlined'
import EditOutlined from '@mui/icons-material/EditOutlined'
import NotificationsOutlined from '@mui/icons-material/NotificationsOutlined'
import { Page, Section, Tiles } from '../ui'

const meta = { title: 'Componentes MUI/Superficies y avisos' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const Opciones = () => (
  <>
    <MenuItem>
      <ListItemIcon><EditOutlined fontSize="small" /></ListItemIcon>
      <ListItemText>Editar</ListItemText>
    </MenuItem>
    <MenuItem>
      <ListItemIcon><ContentCopy fontSize="small" /></ListItemIcon>
      <ListItemText>Duplicar</ListItemText>
    </MenuItem>
    <Divider />
    <MenuItem sx={{ color: 'error.main' }}>
      <ListItemIcon><DeleteOutlined fontSize="small" color="error" /></ListItemIcon>
      <ListItemText>Eliminar</ListItemText>
    </MenuItem>
  </>
)

const Capas = () => {
  const [dialogo, setDialogo] = useState(false)
  const [ancla, setAncla] = useState<HTMLElement | null>(null)
  return (
    <Stack direction="row" spacing={1.5} useFlexGap sx={{ flexWrap: 'wrap', alignItems: 'center' }}>
      <Button variant="contained" onClick={() => setDialogo(true)}>Abrir diálogo</Button>
      <Button variant="outlined" onClick={(e) => setAncla(e.currentTarget)}>Abrir menú</Button>
      <Tooltip title="Tooltip con flecha y posición fija">
        <Button>Pasa el cursor</Button>
      </Tooltip>
      <Dialog open={dialogo} onClose={() => setDialogo(false)} fullWidth maxWidth="sm">
        <DialogTitle>Eliminar tablero</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            Se eliminará TAB-003 y sus 24 circuitos. Esta acción no se puede deshacer.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogo(false)}>Cancelar</Button>
          <Button variant="contained" color="error" onClick={() => setDialogo(false)}>Eliminar</Button>
        </DialogActions>
      </Dialog>
      <Menu anchorEl={ancla} open={!!ancla} onClose={() => setAncla(null)}>
        <Opciones />
      </Menu>
    </Stack>
  )
}

export const Superficies: Story = {
  render: () => (
    <Page title="Superficies y avisos" intro="Cards planas con radio 12; diálogos con radio 14 y sombra azulada; menús con radio 10 y borde fino.">
      <Section title="Card y Paper">
        <Tiles min={260}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="overline" sx={{ color: 'text.secondary' }}>Proyecto</Typography>
              <Typography variant="h6">Subestación Norte</Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>12 tableros · 3 pendientes</Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Abrir</Button>
            </CardActions>
          </Card>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="subtitle2">Paper elevation=1</Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>Sombra suave para paneles flotantes.</Typography>
          </Paper>
          <Paper sx={{ width: 220 }}>
            <MenuList dense>
              <Opciones />
            </MenuList>
          </Paper>
        </Tiles>
      </Section>
      <Section title="Diálogo, menú y tooltip">
        <Capas />
      </Section>
      <Section title="Chips, insignias y pestañas">
        <Stack spacing={2}>
          <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
            <Chip label="Por defecto" />
            <Chip label="Primario" color="primary" />
            <Chip label="Éxito" color="success" />
            <Chip label="Advertencia" color="warning" />
            <Chip label="Error" color="error" />
            <Chip label="Outlined" variant="outlined" onDelete={() => undefined} />
            <Badge badgeContent={4} color="error">
              <NotificationsOutlined />
            </Badge>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>JT</Avatar>
          </Stack>
          <Tabs value={0} aria-label="Secciones">
            <Tab label="Resumen" />
            <Tab label="Circuitos" />
            <Tab label="Historial" />
          </Tabs>
        </Stack>
      </Section>
      <Section title="Alertas">
        <Stack spacing={1.5} sx={{ maxWidth: 640 }}>
          <Alert severity="success">Proyecto guardado.</Alert>
          <Alert severity="info">Hay una versión nueva del catálogo de equipos.</Alert>
          <Alert severity="warning">Dos circuitos superan el 80 % de carga.</Alert>
          <Alert severity="error">No se pudo conectar con el PLC.</Alert>
          <Alert severity="success" variant="filled">Filled: así se ven los avisos globales.</Alert>
        </Stack>
      </Section>
      <Section title="Progreso y carga">
        <Stack spacing={2} sx={{ maxWidth: 480 }}>
          <LinearProgress />
          <LinearProgress variant="determinate" value={65} />
          <Stack direction="row" spacing={2} sx={{ alignItems: 'center' }}>
            <CircularProgress size={28} />
            <Box sx={{ flex: 1 }}>
              <Skeleton width="60%" />
              <Skeleton />
              <Skeleton width="80%" />
            </Box>
          </Stack>
        </Stack>
      </Section>
    </Page>
  ),
}
