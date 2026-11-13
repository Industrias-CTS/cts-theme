/**
 * `QueryState` — estados de carga, error y vacío de una consulta.
 *
 * Unifica `molecules/QueryState.tsx` de E-Panel (rueda de 28, «Reintentar»,
 * icono de vacío 47) con `ui/EmptyState.tsx` de cts-manager (título,
 * descripción y acción). Si no hay carga, error ni vacío, pinta `children`.
 *
 * ```tsx
 * <QueryState loading={isLoading} error={error?.message} onRetry={refetch}
 *   isEmpty={rows.length === 0} emptyTitle="Sin proyectos"
 *   emptyAction={<Button onClick={crear}>Crear proyecto</Button>}>
 *   <Tabla rows={rows} />
 * </QueryState>
 * ```
 */
import type { JSX, ReactNode } from 'react'
import { Box, Button, CircularProgress, Typography } from '@mui/material'
import '../mui/augmentation'

export interface QueryStateProps {
  loading?: boolean
  /** Mensaje de error ya traducido; si existe, se muestra en lugar del contenido. */
  error?: string | null
  /** Si existe, aparece el botón de reintento. */
  onRetry?: () => void
  /** Texto del botón de reintento. Por defecto `'Reintentar'`. */
  retryLabel?: string
  isEmpty?: boolean
  /** Icono del estado vacío (p. ej. `<InboxOutlined />`); toma tamaño y color del sistema. */
  emptyIcon?: ReactNode
  emptyTitle?: string
  emptyDescription?: string
  /** Acción del estado vacío, normalmente un `Button` contained. */
  emptyAction?: ReactNode
  /** Etiqueta accesible del indicador de carga. Por defecto `'Cargando'`. */
  loadingLabel?: string
  children?: ReactNode
}

const centerSx = { textAlign: 'center', py: 8, px: 3 } as const

export function QueryState({
  loading = false,
  error,
  onRetry,
  retryLabel = 'Reintentar',
  isEmpty = false,
  emptyIcon,
  emptyTitle,
  emptyDescription,
  emptyAction,
  loadingLabel = 'Cargando',
  children,
}: QueryStateProps): JSX.Element {
  if (loading) {
    return (
      <Box sx={centerSx} role="status" aria-live="polite">
        <CircularProgress size={28} aria-label={loadingLabel} />
      </Box>
    )
  }
  if (error) {
    return (
      <Box sx={centerSx} role="alert">
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
          {error}
        </Typography>
        {onRetry && (
          <Button size="small" onClick={onRetry}>
            {retryLabel}
          </Button>
        )}
      </Box>
    )
  }
  if (isEmpty) {
    return (
      <Box sx={centerSx}>
        {emptyIcon && (
          <Box
            aria-hidden
            sx={{ color: 'text.disabled', mb: 1, lineHeight: 0, '& .MuiSvgIcon-root': { fontSize: 47 } }}
          >
            {emptyIcon}
          </Box>
        )}
        {emptyTitle && (
          <Typography variant="subtitle1" sx={{ color: 'text.secondary' }}>
            {emptyTitle}
          </Typography>
        )}
        {emptyDescription && (
          <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
            {emptyDescription}
          </Typography>
        )}
        {emptyAction && <Box sx={{ mt: 2 }}>{emptyAction}</Box>}
      </Box>
    )
  }
  return <>{children}</>
}
