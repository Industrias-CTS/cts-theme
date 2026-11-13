/**
 * Piezas del catálogo (no se publican en el paquete). Todo color y medida
 * sale del tema o de `src/`: el catálogo no puede desfasarse del código.
 */
import type { ReactNode } from 'react'
import { Box, Stack, Typography } from '@mui/material'

/** Contraste WCAG entre dos hex `#rrggbb`; `null` si alguno no es hex. */
export const contrast = (fg: string, bg: string): number | null => {
  const lum = (hex: string) => {
    const m = /^#([0-9a-f]{6})$/i.exec(hex)
    if (!m || !m[1]) return null
    const [r, g, b] = [0, 2, 4].map((i) => parseInt(m[1]!.slice(i, i + 2), 16) / 255).map((v) =>
      v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4,
    ) as [number, number, number]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
  }
  const a = lum(fg)
  const b = lum(bg)
  if (a === null || b === null) return null
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)
}

export function Page({ title, intro, children }: { title: string; intro?: ReactNode; children: ReactNode }) {
  return (
    <Box sx={{ maxWidth: 1180, mx: 'auto' }}>
      <Typography variant="h4" component="h1" sx={{ mb: 1 }}>
        {title}
      </Typography>
      {intro && (
        <Typography variant="body1" sx={{ color: 'text.secondary', mb: 4, maxWidth: 760 }}>
          {intro}
        </Typography>
      )}
      <Stack spacing={5}>{children}</Stack>
    </Box>
  )
}

export function Section({ title, note, children }: { title: string; note?: ReactNode; children: ReactNode }) {
  return (
    <Box component="section">
      <Typography variant="overline" component="h2" sx={{ color: 'text.secondary', display: 'block' }}>
        {title}
      </Typography>
      {note && (
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1.5, maxWidth: 760 }}>
          {note}
        </Typography>
      )}
      <Box sx={{ mt: note ? 0 : 1.5 }}>{children}</Box>
    </Box>
  )
}

/** Rejilla CSS (no `Grid` de MUI, prohibido en el sistema). */
export function Tiles({ min = 180, children }: { min?: number; children: ReactNode }) {
  return (
    <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: `repeat(auto-fill, minmax(${min}px, 1fr))` }}>
      {children}
    </Box>
  )
}

/** Muestra de color: bloque, nombre, ruta del token y valor literal. */
export function Swatch({
  name,
  token,
  value,
  on,
}: {
  name: string
  token: string
  value: string
  /** Fondo contra el que se mide el contraste. */
  on?: string
}) {
  const ratio = on ? contrast(value, on) : null
  return (
    <Box
      sx={(t) => ({
        border: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
        borderRadius: `${t.cts.radii.card}px`,
        overflow: 'hidden',
        bgcolor: 'background.paper',
      })}
    >
      <Box sx={{ height: 72, background: value }} />
      <Box sx={{ p: 1.5 }}>
        <Typography variant="subtitle2">{name}</Typography>
        <Code>{token}</Code>
        <Typography variant="caption" component="div" sx={{ color: 'text.secondary', mt: 0.5 }}>
          {value}
          {ratio !== null && ` · ${ratio.toFixed(2)}:1`}
        </Typography>
      </Box>
    </Box>
  )
}

export function Code({ children }: { children: ReactNode }) {
  return (
    <Box
      component="code"
      sx={(t) => ({
        fontFamily: 'monospace',
        fontSize: t.cts.fontSize.caption,
        color: 'text.secondary',
        wordBreak: 'break-all',
      })}
    >
      {children}
    </Box>
  )
}

/** Tabla simple de referencia: filas de celdas ya formateadas. */
export function RefTable({ head, rows }: { head: string[]; rows: ReactNode[][] }) {
  return (
    <Box
      component="table"
      sx={(t) => ({
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: t.cts.fontSize.dense,
        '& th': {
          textAlign: 'left',
          fontWeight: t.cts.fontWeight.semibold,
          color: 'text.secondary',
          fontSize: t.cts.fontSize.overline,
          letterSpacing: t.cts.letterSpacing.overline,
          textTransform: 'uppercase',
          py: 1,
          px: 1.5,
          borderBottom: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
        },
        '& td': {
          py: 1,
          px: 1.5,
          borderBottom: `${t.cts.borders.hairline}px solid ${t.palette.divider}`,
          verticalAlign: 'middle',
        },
      })}
    >
      <thead>
        <tr>
          {head.map((h) => (
            <th key={h}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>
            {r.map((c, j) => (
              <td key={j}>{c}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </Box>
  )
}
