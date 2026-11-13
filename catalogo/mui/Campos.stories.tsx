import type { Meta, StoryObj } from '@storybook/react-vite'
import {
  Autocomplete,
  Checkbox,
  FormControlLabel,
  InputAdornment,
  MenuItem,
  Radio,
  RadioGroup,
  Slider,
  Stack,
  Switch,
  TextField,
} from '@mui/material'
import SearchRounded from '@mui/icons-material/SearchRounded'
import { Page, Section, Tiles } from '../ui'

const meta = { title: 'Componentes MUI/Campos' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const EQUIPOS = ['Breaker 3P 100 A', 'Contactor 40 A', 'Relé térmico', 'Variador 15 kW']

export const Campos: Story = {
  render: () => (
    <Page title="Campos de formulario" intro="Siempre outlined (por defecto en el tema): radio 8, borde 1.5 px, anillo de foco azul. size=&quot;small&quot; en formularios densos y barras de herramientas.">
      <Section title="Texto">
        <Tiles min={240}>
          <TextField label="Nombre del proyecto" defaultValue="Subestación Norte" />
          <TextField label="Pequeño" size="small" defaultValue="TAB-001" />
          <TextField label="Con ayuda" helperText="Máximo 40 caracteres" />
          <TextField label="Con error" error helperText="Campo obligatorio" />
          <TextField label="Deshabilitado" disabled defaultValue="Solo lectura" />
          <TextField
            placeholder="Buscar…"
            size="small"
            slotProps={{ input: { startAdornment: <InputAdornment position="start"><SearchRounded fontSize="small" /></InputAdornment> } }}
          />
        </Tiles>
      </Section>
      <Section title="Selección">
        <Tiles min={240}>
          <TextField select label="Tensión" defaultValue="480">
            {['120', '208', '240', '480'].map((v) => (
              <MenuItem key={v} value={v}>{`${v} V`}</MenuItem>
            ))}
          </TextField>
          <Autocomplete options={EQUIPOS} renderInput={(p) => <TextField {...p} label="Equipo" />} />
          <TextField label="Notas" multiline minRows={3} />
        </Tiles>
      </Section>
      <Section title="Casillas, interruptores y radios">
        <Stack direction="row" spacing={3} useFlexGap sx={{ flexWrap: 'wrap' }}>
          <Stack>
            <FormControlLabel control={<Checkbox defaultChecked />} label="Incluir neutro" />
            <FormControlLabel control={<Checkbox />} label="Incluir tierra" />
            <FormControlLabel control={<Checkbox disabled />} label="Deshabilitado" />
          </Stack>
          <Stack>
            <FormControlLabel control={<Switch defaultChecked />} label="Notificaciones" />
            <FormControlLabel control={<Switch />} label="Modo mantenimiento" />
          </Stack>
          <RadioGroup defaultValue="trifasico">
            <FormControlLabel value="monofasico" control={<Radio />} label="Monofásico" />
            <FormControlLabel value="trifasico" control={<Radio />} label="Trifásico" />
          </RadioGroup>
        </Stack>
      </Section>
      <Section title="Deslizador">
        <Slider defaultValue={60} valueLabelDisplay="auto" sx={{ maxWidth: 360 }} aria-label="Carga" />
      </Section>
    </Page>
  ),
}
