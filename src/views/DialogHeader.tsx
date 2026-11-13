/**
 * `DialogHeader` — cabecera estándar de diálogo: título, subtítulo, acciones
 * y botón de cierre.
 *
 * Porta `molecules/DialogHeader.tsx` de E-Panel (padding `px 3 · pt 3 ·
 * pb 2.5`, cierre a la derecha) leyendo colores del tema en lugar de la
 * paleta paralela `C`. Va dentro de `<Dialog>` en lugar de `<DialogTitle>`.
 *
 * ```tsx
 * <Dialog open={open} onClose={cerrar} fullWidth maxWidth="sm">
 *   <DialogHeader title="Nuevo proyecto" subtitle="Datos básicos" onClose={cerrar} />
 *   <DialogContent>…</DialogContent>
 * </Dialog>
 * ```
 */
import type { JSX, ReactNode } from 'react'
import { useId } from 'react'
import { Box, IconButton, SvgIcon, Typography } from '@mui/material'
import '../mui/augmentation'

export interface DialogHeaderProps {
  title?: string
  subtitle?: string
  /** Contenido propio a la izquierda; reemplaza `title` y `subtitle`. */
  left?: ReactNode
  /** Contenido antes del botón de cierre (pestañas, botones). */
  actions?: ReactNode
  /** Si falta, no hay botón de cierre. */
  onClose?: () => void
  /** `aria-label` del botón de cierre. Por defecto `'Cerrar'`. */
  closeLabel?: string
  /** `'center'` alinea al centro vertical (diálogos con pestañas). Por defecto `'start'`. */
  align?: 'start' | 'center'
  /**
   * `id` del título. Pásale el mismo valor a `aria-labelledby` del `Dialog`.
   * Si falta se genera uno interno.
   */
  titleId?: string
}

/** Icono «Close» de Material (Apache 2.0), sin depender de `@mui/icons-material`. */
const CLOSE_PATH = 'M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'

export function DialogHeader({
  title,
  subtitle,
  left,
  actions,
  onClose,
  closeLabel = 'Cerrar',
  align = 'start',
  titleId,
}: DialogHeaderProps): JSX.Element {
  const autoId = useId()
  const id = titleId ?? autoId
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: align === 'center' ? 'center' : 'flex-start',
        justifyContent: 'space-between',
        gap: 1.5,
        px: 3,
        pt: 3,
        pb: 2.5,
      }}
    >
      <Box sx={{ minWidth: 0 }}>
        {left ?? (
          <>
            {title && (
              <Typography id={id} variant="h6" component="h2" sx={{ fontWeight: 'fontWeightBold' }}>
                {title}
              </Typography>
            )}
            {subtitle && (
              <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
                {subtitle}
              </Typography>
            )}
          </>
        )}
      </Box>
      {(actions || onClose) && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexShrink: 0 }}>
          {actions}
          {onClose && (
            <IconButton size="small" onClick={onClose} aria-label={closeLabel} sx={{ color: 'text.secondary' }}>
              <SvgIcon sx={{ fontSize: 20 }}>
                <path d={CLOSE_PATH} />
              </SvgIcon>
            </IconButton>
          )}
        </Box>
      )}
    </Box>
  )
}
