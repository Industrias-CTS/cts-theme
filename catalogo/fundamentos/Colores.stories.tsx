import type { Meta, StoryObj } from '@storybook/react-vite'
import { Box, Chip, Stack, Typography } from '@mui/material'
import {
  action,
  actionDark,
  brandSurface,
  chrome,
  chromeDark,
  data8,
  palette,
  secondary,
  semantic,
  semanticDark,
  status,
  statusDark,
  surface,
  surfaceDark,
} from '../../src/index'
import type { StatusName } from '../../src/index'
import { Code, Page, RefTable, Section, Swatch, Tiles } from '../ui'

const meta = {
  title: 'Fundamentos/Colores',
  parameters: { layout: 'padded' },
} satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

/** Fila de muestras de un objeto de colores, con contraste contra `on`. */
const Group = ({ obj, path, on }: { obj: Record<string, string>; path: string; on?: string }) => (
  <Tiles>
    {Object.entries(obj).map(([k, v]) => (
      <Swatch key={k} name={k} token={`${path}.${k}`} value={v} on={on} />
    ))}
  </Tiles>
)

export const Marca: Story = {
  render: () => (
    <Page
      title="Marca"
      intro="Azul CTS y grises corporativos. El chrome de las apps (rail, botones, enlaces) es azul + gris; el resto de colores tiene significado."
    >
      <Section title="Primitivos de marca · palette">
        <Group obj={palette} path="palette" on={surface.paper} />
      </Section>
      <Section title="Secundario · secondary">
        <Group obj={secondary} path="secondary" on={surface.paper} />
      </Section>
      <Section title="Superficie de marca · brandSurface" note="Rail, barras de marca, panel del login y cabecera de tabla. Su contenido usa blancos con alfa (theme.cts.rail).">
        <Tiles>
          <Swatch name="claro" token="brandSurface.light" value={brandSurface.light} on={brandSurface.text} />
          <Swatch name="oscuro" token="brandSurface.dark" value={brandSurface.dark} on={brandSurface.text} />
        </Tiles>
      </Section>
    </Page>
  ),
}

export const Superficies: Story = {
  render: () => (
    <Page title="Superficies y texto" intro="Fondos, papel, texto y bordes por modo. En oscuro el papel es más claro que el fondo. El contraste se mide contra el fondo de la página.">
      <Section title="Modo claro · surface">
        <Group obj={surface} path="surface" on={surface.soft} />
      </Section>
      <Section title="Modo oscuro · surfaceDark">
        <Group obj={surfaceDark} path="surfaceDark" on={surfaceDark.base} />
      </Section>
    </Page>
  ),
}

export const Semanticos: Story = {
  name: 'Semánticos',
  render: () => (
    <Page title="Semánticos" intro="Error, advertencia, éxito e información. Solo para significado, nunca decoración. Cada modo tiene su propio juego.">
      <Section title="Claro · semantic">
        <Group obj={semantic} path="semantic" on={surface.paper} />
      </Section>
      <Section title="Oscuro · semanticDark">
        <Group obj={semanticDark} path="semanticDark" on={surfaceDark.paper} />
      </Section>
      <Section title="Guardar · chrome.save" note="El verde de éxito no alcanza contraste sobre blanco para un botón; Guardar usa su propio verde.">
        <Tiles>
          <Swatch name="claro" token="chrome.save" value={chrome.save} on={surface.paper} />
          <Swatch name="oscuro" token="chromeDark.save" value={chromeDark.save} on={surfaceDark.paper} />
        </Tiles>
      </Section>
    </Page>
  ),
}

const STATUS_LABEL: Record<StatusName, string> = {
  ok: 'En marcha',
  warning: 'En proceso',
  fault: 'Falla',
  offline: 'Fuera de línea',
  info: 'Información',
  selected: 'Seleccionado',
}

/** Indicador de equipo: punto + texto. Nunca solo color. */
const StatusRow = ({ dark }: { dark: boolean }) => (
  <Stack
    direction="row"
    spacing={1}
    useFlexGap
    sx={(t) => ({
      flexWrap: 'wrap',
      p: 2,
      borderRadius: `${t.cts.radii.card}px`,
      bgcolor: dark ? surfaceDark.base : surface.soft,
    })}
  >
    {(Object.keys(status) as StatusName[]).map((k) => {
      const c = (dark ? statusDark : status)[k]
      return (
        <Chip
          key={k}
          label={STATUS_LABEL[k]}
          icon={<Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: c, ml: '8px !important' }} />}
          variant="outlined"
          sx={{ borderColor: c, color: dark ? surfaceDark.text : surface.navy }}
        />
      )
    })}
  </Stack>
)

export const Estados: Story = {
  render: () => (
    <Page
      title="Estados de equipo y proceso"
      intro="Un solo vocabulario para HMI, alarmas, tableros y símbolos eléctricos. Antes había 7 verdes distintos para «OK». Siempre acompañados de texto o icono: en claro, ok, warning e info no llegan a 3:1 sobre el fondo (ver la cifra de cada muestra)."
    >
      <Section title="Indicadores">
        <Stack spacing={1.5}>
          <StatusRow dark={false} />
          <StatusRow dark />
        </Stack>
      </Section>
      <Section title="Claro · status">
        <Group obj={status} path="status" on={surface.soft} />
      </Section>
      <Section title="Oscuro · statusDark">
        <Group obj={statusDark} path="statusDark" on={surfaceDark.paper} />
      </Section>
      <Section title="Equivalencias">
        <RefTable
          head={['Rol', 'Úsalo para', 'CSS']}
          rows={[
            ['ok', 'en marcha · energizado · cerrado · aprobado · normal', <Code>--cts-status-ok</Code>],
            ['warning', 'en proceso · reconocido · bloqueado', <Code>--cts-status-warning</Code>],
            ['fault', 'falla · disparado · alarma activa', <Code>--cts-status-fault</Code>],
            ['offline', 'fuera de línea · inactivo · abierto · sin datos', <Code>--cts-status-offline</Code>],
            ['info', 'informativo', <Code>--cts-status-info</Code>],
            ['selected', 'selección en lienzos y editores', <Code>--cts-status-selected</Code>],
          ]}
        />
      </Section>
    </Page>
  ),
}

export const Datos: Story = {
  render: () => (
    <Page title="Paleta de datos · data8" intro="Ocho colores para datos del usuario: series de gráficos, grupos, etiquetas. El orden es significativo; dataColor(i) los recorre en ciclo.">
      <Tiles min={120}>
        {data8.map((c, i) => (
          <Swatch key={c} name={`${i + 1}`} token={`dataColor(${i})`} value={c} />
        ))}
      </Tiles>
      <Section title="Ejemplo">
        <Stack direction="row" spacing={1} sx={{ alignItems: 'flex-end', height: 140 }}>
          {data8.map((c, i) => (
            <Box key={c} sx={(t) => ({ width: 40, height: 40 + i * 12, bgcolor: c, borderRadius: `${t.cts.radii.chip}px ${t.cts.radii.chip}px 0 0` })} />
          ))}
        </Stack>
      </Section>
    </Page>
  ),
}

export const Interfaz: Story = {
  name: 'Chrome e interacción',
  render: () => (
    <Page title="Chrome e interacción" intro="Colores de piezas de interfaz que no son texto ni superficie. Los usan los overrides de componentes; una app rara vez los necesita directamente.">
      <Section title="Claro · chrome">
        <Group obj={chrome} path="chrome" />
      </Section>
      <Section title="Oscuro · chromeDark">
        <Group obj={chromeDark} path="chromeDark" />
      </Section>
      <Section title="Hover y selección · action / actionDark">
        <Tiles>
          {Object.entries(action).map(([k, v]) => (
            <Swatch key={k} name={`claro · ${k}`} token={`action.${k}`} value={v} />
          ))}
          {Object.entries(actionDark).map(([k, v]) => (
            <Swatch key={k} name={`oscuro · ${k}`} token={`actionDark.${k}`} value={v} />
          ))}
        </Tiles>
      </Section>
      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
        Los alfas se ven sobre el papel del tema activo; cambia el tema en la barra superior.
      </Typography>
    </Page>
  ),
}
