import type { Meta, StoryObj } from '@storybook/react-vite'
import type { ReactNode } from 'react'
import { Box, Stack, Typography } from '@mui/material'
import type { SxProps, Theme } from '@mui/material'
import { borders, density, elevation, layout, radii, shadows, spacing, touch } from '../../src/index'
import { Code, Page, RefTable, Section, Tiles } from '../ui'

const meta = { title: 'Fundamentos/Forma y espacio' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const Card = ({ children, sx }: { children: ReactNode; sx?: SxProps<Theme> }) => (
  <Box
    sx={[
      (t) => ({
        p: 2,
        minHeight: 96,
        bgcolor: 'background.paper',
        border: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-end',
      }),
      ...(Array.isArray(sx) ? sx : [sx]),
    ]}
  >
    {children}
  </Box>
)

export const Radios: Story = {
  render: () => (
    <Page title="Radios" intro="Crecen con la elevación: chip 6 → control 8 → base 10 → card 12 → diálogo 14. shape.borderRadius del tema es 10.">
      <Tiles min={150}>
        {Object.entries(radii).map(([k, r]) => (
          <Card key={k} sx={{ borderRadius: `${r}px` }}>
            <Typography variant="subtitle2">{k}</Typography>
            <Code>{`radii.${k} · ${r}px`}</Code>
          </Card>
        ))}
      </Tiles>
    </Page>
  ),
}

export const Sombras: Story = {
  render: () => (
    <Page title="Sombras" intro="Los bordes estructuran; las sombras se reservan para capas flotantes. Las cards son planas.">
      <Section title="Con nombre · shadows">
        <Tiles min={200}>
          {Object.entries(shadows).map(([k, s]) => (
            <Card key={k} sx={(t) => ({ borderRadius: `${t.cts.radii.card}px`, boxShadow: s, border: 'none' })}>
              <Typography variant="subtitle2">{k}</Typography>
              <Code>{s}</Code>
            </Card>
          ))}
        </Tiles>
      </Section>
      <Section title="Escala theme.shadows 1–5 (modo activo)" note="Elevación de MUI. Del 6 al 24 se repite el nivel superior.">
        <Tiles min={160}>
          {elevation.light.map((_, i) => (
            <Card key={i} sx={(t) => ({ borderRadius: `${t.cts.radii.card}px`, boxShadow: t.shadows[i + 1], border: 'none' })}>
              <Typography variant="subtitle2">{`shadows[${i + 1}]`}</Typography>
            </Card>
          ))}
        </Tiles>
      </Section>
    </Page>
  ),
}

export const Bordes: Story = {
  render: () => (
    <Page title="Bordes">
      <Tiles min={170}>
        {Object.entries(borders).map(([k, w]) => (
          <Box key={k} sx={(t) => ({ p: 2, borderRadius: `${t.cts.radii.base}px`, border: `${w}px solid ${t.palette.primary.main}` })}>
            <Typography variant="subtitle2">{k}</Typography>
            <Code>{`borders.${k} · ${w}px`}</Code>
          </Box>
        ))}
      </Tiles>
    </Page>
  ),
}

export const Espaciado: Story = {
  render: () => (
    <Page title="Espaciado y densidad" intro={`Base ${spacing.base} px: en sx, p: 1 = 8 px. Se permiten medios pasos (0.5, 1.5). Gutter de página ${spacing.gutter} px (${spacing.gutterCompact} bajo sm).`}>
      <Section title="Escala de espaciado">
        <Stack spacing={1}>
          {[0.5, 1, 1.5, 2, 3, 4, 6].map((n) => (
            <Stack key={n} direction="row" spacing={2} sx={{ alignItems: 'center' }}>
              <Box sx={{ width: 64 }}>
                <Code>{`${n} · ${n * spacing.base}px`}</Code>
              </Box>
              <Box sx={{ height: 12, width: n * spacing.base, bgcolor: 'primary.main', borderRadius: 1 }} />
            </Stack>
          ))}
        </Stack>
      </Section>
      <Section title="Densidad · density (alturas)" note={`Densidad de hoja de cálculo. En el perfil HMI los controles y filas suben a ${touch.minTarget} px.`}>
        <RefTable
          head={['Token', 'px', 'Muestra']}
          rows={Object.entries(density).map(([k, h]) => [
            <Code>{k}</Code>,
            h,
            <Box sx={(t) => ({ height: h, width: 160, bgcolor: 'action.selected', borderRadius: `${t.cts.radii.control}px` })} />,
          ])}
        />
      </Section>
      <Section title="Layout · layout">
        <RefTable head={['Token', 'Valor']} rows={Object.entries(layout).map(([k, v]) => [<Code>{k}</Code>, v])} />
      </Section>
    </Page>
  ),
}
