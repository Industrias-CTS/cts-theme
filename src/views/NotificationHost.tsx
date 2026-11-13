/**
 * `NotificationHost` — avisos globales de la app (snackbar).
 *
 * Porta `ui/GlobalSnackbar.tsx` de cts-manager: abajo a la derecha, `Alert`
 * filled, 4 s (7 s con acción), ancho máximo 560 y salto de línea para
 * avisos largos. Se monta una vez, cerca de la raíz:
 *
 * ```tsx
 * <ThemeProvider theme={theme}>
 *   <NotificationHost>
 *     <App />
 *   </NotificationHost>
 * </ThemeProvider>
 *
 * const { notify } = useNotify()
 * notify('Proyecto guardado')
 * notify('Tablero movido', { action: { label: 'Deshacer', onClick: deshacer } })
 * ```
 */
import type { JSX, ReactNode } from 'react'
import { useCallback, useMemo, useState } from 'react'
import { Alert, Box, Button, CircularProgress, LinearProgress, Snackbar } from '@mui/material'
import '../mui/augmentation'
import { notify as notifyTokens } from '../tokens'
import { NotificationContext } from './NotificationContext'
import type { NotificationContextValue, NotifyAction, NotifyOptions, NotifySeverity } from './NotificationContext'

interface NotificationState {
  open: boolean
  message: string
  severity: NotifySeverity
  action: NotifyAction | null
  persistent: boolean
  progress: number | null
}

const CLOSED: NotificationState = {
  open: false,
  message: '',
  severity: 'success',
  action: null,
  persistent: false,
  progress: null,
}

export interface NotificationHostProps {
  children: ReactNode
}

export function NotificationHost({ children }: NotificationHostProps): JSX.Element {
  const [state, setState] = useState<NotificationState>(CLOSED)

  const notify = useCallback((message: string, options: NotifyOptions = {}) => {
    setState({
      open: true,
      message,
      severity: options.severity ?? 'success',
      action: options.action ?? null,
      persistent: !!options.persistent,
      progress: options.progress ?? null,
    })
  }, [])

  // Conserva el mensaje al cerrar para que no desaparezca durante la salida.
  const dismiss = useCallback(() => setState((s) => ({ ...s, open: false, action: null })), [])

  const value = useMemo<NotificationContextValue>(() => ({ notify, dismiss }), [notify, dismiss])
  const { open, message, severity, action, persistent, progress } = state

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <Snackbar
        open={open}
        autoHideDuration={persistent ? null : action ? notifyTokens.autoHideWithAction : notifyTokens.autoHide}
        onClose={(_e, reason) => {
          if (persistent && reason === 'clickaway') return
          dismiss()
        }}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        sx={(t) => ({
          zIndex: t.cts.zIndex.toast,
          maxWidth: { xs: 'calc(100vw - 16px)', sm: `min(${t.cts.notify.maxWidth}px, calc(100vw - 48px))` },
        })}
      >
        <Alert
          onClose={dismiss}
          severity={severity}
          variant="filled"
          icon={progress != null ? <CircularProgress size={18} thickness={5} sx={{ color: 'inherit' }} /> : undefined}
          action={
            action ? (
              <Button
                size="small"
                onClick={() => {
                  action.onClick()
                  dismiss()
                }}
                sx={{ fontWeight: 'fontWeightBold', color: 'inherit', textDecoration: 'underline' }}
              >
                {action.label}
              </Button>
            ) : undefined
          }
          sx={(t) => ({
            width: '100%',
            minWidth: 0,
            whiteSpace: 'normal',
            overflowWrap: 'anywhere',
            fontWeight: t.typography.fontWeightMedium,
            color: t.palette.mode === 'dark' ? t.palette.common.white : t.palette.text.primary,
            boxShadow: t.cts.shadows.toast,
          })}
        >
          {message}
          {progress != null && (
            <Box sx={{ mt: 0.75, minWidth: 220 }}>
              <LinearProgress
                variant="determinate"
                value={Math.max(0, Math.min(100, progress))}
                sx={(t) => ({
                  height: 4,
                  borderRadius: 2,
                  // blanco 0.35 sobre el color pleno del aviso (cts-manager usa 0.3)
                  bgcolor: t.cts.rail.avatarBorder,
                  '& .MuiLinearProgress-bar': { bgcolor: 'currentColor' },
                })}
              />
            </Box>
          )}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  )
}
