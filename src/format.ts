/**
 * Formato de fechas y números del Sistema de Diseño CTS.
 *
 * Un solo locale para todas las apps: `es-CO` (decisión G12). Reemplaza las
 * llamadas sueltas a `toLocaleString` con `'es-ES'`, `'es-CO'` o sin locale
 * que conviven hoy en E-Panel, cts-manager y t-monitor.
 *
 * Sin dependencias: usa `Intl`. Los formateadores se cachean por opciones.
 * La zona horaria es la del dispositivo salvo que se pase `timeZone`.
 */

export const LOCALE = 'es-CO'

/** Moneda por defecto de `formatCurrency`. */
export const CURRENCY = 'COP'

export type DateInput = Date | number | string

const cache = new Map<string, Intl.DateTimeFormat | Intl.NumberFormat>()

const dateFormat = (options: Intl.DateTimeFormatOptions): Intl.DateTimeFormat => {
  const key = `d${JSON.stringify(options)}`
  let f = cache.get(key) as Intl.DateTimeFormat | undefined
  if (!f) {
    f = new Intl.DateTimeFormat(LOCALE, options)
    cache.set(key, f)
  }
  return f
}

const numberFormat = (options: Intl.NumberFormatOptions): Intl.NumberFormat => {
  const key = `n${JSON.stringify(options)}`
  let f = cache.get(key) as Intl.NumberFormat | undefined
  if (!f) {
    f = new Intl.NumberFormat(LOCALE, options)
    cache.set(key, f)
  }
  return f
}

/**
 * Convierte la entrada en `Date`. Una cadena `YYYY-MM-DD` sin hora se lee
 * como fecha local (no UTC), para que no salga el día anterior en Colombia.
 */
export const toDate = (value: DateInput): Date => {
  if (value instanceof Date) return value
  if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)) {
    const [y, m, d] = value.split('-').map(Number) as [number, number, number]
    return new Date(y, m - 1, d)
  }
  return new Date(value)
}

const valid = (d: Date) => !Number.isNaN(d.getTime())

/** Texto para fechas inválidas o vacías. */
export const EMPTY = '—'

export type DateStyle = 'short' | 'medium' | 'long'

const DATE_STYLES: Record<DateStyle, Intl.DateTimeFormatOptions> = {
  /** 13/11/2026 */
  short: { day: '2-digit', month: '2-digit', year: 'numeric' },
  /** 13 de nov de 2026 — reemplaza el `D MMM YYYY` de dayjs en cts-manager */
  medium: { day: 'numeric', month: 'short', year: 'numeric' },
  /** 13 de noviembre de 2026 */
  long: { day: 'numeric', month: 'long', year: 'numeric' },
}

export interface FormatDateOptions {
  style?: DateStyle
  timeZone?: string
}

/** Fecha sin hora. Por defecto `medium`: «13 de nov de 2026». */
export const formatDate = (value: DateInput | null | undefined, opts: FormatDateOptions = {}): string => {
  if (value === null || value === undefined || value === '') return EMPTY
  const d = toDate(value)
  if (!valid(d)) return EMPTY
  return dateFormat({ ...DATE_STYLES[opts.style ?? 'medium'], timeZone: opts.timeZone }).format(d)
}

/** Hora en 24 h: «14:05» o, con `seconds`, «14:05:09». */
export const formatTime = (
  value: DateInput | null | undefined,
  opts: { seconds?: boolean; timeZone?: string } = {},
): string => {
  if (value === null || value === undefined || value === '') return EMPTY
  const d = toDate(value)
  if (!valid(d)) return EMPTY
  return dateFormat({
    hour: '2-digit',
    minute: '2-digit',
    ...(opts.seconds ? { second: '2-digit' } : {}),
    hourCycle: 'h23',
    timeZone: opts.timeZone,
  }).format(d)
}

/** Fecha y hora: «13 de nov de 2026, 14:05». */
export const formatDateTime = (
  value: DateInput | null | undefined,
  opts: FormatDateOptions & { seconds?: boolean } = {},
): string => {
  if (value === null || value === undefined || value === '') return EMPTY
  const d = toDate(value)
  if (!valid(d)) return EMPTY
  return `${formatDate(d, opts)}, ${formatTime(d, opts)}`
}

/** `YYYY-MM-DD` en hora local — para inputs `type="date"`, claves y archivos. */
export const formatDateISO = (value: DateInput): string => {
  const d = toDate(value)
  if (!valid(d)) return ''
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

/** Número con separadores de `es-CO`: «1.234.567,89». */
export const formatNumber = (
  value: number | null | undefined,
  opts: { decimals?: number; minDecimals?: number } = {},
): string => {
  if (value === null || value === undefined || Number.isNaN(value)) return EMPTY
  return numberFormat({
    maximumFractionDigits: opts.decimals ?? 2,
    minimumFractionDigits: opts.minDecimals ?? 0,
  }).format(value)
}

/** Moneda; por defecto pesos sin decimales: «$ 1.234.567». */
export const formatCurrency = (
  value: number | null | undefined,
  opts: { currency?: string; decimals?: number } = {},
): string => {
  if (value === null || value === undefined || Number.isNaN(value)) return EMPTY
  const currency = opts.currency ?? CURRENCY
  const decimals = opts.decimals ?? (currency === 'COP' ? 0 : 2)
  return numberFormat({
    style: 'currency',
    currency,
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  }).format(value)
}

/** Porcentaje a partir de una fracción: `0.125` → «12,5%». */
export const formatPercent = (value: number | null | undefined, opts: { decimals?: number } = {}): string => {
  if (value === null || value === undefined || Number.isNaN(value)) return EMPTY
  return numberFormat({ style: 'percent', maximumFractionDigits: opts.decimals ?? 1 }).format(value)
}

/** Magnitud con unidad SI: `formatUnit(230.44, 'V')` → «230,4 V». */
export const formatUnit = (value: number | null | undefined, unit: string, opts: { decimals?: number } = {}): string => {
  if (value === null || value === undefined || Number.isNaN(value)) return EMPTY
  return `${formatNumber(value, { decimals: opts.decimals ?? 1 })} ${unit}`
}
