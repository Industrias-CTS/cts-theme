/**
 * Contexto de notificaciones de `NotificationHost`.
 *
 * API de cts-manager (`stores/snackbarStore.ts`): un solo aviso a la vez,
 * con acción opcional («Deshacer»), persistente para operaciones largas y
 * con barra de avance. Sin Zustand: contexto de React.
 */
import { createContext, useContext } from 'react'

export type NotifySeverity = 'success' | 'error' | 'info' | 'warning'

export interface NotifyAction {
  label: string
  onClick: () => void
}

export interface NotifyOptions {
  /** Por defecto `'success'`. */
  severity?: NotifySeverity
  /** Con acción el aviso dura `notify.autoHideWithAction` (7 s) en lugar de 4 s. */
  action?: NotifyAction
  /** No se cierra solo ni con clic fuera; lo cierra quien lo abrió o la X. */
  persistent?: boolean
  /** 0-100: barra de avance y rueda en lugar del icono. */
  progress?: number | null
}

export interface NotificationContextValue {
  /** Muestra un aviso; reemplaza al que hubiera. Llamarlo de nuevo actualiza el avance. */
  notify: (message: string, options?: NotifyOptions) => void
  dismiss: () => void
}

export const NotificationContext = createContext<NotificationContextValue | null>(null)

/** Lee el contexto. Fuera de `NotificationHost` lanza un error. */
export function useNotify(): NotificationContextValue {
  const ctx = useContext(NotificationContext)
  if (!ctx) throw new Error('useNotify debe usarse dentro de <NotificationHost>.')
  return ctx
}
