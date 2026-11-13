import type { Meta, StoryObj } from '@storybook/react-vite'
import {
  formatCurrency,
  formatDate,
  formatDateISO,
  formatDateTime,
  formatNumber,
  formatPercent,
  formatTime,
  formatUnit,
} from '../../src/index'
import { Code, Page, RefTable } from '../ui'

const meta = { title: 'Fundamentos/Formato' } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>

const ahora = new Date()

export const Formato: Story = {
  render: () => (
    <Page title="Formato es-CO" intro="Un solo locale para todas las apps. Importa desde @industriascts/cts-theme/format; nunca toLocaleString suelto. Vacío o inválido → «—».">
      <RefTable
        head={['Llamada', 'Resultado']}
        rows={[
          ['formatDate(fecha)', formatDate(ahora)],
          ["formatDate(fecha, { style: 'short' })", formatDate(ahora, { style: 'short' })],
          ["formatDate(fecha, { style: 'long' })", formatDate(ahora, { style: 'long' })],
          ['formatTime(fecha)', formatTime(ahora)],
          ['formatTime(fecha, { seconds: true })', formatTime(ahora, { seconds: true })],
          ['formatDateTime(fecha)', formatDateTime(ahora)],
          ['formatDateISO(fecha)', formatDateISO(ahora)],
          ["formatDate('2026-11-13')", formatDate('2026-11-13')],
          ['formatDate(null)', formatDate(null)],
          ['formatNumber(1234567.891)', formatNumber(1234567.891)],
          ['formatNumber(3, { minDecimals: 2 })', formatNumber(3, { minDecimals: 2 })],
          ['formatCurrency(1234567)', formatCurrency(1234567)],
          ["formatCurrency(12.5, { currency: 'USD' })", formatCurrency(12.5, { currency: 'USD' })],
          ['formatPercent(0.125)', formatPercent(0.125)],
          ["formatUnit(230.44, 'V')", formatUnit(230.44, 'V')],
          ["formatUnit(1250, 'kW', { decimals: 0 })", formatUnit(1250, 'kW', { decimals: 0 })],
        ].map(([c, r]) => [<Code>{c}</Code>, r])}
      />
    </Page>
  ),
}
