import type { Meta, StoryObj } from '@storybook/react-vite'
import { Box, Typography, useTheme } from '@mui/material'
import type { TypographyVariant } from '@mui/material/styles'
import { brandFontFamily, fontFamily, fontSize, fontWeight, letterSpacing } from '../../src/index'
import { Code, Page, RefTable, Section } from '../ui'

const meta = { title: 'Fundamentos/Tipografía' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const VARIANTS: { v: TypographyVariant; uso: string }[] = [
  { v: 'h1', uso: 'muy raro; pantallas de marca' },
  { v: 'h2', uso: 'muy raro' },
  { v: 'h3', uso: 'cifras grandes de dashboard' },
  { v: 'h4', uso: 'título de página' },
  { v: 'h5', uso: 'título de sección' },
  { v: 'h6', uso: 'título de tarjeta y de diálogo' },
  { v: 'subtitle1', uso: 'subtítulo, título de estado vacío' },
  { v: 'subtitle2', uso: 'etiqueta destacada' },
  { v: 'body1', uso: 'texto corrido' },
  { v: 'body2', uso: 'tablas, formularios densos, texto de apoyo' },
  { v: 'caption', uso: 'metadatos, ayudas' },
  { v: 'overline', uso: 'títulos de grupo' },
  { v: 'button', uso: 'botones (lo aplica Button)' },
]

const Escala = () => {
  const t = useTheme()
  return (
    <RefTable
      head={['Variante', 'Muestra', 'Tamaño · peso · interlínea', 'Uso']}
      rows={VARIANTS.map(({ v, uso }) => {
        const s = t.typography[v] as { fontSize?: string | number; fontWeight?: string | number; lineHeight?: string | number }
        return [
          <Code>{v}</Code>,
          <Typography variant={v}>Tablero principal 480 V</Typography>,
          <Code>{`${s.fontSize} · ${s.fontWeight} · ${s.lineHeight ?? '—'}`}</Code>,
          uso,
        ]
      })}
    />
  )
}

export const Escala_: Story = {
  name: 'Escala',
  render: () => (
    <Page
      title="Tipografía"
      intro="Titillium Web en toda la interfaz, títulos incluidos. Pesos 300, 400, 600 y 700 (900 solo para el wordmark). Sin 500 ni 800: el lint los rechaza."
    >
      <Section title="Variantes de Typography">
        <Escala />
      </Section>
      <Section title="Familias">
        <RefTable
          head={['Token', 'Muestra', 'Uso']}
          rows={[
            [<Code>fontFamily</Code>, <Box sx={{ fontFamily, fontSize: 20 }}>Industrias CTS 0123456789</Box>, 'toda la interfaz'],
            [
              <Code>brandFontFamily</Code>,
              <Box sx={{ fontFamily: brandFontFamily, fontSize: 20, fontWeight: 700 }}>INDUSTRIAS CTS</Box>,
              'solo marca: wordmark, login, barras de marca (Conthrax; si no está cargada se ve Titillium)',
            ],
          ]}
        />
      </Section>
      <Section title="Pesos · fontWeight">
        <RefTable
          head={['Token', 'Valor', 'Muestra']}
          rows={Object.entries(fontWeight).map(([k, w]) => [
            <Code>{k}</Code>,
            w,
            <Box sx={{ fontWeight: w, fontSize: 18 }}>Tablero de distribución</Box>,
          ])}
        />
      </Section>
      <Section title="Tamaños con nombre · fontSize" note="Para casos que no son una variante (rail, chips, cabecera de tabla). Los fraccionales son intencionales.">
        <RefTable
          head={['Token', 'px', 'Muestra']}
          rows={Object.entries(fontSize).map(([k, s]) => [<Code>{k}</Code>, s, <Box sx={{ fontSize: s }}>Breaker principal</Box>])}
        />
      </Section>
      <Section title="Tracking · letterSpacing">
        <RefTable
          head={['Token', 'Valor']}
          rows={Object.entries(letterSpacing).map(([k, v]) => [<Code>{k}</Code>, v])}
        />
      </Section>
    </Page>
  ),
}
